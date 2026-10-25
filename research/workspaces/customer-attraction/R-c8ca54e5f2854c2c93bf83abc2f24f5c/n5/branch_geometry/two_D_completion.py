"""Targeted joint second/third->D completion of one necessary-condition point.

The source projection is fixed. Feasibility does not construct an SPE.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from third_D_completion import ROOT, SOURCE, THIRD, SECOND, rows as base_rows, sh


def extras(atom,p,q,r,s,t,ell,hh):
    a,b,c,d,e,u,v,w,x,y=map(int,atom["bits"])
    bits=[a,b,c,d,e,u,v,w,x,y,p,q]
    labels="ABCDEUVWXY"+"PQ"
    total=a+d+r+s+t
    own=[sh(r,total),sh(s,total),sh(t,total)]
    bg=a+d
    out={"F2D":sh(b,a+b+c+d+e)-sh(d,total)}
    j=sum(cnt*tt for cnt,(tt,rr,ss) in zip(atom["AB_hist"],THIRD))
    for pos in range(3):
        before=bg+sum((r,s,t)[:pos])
        denom=before+3-pos
        for name,z in zip(labels,bits):out[f"D2:{pos+3}:K:{name}"]=own[pos]-sh(z,denom)
        out[f"D2:{pos+3}:sumopt"]=5*own[pos]-sh(j,denom)
        out[f"D2:{pos+3}:Dmenu"]=5*own[pos]-sh(ell,denom)
        for ri,(le,_) in enumerate(atom["menus_lh"]):out[f"D2:{pos+3}:oldmenu{ri}"]=5*own[pos]-sh(le,denom)
        for fam,typelist in (("AB",THIRD),("AE",THIRD),("second",SECOND)):
            for bit in range(1,len(typelist[0])):
                count=sum(cnt*typ[bit] for cnt,typ in zip(atom[fam+"_hist"],typelist))
                out[f"D2:{pos+3}:menu:{fam}:{bit}"]=5*own[pos]-sh(count,denom)
    for pos in range(3):
        before=bg+sum((r,s,t)[:pos]);denom=before+3-pos
        for name,z in zip("RST",(r,s,t)):
            if (r,s,t)[pos]!=z or name!="RST"[pos]:
                out[f"D2:{pos+3}:K:{name}"]=own[pos]-sh(z,denom)
    paths=(("actual",[a,b,c,d,e],range(5)),
           ("secondE",[a,e,u,v,w],range(2,5)),
           ("thirdE",[a,b,e,x,y],range(3,5)),
           ("thirdD",[a,b,d,p,q],range(3,5)))
    for family,path,positions in paths:
        for pos in positions:
            payoff=sh(path[pos],sum(path));denom=sum(path[:pos])+5-pos
            for name,z in zip("RST",(r,s,t)):out[f"{family}:{pos+1}:K:{name}"]=payoff-sh(z,denom)
    for ri,oldbg in enumerate((a+b+c,a+e+u,a+b+e)):
        le,h=atom["menus_lh"][ri]
        for name,z in zip("RST",(r,s,t)):
            out[f"oldmenu{ri}:new:{name}"]=sh(le-5*z,oldbg+1)+sh(j*z-h,(oldbg+1)*(oldbg+2))
    d_bg=a+b+d
    for name,z in zip("RST",(r,s,t)):
        out[f"Dmenu:new:{name}"]=sh(ell-5*z,d_bg+1)+sh(j*z-hh,(d_bg+1)*(d_bg+2))
    for fam,offset in (("AB",a+b),("AE",a+e)):
        for name,z in zip("RST",(r,s,t)):
            v4=v5=F(0)
            for cnt,(ti,ri,si) in zip(atom[fam+"_hist"],THIRD):
                v4+=cnt*(sh(ri,offset+ti+ri+si)-sh(z,offset+ti+2))
                v5+=cnt*(sh(si,offset+ti+ri+si)-sh(z,offset+ti+ri+1))
            out[f"{fam}:4:{name}"],out[f"{fam}:5:{name}"]=v4,v5
    for name,z in zip("RST",(r,s,t)):
        vals=[F(0)]*3
        for cnt,(ti,h,i,jj) in zip(atom["second_hist"],SECOND):
            den=a+ti+h+i+jj
            vals[0]+=cnt*(sh(h,den)-sh(z,a+ti+3))
            vals[1]+=cnt*(sh(i,den)-sh(z,a+ti+h+2))
            vals[2]+=cnt*(sh(jj,den)-sh(z,a+ti+h+i+1))
        for pos,value in enumerate(vals,3):out[f"secondindexed:{pos}:{name}"]=value
    # Same-background triple comparison, no reordered-policy identification.
    out["D2:threeprofit:BPQ"]=F(5,3)*sum(own)-sh(b+p+q,a+d+b+p+q)
    # Genuine three-player profit theorem averaged over all ten optimal triples.
    profile=F(0)
    for count in range(1,4):
        if count<=j and 3-count<=5-j:
            profile+=math.comb(j,count)*math.comb(5-j,3-count)*sh(count,bg+count)
    out["D2:threeprofit:opt"]=F(50,3)*sum(own)-profile
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--source",type=Path,default=SOURCE)
    args=parser.parse_args();source=json.loads(args.source.read_text());pr=source.get("primal",source)
    atoms=pr["atoms"]
    masses=[F(at["exact_mass"]) if "exact_mass" in at else F(int(at["mass_numerator"]),int(pr["denominator"])) for at in atoms]
    types=[];allrows=[]
    for k,at in enumerate(atoms):
        j=sum(cnt*ti for cnt,(ti,ri,si) in zip(at["AB_hist"],THIRD))
        corners=sorted(set(((0,0),(j,j),(5-j,0),(5,j))))
        base_cache={(p,q,ell,h):base_rows(at,p,q,ell,h) for p,q in itertools.product((0,1),repeat=2) for ell,h in corners}
        for p,q,r,s,t in itertools.product((0,1),repeat=5):
            for ell,h in corners:
                row=dict(base_cache[p,q,ell,h]);row.update(extras(at,p,q,r,s,t,ell,h))
                types.append((k,p,q,r,s,t,ell,h));allrows.append(row)
    names=list(allrows[0]);coeff=np.array([[float(row[name]) for row in allrows] for name in names])
    eq=np.zeros((len(atoms),len(types)))
    for col,typ in enumerate(types):eq[typ[0],col]=1
    obj=np.zeros(len(types)+1);obj[-1]=1
    result=linprog(obj,A_ub=np.column_stack((-coeff,-np.ones(len(names)))),b_ub=np.zeros(len(names)),
                   A_eq=np.column_stack((eq,np.zeros(len(atoms)))),b_eq=np.array(list(map(float,masses))),
                   bounds=[(0,None)]*len(types)+[(None,None)],method="highs")
    out={"source":str(args.source),"status":result.message,"row_count":len(names),"variable_count":len(types),
         "maximum_violation":float(result.fun) if result.success else None,
         "scope":"Fixed-source necessary-condition extension only; no SPE or half-coverage conclusion"}
    if result.success:out["active_rows"]=[names[k] for k,z in enumerate(result.ineqlin.marginals) if abs(z)>1e-8]
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":main()
