"""S1 Arc 1 scientific claims (DESIGN.md — claims that can fail).

Rates are compared to integers as written. No marginal band, no rounding,
no seed substitution. Excursion / diagnostic numbers do not enter the verdict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.linalg import expm

from .coupling import distance_coupled_ring
from .dynamics import build_M
from .meters import R_C, R_C_unweighted
from .targets import CLUSTER, LOCKS, make_target

# Locked disjoint block C' (constructor diagnostic)
C_PRIME = np.concatenate([np.arange(0, 50), np.arange(150, 200)]).astype(int)

EXCURSION_CELLS = (
    ("low", 1.0, 1.5),
    ("high", 3.5, 4.0),
)


@dataclass
class S1Arc1Result:
    n_seeds: int
    sigma: float
    # Primary counts (numerator of rate)
    off_time_fire: int
    cause_not_pattern: int  # count with R_C(x0) <= sigma
    wrong_sb_fire: int
    # Pass flags
    pass_off_time: bool
    pass_cause: bool
    pass_wrong_sb: bool
    s1_addressability: bool
    # Diagnostics (not in verdict)
    matched_norm_fire: int
    unweighted_off_time_fire: int
    unweighted_cause_ok: int
    unweighted_wrong_sb_fire: int
    cprime_at_Tstar_mean: float
    cprime_at_Tstar_fire: int
    excursions: dict[str, dict[str, Any]] = field(default_factory=dict)
    # Per-seed detail (optional inspection)
    per_seed: list[dict[str, float]] = field(default_factory=list)

    def rate_str(self, k: int) -> str:
        return f"{k}/{self.n_seeds}"


def _propagators():
    """Cache expm(±M t) and expm(-M' T★) once (circulant ring, N=201)."""
    N = LOCKS["N"]
    kw = dict(
        epsilon=LOCKS["epsilon"],
        phi=LOCKS["phi"],
        omega=LOCKS["omega"],
    )
    M = build_M(N, alpha=1.0, **kw)
    Mp = build_M(N, alpha=2.0, A=distance_coupled_ring(N, alpha=2.0), **kw)
    T = LOCKS["T_star"]
    T_off = LOCKS["T_off"]
    return {
        "M": M,
        "Mp": Mp,
        "exp_M_T": expm(M * T),
        "exp_mM_T": expm(-M * T),
        "exp_M_Toff": expm(M * T_off),
        "exp_mMp_T": expm(-Mp * T),
    }


def _matched_norm_random(x0: np.ndarray, seed: int) -> np.ndarray:
    """Phases uniform; state ℓ²-norm matched to designed x(0).

    Diagnostic-only RNG stream: default_rng(20_000 + seed). DESIGN.md does
    not lock this stream; 20_000+seed keeps it independent of target / S2
    random-control streams.
    """
    N = x0.size
    rng = np.random.default_rng(20_000 + seed)
    phases = rng.uniform(0.0, 2.0 * np.pi, size=N)
    x = np.exp(1j * phases).astype(np.complex128)
    n0 = np.linalg.norm(x0)
    n = np.linalg.norm(x)
    if n == 0.0:
        return x
    return x * (n0 / n)


def evaluate_amplitude_cell(
    amp_lo: float,
    amp_hi: float,
    props: dict,
    *,
    include_cause: bool,
    include_diagnostics: bool,
) -> dict[str, Any]:
    """Evaluate Arc 1 counts for one amplitude cell over seeds 1…20."""
    N = LOCKS["N"]
    sigma = LOCKS["sigma"]
    seeds = list(LOCKS["seeds"])
    n = len(seeds)

    off_fire = 0
    cause_ok = 0
    wrong_fire = 0
    matched_fire = 0
    uw_off = 0
    uw_cause = 0
    uw_wrong = 0
    cprime_vals: list[float] = []
    cprime_fire = 0
    per_seed: list[dict[str, float]] = []

    E_fwd_T = props["exp_M_T"]
    E_bwd_T = props["exp_mM_T"]
    E_fwd_off = props["exp_M_Toff"]
    E_bwd_Mp = props["exp_mMp_T"]

    for seed in seeds:
        x_star = make_target(seed, amp_lo=amp_lo, amp_hi=amp_hi)
        x0 = E_bwd_T @ x_star
        x_off = E_fwd_off @ x0
        x_wrong0 = E_bwd_Mp @ x_star
        x_wrong_T = E_fwd_T @ x_wrong0

        r_off = R_C(x_off, CLUSTER)
        r0 = R_C(x0, CLUSTER)
        r_wrong = R_C(x_wrong_T, CLUSTER)

        if r_off > sigma:
            off_fire += 1
        if include_cause and r0 <= sigma:
            cause_ok += 1
        if r_wrong > sigma:
            wrong_fire += 1

        row = {
            "seed": float(seed),
            "R_C_off": r_off,
            "R_C_x0": r0,
            "R_C_wrong": r_wrong,
        }

        if include_diagnostics:
            x_T = E_fwd_T @ x0  # should ≈ x_star
            r_cp = R_C(x_T, C_PRIME)
            cprime_vals.append(r_cp)
            if r_cp > sigma:
                cprime_fire += 1

            x_rand = _matched_norm_random(x0, seed)
            x_rand_T = E_fwd_T @ x_rand
            if R_C(x_rand_T, CLUSTER) > sigma:
                matched_fire += 1

            if R_C_unweighted(x_off, CLUSTER) > sigma:
                uw_off += 1
            if R_C_unweighted(x0, CLUSTER) <= sigma:
                uw_cause += 1
            if R_C_unweighted(x_wrong_T, CLUSTER) > sigma:
                uw_wrong += 1

            row["R_C_prime_T"] = r_cp
            row["R_Cu_off"] = R_C_unweighted(x_off, CLUSTER)
            row["R_Cu_x0"] = R_C_unweighted(x0, CLUSTER)
            row["R_Cu_wrong"] = R_C_unweighted(x_wrong_T, CLUSTER)

        per_seed.append(row)

    out: dict[str, Any] = {
        "n_seeds": n,
        "off_time_fire": off_fire,
        "wrong_sb_fire": wrong_fire,
        "per_seed": per_seed,
    }
    if include_cause:
        out["cause_not_pattern"] = cause_ok
    if include_diagnostics:
        out["matched_norm_fire"] = matched_fire
        out["unweighted_off_time_fire"] = uw_off
        out["unweighted_cause_ok"] = uw_cause
        out["unweighted_wrong_sb_fire"] = uw_wrong
        out["cprime_at_Tstar_mean"] = float(np.mean(cprime_vals)) if cprime_vals else 0.0
        out["cprime_at_Tstar_fire"] = cprime_fire
    return out


def run_s1_arc1() -> S1Arc1Result:
    """Compute all S1 Arc 1 primary / diagnostic / excursion numbers."""
    props = _propagators()
    sigma = LOCKS["sigma"]
    n = len(list(LOCKS["seeds"]))

    primary = evaluate_amplitude_cell(
        LOCKS["amp_primary"][0],
        LOCKS["amp_primary"][1],
        props,
        include_cause=True,
        include_diagnostics=True,
    )

    # Pass rules as written (integer comparison, no rounding)
    pass_off = primary["off_time_fire"] <= 4
    pass_cause = primary["cause_not_pattern"] >= 16
    pass_wrong = primary["wrong_sb_fire"] <= 4
    addressability = pass_off and pass_cause and pass_wrong

    excursions: dict[str, dict[str, Any]] = {}
    for name, lo, hi in EXCURSION_CELLS:
        cell = evaluate_amplitude_cell(
            lo, hi, props, include_cause=False, include_diagnostics=False
        )
        excursions[name] = {
            "amp_lo": lo,
            "amp_hi": hi,
            "off_time_fire": cell["off_time_fire"],
            "wrong_sb_fire": cell["wrong_sb_fire"],
            "off_time_rate": f"{cell['off_time_fire']}/{n}",
            "wrong_sb_rate": f"{cell['wrong_sb_fire']}/{n}",
        }

    return S1Arc1Result(
        n_seeds=n,
        sigma=sigma,
        off_time_fire=primary["off_time_fire"],
        cause_not_pattern=primary["cause_not_pattern"],
        wrong_sb_fire=primary["wrong_sb_fire"],
        pass_off_time=pass_off,
        pass_cause=pass_cause,
        pass_wrong_sb=pass_wrong,
        s1_addressability=addressability,
        matched_norm_fire=primary["matched_norm_fire"],
        unweighted_off_time_fire=primary["unweighted_off_time_fire"],
        unweighted_cause_ok=primary["unweighted_cause_ok"],
        unweighted_wrong_sb_fire=primary["unweighted_wrong_sb_fire"],
        cprime_at_Tstar_mean=primary["cprime_at_Tstar_mean"],
        cprime_at_Tstar_fire=primary["cprime_at_Tstar_fire"],
        excursions=excursions,
        per_seed=primary["per_seed"],
    )


def format_s1_arc1(r: S1Arc1Result) -> str:
    # Three lights on primary cell only. One FAIL → addressability FALSE.
    # Excursion cells are reported below; they do NOT enter the verdict
    # and must not be used as a rescue.
    verdict = "HOLDS" if r.s1_addressability else "FALSE (not established)"
    lines = [
        "=== S1 Arc 1 — three lights (primary amplitude cell [1.5, 3.5)) ===",
        f"  1. Off-time T=1.5              {r.rate_str(r.off_time_fire)}  "
        f"R_C>0.8  pass≤4/20: {'PASS' if r.pass_off_time else 'FAIL'}",
        f"  2. Input not already the block {r.rate_str(r.cause_not_pattern)}  "
        f"R_C(x0)≤0.8  pass≥16/20: {'PASS' if r.pass_cause else 'FAIL'}",
        f"  3. Designed on M' (α=2), run M {r.rate_str(r.wrong_sb_fire)}  "
        f"R_C>0.8 at T★  pass≤4/20: {'PASS' if r.pass_wrong_sb else 'FAIL'}",
        f"  S1 addressability: {verdict}",
        "  --- reported only (NOT in verdict; NOT a rescue) ---",
        f"  matched-norm random  {r.rate_str(r.matched_norm_fire)}  R_C>σ at T★",
        f"  unweighted off-time  {r.rate_str(r.unweighted_off_time_fire)}  R_C^u>σ",
        f"  unweighted cause≤σ   {r.rate_str(r.unweighted_cause_ok)}",
        f"  unweighted wrong-sb  {r.rate_str(r.unweighted_wrong_sb_fire)}  R_C^u>σ",
        f"  C' at T★             mean R={r.cprime_at_Tstar_mean:.4f}  "
        f"fire {r.rate_str(r.cprime_at_Tstar_fire)}",
        "  --- excursion cells: report (1),(3) only; do NOT enter verdict ---",
    ]
    for name, cell in r.excursions.items():
        lines.append(
            f"  [{name} amps [{cell['amp_lo']}, {cell['amp_hi']})]  "
            f"off-time {cell['off_time_rate']}  wrong-sb {cell['wrong_sb_rate']}"
        )
    return "\n".join(lines)
