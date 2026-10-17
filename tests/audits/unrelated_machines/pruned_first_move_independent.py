#!/usr/bin/env python3
"""独立审计：首步 U=max(2T,C+T/2) 与限批首步/路径锐界。

不导入任何仓库实现。Fraction 为全部数学运算；有限枚举不是一般证明。
"""
from __future__ import annotations

from fractions import Fraction as F
from heapq import heappush, heappop
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform


def loads(P, assignment):
    m = len(P)
    if m < 1:
        raise ValueError("machine set must be nonempty")
    n = len(P[0])
    if any(len(row) != n for row in P) or len(assignment) != n:
        raise ValueError("dimension mismatch")
    ans = [F(0) for _ in range(m)]
    for j, i in enumerate(assignment):
        if not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < m:
            raise ValueError("invalid machine label")
        p = P[i][j]
        if p is None or p < 0:
            raise ValueError("assignment uses forbidden or negative edge")
        ans[i] += p
    return ans


def first_move(P, sigma, tau, C, T):
    """验证合同后直接搜索 τ 指定的单件搬运；不调用锐族公式。"""
    if T <= 0 or not T <= C <= 2*T:
        raise ValueError("T>0 and T<=C<=2T required")
    sload, tload = loads(P, sigma), loads(P, tau)
    if max(sload) > C or max(tload) > T:
        raise ValueError("schedule bounds violated")
    if any(P[i][j] > T for j, i in enumerate(sigma)):
        raise ValueError("sigma not on T-pruned edges")
    changed = [j for j in range(len(sigma)) if sigma[j] != tau[j]]
    if not changed:
        raise ValueError("tau must differ from sigma")
    U = max(2*T, C+T/2)
    for j in changed:
        nxt = list(sigma)
        nxt[j] = tau[j]
        if max(loads(P, nxt)) <= U:
            return j, nxt
    raise AssertionError("claimed first move does not exist")


def sharp_family(k, C, T, branch):
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("positive integer k required")
    if T <= 0 or not T <= C <= 2*T:
        raise ValueError("invalid scales")
    m = k+1
    jobs = []
    movers = []
    if branch == "low":
        if C > 3*T/2:
            raise ValueError("low branch requires C<=3T/2")
        for i in range(m):
            jobs.append({i: C-T})
        for i in range(m):
            movers.append(len(jobs))
            jobs.append({i: T, (i+1) % m: 2*T-C})
        order = list(range(m))
    elif branch == "high":
        if C < 3*T/2:
            raise ValueError("high branch requires C>=3T/2")
        for i in range(m):
            for _ in range(2):
                movers.append(len(jobs))
                jobs.append({i: C/2, (i+1) % m: T/2})
        order = list(range(0, 2*m, 2))+list(range(1, 2*m, 2))
    else:
        raise ValueError("unknown branch")
    P = [[jobs[j].get(i) for j in range(len(jobs))] for i in range(m)]
    sigma = [next(iter(job)) for job in jobs]
    tau = list(sigma)
    for j in movers:
        tau[j] = next(i for i in jobs[j] if i != sigma[j])
    return P, sigma, tau, movers, order


def all_state_costs(P, sigma, tau, movers):
    # Explicitly form every legal assignment; padding has unique eligibility.
    ans = []
    for mask in range(1 << len(movers)):
        assignment = list(sigma)
        for bit, j in enumerate(movers):
            if mask >> bit & 1:
                assignment[j] = tau[j]
        ans.append(max(loads(P, assignment)))
    return ans


def xor_batches(n, k):
    ans = []
    for size in range(1, min(k, n)+1):
        for ids in combinations(range(n), size):
            mask = 0
            for j in ids:
                mask |= 1 << j
            ans.append(mask)
    return ans


def minimax_path(costs, n, batch_cap):
    """完整状态图的独立Dijkstra；XOR允许回搬，不限单调路径。"""
    moves = xor_batches(n, batch_cap)
    goal = (1 << n)-1
    best = [None]*len(costs)
    prev = [None]*len(costs)
    best[0] = costs[0]
    queue = [(costs[0], 0)]
    popped = 0
    while queue:
        height, mask = heappop(queue)
        if height != best[mask]:
            continue
        popped += 1
        if mask == goal:
            path = [goal]
            while path[-1] != 0:
                path.append(prev[path[-1]])
            path.reverse()
            assert all(1 <= (a ^ b).bit_count() <= batch_cap
                       for a, b in zip(path, path[1:]))
            assert max(costs[x] for x in path) == height
            return height, path, popped
        for delta in moves:
            nxt = mask ^ delta
            candidate = max(height, costs[nxt])
            if best[nxt] is None or candidate < best[nxt]:
                best[nxt], prev[nxt] = candidate, mask
                heappush(queue, (candidate, nxt))
    raise AssertionError("full assignment graph disconnected")


def check_family(k, ratio, T, branch):
    C = ratio*T
    P, sigma, tau, movers, explicit_order = sharp_family(k, C, T, branch)
    U = max(2*T, C+T/2)
    assert max(loads(P, sigma)) == C
    assert max(loads(P, tau)) == T
    assert all(p is None or 0 <= p <= T for row in P for p in row)
    assert all(sum(P[i][j] is not None for i in range(len(P))) <= 2
               for j in range(len(sigma)))
    first_move(P, sigma, tau, C, T)
    costs = all_state_costs(P, sigma, tau, movers)
    assert min(costs) == T  # independent exhaustive true OPT
    n = len(movers)
    first_batches = [costs[x] for x in range(1, 1 << n) if x.bit_count() <= k]
    assert first_batches and min(first_batches) == U
    mask = 0
    explicit_states = [mask]
    for bit in explicit_order:
        assert not (mask >> bit & 1)
        mask |= 1 << bit
        explicit_states.append(mask)
    assert mask == (1 << n)-1
    assert max(costs[x] for x in explicit_states) == U
    one, single_path, visited_one = minimax_path(costs, n, 1)
    batched, batch_path, visited_batch = minimax_path(costs, n, k)
    assert one == batched == U
    return {
        "k": k, "C_over_T": str(ratio), "T": str(T), "branch": branch,
        "machines": len(P), "jobs": len(sigma), "movable_jobs": n,
        "all_assignments": len(costs), "OPT": str(min(costs)),
        "min_nonempty_first_batch": str(min(first_batches)),
        "single_path_peak": str(one), "batch_path_peak": str(batched),
        "explicit_once_only_path": explicit_states,
        "single_oracle_path": single_path, "batch_oracle_path": batch_path,
        "single_popped": visited_one, "batch_popped": visited_batch,
    }


def exhaustive_first_move():
    values = (F(0), F(1, 2), F(1), None)
    eligible_columns = [p for p in product(values, repeat=2) if any(x is not None for x in p)]
    checked_pairs = matrices = 0
    zero_cases = empty_cases = 0
    for n in range(4):
        for cols in product(eligible_columns, repeat=n):
            P = [[cols[j][i] for j in range(n)] for i in range(2)]
            matrices += 1
            schedules = []
            for owner in product(range(2), repeat=n):
                if any(P[owner[j]][j] is None for j in range(n)):
                    continue
                L = loads(P, owner)
                schedules.append((owner, max(L)))
            if not n:
                assert schedules == [((), F(0))]
                empty_cases += 1
            for sigma, svalue in schedules:
                if svalue > 2:
                    continue
                C = max(F(1), svalue)
                for tau, tvalue in schedules:
                    if tau == sigma or tvalue > 1:
                        continue
                    first_move(P, sigma, tau, C, F(1))
                    checked_pairs += 1
                    zero_cases += tvalue == 0
    # Single machine / unique owner cannot satisfy tau != sigma; contract rejects it.
    invalid_rejected = 0
    for P, sigma, tau, C, T in [
        ([[F(0)]], [0], [0], F(1), F(1)),
        ([[F(0)], [F(0)]], [0], [1], F(0), F(0)),
        ([[F(2)], [F(1)]], [0], [1], F(2), F(1)),
    ]:
        try:
            first_move(P, sigma, tau, C, T)
        except ValueError:
            invalid_rejected += 1
        else:
            raise AssertionError("invalid contract input accepted")
    return {"matrices": matrices, "ordered_schedule_pairs": checked_pairs,
            "zero_target_pairs": zero_cases, "empty_inputs": empty_cases,
            "invalid_contracts_rejected": invalid_rejected}


def main():
    family_records = []
    ratios = [("low", F(1)), ("low", F(6, 5)), ("low", F(3, 2)),
              ("high", F(3, 2)), ("high", F(7, 4)), ("high", F(2))]
    for k in range(1, 5):
        for branch, ratio in ratios:
            family_records.append(check_family(k, ratio, F(1), branch))
    huge = (1 << 127)-1
    for branch, ratio in [("low", F(3, 2)-F(1, huge)),
                          ("high", F(3, 2)+F(1, huge))]:
        family_records.append(check_family(2, ratio, F(13, huge), branch))
    result = {
        "status": "all_checks_passed",
        "arithmetic": "exact integers and fractions.Fraction; no float",
        "python": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "first_move_exhaustive": exhaustive_first_move(),
        "sharp_families": family_records,
        "scope": "Finite audit only. No general full-path U theorem and no algorithm to find tau.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
