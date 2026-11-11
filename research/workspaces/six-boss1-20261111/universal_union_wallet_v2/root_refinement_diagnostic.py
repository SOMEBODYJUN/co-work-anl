#!/usr/bin/env python3
"""Exact appendix only. This refinement is NOT added to the219-row input."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib

HERE=Path(__file__).resolve().parent
rows=[];ratios=[]
for bits in product((0,1),repeat=7):
    p,y2,y3,y4,y5,t,o=bits;n=y2+y3+y4+y5;load=p+n+t;theta=F(o,6)
    v=F(p,load) if load else F(0);s=F(y5,load) if load else F(0);w=F(t,load) if load else F(0)
    tau=F(n,2)+t-7*p+25*v-w-theta/(1+5*p)+theta/(1+p+n)
    delta=v-s+theta/(p+n-y5+2)-F(o,12)+F(p,18)
    rho=delta+F(12,5)*tau
    kappa=F(65,84)*rho-tau-F(5,12)*(p-y5)
    assert tau>=0 and rho>=0 and kappa>=0
    paid=(-67140*v+2340*(s-theta/(p+n-y5+2))-1296*(y2+y3+y4)-2556*y5
          -2592*t+2592*(w-theta/(1+p+n))+360*p*(1-o)+3024*kappa)
    assert paid+18914*p+627*o==0
    if rho>0:ratios.append(((tau+F(5,12)*(p-y5))/rho,bits))
    rows.append({"bits":list(bits),"tau":str(tau),"delta":str(delta),"rho":str(rho),"kappa":str(kappa)})
assert max(ratios)[0]==F(65,84)
cert=json.loads((HERE/"exact_certificate.json").read_text())
u1=F(cert["derived"]["u1_u6"][0]);K=F(cert["K"]);O=F(1)
H=150*u1-F(139,6)*K-O;L=10980*u1-1658*K-87*O
J=67140*u1-9878*K-627*O
assert L==0 and H>0 and J==13*L-504*H<0
report={
    "status":"PASS: universal appendix refinement; excluded from219-row solve",
    "included_in_219_row_input":False,"optimizer_calls":0,
    "point_certificate_sha256":hashlib.sha256((HERE/"exact_certificate.json").read_bytes()).hexdigest(),
    "all128_types_checked":True,"inequality":"tau+(5/12)(p-y5) <= (65/84)rho",
    "maximum_ratio":"65/84","max_ratio_types":[list(bits) for ratio,bits in ratios if ratio==F(65,84)],
    "zero_rho_types":[r for r in rows if F(r["rho"])==0],
    "minimum_kappa":str(min(F(r["kappa"]) for r in rows)),
    "universal_refinement":"13L-504H=67140*u1-9878*K-627*O >=0",
    "positive_wallet_weights":{"root_IC":"67140","true_fifth_SAFE":"2340","D2":"1296","D3":"1296","D4":"1296","D5":"2556","D_terminal":"2592","terminal_BR":"2592","C_outside_O":"360","sum_kappa":"3024"},
    "point_H":str(H),"point_L":str(L),"point_J":str(J),"point_J_decimal":float(J),
    "point_excluded_from_SPE":True,"whole_v2_optimal_face_claimed":False,
    "not_claimed":["this refinement is in219-row LP","improved optimized ratio after refinement","half","best-known bound"],
    "types":rows,
}
(HERE/"root_refinement_diagnostic.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k not in ("types","zero_rho_types")},indent=2))
