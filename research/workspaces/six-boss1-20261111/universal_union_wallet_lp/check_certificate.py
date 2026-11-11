#!/usr/bin/env python3
"""Independent stdlib exact checker; no solver or builder import.

Reconstruct every coefficient from the stated source formulas, then verify
the primal, all raw rows, and the nonnegative dual residual on every column.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import lcm
import hashlib
import json

HERE=Path(__file__).resolve().parent
inp=json.loads((HERE/"exact_input.json").read_text())
cert=json.loads((HERE/"exact_certificate.json").read_text())
assert hashlib.sha256((HERE/"exact_input.json").read_bytes()).hexdigest()==cert["input_sha256"]
atoms=[tuple(r["a"])+(r["x"],r["o"]) for r in inp["atom_columns"]]
assert atoms==list(product((0,1),repeat=8))
assert [r["index"] for r in inp["atom_columns"]]==list(range(256))
assert inp["K_column"]==256 and inp["nonnegative_columns"]==list(range(257))


def columns(t, K=F(0)):
    """All 217 homogeneous left sides on one atom or the K column."""
    a=list(t[:6]); x,o=t[6:]; c=sum(a); P=sum(a[:4]); D=P+1
    us=[F(ai,c) if c else F(0) for ai in a]
    pure=a+[x]
    theta=[F(v) for v in pure]+[F(o,6)]
    fs=[v/D for v in theta]
    result={}
    for i in range(6):
        safe_den=sum(a[:i])+6-i
        for j in range(8):
            result[f"SAFE_{i+1}_{j+1}"]=us[i]-theta[j]/safe_den
    for i,C in enumerate((31,25,19,10)):
        b=sum(a[:i]); cap=b+6-i
        union_query=F(o*x,6*cap)+F(o*(1-x),6*(b+1))
        result[f"UP_{i+1}"]=C*us[i]-F((C-1)*x,cap)-union_query
    for j in list(range(6))+[7]:
        result[f"FMAX_{j+1}"]=fs[6]-fs[j]
        result[f"MX_{j+1}"]=us[4]-theta[j]/(D+x)
    for l in range(8):
        for r in range(l,8):
            if r<7:
                right_side=F(pure[l]+pure[r],D)-F(pure[l]*pure[r],D*(D+1))
            elif l<7:
                right_side=F(pure[l],D)+F(o,6*D)-F(pure[l]*o,6*D*(D+1))
            else:
                right_side=F(o,3*D)-F(o,36*D*(D+1))
            result[f"RC_{l+1}_{r+1}"]=us[4]+fs[6]-right_side
            result[f"PAIR_{l+1}_{r+1}"]=us[4]+us[5]+F(a[4],D*(D+1))-right_side
    for omit in range(7):
        result[f"OPT6_omit_{omit+1}"]=-F(any(bit for j,bit in enumerate(pure) if j!=omit))
    for j in range(7):
        result[f"K_ge_size_{j+1}"]=K-pure[j]
    result["K_le_1"]=-K
    for i in range(6):
        result[f"SIZE_FLOOR_{i+1}"]=us[i]-K/6
    result["W_le_1"]=-F(c>0)
    result["ROOT_NEAR"]=150*us[0]-F(139,6)*K-o
    for anchor in range(7):
        for query in range(8):
            result[f"ROOT_RIG_{anchor+1}_{query+1}"]=(
                25*us[0]+3*K-7*pure[anchor]
                -theta[query]+F(5,6)*pure[anchor]*theta[query])
    return result


raw={row["name"]:row for row in inp["raw_rows"]}
assert len(raw)==len(inp["raw_rows"])==217
expected_names=set(columns((0,)*8))
assert set(raw)==expected_names
semantic=[columns(t) for t in atoms]+[columns((0,)*8,F(1))]
for j in range(257):
    for name in expected_names:
        assert F(raw[name]["a"].get(str(j),"0"))==semantic[j][name], (j,name)
for name,row in raw.items():
    expected_rhs=F(-1) if name.startswith("OPT6_omit_") or name in ("K_le_1","W_le_1") else F(0)
    assert F(row["rhs"])==expected_rhs
eq={str(i):"1" for i,t in enumerate(atoms) if t[7]}
objective={str(i):"1" for i,t in enumerate(atoms) if any(t[:6])}
assert inp["equality"]["a"]==eq and F(inp["equality"]["rhs"])==1
assert inp["objective"]==objective

# Reproduce only the permitted zero/exact-duplicate pruning.
seen={}; zero=[]; names=[]
for row in inp["raw_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    if not any(key[0]) and key[1]==0:
        zero.append(row["name"])
    elif key in seen:
        seen[key].append(row["name"])
    else:
        seen[key]=[row["name"]]
        names.append(row["name"])
assert len(seen)==205
assert [r["name"] for r in inp["unique_rows"]]==names
assert inp["removed_zero_rows"]==zero
for row in inp["unique_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    assert row["aliases"]==seen[key]

z=[F(cert["primal"].get(str(j),"0")) for j in range(257)]
assert all(v>=0 for v in z)
O=sum(z[j]*t[7] for j,t in enumerate(atoms))
W=sum(z[j] for j,t in enumerate(atoms) if any(t[:6]))
assert O==1 and W==F(cert["objective"]) and W<F(1,2)
slacks={name:sum(z[j]*semantic[j][name] for j in range(257))-F(raw[name]["rhs"])
        for name in raw}
assert all(v>=0 for v in slacks.values())
assert all(str(slacks[name])==value for name,value in cert["raw_row_slacks"].items())

y={name:F(value) for name,value in cert["dual"]["row_weights"].items()}
assert len(y)==13 and all(value>0 for value in y.values())
assert set(y)<=set(names)
nu=F(cert["dual"]["normalization_multiplier"])
dual_value=nu+sum(weight*F(raw[name]["rhs"]) for name,weight in y.items())
assert dual_value==W==nu
residual=[]
for j in range(257):
    c=F(j<256 and any(atoms[j][:6]))
    e=F(atoms[j][7]) if j<256 else F(0)
    value=c-nu*e-sum(weight*semantic[j][name] for name,weight in y.items())
    residual.append(value)
    assert value>=0,(j,value)
    assert value==F(cert["dual"]["nonnegative_column_residual"].get(str(j),"0"))
    assert value*z[j]==0
assert all(slacks[name]*weight==0 for name,weight in y.items())
assert residual[256]==0
den=W.denominator; numerator=W.numerator
integer_weights={name:weight*den for name,weight in y.items()}
assert all(value.denominator==1 for value in integer_weights.values())
scaled=[value*den for value in residual]
integer_residual_multiplier=lcm(*(r.denominator for r in scaled))

with (HERE/"dual_column_checks.tsv").open("w") as f:
    f.write("column\ta1a2a3a4a5a6\tx\to\texact_residual\tD_scaled_residual\tstatus\n")
    for j,value in enumerate(residual):
        bits="".join(map(str,atoms[j][:6])) if j<256 else "K"
        x=atoms[j][6] if j<256 else "-"; o=atoms[j][7] if j<256 else "-"
        f.write(f'{j}\t{bits}\t{x}\t{o}\t{value}\t{scaled[j]}\t{"zero" if value==0 else "positive"}\n')

with (HERE/"integer_residual_table.tsv").open("w") as f:
    f.write("a1a2a3a4a5a6\tx0_o0\tx0_o1\tx1_o0\tx1_o1\n")
    for mask in range(64):
        row=[scaled[4*mask+k]*integer_residual_multiplier for k in range(4)]
        assert all(v.denominator==1 and v>=0 for v in row)
        bits="".join(map(str,atoms[4*mask][:6]))
        f.write(bits+"\t"+"\t".join(map(str,row))+"\n")

report={
    "result":"PASS: semantic matrix, all raw primal rows, all dual columns, exact optimality",
    "semantic_coefficient_equalities":217*257,
    "all_256_boolean_atom_columns_present":True,"K_true_global_scalar_column":True,
    "raw_inequalities":217,"unique_inequalities":205,"removed_zero_rows":zero,
    "nonnegative_primal_variables":257,"primal_nonzero_atoms":sum(v>0 for v in z[:256]),
    "normalization":str(O),"primal_objective":str(W),"dual_objective":str(dual_value),
    "half_gap":str(F(1,2)-W),"positive_dual_weights":len(y),
    "dual_columns_verified":257,"zero_dual_columns":[j for j,v in enumerate(residual) if v==0],
    "positive_dual_columns":sum(v>0 for v in residual),
    "smallest_positive_D_scaled_residual":str(min(v for v in scaled if v>0)),
    "D":str(den),"N":str(numerator),
    "integer_budget_weights":{name:str(value) for name,value in integer_weights.items()},
    "integer_residual_multiplier":integer_residual_multiplier,
    "K_column_residual":str(residual[256]),
    "zero_duality_gap":True,"optimizer_imported":False,
    "interpretation":"Universal bound W >= (N/D) OPT6, and exact insufficiency of this specified necessary system for half. No claim of SPE realizability or best-known improvement.",
}
(HERE/"checker_output.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
