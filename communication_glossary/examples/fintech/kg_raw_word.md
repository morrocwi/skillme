# kg_raw_word — HYP-SKILLME-046-DEMO-001

**PROTOTYPE output.** Raw, typed, fully-traceable word extraction — not a semantic KG yet. No relation was invented; every edge below reflects only "this word literally appeared in this schema field of this source." See the script docstring for the stated tokenization limitation (unspaced formal Thai/CJK under-tokenizes).

## DAG (Mermaid)

```mermaid
flowchart TD
  CKPT["HYP-SKILLME-046-DEMO-001"]
  CKPT --> CARD_H1_106530dc["H1"]
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_ROLE_612f9988["ROLE"]
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_R_D___Ops__24x7__4a02c46c(["R#amp;D / Ops (24x7)"])
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_merchant__north_cluster___Tier_1__dac36fa9(["merchant #quot;north-cluster#quot; (Tier-1)"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_202_854d6fae(["202"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_Accepted_382ab522(["Accepted"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_AcquirerX_19df5fd9(["AcquirerX"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SETTLED_47022477(["SETTLED"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_actual_5157e3c7(["actual"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_attempt_id_3b71ae7c(["attempt-id"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_callback_924a8cee(["callback"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_double_reads_4324ff2d(["double-reads"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_due_d6692dd3(["due"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_flag_327a6c43(["flag"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_join_731b886d(["join"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_key_3c6e0b8a(["key"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_later_c18788c2(["later"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ledger_f48139f3(["ledger"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_never_c7561db7(["never"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_non_idempotent_a76d84af(["non-idempotent"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_overwrites_bbbb0966(["overwrites"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_premature_d85df52e(["premature"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_queue_ack_92a81b16(["queue-ack"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_receiving_0639f5c0(["receiving"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reconciliation_job_468a33d7(["reconciliation-job"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_retry_orchestrator_51d5a553(["retry-orchestrator"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_row_f1965a85(["row"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_same_51037a4a(["same"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_settlement_6767f5cd(["settlement"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_soft_decline_4f047596(["soft-decline"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_status_9acb4454(["status"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_vendor_7c3613db(["vendor"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_waiting_cb05cab6(["waiting"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_without_fc0cb42f(["without"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_writes_4dcc865d(["writes"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_202_854d6fae(["202"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_HTTP_293c9ea2(["HTTP"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_SETTLED_47022477(["SETTLED"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_ack_82d7ba7e(["ack"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_after_632a2406(["after"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_because_cc70865f(["because"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_callback_924a8cee(["callback"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_confirmed_eda721c5(["confirmed"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_conflated_d068a704(["conflated"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_cycle_9a4c0740(["cycle"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_double_counted_7e5d2102(["double-counted"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_early_2b3de800(["early"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_edge_09039bd1(["edge"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_fire_015f28b9(["fire"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_fires_371fbb05(["fires"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_nack_ab678d51(["nack"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_one_f97c5d29(["one"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_only_6299ba2c(["only"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_payment_f83c2a85(["payment"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_queue_a9d1cbf7(["queue"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_rate_67942503(["rate"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_rather_7c67f786(["rather"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_receipt_1e11b989(["receipt"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_reconciliation_383da6cb(["reconciliation"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_reduces_829f7c77(["reduces"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_reverting_f5366d3e(["reverting"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_settlement_6767f5cd(["settlement"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_soft_decline_4f047596(["soft-decline"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_sprint_1d08fdad(["sprint"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_success_260ca9dd(["success"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_toward_b5b61165(["toward"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_trigger_c7d08e09(["trigger"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_within_60df9e64(["within"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_write_settled_flag_9b745c33(["write-settled-flag"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_zero_d02c4c4c(["zero"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_KNOWN_DIRECT_d19064ee(["KNOWN_DIRECT"])
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_MECHANISM_HYPOTHESIS_4174f82e(["MECHANISM_HYPOTHESIS"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_06_faeac4e1(["06"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_91_54229abf(["91"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_96_26657d5f(["96"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_SETTLED_47022477(["SETTLED"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_acquirer_4cb3ff0d(["acquirer"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_after_632a2406(["after"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_attempt_1db222fe(["attempt"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_attempt_id_3b71ae7c(["attempt-id"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_code_c1336794(["code"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_confirms_ac81e7f2(["confirms"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_even_cc935c5f(["even"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_ledger_f48139f3(["ledger"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_level_c9e9a848(["level"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_response_d1fc8eaf(["response"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_soft_decline_ed276a07(["soft_decline"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_status_9acb4454(["status"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_stays_9e6d6bcf(["stays"])
  CKPT --> CARD_H2_ca2bf3f6["H2"]
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_ROLE_612f9988["ROLE"]
  CARD_H2_ca2bf3f6_BKT_ROLE_612f9988 --> W_ROLE_Payments_Risk___Controls__PRC____on_call_b3d6a422(["Payments Risk #amp; Controls (PRC) — on-call"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H2_ca2bf3f6(["H2"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ack_82d7ba7e(["ack"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_actual_5157e3c7(["actual"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_adapted_fcb84bd2(["adapted"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_any_100b8cad(["any"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_appointments_2417b532(["appointments"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_backend_b43fdd98(["backend"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_before_2f444175(["before"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_behind_9da3be8f(["behind"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_being_3f4cede6(["being"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_booking_service_12aeaaf3(["booking-service"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_bug_ae0e4bda(["bug"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_callback_924a8cee(["callback"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cause_560220fc(["cause"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_caused_68ebfd66(["caused"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_client_62608e08(["client"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cross_domain_7c31144f(["cross-domain"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_delivery_71085379(["delivery"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_double_booked_8decb716(["double-booked"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_each_933dd867(["each"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_external_facing_0a61a4a2(["external-facing"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_failure_3ee28fe1(["failure"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_final_2a1585a8(["final"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_fix_8ab87d4f(["fix"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_fixture_4cf9d4f0(["fixture"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_gate_63d721d2(["gate"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_has_3309a7a7(["has"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_intermediate_438fa616(["intermediate"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_layer_f56b53e4(["layer"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_nack_ab678d51(["nack"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_never_c7561db7(["never"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_observing_ea523468(["observing"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_only_6299ba2c(["only"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_other_795f3202(["other"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_pattern_240bf022(["pattern"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_payments_84d5eaf7(["payments"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_premature_ack_as_success_e2a1498b(["premature-ack-as-success"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_queue_ack_92a81b16(["queue-ack"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reached_f910ff3a(["reached"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_resemble_a64842c2(["resemble"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_root_63a9f0ea(["root"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_same_51037a4a(["same"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_settlement_6767f5cd(["settlement"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_settlement_callback_d1dabc7a(["settlement-callback"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_state_9ed39e2e(["state"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_status_9acb4454(["status"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_structurally_b9ab462a(["structurally"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_superficially_99acbea8(["superficially"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_systems_b31df235(["systems"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_terminal_ede997b0(["terminal"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_treated_c786b555(["treated"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_truth_state_8c6b2672(["truth-state"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_two_b8a9f715(["two"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_unrelated_13ec785f(["unrelated"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_write_efb2a684(["write"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_PENDING_CONFIRMATION_fc992c93(["PENDING_CONFIRMATION"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_accepted_3e4d891a(["accepted"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_acknowledgement_04217844(["acknowledgement"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_acquirer_specific_e28f0d1b(["acquirer-specific"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_already_1ebf4e55(["already"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_ambiguous_SETTLED_1177bdfe(["ambiguous-SETTLED"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_because_cc70865f(["because"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_between_2942c466(["between"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_booking_service_12aeaaf3(["booking-service"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_both_f6cb3e81(["both"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_bugs_e3255bae(["bugs"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_business_layer_9ccfb9e8(["business-layer"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_class_a2f2ed4f(["class"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_collapse_1a721faf(["collapse"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_explicit_e2a3307d(["explicit"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_fix_8ab87d4f(["fix"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_fixture_4cf9d4f0(["fixture"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_intermediate_438fa616(["intermediate"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_introducing_d6c70a13(["introducing"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_logic_c3d3c17b(["logic"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_machine_14754f13(["machine"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_mirroring_34aa5604(["mirroring"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_models_ac5552fd(["models"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_needing_58772862(["needing"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_neither_edab6496(["neither"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_request_10573b87(["request"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_resolved_fafdd4fb(["resolved"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_resolves_c48463d3(["resolves"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_retry_orchestrator_51d5a553(["retry-orchestrator"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_state_9ed39e2e(["state"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_systems_b31df235(["systems"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_terminal_ede997b0(["terminal"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_transport_layer_868095d7(["transport-layer"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_validated_c9e825f4(["validated"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_without_fc0cb42f(["without"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_CROSS_ADAPTIVE_3397cb59(["CROSS_ADAPTIVE"])
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_STRUCTURAL_HYPOTHESIS_6aa85034(["STRUCTURAL_HYPOTHESIS"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_PENDING_CONFIRMATION_fc992c93(["PENDING_CONFIRMATION"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_SETTLED_47022477(["SETTLED"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_absence_351be24a(["absence"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_ack_82d7ba7e(["ack"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_adding_732f3800(["adding"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_between_2942c466(["between"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_callback_924a8cee(["callback"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_change_eb399bca(["change"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_does_5440e70c(["does"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_double_counted_7e5d2102(["double-counted"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_explicit_e2a3307d(["explicit"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_presence_362b908e(["presence"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_rate_67942503(["rate"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_row_f1965a85(["row"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_settlement_6767f5cd(["settlement"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_state_9ed39e2e(["state"])
  CKPT --> CARD_H3_b1476321["H3"]
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_ROLE_612f9988["ROLE"]
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_M_ller___QA_lead___6f13c5a5(["Müller — QA lead 🔧"])
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_Reconciliation___Ledger_Integrity__R_LI__239d96ad(["Reconciliation #amp; Ledger Integrity (R#amp;LI) board"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_FAILED_b9e14d9b(["FAILED"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H3_b1476321(["H3"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_LI_14efbb26(["LI"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_PENDING_c69f06e1(["PENDING"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SETTLED_47022477(["SETTLED"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_acquirer_response_code_0354891a(["acquirer-response-code"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_acquirer_timestamp_155441c3(["acquirer-timestamp"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_append_only_d07754a4(["append-only"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_attempt_id_3b71ae7c(["attempt-id"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_because_cc70865f(["because"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_benefit_b4aea98a(["benefit"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_binary_9d7183f1(["binary"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_bugs_e3255bae(["bugs"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cached_1fb1a060(["cached"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_callback_924a8cee(["callback"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_class_a2f2ed4f(["class"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_condition_3f9178c2(["condition"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_confirmed_eda721c5(["confirmed"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_consumer_1005b14b(["consumer"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_corrupt_bc2f39d4(["corrupt"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cost_4e1566f0(["cost"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_dashboard_dc7161be(["dashboard"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_deriving_31b45332(["deriving"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_downstream_d22a0a80(["downstream"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_entire_1b4a4d90(["entire"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_entirely_b56a6cab(["entirely"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_every_83ab982d(["every"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_existing_f4e0ac58(["existing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_extract_3e40063e(["extract"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_field_06e3d36f(["field"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_fix_8ab87d4f(["fix"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_gating_af8991f3(["gating"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_generative_e15ee067(["generative"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_instead_8dee4916(["instead"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_keyed_87d4c7ad(["keyed"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_label_d304ba20(["label"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ledger_f48139f3(["ledger"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_log_dc1d71bb(["log"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_longer_67c35b06(["longer"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_merchant_4c94e311(["merchant"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_merchant_facing_cd8d075b(["merchant-facing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_migration_b439f9bb(["migration"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_mutable_3fdc2faf(["mutable"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_narrower_9b62ba57(["narrower"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_outweighs_62d9db1e(["outweighs"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_premature_write_8eaaa2a3(["premature-write"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_projection_dfa55578(["projection"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_pure_6b341881(["pure"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_race_2e2a7a2e(["race"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_read_time_72294a4e(["read-time"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reads_0fb9cf5f(["reads"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reconciliation_job_468a33d7(["reconciliation-job"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_redesign_bb906f0b(["redesign"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_removes_0f7a1ea5(["removes"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_replacing_c261679e(["replacing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_report_e98d2f00(["report"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_rewrite_7b4639e8(["rewrite"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_same_51037a4a(["same"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_scope_31a1fd14(["scope"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_settlement_event_08b42710(["settlement-event"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_simply_8a511f20(["simply"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_single_dd5c0703(["single"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_status_9acb4454(["status"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_structurally_b9ab462a(["structurally"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_tax_reporting_6f48aa1c(["tax-reporting"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_there_d850f04c(["there"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_truth_59d42c50(["truth"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_variance_7d921b1f(["variance"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_versus_dacf9980(["versus"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_write_efb2a684(["write"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_SETTLED_47022477(["SETTLED"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_after_632a2406(["after"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_already_emitted_0ccba185(["already-emitted"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_because_cc70865f(["because"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_becomes_962fdda7(["becomes"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_bug_ae0e4bda(["bug"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_can_2c61ebff(["can"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_class_a2f2ed4f(["class"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_construction_f5355504(["construction"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_consumer_1005b14b(["consumer"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_cost_4e1566f0(["cost"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_double_counted_7e5d2102(["double-counted"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_downstream_d22a0a80(["downstream"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_eliminates_baf43d0d(["eliminates"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_event_41196390(["event"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_event_sourced_90a6c58c(["event-sourced"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_every_83ab982d(["every"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_log_dc1d71bb(["log"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_merely_29de3e94(["merely"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_migration_b439f9bb(["migration"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_moving_7b3ef1b1(["moving"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_mutable_status_a61520bb(["mutable-status"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_overwrite_77dced08(["overwrite"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_projection_dfa55578(["projection"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_races_b065afb8(["races"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_rate_67942503(["rate"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_rather_7c67f786(["rather"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_read_ecae1311(["read"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_reduced_282fabc3(["reduced"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_requiring_1aacfd45(["requiring"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_retroactively_1793b98b(["retroactively"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_rewritten_5462c0d7(["rewritten"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_row_f1965a85(["row"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_settlement_6767f5cd(["settlement"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_settlement_event_08b42710(["settlement-event"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_single_dd5c0703(["single"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_state_9ed39e2e(["state"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_structurally_b9ab462a(["structurally"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_undefined_5e543256(["undefined"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_write_efb2a684(["write"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_write_ordering_3e0f5bd5(["write-ordering"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_DESIGN_HYPOTHESIS_0354f2a8(["DESIGN_HYPOTHESIS"])
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_GENERATIVE_TRANSFORMATIVE_5daf45b4(["GENERATIVE_TRANSFORMATIVE"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_FAILED_b9e14d9b(["FAILED"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_SETTLED_47022477(["SETTLED"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_attempt_id_3b71ae7c(["attempt-id"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_can_2c61ebff(["can"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_coexist_4ec6fa00(["coexist"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_conflicting_5b8a0d83(["conflicting"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_consistent_3a6713de(["consistent"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_defined_7238ac6d(["defined"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_event_sourced_90a6c58c(["event-sourced"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_every_83ab982d(["every"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_historical_dff1dc0a(["historical"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_label_d304ba20(["label"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_layer_f56b53e4(["layer"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_manual_3c78b355(["manual"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_migrating_b67030be(["migrating"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_model_20f35e63(["model"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_permits_c2f28daa(["permits"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_projection_dfa55578(["projection"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_reconciliation_383da6cb(["reconciliation"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_reconstruct_17e53f7c(["reconstruct"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_resolution_b7e164b3(["resolution"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_rule_981c1e7b(["rule"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_same_51037a4a(["same"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_settlement_events_262b4aea(["settlement-events"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_still_df55340f(["still"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_two_b8a9f715(["two"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_whether_7d767e6b(["whether"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_without_fc0cb42f(["without"])
  CKPT --> CKPT_BKT_ROLE_612f9988["ROLE (checkpoint-level)"]
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_M_ller___QA_lead___6f13c5a5(["Müller — QA lead 🔧"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_Payments_Risk___Controls__PRC____on_call_b3d6a422(["Payments Risk #amp; Controls (PRC) — on-call"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_R_D___Ops__24x7__4a02c46c(["R#amp;D / Ops (24x7)"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_cardholder_c119760d(["cardholder"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_merchant__north_cluster___Tier_1__dac36fa9(["merchant #quot;north-cluster#quot; (Tier-1)"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_merchant_support_desk_949057ab(["merchant support desk"])
  CKPT --> CKPT_BKT_PROCESS_b93c1384["PROCESS (checkpoint-level)"]
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_ack_nack__soft_decline__394bda31(["ack/nack (soft-decline)"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_reconcile_378d4158(["reconcile"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_submit_retry_067d3d92(["submit-retry"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_write_settled_flag_9b745c33(["write-settled-flag"])
  CKPT --> CKPT_BKT_TOOL_6d968f54["TOOL (checkpoint-level)"]
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_acquirer_gateway__AcquirerX___prod__92411475(["acquirer-gateway #quot;AcquirerX#quot; (prod)"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_ledger_writer__async_batch__7011f194(["ledger-writer (async/batch)"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_reconciliation_job__nightly__02_00_ICT__cd8da869(["reconciliation-job (nightly, 02:00 ICT)"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_retry_orchestrator__north_wing__82d277c3(["retry-orchestrator #quot;north wing#quot;"])
  CKPT --> CKPT_BKT_PROTOCOL_83a59f45["PROTOCOL (checkpoint-level)"]
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_ISO_8583__field_39__mapping_a0e796e0(["ISO-8583 #quot;field 39#quot; mapping"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_Phase_2__draft__review_1dc11dd8(["Phase-2 (draft) review"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_TARGETED_SEARCH__Phase_2__draft___87d1132d(["TARGETED_SEARCH #quot;Phase-2 (draft)#quot;"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_canary_gateway__5__traffic__1a48da3f(["canary gateway (5% traffic)"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_idempotency_key_protocol_v2_757ad483(["idempotency-key protocol v2"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_shadow_write__no_op__mode_db2fbb44(["shadow-write #quot;no-op#quot; mode"])
  CKPT --> CKPT_BKT_METRIC_d83e9b0c["METRIC (checkpoint-level)"]
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_01_96a3be3c(["01"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_06_faeac4e1(["06"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_91_54229abf(["91"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_96_26657d5f(["96"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_SETTLED_47022477(["SETTLED"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_acquirer_4cb3ff0d(["acquirer"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_code_c1336794(["code"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_double_counted_7e5d2102(["double-counted"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_field_06e3d36f(["field"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_ledger_f48139f3(["ledger"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_machine_14754f13(["machine"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_rate_67942503(["rate"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_response_d1fc8eaf(["response"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_retry_state_b7cf8aea(["retry-state"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_soft_decline_4f047596(["soft-decline"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_status_9acb4454(["status"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC________4e0eb75e(["ต่อวัน"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_________f5819035(["ต่ำกว่า"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_________________92a12558(["ยังถูกเขียนเป็น"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC________6898449d(["วัดจาก"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC______5e201eb9(["หรือ"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_________9b3fff14(["หลังแก้"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC__________4f8673d9(["เทียบกับ"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC____20d277f4(["ใน"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_________de9290cb(["ไม่ลดลง"])
```

## Word table (deduped, every source kept)

| word | type | occurrences | sources |
|---|---|---|---|
| `202` | CONCEPT | 1 | H1:claim |
| `Accepted` | CONCEPT | 1 | H1:claim |
| `AcquirerX` | CONCEPT | 1 | H1:claim |
| `FAILED` | CONCEPT | 1 | H3:claim |
| `H1` | CONCEPT | 2 | H1:citation_cards.title, H3:alternative_explanations |
| `H2` | CONCEPT | 1 | H2:citation_cards.title |
| `H3` | CONCEPT | 1 | H3:citation_cards.title |
| `LI` | CONCEPT | 1 | H3:claim |
| `PENDING` | CONCEPT | 1 | H3:claim |
| `SETTLED` | CONCEPT | 3 | H1:claim, H3:claim |
| `SimulatedData` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `ack` | CONCEPT | 1 | H2:claim |
| `acquirer-response-code` | CONCEPT | 1 | H3:claim |
| `acquirer-timestamp` | CONCEPT | 1 | H3:claim |
| `actual` | CONCEPT | 2 | H1:claim, H2:claim |
| `adapted` | CONCEPT | 1 | H2:claim |
| `any` | CONCEPT | 1 | H2:claim |
| `append-only` | CONCEPT | 2 | H3:claim |
| `appointments` | CONCEPT | 1 | H2:claim |
| `attempt-id` | CONCEPT | 2 | H1:claim, H3:claim |
| `backend` | CONCEPT | 1 | H2:claim |
| `because` | CONCEPT | 1 | H3:claim |
| `before` | CONCEPT | 1 | H2:claim |
| `behind` | CONCEPT | 2 | H2:claim |
| `being` | CONCEPT | 1 | H2:claim |
| `benefit` | CONCEPT | 1 | H3:alternative_explanations |
| `binary` | CONCEPT | 1 | H3:claim |
| `booking-service` | CONCEPT | 1 | H2:claim |
| `bug` | CONCEPT | 1 | H2:alternative_explanations |
| `bugs` | CONCEPT | 1 | H3:claim |
| `cached` | CONCEPT | 1 | H3:claim |
| `callback` | CONCEPT | 3 | H1:claim, H2:claim, H3:alternative_explanations |
| `cause` | CONCEPT | 1 | H2:alternative_explanations |
| `caused` | CONCEPT | 1 | H2:claim |
| `class` | CONCEPT | 1 | H3:claim |
| `client` | CONCEPT | 1 | H2:claim |
| `condition` | CONCEPT | 1 | H3:claim |
| `confirmed` | CONCEPT | 1 | H3:alternative_explanations |
| `consumer` | CONCEPT | 1 | H3:claim |
| `corrupt` | CONCEPT | 1 | H3:claim |
| `cost` | CONCEPT | 1 | H3:alternative_explanations |
| `cross-domain` | CONCEPT | 1 | H2:claim |
| `dashboard` | CONCEPT | 1 | H3:claim |
| `delivery` | CONCEPT | 1 | H2:alternative_explanations |
| `deriving` | CONCEPT | 1 | H3:claim |
| `double-booked` | CONCEPT | 1 | H2:claim |
| `double-reads` | CONCEPT | 1 | H1:alternative_explanations |
| `downstream` | CONCEPT | 2 | H3:alternative_explanations, H3:claim |
| `due` | CONCEPT | 1 | H1:alternative_explanations |
| `each` | CONCEPT | 1 | H2:alternative_explanations |
| `entire` | CONCEPT | 1 | H3:claim |
| `entirely` | CONCEPT | 1 | H3:claim |
| `every` | CONCEPT | 1 | H3:claim |
| `evidence` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `existing` | CONCEPT | 1 | H3:alternative_explanations |
| `external-facing` | CONCEPT | 1 | H2:claim |
| `extract` | CONCEPT | 1 | H3:claim |
| `failure` | CONCEPT | 1 | H2:claim |
| `field` | CONCEPT | 2 | H3:claim |
| `final` | CONCEPT | 1 | H2:claim |
| `fix` | CONCEPT | 2 | H2:claim, H3:alternative_explanations |
| `fixture` | CONCEPT | 1 | H2:claim |
| `flag` | CONCEPT | 1 | H1:claim |
| `gate` | CONCEPT | 1 | H2:claim |
| `gating` | CONCEPT | 1 | H3:alternative_explanations |
| `generative` | CONCEPT | 1 | H3:claim |
| `has` | CONCEPT | 1 | H2:alternative_explanations |
| `instead` | CONCEPT | 1 | H3:claim |
| `intermediate` | CONCEPT | 1 | H2:claim |
| `join` | CONCEPT | 1 | H1:alternative_explanations |
| `key` | CONCEPT | 1 | H1:alternative_explanations |
| `keyed` | CONCEPT | 1 | H3:claim |
| `label` | CONCEPT | 2 | H3:claim |
| `later` | CONCEPT | 1 | H1:claim |
| `layer` | CONCEPT | 1 | H2:alternative_explanations |
| `ledger` | CONCEPT | 3 | H1:alternative_explanations, H1:claim, H3:claim |
| `log` | CONCEPT | 2 | H3:claim |
| `longer` | CONCEPT | 1 | H3:claim |
| `merchant` | CONCEPT | 1 | H3:claim |
| `merchant-facing` | CONCEPT | 1 | H3:claim |
| `migration` | CONCEPT | 1 | H3:alternative_explanations |
| `mutable` | CONCEPT | 1 | H3:claim |
| `nack` | CONCEPT | 1 | H2:claim |
| `narrower` | CONCEPT | 1 | H3:alternative_explanations |
| `never` | CONCEPT | 2 | H1:claim, H2:claim |
| `non-idempotent` | CONCEPT | 1 | H1:alternative_explanations |
| `observing` | CONCEPT | 1 | H2:claim |
| `only` | CONCEPT | 1 | H2:alternative_explanations |
| `other` | CONCEPT | 1 | H2:alternative_explanations |
| `outweighs` | CONCEPT | 1 | H3:alternative_explanations |
| `overwrites` | CONCEPT | 1 | H1:claim |
| `pattern` | CONCEPT | 2 | H2:claim |
| `payments` | CONCEPT | 2 | H2:alternative_explanations, H2:claim |
| `premature` | CONCEPT | 1 | H1:claim |
| `premature-ack-as-success` | CONCEPT | 1 | H2:claim |
| `premature-write` | CONCEPT | 1 | H3:claim |
| `projection` | CONCEPT | 1 | H3:claim |
| `pure` | CONCEPT | 1 | H3:claim |
| `queue-ack` | CONCEPT | 3 | H1:claim, H2:claim |
| `race` | CONCEPT | 1 | H3:claim |
| `reached` | CONCEPT | 1 | H2:claim |
| `read-time` | CONCEPT | 1 | H3:claim |
| `reads` | CONCEPT | 1 | H3:claim |
| `receiving` | CONCEPT | 1 | H1:claim |
| `reconciliation-job` | CONCEPT | 2 | H1:alternative_explanations, H3:claim |
| `record` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `redesign` | CONCEPT | 1 | H3:claim |
| `removes` | CONCEPT | 1 | H3:claim |
| `replacing` | CONCEPT | 1 | H3:claim |
| `report` | CONCEPT | 1 | H3:claim |
| `resemble` | CONCEPT | 1 | H2:alternative_explanations |
| `retry-orchestrator` | CONCEPT | 1 | H1:claim |
| `rewrite` | CONCEPT | 1 | H3:alternative_explanations |
| `root` | CONCEPT | 1 | H2:alternative_explanations |
| `row` | CONCEPT | 1 | H1:alternative_explanations |
| `same` | CONCEPT | 5 | H1:alternative_explanations, H1:claim, H2:claim, H3:claim |
| `scope` | CONCEPT | 1 | H3:alternative_explanations |
| `settlement` | CONCEPT | 2 | H1:claim, H2:claim |
| `settlement-callback` | CONCEPT | 1 | H2:alternative_explanations |
| `settlement-event` | CONCEPT | 1 | H3:claim |
| `simply` | CONCEPT | 1 | H3:alternative_explanations |
| `single` | CONCEPT | 1 | H3:claim |
| `soft-decline` | CONCEPT | 1 | H1:claim |
| `state` | CONCEPT | 1 | H2:claim |
| `status` | CONCEPT | 4 | H1:claim, H2:claim, H3:claim |
| `structurally` | CONCEPT | 2 | H2:claim, H3:claim |
| `superficially` | CONCEPT | 1 | H2:alternative_explanations |
| `systems` | CONCEPT | 1 | H2:alternative_explanations |
| `tax-reporting` | CONCEPT | 1 | H3:claim |
| `terminal` | CONCEPT | 1 | H2:claim |
| `there` | CONCEPT | 1 | H3:claim |
| `treated` | CONCEPT | 1 | H2:claim |
| `truth` | CONCEPT | 1 | H3:claim |
| `truth-state` | CONCEPT | 1 | H2:claim |
| `two` | CONCEPT | 1 | H2:alternative_explanations |
| `unrelated` | CONCEPT | 2 | H2:alternative_explanations, H2:claim |
| `variance` | CONCEPT | 1 | H3:claim |
| `vendor` | CONCEPT | 1 | H1:claim |
| `versus` | CONCEPT | 1 | H3:alternative_explanations |
| `waiting` | CONCEPT | 1 | H1:claim |
| `without` | CONCEPT | 1 | H1:claim |
| `write` | CONCEPT | 2 | H2:claim, H3:alternative_explanations |
| `writes` | CONCEPT | 1 | H1:claim |
| `01` | METRIC | 1 | checkpoint:registration.success_rule |
| `06` | METRIC | 2 | H1:discriminating_information, checkpoint:registration.failure_rule |
| `91` | METRIC | 2 | H1:discriminating_information, checkpoint:registration.failure_rule |
| `96` | METRIC | 2 | H1:discriminating_information, checkpoint:registration.failure_rule |
| `FAILED` | METRIC | 1 | H3:discriminating_information |
| `PENDING_CONFIRMATION` | METRIC | 2 | H2:discriminating_information, H2:falsifier |
| `SETTLED` | METRIC | 5 | H1:falsifier, H2:falsifier, H3:discriminating_information, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `absence` | METRIC | 1 | H2:discriminating_information |
| `ack` | METRIC | 1 | H2:discriminating_information |
| `acquirer` | METRIC | 3 | H1:discriminating_information, H1:falsifier, checkpoint:registration.success_rule |
| `adding` | METRIC | 1 | H2:falsifier |
| `after` | METRIC | 1 | H1:falsifier |
| `attempt` | METRIC | 1 | H1:falsifier |
| `attempt-id` | METRIC | 3 | H1:discriminating_information, H3:discriminating_information, H3:falsifier |
| `between` | METRIC | 1 | H2:discriminating_information |
| `callback` | METRIC | 1 | H2:discriminating_information |
| `can` | METRIC | 1 | H3:discriminating_information |
| `change` | METRIC | 1 | H2:falsifier |
| `code` | METRIC | 2 | H1:discriminating_information, checkpoint:registration.success_rule |
| `coexist` | METRIC | 1 | H3:falsifier |
| `confirms` | METRIC | 1 | H1:falsifier |
| `conflicting` | METRIC | 1 | H3:falsifier |
| `consistent` | METRIC | 1 | H3:discriminating_information |
| `defined` | METRIC | 1 | H3:falsifier |
| `does` | METRIC | 1 | H2:falsifier |
| `double-counted` | METRIC | 2 | H2:falsifier, checkpoint:registration.success_rule |
| `even` | METRIC | 1 | H1:falsifier |
| `event-sourced` | METRIC | 1 | H3:falsifier |
| `every` | METRIC | 1 | H3:discriminating_information |
| `explicit` | METRIC | 1 | H2:discriminating_information |
| `field` | METRIC | 1 | checkpoint:registration.success_rule |
| `historical` | METRIC | 1 | H3:discriminating_information |
| `label` | METRIC | 1 | H3:discriminating_information |
| `layer` | METRIC | 1 | H3:discriminating_information |
| `ledger` | METRIC | 4 | H1:discriminating_information, H1:falsifier, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `level` | METRIC | 1 | H1:discriminating_information |
| `machine` | METRIC | 1 | checkpoint:registration.success_rule |
| `manual` | METRIC | 1 | H3:discriminating_information |
| `migrating` | METRIC | 1 | H3:falsifier |
| `model` | METRIC | 1 | H3:falsifier |
| `permits` | METRIC | 1 | H3:falsifier |
| `presence` | METRIC | 1 | H2:discriminating_information |
| `projection` | METRIC | 1 | H3:discriminating_information |
| `rate` | METRIC | 2 | H2:falsifier, checkpoint:registration.success_rule |
| `reconciliation` | METRIC | 1 | H3:discriminating_information |
| `reconstruct` | METRIC | 1 | H3:discriminating_information |
| `resolution` | METRIC | 1 | H3:falsifier |
| `response` | METRIC | 2 | H1:discriminating_information, checkpoint:registration.success_rule |
| `retry-state` | METRIC | 1 | checkpoint:registration.success_rule |
| `row` | METRIC | 1 | H2:discriminating_information |
| `rule` | METRIC | 1 | H3:falsifier |
| `same` | METRIC | 1 | H3:falsifier |
| `settlement` | METRIC | 1 | H2:discriminating_information |
| `settlement-events` | METRIC | 1 | H3:falsifier |
| `soft-decline` | METRIC | 1 | checkpoint:registration.failure_rule |
| `soft_decline` | METRIC | 1 | H1:falsifier |
| `state` | METRIC | 1 | H2:falsifier |
| `status` | METRIC | 3 | H1:discriminating_information, H1:falsifier, checkpoint:registration.success_rule |
| `stays` | METRIC | 1 | H1:falsifier |
| `still` | METRIC | 1 | H3:falsifier |
| `two` | METRIC | 1 | H3:falsifier |
| `whether` | METRIC | 1 | H3:discriminating_information |
| `without` | METRIC | 2 | H3:discriminating_information, H3:falsifier |
| `ต่อวัน` | METRIC | 1 | checkpoint:registration.success_rule |
| `ต่ำกว่า` | METRIC | 1 | checkpoint:registration.success_rule |
| `ยังถูกเขียนเป็น` | METRIC | 1 | checkpoint:registration.failure_rule |
| `วัดจาก` | METRIC | 1 | checkpoint:registration.success_rule |
| `หรือ` | METRIC | 1 | checkpoint:registration.failure_rule |
| `หลังแก้` | METRIC | 1 | checkpoint:registration.success_rule |
| `เทียบกับ` | METRIC | 1 | checkpoint:registration.success_rule |
| `ใน` | METRIC | 1 | checkpoint:registration.failure_rule |
| `ไม่ลดลง` | METRIC | 1 | checkpoint:registration.failure_rule |
| `202` | PROCESS | 1 | H1:mechanism |
| `HTTP` | PROCESS | 1 | H1:mechanism |
| `PENDING_CONFIRMATION` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `SETTLED` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `accepted` | PROCESS | 1 | H2:mechanism |
| `ack` | PROCESS | 1 | H1:mechanism |
| `ack/nack (soft-decline)` | PROCESS | 1 | checkpoint:system_graph.edges |
| `acknowledgement` | PROCESS | 1 | H2:mechanism |
| `acquirer-specific` | PROCESS | 1 | H2:predicted_readout |
| `after` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `already` | PROCESS | 1 | H2:predicted_readout |
| `already-emitted` | PROCESS | 1 | H3:predicted_readout |
| `ambiguous-SETTLED` | PROCESS | 1 | H2:predicted_readout |
| `because` | PROCESS | 3 | H1:mechanism, H2:mechanism, H3:predicted_readout |
| `becomes` | PROCESS | 1 | H3:predicted_readout |
| `between` | PROCESS | 1 | H2:mechanism |
| `booking-service` | PROCESS | 1 | H2:predicted_readout |
| `both` | PROCESS | 1 | H2:mechanism |
| `bug` | PROCESS | 1 | H3:predicted_readout |
| `bugs` | PROCESS | 1 | H2:predicted_readout |
| `business-layer` | PROCESS | 1 | H2:mechanism |
| `callback` | PROCESS | 2 | H1:mechanism, H1:predicted_readout |
| `can` | PROCESS | 1 | H3:predicted_readout |
| `class` | PROCESS | 2 | H2:predicted_readout, H3:predicted_readout |
| `collapse` | PROCESS | 1 | H2:mechanism |
| `confirmed` | PROCESS | 2 | H1:mechanism, H1:predicted_readout |
| `conflated` | PROCESS | 1 | H1:mechanism |
| `construction` | PROCESS | 1 | H3:mechanism |
| `consumer` | PROCESS | 1 | H3:mechanism |
| `cost` | PROCESS | 1 | H3:mechanism |
| `cycle` | PROCESS | 1 | H1:predicted_readout |
| `double-counted` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `downstream` | PROCESS | 1 | H3:mechanism |
| `early` | PROCESS | 1 | H1:mechanism |
| `edge` | PROCESS | 1 | H1:mechanism |
| `eliminates` | PROCESS | 1 | H3:mechanism |
| `event` | PROCESS | 1 | H3:mechanism |
| `event-sourced` | PROCESS | 1 | H3:mechanism |
| `every` | PROCESS | 1 | H3:mechanism |
| `explicit` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `fire` | PROCESS | 1 | H1:predicted_readout |
| `fires` | PROCESS | 1 | H1:mechanism |
| `fix` | PROCESS | 1 | H2:predicted_readout |
| `fixture` | PROCESS | 1 | H2:predicted_readout |
| `intermediate` | PROCESS | 1 | H2:mechanism |
| `introducing` | PROCESS | 1 | H2:predicted_readout |
| `log` | PROCESS | 1 | H3:mechanism |
| `logic` | PROCESS | 1 | H2:predicted_readout |
| `machine` | PROCESS | 1 | H2:mechanism |
| `merely` | PROCESS | 1 | H3:predicted_readout |
| `migration` | PROCESS | 1 | H3:predicted_readout |
| `mirroring` | PROCESS | 1 | H2:predicted_readout |
| `models` | PROCESS | 1 | H2:mechanism |
| `moving` | PROCESS | 1 | H3:mechanism |
| `mutable-status` | PROCESS | 1 | H3:mechanism |
| `nack` | PROCESS | 1 | H1:mechanism |
| `needing` | PROCESS | 1 | H2:predicted_readout |
| `neither` | PROCESS | 1 | H2:mechanism |
| `one` | PROCESS | 1 | H1:predicted_readout |
| `only` | PROCESS | 1 | H1:predicted_readout |
| `overwrite` | PROCESS | 1 | H3:predicted_readout |
| `payment` | PROCESS | 1 | H1:mechanism |
| `projection` | PROCESS | 1 | H3:mechanism |
| `queue` | PROCESS | 1 | H1:mechanism |
| `races` | PROCESS | 1 | H3:mechanism |
| `rate` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `rather` | PROCESS | 2 | H1:mechanism, H3:mechanism |
| `read` | PROCESS | 1 | H3:mechanism |
| `receipt` | PROCESS | 1 | H1:mechanism |
| `reconcile` | PROCESS | 1 | checkpoint:system_graph.edges |
| `reconciliation` | PROCESS | 1 | H1:predicted_readout |
| `reduced` | PROCESS | 1 | H3:predicted_readout |
| `reduces` | PROCESS | 1 | H1:predicted_readout |
| `request` | PROCESS | 2 | H2:mechanism |
| `requiring` | PROCESS | 1 | H3:mechanism |
| `resolved` | PROCESS | 1 | H2:mechanism |
| `resolves` | PROCESS | 1 | H2:predicted_readout |
| `retroactively` | PROCESS | 1 | H3:predicted_readout |
| `retry-orchestrator` | PROCESS | 1 | H2:predicted_readout |
| `reverting` | PROCESS | 1 | H1:predicted_readout |
| `rewritten` | PROCESS | 1 | H3:mechanism |
| `row` | PROCESS | 1 | H3:mechanism |
| `settlement` | PROCESS | 3 | H1:mechanism, H1:predicted_readout, H3:mechanism |
| `settlement-event` | PROCESS | 1 | H3:predicted_readout |
| `single` | PROCESS | 1 | H3:predicted_readout |
| `soft-decline` | PROCESS | 1 | H1:mechanism |
| `sprint` | PROCESS | 1 | H1:mechanism |
| `state` | PROCESS | 5 | H2:mechanism, H2:predicted_readout, H3:mechanism |
| `structurally` | PROCESS | 1 | H3:predicted_readout |
| `submit-retry` | PROCESS | 1 | checkpoint:system_graph.edges |
| `success` | PROCESS | 1 | H1:mechanism |
| `systems` | PROCESS | 1 | H2:mechanism |
| `terminal` | PROCESS | 1 | H2:mechanism |
| `toward` | PROCESS | 1 | H1:predicted_readout |
| `transport-layer` | PROCESS | 1 | H2:mechanism |
| `trigger` | PROCESS | 1 | H1:predicted_readout |
| `undefined` | PROCESS | 1 | H3:predicted_readout |
| `validated` | PROCESS | 1 | H2:predicted_readout |
| `within` | PROCESS | 1 | H1:predicted_readout |
| `without` | PROCESS | 1 | H2:predicted_readout |
| `write` | PROCESS | 1 | H3:predicted_readout |
| `write-ordering` | PROCESS | 1 | H3:mechanism |
| `write-settled-flag` | PROCESS | 3 | H1:mechanism, H1:predicted_readout, checkpoint:system_graph.edges |
| `zero` | PROCESS | 1 | H1:predicted_readout |
| `CROSS_ADAPTIVE` | PROTOCOL | 1 | H2:lane |
| `DESIGN_HYPOTHESIS` | PROTOCOL | 1 | H3:causal_tier |
| `GENERATIVE_TRANSFORMATIVE` | PROTOCOL | 1 | H3:lane |
| `ISO-8583 "field 39" mapping` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `KNOWN_DIRECT` | PROTOCOL | 1 | H1:lane |
| `MECHANISM_HYPOTHESIS` | PROTOCOL | 1 | H1:causal_tier |
| `Phase-2 (draft) review` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `STRUCTURAL_HYPOTHESIS` | PROTOCOL | 1 | H2:causal_tier |
| `TARGETED_SEARCH "Phase-2 (draft)"` | PROTOCOL | 1 | checkpoint:review_mode |
| `canary gateway (5% traffic)` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `idempotency-key protocol v2` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `shadow-write "no-op" mode` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `Müller — QA lead 🔧` | ROLE | 2 | H3:affected_agencies, checkpoint:agency.voice_holders |
| `Payments Risk & Controls (PRC) — on-call` | ROLE | 2 | H2:affected_agencies, checkpoint:agency.decision_owners |
| `R&D / Ops (24x7)` | ROLE | 2 | H1:affected_agencies, checkpoint:agency.accountable_parties |
| `Reconciliation & Ledger Integrity (R&LI) board` | ROLE | 1 | H3:affected_agencies |
| `cardholder` | ROLE | 1 | checkpoint:agency.affected |
| `merchant "north-cluster" (Tier-1)` | ROLE | 2 | H1:affected_agencies, checkpoint:agency.affected |
| `merchant support desk` | ROLE | 1 | checkpoint:agency.voice_holders |
| `acquirer-gateway "AcquirerX" (prod)` | TOOL | 1 | checkpoint:system_graph.nodes |
| `ledger-writer (async/batch)` | TOOL | 1 | checkpoint:system_graph.nodes |
| `reconciliation-job (nightly, 02:00 ICT)` | TOOL | 1 | checkpoint:system_graph.nodes |
| `retry-orchestrator "north wing"` | TOOL | 1 | checkpoint:system_graph.nodes |

## Summary

- hypothesis cards: 3
- total distinct words: 342
- ROLE: 7 distinct words
- CONCEPT: 143 distinct words
- PROCESS: 104 distinct words
- TOOL: 4 distinct words
- PROTOCOL: 12 distinct words
- METRIC: 72 distinct words
