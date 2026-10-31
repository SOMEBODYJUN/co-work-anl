"""New bounded EH arithmetic, not a replay of any missing historical program.

All catalog maxima below are finite enumeration of fixed static inputs.
No SPE search/check, LP/MILP, historical DAG main or network is called.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from math import factorial
from pathlib import Path
import json
import sys


def add(q, b):
    return tuple(x + y for x, y in zip(q, b))


def unit(p, a):
    return tuple(int(b == a) for b in range(p))


@lru_cache(None)
def vectors(p, n):
    return tuple(tuple(z.count(a) for a in range(p))
                 for z in combinations_with_replacement(range(p), n))


def harmonic(n):
    return sum((F(1, j) for j in range(1, n + 1)), F(0))


class Model:
    def __init__(self, names, rows):
        self.names, self.p = names, len(names)
        self.rows = [(frozenset(B), n) for B, n in rows]
        assert all(isinstance(n, int) and n > 0 and B and all(0 <= a < self.p for a in B)
                   for B, n in self.rows)

    @lru_cache(None)
    def phi(self, q):
        return sum((n * harmonic(sum(q[a] for a in B)) for B, n in self.rows), F(0))

    def pay(self, q, a):
        assert q[a] > 0
        return sum((F(n, sum(q[b] for b in B)) for B, n in self.rows if a in B), F(0))

    def query(self, b, a):
        return self.pay(add(b, unit(self.p, a)), a)

    def welfare(self, q):
        return sum(n for B, n in self.rows if any(q[a] for a in B))

    @lru_cache(None)
    def maximum(self, q, k):
        values = [(self.phi(add(q, b)), b) for b in vectors(self.p, k)]
        best = max(x[0] for x in values)
        return best, tuple(b for value, b in values if value == best)

    def specification(self):
        return {'topics': self.names, 'types': [{'topics': sorted(B), 'multiplicity': n}
                                              for B, n in self.rows]}


def membership_checks():
    first, second = [], []
    backgrounds = [F(0), F(1, 2), F(1), F(2), F(10 ** 40)]
    for b in backgrounds:
        for A, B, D, T in product([0, 1], repeat=4):
            q = lambda X, Y: F(X, 1) / (b + 1 + Y)
            slack = 2 * q(T, D) + q(D, A) - q(T, A) - q(T, B)
            assert slack >= 0
            first.append({'b': str(b), 'A_B_D_T': [A, B, D, T], 'slack': str(slack)})
        for A, B, T in product([0, 1], repeat=3):
            slack = F(A, 1) / (b + 1 + B) - (F(T, 1) / (b + 1 + B) - F(T, 1) / (b + 1 + A))
            assert slack >= 0
            second.append({'b': str(b), 'A_B_T': [A, B, T], 'slack': str(slack)})
    return {'P1_rows': first, 'P2_rows': second}


def small_central_checks():
    # Literal x1,x2,y,z; all topics and customers are fixed before enumeration.
    model = Model(['A', 'B', 'C', 'D'], [([0], 2), ([1, 2], 1), ([1, 3], 1)])
    bonuses, identities = [], 0
    for k in range(3):
        for length in range(4):
            for q in vectors(4, length):
                maximum, opts = model.maximum(q, k)
                for opt in opts:
                    total = F(0)
                    for a in range(4):
                        if not q[a]:
                            continue
                        minus = tuple(q[b] - int(a == b) for b in range(4))
                        delta = model.maximum(minus, k)[0] - model.phi(add(minus, opt))
                        assert delta >= 0
                        total += q[a] * delta
                    bound = sum((F(n * sum(q[a] for a in B) * (k - sum(opt[a] for a in B)),
                                   (sum(q[a] for a in B) + sum(opt[a] for a in B))
                                   * (sum(q[a] for a in B) + k))
                                 for B, n in model.rows if sum(q[a] for a in B)), F(0))
                    assert total <= bound
                    bonuses.append({'k': k, 'q': q, 'optimizer': opt,
                                    'bonus_sum': str(total), 'bound': str(bound)})
                for actual in vectors(4, k):
                    gamma = maximum - model.phi(add(q, actual))
                    assert gamma >= 0
                    for a in range(4):
                        if not q[a]:
                            continue
                        minus = tuple(q[b] - int(a == b) for b in range(4))
                        delta = model.maximum(minus, k)[0] - model.phi(add(minus, actual))
                        expected = maximum - model.maximum(minus, k)[0] + delta - gamma
                        assert expected == model.pay(add(q, actual), a)
                        identities += q[a]
    distributions = [tuple(F(int(a == b)) for a in range(4)) for b in range(4)] + [(F(1, 4),) * 4]
    safety = []
    for k in range(3):
        for active in range(1, 4):
            m = active + k
            for distribution in distributions:
                guaranteed = min(sum((distribution[a] * model.query(B, a) for a in range(4)), F(0))
                                 for B in vectors(4, m - 1))
                for q in vectors(4, active - 1):
                    base, opts = model.maximum(q, k)
                    fixed = opts[0]  # Selected once, before the sampled query.
                    actual = sum((distribution[a] * (model.maximum(add(q, unit(4, a)), k)[0] - base)
                                  for a in range(4)), F(0))
                    frozen = sum((distribution[a] * model.query(add(q, fixed), a) for a in range(4)), F(0))
                    assert actual >= frozen >= guaranteed
                    safety.append({'k': k, 'active': active, 'q': q, 'p': [str(x) for x in distribution],
                                   'fixed_optimizer': fixed, 'central_marginal_mean': str(actual),
                                   'fixed_background_mean': str(frozen), 'original_guarantee': str(guaranteed)})
    q = (1, 0, 0, 1)
    points = [q, add(q, unit(4, 2)), add(q, unit(4, 3)), add(add(q, unit(4, 2)), unit(4, 3))]
    values = [model.maximum(z, 1)[0] for z in points]
    assert values == [F(9, 2), F(5), F(29, 6), F(11, 2)]
    assert values[0] + values[3] - values[1] - values[2] == F(1, 6)
    return {'input': model.specification(), 'bonus_rows': bonuses, 'payoff_identity_position_checks': identities,
            'safety_rows': safety, 'envelope_counterexample': {'prefixes': points, 'M1': list(map(str, values)),
            'optimizers': [model.maximum(z, 1)[1] for z in points], 'submodularity_deficit': '1/6'}}


def sharp_family(k, a, t, g, name):
    assert a > 0 and t > 0 and t == F(a, k) * (harmonic(k + 1) - 1)
    names = ['A'] + ['B' + str(i) for i in range(1, k + 1)] + ['D' + str(i) for i in range(1, k + 1)]
    rows = [([0] + list(range(k + 1, 2 * k + 1)), a)]
    rows += [([i], t) for i in range(1, k + 1)]
    rows += [([i, k + j], g) for i in range(1, k + 1) for j in range(1, k + 1)]
    model = Model(names, rows); q = unit(model.p, 0); zero = (0,) * model.p
    B = tuple(int(1 <= i <= k) for i in range(model.p)); D = tuple(int(i > k) for i in range(model.p))
    mq, opts_q = model.maximum(q, k); m0, opts_0 = model.maximum(zero, k)
    assert set(opts_q) == {B, D} and opts_0 == (D,)
    assert mq == k * k * g + a * harmonic(k + 1)
    assert m0 == k * k * g + a * harmonic(k)
    bonus = m0 - model.phi(B)
    assert bonus == F(k * a, k + 1) and model.pay(add(q, B), 0) == a and mq - m0 == F(a, k + 1)
    return {'name': name, 'k': k, 'a': a, 't': t, 'g': g, 'large_g_sufficient_condition': g > 2 * k * t,
            'input': model.specification(), 'response_multisets': [
                {'counts': z, 'potential_with_A': str(model.phi(add(q, z))), 'potential_without_A': str(model.phi(z))}
                for z in vectors(model.p, k)], 'optimizers_with_A': opts_q, 'optimizers_without_A': opts_0,
            'M_with_A': str(mq), 'M_without_A': str(m0), 'Phi_B': str(model.phi(B)),
            'bonus': str(bonus), 'prefix_player_payoff': a, 'reduced_deletion_marginal': str(mq - m0),
            'bonus_over_payoff': str(bonus / a), 'SPE_claim': False}


def static_shared_family(m):
    r = m - 1
    names = ['A' + str(i) for i in range(r)] + ['B', 'T']
    names += [s + str(i) for i in range(r) for s in ['D', 'E']]
    B, T = r, r + 1; Ds = [r + 2 + 2 * i for i in range(r)]; Es = [d + 1 for d in Ds]
    rows = [([i, Ds[i]], 2) for i in range(r)] + [([i, Es[i]], 2) for i in range(r)]
    rows += [([B], 3), ([T], 3), ([B] + Ds + Es, 2), ([T] + Ds + Es, 2)]
    model = Model(names, rows); path = list(range(r)) + [B]
    q = tuple(path.count(a) for a in range(model.p)); bg = tuple(int(a in Ds) for a in range(model.p))
    queries = [model.query(bg, a) for a in range(model.p)]
    for i in range(r):
        assert queries[i] == 3 and queries[Ds[i]] == 1 + F(4, m) and queries[Es[i]] == 2 + F(4, m)
    assert queries[B] == queries[T] == 3 + F(2, m) == max(queries)
    frozen = sum((model.query(tuple(q[b] - int(a == b) for b in range(model.p)), T) for a in path), F(0))
    W = model.welfare(q); assert W == 4 * m + 1 and frozen == 5 * m
    alpha = F(m - 1, m)
    G = sum((F(n, 1) / (1 + alpha * sum(q[a] for a in likes)) for likes, n in model.rows if sum(q[a] for a in likes)), F(0))
    assert G == F((4 * m + 1) * m, 2 * m - 1)
    return {'m': m, 'input': model.specification(), 'actual_tuple_static_only': path, 'W': W,
            'F_T': str(frozen), 'F_T_minus_W': str(frozen - W), 'G': str(G),
            'early_player_fractional_margin': str(4 - 5 + G / m),
            'legal_oblivious_background': Ds, 'all_query_values': list(map(str, queries)),
            'v_m_upper_bound': str(max(queries)), 'W_minus_m_upper_bound': str(W - m * max(queries)),
            'SPE_claim': False}


def nine_topic_static():
    model = Model(['A', 'B', 'T', 'D', 'E', 'P0', 'P1', 'P2', 'P3'],
                  [([0, 3], 2), ([0, 4], 2), ([1], 3), ([2], 3), ([1, 3, 4], 2), ([2, 3, 4], 2)]
                  + [([i], 4) for i in range(5, 9)])
    path = [5, 6, 7, 8, 0, 1]; q = tuple(path.count(a) for a in range(9)); bg = (0, 0, 0, 1, 0, 1, 1, 1, 1)
    values = [model.query(bg, a) for a in range(9)]
    alpha = F(5, 6)
    gs = [sum((F(n, 1) / (1 + alpha * sum(q[b] for b in likes)) for likes, n in model.rows if a in likes), F(0))
          for a in range(9)]
    G = sum((F(n, 1) / (1 + alpha * sum(q[b] for b in likes)) for likes, n in model.rows if sum(q[b] for b in likes)), F(0))
    opts = [(model.welfare(tuple(int(a in J) for a in range(9))), J)
            for size in range(7) for J in combinations(range(9), size)]
    opt = max(x[0] for x in opts)
    assert values == [3, 4, 4, 3, 4, 2, 2, 2, 2]
    assert G == F(150, 11) and max(gs) == 5 and 25 + G - 6 * max(gs) == F(95, 11) and opt == 26
    return {'input': model.specification(), 'static_path': path, 'oblivious_background': bg,
            'query_values': list(map(str, values)), 'fractional_queries': list(map(str, gs)), 'G': str(G),
            'fractional_margin': str(25 + G - 6 * max(gs)), 'OPT6': opt,
            'optimal_supports': [J for value, J in opts if value == opt], 'SPE_checked_in_this_program': False}


def main():
    out = Path(sys.argv[1]); assert sys.flags.optimize == 0 and out.is_dir() and not list(out.iterdir())
    family = []
    for k in [1, 2, 3]:
        a = k * factorial(k + 1); t = F(a, k) * (harmonic(k + 1) - 1); assert t.denominator == 1
        family.append(sharp_family(k, a, int(t), 2 * k * int(t) + 1, 'sufficient_large_grid'))
    family.append(sharp_family(2, 12, 5, 3, 'source_small_k2'))
    report = {'scope': 'new finite static arithmetic and catalog-maximum checks; no original program/SPE/DAG replay',
              'membership': membership_checks(), 'central_fixed_four_customer': small_central_checks(),
              'sharp_family_members': family, 'shared_index_static_family': [static_shared_family(m) for m in [2, 3, 4, 5, 6, 7, 8, 20]],
              'nine_topic_static_only': nine_topic_static(), 'original_entries': 0, 'LP_MILP_calls': 0,
              'full_history_SPE_checks': 0, 'universal_half_claim': False}
    (out / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    central = report['central_fixed_four_customer']
    print(json.dumps({'status': 'pass', 'P1_memberships': len(report['membership']['P1_rows']),
                      'P2_memberships': len(report['membership']['P2_rows']), 'central_bonus_rows': len(central['bonus_rows']),
                      'central_safety_rows': len(central['safety_rows']), 'payoff_identity_positions': central['payoff_identity_position_checks'],
                      'sharp_family_members': len(family), 'sharp_response_multisets': sum(len(x['response_multisets']) for x in family),
                      'shared_index_members': len(report['shared_index_static_family']), 'original_entries': 0,
                      'LP_MILP_calls': 0, 'new_SPE_checks': 0}))


if __name__ == '__main__':
    main()
