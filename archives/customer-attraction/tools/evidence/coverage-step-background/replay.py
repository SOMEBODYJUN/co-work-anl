"""Replay both frozen 23-customer audits and certify the 488 reconstruction.

The original programs run unchanged in a disposable directory. Their saved
source reports are never overwritten. The supplementary checker expands
unit customers, verifies every ordered continuation history, and records all
action comparisons; it is not a new equilibrium search.
"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parent
REL = Path("research/workspaces/customer-attraction/"
           "R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction")
SOURCE = BASE / REL


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def exact_unit_audit(weights, policy, prefix=(2, 5), remaining=3, topics=6):
    customers = [mask for mask, count in weights.items() for _ in range(count)]
    assert all(isinstance(w, int) and w >= 0 for w in weights.values())
    required_counts = {tuple(h.count(a) for a in range(topics))
                       for depth in range(remaining)
                       for h in product(range(topics), repeat=depth)}
    assert set(policy) == required_counts
    assert all(0 <= a < topics for a in policy.values())

    def follow(history):
        history = tuple(history)
        while len(history) < remaining:
            c = tuple(history.count(a) for a in range(topics))
            history += (policy[c],)
        return history

    def pay(future):
        all_actions = tuple(prefix) + tuple(future)
        utilities = [Fraction(0) for _ in all_actions]
        for mask in customers:
            attracted = [i for i, a in enumerate(all_actions) if mask & (1 << a)]
            if attracted:
                share = Fraction(1, len(attracted))
                for i in attracted:
                    utilities[i] += share
        return utilities

    def fresh_covered(choices, excluded=()):
        occupied = tuple(prefix) + tuple(excluded)
        return {i for i, mask in enumerate(customers)
                if not any(mask & (1 << a) for a in occupied)
                and any(mask & (1 << a) for a in choices)}

    def optimum(k, excluded=()):
        # Nonempty catalog and monotonicity permit padding a smaller support.
        return max((len(fresh_covered(c, excluded)), c)
                   for c in combinations(range(topics), min(k, topics)))

    nodes = []
    for depth in range(remaining):
        for h in product(range(topics), repeat=depth):
            actual = follow(h)
            own_position = len(prefix) + depth
            on = pay(actual)[own_position]
            alternatives = []
            for a in range(topics):
                terminal = follow(h + (a,))
                off = pay(terminal)[own_position]
                assert on >= off, (h, a, on, off)
                alternatives.append({
                    "action": a, "future_terminal": terminal,
                    "payoff": str(off), "gap": str(on - off),
                })
            nodes.append({"history": h, "action": actual[depth],
                          "payoff": str(on), "alternatives": alternatives})

    actual = follow(())
    utilities = pay(actual)[len(prefix):]
    opt, opt_topics = optimum(remaining)
    tail_opt, tail_topics = optimum(remaining - 1, (actual[0],))
    first_new = len(fresh_covered((actual[0],)))
    delta = len(fresh_covered(actual))
    profit = sum(utilities, Fraction(0))
    local_gap = utilities[0] + first_new + tail_opt - opt
    global_gap = profit + delta - opt
    tail_gap = sum(utilities[1:], Fraction(0)) + delta - first_new - tail_opt
    assert global_gap == local_gap + tail_gap
    return {
        "scope": "Fixed legal background; supplied full continuation policy only.",
        "weights": weights, "unit_customers": len(customers),
        "fixed_ordered_prefix": prefix, "remaining_players": remaining,
        "topics": topics, "policy": [[c, a] for c, a in sorted(policy.items())],
        "ordered_nodes": len(nodes), "comparisons_including_self": topics * len(nodes),
        "nonself_comparisons": (topics - 1) * len(nodes),
        "actual_future_path": actual,
        "future_payoffs": [str(x) for x in utilities],
        "future_profit": str(profit), "new_coverage": delta,
        "fresh_optimum": opt, "fresh_optimum_topics": opt_topics,
        "first_new_coverage": first_new,
        "tail_fresh_optimum": tail_opt, "tail_optimum_topics": tail_topics,
        "first_step_gap": str(local_gap),
        "whole_candidate_gap": str(global_gap), "tail_candidate_gap": str(tail_gap),
        "all_ordered_node_comparisons": nodes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=BASE / "replay")
    args = parser.parse_args()
    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    for item in manifest["primary_sources"] + manifest.get("runtime_dependencies_not_disposed", []):
        raw = (BASE / item["source_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], item["id"]

    repo = next(p for p in BASE.parents if (p / "work.py").is_file())
    scratch = repo / "cleanup/workspaces/Boss2"
    scratch.mkdir(parents=True, exist_ok=True)
    replay_equal = {}
    with tempfile.TemporaryDirectory(prefix="coverage-step-replay-", dir=scratch) as directory:
        temp = Path(directory)
        for version in ("", "_v2"):
            name = "audit_coverage_step" + version + ".py"
            target = temp / name
            shutil.copyfile(SOURCE / name, target)
            result = subprocess.run([sys.executable, str(target)],
                                    cwd=temp, text=True, capture_output=True, check=True)
            report_name = "coverage_step_exact_audit" + version + ".json"
            report = json.loads((temp / report_name).read_text())
            frozen = json.loads((SOURCE / report_name).read_text())
            assert report == frozen, report_name
            save(out / report_name, report)
            save(out / ("stdout" + (version or "_legacy") + ".json"),
                 json.loads(result.stdout))
            replay_equal[report_name] = True

    old = json.loads((SOURCE / "coverage_step_exact_audit.json").read_text())
    current = json.loads((SOURCE / "coverage_step_exact_audit_v2.json").read_text())
    assert {k: v for k, v in current.items() if k != "witness_version"} == old
    policy = {tuple(c): a for c, a in current["policy"]}
    weights23 = {int(k): v for k, v in current["customer_types"].items()}
    unit23 = exact_unit_audit(weights23, policy)
    assert unit23["first_step_gap"] == "-1/10"
    assert unit23["whole_candidate_gap"] == "47/10"
    assert unit23["tail_candidate_gap"] == "24/5"
    save(out / "unit-expanded-23.json", unit23)

    lp = json.loads((SOURCE / "coverage_step_lp_candidate.json").read_text(),
                    parse_float=Decimal)
    assert {tuple(c): a for c, a in lp["policy"]} == policy
    assert tuple(lp["prefix"]) == tuple((2, 5).count(a) for a in range(6))
    denominator = 488
    weights488 = {int(k): int((v * denominator).to_integral_value())
                  for k, v in lp["weights"].items()}
    max_rounding_error = max(abs(lp["weights"][str(k)] * denominator - v)
                             for k, v in weights488.items())
    assert max_rounding_error < Decimal("0.0000000001")
    assert sum(weights488.values()) == denominator
    unit488 = exact_unit_audit(weights488, policy)
    assert tuple(lp["actual"]) == tuple(unit488["actual_future_path"].count(a)
                                       for a in range(6))
    assert unit488["future_payoffs"] == ["84", "84", "84"]
    assert unit488["first_step_gap"] == "-5"
    assert unit488["whole_candidate_gap"] == "104"
    unit488["reconstruction"] = {
        "source": "coverage_step_lp_candidate.json",
        "common_denominator": denominator,
        "max_absolute_scaled_decimal_rounding_error": str(max_rounding_error),
        "certificate_basis": "The exact unit-customer comparisons, not floating LP status.",
    }
    save(out / "unit-expanded-488.json", unit488)
    summary = {
        "status": "PASS",
        "frozen_primary_hashes": len(manifest["primary_sources"]),
        "runtime_dependency_hashes": len(manifest.get("runtime_dependencies_not_disposed", [])),
        "original_full_reports_equal": replay_equal,
        "legacy_vs_v2_only_report_difference": "witness_version",
        "ordered_nodes_per_witness": 43,
        "comparisons_including_self_per_witness": 258,
        "nonself_comparisons_per_witness": 215,
        "witness_23": {"local_gap": "-1/10", "global_gap": "47/10"},
        "witness_488": {"local_gap": "-5", "global_gap": "104"},
        "not_performed": [
            "No new equilibrium search or LP optimality certification.",
            "No full five-player root strategy construction or on-path reachability claim.",
            "No rerun of the historical random search or floating discovery sequence.",
        ],
    }
    save(out / "semantic-reconciliation.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
