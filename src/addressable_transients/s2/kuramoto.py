"""Kuramoto ODE and instantaneous Jacobian (DESIGN.md S2)."""

from __future__ import annotations

import numpy as np


def kuramoto_rhs(
    theta: np.ndarray,
    A: np.ndarray,
    kappa: float,
    omega: np.ndarray | float = 0.0,
) -> np.ndarray:
    """θ̇_i = ω_i + κ Σ_j A_ij sin(θ_j − θ_i)."""
    theta = np.asarray(theta, dtype=np.float64).reshape(-1)
    A = np.asarray(A, dtype=np.float64)
    dtheta = theta[None, :] - theta[:, None]  # (θ_j − θ_i)
    return np.asarray(omega, dtype=np.float64) + kappa * (A * np.sin(dtheta)).sum(axis=1)


def jacobian(theta: np.ndarray, A: np.ndarray, kappa: float) -> np.ndarray:
    """Instantaneous routing matrix J(θ).

    J_ij = κ A_ij cos(θ_j − θ_i)  (i≠j)
    J_ii = −Σ_{k≠i} κ A_ik cos(θ_k − θ_i)
    """
    theta = np.asarray(theta, dtype=np.float64).reshape(-1)
    A = np.asarray(A, dtype=np.float64)
    N = theta.size
    dtheta = theta[None, :] - theta[:, None]  # (θ_j − θ_i)
    J = kappa * A * np.cos(dtheta)
    np.fill_diagonal(J, 0.0)
    row_sums = J.sum(axis=1)
    J = J.copy()
    np.fill_diagonal(J, -row_sums)
    return J
