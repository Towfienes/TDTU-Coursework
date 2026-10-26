using SaigonBite.Core.Pricing;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR12 order-line limits: 1..30 lines per order and 1..20 units per line (boundaries 0/1, 20/21, 30/31).
/// </summary>
/// <remarks>
/// BR12 also forbids unavailable items and items from a brand the chosen hub does not operate. Those two
/// conditions need menu and hub data that <see cref="PriceLineRequest"/> does not carry, so they are
/// enforced by the web/business layer before pricing; this suite covers the numeric limits.
/// </remarks>
public sealed class PricingLineLimitTests
{
    [Fact]
    public void BR12_one_line_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLineCount(lineCount: 1, unitPrice: 50_000));

        Assert.True(result.IsAccepted);
        Assert.Equal(50_000, result.Subtotal);
    }

    [Fact]
    public void BR12_zero_lines_are_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLines([]));

        Assert.False(result.IsAccepted);
        Assert.Contains(result.Rejections, rejection => rejection.Code == PriceRejection.OrderLines);
    }

    [Fact]
    public void BR12_30_lines_are_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLineCount(lineCount: 30));

        Assert.True(result.IsAccepted);
        Assert.Equal(60_000, result.Subtotal);   // 30 lines × 2,000
    }

    [Fact]
    public void BR12_31_lines_are_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLineCount(lineCount: 31));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.OrderLines, Assert.Single(result.Rejections).Code);
    }

    [Fact]
    public void BR12_quantity_1_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLineCount(lineCount: 1, unitPrice: 50_000));

        Assert.True(result.IsAccepted);
    }

    [Fact]
    public void BR12_quantity_20_is_accepted()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLines(
            [new PriceLineRequest(MenuItemId: 7, Quantity: 20, UnitPrice: 3_000)]));

        Assert.True(result.IsAccepted);
        Assert.Equal(60_000, result.Subtotal);
    }

    [Fact]
    public void BR12_quantity_0_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLines(
            [new PriceLineRequest(MenuItemId: 7, Quantity: 0, UnitPrice: 50_000)]));

        Assert.Contains(result.Rejections, rejection => rejection.Code == PriceRejection.OrderLines);
    }

    [Fact]
    public void BR12_quantity_21_is_rejected()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLines(
            [new PriceLineRequest(MenuItemId: 7, Quantity: 21, UnitPrice: 3_000)]));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.OrderLines, Assert.Single(result.Rejections).Code);
        Assert.Contains("line 1", result.Rejections[0].Message, StringComparison.Ordinal);
    }

    [Fact]
    public void BR12_a_legal_line_beside_an_illegal_one_still_rejects_the_order()
    {
        var result = PricingEngine.Calculate(Snapshot.WithLines(
        [
            new PriceLineRequest(MenuItemId: 1, Quantity: 1, UnitPrice: 50_000),
            new PriceLineRequest(MenuItemId: 2, Quantity: 21, UnitPrice: 1_000),
        ]));

        Assert.False(result.IsAccepted);
        Assert.Equal(PriceRejection.OrderLines, Assert.Single(result.Rejections).Code);
        Assert.Contains("line 2", result.Rejections[0].Message, StringComparison.Ordinal);
    }
}
