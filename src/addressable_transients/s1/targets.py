"""Locked S1 target constructor (DESIGN.md S1 locks)."""

from __future__ import annotations

import numpy as np

# Cluster C: indices 50,51,...,149 (100 nodes, 0-based) — for N=201
CLUSTER = np.arange(50, 150, dtype=int)

LOCKS = {
    "N": 201,
    "alpha": 1.0,
    "epsilon": 50.0,
    "phi": 1.56,
    "f": 10.0,  # Hz
    "omega": 2.0 * np.pi * 10.0,
    "T_star": 3.0,  # s
    "T_off": 1.5,  # s
    "sigma": 0.8,
    "seeds": range(1, 21),
    "amp_primary": (1.5, 3.5),
}


def make_target(
    seed: int,
    *,
    N: int = LOCKS["N"],
    cluster: np.ndarray | None = None,
    amp_lo: float = 1.5,
    amp_hi: float = 3.5,
) -> np.ndarray:
    """Build x★ from locked draw order.

    Draw order (DESIGN.md)::
      (1) N-|C| out-of-cluster phases in index order;
      (2) N amplitudes in index order 0…N-1.
      Cluster phases then overwritten to 0.
    """
    if cluster is None:
        if N != LOCKS["N"]:
            raise ValueError(
                f"Default cluster is for N={LOCKS['N']}; pass cluster= for N={N}"
            )
        cluster = CLUSTER
    cluster = np.asarray(cluster, dtype=int)
    C_set = set(int(i) for i in cluster)
    out_of = np.array([i for i in range(N) if i not in C_set], dtype=int)

    rng = np.random.default_rng(seed)
    # (1) out-of-cluster phases in index order
    out_phases = rng.uniform(0.0, 2.0 * np.pi, size=out_of.size)
    # (2) N amplitudes in index order
    amplitudes = rng.uniform(amp_lo, amp_hi, size=N)

    phases = np.zeros(N, dtype=np.float64)
    phases[out_of] = out_phases
    # cluster phases overwritten to 0 (already zeros)

    x_star = amplitudes * np.exp(1j * phases)
    return x_star.astype(np.complex128)
