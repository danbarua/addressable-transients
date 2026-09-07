# Addressable transients

Specify a future collective state. Construct the cause. Read a cheap meter.
Compose only after addressability is a claim that can fail.

This repository is a new record. It does not inherit questions, graphs,
datasets, statistics, figures, or conclusions from any other
oscillator-network programme.

**Status.** Review-0 accepted this design with amendments (2026-09-07).
Amendments 1a–1e, 2a–2c, and 3a–3c are applied. A follow-up review
(2026-09-07, later) required three more changes. Each threshold now
has a justification at each place it is used. The S2 cutoffs have the
same treatment. The combination rule is written. Nothing in this
document is an established finding. Arc 0 harness work may proceed in
parallel. No Arc 1 number is a finding until the locks in this
document are implemented as written.

---

## Review-0

**Verdict:** accept with amendments.

The first design treated a numerical identity as addressability
($x(T)=e^{MT}e^{-MT}x^\star$, one configuration, a meter that reads
the target). The revision moved that identity off a single-seed
pass/fail. The revision left two of three S1 controls and S2 Claim A as
identities that looked like measurements. The amendments below are the
minimum that makes each written number able to be false.

The review text is the Review-0 note of 2026-09-07 (amendments 1a–1e,
2a–2c, 3a–3c). A later pass on the same day required a justification
for each cutoff at each use, and a combination rule. Those are in the
locks tables, the $\sigma$ paragraph, and "Combination rule". This file
is the applied form. It does not point to a conversation that must
exist.

---

## Question

Can a coupled-oscillator field be used as an addressed machine? The
machine is not trained. The machine is not decoded after the fact. The
method is to solve for the input that produces a chosen state at a
chosen time.

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

Composition (Arc 2) is blocked until the Arc 1 pass rules, as amended
in this document, are met.

---

## Isolation

- This is a new repository. It is not a tenant on any existing
  research-control install.
- Do not import from any retired dynamics package.
- Graphs are synthetic. Each graph is named by its construction.
- Permitted literature: Kuramoto; Budzinski, Busch, Mestern et al.,
  *Commun. Phys.* **7**, 239 (2024); Liboni, Budzinski, Busch et al.,
  *PNAS* **122**, e2321319121 (2025); standard ODE and
  matrix-exponential references.
- Not permitted in this record: findings, figures, node identifiers,
  stage names, and statistics from any retired programme. Sweep rules
  and single-configuration rules are stated as rules. They are not
  inherited measurements.
- Seeds are locked. Do not retry. Do not substitute a friendlier seed
  after you see a meter.

---

## Substrates

There are two substrates. They use the same verbs: **target**,
**inverse**, **meter**, **compose**. This document does not claim that
they are the same physical system.

### S1 — complex-linear

State $x\in\mathbb{C}^N$,

```math
\dot x = Mx,\qquad
M = i\omega I + \varepsilon e^{-i\phi}A,\qquad
x(t)=e^{Mt}x(0),\qquad
x(0)=e^{-MT}x^\star.
```

The solution is closed form. Superposition is permitted. Amplitudes
are registers.

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
that regime. This document does not claim that the paper specified
them.

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

This is exact for the tangent. Finite-amplitude kicks are a later
claim. They are not part of Arc 1.

---

## Arc 0 — objects and oracles

Arc 0 contains no science. A number here that matches an identity
shows that the harness passes. It does not show addressability.

### S1 numerical

- Check `evolve(x0, t)` against `scipy.linalg.expm`, complex128, on
  $N\in\{16,201\}$.
- Check that `design_input(x_star, T)` satisfies
  $\lVert e^{MT}u-x^\star\rVert_\infty$ below $10^{-10}$ at the locked
  $T$.
- Compare the meter of the recovered state at $T$ with the meter of
  $x^\star$. The absolute difference must be below $10^{-8}$. This is
  the $T=T_\star$ crossing rate. Amendment 1a moved it here. Do not
  report it as the S1 primary.

### S2 numerical

- Check the tangent integrator against finite difference at
  $\varepsilon=10^{-6}$.
- Compute $\Phi(T,t_0)$ by integration of the fundamental matrix.
  Integrator: `scipy.integrate.solve_ivp`, RK45, `rtol=1e-8`,
  `atol=1e-8`.
- Recovery: compute $u=\Phi^{-1}e_j$. Propagate by $\Phi$. Report
  $q_j$ and $\kappa_2(\Phi)$ for each eligible baseline. Claim A of
  the earlier note is this number (amendment 2b). It is not the S2
  scientific claim.

---

## Locks that every Arc 1 number is conditioned on

None of these locks is inferred from a reproduction. A change to any
lock is a new design.

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

$\sigma=0.8$ is the fire line of the meter. $R_C>\sigma$ means that
the address bit is on. The line is the same at every time and under
every operator. The reason is that the three S1 primaries ask the same
question: is that bit on? They do not ask whether the result beats a
random-phase null. Why $0.8$ and not $0.3$: a fully aligned cluster has
$R_C=1$. $0.8$ is a high-coherence line. It is not a significance
line. The random-phase scale $1/\sqrt{\lvert C\rvert}=0.1$ shows only
that $0.8$ is far from an unstructured population. That scale does not
justify the cutoff on $x(0)$, on $x(T_{\mathrm{off}})$, or on a
wrong-switchboard state. The paragraph below justifies those uses.
This programme chose $\sigma$ here. It did not inherit $\sigma$.

The primary meter is amplitude-weighted. This lets the amplitude cells
enter the off-time reading. The $T=T_\star$ reading of a
phase-coherent cluster is still $\approx 1$ in both meters. That
reading is Arc 0. It is not the S1 primary. Excursion cells are
reported only for the off-time rate and the wrong-switchboard rate.
They are not reported as a $T=T_\star$ story (amendment 1e).

**Why the same $\sigma$ on three non-random populations.**

- At $t=0$: $x(0)=e^{-MT_\star}x^\star$ is a deterministic
  function of the target. The check does not ask "is this unlike
  uniform phases?" The check asks "does the meter already call this a
  cluster?" If backward evolution leaves $R_C(x(0))>\sigma$, the
  cause is already the pattern, and primary #2 fails. That is the
  intended failure. It is not a mismatch of null distributions.
- At $T_{\mathrm{off}}$: the check asks whether the address bit is on
  at a time nobody asked for. Same bit, same line.
- Under $M'$: the check asks whether a design computed from the wrong
  coupling still turns the bit on at $T_\star$ when run on the right
  coupling. Same bit, same line.

No pre-confirmatory sweep is used to move $\sigma$. If the
confirmatory rates are at the edge of $0.8$, apply the pass rules as
written. Do not edit $\sigma$ after you see the rates.

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

$q_\star=0.25$: on 256 nodes, a uniform share is
$1/256\approx 0.0039$. A node that holds $0.25$ has $\approx 64$ times
that share. This is equivalent to the target being one of at most
four equal-energy sites. That is the definition of "the requested
node was addressed" for a control that is expected to miss. It is not
a random-phase calculation. It is not borrowed from $\sigma$.

$c=0.20$: a global phase rotation leaves $J$ unchanged. The floor
statistic therefore measures relative-phase rearrangement. It does
not measure a drift of the origin. $c=0.20$ means that the routing
matrix moved by one fifth of its own Frobenius size. This is large
enough that $\Phi_{\mathrm{fr}}$ and $\Phi$ are distinct operators.
This is small enough that ordinary mixing on a 4-regular grid can
pass. Baselines below $c$ are not evidence about a moving switchboard.

**Eligibility (amendment 2a).** A baseline seed is eligible for S2
only if its floor statistic is $\ge c$. Exclude ineligible seeds
*before* you compute any inverse. Report the exclusion count. This is
not seed substitution: the set $\{1,\ldots,10\}$ is not extended. If
fewer than 6 of 10 seeds are eligible, do **not** evaluate S2 Claim B.
The result is then inconclusive because there is no moving
switchboard. It is not a refutation.

---

## Arc 1 — claims that can fail

### S1 — specificity to time and to this coupling

If the inverse is numerically sound, the inverse applied to a
phase-coherent cluster target produces $R_C(x(T_\star))\approx 1$ for
every seed. That fact belongs to Arc 0.

**Primary numbers (amendments 1b, 1c):**

1. **Off-time.** Evolve the designed input under $M$ ($\alpha=1$) to
   $T_{\mathrm{off}}=1.5$. Report the fraction of seeds $1\ldots 20$
   with $R_C>\sigma$.
   Pass: $\le 4/20$.
2. **Cause is not already the pattern.** Report the fraction of seeds
   with $R_C(x(0))\le\sigma$.
   Pass: $\ge 16/20$.
3. **Wrong switchboard.** Design $x(0)$ from $M'$ ($\alpha=2$). Evolve
   under $M$ ($\alpha=1$) to $T_\star=3$. Read $R_C$. Report the
   fraction with $R_C>\sigma$.
   Pass: $\le 4/20$.

Evaluate all three on the primary amplitude cell. Excursion cells
report (1) and (3) only.

**Reported, not used as pass (amendment 1c leftover):**

- Matched-norm random initial state: phases uniform, amplitudes
  matched in $\ell^2$ to the designed $x(0)$. Evolve under $M$ to
  $T_\star$. Report the rate of $R_C>\sigma$.
- The unweighted meter on the same states.
- Constructor diagnostic: $R$ on a locked disjoint block
  $C'=\{0,\ldots,49\}\cup\{150,\ldots,199\}$ at $T_\star$. This
  measures the target constructor. It does not measure the dynamics.

If any one of the three primary pass rules fails, S1 addressability is
not established at this instance. Do not rescue the result by seed.
Do not rescue the result by threshold.

### S2 — the time-ordered switchboard is what is inverted

Claim A is Arc 0 recovery plus $\kappa_2(\Phi)$. Report it for each
eligible baseline and for each $j\in\{0,15,136,255\}$.

**Scientific numbers (amendment 2b), on eligible baselines only:**

1. **Random impulse.** Draw $u_{\mathrm{rand}}$ with the same
   Euclidean norm as $u=\Phi^{-1}e_j$. Evolve it by $\Phi$. Report the
   fraction of (eligible seed, $j$) trials with $q_j\ge q_\star$.
   Pass: $\le 2/N_{\mathrm{trials}}$ where
   $N_{\mathrm{trials}}=N_{\mathrm{eligible}}\times 4$.
2. **Frozen $J(t_0)$.** Compute
   $u_{\mathrm{fr}}=\Phi_{\mathrm{fr}}^{-1}e_j$. Evolve it by the true
   $\Phi$. Report the fraction with $q_j\ge q_\star$.
   Pass: $\le 2/N_{\mathrm{trials}}$.

Do not fold these two numbers. (1) can pass while (2) fails. That
outcome means the system is addressable as a linear map, but the
snapshot Jacobian was a sufficient inverse. (2) is the switchboard
claim. A frozen success on an eligible (moving) baseline is a real
negative for that claim. It is not a bookkeeping miss.

If $N_{\mathrm{eligible}}<6$, report the floor statistics and stop.
Do not draw extra seeds.

### Combination rule

There is no single "addressability" verdict across substrates. S1 and
S2 are different machines.

- **S1 addressability** holds if and only if primaries #1, #2, and #3
  all pass on the primary amplitude cell. One failure means that S1
  addressability is not established.
- **S2 random-control claim** holds if and only if S2 scientific
  number (1) passes and $N_{\mathrm{eligible}}\ge 6$.
- **S2 switchboard claim** holds if and only if S2 scientific number
  (2) passes and $N_{\mathrm{eligible}}\ge 6$. Do not fold these two
  S2 claims. (1) can hold without (2).
- $N_{\mathrm{eligible}}<6$ makes both S2 claims **inconclusive**. It
  does not make them false.
- Compare rates to the integers as written. $5/20$ fails a $\le 4/20$
  rule. There is no marginal band. There is no rounding.
- Excursion cells, unweighted meters, the disjoint-block diagnostic,
  and the matched-norm random S1 report do not enter any verdict.

---

## Arc 2 — blocked

Two designed inputs, added, one meter, a $2\times 2$ table.

- S1: addition is exact. Threshold $\sigma$ stays $0.8$. There is no
  Boolean operation in code.
- S2: addition in the tangent only. A finite-$\kappa$ repeat is a
  different claim. It is written later.

Do not start Arc 2 until the Arc 1 pass rules above are met and
written as met.

---

## Out of scope until 1–3 exist

Learning $W$ from data. Reconstructing images. Comparing graph
families on a classification score. Neuromorphic cost. Secrecy
claims. Finite-amplitude S2 composition.

---

## Implementation note

S1 may use a small local solver. A Fourier multiply on the circulant
ring is acceptable if Arc 0 shows agreement with `expm` at the stated
tolerance. The source must be independent of every other repository.
A module copied with the serial numbers filed off is not independent.

S2 is a new integrator in this repository.
