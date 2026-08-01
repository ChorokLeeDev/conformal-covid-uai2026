# English Poster Presentation Script

**Title:** Diagnosing Conformal Prediction Failures Under Distribution Shift  
**Presenter:** Chorok Lee, KAIST  
**Venue:** UAI 2026, Amsterdam

---

## 30-Second Pitch

Hi, I am Chorok Lee from KAIST. This poster asks a simple deployment question: can we predict conformal prediction failure before deployment?

Conformal prediction gives useful uncertainty sets, but its coverage can break when calibration and deployment data are no longer exchangeable. In our COVID-19 supply-chain case study, some APS conformal predictors remain robust, while others lose coverage sharply.

The main finding is that, for GBM-based multiclass APS conformal predictors, top-1 SHAP concentration is a strong pre-deployment risk signal. Across 16 tasks from 9 domains, concentration correlates with coverage drop at **ρ = 0.853**, with **p < 0.001**. A 40% concentration cutoff is exploratory, but it gives **11 out of 12** matched risk labels across the SALT and specificity checks.

---

## Poster Flow With Pointing Cues

Use this if someone walks up and gives you 2-3 minutes.

1. **Start at the left column:** "The problem is that CP coverage can break under shift. COVID-19 creates a clean temporal stress test because supply-chain behavior changed rapidly."
2. **Point to Key Insight:** "The risk is not just whether the dataset shifted. The risk is whether the model relies too heavily on one feature that shifts."
3. **Move to the center Main Result:** "Fig. 1 is the main result. Each point is a task. Higher SHAP concentration before deployment tracks larger coverage loss after shift."
4. **Point to the theorem and Fig. 2:** "The mechanism is that concentrated reliance can amplify APS score inflation. Fig. 2 shows the same idea empirically: failing tasks concentrate SHAP mass on one shifted feature."
5. **Move to the right column:** "The specificity checks are low-concentration tasks, and they avoid catastrophic loss. The scope is GBM multiclass APS CP; RF and MLP likely need different diagnostics."
6. **End with the QR/contact block:** "The paper and code are linked here, and the main future direction is prospective validation plus neural diagnostics."

---

## 2-Minute Walkthrough

Hi, I am Chorok Lee from KAIST. This work is about diagnosing when conformal prediction fails under distribution shift.

The left column starts with the problem. Conformal prediction is attractive because it gives distribution-free uncertainty guarantees, but those guarantees rely on calibration and test data behaving similarly. During COVID-19, supply-chain behavior changed rapidly, so this assumption became fragile. Our research question is: **can we predict when CP fails before deployment?**

The key insight is feature reliance. If a GBM relies heavily on one feature, and that feature shifts, then the model has a single point of failure. The APS scores can inflate after the shift while the conformal cutoff remains calibrated to the old distribution. That creates undercoverage.

In the center, the main result shows that top-1 SHAP concentration predicts coverage drop. Fig. 1 plots 16 tasks: moving right means higher pre-deployment concentration, and moving up means larger coverage loss. The correlation is **ρ = 0.853**, with **p < 0.001** across **9 domains**. The takeaway is that high-concentration GBM models occupy the high-drop region.

Below that, the mechanism and theory block defines concentration as the share of total mean absolute SHAP importance assigned to the top feature. The theorem formalizes the same intuition: when the dominant shifted feature gives weaker true-class support, larger concentration puts more weight on that damaged signal. APS test scores rise, the cutoff stays fixed, and coverage drops.

Fig. 2 gives the mechanism visually. In catastrophic tasks, SHAP mass jumps toward one shifted feature. In robust or protected tasks, importance is more distributed or feature ranking remains more stable.

The right column gives the scope. This is a GBM diagnostic for multiclass APS CP. Random Forests and MLPs show weaker relationships, so they likely need different diagnostics. The future-work direction is to extend this idea with gradient-based explanations for neural networks and prospective validation in new domains.

The main message is: **do not only ask whether the data shifted. Ask whether the shift hits the feature direction the conformal predictor actually relies on.**

---

## 5-Minute Presentation Version

### Opening

Hi, I am Chorok Lee from KAIST. I will present our poster, **Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study**.

The motivation is that conformal prediction is useful because it provides distribution-free uncertainty sets. But in deployment, the guarantee can fail when the calibration distribution and test distribution are no longer exchangeable. This poster asks whether we can diagnose that risk before deployment.

### Problem And Motivation

The left side of the poster frames the problem. Conformal prediction can tell us, for example, how to build a prediction set targeting 90% coverage. But the finite-sample coverage guarantee depends on exchangeability between calibration and deployment data.

COVID-19 is a natural stress test. Supply-chain behavior changed between pre-COVID, lockdown, and post-COVID periods. Under that temporal shift, some conformal predictors remain close to target coverage, while others lose coverage sharply.

So the research question is: **can we predict when conformal prediction will fail before deployment?**

### Key Insight

The key idea is concentrated feature reliance.

If a model spreads importance across many features, then the prediction has some redundancy. A shift in one feature may not dominate the entire score distribution. But if a GBM relies heavily on one top feature, then a shift in that feature can move scores substantially.

For APS conformal prediction, that matters because the conformal cutoff is calibrated before deployment. If post-shift APS scores inflate, the old cutoff is too low, and coverage drops.

That is the core mechanism: **high concentration can create a single point of failure.**

### Data And Analysis Set

The main case study is the RelBench SALT supply-chain benchmark. We use 8 classification tasks under a COVID-19 temporal split from February to July 2020, with LightGBM multiclass APS conformal prediction.

For the primary correlation, we add 8 external multiclass tasks. That gives 16 tasks across 9 domains.

The left column also shows why standard shift tests are not enough. MMD, C2ST, and PSI can detect that a dataset shifted, but in this setting they have only a weak relationship to SALT coverage drop, with ρ at most 0.19. Our diagnostic asks a more model-specific question: is the shift aligned with a fragile feature direction the model already depends on?

### Main Result: Fig. 1

The main result is the center block. Fig. 1 plots SHAP concentration against coverage drop.

Each point is a task. The x-axis is top-1 SHAP concentration measured before deployment. The y-axis is coverage loss after shift, in percentage points. Moving right means the model is more concentrated; moving up means the conformal predictor loses more coverage.

Across 16 tasks, the Spearman correlation is **ρ = 0.853**, with **p < 0.001**, across **9 domains**. The important interpretation is not just that shift exists. The diagnostic identifies which conformal predictors are more likely to suffer coverage failure.

The 40% cutoff shown in the figure is exploratory. It is useful as a risk flag in this study, but it should be prospectively validated before being treated as universal.

### Mechanism And Theory: Fig. 2

The next center block defines the metric:

**Top-1 concentration is the top feature's mean absolute SHAP importance divided by total mean absolute SHAP importance.**

So the number is easy to interpret. If concentration is high, one feature dominates the model's explanatory mass.

The theorem underneath gives an idealized version of the same mechanism. If the dominant shifted feature provides weaker true-class support after shift, then larger concentration gives that damaged signal more weight. As a result, expected APS test scores increase. Since the conformal cutoff was calibrated before the shift, higher test scores imply lower coverage.

Fig. 2 then shows this visually. Panel A shows a catastrophic task where SHAP mass jumps toward one feature. Panel B shows a robust task where importance is more distributed. Panel C highlights the top-feature spike in the failing task. Panel D shows that robust tasks tend to keep feature ranking more stable under shift.

The nuance is important: high concentration is a risk signal, not an absolute failure guarantee. If the top feature is stable or protective, high concentration can be less dangerous. That is why the poster includes open questions about protective factors.

### Specificity Check

The right-top block is a specificity check. These are low-concentration tasks where the diagnostic should not falsely predict catastrophic failure.

CivilComments, Amazon, Covertype, and Adult are below the cutoff in this check and avoid catastrophic coverage loss. The table reports top-1 concentration, coverage drop in percentage points, and the resulting low-risk flag.

Combined with the SALT checks, the rule labels match in **11 out of 12** cases, or **91.7%**. I would describe this as a 12-check audit, not as proof of a universal threshold.

### Scope And Model Sensitivity

The scope block is deliberately conservative. The headline claim is about GBM-based multiclass APS conformal predictors.

In the model-sensitivity results, GBMs show the strongest relationship between concentration and failure. Random Forests are weaker, likely because bagging dilutes single-feature dependence. MLPs are also weaker, likely because their failures may be more distributed or representation-level rather than top-feature based.

So the current claim is not that SHAP concentration diagnoses every model class. The claim is that it captures a concentrated-dependence failure mode that is especially visible in GBMs.

### Conclusions And Future Work

The conclusion is that top-1 SHAP concentration provides a simple, interpretable, pre-deployment risk signal for GBM conformal predictors under shift.

The future-work directions are: prospective validation on new domains, detecting stable or protective top features, developing gradient-based diagnostics for MLPs, and mitigating concentration through features, dropout, or ensembles.

The open questions are also important. Can we design models that are intrinsically low-concentration? Does the 40% threshold hold prospectively? When is high concentration safe because the top feature is stable? And can streaming conformal prediction monitor concentration and trigger mitigation before failure?

The QR code at the bottom right links to the paper and code, and my contact is **choroklee@kaist.ac.kr**.

### Closing

The one-sentence takeaway is: **for GBM-based multiclass APS conformal predictors, concentrated SHAP reliance is a pre-deployment warning sign for coverage failure under distribution shift.**

---

## Short Closing Line

In one sentence: **SHAP concentration helps flag GBM conformal predictors that are vulnerable to coverage loss before deployment.**

---

## Q&A Notes

**What exactly is SHAP concentration?**  
It is the share of total mean absolute SHAP importance assigned to the top feature. High concentration means one feature dominates the model's explanatory mass.

**Why use only the top feature?**  
The observed failure mode is concentrated dependence. The top feature directly measures whether the model has a single dominant reliance point.

**Is the 40% threshold universal?**  
No. It is exploratory and should be prospectively validated. The poster presents it as a useful risk flag in this study, not a universal law.

**What does 91.7% mean?**  
It means 11 out of 12 rule labels matched across 8 SALT checks and 4 specificity checks. It is a compact audit of the exploratory rule.

**Why not use standard shift tests?**  
Standard tests detect distribution shift. They do not necessarily tell us whether the shifted direction is one the CP model relies on. SHAP concentration is model-specific.

**Does this work for all models?**  
No. The evidence is strongest for GBM/LightGBM multiclass APS CP. Random Forests and MLPs show different, weaker patterns.

**Does high concentration cause failure?**  
It is a risk signal. The theory explains why concentration can amplify score inflation when the dominant feature shifts in a damaging way, but stable or protective top features can be exceptions.

**Why mention gradient-based explanations?**  
Because TreeSHAP is natural for GBMs. Extending the diagnostic to neural networks likely requires gradient-based or representation-based explanations.

**What should a practitioner do if concentration is high?**  
Treat the model as vulnerable before deployment. Check the top feature, validate stability, reduce dependence through feature design or regularization, consider ensembles, and monitor post-deployment scores closely.

---

## Key Numbers To Memorize

- Primary correlation: **ρ = 0.853**, **p < 0.001**, **n = 16** tasks, **9 domains**
- Exploratory cutoff: **40%** top-1 SHAP concentration
- 12-check audit: **91.7%**, **11/12** labels matched
- Specificity checks: **4** low-concentration external checks
- Main case study: **8** SALT COVID temporal-split tasks
- Scope: **GBM/LightGBM multiclass APS conformal predictors**
