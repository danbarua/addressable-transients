"""S1 meters (DESIGN.md S1 locks)."""

from __future__ import annotations

import numpy as np


def R_C(x: np.ndarray, cluster: np.ndarray) -> float:
    """Amplitude-weighted order on cluster C (primary meter).

    R_C(x) = || sum_{j in C} x_j / sum_{j in C} |x_j| ||
    if the denominator is nonzero, else 0.
    """
    x = np.asarray(x, dtype=np.complex128).reshape(-1)
    xc = x[np.asarray(cluster, dtype=int)]
    denom = np.sum(np.abs(xc))
    if denom == 0.0:
        return 0.0
    return float(np.abs(np.sum(xc) / denom))


def R_C_unweighted(x: np.ndarray, cluster: np.ndarray) -> float:
    """Unweighted diagnostic meter R_C^u (reported, not Arc 0 primary)."""
    x = np.asarray(x, dtype=np.complex128).reshape(-1)
    xc = x[np.asarray(cluster, dtype=int)]
    n = xc.size
    if n == 0:
        return 0.0
    phases = np.exp(1j * np.angle(xc))
    return float(np.abs(np.mean(phases)))
