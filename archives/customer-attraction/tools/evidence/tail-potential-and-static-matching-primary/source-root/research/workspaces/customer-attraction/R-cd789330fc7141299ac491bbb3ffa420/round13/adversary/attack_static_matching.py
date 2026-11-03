"""Exact targeted attack on min static-optimal-portfolio matching <= SPE W.

Only already frozen complete SPE certificates are used.  Every optimal topic
multiset of exactly m topics is checked, including repeated topics.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def minimum_matching(cost):
    m = len(cost)
    dp = {0: (F(0), ())}
    for i in range(m):
        nxt = {}
        for mask, (value, perm) in dp.items():
            for j in range(m):
                if not mask >> j & 1:
                    newmask = mask | 1 << j
                    candidate = (value + cost[i][j], perm + (j,))
                    if newmask not in nxt or candidate < nxt[newmask]:
                        nxt[newmask] = candidate
        dp = nxt
    return dp[(1 << m) - 1]


def attack(instance_path, certificate_path):
    inst = Instance.from_dict(json.loads(instance_path.read_text()))
    obj = json.loads(certificate_path.read_text())
    obj = obj.get('strategy', obj.get('certificate', obj))
    if not ('actions' in obj and 'terminal_counts' in obj):
        return None
    certificate = StrategyCertificate.from_dict(obj)
    checked = verify_certificate(inst, certificate)
    checked.assert_valid()
    s = checked.terminal_history
    assert s is not None
    actual_counts = inst.counts(s, terminal=True)
    W = inst.welfare(actual_counts)
    opt = inst.optimal_welfare()
    # Costs depend on the position and replacement theme, not the optimal tuple.
    all_costs = []
    for i, old in enumerate(s):
        row = []
        for replacement in range(inst.topic_count):
            counts = list(actual_counts)
            counts[old] -= 1
            counts[replacement] += 1
            row.append(inst.topic_payoff(replacement, counts))
        all_costs.append(row)
    worst = None
    optimal_multisets = 0
    for T in combinations_with_replacement(range(inst.topic_count), inst.players):
        if inst.welfare(inst.counts(T, terminal=True)) != opt:
            continue
        optimal_multisets += 1
        value, perm = minimum_matching([[row[t] for t in T] for row in all_costs])
        candidate = (value, T, perm)
        if worst is None or candidate > worst:
            worst = candidate
    assert worst is not None
    value, T, perm = worst
    return {
        'instance': str(instance_path.relative_to(ROOT)),
        'instance_sha256': hashlib.sha256(instance_path.read_bytes()).hexdigest(),
        'certificate': str(certificate_path.relative_to(ROOT)),
        'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        'players': inst.players, 'topics': inst.topic_count,
        'verified_histories': checked.checked_histories,
        'verified_deviations': checked.checked_deviations,
        'actual_path': list(s), 'actual_payoffs': list(map(str, inst.player_payoffs(s))),
        'W': W, 'OPT': opt,
        'optimal_multisets_checked': optimal_multisets,
        'max_over_optimal_multisets_of_minimum_matching': str(value),
        'gap_above_W': str(value - W),
        'candidate_holds_on_certificate': value <= W,
        'worst_optimal_multiset': list(T),
        'minimizing_assignment_to_positions': [T[j] for j in perm],
        'cost_matrix_for_worst_optimal_multiset': [[str(row[t]) for t in T] for row in all_costs],
    }


def main():
    reports = []
    for instance_path in sorted((ROOT / 'examples/customer_attraction').glob('*.json')):
        certificate_path = ROOT / 'evidence/certificates/customer_attraction' / instance_path.name
        if not certificate_path.exists():
            continue
        obj = json.loads(instance_path.read_text())
        if not all(k in obj for k in ('topics', 'customers', 'players')):
            continue
        report = attack(instance_path, certificate_path)
        if report is not None:
            reports.append(report)
    output = {
        'scope': 'Targeted finite attack on static minmatching candidate; not a universal theorem or half counterexample.',
        'exact_arithmetic': True,
        'certificates_checked': len(reports),
        'violating_certificates': [r['instance'] for r in reports if not r['candidate_holds_on_certificate']],
        'reports': reports,
    }
    path = Path(__file__).with_name('static_matching_frozen.json')
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'certificates_checked': len(reports), 'violations': [r for r in reports if not r['candidate_holds_on_certificate']]}, indent=2))


if __name__ == '__main__':
    main()
