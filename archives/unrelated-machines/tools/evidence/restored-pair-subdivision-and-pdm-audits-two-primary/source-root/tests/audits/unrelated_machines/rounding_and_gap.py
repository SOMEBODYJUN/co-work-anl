#!/usr/bin/env python3
"""Exact finite audits, not a polynomial LP solver or a new approximation result.

Input p is machine-major; None forbids an edge. All other numbers must be
integers or rational strings (floats are rejected). The rounding routine takes
an already supplied feasible rational assignment. CLI writes only to stdout.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import sys


def rational(v):
    if isinstance(v, (float, bool)):
        raise ValueError("Use exact rational input, not float/bool")
    return F(v)


def matrix(p):
    if not p or any(len(row) != len(p[0]) for row in p):
        raise ValueError("Nonempty rectangular machine matrix required")
    p = [[None if v is None else rational(v) for v in row] for row in p]
    if any(v is not None and v < 0 for row in p for v in row):
        raise ValueError("Negative processing time")
    if any(all(row[j] is None for row in p) for j in range(len(p[0]))):
        raise ValueError("Every job needs a finite machine")
    return p


def loads(p, assignment):
    p = matrix(p)
    if len(assignment) != len(p[0]):
        raise ValueError("Assignment length")
    result = [F(0) for _ in p]
    for j, i in enumerate(assignment):
        if type(i) is not int or not 0 <= i < len(p) or p[i][j] is None:
            raise ValueError("Illegal assignment")
        result[i] += p[i][j]
    return result


def exhaustive_optimum(p):
    """Exponential independent oracle; caller must restrict instance size."""
    p = matrix(p)
    choices = [[i for i, row in enumerate(p) if row[j] is not None]
               for j in range(len(p[0]))]
    best, witness, count = None, None, 0
    for assignment in product(*choices):
        count += 1
        value = max(loads(p, assignment))
        if best is None or value < best:
            best, witness = value, assignment
    return best, witness, count


def round_slots(p, x, target):
    """ST ordered unit slots + integral matching, exact rational arithmetic."""
    p = matrix(p)
    t = rational(target)
    if t < 0 or len(x) != len(p) or any(len(row) != len(p[0]) for row in x):
        raise ValueError("Invalid target or assignment dimensions")
    x = [[rational(v) for v in row] for row in x]
    n = len(p[0])
    if any(v < 0 for row in x for v in row):
        raise ValueError("Negative fractional mass")
    for j in range(n):
        if sum(row[j] for row in x) != 1:
            raise ValueError("Job mass is not one")
    for i, row in enumerate(p):
        if any(x[i][j] and (v is None or v > t) for j, v in enumerate(row)):
            raise ValueError("Positive mass on a forbidden/pruned edge")
        if sum((v or 0) * x[i][j] for j, v in enumerate(row)) > t:
            raise ValueError("Fractional load exceeds target")
    slots, neighbors = [], [[] for _ in range(n)]
    for i, row in enumerate(p):
        jobs = sorted((j for j in range(n) if x[i][j]), key=lambda j: (-row[j], j))
        cursor = F(0)
        local = {}
        for j in jobs:
            end = cursor + x[i][j]
            while cursor < end:
                k = cursor.numerator // cursor.denominator
                if k not in local:
                    local[k] = len(slots)
                    slots.append(i)
                neighbors[j].append(local[k])
                cursor = min(end, F(k + 1))
    matched = {}
    for j in range(n):
        # Breadth-first augmentation avoids a recursion-depth assumption.
        pending, seen_jobs, parent, free = [j], {j}, {}, None
        for current in pending:
            for slot in neighbors[current]:
                if slot in parent:
                    continue
                parent[slot] = current
                if slot not in matched:
                    free = slot
                    break
                old = matched[slot]
                if old not in seen_jobs:
                    seen_jobs.add(old)
                    pending.append(old)
            if free is not None:
                break
        if free is None:
            raise AssertionError("Hall condition failed for a feasible fractional matching")
        # Recover the alternating path using the previous job->slot matching.
        inverse = {job: slot for slot, job in matched.items()}
        slot = free
        while True:
            job = parent[slot]
            old_slot = inverse.get(job)
            matched[slot] = job
            if old_slot is None:
                break
            slot = old_slot
    assignment = [None] * n
    for slot, j in matched.items():
        assignment[j] = slots[slot]
    actual = loads(p, assignment)
    bounds = [sum((v or 0) * x[i][j] for j, v in enumerate(row))
              + max((row[j] for j in range(n) if x[i][j]), default=F(0))
              for i, row in enumerate(p)]
    assert all(a <= b <= 2*t for a, b in zip(actual, bounds))
    return assignment, actual


def height(k):
    if type(k) is not int or k < 2:
        raise ValueError("k must be an integer >= 2")
    h, alpha = 1, F(1, k-1)
    while alpha < F(1, 2):
        h, alpha = h+1, alpha*F(k, k-1)
    return h, alpha


def gap_instance(k):
    """VW tree family with explicit, checked configurations; cap materialization."""
    if type(k) is not int or not 2 <= k <= 4:
        raise ValueError("Use compressed_gap for larger k; expanded tree grows rapidly")
    h, alpha = height(k)
    edges, configs = [], []

    def node():
        configs.append([])
        return len(configs)-1

    def edge(a, b, pa=F(1), pb=F(1)):
        edges.append({a: pa, b: pb})
        return len(edges)-1

    def subtree(root, depth, incoming):
        if depth == 1:
            terminal = node()
            children = [edge(root, terminal, F(1,k), F(1)) for _ in range(k)]
            configs[terminal] = [(F(1,k), (j,)) for j in children]
            a = F(1,k-1)
        else:
            children = []
            for _ in range(k):
                child = node()
                j = edge(root, child, F(1,k), F(1))
                children.append(j)
                child_a = subtree(child, depth-1, j)
            a = child_a * F(k,k-1)
        configs[root] = [(1-a, tuple(children))] + [(a/k, (incoming,j)) for j in children]
        return a

    roots = [node(), node()]
    big = edge(*roots)
    for root in roots:
        a = subtree(root,h,big)
        # Delete only the incoming job from a proportion of its configurations;
        # this lowers its root marginal to 1/2, preserving every child marginal.
        thinned = []
        for weight, jobs in configs[root]:
            if big in jobs:
                thinned += [(weight/(2*a), jobs),
                            (weight*(1-1/(2*a)), tuple(j for j in jobs if j != big))]
            else:
                thinned.append((weight,jobs))
        configs[root] = [(w,s) for w,s in thinned if w]
    p = [[edge.get(i) for edge in edges] for i in range(len(configs))]
    t = 1+F(1,k)
    totals = [F(0)]*len(edges)
    for i, choices in enumerate(configs):
        assert sum(w for w,s in choices) == 1
        for w,s in choices:
            assert w >= 0 and len(set(s)) == len(s)
            assert all(p[i][j] is not None for j in s)
            assert sum(p[i][j] for j in s) <= t
            for j in s:
                totals[j] += w
    assert all(total == 1 for total in totals)
    assert all(len(edge) == 2 for edge in edges)
    return p, configs, t


def compressed_gap(k):
    """Tree DP: exact optimum in 1/k units, independent of LP certificate."""
    h, alpha = height(k)
    dp = {b:min(max(k*b+r,k*(k-r)) for r in range(k+1)) for b in (0,1)}
    for _ in range(1,h):
        old = dp
        dp = {b:min(max([k*b+r]+([old[0]] if r else [])
                        +([old[1]] if r<k else [])) for r in range(k+1)) for b in (0,1)}
    optimum = F(max(dp.values()),k)
    return {"k":k,"height":h,"root_alpha":str(alpha),"optimum":str(optimum),
            "certified_lp_upper":str(1+F(1,k)),
            "gap_lower_bound":str(optimum/(1+F(1,k))),
            "dp_units":dp}


def audit():
    rng = random.Random(20261016)
    cases = []
    # Enumerate all two-machine, three-job matrices over 0,1,2,forbidden.
    # Construct feasible half-assignments and compare with an independent oracle.
    for flat in product((None,0,1,2),repeat=6):
        p = [list(flat[:3]),list(flat[3:])]
        if any(p[0][j] is None and p[1][j] is None for j in range(3)):
            continue
        x = [[F(0)]*3 for _ in range(2)]
        for j in range(3):
            available = [i for i in range(2) if p[i][j] is not None]
            for i in available:
                x[i][j] = F(1,len(available))
        t = max([F(v) for row in p for v in row if v is not None]
                + [sum((p[i][j] or 0)*x[i][j] for j in range(3)) for i in range(2)])
        assignment, actual = round_slots(p,x,t)
        opt,witness,count = exhaustive_optimum(p)
        assert opt <= max(actual) <= 2*t
        assert max(loads(p,witness)) == opt
        cases.append(count)
    # Rational nonuniform marginals, longer slot chains, and empty jobs.
    for _ in range(150):
        m,n = rng.randrange(1,6),rng.randrange(0,9)
        p = [[F(rng.randrange(0,15),rng.randrange(1,8)) for _ in range(n)] for _ in range(m)]
        x = [[F(0)]*n for _ in range(m)]
        for j in range(n):
            weights = [rng.randrange(0,9) for _ in range(m)]
            if not sum(weights):weights[0]=1
            for i in range(m):x[i][j]=F(weights[i],sum(weights))
        t = max([F(0)]+[v for row in p for v in row]
                +[sum(p[i][j]*x[i][j] for j in range(n)) for i in range(m)])
        round_slots(p,x,t)
    invalid = [([[1]],[[0]],1), ([[2]],[[1]],1), ([[None],[1]],[[1],[0]],1),
               ([[-1]],[[1]],1), ([[1]],[[1]],-1), ([[1]],[[1.0]],1)]
    for args in invalid:
        try:round_slots(*args)
        except ValueError:pass
        else:raise AssertionError("Invalid input accepted")
    toy = [[3,1,1,1,1,1,1] for _ in range(3)]
    opt,witness,count = exhaustive_optimum(toy)
    bad = (0,0,0,1,1,2,2)
    assert opt == 3 and max(loads(toy,bad)) == 5
    gaps = []
    for k in (2,3,4):
        p,configs,t = gap_instance(k)
        result = compressed_gap(k)
        result.update(machines=len(p),jobs=len(p[0]),configuration_certificate_checked=True)
        if k <= 3:
            exact,witness,number = exhaustive_optimum(p)
            assert exact == F(result["optimum"])
            result.update(enumerated_assignments=number,independent_optimum=str(exact))
        gaps.append(result)
    recurrences = [compressed_gap(k) for k in (5,8,16,32)]
    for row in gaps+recurrences:
        k=row['k']
        assert F(row['optimum']) == F(2*k-1,k)
        assert F(row['gap_lower_bound'])*(1+F(1,k)) == F(row['optimum'])
    return {"schema_version":1,"python_version":platform.python_version(),"seed":20261016,
            "arithmetic":"fractions.Fraction, exact; no floating point solver",
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "matrix_cases":len(cases),"oracle_assignments":sum(cases),
            "rational_cases":150,"invalid_cases":len(invalid),
            "toy":{"optimum":str(opt),"bad_assignment_makespan":"5","ratio":"5/3",
                   "enumerated_assignments":count,"attribution":"Only the OPT and bad schedule checked; no claim this is a reproduced textbook matching"},
            "expanded_gap_cases":gaps,"compressed_gap_cases":recurrences,
            "limitations":["Finite checks are not a universal proof or novelty certificate",
                            "No generic LP solver implemented; rounding receives a feasible x",
                            "Compressed DP applies only to the explicit symmetric VW tree family",
                            "Large k full graphs not materialized; no claim of a generic efficient exact solver"]}


if __name__ == '__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
