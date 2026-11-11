#!/usr/bin/env python3
"""One fresh LP on all 256 actual/X/optimal-union types. No retries."""
from __future__ import annotations
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ATOMS = list(itertools.product((0, 1), repeat=8))
N = 257
raw = []


def u(t, i):
    c = sum(t[:6])
    return F(t[i], c) if c else F(0)


def vrow(name, family, fn, k=F(0), rhs=F(0)):
    values = tuple(F(fn(t)) for t in ATOMS) + (F(k),)
    raw.append({"name": name, "family": family, "a": values, "rhs": F(rhs)})


def q(t, label):
    return F(t[label]) if label < 7 else F(t[7], 6)


def pair_rhs(t, left, right):
    D = sum(t[:4]) + 1
    if left == 7 and right == 7:
        return F(t[7], 3*D) - F(t[7], 36*D*(D+1))
    return (q(t, left)+q(t, right))/D - q(t, left)*q(t, right)/(D*(D+1))


for i in range(6):
    for j in range(8):
        vrow(f"SAFE_{i+1}_{j+1}", "SAFE", lambda t,i=i,j=j:
             u(t,i)-q(t,j)/(sum(t[:i])+6-i))

for i, C in enumerate((31,25,19,10)):
    vrow(f"UP_{i+1}", "UP", lambda t,i=i,C=C:
         C*u(t,i)-F((C-1)*t[6],sum(t[:i])+6-i)
         -F(t[7],6)*(F(t[6],sum(t[:i])+6-i)+F(1-t[6],sum(t[:i])+1)))

for j in (*range(6),7):
    vrow(f"FMAX_{j+1}", "FMAX", lambda t,j=j:
         (F(t[6])-q(t,j))/(sum(t[:4])+1))
    vrow(f"MX_{j+1}", "MX", lambda t,j=j:
         u(t,4)-q(t,j)/(sum(t[:4])+1+t[6]))

for left in range(8):
    for right in range(left,8):
        vrow(f"RC_{left+1}_{right+1}", "RC", lambda t,l=left,r=right:
             u(t,4)+F(t[6],sum(t[:4])+1)-pair_rhs(t,l,r))
        vrow(f"PAIR_{left+1}_{right+1}", "PAIR", lambda t,l=left,r=right:
             u(t,4)+u(t,5)+F(t[4],(sum(t[:4])+1)*(sum(t[:4])+2))-pair_rhs(t,l,r))

for omit in range(7):
    vrow(f"OPT6_omit_{omit+1}", "OPT6", lambda t,omit=omit:
         -int(any(t[j] for j in range(7) if j!=omit)), rhs=-1)
for j in range(7):
    vrow(f"K_ge_size_{j+1}", "KSIZE", lambda t,j=j: -t[j], k=1)
vrow("K_le_1", "KCAP", lambda t:0, k=-1, rhs=-1)
for i in range(6):
    vrow(f"SIZE_FLOOR_{i+1}", "FLOOR", lambda t,i=i:u(t,i), k=-F(1,6))
vrow("W_le_1", "WCAP", lambda t:-int(any(t[:6])), rhs=-1)
vrow("ROOT_NEAR", "ROOT_NEAR", lambda t:150*u(t,0)-t[7], k=-F(139,6))
for anchor in range(7):
    for query in range(8):
        vrow(f"ROOT_RIG_{anchor+1}_{query+1}", "ROOT_RIG",
             lambda t,anchor=anchor,query=query:
             25*u(t,0)-7*t[anchor]-q(t,query)*(1-F(5*t[anchor],6)), k=3)

unique, lookup, zero = [], {}, []
for row in raw:
    key=(row["a"],row["rhs"])
    if not any(row["a"]) and row["rhs"]==0:
        zero.append(row["name"])
    elif key in lookup:
        unique[lookup[key]]["aliases"].append(row["name"])
    else:
        lookup[key]=len(unique)
        unique.append({**row,"aliases":[row["name"]]})


def encrow(row):
    return {k:({str(j):str(x) for j,x in enumerate(v) if x} if k=="a"
               else str(v) if k=="rhs" else v) for k,v in row.items()}


def main():
    result_path=HERE/"discovery_output.json"
    marker=HERE/"single_lp_started.txt"
    if result_path.exists() or marker.exists():
        raise SystemExit("Single-LP budget already consumed; refusing optimizer retry.")
    source_paths=[
        "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
        "research/workspaces/six-boss1-20261111/main_optimal_union_prefix.md",
        "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.md",
        "research/workspaces/six-boss1-20261111/main_full_average_pair.md",
        "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
        "archives/customer-attraction/state/推论/最大主题根近饱和的覆盖阈值--推论.md",
        "archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md",
    ]
    input_data={
        "scope":"all 256 actual bits/X/OPT-union atoms plus true global cardinality K; necessary relaxation",
        "raw_inequality_count":len(raw),"unique_inequality_count":len(unique),
        "atom_columns":[{"index":i,"a":list(t[:6]),"x":t[6],"o":t[7]} for i,t in enumerate(ATOMS)],
        "K_column":256,"nonnegative_columns":list(range(N)),
        "objective":{str(i):"1" for i,t in enumerate(ATOMS) if any(t[:6])},
        "equality":{"name":"OPT_union_normalization","a":{str(i):"1" for i,t in enumerate(ATOMS) if t[7]},"rhs":"1"},
        "inequality_convention":"a dot z >= rhs",
        "raw_rows":[encrow(r) for r in raw],"unique_rows":[encrow(r) for r in unique],
        "removed_zero_rows":zero,
        "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
        "derivation_sha256":hashlib.sha256((HERE/"source_derivations.md").read_bytes()).hexdigest(),
    }
    (HERE/"exact_input.json").write_text(json.dumps(input_data,indent=2,ensure_ascii=False)+"\n")
    import numpy as np
    import scipy
    from scipy.optimize import linprog
    A=np.array([[-float(v) for v in r["a"]] for r in unique])
    b=np.array([-float(r["rhs"]) for r in unique])
    eq=np.array([[float(t[7]) for t in ATOMS]+[0.]])
    cost=np.array([float(any(t[:6])) for t in ATOMS]+[0.])
    marker.write_text("Exactly one scipy.optimize.linprog invocation follows this marker.\n")
    result=linprog(cost,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1.],bounds=(0,None),method="highs")
    output={"solver":"scipy.optimize.linprog/highs","scipy_version":scipy.__version__,
        "optimizer_calls":1,"success":bool(result.success),"status":int(result.status),
        "message":result.message,"iterations":int(result.nit),
        "variables":N,"raw_rows":len(raw),"unique_rows":len(unique),
        "objective":None if result.fun is None else float(result.fun),
        "x":None if result.x is None else result.x.tolist(),
        "inequality_residual":None if result.ineqlin.residual is None else result.ineqlin.residual.tolist(),
        "inequality_marginals":None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist(),
        "equality_marginals":None if result.eqlin.marginals is None else result.eqlin.marginals.tolist(),
        "lower_marginals":None if result.lower.marginals is None else result.lower.marginals.tolist(),
    }
    result_path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:output[k] for k in ("success","status","message","objective","variables","raw_rows","unique_rows","iterations")},indent=2))
    if result.x is not None:
        print("positive_columns",[(i,float(v)) for i,v in enumerate(result.x) if v>1e-9])


if __name__=="__main__":
    main()
