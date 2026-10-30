"""异权共享侧资源排序势：作者有理边界与真实负载核验。

Finite evidence for WC-HETEROGENEOUS-HUB-SORTED-SIDE-v1, not a proof.
No external dependencies or frozen-output writes. Run from the repository root.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys

SEED = 2026101509
rng = random.Random(SEED)
counts = dict(marginals=0, resets=0, scalar=0, games=0, hub_states=0,
              fixed_light_deviations=0, reset_budgets=0, minima=0, pne=0)


def cost(poly, x):
    return sum((c * x**k for k, c in enumerate(poly)), F())


def subsets(items):
    for k in range(len(items) + 1):
        yield from combinations(items, k)


def kap(d, x):
    return min(d*x, 1+x)


def prefix(poly, weights, used, background):
    total = background
    out = F()
    for i in sorted(used, key=lambda i: (-weights[i], i)):
        total += weights[i]
        out += cost(poly, total)
    return out


# Exhaust all identity subsets, both noninteger and equal hub weights, and
# polynomial basis rays. This attacks both integral overlap estimates directly.
for weights in ((F(1), F(1)), (F(1), F(11, 10), F(21, 10)),
                (F(7), F(1, 9), F(5, 6), F(5, 6))):
    all_ids = tuple(range(len(weights)))
    A, U = min(weights), sum(weights, F())
    for d in (2, 3, 6):
        for k in range(d + 1):
            poly = [F()] * k + [F(1)]
            for bg in (F(), F(1, 100), F(7, 3)):
                for ids in subsets(all_ids):
                    for i in set(all_ids) - set(ids):
                        delta = prefix(poly, weights, ids+(i,), bg) - prefix(poly, weights, ids, bg)
                        c = cost(poly, bg + sum((weights[j] for j in ids), F()) + weights[i])
                        assert c <= delta <= (weights[i]/A)*c
                        counts['marginals'] += 1
                    for w in (A/F(10), A, F(11, 10)*A, F(4)*A):
                        delta = prefix(poly, weights, ids, bg+w) - prefix(poly, weights, ids, bg)
                        assert 0 <= delta <= kap(d, w/A)*cost(poly, bg+w+U)
                        counts['resets'] += 1

# The source estimate used in the proof is valid for every alpha>=1 BEFORE
# imposing the final squared threshold. Test this stronger intermediate claim.
for d in (2, 3, 4, 9):
    for ts in ((), (F(1, 100),), (F(1, 2), F(1, 2)),
               (F(1, 3), F(2, 3), F(1, 100)), (F(3), F(1, 17))):
        T = sum(ts, F())
        for alpha in (F(1), F(21, 20), F(3), F(9, 2)):
            for k in range(d+1):
                lhs = sum((kap(d, t)*((1+t)**k-alpha*T**k) for t in ts), F())
                assert lhs <= d*(1+T)**k
                counts['scalar'] += 1


def check_game(hub, lights, sides, d, prescribed_alpha=None):
    """Build actual resource sets independently of the sorted-side formula."""
    n = len(hub)
    W = [sum((w for source, w in lights if source == v), F()) for v in range(n)]
    R, K = F(1), F(1)
    for H, L, poly in sides:
        if H:
            A = min(hub[v] for v in H)
            R = max(R, *(hub[v]/A for v in H))
            K = max([K]+[hub[lights[l][0]]/A for l in L])
    # Exact rational square-root upper bounds, including equality cases.
    m = 1
    while F(m, 4)**2 < K*d:
        m += 1
    alpha = max(R, 1+F(m, 4)) if prescribed_alpha is None else prescribed_alpha
    assert alpha >= R and (alpha-1)**2 >= K*d
    main = []
    for v in range(n):
        amplitude = F()
        for l, (source, w) in enumerate(lights):
            if source != v:
                continue
            debit = sum((alpha*cost(poly, sum((hub[i] for i in H), F()) +
                                                   sum((lights[i][1] for i in L), F())) - cost(poly, w)
                         for H, L, poly in sides if l in L), F())
            surplus = (hub[v]+w)**d - alpha*W[v]**d
            assert surplus > 0
            amplitude = max(amplitude, debit/surplus)
        main.append([F()]*d+[amplitude])  # UF equality for a tight light.
    resource = {}
    strategies = [[set(), set()] for _ in range(n+len(lights))]
    for v, poly in enumerate(main):
        for b in (0, 1):
            key = ('main', v, b)
            resource[key] = poly
            strategies[v][b].add(key)
        for l, (source, w) in enumerate(lights):
            if source == v:
                for b in (0, 1):
                    strategies[n+l][b].add(('main', v, b))
    for j, (H, L, poly) in enumerate(sides):
        for b in (0, 1):
            key = ('side', j, b)
            resource[key] = poly
            for v in H:
                strategies[v][b].add(key)
            for l in L:
                strategies[n+l][1-b].add(key)
    weights = tuple(hub) + tuple(w for source, w in lights)

    def literal(state, side_only=False):
        loads = dict.fromkeys(resource, F())
        for i, b in enumerate(state):
            for e in strategies[i][b]:
                loads[e] += weights[i]
        return [sum((cost(resource[e], loads[e]) for e in strategies[i][b]
                     if not side_only or e[0] == 'side'), F()) for i, b in enumerate(state)]

    def potential(h, light_sides):
        return sum((prefix(poly, hub, tuple(v for v in H if h[v] == b),
                           sum((lights[l][1] for l in L if light_sides[l] == b), F()))
                    for H, L, poly in sides for b in (0, 1)), F())

    for l, (v, w) in enumerate(lights):
        low = cost(main[v], hub[v]+w) + sum((cost(poly, w) for H, L, poly in sides if l in L), F())
        high = cost(main[v], W[v]) + sum((cost(poly, sum((hub[i] for i in H), F())+
                                                         sum((lights[i][1] for i in L), F()))
                                         for H, L, poly in sides if l in L), F())
        assert low >= alpha*high
    for h in product((0, 1), repeat=n):
        counts['hub_states'] += 1
        ls = tuple(h[source] for source, w in lights)
        state = h + tuple(1-b for b in ls)
        E = potential(h, ls)
        old_side = literal(state, True)
        local = True
        for v in range(n):
            ht = h[:v] + (1-h[v],) + h[v+1:]
            st = state[:v] + (1-state[v],) + state[v+1:]
            fixed = potential(ht, ls)
            assert old_side[v]-alpha*literal(st, True)[v] <= E-fixed
            counts['fixed_light_deviations'] += 1
            ls_new = tuple(ht[source] for source, w in lights)
            reset = potential(ht, ls_new)-fixed
            M = alpha*cost(main[v], hub[v]+W[v])-cost(main[v], hub[v])
            assert reset <= M
            counts['reset_budgets'] += 1
            if E > potential(ht, ls_new):
                local = False
        if local:
            counts['minima'] += 1
            old = literal(state)
            for i in range(len(weights)):
                dev = state[:i]+(1-state[i],)+state[i+1:]
                assert old[i] <= alpha*literal(dev)[i]
                counts['pne'] += 1
    counts['games'] += 1
    return dict(R=str(R), K=str(K), alpha=str(alpha), global_ratio=str(max(hub)/min(hub)))


examples = []
for trial in range(54):
    n = 1 + trial % 4
    d = (2, 3, 5)[trial % 3]
    hub = tuple(F(rng.randint(1, 7), rng.randint(1, 4)) for _ in range(n))
    lights = tuple((v, hub[v]*F(rng.randint(1, 3), 10000))
                   for v in range(n) if trial % (v+2))
    sides = []
    for j in range(1+trial % 5):
        H = tuple(v for v in range(n) if rng.randrange(2))
        L = tuple(l for l in range(len(lights)) if rng.randrange(2))
        poly = tuple(F(rng.randint(0, 2), rng.randint(1, 4)) for _ in range(d+1))
        sides.append((H, L, poly))
    example = check_game(hub, lights, sides, d)
    if trial < 4:
        examples.append(example)

# Equalities in H, zero/constant side fees, empty sets, and large global span
# with R=K=1 (two disconnected components). Exact powers verify the thresholds.
examples.append(check_game((F(1), F(2)), ((0, F(1, 100)), (1, F(1, 100))),
                          [((0, 1), (1,), (F(), F(1), F(1)))], 2, F(3)))
examples.append(check_game((F(1), F(1)), ((0, F(1, 100)),),
                          [((0, 1), (0,), (F(), F(), F(1)))], 4, F(3)))
examples.append(check_game((F(1), F(3), F(2)), ((2, F(1, 100)),),
                          [((0, 1), (0,), (F(), F(), F(1)))], 2, F(3)))
examples.append(check_game((F(1), F(10**6)), ((0, F(1, 100)), (1, F(1))),
                          [((0,), (0,), (F(), F(1))),
                           ((1,), (1,), (F(1),)), ((), (0, 1), (F(),))], 2))

# The R marginal factor is sharp for this potential, already on linear rays.
for R in (F(1), F(7, 3), F(11)):
    for n in (1, 3, 17, 100):
        weights = (R,) + (F(1),)*n
        full = tuple(range(n+1))
        delta = prefix((F(), F(1)), weights, full, F()) - prefix((F(), F(1)), weights, full[1:], F())
        assert delta == (n+1)*R
        ratio = delta/(R+n)
        assert ratio == (n+1)*R/(R+n) <= R
        assert R-ratio == R*(R-1)/(R+n)

# Boundary attack: unequal hubs do not admit the equal-weight exact side
# Rosenthal argument. Recompute all eight profiles of the review's triangle.
tri_weights = (F(1), F(2), F(3))
tri_edges = ((0, 1, F(2100)), (0, 2, F(1130)), (1, 2, F(499)))


def tri_cost(state, i):
    value = F()
    for p, q, c in tri_edges:
        if i in (p, q):
            load = sum((tri_weights[v] for v in (p, q) if state[v] == state[i]), F())
            value += c*load**2
    return value


tri_factors = []
for state in product((0, 1), repeat=3):
    factor = F(1)
    for i in range(3):
        dev = state[:i]+(1-state[i],)+state[i+1:]
        old, new = tri_cost(state, i), tri_cost(dev, i)
        assert new > 0
        factor = max(factor, old/new)
    assert factor > 1
    tri_factors.append(factor)
assert min(tri_factors) == F(20896, 20875)

print(json.dumps(dict(title='异权共享侧资源排序势：作者有理边界与真实负载核验',
                      arithmetic='fractions.Fraction', seed=SEED,
                      python=sys.version.split()[0], counts=counts, examples=examples,
                      triangle_best_factor=str(min(tri_factors)),
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      scope='Finite exact checks; general theorem depends on the written proof.'),
                 ensure_ascii=False, indent=2))
