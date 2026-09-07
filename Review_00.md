# Review-0

Verdict: **accept with amendments**. The revision fixes the shape problem the first review raised (pass/fail on ‖x(T)−x*‖ at one seed), but it does not fix it all the way. Two of the three S1 controls, and Claim A in S2, are still numerical identities dressed as measurements. The amendments below are the minimum to make each written number capable of being false.

## 1. S1: the primary rate is still by construction

The note says the primary is "cluster synchrony > 0.8 at T = 3, as a rate over seeds." But x(T) = e^{MT}e^{−MT}x* = x* to complex128 tolerance, so the meter reading at the design time is the meter reading of the *target*. If the target's cluster is built phase-coherent, its synchrony is ~1 for every seed regardless of A, ε, φ, or T. The seed only changes amplitudes, and an unweighted Kuramoto order parameter on arg(x) ignores amplitudes entirely. The 18/20 rule cannot fail unless the inverse is numerically broken, which is Arc 0's job.

The same applies to **control 3** as written. At T = 3 the disjoint block's synchrony is whatever x* has there. If out-of-cluster phases are drawn random, control 3 passes trivially; if they are not, it fails trivially. Either way it measures the target constructor, not the dynamics.

**Control 2 is the only S1 measurement in the note that depends on the ring.** x(1.5) = e^{−1.5M}x*, and whether a 101-node coherent block has dispersed by then is a property of the spectrum of M. That is a real, falsifiable ≤ 4/20.

**Amendments**

- **1a.** Move the T = 3 crossing rate to Arc 0 as a numerical check and report it there. Do not call it the S1 primary.
- **1b.** Promote a *specificity* statement to the S1 claim: designed input fires the meter at the requested time and not at a locked off-time. Primary numbers become the control-2 rate (≤ 4/20) and, for the same seeds, cluster synchrony of the designed **input** x(0) itself (≤ threshold in ≥ 16/20, say). The second one is the sentence "the cause is not already the pattern." Without it, a target that happens to be near a slow mode of M would pass everything while the inverse did nothing.
- **1c.** Replace control 3 with the S1 analogue of the S2 frozen-J control: **design with the wrong switchboard, evolve with the right one.** Concretely, design x(0) from M′ built on a nearest-neighbour ring (or α = 2), evolve under the α = 1 M, read the meter at T = 3. Rule: ≤ 4/20. This is the isolation that says the address is a property of *this* coupling, and it is the control the two substrates share. Control 3 as written can be kept as a reported diagnostic of the target constructor, but it is not a control.
- **1d.** Lock the target constructor and the meter explicitly: cluster nodes' phases (all equal? equal to what?), out-of-cluster phases (uniform random?), whether the order parameter is amplitude-weighted or not, RNG (`numpy.random.default_rng(seed)`) and draw order. Every downstream number is conditioned on these and none are written.
- **1e.** The amplitude excursion cells only do work if the meter is amplitude-sensitive or if the off-time reading is. With an unweighted meter, [1.0,1.5) vs [3.5,4.0) changes nothing at T = 3 and little at T = 1.5. Either use an amplitude-weighted synchrony or state that the excursions test only the off-time control. As written, their purpose ("so a later sentence cannot say we only looked at the published draw") is a defensive sentence about a variable that may not enter the measurement.

## 2. S2: Claim B can be untestable by baseline choice

Claim B (frozen-J inverse fails) is the load-bearing statement and I agree it should not be folded into A. But if the locked baseline θ(τ) sits near a phase-locked or slowly-drifting state, J(θ(τ)) ≈ J(θ(t₀)) over [t₀, T] and the frozen inverse *will* succeed. B then fails as a claim not because the switchboard idea is wrong but because the switchboard did not move. That outcome is currently indistinguishable from a real refutation.

**Amendments**

- **2a.** Lock a baseline-nonstationarity floor, reported before B is read: e.g. ‖J(θ(T)) − J(θ(t₀))‖_F / ‖J(θ(t₀))‖_F ≥ c, with c written now. Baseline initialisations that fall below the floor are *excluded before* the inverse is computed and the exclusion count is reported. That is not seed substitution; it is a pre-registered eligibility condition on the object B is about.
- **2b.** Claim A's energy-share threshold has the same construction problem as S1: Φ^{−1}e_j propagated by Φ gives q_j = 1 up to conditioning. Report A as an Arc 0-style recovery number with the condition number of Φ(T, t₀) per replica. The scientific content of S2 is entirely in the controls: random impulse of equal norm (still in the programme note, dropped from the revised text — restore it explicitly) and frozen-J. The pass rule should be on those.
- **2c.** Missing locks: the lattice (grid-28 per the programme note?), W (uniform? weighted?), baseline initialisation distribution, t₀ and T, the requested node j (or a locked set of j), the share threshold, and the integrator/tolerance for Φ. None are in the revised note. "Say 10" replicas should be "10".

## 3. Clean-room compliance

The revised note quotes the retired repo's findings as motivation: ARI = 1.0 at two seeds vs ≈ 0.6 over 20, message-demo aliasing at 1 Hz, XOR truth table at seed = 1. The programme rule is "disallowed: any finding, figure, node id, or stage name from the retired programme." The lesson ("one seed, one configuration, a decisive demo") is worth keeping; the numbers are not, and they will otherwise be the first inherited statistics in a document whose purpose is to have none.

- **3a.** Strip the ARI / message-demo / seed-1 references from anything that goes into DESIGN.md. State the sweep rule as a rule.
- **3b.** Source the parameter point (N = 201, ε = 50, φ = 1.56, f = 10 Hz, T = 3, cluster 50:150) to the cv-NN paper, not to "the published XOR point" of the repo. The paper is allowed; the repo's reproduction of it is where the seed = 1 table lives.
- **3c.** Threshold 0.8 "already used in-repo" — same issue. It is fine to lock 0.8; write it as a chosen threshold with a one-line justification (random phases on 101 nodes give R ≈ 0.1; 0.8 leaves a wide margin for controls) rather than as an inheritance.

## 4. What I accept as written

- Distance-coupled ring, α = 1, row-normalised: matches the matrix. Use that phrase.
- Seeds 1…20 inclusive, no retries, no substitution. Keep.
- Control 1 demoted to reported-only. Correct.
- A and B not folded. Correct.
- Separate repo, not a tenant. Correct.
- Composition blocked on amended Arc 1 pass rules.
- Review-0 as a named gate that Arc 0 harness work does not wait on.

## 5. Disposition

Accept with amendments 1a–1e, 2a–2c, 3a–3c. The one I would not proceed without is **1c** (wrong-switchboard control for S1) paired with **2a** (nonstationarity floor for S2): those two are what make "addressable" a claim about the coupling rather than about the target constructor, on both substrates, with the same control. The others are locks that are simply missing.

The next concrete move: DESIGN.md in a new empty repo containing the programme note, the revised arc with these amendments applied, and Review-0 checked with a pointer to this text. Arc 0 can start against `expm` in parallel.