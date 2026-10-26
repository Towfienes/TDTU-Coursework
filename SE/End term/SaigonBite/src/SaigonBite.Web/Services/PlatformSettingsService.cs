using Microsoft.EntityFrameworkCore;
using SaigonBite.Web.Data;

namespace SaigonBite.Web.Services;

/// <summary>
/// Reads and writes the platform-wide heavy-rain flag that BR5 depends on (FR-S4, FR-D6).
/// </summary>
/// <remarks>
/// The flag is global, not per hub, and it is snapshotted onto each order at placement so a later toggle
/// can never rewrite a historical price (BR17).
/// </remarks>
public interface IPlatformSettingsService
{
    /// <summary>Current value of the heavy-rain flag.</summary>
    Task<bool> GetRainFlagAsync(CancellationToken cancellationToken = default);

    /// <summary>Sets the heavy-rain flag and returns the new value.</summary>
    Task<bool> SetRainFlagAsync(bool enabled, CancellationToken cancellationToken = default);
}

/// <inheritdoc />
public sealed class PlatformSettingsService : IPlatformSettingsService
{
    /// <summary>Key of the rain-flag row.</summary>
    public const string RainFlagKey = "RainFlag";

    private readonly SaigonBiteDbContext _db;

    /// <summary>Creates the service over the scoped context.</summary>
    public PlatformSettingsService(SaigonBiteDbContext db) => _db = db;

    /// <inheritdoc />
    public async Task<bool> GetRainFlagAsync(CancellationToken cancellationToken = default)
    {
        var row = await _db.PlatformSettings
            .AsNoTracking()
            .FirstOrDefaultAsync(s => s.Key == RainFlagKey, cancellationToken);

        return row is not null && bool.TryParse(row.Value, out var enabled) && enabled;
    }

    /// <inheritdoc />
    public async Task<bool> SetRainFlagAsync(bool enabled, CancellationToken cancellationToken = default)
    {
        var row = await _db.PlatformSettings
            .FirstOrDefaultAsync(s => s.Key == RainFlagKey, cancellationToken);

        if (row is null)
        {
            row = new Data.Entities.PlatformSetting { Key = RainFlagKey };
            _db.PlatformSettings.Add(row);
        }

        row.Value = enabled ? "true" : "false";
        await _db.SaveChangesAsync(cancellationToken);
        return enabled;
    }
}
