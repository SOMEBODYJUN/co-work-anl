"""Exact packet audit for uniform contraction, with fresh output only.

No canonical solver, author's earlier audit, LP, floating point, or sympy.
Universal quantifiers are proved in the companion note; finite replays audit
the source packet, the claimed spectra, and exact rational witnesses.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tail'
INSTANCE = json.loads((SOURCE / 'endogenous_53_instance.json').read_text())
STRATEGY = json.loads((SOURCE / 'endogenous_53_strategy.json').read_text())
CUSTOMERS = tuple(frozenset(row['topics']) for row in INSTANCE['customers']
                  for _ in range(row['multiplicity']))
ACTIONS = {tuple(row['history']): row['action'] for row in STRATEGY['actions']}


@lru_cache(None)
def finish(history):
    return history if len(history) == 4 else finish(history + (ACTIONS[history],))


def profit(path, who, weights):
    return sum((weights[who] / sum((weights[j] for j, topic in enumerate(path)
                                   if topic in customer), F())
                for customer in CUSTOMERS if path[who] in customer), F())


def query(topic, tail, mass):
    return sum((F(1) / (1 + mass * sum(t in customer for t in tail))
                for customer in CUSTOMERS if topic in customer), F())


def static_query(topic, opponents):
    return sum((F(1, 1 + sum(t in customer for t in opponents))
                for customer in CUSTOMERS if topic in customer), F())


def positive_part(x):
    return max(F(), x)


def heterogeneous_frozen_background():
    # This is expressly the frozen-background extension, not a legal prefix
    # from this common catalog: two core clients have different old loads.
    core = frozenset((0, 1))
    topics = (core | {2}, core | frozenset(range(3, 12)), core | {12, 13})
    old_background = (0, 2) + (0,) * 12
    background = tuple(old_background[x] + (x in topics[0]) for x in range(14))
    n = 3
    histories = tuple(h for q in range(n) for h in product(range(3), repeat=q))

    def terminal(h):
        return h + (1,) * (n - len(h))

    def player_profit(path, who, mass):
        return sum((mass / (background[x] + mass * sum(x in topics[t] for t in path))
                    for x in topics[path[who]]), F())

    counts = 0
    for mass in (F(1), F(1, 2), F(2, 7)):
        for h in histories:
            for t in range(3):
                assert player_profit(terminal(h), len(h), mass) >= player_profit(terminal(h + (t,)), len(h), mass)
                counts += 1
    assert topics[1].isdisjoint({x for x in range(14) if background[x] > 0} - core)
    # A previous off-path A and a current deviation A do meet fixed positive
    # noncore background, so this audit does not silently forbid such histories.
    assert 2 in topics[0] and background[2] == 1
    mass = F(1, 2)
    k = tuple(sum(x in topics[t] for t in (1, 1, 1)) for x in range(14))
    K = lambda w: sum((F(1) / (background[x] + n * w) for x in core), F())
    a_star, spectrum = F(3), F(27, 16)
    t = a_star / mass + K(mass)
    minimum = a_star + K(F(1))
    assert t == F(298, 45) and minimum == F(41, 12)
    pool = sum((F(1) / (old_background[x] + 1 + mass * k[x])
                - F(1, old_background[x] + 1 + k[x]) for x in range(14)), F())
    assert pool == F(14, 9)
    assert pool <= spectrum * (1 / mass - 1) + K(mass) - K(F(1)) <= t - minimum
    # Correct core query denominator is b0+1+n*mass=b+n*mass.
    assert K(mass) - K(F(1)) == F(37, 180)
    root_refund = sum((F(1) / (background[x] + mass * k[x])
                       - F(1, background[x] + k[x]) for x in topics[0]), F())
    old_refund = sum((old_background[x] * (F(1) / (background[x] + mass * k[x])
                         - F(1, background[x] + k[x]))
                      for x in range(14) if old_background[x]), F())
    original_tail = n * minimum
    retained_tail = sum((player_profit((1, 1, 1), j, mass) for j in range(n)), F())
    assert root_refund == K(mass) - K(F(1))
    assert old_refund == F(1, 9)
    assert root_refund + old_refund + retained_tail == original_tail
    assert retained_tail == t * n * mass
    # Threshold below the minimum: the claim uses a positive part, not a
    # potentially negative upper bound t-minimum.
    low_t = minimum - 1
    assert positive_part(low_t - minimum) == 0
    # Pure-core a*=0 boundary, at the same heterogeneous frozen background.
    pure_t = K(mass)
    assert K(F(1)) < pure_t < sum((F(1, background[x]) for x in core), F())
    pure_pool = pure_t - K(F(1))
    assert pure_pool <= n * (pure_t - K(F(1)))
    return {'scope': 'heterogeneous frozen background extension; not a legal old prefix',
            'decision_histories': len(histories), 'finite_action_replays': counts,
            'core_initial_background': [background[x] for x in core],
            'threshold': str(t), 'original_minimum': str(minimum),
            'common_query_pool': str(pool), 'spectrum': str(spectrum),
            'core_refund': str(root_refund), 'old_background_refund': str(old_refund),
            'original_tail_profit': str(original_tail), 'retained_tail_profit': str(retained_tail),
            'pure_core_zero_fresh_case': {'threshold': str(pure_t), 'common_pool': str(pure_pool)}}


def main():
    output = HERE / 'waterfill_uniform_contraction_audit.json'
    if output.exists():
        raise FileExistsError(output)
    expected = {h for depth in range(4) for h in product(range(7), repeat=depth)}
    assert set(ACTIONS) == expected and len(CUSTOMERS) == 53
    child = {h for h in expected if h and h[0] == 6}
    assert len(child) == 57 and all(ACTIONS[h] != 6 for h in child)
    actual = finish(())
    assert actual == (6, 0, 3, 4)
    tail = actual[1:]
    k = tuple(sum(t in customer for t in tail) for customer in CUSTOMERS)
    spectrum_counts = Counter(k)
    assert spectrum_counts == {0: 21, 1: 6, 2: 15, 3: 11}
    assert not set.intersection(*(set(range(len(CUSTOMERS))) -
               {x for x, customer in enumerate(CUSTOMERS) if topic not in customer}
               for topic in range(7)))
    fresh = tuple(profit(actual, j, (F(1),) * 4) for j in range(1, 4))
    assert fresh == (F(29, 3), F(67, 6), F(67, 6))
    a_star = min(fresh)
    spectrum = sum((F(load, (load + 1) ** 2) for load in k if load), F())
    assert spectrum == F(331, 48) and a_star - spectrum == F(133, 48)
    threshold = F(28481, 2924)
    deficit = threshold - a_star
    assert deficit == F(647, 8772)
    lambda0 = a_star / threshold
    assert lambda0 == F(84796, 85443)

    # Reconstruct the matching original minimax certificate from constants,
    # without invoking an LP or importing a source audit.
    p = tuple(F(x, 5848) for x in (570, 570, 1197, 570, 570, 1197, 1174))
    dual = {a: F(n, 14620) for a, n in
            (((0, 1, 2), 370), ((0, 1, 6), 3941), ((0, 2, 6), 1481),
             ((1, 2, 6), 1481), ((3, 4, 6), 4089), ((3, 5, 6), 1629), ((4, 5, 6), 1629))}
    opponents = tuple(combinations_with_replacement(range(7), 3))
    assert sum(p) == sum(dual.values()) == 1
    assert min(sum((p[t] * static_query(t, z) for t in range(7)), F()) for z in opponents) == threshold
    assert all(sum((v * static_query(t, z) for z, v in dual.items()), F()) == threshold for t in range(7))

    replay_rows = []
    for mass in (F(1), lambda0, F(1, 3), F(2, 7)):
        weights = (F(1), mass, mass, mass)
        minimum_slack = None
        count = 0
        for h in child:
            assert ACTIONS[h] != 6
            for t in range(7):
                slack = profit(finish(h), len(h), weights) - profit(finish(h + (t,)), len(h), weights)
                assert slack >= 0, (h, t, mass, slack)
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                count += 1
        assert count == 399
        replay_rows.append({'mass': str(mass), 'action_comparisons': count, 'minimum_slack': str(minimum_slack)})

    old_pool = lambda w: sum((F(1) / (1 + w * load) - F(1, 1 + load) for load in k), F())
    credits0 = tuple(query(t, tail, lambda0) - query(t, tail, F(1)) for t in range(7))
    assert old_pool(lambda0) == F(206474219394865, 3934509249981684)
    assert max(credits0) == F(187117307516351, 4918136562477105)
    assert max(credits0) <= old_pool(lambda0) < deficit

    cases = []
    for core_size in (0, 1, 10, 1000, 10**6):
        target = threshold + F(core_size, 4)
        density_min = lambda w: a_star / w + F(core_size, 1 + 3 * w)
        lo, hi = lambda0, F(1)
        if core_size == 0:
            hi = lo
        else:
            assert density_min(lo) > target > density_min(hi)
            for _ in range(80):
                mid = (lo + hi) / 2
                if density_min(mid) >= target:
                    lo = mid
                else:
                    hi = mid
        assert density_min(lo) >= target >= density_min(hi)
        core_gain = F(core_size, 1 + 3 * lo) - F(core_size, 4)
        pool_upper = old_pool(lo) + core_gain
        assert pool_upper < deficit
        legal_credit_upper = max(query(t, tail, lo) - query(t, tail, F(1)) + core_gain for t in range(7))
        assert legal_credit_upper <= pool_upper
        original_tail = F(32) + F(3 * core_size, 4)
        retained_tail = F(32) + 3 * lo * F(core_size, 1 + 3 * lo)
        assert retained_tail + core_gain == original_tail
        assert retained_tail - target * 3 * lo >= 3
        cases.append({'core_unit_customers': core_size, 'lambda_interval': [str(lo), str(hi)],
                      'rational_lower_endpoint_is_feasible_witness': True,
                      'minimum_density_lower': str(density_min(hi)),
                      'common_query_pool_upper': str(pool_upper),
                      'legal_query_credit_upper': str(legal_credit_upper),
                      'tail_profit_above_threshold_mass_at_rational_witness': str(retained_tail - target * 3 * lo)})

    # Check the precise full-tree boundary: preserving the child plus the root
    # row does not preserve the other six root children.
    weights = (F(1), lambda0, lambda0, lambda0)
    root_slacks = tuple(profit(actual, 0, weights) - profit(finish((t,)), 0, weights) for t in range(7))
    assert min(root_slacks) == 0
    assert min(root_slacks[:6]) == F(36675150748, 3946991215) > 0
    failed = []
    for h in sorted(expected, key=lambda h: (len(h), h)):
        for t in range(7):
            slack = profit(finish(h), len(h), weights) - profit(finish(h + (t,)), len(h), weights)
            if slack < 0:
                failed.append({'history': h, 'deviation': t, 'profit_slack': str(slack)})
    assert len(failed) == 36 and all(row['history'] and row['history'][0] != 6 for row in failed)

    report = {'status': 'exact_uniform_contraction_packet_audit_pass',
              'scope': 'Complete P-child preserved; original full four-player strategy is not preserved. General proof is conditional on all-history background avoidance and S<=a_star.',
              'source_sha256': {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
                                for name in ('endogenous_53_instance.json', 'endogenous_53_strategy.json')},
              'source_unit_customers': len(CUSTOMERS), 'source_complete_histories': len(expected),
              'P_child_complete_histories': len(child), 'P_child_prescribed_P_actions': 0,
              'noncore_actual_load_counts': dict(sorted(spectrum_counts.items())),
              'fresh_utilities': list(map(str, fresh)), 'a_star': str(a_star), 'S': str(spectrum),
              'a_star_minus_S': str(a_star - spectrum), 'true_original_v4': str(threshold),
              'matching_static_opponent_multisets': len(opponents), 'original_low_tail_deficit': str(deficit),
              'lambda0': str(lambda0), 'complete_child_finite_replays': replay_rows,
              'c0_common_query_pool': str(old_pool(lambda0)), 'c0_max_legal_query_credit': str(max(credits0)),
              'all_core_cases': cases, 'original_root_row_c0_slacks': list(map(str, root_slacks)),
              'other_root_children_failed_comparisons': failed,
              'heterogeneous_background_and_boundary_audit': heterogeneous_frozen_background(),
              'historical_narrow_obstruction_scope_correction': 'The 53-customer fixed-high-tail obstruction requires both originally high tails to keep mass 1; this audit supplies a broader uniform-mass repair. Frozen earlier evidence is not rewritten.'}
    with output.open('x') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'P_child_complete_histories', 'P_child_prescribed_P_actions',
                                           'fresh_utilities', 'a_star', 'S', 'lambda0', 'c0_common_query_pool',
                                           'c0_max_legal_query_credit')}, ensure_ascii=False, indent=2))
    print('other-root-child failed comparisons:', len(failed))
    print('report:', output)


if __name__ == '__main__':
    main()
