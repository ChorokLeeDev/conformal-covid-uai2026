# Independent UAI scientific review — frozen revision 72132d32f8671fa099711211a5f54f0f55b22caf

Date: 2026-10-09 Asia/Seoul. Reviewer inspected manuscript, source programs and numeric artifacts before reading any prior reviewer verdict. Source was not edited. No models were refitted. This report concerns correctness and evidence, not acceptance likelihood.

## Baseline identity

The newly fetched official arXiv 2601.00908v2 source supplied by the root agent contains `main.tex` with SHA256 `8b7456b576cbcb5631345f761fff384d86c7e67b3e59b7915b8ffc95e65f7fbe`. It is byte-identical to `submission/camera_ready_source.zip`'s `main.tex`. Thus the camera-ready archive is a valid manuscript baseline for this comparison. Public source retrieval and arXiv submission status are the root agent's responsibility.

## Scientific judgment

The rewritten abstract/conclusion adequately distinguish historical rounded-summary associations from a separate recovered 8-task, 3-seed follow-up that fails to reproduce the positive association. The theorem's deterministic tie order, probability-mixture weight distinct from measured SHAP concentration, fixed-threshold condition, and lambda=1 boundary repair the central mathematical overclaims. I found no algebraic flaw in the revised pointwise/expectation/coverage bounds under their stated assumptions. These are not empirical guarantees for the SALT experiments.

The historical 50-seed experiment remains unreproduced. The follow-up arithmetic is supported by available aggregates, but this reviewer did not possess or regenerate the private raw payload or 24 fits; the saved replay/refit receipts are evidence of the earlier audit, not a new independent raw replication. Corrective replacement publication does not require resurrecting unsupported original claims: it requires clear withdrawal/qualification. A few material contradictory assertions survive in the current bodies and captions and should be corrected before calling the manuscript scientifically consistent.

## Independent bounded numeric checks

- Recomputed from displayed/generator constants: SALT8 rho=0.8333333333333335, asymptotic p=0.010175540123456752; external8 same rho/p; pooled16 rho=0.8529411764705882, p=0.00002679074057724726, Kendall tau=0.6666666666666667; all17 rho=0.6544117647058824, p=0.004367978540420788. Matches claimed rounding.
- Enumerated all 40,320 8-rank permutations: 620 at least as extreme as |rho|=5/6; p=0.015376984126984126. Eight-test first-step Holm sensitivity=0.123015873. Matches revised text.
- Recomputed all six displayed threshold rows from the 16 historical point summaries. TP/FP/FN counts and rounded precision/recall agree.
- Independently averaged the 3-seed `raw-replay.json` model rows: all 24 concentration/inclusive-drop/crossing-drop cells in the new 8-task table match two-decimal rounding. Follow-up task correlations match -0.2380952381 and -0.2619047619. This is aggregate arithmetic only.
- Recomputed model sensitivity correlations from manuscript rows: RF=0.2994065655 (p=.4712605287), XGB=.5476190476 (p=.1600256425), CatBoost=.6666666667 (p=.0709876543), MLP=.4285714286 (p=.2894032248). Matches claimed rounding.
- LOO thresholds 7x45 and 1x30 yield mean 43.125, population SD 4.9607837. Reported 43.1 +/-5.0 is coherent, though SD convention should remain descriptive.
- Cohen d recomputed from the rounded 8-task points is 3.09095, versus historical 3.08; plausible original precision difference, not sufficient evidence of an error. The reported group SDs 2.6 and 7.7 use ddof=0 while pooled d uses ddof=1; label this explicitly if retained.

## Material residual findings and minimal replacements

### UAI-R1 — Unverified stability inference stated as a fresh established result (medium)

Location: `paper/main.tex:261`, final sentence. Claim: 1,000 bootstraps of 10K validation records establish CV<1% and CIs within +/-1pp for every task. Original SHAP ledger/bootstrap results are unavailable, and a 128-row follow-up does not verify this historical claim. Nearby disclosure is not enough to make the affirmative sentence true.

Replace that sentence with:

```tex
The original manuscript reported within-model SHAP bootstrap CVs below 1\% and 95\% CIs within $\pm$1 percentage point (1,000 resamples of 10,000 validation rows), but the original attribution/bootstrap ledger is unavailable; this stability claim has not been verified.
```

Also replace `due to reduced power at $n=7$` in the same paragraph with `in the smaller $n=7$ subsets`. The observed p-value changes do not identify loss of power as their cause.

Resolution check: no affirmative attribution-stability conclusion remains without the original bootstrap data.

### UAI-R2 — Residual causal COVID interpretation contradicts the input-join caveat (medium)

Locations: `paper/main.tex:938`, plus standalone table notes at 914. Statement attributes shifted item features to pandemic entry of products/parties/IDs, yet the recovered snapshot has 402,855/402,855 unmatched target item joins. This does not prove historical KS arose from the defect, but it prevents a causal business explanation.

Replace the full line-938 note with:

```tex
The historical summary reports 6/7 features (86\%) as shifted, consistent with Table~\ref{tab:shift_characterization}. Original feature-level outputs are unavailable. The recovered default-join defect prevents attributing these reported differences to pandemic-related changes in products, parties or identifiers.
```

Replace the line-914 note with:

```tex
For the encoded empirical samples, KS $=1$ denotes complete separation. The historical summary reports 3/6 features (50\%) as shifted. Original feature-level outputs and a correctly joined input cohort are needed to verify these values and interpret their source.
```

Resolution check: these table captions/notes are explicitly historical, and no causal pandemic mechanism is inferred from marginal KS values or defective joins.

### UAI-R3 — Unsupported null-shift assertion in an external-protocol caption (medium)

Location: `paper/main.tex:460`. `NC = null-shift control (... no genuine shift; low concentration and robust coverage are the expected and observed outcome)` is not justified by a random/predefined split. Even genuine no-shift sampling would not force low SHAP concentration.

Replace only that parenthetical with:

```tex
(random/pre-defined split intended as a comparison condition; absence of relevant shift and low concentration are not established by the split label)
```

Resolution check: no claim that a split name establishes no shift or predicts concentration remains.

### UAI-R4 — WILDS historical/current provenance contradiction (medium)

Location: `paper/main.tex:943` says `To further validate ... we evaluate` and `Their generating code and outputs are absent`, while later paragraphs explicitly inspect recovered generating code. The recovered archive includes `compute_wilds_real.py` and `compute_wilds_validation.py`. Missing original outputs are distinct from missing code.

Replace the entire paragraph with:

```tex
The original manuscript reported four additional evaluations using WILDS~\citep{koh2021wilds} and standard datasets. These historical summaries report low concentration and small coverage drops. Candidate generating code has since been recovered, but original outputs and execution provenance remain unavailable, and the recovered protocols conflict with several manuscript descriptions. Covertype is reused under another split, and CivilComments/Adult are binary tasks outside the selected primary subset. These reports do not establish independent specificity.
```

In the table caption at line 947 replace `Note: This table tests specificity (low-$C$ $\rightarrow$ robust)` with `These historical classifications do not establish specificity`.

Resolution check: present tense validation is removed; recovered code is acknowledged without implying its execution produced the original figures.

### UAI-R5 — Residual RAPS causal interpretation and incorrect concentration ranking (medium/minor)

Locations: line 366 calls s-shipcond `the most concentrated task`; displayed concentration is 50.7%, below s-payterms' 54.2%. Recovered RAPS source uses the same fixed concentrations. Replace `but not the most concentrated task (s-shipcond:` with `but not s-shipcond (` (adjust punctuation to retain the numerical comparison).

At line 741 replace the final sentence with:

```tex
For item-shippoint ($K=69$), the historical summary reports a larger RAPS coverage drop by 11.2~pp (paired Wilcoxon $p=0.064$, 10 seeds). Missing paired outputs prevent verifying this test or attributing the difference to a specific calibration mechanism.
```

Resolution check: no claim that this observational difference establishes a regularization-induced failure mechanism.

### UAI-R6 — Standalone captions reassert withdrawn prospective/statistical conclusions (medium)

Locations: line 208 main results caption `All drops significant`, line 327 diagnostic caption `Pre-Deployment`, line 625 baseline caption and line 647 footnote `Pre-deployment diagnostic`, Figure 2 image's `Pre-deployment ...` title. The surrounding text discloses limitations, but captions and plotted labels are independently readable and still carry the rejected interpretation.

Minimal caption changes:

- Main-results caption: `Historical Reported Coverage Degradation (50 Seeds; Original Runs Unverified). Reported 95\% seed-level $t$ intervals and paired Wilcoxon $p$-values are retained for the record; the missing seed ledger prevents verification.`
- Diagnostic caption: `Historical Source-Data Diagnostic Comparison ($n=8$; Original Runs Unverified).` Preserve the rest of the metric definitions.
- Baseline caption: `Historical Source-Data (SHAP) and Target-Data (Entropy, ECE) Diagnostic Summaries (10-Seed ACI Experiments; Original Runs Unverified).` Preserve information-requirement definitions.
- Baseline dagger footnote: `Computed on validation covariates for a historically test-aware fitted model; not a validated pre-deployment procedure.`
- If retaining historical plots unchanged, explicitly mark them as historical inside the image or keep their existing caveat caption. Prefer regenerating the n16 plot from the frozen point constants with title `Historical Summary Association (Original Runs Unverified)` and cutoff label `Unvalidated 40% cutoff`; preserve the original submitted figure separately. Do not treat regeneration of point summaries as experiment reproduction.

Resolution check: extract PDF text and inspect captions/figures to ensure no standalone prospective performance claim remains.

## Useful transparency addition (medium, not a contradiction)

In the new follow-up panel, unknown labels outside the historical training alphabet are assigned uncovered status. This is important to the estimand but is currently omitted from main.tex. From `raw-replay.json`, sales-group unknown-label counts are 101/94/106 of 3,000 source-audit rows and 373/383/397 of 6,000 target rows across seeds. The total per-seed records are repeated samples, not unique population counts. Mean target coverage for sales-group is 84.72% inclusive and 84.87% crossing despite a modest ~3.7pp drop; the recovered result is failure to reproduce the old concentration association, not restored 90% coverage. Item-incoterms inclusive mean target coverage is 81.58%. Current paper does not claim restored coverage, but reporting denominator/unknown-label rules removes a preventable ambiguity.

Suggested addition near recovered-panel protocol:

```tex
Labels outside the historical-training alphabet are always counted as uncovered, including at an infinite threshold. Reported drops compare source-audit and target coverage; a small drop does not imply that target coverage attains 90\%.
```

The first sentence should be checked against the actual retained replay code (its output metadata gives this definition). Separate tuning/calibration does not itself restore exchangeability, already disclosed correctly.

## Scientific changes requiring author review

1. Original 16-task empirical association remains only historical summary arithmetic. The separate follow-up does not reproduce it; its different sample sizes, model configuration, preprocessing, label vocabulary and SHAP 128-row protocol preclude calling it an exact rerun of the original experiment.
2. Prospective diagnostic, causal mechanism, threshold-based operational rules, and empirical hyperparameter robustness are withdrawn rather than rescued by the follow-up.
3. The theorem is now about an idealized probability mixture, not an empirically identified SHAP concentration quantity; fixed-threshold monotonicity is not recalibrated model monotonicity.
4. Original seed tests, intervals, benchmark comparisons, SHAP stability and most historical plots remain unverified; retain them only with explicit historical status.
5. The demonstrated join failure concerns the recovered pinned snapshot. It cannot alone establish why every historical collapse occurred.

## Remaining limits after these corrections

Missing original models/predictions/attributions cannot be repaired editorially. The raw follow-up payload was not independently replayed by this reviewer. No external prospective validation or mechanism intervention was added. These limit substantive empirical claims, not the ability to publish a transparent correction that states them. Submission must remain unconfirmed until arXiv supplies actual receipt/version evidence.
