using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR8 hub load and protection: a hub at 90 % load or above refuses new orders (boundary 89 % / 90 %).
/// </summary>
/// <remarks>
/// The load percentage and the <c>HubRejectsNewOrders</c> flag are two views of the same placement
/// snapshot. The engine rejects when either says overloaded, so a caller that fills only one of them
/// cannot accidentally sell into a saturated kitchen.
/// </remarks>
public sealed class PricingHubProtectionTests
{
    [Fact]
    public void BR8_load_0_percent_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 0));

        Assert.True(result.IsAccepted);
    }

    [Fact]
    public void BR8_load_89_percent_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 89));

        Assert.True(result.IsAccepted);
        Assert.Equal(0, result.QuietKitchenDiscount);   // 89 % is above the BR7 threshold, so no discount
        Assert.Equal(225_000, result.Total);
    }

    [Fact]
    public void BR8_load_90_percent_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 90));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.HubProtection, Assert.Single(result.Rejections).Code);
        Assert.Contains("90%", result.Rejections[0].Message, StringComparison.Ordinal);
    }

    [Fact]
    public void BR8_load_100_percent_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 100));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.HubProtection, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR8_overload_flag_rejects_even_when_the_snapshot_percentage_looks_calm()
    {
        // Defensive: the flag is the authoritative "hub is full" signal; a stale percentage must not
        // let the order through.
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 20, hubRejectsNewOrders: true));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.HubProtection, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR8_load_at_or_above_90_rejects_even_when_the_flag_is_false()
    {
        var result = PricingEngine.Calculate(Snapshot.With(hubLoadPercent: 95, hubRejectsNewOrders: false));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.HubProtection, Assert.Single(result.Rejections).Code);
    }
}
