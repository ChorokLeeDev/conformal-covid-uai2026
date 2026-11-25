# Diagnosing Conformal Prediction Failures Under Distribution Shift

One short read-aloud paragraph per slide. Use **Back to point** after a question. The settings follow Setup → Assumptions → Hypothesis → Result → Theorem.

[Basic setup questions](setup-questions.md)

<a id="slide-1"></a>

## 1. Diagnosing Conformal Prediction Failures

> **Back to point:** “What does the model rely on?”

My UAI paper asks a simple question: COVID-19 hit many prediction tasks with the *same* shock, so why did some tasks break badly while others barely moved? I study this on a real supply-chain case study. **My intuition was that the answer is not how much the data changed, but what each model was leaning on.** I'll walk through the setup and assumptions first, then the hypothesis, the result, and a simplified theorem.

<a id="slide-2"></a>

## 2. Setup: feature row to label set

> **Back to point:** “Feature row in, class probabilities, label set out.”

Let me be concrete about what the model does. **The input is a row of tabular features** — things like transaction ID, product type, customer region. That row goes into a **LightGBM classifier**, a tree model, and **the output is a probability for every possible label**. We then wrap those probabilities with **APS — Adaptive Prediction Sets — which keeps adding the highest-probability labels into a set until their cumulative probability clears a calibrated threshold.** So the final output is a *set* of answers, not one guess. **Coverage** is simply how often that set contains the true label — different from whether the single top guess is right.

<a id="slide-3"></a>

## 3. Assumptions: what must stay stable?

> **Back to point:** “The promise and the theorem each have their own assumptions.”

There are two separate assumptions here, and it helps to keep them straight. **The first is what the conformal guarantee needs:** the calibration cases and the future test cases have to be interchangeable — like draws from the same population. Splitting the timeline around COVID-19 breaks exactly that, which is why coverage can fall. **The second is what my theorem assumes** — a cleaner, made-up setting where one part of the model breaks and the rest stays put. I keep them apart because the first is a real-world condition that fails, while the second is a simplified picture I use to explain *why* it fails.

<a id="slide-4"></a>

## 4. Hypothesis: can reliance help explain the loss?

> **Back to point:** “A changed, heavily-used feature is the suspect.”

My intuition was simple: **if a model relies almost entirely on one feature, then when a distribution shift changes that feature's relationship to the answer, the prediction breaks.** To measure that reliance *before* deployment, I use **SHAP — a method that splits a prediction into how much each feature contributed, relative to a baseline.** From that I define **concentration: the share of total SHAP importance held by the single top feature**, a number between 0 and 1. My hypothesis: higher concentration should go with larger coverage loss. One caveat — a stable, genuinely useful feature can also be concentrated, so concentration alone does not mean a model is bad.

<a id="slide-5"></a>

## 5. Result: a historical association

> **Back to point:** “A real association, stated with its scope.”

Across my main set of sixteen tasks, **higher SHAP concentration goes with larger coverage loss** — a strong positive association (ρ = 0.853), while standard shift detectors show almost none. This is a retrospective finding that motivates the question, and I'll come to its limits in a moment.

<a id="slide-6"></a>

## 6. Result: two tasks, same shock, different outcome

> **Back to point:** “A pattern that raises a question; it doesn't prove the cause.”

Here are two tasks hit by the same COVID shock. **In the fragile one, one feature holds most of the importance** — the model relies on that one signal, and when it breaks the model gives a wrong answer with high confidence, shrinking its set when it should widen it. In the robust one, importance is spread across several features, so when one breaks the others cover for it. The point to notice: **standard shift detectors fire on both tasks the same way** — they see that the data changed, but not whether the model will break. These plots show the mechanism; they do not by themselves prove the cause.

<a id="slide-7"></a>

## 7. Theorem: a conditional explanation

> **Back to point:** “A coverage bound for a simplified mixture model.”

To back the intuition with math, the theorem takes a toy model whose probability is a **mixture of two parts**: one part rides the dominant feature, the other rides the rest. Call the weight on the dominant part its *mixing weight* — if it's 0.8, the model leans 80% on that one part. Suppose after the shift that dominant part stops supporting the true label while the other part stays stable. **Then the bigger that mixing weight, the more the true label's APS score gets pushed above the cutoff — which forces coverage down.** One honest caution: this made-up mixing weight is *not* the same number as the SHAP concentration I measure on real models — they're both "how much the model leans on one thing," but one is a theoretical knob and the other is a measurement. So the theorem explains the mechanism; it doesn't prove that measured concentration always lowers real coverage.

<a id="slide-8"></a>

## 8. Limits: where the tool stops — and where I want to go next

> **Back to point:** “What would support a stronger claim?”

I want to be clear about the boundaries. The association is not bulletproof: adding one more borderline task pulls the correlation from 0.85 down to 0.65, and when I re-ran the check on a separate group of tasks it did not hold up everywhere. The 40% cutoff is a rule of thumb, not a validated rule, and a SHAP plot doesn't prove a cause. More fundamentally, **the tool is model-specific** — it works for gradient-boosted trees, where feature splits are localized, but it can't explain entangled, global sensitivity failures in deep networks. **That limit is where I want to take the work next:** for neural networks we can't lean on single-feature attributions — we need to dissect the network itself, its gradient and spectral structure, and turn that internal analysis into lightweight, pre-deployment robustness checks.

<a id="slide-9"></a>

## 9. Takeaway: start from the model and the evidence

> **Back to point:** “What does the evidence actually establish?”

To wrap up: distribution shift causes failures that are easy to miss — the model shrinks its set and gives a wrong answer with high confidence, which standard shift detectors do not catch. For gradient-boosted models, **SHAP concentration on validation data gives a practical pre-deployment warning signal**, supported by a historical association and a conditional theorem, each with its own scope. Where it stops is deep learning — and that is the direction I want to develop: the same kind of lightweight, practical robustness diagnostic, built on a mathematical analysis of what happens inside the network.
