#!/usr/bin/env python3
"""Finite exact replay of the independently reviewed private-missing spectrum.

The all-SPE path enumerator is the repository implementation. Coverage, maximal
sets, private blocks, spectral values, and individual utilities are recomputed
below directly from named unit-customer sets using Fraction arithmetic.
This finite replay is not a proof of the general theorem.
"""

from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def union(sets):
    return set().union(*sets)


def direct_utilities(sets, path):
    clients = union(sets)
    load = {x: sum(x in sets[a] for a in path) for x in clients}
    return tuple(sum((F(1, load[x]) for x in sets[a]), F(0))
                 for a in path)


def spectrum(sets, path):
    m = len(path)
    maxima = [B for B in sets if not any(B < T for T in sets)]
    private = [B - union(T for T in maxima if T != B) for B in maxima]
    covered = union(sets[a] for a in path)
    missing = [P - covered for P in private]
    seats = sorted((F(len(Q), k) + F(len(B) - len(Q), m)
                    for B, Q in zip(maxima, missing)
                    for k in range(1, m + 1)), reverse=True)
    return private, covered, seats


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def run():
    catalog_pairs = paths = corollary_paths = position_checks = 0
    for family in range(1, 1 << 8):
        sets = [frozenset(x for x in range(3) if mask >> x & 1)
                for mask in range(8) if family >> mask & 1]
        for m in range(1, 4):
            instance = Instance.from_topic_sets(sets, players=m)
            solver = ExactSPESolver(instance)
            catalog_pairs += 1
            possible_unions = [set()]
            for size in range(1, min(m, len(sets)) + 1):
                possible_unions.extend(union(support)
                                       for support in combinations(sets, size))
            optimum = max(map(len, possible_unions))
            optimum_unions = [O for O in possible_unions if len(O) == optimum]
            for path in solver.ordered_outcomes():
                paths += 1
                private, covered, seats = spectrum(sets, path)
                utility = direct_utilities(sets, path)
                assert sum(utility) == len(covered)
                for i in range(m):
                    position_checks += 1
                    assert utility[i] >= seats[m - i - 1], (
                        sets, m, path, utility, seats)
                assert sum(utility) >= sum(seats[:m])
                if any(O - covered <= union(private) for O in optimum_unions):
                    corollary_paths += 1
                    assert (2 * m - 1) * len(covered) >= m * optimum

    # Explicit all-zero/empty and m=1 edges, apart from their inclusion above.
    zero_edges = []
    for m in (1, 2, 3, 6):
        sets = [frozenset()]
        path = (0,) * m
        private, covered, seats = spectrum(sets, path)
        assert covered == set() and seats == [F(0)] * m
        assert direct_utilities(sets, path) == (F(0),) * m
        zero_edges.append({"m": m, "W": 0, "OPT": 0})

    # The on/off-path always-A policy is checked through every prefix count.
    # This represents every ordered history because this policy is constant.
    sharp = []
    for m in range(1, 7):
        sets = [frozenset(range(m))]
        sets.extend(frozenset({m + j}) for j in range(m - 1))
        prefixes = comparisons = 0
        for elapsed in range(m):
            remaining = m - elapsed
            for counts in compositions(elapsed, m):
                prefixes += 1
                selected = F(m, counts[0] + remaining)
                for action in range(m):
                    comparisons += 1
                    deviation = (selected if action == 0
                                 else F(1, counts[action] + 1))
                    assert selected >= deviation
        path = (0,) * m
        _, covered, seats = spectrum(sets, path)
        assert len(covered) == m and seats[:m] == [F(1)] * m
        optimum = 2 * m - 1
        assert m * optimum == (2 * m - 1) * len(covered)
        sharp.append({"m": m, "W": m, "OPT": optimum,
                      "prefix_count_states": prefixes,
                      "all_action_comparisons": comparisons})

    return {
        "status": "PASS",
        "scope": "All 255 nonempty catalogs on three named unit customers; m=1,2,3; exact all-SPE ordered paths",
        "catalog_player_pairs": catalog_pairs,
        "all_SPE_ordered_paths": paths,
        "position_inequalities_checked": position_checks,
        "private_missing_corollary_paths": corollary_paths,
        "zero_empty_edges": zero_edges,
        "sharp_all_big_family": sharp,
        "limitations": "Uses the repository all-SPE path enumerator; does not independently audit that enumerator and does not prove the general theorem."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
