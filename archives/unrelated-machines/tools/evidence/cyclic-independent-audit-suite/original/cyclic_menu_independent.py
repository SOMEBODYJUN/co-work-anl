#!/usr/bin/env python3
"""Exact independent audit; imports no repository implementation.

This finite computation checks the three-machine fork family and the abstract
strict-turn SCC / machine-simple cycle equivalence. General proofs are separate.
"""
from fractions import Fraction as F
from itertools import product, permutations
from random import Random
import hashlib
import json
from pathlib import Path
import sys


def load_vector(P, assignment, m):
    return tuple(sum((P[j][i] for j, i in enumerate(assignment) if i == v), F(0))
                 for v in range(m))


def compatible_cycle(arcs):
    if not arcs:
        return False
    return all(arcs[i][1] == arcs[(i + 1) % len(arcs)][0] and
               arcs[i][3] <= arcs[(i + 1) % len(arcs)][2]
               for i in range(len(arcs)))


def strict_cycle(arcs):
    return compatible_cycle(arcs) and any(
        arcs[i][3] < arcs[(i + 1) % len(arcs)][2]
        for i in range(len(arcs)))


def exhaustive_simple_cycles(menu, m):
    by_pair = {}
    for a in menu:
        by_pair.setdefault(a[:2], []).append(a)
    for length in range(2, m + 1):
        for machines in permutations(range(m), length):
            if machines[0] != min(machines):
                continue
            choices = [by_pair.get((machines[i], machines[(i + 1) % length]), [])
                       for i in range(length)]
            for arcs in product(*choices):
                if strict_cycle(arcs):
                    return tuple(arcs)
    return None


def linegraph_closure_cycle(menu):
    """Use explicit transitive closure, independently of Tarjan/Kosaraju code."""
    n = len(menu)
    adjacency = [[menu[a][1] == menu[b][0] and menu[a][3] <= menu[b][2]
                  for b in range(n)] for a in range(n)]
    reach = [row[:] for row in adjacency]
    for a in range(n):
        reach[a][a] = True
    for k in range(n):
        for a in range(n):
            if reach[a][k]:
                for b in range(n):
                    reach[a][b] = reach[a][b] or reach[k][b]
    for a in range(n):
        for b in range(n):
            if adjacency[a][b] and menu[a][3] < menu[b][2] and reach[b][a]:
                # Obtain any return path by breadth-first search.
                queue, predecessor = [b], {b: None}
                for x in queue:
                    if x == a:
                        break
                    for y in range(n):
                        if adjacency[x][y] and y not in predecessor:
                            predecessor[y] = x
                            queue.append(y)
                assert a in predecessor
                backwards, x = [], a
                while x is not None:
                    backwards.append(x)
                    x = predecessor[x]
                path = list(reversed(backwards))
                cycle = [menu[x] for x in [a] + path[:-1]]
                assert strict_cycle(cycle)
                # A repeated source splits the closed walk into two branches.
                # Directly verify both branches, rather than importing the
                # proposed removal-comparison shortcut implementation.
                while len({x[0] for x in cycle}) < len(cycle):
                    first = {}
                    repeated = None
                    for j, arc in enumerate(cycle):
                        if arc[0] in first:
                            repeated = first[arc[0]], j
                            break
                        first[arc[0]] = j
                    i, j = repeated
                    options = [cycle[i:j], cycle[j:] + cycle[:i]]
                    valid = [x for x in options if strict_cycle(x)]
                    assert valid, (cycle, i, j)
                    shorter = min(valid, key=len)
                    assert len(shorter) < len(cycle)
                    cycle = shorter
                assert strict_cycle(cycle)
                return tuple(cycle)
    return None


def menu_audit():
    rng = Random(613512)
    tested, found = 0, 0
    for m in range(2, 5):
        for _ in range(1000):
            menu = []
            for u in range(m):
                for v in range(m):
                    if u == v:
                        continue
                    for _ in range(rng.randrange(3)):
                        removal = F(rng.randrange(9), 4)
                        arrival = F(rng.randrange(13), 4)
                        menu.append((u, v, removal, arrival))
            direct = exhaustive_simple_cycles(menu, m)
            closure = linegraph_closure_cycle(menu)
            assert (direct is None) == (closure is None), menu
            if closure is not None:
                assert len({a[0] for a in closure}) == len(closure)
                assert strict_cycle(closure)
                found += 1
            tested += 1
    return {"seed": 613512, "random_explicit_menus": tested,
            "menus_with_strict_machine_simple_cycle": found,
            "machine_range": [2, 4],
            "scope": "Finite exact test; rational removal/arrival weights need not arise from one scheduling instance."}


def main():
    result = {"status": "passed", "arithmetic": "fractions.Fraction",
              "python": sys.version.split()[0],
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "explicit_menu_equivalence": menu_audit(),
              "limitations": ["Finite independent graph audit, not a general proof.",
                              "Weights need not arise from one scheduling instance."]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
