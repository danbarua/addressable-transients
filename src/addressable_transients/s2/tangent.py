"""S2 tangent / fundamental matrix oracles (DESIGN.md Arc 0 / S2 locks)."""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import inv

from .graph import grid_adjacency
from .kuramoto import jacobian, kuramoto_rhs

LOCKS = {
    "side": 16,
    "N": 256,
    "kappa": 1.0,
    "omega": 0.0,
    "t0": 0.0,
    "T": 1.0,
    "baseline_seeds": range(1, 11),
    "requested_nodes": (0, 15, 136, 255),
    "q_star": 0.25,
    "c": 0.20,
    "rtol": 1e-8,
    "atol": 1e-8,
    "fd_eps": 1e-6,
}


def make_baseline(seed: int, N: int = LOCKS["N"]) -> np.ndarray:
    """i.i.d. uniform phases on [0, 2π)^N in index order (locked RNG)."""
    rng = np.random.default_rng(seed)
    return rng.uniform(0.0, 2.0 * np.pi, size=N)


def _augmented_rhs(t, y, A, kappa, omega, N):
    """Baseline θ plus vectorised fundamental matrix Φ columns."""
    theta = y[:N]
    Phi = y[N:].reshape(N, N)
    dtheta = kuramoto_rhs(theta, A, kappa, omega)
    J = jacobian(theta, A, kappa)
    dPhi = J @ Phi
    return np.concatenate([dtheta, dPhi.ravel()])


def fundamental_matrix(
    theta0: np.ndarray,
    T: float,
    A: np.ndarray,
    kappa: float = LOCKS["kappa"],
    omega: float = LOCKS["omega"],
    t0: float = LOCKS["t0"],
    rtol: float = LOCKS["rtol"],
    atol: float = LOCKS["atol"],
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate Φ(T, t0) with solve_ivp RK45.

    Returns (Phi, theta_T) where δ(T) = Phi @ δ(t0).
    Φ(t0,t0) = I.
    """
    theta0 = np.asarray(theta0, dtype=np.float64).reshape(-1)
    N = theta0.size
    Phi0 = np.eye(N, dtype=np.float64)
    y0 = np.concatenate([theta0, Phi0.ravel()])
    sol = solve_ivp(
        _augmented_rhs,
        (t0, T),
        y0,
        method="RK45",
        args=(A, kappa, omega, N),
        rtol=rtol,
        atol=atol,
        dense_output=False,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    yT = sol.y[:, -1]
    theta_T = yT[:N]
    Phi = yT[N:].reshape(N, N)
    return Phi, theta_T


def evolve_nonlinear(
    theta0: np.ndarray,
    T: float,
    A: np.ndarray,
    kappa: float = LOCKS["kappa"],
    omega: float = LOCKS["omega"],
    t0: float = LOCKS["t0"],
    rtol: float = LOCKS["rtol"],
    atol: float = LOCKS["atol"],
) -> np.ndarray:
    """Integrate the nonlinear Kuramoto flow alone."""
    theta0 = np.asarray(theta0, dtype=np.float64).reshape(-1)

    def rhs(t, theta):
        return kuramoto_rhs(theta, A, kappa, omega)

    sol = solve_ivp(
        rhs,
        (t0, T),
        theta0,
        method="RK45",
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    return sol.y[:, -1]


def tangent_vs_finite_difference(
    theta0: np.ndarray,
    u: np.ndarray,
    T: float,
    A: np.ndarray,
    eps: float = LOCKS["fd_eps"],
    kappa: float = LOCKS["kappa"],
    omega: float = LOCKS["omega"],
    t0: float = LOCKS["t0"],
    rtol: float = LOCKS["rtol"],
    atol: float = LOCKS["atol"],
) -> dict:
    """Compare Φ u to (θ(T; θ0+εu) − θ(T; θ0))/ε at ε=10^{-6}.

    Returns dict with absolute and relative errors (∞-norm and 2-norm).
    """
    Phi, _ = fundamental_matrix(theta0, T, A, kappa, omega, t0, rtol, atol)
    u = np.asarray(u, dtype=np.float64).reshape(-1)
    delta_tan = Phi @ u

    theta_base = evolve_nonlinear(theta0, T, A, kappa, omega, t0, rtol, atol)
    theta_pert = evolve_nonlinear(theta0 + eps * u, T, A, kappa, omega, t0, rtol, atol)
    # Phase differences: wrap to (−π, π] for FD comparison stability
    raw = theta_pert - theta_base
    delta_fd = np.angle(np.exp(1j * raw)) / eps

    err = delta_tan - delta_fd
    abs_inf = float(np.max(np.abs(err)))
    abs_2 = float(np.linalg.norm(err))
    scale = max(float(np.linalg.norm(delta_fd)), 1e-30)
    rel_2 = abs_2 / scale
    return {
        "delta_tan": delta_tan,
        "delta_fd": delta_fd,
        "abs_inf": abs_inf,
        "abs_2": abs_2,
        "rel_2": rel_2,
        "Phi": Phi,
    }


def energy_share(delta: np.ndarray, i: int) -> float:
    """q_i(δ) = δ_i² / Σ_k δ_k² if ||δ||_2 > 0 else 0."""
    delta = np.asarray(delta, dtype=np.float64).reshape(-1)
    s = float(np.dot(delta, delta))
    if s == 0.0:
        return 0.0
    return float(delta[i] ** 2 / s)


def condition_number_2(Phi: np.ndarray) -> float:
    """κ₂(Φ) = ||Φ||_2 ||Φ^{-1}||_2."""
    return float(np.linalg.cond(Phi, p=2))


def recover_and_propagate(
    Phi: np.ndarray,
    j: int,
) -> dict:
    """u = Φ^{-1} e_j; δ = Φ u; report q_j and κ₂(Φ).

    Arc 0 Claim A harness: identity recovery of standard basis vector.
    """
    N = Phi.shape[0]
    e_j = np.zeros(N, dtype=np.float64)
    e_j[j] = 1.0
    u = inv(Phi) @ e_j
    delta = Phi @ u
    return {
        "u": u,
        "delta": delta,
        "q_j": energy_share(delta, j),
        "kappa2": condition_number_2(Phi),
        "err_inf": float(np.max(np.abs(delta - e_j))),
    }


def floor_statistic(theta0: np.ndarray, theta_T: np.ndarray, A: np.ndarray, kappa: float) -> float:
    """||J(θ(T))−J(θ(t0))||_F / ||J(θ(t0))||_F."""
    J0 = jacobian(theta0, A, kappa)
    JT = jacobian(theta_T, A, kappa)
    denom = np.linalg.norm(J0, ord="fro")
    if denom == 0.0:
        return 0.0
    return float(np.linalg.norm(JT - J0, ord="fro") / denom)


def default_adjacency() -> np.ndarray:
    return grid_adjacency(LOCKS["side"])
