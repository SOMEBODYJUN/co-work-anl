"""Exact checks of a general diagnostic, not a proof of its unpaid budget.

Reads only named existing complete policies and writes only this directory.
No solver, optimization package, or canonical model/verifier is imported.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def run(name, instance, policy):
    m, k = instance['players'], len(instance['topics'])
    types = [(set(c['topics']), c['multiplicity']) for c in instance['customers']]

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (policy[h],)
        return h

    def utility(h, a):
        return sum((F(n, sum(t in B for t in h)) for B, n in types if a in B), F())

    def welfare(h):
        return sum(n for B, n in types if any(t in B for t in h))

    histories = comparisons = 0
    for d in range(m):
        for h in product(range(k), repeat=d):
            histories += 1
            prescribed = utility(finish(h), policy[h])
            for a in range(k):
                comparisons += 1
                assert prescribed >= utility(finish(h + (a,)), a)
    z = finish(())
    W = welfare(z)
    utilities = [utility(z, a) for a in z]
    tuples = list(combinations_with_replacement(range(k), m))
    OPT = max(map(welfare, tuples))
    optimal = [t for t in tuples if welfare(t) == OPT]
    records = []
    for T in optimal:
        Q, L, R, margins, statics = [], [], [], [], []
        true_matrix = []
        for i, action in enumerate(z):
            true = [utility(finish(z[:i] + (t,)), t) for t in T]
            frozen = [utility(z[:i] + (t,) + z[i+1:], t) for t in T]
            qi = sum(frozen, F()) - sum(true, F())
            li = F()
            # Explicit nonnegative static coverage slack, by five disjoint cases.
            for B, n in types:
                c = sum(t in B for t in z)
                d = sum(t in B for t in T)
                a = action in B
                if not c:
                    if d:
                        li += n * (d - 1)
                elif d:
                    li += n * (F(d - 1, c) if a else F(d, c + 1))
                else:
                    li += n * (1 - F(1, c) if a else 1)
            assert li >= 0
            ri = sum(true, F())
            assert ri == OPT - W + utilities[i] + li - qi
            assert all(v <= utilities[i] for v in true)
            if i == m - 1:
                assert qi == 0
                assert ri >= OPT - W + utilities[i]
            Q.append(qi); L.append(li); R.append(ri)
            margins.append(ri - (OPT - W))
            statics.append(sum(frozen, F()))
            true_matrix.append(true)
        assert sum(R, F()) == m * (OPT-W) + W + sum(L, F()) - sum(Q, F())
        matchings, match_credits, match_penalties = [], [], []
        for p in permutations(range(m)):
            matched_true = sum((true_matrix[i][p[i]] for i in range(m)), F())
            matched_frozen = sum((utility(z[:i] + (T[p[i]],) + z[i+1:], T[p[i]])
                                  for i in range(m)), F())
            lp = F()
            for B, n in types:
                c = sum(t in B for t in z)
                d = sum(t in B for t in T)
                if not c:
                    if d:
                        lp += n * (d - 1)
                elif d:
                    lp += n * sum((F(1, 1+c-int(z[i] in B))
                                   for i in range(m) if T[p[i]] in B), F())
                else:
                    lp += n
            qp = matched_frozen - matched_true
            assert lp >= 0 and lp == matched_frozen - (OPT-W)
            assert matched_true == OPT-W+lp-qp
            assert 2*W-OPT == W-matched_true+lp-qp
            matchings.append(matched_true)
            match_credits.append(lp)
            match_penalties.append(qp)
        nperm = len(matchings)
        assert sum(match_credits,F())/nperm == F(W+sum(L,F()),m)
        assert sum(match_penalties,F())/nperm == sum(Q,F())/m
        assert sum(matchings,F())/nperm == sum(R,F())/m
        match = max(matchings)
        records.append({'optimal_tuple': T, 'R_true_rows': R, 'F_static_rows': statics,
                        'Q_adaptivity_penalties': Q, 'L_static_credits': L,
                        'ROW_margins': margins,
                        'aggregate_half_budget_margin': W + sum(L,F()) - sum(Q,F()),
                        'aggregate_sharp_budget_margin': sum(L,F()) - sum(Q,F()),
                        'best_true_matching': match,
                        'net_gap_matching_margin': match - (OPT-W),
                        'mean_true_matching': sum(matchings,F())/nperm,
                        'mean_matching_static_credit': sum(match_credits,F())/nperm,
                        'mean_matching_adaptive_penalty': sum(match_penalties,F())/nperm})
    return {'name': name, 'players': m, 'topics': k, 'histories': histories,
            'comparisons_including_self': comparisons, 'actual': z,
            'u': utilities, 'W': W, 'OPT': OPT,
            'optimal_multisets': len(optimal), 'diagnostics': records}


def load(name, ip, cp):
    instance = json.loads((ROOT / ip).read_text())
    raw = json.loads((ROOT / cp).read_text())
    if 'policy' in raw:
        policy = {tuple(map(int,h.split(','))) if h else (): a
                  for h,a in raw['policy'].items()}
    else:
        policy = {tuple(row['history']): row['action'] for row in raw['actions']}
    return run(name, instance, policy)


def main():
    boss = 'research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/'
    report = [load('static_assignment_counterexample', boss+'dynamic_exchange/assignment_instance.json',
                   boss+'dynamic_exchange/assignment_full_policy.json'),
              load('omission_matching_counterexample',
                   'examples/customer_attraction/portfolio_matching_failure.json',
                   'evidence/certificates/customer_attraction/portfolio_matching_failure.json'),
              load('optimal_prefix_bill_counterexample',
                   'examples/customer_attraction/prefix_balance_failure.json',
                   'evidence/certificates/customer_attraction/prefix_balance_failure.json')]
    # The same general identity is specialized to m=5, without optimizing a
    # five-player-only coefficient or claiming anything about other catalogs.
    m = 5
    instance = {'players':m, 'topics':['B']+[f's{j}' for j in range(m-1)],
                'customers':[{'topics':[0], 'multiplicity':m}]+
                            [{'topics':[j], 'multiplicity':1} for j in range(1,m)]}
    policy = {h:0 for d in range(m) for h in product(range(m), repeat=d)}
    report.append(run('five_player_all_big_pressure_sanity', instance, policy))
    output = {'status':'exact_identity_checks_only_no_general_payment_proof',
              'Q_CAG_HALF':'OPEN', 'results':report}
    (HERE/'dynamic_slack_audit.json').write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps(encode(output),indent=2))


if __name__ == '__main__':
    main()
