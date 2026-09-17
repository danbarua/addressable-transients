"""S1 linear dynamics: M, evolve, design_input (DESIGN.md Arc 0 / S1 locks)."""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from .coupling import distance_coupled_ring


def build_M(
    N: int,
    *,
    epsilon: float,
    phi: float,
    omega: float,
    alpha: float = 1.0,
    A: np.ndarray | None = None,
) -> np.ndarray:
    """M = i ω I + ε e^{-i φ} A  (complex128)."""
    if A is None:
        A = distance_coupled_ring(N, alpha=alpha)
    A = np.asarray(A, dtype=np.float64)
    if A.shape != (N, N):
        raise ValueError(f"A shape {A.shape} != ({N}, {N})")
    M = (1j * omega) * np.eye(N, dtype=np.complex128)
    M = M + (epsilon * np.exp(-1j * phi)) * A.astype(np.complex128)
    return M


def evolve(x0: np.ndarray, t: float, M: np.ndarray) -> np.ndarray:
    """x(t) = exp(M t) x0  via scipy.linalg.expm, complex128."""
    x0 = np.asarray(x0, dtype=np.complex128).reshape(-1)
    M = np.asarray(M, dtype=np.complex128)
    return expm(M * t) @ x0


def design_input(x_star: np.ndarray, T: float, M: np.ndarray) -> np.ndarray:
    """u = x(0) = exp(-M T) x★  so that exp(M T) u = x★."""
    x_star = np.asarray(x_star, dtype=np.complex128).reshape(-1)
    M = np.asarray(M, dtype=np.complex128)
    return expm(-M * T) @ x_star
