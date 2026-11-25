# Basic setup questions

Use the short answer first; formulas are optional supporting material.

## UAI

1. **Setup:** feature row → class probabilities → prediction set. SHAP separately explains the fitted model’s output.
2. **Assumptions:** the usual coverage promise needs exchangeable calibration/test cases and independent model fitting. The theoretical mechanism adds explicit assumptions about a damaged component.
3. **Hypothesis:** could reliance on a feature help explain failure when its predictive relationship changes?
4. **Result:** a historical association, with documented selection, pipeline and follow-up limitations.
5. **Theorem:** a bound for an idealized probability mixture. Its mixture share is distinct from measured SHAP concentration.

**“If the labels are random, shouldn’t SHAP be spread evenly?”**

“Not necessarily. If labels are independent of the inputs, there is no real population signal. But a model fitted to a finite sample can still learn accidental patterns and use some features more than others. SHAP explains that fitted model. Random labels alone do not force equal feature attribution.”

If the model is constant, all feature attributions can be zero. A top-feature share then needs a convention because the total is zero. Stochastic labels that still depend on the inputs are a different case: they can contain genuine signal.

**“Isn’t one very useful feature a good thing?”**

“Yes, it can be. The concern is whether the relationship making it useful changes. Concentration by itself does not say that the feature is bad or that coverage will fail.”

**“What exactly is concentration?”**

“For each feature, average the size of its SHAP contribution. Divide the largest feature average by the total. It is a summary of the fitted model’s attribution, not a proof of causal importance.”

**“Does 90% mean you include labels until probabilities add to 0.9?”**

“No. Ninety percent is the desired coverage. A separate labelled calibration sample supplies the score threshold. The threshold is not automatically 0.9.”

**“What does APS do?”**

“It orders labels by their reported probability and computes cumulative scores. The label-set rule then uses a calibration threshold.”

There are different conventions. At probabilities (0.60, 0.25, 0.15), inclusive candidate scores are (0.60, 0.85, 1.00). At threshold 0.80, score inversion includes only the first label. A rule that also includes the threshold-crossing label returns the first two. The audited theorem uses score inversion; the historical SALT implementation used crossing sets.

**“What did you actually prove?”**

“For a simplified model combining two probability components, I assume one component stops supporting the true label and the other stays stable. Under those assumptions, increasing the damaged component’s share worsens particular score and coverage bounds. This is not a proof that measured SHAP concentration always lowers actual coverage.”

For the monotonic bounds, hold the threshold, damage bound and residual law fixed. The expected score lower bound rises when the damaged component’s true-label bound is below the residual mean. The coverage upper bound is non-increasing under the theorem’s additional threshold condition. For the coverage upper bound with lambda < 1, the extra condition is ε ≤ (1−q)/(K−1); for the expected score lower bound, it is ε < E[h(y_true)]. Keep q, ε and the residual law fixed. The theorem’s share is lambda. Measured SHAP concentration is C. No equality between them has been established. The historical selected-16 correlation is 0.853; all 17 give 0.654. The separate later eight-task panel gives −0.238 with inclusive sets and −0.262 with crossing sets. Those protocols must remain distinct.

## Definition references

- [UAI audited setup and theorem](https://github.com/ChorokLeeDev/conformal-covid-uai2026/blob/6a97650664dffeeaad8f090ee3903c9d72ed6d58/paper/main.tex).
- [AISTATS setup, known/unknown link and finite-sample protocol](https://github.com/ChorokLeeDev/conformal-coverage-identification-aistats2027/blob/c13bad9cfd3ef6574e8467e1a4ae87703258f71d/arxiv/source/main.tex).
- [ICLR audit model and theorem conditions](https://github.com/ChorokLeeDev/selective-labels-minimax-iclr2027/blob/1c2535ac92f5e2f0a71ef4022852ef82f206d064/paper/body.tex).
