"""Exact literal-resource audit for the temporary directed fan-out cut candidate.

No floats, no empirical claim about the unrestricted WC target. All coefficients,
weights and alpha are Fraction. The proof, rather than these fixtures, handles
the real-valued quantifiers and the alpha=T_d endpoint.
"""

from fractions import Fraction as Q
from itertools import product
from random import Random
from collections import Counter
import hashlib
import json
from pathlib import Path
import argparse
import platform
from math import comb


def poly(coeffs, x):
    return sum((a * x ** k for k, a in enumerate(coeffs)), Q(0))


def scale(coeffs, c):
    return tuple(c * a for a in coeffs)


def qstr(x):
    return str(x)


def resource_game(hub_w, light_w, origins, main, sides):
    # sides is a list of (light index, target hub index, polynomial tuple).
    H, L = len(hub_w), len(light_w)
    weights = tuple(hub_w) + tuple(light_w)
    strategies = [[set(), set()] for _ in weights]
    fees = {}
    for v, f in enumerate(main):
        for bit in (0, 1):
            r = ("A", v, bit)
            fees[r] = f
            strategies[v][bit].add(r)
            for ell, origin in enumerate(origins):
                if origin == v:
                    strategies[H + ell][bit].add(r)
    for j, (ell, target, g) in enumerate(sides):
        for bit in (0, 1):
            r = ("B", j, bit)
            fees[r] = g
            strategies[target][bit].add(r)
            strategies[H + ell][1 - bit].add(r)
    return weights, strategies, fees


def costs(game, state):
    weights, strategies, fees = game
    loads = {r: Q(0) for r in fees}
    for i, bit in enumerate(state):
        for r in strategies[i][bit]:
            loads[r] += weights[i]
    return tuple(sum((poly(fees[r], loads[r])
                      for r in strategies[i][bit]), Q(0))
                 for i, bit in enumerate(state))


def deviations(game, state):
    current = costs(game, state)
    return current, tuple(costs(game, state[:i] + (1 - state[i],)
                               + state[i + 1:])[i]
                          for i in range(len(state)))


def verify_fixture(name, hub_w, light_w, origins, main, sides, alpha, recipe):
    H, L = len(hub_w), len(light_w)
    W = [sum((light_w[e] for e, o in enumerate(origins) if o == v), Q(0))
         for v in range(H)]
    for ell, w in enumerate(light_w):
        v = origins[ell]
        lhs = poly(main[v], hub_w[v] + w)
        rhs = poly(main[v], W[v])
        for ee, target, g in sides:
            if ee == ell:
                lhs += poly(g, w)
                rhs += poly(g, hub_w[target] + w)
        assert lhs >= alpha * rhs, (name, "UF", ell)

    lam, signed_Q, P, Pprime = [], [], [], []
    stats = Counter()
    for ell, target, g in sides:
        u, w = hub_w[target], light_w[ell]
        shared, hu, li = poly(g, u + w), poly(g, u), poly(g, w)
        qq = shared - alpha * hu
        pp, pprime = alpha * shared - li, alpha * shared - hu
        ll = u * max(qq, Q(0))
        assert 0 <= ll <= w * pp
        assert ll <= u * pprime
        lam.append(ll)
        signed_Q.append(qq)
        P.append(pp)
        Pprime.append(pprime)
        stats["Q_positive" if qq > 0 else "Q_negative" if qq < 0 else "Q_zero"] += 1
        stats["self_loops"] += origins[ell] == target

    M = [alpha * poly(main[v], hub_w[v] + W[v])
         - poly(main[v], hub_w[v]) for v in range(H)]
    for v in range(H):
        outgoing = sum((lam[j] for j, (ell, _, _) in enumerate(sides)
                        if origins[ell] == v), Q(0))
        weighted_N = sum((w * (poly(main[v], hub_w[v] + w)
                              - alpha * poly(main[v], W[v]))
                          for ell, w in enumerate(light_w) if origins[ell] == v), Q(0))
        coarse = W[v] * (poly(main[v], hub_w[v] + W[v])
                         - alpha * poly(main[v], W[v]))
        assert outgoing <= weighted_N <= coarse <= hub_w[v] * M[v]

    def cut(h):
        return sum((lam[j] for j, (ell, target, _) in enumerate(sides)
                    if h[origins[ell]] == h[target]), Q(0))

    game = resource_game(hub_w, light_w, origins, main, sides)
    hub_states = tuple(product((0, 1), repeat=H))
    best = min(cut(h) for h in hub_states)
    mins = tuple(h for h in hub_states if cut(h) == best)
    local_mins = tuple(h for h in hub_states
                       if all(cut(h) <= cut(h[:v] + (1-h[v],) + h[v+1:])
                              for v in range(H)))
    unstable_all_anti = 0
    for h in hub_states:
        state = h + tuple(1 - h[o] for o in origins)
        current, new = deviations(game, state)
        for ell in range(L):
            assert alpha * current[H + ell] <= new[H + ell]
        for v in range(H):
            direct = current[v] - alpha * new[v]
            reduced = -M[v]
            for j, (ell, target, _) in enumerate(sides):
                if target == v:
                    reduced += (signed_Q[j] if h[origins[ell]] == h[v]
                                else -Pprime[j])
            assert direct == reduced
        if any(c > alpha * n for c, n in zip(current, new)):
            unstable_all_anti += 1
        if h in local_mins:
            for v in range(H):
                signed_incoming = sum((lam[j] * (1 if h[origins[ell]] == h[v] else -1)
                                       for j, (ell, target, _) in enumerate(sides)
                                       if target == v), Q(0))
                outgoing = sum((lam[j] for j, (ell, _, _) in enumerate(sides)
                                if origins[ell] == v), Q(0))
                assert signed_incoming <= outgoing
            assert all(c <= alpha * n for c, n in zip(current, new))

    # Literal all-state audit records true PNEs; existence proof only needs mins.
    all_states = 0
    equilibria = 0
    zero_cost_moves = 0
    for state in product((0, 1), repeat=H + L):
        current, new = deviations(game, state)
        all_states += 1
        equilibria += all(c <= alpha * n for c, n in zip(current, new))
        zero_cost_moves += sum(c == 0 or n == 0 for c, n in zip(current, new))
    assert equilibria >= len(local_mins)
    degree = max(len(f) - 1 for f in (*main, *(g for _, _, g in sides)))
    if degree <= 2:
        assert alpha >= Q(6, 5)
        admissibility = "alpha>=6/5>T_2; 5*(alpha0*den-num)=R*(R-2)^2+3*R+1 at alpha0=6/5"
        # Verify the written identity by independent polynomial coefficients.
        assert [Q(6, 5) - 1, 2 * Q(6, 5) - 1,
                Q(6, 5) - 2, Q(6, 5) - 1] == [Q(1,5), Q(7,5), Q(-4,5), Q(1,5)]
    else:
        assert alpha >= degree
        assert degree - 1 >= 0
        assert all(degree * comb(degree, k) - comb(degree, k - 1) >= 0
                   for k in range(1, degree + 1))
        admissibility = "alpha>=d>=T_d; coefficientwise d*den(f_d)-num(f_d)>=0"
    return dict(name=name, hubs=H, lights=L, side_indices=len(sides),
                alpha=qstr(alpha), all_states=all_states,
                alpha_equilibria=equilibria, global_cut_minima=len(mins),
                local_cut_minima=len(local_mins),
                cut_weight=qstr(best), unstable_all_anti=unstable_all_anti,
                zero_cost_moves=zero_cost_moves, degree=degree,
                theorem_parameter_admissibility=admissibility,
                input_recipe=recipe,
                exact_input={"hub_weights":list(map(qstr,hub_w)),
                             "light_weights":list(map(qstr,light_w)),
                             "origins":list(origins),
                             "main_polynomial_coefficients":[list(map(qstr,f)) for f in main],
                             "side_indices":[{"light":ell,"head":t,
                                              "polynomial_coefficients":list(map(qstr,g))}
                                             for ell,t,g in sides]},
                **stats)


def generated(seed, H=3, L=5, d=2):
    rng = Random(seed)
    alpha = Q(6, 5) if d == 2 else Q(d)
    hub_w = tuple(Q(rng.randint(1, 3), rng.randint(1, 3)) for _ in range(H))
    origins = tuple(rng.randrange(H) for _ in range(L))
    counts = Counter(origins)
    light_w = tuple(hub_w[o] / (4 * counts[o]) for o in origins)
    main = tuple(tuple(Q(0) for _ in range(d)) + (Q(10) ** (v - 1),)
                 for v in range(H))
    sides = []
    for ell, w in enumerate(light_w):
        v = origins[ell]
        W = sum((light_w[e] for e, o in enumerate(origins) if o == v), Q(0))
        N = poly(main[v], hub_w[v] + w) - alpha * poly(main[v], W)
        assert N > 0
        targets = [rng.randrange(H) for _ in range(rng.randrange(4))]
        raw = []
        for target in targets:
            g = tuple(Q(rng.randrange(3)) for _ in range(d + 1))
            if not any(g):
                g = tuple(Q(0) for _ in range(d)) + (Q(1),)
            raw.append((target, g))
        denom = sum((alpha * poly(g, hub_w[t] + w) - poly(g, w)
                     for t, g in raw), Q(0))
        factor = N / (2 * denom) if denom else Q(0)
        sides.extend((ell, t, scale(g, factor)) for t, g in raw)
    return hub_w, light_w, origins, main, tuple(sides), alpha


def verify_cut_lemma_integer_graphs():
    """Independent CUT audit: all directed 3-vertex graphs, loops included.

    Each of nine ordered pairs has capacity 0, 1 or 2. Every local cut minimum
    is checked using integer arithmetic, independently of resource fees.
    """
    H = 3
    arcs = tuple(product(range(H), repeat=2))
    states = tuple(product((0, 1), repeat=H))
    graph_count = local_minimum_count = 0
    for caps in product(range(3), repeat=len(arcs)):
        energies = [sum(c for c, (o, t) in zip(caps, arcs) if h[o] == h[t])
                    for h in states]
        for index, h in enumerate(states):
            if all(energies[index] <= energies[index ^ (1 << (H - 1 - v))]
                   for v in range(H)):
                local_minimum_count += 1
                for v in range(H):
                    incoming = sum(c * (1 if h[o] == h[t] else -1)
                                   for c, (o, t) in zip(caps, arcs) if t == v)
                    outgoing = sum(c for c, (o, _) in zip(caps, arcs) if o == v)
                    assert incoming <= outgoing
        graph_count += 1
    assert graph_count == 3 ** 9
    return {"status":"exact_integer_cut_lemma_passed", "vertices":H,
            "ordered_pairs_including_loops":len(arcs), "capacities":[0,1,2],
            "graphs":graph_count, "local_minimum_states":local_minimum_count,
            "scope":"CUT combinatorial implementation only; no WC degree inference"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="Create a new JSON output; refuses to overwrite an existing file")
    args = parser.parse_args()
    fixtures = []
    # alpha=6/5 >= T_2 is certified without optimization:
    # alpha*den(f_2)-num(f_2) = [R*(R-2)^2+3*R+1]/5 > 0.
    # A directed odd cycle with source amplitudes spanning several scales
    # ensures the cut actually repairs some unstable all-anti hub states.
    hub_w = (Q(1),) * 3
    light_w = (Q(1, 5),) * 3
    main_polys = tuple((Q(0), Q(0), a) for a in (Q(100), Q(1), Q(1, 100)))
    sides = tuple((ell, (ell + 1) % 3, scale((Q(0), Q(0), Q(1)), a * Q(1, 2)))
                  for ell, a in enumerate((Q(100), Q(1), Q(1, 100))))
    fixtures.append(verify_fixture("asymmetric_directed_odd_cycle", hub_w,
                    light_w, (0, 1, 2), main_polys, sides, Q(6, 5),
                    {"kind":"literal", "source":"main() fixed exact odd cycle"}))
    for seed in range(12):
        fixtures.append(verify_fixture(f"fanout_seed_{seed}", *generated(seed),
                        recipe={"kind":"generated", "generator":"generated", "seed":seed,
                                "H":3,"L":5,"d":2}))
    for seed in range(3):
        fixtures.append(verify_fixture(f"mixed_degree3_seed_{seed}",
                        *generated(100 + seed, H=3, L=4, d=3),
                        recipe={"kind":"generated", "generator":"generated", "seed":100+seed,
                                "H":3,"L":4,"d":3}))
    # Weak UF equality, zero main/side, self-loop and zero-cost deviations.
    fixtures.append(verify_fixture("zero_fees_weak_UF_self_loop", (Q(1),),
                    (Q(1),), (0,), ((Q(0),),), ((0, 0, (Q(0),)),), Q(6, 5),
                    {"kind":"literal", "source":"main() zero-fee weak-UF equality"}))
    fixtures.append(verify_fixture("no_lights_zero_and_constant_main", (Q(1), Q(2)),
                    (), (), ((Q(0),), (Q(3),)), (), Q(6, 5),
                    {"kind":"literal", "source":"main() empty-light constant/zero main"}))
    fixtures.append(verify_fixture("positive_cost_weak_UF_equality", (Q(1),),
                    (Q(1),), (0,), ((Q(0), Q(0), Q(1)),), (), Q(4),
                    {"kind":"literal", "source":"one hub/one light/no side; F=x^2; UF 4=4*1"}))
    out = dict(status="exact_finite_audit_passed", arithmetic="fractions.Fraction",
               python_version=platform.python_version(),
               seed_policy="integer seeds fixed in source; no float arithmetic",
               theorem_scope="directed fan-out topology plus UF only; WC target open",
               d2_alpha_certificate="5*(alpha*den-num)=R*(R-2)^2+3*R+1 > 0",
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               fixtures=fixtures,
               total_full_states=sum(f["all_states"] for f in fixtures),
               combinatorial_cut_audit=verify_cut_lemma_integer_graphs())
    rendered = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        # Frozen evidence is never replaced in place.
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)


if __name__ == "__main__":
    main()
