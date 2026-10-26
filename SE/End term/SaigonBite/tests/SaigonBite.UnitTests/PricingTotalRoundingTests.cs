using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR10 calculation order and BR11 single rounding — the specification's worked example plus the
/// boundary values 64,499 / 64,500 / 64,950.
/// </summary>
/// <remarks>
/// BR10 fixes nine steps and warns that "order matters; test it". The cases below are built so that
/// computing a later step on the wrong base, or rounding an intermediate value, changes the asserted
/// number.
/// </remarks>
public sealed class PricingTotalRoundingTests
{
    [Fact]
    public void BR10_worked_example_reproduces_the_specification()
    {
        // Section D: S = 200,000, load 20 %, 3.2 km, 15:00, rain off, no voucher.
        var result = PricingEngine.Calculate(Snapshot.With(
            subtotal: 200_000,
            hubLoadPercent: 20,
            distanceKm: 3.2m,
            placedAt: Snapshot.At(15, 0),
            rain: false));

        Assert.True(result.IsAccepted);
        Assert.Equal(200_000, result.Subtotal);              // 1
        Assert.Equal(20_000, result.QuietKitchenDiscount);   // 2
        Assert.Equal(0, result.VoucherDiscount);             // 3
        Assert.Equal(180_000, result.FoodTotal);             // 4
        Assert.Equal(25_000, result.DeliveryFee);            // 5
        Assert.Equal(0, result.RushSurcharge);               // 6
        Assert.Equal(0, result.RainSurcharge);               // 7
        Assert.Equal(205_000, result.FoodTotal + result.DeliveryFee + result.RushSurcharge + result.RainSurcharge); // 8
        Assert.Equal(205_000, result.Total);                 // 9
    }

    [Fact]
    public void BR10_voucher_is_taken_after_the_quiet_kitchen_discount()
    {
        // A 50 % voucher on the discounted food amount: 50 % of 180,000 = 90,000. Taking it from S
        // first would give 100,000 and a total of 105,000, so the number separates the two orders.
        var result = PricingEngine.Calculate(
            Snapshot.With(voucher: Snapshot.Percent(percent: 50, maxDiscount: 1_000_000)));

        Assert.Equal(90_000, result.VoucherDiscount);
        Assert.Equal(90_000, result.FoodTotal);
        Assert.Equal(115_000, result.Total);
    }

    [Fact]
    public void BR10_free_delivery_waiver_is_decided_by_the_subtotal_not_the_food_total()
    {
        // S = 300,000 waives D even though a 50 % voucher cuts the food total to 135,000.
        var result = PricingEngine.Calculate(Snapshot.With(
            subtotal: 300_000,
            voucher: Snapshot.Percent(percent: 50, maxDiscount: 1_000_000)));

        Assert.Equal(30_000, result.QuietKitchenDiscount);
        Assert.Equal(135_000, result.VoucherDiscount);
        Assert.Equal(135_000, result.FoodTotal);
        Assert.Equal(0, result.DeliveryFee);
        Assert.Equal(135_000, result.Total);
    }

    [Fact]
    public void BR11_64950_rounds_to_65000()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 55_500, distanceKm: 2.0m));

        Assert.Equal(5_550, result.QuietKitchenDiscount);
        Assert.Equal(49_950, result.FoodTotal);   // deliberately left un-rounded
        Assert.Equal(15_000, result.DeliveryFee);
        Assert.Equal(65_000, result.Total);       // 64,950 → 65,000
    }

    [Fact]
    public void BR11_64499_rounds_down_to_64000()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 54_998, distanceKm: 2.0m));

        Assert.Equal(5_499, result.QuietKitchenDiscount);   // 10 % of 54,998 is 5,499.8, truncated
        Assert.Equal(49_499, result.FoodTotal);
        Assert.Equal(64_000, result.Total);                 // 64,499 → 64,000
    }

    [Fact]
    public void BR11_exact_half_thousand_rounds_up()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 55_000, distanceKm: 2.0m));

        Assert.Equal(49_500, result.FoodTotal);
        Assert.Equal(65_000, result.Total);   // 64,500 → 65,000, the half rounds up
    }

    [Fact]
    public void BR11_no_intermediate_rounding_of_the_quiet_kitchen_discount()
    {
        // 10 % of 55,499 is 5,549.9. Truncating to 5,549 leaves a food total of 49,950 and a total of
        // 65,000; rounding the discount up to 5,550 would leave 49,949 and round down to 64,000.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 55_499, distanceKm: 2.0m));

        Assert.Equal(5_549, result.QuietKitchenDiscount);
        Assert.Equal(49_950, result.FoodTotal);
        Assert.Equal(65_000, result.Total);
    }

    [Fact]
    public void BR11_no_intermediate_rounding_of_the_delivery_fee()
    {
        // 6.01 km → D = 44,000 and R = 8,800; the raw total 232,800 must round once to 233,000,
        // not be assembled from already-rounded pieces.
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 6.01m, placedAt: Snapshot.At(12, 0)));

        Assert.Equal(44_000, result.DeliveryFee);
        Assert.Equal(8_800, result.RushSurcharge);
        Assert.Equal(232_800, result.FoodTotal + result.DeliveryFee + result.RushSurcharge + result.RainSurcharge);
        Assert.Equal(233_000, result.Total);
    }

    [Fact]
    public void BR11_total_is_always_a_whole_number_of_thousands()
    {
        long[] subtotals = [50_000, 55_499, 64_950, 99_999, 200_000, 299_999, 300_000, 1_234_567];
        decimal[] distances = [0m, 2.01m, 3.2m, 5.01m, 8.0m];

        foreach (var subtotal in subtotals)
        {
            foreach (var distance in distances)
            {
                var result = PricingEngine.Calculate(Snapshot.With(subtotal: subtotal, distanceKm: distance));

                Assert.Equal(0, result.Total % PricingEngine.RoundingGranularity);
            }
        }
    }
}
