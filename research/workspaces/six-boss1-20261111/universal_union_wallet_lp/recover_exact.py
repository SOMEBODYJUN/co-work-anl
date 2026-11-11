#!/usr/bin/env python3
"""Exact linear-algebra recovery only. This file does not import an optimizer."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
from math import lcm
import hashlib
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/"exact_input.json").read_text())
discovery=json.loads((HERE/"discovery_output.json").read_text())
assert discovery["optimizer_calls"]==1 and discovery["success"]
N=257


def rational_vector(d):
    return [F(d.get(str(i),"0")) for i in range(N)]


def sr(v):
    return sp.Rational(v.numerator,v.denominator)


def fr(v):
    assert v.is_Rational
    return F(int(v.p),int(v.q))


A=[rational_vector(row["a"]) for row in data["unique_rows"]]
b=[F(row["rhs"]) for row in data["unique_rows"]]
eq=rational_vector(data["equality"]["a"])
cost=rational_vector(data["objective"])
support=[j for j,x in enumerate(discovery["x"]) if x>1e-9]
tight=[i for i,s in enumerate(discovery["inequality_residual"]) if abs(s)<1e-8]
M=sp.Matrix([[sr(eq[j]) for j in support]]+
            [[sr(A[i][j]) for j in support] for i in tight])
B=sp.Matrix([1]+[sr(b[i]) for i in tight])
solution=sp.linsolve((M,B))
assert len(solution)==1
sol=next(iter(solution))
assert not set().union(*(x.free_symbols for x in sol)), "Non-unique recovered face"
primal=[F(0)]*N
for j,x in zip(support,sol):
    primal[j]=fr(x)
assert all(x>=0 for x in primal)
assert sum(x*y for x,y in zip(eq,primal))==1
slacks=[sum(x*y for x,y in zip(row,primal))-rhs for row,rhs in zip(A,b)]
assert all(s>=0 for s in slacks)
objective=sum(x*y for x,y in zip(cost,primal))
assert objective<F(1,2)

# Recover the discovered dual support using exact complementary equations.
# For min c.z with A.z>=b, y>=0 and free nu obey A^T y+nu e<=c.
dsupport=[i for i,x in enumerate(discovery["inequality_marginals"]) if -x>1e-9]
DM=sp.Matrix([[sr(A[i][j]) for i in dsupport]+[sr(eq[j])] for j in support])
DB=sp.Matrix([sr(cost[j]) for j in support])
dsolution=sp.linsolve((DM,DB))
assert len(dsolution)==1
dsol=next(iter(dsolution))
assert not set().union(*(x.free_symbols for x in dsol)), "Non-unique recovered dual"
dual=[F(0)]*len(A)
for i,y in zip(dsupport,dsol[:-1]):
    dual[i]=fr(y)
nu=fr(dsol[-1])
assert all(y>=0 for y in dual)
reduced=[cost[j]-sum(dual[i]*A[i][j] for i in dsupport)-nu*eq[j] for j in range(N)]
assert all(r>=0 for r in reduced)
dual_objective=sum(y*rhs for y,rhs in zip(dual,b))+nu
assert dual_objective==objective
assert all(s*y==0 for s,y in zip(slacks,dual))
assert all(x*r==0 for x,r in zip(primal,reduced))

rawslacks={}
for row in data["raw_rows"]:
    lhs=sum(F(v)*primal[int(j)] for j,v in row["a"].items())
    rawslacks[row["name"]]=lhs-F(row["rhs"])
assert all(s>=0 for s in rawslacks.values())
atoms=data["atom_columns"]
sizes=[sum(primal[t["index"]]*((t["a"]+[t["x"]])[j]) for t in atoms) for j in range(7)]
payoffs=[sum(primal[t["index"]]*F(t["a"][j],sum(t["a"]))
             for t in atoms if sum(t["a"])) for j in range(6)]
FX=sum(primal[t["index"]]*F(t["x"],sum(t["a"][:4])+1) for t in atoms)
load={str(c):str(sum(primal[t["index"]] for t in atoms if sum(t["a"])==c)) for c in range(7)}
common_denominator=lcm(*(v.denominator for v in primal))
cert={
    "claim":"Exact optimum of the specified universal necessary projection is below one half; not an SPE counterexample.",
    "input_sha256":hashlib.sha256((HERE/"exact_input.json").read_bytes()).hexdigest(),
    "primal":{str(j):str(primal[j]) for j in support},
    "objective":str(objective),"half_gap":str(F(1,2)-objective),
    "K":str(primal[256]),"normalization":"1",
    "common_denominator":str(common_denominator),
    "integer_scaled_primal":{str(j):str(primal[j]*common_denominator) for j in support},
    "recovery":{"positive_columns":support,"candidate_active_rows":tight,
                "exact_restricted_rank":int(M.rank()),"unknown_count":len(support),
                "dual_support_indices":dsupport,"dual_restricted_rank":int(DM.rank())},
    "dual":{"row_weights":{data["unique_rows"][i]["name"]:str(dual[i]) for i in dsupport},
            "normalization_multiplier":str(nu),"objective":str(dual_objective),
            "nonnegative_column_residual":{str(j):str(r) for j,r in enumerate(reduced) if r}},
    "raw_row_slacks":{name:str(s) for name,s in rawslacks.items()},
    "active_raw_rows":[name for name,s in rawslacks.items() if s==0],
    "derived":{"sizes_A1_A6_X":[str(x) for x in sizes],"u1_u6":[str(x) for x in payoffs],
               "F_X":str(FX),"load_mass":load,
               "outside_O_mass":str(sum(primal[t["index"]] for t in atoms if not t["o"]))},
}
(HERE/"exact_certificate.json").write_text(json.dumps(cert,indent=2)+"\n")
with (HERE/"exact_row_checks.tsv").open("w") as f:
    f.write("row\tfamily\texact_slack\tstatus\n")
    for row in data["raw_rows"]:
        s=rawslacks[row["name"]]
        f.write(f'{row["name"]}\t{row["family"]}\t{s}\t{"tight" if s==0 else "positive"}\n')
summary={
    "objective":str(objective),"objective_float":float(objective),"half_gap":str(F(1,2)-objective),
    "positive_atom_count":len([j for j in support if j<256]),"K":str(primal[256]),
    "all_raw_rows_pass":len(rawslacks),"active_raw_rows":cert["active_raw_rows"],
    "sizes_float":[float(x) for x in sizes],"payoffs_float":[float(x) for x in payoffs],
    "dual_rows":cert["dual"]["row_weights"],"dual_verified_columns":N,
    "common_denominator":str(common_denominator),
}
(HERE/"exact_recovery_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
