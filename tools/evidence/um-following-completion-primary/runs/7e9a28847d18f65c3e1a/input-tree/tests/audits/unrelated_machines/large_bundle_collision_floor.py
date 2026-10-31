#!/usr/bin/env python3
"""大需求标签束的碰撞分组、整数配额匹配与实际根树分数。

Core contract (q > 0): bundles[x] is a nonempty set of K_x distinct
nonnegative integer resource IDs, 1 <= c <= q, and Delta is the largest
resource multiplicity.  Return an actual allocation with score at least

    Lambda_c = min(ceil(q/c)/q,
                   min_x floor(K_x*c/(c+Delta-1))/K_x).

Colors are zero based.  Only the largest color class is selected; each
selected bundle corresponds to one distinct label of a depth-three demand
tree with root demand q, intermediate demand 1, and label demand K_x.
Unselected allocation entries are empty.  Empty-family convention: c=0,
score=Lambda=1, Delta=0.  This convention is outside the positive-root theorem.

The construction has polynomial total bit complexity in the explicit
bundle incidence list.  It uses integer local improvement and capacitated
bipartite matching, not a combinatorial optimum oracle.  The exhaustive
oracle is nested inside audit() and is never called by the constructor.
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction


def _validated_bundles(bundles, c):
    """Materialize an explicit ordered family; reject silent coercions."""
    if type(bundles) not in (list, tuple):
        raise ValueError("bundles must be an explicit list or tuple")
    if type(c) is not int:
        raise ValueError("c must be an integer, not bool or float")
    q = len(bundles)
    if (q == 0 and c != 0) or (q > 0 and not 1 <= c <= q):
        raise ValueError("use c=0 for q=0; otherwise require 1<=c<=q")
    clean = []
    for bundle in bundles:
        if type(bundle) not in (list, tuple, set, frozenset):
            raise ValueError("each bundle must be an explicit integer collection")
        values = tuple(bundle)
        if not values:
            raise ValueError("individual bundles must be nonempty")
        if any(type(a) is not int or a < 0 for a in values):
            raise ValueError("resource IDs must be nonnegative integers")
        if len(set(values)) != len(values):
            raise ValueError("duplicate resource ID inside a bundle")
        clean.append(tuple(sorted(values)))
    return tuple(clean)


def _quota_matching(bundles, selected, quotas):
    """Deterministic integral capacitated matching, without recursion.

    Each augmentation adds one resource to its starting bundle.  Other
    reached bundles exchange resources along the alternating path, keeping
    their current cardinality.  There are at most sum(K_x) augmentations;
    a breadth-first search scans at most the explicit incidence list.
    """
    owner = {}
    allocated = [set() for _ in bundles]
    for start in selected:
        for _ in range(quotas[start]):
            pending = deque([start])
            visited_bundles = {start}
            predecessor_resource = {}
            predecessor_bundle = {}
            free = None
            while pending and free is None:
                x = pending.popleft()
                for a in bundles[x]:
                    if a in predecessor_resource:
                        continue
                    predecessor_resource[a] = x
                    if a not in owner:
                        free = a
                        break
                    y = owner[a]
                    if y not in visited_bundles:
                        visited_bundles.add(y)
                        predecessor_bundle[y] = a
                        pending.append(y)
            if free is None:
                raise RuntimeError("proved Hall quota invariant was violated")
            a = free
            while True:
                x = predecessor_resource[a]
                owner[a] = x
                allocated[x].add(a)
                if x == start:
                    break
                previous = predecessor_bundle[x]
                allocated[x].remove(previous)
                a = previous
    return [sorted(resources) for resources in allocated]


def construct_collision_floor(bundles, c):
    """Return colors, disjoint resources, score, Fraction Lambda, and path.

    Accepted input: list/tuple family, each bundle a list/tuple/set/frozenset
    of distinct nonnegative Python int IDs.  Arbitrarily large IDs are
    compressed by sorting; no loop depends on their numeric magnitude.
    All validation failures raise ValueError.

    Output fields: colors, selected, allocation, quotas, score, Lambda, delta,
    c, potential_path, steps.  The potential path contains its initial
    value and every strict decrease.  Fractions remain exact API objects.
    """
    bundles = _validated_bundles(bundles, c)
    q = len(bundles)
    if q == 0:
        return {
            "colors": [], "selected": [], "allocation": [], "quotas": [],
            "score": Fraction(1), "Lambda": Fraction(1), "delta": 0, "c": 0,
            "potential_path": [0], "steps": 0,
        }

    resources = sorted({a for bundle in bundles for a in bundle})
    index = {a: i for i, a in enumerate(resources)}
    encoded = [tuple(index[a] for a in bundle) for bundle in bundles]
    degrees = [0] * len(resources)
    for bundle in encoded:
        for a in bundle:
            degrees[a] += 1
    delta = max(degrees)
    sizes = [len(bundle) for bundle in bundles]
    colors = [0] * q
    counts = [[degree] + [0] * (c - 1) for degree in degrees]
    potential = sum(degree * (degree - 1) // 2 for degree in degrees)
    potential_path = [potential]

    # Psi = sum_{resource,color} binom(d_color(resource), 2).
    # Fixed input order and the first strict improvement make this deterministic.
    while True:
        move = None
        for x, bundle in enumerate(encoded):
            old = colors[x]
            old_cost = sum(counts[a][old] - 1 for a in bundle)
            for new in range(c):
                if new == old:
                    continue
                new_cost = sum(counts[a][new] for a in bundle)
                if new_cost < old_cost:
                    move = (x, old, new, old_cost - new_cost)
                    break
            if move is not None:
                break
        if move is None:
            break
        x, old, new, decrease = move
        for a in encoded[x]:
            counts[a][old] -= 1
            counts[a][new] += 1
        colors[x] = new
        potential -= decrease
        potential_path.append(potential)

    color_sizes = [0] * c
    for color in colors:
        color_sizes[color] += 1
    chosen_color = max(range(c), key=lambda z: (color_sizes[z], -z))
    selected = [x for x in range(q) if colors[x] == chosen_color]
    denominator = c + delta - 1
    quotas = [size * c // denominator for size in sizes]
    allocation = _quota_matching(bundles, selected, quotas)
    score = min(
        [Fraction(1), Fraction(len(selected), q)]
        + [Fraction(len(allocation[x]), sizes[x]) for x in selected]
    )
    lower = min(
        [Fraction((q + c - 1) // c, q)]
        + [Fraction(quotas[x], sizes[x]) for x in range(q)]
    )
    return {
        "colors": colors, "selected": selected, "allocation": allocation,
        "quotas": quotas, "score": score, "Lambda": lower, "delta": delta,
        "c": c, "potential_path": potential_path,
        "steps": len(potential_path) - 1,
    }


def audit():
    """Finite exact audit; exhaustive optimum search lives only here."""
    import hashlib
    import importlib.util
    from itertools import product
    from math import isqrt
    from pathlib import Path

    bridge_path = Path(__file__).with_name("rooted_dag_token_bridge.py")
    bridge_spec = importlib.util.spec_from_file_location(
        "large_bundle_floor_token_bridge_audit", bridge_path,
    )
    bridge = importlib.util.module_from_spec(bridge_spec)
    bridge_spec.loader.exec_module(bridge)
    bridge_records = []
    proof_relative = "research/current/unrelated_machines/large_bundle_collision_square_root_floor.md"
    proof_path = Path(__file__).resolve().parents[3] / proof_relative

    def true_score(bundles, selected, allocation):
        q = len(bundles)
        if q == 0:
            return Fraction(1)
        if not selected:
            return Fraction(0)
        used = set()
        for x in selected:
            if len(allocation[x]) != len(set(allocation[x])):
                raise AssertionError("duplicate actual resource")
            for a in allocation[x]:
                assert a in bundles[x] and a not in used
                used.add(a)
        return min(
            [Fraction(1), Fraction(len(selected), q)]
            + [Fraction(len(allocation[x]), len(bundles[x])) for x in selected]
        )

    def exact_one_label_optimum(bundles):
        # Completing a partial allocation cannot decrease the best score:
        # unused incident resources may be assigned arbitrarily, and the best
        # selected subset is recovered from sorted achieved bundle ratios.
        resources = sorted(set().union(*(set(bundle) for bundle in bundles)))
        choices = [tuple(x for x, bundle in enumerate(bundles) if a in bundle)
                   for a in resources]
        best = Fraction(0)
        for sigma in product(*choices):
            counts = [0] * len(bundles)
            for x in sigma:
                counts[x] += 1
            ratios = sorted(
                (Fraction(counts[x], len(bundles[x]))
                 for x in range(len(bundles))), reverse=True,
            )
            score = max(
                min(Fraction(s, len(bundles)), ratios[s - 1])
                for s in range(1, len(bundles) + 1)
            )
            best = max(best, score)
        return best

    def check_token_schedule(name, bundles, c, result):
        """Build the actual DAG, tree, token jobs, and every machine load."""
        q = len(bundles)
        resources = sorted({a for bundle in bundles for a in bundle})
        resource_vertex = {a: 1 + 2 * q + i for i, a in enumerate(resources)}
        n = 1 + 2 * q + len(resources)
        demands = [q] + [1] * q + [len(bundle) for bundle in bundles] \
            + [0] * len(resources)
        edges = [(0, 1 + x) for x in range(q)] \
            + [(1 + x, 1 + q + x) for x in range(q)] \
            + [(1 + q + x, resource_vertex[a])
               for x, bundle in enumerate(bundles) for a in bundle]
        chosen = []
        for x in result["selected"]:
            chosen.extend([(0, 1 + x), (1 + x, 1 + q + x)])
            chosen.extend((1 + q + x, resource_vertex[a])
                          for a in result["allocation"][x])
        assert bridge.score(n, chosen, demands) == result["score"]
        jobs, sigma = bridge.tree_to_schedule(n, edges, demands, chosen)
        assert len(jobs) == len(sigma)
        # Independently total each actual assignment from the original job
        # domains; do not rely exclusively on bridge.loads or its assertions.
        loads = [Fraction(0)] * n
        for (_, domain), machine in zip(jobs, sigma):
            assert type(machine) is int
            options = dict(domain)
            assert machine in options
            loads[machine] += options[machine]
        assert loads == bridge.loads(n, jobs, sigma)
        makespan = max(loads)
        assert makespan <= 2 - result["score"]
        decoded = None
        decoded_score = None
        if makespan < 2:
            decoded = bridge.decode(n, edges, demands, jobs, sigma)
            assert all(edge in edges for edge in decoded)
            decoded_score = bridge.score(n, decoded, demands)
            assert decoded_score >= 2 - makespan
        bridge_records.append({
            "name": name, "bundles": [list(bundle) for bundle in bundles],
            "c": c, "colors": result["colors"],
            "selected": result["selected"], "allocation": result["allocation"],
            "Lambda": result["Lambda"], "tree_score": result["score"],
            "vertices": n, "edges": edges, "demands": demands,
            "chosen_tree_edges": chosen, "job_count": len(jobs),
            "sigma": sigma, "loads": loads, "makespan": makespan,
            "decoded_edges": decoded, "decoded_score": decoded_score,
        })

    def verify(bundles, c, result):
        q = len(bundles)
        assert result["score"] == true_score(
            bundles, result["selected"], result["allocation"],
        )
        assert result["score"] >= result["Lambda"]
        assert result["steps"] + 1 == len(result["potential_path"])
        assert all(a > b for a, b in zip(
            result["potential_path"], result["potential_path"][1:],
        ))
        if q == 0:
            assert result["delta"] == 0 and result["potential_path"] == [0]
            return
        colors = result["colors"]
        assert len(colors) == q and all(0 <= color < c for color in colors)
        resources = set().union(*(set(bundle) for bundle in bundles))
        delta = max(sum(a in bundle for bundle in bundles) for a in resources)
        assert delta == result["delta"]
        potential = 0
        for a in resources:
            for color in range(c):
                d = sum(a in bundles[x] and colors[x] == color for x in range(q))
                potential += d * (d - 1) // 2
        assert potential == result["potential_path"][-1]
        assert result["steps"] <= (delta - 1) * sum(map(len, bundles)) // 2
        expected_Lambda = min(
            [Fraction((q + c - 1) // c, q)]
            + [Fraction(len(bundle) * c // (c + delta - 1), len(bundle))
               for bundle in bundles]
        )
        assert result["Lambda"] == expected_Lambda
        for x, bundle in enumerate(bundles):
            own_sum = sum(
                sum(a in bundles[y] and colors[y] == colors[x] for y in range(q))
                for a in bundle
            )
            assert own_sum * c <= len(bundle) * (c + delta - 1)
        assert len(result["selected"]) * c >= q
        selected_set = set(result["selected"])
        assert all(not result["allocation"][x] for x in range(q)
                   if x not in selected_set)
        assert all(len(result["allocation"][x]) == result["quotas"][x]
                   for x in result["selected"])

    boundary = construct_collision_floor([], 0)
    verify([], 0, boundary)
    check_token_schedule("empty-terminal-root", [], 0, boundary)
    zero_quota_bundles = [[0], [0]]
    zero_quota = construct_collision_floor(zero_quota_bundles, 1)
    verify(zero_quota_bundles, 1, zero_quota)
    assert zero_quota["score"] == zero_quota["Lambda"] == 0
    check_token_schedule("positive-label-zero-quota", zero_quota_bundles, 1,
                         zero_quota)
    assert bridge_records[-1]["makespan"] == 2
    large_ids = [[0, 10**120], [10**120, 10**121], [10**121, 10**122]]
    for c in range(1, len(large_ids) + 1):
        verify(large_ids, c, construct_collision_floor(large_ids, c))
    assert construct_collision_floor([{9, 2}, frozenset({2, 8})], 2) == \
        construct_collision_floor([[2, 9], [2, 8]], 2)
    invalid = [
        (None, 0), ("bundles", 1), ({0: [1]}, 1), ([None], 1),
        ([[]], 1), ([[0, 0]], 1), ([[-1]], 1), ([[True]], 1),
        ([[1.0]], 1), ([["1"]], 1), ([[0]], True), ([[0]], 1.0),
        ([[0]], 0), ([[0]], -1), ([[0]], 2), ([], 1), ([], False),
    ]
    for bundles, c in invalid:
        try:
            construct_collision_floor(bundles, c)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input was accepted")

    # The final augmentation traverses a chain longer than Python's usual
    # recursion limit.  This is a direct matching regression, not an oracle.
    chain_size = 1200
    chain = [(x, x + 1) for x in range(chain_size - 1)] + [(0,)]
    chain_allocation = _quota_matching(
        chain, list(range(chain_size)), [1] * chain_size,
    )
    assert all(len(row) == 1 and row[0] in chain[x]
               for x, row in enumerate(chain_allocation))
    assert len({a for row in chain_allocation for a in row}) == chain_size

    instances = color_runs = strict_improvements = recomputed_improvements = 0
    for resource_count in range(1, 5):
        families = [
            tuple(a for a in range(resource_count) if mask >> a & 1)
            for mask in range(1, 1 << resource_count)
        ]
        for q in range(1, 4):
            for bundles in product(families, repeat=q):
                optimum = exact_one_label_optimum(bundles)
                for c in range(1, q + 1):
                    result = construct_collision_floor(bundles, c)
                    verify(bundles, c, result)
                    assert result["score"] <= optimum
                    if color_runs < 30:
                        check_token_schedule("exhaustive-color-run-" + str(color_runs),
                                             bundles, c, result)
                    color_runs += 1
                    strict_improvements += result["steps"]
                    recomputed_improvements += len(result["potential_path"]) - 1
                instances += 1
    expected_instances = sum(
        (2**resources - 1)**q
        for resources in range(1, 5) for q in range(1, 4)
    )
    assert instances == expected_instances
    assert strict_improvements == recomputed_improvements

    # A common pool has exact value max_s min(s/q, floor(K/s)/K).
    # These small cases independently enumerate all actual resource assignments.
    small_pool_cases = 0
    for q in range(1, 5):
        for K in range(1, 7):
            bundles = (tuple(range(K)),) * q
            formula = max(
                min(Fraction(s, q), Fraction(K // s, K))
                for s in range(1, min(q, K) + 1)
            )
            assert exact_one_label_optimum(bundles) == formula
            small_pool_cases += 1

    square_pools = []
    for t in range(1, 7):
        q = K = t * t
        bundles = (tuple(range(K)),) * q
        c = isqrt(q) + 1 if t >= 2 else 1
        result = construct_collision_floor(bundles, c)
        verify(bundles, c, result)
        optimum = Fraction(1, t)
        witness_selected = list(range(t))
        witness_allocation = [[] for _ in range(q)]
        for x in witness_selected:
            witness_allocation[x] = list(range(x * t, (x + 1) * t))
        assert true_score(bundles, witness_selected, witness_allocation) == optimum
        # General counting proof: beta^2*q <= 1; equality at the witness.
        assert optimum * optimum * q == 1
        assert result["Lambda"] == result["score"] == optimum
        if t <= 3:
            check_token_schedule("square-pool-t-" + str(t), bundles, c, result)
        square_pools.append({
            "q": q, "K": K, "delta": q, "c": c,
            "exact_optimum": optimum,
            "algorithm_score": result["score"], "Lambda": result["Lambda"],
            "algorithm_selected": result["selected"],
            "algorithm_allocation": {
                x: result["allocation"][x] for x in result["selected"]
            },
            "optimum_witness": {
                x: witness_allocation[x] for x in witness_selected
            },
            "steps": result["steps"],
        })
    return {
        "status": "passed", "arithmetic": "fractions.Fraction and integers",
        "precision": "exact fractions.Fraction and integers; no numerical tolerance",
        "seed": None,
        "exhaustive_bundle_instances": instances, "color_runs": color_runs,
        "strict_improving_moves": strict_improvements,
        "strict_improving_moves_recomputed_from_paths": recomputed_improvements,
        "exhaustive_scope": {"q": [1, 3], "resource_count": [1, 4]},
        "oracle": "all resource-to-incident-bundle assignments; best selected subset",
        "invalid_cases_rejected": len(invalid),
        "empty_family_convention": "q=0,c=0,score=Lambda=1; outside positive-root theorem",
        "large_resource_ID_cases": len(large_ids),
        "nonrecursive_augmenting_chain_size": chain_size,
        "small_common_pool_oracle_cases": small_pool_cases,
        "square_pool_witnesses": square_pools,
        "token_bridge": {
            "source": "tests/audits/unrelated_machines/rooted_dag_token_bridge.py",
            "code_sha256": hashlib.sha256(bridge_path.read_bytes()).hexdigest(),
            "actual_schedules_checked": len(bridge_records),
            "below_two_decoded": sum(row["makespan"] < 2 for row in bridge_records),
            "alpha_zero_cases": sum(row["tree_score"] == 0 for row in bridge_records),
            "records": bridge_records,
        },
        "source_proof": {
            "path": proof_relative,
            "sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
            "claim_id": "UM-LARGE-BUNDLE-COLLISION-FLOOR-v1",
            "scope": "finite executable checks only; this output does not assign canonical status",
            "mechanism": "defective-coloring potential, Cauchy, capacitated Hall",
            "external_theorem_imports": [],
        },
        "limits": [
            "finite audits do not replace the general proof",
            "no general MMDA or unrelated-machines approximation is claimed",
            "no novelty or computational-hardness claim",
        ],
    }


def main():
    import argparse
    import hashlib
    import json
    from pathlib import Path
    import platform
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="write a NEW JSON result; refuse existing files")
    args = parser.parse_args()
    result = audit()
    result["python"] = platform.python_version()
    result["runtime"] = {
        "implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["commands"] = {
        "actual_argv": [sys.executable, *sys.argv],
        "stdout_reproduction": [
            "python3", "tests/audits/unrelated_machines/large_bundle_collision_floor.py",
        ],
    }

    def encode(value):
        if isinstance(value, Fraction):
            return str(value)
        raise TypeError(type(value).__name__)

    payload = json.dumps(result, default=encode, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(payload)
        print(json.dumps({"status": "passed", "output": str(args.output)},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
