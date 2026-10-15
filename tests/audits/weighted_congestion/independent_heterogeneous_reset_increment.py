"""异权前缀重置增量与强迫乘积的独立 Fraction 核验。

Standalone oracle: no author audit or potential helper is imported. Finite
computations check formulas and actual strategies; they are not a proof of
the real-parameter theorem. Only stdout is written.
"""
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
import pathlib
import random
import sys

SEED = 9827061
rng = random.Random(SEED)
counts = {k: 0 for k in (
    "prefix_increment", "marginal", "source_increment", "kappa_scale",
    "UF_games", "hub_states", "local_minima", "literal_deviations",
    "fixed_light_comparisons", "reset_budget", "linear_method_witnesses",
    "linear_global_count_states")}


def fee(coeff, load):
    return sum((a * load ** k for k, a in enumerate(coeff)), Q())


def kappa(d, t):
    return min(d * t, t + 1)


def prefix_potential(coeff, weights, selected, background):
    load = background
    value = Q()
    for i in sorted(selected, key=lambda x: (-weights[x], x)):
        load += weights[i]
        value += fee(coeff, load)
    return value


def ceil_q(t):
    return -((-t.numerator) // t.denominator)


def check_prefix_increment():
    # Includes d=1, empty prefixes, constant and zero fees, w much greater
    # than A, prefix intervals crossing w, and unequal consecutive gaps.
    for d in (1, 2, 3, 5):
        for n in range(6):
            for trial in range(65):
                A = Q(rng.randint(1, 11), rng.randint(1, 7))
                prefix = []
                cursor = Q()
                for _ in range(n):
                    cursor += A * Q(rng.randint(1, 6), 1)
                    prefix.append(cursor)
                U = cursor + A * Q(rng.randint(0, 3), 2)
                w = A * (Q(100) if trial % 7 == 0 else Q(rng.randint(1, 19), rng.randint(1, 9)))
                x = A * Q(rng.randint(0, 8), rng.randint(1, 5))
                T = x + w + A * Q(rng.randint(0, 6), 3)
                coeff = [Q(rng.randint(0, 3), rng.randint(1, 5)) for _ in range(d + 1)]
                if trial % 11 == 0:
                    coeff = [Q(trial % 2)] + [Q()] * d
                Y = T + U
                lhs = sum((fee(coeff, x + w + p) - fee(coeff, x + p) for p in prefix), Q())
                rhs = kappa(d, w / A) * (fee(coeff, Y) - fee(coeff, w))
                assert x + w <= T and n * A <= U <= Y - w
                assert lhs <= rhs, (d, A, prefix, U, x, w, T, coeff, lhs, rhs)
                counts["prefix_increment"] += 1


def check_marginals_and_scaling():
    for d in (1, 2, 3, 5):
        for n in range(1, 5):
            for trial in range(20):
                weights = [Q(rng.randint(1, 13), rng.randint(1, 5)) for _ in range(n)]
                coeff = [Q(rng.randint(0, 3), rng.randint(1, 4)) for _ in range(d + 1)]
                background = Q(rng.randint(0, 9), rng.randint(1, 7))
                A = min(weights)
                for bits in product((0, 1), repeat=n):
                    selected = {i for i, b in enumerate(bits) if b}
                    for i in set(range(n)) - selected:
                        delta = prefix_potential(coeff, weights, selected | {i}, background) - prefix_potential(coeff, weights, selected, background)
                        real = fee(coeff, background + weights[i] + sum((weights[j] for j in selected), Q()))
                        assert real <= delta <= (weights[i] / A) * real
                        counts["marginal"] += 1
                for a in weights:
                    for w in (Q(1, 100), Q(1, 3), Q(2), Q(200)):
                        assert kappa(d, w / A) <= max(Q(1), a / A) * kappa(d, w / a)
                        counts["kappa_scale"] += 1


def check_source_increment():
    for d in (1, 2, 3, 5):
        partitions = [[], [Q(1)], [Q(1, 2), Q(1, 2)], [Q(1, 3)] * 3,
                      [Q(1, 1000)], [Q(1000)], [Q(3, 4), Q(3, 4)]]
        for _ in range(240):
            scale = rng.choice((Q(1, 100), Q(1), Q(100)))
            partitions.append([scale * Q(rng.randint(1, 11), rng.randint(1, 13)) for _ in range(rng.randint(1, 5))])
        for ts in partitions:
            T = sum(ts, Q())
            u = Q(rng.randint(1, 9), rng.randint(1, 5))
            for tau in (Q(1), Q(3, 2), Q(7)):
                for k in range(d + 1):
                    lhs = sum((kappa(d, t) * ((u * (1 + t)) ** k - tau * (u * T) ** k) for t in ts), Q())
                    rhs = d * ((u * (1 + T)) ** k - u ** k)
                    assert lhs <= rhs, (d, ts, u, tau, k, lhs, rhs)
                    if d == 1 and k == 1 and tau == 1:
                        assert lhs == u * (T + sum((t * t for t in ts), Q()) - T * T)
                    counts["source_increment"] += 1


def literal_game(d, hub, lights, sides, tau, alpha, label, main_override=None):
    # sides=(hub identities, light identities, polynomial coefficient list)
    n = len(hub)
    W = [sum((w for v, w in lights if v == i), Q()) for i in range(n)]
    R = max([Q(1)] + [hub[v] / min(hub[u] for u in H) for H, L, g in sides if H for v in H])
    K = max([Q(1)] + [hub[lights[l][0]] / min(hub[u] for u in H) for H, L, g in sides if H for l in L])
    assert tau >= 1 and alpha >= R and alpha * tau >= K * d
    main = []
    for v, a in enumerate(hub):
        multiplier = Q()
        for l, (source, w) in enumerate(lights):
            if source != v:
                continue
            side_budget = sum((tau * fee(g, sum((hub[i] for i in H), Q()) + sum((lights[k][1] for k in L), Q())) - fee(g, w)
                               for H, L, g in sides if l in L), Q())
            denominator = (a + w) ** d - tau * W[v] ** d
            assert denominator > 0
            multiplier = max(multiplier, side_budget / denominator)
        main.append([Q()] * d + [Q(max(0, ceil_q(multiplier)) + 1)])
    if main_override is not None:
        main = main_override

    resource_fee = {}
    for v, f in enumerate(main):
        for b in (0, 1):
            resource_fee[(0, v, b)] = f
    for j, (H, L, g) in enumerate(sides):
        for b in (0, 1):
            resource_fee[(1, j, b)] = g
    strategies = []
    for v in range(n):
        strategies.append([{(0, v, b)} | {(1, j, b) for j, (H, L, g) in enumerate(sides) if v in H} for b in (0, 1)])
    for l, (source, w) in enumerate(lights):
        strategies.append([{(0, source, b)} | {(1, j, 1 - b) for j, (H, L, g) in enumerate(sides) if l in L} for b in (0, 1)])
    weights = hub + [w for source, w in lights]

    def costs(state):
        loads = {e: Q() for e in resource_fee}
        for i, b in enumerate(state):
            for e in strategies[i][b]:
                loads[e] += weights[i]
        return [sum((fee(resource_fee[e], loads[e]) for e in strategies[i][b]), Q()) for i, b in enumerate(state)]

    def potential(h, light_side):
        value = Q()
        for H, L, g in sides:
            for b in (0, 1):
                background = sum((lights[l][1] for l in L if light_side[l] == b), Q())
                value += prefix_potential(g, hub, {v for v in H if h[v] == b}, background)
        return value

    for l, (v, w) in enumerate(lights):
        lhs = fee(main[v], hub[v] + w) + sum((fee(g, w) for H, L, g in sides if l in L), Q())
        rhs = tau * (fee(main[v], W[v]) + sum((fee(g, sum((hub[i] for i in H), Q()) + sum((lights[k][1] for k in L), Q())) for H, L, g in sides if l in L), Q()))
        assert lhs >= rhs
    for h in product((0, 1), repeat=n):
        light_side = tuple(h[source] for source, w in lights)
        E = potential(h, light_side)
        state = h + tuple(1 - h[source] for source, w in lights)
        old = costs(state)
        is_min = True
        for v in range(n):
            hv = h[:v] + (1 - h[v],) + h[v + 1:]
            reset_side = tuple(hv[source] for source, w in lights)
            E_fixed = potential(hv, light_side)
            E_reset = potential(hv, reset_side)
            if E > E_reset:
                is_min = False
            dev = state[:v] + (1 - state[v],) + state[v + 1:]
            real_dev = costs(dev)
            main_old = fee(main[v], hub[v])
            main_new = fee(main[v], hub[v] + W[v])
            side_gap = (old[v] - main_old) - alpha * (real_dev[v] - main_new)
            assert side_gap <= E - E_fixed
            counts["fixed_light_comparisons"] += 1
            reset_bound = Q()
            for l, (source, w) in enumerate(lights):
                if source != v:
                    continue
                for H, L, g in sides:
                    if not H or l not in L:
                        continue
                    A = min(hub[i] for i in H)
                    Y = sum((hub[i] for i in H), Q()) + sum((lights[k][1] for k in L), Q())
                    reset_bound += kappa(d, w / A) * (fee(g, Y) - fee(g, w))
            assert E_reset - E_fixed <= reset_bound
            delta_F = main_new - main_old
            assert reset_bound <= K * d * delta_F / tau <= alpha * delta_F <= alpha * main_new - main_old
            counts["reset_budget"] += 1
        counts["hub_states"] += 1
        if is_min:
            counts["local_minima"] += 1
            for i in range(len(weights)):
                dev = state[:i] + (1 - state[i],) + state[i + 1:]
                new = costs(dev)
                assert old[i] <= alpha * new[i], (label, h, i, old[i], new[i], alpha, tau, R, K)
                counts["literal_deviations"] += 1
    counts["UF_games"] += 1
    return {"label": label, "d": d, "R": str(R), "K": str(K), "alpha": str(alpha), "tau": str(tau),
            "hub_weights": list(map(str, hub)), "lights": [[v, str(w)] for v, w in lights]}


def check_literal_games():
    examples = []
    # R=K=2, alpha=2, tau=d gives both multiplier constraints at equality.
    for d in (1, 2, 3, 5):
        hub = [Q(1), Q(2)]
        lights = [(0, Q(1, 1000)), (1, Q(1, 500))]
        sides = [({0, 1}, {0, 1}, [Q()] * d + [Q(1)]),
                 (set(), {0}, [Q(1)]), ({0}, set(), [Q()])]
        examples.append(literal_game(d, hub, lights, sides, Q(d), Q(2), "both_equalities"))
    # Global hub span huge while all nonempty side-local R,K equal 1.
    for d in (1, 3):
        hub = [Q(1), Q(1000000)]
        lights = [(0, Q(1, 1000)), (1, Q(1000))]
        sides = [({v}, {v}, [Q()] * d + [Q(1)]) for v in range(2)]
        examples.append(literal_game(d, hub, lights, sides, Q(d), Q(1), "unbounded_global_span"))
    for d in (1, 2, 3, 5):
        for n in range(1, 5):
            for trial in range(12):
                hub = [Q(rng.randint(1, 11), rng.randint(1, 4)) for _ in range(n)]
                lights = [(v, a * Q(rng.randint(1, 3), 10000)) for v, a in enumerate(hub) for _ in range(rng.randint(0, 2))]
                sides = []
                for j in range(rng.randint(0, 5)):
                    H = {v for v in range(n) if rng.randrange(3)}
                    L = {l for l in range(len(lights)) if rng.randrange(2)}
                    g = [Q(rng.randint(0, 2), rng.randint(1, 5)) for _ in range(d + 1)]
                    sides.append((H, L, g))
                R = max([Q(1)] + [hub[v] / min(hub[u] for u in H) for H, L, g in sides if H for v in H])
                K = max([Q(1)] + [hub[lights[l][0]] / min(hub[u] for u in H) for H, L, g in sides if H for l in L])
                # Exercise tau=1 and alpha=R/product equality independently.
                alpha = max(R, K * d) if trial % 3 == 0 else R
                tau = max(Q(1), K * d / alpha)
                literal_game(d, hub, lights, sides, tau, alpha, "seeded_random")
    # All-zero and constant side fees, no lights, no hubs on a side.
    examples.append(literal_game(1, [Q(1)], [], [(set(), set(), [Q(1)]), ({0}, set(), [Q(2)]), ({0}, set(), [Q()])], Q(1), Q(1), "constant_zero_empty"))
    for c in (Q(), Q(2)):
        examples.append(literal_game(2, [Q(1)], [(0, Q(1))], [({0}, {0}, [c])], Q(1), Q(2), "zero_or_constant_main_and_side", main_override=[[c]]))
    return examples


def check_linear_method_boundary():
    witnesses = []
    for R in (Q(1), Q(3, 2), Q(2), Q(5)):
        for n in (1, 2, 5, 20, 100):
            A = Q(3, 7)
            hub = [R * A] * n + [A] * n
            h = (0,) * n + (1,) * n
            # For G(x)=x, a group's prefix sum is the direct potential.
            def energy(bits):
                return sum((prefix_potential([Q(), Q(1)], hub, {i for i, b in enumerate(bits) if b == c}, Q()) for c in (0, 1)), Q())
            E = energy(h)
            # The equal-count separated state is a strict local minimum.
            for i in (0, n):
                dev = h[:i] + (1 - h[i],) + h[i + 1:]
                diff = energy(dev) - E
                expected = R * A if i == 0 else (n * R + 1 - n) * A
                assert diff == expected > 0
            # Global minimizers are also fully checked in the count quotient.
            # For small n, cross-check the count formula against literal
            # identity-sorted potential, rather than only its own expansion.
            a = R * A
            for x in range(n + 1):
                for y in range(n + 1):
                    closed_E = a * (Q(x * (x + 1), 2) + x * y + Q((n - x) * (n - x + 1), 2) + (n - x) * (n - y)) + A * (Q(y * (y + 1), 2) + Q((n - y) * (n - y + 1), 2))
                    delta = a * (n - x - y) ** 2 + (a - A) * y * (n - y)
                    assert closed_E - E == delta >= 0
                    if n <= 20:
                        bits = (0,) * x + (1,) * (n - x) + (0,) * y + (1,) * (n - y)
                        assert energy(bits) == closed_E
                    if R > 1:
                        assert (delta == 0) == ((x, y) in ((n, 0), (0, n)))
                    counts["linear_global_count_states"] += 1
            real_old = n * R * A
            real_new = (R + n) * A
            gain = real_old / real_new
            assert gain == n * R / (R + n)
            assert R - gain == R * R / (R + n)
            counts["linear_method_witnesses"] += 1
            if R > 1 and n in (1, 100):
                witnesses.append({"R": str(R), "n": n, "gain": str(gain), "gap_to_R": str(R - gain)})
    return witnesses


if __name__ == "__main__":
    check_prefix_increment()
    check_marginals_and_scaling()
    check_source_increment()
    examples = check_literal_games()
    witnesses = check_linear_method_boundary()
    print(json.dumps({"title": "异权前缀重置增量与强迫乘积的独立精确审计", "seed": SEED,
                      "python": sys.version.split()[0], "arithmetic": "fractions.Fraction",
                      "counts": counts, "examples": examples, "linear_boundary": witnesses,
                      "scope": "Finite checks only; no imports of author audit or core helper.",
                      "sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()},
                     ensure_ascii=False, indent=2))
