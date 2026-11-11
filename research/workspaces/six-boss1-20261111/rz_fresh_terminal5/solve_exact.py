"""Exact full-cone completion for the R20--R22 frozen family1 interface.

All 16 histograms, all 30 named ordered off-diagonal pairs, all four old
R/Z states, and the full product of two 16-state hidden sets are retained.
The full product separates exactly, and each factor is a fractional
knapsack with one upper query budget.  No parameter grid or optimizer.
Only the directory containing this file is written.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
POINT = REPO / 'research/workspaces/six-boss1-20261111/union_augmented_lp/augmented_lp_exact.json'
PACKAGE = REPO / 'research/workspaces/six-boss2-20261111-cross/coverage_bridge/selected_prefix_tail_5752.json'
POINT_SHA = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
PACKAGE_SHA = '595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50'
BITS = tuple(product((0, 1), repeat=4))
WORDS = tuple(product((0, 1), repeat=3))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def clean(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [clean(v) for v in x]
    return x


def save(name, value):
    (HERE / name).write_text(json.dumps(clean(value), ensure_ascii=False, indent=2) + '\n')


def share(num, den):
    if den == 0:
        assert num == 0
        return Q(0)
    return Q(num, den)


def load_sources():
    assert digest(POINT) == POINT_SHA
    assert digest(PACKAGE) == PACKAGE_SHA
    point = json.loads(POINT.read_text())
    package = json.loads(PACKAGE.read_text())
    params = {}
    for name, number, scale, expected in [('A', 2, 999, (999, 139)), ('B', 13, 10000, (10000, 1358))]:
        cut = package['cuts'][number - 1]
        assert (cut['source'], cut['k'], Q(cut['delta'])) == (4, 3, Q(1, 2))
        alpha = {k.replace('@Bj', '@Cj'): scale * Q(v) for k, v in cut['alpha'].items()}
        beta = {k: scale * Q(v) for k, v in cut['beta'].items()}
        assert all(v >= 0 and v.denominator == 1 for v in (*alpha.values(), *beta.values()))
        src = alpha['sourceT'] + alpha['sourceC'] + beta['source']
        price = sum(v for k, v in alpha.items() if k.startswith('price:')) + beta['alpha_mid'] + beta['alpha_last']
        assert (src, price) == expected
        assert tuple(scale * Q(v) for v in cut['budget']) == (*expected, Q(0))
        params[name] = dict(number=number, scale=scale, alpha=alpha, beta=beta, budget=[src, price, 0])
    return point, params


@lru_cache(None)
def tail(branch, p, D, x, y, n):
    # Explicit four-piece normalized Bellman solution for the original
    # frozen tail.  The independent verifier solves all four policies.
    tau = Q(n - x - y, 4)
    if branch == 'A':
        a, m, ell, M, q = 254, 6, 4, 67, 11 * x + 11 * y + 45 * tau
    else:
        a, m, ell, M, q = 2488, 61, 43, 659, 110 * x + 110 * y + 439 * tau
    e00a, e00b = q / (p + 1), Q(m, D) + q / (p + 2)
    e01 = (q - M) / (p + 1) + Q(ell, D)
    e10 = Q(a, p + 2) + Q(m, D) + q / (p + 3)
    e11 = (a - M + q) / (p + 3) + Q(m + ell, D)
    return (min(e00a, e00b, (e01 + e11) / 2, (2 * e01 + e10) / 3),
            min(e11, (e10 + e00a) / 2, (e10 + e00b) / 2, (2 * e10 + e01) / 3))


@lru_cache(None)
def cost(branch, p, D, t, hidden, x, y, ci, cj, a6, n):
    b, c, j, v = hidden
    tau = Q(n - x - y, 4)
    if branch == 'A':
        q1, qp = 36 * x + 145 * ci + 36 * cj, 2 * a6 + 5 * x + 4 * cj + 13 * tau
        val = (share(431 * t - 24 * b - 241 * c, p + t + b + c)
               + share(314 * c - j - 126 * v, p + c + j + v)
               + Q(2 * b + 64 * j + 63 * v, D)
               + Q(q1, p + t + b + 1) + (124 * b + tau) / (p + c + j + 1)
               + (qp + 24 * c) / (p + t + 1)
               - (qp * c + 24 * b) / ((p + t + 1) * (p + t + 2))
               + (tau + b) / (p + c + 1)
               - (tau * b + j) / ((p + c + 1) * (p + c + 2)))
    else:
        qq, uu = Q(103 * n + x + y, 4), Q(39 * n + x + y, 4)
        val = (share(4325 * t - 2196 * c, p + t + b + c)
               + share(3187 * c - 59 * j - 1295 * v, p + c + j + v)
               + Q(630 * j + 624 * v, D)
               + Q(34 * j + 2162 * a6, p + t + b + 1)
               + (1081 * b + qq) / (p + c + j + 1)
               + (uu + 59 * v) / (p + c + 1)
               - (uu * v + 59 * j) / ((p + c + 1) * (p + c + 2)))
    return val + tail(branch, p, D, x, y, n)[v]


def parse(point):
    hist, groups = {}, defaultdict(dict)
    current = None
    for colno, col in enumerate(point['columns'][:4849]):
        if col['kind'] == 'hist':
            current = colno
            words = tuple(w for w, count in zip(WORDS, col['hist']) for _ in range(count))
            assert len(words) == 6
            hist[colno] = dict(column=colno, actual_bits=col['actual_bits'], hist=col['hist'],
                               words=words, mass=Q(col['weight']), n=col['d'])
        elif col['kind'] == 'joint-reply':
            family, diag, wi, wj = col['group']
            key = (family, diag, tuple(wi), tuple(wj))
            groups[current].setdefault(key, {})[tuple(col['state'])] = Q(col['weight'])
    assert len(hist) == 16
    for colno, block in groups.items():
        for key, states in block.items():
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            states[(0, 0)] = hist[colno]['mass'] - sum(states.values(), Q(0))
            assert min(states.values()) >= 0
    incomes = [sum((h['mass'] * share(int(h['actual_bits'][i]), sum(map(int, h['actual_bits']))) for h in hist.values()), Q(0)) for i in range(6)]
    assert sum(incomes, Q(0)) == Q(point['W'])
    assert sum((h['mass'] for h in hist.values()), Q(0)) == Q(point['O']) == 1
    return hist, groups, incomes


def build_states(hist, groups):
    states = []
    for colno, h in hist.items():
        a = tuple(map(int, h['actual_bits']))
        p, P, D, n = sum(a[:3]), sum(a[:4]), sum(a[:5]) + 1, h['n']
        pairs = defaultdict(list)
        for i in range(6):
            for j in range(6):
                if i != j:
                    pairs[(h['words'][i], h['words'][j])].append((i, j))
        assert sum(map(len, pairs.values())) == 30
        for (wi, wj), indices in sorted(pairs.items()):
            x, y, ci, cj = wi[0], wj[0], wi[2], wj[2]
            for r, z in product((0, 1), repeat=2):
                rawmass = groups[colno][1, 0, wi, wj][r, z]
                ac = [cost('A', p, D, r, hh, x, y, ci, cj, a[5], n) for hh in BITS]
                bc = [cost('B', p, D, z, hh, x, y, 0, 0, a[5], n) for hh in BITS]
                rec = dict(id=len(states), hist_column=colno, old_state=(r, z), family=1, diagonal=0,
                           wi=wi, wj=wj, named_pairs=indices, orbit_count=len(indices),
                           hist_mass=h['mass'], old_group_mass=rawmass, mass=Q(len(indices), 30) * rawmass,
                           actual_bits=h['actual_bits'], n=n, p=p, P=P, D=D,
                           denom_R=p + x + cj + 1, denom_Z=P + r + 1,
                           fixed_Z_cost=(Q(n, 6) - z) / (P + r + 1), A_costs=ac, B_costs=bc)
                for branch, values in [('A', ac), ('B', bc)]:
                    arg = [min((i for i, hh in enumerate(BITS) if hh[3] == v), key=lambda i: (values[i], i)) for v in (0, 1)]
                    rec[branch + '_argmin_by_v'] = arg
                    rec[branch + '_min_by_v'] = [values[i] for i in arg]
                states.append(rec)
    assert sum((s['mass'] for s in states), Q(0)) == 1
    assert sum(s['orbit_count'] for s in states) == 16 * 30 * 4
    return states


def solve_knapsack(branch, states, budget):
    denom_key, anchor_index = ('denom_Z', 1) if branch == 'A' else ('denom_R', 0)
    capacity = sum((s['mass'] * s['old_state'][anchor_index] / s[denom_key] for s in states), Q(0))
    base = sum((s['mass'] * s[branch + '_min_by_v'][0] for s in states), Q(0))
    theta = [Q(0)] * len(states)
    items = []
    for s in states:
        c0, c1 = s[branch + '_min_by_v']
        if c1 < c0 and s['mass'] > 0:
            items.append(((c1 - c0) * s[denom_key], s['id'], s['mass'] / s[denom_key]))
    items.sort()
    remaining = capacity
    marginal = Q(0)
    for slope, i, width in items:
        take = min(remaining, width)
        theta[i] = take / width
        remaining -= take
        if take:
            marginal = -slope
        if take < width:
            # This is also valid when capacity is exactly exhausted at the
            # preceding item: any endpoint subgradient works.
            marginal = -slope
            break
    if remaining > 0 or not items:
        marginal = Q(0)
    value = base + sum((s['mass'] * theta[s['id']] * (s[branch + '_min_by_v'][1] - s[branch + '_min_by_v'][0]) for s in states), Q(0))
    query_cost = -capacity + sum((s['mass'] * theta[s['id']] / s[denom_key] for s in states), Q(0))
    assert query_cost <= 0
    # An exact dual/KKT identity certifies the entire continuous knapsack,
    # rather than just a greedy returned feasible assignment.
    dual_value = sum((s['mass'] * min(s[branch + '_min_by_v'][v] + marginal * Q(v - s['old_state'][anchor_index], s[denom_key]) for v in (0, 1)) for s in states), Q(0))
    assert dual_value == value
    assert marginal >= 0 and marginal * query_cost == 0
    slack = budget - value
    return dict(branch=branch, budget=budget, query_capacity=capacity, baseline_v0_cost=base,
                minimum_cost=value, exact_slack=slack, slack_float=float(slack),
                query_cost=query_cost, query_slack=-query_cost, dual_multiplier=marginal,
                exact_dual_value=dual_value, feasible=slack >= 0,
                probabilities_v1=theta, fractional_state_ids=[i for i, q in enumerate(theta) if 0 < q < 1],
                v1_state_count=sum(q > 0 for q in theta), negative_slope_items=len(items),
                complete_sorted_items=items)


def main():
    started = time.monotonic()
    point, params = load_sources()
    hist, groups, incomes = parse(point)
    states = build_states(hist, groups)
    budgets = dict(A=999 * incomes[3] + 139 * incomes[5], B=10000 * incomes[3] + 1358 * incomes[5])
    sols = {branch: solve_knapsack(branch, states, budgets[branch]) for branch in ('A', 'B')}
    zslack = -sum((s['mass'] * s['fixed_Z_cost'] for s in states), Q(0))
    assert zslack > 0
    old_min = {branch: budgets[branch] - sum((s['mass'] * min(s[branch + '_min_by_v']) for s in states), Q(0)) for branch in ('A', 'B')}
    print('histograms', len(hist), 'zero histograms', sum(h['mass'] == 0 for h in hist.values()),
          'orbit old states', len(states), 'literal old states', sum(s['orbit_count'] for s in states), flush=True)
    print('A exact optimal slack float', sols['A']['slack_float'], 'B', sols['B']['slack_float'], 'Z', float(zslack), flush=True)
    print('fractional state IDs', {b: sols[b]['fractional_state_ids'] for b in sols}, flush=True)
    save('inputs_exact.json', dict(point_path=str(POINT.relative_to(REPO)), point_sha256=POINT_SHA,
                                  package_path=str(PACKAGE.relative_to(REPO)), package_sha256=PACKAGE_SHA,
                                  hidden_domain=BITS, hidden_joint_domain=[(i, j) for i in range(16) for j in range(16)],
                                  parameters=params, histograms=list(hist.values()), incomes=incomes, budgets=budgets))
    save('local_tables_exact.json', dict(scope='Every old orbit state including zero masses; all 16 x 16 hidden pairs represented without restriction.',
                                      state_count=len(states), states=states))
    save('knapsack_exact.json', dict(solutions=sols, original_min_slacks=old_min, old_Z_slack=zslack))
    feasible = all(s['feasible'] for s in sols.values())
    completion = []
    if feasible:
        for s in states:
            i = s['id']
            ta, tb = sols['A']['probabilities_v1'][i], sols['B']['probabilities_v1'][i]
            atom_rows = []
            for va, vb in product((0, 1), repeat=2):
                prob = (ta if va else 1 - ta) * (tb if vb else 1 - tb)
                atom_rows.append(dict(hA_index=s['A_argmin_by_v'][va], hB_index=s['B_argmin_by_v'][vb],
                                      probability=prob, averaged_mass=s['mass'] * prob,
                                      per_named_pair_mass=s['old_group_mass'] * prob / 30))
            assert sum((a['probability'] for a in atom_rows), Q(0)) == 1
            completion.append(dict(state_id=i, probability_vA1=ta, probability_vB1=tb, atoms=atom_rows))
        slacks = dict(alpha=sols['A']['exact_slack'], beta=sols['B']['exact_slack'],
                      lam=zslack, mu=sols['B']['query_slack'], nu=sols['A']['query_slack'])
        assert all(v >= 0 for v in slacks.values())
        save('completion_exact.json', dict(scope='One common conditional distribution for each old R/Z state, completed on the full 256 hidden pairs; omitted hidden pairs have zero probability.',
                                          point_sha256=POINT_SHA, slacks=slacks, rows=completion))
    else:
        separating = []
        for branch in ('A', 'B'):
            sol = sols[branch]
            if not sol['feasible']:
                weights = dict(alpha=Q(branch == 'A'), beta=Q(branch == 'B'), lam=Q(0), mu=Q(0), nu=Q(0))
                weights['nu' if branch == 'A' else 'mu'] = sol['dual_multiplier']
                separating.append(dict(branch=branch, weights=weights, exact_slack=sol['exact_slack']))
        save('separating_weights_exact.json', separating)
    summary = dict(status='EXACT_COMMON_COMPLETION' if feasible else 'EXACT_SEPARATING_WEIGHTS',
                   complete_five_nonnegative_weight_cone=feasible, source_zero_faces_retained=True,
                   point_sha256=POINT_SHA, package_sha256=PACKAGE_SHA,
                   counts=dict(histograms=len(hist), zero_histograms=sum(h['mass'] == 0 for h in hist.values()),
                               orbit_old_states=len(states), positive_orbit_old_states=sum(s['mass'] > 0 for s in states),
                               literal_old_states=16 * 30 * 4, full_joint_candidates_by_orbit=len(states) * 256,
                               full_joint_candidates_literal=16 * 30 * 4 * 256),
                   slacks_float=dict(A=sols['A']['slack_float'], B=sols['B']['slack_float'], Z=float(zslack)),
                   elapsed_seconds=time.monotonic()-started, solver_sha256=digest(Path(__file__)))
    save('solve_summary.json', summary)
    print(summary['status'], 'elapsed', summary['elapsed_seconds'], flush=True)


if __name__ == '__main__':
    main()
