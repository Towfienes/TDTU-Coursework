namespace SaigonBite.Core.Orders;

/// <summary>
/// Who is asking for a state transition. BR15 authorises transitions per actor, so the actor is part of
/// the state-machine signature rather than being checked by callers.
/// </summary>
public enum ActorRole
{
    /// <summary>Local Customer or Foreign Tourist; may cancel in Placed and Confirmed (BR16).</summary>
    Customer = 0,

    /// <summary>Belongs to one hub; confirms, prepares, readies, and may reject a Placed order with a reason.</summary>
    KitchenStaff = 1,

    /// <summary>Picks up Ready orders, delivers or fails them, confirms cash collected (BR14).</summary>
    Shipper = 2,

    /// <summary>May cancel a Confirmed order, and must give a reason when doing so (ambiguity A5).</summary>
    Admin = 3,

    /// <summary>
    /// Reserved for automated transitions. The BR15 table grants no transition to the system actor, so
    /// <see cref="OrderStateMachine.CanTransition"/> refuses every request from it: a scheduler or webhook
    /// must act through the role the table names, never around the lifecycle.
    /// </summary>
    System = 4,
}
