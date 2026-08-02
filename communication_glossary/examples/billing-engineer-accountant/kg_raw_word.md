# kg_raw_word — HYP-SKILLME-BILLING-ACCT-DEMO-001

**PROTOTYPE output.** Raw, typed, fully-traceable word extraction — not a semantic KG yet. No relation was invented; every edge below reflects only "this word literally appeared in this schema field of this source." See the script docstring for the stated tokenization limitation (unspaced formal Thai/CJK under-tokenizes).

## DAG (Mermaid)

```mermaid
flowchart TD
  CKPT["HYP-SKILLME-BILLING-ACCT-DEMO-001"]
  CKPT --> CARD_H1_106530dc["H1"]
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_ROLE_612f9988["ROLE"]
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_engineering_5d554bc5(["engineering"])
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_monthly_close_accounting_team_28eaed3c(["monthly close accounting team"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_MRR_35432afe(["MRR"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_across_c5570472(["across"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_amount_e9f40e1f(["amount"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_billing_8efdd107(["billing"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_books_7d8949bc(["books"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_computing_56c5f555(["computing"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_correct_e5d7cffe(["correct"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cycle_9a4c0740(["cycle"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_dashboard_dc7161be(["dashboard"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_date_5fc73231(["date"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_days_44fdec47(["days"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_engine_ad1943a9(["engine"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_full_e9dc924f(["full"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_instead_8dee4916(["instead"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ledger_f48139f3(["ledger"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_new_plan_da1026ec(["new-plan"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_one_f97c5d29(["one"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_posting_8e643a00(["posting"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_remaining_2626772c(["remaining"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_revenue_67362dfb(["revenue"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_spreading_e2ab8b04(["spreading"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_upgrade_ae26b3d8(["upgrade"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_wrong_2bda2998(["wrong"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_adjustment_0e914cc9(["adjustment"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_applied_ad8437d4(["applied"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_before_2f444175(["before"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_charge_41a2e03f(["charge"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_days_44fdec47(["days"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_entire_1b4a4d90(["entire"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_event_41196390(["event"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_general_958153f1(["general"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_handler_c1cbfe27(["handler"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_invoice_e5f96ae0(["invoice"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_ledger_f48139f3(["ledger"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_logic_c3d3c17b(["logic"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_manual_3c78b355(["manual"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_need_e877c56e(["need"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_new_22af645d(["new"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_period_a0acfa46(["period"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_posting_8e643a00(["posting"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_posts_18958e30(["posts"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_prorating_071d81b5(["prorating"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_proration_e0477197(["proration"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_remaining_2626772c(["remaining"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_removes_0f7a1ea5(["removes"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_service_aaabf0d3(["service"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_time_07cc694b(["time"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_upgrade_ae26b3d8(["upgrade"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_upgrade_billed_63a0a3bc(["upgrade-billed"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_KNOWN_DIRECT_d19064ee(["KNOWN_DIRECT"])
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_MECHANISM_HYPOTHESIS_4174f82e(["MECHANISM_HYPOTHESIS"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_already_1ebf4e55(["already"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_amount_e9f40e1f(["amount"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_comparing_6e54f3ba(["comparing"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_days_remaining_prorated_e4d91324(["days-remaining-prorated"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_event_41196390(["event"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_ledger_posted_b2a00b12(["ledger-posted"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_matches_9c28d32d(["matches"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_period_a0acfa46(["period"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_proration_e0477197(["proration"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_recognized_00c1aa7e(["recognized"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_revenue_67362dfb(["revenue"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_same_51037a4a(["same"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_service_aaabf0d3(["service"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_upgrade_ae26b3d8(["upgrade"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_without_fc0cb42f(["without"])
  CKPT --> CARD_H2_ca2bf3f6["H2"]
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_ROLE_612f9988["ROLE"]
  CARD_H2_ca2bf3f6_BKT_ROLE_612f9988 --> W_ROLE_engineering_5d554bc5(["engineering"])
  CARD_H2_ca2bf3f6_BKT_ROLE_612f9988 --> W_ROLE_finance_systems_team_d83c93ef(["finance systems team"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H2_ca2bf3f6(["H2"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_accounting_d4c143f0(["accounting"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_accrual_based_f0ca4045(["accrual-based"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_actually_7ddf8080(["actually"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_alone_c42bbd90(["alone"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_billing_8efdd107(["billing"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cash_93585797(["cash"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cash_vs_accrual_92d30997(["cash-vs-accrual"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_collected_95723b5e(["collected"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_computed_5a317d3d(["computed"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_concepts_ff4e01de(["concepts"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_conflating_9a9203ed(["conflating"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_distinct_ee87bc87(["distinct"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_distinction_cbab4c87(["distinction"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_engine_ad1943a9(["engine"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_field_06e3d36f(["field"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_here_6c92285f(["here"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_internal_d1efad72(["internal"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_invoice_e5f96ae0(["invoice"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_load_bearing_3efb8e6d(["load-bearing"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_name_b068931c(["name"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_one_f97c5d29(["one"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_proration_e0477197(["proration"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_rather_7c67f786(["rather"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_recognition_0c6a50fb(["recognition"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_revenue_67362dfb(["revenue"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_schedule_79985559(["schedule"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_sufficient_d2436a55(["sufficient"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_time_07cc694b(["time"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_two_b8a9f715(["two"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_actually_7ddf8080(["actually"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_allocation_950f4078(["allocation"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_anything_f0e166dc(["anything"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_around_29a5417a(["around"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_cash_collection_a228a0bb(["cash-collection"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_cash_collected_7c9230d0(["cash_collected"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_computed_5a317d3d(["computed"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_conflation_0f054ee1(["conflation"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_dashboards_126c4c32(["dashboards"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_designed_3677b55b(["designed"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_distinct_ee87bc87(["distinct"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_downstream_d22a0a80(["downstream"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_exports_2be75656(["exports"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_field_06e3d36f(["field"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_money_9726255e(["money"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_reading_eceadc1d(["reading"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_reads_0fb9cf5f(["reads"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_received_c5946eb9(["received"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_recognition_period_3fd9c8c8(["recognition-period"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_recognized_revenue_schedule_201e6fd4(["recognized_revenue_schedule"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_removes_0f7a1ea5(["removes"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_revenue_67362dfb(["revenue"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_schema_c9550d5f(["schema"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_separating_8bd0e3df(["separating"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_simplest_ba74c727(["simplest"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_single_dd5c0703(["single"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_source_36cd38f4(["source"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_timestamp_d7e6d55b(["timestamp"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_truth_59d42c50(["truth"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_was_a77b3598(["was"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_CROSS_ADAPTIVE_3397cb59(["CROSS_ADAPTIVE"])
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_STRUCTURAL_HYPOTHESIS_6aa85034(["STRUCTURAL_HYPOTHESIS"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_actually_7ddf8080(["actually"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_case_cd14c323(["case"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_cash_93585797(["cash"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_cash_vs_accrual_92d30997(["cash-vs-accrual"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_collected_95723b5e(["collected"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_depend_6334ae0f(["depend"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_distinction_cbab4c87(["distinction"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_diverge_82fb7647(["diverge"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_does_5440e70c(["does"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_here_6c92285f(["here"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_other_795f3202(["other"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_proration_e0477197(["proration"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_reasons_4b6d4444(["reasons"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_recognized_00c1aa7e(["recognized"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_revenue_67362dfb(["revenue"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_timing_4ad8aa3a(["timing"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_where_567904ef(["where"])
  CKPT --> CARD_H3_b1476321["H3"]
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_ROLE_612f9988["ROLE"]
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_controller_594c103f(["controller"])
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_engineering_5d554bc5(["engineering"])
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_monthly_close_accounting_team_28eaed3c(["monthly close accounting team"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H3_b1476321(["H3"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_accounting_d4c143f0(["accounting"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ambiguity_3e5451f3(["ambiguity"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_close_716f6b30(["close"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_data_8d777f38(["data"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_discarding_9f4fe843(["discarding"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_discards_5984203f(["discards"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_engine_ad1943a9(["engine"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_entirely_b56a6cab(["entirely"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_event_41196390(["event"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_every_83ab982d(["every"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_forcing_5a65028d(["forcing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_hand_573ce596(["hand"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_math_7e676e9e(["math"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_missing_ea21841d(["missing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_model_20f35e63(["model"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_needed_c0ca5324(["needed"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_originates_3a4db8e7(["originates"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_point_in_time_658848bb(["point-in-time"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_proper_d53f18f2(["proper"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_proration_e0477197(["proration"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_rebuild_9e67f9a6(["rebuild"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reconstruct_17e53f7c(["reconstruct"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_remaining_service_period_4ca653b8(["remaining-service-period"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_revenue_recognition_9175e009(["revenue-recognition"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_schedule_79985559(["schedule"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_single_dd5c0703(["single"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_solely_26eb20e0(["solely"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_upgrade_billed_63a0a3bc(["upgrade-billed"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_accounting_d4c143f0(["accounting"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_amount_e9f40e1f(["amount"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_answer_a363b8d1(["answer"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_billing_8efdd107(["billing"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_binary_9d7183f1(["binary"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_change_eb399bca(["change"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_close_716f6b30(["close"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_computed_5a317d3d(["computed"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_customer_facing_b62106e8(["customer-facing"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_data_8d777f38(["data"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_date_5fc73231(["date"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_designed_3677b55b(["designed"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_downstream_d22a0a80(["downstream"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_emitting_95d88cd3(["emitting"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_end_7f021a14(["end"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_event_41196390(["event"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_invoice_e5f96ae0(["invoice"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_lets_21927851(["lets"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_manual_3c78b355(["manual"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_manually_419e9f18(["manually"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_model_20f35e63(["model"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_must_d0e6ef34(["must"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_needed_c0ca5324(["needed"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_nowhere_03840d46(["nowhere"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_paid_76e08477(["paid"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_per_period_d09d7c7b(["per-period"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_period_a0acfa46(["period"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_question_5494af1f(["question"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_recognition_schedule_038a826e(["recognition-schedule"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_recognized_00c1aa7e(["recognized"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_reconstructed_115f5eea(["reconstructed"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_reconstruction_e75ffd9a(["reconstruction"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_schedule_79985559(["schedule"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_second_a9f0e61a(["second"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_should_55f19581(["should"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_start_ea2b2676(["start"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_time_07cc694b(["time"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_upgrade_ae26b3d8(["upgrade"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_was_a77b3598(["was"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_without_fc0cb42f(["without"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_DESIGN_HYPOTHESIS_0354f2a8(["DESIGN_HYPOTHESIS"])
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_GENERATIVE_TRANSFORMATIVE_5daf45b4(["GENERATIVE_TRANSFORMATIVE"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_already_1ebf4e55(["already"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_carries_131be413(["carries"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_contains_857af22f(["contains"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_data_8d777f38(["data"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_downstream_d22a0a80(["downstream"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_engine_ad1943a9(["engine"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_enough_edc1e3ea(["enough"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_event_41196390(["event"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_isn_4f612977(["isn"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_manual_3c78b355(["manual"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_payload_321c3cf4(["payload"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_raw_bdd166af(["raw"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_reconstruct_17e53f7c(["reconstruct"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_remaining_service_period_4ca653b8(["remaining-service-period"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_schedule_79985559(["schedule"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_simply_8a511f20(["simply"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_surfaced_b08340c7(["surfaced"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_whether_7d767e6b(["whether"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_without_fc0cb42f(["without"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_work_67e92c87(["work"])
  CKPT --> CKPT_BKT_ROLE_612f9988["ROLE (checkpoint-level)"]
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_VP_of_Finance_42df6df1(["VP of Finance"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_controller_594c103f(["controller"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_engineering_5d554bc5(["engineering"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_finance_systems_team_d83c93ef(["finance systems team"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_monthly_close_accounting_team_28eaed3c(["monthly close accounting team"])
  CKPT --> CKPT_BKT_PROCESS_b93c1384["PROCESS (checkpoint-level)"]
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_close_month_e8ea7534(["close-month"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_collect_cash_13a361b4(["collect-cash"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_invoice_e5f96ae0(["invoice"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_post_to_gl_0a844f75(["post-to-gl"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_upgrade_ae26b3d8(["upgrade"])
  CKPT --> CKPT_BKT_TOOL_6d968f54["TOOL (checkpoint-level)"]
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_MRR_dashboard_f8853a98(["MRR-dashboard"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_accountant_56f97f48(["accountant"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_billing_engine_584881fb(["billing-engine"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_general_ledger_158427fc(["general-ledger"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_invoice_service_9b03a1e5(["invoice-service"])
  CKPT --> CKPT_BKT_PROTOCOL_83a59f45["PROTOCOL (checkpoint-level)"]
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_TARGETED_SEARCH_b501af4a(["TARGETED_SEARCH"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_cash_vs_accrual_data_model_separation_159a0489(["cash-vs-accrual data-model separation"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_proration_method_redesign_a64c8c7e(["proration-method redesign"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_revenue_recognition_schedule_reconstruct_9f521f66(["revenue-recognition schedule reconstruction"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_synthetic_full_cycle_signup_replay_4f61ee77(["synthetic full-cycle-signup replay"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_synthetic_mid_cycle_upgrade_replay_4997e6c3(["synthetic mid-cycle-upgrade replay"])
  CKPT --> CKPT_BKT_METRIC_d83e9b0c["METRIC (checkpoint-level)"]
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_adjustment_0e914cc9(["adjustment"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_any_100b8cad(["any"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_billing_8efdd107(["billing"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_cash_93585797(["cash"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_collected_95723b5e(["collected"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_conflated_d068a704(["conflated"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_engine_ad1943a9(["engine"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_entries_5fce916b(["entries"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_event_41196390(["event"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_log_dc1d71bb(["log"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_manual_3c78b355(["manual"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_matches_9c28d32d(["matches"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_overstates_7e0747d6(["overstates"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_own_b515e18a(["own"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_period_a0acfa46(["period"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_recognized_00c1aa7e(["recognized"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_revenue_67362dfb(["revenue"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_timing_4ad8aa3a(["timing"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_understates_18d97c0c(["understates"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_upgrade_related_72513194(["upgrade-related"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_way_c83b72dd(["way"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_where_567904ef(["where"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_zero_d02c4c4c(["zero"])
```

## Word table (deduped, every source kept)

| word | type | occurrences | sources |
|---|---|---|---|
| `H1` | CONCEPT | 3 | H1:citation_cards.title, H2:alternative_explanations, H3:alternative_explanations |
| `H2` | CONCEPT | 1 | H2:citation_cards.title |
| `H3` | CONCEPT | 1 | H3:citation_cards.title |
| `MRR` | CONCEPT | 1 | H1:alternative_explanations |
| `SimulatedData` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `accounting` | CONCEPT | 2 | H2:claim, H3:claim |
| `accrual-based` | CONCEPT | 1 | H2:claim |
| `across` | CONCEPT | 1 | H1:claim |
| `actually` | CONCEPT | 1 | H2:alternative_explanations |
| `alone` | CONCEPT | 1 | H2:alternative_explanations |
| `ambiguity` | CONCEPT | 1 | H3:alternative_explanations |
| `amount` | CONCEPT | 1 | H1:claim |
| `billing` | CONCEPT | 3 | H1:claim, H2:claim |
| `books` | CONCEPT | 1 | H1:claim |
| `cash` | CONCEPT | 1 | H2:claim |
| `cash-vs-accrual` | CONCEPT | 1 | H2:alternative_explanations |
| `close` | CONCEPT | 1 | H3:claim |
| `collected` | CONCEPT | 1 | H2:claim |
| `computed` | CONCEPT | 1 | H2:claim |
| `computing` | CONCEPT | 1 | H1:alternative_explanations |
| `concepts` | CONCEPT | 1 | H2:claim |
| `conflating` | CONCEPT | 1 | H2:claim |
| `correct` | CONCEPT | 1 | H1:alternative_explanations |
| `cycle` | CONCEPT | 1 | H1:claim |
| `dashboard` | CONCEPT | 1 | H1:alternative_explanations |
| `data` | CONCEPT | 2 | H3:alternative_explanations, H3:claim |
| `date` | CONCEPT | 1 | H1:claim |
| `days` | CONCEPT | 1 | H1:claim |
| `discarding` | CONCEPT | 1 | H3:alternative_explanations |
| `discards` | CONCEPT | 1 | H3:claim |
| `distinct` | CONCEPT | 1 | H2:claim |
| `distinction` | CONCEPT | 1 | H2:alternative_explanations |
| `engine` | CONCEPT | 3 | H1:claim, H2:claim, H3:claim |
| `entirely` | CONCEPT | 1 | H3:alternative_explanations |
| `event` | CONCEPT | 2 | H3:alternative_explanations, H3:claim |
| `every` | CONCEPT | 1 | H3:claim |
| `evidence` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `field` | CONCEPT | 2 | H2:claim |
| `forcing` | CONCEPT | 1 | H3:claim |
| `full` | CONCEPT | 1 | H1:claim |
| `hand` | CONCEPT | 1 | H3:claim |
| `here` | CONCEPT | 1 | H2:alternative_explanations |
| `instead` | CONCEPT | 1 | H1:claim |
| `internal` | CONCEPT | 1 | H2:claim |
| `invoice` | CONCEPT | 1 | H2:claim |
| `ledger` | CONCEPT | 1 | H1:alternative_explanations |
| `load-bearing` | CONCEPT | 1 | H2:alternative_explanations |
| `math` | CONCEPT | 1 | H3:alternative_explanations |
| `missing` | CONCEPT | 1 | H3:alternative_explanations |
| `model` | CONCEPT | 1 | H3:alternative_explanations |
| `name` | CONCEPT | 1 | H2:claim |
| `needed` | CONCEPT | 1 | H3:claim |
| `new-plan` | CONCEPT | 1 | H1:claim |
| `one` | CONCEPT | 2 | H1:alternative_explanations, H2:claim |
| `originates` | CONCEPT | 1 | H3:alternative_explanations |
| `point-in-time` | CONCEPT | 1 | H3:claim |
| `posting` | CONCEPT | 1 | H1:alternative_explanations |
| `proper` | CONCEPT | 1 | H3:claim |
| `proration` | CONCEPT | 2 | H2:alternative_explanations, H3:alternative_explanations |
| `rather` | CONCEPT | 1 | H2:claim |
| `rebuild` | CONCEPT | 1 | H3:claim |
| `recognition` | CONCEPT | 1 | H2:claim |
| `reconstruct` | CONCEPT | 1 | H3:claim |
| `record` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `remaining` | CONCEPT | 1 | H1:claim |
| `remaining-service-period` | CONCEPT | 1 | H3:claim |
| `revenue` | CONCEPT | 2 | H1:claim, H2:claim |
| `revenue-recognition` | CONCEPT | 1 | H3:claim |
| `schedule` | CONCEPT | 4 | H2:claim, H3:alternative_explanations, H3:claim |
| `single` | CONCEPT | 1 | H3:claim |
| `solely` | CONCEPT | 1 | H3:alternative_explanations |
| `spreading` | CONCEPT | 1 | H1:claim |
| `sufficient` | CONCEPT | 1 | H2:alternative_explanations |
| `time` | CONCEPT | 1 | H2:claim |
| `two` | CONCEPT | 1 | H2:claim |
| `upgrade` | CONCEPT | 1 | H1:claim |
| `upgrade-billed` | CONCEPT | 1 | H3:claim |
| `wrong` | CONCEPT | 1 | H1:alternative_explanations |
| `actually` | METRIC | 1 | H2:falsifier |
| `adjustment` | METRIC | 1 | checkpoint:registration.success_rule |
| `already` | METRIC | 2 | H1:falsifier, H3:falsifier |
| `amount` | METRIC | 2 | H1:discriminating_information |
| `any` | METRIC | 1 | checkpoint:registration.failure_rule |
| `billing` | METRIC | 1 | checkpoint:registration.success_rule |
| `carries` | METRIC | 1 | H3:falsifier |
| `case` | METRIC | 1 | H2:discriminating_information |
| `cash` | METRIC | 2 | H2:discriminating_information, checkpoint:registration.failure_rule |
| `cash-vs-accrual` | METRIC | 1 | H2:falsifier |
| `collected` | METRIC | 2 | H2:discriminating_information, checkpoint:registration.failure_rule |
| `comparing` | METRIC | 1 | H1:discriminating_information |
| `conflated` | METRIC | 1 | checkpoint:registration.failure_rule |
| `contains` | METRIC | 1 | H3:discriminating_information |
| `data` | METRIC | 2 | H3:discriminating_information, H3:falsifier |
| `days-remaining-prorated` | METRIC | 1 | H1:discriminating_information |
| `depend` | METRIC | 1 | H2:falsifier |
| `distinction` | METRIC | 1 | H2:falsifier |
| `diverge` | METRIC | 1 | H2:discriminating_information |
| `does` | METRIC | 1 | H2:falsifier |
| `downstream` | METRIC | 1 | H3:discriminating_information |
| `engine` | METRIC | 2 | H3:discriminating_information, checkpoint:registration.success_rule |
| `enough` | METRIC | 1 | H3:falsifier |
| `entries` | METRIC | 1 | checkpoint:registration.success_rule |
| `event` | METRIC | 4 | H1:discriminating_information, H3:discriminating_information, H3:falsifier, checkpoint:registration.success_rule |
| `here` | METRIC | 1 | H2:falsifier |
| `isn` | METRIC | 1 | H3:discriminating_information |
| `ledger-posted` | METRIC | 1 | H1:discriminating_information |
| `log` | METRIC | 1 | checkpoint:registration.success_rule |
| `manual` | METRIC | 2 | H3:falsifier, checkpoint:registration.success_rule |
| `matches` | METRIC | 2 | H1:falsifier, checkpoint:registration.success_rule |
| `other` | METRIC | 1 | H2:discriminating_information |
| `overstates` | METRIC | 1 | checkpoint:registration.failure_rule |
| `own` | METRIC | 1 | checkpoint:registration.success_rule |
| `payload` | METRIC | 1 | H3:discriminating_information |
| `period` | METRIC | 4 | H1:falsifier, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `proration` | METRIC | 2 | H1:falsifier, H2:discriminating_information |
| `raw` | METRIC | 1 | H3:discriminating_information |
| `reasons` | METRIC | 1 | H2:discriminating_information |
| `recognized` | METRIC | 4 | H1:falsifier, H2:discriminating_information, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `reconstruct` | METRIC | 1 | H3:falsifier |
| `remaining-service-period` | METRIC | 1 | H3:discriminating_information |
| `revenue` | METRIC | 6 | H1:falsifier, H2:discriminating_information, H2:falsifier, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `same` | METRIC | 1 | H1:discriminating_information |
| `schedule` | METRIC | 1 | H3:falsifier |
| `service` | METRIC | 1 | H1:falsifier |
| `simply` | METRIC | 1 | H3:discriminating_information |
| `surfaced` | METRIC | 1 | H3:discriminating_information |
| `timing` | METRIC | 3 | H2:discriminating_information, H2:falsifier, checkpoint:registration.success_rule |
| `understates` | METRIC | 1 | checkpoint:registration.failure_rule |
| `upgrade` | METRIC | 1 | H1:discriminating_information |
| `upgrade-related` | METRIC | 1 | checkpoint:registration.success_rule |
| `way` | METRIC | 1 | checkpoint:registration.failure_rule |
| `where` | METRIC | 2 | H2:discriminating_information, checkpoint:registration.failure_rule |
| `whether` | METRIC | 1 | H3:discriminating_information |
| `without` | METRIC | 2 | H1:falsifier, H3:falsifier |
| `work` | METRIC | 1 | H3:falsifier |
| `zero` | METRIC | 1 | checkpoint:registration.success_rule |
| `accounting` | PROCESS | 1 | H3:predicted_readout |
| `actually` | PROCESS | 1 | H2:mechanism |
| `adjustment` | PROCESS | 1 | H1:predicted_readout |
| `allocation` | PROCESS | 1 | H2:mechanism |
| `amount` | PROCESS | 2 | H3:mechanism, H3:predicted_readout |
| `answer` | PROCESS | 1 | H3:mechanism |
| `anything` | PROCESS | 1 | H2:mechanism |
| `applied` | PROCESS | 1 | H1:mechanism |
| `around` | PROCESS | 1 | H2:mechanism |
| `before` | PROCESS | 1 | H1:predicted_readout |
| `billing` | PROCESS | 1 | H3:predicted_readout |
| `binary` | PROCESS | 1 | H3:mechanism |
| `cash-collection` | PROCESS | 1 | H2:mechanism |
| `cash_collected` | PROCESS | 1 | H2:predicted_readout |
| `change` | PROCESS | 1 | H3:predicted_readout |
| `charge` | PROCESS | 2 | H1:mechanism, H1:predicted_readout |
| `close` | PROCESS | 1 | H3:predicted_readout |
| `close-month` | PROCESS | 1 | checkpoint:system_graph.edges |
| `collect-cash` | PROCESS | 1 | checkpoint:system_graph.edges |
| `computed` | PROCESS | 2 | H2:predicted_readout, H3:mechanism |
| `conflation` | PROCESS | 1 | H2:predicted_readout |
| `customer-facing` | PROCESS | 1 | H3:predicted_readout |
| `dashboards` | PROCESS | 1 | H2:mechanism |
| `data` | PROCESS | 1 | H3:mechanism |
| `date` | PROCESS | 2 | H3:predicted_readout |
| `days` | PROCESS | 1 | H1:predicted_readout |
| `designed` | PROCESS | 2 | H2:mechanism, H3:mechanism |
| `distinct` | PROCESS | 1 | H2:predicted_readout |
| `downstream` | PROCESS | 2 | H2:mechanism, H3:mechanism |
| `emitting` | PROCESS | 1 | H3:predicted_readout |
| `end` | PROCESS | 1 | H3:predicted_readout |
| `entire` | PROCESS | 1 | H1:mechanism |
| `event` | PROCESS | 3 | H1:mechanism, H3:mechanism, H3:predicted_readout |
| `exports` | PROCESS | 1 | H2:mechanism |
| `field` | PROCESS | 2 | H2:predicted_readout |
| `general` | PROCESS | 1 | H1:mechanism |
| `handler` | PROCESS | 1 | H1:mechanism |
| `invoice` | PROCESS | 3 | H1:mechanism, H3:mechanism, checkpoint:system_graph.edges |
| `ledger` | PROCESS | 1 | H1:mechanism |
| `lets` | PROCESS | 1 | H3:predicted_readout |
| `logic` | PROCESS | 1 | H1:mechanism |
| `manual` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `manually` | PROCESS | 1 | H3:mechanism |
| `model` | PROCESS | 1 | H3:mechanism |
| `money` | PROCESS | 1 | H2:mechanism |
| `must` | PROCESS | 1 | H3:mechanism |
| `need` | PROCESS | 1 | H1:predicted_readout |
| `needed` | PROCESS | 1 | H3:mechanism |
| `new` | PROCESS | 1 | H1:mechanism |
| `nowhere` | PROCESS | 1 | H3:mechanism |
| `paid` | PROCESS | 1 | H3:mechanism |
| `per-period` | PROCESS | 1 | H3:predicted_readout |
| `period` | PROCESS | 2 | H1:mechanism, H3:mechanism |
| `post-to-gl` | PROCESS | 1 | checkpoint:system_graph.edges |
| `posting` | PROCESS | 1 | H1:predicted_readout |
| `posts` | PROCESS | 1 | H1:mechanism |
| `prorating` | PROCESS | 1 | H1:predicted_readout |
| `proration` | PROCESS | 1 | H1:mechanism |
| `question` | PROCESS | 3 | H3:mechanism |
| `reading` | PROCESS | 1 | H2:mechanism |
| `reads` | PROCESS | 1 | H2:mechanism |
| `received` | PROCESS | 1 | H2:mechanism |
| `recognition-period` | PROCESS | 1 | H2:mechanism |
| `recognition-schedule` | PROCESS | 1 | H3:predicted_readout |
| `recognized` | PROCESS | 1 | H3:mechanism |
| `recognized_revenue_schedule` | PROCESS | 1 | H2:predicted_readout |
| `reconstructed` | PROCESS | 1 | H3:mechanism |
| `reconstruction` | PROCESS | 1 | H3:predicted_readout |
| `remaining` | PROCESS | 2 | H1:mechanism, H1:predicted_readout |
| `removes` | PROCESS | 2 | H1:predicted_readout, H2:predicted_readout |
| `revenue` | PROCESS | 1 | H2:mechanism |
| `schedule` | PROCESS | 1 | H3:mechanism |
| `schema` | PROCESS | 1 | H2:mechanism |
| `second` | PROCESS | 1 | H3:mechanism |
| `separating` | PROCESS | 1 | H2:predicted_readout |
| `service` | PROCESS | 1 | H1:mechanism |
| `should` | PROCESS | 1 | H3:mechanism |
| `simplest` | PROCESS | 1 | H2:mechanism |
| `single` | PROCESS | 1 | H2:mechanism |
| `source` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `start` | PROCESS | 1 | H3:predicted_readout |
| `time` | PROCESS | 2 | H1:mechanism, H3:predicted_readout |
| `timestamp` | PROCESS | 1 | H2:mechanism |
| `truth` | PROCESS | 1 | H2:mechanism |
| `upgrade` | PROCESS | 3 | H1:predicted_readout, H3:predicted_readout, checkpoint:system_graph.edges |
| `upgrade-billed` | PROCESS | 1 | H1:mechanism |
| `was` | PROCESS | 3 | H2:mechanism, H3:mechanism |
| `without` | PROCESS | 1 | H3:predicted_readout |
| `CROSS_ADAPTIVE` | PROTOCOL | 1 | H2:lane |
| `DESIGN_HYPOTHESIS` | PROTOCOL | 1 | H3:causal_tier |
| `GENERATIVE_TRANSFORMATIVE` | PROTOCOL | 1 | H3:lane |
| `KNOWN_DIRECT` | PROTOCOL | 1 | H1:lane |
| `MECHANISM_HYPOTHESIS` | PROTOCOL | 1 | H1:causal_tier |
| `STRUCTURAL_HYPOTHESIS` | PROTOCOL | 1 | H2:causal_tier |
| `TARGETED_SEARCH` | PROTOCOL | 1 | checkpoint:review_mode |
| `cash-vs-accrual data-model separation` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `proration-method redesign` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `revenue-recognition schedule reconstruction` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `synthetic full-cycle-signup replay` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `synthetic mid-cycle-upgrade replay` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `VP of Finance` | ROLE | 1 | checkpoint:agency.decision_owners |
| `controller` | ROLE | 2 | H3:affected_agencies, checkpoint:agency.accountable_parties |
| `engineering` | ROLE | 5 | H1:affected_agencies, H2:affected_agencies, H3:affected_agencies, checkpoint:agency.affected, checkpoint:agency.voice_holders |
| `finance systems team` | ROLE | 2 | H2:affected_agencies, checkpoint:agency.affected |
| `monthly close accounting team` | ROLE | 4 | H1:affected_agencies, H3:affected_agencies, checkpoint:agency.affected, checkpoint:agency.voice_holders |
| `MRR-dashboard` | TOOL | 1 | checkpoint:system_graph.nodes |
| `accountant` | TOOL | 1 | checkpoint:system_graph.nodes |
| `billing-engine` | TOOL | 1 | checkpoint:system_graph.nodes |
| `general-ledger` | TOOL | 1 | checkpoint:system_graph.nodes |
| `invoice-service` | TOOL | 1 | checkpoint:system_graph.nodes |

## Summary

- hypothesis cards: 3
- total distinct words: 246
- ROLE: 5 distinct words
- CONCEPT: 78 distinct words
- PROCESS: 88 distinct words
- TOOL: 5 distinct words
- PROTOCOL: 12 distinct words
- METRIC: 58 distinct words
