"""Definition-level independent set-valued BI for root's deletion example.

Standard-library arithmetic; does not import the repository SPE solver.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'omitted_deletion' / 'reduced.json'


def solve(obj, delete):
    inst = obj['instance']
    p, m = len(inst['topics']), inst['players']
    target = tuple(obj['target'])
    customers = [(tuple(r['topics']), r['multiplicity']) for r in inst['customers']]
    removed = [(B, w) for B, w in customers if not any(target[a] for a in B)]
    if delete:
        customers = [(B, w) for B, w in customers if any(target[a] for a in B)]

    @lru_cache(None)
    def utility(q, a):
        assert q[a]
        return sum((F(w, sum(q[b] for b in B)) for B, w in customers if a in B), F())

    def inc(q, a):
        return q[:a] + (q[a] + 1,) + q[a+1:]

    info = {}

    @lru_cache(None)
    def outcomes(q):
        if sum(q) == m:
            return frozenset([q])
        branches = [outcomes(inc(q, a)) for a in range(p)]
        minima = [min(utility(z, a) for z in branches[a]) for a in range(p)]
        threshold = max(minima)
        result = frozenset(z for a in range(p) for z in branches[a] if utility(z, a) >= threshold)
        assert result
        info[q] = {'minimum_branch_payoffs': [str(x) for x in minima], 'threshold': str(threshold)}
        return result

    root = (0,) * p
    E = outcomes(root)

    def target_exclusion(q):
        assert target not in outcomes(q)
        if any(q[a] > target[a] for a in range(p)):
            return {'q': q, 'reason': 'prefix exceeds target'}
        proof = {'q': q, 'threshold': info[q]['threshold'], 'actions': []}
        for a in range(p):
            if q[a] == target[a]:
                continue
            nxt = inc(q, a)
            if target in outcomes(nxt):
                threshold = F(info[q]['threshold'])
                assert utility(target, a) < threshold
                b = max(range(p), key=lambda b: F(info[q]['minimum_branch_payoffs'][b]))
                proof['actions'].append({'action': a, 'reason': 'strict incentive exclusion',
                                         'target_mover_payoff': str(utility(target, a)),
                                         'alternative_action': b,
                                         'minimum_alternative_payoff': info[q]['minimum_branch_payoffs'][b],
                                         'alternative_outcomes': [list(t) for t in sorted(outcomes(inc(q, b)))]})
            else:
                proof['actions'].append({'action': a, 'reason': 'target continuation impossible',
                                         'continuation': target_exclusion(nxt)})
        return proof

    report = {'deleted': delete, 'customer_count': sum(w for B, w in customers),
              'removed_types': [{'topics': B, 'multiplicity': w} for B, w in removed],
              'states': outcomes.cache_info().currsize, 'root_outcomes': sorted(E),
              'target_realizable': target in E, 'root_data': info[root]}
    report['second_F_cut'] = [
        {'prefix': [a, c, 0, 0, 1],
         'target_F_payoff': str(utility(target, 4)),
         'D_minimum_payoff': str(min(utility(z, 2) for z in outcomes((a, c, 1, 0, 1)))),
         'D_continuation_outcomes': [list(z) for z in sorted(outcomes((a, c, 1, 0, 1)))]}
        for a in range(3) for c in range(2)
    ]
    if target not in E:
        report['exclusion_tree'] = target_exclusion(root)
    return report


def main():
    obj = json.loads(SOURCE.read_text())
    original, deleted = solve(obj, False), solve(obj, True)
    assert original['target_realizable']
    assert not deleted['target_realizable']
    result = {'exact': True, 'scope': 'Independent finite counterexample to omitted-customer deletion closure; not to half coverage.',
              'source': str(SOURCE.relative_to(HERE.parents[4])), 'target': obj['target'],
              'original': original, 'deleted': deleted}
    (HERE / 'omitted_deletion_independent_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('exact', 'scope', 'target')}, indent=2))
    print(json.dumps({'original_root_outcomes': original['root_outcomes'],
                      'deleted_root_outcomes': deleted['root_outcomes'],
                      'deleted_second_F_cut': deleted['second_F_cut']}, indent=2))


if __name__ == '__main__':
    main()
