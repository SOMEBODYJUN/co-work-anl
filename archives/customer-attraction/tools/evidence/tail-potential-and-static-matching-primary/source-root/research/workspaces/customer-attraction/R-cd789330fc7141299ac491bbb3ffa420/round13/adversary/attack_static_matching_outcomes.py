"""All pure-SPE endpoints of named frozen instances vs static matching claim.

This is targeted finite falsification of one stated candidate, not sampling.
Counterexamples, if found, receive a separately verified full strategy tree.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
from attack_static_matching import minimum_matching


def attack(path):
    inst = Instance.from_dict(json.loads(path.read_text()))
    solver = ExactSPESolver(inst)
    outcomes = solver.outcomes()
    opt = inst.optimal_welfare()
    optimal = [T for T in combinations_with_replacement(range(inst.topic_count), inst.players)
               if inst.welfare(inst.counts(T, terminal=True)) == opt]
    worst = None
    violations = []
    for counts in outcomes:
        s = tuple(a for a, n in enumerate(counts) for _ in range(n))
        W = inst.welfare(counts)
        costs = []
        for old in s:
            row = []
            for replacement in range(inst.topic_count):
                cc = list(counts)
                cc[old] -= 1
                cc[replacement] += 1
                row.append(inst.topic_payoff(replacement, cc))
            costs.append(row)
        for T in optimal:
            value, perm = minimum_matching([[row[t] for t in T] for row in costs])
            candidate = (value - W, value, W, counts, T, perm)
            if worst is None or candidate > worst:
                worst = candidate
    assert worst is not None
    gap, value, W, counts, T, perm = worst
    result = {
        'instance': str(path.relative_to(ROOT)),
        'instance_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'players': inst.players, 'topics': inst.topic_count,
        'all_SPE_terminal_counts': len(outcomes),
        'all_optimal_multisets': len(optimal),
        'pairs_checked': len(outcomes) * len(optimal),
        'worst_matching_gap_above_actual_W': str(gap),
        'worst_matching_value': str(value), 'worst_actual_W': W,
        'worst_terminal_counts': list(counts),
        'worst_optimal_multiset': list(T),
        'minimizing_assignment_to_positions': [T[j] for j in perm],
    }
    if gap > 0:
        certificate = solver.certificate(counts)
        checked = verify_certificate(inst, certificate)
        checked.assert_valid()
        result['verified_path'] = list(checked.terminal_history)
        result['checked_histories'] = checked.checked_histories
        result['checked_deviations'] = checked.checked_deviations
        result['strategy'] = certificate.to_dict()
    return result


def main():
    # The five-provider cases are inspected first.  The remaining cases are
    # frozen prior examples with non-PNE or welfare-bridge failures.
    names = [
        'five_individual_security', 'dynamic_iid_local',
        'eight_cce_welfare_gap', 'worst_cce_welfare_failure',
        'worst_pne_welfare_failure', 'fractional_actual_load_failure',
        'root_tax_failure', 'prefix_balance_failure',
        'aggregate_theta_failure', 'global_decorrelation_failure',
        'empirical_iid_kernel', 'individual_security_failure',
        'local_security_increment', 'root_stationary_kernel',
        'coverage_opportunity_failure', 'tax_bridge_failure',
        'portfolio_matching_failure', 'residual_counterexample',
        'general_tax_failure', 'optimal_last_query_failure',
    ]
    reports = []
    outpath = Path(__file__).with_name('static_matching_all_outcomes.json')
    for name in names:
        start = time.time()
        report = attack(ROOT / 'examples/customer_attraction' / (name + '.json'))
        reports.append(report)
        outpath.write_text(json.dumps({
            'scope': 'Exact candidate attack on every pure-SPE terminal count of the named fixed instances; no universal theorem.',
            'exact_arithmetic': True, 'reports': reports,
        }, indent=2) + '\n')
        print(json.dumps({k: v for k, v in report.items() if k != 'strategy'}, sort_keys=True), flush=True)
        if F(report['worst_matching_gap_above_actual_W']) > 0:
            break


if __name__ == '__main__':
    main()
