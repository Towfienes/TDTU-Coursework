using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR3 delivery fee — the three distance tiers and the partial-kilometre rounding rule
/// ("rounded up means 2.01 km counts as 1 extra km").
/// </summary>
/// <remarks>
/// <para>Partitions and the value each tier must return:</para>
/// <list type="table">
///   <listheader><term>Distance d (km)</term><description>D</description></listheader>
///   <item><term>d ≤ 2.0</term><description>15,000</description></item>
///   <item><term>2.0 &lt; d ≤ 5.0</term><description>15,000 + 5,000 × ⌈d − 2⌉</description></item>
///   <item><term>5.0 &lt; d ≤ 8.0</term><description>30,000 + 7,000 × ⌈d − 5⌉</description></item>
/// </list>
/// <para>
/// The 5.0 km boundary is deliberately discontinuous (ambiguity A4): the specification restarts the
/// second tier from a 30,000 base, so 5.0 km costs 30,000 and 5.01 km costs 37,000. The behaviour is
/// pinned by a test rather than corrected.
/// </para>
/// </remarks>
public sealed class PricingDeliveryFeeTests
{
    [Fact]
    public void BR3_distance_2_0_pays_the_flat_15000()
    {
        Assert.Equal(15_000, PricingEngine.DistanceFee(2.0m));
    }

    [Fact]
    public void BR3_distance_2_01_counts_as_one_extra_km()
    {
        // 15,000 + 5,000 × ⌈0.01⌉ = 20,000: the partial kilometre is charged as a whole one.
        Assert.Equal(20_000, PricingEngine.DistanceFee(2.01m));
    }

    [Fact]
    public void BR3_distance_2_0001_still_counts_as_one_extra_km()
    {
        // Rounding up is not "round to two decimals": any fraction of a kilometre is a whole step.
        Assert.Equal(20_000, PricingEngine.DistanceFee(2.0001m));
    }

    [Fact]
    public void BR3_distance_4_0_pays_25000()
    {
        // 15,000 + 5,000 × ⌈2.0⌉ = 25,000.
        Assert.Equal(25_000, PricingEngine.DistanceFee(4.0m));
    }

    [Fact]
    public void BR3_distance_4_01_counts_as_three_extra_km()
    {
        // 15,000 + 5,000 × ⌈2.01⌉ = 15,000 + 15,000 = 30,000, still inside the middle tier.
        Assert.Equal(30_000, PricingEngine.DistanceFee(4.01m));
    }

    [Fact]
    public void BR3_distance_5_0_vs_5_01_discontinuity()
    {
        // Documented discontinuity (ambiguity A4): 5.0 km ends the middle tier at 30,000, while
        // 5.01 km restarts the third tier at a 30,000 base plus one whole 7,000-km step.
        Assert.Equal(30_000, PricingEngine.DistanceFee(5.0m));
        Assert.Equal(37_000, PricingEngine.DistanceFee(5.01m));
    }

    [Fact]
    public void BR3_distance_5_0001_is_already_in_the_third_tier()
    {
        Assert.Equal(37_000, PricingEngine.DistanceFee(5.0001m));
    }

    [Fact]
    public void BR3_distance_6_0_pays_37000()
    {
        // 30,000 + 7,000 × ⌈1.0⌉ = 37,000.
        Assert.Equal(37_000, PricingEngine.DistanceFee(6.0m));
    }

    [Fact]
    public void BR3_distance_6_01_counts_as_two_extra_km_above_five()
    {
        // 30,000 + 7,000 × ⌈1.01⌉ = 44,000.
        Assert.Equal(44_000, PricingEngine.DistanceFee(6.01m));
    }

    [Fact]
    public void BR3_distance_8_0_pays_the_51_000_upper_bound()
    {
        // 30,000 + 7,000 × ⌈3.0⌉ = 51,000 is the most any covered address can be charged.
        Assert.Equal(51_000, PricingEngine.DistanceFee(8.0m));
    }

    [Fact]
    public void BR3_distance_fee_flows_into_the_rounded_total()
    {
        // S = 200,000, load 20 %, 3.2 km, 15:00, rain off, no voucher (the specification's worked example).
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 3.2m));

        Assert.Equal(25_000, result.DeliveryFee);
        Assert.Equal(205_000, result.Total);
    }
}
