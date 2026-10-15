#!/usr/bin/env python3
"""潜在使用森林与单玩家挂树私人成本归约的Fraction作者审计。

Run: python3 verify_incidence_forest.py --output incidence_forest_audit.json
Only finite evidence. The direct cost oracle never calls the offer constructor.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
from pathlib import Path
import random


@dataclass(frozen=True)
class Fee:
    kind: str
    data: tuple

    def __call__(self, x):
        x = Q(x)
        if self.kind == 'poly':
            return sum((Q(a) * x ** k for k, a in enumerate(self.data)), Q(0))
        if self.kind == 'step':
            return sum((Q(v) for threshold, v in self.data if x >= Q(threshold)), Q(0))
        raise ValueError(self.kind)


class Game:
    def __init__(self, weights, strategies, fees):
        self.weights = {i: Q(w) for i, w in weights.items()}
        self.strategies = {i: tuple(sorted(set(map(frozenset, ss)),
                                 key=lambda s: tuple(sorted(s))))
                           for i, ss in strategies.items()}
        self.fees = dict(fees)
        self.neighbors = {i: set().union(*self.strategies[i]) for i in weights}
        self.users = {e: {i for i in weights if e in self.neighbors[i]} for e in fees}

    def states(self):
        ids = tuple(self.weights)
        for actions in product(*(self.strategies[i] for i in ids)):
            yield dict(zip(ids, actions))

    def cost(self, i, state, action=None):
        # Literal frozen-others oracle, independent of recursive construction.
        action = state[i] if action is None else action
        ans = Q(0)
        for e in action:
            load = self.weights[i] + sum((self.weights[j] for j, sj in state.items()
                                        if j != i and e in sj), Q(0))
            ans += self.fees[e](load)
        return ans

    def is_equilibrium(self, state, alpha=Q(1), players=None):
        players = self.weights if players is None else players
        return all(self.cost(i, state) <= alpha * self.cost(i, state, t)
                   for i in players for t in self.strategies[i])

    def is_forest(self):
        parent = {}
        def find(v):
            parent.setdefault(v, v)
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]
        for i in self.weights:
            for e in self.neighbors[i]:
                a, b = find(('p', i)), find(('e', e))
                if a == b:
                    return False
                parent[a] = b
        return True


@dataclass
class Offer:
    price: Q
    followers: dict
    loads: tuple


class Constructor:
    def __init__(self, game):
        self.g = game
        self.offers = {}
        self.interface_checks = 0

    def resource_offer(self, e, root):
        if (e, root) in self.offers:
            return self.offers[e, root]
        g = self.g
        children = sorted(g.users[e] - {root})
        branch, best, h = {}, {}, {}
        mandatory, optional = [], []
        for i in children:
            branch[i] = {f: self.resource_offer(f, i) for f in sorted(g.neighbors[i] - {e})}
            for bit in (0, 1):
                ss = [s for s in g.strategies[i] if int(e in s) == bit]
                if ss:
                    best[i, bit] = min(ss, key=lambda s: (sum((branch[i][f].price
                                               for f in s if f != e), Q(0)), tuple(sorted(s))))
                    h[i, bit] = sum((branch[i][f].price for f in best[i, bit] if f != e), Q(0))
            if (i, 0) not in h:
                mandatory.append(i)
            elif (i, 1) in h:
                optional.append(i)
        optional.sort(key=lambda i: (-(h[i, 0] - h[i, 1]), i))
        states, loads = {}, []
        for root_bit in (0, 1):
            included = set(mandatory)
            load = sum((g.weights[i] for i in mandatory), Q(0))
            for i in optional:
                if g.fees[e](root_bit * g.weights[root] + load + g.weights[i]) <= h[i, 0] - h[i, 1]:
                    included.add(i)
                    load += g.weights[i]
            st = {}
            for i in children:
                bit = int(i in included)
                si = best[i, bit]
                st[i] = si
                for f, off in branch[i].items():
                    sub = off.followers[int(f in si)]
                    assert not st.keys() & sub.keys()
                    st.update(sub)
            states[root_bit] = st
            loads.append(load)
            boundary = {root: frozenset([e]) if root_bit else frozenset(), **st}
            assert g.is_equilibrium(boundary, players=st.keys())
            self.interface_checks += sum(len(g.strategies[i]) for i in st)
        assert loads[1] <= loads[0]
        price = g.fees[e](g.weights[root] + loads[1])
        assert price <= g.fees[e](g.weights[root] + loads[0])
        ans = Offer(price, states, tuple(loads))
        self.offers[e, root] = ans
        return ans

    def forest_equilibrium(self):
        assert self.g.is_forest()
        state = {}
        for root in self.g.weights:
            if root in state:
                continue
            offers = {e: self.resource_offer(e, root) for e in self.g.neighbors[root]}
            s = min(self.g.strategies[root],
                    key=lambda t: (sum((offers[e].price for e in t), Q(0)), tuple(sorted(t))))
            state[root] = s
            for e, off in offers.items():
                sub = off.followers[int(e in s)]
                assert not state.keys() & sub.keys()
                state.update(sub)
        assert self.g.is_equilibrium(state)
        return state


def star_audit():
    cases = 0
    for weights in product((Q(1), Q(2), Q(3, 2)), repeat=3):
        for thresholds in product((Q(-1), Q(0), Q(2), Q(4)), repeat=3):
            order = sorted(range(3), key=lambda i: (-thresholds[i], i))
            for fee in (Fee('poly', (0, 1)), Fee('poly', (1, 0, 1)),
                        Fee('poly', (0,)), Fee('step', ((Q(2), Q(3)),))):
                old = None
                for b in (Q(0), Q(1, 2), Q(1), Q(2), Q(5)):
                    accepted, load = set(), Q(0)
                    for i in order:
                        if fee(b + load + weights[i]) <= thresholds[i]:
                            accepted.add(i)
                            load += weights[i]
                    if old is not None:
                        assert load <= old
                    old = load
                    for i in range(3):
                        if i in accepted:
                            assert fee(b + load) <= thresholds[i]
                        else:
                            assert fee(b + load + weights[i]) > thresholds[i]
                    cases += 1
    return cases


def random_forest(rng, n=6, m=5):
    # Start with one player; each fresh node attaches to exactly one existing
    # opposite-type node, so the potential-use supergraph is a tree.
    pnodes, enodes, incidence = [0], [], {0: set()}
    schedule = ['e'] * m + ['p'] * (n - 1)
    rng.shuffle(schedule)
    if schedule[0] == 'p':
        schedule.remove('e')
        schedule.insert(0, 'e')
    for typ in schedule:
        if typ == 'p':
            i = len(pnodes)
            pnodes.append(i)
            incidence[i] = {rng.choice(enodes)}
        else:
            e = len(enodes)
            enodes.append(e)
            incidence[rng.choice(pnodes)].add(e)
    weights = {i: Q(rng.randint(1, 8), rng.randint(1, 3)) for i in pnodes}
    strategies = {}
    for i in pnodes:
        nb = sorted(incidence[i])
        subsets = [frozenset(nb[k] for k in range(len(nb)) if mask >> k & 1)
                   for mask in range(1 << len(nb))]
        rng.shuffle(subsets)
        count = rng.randint(1, min(len(subsets), 4))
        strategies[i] = subsets[:count]
    fees = {}
    for e in enodes:
        kind = rng.randrange(4)
        if kind == 0:
            fees[e] = Fee('poly', (0,))
        elif kind == 1:
            fees[e] = Fee('poly', (rng.randint(0, 5),))
        elif kind == 2:
            fees[e] = Fee('poly', tuple(Q(rng.randint(0, 3), rng.randint(1, 3))
                                         for _ in range(rng.randint(2, 5))))
        else:
            fees[e] = Fee('step', ((Q(1), Q(2)), (Q(4), Q(3)), (Q(9), Q(7))))
    return Game(weights, strategies, fees)


def forest_audit(rng):
    games = states = deviations = interfaces = 0
    for _ in range(300):
        g = random_forest(rng, rng.randint(1, 7), rng.randint(1, 6))
        ctor = Constructor(g)
        s = ctor.forest_equilibrium()
        assert all(s[i] in g.strategies[i] for i in g.weights)
        deviations += sum(len(ss) for ss in g.strategies.values())
        interfaces += ctor.interface_checks
        # Enumerating all states independently checks existence separately.
        pne = 0
        for st in g.states():
            states += 1
            pne += g.is_equilibrium(st)
        assert pne
        games += 1
    return dict(games=games, enumerated_states=states,
                output_deviations=deviations, recursive_deviations=interfaces)


def make_core_attachment(rng):
    # A cyclic core with three players, three common resources, and rich
    # arbitrary coupled choices linking both core and tree resources.
    w = {i: Q(rng.randint(1, 9), rng.randint(1, 3)) for i in range(7)}
    ss = {
        0: ({0, 2, 3}, {0, 4}, {2}, {3, 4}, set()),
        1: ({0, 1, 8}, {0}, {1, 8}, set()),
        2: ({1, 2}, {1}, {2}),
        3: ({3, 5}, {5, 6}, {3, 6}, {3, 5, 6}),
        4: ({3, 7}, {7}, {3}),
        5: ({5}, set()),
        6: ({8}, set()),
    }
    fees = {e: Fee('poly', tuple(Q(rng.randint(0, 4), rng.randint(1, 4))
                               for _ in range(rng.randint(1, 5)))) for e in range(9)}
    return Game(w, ss, fees)


def lift_audit(rng):
    checked = state_count = current_equalities = deviation_bounds = lift_count = 0
    for _ in range(60):
        g = make_core_attachment(rng)
        ctor = Constructor(g)
        core, eroot = {0, 1, 2}, {0, 1, 2}
        offers = {(i, e): ctor.resource_offer(e, i) for i in core
                  for e in g.neighbors[i] - eroot}
        z = {(i, e): 100 + 10 * i + e for i, e in offers}
        ss = {i: [frozenset([e for e in s if e in eroot] +
                                 [z[i, e] for e in s if e not in eroot])
                  for s in g.strategies[i]] for i in core}
        hf = {e: g.fees[e] for e in eroot}
        hf.update({z[i, e]: Fee('poly', (off.price,)) for (i, e), off in offers.items()})
        h = Game({i: g.weights[i] for i in core}, ss, hf)
        forward = {i: dict(zip(g.strategies[i], ss[i])) for i in core}
        backward = {i: {new: old for old, new in forward[i].items()} for i in core}
        assert all(len(backward[i]) == len(g.strategies[i]) for i in core)
        for u in h.states():
            s = {i: backward[i][u[i]] for i in core}
            for (i, e), off in offers.items():
                sub = off.followers[int(e in s[i])]
                assert not s.keys() & sub.keys()
                s.update(sub)
            assert set(s) == set(g.weights)
            for i in core:
                assert g.cost(i, s) == h.cost(i, u)
                current_equalities += 1
                for t in g.strategies[i]:
                    assert g.cost(i, s, t) >= h.cost(i, u, forward[i][t])
                    deviation_bounds += 1
            assert g.is_equilibrium(s, players=set(g.weights) - core)
            for alpha in (Q(1), Q(3, 2), Q(2), Q(7), Q(100)):
                if h.is_equilibrium(u, alpha):
                    assert g.is_equilibrium(s, alpha)
                    lift_count += 1
            state_count += 1
        checked += 1
    return dict(games=checked, reduced_states=state_count,
                current_equalities=current_equalities,
                frozen_deviation_bounds=deviation_bounds,
                lifted_equilibria=lift_count)


def unicycle_audit():
    # Independently reconstruct the parent's two-player original resource game.
    g = Game({0: Q(1), 1: Q(2)},
             {0: ({0, 2}, {1}), 1: ({0, 1}, {3})},
             {0: Fee('poly', (0, 0, 1)), 1: Fee('poly', (0, Q(9, 2))),
              2: Fee('poly', (4,)), 3: Fee('poly', (Q(71, 4),))})
    actions = {0: (frozenset([0, 2]), frozenset([1])),
               1: (frozenset([0, 1]), frozenset([3]))}
    expected_costs = ((Q(13), Q(18)), (Q(5), Q(71, 4)),
                      (Q(27, 2), Q(35, 2)), (Q(9, 2), Q(71, 4)))
    expected = (Q(72, 71), Q(10, 9), Q(27, 26), Q(71, 70))
    rows = []
    for bits, ec, er in zip(product((0, 1), repeat=2), expected_costs, expected):
        state = {i: actions[i][bits[i]] for i in range(2)}
        costs = tuple(g.cost(i, state) for i in range(2))
        assert costs == ec
        alternatives = tuple(g.cost(i, state, actions[i][1-bits[i]]) for i in range(2))
        ratios = tuple(costs[i] / alternatives[i] for i in range(2))
        ratio = max([Q(1)] + list(ratios))
        assert ratio == er and ratio > 1
        assert sum(r > 1 for r in ratios) == 1
        assert any(costs[i] * ratio.denominator == alternatives[i] * ratio.numerator
                   for i in range(2))
        assert not g.is_equilibrium(state)
        rows.append({'state': ''.join(map(str, bits)),
                     'current_costs': list(map(str, costs)),
                     'deviation_costs': list(map(str, alternatives)),
                     'max_improvement': str(ratio)})
    edges = sum(len(nb) for nb in g.neighbors.values())
    vertices = len(g.weights) + len(g.fees)
    assert edges == vertices == 6 and edges - vertices + 1 == 1
    assert not g.is_forest()
    assert min(expected) == Q(72, 71)
    endpoint = {0: actions[0][0], 1: actions[1][0]}
    assert g.is_equilibrium(endpoint, Q(72, 71))
    return {'weights': [1, 2], 'cycle_rank': 1,
            'best_factor': '72/71', 'states': rows,
            'scope': 'Single fixed degree-2 example; not asymptotic or optimal.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output')
    args = ap.parse_args()
    seed = 20261015
    rng = random.Random(seed)
    out = {'title': '潜在使用森林精确均衡与挂树私人成本归约作者审计',
           'arithmetic': 'fractions.Fraction; exact comparisons; no tolerance',
           'seed': seed, 'star_background_cases': star_audit(),
           'forest': forest_audit(rng), 'single_core_player_lift': lift_audit(rng),
           'unicycle_boundary': unicycle_audit(),
           'scope': 'Finite audit only; does not prove universal existence outside the written tree class.',
           'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'status': 'passed'}
    if args.output:
        path = Path(args.output)
        if path.exists():
            raise SystemExit('Refusing to overwrite output: ' + str(path))
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
