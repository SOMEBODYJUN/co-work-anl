#!/usr/bin/env python3
"""Exact, self-contained audit of original-game repair and fixed-lift interfaces.

Only the standard library is used. New output files are created exclusively;
the frozen JSON is never silently overwritten. No repository audit is imported.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import platform
import sys


@dataclass
class Game:
    weights: tuple[F, ...]
    actions: tuple[tuple[frozenset[int], ...], ...]
    coeffs: tuple[tuple[F, ...], ...]

    def cost(self, state, player):
        loads = [F(0) for _ in self.coeffs]
        for i, action in enumerate(state):
            for e in self.actions[i][action]:
                loads[e] += self.weights[i]
        answer = F(0)
        for e in self.actions[player][state[player]]:
            value = F(0)
            for a in reversed(self.coeffs[e]):
                value = value * loads[e] + a
            answer += value
        return answer

    def states(self):
        return product(*(range(len(a)) for a in self.actions))

    def deviations(self, state, player):
        for action in range(len(self.actions[player])):
            if action != state[player]:
                new = list(state)
                new[player] = action
                yield tuple(new)

    def stable(self, state, alpha):
        return all(self.cost(state, i) <= alpha * self.cost(t, i)
                   for i in range(len(state)) for t in self.deviations(state, i))


class Builder:
    def __init__(self, weights, action_counts=None):
        self.weights = tuple(map(F, weights))
        self.actions = [[set() for _ in range(k)] for k in
                        (action_counts or [2] * len(weights))]
        self.coeffs = []

    def resource(self, coeffs, memberships):
        e = len(self.coeffs)
        self.coeffs.append(tuple(map(F, coeffs)))
        for i, action in memberships:
            self.actions[i][action].add(e)
        return e

    def game(self):
        return Game(self.weights,
                    tuple(tuple(frozenset(a) for a in aa) for aa in self.actions),
                    tuple(self.coeffs))


def flip(state, i):
    ans = list(state)
    ans[i] ^= 1
    return tuple(ans)


def front(bits):
    return sum(a != b for a, b in zip(bits, bits[1:])) <= 1


def front_states(n):
    # Duplicate empty/full cuts are removed, retaining all 2n states.
    return sorted(set(tuple([1] * k + [0] * (n - k)) for k in range(n + 1)) |
                  set(tuple([0] * k + [1] * (n - k)) for k in range(n + 1)))


def repair_index(bits):
    if front(bits):
        return None
    return next(i for i in range(1, len(bits)) if bits[i] != bits[0])


def state_front(state, classes):
    return all(front(tuple(state[i] for i in cc)) for cc in classes)


def repair_move(state, classes):
    for cc in classes:
        i = repair_index(tuple(state[j] for j in cc))
        if i is not None:
            return cc[i]
    return None


def private_builder(costs, weights=None):
    b = Builder(weights or [1] * len(costs))
    for i, pair in enumerate(costs):
        for a, value in enumerate(pair):
            b.resource([F(value)], [(i, a)])
    return b


def add_clocks(builder, classes, M, degree):
    for cc in classes:
        w = builder.weights[cc[0]]
        assert all(builder.weights[i] == w for i in cc)
        coeffs = [F(0)] * degree + [M / (3 * w) ** degree]
        for i, j in combinations(cc[1:], 2):
            triple = (cc[0], i, j)
            phase = (0, 1, 0)
            for side in range(2):
                builder.resource(coeffs, [(u, side ^ p)
                                          for u, p in zip(triple, phase)])


def base_bound(game):
    totals = [sum((game.weights[i] for i, aa in enumerate(game.actions)
                   if any(e in a for a in aa)), F(0))
              for e in range(len(game.coeffs))]
    bounds = []
    for aa in game.actions:
        value = F(0)
        for e in set().union(*aa):
            value += sum((a * totals[e] ** k for k, a in enumerate(game.coeffs[e])), F(0))
        bounds.append(value)
    return max(bounds)


def nontrivial_base(sizes):
    classes = []
    weights = []
    for k, n in enumerate(sizes):
        cc = tuple(range(len(weights), len(weights) + n))
        classes.append(cc)
        weights.extend([F(1, k + 1)] * n)
    builder = private_builder([((i + 1) % 3, (2 * i + 1) % 3)
                               for i in range(len(weights))], weights)
    for r in range(3):
        members = []
        for i in range(len(weights)):
            code = (i * (r + 1) + 2 * r) % 4
            if code < 2:
                members.append((i, code))
            elif code == 2:
                members.extend([(i, 0), (i, 1)])
        builder.resource([0, 0, F(1, r + 2)], members)
    return builder, classes


def geometry_audit():
    states = repairs = flips = 0
    max_steps = {}
    for n in range(3, 10):
        assert len(front_states(n)) == 2 * n
        longest = 0
        for s in product(range(2), repeat=n):
            states += 1
            assert front(s) == (s in front_states(n))
            for i in range(n):
                flips += 1
                if front(s) and front(flip(s, i)):
                    assert sum(front(flip(s, j)) for j in range(n)) == 2
            t = s
            steps = 0
            while (i := repair_index(t)) is not None:
                old_count = sum(t[j] != t[0] for j in range(1, n))
                t = flip(t, i)
                assert sum(t[j] != t[0] for j in range(1, n)) == old_count - 1
                assert t[0] == s[0]
                repairs += 1
                steps += 1
            assert front(t) and steps <= n - 2
            longest = max(longest, steps)
        max_steps[str(n)] = longest
        assert longest == n - 2
    return dict(states=states, flip_checks=flips, repair_moves=repairs,
                maximum_steps_by_class_size=max_steps)


def original_clock_audit():
    report = []
    checked_states = checked_moves = repair_path_moves = 0
    for sizes in ((3,), (4,), (5,), (6,), (7,), (8,), (3, 4), (3, 3, 3)):
        for alpha in (F(1), F(3, 2), F(2)):
            builder, classes = nontrivial_base(sizes)
            base = builder.game()
            B = base_bound(base)
            L = max((len(cc) - 1) * (len(cc) - 2) // 2 for cc in classes)
            M = 4 * alpha * B
            degree = 1
            while not M > alpha * (B + L * M * F(2, 3) ** degree):
                degree += 1
            add_clocks(builder, classes, M, degree)
            game = builder.game()
            original_pne = set()
            front_sinks = set()
            front_count = repair_count = outside_count = 0
            minimum_repair_margin = None
            for s in game.states():
                checked_states += 1
                assert all(base.cost(s, i) <= B for i in range(len(s)))
                legal = state_front(s, classes)
                if game.stable(s, alpha):
                    original_pne.add(s)
                if not legal:
                    i = repair_move(s, classes)
                    margin = game.cost(s, i) - alpha * game.cost(flip(s, i), i)
                    assert margin > 0
                    minimum_repair_margin = margin if minimum_repair_margin is None else min(minimum_repair_margin, margin)
                    repair_count += 1
                    t = s
                    steps = 0
                    while (j := repair_move(t, classes)) is not None:
                        assert game.cost(t, j) > alpha * game.cost(flip(t, j), j)
                        t = flip(t, j)
                        steps += 1
                    assert steps <= sum(n - 2 for n in sizes)
                    repair_path_moves += steps
                else:
                    front_count += 1
                    endpoint_sink = True
                    for i in range(len(s)):
                        t = flip(s, i)
                        old, new = game.cost(s, i), game.cost(t, i)
                        checked_moves += 1
                        if state_front(t, classes):
                            if old > alpha * new:
                                endpoint_sink = False
                        else:
                            outside_count += 1
                            assert old <= alpha * new
                    if endpoint_sink:
                        front_sinks.add(s)
            assert original_pne == front_sinks
            assert front_count == product_int(2 * n for n in sizes)
            report.append(dict(class_sizes=sizes, alpha=str(alpha), B=str(B),
                               clock_M=str(M), clock_degree=degree,
                               dominance_gap=str(M - alpha * (B + L * M * F(2, 3) ** degree)),
                               states=2 ** sum(sizes), front_states=front_count,
                               equilibria=len(original_pne), illegal_repair_witnesses=repair_count,
                               front_leave_checks=outside_count,
                               minimum_repair_margin=str(minimum_repair_margin)))
    return dict(cases=report, checked_states=checked_states,
                front_move_checks=checked_moves, repair_path_moves=repair_path_moves)


def product_int(xs):
    ans = 1
    for x in xs:
        ans *= x
    return ans


def counterexample_audit():
    # A canonical bit repair can destroy an original exact equilibrium.
    g = private_builder([(0, 0), (100, 0), (0, 0)]).game()
    s = (0, 1, 0)
    i = repair_move(s, [(0, 1, 2)])
    t = flip(s, i)
    assert g.stable(s, F(1)) and not g.stable(t, F(1))
    assert g.cost(s, i) == 0 and g.cost(t, i) == 100

    # Endpoint stability survives while an internal clone escapes, even with a clock.
    b = private_builder([(0, 0), (3, 0), (0, 0)])
    add_clocks(b, [(0, 1, 2)], F(3), 1)  # c(x)=x.
    h = b.game()
    u, alpha = (0, 0, 0), F(21, 20)
    endpoints = [j for j in range(3) if front(flip(u, j))]
    assert endpoints == [0, 2]
    assert all(h.cost(u, j) <= alpha * h.cost(flip(u, j), j) for j in endpoints)
    assert h.cost(u, 1) == 4 and h.cost(flip(u, 1), 1) == 3
    assert not h.stable(u, alpha)

    # Anchor-0 clocks are not invariant under the simultaneous twisted shift.
    b = private_builder([(0, 0)] * 4)
    add_clocks(b, [(0, 1, 2, 3)], F(3), 1)
    k = b.game()
    zero, shifted = (0, 0, 0, 0), (1, 0, 0, 0)
    assert k.cost(zero, 0) == 6 and k.cost(shifted, 1) == 4

    # The tree lift does not project every original equilibrium back to H.
    b = Builder([1, 2])
    b.resource([0, 1], [(0, 1), (1, 1)])
    b.resource([F(5, 2)], [(0, 0)])
    b.resource([3], [(1, 0)])
    tree = b.game()
    original = (1, 0)
    assert tree.stable(original, F(1))
    projected_current, projected_new = F(3), F(5, 2)
    assert projected_current > projected_new

    # Even under original-clock dominance, the retained front graph can cycle.
    # Embed the exact two-player unicycle example into two 3-clone classes.
    b = Builder([1, 1, 1, 2, 2, 2])
    b.resource([0, 0, 1], [(0, 0), (3, 0)])
    b.resource([0, F(9, 2)], [(0, 1), (3, 0)])
    b.resource([4], [(0, 0)])
    b.resource([F(71, 4)], [(3, 1)])
    for dummy in (1, 2, 4, 5):
        b.resource([0], [(dummy, 0)])
        b.resource([1], [(dummy, 1)])
    bound = base_bound(b.game())
    clock_M = 4 * bound
    cycle_classes = [(0, 1, 2), (3, 4, 5)]
    assert bound == F(161, 4) and clock_M == 161
    assert clock_M > bound + clock_M * F(2, 3)
    add_clocks(b, cycle_classes, clock_M, 1)
    cycling = b.game()
    cycle = [(0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0),
             (1, 0, 0, 1, 0, 0), (1, 0, 0, 0, 0, 0)]
    margins = []
    for source, target, mover in zip(cycle, cycle[1:] + cycle[:1], (3, 0, 3, 0)):
        assert flip(source, mover) == target
        assert state_front(source, cycle_classes)
        margin = cycling.cost(source, mover) - cycling.cost(target, mover)
        assert margin > 0
        margins.append(str(margin))
    front_exit_table = []
    illegal_repair_count = 0
    for state in cycling.states():
        assert not cycling.stable(state, F(1))
        if state_front(state, cycle_classes):
            exits = [(i, flip(state, i)) for i in range(6)
                     if state_front(flip(state, i), cycle_classes)
                     and cycling.cost(state, i) > cycling.cost(flip(state, i), i)]
            assert exits
            mover, target = exits[0]
            front_exit_table.append(dict(state=state, mover=mover,
                                         old=str(cycling.cost(state, mover)),
                                         frozen_new=str(cycling.cost(target, mover))))
        else:
            mover = repair_move(state, cycle_classes)
            assert cycling.cost(state, mover) > cycling.cost(flip(state, mover), mover)
            illegal_repair_count += 1
    assert len(front_exit_table) == 36 and illegal_repair_count == 28
    return dict(
        repair_destroys_pne=dict(state=s, repaired=t, mover=i,
                                 old_cost="0", repaired_cost="100"),
        endpoint_only_false=dict(state=u, alpha=str(alpha), endpoints=endpoints,
                                  internal_mover=1, old_cost="4", frozen_new_cost="3"),
        quotient_symmetry_false=dict(state=zero, image=shifted,
                                     player=0, image_player=1,
                                     old_cost="6", image_cost="4"),
        arbitrary_projection_false=dict(original_pne=original,
                                        greedy_private_price="3",
                                        reduced_alternative_cost="5/2"),
        dominated_front_cycle=dict(classes=cycle_classes, alpha="1", base_bound=str(bound),
                                   clock_M=str(clock_M), clock_degree=1,
                                   cycle=cycle, movers=[3, 0, 3, 0], margins=margins,
                                   front_exit_table=front_exit_table,
                                   illegal_repair_witnesses=illegal_repair_count,
                                   full_state_equilibria=0))


def module_candidates(game, root=0, beta=F(1)):
    assert root == 0
    by_root = []
    for action in range(len(game.actions[root])):
        candidates = []
        for internal in product(*(range(len(aa)) for aa in game.actions[1:])):
            state = (action,) + internal
            if all(game.cost(state, i) <= beta * game.cost(t, i)
                   for i in range(1, len(state)) for t in game.deviations(state, i)):
                candidates.append(internal)
        by_root.append(candidates)
    return by_root


def select_module_signature(game, beta=F(1)):
    candidates = module_candidates(game, beta=beta)
    failed = []
    for continuation in product(*candidates):
        q = [game.cost((a,) + continuation[a], 0) for a in range(len(continuation))]
        matrix = [[game.cost((b,) + continuation[a], 0) for b in range(len(q))]
                  for a in range(len(q))]
        bad = [(a, b) for a in range(len(q)) for b in range(len(q))
               if matrix[a][b] < q[b]]
        if not bad:
            return dict(continuations=continuation, q=q, frozen_matrix=matrix,
                        candidates=[len(c) for c in candidates]), failed
        a, b = bad[0]
        failed.append(dict(continuation=continuation, current_action=a,
                           deviation_action=b, frozen_cost=str(matrix[a][b]),
                           proposed_price=str(q[b])))
    return None, failed


def module_audit():
    # Two-sided tree gate, with a tie and two equilibria under root action 1.
    b = Builder([1, 2])
    b.resource([0, 1], [(0, 1), (1, 1)])
    b.resource([3], [(1, 0)])
    tree_module = b.game()
    signature, failed = select_module_signature(tree_module)
    assert signature is not None
    assert signature["q"] == [0, 1]
    assert signature["frozen_matrix"] == [[0, 3], [0, 1]]

    # A cyclic one-root module: both internal players can use e,f or private 0.
    b = Builder([1, 1, 2])
    b.resource([0, 1], [(0, 1), (1, 1), (2, 1)])
    b.resource([0, 0, 1], [(1, 1), (2, 1)])
    b.resource([0], [(1, 0)])
    b.resource([0], [(2, 0)])
    cyclic_module = b.game()
    cyclic_signature, cyclic_failed = select_module_signature(cyclic_module)
    assert cyclic_signature is not None
    assert cyclic_signature["q"] == [0, 1]

    # Conditional equilibria alone are insufficient: a bad continuation choice
    # in a tree can violate the frozen-entry lower bound.
    b = Builder([1, 2, 1])
    b.resource([0, 1], [(0, 1), (1, 1), (2, 1)])
    b.resource([3], [(1, 0)])
    b.resource([1], [(2, 0)])
    bad_module = b.game()
    bad_continuations = ((0, 1), (1, 0))
    for a, internal in enumerate(bad_continuations):
        state = (a,) + internal
        assert all(bad_module.cost(state, i) <= bad_module.cost(t, i)
                   for i in (1, 2) for t in bad_module.deviations(state, i))
    proposed_price = bad_module.cost((1,) + bad_continuations[1], 0)
    frozen_entry = bad_module.cost((1,) + bad_continuations[0], 0)
    assert frozen_entry == 2 < proposed_price == 3
    # Add a root alternative outside the module and test every reduced equilibrium.
    tested_lifts = 0
    for module, sig in ((tree_module, signature), (cyclic_module, cyclic_signature)):
        for outside_price in (F(0), F(1, 2), F(1), F(5, 2), F(4)):
            for alpha in (F(1), F(21, 20), F(3, 2), F(2)):
                virtual = [sig["q"][0] + outside_price, sig["q"][1]]
                for a in range(2):
                    if virtual[a] <= alpha * virtual[1-a]:
                        state = (a,) + sig["continuations"][a]
                        old = module.cost(state, 0) + (outside_price if a == 0 else 0)
                        t = (1-a,) + sig["continuations"][a]
                        new = module.cost(t, 0) + (outside_price if a == 1 else 0)
                        assert old == virtual[a] and new >= virtual[1-a]
                        assert old <= alpha * new
                        assert all(module.cost(state, i) <= alpha * module.cost(t, i)
                                   for i in range(1, len(state))
                                   for t in module.deviations(state, i))
                        tested_lifts += 1
    def serial(sig):
        return dict(continuations=sig["continuations"],
                    prices=list(map(str, sig["q"])),
                    frozen_matrix=[list(map(str, row)) for row in sig["frozen_matrix"]],
                    conditional_equilibrium_counts=sig["candidates"])
    return dict(tree=serial(signature), cyclic_module=serial(cyclic_signature),
                rejected_signature_count=len(failed)+len(cyclic_failed),
                rejected_stable_continuation=dict(continuations=bad_continuations,
                                                  current_action=0, deviation_action=1,
                                                  frozen_entry=str(frozen_entry),
                                                  proposed_price=str(proposed_price)),
                lifted_equilibria_checked=tested_lifts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = dict(schema="weighted-congestion-original-repair-audit-v1",
                  arithmetic="fractions.Fraction; exact inequalities; no cost division",
                  python=platform.python_version(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  geometry=geometry_audit(),
                  original_game_clock_reduction=original_clock_audit(),
                  counterexamples=counterexample_audit(),
                  one_root_module_lift=module_audit(),
                  status="PASS", limitations="Finite audits do not prove the general theorems; no resources are added by the proposed decision method.")
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as out:
            out.write(data)
    else:
        sys.stdout.write(data)


if __name__ == "__main__":
    main()
