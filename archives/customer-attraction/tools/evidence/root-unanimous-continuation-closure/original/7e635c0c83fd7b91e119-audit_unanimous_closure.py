"""Exact audits of the unanimous-continuation closure lemma.

These finite checks audit the stated identity; they do not prove Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import (CustomerType, ExactSPESolver, Instance,
                                 verify_certificate)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    identity_checks = 0
    for q, a, b, nb, nd in product(range(1, 7), range(5), range(5),
                                  range(4), range(4)):
        # B-only clients have background a; D-only clients background b.
        gd = nb * F(1, a + 1) - nd * F(1, b + q)
        gb = nd * F(1, b + 1) - nb * F(1, a + q)
        delta = nb * F(q - 1, (a + 1) * (a + q))
        delta += nd * F(q - 1, (b + 1) * (b + q))
        assert gd + gb == delta
        if q >= 2 and nb + nd:
            assert delta > 0
            assert gd > 0 or gb > 0
            if gd <= 0:
                assert gb >= delta
        else:
            assert delta == 0
        identity_checks += 1

    solver_instances = prefix_checks = 0
    for wb, wd, wc in product(range(3), repeat=3):
        customers = tuple(CustomerType(mask, w) for mask, w in
                          ((frozenset({0}), wb), (frozenset({1}), wd),
                           (frozenset({0, 1}), wc)) if w)
        different_coverage = wb + wd > 0
        for m in range(2, 6):
            ins = Instance(('B', 'D'), customers, m)
            solver = ExactSPESolver(ins)
            for t in range(m - 1):
                q = m - t
                for k0 in range(t + 1):
                    prefix = (k0, t - k0)
                    targets = ((prefix[0] + q, prefix[1]),
                               (prefix[0], prefix[1] + q))
                    outs = solver.outcomes(prefix)
                    retained = [v for v in targets if v in outs]
                    assert not different_coverage or len(retained) <= 1
                    prefix_checks += 1
            solver_instances += 1

    # q=1 boundary: the original five-client collision-free gadget.
    ins1 = Instance.from_topic_sets(({0, 1}, {0, 1, 2},
                                    {0, 1, 3}, {3, 4}), players=2,
                                   labels=('C', 'A', 'B', 'D'))
    sol1 = ExactSPESolver(ins1)
    cert1 = sol1.certificate(on_path=(0, 3))
    report1 = verify_certificate(ins1, cert1)
    report1.assert_valid()
    assert (1, 0, 0, 1) in sol1.outcomes((1, 0, 0, 0))
    assert (0, 1, 1, 0) in sol1.outcomes((0, 1, 0, 0))
    assert ins1.welfare((1, 0, 0, 1)) == 4
    assert ins1.optimal_welfare() == 5

    # q=2: qD is locally credible after C, but qB is not credible after A.
    # This is deliberately a subgame observation, not a root SPE claim.
    x, y, z, reserve = 6, 3, 6, 6
    ins2 = Instance(('C', 'A', 'B', 'D'), (
        CustomerType(frozenset({0, 1, 2}), x),
        CustomerType(frozenset({1}), y),
        CustomerType(frozenset({2, 3}), z),
        CustomerType(frozenset({3}), reserve)), 3)
    sol2 = ExactSPESolver(ins2)
    all_d = (1, 0, 0, 2)
    all_b = (0, 1, 2, 0)
    assert all_d in sol2.outcomes((1, 0, 0, 0))
    assert all_b not in sol2.outcomes((0, 1, 0, 0))
    gd = F(x, 2) - F(reserve, 2)
    gb = F(reserve) - F(x, 3)
    assert gd == 0 and gb == 4
    assert gb == (x * (F(1, 2) - F(1, 3))
                  + reserve * (F(1) - F(1, 2)))
    result = {
        'status': 'all exact assertions passed',
        'main_goal': 'Q-CAG-HALF remains OPEN',
        'algebra_identity_checks': identity_checks,
        'canonical_two_topic_instances': solver_instances,
        'canonical_prefix_checks': prefix_checks,
        'q1_boundary': {'full_root_SPE_verified': True, 'W': 4, 'OPT': 5},
        'q2_architecture': {
            'instance': ins2.to_dict(),
            'after_C_two_D_locally_SPE': True,
            'after_A_two_B_locally_SPE': False,
            'last_D_gain_switching_to_B': str(gd),
            'last_B_gain_switching_to_D': str(gb),
            'q2_actual_root_SPE_claim': False,
        },
    }
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output)


if __name__ == '__main__':
    main()
