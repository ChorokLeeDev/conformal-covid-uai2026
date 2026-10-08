"""Auditable deterministic APS reference for future reruns.

Added during the 2026-10-08 audit. This does not generate or validate the
historical manuscript results. Classes use a fixed ascending-index tie order;
sets invert the inclusive cumulative-probability score without adding an extra
crossing label. Model fitting/tuning must be separate from calibration.
"""

import math

import numpy as np


def all_scores(probabilities):
    """Return the inclusive rank score of every class in every row."""
    probs = np.asarray(probabilities, dtype=float)
    if probs.ndim != 2 or probs.shape[1] < 2:
        raise ValueError("probabilities must have shape (observations, classes>=2)")
    if not np.isfinite(probs).all() or np.any(probs < 0):
        raise ValueError("probabilities must be finite and nonnegative")
    if not np.allclose(probs.sum(axis=1), 1.0, rtol=0, atol=1e-10):
        raise ValueError("probability rows must sum to one")
    order = np.argsort(-probs, axis=1, kind="stable")
    ranked = np.take_along_axis(probs, order, axis=1)
    cumulative = np.minimum(np.cumsum(ranked, axis=1), 1.0)
    scores = np.empty_like(cumulative)
    np.put_along_axis(scores, order, cumulative, axis=1)
    return scores


def true_label_scores(probabilities, labels):
    scores = all_scores(probabilities)
    labels = np.asarray(labels)
    if labels.shape != (len(scores),) or not np.issubdtype(labels.dtype, np.integer):
        raise ValueError("labels must contain one integer class index per row")
    if np.any(labels < 0) or np.any(labels >= scores.shape[1]):
        raise ValueError("labels are outside the declared class vocabulary")
    return scores[np.arange(len(scores)), labels]


def calibration_quantile(scores, alpha=0.1):
    """Finite-sample order statistic, including the +infinity boundary."""
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 1 or not len(scores) or not np.isfinite(scores).all():
        raise ValueError("calibration scores must be a nonempty finite vector")
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one")
    k = math.ceil((len(scores) + 1) * (1 - alpha))
    return float("inf") if k > len(scores) else float(np.partition(scores, k - 1)[k - 1])


def predict_sets(probabilities, quantile):
    """Boolean membership matrix: coverage and sizes must use this matrix."""
    if np.isnan(quantile):
        raise ValueError("quantile cannot be NaN")
    return all_scores(probabilities) <= quantile
