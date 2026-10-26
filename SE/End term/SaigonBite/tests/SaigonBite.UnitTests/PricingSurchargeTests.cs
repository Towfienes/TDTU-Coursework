using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR4 rush-hour surcharge, BR5 heavy-rain surcharge and BR6 free delivery.
/// </summary>
/// <remarks>
/// BR4 partitions the placement time into [11:00, 13:00), [17:30, 19:30) and everything else; start is
/// inclusive and end exclusive, so 11:00 and 17:30 are rush and 13:00 and 19:30 are not. BR6 partitions
/// S at 299,999 / 300,000 and must waive D and R while leaving R2 intact.
/// </remarks>
public sealed class PricingSurchargeTests
{
    [Fact]
    public void BR4_1100_exactly_is_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(11, 0)));

        Assert.Equal(5_000, result.RushSurcharge);   // 20 % of 25,000
        Assert.Equal(210_000, result.Total);         // 180,000 + 25,000 + 5,000
    }

    [Fact]
    public void BR4_1059_is_not_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(10, 59)));

        Assert.Equal(0, result.RushSurcharge);
        Assert.Equal(205_000, result.Total);
    }

    [Fact]
    public void BR4_1259_is_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(12, 59)));

        Assert.Equal(5_000, result.RushSurcharge);
    }

    [Fact]
    public void BR4_1300_exactly_is_not_rush()
    {
        // The window is end-exclusive: 13:00 is outside [11:00, 13:00).
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(13, 0)));

        Assert.Equal(0, result.RushSurcharge);
        Assert.Equal(205_000, result.Total);
    }

    [Fact]
    public void BR4_1730_exactly_is_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(17, 30)));

        Assert.Equal(5_000, result.RushSurcharge);
    }

    [Fact]
    public void BR4_1929_is_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(19, 29)));

        Assert.Equal(5_000, result.RushSurcharge);
    }

    [Fact]
    public void BR4_1930_exactly_is_not_rush()
    {
        // The window is end-exclusive: 19:30 is outside [17:30, 19:30).
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(19, 30)));

        Assert.Equal(0, result.RushSurcharge);
    }

    [Fact]
    public void BR4_1500_is_not_rush()
    {
        var result = PricingEngine.Calculate(Snapshot.With(placedAt: Snapshot.At(15, 0)));

        Assert.Equal(0, result.RushSurcharge);
    }

    [Fact]
    public void BR4_surcharge_is_20_percent_of_the_delivery_fee()
    {
        // 8.0 km → D = 51,000, so R = 10,200 and the raw total is 180,000 + 51,000 + 10,200 = 241,200.
        var result = PricingEngine.Calculate(Snapshot.With(distanceKm: 8.0m, placedAt: Snapshot.At(12, 0)));

        Assert.Equal(51_000, result.DeliveryFee);
        Assert.Equal(10_200, result.RushSurcharge);
        Assert.Equal(241_000, result.Total);   // 241,200 rounded once to the nearest 1,000 (BR11)
    }

    [Fact]
    public void BR5_rain_flag_on_adds_a_flat_10000()
    {
        var result = PricingEngine.Calculate(Snapshot.With(rain: true));

        Assert.Equal(10_000, result.RainSurcharge);
        Assert.Equal(215_000, result.Total);   // 180,000 + 25,000 + 10,000
    }

    [Fact]
    public void BR5_rain_flag_off_adds_nothing()
    {
        var result = PricingEngine.Calculate(Snapshot.With(rain: false));

        Assert.Equal(0, result.RainSurcharge);
        Assert.Equal(205_000, result.Total);
    }

    [Fact]
    public void BR6_subtotal_299999_still_pays_delivery()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 299_999));

        Assert.Equal(25_000, result.DeliveryFee);
        Assert.Equal(295_000, result.Total);   // 270,000 food + 25,000 delivery
    }

    [Fact]
    public void BR6_subtotal_300000_waives_delivery()
    {
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 300_000));

        Assert.Equal(0, result.DeliveryFee);
        Assert.Equal(270_000, result.Total);   // 300,000 − 30,000 food, delivery waived
    }

    [Fact]
    public void BR6_waiver_also_waives_the_rush_surcharge()
    {
        // BR10 step 6: R is computed only when D is not waived.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 300_000, placedAt: Snapshot.At(12, 0)));

        Assert.Equal(0, result.DeliveryFee);
        Assert.Equal(0, result.RushSurcharge);
        Assert.Equal(270_000, result.Total);
    }

    [Fact]
    public void BR6_waiver_keeps_the_rain_surcharge()
    {
        // BR6 explicitly keeps R2: "R2 still applies".
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 300_000, placedAt: Snapshot.At(12, 0), rain: true));

        Assert.Equal(0, result.DeliveryFee);
        Assert.Equal(0, result.RushSurcharge);
        Assert.Equal(10_000, result.RainSurcharge);
        Assert.Equal(280_000, result.Total);
    }
}
