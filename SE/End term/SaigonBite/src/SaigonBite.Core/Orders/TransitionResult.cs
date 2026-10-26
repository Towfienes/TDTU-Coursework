namespace SaigonBite.Core.Orders;

/// <summary>
/// The outcome of asking the state machine whether a transition is permitted (BR15, BR16, NFR6).
/// </summary>
/// <param name="Allowed">
/// True when the BR15 state table grants this transition to this actor.
/// </param>
/// <param name="Reason">
/// Refusal explanation when <paramref name="Allowed"/> is false;  the obligation that a reason must be
/// supplied, when <paramref name="Allowed"/> is true and the move is permitted but conditional.
/// </param>
/// <remarks>
/// <para>Read the two members together — there are three states, not two:</para>
/// <list type="table">
///   <listheader><term>Allowed</term><description>Reason</description></listheader>
///   <item><term>false</term><description>Non-null: why the transition is refused. Reject the request.</description></item>
///   <item><term>true</term><description>Null: permitted unconditionally. Write the history row.</description></item>
///   <item><term>true</term><description>
///     Non-null: permitted, but the caller must collect a non-empty reason before writing the
///     <c>OrderStatusHistory</c> row (kitchen staff rejecting a Placed order, admin cancelling a
///     Confirmed order — BR16, ambiguity A5). The caller must not silently drop this text.
///   </description></item>
/// </list>
/// </remarks>
public sealed record TransitionResult(bool Allowed, string? Reason);
