# English Poster Presentation Script

**Title:** Diagnosing Conformal Prediction Failures Under Distribution Shift  
**Presenter:** Chorok Lee, KAIST  
**Poster:** UAI 2026

---

## 30-Second Pitch

Hi, I am Chorok Lee from KAIST. This poster studies when conformal prediction fails under distribution shift.

Conformal prediction gives distribution-free coverage guarantees, but those guarantees rely on exchangeability between calibration and deployment data. In real deployments, especially during events like COVID-19, that assumption can break.

Our main finding is that, for gradient boosting models, SHAP concentration is a strong pre-deployment diagnostic. If one feature dominates the model's SHAP importance, then a shift in that feature can cause severe coverage failure. Across 16 tasks, SHAP concentration correlates with coverage drop at rho = 0.853, and a 40% threshold gives 87.5% leave-one-out accuracy.

---

## 2-Minute Walkthrough

Hi, I am Chorok Lee from KAIST. This work is about diagnosing conformal prediction failures under distribution shift, using COVID-19 as a case study.

The starting point is the problem on the left side of the poster. Conformal prediction is attractive because it provides distribution-free uncertainty estimates. For example, if we target 90% coverage, the conformal set should contain the true label at least 90% of the time. But that guarantee depends on calibration and test data being exchangeable. During COVID-19, behavior patterns changed sharply, so this assumption became fragile.

The research question is: can we predict when conformal prediction will fail before deployment?

Our key insight is shown in the orange box. Models with concentrated feature reliance are more vulnerable. If the model depends heavily on a single dominant feature, and that feature shifts, then the conformal scores can move substantially. There are fewer redundant features to absorb the shift, so the calibration threshold becomes misaligned.

In the center, we define SHAP concentration as the fraction of total SHAP importance assigned to the top feature. So the metric is very simple: top feature importance divided by total feature importance. We use 40% as the empirical threshold. Below 40%, the model is usually robust; at or above 40%, the model is flagged as vulnerable.

The main result is the large number in the center. Across 16 multiclass tasks from 9 domains, SHAP concentration has a Spearman correlation of rho = 0.853 with coverage drop, with p < 0.001. Within the SALT COVID tasks alone, the correlation is also strong: rho = 0.833.

The right column shows external validation and practical use. On WILDS and UCI benchmarks, the diagnostic predicts robust behavior for the external tasks, and the combined accuracy is 91.7%, or 11 out of 12 correct predictions.

The practical framework is straightforward: train the model, compute SHAP, calculate concentration, and then decide. If concentration is below 40%, proceed with standard monitoring. If it is at least 40%, mitigate before deployment.

The important scope limitation is that this is a GBM diagnostic. It works best for LightGBM, CatBoost, and XGBoost. It does not transfer cleanly to Random Forests or MLPs, which appear to have different failure modes.

The takeaway is that SHAP concentration gives a simple, interpretable, pre-deployment signal for conformal prediction vulnerability under distribution shift.

---

## 5-Minute Presentation Version

### Opening

Hi, I am Chorok Lee from KAIST. I will present our work, **Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study**.

The motivation is simple: conformal prediction is widely used because it gives distribution-free uncertainty guarantees. But in deployment, those guarantees can fail when the data distribution changes. This poster asks whether we can diagnose that vulnerability before deployment.

### Problem and Motivation

On the left side, the poster summarizes the core problem. Conformal prediction assumes that calibration and test data are exchangeable. In practice, this assumption is often violated. COVID-19 is a clear example: supply-chain behavior changed rapidly between pre-COVID, lockdown, and post-COVID periods.

The key issue is that not all tasks fail equally. Some tasks remain close to the target coverage, while others collapse catastrophically. Standard shift detectors can tell us that shift exists, but they are much weaker at predicting which conformal predictors will actually lose coverage.

So the research question is: **can we predict when conformal prediction fails before deployment?**

### Key Insight

Our hypothesis is that failure depends on how concentrated the model's feature reliance is.

If importance is spread across many features, then the model has some redundancy. A shift in one feature may not dominate the prediction behavior. But if one feature carries most of the model's importance, then a shift in that feature can strongly perturb the model scores. Since conformal prediction calibrates a threshold based on past scores, that score perturbation can translate into undercoverage.

This is why the poster emphasizes the mechanism: **high concentration implies high vulnerability**.

### Dataset

The main case study is the SALT supply-chain benchmark from RelBench. We evaluate 8 classification tasks under a COVID-19 temporal split from February to July 2020. The poster also includes 8 external tasks, giving 16 total tasks across 9 domains.

### SHAP Concentration Metric

The center-top panel defines the diagnostic. We compute SHAP values and measure the share of total importance assigned to the top feature:

`SHAP concentration = top feature SHAP importance / total SHAP importance`.

This has two advantages. First, it is interpretable: it tells us whether the model relies too heavily on one feature. Second, it is available before deployment, as long as we can compute feature importance on validation data.

Empirically, we use a 40% threshold. If the top feature accounts for less than 40% of total importance, we classify the model as robust. If it accounts for 40% or more, we flag it as vulnerable.

Fig. 2 gives the intuition. In a catastrophic task, the dominant feature becomes much more important under the shifted test distribution. In a robust task, importance is more distributed and the ranking is more stable.

### Main Result

The main result is in the center of the poster. Across 16 tasks, SHAP concentration correlates strongly with coverage drop:

**rho = 0.853, p < 0.001**.

Within the SALT COVID tasks alone, the result is also strong:

**rho = 0.833, p = 0.010**.

This means that the diagnostic is not only identifying that distribution shift exists. It is specifically capturing which tasks are more likely to suffer conformal coverage failure.

### Model Scope

The model-scope box is important. This result is strongest for gradient boosting models. LightGBM has rho = 0.833, CatBoost has rho = 0.667, and XGBoost has rho = 0.548.

However, Random Forest and MLP do not show the same pattern. Random Forest has rho = 0.30, and MLP has rho = 0.43. Our interpretation is that GBMs often create concentrated dependence through sequential boosting, while Random Forests and MLPs can fail through different mechanisms. So the scope of the poster is deliberately conservative: this is a GBM diagnostic, not a universal model diagnostic.

### External Validation

The right-top panel shows external validation on WILDS and UCI datasets. CivilComments, Amazon, Covertype, and Adult all have low SHAP concentration under this evaluation, and the diagnostic predicts them as robust. Combined with the SALT tasks, the diagnostic reaches **91.7% accuracy**, or **11 out of 12** correct predictions.

### Practical Framework

The practical workflow is shown in the orange box on the right. It has three steps.

First, train the model. Second, compute SHAP values. Third, calculate concentration.

If concentration is below 40%, the model can proceed with standard deployment monitoring. If concentration is at least 40%, the model should be treated as vulnerable. In that case, we recommend mitigation before deployment, such as diversifying features, reducing reliance on a dominant feature, adding regularization, using ensembles with diverse feature subsets, or setting up tighter monitoring and retraining triggers.

### Conclusion and Future Work

The conclusion is that SHAP concentration is a simple, interpretable, pre-deployment diagnostic for conformal prediction vulnerability under distribution shift.

The key numbers are: rho = 0.853 across 16 tasks, 87.5% leave-one-out threshold accuracy, and 91.7% combined external validation accuracy.

Future work goes in three directions. First, mitigation: how do we automatically reduce concentration before deployment? Second, prospective validation: how stable is the 40% threshold in new domains? Third, streaming conformal prediction: can we monitor concentration and coverage drift online and trigger model updates before coverage collapses?

The broader message is that we should not only ask whether distribution shift happened. We should ask whether the shift affects the features the model actually relies on.

---

## Short Closing Line

In one sentence: **SHAP concentration helps identify GBM-based conformal predictors that are vulnerable to coverage failure before they are deployed.**

---

## Q&A Notes

**Why use the top feature only?**  
Because the failure mode we observe is concentrated dependence. The top feature captures whether one feature dominates the model's behavior. Adding more features can dilute this signal.

**Is the 40% threshold universal?**  
No. It is an empirical threshold from this study. The leave-one-out result is strong, but prospective validation on new domains is an explicit future-work direction.

**Does this work for all model classes?**  
No. The current evidence supports GBM classifiers. Random Forests and MLPs appear to have different failure modes, so they likely need different diagnostics.

**Does high concentration cause failure?**  
High concentration is a vulnerability signal. It becomes especially dangerous when the dominant feature shifts. The theory supports the mechanism, but the diagnostic should be interpreted as risk prediction, not a universal causal claim.

**What should a practitioner do when concentration is high?**  
Mitigate before deployment: diversify features, reduce reliance on the dominant feature, regularize the model, use diverse ensembles, monitor concentration over time, and prepare retraining or adaptive conformal updates.

---

## Key Numbers to Memorize

- Primary correlation: **rho = 0.853**, **p < 0.001**, **n = 16** tasks
- SALT-only correlation: **rho = 0.833**, **p = 0.010**, **n = 8** tasks
- Threshold: **40% SHAP concentration**
- Leave-one-out threshold accuracy: **87.5%**
- Combined validation accuracy: **91.7%**, **11/12 correct**
- Scope: **GBM classifiers only**
