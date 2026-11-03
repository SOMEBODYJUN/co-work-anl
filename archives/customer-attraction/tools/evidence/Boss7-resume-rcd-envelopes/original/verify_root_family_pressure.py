"""Recover and check one exact >2 point for the named 107-row relaxation.

This audits the row coefficients, not original-SPE realizability. It does not
claim a full-universe dual or an optimal relaxation constant.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from root_family_pressure import col

HERE=Path(__file__).resolve().parent

def eliminate(rows,rhs=None):
    a=[list(map(F,row))+([F(rhs[i])] if rhs is not None else []) for i,row in enumerate(rows)]
    n=len(rows[0]);r=0;piv=[]
    for c in range(n):
        at=next((i for i in range(r,len(a)) if a[i][c]),None)
        if at is None:continue
        a[r],a[at]=a[at],a[r];d=a[r][c];a[r]=[x/d for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                d=a[i][c];a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        piv.append(c);r+=1
        if r==len(a):break
    return r,a,piv
def main():
    src=json.loads((HERE/'root_family_pressure_discovery.json').read_text())
    atoms=src['atoms']; rows=[]; ws=[];os=[]
    for z in atoms:
        rr,w,o,names=col(z['actual'],z['opt_multiplicity'],z['root_if_t1'],z['root_if_t0'])
        rows.append(list(map(F,rr)));ws.append(F(w));os.append(F(o))
    mat=list(map(list,zip(*rows))); n=len(atoms)
    # Add numerically tight rows until the support coordinates are determined.
    floats=[z['mass_float'] for z in atoms]
    order=sorted(range(len(mat)),key=lambda i:abs(sum(float(a)*b for a,b in zip(mat[i],floats))))
    eq=[ws]; ids=[];rank=1
    for i in order:
        if abs(sum(float(a)*b for a,b in zip(mat[i],floats)))>1e-7:break
        nr=eliminate(eq+[mat[i]])[0]
        if nr>rank:eq.append(mat[i]);ids.append(i);rank=nr
        if rank==n:break
    assert rank==n,(rank,n)
    _,reduced,piv=eliminate(eq,[1]+[0]*(n-1))
    assert piv==list(range(n))
    mass=[row[-1] for row in reduced]
    slacks=[sum(a*b for a,b in zip(row,mass)) for row in mat]
    assert min(mass)>0 and min(slacks)>=0
    W=sum(a*b for a,b in zip(ws,mass));O=sum(a*b for a,b in zip(os,mass))
    assert W==1 and O>2
    out={'scope':'Exact feasible point only for the named 107-row affine relaxation; not an original game or SPE',
      'rows':len(mat),'atoms':n,'W':str(W),'O':str(O),'O_minus_2W':str(O-2*W),
      'min_row_slack':str(min(slacks)),
      'selected_zero_rows':[names[i] for i in ids],
      'point':[{**{k:v for k,v in z.items() if k!='mass_float'},'mass':str(v)} for z,v in zip(atoms,mass)],
      'slacks':{name:str(s) for name,s in zip(names,slacks)}}
    (HERE/'root_family_pressure_exact.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('point','slacks','selected_zero_rows')},indent=2))

if __name__=='__main__':main()
