# Independent statistical recheck — 2026-10-08

Initial reviewed revision: `c5df94d0b571c2e61c256aacb2c7db92ced14dd0`, branch `revision/statistical-audit-20261008`; original study baseline: `96d9616961e5ae8607373181d35262cb21a2b0d1`. The working tree was clean when this pass began. This reviewer did not author the UAI revision and did not use the prior initial-review verdicts as evidence. The later revision record was read to distinguish actual reruns from unavailable evidence. This is an independent agent check, not human peer review or external replication.

## Core mathematical and implementation result

The repaired theorem at `paper/main.tex:152–195` is internally correct under its stated assumptions. In a fixed descending class order, every class after the true label has probability at most its probability, so the inclusive cumulative score obeys `s >= 1-(K-1)p_y`. The assumed probability mixture and pointwise bound on `g_y` give the displayed score lower bound. The equality-in-law assumption for `(h, Y)` supplies the calibration/test distribution used in expectation and tail probability. The coverage implication uses the explicit event `s<=q`, with fixed deterministic `q`; the derivative of its tail threshold is `[(1-q)/(K-1)-epsilon]/(1-lambda)^2`. The stated lambda=1 and q=1 cases are handled correctly. No inference that actual empirical coverage is monotone in SHAP concentration remains in this theorem.

The new `src/aps_reference.py` implements that score-inversion convention consistently. Stable descending sorting provides the stated index tie order; coverage and set size use one membership matrix; calibration uses the kth order statistic with the required +infinity boundary. At p=(1,0), q=1, both labels are included, unlike the archived crossing-label algorithm. The helper explicitly says it is for future reruns and does not produce historical tables. The manuscript/README also distinguish the historical membership inconsistency and calibration-label reuse. These are appropriate limitations, not a claim that the old experiments have been repaired or independently rerun.

The revised dependence discussion correctly withdraws two invalid inferences: between-task ICC cannot establish independence of tasks sharing a benchmark, and negative one-way agreement ICC cannot prove negative correlation or inflate 50 paired runs into more than 50 independent shifts. The retained historical p-values and CIs remain conditional/model-based summaries whose underlying runs have not been recovered.

## Executed independent checks

- `python audit/2026-10-08/check_statistical_claims.py`: exit 0, all eight checks pass. This checks counterexamples and rounded-point arithmetic; it does not fit models.
- A separate frozen-source check loaded `src/aps_reference.py` directly from `git show c5df94d:src/aps_reference.py`. It enumerated all 251 probability vectors on the quarter-unit simplex for K=2 through 6, including zeros/ties. All 6,505 class-membership events over thresholds {0,.25,.5,.75,1} agree with score inversion and satisfy the necessary pointwise bound.
- An independently written seeded synthetic mixture check (seed 20261008) used 400 configurations, K=2 through 8, lambda in {0,.3,.8,1}, epsilon in {0,.01,.1,.5}, and 100 rows per configuration. All 40,000 pointwise inequalities and 2,800 fixed-threshold coverage inequalities passed. This is a consistency check, not proof or empirical validation of the assumed SHAP mechanism.
- Independently enumerated all 8! rank permutations at observed Spearman rho=5/6: 620 of 40,320 have absolute statistic at least as large, giving two-sided p=0.015376984126984126 and eight-test Holm first-step value 0.12301587301587301. This conditional permutation calculation presumes exchangeable task pairs; the study has not established that assumption. The earlier p=0.0101755 is the asymptotic SciPy-style calculation and should be identified as such.

## New concrete issues found in the frozen revision

### UAI-R01 — Marginal label drift is still mislabeled as concept shift

**Severity:** high inference error in the remaining appendix, not a flaw in the repaired theorem. In `paper/main.tex:948–982`, featurewise KS, label-marginal JS and accuracy differences are described as a decomposition into covariate and concept shift, with a “Cov + Concept” classification. None of those quantities identifies a change in `P(Y|X)`. For a direct counterexample, let Y=X in both populations and change P(X=1) from .1 to .9. Label-marginal JS changes despite identical deterministic conditionals. Conversely, keeping X uniform and changing Y=X to Y=1-X preserves the label marginal while changing the conditional law everywhere. Thus label-JS is not a concept-shift magnitude. The same paragraph calls i-incoterms catastrophic although the retained coverage-drop table reports 11.3 percentage points, outside its catastrophic definition.

**Resolution:** retain the historical numerical summaries as unverified marginal-drift statistics, remove or label the concept classification unsupported, and remove the contradictory catastrophic attribution. A conditional-label claim requires a separately specified estimand and identifying evidence.

### UAI-R02 — A figure caption contradicts the corrected stochastic-dominance caveat

**Severity:** medium unsupported claim. `paper/main.tex:651` still states that rightward score shifts show stochastic dominance. At `:683`, the revised prose correctly says two-sided KS and mean shifts do not establish that dominance. The figure's underlying raw score laws are unavailable here.

**Resolution:** label the caption as historical score-distribution comparisons, without a dominance conclusion; align the section title as appropriate. Do not infer first-order stochastic dominance from significant two-sided KS or differences of means.

### UAI-R03 — Uncomputed BCa result is predicted

**Severity:** medium unsupported uncertainty statement. At `paper/main.tex:261`, the retained parenthetical claims that BCa “would yield a modestly tighter lower bound at n=8.” No computed BCa interval or resample provenance supports that method-specific outcome. Sample size alone does not determine the BCa correction's direction or magnitude.

**Resolution:** remove the hypothetical numerical-direction claim, or compute and retain a clearly retrospective, appropriately scoped sensitivity analysis. A generic bootstrap-method caveat does not warrant claiming an unexecuted method has a particular result.

These issues were sent to the UAI author and root for a targeted follow-up. The corrected mathematical core and explicit no-rerun disclosures are supported. Approval of the whole revised narrative remains conditional on resolving the three located contradictions; unavailable original runs, preprocessing/calibration issues, and external citation checks remain substantive open limitations even after wording is corrected.

## Targeted recheck of final follow-up

Follow-up examined: `7cad9d7a830e7a91329015c7295630a00290205f`. The final delta was inspected against the frozen revision above; mathematical helper and theorem code are unchanged.

- **UAI-R01 resolved:** the concept-mechanism classification column is removed, historical label/feature marginals are explicitly distinguished from conditional-label shift, and i-incoterms is correctly identified as having an 11.3-point reported drop rather than catastrophic failure. Historical numeric values are preserved and marked unverified.
- **UAI-R02 resolved:** the CDF caption now says the historical curves suggest distributional shifts while score arrays and a dominance test are unavailable. Its assertion agrees with the corrected KS interpretation.
- **UAI-R03 resolved:** the manuscript states that BCa was not computed and makes no claim about its direction/width.
- The added exact-permutation script was executed independently and reproduces the same 620/40,320 count and p=0.015376984126984126. The manuscript distinguishes this from the asymptotic p-value and calls the eight-test calculation a first-step sensitivity rather than an exact rerun of all eight metrics. The task-exchangeability and no-original-rerun limits are explicit.
- `pdfinfo` confirms the reviewed revised PDF has 23 pages. Extracted text contains the corrected concept-shift, BCa and CDF caveats and exact-permutation values. This independently checks the text made it into the artifact, not every page's visual layout or a fresh compile by this reviewer.
- Byte comparisons using `git show 96d9616:<path>` confirm `paper/main.pdf`, `submission/camera_ready_main.pdf`, `submission/camera_ready_source.zip`, and `submission/supplementary_material_fixed.zip` are unchanged from the original baseline.

The targeted scientific correction milestone is supported after this follow-up. Original model experiments remain **unreproduced** and some underlying protocols are invalid or inconsistent; no operational or population-generalization claim is approved by these checks. Broader historical explanatory prose (for example, “concentration determines vulnerability” in the diagnostic analysis) should be read as an unverified hypothesis, not an identified causal result; further neutral wording can improve consistency but cannot replace the missing data and controlled experiments.
