"""16×16 periodic 4-neighbour grid adjacency (DESIGN.md S2 locks)."""

from __future__ import annotations

import numpy as np


def grid_adjacency(side: int = 16) -> np.ndarray:
    """Unweighted adjacency of a side×side 4-neighbour grid, periodic.

    Row-major index i = side*r + c.  A is real float64, zeros 0/1,
    symmetric, zero diagonal.
    """
    N = side * side
    A = np.zeros((N, N), dtype=np.float64)
    for r in range(side):
        for c in range(side):
            i = side * r + c
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                rr = (r + dr) % side
                cc = (c + dc) % side
                j = side * rr + cc
                A[i, j] = 1.0
    return A
