# Frozen Arc 0 judgment calls

These were fixed **before** any Arc 1 fraction existed. They must not move
after a rate comes in. If they move, that rate is not the design's rate.

| Call | Freeze |
|---|---|
| S2 FD bound | relative 2-norm `< 5e-3` (observed ~1e-6) |
| N=16 target recipe | same `(ε,φ,ω,T★)`; non-locked RNG target for identity oracle only |
| S2 recovery pass (Claim A harness) | `q_j ≥ 1 − 1e-6` and `‖Φu − e_j‖_∞ < 1e-8` |
| Meter modulus | `R_C = \| (∑_{j∈C} x_j) / (∑_{j∈C} \|x_j\|) \|` |
| Phase wrap in FD | `np.angle(exp(i·raw)) / ε` before comparing to Φu |

Claim A recovery and `κ₂(Φ)` remain Arc 0 / diagnostic only. They are not
S2 addressability.
