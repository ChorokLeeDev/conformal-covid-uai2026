"""Exhaustive small-n rank sensitivity using published SALT summary points.

The permutation null assumes exchangeability of task pairs. That assumption is
not established for related SALT tasks, and no original models are rerun here.
Run from any directory; stdout is the complete machine-readable audit result.
"""

import ast
import itertools
import json
import math
from pathlib import Path

from scipy.stats import rankdata, spearmanr

root = Path(__file__).resolve().parents[2]
tree = ast.parse((root / "src/generate_n16_figure.py").read_text())
assignment = next(
    node for node in tree.body
    if isinstance(node, ast.Assign)
    and isinstance(node.targets[0], ast.Name)
    and node.targets[0].id == "salt_tasks"
)
rows = ast.literal_eval(assignment.value)
x = [row[1] for row in rows]
y = [row[2] for row in rows]
n = len(rows)
assert n == 8 and len(set(x)) == n and len(set(y)) == n
rx = rankdata(x).astype(int)
ry = rankdata(y).astype(int)
observed_distance = int(sum((rx - ry) ** 2))
max_distance = n * (n * n - 1) // 3
extreme = sum(
    distance <= observed_distance or distance >= max_distance - observed_distance
    for perm in itertools.permutations(range(1, n + 1))
    for distance in [sum((i - value) ** 2 for i, value in enumerate(perm, 1))]
)
total = math.factorial(n)
exact_p = extreme / total
print(json.dumps({
    "data_status": "rounded published SALT summaries; original models not rerun",
    "null_assumption": "task-pair exchangeability; not established for SALT",
    "alternative": "two-sided absolute Spearman statistic, no ties",
    "n": n,
    "rho": float(spearmanr(x, y).statistic),
    "rank_squared_distance": observed_distance,
    "permutations": total,
    "extreme_permutations": extreme,
    "exact_p": exact_p,
    "scipy_asymptotic_p": float(spearmanr(x, y).pvalue),
    "eight_test_holm_first_step": min(1.0, 8 * exact_p),
    "multiplicity_limit": "first-step sensitivity for reported smallest p; not an exact rerun of all eight metrics",
}, indent=2))
