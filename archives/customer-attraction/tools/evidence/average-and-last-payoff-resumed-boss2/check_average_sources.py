"""Two fixed input checks, using rational arithmetic, with no search or LP.

The saved mean outcome is compared with the exact mean-relaxation outcome set
and full-SPE outcome set. A new complete mean-policy is reconstructed to make
the weaker quantifier explicit. It is not claimed to be the original policy.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
import argparse
import hashlib
import json
from pathlib import Path


def qcount(h, p):
    return tuple(h.count(a) for a in range(p))


def describe_policy(p, n, sigma, weights, J):
    assert set(sigma) == {h for depth in range(n) for h in product(range(p), repeat=depth)}
    assert all(a in range(p) for a in sigma.values())

    @lru_cache(None)
    def terminal(h):
        return qcount(h, p) if len(h) == n else terminal(h+(sigma[h],))

    def utility(a, q):
        assert q[a] > 0
        return sum((w/F(sum(q[b] for b in range(p) if mask >> b & 1))
                    for mask, w in enumerate(weights, 1) if mask >> a & 1), F(0))

    rows = []
    negative = []
    for h in sorted(sigma, key=lambda x: (len(x), x)):
        a = sigma[h]
        u = utility(a, terminal(h))
        v = [utility(b, terminal(h+(b,))) for b in range(p)]
        individual = [u-x for x in v]
        for b, slack in enumerate(individual):
            if slack < 0:
                negative.append({'history': h, 'action': a, 'alternative': b, 'slack': str(slack)})
        is_perm = len(set(h)) == len(h) and set(h) <= set(J)
        remaining = sorted(set(J)-set(h))
        avg = u-sum((v[b] for b in J), F(0))/len(J)
        perm = u-sum((v[b] for b in remaining), F(0))/len(remaining) if is_perm else None
        rows.append({'history': h, 'action': a, 'terminal_counts': terminal(h),
                     'chosen_payoff': str(u), 'alternative_payoffs': list(map(str, v)),
                     'individual_slacks': list(map(str, individual)),
                     'full_uniform_slack': str(avg),
                     'permutation_prefix_slack': str(perm) if perm is not None else None})
    return {'root_counts': terminal(()), 'histories': len(sigma), 'all_rows': rows,
            'negative_individual_rows': negative,
            'permutation_prefix_rows': sum(x['permutation_prefix_slack'] is not None for x in rows),
            'negative_permutation_prefix_rows': sum(x['permutation_prefix_slack'] is not None
                                                    and F(x['permutation_prefix_slack']) < 0 for x in rows),
            'negative_full_uniform_rows': sum(F(x['full_uniform_slack']) < 0 for x in rows)}


def mean_fixed(saved):
    p, n, J = saved['p'], saved['n'], tuple(saved['J'])
    weights = tuple(map(F, saved['r']))

    @lru_cache(None)
    def utility(a, q):
        assert q[a] > 0
        return sum((w/F(sum(q[b] for b in range(p) if mask >> b & 1))
                    for mask, w in enumerate(weights, 1) if mask >> a & 1), F(0))

    def welfare(q):
        return sum((w for mask, w in enumerate(weights, 1)
                    if any(q[b] and mask >> b & 1 for b in range(p))), F(0))

    def next_counts(q, a):
        z = list(q)
        z[a] += 1
        return tuple(z)

    state_sets = {'mean': {}, 'spe': {}}

    @lru_cache(None)
    def E(kind, q):
        if sum(q) == n:
            ans = frozenset([q])
        else:
            children = [E(kind, next_counts(q, a)) for a in range(p)]
            allowed = J if kind == 'mean' else tuple(range(p))
            minima = {a: min(utility(a, t) for t in children[a]) for a in allowed}
            out = set()
            for a in range(p):
                for t in children[a]:
                    if kind == 'mean':
                        ok = (len(J)-(a in J))*utility(a, t) >= sum(v for b, v in minima.items() if b != a)
                    else:
                        ok = utility(a, t) >= max(minima.values())
                    if ok:
                        out.add(t)
            ans = frozenset(out)
        assert ans
        state_sets[kind][q] = sorted(ans)
        return ans

    zero = (0,)*p
    em, es = sorted(E('mean', zero)), sorted(E('spe', zero))
    target = tuple(saved['q'])
    O = sum(w for mask, w in enumerate(weights, 1) if any(mask >> b & 1 for b in J))
    true_opt = max(sum(w for mask, w in enumerate(weights, 1) if any(mask >> b & 1 for b in subset))
                   for subset in combinations(range(p), min(p, n)))
    assert target in em and welfare(target) == min(map(welfare, em))
    assert len(em) == saved['outcomes'] and len(state_sets['mean']) == saved['states']
    assert O == saved['OPT'] and welfare(target) == saved['W']
    sigma = {}

    def build(h, wanted):
        if len(h) == n:
            assert qcount(h, p) == wanted
            return
        q = qcount(h, p)
        children = [E('mean', next_counts(q, a)) for a in range(p)]
        minima = {b: min(utility(b, t) for t in children[b]) for b in J}
        valid = [a for a in range(p) if wanted in children[a]
                 and (len(J)-(a in J))*utility(a, wanted) >= sum(v for b,v in minima.items() if b != a)]
        a = min(valid)
        sigma[h] = a
        for b in range(p):
            if b == a:
                outcome = wanted
            elif b in J:
                outcome = min(children[b], key=lambda t: (utility(b, t), t))
            else:
                outcome = min(children[b])
            build(h+(b,), outcome)
    build((), target)
    policy = describe_policy(p, n, sigma, weights, J)
    assert policy['negative_full_uniform_rows'] == 0
    return {'customers': str(sum(weights)), 'J_coverage': str(O), 'true_OPT': str(true_opt),
            'saved_named_OPT_is_J_coverage': True, 'saved_worst_W': str(welfare(target)),
            'J_over_saved_W': str(O/welfare(target)), 'true_OPT_over_saved_W': str(true_opt/welfare(target)),
            'mean_outcomes': em, 'spe_outcomes': es,
            'mean_minimum_welfare': str(min(map(welfare, em))),
            'spe_minimum_welfare': str(min(map(welfare, es))),
            'saved_target_is_full_SPE_outcome': target in es,
            'mean_state_count': len(state_sets['mean']), 'spe_state_count': len(state_sets['spe']),
            'new_mean_policy': [{'history': h, 'action': sigma[h]} for h in sorted(sigma, key=lambda x:(len(x),x))],
            'new_mean_policy_checks': policy,
            'all_state_sets': {kind: [{'counts': q, 'outcomes': states[q]}
                                    for q in sorted(states, key=lambda x:(sum(x),x))]
                               for kind,states in state_sets.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--original-dir', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    average = json.loads((args.original_dir/'average_probe.json').read_text())
    f = average['failures']['permutation_prefix']
    # Explicit new rational candidate, never an assertion of exact float identity.
    weights = tuple(F(str(v)).limit_denominator(96) for v in f['point'])
    assert [(i+1,str(w)) for i,w in enumerate(weights) if w] == [(2,'19/96'),(5,'1'),(9,'19/48'),(17,'15/32')]
    sigma = {tuple(x['history']): x['action'] for x in f['actions']}
    assert len(sigma) == len(f['actions']) == 156
    details = describe_policy(5, 4, sigma, weights, tuple(f['J']))
    assert details['negative_permutation_prefix_rows'] == 0
    assert details['root_counts'] == (0,0,4,0,0)
    O = sum(w for mask,w in enumerate(weights,1) if any(mask >> b & 1 for b in f['J']))
    assert O == F(33,16) and sum(weights) == O and weights[4] == 1
    mean = json.loads((args.original_dir/'mean_reply_search.json').read_text())['best']
    result = {'scope': 'two fixed new rational checks; zero original optimizer/random runs',
              'average_fixed_candidate': {'new_exact_weights': list(map(str,weights)),
                   'raw_decimal_to_candidate_errors': [str(F(str(v))-w) for v,w in zip(f['point'],weights)],
                   'integer_customer_scale': 96, 'integer_customer_count': 198,
                   'J_coverage_equals_all_customers': True, 'normalized_W': '1',
                   'normalized_J_coverage': str(O), 'checks': details},
              'mean_fixed_input': mean_fixed(mean),
              'source_files': [{'name': p.name, 'size':p.stat().st_size,
                                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                               for p in sorted(args.original_dir.iterdir()) if p.is_file()]}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'average_negative_individual':len(details['negative_individual_rows']),
                      'average_negative_full_uniform':details['negative_full_uniform_rows'],
                      'mean_summary':{k:v for k,v in result['mean_fixed_input'].items()
                                      if k not in ['new_mean_policy','new_mean_policy_checks','all_state_sets']},
                      'new_mean_policy_negative_individual':len(result['mean_fixed_input']['new_mean_policy_checks']['negative_individual_rows'])},ensure_ascii=False))


if __name__ == '__main__':
    main()
