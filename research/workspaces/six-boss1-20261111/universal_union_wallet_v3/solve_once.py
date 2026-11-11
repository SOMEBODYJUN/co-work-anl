#!/usr/bin/env python3
"""One explicitly released v3 LP, with recorded positive rational row scaling."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json

HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inp=json.loads((HERE/"exact_input.json").read_text());pre=json.loads((HERE/"source_check.json").read_text())
release=json.loads((HERE/"main_release.json").read_text())
assert pre["status"]=="PASS" and pre["input_sha256"]==sha(HERE/"exact_input.json")
assert release["input_sha256"]==sha(HERE/"exact_input.json") and release["authorized_by"]=="/root"
assert not (HERE/"single_lp_started.txt").exists() and not (HERE/"discovery_output.json").exists(),"No optimizer retry permitted"
rows=inp["unique_rows"]
av=[[F(r["a"].get(str(j),"0")) for j in range(257)] for r in rows];bv=[F(r["rhs"]) for r in rows]
scales=[max(F(1),abs(b),*(abs(v) for v in a)) for a,b in zip(av,bv)]
scaling={"definition":"s=max(1,abs(rhs),max_abs_column); solver uses a/s and rhs/s",
         "row_scales":{r["name"]:str(s) for r,s in zip(rows,scales)},"all_strictly_positive":all(s>0 for s in scales)}
(HERE/"numerical_scaling.json").write_text(json.dumps(scaling,indent=2)+"\n")
import numpy as np
import scipy
from scipy.optimize import linprog
A=np.array([[-float(v/s) for v in a] for a,s in zip(av,scales)])
b=np.array([-float(v/s) for v,s in zip(bv,scales)])
cost=np.array([float(F(inp["objective"].get(str(j),"0"))) for j in range(257)])
eq=np.array([[float(F(inp["equality"]["a"].get(str(j),"0"))) for j in range(257)]])
(HERE/"single_lp_started.txt").write_text("Exactly one positively row-scaled scipy.optimize.linprog follows; Main release and source preflight checked.\n")
result=linprog(cost,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1.],bounds=(0,None),method="highs")
out={"solver":"scipy.optimize.linprog/highs","scipy_version":scipy.__version__,"optimizer_calls":1,
     "input_sha256":sha(HERE/"exact_input.json"),"release_sha256":sha(HERE/"main_release.json"),
     "success":bool(result.success),"status":int(result.status),"message":result.message,"iterations":int(result.nit),
     "variables":257,"raw_rows":221,"unique_rows":len(rows),"row_scales":[str(s) for s in scales],
     "objective":None if result.fun is None else float(result.fun),
     "x":None if result.x is None else result.x.tolist(),
     "inequality_residual_scaled":None if result.ineqlin.residual is None else result.ineqlin.residual.tolist(),
     "inequality_marginals_scaled":None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist(),
     "equality_marginals":None if result.eqlin.marginals is None else result.eqlin.marginals.tolist(),
     "lower_marginals":None if result.lower.marginals is None else result.lower.marginals.tolist()}
(HERE/"discovery_output.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ["success","status","objective","iterations","variables","raw_rows","unique_rows"]},indent=2))
if result.x is not None:print("positive_columns",[(j,float(v)) for j,v in enumerate(result.x) if v>1e-9])
