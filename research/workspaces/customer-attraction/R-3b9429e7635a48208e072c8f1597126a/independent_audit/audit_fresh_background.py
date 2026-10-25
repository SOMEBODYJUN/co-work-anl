"""Independent definition-level replay of the existing GLOBAL obstruction.

The customer list below is copied from the mathematical statement, not from a
model or a solver. The only external input is the proposed complete policy.
"""

from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_complete_spe.json"
GROUPS = [(1, 10), (2, 12), (4, 5), (8, 5), (20, 2), (24, 2),
          (36, 2), (40, 2), (49, 6), (50, 6)]
CUSTOMERS = [mask for mask, count in GROUPS for _ in range(count)]
TOPICS = tuple(frozenset(x for x, mask in enumerate(CUSTOMERS) if mask >> a & 1)
               for a in range(6))


def payoffs(leaf):
    loads = [sum(x in TOPICS[a] for a in leaf) for x in range(len(CUSTOMERS))]
    return tuple(sum((Fraction(1, loads[x]) for x in TOPICS[a]), Fraction())
                 for a in leaf)


def covered(leaf):
    return frozenset().union(*(TOPICS[a] for a in leaf))


def main():
    source_bytes = SOURCE.read_bytes()
    raw = json.loads(source_bytes)
    rows = raw["actions"]
    policy = {tuple(row["history"]): row["action"] for row in rows}
    histories = {h for k in range(4) for h in product(range(6), repeat=k)}
    assert len(policy) == len(rows) == 259
    assert set(policy) == histories
    assert all(a in range(6) for a in policy.values())

    def run(h):
        while len(h) < 4:
            h = h + (policy[h],)
        return h

    checks = 0
    min_slack = None
    for h in sorted(histories, key=lambda h: (len(h), h)):
        i = len(h)
        actual = payoffs(run(h))[i]
        for a in range(6):
            slack = actual - payoffs(run(h + (a,)))[i]
            assert slack >= 0, (h, a, slack)
            min_slack = slack if min_slack is None else min(min_slack, slack)
            checks += 1

    actual = run(())
    assert actual == (0, 1, 0, 1)
    u = payoffs(actual)
    assert u == (8, 9, 8, 9)
    welfare = len(covered(actual))
    optimum = max(map(lambda z: len(covered(z)), product(range(6), repeat=4)))
    assert (welfare, optimum) == (34, 52)

    prefix = (0, 1)
    old = covered(prefix)
    fresh_optimum = max(len(covered(z) - old) for z in product(range(6), repeat=2))
    new_coverage = len(covered(actual) - old)
    active_payoff = sum(u[2:])
    assert (active_payoff, new_coverage, fresh_optimum) == (17, 0, 18)

    # Recompute the entire two-player tail response table from the policy.
    tail_responses = [policy[prefix + (a,)] for a in range(6)]
    tail_current = [payoffs(run(prefix + (a,)))[2] for a in range(6)]
    tail_last = [[payoffs(prefix + (a, b))[3] for b in range(6)]
                 for a in range(6)]
    assert tail_responses == [1, 5, 5, 5, 5, 4]
    assert tail_current == [8] * 6
    # The prose gives another valid tie selection, not the exact full JSON.
    representative = [1, 4, 4, 4, 5, 4]
    for a, b in enumerate(representative):
        assert tail_last[a][b] == max(tail_last[a])
        assert payoffs(prefix + (a, b))[2] == 8

    result = {
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "script_path": str(Path(__file__).resolve().relative_to(ROOT)),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": sys.version,
        "randomness": "none",
        "arithmetic": "integers and fractions.Fraction; no floating point",
        "status": "exact_replay_passed",
        "unit_customers": len(CUSTOMERS),
        "history_count": len(histories),
        "all_action_comparisons": checks,
        "minimum_ic_slack": str(min_slack),
        "root_terminal": actual,
        "root_payoffs": list(map(str, u)),
        "root_welfare": welfare,
        "root_optimum": optimum,
        "actual_prefix": prefix,
        "remaining_payoff": str(active_payoff),
        "new_coverage": new_coverage,
        "fresh_optimum": fresh_optimum,
        "global_slack": str(active_payoff + new_coverage - fresh_optimum),
        "tail_responses": tail_responses,
        "prose_representative_responses": representative,
        "tail_forced_current_payoffs": list(map(str, tail_current)),
        "tail_last_payoff_table": [[str(v) for v in row] for row in tail_last],
    }
    target = Path(__file__).with_name("fresh_background_exact_replay.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if not k.startswith("tail_")}, indent=2))


if __name__ == "__main__":
    main()
