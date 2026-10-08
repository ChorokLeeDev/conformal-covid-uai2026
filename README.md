# Diagnosing Conformal Prediction Failures Under Distribution Shift: A COVID-19 Case Study

**Original repository status: accepted at UAI 2026. Statistical audit revision in progress.**

The active manuscript now documents material statistical and reproducibility
limitations. Historical numerical results have **not** been reproduced under a
corrected common protocol: supplied scripts use different APS membership rules,
fit preprocessing with test information, and reuse calibration labels for early
stopping. Original submitted PDFs and ZIPs are preserved unchanged.

See [initial audit](audit/2026-10-08/initial-review.md) and
[revision record](audit/2026-10-08/revision-record.md). The new
`src/aps_reference.py` is a separately labeled reference for future reruns, not
the code that generated the historical tables. Run the focused statistical
counterexamples with `python audit/2026-10-08/check_statistical_claims.py`.

Chorok Lee  
Korea Advanced Institute of Science and Technology (KAIST)  
choroklee@kaist.ac.kr

## Abstract

Historical summaries suggest an association between SHAP concentration and
coverage degradation. The selected 16-task summaries give ρ = 0.853; including
the excluded three-class task gives ρ = 0.654 across 17 tasks. These correlations
can be checked from rounded reported points. They do not establish prospective
validity, causal mechanisms, or replication of the missing original experiments.

## Historical Reported Results (underlying experiments unverified)

| Metric | Value |
|--------|-------|
| Primary correlation (n=16) | ρ = 0.853, p < 0.001 |
| Bootstrap 95% CI | [0.50, 0.96] |
| Within SALT (n=8) | ρ = 0.833, p = 0.010 |
| Covertype (external) | C = 49.8%, drop = 81.8pp (historical report) |

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
