"""路线整合审查：菜单组装、单位需求流与真矩仿射恢复的有限核验。

Stdlib exact arithmetic. Bounded exponential oracles are audit-only, never a
general scheduling algorithm. Writes to stdout; frozen records are not touched.
"""
from collections import deque
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def rref(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return a, []
    pivots = []
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col]:
                scale = a[i][col]
                a[i] = [x - scale*y for x, y in zip(a[i], a[rank])]
        pivots.append(col)
        rank += 1
        if rank == len(a):
            break
    return a, pivots


def affine_boolean_candidates(mu, covariance):
    """Enumerate cube points in mu+range(C), not necessarily true support."""
    d = len(mu)
    assert len(covariance) == d and all(len(row) == d for row in covariance)
    _, columns = rref(covariance)
    rank = len(columns)
    basis = [[covariance[i][j] for j in columns] for i in range(d)]
    _, coordinates = rref(list(zip(*basis)))
    assert len(coordinates) == rank
    square = [basis[i] for i in coordinates]
    result = set()
    for bits in product((0, 1), repeat=rank):
        rhs = [F(bit) - mu[i] for bit, i in zip(bits, coordinates)]
        reduced, pivots = rref([row + [y] for row, y in zip(square, rhs)])
        assert pivots == list(range(rank))
        z = [row[-1] for row in reduced]
        x = tuple(mu[i] + sum((basis[i][j]*z[j] for j in range(rank)), F(0))
                  for i in range(d))
        if all(t in (0, 1) for t in x):
            result.add(x)
    return rank, result


def moment_audit():
    cases = extra = rank_zero = 0
    for d in range(4):
        cube = list(product((0, 1), repeat=d))
        for mask in range(1, 1 << len(cube)):
            support = [x for i, x in enumerate(cube) if mask >> i & 1]
            for weighted in (False, True):
                # Deliberately include a large rational denominator.
                weights = [2**257 + 1 if weighted and i == 0 else i+1 if weighted else 1
                           for i in range(len(support))]
                total = sum(weights)
                mu = [sum((F(w*x[i], total) for w, x in zip(weights, support)), F(0))
                      for i in range(d)]
                cov = [[sum((F(w, total)*(x[i]-mu[i])*(x[j]-mu[j])
                             for w, x in zip(weights, support)), F(0))
                        for j in range(d)] for i in range(d)]
                rank, recovered = affine_boolean_candidates(mu, cov)
                assert set(support) <= recovered
                assert len(recovered) <= 2**rank
                if rank == 0:
                    assert recovered == {tuple(mu)} and len(support) == 1
                    rank_zero += 1
                extra += len(recovered - set(support))
                cases += 1
    expected = 2*sum(2**(2**d)-1 for d in range(4))
    assert cases == expected
    assert rank_zero == 2*sum(2**d for d in range(4))
    mu = [F(1, 2)]*3
    cov = [[F(1, 4) if i == j else F(-1, 8) for j in range(3)] for i in range(3)]
    rank, recovered = affine_boolean_candidates(mu, cov)
    assert rank == 2 and recovered == set()
    # C=(3I-J)/8 is PSD; every affine point has coordinate sum 3/2.
    assert all(sum(row) == 0 for row in cov)
    tiny_partition = []
    for numbers in ((1, 1), (1, 2, 3), (2, 2, 2), (1, 1, 1, 3)):
        B = F(sum(numbers), 2)
        assert max(numbers) <= B
        for delta, s in ((F(1, 3), 4), (F(1, 10), 11)):
            assert F(1, s) < delta
            lengths = [F(a)/(s*B) for a in numbers]
            assert all(0 < p < delta for p in lengths)
            yes = any(sum(a for a, side in zip(numbers, bits) if side) == B
                      for bits in product((0, 1), repeat=len(numbers)))
            feasible = any(max(F(s-1, s) + sum(p for p, side in zip(lengths, bits) if side == i)
                               for i in range(2)) <= 1
                           for bits in product((0, 1), repeat=len(numbers)))
            assert yes == feasible
            tiny_partition.append(dict(numbers=numbers, delta=str(delta), s=s, feasible=feasible))
    return dict(distributions=cases, count_backcheck=expected, rank_zero=rank_zero,
                extra_affine_candidates=extra,
                fake_psd_rank=rank, fake_psd_boolean_candidates=len(recovered),
                empty_big_partition_fixtures=tiny_partition,
                scope="All nonempty Boolean supports in dimensions 0..3, two exact weight schemes. No moment extractor and no truth-promise verifier.")


def menu_audit():
    mod = load("route_review_menu", HERE / "forest_two_boundary_menu.py")
    single = 0
    for p, q, eta in product((F(1, 3), F(1, 2), F(1), F(4, 3)),
                             (F(1, 3), F(1, 2), F(1), F(4, 3)),
                             (F(1, 10), F(1, 2), F(1))):
        menu, _ = mod.boundary_menu([{0: p, 1: q}], 0, 1, q, eta)
        pairs = {(x.a_load, x.b_load) for x in menu}
        assert pairs == {(p, F(0)), (F(0), q)}
        single += 1
    domains = [{a: p, b: q} for a, b in ((0, 1), (0, 2), (1, 2))
               for p, q in product((F(1, 2), F(1)), repeat=2)]
    cached = {}
    for i, dom in enumerate(domains):
        a, b = sorted(dom)
        menu, _ = mod.boundary_menu([dom], a, b, F(1), F(1, 3))
        cached[i] = [item.assignment[0] for item in menu]
        assert set(cached[i]) == set(dom)
    cases = assignment_count = 0
    for n in range(4):
        for ids in product(range(len(domains)), repeat=n):
            jobs = [domains[i] for i in ids]
            original = set(product(*(tuple(job) for job in jobs)))
            assembled = set(product(*(cached[i] for i in ids)))
            assert original == assembled
            def value(s):
                return max(sum((job[v] for job, v in zip(jobs, s) if v == i), F(0))
                           for i in range(3))
            assert min(map(value, original)) == min(map(value, assembled))
            assignment_count += len(original)
            cases += 1
    assert cases == sum(12**n for n in range(4))
    assert assignment_count == sum(24**n for n in range(4))
    # Zero endpoints need not force both outcomes: only verify real witnesses.
    zero = 0
    for p, q in product((F(0), F(1)), repeat=2):
        menu, _ = mod.boundary_menu([{0: p, 1: q}], 0, 1, F(0), F(1, 2))
        for item in menu:
            selected = item.assignment[0]
            assert item.a_load == (p if selected == 0 else 0)
            assert item.b_load == (q if selected == 1 else 0) == 0
        assert menu
        zero += 1
    return dict(positive_single_job_cases=single, assembled_instances=cases,
                assignments=assignment_count, zero_target_cases=zero,
                scope="Single-job coverage forces both positive endpoints; assembly identity only, no general menu-core approximation.")


def flow_paths(n, edges, demands):
    """Node-capacity maxflow, return vertex-disjoint root-terminal paths."""
    sink = 2*n
    cap = [[0]*(sink+1) for _ in range(sink+1)]
    for v in range(1, n):
        cap[2*v][2*v+1] = 1
        if demands[v] == 0:
            cap[2*v+1][sink] = 1
    for u, v in edges:
        cap[0 if u == 0 else 2*u+1][2*v] = n
    original = [row[:] for row in cap]
    value = 0
    while True:
        parent = {0: None}
        queue = deque([0])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, c in enumerate(cap[u]):
                if c and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        v = sink
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        value += 1
    used = [[max(0, original[u][v]-cap[u][v]) for v in range(sink+1)]
            for u in range(sink+1)]
    paths = []
    for _ in range(value):
        u = 0
        path = [0]
        while u != sink:
            v = next(v for v, amount in enumerate(used[u]) if amount)
            used[u][v] -= 1
            if v != sink and v % 2 == 0:
                path.append(v//2)
            u = v
        paths.append(path)
    return value, paths


def tree_score(n, edges, chosen, k):
    if any(edge not in edges for edge in chosen):
        return None
    ind = [0]*n
    out = [[] for _ in range(n)]
    for u, v in chosen:
        ind[v] += 1
        out[u].append(v)
    if ind[0] or max(ind) > 1:
        return None
    reach = {0}
    for u in range(n):
        if u in reach:
            reach.update(out[u])
    if any(u not in reach for u, v in chosen):
        return None
    return min([F(1)] + [F(len(out[v]), k[v]) for v in reach if k[v]])


def flow_audit():
    bridge = load("route_review_bridge", HERE / "rooted_dag_token_bridge.py")
    cases = trees = 0
    for n in range(1, 5):
        pool = [(u, v) for u in range(n) for v in range(u+1, n)]
        for bits in product((0, 1), repeat=len(pool)):
            edges = [edge for edge, take in zip(pool, bits) if take]
            nonsinks = {u for u, v in edges}
            free = [v for v in range(1, n) if v not in nonsinks]
            for terminal_bits in product((0, 1), repeat=len(free)):
                for root_k in (1, 2, 5, 2**101+3):
                    k = [root_k] + [1]*(n-1)
                    for v, terminal in zip(free, terminal_bits):
                        k[v] = 0 if terminal else 1
                    nu, paths = flow_paths(n, edges, k)
                    expected = min(F(1), F(nu, root_k))
                    best = F(0)
                    for mask in range(1 << len(edges)):
                        chosen = [e for i, e in enumerate(edges) if mask >> i & 1]
                        beta = tree_score(n, edges, chosen, k)
                        if beta is not None:
                            best = max(best, beta)
                        trees += 1
                    assert best == expected
                    selected = [e for path in paths[:min(root_k, nu)]
                                for e in zip(path, path[1:])]
                    assert tree_score(n, edges, selected, k) == best
                    jobs, schedule = bridge.tree_to_schedule(n, edges, k, selected)
                    actual = [F(0)]*n
                    for (_, domain), i in zip(jobs, schedule):
                        assert i in dict(domain)
                        actual[i] += dict(domain)[i]
                    assert max(actual) == 2-best
                    cases += 1
    # Independent generating-function counts (do not reuse graph traversal).
    expected_cases = sum(4*2**(n-1)*prod(2**h+1 for h in range(n-1))
                         for n in range(1, 5))
    expected_trees = sum(4*3**(n-1)*prod(3**h+1 for h in range(n-1))
                         for n in range(1, 5))
    assert cases == expected_cases and trees == expected_trees
    # Root-terminal case is a different branch, never divide by its demand.
    jobs, assignment = bridge.tree_to_schedule(1, [], [0], [])
    assert max(bridge.loads(1, jobs, assignment)) == 1
    alias = []
    for m in range(2, 9):
        # r, u_i, g_i, b_i, private z_i, shared z_0.
        n = 4*m+2
        z0 = n-1
        edges = []
        restricted = []
        for i in range(m):
            u, g, b, z = 1+i, 1+m+i, 1+2*m+i, 1+3*m+i
            edges += [(0, u), (u, g), (u, b), (g, z), (b, z0)]
            restricted += [(0, u), (u, b), (b, z0)]
        k = [m] + [1]*(3*m) + [0]*(m+1)
        full, _ = flow_paths(n, edges, k)
        frozen, _ = flow_paths(n, restricted, k)
        assert full == m and frozen == 1
        alias.append(dict(m=m, full_ratio="1", frozen_ratio=str(F(1, m))))
    return dict(instances=cases, tree_subsets=trees, root_terminal_cases=1,
                alias_examples=alias,
                scope="All topologically labelled DAGs n<=4; each nonroot nonsink demand1, every sink independently terminal/deadend; four root demands including 102-bit demand. Exponential oracle only for audit.")


def bounded_demand_audit():
    cases = trees = 0
    for K in (2, 3):
        for n in range(1, 5):
            pool = [(u, v) for u in range(n) for v in range(u+1, n)]
            for bits in product((0, 1), repeat=len(pool)):
                edges = [e for e, take in zip(pool, bits) if take]
                nonsinks = {u for u, v in edges}
                domains = [(1, K) if v in nonsinks else (0, 1, K) for v in range(1, n)]
                for nonroot in product(*domains):
                    for root_k in (1, 2, 5, 2**101+3):
                        k = [root_k] + list(nonroot)
                        best = F(0)
                        for mask in range(1 << len(edges)):
                            chosen = [e for i, e in enumerate(edges) if mask >> i & 1]
                            beta = tree_score(n, edges, chosen, k)
                            if beta is not None:
                                best = max(best, beta)
                            trees += 1
                        nu, paths = flow_paths(n, edges, k)
                        chosen = [e for path in paths[:min(root_k, nu)]
                                  for e in zip(path, path[1:])]
                        beta = tree_score(n, edges, chosen, k)
                        assert beta >= min(best, F(1, K)) >= best/K
                        assert 2-beta <= (2-F(1, K))*(2-best)
                        # Reversal of the symbolic claimed difference.
                        assert (2-F(1, K))*(2-best)-(2-best/K) == 2*(1-F(1, K))*(1-best)
                        cases += 1
    expected = 2*sum(4*2**(n-1)*prod(2**(h+1)+1 for h in range(n-1)) for n in range(1, 5))
    expected_trees = 2*sum(4*3**(n-1)*prod(2*3**h+1 for h in range(n-1)) for n in range(1, 5))
    assert cases == expected and trees == expected_trees
    return dict(instances=cases, tree_subsets=trees, K_values=[2, 3], count_backcheck=expected,
                scope="n<=4 all topological DAGs; nonroot positive demands in {1,K}, sink additionally 0; four root demands. Standard maxflow corollary, not general scheduling progress.")


def main():
    deps = [HERE / "forest_two_boundary_menu.py", HERE / "rooted_dag_token_bridge.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in deps}
    result = dict(title="共同容量路线拼接接口的有限独立审查", python=platform.python_version(),
                  arithmetic="integers / fractions.Fraction; exact", seed=None,
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashes, menu=menu_audit(), flow=flow_audit(),
                  bounded_demand=bounded_demand_audit(),
                  moments=moment_audit(),
                  limits="Not a general <2 algorithm, hardness experiment, novelty certification, full review of imported implementations, or proof of universal conclusions.")
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in deps}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
