using System.ComponentModel.DataAnnotations;
using SaigonBite.Core.Orders;
using SaigonBite.Core.Payments;

namespace SaigonBite.Web.ViewModels;

/// <summary>Sign-in form model (FR-E3).</summary>
public sealed class LoginVm
{
    /// <summary>Mobile number, email address or staff handle.</summary>
    [Required]
    public string Username { get; set; } = string.Empty;

    /// <summary>Plaintext password; only ever compared against the stored hash.</summary>
    [Required]
    public string Password { get; set; } = string.Empty;

    /// <summary>Local URL to return to after sign-in.</summary>
    public string? ReturnUrl { get; set; }
}

/// <summary>Local Customer registration form (FR-E1, BR18).</summary>
public sealed class RegisterLocalVm
{
    /// <summary>Ten digits starting 03, 05, 07, 08 or 09.</summary>
    [Required]
    public string Mobile { get; set; } = string.Empty;

    /// <summary>Name shown in the interface.</summary>
    public string DisplayName { get; set; } = string.Empty;

    /// <summary>At least eight characters.</summary>
    [Required]
    public string Password { get; set; } = string.Empty;

    /// <summary>Repeated password.</summary>
    [Required]
    public string ConfirmPassword { get; set; } = string.Empty;
}

/// <summary>Foreign Tourist registration form (FR-E2, BR18).</summary>
public sealed class RegisterTouristVm
{
    /// <summary>Valid email address and the sign-in identifier.</summary>
    [Required]
    public string Email { get; set; } = string.Empty;

    /// <summary>Six to nine letters or digits.</summary>
    [Required]
    public string PassportNumber { get; set; } = string.Empty;

    /// <summary>Country of citizenship.</summary>
    [Required]
    public string Nationality { get; set; } = string.Empty;

    /// <summary>Name shown in the interface.</summary>
    public string DisplayName { get; set; } = string.Empty;

    /// <summary>At least eight characters.</summary>
    [Required]
    public string Password { get; set; } = string.Empty;

    /// <summary>Repeated password.</summary>
    [Required]
    public string ConfirmPassword { get; set; } = string.Empty;
}

/// <summary>Simulated OTP / email code form (FR-E1, FR-E2).</summary>
public sealed class VerifyCodeVm
{
    /// <summary>Six-digit code shown in the development UI.</summary>
    [Required]
    public string Code { get; set; } = string.Empty;
}

/// <summary>Brand create/edit form (FR-A1, FR-A3).</summary>
public sealed class BrandFormVm
{
    /// <summary>Brand identifier; 0 when creating.</summary>
    public int Id { get; set; }

    /// <summary>Unique brand name.</summary>
    [Required, StringLength(120)]
    public string Name { get; set; } = string.Empty;

    /// <summary>Short description.</summary>
    [Required, StringLength(400)]
    public string Description { get; set; } = string.Empty;

    /// <summary>Hubs that will operate the brand (BR12 requires at least one).</summary>
    public List<int> HubIds { get; set; } = new();
}

/// <summary>Menu item create/edit form (FR-A3, FR-A5).</summary>
public sealed class MenuItemFormVm
{
    /// <summary>Item identifier; 0 when creating.</summary>
    public int Id { get; set; }

    /// <summary>Owning brand.</summary>
    public int BrandId { get; set; }

    /// <summary>Reporting category used by R1.</summary>
    [Required, StringLength(60)]
    public string Category { get; set; } = string.Empty;

    /// <summary>Item name.</summary>
    [Required, StringLength(120)]
    public string Name { get; set; } = string.Empty;

    /// <summary>Unit price in whole VND.</summary>
    [Range(1, 10_000_000)]
    public long Price { get; set; }

    /// <summary>Availability switch (FR-A5).</summary>
    public bool IsAvailable { get; set; } = true;
}

/// <summary>Hub create/edit form (FR-B1, FR-B3).</summary>
public sealed class HubFormVm
{
    /// <summary>Hub identifier; 0 when creating.</summary>
    public int Id { get; set; }

    /// <summary>Display name.</summary>
    [Required, StringLength(120)]
    public string Name { get; set; } = string.Empty;

    /// <summary>District.</summary>
    [Required, StringLength(80)]
    public string District { get; set; } = string.Empty;

    /// <summary>Street address.</summary>
    [Required, StringLength(200)]
    public string Address { get; set; } = string.Empty;

    /// <summary>Whole-number kitchen capacity greater than zero (FR-B1, BR8).</summary>
    [Range(1, 1000)]
    public int KitchenCapacity { get; set; } = 10;
}

/// <summary>Voucher create/edit form (FR-C1, BR9).</summary>
public sealed class VoucherFormVm
{
    /// <summary>Voucher identifier; 0 when creating.</summary>
    public int Id { get; set; }

    /// <summary>Unique code (stored upper-case).</summary>
    [Required, StringLength(40)]
    public string Code { get; set; } = string.Empty;

    /// <summary>PERCENT or FIXED.</summary>
    public VoucherType Type { get; set; } = VoucherType.Percent;

    /// <summary>Percentage points or whole VND.</summary>
    [Range(1, 100_000_000)]
    public long Value { get; set; }

    /// <summary>Cap in VND for a percentage voucher.</summary>
    [Range(0, 100_000_000)]
    public long MaxDiscount { get; set; }

    /// <summary>Minimum item subtotal in VND.</summary>
    [Range(0, 100_000_000)]
    public long MinSubtotal { get; set; }

    /// <summary>First usable day.</summary>
    public DateOnly ValidFrom { get; set; } = DateOnly.FromDateTime(DateTime.Today);

    /// <summary>Last usable day.</summary>
    public DateOnly ValidTo { get; set; } = DateOnly.FromDateTime(DateTime.Today).AddDays(30);

    /// <summary>Active flag; deactivating is the FR-C2 removal.</summary>
    public bool IsActive { get; set; } = true;
}

/// <summary>Checkout form (FR-D11, BR13, BR14).</summary>
public sealed class CheckoutFormVm
{
    /// <summary>Simulated delivery distance in km (BR2, BR3).</summary>
    [Range(0.1, 20)]
    public decimal DistanceKm { get; set; } = 3.2m;

    /// <summary>Optional voucher code (BR9).</summary>
    public string? VoucherCode { get; set; }

    /// <summary>Chosen payment method (BR13).</summary>
    public PaymentMethod? Method { get; set; }

    /// <summary>Tourist hotel name (User Story 2).</summary>
    public string? HotelName { get; set; }

    /// <summary>Tourist room number (User Story 2).</summary>
    public string? RoomNumber { get; set; }

    /// <summary>Free-text note for the kitchen.</summary>
    public string? Notes { get; set; }

    /// <summary>
    /// False renders the same page with a fresh price so the customer can see a voucher before committing;
    /// true places the order. The price is always recomputed on the server either way.
    /// </summary>
    public bool Place { get; set; }
}

/// <summary>One posted line of the edit form (FR-D12).</summary>
public sealed class EditLineVm
{
    /// <summary>Menu item of the line.</summary>
    public int MenuItemId { get; set; }

    /// <summary>New quantity, 1..20 per BR12.</summary>
    public int Quantity { get; set; }
}

/// <summary>Order edit form: a quantity per existing line plus the items that may be added (FR-D12, BR17).</summary>
public sealed class EditOrderVm
{
    /// <summary>Order being edited.</summary>
    public int OrderId { get; set; }

    /// <summary>Current lines with their quantities.</summary>
    public List<EditLineVm> Lines { get; set; } = new();

    /// <summary>New item to add in this edit, if any.</summary>
    public int? NewMenuItemId { get; set; }

    /// <summary>Quantity of the new item.</summary>
    public int NewQuantity { get; set; } = 1;

    /// <summary>Items the hub can still add.</summary>
    public IReadOnlyList<Data.Entities.MenuItem> AddableItems { get; set; } = new List<Data.Entities.MenuItem>();
}

/// <summary>A menu item add-to-basket request from the public menu (BR12).</summary>
public sealed class AddToCartVm
{
    /// <summary>Hub the item is ordered from.</summary>
    public int HubId { get; set; }

    /// <summary>Menu item.</summary>
    public int MenuItemId { get; set; }

    /// <summary>Quantity, 1..20.</summary>
    [Range(1, 20)]
    public int Quantity { get; set; } = 1;

    /// <summary>Page to return to.</summary>
    public string? ReturnUrl { get; set; }
}
