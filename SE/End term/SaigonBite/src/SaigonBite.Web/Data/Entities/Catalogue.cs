namespace SaigonBite.Web.Data.Entities;

/// <summary>
/// A cloud kitchen. Load is derived, never stored (BR8, FR-B2): it is the number of orders in
/// <c>Confirmed</c> or <c>Preparing</c> divided by <see cref="KitchenCapacity"/>.
/// </summary>
/// <remarks>
/// FR-B1 requires a whole-number capacity greater than zero; the check lives in the hub controller and
/// is repeated in the EF configuration's check constraint so the database cannot hold a zero either.
/// The soft-delete flag (FR-B4) keeps historical orders and report rows pointing at a live row.
/// </remarks>
public class Hub
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Display name, for example "SaigonBite District 1".</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>District of Ho Chi Minh City.</summary>
    public string District { get; set; } = string.Empty;

    /// <summary>Street address of the kitchen.</summary>
    public string Address { get; set; } = string.Empty;

    /// <summary>Concurrent orders the kitchen can handle; must be at least 1 (BR8, FR-B1).</summary>
    public int KitchenCapacity { get; set; }

    /// <summary>Soft-delete flag (FR-B4).</summary>
    public bool IsDeleted { get; set; }

    /// <summary>Brands operated by this hub (BR12: items must belong to an operated brand).</summary>
    public ICollection<HubBrand> HubBrands { get; set; } = new List<HubBrand>();

    /// <summary>Orders placed at this hub (never deleted).</summary>
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

/// <summary>
/// A virtual brand cooked by one or more hubs, for example a pho brand and a banh mi brand.
/// </summary>
public class Brand
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Unique brand name (FR-A1).</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>Short pitch shown on the menu screen (FR-A1).</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>Soft-delete flag (FR-A4): historical orders keep the brand name they snapshotted.</summary>
    public bool IsDeleted { get; set; }

    /// <summary>Hubs that operate this brand.</summary>
    public ICollection<HubBrand> HubBrands { get; set; } = new List<HubBrand>();

    /// <summary>Menu items of the brand.</summary>
    public ICollection<MenuItem> MenuItems { get; set; } = new List<MenuItem>();
}

/// <summary>
/// Join row between <see cref="Hub"/> and <see cref="Brand"/> — the "operating hubs" of FR-A1.
/// </summary>
public class HubBrand
{
    /// <summary>Foreign key to <see cref="Hub"/>.</summary>
    public int HubId { get; set; }

    /// <summary>Navigation for <see cref="HubId"/>.</summary>
    public Hub? Hub { get; set; }

    /// <summary>Foreign key to <see cref="Brand"/>.</summary>
    public int BrandId { get; set; }

    /// <summary>Navigation for <see cref="BrandId"/>.</summary>
    public Brand? Brand { get; set; }
}

/// <summary>
/// A sellable menu item. <see cref="Price"/> is a snapshot source for <see cref="OrderLine"/>, which
/// copies the value at placement so later edits cannot rewrite history (FR-A4).
/// </summary>
public class MenuItem
{
    /// <summary>Primary key.</summary>
    public int Id { get; set; }

    /// <summary>Owning brand (FR-A1, BR12).</summary>
    public int BrandId { get; set; }

    /// <summary>Navigation for <see cref="BrandId"/>.</summary>
    public Brand? Brand { get; set; }

    /// <summary>Reporting category, for example noodles, rice, drinks (FR-R1).</summary>
    public string Category { get; set; } = string.Empty;

    /// <summary>Item name shown on the menu and copied onto the order line.</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>Unit price in whole VND.</summary>
    public long Price { get; set; }

    /// <summary>Availability switch (FR-A5): an unavailable item cannot be ordered (BR12).</summary>
    public bool IsAvailable { get; set; } = true;

    /// <summary>Soft-delete flag (FR-A4).</summary>
    public bool IsDeleted { get; set; }
}
