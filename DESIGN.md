# Addressable transients

Specify a future collective state. Construct the cause. Read a cheap meter.
Compose only after addressability is a claim that can fail.

This repository is a new record. It does not inherit questions, graphs,
datasets, statistics, figures, or conclusions from any other
oscillator-network programme.

**Status.** Review-0: accept with amendments (2026-09-07), amendments
1a–1e, 2a–2c, 3a–3c applied. Follow-up review (2026-09-07, later):
threshold justifications restated per use, S2 cutoffs given the same
treatment, combination rule written. Nothing in this document is an
established finding. Arc 0 harness work may proceed in parallel. No
Arc 1 number is a finding until the locks here have been implemented
as written.

---

## Review-0

**Verdict:** accept with amendments.

The first design treated a numerical identity as addressability
($x(T)=e^{MT}e^{-MT}x^\star$, one configuration, a meter that reads
the target). The revision moved that identity off a single-seed
pass/fail, but left two of three S1 controls and S2 Claim A as
identities dressed as measurements. The amendments below are the
minimum that makes each written number capable of being false.

Review text is the Review-0 note of 2026-09-07 (amendments 1a–1e,
2a–2c, 3a–3c). A later pass the same day required per-use cutoff
justifications and a combination rule; those are in the locks
tables, the $\sigma$ paragraph, and “Combination rule.” This file
is the applied form, not a pointer that requires the conversation
to exist.

---

## Question

Can a coupled-oscillator field be used as an addressed machine — not
trained, not decoded after the fact — by solving for the input that
produces a chosen state at a chosen time?

A computation, when one is attempted later, is a constructed map

```math
\text{symbols}
\xrightarrow{\text{inverse}}
\text{input}
\xrightarrow{\text{flow}}
\text{pattern}
\xrightarrow{\text{meter}}
\text{symbols}.
```

Composition (Arc 2) is blocked until Arc 1 pass rules, as amended
here, are met.

---

## Isolation

- New repository. Not a tenant on any existing research-control
  install.
- No imports from any retired dynamics package.
- Graphs are synthetic and named by construction.
- Literature allowed: Kuramoto; Budzinski, Busch, Mestern et al.,
  *Commun. Phys.* **7**, 239 (2024); Liboni, Budzinski, Busch et al.,
  *PNAS* **122**, e2321319121 (2025); standard ODE / matrix-exponential
  references.
- Disallowed in this record: findings, figures, node identifiers,
  stage names, and statistics from any retired programme. Sweep and
  single-configuration rules are stated as rules, not as inherited
  measurements.
- Seeds are locked. No retries. No substitution of a friendlier seed
  after seeing a meter.

---

## Substrates

Two substrates, same verbs: **target**, **inverse**, **meter**,
**compose**. They are not claimed to be the same physical system.

### S1 — complex-linear

State $x\in\mathbb{C}^N$,

```math
\dot x = Mx,\qquad
M = i\omega I + \varepsilon e^{-i\phi}A,\qquad
x(t)=e^{Mt}x(0),\qquad
x(0)=e^{-MT}x^\star.
```

Closed form. Superposition is legal. Amplitudes are registers.

**Coupling.** Distance-coupled ring, exponent $\alpha=1$,
row-normalised:

```math
d_{ij}=\min\bigl(|i-j|,\,N-|i-j|\bigr),\qquad
a_{ij}=\frac{d_{ij}^{-1}}{\sum_{k\neq i}d_{ik}^{-1}}\quad(i\neq j),\qquad
a_{ii}=0.
```

Budzinski et al. (2024) study distance-dependent rings with
$\alpha=1.0$, natural frequency $f=10\,\mathrm{Hz}$
($\omega=2\pi f$), and phase lag $\phi$ in an interval near
$\pi/2$. The integers locked below are this programme's instance in
that regime, not a claim that the paper specified them.

### S2 — real phases

State $\theta\in\mathbb{T}^N$,

```math
\dot\theta_i = \omega_i + \kappa\sum_j A_{ij}\sin(\theta_j-\theta_i).
```

Instantaneous routing matrix

```math
J_{ij}(\theta)
=
\begin{cases}
\kappa A_{ij}\cos(\theta_j-\theta_i) & i\neq j,\\
-\sum_{k\neq i}\kappa A_{ik}\cos(\theta_k-\theta_i) & i=j.
\end{cases}
```

Along a baseline $\theta(\tau)$,

```math
\dot\delta = J(\theta(\tau))\,\delta,\qquad
\delta(T)=\Phi(T,t_0)\,\delta(t_0),\qquad
u=\Phi(T,t_0)^{-1}\delta^\star.
```

Exact for the tangent. Finite-amplitude kicks are a later claim, not
Arc 1.

---

## Arc 0 — objects and oracles

No science. A number here that matches an identity is a passing
harness, not addressability.

### S1 numerical

- `evolve(x0, t)` against `scipy.linalg.expm`, complex128, on
  $N\in\{16,201\}$.
- `design_input(x_star, T)` satisfies
  $\lVert e^{MT}u-x^\star\rVert_\infty$ below $10^{-10}$ at the locked
  $T$.
- Meter of the recovered state at $T$ versus meter of $x^\star$:
  absolute difference below $10^{-8}$. This is the $T=T_\star$
  crossing rate, moved here per amendment 1a. Do not report it as the
  S1 primary.

### S2 numerical

- Tangent integrator versus finite difference at
  $\varepsilon=10^{-6}$.
- $\Phi(T,t_0)$ by integration of the fundamental matrix.
  Integrator: `scipy.integrate.solve_ivp`, RK45, `rtol=1e-8`,
  `atol=1e-8`.
- Recovery: $u=\Phi^{-1}e_j$, propagate by $\Phi$, report
  $q_j$ and $\kappa_2(\Phi)$ per eligible baseline. Claim A of
  the earlier note is this number (amendment 2b). It is not the
  S2 scientific claim.

---

## Locks that every Arc 1 number is conditioned on

None of these are inferred from a reproduction. Changing any of them
is a new design.

### S1 locks

| Quantity | Lock |
|---|---|
| $N$ | 201 |
| $\alpha$ | 1 |
| $\varepsilon$ | 50 |
| $\phi$ | 1.56 |
| $f$ | $10\,\mathrm{Hz}$, $\omega=2\pi f$ |
| Design time $T_\star$ | $3\,\mathrm{s}$ |
| Off-time $T_{\mathrm{off}}$ | $1.5\,\mathrm{s}$ |
| Cluster $C$ | indices $50,51,\ldots,149$ (100 nodes, 0-based) |
| Cluster phases | all $0$ |
| Out-of-cluster phases | i.i.d. uniform on $[0,2\pi)$ |
| Amplitudes, primary cell | i.i.d. uniform on $[1.5, 3.5)$ |
| Amplitude excursions | $[1.0, 1.5)$ and $[3.5, 4.0)$; see meter note |
| Wrong-switchboard $M'$ | same $\varepsilon,\phi,\omega,N$; distance-coupled ring with $\alpha=2$, same row-normalisation |
| Seeds | integers $1,\ldots,20$ inclusive |
| RNG | `numpy.random.default_rng(seed)` |
| Draw order | (1) $N-\lvert C\rvert$ out-of-cluster phases in index order; (2) $N$ amplitudes in index order $0\ldots N-1$. Cluster phases then overwritten to $0$. |
| Meter (primary) | amplitude-weighted order on $C$: $\displaystyle R_C(x)=\Bigl\lVert\frac{\sum_{j\in C}x_j}{\sum_{j\in C}\lvert x_j\rvert}\Bigr\rVert$ if the denominator is nonzero, else $0$ |
| Meter (reported diagnostic) | unweighted $R_C^{\mathrm{u}}(x)=\bigl\lVert\,\lvert C\rvert^{-1}\sum_{j\in C}e^{i\arg x_j}\bigr\rVert$ |
| Threshold $\sigma$ | $0.8$ (fire line; justification below, not in this cell) |

$\sigma=0.8$ is the meter's fire line: $R_C>\sigma$ means the
address bit is on. It is the same line at every time and under
every operator because the three S1 primaries ask whether that
same bit is on, not whether a random-phase null has been beaten.
Why $0.8$ rather than $0.3$: a fully aligned cluster has $R_C=1$;
$0.8$ is a high-coherence line, not a significance line. The
random-phase scale $1/\sqrt{\lvert C\rvert}=0.1$ only shows that
$0.8$ is far from an unstructured population. It does not, by
itself, justify the cutoff on $x(0)$, $x(T_{\mathrm{off}})$, or a
wrong-switchboard state. Those uses are earned in the paragraph
below. Chosen here, not inherited.

The primary meter is amplitude-weighted so that the amplitude cells
can enter the off-time reading. The $T=T_\star$ reading of a
phase-coherent cluster is still $\approx 1$ in both meters; that
reading is Arc 0, not the S1 primary. Excursion cells are reported
only for the off-time and wrong-switchboard rates, not as a
$T=T_\star$ story (amendment 1e).

**Why the same $\sigma$ on three non-random populations.**

- At $t=0$: $x(0)=e^{-MT_\star}x^\star$ is a deterministic
  function of the target. The check is not “is this unlike uniform
  phases?” It is “does the meter already call this a cluster?” If
  backward evolution leaves $R_C(x(0))>\sigma$, the cause *is*
  already the pattern and primary #2 fails. That is the intended
  failure, not a mismatch of null distributions.
- At $T_{\mathrm{off}}$: the check is whether the address bit is
  on at a time nobody asked for. Same bit, same line.
- Under $M'$: the check is whether a design computed from the
  wrong coupling still turns the bit on at $T_\star$ when run on
  the right coupling. Same bit, same line.

No pre-confirmatory sweep is used to move $\sigma$. If the
confirmatory rates sit on the knife-edge of $0.8$, the pass rules
are applied as written; $\sigma$ is not edited after seeing them.

### S2 locks

| Quantity | Lock |
|---|---|
| Graph | $16\times 16$ 4-neighbour grid, periodic, 256 nodes, row-major index $i=16r+c$ |
| $A$ | unweighted adjacency of that grid |
| $\kappa$ | $1.0$ |
| $\omega_i$ | $0$ (rotating frame) |
| Baseline law | i.i.d. uniform on $[0,2\pi)^{256}$ |
| Baseline seeds | integers $1,\ldots,10$ inclusive |
| RNG | `numpy.random.default_rng(seed)`, phases drawn in index order $0\ldots 255$ |
| $t_0$ | $0$ |
| $T$ | $1.0$ (dimensionless) |
| Requested nodes $j$ | $\{0,\;15,\;136,\;255\}$ — corner, opposite corner of the first row, interior, last index |
| Target perturbation | $\delta^\star=e_j$ (standard basis), one $j$ per trial |
| Energy share | $q_i(\delta)=\delta_i^2\big/\sum_k\delta_k^2$ if $\lVert\delta\rVert_2>0$, else $0$ |
| Control threshold $q_\star$ | $0.25$ (justification below) |
| Nonstationarity floor $c$ | $0.20$ (justification below) |
| Floor statistic | $\lVert J(\theta(T))-J(\theta(t_0))\rVert_F\big/\lVert J(\theta(t_0))\rVert_F$ |
| Frozen map | $\Phi_{\mathrm{fr}}=\exp\bigl(J(\theta(t_0))\,T\bigr)$ |
| Random control | i.i.d. real Gaussian vector, rescaled to $\lVert u\rVert_2$, independent stream `default_rng(10_000+seed)` |
| Integrator | as Arc 0 |

$q_\star=0.25$: on 256 nodes a uniform share is
$1/256\approx 0.0039$. A node holding $0.25$ has $\approx 64$ times
that share, equivalent to the target being one of at most four
equal-energy sites. That is the definition of “the requested node
was addressed” for a control that is supposed to miss. It is not a
random-phase calculation and is not borrowed from $\sigma$.

$c=0.20$: a global phase rotation leaves $J$ invariant, so the
floor statistic measures relative-phase rearrangement, not a drift
of the origin. $c=0.20$ means the routing matrix moved by a fifth
of its own Frobenius size: large enough that $\Phi_{\mathrm{fr}}$
and $\Phi$ are distinct operators, small enough that ordinary
mixing on a 4-regular grid can pass. Baselines below $c$ are not
evidence about a moving switchboard.

**Eligibility (amendment 2a).** A baseline seed is eligible for S2
only if its floor statistic is $\ge c$. Ineligible seeds are
excluded *before* any inverse is computed. The exclusion count is
reported. This is not seed substitution: the set $\{1,\ldots,10\}$
is not extended. If fewer than 6 of 10 are eligible, S2 Claim B is
**not evaluated** and the result is inconclusive for want of a moving
switchboard, not a refutation.

---

## Arc 1 — claims that can fail

### S1 — specificity to time and to this coupling

The inverse applied to a phase-coherent cluster target produces
$R_C(x(T_\star))\approx 1$ for every seed if the inverse is
numerically sound. That fact lives in Arc 0.

**Primary numbers (amendment 1b, 1c):**

1. **Off-time.** Fraction of seeds $1\ldots 20$ for which the
   designed input, evolved under $M$ ($\alpha=1$) to
   $T_{\mathrm{off}}=1.5$, has $R_C>\sigma$.
   Pass: $\le 4/20$.
2. **Cause is not already the pattern.** Fraction of seeds for which
   $R_C(x(0))\le\sigma$.
   Pass: $\ge 16/20$.
3. **Wrong switchboard.** Design $x(0)$ from $M'$ ($\alpha=2$),
   evolve under $M$ ($\alpha=1$) to $T_\star=3$, read $R_C$.
   Fraction with $R_C>\sigma$.
   Pass: $\le 4/20$.

All three are evaluated on the primary amplitude cell. Excursion
cells report (1) and (3) only.

**Reported, not used as pass (amendment 1c leftover):**

- Matched-norm random initial state (phases uniform, amplitudes
  matched in $\ell^2$ to the designed $x(0)$), evolved under
  $M$ to $T_\star$, rate $R_C>\sigma$.
- Unweighted meter on the same states.
- Constructor diagnostic: $R$ on a locked disjoint block
  $C'=\{0,\ldots,49\}\cup\{150,\ldots,199\}$ at $T_\star$.
  This measures the target constructor, not the dynamics.

If any of the three primary pass rules fails, S1 addressability is
not established at this instance. No rescue by seed or threshold.

### S2 — the time-ordered switchboard is what is inverted

Claim A is Arc 0 recovery plus $\kappa_2(\Phi)$. It is reported
per eligible baseline and per $j\in\{0,15,136,255\}$.

**Scientific numbers (amendment 2b), on eligible baselines only:**

1. **Random impulse.** $u_{\mathrm{rand}}$ of equal Euclidean
   norm to $u=\Phi^{-1}e_j$, evolved by $\Phi$. Fraction of
   (eligible seed, $j$) trials with $q_j\ge q_\star$.
   Pass: $\le 2/N_{\mathrm{trials}}$ where
   $N_{\mathrm{trials}}=N_{\mathrm{eligible}}\times 4$.
2. **Frozen $J(t_0)$.** $u_{\mathrm{fr}}=\Phi_{\mathrm{fr}}^{-1}e_j$,
   evolved by the true $\Phi$. Fraction with $q_j\ge q_\star$.
   Pass: $\le 2/N_{\mathrm{trials}}$.

These two are not folded. (1) can pass while (2) fails: addressable
as a linear map, but the snapshot Jacobian was a sufficient inverse.
(2) is the switchboard claim. A frozen success on an eligible
(moving) baseline is a real negative for that claim, not a
bookkeeping miss.

If $N_{\mathrm{eligible}}<6$, report the floor statistics and
stop. Do not draw extra seeds.

### Combination rule

There is no omnibus “addressability” verdict across substrates.
S1 and S2 are different machines.

- **S1 addressability** holds if and only if primaries #1, #2, and
  #3 all pass on the primary amplitude cell. One failure and S1
  addressability is not established.
- **S2 random-control claim** holds if and only if S2 scientific
  number (1) passes and $N_{\mathrm{eligible}}\ge 6$.
- **S2 switchboard claim** holds if and only if S2 scientific
  number (2) passes and $N_{\mathrm{eligible}}\ge 6$.
  These two S2 claims are not folded: (1) can hold without (2).
- $N_{\mathrm{eligible}}<6$ makes both S2 claims **inconclusive**,
  not false.
- Rates are compared to the integers as written. $5/20$ fails an
  $\le 4/20$ rule. There is no marginal band and no rounding.
- Excursion cells, unweighted meters, the disjoint-block diagnostic,
  and the matched-norm random S1 report do not enter any verdict.

---

## Arc 2 — blocked

Two designed inputs, added, one meter, a $2\times 2$ table.

- S1: addition is exact. Threshold $\sigma$ stays $0.8$. No
  Boolean operation in code.
- S2: addition in the tangent only. A finite-$\kappa$ repeat is a
  different claim, written later.

Not started until Arc 1 pass rules above are met and written as
such.

---

## Out of scope until 1–3 exist

Learning $W$ from data. Reconstructing images. Comparing graph
families on a classification score. Neuromorphic cost. Secrecy
claims. Finite-amplitude S2 composition.

---

## Implementation note

S1 may use a small local solver. A Fourier multiply on the circulant
ring is acceptable if Arc 0 shows agreement with `expm` at the
stated tolerance. Independence of any other repository's source is
required; copying a module with serial numbers filed off is not
independence.

S2 is a new integrator in this repository.
