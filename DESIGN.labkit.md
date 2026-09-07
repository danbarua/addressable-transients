# Addressable transients — the design, as a record

The same design as `DESIGN.md`, written as the record it becomes. Every
heading below names the act that puts that section on the record and the
fields the act takes. Names in `code` — `S1`, `harness-S1`, `P2` — are
this document's, for cross-reference; the record mints its own ids when
the act is recorded, and those are what later acts name.

Specify a future collective state. Construct the cause. Read a cheap
meter. Compose only after addressability is a claim that can fail.

Nothing here is an established finding. The document says what will be
asked, how, what it will be held to, and what waits on what. Findings
arrive as acts under "What running it puts on the record".

---

## The question — `pose`

> Can a coupled-oscillator field be used as an addressed machine — not
> trained, not decoded after the fact — by solving for the input that
> produces a chosen state at a chosen time?

One question. It is *untested* until something has been run against it,
and pursuing it does not change that.

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

---

## Two lines of enquiry — `pursue <question> --approach`

Two substrates, same verbs: **target**, **inverse**, **meter**,
**compose**. They are not claimed to be the same physical system, so
they are two pursuits of one question, and nothing later folds them.

### `S1` — complex-linear

**Approach.** State $x\in\mathbb{C}^N$,

```math
\dot x = Mx,\qquad
M = i\omega I + \varepsilon e^{-i\phi}A,\qquad
x(t)=e^{Mt}x(0),\qquad
x(0)=e^{-MT}x^\star.
```

Closed form. Superposition is legal. Amplitudes are registers.
Distance-coupled ring, exponent $\alpha=1$, row-normalised:

```math
d_{ij}=\min\bigl(|i-j|,\,N-|i-j|\bigr),\qquad
a_{ij}=\frac{d_{ij}^{-1}}{\sum_{k\neq i}d_{ik}^{-1}}\quad(i\neq j),\qquad
a_{ii}=0.
```

Budzinski et al. (2024) study distance-dependent rings with
$\alpha=1.0$, $f=10\,\mathrm{Hz}$ ($\omega=2\pi f$), and phase lag
$\phi$ near $\pi/2$. The integers locked below are this programme's
instance in that regime, not a claim that the paper specified them.

### `S2` — real phases

**Approach.** State $\theta\in\mathbb{T}^N$,

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

Exact for the tangent. Finite-amplitude kicks are a later claim, and a
later pursuit.

---

## What is fixed before anything runs — `note --on`

A note is dated and attributed and constrains nothing by itself. What
makes a lock binding is the condition `L1`/`L2` below, which every
Arc 1 analysis is held to. **A changed lock is a new pursuit of the
question**, recorded with `pursue` and a new approach — never an edit to
the note, which is what the note was written to make impossible.

### On the question: isolation

New repository. Not a tenant on any existing research-control install.
No imports from any retired dynamics package. Graphs are synthetic and
named by construction. Literature allowed: Kuramoto; Budzinski, Busch,
Mestern et al., *Commun. Phys.* **7**, 239 (2024); Liboni, Budzinski,
Busch et al., *PNAS* **122**, e2321319121 (2025); standard ODE /
matrix-exponential references. Disallowed in this record: findings,
figures, node identifiers, stage names, and statistics from any retired
programme. Independence of any other repository's source is required;
copying a module with serial numbers filed off is not independence.

### On the question: Review-0

Verdict: accept with amendments 1a–1e, 2a–2c, 3a–3c (2026-09-07), and
a later pass the same day requiring per-use cutoff justifications and a
combination rule. The first design treated a numerical identity as
addressability ($x(T)=e^{MT}e^{-MT}x^\star$, one configuration, a meter
that reads the target). The revision moved that identity off a
single-seed pass/fail but left two of three S1 controls and S2 Claim A
as identities dressed as measurements. Every condition below is the
applied, amended wording. A condition amended after work has begun is
recorded with `amend`, citing what prompted it — not by editing this
file.

### On `S1`: locks

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
| Amplitude excursions | $[1.0, 1.5)$ and $[3.5, 4.0)$ |
| Wrong-switchboard $M'$ | same $\varepsilon,\phi,\omega,N$; distance-coupled ring with $\alpha=2$, same row-normalisation |
| Seeds | integers $1,\ldots,20$ inclusive |
| RNG | `numpy.random.default_rng(seed)` |
| Draw order | (1) $N-\lvert C\rvert$ out-of-cluster phases in index order; (2) $N$ amplitudes in index order $0\ldots N-1$. Cluster phases then overwritten to $0$. |
| Meter (primary) | amplitude-weighted order on $C$: $\displaystyle R_C(x)=\Bigl\lVert\frac{\sum_{j\in C}x_j}{\sum_{j\in C}\lvert x_j\rvert}\Bigr\rVert$ if the denominator is nonzero, else $0$ |
| Meter (reported diagnostic) | unweighted $R_C^{\mathrm{u}}(x)=\bigl\lVert\,\lvert C\rvert^{-1}\sum_{j\in C}e^{i\arg x_j}\bigr\rVert$ |
| Threshold $\sigma$ | $0.8$ |

$\sigma=0.8$ is the meter's fire line: $R_C>\sigma$ means the address
bit is on. It is the same line at every time and under every operator
because the three S1 primaries ask whether that same bit is on, not
whether a random-phase null has been beaten. A fully aligned cluster has
$R_C=1$; $0.8$ is a high-coherence line, not a significance line. The
random-phase scale $1/\sqrt{\lvert C\rvert}=0.1$ only shows that $0.8$
is far from an unstructured population; it does not by itself justify
the cutoff on $x(0)$, $x(T_{\mathrm{off}})$, or a wrong-switchboard
state. Those uses:

- At $t=0$: $x(0)=e^{-MT_\star}x^\star$ is a deterministic function of
  the target. The check is not "is this unlike uniform phases?" but
  "does the meter already call this a cluster?" If backward evolution
  leaves $R_C(x(0))>\sigma$, the cause *is* already the pattern and
  `P2` fails. That is the intended failure.
- At $T_{\mathrm{off}}$: whether the address bit is on at a time nobody
  asked for. Same bit, same line.
- Under $M'$: whether a design computed from the wrong coupling still
  turns the bit on at $T_\star$ when run on the right coupling. Same
  bit, same line.

The primary meter is amplitude-weighted so the amplitude cells can enter
the off-time reading. The $T=T_\star$ reading of a phase-coherent
cluster is $\approx 1$ in both meters; that reading is the harness, not
a primary. Excursion cells are reported for `P1` and `P3` only.

No pre-confirmatory sweep moves $\sigma$. If the confirmatory rates sit
on the knife-edge of $0.8$, the conditions are applied as written.

### On `S2`: locks

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
| Control threshold $q_\star$ | $0.25$ |
| Nonstationarity floor $c$ | $0.20$ |
| Floor statistic | $\lVert J(\theta(T))-J(\theta(t_0))\rVert_F\big/\lVert J(\theta(t_0))\rVert_F$ |
| Frozen map | $\Phi_{\mathrm{fr}}=\exp\bigl(J(\theta(t_0))\,T\bigr)$ |
| Random control | i.i.d. real Gaussian vector, rescaled to $\lVert u\rVert_2$, independent stream `default_rng(10_000+seed)` |
| Integrator | `scipy.integrate.solve_ivp`, RK45, `rtol=1e-8`, `atol=1e-8` |

$q_\star=0.25$: on 256 nodes a uniform share is $1/256\approx 0.0039$.
A node holding $0.25$ has $\approx 64$ times that share, equivalent to
the target being one of at most four equal-energy sites. That is the
definition of "the requested node was addressed" for a control that is
supposed to miss. Not a random-phase calculation; not borrowed from
$\sigma$.

$c=0.20$: a global phase rotation leaves $J$ invariant, so the floor
statistic measures relative-phase rearrangement, not a drift of the
origin. $c=0.20$ means the routing matrix moved by a fifth of its own
Frobenius size: large enough that $\Phi_{\mathrm{fr}}$ and $\Phi$ are
distinct operators, small enough that ordinary mixing on a 4-regular
grid can pass. Baselines below $c$ are not evidence about a moving
switchboard.

Eligibility is computed *before* any inverse; ineligible seeds are
excluded and the exclusion count reported. The set $\{1,\ldots,10\}$ is
never extended.

---

## The conditions results are held to — `criterion`

Stated now, before any number exists, so that a check nobody ran still
counts against the finding it qualifies. Each is one sentence a check
can pass or fail. Rates are compared to the integers as written: $5/20$
fails a $\le 4/20$ rule; no marginal band, no rounding.

**Harness, S1** — what `harness-S1` must show before `arc1-S1` runs:

- `H1a` — `evolve(x0, t)` agrees with `scipy.linalg.expm` in complex128
  on $N\in\{16,201\}$.
- `H1b` — `design_input(x_star, T)` satisfies
  $\lVert e^{MT}u-x^\star\rVert_\infty<10^{-10}$ at $T=T_\star$.
- `H1c` — the meter of the recovered state at $T_\star$ and the meter of
  $x^\star$ differ by less than $10^{-8}$ in absolute value.

`H1c` is the $T=T_\star$ crossing rate (amendment 1a). It is a harness
check, and it is never reported as an S1 primary.

**Harness, S2** — what `harness-S2` must show before `arc1-S2` runs:

- `H2a` — the tangent integrator agrees with finite difference at
  $\varepsilon=10^{-6}$.
- `H2b` — $\Phi(T,t_0)$ is obtained by integrating the fundamental
  matrix with the locked integrator, and $u=\Phi^{-1}e_j$ propagated by
  $\Phi$ recovers $e_j$ to integrator tolerance.

**Locks** — what every Arc 1 analysis is held to:

- `L1` — the S1 analysis was run under the S1 locks exactly as noted:
  seeds $1\ldots 20$ inclusive, none dropped or added, $\sigma=0.8$,
  the primary amplitude cell for every primary.
- `L2` — the S2 analysis was run under the S2 locks exactly as noted:
  seeds $1\ldots 10$, eligibility decided by the floor statistic before
  any inverse, exclusion count reported, no seed added.

**S1 primaries** (amendments 1b, 1c) — on the primary amplitude cell:

- `P1` **Off-time.** Of seeds $1\ldots 20$, at most $4$ have
  $R_C>\sigma$ when the designed input is evolved under $M$
  ($\alpha=1$) to $T_{\mathrm{off}}=1.5$.
- `P2` **Cause is not already the pattern.** Of seeds $1\ldots 20$, at
  least $16$ have $R_C(x(0))\le\sigma$.
- `P3` **Wrong switchboard.** Of seeds $1\ldots 20$, at most $4$ have
  $R_C>\sigma$ at $T_\star=3$ when $x(0)$ is designed from $M'$
  ($\alpha=2$) and evolved under $M$ ($\alpha=1$).

**S2 eligibility** (amendment 2a):

- `E` — at least $6$ of the $10$ baseline seeds have floor statistic
  $\ge c$.

**S2 scientific numbers** (amendment 2b) — on eligible baselines only,
$N_{\mathrm{trials}}=N_{\mathrm{eligible}}\times 4$:

- `R` **Random impulse.** At most $2$ of $N_{\mathrm{trials}}$
  (eligible seed, $j$) trials reach $q_j\ge q_\star$ when
  $u_{\mathrm{rand}}$, of equal Euclidean norm to $u=\Phi^{-1}e_j$, is
  evolved by $\Phi$.
- `F` **Frozen $J(t_0)$.** At most $2$ of $N_{\mathrm{trials}}$ trials
  reach $q_j\ge q_\star$ when
  $u_{\mathrm{fr}}=\Phi_{\mathrm{fr}}^{-1}e_j$ is evolved by the true
  $\Phi$.

`R` and `F` are never folded. `R` can pass while `F` fails: addressable
as a linear map, but the snapshot Jacobian was a sufficient inverse.
`F` is the switchboard claim; a frozen success on an eligible baseline
is a real negative for it, not a bookkeeping miss.

---

## What waits on what — `declare --governed-by --protecting --consequence`

A gate is satisfied when every condition governing it has a standing
pass; it holds its work while any is unchecked, and blocks it when one
has failed. It is computed from the evaluations and never set.

- `gate-arc1-S1` — governed by `H1a H1b H1c`; protecting `arc1-S1`.
  Consequence: *no S1 primary is run until the S1 harness reproduces
  the identity at the stated tolerances; an Arc 1 number from an
  unverified harness is not a number.*
- `gate-arc1-S2` — governed by `H2a H2b`; protecting `arc1-S2`.
  Consequence: *no S2 scientific number is run until the tangent
  integrator and $\Phi$ are verified.*
- `gate-arc2` — governed by `L1 L2 P1 P2 P3 E R F`; protecting `arc2`.
  Consequence: *composition is not started until every Arc 1 condition
  has been evaluated and passed, under the locks as written.*

The gate is the whole of the combination rule as far as Arc 2 is
concerned: all of them, or nothing. Which *claims* a set of passes earns
is a matter of conclusions, below, and is narrower than the gate.

---

## The work — `plan --objective --acceptance --may-read --enquiry`

- `harness-S1` — advances `S1`.
  **Objective:** objects and oracles for S1; no science. Implement
  `evolve(x0, t)` and `design_input(x_star, T)` and the two meters. A
  small local solver, or a Fourier multiply on the circulant ring, is
  acceptable if it agrees with `expm` at the stated tolerance.
  **Acceptance:** `H1a`, `H1b`, `H1c` each evaluated and passed, citing
  the harness's own numbers. **May read:** the S1 locks note; nothing
  from any other repository.

- `harness-S2` — advances `S2`.
  **Objective:** a new tangent integrator and fundamental-matrix solver
  in this repository; no science. **Acceptance:** `H2a`, `H2b` evaluated
  and passed; $q_j$ and $\kappa_2(\Phi)$ reported per baseline and per
  $j$ as an observation — Claim A of the earlier note is that report,
  and it is not an S2 scientific claim. **May read:** the S2 locks note.

- `arc1-S1` — advances `S1`; behind `gate-arc1-S1`.
  **Objective:** the three S1 primaries on the primary amplitude cell,
  seeds $1\ldots 20$. **Acceptance:** one analysis, held to
  `L1 P1 P2 P3`, reporting the three rates; `P1` and `P3` additionally
  on both excursion cells; and, reported without entering any verdict,
  the matched-norm random initial state (phases uniform, amplitudes
  matched in $\ell^2$ to the designed $x(0)$) evolved to $T_\star$, the
  unweighted meter on every state above, and the constructor diagnostic
  $R$ on the disjoint block $C'=\{0,\ldots,49\}\cup\{150,\ldots,199\}$
  at $T_\star$. **May read:** `harness-S1`'s outputs; the S1 locks note.

- `arc1-S2` — advances `S2`; behind `gate-arc1-S2`.
  **Objective:** eligibility, then `R` and `F` on eligible baselines.
  **Acceptance:** the floor statistic per baseline as an observation and
  `E` evaluated from it before any inverse is computed; if `E` passes,
  one analysis held to `L2 R F` reporting both rates and $\kappa_2(\Phi)$
  per eligible baseline and per $j$; if `E` fails, the floor statistics
  and nothing else. **May read:** `harness-S2`'s outputs; the S2 locks
  note.

- `arc2` — behind `gate-arc2`; advances no line of enquiry yet.
  **Objective:** two designed inputs, added, one meter, a $2\times 2$
  table. S1: addition is exact, $\sigma$ stays $0.8$, no Boolean
  operation in code. S2: addition in the tangent only; a finite-$\kappa$
  repeat is a different claim and a different pursuit. **Acceptance:**
  written when Arc 1 has been written up, and not before — which
  substrate composes is what Arc 1 decides. When it starts it gets its
  own question, `open`ed then.

Out of scope until the three arcs exist, and so not planned: learning
$W$ from data; reconstructing images; comparing graph families on a
classification score; neuromorphic cost; secrecy claims;
finite-amplitude S2 composition.

---

## What running it puts on the record

The acts, in the order the gates allow them. None has happened.

**Arc 0.** `observe` the harness numbers under `S1` and `S2`, with a
hash of the run. `analyse` the comparison against the oracle,
`--implementing harness-S1 --held-to H1a H1b H1c`, and `conclude` what
it found. `evaluate` each of `H1a H1b H1c --gate gate-arc1-S1 --citing`
the conclusion. Same for S2. When the harness gates are satisfied,
`arc1-S1` and `arc1-S2` leave *waiting* and become ready.

**Arc 1, S1.** One `analyse --implementing arc1-S1 --held-to L1 P1 P2 P3
--from` the harness outputs. Three `conclude`s, one per primary, each
stating the rate and whether it *supports* or *challenges* the
proposition that S1 is addressable at this instance. `evaluate` each of
`P1 P2 P3 --gate gate-arc2 --citing` its conclusion, and `L1` citing the
analysis. If all three pass, `synthesise` **S1 addressability holds at
this instance** `--resting-on` the three conclusions. If any fails, no
synthesis: the challenging conclusion is the answer, and `close S1
--answered-by` it closes the pursuit answered *no*. No rescue by seed or
threshold — `L1` is what a rescue would fail.

**Arc 1, S2.** `observe` the floor statistics; `evaluate E --gate
gate-arc2 --citing` them. If `E` fails: `R` and `F` are never run and
stay *never-run* on `gate-arc2`, and `accept S2 --until` *a baseline
law under which at least 6 of 10 seeds move the switchboard by $\ge c$*
`--in-light-of` the eligibility finding. The record then says
**inconclusive for want of a moving switchboard**, in its own bucket,
never *refuted* and never *unresolved*. If `E` passes: one `analyse
--held-to L2 R F`, two `conclude`s — the random-control claim and the
switchboard claim, two findings, never one — and `evaluate R`, `F`,
`L2`. Nothing synthesises across `R` and `F`.

**No omnibus claim.** Nothing synthesises across `S1` and `S2`. Two
machines, two pursuits, two answers.

**Arc 2.** `gate-arc2` is satisfied only when all eight conditions have
standing passes. Then `open` the composition question, `pursue` it per
substrate that earned it, and write `arc2`'s acceptance.

---

## What the record cannot say, and what stands in

- **Lock values are prose.** A note holds the table; nothing queries
  $\varepsilon=50$ as a number. What makes it binding is `L1`/`L2`, a
  check a person performs by reading the analysis against the note.
- **"Inconclusive" is not a verdict a condition can return.** A
  condition passes or fails. The design's third outcome for S2 — not
  evaluated, for want of eligible baselines — is an *act*: `accept
  --until`, which puts the pursuit in the accepted-as-unresolved bucket
  with its reopening condition on the record.
- **A gate is a conjunction and nothing else.** "`R` can pass while `F`
  fails" and "S1 needs all three" are not gate structure; they are which
  conclusions get drawn and which syntheses are refused. The gate on
  Arc 2 needs all eight regardless.
- **The $\sigma$ justification is design, not a condition.** It lives on
  the S1 locks note, per population, beside the value it justifies. A
  condition reading *"$\sigma$ has a written justification"* would be
  satisfied by the note it sits next to and check nothing; what a
  check can catch is `L1` — that the number reported was produced under
  that $\sigma$ and not another.
- **Arc 2 has no line of enquiry until it starts.** Planning it now
  records the intent and the gate; the question it advances is not yet
  known, because which substrate composes is what Arc 1 decides.
