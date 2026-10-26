namespace SaigonBite.Core.Orders;

/// <summary>
/// The BR15 order lifecycle as executable business logic, not UI state.
/// </summary>
/// <remarks>
/// <para>
/// The table below is the specification's section C state table, one row per permitted move. Anything
/// not in it is invalid and must be refused here (BR15: "Any transition not listed is invalid and must
/// be rejected by the business layer, not just hidden in the UI").
/// </para>
/// <para>
/// Two rows carry a precondition that needs order data this pure type does not receive: a shipper must
/// be assigned before Ready → OutForDelivery, and COD cash must be confirmed before Out for Delivery →
/// Delivered (BR14). The business layer checks those before calling
/// <see cref="CanTransition"/>; the actor matrix here is the part that belongs to the state machine.
/// </para>
/// </remarks>
public static class OrderStateMachine
{
    /// <summary>
    /// Returned in <see cref="TransitionResult.Reason"/> when kitchen staff reject a Placed order: the move
    /// is legal but the reason is mandatory (BR16: "Kitchen Staff may reject an order while it is Placed,
    /// giving a reason").
    /// </summary>
    public const string KitchenRejectionReasonRequired =
        "BR16: kitchen staff must give a reason when rejecting a Placed order.";

    /// <summary>
    /// Returned in <see cref="TransitionResult.Reason"/> when an admin cancels a Confirmed order: the move is
    /// legal but the reason is mandatory (ambiguity A5 resolves the state table's "Customer or Admin" row
    /// the same way BR16 treats the kitchen).
    /// </summary>
    public const string AdminCancellationReasonRequired =
        "BR16/A5: an administrator must give a reason when cancelling a Confirmed order.";

    /// <summary>The section C state table, including which actor each row authorises.</summary>
    private static readonly Transition[] Table =
    [
        // From                  To                       Actor                        ReasonRequired
        new(OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.KitchenStaff, false),
        new(OrderStatus.Placed, OrderStatus.Cancelled, ActorRole.Customer, false),
        new(OrderStatus.Placed, OrderStatus.Cancelled, ActorRole.KitchenStaff, true),
        new(OrderStatus.Confirmed, OrderStatus.Preparing, ActorRole.KitchenStaff, false),
        new(OrderStatus.Confirmed, OrderStatus.Cancelled, ActorRole.Customer, false),
        new(OrderStatus.Confirmed, OrderStatus.Cancelled, ActorRole.Admin, true),
        new(OrderStatus.Preparing, OrderStatus.Ready, ActorRole.KitchenStaff, false),
        new(OrderStatus.Ready, OrderStatus.OutForDelivery, ActorRole.Shipper, false),
        new(OrderStatus.OutForDelivery, OrderStatus.Delivered, ActorRole.Shipper, false),
        new(OrderStatus.OutForDelivery, OrderStatus.Failed, ActorRole.Shipper, false),
    ];

    /// <summary>
    /// Decides whether <paramref name="actor"/> may move an order from <paramref name="from"/> to
    /// <paramref name="to"/> (BR15, BR16).
    /// </summary>
    /// <param name="from">Current state.</param>
    /// <param name="to">Requested state.</param>
    /// <param name="actor">Actor asking for the move.</param>
    /// <returns>
    /// A <see cref="TransitionResult"/> whose <c>Reason</c> is null for a plain move, carries the
    /// "reason required" obligation for the two conditional moves, and explains the refusal otherwise.
    /// </returns>
    public static TransitionResult CanTransition(OrderStatus from, OrderStatus to, ActorRole actor)
    {
        if (IsTerminal(from))
        {
            return Refuse(string.Format(
                System.Globalization.CultureInfo.InvariantCulture,
                "BR15: {0} is a terminal state; no transition leaves it.",
                from));
        }

        foreach (var row in Table)
        {
            if (row.From != from || row.To != to || row.Actor != actor)
            {
                continue;
            }

            if (!row.ReasonRequired)
            {
                return new TransitionResult(true, null);
            }

            return new TransitionResult(
                true,
                row.Actor == ActorRole.Admin ? AdminCancellationReasonRequired : KitchenRejectionReasonRequired);
        }

        // The move may still exist in the table for a different actor; say so, because "wrong actor" and
        // "not a transition at all" are different bugs in the caller (NFR6, NFR4).
        foreach (var row in Table)
        {
            if (row.From == from && row.To == to)
            {
                return Refuse(string.Format(
                    System.Globalization.CultureInfo.InvariantCulture,
                    "BR15: {0} may not move an order from {1} to {2}; only {3} may.",
                    actor,
                    from,
                    to,
                    row.Actor));
            }
        }

        return Refuse(string.Format(
            System.Globalization.CultureInfo.InvariantCulture,
            "BR15: the transition {0} -> {1} is not in the lifecycle table.",
            from,
            to));
    }

    /// <summary>True for Delivered, Cancelled and Failed (BR15), the three states the lifecycle ends in.</summary>
    public static bool IsTerminal(OrderStatus status) =>
        status is OrderStatus.Delivered or OrderStatus.Cancelled or OrderStatus.Failed;

    /// <summary>
    /// Every state <paramref name="actor"/> may move the order to from <paramref name="from"/>, in table order.
    /// </summary>
    /// <remarks>
    /// The UI uses this to render the buttons the actor is entitled to (FR-F2); the server still calls
    /// <see cref="CanTransition"/> because hiding a button is not enforcement (NFR4).
    /// </remarks>
    public static IReadOnlyCollection<OrderStatus> AllowedNext(OrderStatus from, ActorRole actor)
    {
        if (IsTerminal(from))
        {
            return Array.Empty<OrderStatus>();
        }

        var allowed = new List<OrderStatus>(capacity: 2);

        foreach (var row in Table)
        {
            if (row.From == from && row.Actor == actor && !allowed.Contains(row.To))
            {
                allowed.Add(row.To);
            }
        }

        return allowed;
    }

    private static TransitionResult Refuse(string reason) => new(false, reason);

    /// <summary>One row of the section C state table.</summary>
    /// <param name="From">Source state.</param>
    /// <param name="To">Target state.</param>
    /// <param name="Actor">The only actor the row authorises.</param>
    /// <param name="ReasonRequired">True for the two rows where the actor must supply a reason.</param>
    private readonly record struct Transition(
        OrderStatus From,
        OrderStatus To,
        ActorRole Actor,
        bool ReasonRequired);
}
