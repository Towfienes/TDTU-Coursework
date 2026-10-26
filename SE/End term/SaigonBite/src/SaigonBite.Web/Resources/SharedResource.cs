namespace SaigonBite.Web;

/// <summary>
/// Marker type for the shared interface resources. <c>IStringLocalizer&lt;SharedResource&gt;</c> resolves
/// <c>Resources/SharedResource.resx</c> (English, the neutral culture) and
/// <c>Resources/SharedResource.vi.resx</c> (Vietnamese), which is what the visible EN/VI toggle switches
/// (FR-S1, NFR3).
/// </summary>
/// <remarks>
/// The type lives in the application's root namespace on purpose: with
/// <c>ResourcesPath = "Resources"</c> the localiser builds the resource base name from the type name
/// relative to the root namespace, so the files stay in the <c>Resources/</c> folder without a duplicated
/// folder segment.
/// </remarks>
public sealed class SharedResource
{
}
