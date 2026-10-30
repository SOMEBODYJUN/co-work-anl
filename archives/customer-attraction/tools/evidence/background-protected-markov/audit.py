"""Recheck the saved Markov point as a complete ordered-history strategy.

Default: exact certificate reconstructed near the saved floating point.
--replay-search: also execute the unchanged, finite 200-trial original search
in a temporary directory. Historical files are never overwritten.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import itertools
import json
from math import lcm
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def count_vector(history, q):
    return tuple(history.count(i) for i in range(q))


def verify_saved():
    raw = (HERE / "original/protected_best_q6k3.json").read_text()
    original = json.loads(raw)
    decimal = json.loads(raw, parse_float=str)
    q, k = original["q"], original["k"]
    assert (q, k) == (6, 3)
    assert original["prefix"] == [0] * q
    policy = {tuple(c): a for c, a in original["policy"]}
    states = {count_vector(h, q) for length in range(k)
              for h in itertools.product(range(q), repeat=length)}
    assert len(policy) == len(original["policy"]) == 28
    assert set(policy) == states and all(0 <= a < q for a in policy.values())
    rounded = {int(m): F(w).limit_denominator(10**7) for m, w in original["weights"].items()}
    scale = lcm(*(w.denominator for w in rounded.values()))
    units = {m: int(w * scale) for m, w in rounded.items()}
    assert scale == 57
    assert units == {1: 18, 2: 18, 8: 4, 12: 21, 17: 1, 18: 1,
                     20: 24, 24: 8, 32: 18, 48: 1}

    def rollout(history):
        while len(history) < k:
            history += (policy[count_vector(history, q)],)
        return history

    def check(weights):
        def payoff(action, terminal):
            return sum((mass / sum((mask >> a) & 1 for a in terminal)
                        for mask, mass in weights.items() if (mask >> action) & 1), F())

        rows = []
        ordered_policy = []
        for length in range(k):
            for history in itertools.product(range(q), repeat=length):
                chosen = policy[count_vector(history, q)]
                actual = rollout(history)
                on = payoff(chosen, actual)
                ordered_policy.append({"history": list(history), "action": chosen})
                for alternative in range(q):
                    off = rollout(history + (alternative,))
                    other = payoff(alternative, off)
                    rows.append({"history": list(history), "action": chosen,
                                 "alternative": alternative, "actual_terminal": list(actual),
                                 "deviation_terminal": list(off), "actual_payoff": str(on),
                                 "deviation_payoff": str(other), "slack": str(on - other)})
        slacks = [F(row["slack"]) for row in rows]
        return {
            "ordered_nodes": len(ordered_policy), "comparisons_including_self": len(rows),
            "nonself_comparisons": sum(r["action"] != r["alternative"] for r in rows),
            "minimum_slack": str(min(slacks)), "zero_slacks_including_self": slacks.count(F()),
            "negative_slacks": sum(x < 0 for x in slacks),
            "positive_slacks": sum(x > 0 for x in slacks),
            "minimum_positive_slack": str(min(x for x in slacks if x > 0)),
            "policy": ordered_policy, "comparisons": rows,
        }

    exact = check({m: F(w) for m, w in units.items()})
    assert exact["negative_slacks"] == 0
    binary = check({int(m): F(w) for m, w in original["weights"].items()})
    literal_decimal = check({int(m): F(w) for m, w in decimal["weights"].items()})
    actual = rollout(())
    assert count_vector(actual, q) == tuple(original["actual"]) == (0, 0, 2, 1, 0, 0)
    comparison = tuple(original["comparison"])
    assert comparison == (0, 1, 5)

    def union(actions):
        return sum(w for m, w in units.items() if any((m >> a) & 1 for a in actions))

    W = union(actual)
    D = sum(w for m, w in units.items()
            if not any((m >> a) & 1 for a in actual)
            and any((m >> a) & 1 for a in comparison))
    combinations = [{"actions": list(actions), "coverage": union(actions)}
                    for actions in itertools.combinations_with_replacement(range(q), k)]
    optimum = max(row["coverage"] for row in combinations)
    assert (W, D, optimum) == (57, 57, 83)
    assert actual == (3, 2, 2)
    # The compact rule below is independently compared with every saved state.
    for c, action in policy.items():
        if sum(c) == 0:
            compact = 3
        elif sum(c) == 1:
            compact = 3 if c[2] else 2
        else:
            multiset = tuple(a for a, multiplicity in enumerate(c) for _ in range(multiplicity))
            compact = 4 if multiset in [(0, 2), (2, 5)] else (
                3 if multiset in [(1, 2), (2, 2), (2, 4)] else 2)
        assert compact == action

    max_binary_delta = max(abs(F(original["weights"][str(m)]) - w) for m, w in rounded.items())
    max_decimal_delta = max(abs(F(decimal["weights"][str(m)]) - w) for m, w in rounded.items())
    root_rows = [r for r in exact["comparisons"] if r["history"] == []]
    report = {
        "status": "reconstructed-unit-customer-full-history-SPE-passed",
        "source_sha256": sha256(raw.encode()).hexdigest(),
        "rational_reconstruction_rule": "Fraction(parsed_float).limit_denominator(10**7), then exact verification",
        "unit_scale": scale, "unit_customers": sum(units.values()),
        "unit_types": [{"mask": m, "customers": n} for m, n in units.items()],
        "maximum_binary_float_adjustment": str(max_binary_delta),
        "maximum_literal_decimal_adjustment": str(max_decimal_delta),
        "topic_sizes": [union((a,)) for a in range(q)], "actual_ordered_history": list(actual),
        "actual_count_vector": list(count_vector(actual, q)),
        "actual_payoffs": [r["actual_payoff"] for r in [root_rows[0]]]
            + [next(r["actual_payoff"] for r in exact["comparisons"] if r["history"] == list(actual[:i]))
               for i in [1, 2]],
        "root_true_deviation_payoffs": [r["deviation_payoff"] for r in root_rows],
        "actual_welfare_and_tail_profit": W, "protected_comparison_labels": list(comparison),
        "protected_mass": D, "protected_ratio": str(F(D, W)),
        "unordered_triples_with_repetition": combinations, "OPT3": optimum,
        "OPT3_argmax": [r["actions"] for r in combinations if r["coverage"] == optimum],
        "half_slack": 2 * W - optimum,
        "count_policy_states": len(states),
        "count_state_nonself_comparisons": len(states) * (q - 1),
        "exact_unit_audit": exact,
        "frozen_binary_float_as_exact_rationals": {
            key: value for key, value in binary.items() if key != "policy"
        },
        "frozen_literal_decimals_as_exact_rationals": {
            key: value for key, value in literal_decimal.items() if key != "policy"
        },
    }
    out = HERE / "replay"
    out.mkdir(exist_ok=True)
    (out / "exact-reconstructed-certificate.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def replay_original():
    with tempfile.TemporaryDirectory(prefix="protected-markov-replay-") as directory:
        root = Path(directory)
        script = root / "protected_probe.py"
        shutil.copyfile(HERE / "original/protected_probe.py", script)
        args = [sys.executable, str(script), "--q", "6", "--k", "3", "--trials", "200",
                "--seed", "513823", "--background", "6", "--mode", "protected"]
        run = subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
        assert not run.stderr, run.stderr
        out = HERE / "replay"
        out.mkdir(exist_ok=True)
        (out / "original-search.stdout.txt").write_text(run.stdout)
        comparison = {}
        for name in ["protected_best_q6k3.json", "protected_summary_q6k3.json"]:
            generated = (root / name).read_bytes()
            (out / ("rerun-" + name)).write_bytes(generated)
            before = json.loads((HERE / "original" / name).read_text())
            after = json.loads(generated)
            keys = sorted(set(before) | set(after))
            differing = [key for key in keys if before.get(key) != after.get(key)]
            comparison[name] = {
                "differing_top_level_fields": differing,
                "equal_excluding_elapsed": {k: v for k, v in before.items() if k != "elapsed"}
                    == {k: v for k, v in after.items() if k != "elapsed"},
                "bytes_equal": generated == (HERE / "original" / name).read_bytes(),
                "generated_sha256": sha256(generated).hexdigest(),
            }
        import numpy
        import scipy
        summary = {
            "scope": "one unchanged original 200-trial finite search rerun; no mathematical upper-bound claim",
            "parameters": {"q": 6, "k": 3, "trials": 200, "seed": 513823,
                           "background_limit": 6, "mode": "protected"},
            "python": sys.version.split()[0], "numpy": numpy.__version__, "scipy": scipy.__version__,
            "stderr_empty": True, "output_comparison": comparison,
        }
        (out / "original-search-reconciliation.json").write_text(json.dumps(summary, indent=2) + "\n")
        return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-search", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for item in manifest["primary_sources"]:
        data = (HERE / item["preserved_relative_path"]).read_bytes()
        assert len(data) == item["size"] and sha256(data).hexdigest() == item["sha256"]
    report = verify_saved()
    compact = {key: value for key, value in report.items()
               if key not in ["exact_unit_audit", "frozen_binary_float_as_exact_rationals",
                              "frozen_literal_decimals_as_exact_rationals",
                              "unordered_triples_with_repetition"]}
    compact["unit_audit_counts"] = {key: value for key, value in report["exact_unit_audit"].items()
                                   if key not in ["policy", "comparisons"]}
    compact["frozen_literal_status"] = {
        label: {key: report[label][key] for key in ["minimum_slack", "negative_slacks"]}
        for label in ["frozen_binary_float_as_exact_rationals", "frozen_literal_decimals_as_exact_rationals"]}
    if args.replay_search:
        compact["original_search_replay"] = replay_original()
    (HERE / "replay/summary.json").write_text(json.dumps(compact, indent=2) + "\n")
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
