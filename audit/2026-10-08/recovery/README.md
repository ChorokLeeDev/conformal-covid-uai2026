# Recovered evidence and actual reruns, 2026-10-08

**The complete recovered follow-up SALT panel does not reproduce the historical positive concentration–coverage-decline association.** We restored raw inputs, replayed saved models, and refitted all eight tasks × seeds 42–44 using the fixed existing protocol. The original 50-seed publication's fitted models/per-record outputs are still unrecovered; follow-up reproduction is not historical reconstruction.

## Recovery and provenance

- Public upstream `ChorokLeeDev/ai-in-finance` at `f283047d2d7d81fb7c726af3763bd452b99cee12`: recovered missing source programs, historical summary JSONs and selected retraining logs. `provenance.json` binds 102 source/summary/log files to source commits and SHA-256. `recovered-upstream-source.zip` preserves 92 relevant source files exactly. Logs are original bytes with a `.txt` transport extension.
- `ChorokLeeDev/conformal-covid` at `b0a98ba3ba738a693df736cfdc6c7fca30f49437`: source and history searched; no original prediction/model ledger recovered.
- Private `ChorokLeeDev/conformal-covid-followup` at `e2eb3e38f072745f0f60bd67425cffbd68f7ab9e`: recovered September continuation, all eight pinned SALT task tables and two entity tables, 24 subsequent models and arrays. The GitHub release `drive-archive-20260908` has 33 parts; each part and the 2,185,804,556-byte reconstructed ZIP verified. Whole SHA-256: `d31e4522bf8050d1447547c1ae58eb4da582600f764a24f40f6a95da2d963559`.
- The archive index contains 6,488 members, including its internal manifest. Restoring only missing `latest_v3` payload files preserved 2,296 existing files and restored 2,083. Private raw data/model payload stays in the local recovery checkout; this public audit contains aggregate diagnostics, public-source copies and input hashes.
- Account-wide repository/release searches were coordinated separately; no original 50-seed ledger was recovered from this archive or the searched UAI histories. Source files, historical summaries, and later fitted models are distinct evidence levels.

## Actual calculations and fits

1. Re-executed the continuation's 12 protocol boundary fixtures; all passed. The full 24-model factorial replay matched 48 canonical rows, 1,248 numeric CSV/JSON comparisons and 72 overlap comparisons exactly. `protocol-replay-summary.json` records all four threshold/inversion combinations.
2. Re-executed its raw-ID/time/label/feature-mask/support audit for all 24 fits; all passed. This validates saved cohort identities and masks, not exchangeability.
3. Independently implemented `replay_recovered_evidence.py`, importing only this public repository's separately reviewed APS reference. It reconstructs training-only feature dictionaries from raw entity rows and frozen IDs, reloads every model, and recalculates calibration/audit/target probabilities and 128-row native TreeSHAP. **All 24 probability comparisons and all 24 concentration comparisons have maximum absolute error 0.** All input hashes and raw join counts are in `raw-replay.json`.
4. Actually ran the recovered fixed `run_breadth.py` for all eight tasks and seeds 42, 43, 44, with two threads, into a fresh `runs/20261008-refit` directory. There was no seed/model selection or result-dependent tuning. `compare_refits.py` verified **528 arrays and all scientific metadata exactly equal** to recovered outputs. Model text differed only by omission of the precise empty `[gpu_device_id_list: ]` field in this CPU wheel; all tree text and other parameters matched. Original and rerun hashes are recorded in `refit-comparison.json`. No original artifact was overwritten.

Three seeds are averaged within each task. The eight task means produce:

| Task | Native concentration % | Inclusive APS drop pp | Crossing drop pp |
|---|---:|---:|---:|
| item-incoterms | 26.06 | 7.52 | 3.78 |
| item-plant | 22.56 | 2.63 | 2.28 |
| item-shippoint | 28.80 | 1.36 | 1.57 |
| sales-group | 52.10 | 3.70 | 3.65 |
| sales-incoterms | 30.86 | 1.61 | 0.47 |
| sales-office | 49.05 | 0.16 | 0.02 |
| sales-payterms | 60.01 | 1.82 | 1.86 |
| sales-shipcond | 32.41 | 2.24 | 2.26 |

Inclusive inversion: Spearman −0.238095, nominal asymptotic p=0.570156. Crossing: −0.261905, p=0.530923. These negative sample associations do not establish a population negative effect or equivalence. Shared-domain tasks are not independent replications; seeds do not increase the task count to 24. No task has a mean drop >15 pp, so this panel cannot estimate sensitivity to severe failures.

## Scientific changes justified by recovered evidence

1. **Critical — input join artifact verified on pinned raw data.** Historical code calls default `get_db()`, which truncates entities at 2020-07-01. The independent raw join check misses **88,942/88,942 target IDs in each sales task and 402,855/402,855 in each item task**. Train/validation have zero missing IDs. Full entity tables match every target ID. This is a demonstrated current-snapshot input-contract defect, not proof of the original results' cause. Original snapshots, model files and probability ledgers would be necessary to identify that cause. Full-table access also needs an as-of feature availability contract before deployment.
2. **High — positive association does not replicate in complete follow-up panel.** Both fixed-threshold APS definitions and the exact/linear factorial preserve this result. Differences in snapshot, training sample, early stopping, label support, feature dictionary and SHAP definition prevent attributing the discrepancy to a single change. The original 40% operational risk rule is withdrawn pending prospective validation.
3. **High — hyperparameter evidence contradicts claimed experiment.** Public source `compute_hp_sensitivity_real_salt.py:80–110` applies multiplicative factors and Gaussian noise to loaded aggregate concentrations, without fitting a model. `compute_hp_sensitivity_full.py` generates synthetic SALT tasks. The source's real-data four-configuration retraining claim is not supported by these programs. Removed active numerical HP tables and withdrew their empirical interpretation; original submitted tables remain immutable. The new 24-model reproduction uses one configuration and is not an HP experiment.
4. **High — PSI implementation has genuine failure witnesses.** Actual recovered `run_mmd_c2st_comparison.py:258` returns zero for source-uniform [0,1] versus target-uniform [2,3], and for constant 0 versus constant 1. Out-of-range values fall outside histogram endpoints; low-cardinality features return zero. C2ST early stopping also sees its evaluation fold. Historical detector superiority is not established; recovered summary correlations only reproduce arithmetic. Counterexamples execute the actual recovered PSI function via AST and are stored in `source-summary-recheck.json`.
5. **High — retraining estimand corrected.** Eight public logs were recovered. The shipping-condition +18.9 pp is an equal-month mean over **February–December**, mixing validation and target periods. Rounded July–December entries give +36.083 pp, concentrated in the final two months. Neither is an independent-month inferential result or an instance-weighted effect. Payterms/group per-month ledgers remain missing. No new p-value is claimed.
6. **Medium — unsupported Wasserstein bound removed.** A Lipschitz score does not make the coverage indicator Lipschitz. With score `s(x)=0.5+x`, threshold 0.5, source point −0.001 and target point +0.001, score Lipschitz constant is 1 and W2 is .002, but coverage falls from 1 to 0, violating the proposed .998 lower bound. A margin-mass/coupling assumption is necessary.
7. **Medium — recovered external code disagrees with described protocol.** `compute_wilds_real.py` uses Adult age<40 versus text<50, CivilComments 200 versus text1,000 TF-IDF features, and positional Covertype splits versus wilderness-area claims. Original results cannot be mapped confidently to one execution solely from filenames.
8. **Descriptive uncertainty arithmetic now runnable.** Recovered 16-task summary JSON permits a seeded 10,000-resample task bootstrap: primary16 interval [0.499981,0.961253]; SALT8 [0.291139,1]. This does not justify exchangeable task resampling. Per-seed, per-row historical intervals and all SHAP bootstrap claims remain unreproduced.

## Protocol limits

Recovered follow-up fits use 10,000 training, 3,000 tuning, 3,000 calibration, 3,000 source-audit and 6,000 target rows per task/seed; task partitions are chronological and disjoint. Training-only dictionaries, full-training label alphabets, task-target exclusions, and the retained uppercase entity-key contract are checked. Native raw-margin path-dependent TreeSHAP uses the first 128 calibration rows. This differs from the historical fitting cohort, all-split preprocessing and SHAP protocol. Chronology alone does not supply split-conformal exchangeability; no universal conformal guarantee for these temporal cohorts is claimed.

## Reproduction

Install `requirements-recovery.txt` in a separate Python 3.12 environment. The owner must restore the private release using its checksum-verifying `restore_zip.py` and `tools/restore_archive.py`; the public aggregate package alone cannot rerun private arrays.

From this repository:

```sh
python audit/2026-10-08/recovery/replay_recovered_evidence.py --followup-root /path/to/conformal-covid-followup --output /new/path/raw-replay.json
python audit/2026-10-08/recovery/recheck_source_summaries.py
python audit/2026-10-08/recovery/compare_refits.py --followup-root /path/to/conformal-covid-followup --output /new/path/refit-comparison.json
```

The exact executed training command, from the private checkout:

```sh
python thesis_extension/deepening/breadth/run_breadth.py --data thesis_extension/external_inputs/rel-salt --output runs/20261008-refit --tasks sales-shipcond sales-office sales-group sales-payterms sales-incoterms item-plant item-shippoint item-incoterms --seeds 42 43 44
```

Preserved execution limits/failures: the first independent script stopped before data access because of an incorrect repository-relative import path; that path was corrected (`initial-import-failure.txt`). The first refit comparison failed its strict model-byte check; the exact empty GPU-field diff was inspected before adding that single documented serialization allowance. No numerical tolerance, seed, model or data change was introduced to pass this comparison.

The official arXiv v2 source is byte-identical to the original camera-ready source. See `arxiv-assessment.md` for the material-update assessment. No arXiv or publisher submission was performed.

Independent-review follow-up: removed the appendix operational decision table and concentration-based causal failure definitions, corrected the MLP statistic label to permutation importance, and replaced remaining pre-deployment/specificity claims with historical arithmetic or explicitly unvalidated research hypotheses. This change does not alter raw inputs, fits, arrays or quantitative recovery results.
