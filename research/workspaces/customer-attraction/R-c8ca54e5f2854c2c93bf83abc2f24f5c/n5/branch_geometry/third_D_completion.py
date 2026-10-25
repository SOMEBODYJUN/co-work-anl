"""Targeted test: can the historical primal acquire one true third->D pair?

This is a necessary-condition extension test, not SPE completion or half proof.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
SOURCE = ROOT / "evidence/certificates/customer_attraction/five_player_indexed_bound.json"
THIRD = list(itertools.product((0, 1), repeat=3))
SECOND = list(itertools.product((0, 1), repeat=4))


def sh(n, d):
    return F(n, d) if n else F(0)


def rows(atom, p, q, ell_new=None, h_new=None):
    b = list(map(int, atom["bits"]))
    a, bb, c, d, e, u, v, w, x, y = b
    full = a + bb + c + d + e
    ua = [sh(z, full) for z in b[:5]]
    paths = (([a, bb, c, d, e], range(5)),
             ([a, e, u, v, w], range(2, 5)),
             ([a, bb, e, x, y], range(3, 5)))
    out = {}
    for k, (path, positions) in enumerate(paths):
        total = sum(path)
        for pos in positions:
            own = sh(path[pos], total)
            bg = sum(path[:pos])
            rem = 5 - pos
            for name, z in (("P", p), ("Q", q)):
                out[f"old{k}:{pos}:K:{name}"] = own - sh(z, bg + rem)
    bg = a + bb + d
    total = bg + p + q
    up, uq = sh(p, total), sh(q, total)
    out["F3D"] = ua[2] - sh(d, total)
    for name, z in zip("ABCDEUVWXY", b):
        out[f"P:K:{name}"] = up - sh(z, bg + 2)
        out[f"Q:K:{name}"] = uq - sh(z, bg + p + 1)
    out["P:K:Q"] = up - sh(q, bg + 2)
    out["Q:K:P"] = uq - sh(p, bg + p + 1)
    hist = atom["AB_hist"]
    j = sum(cnt*t for cnt, (t,r,s) in zip(hist, THIRD))
    out["Q:sumopt"] = 5*uq - sh(j, bg + p + 1)
    out["P:sumopt"] = 5*up - sh(j, bg + 2)
    htax = up + uq + sh(p, (bg + 1)*(bg + 2))
    out["pair:opt"] = 10*htax - sh(j*(5-j), bg+1) - sh(j*(j-1), bg+2)
    for ri, oldbg in enumerate((a+bb+c, a+e+u, a+bb+e)):
        ell,h = atom["menus_lh"][ri]
        div = (oldbg+1)*(oldbg+2)
        for name,z in (("P",p),("Q",q)):
            out[f"oldmenu{ri}:{name}"] = sh(ell-5*z,oldbg+1)+sh(j*z-h,div)
        out[f"P:menu{ri}"] = 5*up-sh(ell,bg+2)
        out[f"Q:menu{ri}"] = 5*uq-sh(ell,bg+p+1)
    for fam, offset in (("AB", a+bb), ("AE", a+e)):
        for name,z in (("P",p),("Q",q)):
            r4=r5=F(0)
            for cnt,(t,r,s) in zip(atom[fam+"_hist"],THIRD):
                r4+=cnt*(sh(r,offset+t+r+s)-sh(z,offset+t+2))
                r5+=cnt*(sh(s,offset+t+r+s)-sh(z,offset+t+r+1))
            out[f"{fam}:4:{name}"],out[f"{fam}:5:{name}"]=r4,r5
        for bit,label in ((1,"R"),(2,"S")):
            count=sum(cnt*typ[bit] for cnt,typ in zip(atom[fam+"_hist"],THIRD))
            out[f"P:menu:{fam}:{label}"]=5*up-sh(count,bg+2)
            out[f"Q:menu:{fam}:{label}"]=5*uq-sh(count,bg+p+1)
    for name,z in (("P",p),("Q",q)):
        vals=[F(0),F(0),F(0)]
        for cnt,(t,h,i,jj) in zip(atom["second_hist"],SECOND):
            den=a+t+h+i+jj
            vals[0]+=cnt*(sh(h,den)-sh(z,a+t+3))
            vals[1]+=cnt*(sh(i,den)-sh(z,a+t+h+2))
            vals[2]+=cnt*(sh(jj,den)-sh(z,a+t+h+i+1))
        for position,value in enumerate(vals,3):out[f"second:{position}:{name}"]=value
    for bit,label in ((1,"H"),(2,"I"),(3,"J")):
        count=sum(cnt*typ[bit] for cnt,typ in zip(atom["second_hist"],SECOND))
        out[f"P:menu:second:{label}"]=5*up-sh(count,bg+2)
        out[f"Q:menu:second:{label}"]=5*uq-sh(count,bg+p+1)
    if ell_new is None:
        return out
    ell,h=ell_new,h_new
    dd=(bg+1)*(bg+2)
    out["Dmenu:S"]=5*up-sh(j,bg+1)+sh(h,dd)
    out["Dmenu:V"]=sh(j*ell-5*h,dd)
    out["Dmenu:Z"]=5*uq-sh(ell,bg+p+1)
    out["Dmenu:C"]=sh(ell,bg+1)-sh(h,dd)-sh(j,bg+2)
    out["Dmenu:Q"]=sh(5*(ell-j),bg+1)+sh(j*j-5*h,dd)
    for name,z in zip("ABCDEUVWXY",b):
        out[f"Dmenu:fixed:{name}"]=sh(ell-5*z,bg+1)+sh(j*z-h,dd)
    for name,z in (("P",p),("Q",q)):
        out[f"Dmenu:new:{name}"]=sh(ell-5*z,bg+1)+sh(j*z-h,dd)
    for k,(path,positions) in enumerate(paths):
        total=sum(path)
        for pos in positions:
            out[f"old{k}:{pos}:Dmenu"]=5*sh(path[pos],total)-sh(ell,sum(path[:pos])+5-pos)
    for ri,oldbg in enumerate((a+bb+c,a+e+u,a+bb+e)):
        le,hh=atom["menus_lh"][ri]
        out[f"Dmenu:oldmenu:{ri}"]=sh(5*(ell-le),bg+1)+sh(j*le-5*h,dd)
        out[f"oldmenu{ri}:Dmenu"]=sh(5*(le-ell),oldbg+1)+sh(j*ell-5*hh,(oldbg+1)*(oldbg+2))
    for fam,offset in (("AB",a+bb),("AE",a+e)):
        r4=r5=F(0)
        for cnt,(t,r,s) in zip(atom[fam+"_hist"],THIRD):
            r4+=cnt*(5*sh(r,offset+t+r+s)-sh(ell,offset+t+2))
            r5+=cnt*(5*sh(s,offset+t+r+s)-sh(ell,offset+t+r+1))
        out[f"{fam}:4:Dmenu"],out[f"{fam}:5:Dmenu"]=r4,r5
        for bit,label in ((1,"R"),(2,"S")):
            count=sum(cnt*typ[bit] for cnt,typ in zip(atom[fam+"_hist"],THIRD))
            out[f"Dmenu:{fam}:{label}"]=sh(5*(ell-count),bg+1)+sh(j*count-5*h,dd)
    vals=[F(0)]*3
    for cnt,(t,h0,i,jj) in zip(atom["second_hist"],SECOND):
        den=a+t+h0+i+jj
        vals[0]+=cnt*(5*sh(h0,den)-sh(ell,a+t+3))
        vals[1]+=cnt*(5*sh(i,den)-sh(ell,a+t+h0+2))
        vals[2]+=cnt*(5*sh(jj,den)-sh(ell,a+t+h0+i+1))
    for position,value in enumerate(vals,3):out[f"second:{position}:Dmenu"]=value
    for bit,label in ((1,"H"),(2,"I"),(3,"J")):
        count=sum(cnt*typ[bit] for cnt,typ in zip(atom["second_hist"],SECOND))
        out[f"Dmenu:second:{label}"]=sh(5*(ell-count),bg+1)+sh(j*count-5*h,dd)
    return out


def main():
    primal=json.loads(SOURCE.read_text())["primal"]
    atoms=primal["atoms"]
    types=[]
    for k,atom in enumerate(atoms):
        j=sum(cnt*t for cnt,(t,r,s) in zip(atom["AB_hist"],THIRD))
        corners=set(((0,0),(j,j),(5-j,0),(5,j)))
        types.extend((k,p,q,ell,h) for p,q in itertools.product((0,1),repeat=2) for ell,h in sorted(corners))
    allrows=[rows(atoms[k],p,q,ell,h) for k,p,q,ell,h in types]
    names=list(allrows[0])
    coeff=np.array([[float(row[name]) for row in allrows] for name in names])
    eq=np.zeros((len(atoms),len(types)))
    for col,(k,p,q,ell,h) in enumerate(types):eq[k,col]=1
    masses=np.array([float(F(int(z["mass_numerator"]),int(primal["denominator"]))) for z in atoms])
    # Minimize the maximum violation t. Feasible extension iff optimum <=0.
    obj=np.zeros(len(types)+1);obj[-1]=1
    aeq=np.column_stack((eq,np.zeros(len(atoms))))
    aub=np.column_stack((-coeff,-np.ones(len(names))))
    result=linprog(obj,A_ub=aub,b_ub=np.zeros(len(names)),A_eq=aeq,b_eq=masses,
                   bounds=[(0,None)]*len(types)+[(None,None)],method="highs")
    out={"status":result.message,"row_count":len(names),"variable_count":len(types),
         "maximum_violation":float(result.fun) if result.success else None,
         "scope":"Targeted old-primal extension test only; no full SPE or positivity inference"}
    if result.success:
        out["active_rows"]=[names[k] for k,z in enumerate(result.ineqlin.marginals) if abs(z)>1e-8]
        out["nonzero_splits"]=[{"atom":k,"P":p,"Q":q,"ell":ell,"h":h,"mass":float(result.x[col])}
                               for col,(k,p,q,ell,h) in enumerate(types) if result.x[col]>1e-9]
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="nonzero_splits"},indent=2))


if __name__=="__main__":main()
