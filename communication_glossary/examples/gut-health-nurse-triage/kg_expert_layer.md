# kg_expert_layer — HYP-SKILLME-GUT-NURSE-DEMO-001 (AI-INTERPRETIVE, OPEN TIER)

**This is NOT a readout.** Unlike kg_raw_word.md (a deterministic extraction — every
node is a literal fact about what text appeared where), everything below is an AI's
judgment call about what expertise is relevant. Treat it as a starting point for a
human expert (a real nurse, a real clinical informaticist) to confirm or correct,
not as validated fact. Tier: Open (per this workspace's readout-not-truth
discipline) until reviewed by an actual domain expert.

## Domain(s) identified

- **Clinical GI symptom taxonomy / triage nursing** — H1 and H3 both center on the
  gap between a single "stomach issue" label and the distinct clinical symptom
  categories (and their differing urgency) a nurse actually needs to triage on.
- **Functional/chronic GI diagnostic criteria** — H2's proposed duration/frequency
  field maps directly onto the data clinical diagnostic criteria for GI disorders
  actually require.
- **Emergency/urgency triage acuity scoring** — H3's "compute an urgency tier the
  backend already has signal for but doesn't surface" is precisely what a formal
  triage acuity framework does.
- **Health data interoperability / structured clinical coding** — the underlying
  engineering fix all three hypotheses gesture toward (a controlled symptom
  vocabulary instead of free text) is a solved problem in health IT with a real
  named standard.

## Relevant frameworks/methodologies per domain

- **Rome IV criteria (Disorders of Gut-Brain Interaction, DGBI)** — the current,
  active diagnostic framework for functional GI disorders (IBS, functional
  bloating, etc.), and it explicitly requires duration/frequency data (e.g. IBS:
  recurrent abdominal pain ≥1 day/week over the last 3 months, onset ≥6 months
  prior) — exactly the structured field H2 proposes adding and the app currently
  lacks. A 2024 validation study found relaxing the frequency threshold to 3
  days/month improved diagnostic performance (90.2% sensitivity, 85.1%
  specificity) without losing specificity, showing this is an actively-refined,
  current framework, not a static/outdated one. Confidence: VERIFIED-VIA-SEARCH.
- **NICE-guideline-style GI "red flag"/alarm symptoms (rectal bleeding, weight
  loss, altered bowel habit, anemia)** — the exact, real, named clinical concept
  H1 and H3 gesture at informally ("red-flag symptoms like rectal bleeding").
  Confirmed current: NICE CG27 referral criteria (rectal bleeding + bowel-habit
  change, age-stratified two-week-wait referral) are still the reference alarm-
  symptom framework cited in current (2023-2024) clinical literature. Confidence:
  VERIFIED-VIA-SEARCH.
- **Emergency Severity Index (ESI)** — a real, current, 5-level nurse triage
  acuity framework (not specific to GI, but directly the class of tool H3's
  "compute an urgency tier the backend already has signal for" is reinventing
  ad hoc). Confirmed still in active use and under active validation research as
  of 2024-2025 (diagnostic-accuracy meta-analyses, reliability studies).
  Confidence: VERIFIED-VIA-SEARCH.
- **SNOMED CT** — the real, current, internationally-maintained structured
  clinical terminology standard that already has a dedicated "Gastrointestinal
  symptom (finding)" concept (ID 267045008) with subtype hierarchy via "is a"
  relationships. This is the named standard H1's proposed symptom-subtype
  taxonomy would be reinventing informally; adopting SNOMED CT GI-symptom codes
  instead of an app-specific enum would also solve H2's cross-system
  interoperability angle for free. Confidence: VERIFIED-VIA-SEARCH.
- **Event-driven schema design with a computed/derived field at ingestion**
  (applies to H3's proposal to compute an urgency tier from free-text at
  ingestion rather than at render time) — a standard, well-established software-
  engineering pattern (enrich-at-ingestion vs. compute-at-read), not searched
  this session since it's general engineering knowledge rather than a
  domain-specific named clinical standard. Confidence: MEDIUM (asserted, not
  independently verified this session for a more specific named pattern beyond
  the generic description).

## What I verified via WebSearch vs. asserted from training knowledge

- **Rome IV / DGBI current status, duration/frequency requirements, and the 2024
  validation-study finding** — SEARCHED. Sources:
  [Rome IV Criteria | The Rome Foundation](https://theromefoundation.org/rome-iv/rome-iv-criteria/),
  [Validating Simple Modifications to the Rome IV Criteria (2024)](https://eprints.whiterose.ac.uk/id/eprint/220205/3/Aliment%20Pharmacol%20Ther%20-%202024%20-%20Goodoory%20-%20Validating%20Simple%20Modifications%20to%20the%20Rome%20IV%20Criteria%20for%20the%20Diagnosis%20of.pdf),
  [The road to Rome IV and beyond (PubMed)](https://pubmed.ncbi.nlm.nih.gov/40613853/)
- **Emergency Severity Index (ESI) — current status, GI-relevant red-flag
  handling** — SEARCHED. Sources:
  [Emergency Severity Index — Wikipedia](https://en.wikipedia.org/wiki/Emergency_Severity_Index),
  [Diagnostic test accuracy of the ESI: systematic review and meta-analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12382730/)
- **SNOMED CT gastrointestinal-symptom coding, current standard status** —
  SEARCHED. Sources:
  [SNOMED CT — Gastrointestinal symptom — BioPortal](https://purl.bioontology.org/ontology/SNOMEDCT/267045008),
  [SNOMED CT Clinical Decision Support Guide](https://docs.snomed.org/snomed-ct-practical-guides/snomed-ct-clinical-decision-support-guide/1-introduction/1.1-overview)
- **NICE-guideline GI red-flag/alarm symptoms, current referral criteria** —
  SEARCHED. Sources:
  [Rectal Bleeding — StatPearls (NCBI)](https://www.ncbi.nlm.nih.gov/books/NBK563143/),
  [Alarm Symptoms: A Cause For Alarm? (IFFGD)](https://iffgd.org/gi-disorders/symptoms-causes/alarm-symptoms/)
- **Event-driven "compute-at-ingestion" schema pattern** — ASSERTED (general
  software-engineering knowledge, not independently searched this session; this
  is the weakest-sourced claim in this document).
- **Whether this exact app/org would be SNOMED CT-licensed or has any real
  clinical-data-governance process** — NOT knowable from the checkpoint (it's a
  synthetic fixture, `metadata.simulation: true`) — flagged as open below, not
  asserted either way.

## Vocabulary this adds beyond kg_raw_word.md's raw extraction

None of the following appear as literal words/phrases in the checkpoint text
(checked against kg_raw_word.md's word table) — they are this layer's
interpretive contribution:

- Rome IV criteria / disorders of gut-brain interaction (DGBI)
- NICE CG27 / two-week-wait referral criteria
- Emergency Severity Index (ESI) — the checkpoint never names any formal triage
  acuity framework, even though H3 is functionally proposing one
- SNOMED CT (concept 267045008, "Gastrointestinal symptom (finding)")
- The specific 6-month-onset / 3-month-active / ≥1-day-per-week diagnostic
  thresholds Rome IV actually uses (the checkpoint's H2 says "duration/frequency"
  generically, never these concrete numbers)
- "Alarm symptoms" / "red-flag features" as the formal clinical term-of-art
  (the checkpoint's H1/H3 use "red-flag" informally, without citing that this is
  itself established clinical vocabulary with a specific, named symptom list)

## Open questions / where a human expert should override this

- **Is SNOMED CT actually licensed/available to this org?** SNOMED CT requires a
  national/regional license in many jurisdictions — adopting it isn't free even
  though it's the technically correct named standard. The checkpoint gives no
  evidence either way (synthetic fixture).
- **Would ESI (an emergency-department-specific tool) actually transfer to an
  outpatient app-based triage context**, or does outpatient/telehealth GI triage
  have its own more specific named acuity framework this session didn't surface?
  Flagged as the weakest domain-fit claim among the VERIFIED-VIA-SEARCH items.
- **The Rome IV frequency-threshold modification (3 days/month) is from a single
  2024 validation study**, not yet necessarily adopted into mainstream clinical
  practice guidelines — a domain expert should confirm current guideline status
  rather than treating this as settled.
- **Whether the app's free-text field genuinely contains a detectable "red-flag
  keyword" signal (H3's premise)** is itself unverified — this layer can name the
  clinical vocabulary red-flag detection would need to match against, but cannot
  confirm the NLP/keyword-detection engineering claim H3 makes.
