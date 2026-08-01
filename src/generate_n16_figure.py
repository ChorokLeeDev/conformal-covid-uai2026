#!/usr/bin/env python3
"""
Generate Figure: SHAP Concentration vs Coverage Drop, n=16 multiclass tasks (9 domains).
Primary result: rho=0.853, p<0.001.

Output: results/figure_n16_correlation.pdf
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import spearmanr

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ── Data ──────────────────────────────────────────────────────────────────────
# 8 SALT tasks (supply-chain domain, COVID temporal shift)
salt_tasks = [
    ("s-shipcond",   50.7,  71.6),
    ("s-payterms",   54.2,  77.1),
    ("s-group",      47.3,  71.2),
    ("i-shippoint",  48.8,  18.5),
    ("s-office",     42.6,   0.1),
    ("i-incoterms",  28.9,  11.3),
    ("i-plant",      23.9,  10.6),
    ("s-incoterms",  23.7,   8.5),
]

# 8 external multiclass tasks (7 non-supply-chain domains, 10-seed means)
ext_tasks = [
    ("Covertype",   49.78,  81.8),
    ("KDDCup99",    21.13,  15.9),
    ("Gas Sensor",   7.27,  -3.8),
    ("Avila",       20.49,   1.0),
    ("Shuttle",     30.66,   0.3),
    ("PAMAP2",      19.24,  -2.1),
    ("Pendigits",   14.45,  -1.7),
    ("Satimage",     9.04,  -0.3),
]

# Verify correlation
all_c   = [t[1] for t in salt_tasks + ext_tasks]
all_d   = [t[2] for t in salt_tasks + ext_tasks]
rho, p  = spearmanr(all_c, all_d)
print(f"n=16 Spearman rho={rho:.3f}, p={p:.4f}")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.2, 4.4))

# SALT points (dark filled circles)
salt_c = [t[1] for t in salt_tasks]
salt_d = [t[2] for t in salt_tasks]
ax.scatter(salt_c, salt_d, color='#1f4e79', s=60, zorder=5,
           marker='o', label='SALT (supply-chain, COVID)')

# External points (orange triangles)
ext_c = [t[1] for t in ext_tasks]
ext_d = [t[2] for t in ext_tasks]
ax.scatter(ext_c, ext_d, color='#c55a11', s=60, zorder=5,
           marker='^', label='External (8 domains, 10 seeds)')

# 40% threshold, shown as an exploratory decision boundary rather than a result.
ax.axvline(40, color='#555555', linestyle='--', linewidth=1.4, alpha=0.8)
ax.text(40.8, -10.5, '40% exploratory cutoff', rotation=90,
        fontsize=9.5, color='#555555', va='bottom', ha='left')

# Label only the points needed to read the scientific story at poster distance.
labels = {
    "Covertype":   ( 1.5, -4),
    "s-payterms":  (-13,  3),
    "s-shipcond":  (-14, -3),
    "s-group":     ( 1.5,  2),
    "s-office":    ( 1.5,  4),   # high C but protected/stable feature
    "KDDCup99":    ( 1.5,  3),   # low C but nonzero drop
}

for name, c, d in salt_tasks + ext_tasks:
    if name not in labels:
        continue
    dx, dy = labels[name]
    color = '#1f4e79' if name.startswith(('s-', 'i-')) else '#c55a11'
    ax.annotate(name, (c, d), fontsize=9, color=color,
                xytext=(dx, dy), textcoords='offset points')

# Annotation box
ax.text(0.04, 0.97,
        f'$\\rho={rho:.3f}$, $p<0.001$\n$n=16$, 9 domains',
        transform=ax.transAxes, fontsize=11, va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))

ax.set_xlabel('SHAP Concentration $C$ (%)', fontsize=12)
ax.set_ylabel('Coverage Drop (pp)', fontsize=12)
ax.set_title('Pre-deployment SHAP Concentration vs. Coverage Drop',
             fontsize=13, pad=8)
ax.legend(fontsize=9.5, loc='upper center', bbox_to_anchor=(0.5, -0.16),
          ncol=2, frameon=False)
ax.set_xlim(-2, 65)
ax.set_ylim(-15, 90)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=(0, 0.08, 1, 1))
out = 'figures/figure_n16_correlation.pdf'
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"Saved: {out}")
