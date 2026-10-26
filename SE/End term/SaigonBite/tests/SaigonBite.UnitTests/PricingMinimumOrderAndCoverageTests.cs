using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR1 minimum order and BR2 coverage — equivalence partitioning plus the specified boundary values
/// (49,999 / 50,000 and 8.0 / 8.01).
/// </summary>
/// <remarks>
/// Partitioning for BR1: [0, 49,999] rejected, [50,000, ∞) accepted. For BR2: [0, 8.0] accepted,
/// (8.0, ∞) rejected. Every test holds the rest of the snapshot at its neutral default, so a failure
/// can only come from the rule under test.
/// </remarks>
public sealed class PricingMinimumOrderAndCoverageTests
{
    [Fact]
    public void BR1_subtotal_49999_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 49_999));

        Assert.False(result.IsAccepted);
        Assert.Single(result.Rejections);
        Assert.Equal(PriceRejection.MinimumOrder, result.Rejections[0].Code);
        Assert.Contains("BR1", result.Rejections[0].Message, StringComparison.Ordinal);
    }

    [Fact]
    public void BR1_subtotal_50000_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 50_000));

        Assert.True(result.IsAccepted);
        Assert.Empty(result.Rejections);
        Assert.Equal(50_000, result.Subtotal);
        Assert.Equal(45_000, result.FoodTotal);   // 50,000 − 5,000 Quiet Kitchen
        Assert.Equal(70_000, result.Total);
    }

    [Fact]
    public void BR1_subtotal_zero_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 0));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.MinimumOrder, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR1_minimum_is_checked_against_subtotal_before_discount()
    {
        // A voucher that would push the payable amount below 50,000 must not rescue the order:
        // BR1 compares S, the item subtotal before any discount.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 49_999, voucher: Snapshot.Fixed(amount: 20_000)));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.MinimumOrder, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR2_distance_8_0_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 8.0m));

        Assert.True(result.IsAccepted);
        Assert.Equal(51_000, result.DeliveryFee);  // 30,000 + 7,000 × ⌈8.0 − 5⌉ = 30,000 + 21,000
    }

    [Fact]
    public void BR2_distance_8_01_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 8.01m));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.Coverage, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR2_distance_8_001_is_rejected()
    {
        // Three decimal places are not expected, but any excess at all is outside coverage.
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 8.001m));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.Coverage, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR2_distance_zero_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 0m));

        Assert.True(result.IsAccepted);
        Assert.Equal(15_000, result.DeliveryFee);
    }
}
