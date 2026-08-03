# English Poster Presentation Script

**Title:** Diagnosing Conformal Prediction Failures Under Distribution Shift  
**Presenter:** Chorok Lee, KAIST  
**Venue:** UAI 2026, Amsterdam

---

## 30-Second Pitch

Hi, I'm Chorok Lee from KAIST. Can we predict when conformal prediction fails before deployment?

CP gives distribution-free uncertainty sets, but coverage breaks under shift. Our finding: for GBM multiclass APS conformal predictors, **top-1 SHAP concentration** is a pre-deployment risk signal. Across 16 tasks from 9 domains, concentration correlates with coverage drop at **ρ = 0.853** (p < 0.001). A 40% cutoff achieves **11/12** matched risk labels.

---

## 3-Minute Walkthrough

**[Opening — 15 sec]**

Hi, I'm Chorok Lee from KAIST. This poster asks: can we predict when conformal prediction will fail before deployment?

**[Problem — 30 sec]**

[Point to left column]

Conformal prediction provides distribution-free uncertainty—the true label is in the prediction set with probability ≥ 90%. But this guarantee requires exchangeability between calibration and test data. COVID-19 broke this assumption in supply chains. Some CP models stayed robust; others lost coverage catastrophically.

Standard shift tests like MMD and C2ST detect that shift happened, but they don't tell us *which* CP model will break—correlation with coverage drop is only ρ ≤ 0.19.

**[Key Insight — 30 sec]**

[Point to Key Insight box]

The key idea: concentrated feature reliance creates a single point of failure. If a GBM relies heavily on one feature and that feature shifts, APS scores inflate while the calibration cutoff stays fixed. Result: undercoverage.

**[Main Result — 45 sec]**

[Point to center hero section and Fig. 1]

Fig. 1 is the main result. Pre-deployment risk signal predicts coverage drop.

Each point is a task. X-axis: top-1 SHAP concentration before deployment. Y-axis: coverage drop after shift—that's the fraction of samples where the true label is in the prediction set (validation minus post-shift test, in percentage points).

Across 16 tasks from 9 domains: **ρ = 0.853**, **p < 0.001**. High-concentration models cluster in the high-drop region.

The concentration formula is simple: the top feature's mean absolute SHAP importance divided by total. The 40% cutoff is exploratory but achieves **91.7%** label agreement (11/12 checks).

**[Mechanism — 30 sec]**

[Point to Fig. 2]

Fig. 2 shows the mechanism empirically. Panel A (catastrophic, 77pp drop): SHAP mass concentrates on one shifted feature. Panel B (robust, 8pp drop): importance distributes across multiple features. Panel D shows that the catastrophic task locks onto one feature ranking—stable but fragile. The robust task reshuffles—less stable but resilient.

**[Scope & Close — 30 sec]**

[Point to right column]

The scope is deliberate: GBM multiclass APS conformal predictors. Random Forests and MLPs show weaker patterns—they likely need different diagnostics.

The takeaway: **don't just ask whether data shifted. Ask whether the shift hits the feature direction your CP model relies on.**

Paper and code are linked via QR. Contact: choroklee@kaist.ac.kr.

---

## Poster Flow (if asked to point)

1. Left column: Problem & Motivation, Key Insight, SALT case study, Why Not Standard Shift Tests, Keywords
2. Center: Main Result (ρ=0.853), Mechanism & Theory, Fig. 2
3. Right: Specificity Check (91.7%), Scope & Model Sensitivity, Conclusions & Future Work, Open Questions

---

## Q&A Quick Answers

**What is coverage?**  
Fraction of samples where true label is in the prediction set. Target is 90%.

**What is SHAP concentration?**  
Top feature's mean |SHAP| divided by total. High C = one feature dominates.

**Is 40% universal?**  
Exploratory. Needs prospective validation.

**What does 91.7% mean?**  
11/12 rule labels matched across 8 SALT + 4 specificity checks.

**Why not MMD/C2ST/PSI?**  
They detect shift exists, not whether shift hits the model's key feature. ρ ≤ 0.19.

**Does high C cause failure?**  
It's a risk signal. If the top feature is stable, high C may be safe.

**What about top-2, top-3?**  
Future work. Paper shows top-1 had the strongest signal in this study.

**What should practitioners do?**  
Treat high-C models as vulnerable. Check the top feature, validate stability, consider regularization or ensembles, monitor post-deployment.

---

## Key Numbers

- **ρ = 0.853**, p < 0.001, n = 16 tasks, 9 domains
- **40%** exploratory cutoff
- **91.7%** (11/12) audit agreement
- **Coverage** = fraction where true label is in prediction set (target 90%)
- **GBM/LightGBM** multiclass APS CP scope
