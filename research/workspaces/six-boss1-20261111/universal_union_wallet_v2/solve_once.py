#!/usr/bin/env python3
"""The one explicitly released v2 LP; every proof is checked separately."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json

HERE=Path(__file__).resolve().parent;RUN=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
release=json.loads((HERE/"main_cut_release.json").read_text())
assert release["decision"]=="explicit Main cut release granted"
inp=json.loads((HERE/"exact_input.json").read_text())
preflight=json.loads((HERE/"source_check.json").read_text())
assert preflight["status"]=="PASS" and preflight["input_sha256"]==sha(HERE/"exact_input.json")
assert release["tail_input_sha256"]==inp["source_sha256"]["universal_true_x_tail/exact_input.json.gz"]
assert release["tail_certificate_sha256"]==inp["source_sha256"]["universal_true_x_tail/exact_certificate.json"]
assert release["tail_freeze_sha256"]==sha(RUN/"universal_true_x_tail/freeze_manifest.json")
assert not (HERE/"single_lp_started.txt").exists() and not (HERE/"discovery_output.json").exists(),"No optimizer retry permitted"
import numpy as np
import scipy
from scipy.optimize import linprog
rows=inp["unique_rows"]
A=np.array([[-float(F(row["a"].get(str(j),"0"))) for j in range(257)] for row in rows])
b=np.array([-float(F(row["rhs"])) for row in rows])
cost=np.array([float(F(inp["objective"].get(str(j),"0"))) for j in range(257)])
eq=np.array([[float(F(inp["equality"]["a"].get(str(j),"0"))) for j in range(257)]])
(HERE/"single_lp_started.txt").write_text("Exactly one scipy.optimize.linprog call follows; Main release and source preflight checked.\n")
result=linprog(cost,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1.],bounds=(0,None),method="highs")
out={"solver":"scipy.optimize.linprog/highs","scipy_version":scipy.__version__,"optimizer_calls":1,
     "input_sha256":sha(HERE/"exact_input.json"),"release_sha256":sha(HERE/"main_cut_release.json"),
     "success":bool(result.success),"status":int(result.status),"message":result.message,"iterations":int(result.nit),
     "variables":257,"raw_rows":219,"unique_rows":len(rows),
     "objective":None if result.fun is None else float(result.fun),
     "x":None if result.x is None else result.x.tolist(),
     "inequality_residual":None if result.ineqlin.residual is None else result.ineqlin.residual.tolist(),
     "inequality_marginals":None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist(),
     "equality_marginals":None if result.eqlin.marginals is None else result.eqlin.marginals.tolist(),
     "lower_marginals":None if result.lower.marginals is None else result.lower.marginals.tolist()}
(HERE/"discovery_output.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ["success","status","objective","iterations","variables","raw_rows","unique_rows"]},indent=2))
if result.x is not None:print("positive_columns",[(j,float(v)) for j,v in enumerate(result.x) if v>1e-9])
