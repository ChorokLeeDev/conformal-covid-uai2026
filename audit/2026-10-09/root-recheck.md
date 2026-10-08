# Separate root-agent scientific recheck

Date: 2026-10-09 KST. Baseline: `533814f27add9dd05bcebb74e71ea21bfeb76649`. Reviewed the staged `paper/main.tex` diff after the initial reviewer had reported findings. This is a second AI-agent check with shared model/tool limitations, not independent human review.

The root agent separately computed the quantile arithmetic using Python `fractions.Fraction`, without calling the reviewer witness helper. At alpha=0.1, n=35,737 gives k=32,165 and level excess 0.000047569745641771835; n=146,948 gives excess 0.000012249231020497046. Both rounded manuscript values agree.

A second check exercised `src/aps_reference.py` directly: k calibration scores at 0.6 followed by n-k scores at 1.0 give exact threshold 0.6 and NumPy interpolated threshold 0.639980972102785. Valid target probabilities (0.62, 0.38) with true class 0 are excluded/included by inclusive-score inversion respectively. This is a constructed distribution-shift witness; it does not quantify any original empirical coverage error. The reviewer also tests historical crossing sets separately. Increasing top-ranked true-class probability from 0.6 to 0.9 raises the inclusive score from 0.6 to 0.9, refuting its interpretation as decreasing true-class confidence.

The staged prose distinguishes level differences from threshold/coverage effects and does not infer the historical effect without original scores. The changed model-class caption explicitly separates LightGBM 50-seed mean drops from alternative seed-42 values. Diagnostic mechanism language is qualified consistently with the missing original feature ledger and recovered follow-up. No historical numeric table entry or original artifact was changed by the root check.

This recheck covers the new corrections. It does not verify all historical claims, repeat model training, establish external validity, or identify the arXiv submission payload. PDF validation is recorded separately after the final build.
