"""S1 Arc 0 oracles — fail if DESIGN.md tolerances are violated."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.linalg import expm

from addressable_transients.s1 import (
    CLUSTER,
    LOCKS,
    R_C,
    build_M,
    design_input,
    distance_coupled_ring,
    evolve,
    make_target,
)

TOL_RECOVERY_INF = 1e-10
TOL_METER = 1e-8


@pytest.fixture(scope="module")
def M201():
    return build_M(
        LOCKS["N"],
        epsilon=LOCKS["epsilon"],
        phi=LOCKS["phi"],
        omega=LOCKS["omega"],
        alpha=LOCKS["alpha"],
    )


@pytest.mark.parametrize("N", [16, 201])
def test_evolve_matches_expm(N):
    """evolve(x0, t) agrees with scipy.linalg.expm @ x0 (complex128)."""
    rng = np.random.default_rng(0)
    A = distance_coupled_ring(N, alpha=1.0)
    # Use locked ε,φ,ω for N=201; same physical params on N=16 for the oracle
    M = build_M(
        N,
        epsilon=LOCKS["epsilon"],
        phi=LOCKS["phi"],
        omega=LOCKS["omega"],
        alpha=1.0,
        A=A,
    )
    assert M.dtype == np.complex128
    x0 = (rng.normal(size=N) + 1j * rng.normal(size=N)).astype(np.complex128)
    t = 0.37
    x_ev = evolve(x0, t, M)
    x_ref = expm(M * t) @ x0
    assert x_ev.dtype == np.complex128
    assert np.max(np.abs(x_ev - x_ref)) < 1e-12


@pytest.mark.parametrize("N", [16, 201])
def test_design_input_recovery_inf(N):
    """‖e^{MT} u − x★‖_∞ < 10^{-10} at locked T (T★ for N=201; same T on N=16)."""
    T = LOCKS["T_star"]
    A = distance_coupled_ring(N, alpha=1.0)
    M = build_M(
        N,
        epsilon=LOCKS["epsilon"],
        phi=LOCKS["phi"],
        omega=LOCKS["omega"],
        alpha=1.0,
        A=A,
    )
    if N == LOCKS["N"]:
        x_star = make_target(1)
    else:
        # Minimal target for N=16 oracle (not a locked science target)
        rng = np.random.default_rng(1)
        amps = rng.uniform(1.5, 3.5, size=N)
        phases = rng.uniform(0.0, 2.0 * np.pi, size=N)
        x_star = (amps * np.exp(1j * phases)).astype(np.complex128)
    u = design_input(x_star, T, M)
    recovered = evolve(u, T, M)
    err = np.max(np.abs(recovered - x_star))
    assert err < TOL_RECOVERY_INF, f"recovery ∞-error {err} >= {TOL_RECOVERY_INF}"


@pytest.mark.parametrize("seed", [1, 7, 20])
def test_meter_recovered_vs_target(seed, M201):
    """Meter of recovered state at T★ vs meter of x★: abs diff < 10^{-8}."""
    T = LOCKS["T_star"]
    x_star = make_target(seed)
    u = design_input(x_star, T, M201)
    x_T = evolve(u, T, M201)
    m_star = R_C(x_star, CLUSTER)
    m_T = R_C(x_T, CLUSTER)
    diff = abs(m_T - m_star)
    assert diff < TOL_METER, f"meter |Δ|={diff} >= {TOL_METER} (seed={seed})"
    # Sanity: coherent cluster target should have R_C ≈ 1
    assert m_star > 0.99


def test_primary_meter_formula():
    """R_C matches the locked amplitude-weighted definition."""
    x = np.array([1.0 + 0j, 2.0 + 0j, 0.0 + 1j], dtype=np.complex128)
    C = np.array([0, 1], dtype=int)
    # sum x_j = 3, sum |x_j| = 3 → R_C = 1
    assert abs(R_C(x, C) - 1.0) < 1e-15
    C2 = np.array([0, 2], dtype=int)
    # sum = 1+i, |sum|=√2; denom = 1+1=2; R = √2/2
    assert abs(R_C(x, C2) - (np.sqrt(2) / 2)) < 1e-14


def test_ring_row_normalised():
    A = distance_coupled_ring(16, alpha=1.0)
    assert np.allclose(A.sum(axis=1), 1.0)
    assert np.allclose(np.diag(A), 0.0)
    # Circulant: each row is a cyclic shift of the first
    for i in range(1, 16):
        assert np.allclose(A[i], np.roll(A[0], i))


def test_draw_order_locked():
    """Seeds produce deterministic targets; cluster phases are 0."""
    x1 = make_target(1)
    x1b = make_target(1)
    x2 = make_target(2)
    assert np.array_equal(x1, x1b)
    assert not np.array_equal(x1, x2)
    assert np.allclose(np.angle(x1[CLUSTER]), 0.0, atol=1e-15)
    amps = np.abs(x1)
    assert np.all(amps >= 1.5) and np.all(amps < 3.5)
