"""Round discovery coefficients safely, then exact-check every root-copy type.

Uniformly increasing all CAP multipliers pays any roundoff on M=0 states.
An upward correction to the K coefficient pays M=1 states. This turns the
floating discovery into explicit exact nonnegative customerwise identities.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from root_copy_lp import solve,data

def export(n=6):
    found=solve(n)
    names,mat,root,mc=data(n,exact=True)
    capidx=[j for j,name in enumerate(names) if name.startswith('CAP:')]
    oidx=[j for j,name in enumerate(names) if name.endswith('O')]
    out=[]
    for original in found['bounds'][:4]:
        den=10**8
        coeff=[F(round(original.get('active',{}).get(name,0)*den),den) for name in names]
        coeff[names.index('P0:lastO')]+=1-sum(coeff[j] for j in oidx)
        assert min(coeff)>=0
        B=F(round(original['B']*den),den);C=F(round(original['C']*den),den)
        dots=[sum(q*a for q,a in zip(coeff,row))-B*r-C*m for row,r,m in zip(mat,root,mc)]
        correction=max([F(0)]+[v/(-sum(row[j] for j in capidx)) for row,m,v in zip(mat,mc,dots) if not m and v>0])
        for j in capidx:coeff[j]+=correction
        C+=len(capidx)*correction
        dots=[sum(q*a for q,a in zip(coeff,row))-B*r-C*m for row,r,m in zip(mat,root,mc)]
        C+=max([F(0)]+[v for v,m in zip(dots,mc) if m])
        residuals=[B*r+C*m-sum(q*a for q,a in zip(coeff,row)) for row,r,m in zip(mat,root,mc)]
        assert min(residuals)>=0
        assert sum(coeff[j] for j in oidx)==1
        out.append({'discovery_r_over_K':original['r_over_K'],'B':str(B),'C':str(C),'B_decimal':float(B),'C_decimal':float(C),'multipliers':{name:str(q) for name,q in zip(names,coeff) if q},'coefficient_states':len(mat),'minimum_residual':str(min(residuals)),'zero_count':sum(q==0 for q in residuals)})
    return {'status':'EXACT_LOCAL_ROOT_LINES_ONLY','n':n,'claim':'For every full-history pure SPE and arbitrary six-comparison union O, O <= B*u1 + C*K for each listed line. K is the common maximum cardinality. This does not prove half.','lines':out}

if __name__=='__main__':
    obj=export()
    path=Path(__file__).with_name('root_lines_certificate_v2.json')
    if path.exists():raise FileExistsError(path)
    path.write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='lines'},indent=2))
    print(json.dumps([{k:v for k,v in row.items() if k!='multipliers'} for row in obj['lines']],indent=2))
