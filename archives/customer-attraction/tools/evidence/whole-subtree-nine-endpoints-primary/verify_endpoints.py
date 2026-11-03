"""Exact definition-level replay of the nine frozen endpoints, no solver imports."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def verify(path):
    d = json.loads(path.read_text())
    par, e = d['parameters'], d['exact']
    q = tuple(map(int, par['root'].split(',')))
    p, m = len(q), sum(q)
    r = tuple(e['integer_clones'])
    entries = e['strategy']['actions']
    actions = {tuple(t['history']): t['action'] for t in entries}
    expected = {h for n in range(m) for h in product(range(p), repeat=n)}
    assert len(actions) == len(entries) and set(actions) == expected
    assert len(r) == 2**p - 1 and all(type(v) is int and v >= 0 for v in r)
    assert all(type(a) is int and 0 <= a < p for a in actions.values())
    positive = [(b, n) for b, n in enumerate(r, 1) if n]

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (actions[h],))

    @lru_cache(None)
    def payoff(z, a):
        return sum((F(n, sum((b >> t) & 1 for t in z))
                    for b, n in positive if b >> a & 1), F(0))

    @lru_cache(None)
    def payoff_row(z, a):
        return tuple(F(1, sum((b >> t) & 1 for t in z)) if b >> a & 1 else F(0)
                     for b in range(1, 2**p))

    strict = ties = 0
    root_comparisons = []
    rows = set()
    for h, a in actions.items():
        z = terminal(h)
        u = payoff(z, a)
        ar = payoff_row(z, a)
        for b in range(p):
            if b == a:
                continue
            zz = terminal(h + (b,))
            alt = payoff(zz, b)
            assert u >= alt, (path.name, h, a, b, str(u-alt))
            strict += u > alt
            ties += u == alt
            if not h:
                root_comparisons.append([b, str(u), str(alt)])
            br = payoff_row(zz, b)
            row = tuple(x-y for x, y in zip(ar, br))
            if any(row):
                rows.add(row)
    rows = sorted(rows)
    z = terminal(())
    assert q == tuple(z.count(a) for a in range(p)) == tuple(e['strategy']['terminal_counts'])
    def coverage(J):
        union = sum(1 << a for a in set(J))
        return sum(n for b, n in positive if union & b)
    w = coverage(z)
    optimal_portfolios = []
    opt = -1
    for J in combinations(range(p), min(p, m)):
        value = coverage(J)
        if value > opt:
            opt, optimal_portfolios = value, [J]
        elif value == opt:
            optimal_portfolios.append(J)
    utilities = [payoff(z, a) if a in z else F(0) for a in range(p)]
    assert sum(utilities[a] for a in z) == w
    saved = e['independent_check']
    reconstructed = dict(verified=True, histories=len(actions), nonself_comparisons=strict+ties,
                         strict=strict, ties=ties, path=list(z), root_comparisons=root_comparisons,
                         welfare=w, optimum=opt, topic_payoffs=list(map(str, utilities)),
                         client_count=sum(r), positive_types=len(positive))
    assert saved == reconstructed, (path.name, saved, reconstructed)
    target_u = utilities[e['target']]
    assert F(e['OPT_over_target_payoff']) == F(opt)/target_u
    assert F(e['welfare_ratio']) == F(opt, w)
    assert F(e['weak_OPT_floor_gap']) == 2*m*target_u-opt
    assert F(e['weak_residual_floor_gap']) == m*target_u-(opt-w)
    assert F(e['half_gap']) == 2*w-opt
    J = e['portfolio']
    selected_union = sum(1 << a for a in J)
    wr = tuple(F(bool(b & sum(1 << a for a in set(z)))) for b in range(1, 2**p))
    vr = tuple(F(bool(b & selected_union)) for b in range(1, 2**p))
    ur = payoff_row(z, e['target'])
    mode = par['objective']
    objective = vr if mode == 'half' else tuple(
        v-(2*m*u if mode == 'individual' else ww+m*u)
        for v, ww, u in zip(vr, wr, ur))
    dot = lambda a, b: sum((x*y for x, y in zip(a, b)), F(0))
    val = dot(objective, r)/w
    assert val == F(e['objective_value'])
    dual = None
    if e['dual_bound'] is not None:
        beta = F(e['dual_bound'])
        mu = {}
        for i, mass in e['dual_support']:
            assert i not in mu and i in range(len(rows)) and F(mass) >= 0
            mu[i] = F(mass)
        residual = [beta*ww - sum((mass*rows[i][j] for i, mass in mu.items()), F(0))-vv
                    for j, (ww, vv) in enumerate(zip(wr, objective))]
        assert min(residual) >= 0 and beta == val and e['dual_optimal']
        dual = dict(beta=str(beta), support=len(mu), coefficient_cases=len(residual),
                    minimum_residual=str(min(residual)))
    else:
        assert not e['dual_optimal'] and not e['dual_support']
    branch_binding = []
    for entry in d['milp']['selected']:
        b = entry['branch']
        subset = {h: a for h, a in actions.items() if h and h[0] == b}
        digest = hashlib.sha256(repr(sorted(subset.items())).encode()).hexdigest()
        counts = [terminal((b,)).count(a) for a in range(p)]
        branch_binding.append(dict(branch=b, digest_matches_selected=digest == entry['digest'],
                                   target_matches_selected=counts == entry['target'],
                                   exact_branch_path=list(terminal((b,))), action_entries=len(subset)))
    same_count = defaultdict(set)
    for h, a in actions.items():
        same_count[tuple(h.count(j) for j in range(p))].add(a)
    return dict(file=path.name, parameters=par, milp=d['milp'],
                exact_scalars={k: v for k, v in e.items() if k not in ['strategy', 'integer_clones']},
                positive_client_types=positive, reconstructed=reconstructed,
                objective=str(val), fixed_cone_rows=len(rows), exact_dual=dual,
                all_optimal_portfolios=optimal_portfolios, selected_branch_binding=branch_binding,
                count_classes_with_different_actions=sum(len(s)>1 for s in same_count.values()))


def main():
    reports = [verify(p) for p in sorted((HERE/'original').glob('*.json'))]
    (HERE/'replay'/'endpoint-reconstruction.json').write_text(
        json.dumps(reports, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(endpoints=len(reports),
         histories=sum(x['reconstructed']['histories'] for x in reports),
         nonself_comparisons=sum(x['reconstructed']['nonself_comparisons'] for x in reports),
         exact_optimal_fixed_objective_duals=sum(x['exact_dual'] is not None for x in reports),
         all_selected_digests_match=all(e['digest_matches_selected'] for x in reports for e in x['selected_branch_binding'])),
         ensure_ascii=False))


if __name__ == '__main__':
    main()
