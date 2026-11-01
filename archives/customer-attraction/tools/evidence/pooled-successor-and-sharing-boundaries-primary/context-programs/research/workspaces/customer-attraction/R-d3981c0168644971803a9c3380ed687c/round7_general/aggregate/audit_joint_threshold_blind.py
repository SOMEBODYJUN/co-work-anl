"""Exact, bounded audit of the general joint-threshold contract.

No author code, repository model, LP package or SPE solver is imported.
The abstract menu is only a polytope test, not a realizable-CAG assertion.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def vertices(groups):
    """All possible basic supports: one per group, or one mixed group."""
    ans = []
    threshold = sum(F(g['n']) * g['theta'] for g in groups)
    G = len(groups)

    def add(rows):
        vv = sum(x * groups[g]['o'][o]['v'] for g, o, x in rows)
        if vv < threshold:
            return
        dd = sum(x * groups[g]['o'][o]['d'] for g, o, x in rows)
        ans.append((dd, rows))

    for picks in product(*(range(len(g['o'])) for g in groups)):
        add([(g, o, F(groups[g]['n'])) for g, o in enumerate(picks)])
    for mixed in range(G):
        rest = [g for g in range(G) if g != mixed]
        for picks in product(*(range(len(groups[g]['o'])) for g in rest)):
            fixed = [(g, o, F(groups[g]['n'])) for g, o in zip(rest, picks)]
            fixed_v = sum(x * groups[g]['o'][o]['v'] for g, o, x in fixed)
            for a, b in combinations(range(len(groups[mixed]['o'])), 2):
                va, vb = (groups[mixed]['o'][o]['v'] for o in (a, b))
                if va == vb:
                    continue
                n = F(groups[mixed]['n'])
                xb = (threshold - fixed_v - n * va) / (vb - va)
                if 0 <= xb <= n:
                    add(fixed + [(mixed, a, n-xb), (mixed, b, xb)])
    assert ans
    return ans


def solve_round(groups):
    cost, rows = min(vertices(groups), key=lambda z: z[0])
    plan = {g: {} for g in range(len(groups))}
    for g, o, x in rows:
        if x:
            plan[g][o] = x
    mixed = [g for g, pp in plan.items() if len(pp) == 2]
    assert len(mixed) <= 1
    if mixed:
        g = mixed[0]
        a, b = sorted(plan[g], key=lambda o: groups[g]['o'][o]['v'])
        high = plan[g][b]
        rounded = -((-high.numerator) // high.denominator)
        plan[g] = {a: F(groups[g]['n'] - rounded), b: F(rounded)}
    D = max((max(o['d'] for o in g['o']) - min(o['d'] for o in g['o'])
             for g in groups), default=F())
    out = []
    for g, pp in plan.items():
        assert sum(pp.values()) == groups[g]['n']
        for o, x in pp.items():
            assert x.denominator == 1 and x >= 0
            out.extend((g, o) for _ in range(int(x)))
    rounded_d = sum(groups[g]['o'][o]['d'] for g, o in out)
    rounded_v = sum(groups[g]['o'][o]['v'] for g, o in out)
    assert rounded_v >= sum(g['n'] * g['theta'] for g in groups)
    assert rounded_d <= cost + D
    return cost, rounded_d, out, D


def lines(menu):
    return [(o['d'], menu['theta'] - o['v']) for o in menu['o']]


def times(menus):
    ll = [line for menu in menus for line in lines(menu)]
    ts = {F()}
    for (a, b), (c, d) in combinations(ll, 2):
        if b != d:
            t = (c-a)/(b-d)
            if t >= 0:
                ts.add(t)
    return sorted(ts)


def f(menu, t):
    return min(a + t*b for a, b in lines(menu))


def utility(actions, background, profile, role):
    return sum((F(1, background[x] + sum(x in actions[a] for a in profile))
                for x in actions[profile[role]]), F())


def menus_r3(actions, background):
    K = len(actions)
    result = []
    for A in range(K):
        oo = []
        mins = []
        for B in range(K):
            best = max(utility(actions, background, (A, B, C), 2) for C in range(K))
            replies = [C for C in range(K)
                       if utility(actions, background, (A, B, C), 2) == best]
            for C in replies:
                oo.append({'d': utility(actions, background, (A, B, C), 0),
                           'v': utility(actions, background, (A, B, C), 1),
                           'B': B, 'C': C})
            mins.append(min(o['v'] for o in oo if o['B'] == B))
        result.append({'n': 1, 'theta': max(mins), 'o': oo})
    return result


def main():
    # Each theta is independently consistent with max_B min_options v:
    # B=0 has the first two options; B=1 has the constant option.
    abstract = [
        {'n': 1, 'theta': F(1), 'o': [
            {'d': F(0), 'v': F(0)}, {'d': F(2), 'v': F(2)},
            {'d': F(1), 'v': F(1)}]},
        {'n': 1, 'theta': F(2), 'o': [
            {'d': F(0), 'v': F(0)}, {'d': F(8), 'v': F(4)},
            {'d': F(4), 'v': F(2)}]},
    ]
    tt = times(abstract)
    common = max(sum(f(g, t) for g in abstract) for t in tt)
    separate = sum(max(f(g, t) for t in tt) for g in abstract)
    lp, rounded, _, D = solve_round(abstract)
    assert common == lp == 4 and separate == 5
    assert common < separate
    # Integer group masses larger than one exercise the same rounding kernel.
    large = [dict(abstract[0], n=3), dict(abstract[1], n=2)]
    large_lp, large_round, _, large_D = solve_round(large)
    assert large_lp == max(sum(g['n'] * f(g, t) for g in large) for t in tt)

    actions = [({0, 1}, {2, 3}, {1, 2, 3}),
               ({0, 1, 2}, {0, 3}, {2, 3})]
    bg = [[0]*4, [0]*4]
    menus = [menus_r3(a, b) for a, b in zip(actions, bg)]
    all_times = times([g for mm in menus for g in mm])
    psi = max(sum(max(f(g, t) for g in mm) for mm in menus) for t in all_times)
    global_D = max(max(o['d'] for o in g['o']) - min(o['d'] for o in g['o'])
                   for mm in menus for g in mm)
    child_checks = last_checks = 0
    records = []
    for AA in product(range(3), repeat=2):
        gg = [menus[k][A] for k, A in enumerate(AA)]
        val, rd, plan, _ = solve_round(gg)
        assert val == max(sum(f(g, t) for g in gg) for t in all_times)
        assert rd <= psi + global_D
        selected = [None, None]
        for g, o in plan:
            selected[g] = gg[g]['o'][o]
        BB = tuple(o['B'] for o in selected)
        prescribed_v = sum(o['v'] for o in selected)
        assert prescribed_v >= sum(g['theta'] for g in gg)
        for bb in product(range(3), repeat=2):
            if bb == BB:
                chosen = selected
            else:
                chosen = [min((o for o in gg[k]['o'] if o['B'] == bb[k]),
                              key=lambda o: o['v']) for k in range(2)]
            cc = tuple(o['C'] for o in chosen)
            next_v = sum(utility(actions[k], bg[k], (AA[k], bb[k], cc[k]), 1)
                         for k in range(2))
            assert prescribed_v >= next_v
            child_checks += 1
            last_v = sum(utility(actions[k], bg[k], (AA[k], bb[k], cc[k]), 2)
                         for k in range(2))
            for alt in product(range(3), repeat=2):
                assert last_v >= sum(utility(actions[k], bg[k],
                                            (AA[k], bb[k], alt[k]), 2)
                                     for k in range(2))
                last_checks += 1
        records.append({'A': AA, 'LP': val, 'rounded_current': rd})

    # r=2, a legal one-player background in each component.
    bg2 = [[int(x in a[0]) for x in range(4)] for a in actions]
    component_floor = []
    for a, b in zip(actions, bg2):
        vals = []
        for A in range(3):
            top = max(utility(a, b, (A, B), 1) for B in range(3))
            vals.append(min(utility(a, b, (A, B), 0) for B in range(3)
                            if utility(a, b, (A, B), 1) == top))
        component_floor.append(max(vals))
    product_vals = []
    for AA in product(range(3), repeat=2):
        table = [(bb, sum(utility(actions[k], bg2[k], (AA[k], bb[k]), 0)
                          for k in range(2)),
                  sum(utility(actions[k], bg2[k], (AA[k], bb[k]), 1)
                      for k in range(2))) for bb in product(range(3), repeat=2)]
        top = max(v for _, _, v in table)
        product_vals.append(min(d for _, d, v in table if v == top))
    assert max(product_vals) == sum(component_floor)
    assert solve_round([])[:2] == (0, 0)

    out = {'scope': 'Bounded exact audit of a general proved construction; no general HALF claim.',
           'author_code_or_draft_read': False,
           'statement_contained_extreme_point_and_rounding_hints': True,
           'abstract_menu_not_claimed_CAG_realizable': {
               'LP_and_common_t': lp, 'separate_sup': separate,
               'rounded_cost': rounded, 'D': D,
               'integer_masses_3_2': {'LP': large_lp, 'rounded': large_round, 'D': large_D}},
           'true_CAG_r3_product': {'forced_joint_As': len(records),
               'next_joint_IC_checks': child_checks, 'last_joint_IC_checks': last_checks,
               'Psi': psi, 'D': global_D, 'records': records},
           'r2_legal_background': {'component_floors': component_floor,
               'product_floor': max(product_vals), 'D_needed': 0},
           'empty_product': 'zero, checked'}
    (HERE/'joint_threshold_blind_audit.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print(json.dumps(encode(out), indent=2))


if __name__ == '__main__':
    main()
