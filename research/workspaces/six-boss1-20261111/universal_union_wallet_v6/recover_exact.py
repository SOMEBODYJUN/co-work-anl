#!/usr/bin/env python3
"""Exact linear-algebra recovery from the single v6 discovery with positive row scaling; no optimizer."""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
import hashlib,json
import sympy as sp

HERE=Path(__file__).resolve().parent
inp=json.loads((HERE/"exact_input.json").read_text())
disc=json.loads((HERE/"discovery_output.json").read_text())
assert disc["success"] and disc["optimizer_calls"]==1
assert disc["input_sha256"]==hashlib.sha256((HERE/"exact_input.json").read_bytes()).hexdigest()
N=257
vec=lambda d:[F(d.get(str(j),"0")) for j in range(N)]
sr=lambda f:sp.Rational(f.numerator,f.denominator)
fr=lambda r:F(int(r.p),int(r.q))
rows=inp["unique_rows"];A=[vec(r["a"]) for r in rows];b=[F(r["rhs"]) for r in rows]
eq=vec(inp["equality"]["a"]);cost=vec(inp["objective"])
support=[j for j,x in enumerate(disc["x"]) if x>1e-9]
tight=[i for i,x in enumerate(disc["inequality_residual_scaled"]) if abs(x)<1e-8]
M=sp.Matrix([[sr(eq[j]) for j in support]]+[[sr(A[i][j]) for j in support] for i in tight])
rhs=sp.Matrix([1]+[sr(b[i]) for i in tight])
solset=sp.linsolve((M,rhs));assert len(solset)==1
sol=next(iter(solset));assert all(not v.free_symbols and v.is_Rational for v in sol)
z=[F(0)]*N
for j,v in zip(support,sol):z[j]=fr(v)
assert all(v>=0 for v in z) and sum(eq[j]*z[j] for j in range(N))==1
slacks=[sum(a*zj for a,zj in zip(row,z))-br for row,br in zip(A,b)]
assert all(v>=0 for v in slacks)
W=sum(c*zj for c,zj in zip(cost,z))
dsupport=[i for i,x in enumerate(disc["inequality_marginals_scaled"]) if -x>1e-10]
DM=sp.Matrix([[sr(A[i][j]) for i in dsupport]+[sr(eq[j])] for j in support])
DB=sp.Matrix([sr(cost[j]) for j in support])
dset=sp.linsolve((DM,DB));assert len(dset)==1
dsol=next(iter(dset));assert all(not v.free_symbols and v.is_Rational for v in dsol)
y=[F(0)]*len(rows)
for i,v in zip(dsupport,dsol[:-1]):y[i]=fr(v)
nu=fr(dsol[-1]);assert all(v>=0 for v in y)
res=[cost[j]-nu*eq[j]-sum(y[i]*A[i][j] for i in dsupport) for j in range(N)]
assert all(v>=0 for v in res)
dual=sum(y[i]*b[i] for i in dsupport)+nu
assert dual==W and all(slacks[i]*y[i]==0 for i in dsupport)
assert all(res[j]*z[j]==0 for j in range(N))
baseline=F(json.loads((HERE/"baseline_dual_extension.json").read_text())["objective"])
assert W>=baseline
raw_slacks={r["name"]:sum(F(v)*z[int(j)] for j,v in r["a"].items())-F(r["rhs"]) for r in inp["raw_rows"]}
assert all(v>=0 for v in raw_slacks.values())
atoms=inp["atom_columns"]
sizes=[sum(z[r["index"]]*(r["a"]+[r["x"]])[j] for r in atoms) for j in range(7)]
payoffs=[sum(z[r["index"]]*F(r["a"][i],sum(r["a"])) for r in atoms if sum(r["a"])) for i in range(6)]
FX=sum(z[r["index"]]*F(r["x"],sum(r["a"][:4])+1) for r in atoms)
den=lcm(*(v.denominator for v in z))
cert={
    "claim":"Exact optimum of the full256-type v6 necessary system, with matching universal nonnegative dual; no SPE realization claim",
    "input_sha256":disc["input_sha256"],"optimizer_calls":1,
    "primal":{str(j):str(z[j]) for j in support},"objective":str(W),"half_gap":str(F(1,2)-W),"K":str(z[256]),
    "common_denominator":str(den),"integer_scaled_primal":{str(j):str(z[j]*den) for j in support},
    "recovery":{"positive_columns":support,"active_unique_rows":tight,"primal_restricted_rank":int(M.rank()),
                "primal_unknown_count":len(support),"positive_dual_indices":dsupport,"dual_restricted_rank":int(DM.rank())},
    "dual":{"row_weights":{rows[i]["name"]:str(y[i]) for i in dsupport},"normalization_multiplier":str(nu),
            "objective":str(dual),"nonnegative_column_residual":{str(j):str(v) for j,v in enumerate(res) if v}},
    "raw_row_slacks":{name:str(value) for name,value in raw_slacks.items()},
    "active_raw_rows":[name for name,value in raw_slacks.items() if value==0],
    "derived":{"sizes_A1_A6_X":[str(v) for v in sizes],"u1_u6":[str(v) for v in payoffs],"F_X":str(FX),
               "outside_O_mass":str(sum(z[r["index"]] for r in atoms if not r["o"])),
               "load_mass":{str(c):str(sum(z[r["index"]] for r in atoms if sum(r["a"])==c)) for c in range(7)}},
    "prior_constructed_bound":str(baseline),"improvement_over_prior_bound":str(W-baseline),
}
(HERE/"exact_certificate.json").write_text(json.dumps(cert,indent=2)+"\n")
with (HERE/"exact_row_checks.tsv").open("w") as out:
    out.write("row\tfamily\texact_slack\tstatus\n")
    for r in inp["raw_rows"]:
        s=raw_slacks[r["name"]];out.write(f'{r["name"]}\t{r["family"]}\t{s}\t{"tight" if s==0 else "positive"}\n')
summary={"objective":str(W),"objective_decimal":float(W),"half_gap":str(F(1,2)-W),
    "positive_atoms":sum(j<256 for j in support),"K":str(z[256]),"all_raw_rows_pass":867,"all_dual_columns_pass":257,
    "dual_rows":cert["dual"]["row_weights"],"active_raw_rows":cert["active_raw_rows"],
    "sizes_float":[float(v) for v in sizes],"payoffs_float":[float(v) for v in payoffs],
    "common_denominator":str(den),"improvement_over_prior_bound":str(W-baseline)}
(HERE/"exact_recovery_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
