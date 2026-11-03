"""Exact seven-row second->D envelope separating the historical primal."""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from third_D_completion import SOURCE, THIRD, SECOND, sh

NAMES=("F2D","last:E","last:sumopt","AE4:R","AE4:S","second3:T","second4:T")


def seven(atom,r,s,t):
    a,b,c,d,e,u,v,w,x,y=map(int,atom["bits"])
    total=a+d+r+s+t
    j=sum(cnt*ti for cnt,(ti,ri,si) in zip(atom["AE_hist"],THIRD))
    ae4=F(0);cae=F(0)
    for cnt,(ti,ri,si) in zip(atom["AE_hist"],THIRD):
        ae4+=cnt*sh(ri,a+e+ti+ri+si)
        cae+=cnt*F(1,a+e+ti+2)
    sec3=sec4=cs3=cs4=F(0)
    for cnt,(ti,h,i,jj) in zip(atom["second_hist"],SECOND):
        den=a+ti+h+i+jj
        sec3+=cnt*sh(h,den);sec4+=cnt*sh(i,den)
        cs3+=cnt*F(1,a+ti+3);cs4+=cnt*F(1,a+ti+h+2)
    return (sh(b,a+b+c+d+e)-sh(d,total),
            sh(t,total)-sh(e,a+d+r+s+1),
            5*sh(t,total)-sh(j,a+d+r+s+1),
            ae4-r*cae,ae4-s*cae,sec3-t*cs3,sec4-t*cs4)


def main():
    pr=json.loads(SOURCE.read_text())["primal"];atoms=pr["atoms"]
    masses=[F(int(z["mass_numerator"]),int(pr["denominator"])) for z in atoms]
    states=list(itertools.product((0,1),repeat=3))
    coeffs=[[seven(atom,*state) for state in states] for atom in atoms]
    columns=[coeff for group in coeffs for coeff in group]
    matrix=np.array([[float(col[k]) for col in columns] for k in range(7)])
    eq=np.kron(np.eye(len(atoms)),np.ones((1,8)))
    obj=np.zeros(len(columns)+1);obj[-1]=1
    sol=linprog(obj,A_ub=np.column_stack((-matrix,-np.ones(7))),b_ub=np.zeros(7),
                A_eq=np.column_stack((eq,np.zeros(len(atoms)))),b_eq=np.array(list(map(float,masses))),
                bounds=[(0,None)]*len(columns)+[(None,None)],method="highs")
    assert sol.success and sol.fun>0
    raw=-sol.ineqlin.marginals
    # Rounded rational weights suffice; exact nonnegative support audit is below.
    weights=[F(round(float(z)*1000000),1000000) for z in raw]
    weights[3]=weights[4]=(weights[3]+weights[4])/2
    maximums=[max(sum(w*c for w,c in zip(weights,coeff)) for coeff in group) for group in coeffs]
    gap=sum(m*z for m,z in zip(masses,maximums))
    assert all(w>=0 for w in weights) and gap<0
    out={"status":"Exact separation of historical relaxation primal; not an SPE counterexample or half proof",
         "numerical_minimax_violation":float(sol.fun),
         "nonnegative_weights":dict(zip(NAMES,map(str,weights))),
         "exact_projected_slack":str(gap),"approx_projected_slack":float(gap),
         "maximums":[str(z) for z in maximums]}
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="maximums"},indent=2))


if __name__=="__main__":main()
