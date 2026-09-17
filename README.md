# Addressable transients

Specify a future collective state. Construct the cause. Read a cheap meter.

**Authority:** [`DESIGN.md`](DESIGN.md) is the specification. This package
implements **Arc 0** (objects and oracles) and **Arc 1** (claims that can
fail) for substrates S1 and S2. Arc 2 is blocked until Arc 1 pass rules hold.

Clean-room implementation from the DESIGN.md locks. No imports from any
retired dynamics package.

**Frozen Arc 0 judgment calls:** see [`FROZEN_ARC0.md`](FROZEN_ARC0.md). Do not retune after Arc 1 rates exist.

**Protocol:** S1 needs all three primary lights on the primary amplitude cell; excursion cells do not rescue a fail. S2 eligibility first; `N_eligible < 6` → INCONCLUSIVE (no extra seeds). Arc 2 is blocked.

**Arc 1 admission (2026-09-17):** see [`ADMISSION_ARC1.md`](ADMISSION_ARC1.md). S1 addressability FALSE; S2 random-control HOLDS; S2 switchboard FAILS. Addressability at these locks is \(e^{-MT}\) / \(J(t_0)^{-1}\), not a switchboard. Default: stop. Sequel cell \((\kappa=2,T=3)\) drafted there but **not minted**.

## Requirements

- Python ≥ 3.11
- numpy, scipy, pytest

## Install

```bash
cd addressable-transients
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

### Arc 0 harness

```bash
python -m addressable_transients --arc 0
pytest tests/test_s1_arc0.py tests/test_s2_arc0.py -q
```

### Arc 1 scientific claims

```bash
python -m addressable_transients --arc 1
```

Prints each primary rate as `k/n`, pass/fail per rule, excursion /
diagnostic reports (not in verdict), and Combination-rule verdicts:
S1 addressability, S2 random-control, S2 switchboard (or INCONCLUSIVE).

### Both

```bash
python -m addressable_transients          # default --arc all
pytest -q
```

Arc 1 pytest files check **machinery** only (rates in range, eligibility
filter, combination-rule logic). They do **not** hardcode scientific
pass/fail — the science can fail.

## Layout

```
src/addressable_transients/
  s1/          # complex-linear ring + arc1.py
  s2/          # Kuramoto grid + arc1.py
tests/         # Arc 0 oracles + Arc 1 machinery
DESIGN.md      # locks (changing a lock is a new design)
ADMISSION_ARC1.md  # Arc 1 negative as the record
FROZEN_ARC0.md     # Arc 0 judgment calls frozen before rates
```
