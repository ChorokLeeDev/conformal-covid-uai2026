# Statistical correction milestone — 2026-10-08

Baseline: `96d9616961e5ae8607373181d35262cb21a2b0d1`; revision branch:
`revision/statistical-audit-20261008`. The original initial-review.md is preserved.
This is a correction of statistical interpretation and a new reference helper,
not a rerun or independent reproduction of the historical experiments.

## Changed claims and artifacts

- Active `paper/main.tex` and README now prominently disclose unavailable raw
  experiments, test-aware preprocessing, tuning/calibration reuse and inconsistent
  historical APS sets. Original numerical tables remain labeled historical and
  unverified; no newly invented training results replace them.
- UAI-01/02/03/08: protocol discrepancies and KDD split mismatch are documented.
  Their numerical consequences remain **unresolved pending original artifacts or
  a separately labeled rerun**. Submitted ZIPs and original PDFs are immutable.
- UAI-04: withdrawn invalid negative-ICC interpretation and effective-n table;
  uncertainty is explicitly conditional on shared data, not 50 independent shifts.
- UAI-05: repaired conditional theorem with separate mixture weight, fixed tie
  order, deterministic fixed threshold, and lambda=1/q=1 boundaries. Its illustrative
  substitutions are no longer called empirical verification. No theorem for
  measured TreeSHAP concentration is claimed.
- UAI-06/07: removed general K<=3 ceiling claim and class-count explanation for
  subnominal marginal coverage; displayed all-17 sensitivity. Pooled analysis is
  exploratory; full eight-metric Holm correction is 0.0814 using unrounded p,
  not a significance claim based on rounded 0.050.
- UAI-09/10/11/12: corrected region/class conflation and benchmark identities;
  narrowed mechanism, PSI detection and clipped-ACI claims. Original protective
  feature ledger and experiment provenance are still missing.
- Additional appendix findings: removed an uncomputed Kenward–Roger p-value
  range and the claim that the Wald interval remains significant regardless of
  correction. Explicitly distinguished MLP permutation importance from TreeSHAP.
- `src/aps_reference.py` is a new deterministic score-inversion implementation
  for future reruns. It has stable class-index ties, exact finite-sample order
  statistics, +infinity for small-calibration boundaries, and one membership
  matrix for coverage/size. It does not silently modify the archived pipelines.

## Validation and actual experiment status

Retrospective audit plan: examine logical/statistical counterexamples before any
new model run, preserve reported data, and reject unsupported guarantees. No new
empirical hypothesis was tested by training models. NumPy/SciPy synthetic checks
and rounded-table recomputation are executed/validated; full model reproduction
is blocked by missing generating artifacts and results.

`python audit/2026-10-08/check_statistical_claims.py` passes 8 checks: inconsistent
archived crossing membership; coherent reference membership/size; fixed ties;
exact order statistic and small-calibration +infinity; q=1 zero-probability labels;
binary/three-class catastrophic shift counterexamples; agreement-ICC vs correlation
counterexample; published rounded-point arithmetic. Output is retained in
`validation-output.txt`. These checks are not evidence that historical experiments
were rerun or that the proposed diagnostic generalizes.

Build command from repository root:

```bash
TEXINPUTS=paper//: BIBINPUTS=paper//: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=audit/2026-10-08/revision -jobname=uai-statistical-audit-revision paper/main.tex
```

The first build failed because unused `algorithm.sty`/`algorithmic.sty` imports
were unavailable. No algorithm environment uses these packages; removing those
unused imports allowed compilation. A subsequent overwide theorem equation was
split over two displays. The revised PDF is deliberately saved under the audit
revision directory, not over `paper/main.pdf` or a submitted artifact. It is a
review draft; compilation does not establish submission readiness.

Original-file byte comparisons against the baseline commit all passed:

| Original artifact | SHA-256 |
|---|---|
| paper/main.pdf and submission/camera_ready_main.pdf | 578db042a75d5734d2ca41c780a57b20c5e592a873cee80e565dd89f517558ae |
| submission/camera_ready_source.zip | deeb181077490fd1b0f0be33cabed8bc4fbf50d8cec2c656b07ccc04c5046d1f |
| submission/supplementary_material_fixed.zip | 84bd86738b78727dae50b25b358cac7bc18ef2e9045ba324aa9db2f345bd22cf |

External citation metadata/claim-support checks remain unavailable: primary-site
HTTP requests returned proxy 403. No claim of a full literature/novelty audit is
made. Independent recheck is a separate artifact and must be read alongside this
record. No push was performed by this reviewer; root coordinates publication.
