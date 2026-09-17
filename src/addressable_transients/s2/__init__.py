"""S2 — Kuramoto phases on a periodic grid (Arc 0 / Arc 1)."""

from .graph import grid_adjacency
from .kuramoto import jacobian, kuramoto_rhs
from .tangent import (
    LOCKS,
    condition_number_2,
    energy_share,
    fundamental_matrix,
    recover_and_propagate,
    tangent_vs_finite_difference,
)

__all__ = [
    "LOCKS",
    "condition_number_2",
    "energy_share",
    "fundamental_matrix",
    "grid_adjacency",
    "jacobian",
    "kuramoto_rhs",
    "recover_and_propagate",
    "tangent_vs_finite_difference",
]
