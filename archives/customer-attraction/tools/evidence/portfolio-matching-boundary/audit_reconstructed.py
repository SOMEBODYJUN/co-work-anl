"""Exact reconstruction of the portfolio obstruction and two-tail identity.

No canonical game model, outcome recurrence, or floating optimizer is imported.
The two-player all-SPE check explicitly enumerates every last-player best
response function, preserving each ordered first-action history and every tie.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_check():
    raw = json.loads((ROOT / 'original/instance.json').read_text())
    cert = json.loads((ROOT / 'original/strategy.json').read_text())
    k = len(raw['topics'])
    assert raw['players'] == 2 and k == 5
    clients = [(set(x['topics']), x['multiplicity']) for x in raw['customers']]
    assert all(type(w) is int and w > 0 for _, w in clients)
    policy = {tuple(x['history']): x['action'] for x in cert['actions']}
    assert set(policy) == {()} | {(a,) for a in range(k)}

    def pay(own, other):
        return sum((F(w, 1 + (other in interest))
                    for interest, w in clients if own in interest), F(0))

    def cov(a, b):
        return sum(w for interest, w in clients if a in interest or b in interest)

    tables = []
    best_replies = []
    for a in range(k):
        values = [pay(b, a) for b in range(k)]
        best = [b for b in range(k) if values[b] == max(values)]
        assert policy[(a,)] in best
        best_replies.append(best)
        tables.append({'first': a, 'follower_payoffs': list(map(str, values)),
                       'selected': policy[(a,)],
                       'first_final_payoff': str(pay(a, policy[(a,)]))})
    root = [pay(a, policy[(a,)]) for a in range(k)]
    assert root[policy[()]] == max(root)
    a = policy[()]
    actual = (a, policy[(a,)])
    assert actual == (4, 0)
    assert cert['terminal_counts'] == [actual.count(a) for a in range(k)]

    # Every follower best-response function extends to all first histories.
    # A root maximizer then gives precisely every complete pure SPE outcome.
    outcomes = set()
    reply_function_count = 0
    for replies in product(*best_replies):
        reply_function_count += 1
        first_values = [pay(i, replies[i]) for i in range(k)]
        for i in range(k):
            if first_values[i] == max(first_values):
                hist = (i, replies[i])
                outcomes.add(tuple(hist.count(j) for j in range(k)))
    all_pairs = [(a, b, cov(a, b))
                 for a, b in combinations_with_replacement(range(k), 2)]
    optimum = max(w for _, _, w in all_pairs)
    optimal = [(a, b) for a, b, w in all_pairs if w == optimum]
    assert optimal == [(1, 3)] and optimum == 45
    residual = sum(w for interest, w in clients
                   if interest.intersection(optimal[0]) and not interest.intersection(actual))
    matrix = [[pay(t, policy[(t,)]) for t in optimal[0]],
              [pay(t, actual[0]) for t in optimal[0]]]
    matchings = [sum(matrix[i][p[i]] for i in range(2))
                 for p in permutations(range(2))]
    welfare = cov(*actual)
    min_welfare = min(sum(w for interest, w in clients
                          if any(q[j] and j in interest for j in range(k)))
                      for q in outcomes)
    assert (sum(w for _, w in clients), welfare, residual) == (86, 44, 42)
    assert matrix == [[19, 19], [22, 22]] and matchings == [41, 41]
    assert min_welfare == 41
    frozen = json.loads((ROOT / 'original/matching_frozen_run.json').read_text())
    assert sorted(map(tuple, frozen['canonical_all_spe_terminal_counts'])) == sorted(outcomes)
    for key, expected in [('actual_welfare', welfare), ('opt_m', optimum),
                          ('optimal_uncovered_customers', residual),
                          ('canonical_minimum_spe_welfare', min_welfare)]:
        assert frozen[key] == expected
    return {
        'all_ordered_decision_histories': len(policy),
        'nontrivial_single_action_comparisons': len(policy)*(k-1),
        'all_follower_best_response_functions': reply_function_count,
        'all_spe_terminal_counts': list(map(list, sorted(outcomes))),
        'minimum_spe_welfare': min_welfare,
        'actual_history': actual, 'actual_welfare': welfare, 'optimum': optimum,
        'all_pairs_including_repeats': all_pairs, 'unique_optimum': optimal,
        'residual': residual, 'deviation_matrix': [[str(v) for v in row] for row in matrix],
        'matching_sums': list(map(str, matchings)),
        'root_payoffs': list(map(str, root)), 'follower_table': tables,
        'frozen_all_spe_outcomes_and_main_values_agree': True,
    }


def uniform_check():
    # U_x(own,other) = own*(d+2-other)/((d+1)*(d+2)).
    # Numerators below are represented by (constant, coefficient of d).
    def num(own, other):
        return (F(own*(2-other)), F(own))

    def combine(terms):
        return tuple(sum((c*p[i] for c, p in terms), F(0)) for i in range(2))

    checks = 0
    backgrounds = [F(0), F(1), F(2), F(7), F(101), F(10**6), F(1, 2), F(4, 3), F(1001, 37)]
    min_p = None
    for a,b,t,s,q,r in product((0,1), repeat=6):
        p = (6*a+2*b+2*q+2*r-4*a*b+12*t*s-2*t*q-2*s*r
             -3*t*a-3*s*a-a*q-a*r-t*r-s*q)
        table = {
            (0,0): (2*b+2*q+2*r, 6-2*b+q+r),
            (1,0): (2*b+r, 3-2*b-q),
            (0,1): (2*b+q, 3-2*b-r),
            (1,1): (12+2*b-q-r, 12-2*b-2*q-2*r),
        }[(t,s)][a]
        assert p == table and p >= 0
        min_p = p if min_p is None else min(min_p, p)
        left_num = combine([(1,num(a,b)), (1,num(b,a)), (1,num(t,q)),
                            (1,num(s,r)), (1,num(t,a)), (1,num(s,a)),
                            (-2,num(t,s)), (-2,num(s,t))])
        slack_num = combine([(2,num(b,a)), (-1,num(q,a)), (-1,num(r,a)),
                             (1,num(q,t)), (-1,num(r,t)),
                             (1,num(r,s)), (-1,num(q,s))])
        remainder = combine([(1,left_num), (-F(1,3),slack_num)])
        assert remainder == (F(p,3), F(3*a+b+q+r,3))
        for d in backgrounds:
            def u(own, other): return F(own, d+1+other)
            lhs = u(a,b)+u(b,a)+u(t,q)+u(s,r)+u(t,a)+u(s,a)-2*u(t,s)-2*u(s,t)
            slacks = 2*u(b,a)-u(q,a)-u(r,a)+u(q,t)-u(r,t)+u(r,s)-u(q,s)
            assert lhs == slacks/3 + (p+d*(3*a+b+q+r))/(3*(d+1)*(d+2))
            checks += 1
        assert F(a,1+b)+F(b,1+a) == int(bool(a or b))
        assert F(t,1+s)+F(s,1+t) == int(bool(t or s))
    return {'membership_patterns':64, 'eight_case_entries_checked_on_all_patterns':64,
            'symbolic_affine_numerators':64, 'direct_fraction_identities':checks,
            'root_coverage_identities':128, 'minimum_polynomial':min_p,
            'backgrounds': list(map(str, backgrounds)),
            'universal_scope': 'Affine numerator coefficients prove every nonnegative background; no m>=3 inference.'}


def main():
    result = {'matching': matching_check(), 'uniform_identity': uniform_check(),
              'sha256':{p.name:digest(p) for p in sorted((ROOT/'original').iterdir())},
              'reconstruction_script_sha256':digest(Path(__file__)),
              'arithmetic':'integer and fractions.Fraction only', 'all_checks_passed':True}
    output = ROOT/'replay/reconstructed.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['matching','sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
