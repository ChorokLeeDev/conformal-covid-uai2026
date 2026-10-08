"""Deterministic claim checks; no training or historical experiment reproduction.

The two quantile witnesses isolate (1) a level/rank change and (2) interpolation
versus the exact order statistic. Both use valid binary inclusive APS scores and
execute the actual archived calibration and crossing-membership implementation.
Run from the repository root; JSON is emitted to stdout without overwriting data.
"""
import ast
import hashlib
import json
import math
import sys
import typing
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from aps_reference import calibration_quantile, true_label_scores

source = (ROOT / "src/run_aci_experiment.py").read_text()
node = next(n for n in ast.parse(source).body
            if isinstance(n, ast.ClassDef) and n.name == "ConformalClassifier")
namespace = {"np": np, "List": typing.List}
exec(compile(ast.Module(body=[node], type_ignores=[]), "archived_APS", "exec"), namespace)
Archived = namespace["ConformalClassifier"]


def crossing_hit(threshold, probabilities, true_label):
    predictor = Archived()
    predictor.quantile = threshold
    return int(true_label in predictor.predict_sets(np.array([probabilities]))[0])


cases = []
for n in [35737, 146948]:
    k = math.ceil((n + 1) * .9)
    level = k / n
    case = {"n": n, "rank": k, "level": level, "level_minus_nominal": level - .9}
    for name, low_count, target in [
        ("rank_correction", k - 1, [.8, .2]),
        ("interpolation", k, [.62, .38]),
    ]:
        probabilities = np.r_[np.tile([.6, .4], (low_count, 1)),
                              np.tile([0., 1.], (n - low_count, 1))]
        labels = np.zeros(n, dtype=int)
        predictor = Archived().calibrate(probabilities, labels)
        scores = true_label_scores(probabilities, labels)
        np.testing.assert_allclose(predictor._compute_scores(probabilities, labels), scores)
        nominal = float(np.quantile(scores, .9))
        exact = calibration_quantile(scores)
        linear = float(predictor.quantile)
        assert linear == float(np.quantile(scores, level))
        thresholds = {"nominal_linear": nominal, "exact_order_statistic": exact,
                      "historical_corrected_linear": linear}
        hits = {key: crossing_hit(value, target, 1) for key, value in thresholds.items()}
        case[name] = {"calibration_score_counts": {"0.6": low_count, "1.0": n-low_count},
                      "thresholds": thresholds, "target_probabilities": target,
                      "target_true_label": 1, "crossing_coverage_at_target_atom": hits}
        if name == "rank_correction":
            assert exact == 1. and nominal == .6
            assert hits["nominal_linear"] == 0 and hits["exact_order_statistic"] == 1
        else:
            assert exact == .6 and .63 < linear < .65
            assert hits["exact_order_statistic"] == 0 and hits["historical_corrected_linear"] == 1
    cases.append(case)

confidence_probabilities = np.array([[.6, .4], [.9, .1]])
confidence_scores = true_label_scores(confidence_probabilities, [0, 0])
np.testing.assert_allclose(confidence_scores, [.6, .9])

recovered = json.loads((ROOT / "audit/2026-10-08/recovery/raw-replay.json").read_text())
associations = []
for rule in ["inclusive", "crossing"]:
    means = [r for r in recovered["task_means"] if r["rule"] == rule]
    assert len(means) == 8
    result = spearmanr([r["C"] for r in means], [r["drop_pp"] for r in means])
    saved = next(r for r in recovered["associations"] if r["rule"] == rule)
    np.testing.assert_allclose([result.statistic, result.pvalue],
                               [saved["rho"], saved["p_asymptotic"]], rtol=0, atol=1e-14)
    associations.append({"rule": rule, "n_tasks": 8, "rho": float(result.statistic),
                         "p_asymptotic": float(result.pvalue)})

print(json.dumps({
    "scope": "Synthetic mathematical counterexamples and saved aggregate arithmetic only; no models fit or replayed",
    "baseline": "533814f27add9dd05bcebb74e71ea21bfeb76649",
    "versions": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__},
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "archived_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "quantile_cases": cases,
    "confidence_counterexample": {"probabilities": confidence_probabilities.tolist(),
                                   "true_labels": [0, 0], "inclusive_scores": confidence_scores.tolist()},
    "recovered_aggregate_associations": associations,
    "limits": "Target atoms are hypothetical witnesses, not recovered target distributions. They establish possibility, not the actual historical quantile effect. Nominal association p-values do not validate task exchangeability."
}, indent=2, allow_nan=False))
