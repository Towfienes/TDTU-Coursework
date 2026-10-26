namespace SaigonBite.Web.Infrastructure;

/// <summary>
/// Role names used by the cookie claims and the authorisation policies (FR-S2, NFR4).
/// </summary>
/// <remarks>
/// The abstract Customer actor of the case study is a single role here; the two concrete customer types
/// are told apart by the <c>CustomerType</c> claim and the BR13 payment filter.
/// </remarks>
public static class Roles
{
    /// <summary>Local Customer or Foreign Tourist (the abstract Customer actor).</summary>
    public const string Customer = "Customer";

    /// <summary>Kitchen Staff, bound to one hub.</summary>
    public const string KitchenStaff = "KitchenStaff";

    /// <summary>Shipper, picks up Ready orders.</summary>
    public const string Shipper = "Shipper";

    /// <summary>System Administrator.</summary>
    public const string Admin = "Admin";

    /// <summary>Every role name, used by validators and seeding.</summary>
    public static readonly IReadOnlyList<string> All = new[] { Customer, KitchenStaff, Shipper, Admin };
}

/// <summary>
/// Names of the authorisation policies registered in <c>Program.cs</c> (FR-S2).
/// </summary>
public static class Policies
{
    /// <summary>Customer-only functions: cart, checkout, my orders, registration-linked screens.</summary>
    public const string Customer = "Customer";

    /// <summary>Kitchen Staff questions/transitions for their own hub.</summary>
    public const string KitchenStaff = "KitchenStaff";

    /// <summary>Shipper functions: assigned deliveries, cash confirmation, failed delivery.</summary>
    public const string Shipper = "Shipper";

    /// <summary>Administrator functions: CRUD, reports, dashboard, rain flag.</summary>
    public const string Admin = "Admin";

    /// <summary>Kitchen Staff or Administrator — both may read the kitchen board.</summary>
    public const string Kitchen = "Kitchen";

    /// <summary>Shipper, Kitchen Staff or Administrator — the delivery board.</summary>
    public const string Delivery = "Delivery";
}
