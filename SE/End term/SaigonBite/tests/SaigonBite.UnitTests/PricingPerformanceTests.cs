using System.Diagnostics;
using SaigonBite.Core.Pricing;
using Xunit;
using Xunit.Abstractions;

namespace SaigonBite.UnitTests;

/// <summary>
/// NFR1 — a price calculation for an order of 30 line items completes in under 1.5 seconds.
/// The test measures the engine in isolation so the figure is attributable to pricing and not to
/// HTTP, rendering or database access.
/// </summary>
public sealed class PricingPerformanceTests
{
    private readonly ITestOutputHelper _output;

    public PricingPerformanceTests(ITestOutputHelper output) => _output = output;

    private static PriceContext ThirtyLineContext() => new()
    {
        Lines = Enumerable.Range(1, 30)
            .Select(i => new PriceLineRequest(i, 2, 35_000))
            .ToList(),
        DistanceKm = 3.2m,
        PlacementTime = new DateTime(2026, 10, 23, 15, 0, 0, DateTimeKind.Unspecified),
        RainFlagOn = false,
        HubLoadPercent = 20,
    };

    [Fact]
    public void NFR1_thirty_line_order_prices_well_under_1500_milliseconds()
    {
        var context = ThirtyLineContext();

        // warm up the JIT so the measurement reflects steady-state cost
        for (var i = 0; i < 50; i++) PricingEngine.Calculate(context);

        const int runs = 1000;
        var watch = Stopwatch.StartNew();
        for (var i = 0; i < runs; i++) PricingEngine.Calculate(context);
        watch.Stop();

        var perCallMs = watch.Elapsed.TotalMilliseconds / runs;
        _output.WriteLine(
            $"NFR1 measured: {perCallMs:F4} ms per 30-line calculation, mean of {runs} runs "
            + $"(total {watch.Elapsed.TotalMilliseconds:F1} ms). Limit: 1500 ms.");

        Assert.True(perCallMs < 1500,
            $"NFR1 violated: {perCallMs:F2} ms per calculation exceeds the 1500 ms limit.");
    }

    [Fact]
    public void NFR1_the_measured_figure_is_recorded_for_the_report()
    {
        var context = ThirtyLineContext();
        for (var i = 0; i < 50; i++) PricingEngine.Calculate(context);

        const int runs = 5000;
        var watch = Stopwatch.StartNew();
        for (var i = 0; i < runs; i++) PricingEngine.Calculate(context);
        watch.Stop();

        var perCallMs = watch.Elapsed.TotalMilliseconds / runs;
        // Written to the test log so the QA report quotes a measured number, not a claim.
        _output.WriteLine($"NFR1 steady-state: {perCallMs:F4} ms per call over {runs} runs");
        Assert.True(perCallMs > 0);
    }
}
