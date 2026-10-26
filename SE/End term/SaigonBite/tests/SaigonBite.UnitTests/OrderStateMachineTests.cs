using SaigonBite.Core.Orders;
using Xunit;

namespace SaigonBite.UnitTests;

/// <summary>
/// BR15 order lifecycle and BR16 cancellation, with the ambiguity A5 reading of the reason requirement.
/// </summary>
/// <remarks>
/// BR15 requires the business layer — not the UI — to reject every transition the section C table does
/// not list. Each illegal case below therefore asserts a refusal with a non-null reason, and each legal
/// case asserts acceptance, so a permissive state machine cannot pass this suite by accident.
/// </remarks>
public sealed class OrderStateMachineIllegalTransitionTests
{
    [Fact]
    public void BR15_placed_to_preparing_is_rejected()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Preparing, ActorRole.KitchenStaff);

        Assert.False(result.Allowed);
        Assert.NotNull(result.Reason);
    }

    [Fact]
    public void BR15_placed_to_delivered_is_rejected()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Delivered, ActorRole.Shipper);

        Assert.False(result.Allowed);
        Assert.NotNull(result.Reason);
    }

    [Fact]
    public void BR15_placed_to_out_for_delivery_is_rejected()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.OutForDelivery, ActorRole.Shipper);

        Assert.False(result.Allowed);
        Assert.Contains("BR15", result.Reason!, StringComparison.Ordinal);
    }

    [Fact]
    public void BR15_placed_to_placed_is_rejected()
    {
        // A no-op is not a transition in the table, so it must not write a history row.
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Placed, ActorRole.Customer);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_customer_cannot_confirm_a_placed_order()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.Customer);

        Assert.False(result.Allowed);
        Assert.Contains("KitchenStaff", result.Reason!, StringComparison.Ordinal);
    }

    [Fact]
    public void BR15_shipper_cannot_confirm_a_placed_order()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.Shipper);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_admin_cannot_confirm_a_placed_order()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.Admin);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_kitchen_staff_cannot_deliver_an_order()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.OutForDelivery, OrderStatus.Delivered, ActorRole.KitchenStaff);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_kitchen_staff_cannot_move_ready_to_out_for_delivery()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Ready, OrderStatus.OutForDelivery, ActorRole.KitchenStaff);

        Assert.False(result.Allowed);
        Assert.Contains("Shipper", result.Reason!, StringComparison.Ordinal);
    }

    [Fact]
    public void BR16_customer_cannot_cancel_while_preparing()
    {
        // BR16: "No cancellation after Preparing".
        var result = OrderStateMachine.CanTransition(OrderStatus.Preparing, OrderStatus.Cancelled, ActorRole.Customer);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR16_customer_cannot_cancel_a_ready_order()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Ready, OrderStatus.Cancelled, ActorRole.Customer);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_delivered_is_terminal()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Delivered, OrderStatus.Confirmed, ActorRole.Admin);

        Assert.False(result.Allowed);
        Assert.Contains("terminal", result.Reason!, StringComparison.Ordinal);
    }

    [Fact]
    public void BR15_cancelled_is_terminal()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Cancelled, OrderStatus.Confirmed, ActorRole.KitchenStaff);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_failed_is_terminal()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Failed, OrderStatus.OutForDelivery, ActorRole.Shipper);

        Assert.False(result.Allowed);
    }

    [Fact]
    public void BR15_system_actor_has_no_permitted_transition()
    {
        // The BR15 table grants nothing to the system actor; automation must act through the named role.
        foreach (var from in Enum.GetValues<OrderStatus>())
        {
            foreach (var to in Enum.GetValues<OrderStatus>())
            {
                Assert.False(OrderStateMachine.CanTransition(from, to, ActorRole.System).Allowed);
                Assert.Empty(OrderStateMachine.AllowedNext(from, ActorRole.System));
            }
        }
    }

    [Fact]
    public void BR15_an_undefined_status_value_is_rejected()
    {
        var result = OrderStateMachine.CanTransition((OrderStatus)99, OrderStatus.Confirmed, ActorRole.KitchenStaff);

        Assert.False(result.Allowed);
        Assert.False(OrderStateMachine.IsTerminal((OrderStatus)99));
    }
}

/// <summary>
/// BR15/BR16 transitions the section C table permits, including the two that require a reason
/// (ambiguity A5).
/// </summary>
public sealed class OrderStateMachineLegalTransitionTests
{
    [Fact]
    public void BR15_kitchen_staff_confirming_a_placed_order_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.KitchenStaff);

        Assert.True(result.Allowed);
        Assert.Null(result.Reason);   // unconditional move: no reason to collect
    }

    [Fact]
    public void BR15_kitchen_staff_moving_confirmed_to_preparing_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Confirmed, OrderStatus.Preparing, ActorRole.KitchenStaff);

        Assert.True(result.Allowed);
        Assert.Null(result.Reason);
    }

    [Fact]
    public void BR15_kitchen_staff_marking_preparing_as_ready_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Preparing, OrderStatus.Ready, ActorRole.KitchenStaff);

        Assert.True(result.Allowed);
    }

    [Fact]
    public void BR15_shipper_picking_up_a_ready_order_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Ready, OrderStatus.OutForDelivery, ActorRole.Shipper);

        Assert.True(result.Allowed);
    }

    [Fact]
    public void BR15_shipper_delivering_an_out_for_delivery_order_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.OutForDelivery, OrderStatus.Delivered, ActorRole.Shipper);

        Assert.True(result.Allowed);
        Assert.Null(result.Reason);
    }

    [Fact]
    public void BR15_shipper_failing_an_out_for_delivery_order_is_allowed()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.OutForDelivery, OrderStatus.Failed, ActorRole.Shipper);

        Assert.True(result.Allowed);
    }

    [Fact]
    public void BR16_customer_cancelling_a_placed_order_needs_no_reason()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Cancelled, ActorRole.Customer);

        Assert.True(result.Allowed);
        Assert.Null(result.Reason);
    }

    [Fact]
    public void BR16_customer_cancelling_a_confirmed_order_needs_no_reason()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Confirmed, OrderStatus.Cancelled, ActorRole.Customer);

        Assert.True(result.Allowed);
        Assert.Null(result.Reason);
    }

    [Fact]
    public void BR16_kitchen_staff_rejecting_a_placed_order_requires_a_reason()
    {
        // A5: the move is legal, and the result carries the obligation instead of the caller.
        var result = OrderStateMachine.CanTransition(OrderStatus.Placed, OrderStatus.Cancelled, ActorRole.KitchenStaff);

        Assert.True(result.Allowed);
        Assert.Equal(OrderStateMachine.KitchenRejectionReasonRequired, result.Reason);
    }

    [Fact]
    public void A5_admin_cancelling_a_confirmed_order_requires_a_reason()
    {
        var result = OrderStateMachine.CanTransition(OrderStatus.Confirmed, OrderStatus.Cancelled, ActorRole.Admin);

        Assert.True(result.Allowed);
        Assert.Equal(OrderStateMachine.AdminCancellationReasonRequired, result.Reason);
    }

    [Fact]
    public void BR15_terminal_states_are_delivered_cancelled_and_failed()
    {
        Assert.True(OrderStateMachine.IsTerminal(OrderStatus.Delivered));
        Assert.True(OrderStateMachine.IsTerminal(OrderStatus.Cancelled));
        Assert.True(OrderStateMachine.IsTerminal(OrderStatus.Failed));

        Assert.False(OrderStateMachine.IsTerminal(OrderStatus.Placed));
        Assert.False(OrderStateMachine.IsTerminal(OrderStatus.Confirmed));
        Assert.False(OrderStateMachine.IsTerminal(OrderStatus.Preparing));
        Assert.False(OrderStateMachine.IsTerminal(OrderStatus.Ready));
        Assert.False(OrderStateMachine.IsTerminal(OrderStatus.OutForDelivery));
    }

    [Fact]
    public void BR15_allowed_next_matches_the_actor()
    {
        // A Placed order offers kitchen staff two moves and the customer one.
        Assert.Equal(
            new[] { OrderStatus.Confirmed, OrderStatus.Cancelled },
            OrderStateMachine.AllowedNext(OrderStatus.Placed, ActorRole.KitchenStaff));

        Assert.Equal(
            new[] { OrderStatus.Cancelled },
            OrderStateMachine.AllowedNext(OrderStatus.Placed, ActorRole.Customer));

        Assert.Empty(OrderStateMachine.AllowedNext(OrderStatus.Delivered, ActorRole.Admin));
    }

    [Fact]
    public void BR15_the_happy_path_runs_placed_to_delivered()
    {
        // The exact chain the specification's user story 3 walks through.
        (OrderStatus From, OrderStatus To, ActorRole Actor)[] path =
        [
            (OrderStatus.Placed, OrderStatus.Confirmed, ActorRole.KitchenStaff),
            (OrderStatus.Confirmed, OrderStatus.Preparing, ActorRole.KitchenStaff),
            (OrderStatus.Preparing, OrderStatus.Ready, ActorRole.KitchenStaff),
            (OrderStatus.Ready, OrderStatus.OutForDelivery, ActorRole.Shipper),
            (OrderStatus.OutForDelivery, OrderStatus.Delivered, ActorRole.Shipper),
        ];

        foreach (var step in path)
        {
            Assert.True(OrderStateMachine.CanTransition(step.From, step.To, step.Actor).Allowed, $"{step.From} -> {step.To}");
        }
    }
}
