# Exact rank-permutation sensitivity — 2026-10-08

This follow-up uses the eight rounded SALT points in
`src/generate_n16_figure.py`. It does not rerun any original model or claim that
the task observations are independent or exchangeable.

Under the hypothetical permutation null of exchangeable task pairings, fixed
untied ranks allow exhaustive enumeration of all 8! = 40,320 pairings. The observed
Spearman rho is 5/6 (sum of squared rank differences = 14). Exactly 620 permutations
have absolute correlation at least as large, giving the exact two-sided
p = 620/40,320 = **0.015376984126984126**. SciPy's asymptotic approximation on the
same points is **0.010175540123456752**.

For the reported smallest p in an eight-metric family, the Holm first-step
sensitivity is 8 × p = **0.12301587301587301**. This is not an exact rerun of the
other seven metrics; their complete taskwise values are absent. Neither this
value nor the earlier asymptotic eight-test value 0.0814 supports significance
at 0.05 after the stated multiplicity adjustment.

The exchangeability assumption is material: common SALT entities and time
periods may invalidate permutation inference. An exact conditional calculation
does not repair dependent tasks, retrospective metric/endpoint selection,
incompatible historical APS conventions, or missing experiment provenance.

Executed command (exit 0):

```bash
python audit/2026-10-08/exact_permutation_sensitivity.py > audit/2026-10-08/exact-permutation-result.json
```

The generated JSON preserves the observed statistic, enumeration counts,
asymptotic comparator, multiplicity sensitivity and assumptions. The manuscript
adds this as a bounded statistical sensitivity check, not a new empirical result.
