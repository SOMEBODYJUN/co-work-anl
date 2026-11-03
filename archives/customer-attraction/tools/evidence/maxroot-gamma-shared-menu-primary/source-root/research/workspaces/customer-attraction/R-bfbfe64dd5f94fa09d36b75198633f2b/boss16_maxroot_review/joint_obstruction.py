"""Exact separation for a specified actual/maxroot necessary-condition family.

The 6144-type cone is a relaxation. Its primal points are not game instances,
not SPE, and not a disproof of HALF(5). It tests only this explicit row family.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,numpy as np
from scipy.optimize import linprog
import envelope as e
HERE=Path(__file__).resolve().parent
JP=HERE.parents[1]/'R-d3981c0168644971803a9c3380ed687c'/'round8_five'/'maxroot'/'joint_paths.py'
spec=importlib.util.spec_from_file_location('legacy_joint_paths',JP);j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
ATOMS=list(product(list(product((0,1),repeat=10)),range(6)))
PATHS=(tuple(range(5)),tuple(range(5,10)))
WEIGHTED=((F(80),F(71,5)),(F(70),F(423,35)),(F(1920,29),F(11393,1015)),(F(5840,91),F(2627,245)))
INTEGER_SUPPORT=(
    ('0000000000',10),('0000000001',3),('0000000010',3),('0000000100',1),
    ('0000100000',2),('0000111100',3),('0001000000',3),('0001100000',1),
    ('0010000000',1),('1011011011',1),('1110000001',2),('1110011110',3))
def rows(b,d):
    out=j.rows(b,d)
    for tag,path in enumerate(PATHS):
        p=sum(b[z] for z in path[:2]);u=e.q(b[path[2]],sum(b[z] for z in path))
        for z in range(10):out[f'TrueH:{tag}:repeat:{z}']=17040*u+1085*b[5]-e.q(13395*b[z],p+3)-e.FT[p][d]
        out[f'TrueH:{tag}:opt']=17040*u+1085*b[5]-e.q(2679*d,p+3)-e.FT[p][d]
    r=e.q(b[0],sum(b[:5]));K=b[5];O=int(d>0)
    for i,(B,C) in enumerate(WEIGHTED):out[f'weighted_root:{i}']=B*r-C*K-O
    return out

def recover_support(cols,names,weights,atoms):
    # Tight rational equations reconstruct a basic point from float support.
    tight=[n for n in names if abs(sum(c[n]*float(w) for c,w in zip(cols,weights)))<1e-7]
    A=[[c[n] for c in cols] for n in tight];rhs=[F()]*len(A)
    A.append([F(any(b[:5])) for b,d in atoms]);rhs.append(F(1))
    masses=e.exact_solve(A,rhs,weights)
    assert min(masses)>=0
    slacks={n:sum((c[n]*w for c,w in zip(cols,masses)),F()) for n in names}
    assert min(slacks.values())>=0
    return masses,slacks

def run():
    names=list(rows(*ATOMS[0]));cols=[]
    for a in ATOMS:cols.append([float(z) for z in rows(*a).values()])
    mat=np.array(cols).T;W=np.array([any(b[:5]) for b,d in ATOMS],float);O=np.array([d>0 for b,d in ATOMS],float)
    ans=linprog(-O,A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs');assert ans.success,ans.message
    support=[i for i,w in enumerate(ans.x) if w>1e-8];ats=[ATOMS[i] for i in support]
    cc=[rows(*a) for a in ats];weights=[float(ans.x[i]) for i in support]
    masses,slacks=recover_support(cc,names,weights,ats)
    oo=sum((w*int(d>0) for w,(b,d) in zip(masses,ats)),F());ww=sum((w*int(any(b[:5])) for w,(b,d) in zip(masses,ats)),F());assert ww==1 and oo>2
    out={'scope':__doc__,'source_joint_paths':str(JP),'rows':len(names),'domain_atoms':len(ATOMS),'row_names':names,
         'W':str(ww),'O':str(oo),'O_minus_2W':str(oo-2*ww),'minimum_slack':str(min(slacks.values())),
         'atoms':[{'bits':list(b),'d':d,'mass':str(w)} for (b,d),w in zip(ats,masses)],
         'slacks':{n:str(w) for n,w in slacks.items()}}
    HERE.joinpath('joint_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
    # A small exact integer point was recovered separately by MILP on the above
    # rational support; reproduction requires no MILP and no floating arithmetic.
    integer_atoms=[(tuple(map(int,b)),1,F(m)) for b,m in INTEGER_SUPPORT]
    slacks={n:sum((m*rows(b,d)[n] for b,d,m in integer_atoms),F()) for n in names}
    iw=sum((m*int(any(b[:5])) for b,d,m in integer_atoms),F());io=sum((m*int(d>0) for b,d,m in integer_atoms),F())
    assert iw==16 and io==33 and min(slacks.values())>=0
    integer={'scope':__doc__,'source_joint_paths':str(JP),'rows':len(names),'domain_atoms':len(ATOMS),
             'W':str(iw),'O':str(io),'O_minus_2W':str(io-2*iw),'minimum_slack':str(min(slacks.values())),
             'atoms':[{'bits':list(b),'d':d,'mass':str(m)} for b,d,m in integer_atoms],
             'slacks':{n:str(w) for n,w in slacks.items()}}
    HERE.joinpath('joint_obstruction_integer.json').write_text(json.dumps(integer,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('row_names','atoms','slacks')},indent=2))

if __name__=='__main__':run()
