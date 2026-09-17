"""CLI: python -m addressable_transients — Arc 0 harness + Arc 1 claims."""

from __future__ import annotations

import argparse
import sys
import time
import traceback

import numpy as np

from addressable_transients.s1 import (
    CLUSTER,
    LOCKS as S1_LOCKS,
    R_C,
    build_M,
    design_input,
    distance_coupled_ring,
    evolve,
    make_target,
)
from addressable_transients.s1.arc1 import format_s1_arc1, run_s1_arc1
from addressable_transients.s2 import (
    LOCKS as S2_LOCKS,
    fundamental_matrix,
    grid_adjacency,
    recover_and_propagate,
    tangent_vs_finite_difference,
)
from addressable_transients.s2.arc1 import format_s2_arc1, run_s2_arc1
from addressable_transients.s2.tangent import make_baseline


def run_s1_arc0() -> bool:
    print("=== S1 Arc 0 ===")
    ok = True
    for N in (16, 201):
        A = distance_coupled_ring(N, alpha=1.0)
        M = build_M(
            N,
            epsilon=S1_LOCKS["epsilon"],
            phi=S1_LOCKS["phi"],
            omega=S1_LOCKS["omega"],
            alpha=1.0,
            A=A,
        )
        rng = np.random.default_rng(0)
        x0 = (rng.normal(size=N) + 1j * rng.normal(size=N)).astype(np.complex128)
        t = 0.37
        from scipy.linalg import expm

        err_ev = np.max(np.abs(evolve(x0, t, M) - expm(M * t) @ x0))
        status = "PASS" if err_ev < 1e-12 else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"  evolve vs expm  N={N}: {status}  (∞-err={err_ev:.3e})")

        T = S1_LOCKS["T_star"]
        if N == S1_LOCKS["N"]:
            x_star = make_target(1)
        else:
            amps = rng.uniform(1.5, 3.5, size=N)
            phases = rng.uniform(0.0, 2.0 * np.pi, size=N)
            x_star = (amps * np.exp(1j * phases)).astype(np.complex128)
        u = design_input(x_star, T, M)
        rec = evolve(u, T, M)
        err_rec = np.max(np.abs(rec - x_star))
        status = "PASS" if err_rec < 1e-10 else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"  design_input    N={N}: {status}  (∞-err={err_rec:.3e})")

    M = build_M(
        S1_LOCKS["N"],
        epsilon=S1_LOCKS["epsilon"],
        phi=S1_LOCKS["phi"],
        omega=S1_LOCKS["omega"],
        alpha=S1_LOCKS["alpha"],
    )
    T = S1_LOCKS["T_star"]
    meter_ok = True
    worst = 0.0
    for seed in (1, 7, 20):
        x_star = make_target(seed)
        x_T = evolve(design_input(x_star, T, M), T, M)
        diff = abs(R_C(x_T, CLUSTER) - R_C(x_star, CLUSTER))
        worst = max(worst, diff)
        if diff >= 1e-8:
            meter_ok = False
    status = "PASS" if meter_ok else "FAIL"
    if not meter_ok:
        ok = False
    print(f"  meter |Δ| < 1e-8:   {status}  (worst={worst:.3e})")
    print(f"S1 Arc 0: {'PASS' if ok else 'FAIL'}")
    return ok


def run_s2_arc0() -> bool:
    print("=== S2 Arc 0 ===")
    ok = True
    A = grid_adjacency(S2_LOCKS["side"])

    fd_ok = True
    worst_rel = 0.0
    for seed in (1, 5, 10):
        theta0 = make_baseline(seed)
        rng = np.random.default_rng(1000 + seed)
        u = rng.normal(size=S2_LOCKS["N"])
        u /= np.linalg.norm(u)
        r = tangent_vs_finite_difference(
            theta0, u, S2_LOCKS["T"], A, eps=S2_LOCKS["fd_eps"]
        )
        worst_rel = max(worst_rel, r["rel_2"])
        if r["rel_2"] >= 5e-3:
            fd_ok = False
    status = "PASS" if fd_ok else "FAIL"
    if not fd_ok:
        ok = False
    print(f"  tangent vs FD ε=1e-6: {status}  (worst rel2={worst_rel:.3e})")

    rec_ok = True
    worst_q = 1.0
    kappas = []
    for seed in (1, 3, 7):
        theta0 = make_baseline(seed)
        Phi, _ = fundamental_matrix(theta0, S2_LOCKS["T"], A)
        for j in S2_LOCKS["requested_nodes"]:
            out = recover_and_propagate(Phi, j)
            worst_q = min(worst_q, out["q_j"])
            kappas.append(out["kappa2"])
            if out["q_j"] < 1.0 - 1e-6 or out["err_inf"] >= 1e-8:
                rec_ok = False
    status = "PASS" if rec_ok else "FAIL"
    if not rec_ok:
        ok = False
    kappa_min = min(kappas) if kappas else float("nan")
    kappa_max = max(kappas) if kappas else float("nan")
    print(
        f"  recovery Claim A:    {status}  "
        f"(min q_j={worst_q:.6f}, κ₂∈[{kappa_min:.3e},{kappa_max:.3e}])"
    )
    print(f"S2 Arc 0: {'PASS' if ok else 'FAIL'}")
    return ok


def run_arc1() -> int:
    print("Addressable transients — Arc 1 scientific claims")
    print("Authority: DESIGN.md (locks + combination rule)\n")
    t0 = time.perf_counter()
    try:
        s1 = run_s1_arc1()
        print(format_s1_arc1(s1))
        t1 = time.perf_counter()
        print(f"  (S1 wall time: {t1 - t0:.2f}s)\n")

        s2 = run_s2_arc1()
        print(format_s2_arc1(s2))
        t2 = time.perf_counter()
        print(f"  (S2 wall time: {t2 - t1:.2f}s)")
        print(f"  (Arc 1 total wall time: {t2 - t0:.2f}s)\n")

        print("=== Combination rule verdicts ===")
        print(
            f"  S1 addressability:      "
            f"{'HOLDS' if s1.s1_addressability else 'FALSE (not established at this setup)'}"
        )
        print(f"  S2 random-control claim: {s2.random_control_claim}")
        print(f"  S2 switchboard claim:    {s2.switchboard_claim}")
        print("  (Excursions / Claim A / κ₂ do not enter these verdicts.)")
    except Exception:
        traceback.print_exc()
        return 1
    return 0


def run_arc0() -> int:
    print("Addressable transients — Arc 0 harness")
    print("Authority: DESIGN.md (Arc 0 objects and oracles)\n")
    try:
        s1 = run_s1_arc0()
        print()
        s2 = run_s2_arc0()
    except Exception:
        traceback.print_exc()
        print("\nArc 0: FAIL (exception)")
        return 1
    print()
    if s1 and s2:
        print("Arc 0 OVERALL: PASS")
        return 0
    print("Arc 0 OVERALL: FAIL")
    return 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Addressable transients Arc 0 / Arc 1")
    p.add_argument(
        "--arc",
        choices=("0", "1", "all"),
        default="all",
        help="Which arc(s) to run (default: all)",
    )
    args = p.parse_args(argv)
    rc = 0
    if args.arc in ("0", "all"):
        rc = run_arc0() or rc
        if args.arc == "all":
            print()
    if args.arc in ("1", "all"):
        rc = run_arc1() or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
