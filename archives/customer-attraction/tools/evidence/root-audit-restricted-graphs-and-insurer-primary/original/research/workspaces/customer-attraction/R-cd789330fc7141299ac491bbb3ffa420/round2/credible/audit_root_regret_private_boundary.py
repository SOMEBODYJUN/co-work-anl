"""Targeted exact audit: all seven roots of the fixed 53-type suffix plan.

The all-multiplicity statement is analytic, using only the typewise omission
identity plus the existing private-seat lemma. No LP, tail cone search,
canonical solver, or author's previous audit is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tail'
INSTANCE = json.loads((SOURCE / 'endogenous_53_instance.json').read_text())
STRATEGY = json.loads((SOURCE / 'endogenous_53_strategy.json').read_text())
ROWS = tuple((frozenset(row['topics']), row['multiplicity']) for row in INSTANCE['customers'])
CUSTOMERS = tuple(topics for topics, count in ROWS for _ in range(count))
ACTIONS = {tuple(row['history']): row['action'] for row in STRATEGY['actions']}


@lru_cache(None)
def finish(h):
    return h if len(h) == 4 else finish(h + (ACTIONS[h],))


def payoff(path, who):
    return sum((F(1, sum(t in customer for t in path))
                for customer in CUSTOMERS if path[who] in customer), F())


def coverage(path):
    return sum(any(t in customer for t in path) for customer in CUSTOMERS)


def mask(customer):
    return sum(1 << t for t in customer)


def main():
    target = HERE / 'root_regret_private_boundary_audit.json'
    if target.exists():
        raise FileExistsError(target)
    expected = {h for depth in range(4) for h in product(range(7), repeat=depth)}
    assert set(ACTIONS) == expected
    assert len(CUSTOMERS) == 53 and len(ROWS) == 14
    positive = expected - {()}
    count = 0
    for h in positive:
        prescribed = payoff(finish(h), len(h))
        for t in range(7):
            assert prescribed >= payoff(finish(h + (t,)), len(h))
            count += 1
    assert len(positive) == 399 and count == 2793

    all_types = tuple(topics for topics, _ in ROWS) + (frozenset(range(7)),)
    optimal_support = (0, 2, 5, 6)
    assert all(any(t in customer for t in optimal_support) for customer in all_types)
    multisets = tuple(combinations_with_replacement(range(7), 4))
    assert len(multisets) == 210
    optimum = max(coverage(path) for path in multisets)
    assert optimum == coverage(optimal_support) == len(CUSTOMERS)
    paths = tuple(finish((t,)) for t in range(7))
    assert paths == ((0, 6, 3, 4), (1, 6, 3, 4), (2, 6, 3, 4),
                     (3, 6, 0, 1), (4, 6, 0, 1), (5, 6, 0, 1), (6, 0, 3, 4))
    root_values = tuple(payoff(path, 0) for path in paths)
    assert root_values == (F(29, 3),) * 6 + (F(19),)
    expected_missing = ({4, 32}, {4, 32}, {32}, {4, 32}, {4, 32}, {4}, {4, 32})
    records = []
    type_checks = 0
    for root, path in enumerate(paths):
        missing = set()
        for customer in all_types:
            covered = any(t in customer for t in path)
            if not covered:
                assert len(customer) == 1 and customer in (frozenset((2,)), frozenset((5,)))
                missing.add(mask(customer))
            type_checks += 1
        assert missing == expected_missing[root]
        utilities = tuple(payoff(path, j) for j in range(4))
        welfare = coverage(path)
        omitted = optimum - welfare
        regret = max(root_values) - utilities[0]
        margin = optimum - 2 * welfare - 3 * regret
        assert omitted <= utilities[2] + utilities[3]
        assert optimum <= 2 * welfare - utilities[0] - utilities[1]
        assert margin <= -utilities[0] - utilities[1] - 3 * regret
        # A new common-core unit customer contributes exactly 1/4 at all
        # seven root terminal profiles, so regret is unchanged; coverage and
        # OPT each rise by 1, and the compiled half margin falls by 1.
        assert all(F(1, sum(t in range(7) for t in p)) == F(1, 4) for p in paths)
        records.append({'root': root, 'actual_path': path, 'omitted_interest_masks': sorted(missing),
                        'actual_payoffs': list(map(str, utilities)), 'welfare': welfare,
                        'optimal_coverage': optimum, 'root_regret': str(regret),
                        'OPT_minus_2W_minus_3regret': str(margin),
                        'private_omissions': omitted,
                        'last_two_real_profit_budget': str(utilities[2] + utilities[3]),
                        'first_two_profit_saving': str(utilities[0] + utilities[1])})
    assert tuple(row['welfare'] for row in records) == (51, 51, 52, 51, 51, 52, 51)
    assert tuple(F(row['OPT_minus_2W_minus_3regret']) for row in records) == (-77, -77, -79, -77, -77, -79, -49)

    report = {'status': 'PASS: targeted 53-family all-root private-omission boundary',
              'source_hashes': {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
                                for name in ('endogenous_53_instance.json', 'endogenous_53_strategy.json')},
              'source_unit_customers': len(CUSTOMERS), 'original_interest_types': len(ROWS),
              'positive_depth_complete_histories': len(positive), 'positive_depth_action_comparisons': count,
              'targeted_typewise_root_checks_including_added_core_type': type_checks,
              'fixed_optimal_support_covers_all_allowed_interest_types': optimal_support,
              'optimal_multisets_checked_at_source_point': len(multisets), 'root_plans': records,
              'all_multiplicity_scope': 'Any nonnegative integer multiplicities of these types, and any added common core, conditional on the fixed positive-depth strategy remaining a legal complete SPE. Type basis directions are coverage identities, not claimed feasible SPE instances.',
              'analytic_reuse': 'The existing private-seat spectrum for the last two positive-depth players gives OPT<=2W-u1-u2 for every root and all feasible multiplicities; no root-regret credit is needed.',
              'stop': 'Do not optimize this fixed suffix cone further. This does not address shared omissions or general root-only plans.'}
    with target.open('x') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'positive_depth_complete_histories',
                                           'positive_depth_action_comparisons', 'targeted_typewise_root_checks_including_added_core_type',
                                           'fixed_optimal_support_covers_all_allowed_interest_types')}, ensure_ascii=False, indent=2))
    print('all-root compiled margins:', [row['OPT_minus_2W_minus_3regret'] for row in records])
    print('report:', target)


if __name__ == '__main__':
    main()
