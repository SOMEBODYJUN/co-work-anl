"""Definition-level audit of the frozen two-pool tail report.

No imports from the author's oracle, NumPy, or the canonical SPE solver.
Expand each integer pool into separate unit customers; visit all 18^3 ordered
terminal histories for each of the twelve historical samples and one zero case.
This is a small independent oracle audit, not a second full parameter search.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import time


HERE = Path(__file__).resolve().parent


def unit_clients(parameters):
    x, a, b1, d1, b2, d2 = parameters
    clients = []
    for i in range(4):
        clients.extend([frozenset(range(4*i, 4*i+4))] * x)
        clients.extend([frozenset([4*i])] * a)
    for r, (b, d) in enumerate(((b1, d1), (b2, d2))):
        clients.extend([frozenset([4*i+1+r for i in range(4)] + [16+r])] * b)
        clients.extend([frozenset([16+r])] * d)
    return clients


def audit_one(parameters):
    clients = unit_clients(parameters)
    prefix = (3, 7, 11)
    # Each client contributes an integer multiple of 1/12: load is 1..4.
    leaves = {}
    for q, s, t in product(range(18), repeat=3):
        path = prefix + (q, s, t)
        u = [0, 0, 0]
        for interest in clients:
            load = sum(action in interest for action in path)
            if load:
                assert 12 % load == 0
                share = 12 // load
                for j, action in enumerate((q, s, t)):
                    if action in interest:
                        u[j] += share
        leaves[q, s, t] = tuple(u)

    root_min = []
    child_details = []
    target_tail = False
    for q in range(18):
        last_brs = {}
        middle_floor_by_action = []
        for s in range(18):
            max_last = max(leaves[q, s, t][2] for t in range(18))
            br = tuple(t for t in range(18) if leaves[q, s, t][2] == max_last)
            last_brs[s] = br
            middle_floor_by_action.append(min(leaves[q, s, t][1] for t in br))
        middle_floor = max(middle_floor_by_action)
        credible = [(s, t) for s in range(18) for t in last_brs[s]
                    if leaves[q, s, t][1] >= middle_floor]
        assert credible
        root_min.append(min(leaves[q, s, t][0] for s, t in credible))
        if q == 15:
            target_tail = (16, 17) in credible
        child_details.append({
            'root_action': q,
            'middle_floor_times_12': middle_floor,
            'root_min_times_12': root_min[-1],
            'credible_pairs': [list(pair) for pair in credible],
            'last_best_reply_sets': [list(last_brs[s]) for s in range(18)],
        })
    threshold = max(root_min)
    target_profit = leaves[15, 16, 17][0]
    assert target_profit == 12 * parameters[0]
    return {
        'parameters': list(parameters),
        'unit_clients': len(clients),
        'ordered_terminal_histories': len(leaves),
        'threshold': str(Fraction(threshold, 12)),
        'threshold_times_12': threshold,
        'target_profit_times_12': target_profit,
        'target_D1_D2_tail_supported': target_tail,
        'target_C_D1_D2_path_supported': target_tail and threshold <= target_profit,
        'children': child_details,
    }


def main():
    started = time.time()
    report_path = HERE / 'original/two_pool_tail_search.json'
    sample_path = HERE / 'related/tail_oracle_crosscheck.json'
    report = json.loads(report_path.read_text())
    samples = json.loads(sample_path.read_text())['samples']
    full_grid = list(product(range(19), repeat=4))
    eligible = [(b1, d1, b2, d2) for b1, d1, b2, d2 in full_grid
                if 2*(b2+d2) >= 6+b1 and d2 >= 3]
    assert len(full_grid) == 130321
    assert len(eligible) == report['prefilter_pass'] == report['exact_BI_checked']
    results = []
    for expected in samples:
        row = audit_one(tuple(expected['parameters']))
        assert row['threshold'] == expected['canonical_threshold']
        assert row['threshold'] == expected['vectorized_threshold']
        for field in ('target_D1_D2_tail_supported', 'target_C_D1_D2_path_supported'):
            assert row[field] == expected[field]
        row['historical_fields_matched'] = 4
        results.append(row)
    zero = audit_one((0, 0, 0, 0, 0, 0))
    assert zero['threshold'] == '0'
    assert zero['target_C_D1_D2_path_supported']
    assert all(len(c['credible_pairs']) == 324 for c in zero['children'])
    out = {
        'status': 'PASS',
        'method': 'independent explicit unit clients and all ordered three-mover leaves',
        'original_functions_called': 0,
        'canonical_solver_calls': 0,
        'full_search_repeats': 0,
        'full_grid_size': len(full_grid),
        'prefilter_pass': len(eligible),
        'prefilter_rejected': len(full_grid)-len(eligible),
        'historical_samples': results,
        'zero_customer_all_ties_case': zero,
        'new_terminal_histories': 13*18**3,
        'elapsed_seconds': time.time()-started,
        'inputs': {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (report_path, sample_path)},
        'scope': '12 fixed historical samples plus 1 zero case; no second 103474-parameter search',
    }
    (HERE/'unit-client-audit.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ('historical_samples', 'zero_customer_all_ties_case')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
