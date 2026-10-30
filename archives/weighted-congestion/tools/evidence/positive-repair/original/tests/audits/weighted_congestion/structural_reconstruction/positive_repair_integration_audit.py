#!/usr/bin/env python3
"""Second implementation of positive repair, with literal resources and Fractions.

This audit imports no repository module. Its finite checks are supporting
evidence, not a proof of the parameterized statements in the review.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json


class Instance:
    def __init__(self, weights):
        self.weights = tuple(F(w) for w in weights)
        self.menu = [[set(), set()] for _ in weights]
        self.resources = {}

    def add(self, name, coefficients, users):
        assert name not in self.resources
        self.resources[name] = tuple(F(c) for c in coefficients)
        for player, action in users:
            self.menu[player][action].add(name)

    def evaluate(self, state):
        loads = {name: sum((self.weights[i] for i, b in enumerate(state)
                           if name in self.menu[i][b]), F(0))
                 for name in self.resources}
        fees = {name: sum((coefficient * loads[name] ** degree
                          for degree, coefficient in enumerate(coefficients)), F(0))
                for name, coefficients in self.resources.items()}
        costs = tuple(sum((fees[name] for name in self.menu[i][b]), F(0))
                      for i, b in enumerate(state))
        social = sum((w * cost for w, cost in zip(self.weights, costs)), F(0))
        assert social == sum((loads[name] * fees[name] for name in self.resources), F(0))
        return costs, social

    def all_states(self):
        return tuple(product((0, 1), repeat=len(self.weights)))


def changed(state, player):
    return state[:player] + (1 - state[player],) + state[player + 1:]


def is_front(bits):
    return sum(bits[i] != bits[i + 1] for i in range(len(bits) - 1)) < 2


def front_state(state, classes):
    return all(is_front(tuple(state[i] for i in cc)) for cc in classes)


def triggers(state, cc):
    return frozenset((cc[0], j, k) for j, k in combinations(cc[1:], 2)
                     if state[cc[0]] == state[k] != state[j])


def repair_player(state, cc):
    return next(i for i in cc[1:] if state[i] != state[cc[0]])


def gates(instance, classes, parameters):
    for a, (cc, (height, degree)) in enumerate(zip(classes, parameters)):
        w = instance.weights[cc[0]]
        assert all(instance.weights[i] == w for i in cc)
        polynomial = [F(0)] * degree + [height / (3 * w) ** degree]
        for j, k in combinations(cc[1:], 2):
            for side in (0, 1):
                instance.add(f"gate-{a}-{j}-{k}-{side}", polynomial,
                             [(cc[0], side), (j, 1 - side), (k, side)])


def stability(instance, state, alpha):
    current = instance.evaluate(state)[0]
    return all(current[i] <= alpha * instance.evaluate(changed(state, i))[0][i]
               for i in range(len(state)))


def geometry():
    states = edges = repairs = 0
    for n in range(1, 9):
        cc = tuple(range(n))
        for state in product((0, 1), repeat=n):
            states += 1
            assert bool(triggers(state, cc)) == (not is_front(state))
            if is_front(state):
                for i in cc:
                    new = changed(state, i)
                    if not is_front(new):
                        continue
                    edges += 1
                    for triple in ((0, j, k) for j, k in combinations(cc[1:], 2)):
                        if i in triple:
                            pos = triple.index(i)
                            old_sides = tuple(state[p] ^ (q == 1)
                                              for q, p in enumerate(triple))
                            new_sides = tuple(new[p] ^ (q == 1)
                                              for q, p in enumerate(triple))
                            assert old_sides.count(old_sides[pos]) == 2
                            assert new_sides.count(new_sides[pos]) == 2
            else:
                new = changed(state, repair_player(state, cc))
                assert triggers(new, cc) < triggers(state, cc)
                steps = 1
                while not is_front(new):
                    new = changed(new, repair_player(new, cc))
                    steps += 1
                assert steps <= n - 2
                repairs += 1
    return {"states": states, "directed_core_edges": edges,
            "nonfront_repair_paths": repairs}


def heterogeneous_base():
    classes = ((0, 1, 2, 3), (4, 5, 6), (7,))
    game = Instance([F(1, 2)] * 4 + [F(5, 3)] * 3 + [F(7, 2)])
    for i in range(8):
        for b in (0, 1):
            game.add(f"private-{i}-{b}", [F((i + 2 * b) % 5, 7)], [(i, b)])
    game.add("shared-retained", [F(1, 3), F(1, 5), F(1, 11)],
             [(i, b) for i in range(8) for b in (0, 1)])
    game.add("cross-class-entry", [F(1, 7), F(1, 13), F(1, 17)],
             [(0, 0), (2, 1), (4, 0), (5, 1), (7, 0), (7, 1)])
    game.add("another-shared", [F(0), F(1, 19)],
             [(1, 0), (3, 1), (4, 1), (6, 0)])
    return game, classes


def joint_transfer(alpha):
    game, classes = heterogeneous_base()
    states = game.all_states()
    base = {s: game.evaluate(s) for s in states}
    bounds = [max(base[s][0][i] for s in states for i in cc) for cc in classes]
    parameters = []
    for cc, bound in zip(classes, bounds):
        count = (len(cc) - 1) * (len(cc) - 2) // 2
        height, degree = 2 * alpha * bound, 1
        while count and not height > alpha * (bound + count * height * F(2, 3) ** degree):
            degree += 1
        parameters.append((height, degree))
    gates(game, classes, parameters)
    u = [h * F(2, 3) ** d for h, d in parameters]
    z = [h * F(1, 3) ** d for h, d in parameters]
    gaps = [3 * h - 2 * ua - za for (h, _), ua, za in zip(parameters, u, z)]
    K = sum((game.weights[cc[0]] * ((len(cc) - 1) * (len(cc) - 2) // 2)
             * (2 * ua + za) for cc, ua, za in zip(classes, u, z)), F(0))
    edge_checks = social_repair_checks = path_checks = 0
    actual, predicted = set(), set()
    for state in states:
        full = game.evaluate(state)
        assert full[1] == base[state][1] + K + sum(
            (game.weights[cc[0]] * len(triggers(state, cc)) * gap
             for cc, gap in zip(classes, gaps)), F(0))
        if stability(game, state, alpha):
            actual.add(state)
        if front_state(state, classes):
            valid = True
            for a, cc in enumerate(classes):
                for position, i in enumerate(cc):
                    edge_checks += 1
                    new = changed(state, i)
                    full_margin = full[0][i] - alpha * game.evaluate(new)[0][i]
                    if front_state(new, classes):
                        r = ((len(cc) - 1) * (len(cc) - 2) // 2
                             if position == 0 else max(len(cc) - 2, 0))
                        base_margin = base[state][0][i] - alpha * base[new][0][i]
                        assert full_margin == base_margin - (alpha - 1) * r * u[a]
                        valid &= base_margin <= (alpha - 1) * r * u[a]
                    else:
                        assert full_margin < 0
            if valid:
                predicted.add(state)
        else:
            for a, cc in enumerate(classes):
                if is_front(tuple(state[i] for i in cc)):
                    continue
                i = repair_player(state, cc)
                new = changed(state, i)
                assert full[0][i] > alpha * game.evaluate(new)[0][i]
                assert full[1] > game.evaluate(new)[1]
                # Retained resources and cross-class mandatory users remain in W.
                assert base[new][1] - base[state][1] <= 3 * game.weights[i] * base[new][0][i]
                assert gaps[a] > 3 * bounds[a]
                social_repair_checks += 1
            path = state
            steps = 0
            while not front_state(path, classes):
                cc = next(cc for cc in classes
                          if not is_front(tuple(path[i] for i in cc)))
                path = changed(path, repair_player(path, cc))
                steps += 1
            assert steps <= 3
            path_checks += 1
    assert actual == predicted
    full_opt = min(game.evaluate(s)[1] for s in states)
    base_front_opt = min(base[s][1] for s in states if front_state(s, classes))
    assert full_opt == K + base_front_opt
    return {"alpha": str(alpha), "states": len(states), "classes": [4, 3, 1],
            "weights": ["1/2", "5/3", "7/2"], "degrees": [d for _, d in parameters],
            "core_edge_checks": edge_checks, "social_repair_checks": social_repair_checks,
            "complete_repair_paths": path_checks, "stable_states": len(actual),
            "K": str(K), "base_front_opt": str(base_front_opt), "full_opt": str(full_opt)}


def article_example():
    game = Instance([1, 1, 1])
    game.add("A", [0, 1], [(i, 0) for i in range(3)])
    game.add("B", [2], [(i, 1) for i in range(3)])
    states = game.all_states()
    base = {s: game.evaluate(s) for s in states}
    gates(game, [(0, 1, 2)], [(F(6), 2)])
    table = []
    for s in states:
        costs, social = game.evaluate(s)
        slacks = [game.evaluate(changed(s, i))[0][i] - costs[i] for i in range(3)]
        table.append({"state": "".join(map(str, s)), "front": is_front(s),
                      "base_W": str(base[s][1]), "full_costs": list(map(str, costs)),
                      "full_W": str(social), "PNE": all(q >= 0 for q in slacks),
                      "deviation_slacks": list(map(str, slacks))})
    equilibria = {row["state"] for row in table if row["PNE"]}
    assert equilibria == {"001", "011", "100", "110"}
    assert min(game.evaluate(s)[1] for s in states) == 11
    assert {game.evaluate(s)[1] for s in states if stability(game, s, F(1))} == {F(11), F(12)}
    for start in ((0, 1, 0), (1, 0, 1)):
        end = changed(start, 1)
        assert game.evaluate(start)[1] > game.evaluate(end)[1]
    # Rosenthal potential on the base: Phi=k(k+1)/2+2(3-k), k=#A.
    phi = lambda s: F(s.count(0) * (s.count(0) + 1), 2) + 2 * s.count(1)
    core = [s for s in states if is_front(s)]
    assert min(phi(s) / base[s][1] for s in core) == F(2, 3)
    assert max(phi(s) / base[s][1] for s in core) == 1
    min_phi = min(map(phi, core))
    assert {base[s][1] for s in core if phi(s) == min_phi} == {F(5), F(6)}
    eta = F(1)
    regularized = [s for s in core if phi(s) + eta * base[s][1]
                   == min(phi(t) + eta * base[t][1] for t in core)]
    assert {"".join(map(str, s)) for s in regularized} == {"011", "110"}
    return {"bit_meaning": "0=A, 1=B", "gate": "c(x)=6(x/3)^2", "K": "6",
            "RD_margin": "1/3", "SD_margin": "6", "table": table,
            "all_state_deviation_checks": 24, "best_stable_W": "11", "OPT": "11",
            "core_regularization": {"eta": "1", "m": "2/3", "M": "1",
                                    "beta_bound": "3/2", "quality_bound": "6/5",
                                    "bound_scope": "base core; this gate is certified at alpha=1",
                                    "selected_states": ["011", "110"],
                                    "actual_stability": "exact, independently checked"}}


def composed_regularization():
    game = Instance([1, 1, 1])
    game.add("A", [0, 1], [(i, 0) for i in range(3)])
    game.add("B", [2], [(i, 1) for i in range(3)])
    states = game.all_states()
    core = [s for s in states if is_front(s)]
    base = {s: game.evaluate(s)[1] for s in states}
    phi = lambda s: F(s.count(0) * (s.count(0) + 1), 2) + 2 * s.count(1)
    beta, quality = F(3, 2), F(6, 5)
    score = lambda s: phi(s) + base[s]
    selected = [s for s in core if score(s) == min(map(score, core))]
    gates(game, [(0, 1, 2)], [(F(12), 4)])
    u, z = F(64, 27), F(4, 27)
    assert 12 > beta * (3 + u)
    assert 36 - 2 * u - z > 6
    K, optimum = 2 * u + z, min(game.evaluate(s)[1] for s in states)
    assert K == F(44, 9)
    assert optimum == K + min(base[s] for s in core) == F(89, 9)
    assert all(stability(game, s, beta) and game.evaluate(s)[1] <= quality * optimum
               for s in selected)
    assert all(stability(game, s, F(1)) for s in selected)
    return {"gate": "c(x)=12(x/3)^4", "base_degree": 1,
            "eta": "1", "h_i": "1", "base_alpha": "1", "beta": str(beta),
            "m": "2/3", "M": "1", "quality_bound": str(quality),
            "RD_margin_at_beta": str(12 - beta * (3 + u)),
            "SD_margin": str(36 - 2 * u - z - 6), "K": str(K),
            "selected": ["".join(map(str, s)) for s in selected],
            "selected_W": str(optimum), "full_OPT": str(optimum),
            "actual_stability": "exact, independently checked"}


def approximate_addition():
    game = Instance([1, 1, 1])
    for i, row in enumerate(((3, 1), (1, 1), (1, 1))):
        for b, cost in enumerate(row):
            game.add(f"private-{i}-{b}", [cost], [(i, b)])
    s = (0, 0, 0)
    assert not stability(game, s, F(2))
    gates(game, [(0, 1, 2)], [(F(20), 3)])
    assert stability(game, s, F(2))
    return {"state": "000", "alpha": "2", "base_margin_player0": "1",
            "gate_tolerance": "160/27", "full_costs": list(map(str, game.evaluate(s)[0])),
            "full_deviation_costs": [str(game.evaluate(changed(s, i))[0][i]) for i in range(3)]}


def high_degree_boundary():
    game = Instance([1, 1, 1, 3, 3, 3])
    cheap = (0, 1, 0)
    for i in range(3):
        game.add(f"congested-{i}", [0] * 10 + [F(1, 4 ** 10)],
                 [(i, 1 - cheap[i]), (i + 3, 0), (i + 3, 1)])
        for b in (0, 1):
            game.add(f"distinct-zero-{i}-{b}", [0], [(i + 3, b)])
    gates(game, [(0, 1, 2)], [(F(6, 5), 6)])
    s, t = (0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0)
    assert game.evaluate(s)[0][1] > game.evaluate(t)[0][1]
    assert game.evaluate(s)[1] < game.evaluate(t)[1]
    states = game.all_states()
    opt = min(game.evaluate(q)[1] for q in states)
    assert opt == game.evaluate(s)[1]
    assert all(not is_front(q[:3]) for q in states if game.evaluate(q)[1] == opt)
    return {"states": len(states), "base_degree": 10, "RD_margin": "23/243",
            "mover_old": str(game.evaluate(s)[0][1]), "mover_new": str(game.evaluate(t)[0][1]),
            "W_old": str(game.evaluate(s)[1]), "W_new": str(game.evaluate(t)[1]),
            "OPT": str(opt), "all_optima_outside_front": True}


def background_restore():
    # One mandatory weight-2 user, one optional weight-1 user, c(x)=x^2.
    # Optional potential is normalized at empty; h_i=w_i and q_min=1.
    # Choosing the legal upper-endpoint increments gives an alpha=1 optional
    # certificate (only one optional user), and the base is restored explicitly.
    background = F(2)
    raw = {0: F(0), 1: F(9)}
    restored = {b: raw[b] + background ** 3 for b in (0, 1)}
    W = {b: (background + b) ** 3 for b in (0, 1)}
    assert raw[0] == 0 < W[0]
    assert all(F(1, 3) * W[b] <= restored[b] <= W[b] for b in (0, 1))
    assert restored[1] - restored[0] == raw[1] - raw[0] == 9
    return {"raw_potential": {str(k): str(v) for k, v in raw.items()},
            "restored_potential": {str(k): str(v) for k, v in restored.items()},
            "full_W": {str(k): str(v) for k, v in W.items()},
            "verified_envelope": "W/3 <= restored_Phi <= W"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {"status": "all exact assertions passed",
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "geometry": geometry(),
              "joint_transfer": [joint_transfer(alpha) for alpha in (F(1), F(3, 2), F(2))],
              "article_example": article_example(),
              "composed_regularization": composed_regularization(),
              "new_approximate_equilibrium": approximate_addition(),
              "high_degree_background_boundary": high_degree_boundary(),
              "background_restoration": background_restore()}
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"status": report["status"], "output": str(args.output),
                      "geometry": report["geometry"], "mixed_cases": len(report["joint_transfer"]),
                      "article_equilibria": [r["state"] for r in report["article_example"]["table"]
                                             if r["PNE"]]}, indent=2))


if __name__ == "__main__":
    main()
