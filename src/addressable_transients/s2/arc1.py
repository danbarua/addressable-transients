"""S2 Arc 1 scientific claims (DESIGN.md — time-ordered switchboard).

Eligibility before any inverse. No seed substitution. Random-control and
switchboard (frozen) claims are not folded. N_eligible < 6 → inconclusive.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
from scipy.linalg import expm, inv

from .graph import grid_adjacency
from .kuramoto import jacobian
from .tangent import (
    LOCKS,
    energy_share,
    floor_statistic,
    fundamental_matrix,
    make_baseline,
)

Verdict = Literal["HOLDS", "FAILS", "INCONCLUSIVE"]


@dataclass
class S2Arc1Result:
    n_baselines: int
    n_eligible: int
    n_excluded: int
    floor_stats: dict[int, float]
    eligible_seeds: list[int]
    n_trials: int
    random_hits: int
    frozen_hits: int
    pass_random: bool | None  # None if inconclusive
    pass_frozen: bool | None
    random_control_claim: Verdict
    switchboard_claim: Verdict
    # Claim A harness on eligible baselines (reported)
    claim_a: list[dict[str, Any]] = field(default_factory=list)
    trial_detail: list[dict[str, Any]] = field(default_factory=list)


def _random_control_u(u: np.ndarray, seed: int, draw_index: int) -> np.ndarray:
    """i.i.d. Gaussian, rescaled to ‖u‖₂; stream default_rng(10_000+seed).

    Draw order: for each eligible seed, j in locked order (0,15,136,255),
    one Gaussian vector is drawn (draw_index = 0..3).
    """
    rng = np.random.default_rng(10_000 + seed)
    # Advance through prior draws for this seed so each j is independent
    for _ in range(draw_index):
        rng.normal(size=u.size)
    g = rng.normal(size=u.size)
    nu = float(np.linalg.norm(u))
    ng = float(np.linalg.norm(g))
    if ng == 0.0:
        return np.zeros_like(u)
    return g * (nu / ng)


def run_s2_arc1() -> S2Arc1Result:
    """Eligibility filter, then random-impulse and frozen-J scientific numbers."""
    A = grid_adjacency(LOCKS["side"])
    kappa = LOCKS["kappa"]
    T = LOCKS["T"]
    t0 = LOCKS["t0"]
    c = LOCKS["c"]
    q_star = LOCKS["q_star"]
    nodes = list(LOCKS["requested_nodes"])
    seeds = list(LOCKS["baseline_seeds"])

    floor_stats: dict[int, float] = {}
    eligible: list[int] = []
    # Eligibility: floor statistic BEFORE any inverse
    for seed in seeds:
        theta0 = make_baseline(seed)
        # Need θ(T) for floor statistic — evolve nonlinearly (no Φ inverse yet)
        from .tangent import evolve_nonlinear

        theta_T = evolve_nonlinear(theta0, T, A, kappa=kappa, omega=LOCKS["omega"], t0=t0)
        fs = floor_statistic(theta0, theta_T, A, kappa)
        floor_stats[seed] = fs
        if fs >= c:
            eligible.append(seed)

    n_eligible = len(eligible)
    n_excluded = len(seeds) - n_eligible
    n_trials = n_eligible * len(nodes)

    if n_eligible < 6:
        return S2Arc1Result(
            n_baselines=len(seeds),
            n_eligible=n_eligible,
            n_excluded=n_excluded,
            floor_stats=floor_stats,
            eligible_seeds=eligible,
            n_trials=n_trials,
            random_hits=0,
            frozen_hits=0,
            pass_random=None,
            pass_frozen=None,
            random_control_claim="INCONCLUSIVE",
            switchboard_claim="INCONCLUSIVE",
        )

    random_hits = 0
    frozen_hits = 0
    claim_a: list[dict[str, Any]] = []
    trial_detail: list[dict[str, Any]] = []

    for seed in eligible:
        theta0 = make_baseline(seed)
        Phi, _ = fundamental_matrix(
            theta0, T, A, kappa=kappa, omega=LOCKS["omega"], t0=t0
        )
        J0 = jacobian(theta0, A, kappa)
        Phi_fr = expm(J0 * T)
        Phi_inv = inv(Phi)
        Phi_fr_inv = inv(Phi_fr)

        for draw_index, j in enumerate(nodes):
            e_j = np.zeros(LOCKS["N"], dtype=np.float64)
            e_j[j] = 1.0
            u = Phi_inv @ e_j

            # Claim A report (harness on eligible)
            delta_a = Phi @ u
            claim_a.append(
                {
                    "seed": seed,
                    "j": j,
                    "q_j": energy_share(delta_a, j),
                    "kappa2": float(np.linalg.cond(Phi, p=2)),
                }
            )

            # (1) Random impulse
            u_rand = _random_control_u(u, seed, draw_index)
            delta_rand = Phi @ u_rand
            q_rand = energy_share(delta_rand, j)
            hit_rand = q_rand >= q_star
            if hit_rand:
                random_hits += 1

            # (2) Frozen J(t0)
            u_fr = Phi_fr_inv @ e_j
            delta_fr = Phi @ u_fr
            q_fr = energy_share(delta_fr, j)
            hit_fr = q_fr >= q_star
            if hit_fr:
                frozen_hits += 1

            trial_detail.append(
                {
                    "seed": seed,
                    "j": j,
                    "q_rand": q_rand,
                    "q_frozen": q_fr,
                    "hit_rand": hit_rand,
                    "hit_frozen": hit_fr,
                    "norm_u": float(np.linalg.norm(u)),
                }
            )

    # Pass: ≤ 2 / N_trials (integer comparison)
    pass_random = random_hits <= 2
    pass_frozen = frozen_hits <= 2

    return S2Arc1Result(
        n_baselines=len(seeds),
        n_eligible=n_eligible,
        n_excluded=n_excluded,
        floor_stats=floor_stats,
        eligible_seeds=eligible,
        n_trials=n_trials,
        random_hits=random_hits,
        frozen_hits=frozen_hits,
        pass_random=pass_random,
        pass_frozen=pass_frozen,
        random_control_claim="HOLDS" if pass_random else "FAILS",
        switchboard_claim="HOLDS" if pass_frozen else "FAILS",
        claim_a=claim_a,
        trial_detail=trial_detail,
    )


def format_s2_arc1(r: S2Arc1Result) -> str:
    lines = [
        "=== S2 Arc 1 (eligible baselines only) ===",
        f"  baselines 1…10: eligible={r.n_eligible}  excluded={r.n_excluded}  "
        f"(floor ≥ c={LOCKS['c']})",
    ]
    fs_parts = [f"{s}:{r.floor_stats[s]:.3f}" for s in sorted(r.floor_stats)]
    lines.append(f"  floor stats: {', '.join(fs_parts)}")
    lines.append(f"  eligible seeds: {r.eligible_seeds}")

    if r.random_control_claim == "INCONCLUSIVE":
        lines.append(
            f"  N_eligible={r.n_eligible} < 6 → both S2 claims INCONCLUSIVE "
            "(no extra seeds drawn)"
        )
        lines.append(f"  S2 random-control claim: INCONCLUSIVE")
        lines.append(f"  S2 switchboard claim:    INCONCLUSIVE")
        return "\n".join(lines)

    n = r.n_trials
    ne = r.n_eligible
    # N_eligible on the SAME line as each fraction (denominator moves with eligibility)
    lines.append(
        f"  1. Random impulse  {r.random_hits}/{n}  "
        f"(N_eligible={ne}, N_trials={ne}×4)  "
        f"q_j≥0.25  pass≤2/{n}: {'PASS' if r.pass_random else 'FAIL'}"
    )
    lines.append(
        f"  2. Frozen J(t0)    {r.frozen_hits}/{n}  "
        f"(N_eligible={ne}, N_trials={ne}×4)  "
        f"q_j≥0.25  pass≤2/{n}: {'PASS' if r.pass_frozen else 'FAIL'}"
    )
    lines.append(
        "  (Claim A recovery / κ₂(Φ) are Arc 0 harness diagnostics — NOT science)"
    )
    lines.append(f"  S2 random-control claim: {r.random_control_claim}")
    lines.append(f"  S2 switchboard claim:    {r.switchboard_claim}")
    return "\n".join(lines)
