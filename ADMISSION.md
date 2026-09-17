# Admission — Arc 1 at the locked instance

**Date.** 2026-09-17  
**Authority.** `DESIGN.md` (canonical). Arc 0 judgment calls frozen in `FROZEN_ARC0.md` before any Arc 1 fraction.  
**Status.** Recorded negative. Arc 2 closed. No amplitude cell. No parameter hunt.

This file is the artefact. It does not reopen the design.

---

## What was run

Arc 0 harness: PASS (S1 and S2 oracles).  
Arc 1 claims: evaluated exactly as locked in `DESIGN.md`, combination rule as written.

Judgment calls that Arc 0 had to invent (S2 FD bound, N=16 target recipe, recovery numeric gates, meter modulus, phase wrap in FD) were frozen in `FROZEN_ARC0.md` **before** the first Arc 1 fraction. None were moved after rates landed.

---

## S1 — three lights, primary amplitude cell [1.5, 3.5)

| Light | Rate | Rule | Result |
|---|---|---|---|
| Off-time T = 1.5 | 0/20 | ≤ 4/20 | pass |
| Input not already the block | 20/20 | ≥ 16/20 | pass |
| Designed on M′ (α = 2), run on M (α = 1) | **9/20** | ≤ 4/20 | **fail** |

**S1 addressability: FALSE** at this setup.

One fail ends the claim. Excursion cells were not used as a rescue. No other amplitude cell was opened.

### Reading

S1 is invertible: the closed-form inverse recovers the target (Arc 0). It is **not coupling-specific** at these locks: an input designed on the α = 2 cousin still lights the meter on α = 1 in 9/20 seeds. Addressability here is \(e^{-MT}\), not a property of this ring’s switchboard. A later S1 specificity test, if ever wanted, needs an M′ that is not a stretched version of M (different topology or scrambled lag), as its own locked design — not a passenger on an S2 sequel.

---

## S2 — eligibility, then two lights

| Gate | Value |
|---|---|
| N_eligible | **10** (excluded = 0) |
| Floor | all ≥ 0.20 (actually ≫) |
| N_trials | 10 × 4 = 40 |

| Claim | Rate | Rule | Result |
|---|---|---|---|
| Random impulse | 0/40 (N_eligible=10) | ≤ 2/40 | **holds** |
| Frozen J(t₀) | **15/40** (N_eligible=10) | ≤ 2/40 | **fails** |

Not inconclusive (N_eligible ≥ 6). Claims not folded.

### Reading

Eligibility was already 10/10. J moved. The snapshot still won on 15/40 trials against q★ = 0.25.

The design wrote this negative in advance: random can pass while frozen fails, meaning the snapshot was a good enough inverse. That is what happened. “Make the board move more” is not a new question; it is the same question with a bigger shrug.

S2 at (κ = 1, T = 1, q★ = 0.25) on this grid is a good linear map from u to eⱼ. The time-ordered product is not necessary. Addressability here is \(J(t_0)^{-1}\), not a switchboard.

Claim A recovery and κ₂(Φ) remain Arc 0 diagnostics. A well-conditioned inverse was not sold as addressability.

---

## Combination-rule summary

- **S1 addressability:** not established (FALSE).
- **S2 random-control claim:** holds.
- **S2 switchboard claim:** fails.
- **Arc 2:** blocked; stays closed.
- **Amplitude grid:** not opened.

---

## What this record is not

- Not a finding that “oscillator addressability is impossible.”
- Not a licence to scan (κ, T) until frozen fails.
- Not a sequel. A sequel exists only if the **sentence** changes (see below), written before any run.

---

## Optional sequel (not minted)

Only if the programme still cares whether a switchboard exists **somewhere on this family**. The sequel is not “find parameters where frozen fails.” That is a hunt.

The sequel sentence:

> At a pre-specified (κ, T) where Φ and Φ_fr are both well-conditioned, does inverting the snapshot fail the q★ bar while inverting Φ still passes?

One cell, written before the run:

| Lock | Value | Why |
|---|---|---|
| Graph, seeds, four j, integrator | unchanged | not a new substrate |
| κ | 2.0 | more nonlinear accumulation than 1.0, not a scan |
| T | 3.0 | long enough that 𝒯 exp ∫J can leave exp(J₀ T) |
| q★, c | 0.25, 0.20 | do not move the meter after a miss |
| Extra gate | median κ₂(Φ) < 10⁶ and median κ₂(Φ_fr) < 10⁶ | ill-conditioned inverse is not a switchboard |
| Eligibility | still ≥ 6/10 | else inconclusive, same as Arc 1 |
| Pass | random ≤ 2/N_trials **and** frozen ≤ 2/N_trials **and** true-Φ recovery holds on the same trials | frozen must fail while Φ works |

If κ₂ blows up, that is not “time-order mattered.” If frozen still clears q★, the admission is repeated at a harder cell, and that is the end of S2 on this grid.

Do not reopen S1 inside that cell.

**This sequel is not locked until the programme says to mint it.** Until then, the artefact is the negative above.


---

## Decision

**2026-09-17.** Stop on this admission. The optional (κ = 2, T = 3) sequel is **not minted**. The negative above is the record.
