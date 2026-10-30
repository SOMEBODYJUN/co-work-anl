"""Exact aggregate last-best-response floor obstruction.

This independent Fraction audit checks the 36-unit-customer, six-topic,
three-player complete pure SPE. It also checks the signed two-partition family
at n=3,4,5 as algebra and restricted-policy regressions. The signed rows are
not legal customer inputs; the general positive compilation is proved in the
accompanying Markdown. No optimizer or canonical SPE solver is imported.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[2]
INSTANCE = ROOT / "examples/customer_attraction/aggregate_theta_failure.json"
CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/aggregate_theta_failure.json"


def unit_types():
    """One cross-pair customer; three customers for each two-plus-two type."""
    return [(tuple((x, y)), 1) for x in range(3) for y in range(3, 6)] + [
        (x + y, 3) for x in combinations(range(3), 2)
        for y in combinations(range(3, 6), 2)]


def policy(history):
    if not history:
        return 0
    a = history[0]
    if len(history) == 1:
        return 3 if a < 3 else 0
    b = history[1]
    group = range(0, 3) if b < 3 else range(3, 6)
    return next(c for c in group if c not in history)


def utility(types, history, selected):
    return sum((Q(mass, sum(a in membership for a in history))
                for membership, mass in types if selected in membership), Q(0))


def coverage(types, history):
    return sum(mass for membership, mass in types if set(membership).intersection(history))


def replay(types, actions):
    histories = {h for d in range(3) for h in product(range(6), repeat=d)}
    assert set(actions) == histories
    terminals = {h: h for h in product(range(6), repeat=3)}
    comparisons = 0
    for d in range(2, -1, -1):
        for h in product(range(6), repeat=d):
            a = actions[h]
            assert a in range(6)
            chosen = terminals[h + (a,)]
            own = utility(types, chosen, a)
            for b in range(6):
                assert own >= utility(types, terminals[h + (b,)], b), (h, a, b)
                comparisons += 1
            terminals[h] = chosen
    return terminals[()], comparisons


def check_small():
    expected = unit_types()
    obj = json.loads(INSTANCE.read_text())
    assert obj["players"] == 3 and len(obj["topics"]) == 6
    types = [(tuple(item["topics"]), item["multiplicity"]) for item in obj["customers"]]
    assert sorted(types) == sorted(expected)
    assert sum(mass for _, mass in types) == 36
    cert = json.loads(CERTIFICATE.read_text())
    records = cert["strategy"]["actions"]
    actions = {tuple(item["history"]): item["action"] for item in records}
    assert len(actions) == len(records) == 43
    assert actions == {h: policy(h) for d in range(3) for h in product(range(6), repeat=d)}
    terminal, comparisons = replay(types, actions)
    assert terminal == (0, 3, 4)
    assert cert["strategy"]["terminal_counts"] == [1, 0, 0, 1, 1, 0]
    profits = tuple(utility(types, terminal, a) for a in terminal)
    welfare = coverage(types, terminal)
    optimum = max(coverage(types, h) for h in product(range(6), repeat=3))
    assert profits == (10, 12, 12) and sum(profits) == welfare == 34
    assert optimum == 36
    theta_rows = []
    for h in product(range(6), repeat=2):
        value = max(utility(types, h + (a,), a) for a in range(6))
        assert value == (15 if h[0] == h[1] else 12)
        theta_rows.append(value)
    theta = min(theta_rows)
    assert theta == 12 and welfare - 3 * theta == -2
    # Exhaust all terminal count patterns, including every repeat pattern.
    representatives = [(0, 1, 2), (0, 3, 4), (0, 0, 1), (0, 0, 3), (0, 0, 0)]
    table = {','.join(map(str, h)): [str(utility(types, h, a)) for a in h]
             for h in representatives}
    assert table == {'0,1,2': ['12', '12', '12'], '0,3,4': ['10', '12', '12'],
                     '0,0,1': ['9', '9', '15'], '0,0,3': ['25/3', '25/3', '37/3'],
                     '0,0,0': ['7', '7', '7']}
    return {"unit_customers": 36, "topics": 6, "players": 3,
            "ordered_decision_histories": 43, "all_action_comparisons": comparisons,
            "root_history": terminal, "payoffs": list(map(str, profits)),
            "welfare": welfare, "optimum": optimum, "theta": str(theta),
            "welfare_minus_players_theta": str(welfare - 3 * theta),
            "ordered_last_prefixes": len(theta_rows), "terminal_payoff_table": table}


def partition_F(mask, n):
    size = mask.bit_count()
    left = (mask & ((1 << n) - 1)).bit_count()
    pure = left in (0, size)
    if size == n:
        return int(pure)
    if size == n - 1:
        return 0 if pure else -1
    return 0


def partition_policy(h, n):
    if not h:
        return 0
    if len(h) == 1:
        return n if h[0] < n else 0
    pure = all((a < n) == (h[0] < n) for a in h)
    group_member = h[0] if pure else h[1]
    group = range(n) if group_member < n else range(n, 2 * n)
    return next(a for a in group if a not in h)


def check_partition(n):
    p = 2 * n
    def payoff(mask, a):
        return partition_F(mask, n) - partition_F(mask ^ (1 << a), n)
    terminals = {}
    for h in permutations(range(p), n):
        terminals[h] = sum(1 << a for a in h)
    histories = comparisons = 0
    for d in range(n - 1, -1, -1):
        for h in permutations(range(p), d):
            a = partition_policy(h, n)
            chosen = terminals[h + (a,)]
            own = payoff(chosen, a)
            for b in range(p):
                if b not in h:
                    assert own >= payoff(terminals[h + (b,)], b)
                    comparisons += 1
            terminals[h] = chosen
            histories += 1
    root = terminals[()]
    signed_welfare = sum(payoff(root, a) for a in range(p) if root >> a & 1)
    theta = min(max(payoff(sum(1 << a for a in h) | (1 << b), b)
                    for b in range(p) if b not in h)
                for h in combinations(range(p), n - 1))
    assert signed_welfare == n - 1 and theta == 1
    # Exact split inequality used to control all repeated legal prefixes.
    splits = 0
    for v in range(2, n):
        for background in range(n - v):
            delta = Q(1, (1 + background) * (2 + background)) - Q(1, (v + background) * (v + background + 1))
            assert delta >= 0
            if not background:
                assert delta >= Q(1, 3)
            splits += 1
    return {"players": n, "topics": p, "restricted_ordered_histories": histories,
            "restricted_action_comparisons": comparisons, "signed_root_sum": signed_welfare,
            "fresh_theta": theta, "split_checks": splits,
            "scope": "signed algebra and no-repeat policy regression, not a standalone legal input"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = {"claim": "CA-AGGREGATE-LAST-FLOOR-NO", "all_exact_checks_passed": True,
              "base_git_commit": subprocess.check_output(
                  ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              "python_version": platform.python_version(),
              "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "instance_sha256": hashlib.sha256(INSTANCE.read_bytes()).hexdigest(),
              "certificate_sha256": hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
              "replay_commands": ['python3 tests/audits/customer_attraction_aggregate_theta.py'],
              "optimizer_dependency": False,
              "small_legal_witness": check_small(),
              "partition_family_regressions": [check_partition(n) for n in (3, 4, 5)],
              "half_coverage_refuted": False}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            f.write(encoded)
    print(encoded, end='')

if __name__ == '__main__':
    main()
