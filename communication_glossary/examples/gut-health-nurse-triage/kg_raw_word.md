# kg_raw_word — HYP-UIA-GUT-NURSE-DEMO-001

**PROTOTYPE output.** Raw, typed, fully-traceable word extraction — not a semantic KG yet. No relation was invented; every edge below reflects only "this word literally appeared in this schema field of this source." See the script docstring for the stated tokenization limitation (unspaced formal Thai/CJK under-tokenizes).

## DAG (Mermaid)

```mermaid
flowchart TD
  CKPT["HYP-UIA-GUT-NURSE-DEMO-001"]
  CKPT --> CARD_H1_106530dc["H1"]
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_ROLE_612f9988["ROLE"]
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_clinical_nursing_triage_efb4daf7(["clinical nursing triage"])
  CARD_H1_106530dc_BKT_ROLE_612f9988 --> W_ROLE_patients_3495d5d8(["patients"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_app_d2a57dc1(["app"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_bleeding_c68e1e6f(["bleeding"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_bloating_a9df3788(["bloating"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_checkbox_9fced129(["checkbox"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_conflates_8694460f(["conflates"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_constipation_94095923(["constipation"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cramping_611b7a8b(["cramping"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_detail_951da6b7(["detail"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_diarrhea_29117dc0(["diarrhea"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_existing_f4e0ac58(["existing"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_field_06e3d36f(["field"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_free_text_dfd15350(["free-text"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_generic_3d517f89(["generic"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_issue_0aae4c8f(["issue"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_label_d304ba20(["label"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_like_be1ab163(["like"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_nurses_d5c0c340(["nurses"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_one_f97c5d29(["one"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_picker_76a68eae(["picker"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_reading_eceadc1d(["reading"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_rectal_f69f5c61(["rectal"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_red_flag_220db67a(["red-flag"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_single_dd5c0703(["single"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_stomach_c01a2057(["stomach"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_symptom_d9f6e36e(["symptom"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_symptoms_89d77329(["symptoms"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_undertrained_94eaba1e(["undertrained"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_undifferentiated_0b20c6a3(["undifferentiated"])
  CARD_H1_106530dc_BKT_CONCEPT_7b01b981 --> W_CONCEPT_uses_7febea91(["uses"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_GI_02c73fe4(["GI"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_adding_732f3800(["adding"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_all_a181a603(["all"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_case_cd14c323(["case"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_categories_b0b5ccb4(["categories"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_category_c4ef352f(["category"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_clinical_f1f39546(["clinical"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_designed_3677b55b(["designed"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_display_ebf78b51(["display"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_distinguishable_072c734c(["distinguishable"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_entry_1043bfc7(["entry"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_fast_31d4541b(["fast"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_label_d304ba20(["label"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_lets_21927851(["lets"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_map_1d78dc8e(["map"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_opening_c1d8ae6c(["opening"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_patient_b39024ef(["patient"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_picker_76a68eae(["picker"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_queue_a9d1cbf7(["queue"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_same_51037a4a(["same"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_submission_0f710bba(["submission"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_subtype_2e282b0d(["subtype"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_subtypes_55f4f06d(["subtypes"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_symptom_d9f6e36e(["symptom"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_taxonomy_7a5dd46f(["taxonomy"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_time_07cc694b(["time"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_value_2063c160(["value"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_was_a77b3598(["was"])
  CARD_H1_106530dc_BKT_PROCESS_b93c1384 --> W_PROCESS_without_fc0cb42f(["without"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_KNOWN_DIRECT_d19064ee(["KNOWN_DIRECT"])
  CARD_H1_106530dc_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_MECHANISM_HYPOTHESIS_4174f82e(["MECHANISM_HYPOTHESIS"])
  CARD_H1_106530dc --> CARD_H1_106530dc_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_absent_e5671794(["absent"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_alone_c42bbd90(["alone"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_already_1ebf4e55(["already"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_can_2c61ebff(["can"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_distinguish_1b5c872c(["distinguish"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_label_d304ba20(["label"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_measured_9b68c32a(["measured"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_nurse_0701aa31(["nurse"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_nurses_d5c0c340(["nurses"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_present_47ed4995(["present"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_reliably_403b24e4(["reliably"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_single_dd5c0703(["single"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_subtype_2e282b0d(["subtype"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_triage_time_3267ab55(["triage-time"])
  CARD_H1_106530dc_BKT_METRIC_d83e9b0c --> W_METRIC_urgency_af28b277(["urgency"])
  CKPT --> CARD_H2_ca2bf3f6["H2"]
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_ROLE_612f9988["ROLE"]
  CARD_H2_ca2bf3f6_BKT_ROLE_612f9988 --> W_ROLE_clinical_nursing_triage_efb4daf7(["clinical nursing triage"])
  CARD_H2_ca2bf3f6_BKT_ROLE_612f9988 --> W_ROLE_product_engineering_fe3b43d0(["product engineering"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_GI_02c73fe4(["GI"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H2_ca2bf3f6(["H2"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_acute_56777c15(["acute"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_alone_c42bbd90(["alone"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_app_d2a57dc1(["app"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_apply_4da463dc(["apply"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_cannot_a156a643(["cannot"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_chronic_955fb354(["chronic"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_clinical_f1f39546(["clinical"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_could_f0441366(["could"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_criteria_15c46c6e(["criteria"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_data_8d777f38(["data"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_dedicated_06f287d4(["dedicated"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_distinguishing_65b10112(["distinguishing"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_does_5440e70c(["does"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_duration_b85ec314(["duration"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_field_06e3d36f(["field"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_frequency_fad6c43b(["frequency"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_infer_00236eac(["infer"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_log_dc1d71bb(["log"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_nurses_d5c0c340(["nurses"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_pattern_240bf022(["pattern"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_presentation_2486923a(["presentation"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_require_f0ffd3b7(["require"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_standard_c00f0c46(["standard"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_submission_0f710bba(["submission"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_symptom_d9f6e36e(["symptom"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_timestamps_705ec82e(["timestamps"])
  CARD_H2_ca2bf3f6_BKT_CONCEPT_7b01b981 --> W_CONCEPT_without_fc0cb42f(["without"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_adding_732f3800(["adding"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_against_36a38399(["against"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_apply_4da463dc(["apply"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_captures_8856ffdd(["captures"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_category_c4ef352f(["category"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_clinical_f1f39546(["clinical"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_criteria_15c46c6e(["criteria"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_data_8d777f38(["data"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_directly_c674f043(["directly"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_duration_b85ec314(["duration"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_evaluate_94d2f2aa(["evaluate"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_field_06e3d36f(["field"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_free_text_dfd15350(["free-text"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_frequency_fad6c43b(["frequency"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_have_b42dad54(["have"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_lets_21927851(["lets"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_note_aad653ca(["note"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_pattern_240bf022(["pattern"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_pattern_based_0c921d49(["pattern-based"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_point_in_time_658848bb(["point-in-time"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_queue_a9d1cbf7(["queue"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_schema_c9550d5f(["schema"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_standard_c00f0c46(["standard"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_structured_32234519(["structured"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_symptom_entry_20b5e9e3(["symptom-entry"])
  CARD_H2_ca2bf3f6_BKT_PROCESS_b93c1384 --> W_PROCESS_triage_466e8b3f(["triage"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_CROSS_ADAPTIVE_3397cb59(["CROSS_ADAPTIVE"])
  CARD_H2_ca2bf3f6_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_STRUCTURAL_HYPOTHESIS_6aa85034(["STRUCTURAL_HYPOTHESIS"])
  CARD_H2_ca2bf3f6 --> CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_accuracy_5d6db9a1(["accuracy"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_actually_7ddf8080(["actually"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_available_e4894ca1(["available"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_comparison_347cd68a(["comparison"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_data_8d777f38(["data"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_depend_6334ae0f(["depend"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_does_5440e70c(["does"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_duration_b85ec314(["duration"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_frequency_fad6c43b(["frequency"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_structured_32234519(["structured"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_triage_466e8b3f(["triage"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_urgency_af28b277(["urgency"])
  CARD_H2_ca2bf3f6_BKT_METRIC_d83e9b0c --> W_METRIC_without_fc0cb42f(["without"])
  CKPT --> CARD_H3_b1476321["H3"]
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_ROLE_612f9988["ROLE"]
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_clinical_nursing_triage_efb4daf7(["clinical nursing triage"])
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_patients_3495d5d8(["patients"])
  CARD_H3_b1476321_BKT_ROLE_612f9988 --> W_ROLE_product_engineering_fe3b43d0(["product engineering"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_CONCEPT_7b01b981["CONCEPT"]
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H1_106530dc(["H1"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_H3_b1476321(["H3"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_SimulatedData_681e56e7(["SimulatedData"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_already_available_6ddc4e29(["already-available"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_already_existing_6ffd6377(["already-existing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_ambiguity_3e5451f3(["ambiguity"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_app_d2a57dc1(["app"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_backend_b43fdd98(["backend"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_binary_9d7183f1(["binary"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_collapsing_6becc10b(["collapsing"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_compute_77e73f3a(["compute"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_could_f0441366(["could"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_discarding_9f4fe843(["discarding"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_distinction_cbab4c87(["distinction"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_doesn_6691fadb(["doesn"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_event_41196390(["event"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_evidence_14e10d57(["evidence"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_exposes_4befbce3(["exposes"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_logged_symptom_e7d95d23(["logged-symptom"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_model_20f35e63(["model"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_nurses_d5c0c340(["nurses"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_one_f97c5d29(["one"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_only_6299ba2c(["only"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_originates_3a4db8e7(["originates"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_own_b515e18a(["own"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_picker_76a68eae(["picker"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_queue_a9d1cbf7(["queue"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_record_de17f0f2(["record"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_red_flag_vs_benign_cb12c853(["red-flag-vs-benign"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_signal_521345a9(["signal"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_solely_26eb20e0(["solely"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_surface_d302e976(["surface"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_tier_af2e53a7(["tier"])
  CARD_H3_b1476321_BKT_CONCEPT_7b01b981 --> W_CONCEPT_undifferentiated_0b20c6a3(["undifferentiated"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROCESS_b93c1384["PROCESS"]
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_any_100b8cad(["any"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_change_eb399bca(["change"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_clinical_f1f39546(["clinical"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_computed_5a317d3d(["computed"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_dashboard_dc7161be(["dashboard"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_distinguishable_072c734c(["distinguishable"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_emits_bd0c7c58(["emits"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_entry_1043bfc7(["entry"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_even_cc935c5f(["even"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_event_41196390(["event"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_field_06e3d36f(["field"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_free_text_dfd15350(["free-text"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_has_3309a7a7(["has"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_ingestion_bf7189d1(["ingestion"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_keywords_59aeb2c9(["keywords"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_lets_21927851(["lets"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_model_20f35e63(["model"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_patient_facing_8a6def54(["patient-facing"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_present_47ed4995(["present"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_queue_a9d1cbf7(["queue"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_red_flag_220db67a(["red-flag"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_regardless_e4d31f74(["regardless"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_render_9e5f0bb3(["render"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_rows_df347a37(["rows"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_severity_f6cdd856(["severity"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_signal_521345a9(["signal"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_single_dd5c0703(["single"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_surfaced_b08340c7(["surfaced"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_symptom_logged_0796ec05(["symptom-logged"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_though_23f9c1b0(["though"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_triage_queue_9b6901fd(["triage-queue"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_type_599dcce2(["type"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_urgency_tier_a05a76fd(["urgency-tier"])
  CARD_H3_b1476321_BKT_PROCESS_b93c1384 --> W_PROCESS_without_fc0cb42f(["without"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_PROTOCOL_83a59f45["PROTOCOL"]
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_DESIGN_HYPOTHESIS_0354f2a8(["DESIGN_HYPOTHESIS"])
  CARD_H3_b1476321_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_GENERATIVE_TRANSFORMATIVE_5daf45b4(["GENERATIVE_TRANSFORMATIVE"])
  CARD_H3_b1476321 --> CARD_H3_b1476321_BKT_METRIC_d83e9b0c["METRIC"]
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_already_1ebf4e55(["already"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_backend_b43fdd98(["backend"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_benign_83e7dc6f(["benign"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_different_29e4b66f(["different"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_keyword_d7df5b64(["keyword"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_log_dc1d71bb(["log"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_positions_365a4a97(["positions"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_present_47ed4995(["present"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_queue_a9d1cbf7(["queue"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_queue_row_30c189d6(["queue-row"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_red_flag_220db67a(["red-flag"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_render_9e5f0bb3(["render"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_showing_5837210d(["showing"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_surfaced_b08340c7(["surfaced"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_symptoms_89d77329(["symptoms"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_visibly_aa1c69b3(["visibly"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_was_a77b3598(["was"])
  CARD_H3_b1476321_BKT_METRIC_d83e9b0c --> W_METRIC_whether_7d767e6b(["whether"])
  CKPT --> CKPT_BKT_ROLE_612f9988["ROLE (checkpoint-level)"]
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_clinical_nursing_triage_efb4daf7(["clinical nursing triage"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_clinical_nursing_triage_lead_33c5eeba(["clinical nursing triage lead"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_patient_safety_officer_a01befa3(["patient safety officer"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_patients_3495d5d8(["patients"])
  CKPT_BKT_ROLE_612f9988 --> W_ROLE_product_engineering_fe3b43d0(["product engineering"])
  CKPT --> CKPT_BKT_PROCESS_b93c1384["PROCESS (checkpoint-level)"]
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_categorize_fc97c93f(["categorize"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_escalate_499f842c(["escalate"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_log_symptom_e9e3acc1(["log-symptom"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_open_case_027890ce(["open-case"])
  CKPT_BKT_PROCESS_b93c1384 --> W_PROCESS_render_queue_row_71fde27b(["render-queue-row"])
  CKPT --> CKPT_BKT_TOOL_6d968f54["TOOL (checkpoint-level)"]
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_nurse_0701aa31(["nurse"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_red_flag_escalation_line_17ad9265(["red-flag-escalation-line"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_symptom_entry_schema_eddbe6c8(["symptom-entry-schema"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_symptom_tracker_app_cfbb06a7(["symptom-tracker-app"])
  CKPT_BKT_TOOL_6d968f54 --> W_TOOL_triage_queue_dashboard_5a755c17(["triage-queue-dashboard"])
  CKPT --> CKPT_BKT_PROTOCOL_83a59f45["PROTOCOL (checkpoint-level)"]
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_GI_symptom_triage_taxonomy_748683b2(["GI symptom triage taxonomy"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_TARGETED_SEARCH_b501af4a(["TARGETED_SEARCH"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_event_schema_granularity_redesign_4fa1b487(["event-schema granularity redesign"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_red_flag_symptom_escalation_protocol_733a8aca(["red-flag symptom escalation protocol"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_synthetic_benign_entry_replay_a3d7e9ac(["synthetic benign-entry replay"])
  CKPT_BKT_PROTOCOL_83a59f45 --> W_PROTOCOL_synthetic_red_flag_entry_replay_50e1d653(["synthetic red-flag-entry replay"])
  CKPT --> CKPT_BKT_METRIC_d83e9b0c["METRIC (checkpoint-level)"]
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_90_8613985e(["90"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_GI_02c73fe4(["GI"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_benign_83e7dc6f(["benign"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_entry_1043bfc7(["entry"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_nurse_0701aa31(["nurse"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_pilot_a3452f94(["pilot"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_red_flag_220db67a(["red-flag"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_symptom_d9f6e36e(["symptom"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_triage_466e8b3f(["triage"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_________a0635846(["ผิดเป็น"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC____45ea26eb(["มี"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_____________aa55c3a1(["ลดลงต่ำกว่า"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC______________a97d16a5(["วินาทีต่อเคส"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC______5e201eb9(["หรือ"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC___________d817ff5a(["ออกจากคิว"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC__________ce3c98d9(["เคสใดถูก"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC__________________dc844340(["เคสไหนถูกมองข้าม"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC_______________ecce76b1(["เวลาเฉลี่ยที่"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC__________4dfe12e0(["โดยไม่มี"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC______________________________f422a628(["ใช้เวลาแยกเคสนานขึ้นกว่าก่อน"])
  CKPT_BKT_METRIC_d83e9b0c --> W_METRIC________090d06c3(["ใช้แยก"])
```

## Word table (deduped, every source kept)

| word | type | occurrences | sources |
|---|---|---|---|
| `GI` | CONCEPT | 1 | H2:claim |
| `H1` | CONCEPT | 2 | H1:citation_cards.title, H3:alternative_explanations |
| `H2` | CONCEPT | 1 | H2:citation_cards.title |
| `H3` | CONCEPT | 1 | H3:citation_cards.title |
| `SimulatedData` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `acute` | CONCEPT | 1 | H2:claim |
| `alone` | CONCEPT | 1 | H2:alternative_explanations |
| `already-available` | CONCEPT | 1 | H3:alternative_explanations |
| `already-existing` | CONCEPT | 1 | H3:claim |
| `ambiguity` | CONCEPT | 1 | H3:alternative_explanations |
| `app` | CONCEPT | 4 | H1:claim, H2:claim, H3:claim |
| `apply` | CONCEPT | 1 | H2:claim |
| `backend` | CONCEPT | 1 | H3:claim |
| `binary` | CONCEPT | 1 | H3:claim |
| `bleeding` | CONCEPT | 1 | H1:claim |
| `bloating` | CONCEPT | 1 | H1:claim |
| `cannot` | CONCEPT | 1 | H2:claim |
| `checkbox` | CONCEPT | 1 | H1:claim |
| `chronic` | CONCEPT | 1 | H2:claim |
| `clinical` | CONCEPT | 1 | H2:claim |
| `collapsing` | CONCEPT | 1 | H3:claim |
| `compute` | CONCEPT | 1 | H3:claim |
| `conflates` | CONCEPT | 1 | H1:claim |
| `constipation` | CONCEPT | 1 | H1:claim |
| `could` | CONCEPT | 2 | H2:alternative_explanations, H3:claim |
| `cramping` | CONCEPT | 1 | H1:claim |
| `criteria` | CONCEPT | 1 | H2:claim |
| `data` | CONCEPT | 1 | H2:claim |
| `dedicated` | CONCEPT | 1 | H2:alternative_explanations |
| `detail` | CONCEPT | 1 | H1:alternative_explanations |
| `diarrhea` | CONCEPT | 1 | H1:claim |
| `discarding` | CONCEPT | 1 | H3:alternative_explanations |
| `distinction` | CONCEPT | 1 | H3:claim |
| `distinguishing` | CONCEPT | 1 | H2:claim |
| `does` | CONCEPT | 1 | H2:claim |
| `doesn` | CONCEPT | 1 | H3:claim |
| `duration` | CONCEPT | 2 | H2:alternative_explanations, H2:claim |
| `event` | CONCEPT | 2 | H3:alternative_explanations, H3:claim |
| `evidence` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `existing` | CONCEPT | 1 | H1:alternative_explanations |
| `exposes` | CONCEPT | 1 | H3:claim |
| `field` | CONCEPT | 2 | H1:alternative_explanations, H2:alternative_explanations |
| `free-text` | CONCEPT | 1 | H1:alternative_explanations |
| `frequency` | CONCEPT | 1 | H2:claim |
| `generic` | CONCEPT | 1 | H1:claim |
| `infer` | CONCEPT | 1 | H2:alternative_explanations |
| `issue` | CONCEPT | 1 | H1:claim |
| `label` | CONCEPT | 1 | H1:claim |
| `like` | CONCEPT | 1 | H1:claim |
| `log` | CONCEPT | 1 | H2:claim |
| `logged-symptom` | CONCEPT | 1 | H3:claim |
| `model` | CONCEPT | 2 | H3:alternative_explanations, H3:claim |
| `nurses` | CONCEPT | 4 | H1:alternative_explanations, H2:alternative_explanations, H2:claim, H3:claim |
| `one` | CONCEPT | 2 | H1:claim, H3:claim |
| `only` | CONCEPT | 1 | H3:claim |
| `originates` | CONCEPT | 1 | H3:alternative_explanations |
| `own` | CONCEPT | 1 | H3:claim |
| `pattern` | CONCEPT | 1 | H2:claim |
| `picker` | CONCEPT | 2 | H1:claim, H3:alternative_explanations |
| `presentation` | CONCEPT | 1 | H2:claim |
| `queue` | CONCEPT | 1 | H3:claim |
| `reading` | CONCEPT | 1 | H1:alternative_explanations |
| `record` | CONCEPT | 3 | H1:citation_cards.title, H2:citation_cards.title, H3:citation_cards.title |
| `rectal` | CONCEPT | 1 | H1:claim |
| `red-flag` | CONCEPT | 1 | H1:claim |
| `red-flag-vs-benign` | CONCEPT | 1 | H3:claim |
| `require` | CONCEPT | 1 | H2:claim |
| `signal` | CONCEPT | 1 | H3:alternative_explanations |
| `single` | CONCEPT | 1 | H1:claim |
| `solely` | CONCEPT | 1 | H3:alternative_explanations |
| `standard` | CONCEPT | 1 | H2:claim |
| `stomach` | CONCEPT | 1 | H1:claim |
| `submission` | CONCEPT | 1 | H2:alternative_explanations |
| `surface` | CONCEPT | 1 | H3:claim |
| `symptom` | CONCEPT | 3 | H1:claim, H2:claim |
| `symptoms` | CONCEPT | 1 | H1:claim |
| `tier` | CONCEPT | 1 | H3:claim |
| `timestamps` | CONCEPT | 1 | H2:alternative_explanations |
| `undertrained` | CONCEPT | 1 | H1:alternative_explanations |
| `undifferentiated` | CONCEPT | 2 | H1:claim, H3:claim |
| `uses` | CONCEPT | 1 | H1:claim |
| `without` | CONCEPT | 1 | H2:alternative_explanations |
| `90` | METRIC | 1 | checkpoint:registration.success_rule |
| `GI` | METRIC | 1 | checkpoint:registration.failure_rule |
| `absent` | METRIC | 1 | H1:discriminating_information |
| `accuracy` | METRIC | 1 | H2:discriminating_information |
| `actually` | METRIC | 1 | H2:falsifier |
| `alone` | METRIC | 1 | H1:falsifier |
| `already` | METRIC | 2 | H1:falsifier, H3:falsifier |
| `available` | METRIC | 1 | H2:discriminating_information |
| `backend` | METRIC | 1 | H3:discriminating_information |
| `benign` | METRIC | 2 | H3:falsifier, checkpoint:registration.failure_rule |
| `can` | METRIC | 1 | H1:falsifier |
| `comparison` | METRIC | 1 | H2:discriminating_information |
| `data` | METRIC | 2 | H2:discriminating_information, H2:falsifier |
| `depend` | METRIC | 1 | H2:falsifier |
| `different` | METRIC | 1 | H3:falsifier |
| `distinguish` | METRIC | 1 | H1:falsifier |
| `does` | METRIC | 1 | H2:falsifier |
| `duration` | METRIC | 2 | H2:discriminating_information, H2:falsifier |
| `entry` | METRIC | 1 | checkpoint:registration.success_rule |
| `frequency` | METRIC | 1 | H2:falsifier |
| `keyword` | METRIC | 1 | H3:discriminating_information |
| `label` | METRIC | 2 | H1:discriminating_information, H1:falsifier |
| `log` | METRIC | 1 | H3:discriminating_information |
| `measured` | METRIC | 1 | H1:discriminating_information |
| `nurse` | METRIC | 3 | H1:discriminating_information, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `nurses` | METRIC | 1 | H1:falsifier |
| `pilot` | METRIC | 1 | checkpoint:registration.failure_rule |
| `positions` | METRIC | 1 | H3:falsifier |
| `present` | METRIC | 2 | H1:discriminating_information, H3:discriminating_information |
| `queue` | METRIC | 1 | H3:falsifier |
| `queue-row` | METRIC | 1 | H3:discriminating_information |
| `red-flag` | METRIC | 5 | H3:discriminating_information, H3:falsifier, checkpoint:registration.failure_rule, checkpoint:registration.success_rule |
| `reliably` | METRIC | 1 | H1:falsifier |
| `render` | METRIC | 2 | H3:discriminating_information, H3:falsifier |
| `showing` | METRIC | 1 | H3:discriminating_information |
| `single` | METRIC | 1 | H1:falsifier |
| `structured` | METRIC | 1 | H2:discriminating_information |
| `subtype` | METRIC | 1 | H1:discriminating_information |
| `surfaced` | METRIC | 1 | H3:discriminating_information |
| `symptom` | METRIC | 1 | checkpoint:registration.failure_rule |
| `symptoms` | METRIC | 1 | H3:falsifier |
| `triage` | METRIC | 3 | H2:discriminating_information, H2:falsifier, checkpoint:registration.failure_rule |
| `triage-time` | METRIC | 1 | H1:discriminating_information |
| `urgency` | METRIC | 2 | H1:falsifier, H2:falsifier |
| `visibly` | METRIC | 1 | H3:falsifier |
| `was` | METRIC | 1 | H3:discriminating_information |
| `whether` | METRIC | 1 | H3:discriminating_information |
| `without` | METRIC | 1 | H2:discriminating_information |
| `ผิดเป็น` | METRIC | 1 | checkpoint:registration.failure_rule |
| `มี` | METRIC | 1 | checkpoint:registration.failure_rule |
| `ลดลงต่ำกว่า` | METRIC | 1 | checkpoint:registration.success_rule |
| `วินาทีต่อเคส` | METRIC | 1 | checkpoint:registration.success_rule |
| `หรือ` | METRIC | 1 | checkpoint:registration.failure_rule |
| `ออกจากคิว` | METRIC | 1 | checkpoint:registration.success_rule |
| `เคสใดถูก` | METRIC | 1 | checkpoint:registration.failure_rule |
| `เคสไหนถูกมองข้าม` | METRIC | 1 | checkpoint:registration.success_rule |
| `เวลาเฉลี่ยที่` | METRIC | 1 | checkpoint:registration.success_rule |
| `โดยไม่มี` | METRIC | 1 | checkpoint:registration.success_rule |
| `ใช้เวลาแยกเคสนานขึ้นกว่าก่อน` | METRIC | 1 | checkpoint:registration.failure_rule |
| `ใช้แยก` | METRIC | 1 | checkpoint:registration.success_rule |
| `GI` | PROCESS | 1 | H1:mechanism |
| `adding` | PROCESS | 2 | H1:predicted_readout, H2:predicted_readout |
| `against` | PROCESS | 1 | H2:mechanism |
| `all` | PROCESS | 1 | H1:mechanism |
| `any` | PROCESS | 1 | H3:predicted_readout |
| `apply` | PROCESS | 1 | H2:predicted_readout |
| `captures` | PROCESS | 1 | H2:mechanism |
| `case` | PROCESS | 1 | H1:predicted_readout |
| `categories` | PROCESS | 1 | H1:predicted_readout |
| `categorize` | PROCESS | 1 | checkpoint:system_graph.edges |
| `category` | PROCESS | 2 | H1:mechanism, H2:mechanism |
| `change` | PROCESS | 1 | H3:predicted_readout |
| `clinical` | PROCESS | 4 | H1:mechanism, H2:mechanism, H2:predicted_readout, H3:mechanism |
| `computed` | PROCESS | 1 | H3:predicted_readout |
| `criteria` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `dashboard` | PROCESS | 1 | H3:mechanism |
| `data` | PROCESS | 1 | H2:mechanism |
| `designed` | PROCESS | 1 | H1:mechanism |
| `directly` | PROCESS | 1 | H2:predicted_readout |
| `display` | PROCESS | 1 | H1:predicted_readout |
| `distinguishable` | PROCESS | 3 | H1:predicted_readout, H3:mechanism, H3:predicted_readout |
| `duration` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `emits` | PROCESS | 1 | H3:mechanism |
| `entry` | PROCESS | 3 | H1:mechanism, H1:predicted_readout, H3:predicted_readout |
| `escalate` | PROCESS | 1 | checkpoint:system_graph.edges |
| `evaluate` | PROCESS | 1 | H2:mechanism |
| `even` | PROCESS | 1 | H3:mechanism |
| `event` | PROCESS | 3 | H3:mechanism, H3:predicted_readout |
| `fast` | PROCESS | 1 | H1:mechanism |
| `field` | PROCESS | 4 | H2:mechanism, H2:predicted_readout, H3:mechanism, H3:predicted_readout |
| `free-text` | PROCESS | 2 | H2:mechanism, H3:mechanism |
| `frequency` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `has` | PROCESS | 1 | H3:mechanism |
| `have` | PROCESS | 1 | H2:mechanism |
| `ingestion` | PROCESS | 1 | H3:predicted_readout |
| `keywords` | PROCESS | 1 | H3:mechanism |
| `label` | PROCESS | 1 | H1:predicted_readout |
| `lets` | PROCESS | 3 | H1:predicted_readout, H2:predicted_readout, H3:predicted_readout |
| `log-symptom` | PROCESS | 1 | checkpoint:system_graph.edges |
| `map` | PROCESS | 1 | H1:mechanism |
| `model` | PROCESS | 2 | H3:mechanism, H3:predicted_readout |
| `note` | PROCESS | 1 | H2:mechanism |
| `open-case` | PROCESS | 1 | checkpoint:system_graph.edges |
| `opening` | PROCESS | 1 | H1:predicted_readout |
| `patient` | PROCESS | 1 | H1:mechanism |
| `patient-facing` | PROCESS | 1 | H3:predicted_readout |
| `pattern` | PROCESS | 1 | H2:predicted_readout |
| `pattern-based` | PROCESS | 1 | H2:mechanism |
| `picker` | PROCESS | 1 | H1:mechanism |
| `point-in-time` | PROCESS | 1 | H2:mechanism |
| `present` | PROCESS | 1 | H3:mechanism |
| `queue` | PROCESS | 3 | H1:predicted_readout, H2:predicted_readout, H3:predicted_readout |
| `red-flag` | PROCESS | 1 | H3:mechanism |
| `regardless` | PROCESS | 1 | H3:mechanism |
| `render` | PROCESS | 2 | H3:mechanism, H3:predicted_readout |
| `render-queue-row` | PROCESS | 1 | checkpoint:system_graph.edges |
| `rows` | PROCESS | 2 | H3:mechanism, H3:predicted_readout |
| `same` | PROCESS | 1 | H1:mechanism |
| `schema` | PROCESS | 1 | H2:mechanism |
| `severity` | PROCESS | 1 | H3:mechanism |
| `signal` | PROCESS | 1 | H3:mechanism |
| `single` | PROCESS | 1 | H3:mechanism |
| `standard` | PROCESS | 1 | H2:predicted_readout |
| `structured` | PROCESS | 2 | H2:mechanism, H2:predicted_readout |
| `submission` | PROCESS | 1 | H1:mechanism |
| `subtype` | PROCESS | 1 | H1:predicted_readout |
| `subtypes` | PROCESS | 1 | H1:mechanism |
| `surfaced` | PROCESS | 1 | H3:predicted_readout |
| `symptom` | PROCESS | 2 | H1:mechanism |
| `symptom-entry` | PROCESS | 1 | H2:mechanism |
| `symptom-logged` | PROCESS | 1 | H3:mechanism |
| `taxonomy` | PROCESS | 1 | H1:mechanism |
| `though` | PROCESS | 1 | H3:mechanism |
| `time` | PROCESS | 1 | H1:mechanism |
| `triage` | PROCESS | 1 | H2:predicted_readout |
| `triage-queue` | PROCESS | 1 | H3:mechanism |
| `type` | PROCESS | 1 | H3:mechanism |
| `urgency-tier` | PROCESS | 1 | H3:predicted_readout |
| `value` | PROCESS | 1 | H1:mechanism |
| `was` | PROCESS | 1 | H1:mechanism |
| `without` | PROCESS | 2 | H1:predicted_readout, H3:predicted_readout |
| `CROSS_ADAPTIVE` | PROTOCOL | 1 | H2:lane |
| `DESIGN_HYPOTHESIS` | PROTOCOL | 1 | H3:causal_tier |
| `GENERATIVE_TRANSFORMATIVE` | PROTOCOL | 1 | H3:lane |
| `GI symptom triage taxonomy` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `KNOWN_DIRECT` | PROTOCOL | 1 | H1:lane |
| `MECHANISM_HYPOTHESIS` | PROTOCOL | 1 | H1:causal_tier |
| `STRUCTURAL_HYPOTHESIS` | PROTOCOL | 1 | H2:causal_tier |
| `TARGETED_SEARCH` | PROTOCOL | 1 | checkpoint:review_mode |
| `event-schema granularity redesign` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `red-flag symptom escalation protocol` | PROTOCOL | 1 | checkpoint:translation.adapter_cards |
| `synthetic benign-entry replay` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `synthetic red-flag-entry replay` | PROTOCOL | 1 | checkpoint:causal_analysis.controls |
| `clinical nursing triage` | ROLE | 5 | H1:affected_agencies, H2:affected_agencies, H3:affected_agencies, checkpoint:agency.affected, checkpoint:agency.voice_holders |
| `clinical nursing triage lead` | ROLE | 1 | checkpoint:agency.accountable_parties |
| `patient safety officer` | ROLE | 1 | checkpoint:agency.decision_owners |
| `patients` | ROLE | 4 | H1:affected_agencies, H3:affected_agencies, checkpoint:agency.affected, checkpoint:agency.voice_holders |
| `product engineering` | ROLE | 3 | H2:affected_agencies, H3:affected_agencies, checkpoint:agency.affected |
| `nurse` | TOOL | 1 | checkpoint:system_graph.nodes |
| `red-flag-escalation-line` | TOOL | 1 | checkpoint:system_graph.nodes |
| `symptom-entry-schema` | TOOL | 1 | checkpoint:system_graph.nodes |
| `symptom-tracker-app` | TOOL | 1 | checkpoint:system_graph.nodes |
| `triage-queue-dashboard` | TOOL | 1 | checkpoint:system_graph.nodes |

## Summary

- hypothesis cards: 3
- total distinct words: 245
- ROLE: 5 distinct words
- CONCEPT: 82 distinct words
- PROCESS: 81 distinct words
- TOOL: 5 distinct words
- PROTOCOL: 12 distinct words
- METRIC: 60 distinct words
