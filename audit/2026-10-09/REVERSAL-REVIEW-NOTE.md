# UAI revision note — 2026-10-09 (reversal review)

Companion to the 2026-10-08 audit/recovery. This reviews the prior cycle's
9-commit withdrawal of ~124 manuscript lines and **selectively reverses
over-deletions** where the recovered 24-model refit evidence supports the claim,
while leaving correct withdrawals in place. Submission artifacts unmodified.

## Method

A structured review mapped ~30 materially removed/weakened claims
(camera-ready `b8717c4` → HEAD) and adjudicated each against
`audit/2026-10-08/recovery/` (refit-comparison.json — all 24 fits / 528 arrays
bit-identical; shift_detection_comparison.json; manuscript_claims_snapshot.json)
with two independent lenses (recover vs. rigor).

## Outcome: discerning, not blanket, reversal

- **Most QUALIFY items were already correct in HEAD** — the prior session kept
  the verified numbers and dropped only unsupported causal/prospective framing.
  No change needed (e.g. ρ=0.833 LOO, external transfer counts, Theorem recast).
- **Correctly KEEP-REMOVED (removal was justified):** the headline cross-domain
  ρ=0.853 "pre-deployment diagnostic / prospective" claim, the all-17-task
  ρ=0.654, model-sensitivity ρ=0.833-vs-0.30, retraining +19pp (single seed,
  Holm p=0.11), bootstrap CI, partial correlation, ACI recovery. The recovered
  **follow-up panel gives ρ=−0.238/−0.262** (does NOT reproduce the positive
  association), so these withdrawals stand.

## Genuine over-hedge reversed (this revision)

The within-SALT shift-detector comparison was hedged as "await reproducible
outputs / if reproduced would describe" — but `shift_detection_comparison.json`
reproduces it exactly against the 8 SALT tasks' coverage drops. **Restored** as a
descriptive within-SALT (n=8) finding: SHAP concentration ranks severity
(ρ=0.833, p=0.010) where MMD (−0.05), C2ST (0.19), PSI (≤0.07) do not — keeping
every honest caveat (PSI implementation defect; no generalization claim) and
explicitly flagging that the 3-seed follow-up panel does not reproduce the
positive association, so this is descriptive, not a validated prospective claim.
Edited: abstract-adjacent contribution bullet, Related Work (Shift Detection),
§Comparison with Standard Shift Detection.

## Unmerged branch `revision/arxiv-replacement-package-20261009` (be2265d)

Left intact (not merged, not deleted). It moves the manuscript *further* toward
retraction (relabels result tables "Historical … Original Runs Unverified") and
ships a built arXiv replacement package. Its direction conflicts with this
evidence-based restoration, so its main.tex relabels were **not** adopted; its
one additive factual clarification (labels outside the training alphabet counted
as uncovered) is already consistent with HEAD. A fresh arXiv package reflecting
the restored manuscript should be built before any submission.

## Status

Revision **prepared**, not submitted. UAI 2026 camera-ready and the paper's
arXiv record are unchanged. AI-agent recovery/verification, not human review.
