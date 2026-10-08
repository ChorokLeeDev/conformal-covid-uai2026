# Bounded UAI statistical review — frozen baseline

This is a delegated model audit, not human peer review or external replication.
One bounded cycle was authorized. Existing audit verdicts were available as leads;
this is not claimed to be an unprimed independent review. No new training was
planned. Initial findings were sent to the coordinating reviewer before edits.

## Baseline and scope

- Repository: `ChorokLeeDev/conformal-covid-uai2026`.
- Reviewed and remotely checked main: `533814f27add9dd05bcebb74e71ea21bfeb76649`.
- Active source: `paper/main.tex`, SHA-256
  `6d952c111561dd8e4f276474afc538fd1ea08048924ec2d246f764cd5889db7d`.
- Active PDF: `audit/2026-10-08/revision/uai-statistical-audit-revision.pdf`,
  SHA-256 `5d46a447a9f0972660acb228c566eaeb0fda93b4fa365c4c09454bd0c400a9f9`.
- `paper/main.pdf` and all submission PDFs/ZIPs are preserved historic artifacts,
  not the active revised manuscript. Their bytes match original commit
  `96d9616961e5ae8607373181d35262cb21a2b0d1`; active TeX differs from submitted TeX.
- No repository AGENTS.md was present. Read the materialized paper-revision-loop
  skill and its records/validation references. Revision uses a dedicated branch.
- Inspected current TeX, reference APS code, archived APS code, earlier audit
  records, recovered aggregate JSONs, relevant upstream source in the preserved
  ZIP, and original/submitted provenance. Private raw/model payload is absent in
  this fresh checkout; LightGBM is not installed. Full replay was not attempted.

## New and residual findings

### UAI-N01 — Medium: finite-sample dismissal is numerically false and logically unsupported

**Location:** baseline `paper/main.tex:440`.

The paragraph claims the correction is below `3e-5` for every task and thus cannot
affect observed coverage gaps. The archived class actually uses
`u_n = ceil((n+1)*0.9)/n` followed by NumPy linear interpolation. With the stated
sales calibration size 35,737, `u_n-0.9 = 4.756974564e-5`; item size 146,948 gives
`1.224923102e-5`. The notation also confuses quantile level with score threshold.

A small level increment cannot bound the change in a discontinuous target
coverage event. Valid binary APS calibration scores with `k-1` scores equal to
0.6 and the rest 1 produce nominal-linear threshold 0.6 but corrected exact
threshold 1. Separately, `k` scores equal to 0.6 and the rest 1 produce exact
threshold 0.6 versus archived interpolated threshold 0.63998097 at the sales
size. In the actual archived crossing-set implementation, a fixed shifted target
atom can change coverage from zero to one in either comparison. These witnesses
isolate rank correction and interpolation; they do not estimate the historical
effect. Resolution: correct levels and withdraw the coverage-effect dismissal
pending original score arrays.

### UAI-N02 — Medium: inclusive APS score direction is not true-label confidence

**Locations:** baseline `paper/main.tex:680–682,709`.

Higher inclusive APS score is described as lower confidence in the correct class;
leftward score shifts are interpreted as increased confidence, possibly caused
by reduced product diversity. For a top-ranked true label, binary probabilities
`(0.6,0.4)` and `(0.9,0.1)` give scores 0.6 and 0.9. Confidence and score increase
together, contradicting the asserted direction. KS/mean summaries cannot recover
the confidence or diversity interpretation. Resolution: describe scores as rank
cumulative mass and retain only the reported distribution comparisons.

### UAI-N03 — Medium: alternative-model comparison mixes seed aggregation and mislabels LightGBM

**Locations:** baseline `paper/main.tex:434,746–750,781`; archived supplement
`run_50seed_ensemble.py:224` and `src/run_aci_experiment.py:271`.

The model section describes seed-42 alternative models, but its LightGBM drop
column repeats the main 50-seed means. The table should make the unmatched
aggregation explicit. Its LightGBM method is labeled GOSS, contradicting the
documented and supplied `boosting_type='gbdt'`. Also, "all models" overextends the
50-seed LightGBM settings to alternative/follow-up fits. The model correlations
themselves recompute correctly from the displayed rounded values (RF 0.2994,
XGB 0.5476, CB 0.6667, MLP 0.4286). Resolution: label the historical aggregations,
scope settings to their source, and correct the algorithm label; do not invent
a matched model-family rerun.

### UAI-N04 — High: residual mechanism claims contradict the corrected evidence status

**Locations:** baseline `paper/main.tex:232–236,312–316`.

The active text still says two factors account for much of the variance,
concentration "determines vulnerability", and native-gain differences arise from
cardinality confounding. These are stronger than the saved historical summaries,
missing original feature/model ledger, and non-replicating follow-up panel can
establish. The corrected theorem concerns a separate probability-mixture weight;
it cannot validate these measured-SHAP causal claims. This is a residual scope
failure, not a new empirical disproof of the original results. Resolution: narrow
these passages to descriptive historical hypotheses and retain the failed
follow-up replication prominently.

## Verified or unresolved central claims

| Claim | Status at review | Evidence and limit |
|---|---|---|
| Repaired probability-mixture proposition | No new defect found in bounded proof review | Rank complement, pointwise bound, event implication, derivative and boundary cases follow under the stated fixed-quantity assumptions; no empirical SHAP identification follows. |
| Exact APS helper membership/order statistic | Targeted checks pass | All 8 existing synthetic/statistical checks pass; this does not certify historical pipelines. |
| Follow-up negative task associations | Aggregate arithmetic verified | Saved eight-task means reproduce rho −0.238095 and −0.261905; private models/raw data were not replayed this round. |
| Original 50-seed results | Unavailable for reproduction | Original per-row probabilities, fitted models and SHAP ledgers remain missing. |
| Archived/follow-up distinction | Verified | Current source and PDF hashes match the preceding verification record; original submissions remain byte-identical. |
| Novelty and primary citation support | Outside this round | No new literature search or venue-readiness assessment. |

No acceptance score, consensus target or additional model-search budget was used.
