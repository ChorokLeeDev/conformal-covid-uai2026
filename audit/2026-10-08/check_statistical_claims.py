"""Small audit checks, not a reproduction of the original experiments.

Run: python audit/2026-10-08/check_statistical_claims.py
Only synthetic counterexamples and already published rounded table entries are
used. Original supplementary ZIP members are inspected without extraction.
"""

import ast
from pathlib import Path
import sys
import typing
import unittest
import zipfile

import numpy as np
from scipy.stats import pearsonr, spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from aps_reference import all_scores, calibration_quantile, predict_sets, true_label_scores


class StatisticalAudit(unittest.TestCase):
    def test_same_membership_event_for_coverage_and_size(self):
        probabilities = np.array([[0.6, 0.3, 0.1]])
        membership = predict_sets(probabilities, 0.7)
        np.testing.assert_array_equal(membership, [[True, False, False]])
        self.assertEqual(int(membership.sum()), 1)
        self.assertEqual(bool(membership[0, 1]), bool(true_label_scores(probabilities, [1])[0] <= 0.7))

    def test_archived_crossing_rule_is_different(self):
        tree = ast.parse((ROOT / "src/run_aci_experiment.py").read_text())
        node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ConformalClassifier")
        namespace = {"np": np, "List": typing.List}
        exec(compile(ast.Module(body=[node], type_ignores=[]), "archived_aci_class", "exec"), namespace)
        classifier = namespace["ConformalClassifier"]()
        classifier.quantile = 0.7
        probabilities = np.array([[0.6, 0.3, 0.1]])
        self.assertIn(1, classifier.predict_sets(probabilities)[0])
        self.assertGreater(classifier._compute_scores(probabilities, np.array([1]))[0], 0.7)

    def test_ties_have_fixed_rank_order(self):
        np.testing.assert_allclose(all_scores([[0.2, 0.4, 0.4]]), [[1.0, 0.4, 0.8]])

    def test_quantile_one_includes_zero_probability_labels(self):
        np.testing.assert_array_equal(predict_sets([[1.0, 0.0]], 1.0), [[True, True]])

    def test_exact_order_statistic_and_small_calibration_boundary(self):
        self.assertAlmostEqual(calibration_quantile([0.1, 0.2, 0.3, 0.4], alpha=0.4), 0.3)
        q = calibration_quantile([0.1, 0.2], alpha=0.1)
        self.assertTrue(np.isposinf(q))
        self.assertTrue(predict_sets([[0.6, 0.3, 0.1]], q).all())

    def test_binary_and_three_class_shift_can_destroy_coverage(self):
        for k in (2, 3):
            cal = np.tile([0.9] + [0.1 / (k - 1)] * (k - 1), (20, 1))
            q = calibration_quantile(true_label_scores(cal, np.zeros(20, dtype=int)))
            test = [[0.01, 0.99] + [0.0] * (k - 2)]
            self.assertFalse(predict_sets(test, q)[0, 0])

    def test_negative_agreement_icc_does_not_imply_negative_correlation(self):
        with zipfile.ZipFile(ROOT / "submission/supplementary_material_fixed.zip") as package:
            tree = ast.parse(package.read("conformal_covid_code/compute_icc_and_partial.py"))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compute_icc_one_way")
        namespace = {"np": np}
        exec(compile(ast.Module(body=[node], type_ignores=[]), "archived_icc_function", "exec"), namespace)
        val = np.linspace(0.85, 0.95, 50)
        test = val - 0.7
        icc = namespace["compute_icc_one_way"](np.column_stack([val, test]))[0]
        self.assertLess(icc, -0.98)
        self.assertAlmostEqual(pearsonr(val, test).statistic, 1.0)

    def test_published_rounded_points_only(self):
        tree = ast.parse((ROOT / "src/generate_n16_figure.py").read_text())
        points = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in {"salt_tasks", "ext_tasks"}:
                    points[node.targets[0].id] = ast.literal_eval(node.value)
        rows = points["salt_tasks"] + points["ext_tasks"]
        rho = spearmanr([r[1] for r in rows], [r[2] for r in rows]).statistic
        self.assertAlmostEqual(rho, 0.8529411764705882)
        self.assertEqual(sum(c > 40 and drop > 15 for _, c, drop in rows), 5)
        self.assertEqual(sum(c > 40 and drop <= 15 for _, c, drop in rows), 1)
        self.assertEqual(sum(c <= 40 and drop > 15 for _, c, drop in rows), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
