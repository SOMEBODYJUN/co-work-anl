"""New fixed witnesses for the response-debt identity, using unit customers.

The m=4 full SPE is the already-proved bank controller.  This script only
checks its twelve true root branches; it does not claim a new whole-tree audit.
No canonical solver or old controller implementation is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def scalar(background, probability, indicator, load):
    assert sum(probability) == 1
    assert all(not i or c >= 1 for i, c in zip(indicator, load))
    t = sum((p*i for p, i in zip(probability, indicator)), F())
    L = sum((p*c for p, c in zip(probability, load)), F())
    A = background + 1 + L
    D = sum((p/F(background+c) for p, i, c in zip(probability, indicator, load) if i), F())
    covariance = sum((p*i*c for p, i, c in zip(probability, indicator, load)), F()) - t*L
    J = sum((p*(background+c-A)**2/F(background+c)
             for p, i, c in zip(probability, indicator, load) if i), F())
    pushed = t/A
    assert D-pushed == (t-covariance+J)/A**2
    return dict(t=t, L=L, A=A, D=D, F=pushed, covariance=covariance,
                J=J, D_minus_F=D-pushed,
                normalized_debt=(covariance-t-J)/A**2)


def main():
    # A single customer of original positive type mask29 in the already-done
    # 34-unit, three-player complete SPE; no new equilibrium audit is run.
    local34 = scalar(0, (F(1, 4), F(3, 4)), (1, 0), (3, 1))
    assert local34['D'] == F(1, 12) and local34['F'] == F(1, 10)
    assert local34['J'] == F(1, 48) and local34['D_minus_F'] == -F(1, 60)

    # Already-proved four-player controller: every root action reanchors BASE,
    # then the two middle banks are the unused banks in increasing order and
    # the last player takes the first unused economic row and the root bank.
    players = 4
    actions = tuple(product(range(players), range(players-1)))
    units = tuple(['e'+str(i) for i in range(players)] +
                  ['b'+str(b)+'_'+str(j) for b in range(players-1) for j in range(2)])
    topics = {a: frozenset(('e'+str(a[0]), 'b'+str(a[1])+'_0', 'b'+str(a[1])+'_1'))
              for a in actions}
    probability = tuple(F(1, len(actions)) for _ in actions)
    branches = []
    for a, b in actions:
        others = sorted(set(range(players-1))-{b})
        fresh_row = min(set(range(players))-{a})
        profile = ((a, b), (a, others[0]), (a, others[1]), (fresh_row, b))
        loads = {x: sum(x in topics[z] for z in profile) for x in units}
        root_utility = sum((F(1, loads[x]) for x in topics[(a, b)]), F())
        assert root_utility == F(4, 3)
        branches.append(dict(query=(a, b), probability=F(1, 12),
                             true_profile=profile, unit_client_loads=loads,
                             root_utility=root_utility))
    per_client = []
    for x in units:
        indicator = tuple(int(x in topics[a]) for a in actions)
        loads = tuple(row['unit_client_loads'][x] for row in branches)
        metrics = scalar(0, probability, indicator, loads)
        per_client.append(dict(client=x, indicators=indicator, loads=loads, **metrics))
    D = sum(row['D'] for row in per_client)
    pushed = sum(row['F'] for row in per_client)
    debt = sum(row['normalized_debt'] for row in per_client)
    assert D == F(4, 3) and pushed == F(383, 280)
    assert debt == pushed-D == F(29, 840)
    assert [row['L'] for row in per_client[:4]] == [F(3, 2), F(1), F(3, 4), F(3, 4)]
    assert all(row['L'] == F(4, 3) for row in per_client[4:])
    extra_floor = F(1, 2)+F(6, 7)
    assert extra_floor == F(19, 14) > D
    report = dict(
        status='exact_pass',
        local34_single_unit=dict(original_positive_type_mask=29,
            original_type_multiplicity=3, root_queries=(0, 5),
            true_profiles=((0, 3, 4), (5, 0, 1)), **local34),
        bank_m4_uniform_root_push=dict(
            players=players, unit_clients=len(units), common_topics=len(actions),
            branches=branches, per_unit_client=per_client, D=D, u=D,
            incentive_slack=F(0), F=pushed, F_minus_u=pushed-D,
            total_normalized_response_debt=debt,
            fractional_competitor_mass=players,
            t_5_delta_5=extra_floor, t_5_minus_root=extra_floor-D,
            welfare=8, OPT=10,
            scope='Only twelve actual root-response branches recomputed. Full-history SPE and the global fractional optimum are reused from the already-done all-m bank family proof.'))
    print(json.dumps(report, ensure_ascii=False, default=str, indent=2))


if __name__ == '__main__':
    main()
