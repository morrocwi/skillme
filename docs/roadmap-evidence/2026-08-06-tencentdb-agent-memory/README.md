# Evidence trail — TencentDB Agent Memory synthesis (2026-08-06)

Backing record for the `### TencentDB Agent Memory synthesis` entry in `SKILLME.md` §14
(Development roadmap). SKILLME.md carries the compressed, registered form; these two files are the
uncompressed intermediate output of the two ultracode Workflow runs that produced it, kept for
lineage per `SKILLME-A0` (finite record) and `SKILLME-A11` (correction is reliability — round 2's
corrections to round 1 should stay inspectable, not just their final merged form).

- `round1-filter-draft.md` — output of workflow run `wf_bc008523-67c` (research → philosophy-filter
  → adversarial-verify → synthesize against `github.com/TencentCloud/TencentDB-Agent-Memory`).
  52 mechanisms found, 35 survived, 17 rejected. This is the *pre-round-2* draft — three of its
  claims were later found imprecise and corrected (see round 2 file, items 1/4/6/10).
- `round2-verified-walkthrough.md` — output of workflow run `wf_514d162a-de2`. Text-only simulation
  (no code written) of the 5 round-1 survivors that have a real, existing attachment point in this
  repo's actual code today, each re-verified against live source (`kg_extract.py`,
  `kg_accumulate.py`, `hypothesis_runner.py`, `hypothesis_checker.py`) a second time. Found and
  corrected: a wrong file citation (item 1), an inaccurate hash-provenance claim (item 6), an
  overbroad "zero references" claim (item 10), and one genuine axiom conflict in the originally
  proposed field naming for item 4 (`checked_found`/`checked_absent` collided with `SKILLME-A4`/
  `SKILLME-A10` — corrected to `maker_found`/`maker_absent`/`not_yet_run`).

Both files are raw workflow output, not independently copyedited — read them as intermediate
working record, not as the citable form. `SKILLME.md` is the citable form.
