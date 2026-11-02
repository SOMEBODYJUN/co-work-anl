"""Universal client-type relaxation of genuine terminal/copy comparisons.

Numerical exploration only. All output is a relaxation result, never an SPE.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def build(m):
    names = []
    names += [f"copy:{i}:{j}" for i in range(m) for j in range(m)]
    names += [f"copy-opt:{i}" for i in range(m)]
    names += ["menu-G", "pair-opt-all", "pair-opt-diag", "pair-opt-offdiag"]
    names += [f"pair-opt-actual:{j}" for j in range(m)]
    names += [f"pair-actual:{j}:{k}" for j in range(m) for k in range(j,m)]
    columns, states, welfare, opt = [], [], [], []
    for bits in itertools.product((0, 1), repeat=m):
        c = sum(bits)
        p = sum(bits[:-2])
        a, b = bits[-2:]
        D = (p + 1) * (p + 2)
        utility = [v / c if c else 0 for v in bits]
        H = utility[-2] + utility[-1] + a / D
        q = []
        before = 0
        for i in range(m):
            q.append(before + m - i)
            before += bits[i]
        for d in range(m+1):
            for ell in (0, m):
                row = []
                row += [utility[i] - bits[j]/q[i]
                        for i in range(m) for j in range(m)]
                row += [m*utility[i] - d/q[i] for i in range(m)]
                G = (m*utility[-2] + utility[-1]/2 - d/(p+1)
                     - ell/(2*m*(p+a+1)) + d*ell/(m*D))
                row.append(G)
                row += [m*m*H-2*m*d/(p+1)+d*d/D,
                        m*H-2*d/(p+1)+d/D,
                        m*(m-1)*H-2*(m-1)*d/(p+1)+(d*d-d)/D]
                row += [m*H-(d+m*v)/(p+1)+d*v/D for v in bits]
                row += [H-(bits[j]+bits[k])/(p+1)+bits[j]*bits[k]/D
                        for j in range(m) for k in range(j,m)]
                columns.append(row)
                states.append([list(bits),d,ell])
                welfare.append(int(c>0))
                opt.append(int(d>0))
    return names, states, np.array(columns).T, np.array(welfare), np.array(opt)


def solve(m):
    names, states, rows, welfare, opt = build(m)
    result = linprog(-opt, A_ub=-rows, b_ub=np.zeros(len(names)),
                     A_eq=welfare[None,:], b_eq=[1],
                     bounds=(0,None), method="highs")
    out = {"m":m,"rows":len(names),"types":len(states),
           "status":result.message,"success":result.success}
    if result.success:
        out.update(beta=float(-result.fun),
                   support=[{"state":states[k],"mass":float(x)}
                            for k,x in enumerate(result.x) if x>1e-8],
                   dual=[{"row":names[k],"weight":float(-x)}
                         for k,x in enumerate(result.ineqlin.marginals) if x < -1e-8],
                   equality_dual=float(-result.eqlin.marginals[0]))
    return out


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("m",type=int)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    report=solve(args.m)
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("support","dual")},indent=2))
