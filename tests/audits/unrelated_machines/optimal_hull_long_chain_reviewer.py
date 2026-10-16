"""独立审查者的交错任务编号、全合法分配及槽匹配计数审计。"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform


def audit(k, d):
    scale, long = 2*k, d+2*k-1
    jobs, branches, machine = [], [], 1
    # Distinct numbering from the normative and potential_attack scripts:
    # each root job is immediately followed by the jobs of its own chain.
    for branch, length in [('b', long)]+[(f't{j}', d) for j in range(k)]:
        nodes = list(range(machine, machine+length+1))
        machine += length+1
        root = len(jobs)
        jobs.append((0, nodes[0], scale if branch == 'b' else 2, scale))
        ids = []
        for h in range(length):
            ids.append(len(jobs))
            jobs.append((nodes[h], nodes[h+1], scale-1, scale))
        branches.append((branch, root, ids))
    n, m = len(jobs), machine
    s0, s1, bad = [[0]*n for _ in range(3)]
    for branch, root, ids in branches:
        for j in [root]+ids:
            s0[j] = int(branch != 'b')
            s1[j] = int(branch == 'b')
            bad[j] = int(branch == 't0')

    def loads(bits):
        result = [0]*m
        for bit, (u, v, pu, pv) in zip(bits, jobs):
            result[v if bit else u] += pv if bit else pu
        return result

    rows = [{} for _ in range(m)]
    for j, (u, v, pu, pv) in enumerate(jobs):
        for schedule, weight in [(s0, F(1, k)), (s1, 1-F(1, k))]:
            i = v if schedule[j] else u
            rows[i][j] = rows[i].get(j, F(0))+weight
    edges, slots = {}, []
    for i, row in enumerate(rows):
        at = F(0)
        def processing(j):
            return jobs[j][3] if jobs[j][1] == i else jobs[j][2]
        for j in sorted(row, key=lambda j: (-processing(j), j)):
            end = at+row[j]
            for ell in range(at.numerator//at.denominator,
                             -(-end.numerator//end.denominator)):
                if min(end, ell+1) > max(at, ell):
                    edges.setdefault((i, j), set()).add(ell)
            at = end
        slots.append(-(-at.numerator//at.denominator))

    def covering_matchings(bits):
        by_machine = [[] for _ in range(m)]
        for j, bit in enumerate(bits):
            by_machine[jobs[j][bit]].append(j)
        ways = 1
        for i, assigned in enumerate(by_machine):
            if len(assigned) > slots[i]:
                return 0
            dp = {0: 1}
            for j in assigned:
                nxt = {}
                for mask, count in dp.items():
                    for ell in edges.get((i, j), ()):
                        if not (mask >> ell) & 1:
                            target = mask | (1 << ell)
                            nxt[target] = nxt.get(target, 0)+count
                dp = nxt
            ways *= sum(dp.values())
            if ways == 0:
                return 0
        return ways

    old = tuple(sorted(loads(bad), reverse=True))
    optimum, min_jobs, min_machines = None, None, None
    lex_count, cost, owner_count, matching_count = 0, None, 0, 0
    minimizer = None
    for bits in product((0, 1), repeat=n):
        current = loads(bits)
        makespan = max(current)
        optimum = makespan if optimum is None else min(optimum, makespan)
        if tuple(sorted(current, reverse=True)) < old:
            lex_count += 1
            changed = [j for j, (b, c) in enumerate(zip(bits, bad)) if b != c]
            touched = {i for j in changed for i in jobs[j][:2]}
            min_jobs = len(changed) if min_jobs is None else min(min_jobs, len(changed))
            min_machines = len(touched) if min_machines is None else min(min_machines, len(touched))
        ways = covering_matchings(bits)
        if not ways:
            continue
        total = sum(current)
        if cost is None or total < cost:
            cost, owner_count, matching_count, minimizer = total, 1, ways, bits
        elif total == cost:
            owner_count += 1
            matching_count += ways
    assert optimum == scale
    assert min_jobs == d+1 and min_machines == d+2
    assert owner_count == 1 and minimizer == tuple(bad)
    return dict(k=k, d=d, jobs=n, machines=m,
                enumerated_assignments=2**n, optimum=str(F(optimum, scale)),
                initial_makespan=str(F(old[0], scale)),
                strict_lex_improving_assignments=lex_count,
                minimum_changed_jobs=min_jobs,
                minimum_participating_machines=min_machines,
                minimum_slot_cost=str(F(cost, scale)),
                minimum_slot_owner_assignments=owner_count,
                minimum_cover_matchings=matching_count)


if __name__ == '__main__':
    runs = [audit(*pair) for pair in [(3, 1), (3, 2), (4, 1)]]
    print(json.dumps(dict(status='PASS', python=platform.python_version(),
                         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         arithmetic='integer loads scaled by 2k; exact Fraction slot intervals',
                         limitations='finite implementation evidence only; no universal proof',
                         runs=runs), ensure_ascii=False, indent=2))
