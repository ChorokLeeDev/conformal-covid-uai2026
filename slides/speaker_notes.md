# Diagnosing Conformal Prediction Failures Under Distribution Shift

One short read-aloud paragraph per slide. Use **Back to point** after a question. The settings follow Setup → Assumptions → Hypothesis → Result → Theorem.

[Basic setup questions](setup-questions.md)

<a id="slide-1"></a>

## 1. Diagnosing Conformal Prediction Failures

> **Back to point:** “What does the model rely on?”

My UAI paper asks why the same broad disruption can hurt some prediction tasks much more than others. I studied a COVID-19 supply-chain case study, looking at what fitted classifiers relied on and how their prediction-set coverage changed. I will explain the setup and assumptions before the question, findings and simplified theorem.

<a id="slide-2"></a>

## 2. Setup: feature row to label set

> **Back to point:** “Feature row, class probabilities, label set.”

For each business task, a row of tabular features enters a LightGBM classifier. It produces a probability for each possible label. APS uses those probabilities and a threshold chosen from labelled calibration cases to make a set of answers. Coverage is how often that set includes the true label. It is different from the accuracy of one best guess.

<a id="slide-3"></a>

## 3. Assumptions: what must stay stable?

> **Back to point:** “The promise and the mechanism each have assumptions.”

The usual conformal promise needs calibration and future cases to be statistically interchangeable, with the classifier fitted independently of calibration. A chronological split does not ensure that. Separately, the simplified theorem assumes one probability component stops supporting the true label while the remaining component stays stable. It holds the set threshold fixed. The historical pipeline has documented preprocessing and calibration limitations.

<a id="slide-4"></a>

## 4. Hypothesis: can reliance help explain loss?

> **Back to point:** “The changed relationship matters.”

I use SHAP to summarize how strongly the fitted model uses its features. Concentration is the share of measured attribution assigned to the top feature. If the relationship making that feature useful changes, could concentration help explain a larger coverage loss? A highly useful stable feature can be concentrated too. Concentration alone does not mean a model is bad.

<a id="slide-5"></a>

## 5. Result: a historical association

> **Back to point:** “Historical association, with its empirical scope.”

The selected-sixteen historical summaries show a positive association between concentration and coverage loss. Including the seventeenth task weakens it. This figure shows a retrospective finding, not a validated deployment alarm. Later checks with a different pipeline did not reproduce the positive association across all eight supply-chain tasks. The result motivates the question while leaving important limits.

<a id="slide-6"></a>

## 6. Result: different attribution patterns

> **Back to point:** “A pattern suggests a question; it does not prove its cause.”

These historical examples illustrate different attribution patterns around COVID. They help explain why model reliance was worth investigating. But the plots do not establish the theorem’s assumptions or prove the cause of a coverage change. I keep the measured pattern separate from the simplified explanation.

<a id="slide-7"></a>

## 7. Theorem: a conditional explanation

> **Back to point:** “A bound for a simplified model.”

Imagine a model that combines two sources of predicted probability. One becomes unreliable after the shift, while the other keeps its relationship to the true label. Under the stated conditions, giving the damaged component more weight worsens bounds on the APS score and coverage. That theoretical mixing share is not the measured SHAP share. The theorem does not prove that concentration always lowers actual coverage.

<a id="slide-8"></a>

## 8. Limits: what is still unvalidated?

> **Back to point:** “What evidence would support a stronger claim?”

The historical forty-percent cutoff is not a validated deployment rule. The later eight-task panel used a different protocol and did not reproduce the positive association. A SHAP plot also does not prove a causal mechanism. These limits lead to my next question: what information is actually enough to determine coverage under shift?

<a id="slide-9"></a>

## 9. Takeaway: ask what the evidence supports

> **Back to point:** “What does the evidence establish?”

The takeaway is to start with the model and the evidence. The classifier outputs probabilities and the calibrated rule creates a label set. Attribution is a measured clue about that fitted model. The historical finding and the simplified theorem have different scopes. My thesis asks what information would be needed to make a stronger coverage claim.
