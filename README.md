# Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study

**Accepted at UAI 2026**

Chorok Lee  
Korea Advanced Institute of Science and Technology (KAIST)  
choroklee@kaist.ac.kr

## Abstract

Conformal prediction provides distribution-free coverage guarantees, but these degrade under distribution shift—and practitioners lack tools to anticipate which deployed models will fail before observing test data. We propose SHapley Additive exPlanations (SHAP) concentration—the fraction of feature importance concentrated in the top feature—as a pre-deployment diagnostic for conformal prediction vulnerability in gradient-boosted classifiers. Using COVID-19 as a naturalistic case study, eight supply chain tasks experience identical temporal shift yet coverage drops ranging from negligible to catastrophic. Feature-importance concentration is strongly associated with failure severity across 16 multiclass tasks in 9 domains (ρ = 0.853, p < 0.001), while standard distributional shift detectors cannot distinguish catastrophic from robust outcomes.

## Key Results

| Metric | Value |
|--------|-------|
| Primary correlation (n=16) | ρ = 0.853, p < 0.001 |
| Bootstrap 95% CI | [0.50, 0.96] |
| Within SALT (n=8) | ρ = 0.833, p = 0.010 |
| Covertype (external) | C = 49.8%, drop = 81.8pp ✓ |

## Repository Structure

```
├── paper/
│   ├── main.pdf          # Camera-ready paper
│   ├── main.tex          # LaTeX source
│   ├── references.bib    # Bibliography
│   └── uai2026.cls       # UAI 2026 style
├── src/                  # Core experimental code
│   ├── compute_shap_concentration_all_tasks.py
│   ├── run_aci_experiment.py
│   ├── create_figure3_shap.py
│   ├── generate_4panel_cdf.py
│   └── generate_n16_figure.py
└── figures/              # Paper figures (PDF)
```

## Citation

```bibtex
@inproceedings{lee2026diagnosing,
  title={Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study},
  author={Lee, Chorok},
  booktitle={Proceedings of the 42nd Conference on Uncertainty in Artificial Intelligence (UAI)},
  year={2026},
  publisher={PMLR}
}
```

## License

CC BY 4.0
