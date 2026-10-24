"""One precise fixed-policy cone test of pure self-consistent query existence.

Uses the frozen 13-player refined-tax automaton, its eight existing unit-client
types, every automaton IC, and one explicit challenger for each catalogue topic.
No policy search, random sampling, or instance scan is performed.
"""
from fractions import Fraction as F
from math import lcm, gcd
from pathlib import Path
import gzip, json

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
PACKET = ROOT / "research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz"


def primitive(row):
    div = 0
    for value in row:
        div = gcd(div, abs(value))
    return tuple(value // div for value in row) if div else tuple(row)


def main():
    data = json.load(gzip.open(PACKET, "rt"))
    ins, nodes = data["instance"], data["nodes"]
    m, k = ins["players"], len(ins["topics"])
    types = [frozenset(c["topics"]) for c in ins["customers"]]
    L = lcm(*range(1, m + 1))
    term, cache = {}, {}

    def row(a, t):
        key = a, t
        if key not in cache:
            cache[key] = tuple(L // sum(t[b] for b in S) if a in S else 0 for S in types)
        return cache[key]

    ic = set()
    comparisons = 0
    for idx in sorted(range(len(nodes)), key=lambda j: sum(nodes[j]["counts"]), reverse=True):
        q = nodes[idx]
        if q.get("terminal"):
            term[idx] = tuple(q["counts"])
            continue
        a = q["action"]
        t = term[q["children"][a]]
        term[idx] = t
        original = row(a, t)
        for b, child in enumerate(q["children"]):
            deviation = row(b, term[child])
            delta = primitive(tuple(x - y for x, y in zip(original, deviation)))
            ic.add(delta)
            comparisons += 1

    actual_nodes = []
    idx = data["root"]
    while not nodes[idx].get("terminal"):
        actual_nodes.append(idx)
        idx = nodes[idx]["children"][nodes[idx]["action"]]
    assert len(actual_nodes) == m

    query_coeff = []
    load_sums = []
    for a in range(k):
        totals = [0] * len(types)
        for idx in actual_nodes:
            t = term[nodes[idx]["children"][a]]
            for l, S in enumerate(types):
                totals[l] += sum(t[b] for b in S) - int(a in S)
        load_sums.append(totals)
        query_coeff.append([
            tuple(F(m, m + totals[l]) if b in S else F(0) for l, S in enumerate(types))
            for b in range(k)
        ])

    challengers = [3, 5, 5, 5, 5, 2]
    strict_rows = [tuple(x-y for x,y in zip(query_coeff[a][challengers[a]], query_coeff[a][a]))
                   for a in range(k)]
    ic = sorted(ic)
    A_ub = [[-float(v) for v in r] + [0.] for r in ic]
    A_ub += [[-float(v) for v in r] + [1.] for r in strict_rows]
    result = linprog([0.] * len(types) + [-1.], A_ub=np.asarray(A_ub),
                     b_ub=np.zeros(len(A_ub)), A_eq=[[1.] * len(types) + [0.]],
                     b_eq=[1.], bounds=[(0., None)]*len(types)+[(None,None)], method="highs")
    report = {"scope": "One fixed 13-player complete policy, eight fixed client types; all original IC; prescribed strict challengers for all six topics.",
              "packet": str(PACKET.relative_to(ROOT)), "players": m, "topics": ins["topics"],
              "automaton_nodes": len(nodes), "ic_comparisons": comparisons, "unique_primitive_ic_rows": len(ic),
              "types": [sorted(S) for S in types], "challengers": challengers,
              "load_sums": load_sums, "status": result.message, "success": bool(result.success)}
    if result.success:
        candidate = [F(float(v)).limit_denominator(10**8) for v in result.x[:-1]]
        gaps = [sum((v*w for v,w in zip(r,candidate)), F(0)) for r in strict_rows]
        minimum_ic = min(sum((F(v)*w for v,w in zip(r,candidate)), F(0)) for r in ic)
        report.update({"numeric_max_margin": float(result.x[-1]), "rational_candidate": list(map(str,candidate)),
                       "rational_sum": str(sum(candidate)), "exact_minimum_ic": str(minimum_ic),
                       "exact_challenger_gaps": list(map(str,gaps)),
                       "exact_positive_witness": minimum_ic >= 0 and min(gaps)>0 and min(candidate)>=0})
        # The LP dual can be independently exact-rationalized if this candidate is blocked.
        nz = [(i,float(v)) for i,v in enumerate(result.ineqlin.marginals) if abs(v)>1e-9]
        report["dual_nonzero"] = [{"row": i, "value": v,
            "kind": "IC" if i<len(ic) else "challenger", "coefficients": list(ic[i]) if i<len(ic) else list(map(str,strict_rows[i-len(ic)]))} for i,v in nz]
        report["equality_dual"] = list(map(float,result.eqlin.marginals))
    path = HERE / "self_consistent_13_probe.json"
    path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
