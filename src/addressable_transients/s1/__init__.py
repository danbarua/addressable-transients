"""S1 — complex-linear substrate (Arc 0 / Arc 1)."""

from .coupling import distance_coupled_ring
from .dynamics import build_M, design_input, evolve
from .meters import R_C, R_C_unweighted
from .targets import CLUSTER, LOCKS, make_target

__all__ = [
    "CLUSTER",
    "LOCKS",
    "R_C",
    "R_C_unweighted",
    "build_M",
    "design_input",
    "distance_coupled_ring",
    "evolve",
    "make_target",
]
