"""Attack one general construction: stationary source/full-slot column kernel.

This is a finite diagnostic for the stated kernel, not a half-coverage search.
The input is a fixed complete history strategy.  All nonempty customer types
are free nonnegative variables; every genuine SPE comparison is retained.
Only a positive candidate, reconstructed over Q and checked exactly, is saved.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def rank(matrix):
    a = [list(map(F,row)) for row in matrix]
    if not a:
        return 0
    i = 0
    for j in range(len(a[0])):
        pivot = next((t for t in range(i,len(a)) if a[t][j]),None)
        if pivot is None:
            continue
        a[i],a[pivot] = a[pivot],a[i]
        value = a[i][j]
        a[i] = [q/value for q in a[i]]
        for t in range(i+1,len(a)):
            value = a[t][j]
            if value:
                a[t] = [x-value*y for x,y in zip(a[t],a[i])]
        i += 1
        if i == len(a):
            break
    return i


def solve_unique(matrix,rhs):
    n = len(matrix[0])
    a = [list(map(F,row))+[F(b)] for row,b in zip(matrix,rhs)]
    i = 0
    pivots = []
    for j in range(n):
        pivot = next((t for t in range(i,len(a)) if a[t][j]),None)
        if pivot is None:
            continue
        a[i],a[pivot] = a[pivot],a[i]
        value = a[i][j]
        a[i] = [q/value for q in a[i]]
        for t in range(len(a)):
            if t == i:
                continue
            value = a[t][j]
            if value:
                a[t] = [x-value*y for x,y in zip(a[t],a[i])]
        pivots.append(j)
        i += 1
    assert len(pivots) == n
    assert all(any(row[:-1]) or not row[-1] for row in a)
    solution = [F(0)]*n
    for row,j in enumerate(pivots):
        solution[j] = a[row][-1]
    return solution


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.input.read_text())
    instance = data["instance"]
    k, m = len(instance["topics"]), instance["players"]
    actions = {tuple(d["history"]): d["action"] for d in data["certificate"]["actions"]}
    types = list(range(1, 1 << k))

    def terminal(prefix):
        z = tuple(prefix)
        while len(z) < m:
            z += (actions[z],)
        return z

    def coeff(z, player):
        return [F(int(bool(mask & (1 << z[player]))), sum(bool(mask & (1 << a)) for a in z))
                if mask & (1 << z[player]) else F(0) for mask in types]

    actual = terminal(())
    root = coeff(actual, 0)
    coverage = [F(int(any(mask & (1 << a) for a in actual))) for mask in types]
    rows = []
    row_names = []
    for length in range(m):
        for h in itertools.product(range(k), repeat=length):
            selected = coeff(terminal(h), length)
            for a in range(k):
                alternative = coeff(terminal(h + (a,)), length)
                rows.append([x-y for x, y in zip(selected, alternative)])
                row_names.append((h, a))

    forced = [terminal((a,)) for a in range(k)]
    transition = [[F(Counter(z)[a], m) for a in range(k)] for z in forced]
    # Identify the stationary vertices by closed communicating classes.
    reach = [[bool(transition[i][j]) for j in range(k)] for i in range(k)]
    for i in range(k):
        reach[i][i] = True
    for t in range(k):
        for i in range(k):
            for j in range(k):
                reach[i][j] = reach[i][j] or (reach[i][t] and reach[t][j])
    classes = []
    for i in range(k):
        cls = tuple(j for j in range(k) if reach[i][j] and reach[j][i])
        if cls in classes:
            continue
        if all(not transition[j][t] for j in cls for t in range(k) if t not in cls):
            classes.append(cls)
    p_vertices = []
    for cls in classes:
        system = [[transition[j][a]-F(j==a) for j in cls] for a in cls]
        system.append([F(1)]*len(cls))
        rhs = [F(0)]*len(cls)+[F(1)]
        value = solve_unique(system,rhs)
        p = [F(0)] * k
        for a, q in zip(cls, value):
            p[a] = q
        p_vertices.append(p)

    gamma_np = np.array([[float(q) for q in row] for row in rows])
    norm_np = np.array([[float(q) for q in coverage]])
    results = []
    for p in p_vertices:
        for query in range(k):
            price = [sum((p[a] / (1 + sum(bool(mask & (1 << t)) for t in forced[a]))
                          for a in range(k)), F(0))
                     if mask & (1 << query) else F(0) for mask in types]
            objective = [x-y for x,y in zip(price, root)]
            result = linprog(-np.array([float(q) for q in objective]),
                             A_ub=-gamma_np, b_ub=np.zeros(len(rows)),
                             A_eq=norm_np, b_eq=[1], bounds=(0, None), method="highs")
            entry = {"stationary": list(map(str,p)), "query": query,
                     "status": result.message,
                     "floating_gap": -float(result.fun) if result.success else None}
            if result.success and result.fun < -1e-7:
                support = [i for i,x in enumerate(result.x) if x > 1e-8]
                equations = [[coverage[i] for i in support]]
                rhs = [F(1)]
                current_rank = 1
                for row in rows:
                    if abs(sum(float(row[i])*result.x[i] for i in support)) > 1e-7:
                        continue
                    candidate = [row[i] for i in support]
                    newrank = rank(equations+[candidate])
                    if newrank > current_rank:
                        equations.append(candidate)
                        rhs.append(F(0))
                        current_rank = newrank
                        if current_rank == len(support):
                            break
                if current_rank != len(support):
                    raise RuntimeError("Could not reconstruct exact LP vertex")
                solution = solve_unique(equations,rhs)
                weights = [F(0)] * len(types)
                for i,q in zip(support, solution):
                    weights[i] = q
                slacks = [sum((x*y for x,y in zip(row,weights)), F(0)) for row in rows]
                gap = sum((x*y for x,y in zip(objective,weights)), F(0))
                assert min(weights) >= 0 and min(slacks) >= 0 and gap > 0
                from math import lcm
                denominator = lcm(*[q.denominator for q in weights])
                integer = [int(q*denominator) for q in weights]
                from math import gcd
                divisor = 0
                for q in integer:
                    divisor = gcd(divisor,q)
                integer = [q//divisor for q in integer]
                units = [F(q) for q in integer]
                root_value = sum((x*y for x,y in zip(root,units)),F(0))
                price_value = sum((x*y for x,y in zip(price,units)),F(0))
                entry.update({"exact_gap_normalized":str(gap),
                              "unit_customers":[{"mask":types[i],"multiplicity":q}
                                                for i,q in enumerate(integer) if q],
                              "total_customers":sum(integer),
                              "root_u":str(root_value),"query_price":str(price_value),
                              "spe_min_slack_normalized":str(min(slacks)),
                              "complete_strategy_nodes":len(actions),
                              "all_comparisons":len(rows),
                              "forced_paths":[list(z) for z in forced]})
            results.append(entry)
    report = {"kind":"STATIONARY-FULL-SLOT-KERNEL-DIAGNOSTIC",
              "source":str(args.input),"m":m,"k":k,"results":results}
    output = json.dumps(report,indent=2)+"\n"
    if args.output:
        args.output.write_text(output)
    print(output)


if __name__ == "__main__":
    main()
