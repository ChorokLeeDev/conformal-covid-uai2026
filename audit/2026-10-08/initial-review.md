# Independent initial scientific audit — UAI conformal COVID

Date: 2026-10-08. Reviewer: a delegated model reviewer; this is a simulated independent audit, not external replication or human peer review. No other review verdicts were supplied before this report. Initial pass was read-only except this report. No training, manuscript/code edits, commits, pushes, or submission actions occurred.

## Frozen baseline and evidence inventory

- Repository: `/workspace/conformal-covid-uai2026`; initial branch `main`; HEAD `96d9616961e5ae8607373181d35262cb21a2b0d1`; initial working tree clean. No applicable AGENTS.md found in the repository or workspace parent.
- `paper/main.tex` is byte-identical to `submission/camera_ready_source.zip:main.tex` (unified diff has zero lines).
- `paper/main.pdf` and `submission/camera_ready_main.pdf` have the same SHA-256: `578db042a75d5734d2ca41c780a57b20c5e592a873cee80e565dd89f517558ae`.
- Supplement ZIP contains six Python files and a README, but **no prediction ledger, model checkpoint, numerical result JSON/CSV/pickle, split manifest, or run log**. Three key pipeline files exist only inside this ZIP. The source tree has five experimental/figure Python scripts, PDFs and rebuttal summaries.
- `paper-revision-loop` SKILL.md was read. Skill reference resources were reported unavailable by the coordinating agent; no invented reference-template requirements were applied.
- Scope: claims, theory, data access timing, code/manuscript alignment, statistical inference, artifact availability, and small deterministic checks. Existing original experimental outcomes were not regenerated.

## Claim–evidence ledger

| Claim | Status | Evidence and limit |
|---|---|---|
| Reported 16-task Spearman 0.853 and Kendall 0.667 | Verified arithmetic only | AST-read hard-coded points in `src/generate_n16_figure.py` give rho 0.8529411765, p 2.6790741e-05, tau 0.6666666667. Values are manuscript summaries, not raw experiment replication. |
| Within-SALT rho 0.833; all-17 rho 0.654 | Verified arithmetic only | Recomputed rho 0.8333333333, p 0.01017554; adding reported Stack Overflow gives rho 0.6544117647, p 0.00436798. |
| Threshold table counts at 25/30/35/40/45/50 percent | Verified arithmetic only | TP/FP/FN respectively 5/3/1, 5/2/1, 5/1/1, 5/1/1, 5/0/1, 2/0/4 from displayed points. |
| Same APS pipeline across SALT/external tasks | Contradicted by supplied code | SALT uses crossing-label inclusion; external coverage uses score-threshold membership but sizes use crossing-label inclusion. UAI-01. |
| Pre-deployment model pipeline uses no test information | Contradicted by supplied code | Encoders and class vocabulary fit across train/validation/test; early stopping consumes later calibration labels. UAI-02. |
| KDD official train/test split | Contradicted by supplied loader | One percent10 file, positional 60/20/20 split, whole-file label filtering. UAI-03. |
| Negative val/test ICC proves conservative paired inference | Contradicted mathematically | Supplied ICC can be negative under perfect positive Pearson correlation after a mean offset. UAI-04. |
| Empirical theorem assumptions/bounds verified | Unsupported | Unknown residual model and mixture coefficient; uniform residual substitution is not generally conservative. UAI-05. |
| K<=3 blocks catastrophic APS coverage failure | Contradicted by counterexample | Binary and three-class distributions admit 0% shifted coverage. UAI-06. |
| Complete reproducibility package | Contradicted | Missing artifacts/loaders; a packaged detector script does not parse. UAI-08. |
| All bibliography keys exist | Verified internal consistency | 36 cited keys, none missing. Existence/metadata/support of cited primary publications remain unverified; source HTTP requests were blocked. |

## Numbered issues

### UAI-01 — Critical: different prediction sets define the central combined endpoint

**Locations.** `src/run_aci_experiment.py:44-79`; ZIP `conformal_covid_code/run_50seed_ensemble.py:84-119`; ZIP `run_external_multiseed.py:115-150`; `paper/main.tex:96`, `444`.

**Evidence.** SALT sets add the label before checking whether cumulative probability reaches q. External coverage instead evaluates the inclusive true-label score `<= q`; its set-size routine nevertheless includes the crossing label. Executing the actual SALT class via AST isolation at p=(0.6,0.3,0.1), q=0.7 includes label 1, while its score is 0.9 and external coverage excludes it. Consequently external reported coverage and reported size do not even describe the same set.

**Consequence.** The pooled correlation combines materially different coverage estimands, contrary to the same-pipeline claim. The theorem's stated score event also is not the implemented SALT membership event. This does not by itself prove the reported correlation disappears, but its scientific interpretation cannot be validated without a uniform implementation.

**Uncertainty.** Definite code disagreement; effect on historical numerical results unavailable without probabilities and provenance.

**Resolution criterion.** Specify one deterministic APS/tie/quantile convention; test that reported membership, coverage and sizes are computed from the same sets; reevaluate both cohorts on stored probabilities or explicitly label a new rerun. Preserve historical results and do not merely substitute new code under unchanged historical tables.

### UAI-02 — Critical: test-aware preprocessing and calibration reuse violate claimed information boundaries

**Locations.** `src/run_aci_experiment.py:220-255`, `263-290`, `306-312`; ZIP `run_50seed_ensemble.py:172-217`, `235-255`; ZIP `run_external_multiseed.py:58-65`, `98-113`, `443-451`; `paper/main.tex:92`, `96-105`, `426`.

**Evidence.** Feature label encoders are fitted on concatenated train, validation and test data; target encoder and number of classes include test labels. LightGBM early-stops using **all validation labels**, and that same validation sample is only later divided into conformal calibration and evaluation. External experiments have the same early-stopping/calibration reuse.

**Consequence.** Test covariates influence ordinal feature representation and test labels influence the class vocabulary/model dimensionality; this contradicts an entirely pre-deployment pipeline. Reusing calibration labels for model selection invalidates the usual held-out split-conformal guarantee, even before temporal shift. The size and direction of bias are unknown.

**Uncertainty.** Code paths are definite. A documented externally fixed class ontology might justify class vocabulary without test labels, but no such manifest is supplied. Dataset entity joins also require an as-of availability audit; current code alone does not establish leakage of every joined field.

**Resolution criterion.** Fit preprocessing on permitted training data, supply an externally defined class vocabulary or explicit unseen-label policy, separate tuning from calibration/evaluation, document timestamp-safe joins, and rerun affected models. Until then explicitly disclose the transductive/reused-validation historical protocol and withhold standard finite-sample coverage guarantees for these experiments.

### UAI-03 — High: KDD split and covariates do not match the manuscript protocol

**Locations.** `paper/main.tex:376`, `456`, `469`; ZIP `run_external_multiseed.py:200-246`.

**Evidence.** Text says official KDD 1999 train/test files, with approximately 395K official training and 98,769 official testing rows. Loader calls `fetch_kddcup99(subset=None, percent10=True)` once, filters classes using whole-file counts >=100, and partitions the filtered array at 60% and 80%. It never fetches a separate official test file. It encodes every object-typed column by string LabelEncoder before splitting, potentially including numerical columns in this object-array dataset.

**Consequence.** The claimed documented attack-distribution/official-test evaluation is not supported by the supplied loader; test-aware class selection also changes the evaluation population. Encoded numeric categories can create an unintended ordinal model.

**Uncertainty.** The original run may have used different unavailable code; current artifacts do not establish which protocol generated the table.

**Resolution criterion.** Recover data checksums, actual train/cal/test indices, fitted encoders and generating commit. Either correct the historical split description with provenance or run the claimed official split as a separately labeled experiment. Preserve numeric types and fit encoders on permitted data.

### UAI-04 — High: ICC inference and effective sample sizes are invalid

**Locations.** `paper/main.tex:279`, `644-646`, `654-665`; ZIP `compute_icc_and_partial.py:53-93`.

**Evidence.** The one-way ICC compares raw val/test levels as repeated measurements. Running its actual function with val=linspace(0.85,0.95,50) and test=val-0.7 gives Pearson correlation **1.0**, but ICC **-0.9856538874**. A large systematic level shift produces negative agreement ICC even when seed fluctuations align perfectly. It therefore cannot establish the manuscript's claim that high-validation seeds do not have high test coverage. The formula `50/(1+ICC)` does not create 55–250 independent seed pairs. Between-task ICC quantifies variance decomposition, not independence of tasks sharing the same SALT entities/time periods.

**Consequence.** Statements that paired tests are conservative, effective sample size exceeds 50, and ICC confirms eight independent tasks are unsupported. Seed-level uncertainty conditions on one shared dataset and is not domain/event population uncertainty.

**Uncertainty.** Mathematical defect definite; raw pairs needed to recompute actual dependence and uncertainty.

**Resolution criterion.** Remove these invalid interpretations/effective-n table; distinguish agreement from correlation; use paired differences for within-task inference and explicitly define what seed variation estimates. Use independent domain replication or appropriate cluster-aware sensitivity analysis rather than claiming task independence from ICC.

### UAI-05 — High: theorem scope, ties and claimed empirical verification exceed the derivation

**Locations.** `paper/main.tex:163-200`, `674-676`.

**Evidence.** C is defined on [0,1], but the coverage threshold divides by 1-C; C=1 is unhandled. At q=1, epsilon=0 does not give strict threshold monotonicity, despite the parenthetical assertion. The APS equality based on strictly lower **probabilities** fails with ties: actual deterministic score for p=(0.2,0.4,0.4), y=2 is 0.4, while the displayed strict-probability formula is 0.8. A fixed rank/tie order gives a valid complement formula, using probabilities <= true probability for omitted tied classes. Monotonicity of a bound requires holding q, h and epsilon fixed; retraining/recalibration as C changes does not establish that condition.

The reported empirical check substitutes epsilon=0 and mean residual true-class probability=1/K, but neither is estimated or verified. Since the lower bound **decreases** as residual true-class probability increases, 1/K is not a universally conservative substitution for a residual model that is at least uniform: K=3,C=0.5,epsilon=0 gives an assumed 2/3 lower bound at h=1/3 but a permitted bound of 0 at h=1. The paper admits TreeSHAP C is not established as the probability-mixture weight. Checking observed scores exceed illustrative numbers cannot verify A1–A3 or validate that mapping.

**Consequence.** Parts of the algebra can support a conditional idealized proposition; they do not provide a measured-SHAP guarantee, empirical verification of assumptions, or monotonicity of actual coverage across retrained classifiers.

**Uncertainty.** Boundary/tie/substitution issues definite; a repaired theorem may remain valid. UAI-01's set/score discrepancy requires separate alignment and does not alone prove every loose upper bound false.

**Resolution criterion.** Distinguish mixture weight from SHAP C; handle C=1/q=1; define a fixed tie order and precise set event; state which quantities remain fixed for monotonicity. Relabel the five score comparisons as illustrative conditional calculations, or estimate/validate the required residual decomposition before calling them verification.

### UAI-06 — High: class-count exclusions and subnominal coverage explanations are false as general APS claims

**Locations.** `paper/main.tex:85`, `172` footnote, `239`, `598`; citation `ding2023class`.

**Evidence.** There is no general binary/three-class ceiling preventing catastrophic shifted coverage. For either K=2 or 3, calibrate on correctly predicted true class 0 with p0=0.9 and q=0.9; shifted test predictions with p1=0.99 and p0=0.01 produce only {1}, hence 0% coverage. This was evaluated numerically. A finite-sample **marginal** split-conformal guarantee under its assumptions does not become subnominal solely because K=459. Class-conditional sample-size difficulties are a different result. K=3 also need not induce a near-uniform score distribution.

**Consequence.** The claimed theory-driven K>=4 exclusion and explanation for 83.6% marginal validation coverage are not valid; an exclusion that boosts rho from 0.654 to 0.853 must be presented transparently as an empirical scope choice unless a dated prospective plan exists.

**Uncertainty.** General mathematical statements are contradicted; cannot establish whether the actual exclusion was selected after observing results. Primary citation content was not retrieved, so no bibliographic fabrication accusation is made.

**Resolution criterion.** Remove categorical APS-mechanics justifications and attribution of undercoverage to class count; prominently retain all-17 sensitivity results; document the timing/reason for the subset. Investigate calibration reuse, temporal calibration/evaluation shift, and implementation for undercoverage.

### UAI-07 — High: pooled analysis is not independent confirmatory replication; multiplicity is understated

**Locations.** `paper/main.tex:133`, `156`, `281-283`, `330`, `668-670`.

**Evidence.** The n=16 endpoint includes all eight SALT tasks used to assess/select concentration metrics, so it cannot be an independent replication of that selection. No dated analysis plan is present to justify “confirmatory” or “a priori.” The displayed metric family contains top-1/2/3/5/10, HHI, Gini and entropy (eight), while adjustment covers only five. Exact displayed SALT rho gives p=0.01017554, so five-test Holm first step is 0.05087770 rather than exactly 0.050; for eight it is 0.08140432. Choosing a smaller family requires a documented rationale. Observed-effect post-hoc power cannot confer confirmatory status. Partial association controlling for class count does not establish concentration “drives” severity independently of other domain/shift confounding.

**Consequence.** Significance language overstates inferential strength despite internally correct primary correlation arithmetic.

**Uncertainty.** Original prespecification and selection chronology unavailable. Independently calculating the eight external displayed points gives rho=0.8333,p=0.01018, useful descriptive sensitivity evidence but not raw replication or proof of independence/selection control.

**Resolution criterion.** Label pooled/selected analyses exploratory or retrospective, report external-only association separately, disclose the full metric search, avoid rounding p before correction, and reserve causal/confirmatory language for a defensible design with recorded provenance.

### UAI-08 — High: released supplementary package cannot reproduce its advertised suite

**Locations.** `paper/main.tex:402`, `418`, `444`; `src/compute_shap_concentration_all_tasks.py:42-50`, `77-96`; ZIP `run_mmd_c2st_comparison.py:297`; ZIP README and external loader.

**Evidence.** AST parsing of all six ZIP Python files yields five passes and one **SyntaxError** at `output_dir = Path("Path(__file__).parent / "results"")`. The SHAP script invokes missing `analyze_feature_importance.py` and a local workstation interpreter in source; its cached-result paths are absent. It hard-codes sales-group drop 86.7 while the current manuscript/figure uses 71.2, and sales-office 0.0 vs 0.1. External script only supplies loaders for Covertype, KDD, Gas Sensor and Stack Overflow; no supplied loaders or outputs for the remaining five primary datasets or WILDS/model/hyperparameter/placebo/retraining analyses. No raw numeric artifacts exist in the ZIP.

**Consequence.** The complete-suite/supplementary reproducibility claim is contradicted; concentration and high-value sensitivity results cannot currently be independently checked. Fixing one path/syntax error is not a reproduction of the study.

**Uncertainty.** Files may exist elsewhere in the author's original project, but are absent from this frozen repository/package.

**Resolution criterion.** Inventory actual supported commands; fix syntax and supported local paths; package missing source/data manifests/output provenance; reconcile hard-coded summaries; independently rerun the affected analyses. Until recovered, label missing experiments as unverified historical reports and retain evidence gaps.

### UAI-09 — Medium: benchmark identity and geographic annotations are inaccurate

**Locations.** `paper/main.tex:454`, `469`, `1067-1097`; `rebuttal/R4_wilds_external.md`.

**Evidence.** Covertype wilderness areas are covariate geographic partition indicators, whereas Spruce-Fir/Lodgepole Pine/Ponderosa Pine/Cottonwood-Willow are target cover-type names, not the meanings of the area columns. The WILDS section calls four datasets “all four WILDS benchmarks” although its own source column labels Covertype sklearn and Adult OpenML; Covertype is also reused from the primary endpoint under a different split, contrary to “four datasets distinct.” A geographic area1-versus-other split supplies no temporal ordering. CivilComments and Adult are binary despite the primary scope assertion K>3.

**Consequence.** Incorrect dataset semantics obscure what external evidence is independent and what shift is tested.

**Uncertainty.** Source/label contradiction is internal; authoritative dataset webpage fetch was blocked, so area names should be verified from packaged data documentation before substituting exact names.

**Resolution criterion.** Say two WILDS and two standard benchmarks; identify reused Covertype and different protocols; call its split geographic; separate cover classes from wilderness regions; label binary evidence outside the primary scope.

### UAI-10 — Medium: mechanism and protective-factor conclusions are stronger than their evidence

**Locations.** `paper/main.tex:159`, `244-248`, `275-277`, `330`, `380`, `394-395`, `556`, `595`.

**Evidence.** Between-architecture correlations do not prove gradient boosting reinforces single-feature dependence, RF averaging necessarily dilutes it, or approximation noise explains MLP results. Feature shifts and SHAP concentration are observational. The same protective feature is described as secondary/train-validation at lines 277/595, but dominant/train-test at 556; latter is post-deployment information. Main text calls high concentration necessary for vulnerability, while KDD is an admitted low-C false negative. “Identical temporal shift” means common periods, not identical task distributions. A rightward true-label score shift does not alone establish smaller prediction-set sizes. Placebo effects include a 1x s-office row, despite “6–143x” across-task summary.

**Consequence.** Causal/structural language and an operational protective rule are not established by the reported observational comparisons.

**Uncertainty.** Original intervention experiments and train-validation feature-overlap ledgers are missing.

**Resolution criterion.** Use association/hypothesis language, identify the actual feature and permitted overlap split, acknowledge false negatives and single-case rule construction, remove general “necessary” claims, and support size/mechanism claims with direct outputs or controlled interventions.

### UAI-11 — Medium: PSI detection and broad baseline-superiority conclusions lack support

**Locations.** `paper/main.tex:63` footnote, `76`, `368`, `394`; ZIP `run_mmd_c2st_comparison.py`.

**Evidence.** PSI>0.002 is described as detectable/nonzero shift while the same footnote gives a conventional 0.1 threshold; positivity alone does not demonstrate statistical detection and no PSI null calibration is supplied. Weak correlation in eight related tasks cannot establish that MMD/C2ST generally cannot predict failure severity. Detector script fails parsing and raw taskwise outputs are unavailable.

**Consequence.** An empirical finding on a small suite is presented as broad inability and PSI detection is overstated.

**Uncertainty.** Actual baseline outputs/test calibration cannot be rechecked.

**Resolution criterion.** Report taskwise scores, explicit null/permutation procedures and uncertainty; separate statistical detection from nonzero descriptive indices; limit superiority conclusions to this evaluated suite pending replication.

### UAI-12 — Medium: clipped ACI differs from the cited unbounded-alpha guarantee

**Locations.** `src/run_aci_experiment.py:151-170`; `paper/main.tex:74`, `360`.

**Evidence.** Alpha is clipped to [0.001,0.999] and quantile levels clipped to [0,1]. Classical ACI's telescoping update and empty/full-set conventions outside [0,1] are modified. Merely citing ACI does not transfer its long-run guarantee to this clipped implementation. Immediate label feedback also needs to match the deployment setting.

**Consequence.** Empirical adaptation results may remain descriptive but should not inherit an unproved arbitrary-shift coverage guarantee.

**Uncertainty.** No new guarantee is explicitly proved; empirical outputs unavailable.

**Resolution criterion.** Label the clipped variant and feedback assumptions; either implement/test the intended boundary behavior with a validated rerun or state the absence of the original guarantee for this variant.

## Commands/checks actually executed

1. `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git log -3 --oneline`, `rg --files`, `git ls-files`, parent AGENTS search, line-numbered source reads and ZIP member inventory. Initial repository clean; all paths above inspected.
2. In-memory Python ZIP diff and SHA-256 check: zero source differences, identical PDFs as recorded above. ZIP source was not extracted over the checkout.
3. In-memory AST isolation of existing `ConformalClassifier`, `AdaptiveConformalClassifier`, and packaged `compute_icc_one_way`; deterministic score/tie/ICC examples above. First attempt failed because the harness namespace omitted `typing.Dict`; supplied it and reran successfully. No model import/training needed.
4. AST-literal extraction of SALT/external figure coordinates plus SciPy `spearmanr`/`kendalltau`; threshold-count recomputation. These verify arithmetic of rounded summaries only.
5. AST parse of all six supplementary Python members: five pass, detector script fails at line 297. First batch aborted at that syntax error; rerun caught errors individually and inspected all members.
6. Internal bibliography-key scan: 36 cited keys, no missing keys. No full bibliographic authentication completed.
7. HTTPS requests via Python urllib to PMLR, arXiv, NeurIPS and UCI primary sites all failed with `Tunnel connection failed: 403 Forbidden`. No integrity checks were disabled. Citation existence, metadata, acceptance status and literature novelty therefore remain unverified externally.
8. No high-cost experiment, manuscript rebuild, data download, or full replication performed in this initial review. Local dependency inspection found NumPy/SciPy/pandas available, LightGBM absent.

## Feasible correction order and stopping point

First correct unsupported interpretation and document the historical pipeline, preserving original submitted PDFs/ZIP. Remove invalid ICC effective-n and class-count assertions; narrow theorem claims and fix its boundary/tie scope; downgrade confirmatory/causal language; correct dataset and missing-artifact descriptions. These are feasible without inventing experiments.

Next build a single auditable APS convention and leakage-free split/preprocessing implementation with discriminating tests. Changes to its numerical findings require restored prediction/model/split artifacts or a separately labeled rerun. Missing SHAP generator, five external loaders, WILDS/model/placebo/retraining scripts, and original result ledgers block verification of the corresponding historical claims. Another independent reviewer should assess the revised scientific claims and tests after corrections; agreement alone is not closure.
