namespace SaigonBite.Core.Orders;

/// <summary>
/// The eight order states of the section C lifecycle (BR15, BR16).
/// </summary>
/// <remarks>
/// <see cref="Delivered"/>, <see cref="Cancelled"/> and <see cref="Failed"/> are terminal: no
/// transition leaves them.
/// </remarks>
public enum OrderStatus
{
    /// <summary>Order created and priced; the only state in which items may be edited (BR17).</summary>
    Placed = 0,

    /// <summary>Kitchen staff accepted the order at their hub; load now counts this order (BR8).</summary>
    Confirmed = 1,

    /// <summary>Kitchen staff are cooking.</summary>
    Preparing = 2,

    /// <summary>Food is packed and waiting for a shipper.</summary>
    Ready = 3,

    /// <summary>Shipper left the hub with the order.</summary>
    OutForDelivery = 4,

    /// <summary>Terminal. Reached only after the COD cash confirmation for a COD order (BR14).</summary>
    Delivered = 5,

    /// <summary>Terminal. Reachable from <see cref="Placed"/> and <see cref="Confirmed"/> only (BR16).</summary>
    Cancelled = 6,

    /// <summary>Terminal. Delivery attempted and failed.</summary>
    Failed = 7,
}
