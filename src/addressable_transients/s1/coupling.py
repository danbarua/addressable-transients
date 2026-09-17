"""Distance-coupled ring adjacency (DESIGN.md S1 locks)."""

from __future__ import annotations

import numpy as np


def distance_coupled_ring(N: int, alpha: float = 1.0) -> np.ndarray:
    """Row-normalised distance-coupled ring adjacency.

    Locks (DESIGN.md)::

        d_ij = min(|i-j|, N-|i-j|)
        a_ij = d_ij^{-alpha} / sum_{k≠i} d_ik^{-alpha}   (i≠j)
        a_ii = 0
    """
    if N < 2:
        raise ValueError(f"N must be >= 2, got {N}")
    idx = np.arange(N)
    # Broadcast pairwise circular distances
    dij = np.minimum(np.abs(idx[:, None] - idx[None, :]), N - np.abs(idx[:, None] - idx[None, :]))
    with np.errstate(divide="ignore"):
        weights = np.where(dij > 0, dij.astype(np.float64) ** (-alpha), 0.0)
    row_sums = weights.sum(axis=1, keepdims=True)
    if np.any(row_sums == 0):
        raise ValueError("Zero row sum in distance weights")
    A = weights / row_sums
    np.fill_diagonal(A, 0.0)
    return A
