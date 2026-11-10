"""Check only the two finite certificates' interface to the legal-tail family.

The existing exact whole-root audits are reused at their SHA-bound inputs.
This program does not regenerate roots or repeat their ordered-node audits.
It decodes eight actual actions at most, six last-node replies, and checks
42 two-player tail IC comparisons per input with fractions.
"""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import argparse
import json


def digest(raw):
    return sha256(raw).hexdigest()


def inspect(repo, p):
    relative = "archives/customer-attraction/tools/evidence/global-actual-prefix/replay/finite-parameters"
    base = repo / relative
    report_path = base / f"full-root-p{p}-audit.json"
    report_raw = report_path.read_bytes()
    old = json.loads(report_raw)
    policy_path = base / old["policy_file"]
    raw = policy_path.read_bytes()
    assert digest(raw) == old["policy_sha256"]
    digits = raw[:-1].decode("ascii")
    n, q = 2 * p + 2, 6
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert len(digits) == sum(q ** depth for depth in range(n))
    assert set(digits) <= set("012345")

    def offset(history):
        ordinal = 0
        for action in history:
            ordinal = q * ordinal + action
        return (q ** len(history) - 1) // (q - 1) + ordinal

    def action(history):
        return int(digits[offset(history)])

    actual = ()
    while len(actual) < n:
        actual += (action(actual),)
    prefix = (0,) * p + (1,) * p
    assert actual == prefix + (0, 1) == tuple(old["actual_path"])
    old_replies = tuple(action(prefix + (t,)) for t in range(q))
    hand_replies = (1, 4, 4, 4, 5, 4)
    weights = {int(mask): weight for mask, weight in old["weights"].items()}
    family_weights = {
        1: (p + 1) * (p + 4), 2: (p + 1) * (p + 5),
        4: 2 * p + 3, 8: 2 * p + 3, 20: 2, 24: 2,
        36: 2, 40: 2, 49: (p + 1) * (p + 2),
        50: (p + 1) * (p + 2),
    }
    assert weights == family_weights

    def payoff(path, label):
        return sum((Fraction(weight, sum(bool(mask & (1 << a)) for a in path))
                    for mask, weight in weights.items() if mask & (1 << label)),
                   Fraction())

    last_matrix = [[payoff(prefix + (first, last), last)
                    for last in range(q)] for first in range(q)]
    hand_last_gaps = [[last_matrix[t][hand_replies[t]] - last_matrix[t][r]
                       for r in range(q)] for t in range(q)]
    first_values = [payoff(prefix + (t, hand_replies[t]), t) for t in range(q)]
    assert all(gap >= 0 for row in hand_last_gaps for gap in row)
    assert all(value == 2 * p + 6 for value in first_values)
    assert action(prefix) == 0 and old_replies == (1, 5, 5, 5, 5, 4)
    old_first_values = [payoff(prefix + (t, old_replies[t]), t) for t in range(q)]
    assert old_first_values == first_values

    def covered(path):
        return {mask for mask in weights if any(mask & (1 << a) for a in path)}

    old_covered = covered(prefix)
    tail_covered = covered(actual) - old_covered
    fresh_optimum = max(sum(weights[mask] for mask in
                            covered(prefix + (t, r)) - old_covered)
                        for t in range(q) for r in range(q))
    tail_profit = payoff(actual, 0) + payoff(actual, 1)
    assert tail_profit == 4 * p + 13 == old["tail_P"]
    assert sum(weights[mask] for mask in tail_covered) == 0 == old["tail_Delta"]
    assert fresh_optimum == 4 * p + 14 == old["tail_freshOPT2"]

    modified = bytearray(raw)
    patches = []
    for t, new in enumerate(hand_replies):
        at = offset(prefix + (t,))
        previous = action(prefix + (t,))
        if previous != new:
            assert modified[at] == ord(str(previous))
            modified[at] = ord(str(new))
            patches.append({"history": list(prefix + (t,)), "zero_based_digit_offset": at,
                            "old_action": previous, "new_action": new})

    return {
        "p": p, "players": n, "topics": list("ABTQRS"), "unit_customers": sum(weights.values()),
        "weights_by_interest_mask": weights,
        "policy": {"path": str(policy_path.relative_to(repo)), "sha256": digest(raw),
                   "bytes": len(raw), "digits": len(digits), "encoding_valid": True},
        "mature_root_audit_reused": {"path": str(report_path.relative_to(repo)),
                                     "sha256": digest(report_raw),
                                     "ordered_nodes": old["ordered_nodes"],
                                     "comparisons_including_self": old["comparisons_including_self"],
                                     "not_rerun": True},
        "actual_path": list(actual), "actual_prefix": list(prefix),
        "original_tail_first": action(prefix), "original_tail_replies": list(old_replies),
        "handwritten_tail_replies": list(hand_replies),
        "last_payoff_matrix": [[str(v) for v in row] for row in last_matrix],
        "handwritten_last_ic_gaps": [[str(v) for v in row] for row in hand_last_gaps],
        "handwritten_first_deviation_payoffs": [str(v) for v in first_values],
        "original_first_deviation_payoffs": [str(v) for v in old_first_values],
        "tail_checks_including_self": 42, "tail_checks_exact": True,
        "root_W": old["root_W"], "root_OPT": old["root_OPT"],
        "tail_P": str(tail_profit), "fresh_cover_increment": 0,
        "fresh_OPT2": fresh_optimum, "GLOBAL_gap_for_every_real_lambda": -1,
        "derived_handwritten_root_encoding": {
            "base_policy_sha256": digest(raw), "patches": patches,
            "sha256_of_full_patched_encoding_including_newline": digest(modified),
            "actual_terminal_at_prefix_preserved": list(actual),
            "whole_root_ic_basis": "Reuse exact base audit plus the outcome-preserving subtree replacement proof; no new full-root audit is claimed.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {
        "scope": "Only the p=2 and p=3 SHA-bound finite inputs and their 42-comparison tails.",
        "large_root_audits_rerun": False,
        "new_mathematical_claims": "Exact family-input identity, decoded tail policy differences, finite tail payoff checks, and a complete derived patched-policy encoding. All-p root reachability is not asserted.",
        "inputs": [inspect(args.repo, p) for p in (2, 3)],
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
