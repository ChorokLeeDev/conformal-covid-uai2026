# Speaker Notes: Diagnosing Conformal Prediction Failures Under Distribution Shift

**UAI 2026 | Amsterdam | August 17-21, 2026**
**Chorok Lee, KAIST**

---

## Slide 1: Title

> "Good morning/afternoon. I'm Chorok Lee from KAIST. Today I'll present our work on diagnosing conformal prediction failures under distribution shift, using COVID-19 as a case study."

---

## Slide 2: The Promise of Conformal Prediction

> "Conformal prediction is powerful—it gives us distribution-free coverage guarantees that work with any base model. If we target 90% coverage, we're guaranteed the true label is in our prediction set at least 90% of the time."

> "But there's a catch..."

---

## Slide 3: The Hidden Assumption

> "Conformal prediction requires exchangeability—calibration and test data must come from the same distribution. But in real deployments, distribution shift is inevitable. COVID-19 is a perfect example—it changed everything."

---

## Slide 4: The Research Gap

> "Standard shift detectors like MMD and C2ST can detect that shift happened, but they detect it uniformly across all tasks. They can't tell you which models will catastrophically fail versus which will remain robust. Their correlation with coverage drop is only rho ≤ 0.19."

> "So our research question is: Can we predict WHEN conformal prediction will fail, before we deploy?"

---

## Slide 5-6: Conformal Prediction Primer

> "Quick primer on APS—Adaptive Prediction Sets. We compute nonconformity scores, calibrate a threshold on held-out data, and form prediction sets. The coverage guarantee holds under exchangeability."

---

## Slide 7: What Happens Under Shift

> "Under shift, coverage can degrade dramatically. In our SALT supply chain dataset, some tasks maintained 90% coverage while others dropped to as low as 12%. Same shift, wildly different outcomes."

---

## Slide 8-9: Our Proposal - SHAP Concentration

> "Our key insight: models with concentrated feature reliance are vulnerable. If your model depends heavily on a single feature and that feature shifts, you're in trouble."

> "We define SHAP concentration as the fraction of total feature importance in the top feature. It's simple, interpretable, and computable before deployment."

---

## Slide 10: The 40% Threshold

> "We found a natural gap in concentration values. Tasks above 40% tend to fail catastrophically; tasks below tend to remain robust."

> **Key stats to mention:**
> - LOO-CV accuracy: **87.5%** (7/8 correct)
> - Threshold stability: **43.1% ± 5.0%**
> - Cohen's d = **3.08** (large effect size)

---

## Slide 11: Methodology

> "We used LightGBM as our primary model. Important scope note: this diagnostic is **specific to gradient-boosted classifiers**. Random Forest shows rho=0.30 and MLP shows rho=0.43—both non-significant. This is because bagging dilutes concentration and MLP-SHAP is approximate."

---

## Slide 12: Main Result

> "Here's our primary finding. Across 16 multiclass tasks in 9 domains, SHAP concentration correlates with coverage drop with rho = 0.853, p < 0.001. This is a strong, statistically significant relationship."

---

## Slide 13: Within SALT Results

> "Within the SALT COVID dataset alone—8 supply chain tasks experiencing identical temporal shift—we see rho = 0.833, p = 0.010. The diagnostic works."

---

## Slide 14: External Validation - WILDS

> "We validated on external benchmarks including WILDS datasets:"
> - CivilComments: 26.2% concentration, robust ✓
> - Amazon: 1.9% concentration, robust ✓
> - Covertype: 12.5% concentration, robust ✓
> - Adult: 27.5% concentration, robust ✓

> "Combined accuracy across SALT + WILDS: **91.7%** (11/12 correct predictions)"

---

## Slide 15: Comparison with Standard Detectors

> "Standard shift detectors—MMD, C2ST, PSI—all detect shift for every task. But their correlation with coverage drop is at most 0.19. They can't distinguish catastrophic from robust outcomes. SHAP concentration can."

---

## Slide 16: Model Sensitivity

> "This is crucial: the diagnostic is **GBM-specific**."

| Model | ρ | Diagnostic? |
|-------|---|-------------|
| LightGBM | 0.833 | ✓ Yes |
| CatBoost | 0.667 | ✓ Yes |
| XGBoost | 0.548 | ✓ Yes |
| Random Forest | 0.30 | ✗ No |
| MLP | 0.43 | ✗ No |

> "Why? GBMs use sequential boosting that reinforces single-feature dependence. Bagging in RF dilutes it. MLP-SHAP is approximate and captures a different failure mode—global sensitivity."

---

## Slide 17-18: Theoretical Foundation

> "Theorem 1 provides mechanistic insight—not tight quantitative bounds, but directional understanding. Higher concentration monotonically worsens APS score bounds under shift. The theorem correctly predicts direction and monotonicity."

---

## Slide 19: Practical Framework

> "Our three-step framework:"
> 1. Train your GBM model
> 2. Compute SHAP concentration on validation data
> 3. If C ≥ 40%: flag as vulnerable, monitor closely
>    If C < 40%: lower risk, standard monitoring

---

## Slide 20: Limitations

> "Important limitations to acknowledge:"
> - **Model-specific**: GBM only—RF and MLP have different failure modes
> - 40% threshold is empirical, may need domain calibration
> - Diagnostic tool, not a fix
> - Correlation ≠ causation (though theory supports the mechanism)

---

## Slide 21: Conclusion

> "To summarize:"
> 1. SHAP concentration predicts CP failures **in GBMs** (ρ = 0.853)
> 2. Validated: LOO-CV 87.5%, WILDS 91.7%
> 3. Practical 40% threshold with uncertainty band
> 4. **Scope**: GBM classifiers only—not RF or MLP

> "This enables proactive identification of vulnerable deployments before failures occur."

---

## Q&A Preparation

### Likely Questions:

**Q: Why top-1 instead of top-k?**
> "We tested top-1, 2, 3, 5, 10, HHI, Gini, and entropy. Top-1 is the ONLY statistically significant metric (ρ=0.833, p=0.010). Adding more features actually decreases correlation because features 2-5 capture stable relationships, not the vulnerability source."

**Q: Why doesn't it work for neural networks?**
> "Two reasons: (1) MLP-SHAP uses kernel approximation, not exact decomposition like TreeSHAP, adding noise; (2) MLPs can fail via 'global sensitivity'—distributed importance but still catastrophic drops. The diagnostic captures concentrated-dependence failures, not global-sensitivity failures."

**Q: How do you handle the false positive (sales-office)?**
> "Sales-office has C=42.6% but maintained coverage. The protective factor is that its dominant feature (SALESORGANIZATION) has Jaccard=0.61 between train and test—it didn't actually shift. High concentration only causes failure when the concentrated feature shifts."

**Q: Is the 40% threshold overfitted?**
> "LOO-CV gives 87.5% accuracy with threshold stability of 43.1% ± 5.0%. Effect size is Cohen's d = 3.08 (large). The threshold emerged from a natural gap in concentration values, not from optimization."

---

## Timing Guide

| Section | Slides | Time |
|---------|--------|------|
| Intro/Motivation | 1-4 | 3 min |
| Background | 5-7 | 2 min |
| Method | 8-11 | 3 min |
| Results | 12-16 | 4 min |
| Theory | 17-18 | 2 min |
| Framework/Conclusion | 19-21 | 2 min |
| **Total** | 21 | **16 min** |
| Q&A | - | 4 min |

---

## Key Numbers to Remember

- **ρ = 0.853** (primary correlation, n=16, p<0.001)
- **ρ = 0.833** (SALT only, n=8, p=0.010)
- **40%** threshold
- **87.5%** LOO-CV accuracy
- **91.7%** combined SALT+WILDS accuracy
- **Cohen's d = 3.08** (large effect)
- **ρ ≤ 0.19** for standard detectors (MMD, C2ST)
