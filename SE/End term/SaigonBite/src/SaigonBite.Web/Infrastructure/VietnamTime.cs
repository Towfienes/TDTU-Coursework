using System.Globalization;

namespace SaigonBite.Web.Infrastructure;

/// <summary>
/// Vietnam local time helper. The specification fixes the business clock to UTC+7 (BR4 windows, BR9
/// validity, BR17 snapshot), so every timestamp written by this tier goes through here.
/// </summary>
public static class VietnamTime
{
    private static readonly TimeZoneInfo Zone = ResolveZone();

    /// <summary>Current Vietnam local time (UTC+7).</summary>
    public static DateTime Now => TimeZoneInfo.ConvertTimeFromUtc(DateTime.UtcNow, Zone);

    /// <summary>Converts a UTC instant to Vietnam local time.</summary>
    public static DateTime FromUtc(DateTime utc) =>
        TimeZoneInfo.ConvertTimeFromUtc(DateTime.SpecifyKind(utc, DateTimeKind.Utc), Zone);

    /// <summary>Today in Vietnam, used for BR9 validity checks and report defaults.</summary>
    public static DateOnly Today => DateOnly.FromDateTime(Now);

    private static TimeZoneInfo ResolveZone()
    {
        foreach (var id in new[] { "Asia/Ho_Chi_Minh", "SE Asia Standard Time" })
        {
            try
            {
                return TimeZoneInfo.FindSystemTimeZoneById(id);
            }
            catch (TimeZoneNotFoundException)
            {
                // Try the next id: Linux uses the IANA name, Windows the Windows name.
            }
            catch (InvalidTimeZoneException)
            {
                // Corrupt zone data; fall through to the fixed offset below.
            }
        }

        // Last resort: a fixed UTC+7 offset, which is correct for Vietnam (no daylight saving).
        return TimeZoneInfo.CreateCustomTimeZone("VN", TimeSpan.FromHours(7), "Vietnam", "Vietnam");
    }
}

/// <summary>
/// Money formatting shared by every Razor view. Money is whole VND stored as <see cref="long"/>
/// (CONTRACT.md); the interface must never imply decimals.
/// </summary>
public static class Money
{
    private static readonly NumberFormatInfo Format = new()
    {
        NumberGroupSeparator = ",",
        NumberGroupSizes = new[] { 3 },
        NumberDecimalDigits = 0,
    };

    /// <summary>Formats an amount as grouped VND, for example <c>205,000 ₫</c>.</summary>
    public static string Vnd(long amount) => amount.ToString("N0", Format) + " ₫";

    /// <summary>Formats a signed amount, for example <c>−205,000 ₫</c> on a refund row.</summary>
    public static string VndSigned(long amount) =>
        (amount < 0 ? "−" : string.Empty) + Vnd(Math.Abs(amount));
}
