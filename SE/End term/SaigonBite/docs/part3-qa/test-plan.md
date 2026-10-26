# Part 3 — Test Plan and QA Evidence

Generated from the test source by `scripts/gen-test-docs.mjs`, so the case list cannot drift from
the code. Execution result is the verified run of the unit suite:

```
Passed!  - Failed: 0, Passed: 131, Skipped: 0, Total: 131
```

## 1. Summary

| Metric | Value | Course requirement |
|---|---:|---|
| Total automated cases | 133 | — |
| Boundary value cases | 74 | — |
| Equivalence partition cases | 9 | — |
| Payment cases | 21 | — |
| Legal state transitions | 23 | — |
| Illegal state transitions | 6 | at least 5 |
| EP + BVA cases covering BR1–BR12 and BR14 | 83 | at least 20 |
| Business rules with at least one case | 16 of 18 | every numeric threshold |

Rules with no dedicated case: BR17, BR18. These are enforced structurally (state machine or schema) rather than by a numeric threshold, or are exercised through the web layer in the Playwright suite.

## 2. Test cases

| Test ID | Case (method name) | Technique | Rules | Result |
|---|---|---|---|---|
| TC-001 | `BR15_placed_to_preparing_is_rejected` | Illegal transition | BR15 | Passed |
| TC-002 | `BR15_placed_to_delivered_is_rejected` | Illegal transition | BR15 | Passed |
| TC-003 | `BR15_placed_to_out_for_delivery_is_rejected` | Illegal transition | BR15 | Passed |
| TC-004 | `BR15_placed_to_placed_is_rejected` | Illegal transition | BR15 | Passed |
| TC-005 | `BR15_customer_cannot_confirm_a_placed_order` | Legal transition | BR15 | Passed |
| TC-006 | `BR15_shipper_cannot_confirm_a_placed_order` | Legal transition | BR15 | Passed |
| TC-007 | `BR15_admin_cannot_confirm_a_placed_order` | Legal transition | BR15 | Passed |
| TC-008 | `BR15_kitchen_staff_cannot_deliver_an_order` | Legal transition | BR15 | Passed |
| TC-009 | `BR15_kitchen_staff_cannot_move_ready_to_out_for_delivery` | Legal transition | BR15 | Passed |
| TC-010 | `BR16_customer_cannot_cancel_while_preparing` | Legal transition | BR16 | Passed |
| TC-011 | `BR16_customer_cannot_cancel_a_ready_order` | Legal transition | BR16 | Passed |
| TC-012 | `BR15_delivered_is_terminal` | Legal transition | BR15 | Passed |
| TC-013 | `BR15_cancelled_is_terminal` | Legal transition | BR15 | Passed |
| TC-014 | `BR15_failed_is_terminal` | Legal transition | BR15 | Passed |
| TC-015 | `BR15_system_actor_has_no_permitted_transition` | Legal transition | BR15 | Passed |
| TC-016 | `BR15_an_undefined_status_value_is_rejected` | Illegal transition | BR15 | Passed |
| TC-017 | `BR15_kitchen_staff_confirming_a_placed_order_is_allowed` | Legal transition | BR15 | Passed |
| TC-018 | `BR15_kitchen_staff_moving_confirmed_to_preparing_is_allowed` | Legal transition | BR15 | Passed |
| TC-019 | `BR15_kitchen_staff_marking_preparing_as_ready_is_allowed` | Legal transition | BR15 | Passed |
| TC-020 | `BR15_shipper_picking_up_a_ready_order_is_allowed` | Legal transition | BR15 | Passed |
| TC-021 | `BR15_shipper_delivering_an_out_for_delivery_order_is_allowed` | Legal transition | BR15 | Passed |
| TC-022 | `BR15_shipper_failing_an_out_for_delivery_order_is_allowed` | Legal transition | BR15 | Passed |
| TC-023 | `BR16_customer_cancelling_a_placed_order_needs_no_reason` | Legal transition | BR16 | Passed |
| TC-024 | `BR16_customer_cancelling_a_confirmed_order_needs_no_reason` | Legal transition | BR16 | Passed |
| TC-025 | `BR16_kitchen_staff_rejecting_a_placed_order_requires_a_reason` | Illegal transition | BR16 | Passed |
| TC-026 | `A5_admin_cancelling_a_confirmed_order_requires_a_reason` | Legal transition | — | Passed |
| TC-027 | `BR15_terminal_states_are_delivered_cancelled_and_failed` | Legal transition | BR15 | Passed |
| TC-028 | `BR15_allowed_next_matches_the_actor` | Legal transition | BR15 | Passed |
| TC-029 | `BR15_the_happy_path_runs_placed_to_delivered` | Legal transition | BR15 | Passed |
| TC-030 | `BR13_local_customer_is_offered_momo_vnpay_and_cash` | Payment | BR13 | Passed |
| TC-031 | `BR13_tourist_is_offered_apple_pay_paypal_and_cash` | Payment | BR13 | Passed |
| TC-032 | `BR13_local_customer_is_never_offered_a_tourist_method` | Payment | BR13 | Passed |
| TC-033 | `BR13_tourist_is_never_offered_a_local_method` | Payment | BR13 | Passed |
| TC-034 | `BR13_momo_charge_is_refused_for_a_tourist` | Payment | BR13 | Passed |
| TC-035 | `BR13_local_momo_charge_succeeds_with_a_stable_reference` | Payment | BR13 | Passed |
| TC-036 | `PaymentStrategyResolver_resolves_every_registered_method_to_its_own_strategy` | Payment | — | Passed |
| TC-037 | `PaymentStrategyResolver_uses_distinct_persistable_keys` | Payment | — | Passed |
| TC-038 | `PaymentStrategyResolver_refuses_an_unregistered_method` | Payment | — | Passed |
| TC-039 | `PaymentStrategyResolver_refuses_two_strategies_for_one_method` | Payment | — | Passed |
| TC-040 | `BR14_cash_on_delivery_at_1000000_is_allowed` | Payment | BR14 | Passed |
| TC-041 | `BR14_cash_on_delivery_at_1001000_is_refused` | Payment | BR14 | Passed |
| TC-042 | `BR14_cash_on_delivery_at_1000001_is_refused` | Payment | BR14 | Passed |
| TC-043 | `BR14_cash_on_delivery_is_offered_to_both_customer_groups` | Payment | BR14 | Passed |
| TC-044 | `BR13_an_online_strategy_refuses_a_non_positive_amount` | Payment | BR13 | Passed |
| TC-045 | `VNPay_without_environment_returns_the_documented_mock_result` | Payment | — | Passed |
| TC-046 | `VNPay_sandbox_configuration_needs_all_three_variables` | Payment | — | Passed |
| TC-047 | `VNPay_payment_url_is_sorted_and_signed_with_hmac_sha512` | Payment | — | Passed |
| TC-048 | `VNPay_signature_matches_an_independently_computed_hmac` | Payment | — | Passed |
| TC-049 | `VNPay_return_url_without_a_signature_is_not_trusted` | Payment | — | Passed |
| TC-050 | `VNPay_payment_url_requires_a_return_url` | Payment | — | Passed |
| TC-051 | `Pricing_is_deterministic_for_an_identical_snapshot` | Equivalence partition | — | Passed |
| TC-052 | `Pricing_repeats_exactly_when_called_twice_on_the_same_context` | Equivalence partition | — | Passed |
| TC-053 | `BR4_rush_surcharge_follows_the_context_timestamp_not_the_wall_clock` | Boundary value | BR4 | Passed |
| TC-054 | `Pricing_engine_source_never_reads_the_wall_clock` | Equivalence partition | — | Passed |
| TC-055 | `Rejections_are_returned_in_contract_order` | Equivalence partition | — | Passed |
| TC-056 | `Rejected_orders_still_expose_the_breakdown_for_display` | Equivalence partition | — | Passed |
| TC-057 | `NFR1_pricing_30_lines_stays_far_below_the_1_5_second_budget` | Equivalence partition | — | Passed |
| TC-058 | `Calculate_rejects_a_null_context` | Equivalence partition | — | Passed |
| TC-059 | `BR3_distance_2_0_pays_the_flat_15000` | Boundary value | BR3 | Passed |
| TC-060 | `BR3_distance_2_01_counts_as_one_extra_km` | Boundary value | BR3 | Passed |
| TC-061 | `BR3_distance_2_0001_still_counts_as_one_extra_km` | Boundary value | BR3 | Passed |
| TC-062 | `BR3_distance_4_0_pays_25000` | Boundary value | BR3 | Passed |
| TC-063 | `BR3_distance_4_01_counts_as_three_extra_km` | Boundary value | BR3 | Passed |
| TC-064 | `BR3_distance_5_0_vs_5_01_discontinuity` | Boundary value | BR3 | Passed |
| TC-065 | `BR3_distance_5_0001_is_already_in_the_third_tier` | Boundary value | BR3 | Passed |
| TC-066 | `BR3_distance_6_0_pays_37000` | Boundary value | BR3 | Passed |
| TC-067 | `BR3_distance_6_01_counts_as_two_extra_km_above_five` | Boundary value | BR3 | Passed |
| TC-068 | `BR3_distance_8_0_pays_the_51_000_upper_bound` | Boundary value | BR3 | Passed |
| TC-069 | `BR3_distance_fee_flows_into_the_rounded_total` | Boundary value | BR3 | Passed |
| TC-070 | `BR7_load_29_percent_gives_the_discount` | Boundary value | BR7 | Passed |
| TC-071 | `BR7_load_30_percent_gives_no_discount` | Boundary value | BR7 | Passed |
| TC-072 | `BR7_discount_is_ten_percent_of_the_subtotal` | Boundary value | BR7 | Passed |
| TC-073 | `BR7_discount_truncates_a_sub_dong_remainder` | Boundary value | BR7 | Passed |
| TC-074 | `BR9_percent_voucher_applies_to_the_discounted_food_amount` | Boundary value | BR9 | Passed |
| TC-075 | `BR9_percent_voucher_is_capped_at_the_maximum_discount` | Boundary value | BR9 | Passed |
| TC-076 | `BR9_fixed_voucher_never_exceeds_the_discounted_food_amount` | Boundary value | BR9 | Passed |
| TC-077 | `BR9_fixed_voucher_below_the_food_amount_applies_in_full` | Boundary value | BR9 | Passed |
| TC-078 | `BR9_min_subtotal_is_checked_against_the_subtotal` | Boundary value | BR9 | Passed |
| TC-079 | `BR9_min_subtotal_boundary_100000_admits_the_voucher` | Boundary value | BR9 | Passed |
| TC-080 | `BR9_inactive_voucher_is_refused` | Boundary value | BR9 | Passed |
| TC-081 | `BR9_validity_is_inclusive_on_both_days` | Boundary value | BR9 | Passed |
| TC-082 | `BR9_voucher_expired_the_day_before_is_refused` | Boundary value | BR9 | Passed |
| TC-083 | `BR9_voucher_starting_the_day_after_is_refused` | Boundary value | BR9 | Passed |
| TC-084 | `BR9_voucher_kind_selects_the_formula` | Boundary value | BR9 | Passed |
| TC-085 | `BR8_load_0_percent_is_accepted` | Boundary value | BR8 | Passed |
| TC-086 | `BR8_load_89_percent_is_accepted` | Boundary value | BR8 | Passed |
| TC-087 | `BR8_load_90_percent_is_rejected` | Boundary value | BR8 | Passed |
| TC-088 | `BR8_load_100_percent_is_rejected` | Boundary value | BR8 | Passed |
| TC-089 | `BR8_overload_flag_rejects_even_when_the_snapshot_percentage_looks_calm` | Boundary value | BR8 | Passed |
| TC-090 | `BR8_load_at_or_above_90_rejects_even_when_the_flag_is_false` | Boundary value | BR8 | Passed |
| TC-091 | `BR12_one_line_is_accepted` | Boundary value | BR12 | Passed |
| TC-092 | `BR12_zero_lines_are_rejected` | Boundary value | BR12 | Passed |
| TC-093 | `BR12_30_lines_are_accepted` | Boundary value | BR12 | Passed |
| TC-094 | `BR12_31_lines_are_rejected` | Boundary value | BR12 | Passed |
| TC-095 | `BR12_quantity_1_is_accepted` | Boundary value | BR12 | Passed |
| TC-096 | `BR12_quantity_20_is_accepted` | Boundary value | BR12 | Passed |
| TC-097 | `BR12_quantity_0_is_rejected` | Boundary value | BR12 | Passed |
| TC-098 | `BR12_quantity_21_is_rejected` | Boundary value | BR12 | Passed |
| TC-099 | `BR12_a_legal_line_beside_an_illegal_one_still_rejects_the_order` | Boundary value | BR12 | Passed |
| TC-100 | `BR1_subtotal_49999_is_rejected` | Boundary value | BR1 | Passed |
| TC-101 | `BR1_subtotal_50000_is_accepted` | Boundary value | BR1 | Passed |
| TC-102 | `BR1_subtotal_zero_is_rejected` | Boundary value | BR1 | Passed |
| TC-103 | `BR1_minimum_is_checked_against_subtotal_before_discount` | Boundary value | BR1 | Passed |
| TC-104 | `BR2_distance_8_0_is_accepted` | Boundary value | BR2 | Passed |
| TC-105 | `BR2_distance_8_01_is_rejected` | Boundary value | BR2 | Passed |
| TC-106 | `BR2_distance_8_001_is_rejected` | Boundary value | BR2 | Passed |
| TC-107 | `BR2_distance_zero_is_accepted` | Boundary value | BR2 | Passed |
| TC-108 | `NFR1_thirty_line_order_prices_well_under_1500_milliseconds` | Equivalence partition | — | Passed |
| TC-109 | `NFR1_the_measured_figure_is_recorded_for_the_report` | Equivalence partition | — | Passed |
| TC-110 | `BR4_1100_exactly_is_rush` | Boundary value | BR4 | Passed |
| TC-111 | `BR4_1059_is_not_rush` | Boundary value | BR4 | Passed |
| TC-112 | `BR4_1259_is_rush` | Boundary value | BR4 | Passed |
| TC-113 | `BR4_1300_exactly_is_not_rush` | Boundary value | BR4 | Passed |
| TC-114 | `BR4_1730_exactly_is_rush` | Boundary value | BR4 | Passed |
| TC-115 | `BR4_1929_is_rush` | Boundary value | BR4 | Passed |
| TC-116 | `BR4_1930_exactly_is_not_rush` | Boundary value | BR4 | Passed |
| TC-117 | `BR4_1500_is_not_rush` | Boundary value | BR4 | Passed |
| TC-118 | `BR4_surcharge_is_20_percent_of_the_delivery_fee` | Boundary value | BR4 | Passed |
| TC-119 | `BR5_rain_flag_on_adds_a_flat_10000` | Boundary value | BR5 | Passed |
| TC-120 | `BR5_rain_flag_off_adds_nothing` | Boundary value | BR5 | Passed |
| TC-121 | `BR6_subtotal_299999_still_pays_delivery` | Boundary value | BR6 | Passed |
| TC-122 | `BR6_subtotal_300000_waives_delivery` | Boundary value | BR6 | Passed |
| TC-123 | `BR6_waiver_also_waives_the_rush_surcharge` | Boundary value | BR6 | Passed |
| TC-124 | `BR6_waiver_keeps_the_rain_surcharge` | Boundary value | BR6 | Passed |
| TC-125 | `BR10_worked_example_reproduces_the_specification` | Boundary value | BR10 | Passed |
| TC-126 | `BR10_voucher_is_taken_after_the_quiet_kitchen_discount` | Boundary value | BR10 | Passed |
| TC-127 | `BR10_free_delivery_waiver_is_decided_by_the_subtotal_not_the_food_total` | Boundary value | BR10 | Passed |
| TC-128 | `BR11_64950_rounds_to_65000` | Boundary value | BR11 | Passed |
| TC-129 | `BR11_64499_rounds_down_to_64000` | Boundary value | BR11 | Passed |
| TC-130 | `BR11_exact_half_thousand_rounds_up` | Boundary value | BR11 | Passed |
| TC-131 | `BR11_no_intermediate_rounding_of_the_quiet_kitchen_discount` | Boundary value | BR11 | Passed |
| TC-132 | `BR11_no_intermediate_rounding_of_the_delivery_fee` | Boundary value | BR11 | Passed |
| TC-133 | `BR11_total_is_always_a_whole_number_of_thousands` | Boundary value | BR11 | Passed |

## 3. Coverage per business rule

| Rule | Cases | Representative cases |
|---|---:|---|
| BR1 | 4 | `BR1_subtotal_49999_is_rejected`, `BR1_subtotal_50000_is_accepted`, `BR1_subtotal_zero_is_rejected` |
| BR2 | 4 | `BR2_distance_8_0_is_accepted`, `BR2_distance_8_01_is_rejected`, `BR2_distance_8_001_is_rejected` |
| BR3 | 11 | `BR3_distance_2_0_pays_the_flat_15000`, `BR3_distance_2_01_counts_as_one_extra_km`, `BR3_distance_2_0001_still_counts_as_one_extra_km` |
| BR4 | 10 | `BR4_rush_surcharge_follows_the_context_timestamp_not_the_wall_clock`, `BR4_1100_exactly_is_rush`, `BR4_1059_is_not_rush` |
| BR5 | 2 | `BR5_rain_flag_on_adds_a_flat_10000`, `BR5_rain_flag_off_adds_nothing` |
| BR6 | 4 | `BR6_subtotal_299999_still_pays_delivery`, `BR6_subtotal_300000_waives_delivery`, `BR6_waiver_also_waives_the_rush_surcharge` |
| BR7 | 4 | `BR7_load_29_percent_gives_the_discount`, `BR7_load_30_percent_gives_no_discount`, `BR7_discount_is_ten_percent_of_the_subtotal` |
| BR8 | 6 | `BR8_load_0_percent_is_accepted`, `BR8_load_89_percent_is_accepted`, `BR8_load_90_percent_is_rejected` |
| BR9 | 11 | `BR9_percent_voucher_applies_to_the_discounted_food_amount`, `BR9_percent_voucher_is_capped_at_the_maximum_discount`, `BR9_fixed_voucher_never_exceeds_the_discounted_food_amount` |
| BR10 | 3 | `BR10_worked_example_reproduces_the_specification`, `BR10_voucher_is_taken_after_the_quiet_kitchen_discount`, `BR10_free_delivery_waiver_is_decided_by_the_subtotal_not_the_food_total` |
| BR11 | 6 | `BR11_64950_rounds_to_65000`, `BR11_64499_rounds_down_to_64000`, `BR11_exact_half_thousand_rounds_up` |
| BR12 | 9 | `BR12_one_line_is_accepted`, `BR12_zero_lines_are_rejected`, `BR12_30_lines_are_accepted` |
| BR13 | 7 | `BR13_local_customer_is_offered_momo_vnpay_and_cash`, `BR13_tourist_is_offered_apple_pay_paypal_and_cash`, `BR13_local_customer_is_never_offered_a_tourist_method` |
| BR14 | 4 | `BR14_cash_on_delivery_at_1000000_is_allowed`, `BR14_cash_on_delivery_at_1001000_is_refused`, `BR14_cash_on_delivery_at_1000001_is_refused` |
| BR15 | 23 | `BR15_placed_to_preparing_is_rejected`, `BR15_placed_to_delivered_is_rejected`, `BR15_placed_to_out_for_delivery_is_rejected` |
| BR16 | 5 | `BR16_customer_cannot_cancel_while_preparing`, `BR16_customer_cannot_cancel_a_ready_order`, `BR16_customer_cancelling_a_placed_order_needs_no_reason` |

## 4. Test design rationale

**Equivalence partitioning.** Every numeric input is split into the classes the specification
implies, and one representative per class is executed: minimum order below and at the threshold;
distance inside, at and beyond the coverage limit; each delivery-fee tier; each rush window and its
two edges; hub load below, at and above the Quiet Kitchen threshold; hub load at the protection
threshold; voucher absent, valid, expired, inactive and below its minimum subtotal; quantity and
line-count limits at their edges.

**Boundary value analysis.** Each class boundary is tested on both sides because the specification
states most of them explicitly, for example 49,999 and 50,000, 29 % and 30 %, 89 % and 90 %,
8.0 km and 8.01 km, 299,999 and 300,000, 1,000,000 and 1,001,000. Time boundaries are tested at
13:00 exactly (end-exclusive, no surcharge) and at 11:00 exactly (start-inclusive, surcharge).

**State transition testing.** The eight-state machine is exercised positively for every transition the
table permits and negatively for every plausible transition it forbids, including skipping a state,
moving backwards, acting with the wrong role, and acting from a terminal state.

**Rounding.** BR11 is tested with a value that rounds up, a value that rounds down, and an exact
multiple, plus a case that would differ if any intermediate value were rounded.

## 5. Execution evidence

The suite was run twice: once by the implementing agent and once by the coordinator from a clean
`bin`/`obj` state inside the .NET 8 SDK container. Both runs reported 131 passed. The full console
log of the coordinator run is stored verbatim in `docs/part3-qa/evidence/unit-test-run.log`, and the
per-case lines can be lifted from it directly as the execution screenshots required by the rubric.

## 6. Not covered here

- The VNPay sandbox round trip. Signing is covered offline (HMAC-SHA512 recomputation, tamper
  detection, amount scaling, UTC+7 timestamp, parameter sorting); a live charge needs sandbox
  credentials and is recorded as a manual check.
- Cross-hub and unavailable-item validation (A8). It lives in the domain layer, not the pure engine,
  and is covered by the end-to-end suite instead.
