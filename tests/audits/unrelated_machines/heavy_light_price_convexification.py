#!/usr/bin/env python3
"""有限精确审计：重轻任务价格凸化，不是通用多项式 LP 求解器。

小输入的 primal 顶点枚举与 dual 分段线性枚举互不调用；所有运算
使用 Fraction。给定见证的 ST 调用既有规范实现，负载/基数独立回算。
CLI 仅输出 stdout，重跑不得覆盖冻结证据。
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).with_name("rounding_and_gap.py")
spec = importlib.util.spec_from_file_location("classical_baseline", BASE)
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)


def solve_square(rows, rhs):
    """独立有理 Gaussian elimination；奇异系统返回 None。"""
    n = len(rhs)
    a = [list(map(F, row)) + [F(b)] for row, b in zip(rows, rhs)]
    for c in range(n):
        pivot = next((r for r in range(c, n) if a[r][c]), None)
        if pivot is None:
            return None
        a[c], a[pivot] = a[pivot], a[c]
        z = a[c][c]
        a[c] = [v/z for v in a[c]]
        for r in range(n):
            if r != c and a[r][c]:
                z = a[r][c]
                a[r] = [v-z*w for v, w in zip(a[r], a[c])]
    return [row[-1] for row in a]


def pruned(p, t):
    return [[None if v is None or F(v) > t else F(v) for v in row]
            for row in p]


def primal_vertices(p, t, beta):
    """仅供二机小例：枚举 Q 中 min max load 的精确顶点。"""
    n = len(p[0])
    if n == 0:
        return F(0), [[] for _ in p]
    edges = [(i, j) for i, row in enumerate(p)
             for j, v in enumerate(row) if v is not None]
    if any(not any(j == jj for _, jj in edges) for j in range(n)):
        return None, None
    d = len(edges) + 1  # last coordinate is max-load objective z
    eq = [[F(jj == j) for _, jj in edges] + [F(0)] for j in range(n)]
    bounds = []
    for e in range(d):
        row = [F(0)]*d
        row[e] = -1
        bounds.append((row, F(0)))
    for i in range(len(p)):
        row = [F(ii == i and p[ii][j] > beta*t) for ii, j in edges]+[F(0)]
        bounds.append((row, F(1)))
        row = [p[ii][j] if ii == i else F(0) for ii, j in edges]+[F(-1)]
        bounds.append((row, F(0)))
    best, witness = None, None
    for active in combinations(bounds, d-n):
        ans = solve_square(eq + [a for a, _ in active],
                           [F(1)]*n + [b for _, b in active])
        if ans is None or any(sum(a*v for a, v in zip(row, ans)) > b
                              for row, b in bounds):
            continue
        if best is None or ans[-1] < best:
            best = ans[-1]
            witness = [[F(0)]*n for _ in p]
            for (i, j), v in zip(edges, ans):
                witness[i][j] = v
    return best, witness


def pure_states(p, t, beta):
    """独立枚举底层完整整数指派，仅约束每机 heavy 数。"""
    choices = [[i for i in range(len(p)) if p[i][j] is not None]
               for j in range(len(p[0]))]
    states = []
    for sigma in product(*choices):
        count = [0]*len(p)
        load = [F(0)]*len(p)
        heavy = []
        for j, i in enumerate(sigma):
            load[i] += p[i][j]
            if p[i][j] > beta*t:
                count[i] += 1
                heavy.append((i, j))
        if max(count, default=0) <= 1:
            states.append((tuple(load), tuple(heavy), sigma))
    return states


def dual_two_machine(states):
    """λ=(a,1-a) 上所有折点，与 primal 顶点枚举独立。"""
    if not states:
        return None, None
    candidates = {F(0), F(1)}
    for (u, _, _), (v, _, _) in combinations(states, 2):
        den = (u[0]-u[1])-(v[0]-v[1])
        if den:
            a = (v[1]-u[1])/den
            if 0 <= a <= 1:
                candidates.add(a)
    costs = [(min(a*l[0]+(1-a)*l[1] for l, _, _ in states), a)
             for a in candidates]
    return max(costs)


def independent_loads(p, sigma):
    out = [F(0)]*len(p)
    for j, i in enumerate(sigma):
        assert p[i][j] is not None
        out[i] += p[i][j]
    return out


def audit():
    assert solve_square([[1, 1], [1, -1]], [1, 0]) == [F(1, 2)]*2
    assert solve_square([[1, 1], [2, 2]], [1, 2]) is None
    beta_cases = (F(1, 2), F(3, 5), F(4, 5), F(99, 100),
                  1-F(1, 2**160))
    reports = []
    fixtures = []
    for beta in beta_cases:
        eta = (1-beta)/4
        a, b, s = 1-eta, 1-3*eta, 2*eta
        p = [[a, b, s, None], [a, b, None, s]]
        fixtures.append(("two_machine_"+str(beta), p, F(1), beta))
        assert a > beta and b > beta and s <= beta
        states = pure_states(p, F(1), beta)
        assert {l for l, _, _ in states} == {(1+eta, 1-eta), (1-eta, 1+eta)}
        opt, _, _ = baseline.exhaustive_optimum(p)
        assert opt == 1+eta
        for u, v in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 7),
                     (F(1, 2**180), F(1, 3**100))):
            g = min(u*l[0]+v*l[1]-(u+v) for l, _, _ in states)
            assert g == -eta*abs(u-v)
        # A unique response to a non-dual-optimal price is not a capacity proof.
        cheapest = min(l[0] for l, _, _ in states)
        nondual_heavy = {h for l, h, _ in states if l[0] == cheapest}
        assert cheapest == 1-eta < 1 and len(nondual_heavy) == 1
        assert all(max(l) == 1+eta for l, h, _ in states if h in nondual_heavy)
    fixtures += [
        ("empty", [[], []], F(1), F(1, 2)),
        ("zero", [[F(0), F(0)], [F(0), F(0)]], F(0), F(1, 2)),
        ("mixed_role", [[F(1), F(1, 4)], [F(1, 4), F(1)]], F(1), F(3, 4)),
        ("forced_face", [[F(1), None, F(0)], [None, F(1, 3), F(0)]], F(1), F(1, 2)),
        ("fractional_light_face", [[F(4, 5), F(2, 5), F(2, 5), F(2, 5)],
                                   [None, F(2, 5), F(2, 5), F(2, 5)]], F(1), F(7, 10)),
        ("capacity_conflict", [[F(1, 2)]*3, [None]*3], F(1), F(1, 2)),
        ("heavy_conflict", [[F(1), F(1)], [None, None]], F(1), F(1, 2)),
        ("pruned_job_lost", [[F(2)], [F(2)]], F(1), F(1, 2)),
    ]
    face_exits = 0
    for name, original, t, beta in fixtures:
        p = pruned(original, t)
        primal, x = primal_vertices(p, t, beta)
        states = pure_states(p, t, beta)
        dual, price = dual_two_machine(states)
        assert primal == dual, (name, primal, dual)
        report = {"name": name, "primal": str(primal), "dual": str(dual)}
        if primal is not None:
            costs = [price*l[0]+(1-price)*l[1] for l, _, _ in states]
            opt_heavy = {h for (_, h, _), cost in zip(states, costs) if cost == dual}
            if len(opt_heavy) == 1:
                common_h = set(next(iter(opt_heavy)))
                assert all(x[i][j] == F((i, j) in common_h)
                           for i, row in enumerate(p)
                           for j, v in enumerate(row)
                           if v is not None and v > beta*t)
                face_exits += 1
                # Force the opposite value on each big edge: finite independent
                # oracle for the stated optimal-face test, not a flow solver.
                for i, row in enumerate(p):
                    for j, value in enumerate(row):
                        if value is None or value <= beta*t:
                            continue
                        flipped = [price*l[0]+(1-price)*l[1] for l, h, _ in states
                                   if ((i, j) in h) != ((i, j) in common_h)]
                        assert not flipped or min(flipped) > dual
                if primal <= t:
                    covered = {j for _, j in common_h}
                    rest = [j for j in range(len(p[0])) if j not in covered]
                    light_p = [[p[i][j] if p[i][j] is not None and p[i][j] <= beta*t
                                else None for j in rest] for i in range(len(p))]
                    light_x = [[x[i][j] for j in rest] for i in range(len(p))]
                    light_sigma, _ = baseline.round_slots(light_p, light_x, t)
                    sigma = [None]*len(p[0])
                    for i, j in common_h:
                        sigma[j] = i
                    for j, i in zip(rest, light_sigma):
                        sigma[j] = i
                    actual = independent_loads(p, sigma)
                    assert max(actual) <= primal+beta*t
                    report.update(face_sigma=sigma,
                                  face_actual_loads=list(map(str, actual)),
                                  face_bound=str(primal+beta*t))
            if primal <= t:
                sigma, _ = baseline.round_slots(p, x, t)
                loads = independent_loads(p, sigma)
                assert max(loads) <= 2*t
                assert all(sum(p[i][j] > beta*t for j, dest in enumerate(sigma)
                               if dest == i) <= 1 for i in range(len(p)))
                report.update(sigma=list(sigma), actual_loads=list(map(str, loads)))
        reports.append(report)
    # Actual small two-tree P/certificates and independent full assignments.
    trees = []
    for k in (2, 3):
        p, configs, t = baseline.gap_instance(k)
        beta = F(1, 2)
        x = [[F(0)]*len(p[0]) for _ in p]
        for i, row in enumerate(configs):
            for weight, jobs in row:
                for j in jobs:
                    x[i][j] += weight
        assert all(sum(row[j] for row in x) == 1 for j in range(len(p[0])))
        assert all(sum(p[i][j]*x[i][j] for j in range(len(p[0]))
                       if p[i][j] is not None) <= t for i in range(len(p)))
        assert all(sum(x[i][j] for j in range(len(p[0]))
                       if p[i][j] is not None and p[i][j] > beta*t) <= 1
                   for i in range(len(p)))
        states = pure_states(p, t, beta)
        common = min(max(l) for l, _, _ in states)
        all_choices = [[i for i in range(len(p)) if p[i][j] is not None]
                       for j in range(len(p[0]))]
        actual = min(max(independent_loads(p, sigma)) for sigma in product(*all_choices))
        assert common == actual == 2-F(1, k)
        assert common/t == 2-F(3, k+1)
        trees.append({"k": k, "T": str(t), "common": str(common),
                      "original_optimum": str(actual), "admissible_states": len(states)})
    # Larger k: exact algebra only, no unreported tree materialization.
    for k in (4, 8, 16, 32):
        for beta in (F(1, 2), F(3, 4), F(9, 10)):
            if k > beta/(1-beta):
                t = 1+F(1, k)
                assert F(1, k) <= beta*t < 1
                assert (2-F(1, k))/t == 2-F(3, k+1)
    unpruned = []
    for m in (1, 2, 3, 7):
        p = [[F(m)] for _ in range(m)]
        states = pure_states(p, F(1), F(1, 2))
        assert min(max(l) for l, _, _ in states) == m
        assert all(p[i][0]*F(1, m) == 1 for i in range(m))
        assert all((not any(row)) for row in pruned(p, F(1))) if m > 1 else True
        unpruned.append({"m": m, "fractional_load": "1", "joint_load": str(m)})
    return {"status": "passed", "arithmetic": "Fraction; no floating point or random seed",
            "python": platform.python_version(),
            "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "baseline_sha256": hashlib.sha256(BASE.read_bytes()).hexdigest(),
            "primal_dual_fixtures": reports, "dual_common_heavy_faces": face_exits,
            "expanded_tree_checks": trees, "unpruned_fixed_m": unpruned,
            "limits": "Only listed finite fixtures; vertex/state enumeration is exponential. Larger-k checks are algebra only. General proof is in the manuscript; no general LP solver is implemented."}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
