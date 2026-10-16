"""Exact grid DP for one-boundary batch reassignment on a machine forest.

All arithmetic is Fraction/integer. This file is an exact research implementation of a restricted interface,
not a general R||Cmax approximation algorithm. The objective machine's load is
kept exact. Every other machine is relaxed by at most eta*T.
"""

from fractions import Fraction as F
from itertools import product
from random import Random
import json
import platform


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def load_vector(m, jobs, assignment):
    load = [F(0) for _ in range(m)]
    for j, i in enumerate(assignment):
        load[i] += jobs[j][i]
    return load


def brute(m, jobs, root, capacities):
    """Independent assignment enumeration, minimizing exact root load."""
    best = None
    witness = None
    for a in product(*(tuple(sorted(j)) for j in jobs)):
        load = load_vector(m, jobs, a)
        if all(load[i] <= capacities[i] for i in range(m) if i != root):
            if best is None or load[root] < best:
                best, witness = load[root], a
    return best, witness


def boundary_oracle(m, jobs, root, target, eta):
    """Compress unused machine indices before running the dense prototype."""
    if m < 1 or not 0 <= root < m or target < 0 or eta <= 0:
        raise ValueError("invalid parameters")
    if any(not ps or len(ps) > 2 or any(not 0 <= i < m or p < 0 for i, p in ps.items()) for ps in jobs):
        raise ValueError("invalid job")
    active = sorted({root}.union(*(set(ps) for ps in jobs)))
    position = {v: i for i, v in enumerate(active)}
    dense_jobs = [{position[i]: p for i, p in ps.items()} for ps in jobs]
    out = _boundary_oracle_dense(len(active), dense_jobs, position[root], target, eta)
    if out is None:
        return None
    value, assignment, meta = out
    meta["q"] = [{active[i]: p for i, p in ps.items()} for ps in meta["q"]]
    return value, tuple(active[i] for i in assignment), meta


def _boundary_oracle_dense(m, jobs, root, target, eta):
    """Return (minimum grid-relaxed root load, assignment, grid metadata).

    jobs[j] is a nonempty dict i -> Fraction processing time. At most two
    endpoints are allowed. The simple machine graph must be a forest.
    Singleton jobs are fixed. No root capacity is imposed.

    If a schedule with all nonroot loads <= target exists, the method returns
    a schedule with all nonroot loads <= (1+eta)*target and root load no
    larger than the minimum root load of any target-feasible schedule.
    A None result certifies no target-feasible schedule exists.
    """
    if m < 1 or not 0 <= root < m or target < 0 or eta <= 0:
        raise ValueError("invalid parameters")
    n = len(jobs)
    bundles = {}
    fixed = [[] for _ in range(m)]
    adj = [[] for _ in range(m)]
    parent_dsu = list(range(m))

    def find(v):
        while parent_dsu[v] != v:
            parent_dsu[v] = parent_dsu[parent_dsu[v]]
            v = parent_dsu[v]
        return v

    for j, ps in enumerate(jobs):
        if not ps or len(ps) > 2:
            raise ValueError("one or two available machines required")
        if any(not 0 <= i < m or p < 0 for i, p in ps.items()):
            raise ValueError("invalid job")
        vertices = tuple(sorted(ps))
        if len(vertices) == 1:
            fixed[vertices[0]].append(j)
        else:
            if vertices not in bundles:
                u, v = vertices
                fu, fv = find(u), find(v)
                if fu == fv:
                    raise ValueError("machine graph is not a forest")
                parent_dsu[fu] = fv
                adj[u].append(v)
                adj[v].append(u)
                bundles[vertices] = []
            bundles[vertices].append(j)

    if n == 0:
        return F(0), (), {"K": 0, "delta": F(0), "q": []}
    if target == 0:
        assignment = []
        for ps in jobs:
            # Root objective is exact; zero internal endpoints take priority.
            zero_internal = [i for i in sorted(ps) if i != root and ps[i] == 0]
            if zero_internal:
                assignment.append(zero_internal[0])
            elif root in ps:
                assignment.append(root)
            else:
                return None
        load = load_vector(m, jobs, assignment)
        return load[root], tuple(assignment), {"K": 0, "delta": F(0), "q": []}

    delta = eta * target / n
    K = (F(n) * (1 + 1 / eta)).numerator // (F(n) * (1 + 1 / eta)).denominator
    q = [{i: ceil_fraction(p / delta) for i, p in ps.items()} for ps in jobs]

    # Root the objective component at root; root any other component arbitrarily.
    parent = [None] * m
    children = [[] for _ in range(m)]
    order = []
    roots = []
    for start in [root] + [i for i in range(m) if i != root]:
        if parent[start] is not None:
            continue
        roots.append(start)
        parent[start] = -1
        stack = [start]
        while stack:
            v = stack.pop()
            order.append(v)
            for w in sorted(adj[v], reverse=True):
                if w == parent[v]:
                    continue
                parent[w] = v
                children[v].append(w)
                stack.append(w)

    # Node residual is in its own rounded units, unless this is objective root.
    residual = [None] * m
    choice = {}
    minimum = [None] * m

    def bundle_dp(u, v, capacity):
        """Minimum burden at u, while bundle load at child v <= capacity."""
        js = bundles[tuple(sorted((u, v)))]
        dp = [None] * (capacity + 1)
        dp[0] = F(0) if u == root else 0
        layers = []
        for j in js:
            ndp = [None] * (capacity + 1)
            prev = [None] * (capacity + 1)
            for d, value in enumerate(dp):
                if value is None:
                    continue
                parent_cost = jobs[j][u] if u == root else q[j][u]
                pv = value + parent_cost
                if ndp[d] is None or pv < ndp[d]:
                    ndp[d], prev[d] = pv, (d, u)
                child_cost = q[j][v]
                if d + child_cost <= capacity:
                    if ndp[d + child_cost] is None or value < ndp[d + child_cost]:
                        ndp[d + child_cost], prev[d + child_cost] = value, (d, v)
            dp = ndp
            layers.append(prev)
        valid = [(value, d) for d, value in enumerate(dp) if value is not None]
        if not valid:
            return None
        value, d = min(valid)
        assignments = []
        for layer, j in reversed(list(zip(layers, js))):
            old_d, machine = layer[d]
            assignments.append((j, machine))
            d = old_d
        return value, assignments

    for v in reversed(order):
        value = sum((jobs[j][v] if v == root else q[j][v] for j in fixed[v]), F(0) if v == root else 0)
        for w in children[v]:
            result = bundle_dp(v, w, residual[w])
            if result is None:
                return None
            burden, witness = result
            value += burden
            choice[v, w] = witness
        minimum[v] = value
        if v != root:
            if value > K:
                return None
            residual[v] = K - value
    assignment = [None] * n
    for v in range(m):
        for j in fixed[v]:
            assignment[j] = v
    for witness in choice.values():
        for j, v in witness:
            assignment[j] = v
    assert all(i is not None for i in assignment)
    load = load_vector(m, jobs, assignment)
    assert load[root] == minimum[root]
    assert all(load[v] <= (1 + eta) * target for v in range(m) if v != root)
    return minimum[root], tuple(assignment), {"K": K, "delta": delta, "q": q}


def run_audit():
    rng = Random(9162026)
    cases = 0
    positive = 0
    rejected = 0
    # Independent exhaustive oracle uses rounded integer capacities on internal nodes.
    for m in range(1, 6):
        for _ in range(100):
            edges = [(v, rng.randrange(v)) for v in range(1, m) if rng.randrange(4)]
            n = rng.randrange(9)
            jobs = []
            for j in range(n):
                if edges and rng.randrange(4):
                    u, v = rng.choice(edges)
                    jobs.append({u: F(rng.randrange(9), rng.randrange(1, 8)), v: F(rng.randrange(9), rng.randrange(1, 8))})
                else:
                    v = rng.randrange(m)
                    jobs.append({v: F(rng.randrange(9), rng.randrange(1, 8))})
            root = rng.randrange(m)
            target = F(rng.randrange(7), rng.randrange(1, 6))
            eta = rng.choice([F(1, 2), F(1, 3), F(1, 5)])
            out = boundary_oracle(m, jobs, root, target, eta)
            exact, exact_witness = brute(m, jobs, root, [target] * m)
            if out is None:
                assert exact is None
                rejected += 1
            else:
                value, witness, meta = out
                if exact is not None:
                    assert value <= exact
                if target > 0 and jobs:
                    rounded_jobs = [{i: F(q) if i != root else jobs[j][i] for i, q in ps.items()} for j, ps in enumerate(meta["q"])]
                    grid_exact, _ = brute(m, rounded_jobs, root, [F(meta["K"])] * m)
                    assert value == grid_exact
                load = load_vector(m, jobs, witness)
                assert all(load[i] <= (1 + eta) * target for i in range(m) if i != root)
                positive += 1
            cases += 1

    # A nonlocal repair stress test: both big jobs and arbitrarily many smalls move.
    # A has two unit jobs with alternatives B,C; B,C have 2k smalls, alternative A.
    stress = []
    for k in [1, 2, 3, 10, 50]:
        jobs = [{0: F(1), 1: F(1)}, {0: F(1), 2: F(1)}]
        jobs += [{1: F(1, k), 0: F(1, 4 * k)} for _ in range(2 * k)]
        jobs += [{2: F(1, k), 0: F(1, 4 * k)} for _ in range(2 * k)]
        value, a, meta = boundary_oracle(3, jobs, 0, F(1), F(1, 5))
        load = load_vector(3, jobs, a)
        assert max(load) <= F(6, 5)
        moved_big = sum(a[j] != 0 for j in [0, 1])
        moved_small = sum(a[j] == 0 for j in range(2, len(jobs)))
        stress.append({"k": k, "root_load": str(value), "loads": list(map(str, load)), "moved_big": moved_big, "moved_small": moved_small, "K": meta["K"]})

    # Extremely small positive internal times and zero objective time: no precision loss.
    denominator = 2**1000 + 937
    jobs = [{0: F(0), 1: F(1, denominator)}, {0: F(5, 7), 1: F(0)}, {1: F(1, denominator)}]
    out = boundary_oracle(2, jobs, 0, F(1, denominator), F(1, 5))
    assert out is not None and out[0] == 0
    assert load_vector(2, jobs, out[1])[1] == F(1, denominator)
    huge_m = 2**1000
    sparse_jobs = [{huge_m - 1: F(1), 0: F(0)}, {huge_m - 1: F(0)}]
    sparse_out = boundary_oracle(huge_m, sparse_jobs, huge_m - 1, F(0), F(1, 5))
    assert sparse_out is not None and sparse_out[0] == 0
    assert sparse_out[1] == (0, huge_m - 1)
    # Cycle is explicitly rejected as outside the oracle's contract.
    try:
        boundary_oracle(3, [{0: F(2), 1: F(1)}, {1: F(2), 2: F(1)}, {2: F(2), 0: F(1)}], 0, F(1), F(1, 5))
        raise AssertionError("cycle accepted")
    except ValueError as e:
        assert "forest" in str(e)
    return {"claim": "scratch one-boundary forest resource augmentation oracle", "cases": cases, "returned": positive, "correct_rejections": rejected, "stress": stress, "large_denominator_bits": denominator.bit_length(), "seed": 9162026, "arithmetic": "Fraction and integer only", "python": platform.python_version(), "limits": "finite audit, not a general proof; forest interface only; no UM-TARGET-v1 algorithm"}


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2))
