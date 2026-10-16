#!/usr/bin/env python3
"""Frozen-code conformance against the independent per-leaf oracle."""
from fractions import Fraction
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import platform
import random
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignment_optimum(neigh, child_k, root_k, w):
    """Self-contained oracle: enumerate each leaf's center or unused state."""
    best = Fraction(0)
    for dest in product(range(-1, len(neigh)), repeat=w):
        count = [0] * len(neigh)
        valid = True
        for leaf, center in enumerate(dest):
            if center < 0:
                continue
            if not (neigh[center] >> leaf & 1):
                valid = False
                break
            count[center] += 1
        if not valid:
            continue
        selected = [i for i, d in enumerate(count) if d]
        if not selected:
            continue
        value = min([Fraction(1), Fraction(len(selected), root_k)] +
                    [Fraction(count[i], child_k[i]) for i in selected])
        best = max(best, value)
    return best


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path,
                        default=Path(__file__).resolve().parents[3],
                        help='repository root; defaults to three parents above tests/audits/unrelated_machines')
    args = parser.parse_args()
    repo = args.repo.resolve()
    canonical = repo / 'tests/audits/unrelated_machines/depth_two_quota_greedy.py'
    manuscript = repo / 'research/current/unrelated_machines/rooted_dag_degree_token_bridge.md'
    code_hash, text_hash = sha(canonical), sha(manuscript)
    sys.path.insert(0, str(canonical.parent))
    from depth_two_quota_greedy import depth_two_half, tree_to_schedule
    seed = 197604919
    rng = random.Random(seed)
    total = disconnected = nonzero_roots = huge = 0
    magnitude = 2**130 + 33
    for _ in range(1000):
        u, w = rng.randrange(5), rng.randrange(6)
        n = 1 + u + w
        labels = list(range(n))
        rng.shuffle(labels)
        root = labels[0]
        centers = labels[1:1+u]
        leaves = labels[1+u:]
        ks = (1, 2, 3, 5, magnitude)
        child = tuple(rng.choice(ks) for _ in centers)
        root_k = rng.choice(ks)
        neighbors = tuple(rng.randrange(1 << w) for _ in centers)
        adjacent = tuple(rng.randrange(2) for _ in centers)
        edges = [(root, v) for v, use in zip(centers, adjacent) if use]
        edges += [(v, leaves[j]) for v, mask in zip(centers, neighbors)
                  for j in range(w) if mask >> j & 1]
        demands = [0] * n
        demands[root] = root_k
        for v, k in zip(centers, child):
            demands[v] = k
        chosen = depth_two_half(n, edges, demands, root)
        assert len(chosen) == len(set(chosen))
        assert set(chosen) <= set(edges)
        incoming = [0] * n
        degree = [0] * n
        for a, b in chosen:
            incoming[b] += 1
            degree[a] += 1
        assert incoming[root] == 0 and max(incoming) <= 1
        seen, todo = {root}, [root]
        while todo:
            a = todo.pop()
            for x, b in chosen:
                if x == a and b not in seen:
                    seen.add(b)
                    todo.append(b)
        assert all(a in seen and b in seen for a, b in chosen)
        got = min([Fraction(1)] + [Fraction(degree[v], demands[v])
                                  for v in seen if demands[v]])
        opt = assignment_optimum(tuple(mask for mask, a in zip(neighbors, adjacent) if a),
                                 tuple(k for k, a in zip(child, adjacent) if a),
                                 root_k, w)
        assert 2 * got >= opt
        jobs, assignment = tree_to_schedule(n, edges, demands, chosen, root)
        assert len(jobs) == len(assignment)
        actual_load = [Fraction(0)] * n
        for (_, domain), machine in zip(jobs, assignment):
            processing = dict(domain)
            assert machine in processing
            actual_load[machine] += processing[machine]
        actual = max(actual_load)
        assert actual <= 2 - got
        assert 2 * actual <= 3 * (2 - opt)
        total += 1
        disconnected += int(any(not a for a in adjacent))
        nonzero_roots += int(root != 0)
        huge += int(magnitude in demands)
    assert sha(canonical) == code_hash
    assert sha(manuscript) == text_hash
    print(json.dumps({'status':'passed','seed':seed,'inputs':total,
                      'with_disconnected_centers':disconnected,
                      'with_nonzero_root_label':nonzero_roots,
                      'with_131bit_demand':huge,
                      'canonical_sha256':code_hash,
                      'manuscript_sha256':text_hash,
                      'script_sha256':sha(Path(__file__)),
                      'oracle':'independent per-leaf destination enumeration',
                      'input_domain':'1000 seeded random instances; U<=4,W<=5; root labels shuffled; missing root edges permitted; demands in {1,2,3,5,2**130+33}',
                      'python':platform.python_version(),
                      'arithmetic':'exact integers and Fraction',
                      'limits':'Finite implementation conformance only; general proof and novelty are separate.'},indent=2))


if __name__ == '__main__':
    main()
