"""Exact static occupied-payoff counterexample audit; no solver imports."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for x in range(total + 1):
            for rest in compositions(total - x, parts - 1):
                yield (x,) + rest


def explicit_ten():
    topics = [{0, 1}, {0, 2, 3}, {0, 4, 5}, {1, 6, 7}, {1, 8, 9}]
    K = [[sum((F(1, 1 + int(x in opponent)) for x in query), F(0))
          for opponent in topics] for query in topics]
    lower = [sum((K[a][b] for a in range(1, 5)), F(0)) / 4 for b in range(5)]
    upper = [K[a][0] for a in range(5)]
    v = F(5, 2)
    assert lower == [v] * 5 and max(upper) == v
    occupied = F(len(topics[0]))
    nu = K[0][0]
    rho = sum((F(1, 2) for _ in topics[0]), F(0))
    assert occupied == 2 and nu == rho == 1
    assert v - nu - rho == F(1, 2)
    return {'clients': 10, 'topics': 5, 'static_competitors': 1,
            'matrix_query_by_background': [[str(x) for x in row] for row in K],
            'primal_uniform_leaf_column_values': list(map(str, lower)),
            'dual_pure_B_row_values': list(map(str, upper)),
            'safe_value': str(v), 'occupied_payoff': str(occupied),
            'net_mark_debt_after_refund': str(v - occupied)}


def general_case(m):
    C, h, P = m * (m + 1), m + 2, m + 3
    v, occupied = F(C, m + 1) + P, F(2 * C, m)
    static_count = 0
    active = []
    min_gap = None
    for counts in compositions(m, 2 * h + 1):
        b, *leaves = counts
        u, w = sum(leaves[:h]), sum(leaves[h:])
        t = u + w
        query = F(C, 2) * (F(1, m - w + 1) + F(1, m - u + 1))
        query += F(P, 2 * h) * sum((F(1, r + 1) for r in leaves), F(0))
        bound = t * (F(C, 2 * m * (m + 1)) - F(P, 4 * h))
        assert query - v >= bound >= 0
        assert (query == v) == (t == 0)
        if t == 0:
            active.append(counts)
        else:
            min_gap = query - v if min_gap is None else min(min_gap, query - v)
        static_count += 1
    assert len(active) == 1
    assert F(2 * C, m + 1) < v
    nu, rho = F(2 * C, m + 1), F(2 * C, m * (m + 1))
    assert v - nu - rho == v - occupied == 1
    last_dev = F(C, m) + P - occupied
    assert last_dev == 2
    return {'m': m, 'core_size_C': C, 'leaves_per_group_h': h,
            'private_size_P': P, 'topics': 2 * h + 1,
            'unit_clients': 2 * C + 2 * h * P,
            'static_count_backgrounds_exhausted': static_count,
            'safe_value': str(v), 'occupied_B_payoff': str(occupied),
            'unique_static_minimizer': 'B^m',
            'minimum_positive_static_gap': str(min_gap),
            'net_mark_debt_after_refund': str(v - occupied),
            'explicit_last_player_profitable_deviation': str(last_dev)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='create a new frozen report; never overwrite')
    args = parser.parse_args()
    out = {'status': 'exact auxiliary counterexample audit passed',
           'scope': 'static minimax occupied-payoff claim only; no SPE counterexample',
           'ten_client_example': explicit_ten(),
           'all_m_family_finite_audit': [general_case(m) for m in range(1, 7)]}
    if args.output:
        with args.output.open('x') as handle:
            json.dump(out, handle, indent=2)
            handle.write('\n')
    print(json.dumps({'ten_client_safe_value': out['ten_client_example']['safe_value'],
                      'audited_m': [r['m'] for r in out['all_m_family_finite_audit']],
                      'all_m_net_debt': 1, 'all_m_last_deviation_gain': 2}))
