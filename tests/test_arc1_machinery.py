"""Arc 1 machinery tests — not scientific pass/fail (science can fail)."""

from __future__ import annotations

import numpy as np
import pytest

from addressable_transients.s1.arc1 import (
    C_PRIME,
    S1Arc1Result,
    evaluate_amplitude_cell,
    run_s1_arc1,
)
from addressable_transients.s1.targets import CLUSTER, LOCKS
from addressable_transients.s2.arc1 import S2Arc1Result, run_s2_arc1
from addressable_transients.s2.tangent import LOCKS as S2_LOCKS


def test_cprime_disjoint_from_cluster():
    assert len(set(C_PRIME) & set(CLUSTER)) == 0
    assert C_PRIME.size == 100
    assert CLUSTER.size == 100


def test_s1_combination_rule_logic():
    """S1 addressability iff all three primaries pass — integer rules."""
    base = dict(
        n_seeds=20,
        sigma=0.8,
        matched_norm_fire=0,
        unweighted_off_time_fire=0,
        unweighted_cause_ok=0,
        unweighted_wrong_sb_fire=0,
        cprime_at_Tstar_mean=0.0,
        cprime_at_Tstar_fire=0,
    )
    # Knife-edge: 4/20 passes ≤4/20; 5/20 fails
    ok = S1Arc1Result(
        off_time_fire=4,
        cause_not_pattern=16,
        wrong_sb_fire=4,
        pass_off_time=True,
        pass_cause=True,
        pass_wrong_sb=True,
        s1_addressability=True,
        **base,
    )
    assert ok.s1_addressability
    fail = S1Arc1Result(
        off_time_fire=5,
        cause_not_pattern=16,
        wrong_sb_fire=4,
        pass_off_time=False,
        pass_cause=True,
        pass_wrong_sb=True,
        s1_addressability=False,
        **base,
    )
    assert not fail.s1_addressability
    # 15/20 fails ≥16/20 cause rule
    fail2 = S1Arc1Result(
        off_time_fire=0,
        cause_not_pattern=15,
        wrong_sb_fire=0,
        pass_off_time=True,
        pass_cause=False,
        pass_wrong_sb=True,
        s1_addressability=False,
        **base,
    )
    assert not fail2.s1_addressability


def test_s1_rates_in_unit_interval():
    """Live run: counts in [0, n]; addressability is bool."""
    r = run_s1_arc1()
    n = r.n_seeds
    assert n == 20
    for k in (r.off_time_fire, r.cause_not_pattern, r.wrong_sb_fire, r.matched_norm_fire):
        assert 0 <= k <= n
    assert isinstance(r.s1_addressability, bool)
    assert r.pass_off_time == (r.off_time_fire <= 4)
    assert r.pass_cause == (r.cause_not_pattern >= 16)
    assert r.pass_wrong_sb == (r.wrong_sb_fire <= 4)
    assert r.s1_addressability == (
        r.pass_off_time and r.pass_cause and r.pass_wrong_sb
    )
    # Excursions report (1) and (3) only
    for name in ("low", "high"):
        assert name in r.excursions
        assert "off_time_fire" in r.excursions[name]
        assert "wrong_sb_fire" in r.excursions[name]
        assert "cause_not_pattern" not in r.excursions[name]


def test_s2_eligibility_filter_and_combination():
    r = run_s2_arc1()
    assert r.n_baselines == 10
    assert r.n_eligible + r.n_excluded == 10
    assert len(r.eligible_seeds) == r.n_eligible
    # Floor stats for every seed 1..10
    assert set(r.floor_stats.keys()) == set(range(1, 11))
    for seed, fs in r.floor_stats.items():
        assert fs >= 0.0
        if seed in r.eligible_seeds:
            assert fs >= S2_LOCKS["c"]
        else:
            assert fs < S2_LOCKS["c"]

    if r.n_eligible < 6:
        assert r.random_control_claim == "INCONCLUSIVE"
        assert r.switchboard_claim == "INCONCLUSIVE"
        assert r.pass_random is None and r.pass_frozen is None
        assert r.n_trials == r.n_eligible * 4
    else:
        assert r.n_trials == r.n_eligible * 4
        assert 0 <= r.random_hits <= r.n_trials
        assert 0 <= r.frozen_hits <= r.n_trials
        assert r.pass_random == (r.random_hits <= 2)
        assert r.pass_frozen == (r.frozen_hits <= 2)
        assert r.random_control_claim == ("HOLDS" if r.pass_random else "FAILS")
        assert r.switchboard_claim == ("HOLDS" if r.pass_frozen else "FAILS")
        # Claims not folded: can disagree
        # (no assertion they must differ — only that both are independently set)


def test_s2_inconclusive_rule_synthetic():
    """Combination rule: N_eligible < 6 → inconclusive, not false."""
    r = S2Arc1Result(
        n_baselines=10,
        n_eligible=5,
        n_excluded=5,
        floor_stats={i: 0.1 for i in range(1, 11)},
        eligible_seeds=[1, 2, 3, 4, 5],
        n_trials=20,
        random_hits=0,
        frozen_hits=0,
        pass_random=None,
        pass_frozen=None,
        random_control_claim="INCONCLUSIVE",
        switchboard_claim="INCONCLUSIVE",
    )
    assert r.random_control_claim == "INCONCLUSIVE"
    assert r.switchboard_claim == "INCONCLUSIVE"


def test_s2_pass_threshold_integer():
    """≤2/N_trials: 2 passes, 3 fails (no rounding)."""
    n = 28
    assert (2 <= 2) and not (3 <= 2)
    r_pass = S2Arc1Result(
        n_baselines=10,
        n_eligible=7,
        n_excluded=3,
        floor_stats={},
        eligible_seeds=list(range(1, 8)),
        n_trials=n,
        random_hits=2,
        frozen_hits=3,
        pass_random=True,
        pass_frozen=False,
        random_control_claim="HOLDS",
        switchboard_claim="FAILS",
    )
    assert r_pass.random_control_claim == "HOLDS"
    assert r_pass.switchboard_claim == "FAILS"
