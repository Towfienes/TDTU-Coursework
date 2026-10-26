namespace SaigonBite.Core.Pricing;

/// <summary>
/// One requested order line handed to the pricing engine.
/// </summary>
/// <param name="MenuItemId">Menu item identity, used only for diagnostics in rejection messages.</param>
/// <param name="Quantity">Units ordered; BR12 restricts this to 1..20.</param>
/// <param name="UnitPrice">Unit price in whole VND, snapshotted when the customer added the item.</param>
/// <remarks>
/// BR12 also requires that every item is marked Available and belongs to a brand the chosen hub
/// operates. Neither fact can travel through this record — it carries no brand or hub reference —
/// so that part of BR12 is enforced by the web/business layer before calling
/// <see cref="PricingEngine.Calculate"/>; see the note on <c>PriceRejection</c> code <c>BR12</c>.
/// </remarks>
public sealed record PriceLineRequest(int MenuItemId, int Quantity, long UnitPrice);
