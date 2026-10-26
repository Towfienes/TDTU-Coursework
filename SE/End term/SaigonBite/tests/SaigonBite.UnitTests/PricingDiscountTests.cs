using SaigonBite.Core.Payments;
using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR7 Quiet Kitchen discount and BR9 vouchers.
/// </summary>
/// <remarks>
/// BR7 partitions hub load at 29 % / 30 %: below 30 % earns 10 % of S, and exactly 30 % earns nothing.
/// BR9 has four independent conditions (active, inside validity dates, minimum subtotal reached, and the
/// cap) plus two voucher kinds, so each is partitioned separately.
/// </remarks>
public sealed class PricingDiscountTests
{
    [Fact]
    public void BR7_load_29_percent_gives_the_discount()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 29));

        Assert.Equal(20_000, result.QuietKitchenDiscount);   // 10 % of 200,000
        Assert.Equal(205_000, result.Total);
    }

    [Fact]
    public void BR7_load_30_percent_gives_no_discount()
    {
        // Exactly 30 % is the first load that earns nothing.
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 30));

        Assert.Equal(0, result.QuietKitchenDiscount);
        Assert.Equal(200_000, result.FoodTotal);
        Assert.Equal(225_000, result.Total);
    }

    [Fact]
    public void BR7_discount_is_ten_percent_of_the_subtotal()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 250_000, hubLoadPercent: 10));

        Assert.Equal(25_000, result.QuietKitchenDiscount);
        Assert.Equal(225_000, result.FoodTotal);
    }

    [Fact]
    public void BR7_discount_truncates_a_sub_dong_remainder()
    {
        // 10 % of 51,005 is 5,100.5; the platform grants the whole 5,100 and never credits more than 10 %.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 51_005));

        Assert.Equal(5_100, result.QuietKitchenDiscount);
        Assert.Equal(45_905, result.FoodTotal);
        Assert.Equal(71_000, result.Total);   // 45,905 + 25,000 = 70,905 → 71,000
    }

    [Fact]
    public void BR9_percent_voucher_applies_to_the_discounted_food_amount()
    {
        // 10 % of (200,000 − 20,000) = 18,000 — not 10 % of S, which would be 20,000.
        var result = PricingEngine.Calculate(
            Snapshot.With(voucher: Snapshot.Percent(percent: 10, maxDiscount: 30_000, minSubtotal: 100_000)));

        Assert.Equal(18_000, result.VoucherDiscount);
        Assert.Equal(162_000, result.FoodTotal);
        Assert.Equal(187_000, result.Total);   // 162,000 + 25,000
    }

    [Fact]
    public void BR9_percent_voucher_is_capped_at_the_maximum_discount()
    {
        // 10 % of (400,000 − 40,000) = 36,000, capped at 30,000.
        var result = PricingEngine.Calculate(Snapshot.With(
            subtotal: 400_000,
            voucher: Snapshot.Percent(percent: 10, maxDiscount: 30_000, minSubtotal: 100_000)));

        Assert.Equal(30_000, result.VoucherDiscount);
        Assert.Equal(330_000, result.FoodTotal);
        Assert.Equal(330_000, result.Total);   // S ≥ 300,000 also waives the delivery fee
    }

    [Fact]
    public void BR9_fixed_voucher_never_exceeds_the_discounted_food_amount()
    {
        // A 100,000 voucher against 54,000 of food discount is worth 54,000, so the food total is 0.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 60_000, voucher: Snapshot.Fixed(amount: 100_000)));

        Assert.Equal(54_000, result.VoucherDiscount);
        Assert.Equal(0, result.FoodTotal);
        Assert.Equal(25_000, result.Total);   // only the delivery fee remains
    }

    [Fact]
    public void BR9_fixed_voucher_below_the_food_amount_applies_in_full()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 200_000, voucher: Snapshot.Fixed(amount: 25_000)));

        Assert.Equal(25_000, result.VoucherDiscount);
        Assert.Equal(155_000, result.FoodTotal);
        Assert.Equal(180_000, result.Total);
    }

    [Fact]
    public void BR9_min_subtotal_is_checked_against_the_subtotal()
    {
        // S = 99,999 is one dong short of the voucher's 100,000 minimum, so the voucher is refused.
        var result = PricingEngine.Calculate(Snapshot.With(
            subtotal: 99_999,
            voucher: Snapshot.Percent(percent: 20, maxDiscount: 50_000, minSubtotal: 100_000)));

        Assert.Equal(0, result.VoucherDiscount);
        Assert.Equal(90_000, result.FoodTotal);      // 99,999 − 9,999 Quiet Kitchen
        Assert.Equal(115_000, result.Total);
        Assert.True(result.IsAccepted);              // BR9 refuses the voucher, not the order
    }

    [Fact]
    public void BR9_min_subtotal_boundary_100000_admits_the_voucher()
    {
        var result = PricingEngine.Calculate(Snapshot.With(
            subtotal: 100_000,
            voucher: Snapshot.Percent(percent: 20, maxDiscount: 50_000, minSubtotal: 100_000)));

        Assert.Equal(18_000, result.VoucherDiscount);   // 20 % of (100,000 − 10,000)
        Assert.Equal(72_000, result.FoodTotal);
        Assert.Equal(97_000, result.Total);
    }

    [Fact]
    public void BR9_inactive_voucher_is_refused()
    {
        var result = PricingEngine.Calculate(Snapshot.With(
            voucher: Snapshot.Percent(percent: 10, maxDiscount: 30_000, active: false)));

        Assert.Equal(0, result.VoucherDiscount);
        Assert.Equal(205_000, result.Total);
        Assert.True(result.IsAccepted);
    }

    [Fact]
    public void BR9_validity_is_inclusive_on_both_days()
    {
        // Valid from and to the placement date itself: both ends count.
        var placement = new DateTime(2026, 10, 20, 15, 0, 0, DateTimeKind.Unspecified);
        var voucher = Snapshot.Percent(
            percent: 10,
            maxDiscount: 30_000,
            validFrom: new DateOnly(2026, 10, 20),
            validTo: new DateOnly(2026, 10, 20));

        var result = PricingEngine.Calculate(Snapshot.With(placedAt: placement, voucher: voucher));

        Assert.Equal(18_000, result.VoucherDiscount);
    }

    [Fact]
    public void BR9_voucher_expired_the_day_before_is_refused()
    {
        var voucher = Snapshot.Percent(percent: 10, maxDiscount: 30_000, validTo: new DateOnly(2026, 10, 19));

        var result = PricingEngine.Calculate(Snapshot.With(voucher: voucher));

        Assert.Equal(0, result.VoucherDiscount);
    }

    [Fact]
    public void BR9_voucher_starting_the_day_after_is_refused()
    {
        var voucher = Snapshot.Percent(percent: 10, maxDiscount: 30_000, validFrom: new DateOnly(2026, 10, 21));

        var result = PricingEngine.Calculate(Snapshot.With(voucher: voucher));

        Assert.Equal(0, result.VoucherDiscount);
    }

    [Fact]
    public void BR9_voucher_kind_selects_the_formula()
    {
        // Same face value, different kinds: 10 percent of 180,000 is 18,000; a fixed 10,000 stays 10,000.
        var percent = PricingEngine.Calculate(Snapshot.With(voucher: Snapshot.Percent(10, 30_000)));
        var fixedAmount = PricingEngine.Calculate(Snapshot.With(voucher: Snapshot.Fixed(10_000)));

        Assert.Equal(18_000, percent.VoucherDiscount);
        Assert.Equal(10_000, fixedAmount.VoucherDiscount);
        Assert.Equal(VoucherType.Percent, Snapshot.Percent(10, 30_000).Type);
    }
}
