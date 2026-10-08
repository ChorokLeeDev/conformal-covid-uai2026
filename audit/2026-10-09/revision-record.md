# Bounded statistical clarification milestone

Baseline: `533814f27add9dd05bcebb74e71ea21bfeb76649`, checked against remote main.
Branch: `revision/bounded-statistical-review-20261009`. One substantive review
cycle; no fitting, tuning, new data access or historical result replacement.
The coordinating reviewer authorized these narrow corrections after the initial
findings. No remote write or paper submission occurred in this delegated pass.

## Before/after claim ledger

| Issue | Before | Corrected claim | Verification and remaining limit |
|---|---|---|---|
| UAI-N01 | Quantile correction below `3e-5` for every task; hence finite-sample effects cannot contribute to gaps | Correct historical level increments; distinguish level, score threshold and coverage; historical effects unquantified | Four valid binary APS witnesses execute the archived calibration/crossing implementation. Rank correction and interpolation are isolated. No original score distribution is inferred. |
| UAI-N02 | Larger APS score means lower true-label confidence; lower scores imply increased confidence and possibly reduced diversity | Inclusive score is rank cumulative mass and is not monotone in true-label confidence | Top-ranked true-label probability 0.6 to 0.9 produces score 0.6 to 0.9. KS/mean shifts retain their descriptive meaning only. |
| UAI-N03 | Model-family setup obscures mixed seed aggregation; labels LightGBM GOSS; settings describe all models | Alternative-model seed-42 reports are contrasted with historical 50-seed LightGBM drops; GBDT label; settings scoped to archived script | Code inspection and main/model-table comparison. Model correlations checked from rounded table points; no matched family experiment was run. |
| UAI-N04 | Feature concentration determines vulnerability; gain differences have an established cause | Historical feature/diagnostic associations are descriptive hypotheses with missing provenance and failed follow-up replication | Source diff removes these specific unsupported assertions. It does not identify a causal mechanism or validate the historical/follow-up pipelines. |

All four enumerated manuscript issues are corrected within this scope. Missing
original predictions/models/SHAP arrays, decision-time feature contracts and
prospective external validity remain unresolved. The repaired mixture theorem
was checked analytically and no new defect found, under its explicit assumptions;
the observed SHAP ratio is still not its mixture weight.

## Executed validation

1. `python audit/2026-10-08/check_statistical_claims.py` — exit 0; all eight
   existing checks passed. Output: `existing-checks-output.txt`.
2. `python audit/2026-10-09/check_revision_claims.py > audit/2026-10-09/claim-check-output.json`
   — exit 0. Four quantile witnesses and one confidence witness passed; both
   recovered eight-task correlations match saved aggregate JSON. The script
   records Python/NumPy/SciPy versions and code hashes. No random trials or model
   runs are involved. This was a retrospective discriminating check, not a
   preregistered experiment.
3. Separate inline rounded-table calculations recover RF rho 0.2994066,
   XGBoost 0.5476190, CatBoost 0.6666667 and MLP 0.4285714. Recovered panel rho is
   −0.2380952 inclusive and −0.2619048 crossing. These are arithmetic checks, not
   new fitted-model or population evidence.
4. `git diff --check` — exit 0. Original PDFs/ZIPs and the previous revised PDF
   match baseline bytes; hashes are retained in `verification.json`.
5. The PDF operation marker ran once successfully. Final clean build command:

   ```sh
   TEXINPUTS=paper//: BIBINPUTS=paper//: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/workspace/scratch/ab1459f847c7/uai-final-build-WcfyP8 -jobname=uai-bounded-statistical-revision paper/main.tex
   ```

   The final build, `pdfinfo`, `pdftotext -layout` and `pdftoppm -r 105 -png`
   completed successfully. The verified closed PDF was copied atomically to
   `revision/uai-bounded-statistical-revision.pdf`; subsequent reads verified
   its hash and 23 pages. Pages 5, 6, 12, 17, 19 and 20 were visually inspected
   for the changed paragraphs/tables: no clipping or overlap observed. Final
   log has no undefined references or overfull boxes; underfull-box warnings
   remain. Compilation is not a submission-readiness assessment.
6. The coordinating reviewer independently reconstructed the sales quantile
   witness using exact rational arithmetic and the actual APS reference, and
   checked the score-confidence witness. See `root-recheck.md`; it is a separate
   targeted model recheck, not external replication or a new unprimed full review.

## Preserved execution failures

The initial build reported a 23-page PDF, but a subsequent read found that its
PDF and auxiliary output were truncated. A forced retry failed on its empty
auxiliary bibliography state. A second staging output also became unreadable
after the build returned. No scientific source changes were made to work around
this. A fresh unique staging build, same source, followed by same-command PDF
parsing/rendering and atomic final-file copy succeeded; the final artifact was
then verified again from a later command. Initial/retry/staging/final build
stdout is preserved with trailing whitespace normalized and non-UTF-8 diagnostic font bytes replaced; scientific output is unchanged. The cause of transient build-output truncation is not
established. An initial verification script also encountered a non-UTF-8 byte
in the TeX log; decoding that diagnostic log with replacement permitted the
ASCII error checks. No manuscript/output bytes were altered for that purpose.

## Final artifacts

- Active TeX SHA-256:
  `1195a39a006f16bb61cd712b9156dbe33768f6dc8b05a7593b5d925994917962`.
- New PDF SHA-256:
  `4afad8409176223827c0872862cf7a00a0a25cb0dee88cb980fce7c8b44cbc79`.
- Historical numerical tables are preserved; protocol descriptions and one
  algorithm label are corrected. Existing experimental code is unchanged.
- Private raw/model replay, primary citation/novelty assessment and original
  50-seed reproduction were outside this bounded round.

The next discriminating work requires original calibration/target score ledgers
to measure quantile sensitivity, or a separately designed matched model-family
study. Further prose-only cycles cannot resolve those missing experiments.
