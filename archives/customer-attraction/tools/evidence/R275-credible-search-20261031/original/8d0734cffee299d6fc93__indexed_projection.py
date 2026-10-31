"""One actual-customer credible completion of the indexed >2 necessary point.

Preserve each atom's actual A...E membership and number j of comparison
memberships. Spread its mass uniformly over the j-subsets of five comparison
labels; omit all formal auxiliary reply labels. This is ONE legal projection,
not a proof that all indexed atoms have or lack a credible completion.
"""
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import comb, gcd
from pathlib import Path
import signal
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/model.py').is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def serializable(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(v) for v in value]
    return value


def main():
    source = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
    original = json.loads(source.read_text())['primal']
    grouped = defaultdict(int)
    for atom in original['atoms']:
        actual_mask = sum(int(ch == '1') << a for a, ch in enumerate(atom['bits'][:5]))
        j = sum(atom['AB_hist'][4:])
        assert j == sum(atom['AE_hist'][4:]) == sum(atom['second_hist'][8:])
        grouped[actual_mask, j] += int(atom['mass_numerator'])
    clones = defaultdict(int)
    for (actual_mask, j), weight in grouped.items():
        assert 10 % comb(5, j) == 0
        for outside in combinations(range(5, 10), j):
            mask = actual_mask | sum(1 << a for a in outside)
            if mask:
                clones[mask] += weight * (10 // comb(5, j))
    common = gcd(*clones.values())
    scale = F(int(original['denominator']) * 10, common)
    inst = Instance(tuple('ABCDE') + tuple('T' + str(i + 1) for i in range(5)),
        tuple(CustomerType(frozenset(a for a in range(10) if mask & (1 << a)), n // common)
              for mask, n in sorted(clones.items())), 5)
    q = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0)
    T = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1)
    W, comparison, optimum = inst.welfare(q), inst.welfare(T), inst.optimal_welfare()
    assert F(W) / scale == 1
    beta = F(original['comparison_cover'])
    assert F(comparison, W) == beta and comparison > 2 * W
    (HERE / 'indexed_projection_instance.json').write_text(json.dumps(inst.to_dict(), indent=2) + '\n')
    solver = ExactSPESolver(inst)
    started = time.monotonic()
    report = {'scope': 'one explicit actual-unit-customer projection; target is not presumed SPE',
        'source': str(source.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'grouped_actual_mask_j_types': len(grouped), 'concrete_customer_types': len(clones),
        'normalization_scale': scale, 'target_counts': q, 'target_W': W,
        'comparison_cover': comparison, 'comparison_over_target_W': beta,
        'OPT': optimum, 'OPT_over_target_W': F(optimum, W)}
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('60-second exact BI budget')))
    signal.alarm(60)
    try:
        outcomes = solver.outcomes()
        signal.alarm(0)
        report['complete_BI'] = True
        report['target_reachable'] = q in outcomes
        report['root_outcomes'] = len(outcomes)
        minimum = min(inst.welfare(c) for c in outcomes)
        report['minimum_SPE_W'] = minimum
        report['OPT_over_minimum_SPE_W'] = F(optimum, minimum)
        prefix = (0,) * 10
        obstructions = []
        for a in range(5):
            child = tuple(n + int(b == a) for b, n in enumerate(prefix))
            own = inst.topic_payoff(a, q)
            floor = solver.threshold(prefix)
            if q not in solver.outcomes(child) or own < floor:
                obstructions.append({'prefix_counts': prefix, 'next_action': a,
                    'target_payoff_over_W': own / W, 'credible_floor_over_W': floor / W,
                    'target_in_selected_child': q in solver.outcomes(child)})
            prefix = child
        report['actual_order_ABCDE_obstructions'] = obstructions
        if q in outcomes:
            cert = solver.certificate(q)
            ver = verify_certificate(inst, cert)
            ver.assert_valid()
            report['complete_certificate'] = cert.to_dict()
            report['definition_verification'] = {'valid': True,
                'histories': ver.checked_histories, 'deviations': ver.checked_deviations}
    except TimeoutError:
        signal.alarm(0)
        report['complete_BI'] = False
        report['reason'] = '60-second exact BI budget reached; no conclusion about target reachability'
    report['seconds'] = time.monotonic() - started
    report['solver_stats'] = vars(solver.stats)
    (HERE / 'indexed_projection_completion.json').write_text(json.dumps(serializable(report), indent=2) + '\n')
    print(json.dumps(serializable({k: v for k, v in report.items() if k != 'complete_certificate'}), indent=2), flush=True)


if __name__ == '__main__':
    main()
