"""Verify the separate 52-customer certificate used to correct historical status.

This is a comparison audit, not a cleanup receipt for the separate source
package. It reads only its explicit input and complete ordered policy, expands
unit customers, and uses no canonical game solver or original verifier.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    base = root / "comparison-later-global"
    manifest = json.loads((root / "source-manifest.json").read_text())
    for item in manifest["current_status_comparison_not_disposed"]:
        raw = (root / item["preserved_relative_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
    instance = json.loads((base / "global_actual_prefix_instance.json").read_text())
    raw_certificate = (base / "global_actual_prefix_complete_spe.json").read_bytes()
    certificate = json.loads(raw_certificate)
    assert instance["players"] == 4 and instance["topics"] == list("ABTQRS")
    clients = [frozenset(row["topics"]) for row in instance["customers"]
               for _ in range(row["multiplicity"])]
    assert len(clients) == 52
    rows = certificate["actions"]
    policy = {tuple(row["history"]): row["action"] for row in rows}
    histories = {h for depth in range(4) for h in product(range(6), repeat=depth)}
    assert len(rows) == len(policy) == len(histories) == 259
    assert set(policy) == histories and all(a in range(6) for a in policy.values())

    def follow(history):
        while len(history) < 4:
            history = history + (policy[history],)
        return history

    def payoff(action, terminal):
        return sum((F(1, sum(a in client for a in terminal))
                    for client in clients if action in client), F(0))

    comparisons = []
    for history in sorted(histories, key=lambda h: (len(h), h)):
        action = policy[history]
        actual = follow(history)
        value = payoff(action, actual)
        for alternative in range(6):
            terminal = follow(history + (alternative,))
            other = payoff(alternative, terminal)
            assert value >= other, (history, alternative, value, other)
            comparisons.append({
                "history": list(history), "action": action, "alternative": alternative,
                "true_terminal": list(actual), "alternative_terminal": list(terminal),
                "payoff": str(value), "alternative_payoff": str(other),
                "gap": str(value - other),
            })
    actual = follow(())
    values = [payoff(a, actual) for a in actual]
    welfare = sum(any(a in client for a in actual) for client in clients)
    optimum = max(sum(any(a in client for a in t) for client in clients)
                  for t in product(range(6), repeat=4))
    prefix = actual[:2]
    fresh = [client for client in clients if not any(a in client for a in prefix)]
    delta = sum(any(a in client for a in actual[2:]) for client in fresh)
    fresh_optimum = max(sum(any(a in client for a in t) for client in fresh)
                        for t in product(range(6), repeat=2))
    assert actual == (0, 1, 0, 1) and values == [F(8), F(9), F(8), F(9)]
    assert (welfare, optimum, delta, fresh_optimum) == (34, 52, 0, 18)
    result = {
        "status": "PASS",
        "role": "Current-status comparison only; no source done receipt for the separate GLOBAL package.",
        "certificate_sha256": hashlib.sha256(raw_certificate).hexdigest(),
        "ordered_nodes": 259, "comparisons_including_self": 1554,
        "nonself_comparisons": 1295, "actual_path": list(actual),
        "payoffs": list(map(str, values)), "W": welfare, "OPT4": optimum,
        "actual_prefix": list(prefix), "tail_P": str(sum(values[2:])),
        "tail_Delta": delta, "fresh_OPT2": fresh_optimum,
        "global_gap": str(sum(values[2:]) + delta - fresh_optimum),
        "all_comparisons": comparisons,
    }
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "all_comparisons"}))


if __name__ == "__main__":
    main()
