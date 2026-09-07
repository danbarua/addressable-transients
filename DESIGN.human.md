# Addressable transients — handoff note

For whoever is implementing this. It is the same design as `DESIGN.md`,
written as I would explain it to you at a whiteboard: what we are trying
to find out, why it is set up this way, what to build first, and what
would make me say we were wrong. Numbers and formulas are in `DESIGN.md`
and are authoritative; if this note and that file disagree, that file
wins and this note has a bug.

## The idea in one paragraph

Take a network of coupled oscillators. Decide in advance what pattern you
want it to be in at time $T$ — say, a particular block of 100 nodes all
in phase. Work *backwards* through the dynamics to find the input state
at time 0 that gets there. Start the system in that state, let it run,
and at $T$ read a cheap meter that says "yes, that block is coherent".
If that works, and works *only* at $T$ and *only* for the coupling you
solved against, then you have addressed the system: you chose a future
collective state and constructed its cause. That is the whole claim. It
is not learning, there is no training set, and nothing is decoded after
the fact — the meter is fixed before anything runs.

Composing two such addresses (two inputs, added, does the meter read the
sum?) is the interesting follow-on. We do not touch it until the single
address is shown to be a claim that can fail and did not.

## Why it is two experiments

We try it on two different systems, and we are deliberately *not*
claiming they are the same thing.

**S1 is the linear one.** $\dot x = Mx$ with $M$ a complex matrix: a
ring of 201 oscillators, each coupled to the others with strength
falling off as $1/\text{distance}$, plus a phase lag. It has a closed
form, $x(t) = e^{Mt}x(0)$, so the inverse is exact:
$x(0) = e^{-MT}x^\star$. Superposition holds, which is what makes
composition even conceivable. It is the clean case.

**S2 is the nonlinear one.** Kuramoto phases on a $16\times16$ periodic
grid. No closed form. What we can do is linearise around a baseline
trajectory $\theta(\tau)$ and address a *perturbation*: the tangent
dynamics $\dot\delta = J(\theta(\tau))\delta$ have a fundamental matrix
$\Phi$, and $u = \Phi^{-1}\delta^\star$ is the tangent-space input that
lands on $\delta^\star$ at $T$. The point of S2 is that $J$ changes
along the trajectory — the "switchboard" is time-ordered — and we want
to know whether inverting the *time-ordered* map is what does the work,
or whether a snapshot of $J$ at $t_0$ would have done just as well.

Each gets its own pass/fail. There is no combined "addressability"
verdict across the two. If S1 passes and S2 does not, that is the result.

## Build order

**Arc 0 first, and it is not science.** It is the harness: the objects
and the oracles we check them against. Nothing in Arc 0 can tell us
anything about addressability — every number in it is a numerical
identity that either holds to tolerance or the code is wrong.

For S1:
- `evolve(x0, t)`, checked against `scipy.linalg.expm` in complex128 on
  $N = 16$ and $N = 201$.
- `design_input(x_star, T)`, checked by evolving its output forward and
  requiring $\lVert e^{MT}u - x^\star\rVert_\infty < 10^{-10}$.
- The meter on the recovered state versus the meter on $x^\star$,
  agreeing to $10^{-8}$.

You may use a Fourier multiply on the circulant ring instead of `expm`
if it agrees to those tolerances. You may not lift code from any other
repository — a module with the serial numbers filed off is not
independent, and independence is a stated requirement of this record.

For S2:
- A tangent integrator, checked against finite difference at
  $\varepsilon = 10^{-6}$.
- $\Phi(T, t_0)$ by integrating the fundamental matrix
  (`solve_ivp`, RK45, `rtol=atol=1e-8`).
- Recovery: $u = \Phi^{-1}e_j$, propagate by $\Phi$, confirm you get
  $e_j$ back. Report the energy share $q_j$ and the condition number
  $\kappa_2(\Phi)$ per baseline while you are there — we want those
  numbers on file, but they are a harness report, not a claim.

S2 is a new integrator written here. Do not import one.

**Then Arc 1**, which is the experiment. **Then, and only if Arc 1
passes, Arc 2** (composition). Arc 2 is not designed yet beyond a
sketch, and that is on purpose: which substrate composes depends on what
Arc 1 says.

## The locked parameters

Every number is in the two tables in `DESIGN.md` ("S1 locks", "S2
locks"). I am not repeating them here because a second copy is a second
thing to get wrong. Read them once, put them in a config file that is
loaded and never edited, and treat any change as a *new design* — not a
tweak.

The ones you will want to know exist before you open the table:

- S1: $N=201$, 20 seeds (integers 1–20), a 100-node cluster at indices
  50–149, design time $T_\star = 3\,\mathrm{s}$, off-time
  $T_{\mathrm{off}} = 1.5\,\mathrm{s}$, and a "wrong switchboard" $M'$
  which is the same ring with $\alpha=2$ instead of $1$.
- S2: 256 nodes, 10 baseline seeds (1–10), four requested nodes
  $j \in \{0, 15, 136, 255\}$, $T = 1$, and an independent RNG stream
  for the random control.
- The RNG is `numpy.random.default_rng(seed)` and the **draw order is
  specified** — out-of-cluster phases first in index order, then all
  amplitudes in index order, then cluster phases overwritten to zero.
  Get this exactly right or your seed 7 is not my seed 7.

**Seeds are not negotiable.** No retries. No dropping a seed that looks
odd. No adding seeds to get a rounder denominator. If a seed gives a
bad number, that is a number.

## The meter, and the threshold

S1's meter is the amplitude-weighted order parameter on the cluster,
$R_C(x)$. It is 1 for a perfectly phase-aligned cluster and near 0.1 for
100 uniformly random phases. The fire line is $\sigma = 0.8$: above it,
the address bit is on.

Why 0.8 and not, say, 0.3: it is a *high-coherence* line, not a
significance line. We are not asking "is this distinguishable from
noise" — we are asking "is the cluster actually coherent". The same
line is used at every time and under every operator because the three
S1 checks all ask the same question about the same bit. $x(0)$ is not a
random population, and neither is the off-time state; the per-population
reasoning is in `DESIGN.md` under the S1 locks and you should read it,
but the short version is: same bit, same line, on purpose.

**We do not move $\sigma$ after seeing data.** If the rates land right
on 0.8, the pass rules apply as written. Build the analysis so that
$\sigma$ is read from the config alongside everything else, and so that
a run under a different $\sigma$ is visibly a different run.

S2's meter is the energy share $q_j$ at the requested node, with fire
line $q_\star = 0.25$: the node holds a quarter of the energy, about 64
times a uniform share. Justified separately in `DESIGN.md`; it is not
borrowed from $\sigma$.

## What Arc 1 actually measures

### S1 — is it specific to the time and to the coupling?

The inverse hitting the target at $T_\star$ is Arc 0 — it will read
$\approx 1$ for every seed if the code is right, and that number is
**never** reported as a result. What Arc 1 asks is whether the address
is *specific*:

1. **Off-time.** Evolve the designed input only to
   $T_{\mathrm{off}} = 1.5$. Fraction of seeds with $R_C > \sigma$.
   Pass: at most 4 of 20. (If the bit is already on halfway there, we
   did not address a *time*.)
2. **Cause is not already the pattern.** Look at $x(0)$ itself. Fraction
   with $R_C(x(0)) \le \sigma$. Pass: at least 16 of 20. (If the input
   already reads as the cluster, we constructed nothing.)
3. **Wrong switchboard.** Design $x(0)$ from $M'$ ($\alpha = 2$), then
   evolve under the real $M$ ($\alpha = 1$). Fraction with $R_C > \sigma$
   at $T_\star$. Pass: at most 4 of 20. (If any input works, the coupling
   was not what we inverted.)

All three on the primary amplitude cell. **S1 addressability holds if
and only if all three pass.** One failure and it does not, at this
instance — no rescue by seed or threshold.

Also report, without using in any verdict: the same three numbers on the
two amplitude-excursion cells (for 1 and 3 only); a matched-norm random
initial state evolved to $T_\star$; the unweighted meter on everything;
and $R$ on the disjoint block $C' = \{0..49\} \cup \{150..199\}$, which
tells us about the target constructor rather than the dynamics.

### S2 — is the time-ordered switchboard what is being inverted?

First, **eligibility**. Compute the floor statistic — how much $J$
changed between $t_0$ and $T$, relative to its own size — for each of
the 10 baseline seeds, *before computing any inverse*. A seed is
eligible if that is $\ge c = 0.20$: the switchboard actually moved. If
fewer than 6 of 10 are eligible, **stop**. Report the floor statistics
and nothing else. Do not draw more seeds. The result is *inconclusive
for want of a moving switchboard*, which is a different thing from a
refutation and must be written up as one.

On eligible baselines, two numbers, with $N_{\mathrm{trials}} =
N_{\mathrm{eligible}} \times 4$:

1. **Random impulse.** A Gaussian $u_{\mathrm{rand}}$ of the same norm
   as the designed $u$, evolved by $\Phi$. Fraction of trials with
   $q_j \ge q_\star$. Pass: at most 2 of $N_{\mathrm{trials}}$.
2. **Frozen Jacobian.** Design $u$ from $\Phi_{\mathrm{fr}} =
   \exp(J(\theta(t_0)) T)$ — the snapshot — then evolve by the true
   $\Phi$. Fraction with $q_j \ge q_\star$. Pass: at most 2 of
   $N_{\mathrm{trials}}$.

**These are two separate claims and stay separate.** (1) passing says
the system is addressable as a linear map. (2) passing says the
*time-ordering* is what does the work. (1) can pass while (2) fails —
that would mean the snapshot Jacobian was a good enough inverse, which
is a real and interesting negative for the switchboard claim, not a
bookkeeping problem. Do not fold them into one verdict.

## Arc 2, in outline only

Two designed inputs, added; one meter; a $2\times2$ table. S1: addition
is exact, $\sigma$ stays 0.8, and there is no Boolean operation in the
code — the table is what it is. S2: addition in the tangent only; a
finite-amplitude repeat is a different claim we would write up
separately.

Nothing starts until the Arc 1 pass rules above are met **and written
up as met**. Not "looks like it passed"; written.

## Things that are out of scope

Learning $W$ from data. Reconstructing images. Comparing graph families
on a classification score. Neuromorphic cost. Secrecy claims.
Finite-amplitude S2 composition. If any of these come up as a "quick
extension" while Arc 1 is running, the answer is no until the three arcs
exist.

## What I would like from you

1. The Arc 0 harness for both substrates, with the oracle checks as
   tests that fail if the tolerances are not met. Tell me when they are
   green and I will look at the $q_j$ / $\kappa_2$ report.
2. A config that holds every lock, loaded from one place, with the draw
   order implemented exactly as specified.
3. The Arc 1 analysis written so that each of the five pass rules is one
   function returning a rate and a boolean, with the threshold and
   denominators read from the config — not hardcoded, not rounded.
4. Any place where you had to make a choice the design does not
   specify, written down before you run, so we can decide whether it is
   a lock we forgot.

If something in here reads as ambiguous, ask before running rather than
after — the whole design is built around not changing things once we
have seen a number.
