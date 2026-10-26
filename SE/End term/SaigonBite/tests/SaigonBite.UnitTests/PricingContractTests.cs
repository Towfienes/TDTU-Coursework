using System.Diagnostics;
using System.Runtime.CompilerServices;
using System.Text;
using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// The contract-level properties of the pricing engine: determinism for a fixed snapshot (NFR6), purity
/// with respect to the wall clock (BR17), rejection ordering (BR1, BR2, BR8, BR12) and the NFR1 budget.
/// </summary>
public sealed class PricingContractTests
{
    [Fact]
    public void Pricing_is_deterministic_for_an_identical_snapshot()
    {
        // Two independently built contexts carrying the same values must produce the same breakdown.
        var first = PricingEngine.Calculate(Snapshot.With(
            subtotal: 237_500,
            distanceKm: 4.4m,
            placedAt: Snapshot.At(18, 5),
            rain: true,
            hubLoadPercent: 12,
            voucher: Snapshot.Percent(percent: 15, maxDiscount: 25_000, minSubtotal: 100_000)));

        var second = PricingEngine.Calculate(Snapshot.With(
            subtotal: 237_500,
            distanceKm: 4.4m,
            placedAt: Snapshot.At(18, 5),
            rain: true,
            hubLoadPercent: 12,
            voucher: Snapshot.Percent(percent: 15, maxDiscount: 25_000, minSubtotal: 100_000)));

        Assert.Equal(first.Subtotal, second.Subtotal);
        Assert.Equal(first.QuietKitchenDiscount, second.QuietKitchenDiscount);
        Assert.Equal(first.VoucherDiscount, second.VoucherDiscount);
        Assert.Equal(first.FoodTotal, second.FoodTotal);
        Assert.Equal(first.DeliveryFee, second.DeliveryFee);
        Assert.Equal(first.RushSurcharge, second.RushSurcharge);
        Assert.Equal(first.RainSurcharge, second.RainSurcharge);
        Assert.Equal(first.Total, second.Total);
        Assert.Equal(
            first.Rejections.Select(rejection => rejection.Code),
            second.Rejections.Select(rejection => rejection.Code));
        Assert.Equal(first.IsAccepted, second.IsAccepted);
    }

    [Fact]
    public void Pricing_repeats_exactly_when_called_twice_on_the_same_context()
    {
        var context = Snapshot.With(subtotal: 55_499, distanceKm: 2.0m);

        var first = PricingEngine.Calculate(context);
        var second = PricingEngine.Calculate(context);

        // PriceResult is a record, so value equality holds while the rejection list is the shared empty
        // instance the engine returns for an accepted order.
        Assert.Equal(first, second);
    }

    [Fact]
    public void BR4_rush_surcharge_follows_the_context_timestamp_not_the_wall_clock()
    {
        // Both placements are in the year 2000. If the engine read the current time instead of the stored
        // snapshot (BR17), both calls would produce the same surcharge; they must not.
        var midday = new DateTime(2000, 1, 3, 12, 0, 0, DateTimeKind.Unspecified);
        var afternoon = new DateTime(2000, 1, 3, 15, 0, 0, DateTimeKind.Unspecified);

        var rush = PricingEngine.Calculate(Snapshot.With(placedAt: midday));
        var quiet = PricingEngine.Calculate(Snapshot.With(placedAt: afternoon));

        Assert.Equal(5_000, rush.RushSurcharge);
        Assert.Equal(0, quiet.RushSurcharge);
        Assert.Equal(210_000, rush.Total);
        Assert.Equal(205_000, quiet.Total);
    }

    [Fact]
    public void Pricing_engine_source_never_reads_the_wall_clock()
    {
        // A behavioural test can only prove the clock is not read today; scanning the sources proves the
        // module cannot read it at all. Comments are stripped first, because the design notes mention the
        // forbidden APIs by name.
        var directory = FindPricingSourceDirectory();
        var files = Directory.GetFiles(directory, "*.cs", SearchOption.TopDirectoryOnly);

        Assert.NotEmpty(files);

        string[] forbidden = ["DateTime.Now", "DateTime.Today", "DateTime.UtcNow", "DateTimeOffset.Now", "DateTimeOffset.UtcNow"];

        foreach (var file in files)
        {
            var code = StripComments(File.ReadAllText(file));

            foreach (var token in forbidden)
            {
                Assert.False(
                    code.Contains(token, StringComparison.Ordinal),
                    string.Concat("PricingEngine purity violated: ", Path.GetFileName(file), " reads ", token, "."));
            }
        }
    }

    [Fact]
    public void Rejections_are_returned_in_contract_order()
    {
        // Every rule is broken at once: below the minimum, outside coverage, hub saturated, too many lines.
        var lines = Enumerable
            .Range(1, 31)
            .Select(index => new PriceLineRequest(MenuItemId: index, Quantity: 1, UnitPrice: 1_000))
            .ToList();

        var context = new PriceContext
        {
            Lines = lines,
            DistanceKm = 9.5m,
            PlacementTime = Snapshot.QuietAfternoon,
            RainFlagOn = false,
            HubLoadPercent = 95,
        };

        var result = PricingEngine.Calculate(context);

        Assert.False(result.IsAccepted);
        Assert.Equal(
            new[] { PriceRejection.MinimumOrder, PriceRejection.Coverage, PriceRejection.HubProtection, PriceRejection.OrderLines },
            result.Rejections.Select(rejection => rejection.Code).ToArray());
    }

    [Fact]
    public void Rejected_orders_still_expose_the_breakdown_for_display()
    {
        // The checkout screen shows what the customer built and what is missing, so the money fields are
        // populated even when BR1 refuses the order. Only IsAccepted gates the charge.
        var result = PricingEngine.Calculate(Snapshot.With(subtotal: 49_999));

        Assert.False(result.IsAccepted);
        Assert.Equal(49_999, result.Subtotal);
        Assert.Equal(4_999, result.QuietKitchenDiscount);
        Assert.Equal(45_000, result.FoodTotal);
    }

    [Fact]
    public void NFR1_pricing_30_lines_stays_far_below_the_1_5_second_budget()
    {
        var context = Snapshot.WithLines(
            Enumerable
                .Range(1, 30)
                .Select(index => new PriceLineRequest(MenuItemId: index, Quantity: 20, UnitPrice: 1_750))
                .ToList());

        var stopwatch = Stopwatch.StartNew();
        var result = PricingEngine.Calculate(context);
        stopwatch.Stop();

        Assert.Equal(1_050_000, result.Subtotal);   // 30 lines × 20 × 1,750
        Assert.True(
            stopwatch.ElapsedMilliseconds < 1_500,
            $"pricing took {stopwatch.ElapsedMilliseconds} ms, budget 1500 ms");
    }

    [Fact]
    public void Calculate_rejects_a_null_context()
    {
        Assert.Throws<ArgumentNullException>(() => PricingEngine.Calculate(null!));
    }

    /// <summary>Walks up from this test file to the repository's pricing source directory.</summary>
    private static string FindPricingSourceDirectory([CallerFilePath] string callerFilePath = "")
    {
        for (var directory = new DirectoryInfo(Path.GetDirectoryName(callerFilePath)!);
             directory is not null;
             directory = directory.Parent)
        {
            var candidate = Path.Combine(directory.FullName, "src", "SaigonBite.Core", "Pricing");

            if (Directory.Exists(candidate))
            {
                return candidate;
            }
        }

        throw new DirectoryNotFoundException(
            string.Concat("Could not locate src/SaigonBite.Core/Pricing above ", callerFilePath, "."));
    }

    /// <summary>
    /// Removes <c>//</c> line comments and <c>/* */</c> blocks so the scan reads executable code only.
    /// </summary>
    /// <remarks>
    /// The pricing sources contain no string literal holding a comment delimiter, so a lexical scan is
    /// enough here and avoids taking a dependency on the compiler's syntax API.
    /// </remarks>
    private static string StripComments(string source)
    {
        var code = new StringBuilder(source.Length);
        var insideBlockComment = false;

        for (var index = 0; index < source.Length; index++)
        {
            if (insideBlockComment)
            {
                if (source[index] == '*' && index + 1 < source.Length && source[index + 1] == '/')
                {
                    insideBlockComment = false;
                    index++;
                }

                continue;
            }

            if (source[index] == '/' && index + 1 < source.Length)
            {
                if (source[index + 1] == '/')
                {
                    while (index < source.Length && source[index] != '\n')
                    {
                        index++;
                    }

                    code.Append('\n');
                    continue;
                }

                if (source[index + 1] == '*')
                {
                    insideBlockComment = true;
                    index++;
                    continue;
                }
            }

            code.Append(source[index]);
        }

        return code.ToString();
    }
}
