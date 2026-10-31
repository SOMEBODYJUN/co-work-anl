#!/usr/bin/env python3
"""Finite crosscheck of the frozen abstract-matroid exchange audit, n <= 5.

Independence augmentation, set-based exchange arcs and Floyd-Warshall are
rebuilt independently of the source's basis axiom, bitset arcs and BFS.
This script does not prove any assertion for larger ground sets.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "matroid_exchange_diameter_independent.py"
RERUN = HERE / "matroid_exchange_diameter_independent_rerun.json"
ROOT = next(p for p in HERE.parents if (p / "cleanup/OBJECTS.md").is_file())
FROZEN = ROOT / "archives/fair-allocation/tools/evidence/retired-topic-selection-fair-results-20261031/matroid_exchange_diameter_independent_20261020.json"


def powerset(items):
    items = tuple(items)
    return (frozenset(c) for size in range(len(items) + 1)
            for c in itertools.combinations(items, size))


def independent_sets(bases):
    return set().union(*(set(powerset(b)) for b in bases))


def augmentation_holds(ind):
    return all(any(a | {e} in ind for e in b - a)
               for a in ind for b in ind if len(a) < len(b))


def exchange_arcs(n, bases, profile):
    return frozenset((r, s) for b in profile for r in b
                     for s in set(range(n)) - b
                     if (b - {r}) | {s} in bases)


def encode(n, arcs):
    return sum(1 << (r * n + s) for r, s in arcs)


def floyd(n, arcs):
    d = [[0 if a == b else n + 1 for b in range(n)] for a in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for a, b in arcs:
        d[a][b], nxt[a][b] = 1, b
    for c in range(n):
        for a in range(n):
            for b in range(n):
                if d[a][c] + d[c][b] < d[a][b]:
                    d[a][b] = d[a][c] + d[c][b]
                    nxt[a][b] = nxt[a][c]
    return d, nxt


def decode(mask, n):
    return frozenset(i for i in range(n) if mask & (1 << i))


def run():
    assert __debug__, "Run without -O: assertions are part of this finite audit."
    spec = importlib.util.spec_from_file_location("frozen_matroid_probe", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rerun = json.loads(RERUN.read_text())
    frozen = json.loads(FROZEN.read_text())
    assert rerun == frozen
    expected_rows = {(r["n"], r["rank"]): r for r in rerun["strata"]}
    totals = {k: 0 for k in rerun["totals"]}
    candidates = 0
    compared_source_distances = 0
    max_distance_by_delta = {}
    rows = []
    for n in range(6):
        ground = frozenset(range(n))
        for rank in range(n + 1):
            possible = tuple(frozenset(c) for c in itertools.combinations(ground, rank))
            row = dict(n=n, rank=rank, **{k: 0 for k in totals})
            for bfamily in powerset(possible):
                if not bfamily:
                    continue
                candidates += 1
                ind = independent_sets(bfamily)
                independent_axioms = frozenset() in ind and augmentation_holds(ind)
                # Heredity holds by construction: ind contains all subsets of bases.
                bitbases = [sum(1 << e for e in b) for b in bfamily]
                assert independent_axioms == module.is_basis_family(bitbases)
                if not independent_axioms:
                    continue
                row["matroids"] += 1
                dependent = [s for s in powerset(ground) if s not in ind]
                g = min(map(len, dependent)) if dependent else None
                assert g == module.girth(n, bitbases)
                graphs = set()
                for profile in powerset(bfamily):
                    if not profile:
                        continue
                    row["profiles"] += 1
                    graphs.add(exchange_arcs(n, bfamily, profile))
                row["distinct_graphs"] += len(graphs)
                for arcs in graphs:
                    d, _ = floyd(n, arcs)
                    graph = encode(n, arcs)
                    for a in range(n):
                        source_d = module.distances(n, graph, a)
                        for b in range(n):
                            expected = d[a][b] if d[a][b] <= n else None
                            assert source_d[b] == expected
                            compared_source_distances += 1
                            if a == b or expected is None:
                                continue
                            row["reachable_pairs"] += 1
                            assert g is not None and expected <= rank - g + 3
                            delta = str(rank - g)
                            max_distance_by_delta[delta] = max(expected, max_distance_by_delta.get(delta, 0))
            assert row == expected_rows[n, rank], row
            rows.append(row)
            for k in totals:
                totals[k] += row[k]
    assert totals == rerun["totals"]
    witnesses = {}
    for delta, w in rerun["longest_witnesses"].items():
        n = w["n"]
        bases = tuple(decode(b, n) for b in w["bases"])
        ind = independent_sets(bases)
        assert augmentation_holds(ind)
        assert int(delta) == w["rank"] - w["girth"]
        profile = next(p for p in powerset(bases) if p
                       and encode(n, exchange_arcs(n, bases, p)) == w["graph"])
        arcs = exchange_arcs(n, bases, profile)
        d, nxt = floyd(n, arcs)
        a, b = w["source"], w["target"]
        assert d[a][b] == w["distance"] == max_distance_by_delta[delta]
        path = [a]
        while path[-1] != b:
            path.append(nxt[path[-1]][b])
        circuits = [s for s in powerset(range(n)) if s not in ind
                    and all(s - {e} in ind for e in s)]
        witnesses[delta] = dict(
            n=n, rank=w["rank"], girth=w["girth"], distance=w["distance"],
            bound=w["bound"], source=a, target=b, path=path,
            bases=[sorted(t) for t in bases],
            one_profile=[sorted(t) for t in sorted(profile, key=lambda t: tuple(sorted(t)))],
            arcs=[list(t) for t in sorted(arcs)],
            circuits=[sorted(t) for t in circuits],
        )
    return dict(
        status="finite semantics crosscheck passed", python=platform.python_version(),
        assertions_enabled=__debug__, max_n=5, candidate_nonempty_equal_size_families=candidates,
        totals=totals, rows=rows, compared_source_distance_entries=compared_source_distances,
        max_distance_by_delta=max_distance_by_delta, reconstructed_witnesses=witnesses,
        rerun_equals_frozen_json=True,
        source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        rerun_sha256=hashlib.sha256(RERUN.read_bytes()).hexdigest(),
        frozen_sha256=hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
        scope="All abstract labelled matroids and nonempty basis supports for 0<=n<=5; no claim for larger n, arbitrary deleted-arc graphs, game costs, or novelty.",
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().with_suffix(".json")
    result = run()
    with out.open("x") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({k: result[k] for k in (
        "status", "candidate_nonempty_equal_size_families", "totals",
        "compared_source_distance_entries", "max_distance_by_delta",
        "rerun_equals_frozen_json")}, ensure_ascii=False, indent=2))
