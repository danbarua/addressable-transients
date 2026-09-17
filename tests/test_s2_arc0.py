"""S2 Arc 0 oracles — fail if DESIGN.md tolerances / identities are violated."""

from __future__ import annotations

import numpy as np
import pytest

from addressable_transients.s2 import (
    LOCKS,
    condition_number_2,
    energy_share,
    fundamental_matrix,
    grid_adjacency,
    jacobian,
    kuramoto_rhs,
    recover_and_propagate,
    tangent_vs_finite_difference,
)
from addressable_transients.s2.tangent import make_baseline

# Arc 0 harness tolerances (identity checks; not Arc 1 scientific rates)
TOL_FD_REL = 5e-3  # relative 2-norm vs FD at ε=1e-6
TOL_RECOVERY_Q = 1.0 - 1e-6  # q_j after Φ Φ^{-1} e_j
TOL_RECOVERY_INF = 1e-8


@pytest.fixture(scope="module")
def A():
    return grid_adjacency(LOCKS["side"])


def test_grid_adjacency_shape_and_degree(A):
    N = LOCKS["N"]
    assert A.shape == (N, N)
    assert np.allclose(np.diag(A), 0.0)
    degrees = A.sum(axis=1)
    assert np.allclose(degrees, 4.0)
    assert np.allclose(A, A.T)


def test_jacobian_row_sum_zero(A):
    theta = make_baseline(1)
    J = jacobian(theta, A, LOCKS["kappa"])
    assert np.allclose(J.sum(axis=1), 0.0, atol=1e-12)


@pytest.mark.parametrize("seed", [1, 5, 10])
def test_tangent_vs_finite_difference(seed, A):
    """Tangent integrator vs FD at ε=10^{-6} (DESIGN.md Arc 0)."""
    theta0 = make_baseline(seed)
    rng = np.random.default_rng(1000 + seed)
    u = rng.normal(size=LOCKS["N"])
    u /= np.linalg.norm(u)
    result = tangent_vs_finite_difference(
        theta0,
        u,
        LOCKS["T"],
        A,
        eps=LOCKS["fd_eps"],
        kappa=LOCKS["kappa"],
        omega=LOCKS["omega"],
        t0=LOCKS["t0"],
        rtol=LOCKS["rtol"],
        atol=LOCKS["atol"],
    )
    assert result["rel_2"] < TOL_FD_REL, (
        f"FD relative 2-error {result['rel_2']} >= {TOL_FD_REL} (seed={seed})"
    )


@pytest.mark.parametrize("seed", [1, 3, 7])
@pytest.mark.parametrize("j", list(LOCKS["requested_nodes"]))
def test_recovery_claim_a(seed, j, A):
    """u=Φ^{-1}e_j, propagate by Φ; q_j ≈ 1 and report κ₂(Φ)."""
    theta0 = make_baseline(seed)
    Phi, _ = fundamental_matrix(
        theta0,
        LOCKS["T"],
        A,
        kappa=LOCKS["kappa"],
        omega=LOCKS["omega"],
        t0=LOCKS["t0"],
        rtol=LOCKS["rtol"],
        atol=LOCKS["atol"],
    )
    out = recover_and_propagate(Phi, j)
    assert out["q_j"] >= TOL_RECOVERY_Q, (
        f"q_j={out['q_j']} < {TOL_RECOVERY_Q} (seed={seed}, j={j})"
    )
    assert out["err_inf"] < TOL_RECOVERY_INF, (
        f"||Φu - e_j||_∞={out['err_inf']} (seed={seed}, j={j})"
    )
    # κ₂ reported (finite, positive)
    assert out["kappa2"] > 0.0
    assert np.isfinite(out["kappa2"])


def test_energy_share_unit_vector():
    e = np.zeros(8)
    e[3] = 1.0
    assert energy_share(e, 3) == 1.0
    assert energy_share(e, 0) == 0.0


def test_phi_at_t0_is_identity(A):
    """Φ(t0,t0) should be I; integrate a tiny interval and check near-I start."""
    theta0 = make_baseline(2)
    # Integrate to very small T: Φ ≈ I + J T
    T_tiny = 1e-6
    Phi, _ = fundamental_matrix(theta0, T_tiny, A)
    J0 = jacobian(theta0, A, LOCKS["kappa"])
    approx = np.eye(LOCKS["N"]) + J0 * T_tiny
    assert np.max(np.abs(Phi - approx)) < 1e-8
