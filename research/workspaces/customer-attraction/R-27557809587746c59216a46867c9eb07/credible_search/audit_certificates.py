"""Independent standard-library exact full-history audit of local candidates.

No customer_attraction, scipy, LP/MILP, or outcome-recursion import. Complete
strategies are checked directly against every supplied actual continuation.
"""
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def audit(instance, strategy):
    p, m = len(instance['topics']), instance['players']
    types = [(frozenset(c['topics']), c['multiplicity']) for c in instance['customers']]
    assert all(isinstance(n, int) and n > 0 for _, n in types)
    actions = {tuple(r['history']): r['action'] for r in strategy['actions']}
    expected = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert len(actions) == len(strategy['actions']) and set(actions) == expected
    assert all(isinstance(a, int) and 0 <= a < p for a in actions.values())
    payoff_cache = {}

    def counts(h):
        return tuple(h.count(a) for a in range(p))

    def pay(q):
        if q not in payoff_cache:
            row = [Fraction(0)] * p
            for likes, n in types:
                load = sum(q[a] for a in likes)
                if load:
                    for a in likes:
                        if q[a]:
                            row[a] += Fraction(n, load)
            payoff_cache[q] = tuple(row)
        return payoff_cache[q]

    def welfare(support):
        return sum(n for likes, n in types if likes.intersection(support))

    terminals = {}
    ties = strict = 0
    min_slack = None
    for depth in range(m, -1, -1):
        for h in product(range(p), repeat=depth):
            if depth == m:
                terminals[h] = counts(h)
                continue
            chosen = actions[h]
            q = terminals[h + (chosen,)]
            terminals[h] = q
            value = pay(q)[chosen]
            for a in range(p):
                if a == chosen:
                    continue
                deviation = pay(terminals[h + (a,)])[a]
                slack = value - deviation
                assert slack >= 0, (h, chosen, a, value, deviation)
                min_slack = slack if min_slack is None else min(min_slack, slack)
                ties += int(slack == 0)
                strict += int(slack > 0)
    q = terminals[()]
    assert tuple(strategy['terminal_counts']) == q
    path = ()
    while len(path) < m:
        path += (actions[path],)
    U = tuple(pay(q)[a] for a in path)
    W = welfare(set(path))
    assert sum(U) == W
    opt = max(welfare(set(J)) for size in range(min(m, p) + 1)
              for J in combinations(range(p), size))
    # Exact containment needs only positive customer types, not unit expansion.
    coverage = [frozenset(i for i, (likes, _) in enumerate(types) if a in likes)
                for a in range(p)]
    distinct = set(coverage)
    maxima = {A for A in distinct if not any(A < B for B in distinct)}
    by_counts = {}
    for h, a in actions.items():
        by_counts.setdefault(counts(h), set()).add(a)
    return {'valid_complete_pure_SPE': True, 'customers': sum(n for _, n in types),
            'players': m, 'topics': p, 'distinct_coverages': len(distinct),
            'distinct_maximal_coverages': len(maxima), 'root_history': path,
            'root_payoffs': [str(u) for u in U], 'W': W, 'OPT': opt,
            'OPT_over_W': str(Fraction(opt, W)), 'half_slack': 2 * W - opt,
            'histories': len(expected), 'nonself_deviations': ties + strict,
            'ties': ties, 'strict': strict, 'minimum_slack': str(min_slack),
            'equal_count_states_with_different_prescribed_actions':
                sum(len(v) > 1 for v in by_counts.values())}


def main():
    records = []
    for source in sorted(HERE.glob('*.json')):
        obj = json.loads(source.read_text())
        point = obj.get('exact_candidate')
        if not isinstance(point, dict) or not point.get('certified'):
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        for key in ('exact_candidate', 'exact_symmetric_candidate'):
            rec = obj.get(key)
            if not isinstance(rec, dict) or not rec.get('certified'):
                continue
            if 'instance' not in rec:
                continue
            result = audit(rec['instance'], point['strategy'])
            if key == 'exact_symmetric_candidate':
                d = obj['milp'].get('distinguished_topics', obj['milp'].get('distinct_topics'))
                p = len(rec['instance']['topics'])
                weights = {sum(1 << a for a in c['topics']): c['multiplicity']
                           for c in rec['instance']['customers']}
                orbit_values = {}
                for mask in range(1, 1 << p):
                    orbit = (mask & ((1 << d) - 1), (mask >> d).bit_count())
                    n = weights.get(mask, 0)
                    if orbit in orbit_values:
                        assert orbit_values[orbit] == n
                    else:
                        orbit_values[orbit] = n
                separator = min(sum(n for mask, n in weights.items()
                    if mask & (1 << a) and not mask & (1 << b))
                    for a in range(p) for b in range(p) if a != b)
                floor = rec.get('noncontainment_floor')
                if floor is not None:
                    assert separator >= Fraction(str(floor)) * result['W']
                result['input_symmetry_verified'] = True
                result['minimum_pairwise_noncontainment_over_W'] = str(Fraction(separator, result['W']))
            records.append({'source': source.name, 'sha256': digest,
                            'candidate_key': key, **result})
    report = {'method': 'standard-library direct continuation audit of every ordered history and deviation; no canonical imports',
              'universal_claim_proved': False, 'records': records}
    (HERE / 'certificate_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
