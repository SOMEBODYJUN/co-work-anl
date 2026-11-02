"""New standard-library seed regeneration and definition-level IC check, no LP.

This does not execute either original program or import the canonical verifier.
It preserves current regenerated action tables, not missing historical bytes.
"""

import hashlib
import itertools
import json
import platform
import random
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "original/envelope_fresh_cones.json"
OUT = ROOT / "regenerated"


def dump(path, value):
    with path.open("x") as handle:
        json.dump(value, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")


def fingerprint(path):
    data = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main():
    report = json.loads(REPORT.read_text())
    assert set(report) == {"status", "parameters", "policy_family", "records"}
    assert report["status"] == "floating_exploration_only"
    par = report["parameters"]
    assert set(par) == {"players", "topics", "trials", "seed", "output"}
    m, p = par["players"], par["topics"]
    assert (m, p, par["trials"], par["seed"]) == (5, 7, 12, 21062026)
    assert len(report["records"]) == par["trials"]
    assert report["policy_family"] == "all ordered-history actions sampled independently among unused labels"
    OUT.mkdir(exist_ok=False)
    rng = random.Random(par["seed"])
    histories = [h for d in range(m) for h in itertools.product(range(p), repeat=d)]
    masks = tuple(range(1, 1 << p))
    n_ic = len(histories) * (p - 1)
    n_env = len(tuple(itertools.combinations_with_replacement(range(p), m - 1)))

    def counts(h):
        return tuple(h.count(a) for a in range(p))

    @lru_cache(None)
    def uniform_payoffs(q):
        values = [Fraction(0) for _ in range(p)]
        for mask in masks:
            load = sum(q[a] for a in range(p) if mask >> a & 1)
            if load:
                for a in range(p):
                    if q[a] and mask >> a & 1:
                        values[a] += Fraction(1, load)
        return tuple(values)

    def welfare(q):
        return sum(any(q[a] and mask >> a & 1 for a in range(p)) for mask in masks)

    result = []
    record_fields = {"success", "actual_path", "ordered_spe_rows", "all_rows",
                     "max_Estar_minus_2W_normalized_W", "numerical_weights", "trial"}
    for trial, old in enumerate(report["records"]):
        assert set(old) == record_fields
        assert old["trial"] == trial
        assert old["success"] is True
        assert old["ordered_spe_rows"] == n_ic == 16806
        assert old["all_rows"] == n_ic + n_env == 17016
        assert old["max_Estar_minus_2W_normalized_W"] == -0.19999999999999996
        assert old["numerical_weights"] == {"127": 1.0}
        actions = {}
        for h in histories:
            unused = tuple(a for a in range(p) if a not in h)
            actions[h] = rng.choice(unused)
        assert len(actions) == 2801
        assert all(a not in h for h, a in actions.items())

        @lru_cache(None)
        def terminal(h):
            if len(h) == m:
                return h
            return terminal(h + (actions[h],))

        actual = terminal(())
        assert list(actual) == old["actual_path"]
        q_root = counts(actual)
        assert welfare(q_root) == 124
        assert len(set(actual)) == m
        assert all(uniform_payoffs(q_root)[a] == Fraction(124, 5) for a in actual)
        violations = []
        strict_old = tied_fresh = checked = 0
        min_old_slack = None
        for h in histories:
            chosen = actions[h]
            own = uniform_payoffs(counts(terminal(h)))[chosen]
            for alternative in range(p):
                if alternative == chosen:
                    continue
                alt = uniform_payoffs(counts(terminal(h + (alternative,))))[alternative]
                slack = own - alt
                checked += 1
                if slack < 0:
                    violations.append({"history": list(h), "alternative": alternative})
                if alternative in h:
                    assert slack > 0
                    strict_old += 1
                    min_old_slack = slack if min_old_slack is None else min(min_old_slack, slack)
                else:
                    assert slack == 0
                    tied_fresh += 1
        assert checked == n_ic and not violations
        # For the one full-interest customer, every actual/deviation terminal has
        # exactly m covering players, independently of repeated labels or path.
        full_interest_checked = 0
        for h in histories:
            own_load = sum(counts(terminal(h)))
            for alternative in range(p):
                if alternative != actions[h]:
                    alt_load = sum(counts(terminal(h + (alternative,))))
                    assert Fraction(1, own_load) == Fraction(1, alt_load) == Fraction(1, m)
                    full_interest_checked += 1
        assert full_interest_checked == n_ic
        nonanonymous = None
        grouped = {}
        for h in histories:
            key = counts(h)
            if key in grouped and actions[grouped[key]] != actions[h]:
                first = grouped[key]
                nonanonymous = {"first": list(first), "second": list(h),
                                "first_action": actions[first], "second_action": actions[h]}
                break
            grouped[key] = h
        assert nonanonymous is not None
        policy = {"status": "current_seed_regeneration_not_historical_policy_bytes",
                  "trial": trial, "players": m, "topics": p,
                  "actions": [{"history": list(h), "action": actions[h]} for h in histories],
                  "actual_path": list(actual), "terminal_counts": list(q_root)}
        target = OUT / f"policy-{trial:02d}.json"
        dump(target, policy)
        result.append({"trial": trial, "policy": fingerprint(target),
                       "actual_path": list(actual), "historical_path_matches": True,
                       "complete_histories": len(histories), "uniform_seed_customers": 127,
                       "uniform_seed_W": 124, "uniform_seed_OPT": 124,
                       "uniform_seed_root_player_payoff": "124/5",
                       "uniform_seed_nonself_IC_checked": checked,
                       "strict_old_comparisons": strict_old,
                       "tied_fresh_comparisons": tied_fresh,
                       "minimum_strict_old_slack": str(min_old_slack),
                       "uniform_seed_violations": violations,
                       "full_interest_point_nonself_IC_checked": full_interest_checked,
                       "full_interest_W": 1, "full_interest_OPT": 1,
                       "full_interest_Estar": str(Fraction(2) - Fraction(1, m)),
                       "full_interest_Estar_minus_2W": str(-Fraction(1, m)),
                       "same_count_different_action_example": nonanonymous})
    summary = {"status": "new_independent_exact_seed_and_feasible_point_check",
               "python": sys.version, "implementation": platform.python_implementation(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "frozen_report": fingerprint(REPORT),
               "frozen_code": fingerprint(ROOT / "original/envelope_fresh_cones.py"),
               "original_main_executions": 0, "original_optimize_executions": 0,
               "canonical_verifier_calls": 0, "LP_calls": 0,
               "historical_optimization_replay": False,
               "record_count": len(result), "decision_histories_per_policy": len(histories),
               "nonself_IC_per_policy_per_instance": n_ic, "envelope_backgrounds": n_env,
               "total_uniform_seed_IC_checked": sum(r["uniform_seed_nonself_IC_checked"] for r in result),
               "total_full_interest_IC_checked": sum(r["full_interest_point_nonself_IC_checked"] for r in result),
               "full_policy_identity_with_unstored_historical_tables_claimed": False,
               "exact_LP_optimality_claimed": False,
               "records": result}
    dump(OUT / "verification.json", summary)
    print(json.dumps({"status": summary["status"], "records": len(result),
                      "uniform_seed_IC_checked": summary["total_uniform_seed_IC_checked"],
                      "full_interest_IC_checked": summary["total_full_interest_IC_checked"],
                      "all_12_historical_paths_match": True, "LP_calls": 0}))


if __name__ == "__main__":
    main()
