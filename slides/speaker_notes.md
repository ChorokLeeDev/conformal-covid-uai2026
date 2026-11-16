# Spoken Script — "Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study"

Chorok Lee, KAIST — UAI 2026 conference talk (~12 minutes). Timing markers per slide; delivery ~150 words per minute.

---

## Slide 1 — Title  [0:00–0:40]

Thank you. I'm Chorok Lee, from KAIST. My question is practical: when conformal prediction fails under distribution shift, can we see the failure coming *before* it happens? I study this through a natural experiment — the COVID-19 shift in a real supply-chain dataset — where many models hit the exact same shift yet respond in completely different ways.

---

## Slide 2 — Why this matters  [0:40–2:20]

Let me start with the tool and the problem. Conformal prediction is a method that takes any trained model and, instead of a single label, outputs a *prediction set* — a set of labels — with a coverage guarantee. "Coverage" just means the fraction of the time the true label actually lands inside the set. If I target ninety percent coverage, then across test points the true answer should be in my set about nine times out of ten. The guarantee is about label inclusion, not about the set being small — and it's distribution-free: it holds for any model.

But it holds only under one assumption, called exchangeability — roughly, that the test data looks statistically like the calibration data. In the real world that breaks: the distribution moves over time — distribution shift — and coverage can quietly fall below the ninety percent I promised.

Now, a lot of prior work has characterized *how much* coverage degrades under shift. The gap I target is different, and it's on the slide: can we identify *which* deployed models will fail, before we observe any test data at all? That "before" is the hard part — at deployment time you have no test labels to check coverage against.

And here's what makes the question sharp. In my case study, eight tasks go through one identical COVID-19 shift — same shock, same pipeline — yet their coverage drops range from one tenth of a percentage point to seventy-seven percentage points. Same shift, opposite outcomes. So the severity is not coming from the shift alone. Something about the *model* decides who survives.

---

## Slide 3 — Problem setup  [2:20–3:50]

Here's the setup. I use the SALT supply-chain benchmark from RelBench, and I split it in time around the pandemic. Training data is everything before February 2020 — pre-COVID. Validation is February to July 2020, the onset. Test is after July 2020, the peak.

The critical discipline is this: SHAP concentration and the initial forty-percent cutoff use validation-time data only. I don't tune that cutoff on the test set. Test observations do support held-out evaluation and some post-hoc mechanism and threshold-sensitivity analyses — the paper is explicit that threshold sensitivity is post-hoc validation, not prospective assessment. The point is that the *diagnostic itself* is computed before any test label is seen, which is what makes it a genuine pre-deployment signal rather than hindsight.

The model is a LightGBM classifier — a gradient-boosted tree model — wrapped in Adaptive Prediction Sets, or APS, which is a standard conformal method for classification. I target ninety percent coverage.

Coverage drop is validation minus test coverage, in percentage points. A large drop signals failure; a near-zero drop means coverage held.

---

## Slide 4 — Method  [3:50–5:30]

So what's the diagnostic? The intuition is simple. A model that leans almost entirely on one feature is fragile. If that single feature is the thing that shifts under COVID, the model's whole output shifts with it. A model that spreads its reliance across many features has somewhere to fall back on.

I make that measurable with SHAP values. A SHAP value is a principled, per-feature attribution: how much, on average, each feature contributes to the model's predictions. I take the mean absolute SHAP value of every feature, and I define concentration, C, as the top feature's importance divided by the total importance across all features. That's equation one.

Because it's a ratio, C lives between zero and one, and it's comparable across tasks that have different numbers of features or different scales. A C near one means one feature dominates; a smaller C just means less of the total importance sits on the top feature — not that importance is perfectly uniform.

The key property: C is computed before deployment, on validation data only. No test labels. That's the whole point.

And it gives a simple decision rule — which I'll stress is exploratory. If concentration is at or below forty percent, treat the model as lower risk. If it's above forty percent, don't flag it blindly: first check for protective factors, and only then flag it as vulnerable. I'll come back to why that protective check matters.

---

## Slide 5 — Theory  [5:30–7:00]

I don't want this to rest only on correlation, so there's a theorem behind it. Theorem one gives a mechanistic account for why concentration should relate to failure.

The setup is a K-class classifier with an APS conformal predictor, and it rests on three explicit assumptions. First, additive decomposition: the prediction splits into a piece driven by the top feature, weighted by C, and a remaining piece weighted by one minus C. Second, concentrated misclassification: under shift, the error concentrates on that top feature. Third, residual exchangeability: the remaining features are still well-behaved.

Under those assumptions, and on a bounded domain — the per-class shift error staying below the baseline — a *lower bound* on the expected conformity score increases with C, and an *upper bound* on coverage is non-increasing in C. That's equation two. Note the care here: a rising lower bound doesn't by itself prove the actual scores rise, and a falling upper bound doesn't prove actual coverage falls — it's a ceiling, in an idealized model.

This is mechanistic intuition, not a guarantee for measured TreeSHAP C: A1 mixes probabilities, whereas TreeSHAP explains log-odds. Catastrophic tasks show rightward score shifts, with KS statistics .68 to .96, consistent with the mechanism.

---

## Slide 6 — The mechanism  [7:00–8:30]

Let me make the two outcomes concrete by contrasting a catastrophic task with a robust one, both under that same shift.

On the left, sales-shipcond — a seventy-one point drop. Here one dominant feature explodes: its importance jumps roughly four-and-a-half times under the shift. And something counterintuitive happens — the prediction sets actually *shrink* when they should be growing. The model becomes confidently wrong.

On the right, sales-office — a drop of one tenth of a percentage point. Here, importance redistributes across many features; the rankings reshuffle, but gracefully, and coverage holds.

The table underneath separates them. Feature-temporal stability — Jaccard overlap of a feature's values before and after the shift — is near zero for the catastrophic task, above one-half for the robust one. The subtle part: concentration C is high for *both* — fifty-point-seven versus forty-two-point-six percent — so concentration alone would flag both. The framework reports a protective-feature stability contrast; its feature-ranking and split details are not fully consistent across the paper. Prediction entropy goes *down* on the catastrophic task — confidently wrong — while it rises on the robust one.

Now, the crucial negative result at the bottom. Standard shift detectors — Maximum Mean Discrepancy, Classifier Two-Sample Tests, and PSI, the Population Stability Index from credit scoring — all fire on all eight tasks. They correctly see that a shift happened. But they cannot tell catastrophic apart from harmless. They detect the shift; they do not predict the severity. That's the space my diagnostic fills.

---

## Slide 7 — Key result  [8:30–10:00]

Here's the headline. My primary endpoint extends beyond supply chains to sixteen multiclass tasks across nine domains, and across those, SHAP concentration correlates with coverage-drop severity at a Spearman rho of zero-point-eight-five-three, with p below zero-point-zero-zero-one. Within the eight SALT tasks alone, rho is zero-point-eight-three-three at p equal to zero-point-zero-one-zero — and I flag that within-SALT result as exploratory, because eight tasks is underpowered.

Within the eight SALT tasks, concentration also beats every other pre-deployment alternative I tried: the log of the class count gets rho zero-point-seven-four, the model's own native feature importance gets zero-point-six-seven, and ensemble disagreement gets zero-point-four-five — all on that same eight-task set. And the shift detectors get rho at or below zero-point-one-nine with severity — essentially no signal.

This is the paper's Figure 2: sixteen tasks, circles for SALT and triangles for eight external datasets. Keep the exceptions in view: sales-office has C 42.6 percent and a .1-point drop; item-shippoint has C 48.8 percent and an 18.5-point drop. The forty-percent rule correctly flags Covertype at C 49.8 percent. A separate nine-dataset transfer check includes three-class Stack Overflow: seven of nine calls are correct, deterministic or near-deterministic across seeds. Always predicting robust also gets seven of nine, so this is not a baseline win. The primary evidence is the sixteen-task severity association.

---

## Slide 8 — Limitations  [10:00–11:15]

Because this is my own paper, I want to be candid about the boundaries, and there are four.

First, it's model-specific. The signal is strong for gradient-boosted trees — LightGBM at zero-point-eight-three-three, CatBoost zero-point-six-seven, XGBoost zero-point-five-five — but it fails for bagging. Random Forest gives rho zero-point-three-zero, not significant. Boosting builds concentrated single-feature dependence; bagging averages it away. So compute C on your deployed model class; don't transfer across families.

Second, the forty-percent threshold is exploratory. It's derived from eight SALT tasks, and the within-SALT power is below convention. Treat it as provisional and re-validate in a new domain.

Third, I have one false positive, and I report it openly. Sales-office has concentration forty-two-point-six percent — above threshold — yet only a one-tenth-point drop. In the framework its top protective feature, SALESORGANIZATION, is treated as a secondary feature with a train–validation Jaccard of zero-point-six-one; I'll flag that the source's feature-ranking and split details aren't fully consistent, so I state this as reported, not as a settled fact. Either way, that stability is why the decision rule includes a protective-factor check instead of a hard cutoff.

Fourth, this diagnoses; it does not fix. Quarterly retraining recovered about nineteen points on sales-shipcond in a single-seed experiment, with Holm-adjusted p .11: suggestive, not conclusive. RAPS helps class-accumulation failures, not single-feature dependence.

---

## Slide 9 — Takeaway  [11:15–12:00]

Three things to take away. First, the failure is silent: under shift, the catastrophic tasks become confidently wrong — their sets shrink while coverage collapses — and the standard detectors can't see it. Second, a single number, computed before deployment on validation data only, is associated with that severity: SHAP concentration, rho zero-point-eight-five-three across sixteen tasks and nine domains. Third, the honest scope — gradient-boosted models, genuine single-feature dependence, an exploratory threshold; it flags risk, it does not repair it.

So the one-line message: check the concentration before you trust the coverage. Thank you — I'm happy to take questions.

---

## Anticipated Q&A

**Q: Isn't SHAP concentration just measuring model simplicity, or class count in disguise?**
No — I control for that. Within SALT, the partial correlation controlling for log class count stays meaningful, and at the sixteen-task level the partial Spearman controlling for class count is zero-point-seven-seven while controlling the other way is essentially zero. Concentration carries the signal independently of how many classes the task has.

**Q: Why forty percent? That looks hand-picked.**
There's a natural gap in the validation data between low-concentration tasks, around twenty-four to twenty-nine percent, and high-concentration ones, forty-three to fifty-four percent. Leave-one-out cross-validation keeps the threshold stable at about forty-three percent plus or minus five, with large effect-size separation. But I explicitly call it exploratory and provisional — it's derived from eight tasks.

**Q: Why does it fail for Random Forests?**
Bagging trains many trees on bootstrap samples and averages them, which smooths the probability surface and dilutes single-feature dependence. Boosting is sequential and reinforces it. So concentration faithfully measures a boosting model's vulnerability, but a forest rarely develops the concentrated dependence in the first place.

**Q: What about Adaptive Conformal Inference — doesn't it just fix the shift at test time?**
ACI recovers marginal coverage on the severe tasks, but at a cost: it inflates the prediction sets, often to the point of being uninformative, and among the three severe tasks only sales-shipcond retained usable sets under the study's criterion. It's also a test-time method — it needs to observe the shift. Mine is pre-deployment and complementary.

**Q: Could the whole effect just be the COVID shock?**
I ran a pre-COVID temporal placebo — train 2018, validate and test across 2019 — and for seven of the eight tasks the degradation is six to over a hundred times smaller; sales-office was near zero in both periods, so it's the exception. The diagnostic is most informative precisely under severe, event-driven shift, which is where you'd want it.
