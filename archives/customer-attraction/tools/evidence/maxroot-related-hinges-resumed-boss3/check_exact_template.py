"""Definition-level Fraction check of the saved 29-atom point, not an LP run.

Both row banks are rebuilt here from terminal shares, subset counts and tax.
No legacy program, optimizer, or strategy evaluator is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
import hashlib,json
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
PREFIX='research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/maxroot'
SRC=HERE/'original'/PREFIX
def q(a,b):return F(a,b) if a else F(0)
def choose(n,k):return comb(n,k) if 0<=k<=n else 0
def subsets(p,d,k):return sum((choose(d,j)*choose(5-d,k-j)*q(j,p+j) for j in range(1,k+1)),F(0))
def row_banks(bits,d):
    new={};old={};pu=[]
    for pi,(tag,path,start) in enumerate([('actual',range(5),0),('maxroot',range(5,10),1)]):
        path=list(path);u=[q(bits[j],sum(bits[z] for z in path)) for j in path];pu.append(u)
        for pos in range(start,5):
            p=sum(bits[j] for j in path[:pos]);k=5-pos
            for j in range(10):
                v=u[pos]-q(bits[j],p+k)
                new[f'{pi}:IC:{pos}:{j}']=v;old[f'{tag}:node{pos+1}:floor{j}']=v
            v=5*u[pos]-q(d,p+k)
            new[f'{pi}:opt:{pos}']=v;old[f'{tag}:node{pos+1}:sumopt']=v
            new[f'{pi}:O:{pos}']=5*k*u[pos]+q(p,p+k)-int(d>0)
            if k in (2,3,4):
                old[f'{tag}:tail{k}:opt_profit']=comb(5,k)*{2:F(3,2),3:F(5,3),4:F(1499,750)}[k]*sum(u[pos:])-subsets(p,d,k)
        p=sum(bits[j] for j in path[:3]);H=sum(u[3:])+q(bits[path[3]],(p+1)*(p+2))
        new[f'{pi}:r2:O']=F(5,2)*H+q(p,p+1)-int(d>0)
        v=10*H-subsets(p,d,2)
        new[f'{pi}:r2:opt']=v;old[f'{tag}:tail2:exact_tax_opt']=v
        for a,b in combinations_with_replacement(range(10),2):
            v=H-q(bits[a]+bits[b],p+bits[a]+bits[b])
            new[f'{pi}:r2:pair:{a}:{b}']=v;old[f'{tag}:tail2:exact_tax{a},{b}']=v
        p3=sum(bits[j] for j in path[:2]);p4=bits[path[0]]
        new[f'{pi}:r3:opt']=50*sum(u[2:])-3*subsets(p3,d,3)
        new[f'{pi}:r4:opt']=7495*sum(u[1:])-750*subsets(p4,d,4)
        new[f'{pi}:r4:binary']=29985*sum(u[1:])-4985*(p4-u[0])-3000*subsets(p4,d,4)
    new['root-to-max']=old['root_IC_max']=pu[0][0]-pu[1][0]
    for j in range(10):new[f'max-size:{j}']=old[f'max_size{j}']=F(bits[5]-bits[j])
    new['max-size:opt']=old['max_size_opt_average']=F(5*bits[5]-d)
    for i in range(5):old[f'actual{i+1}:global_size_cap']=5*pu[0][i]-bits[5]
    assert len(new)==240 and len(old)==234
    return new,old
def rank(A):
    m=[list(map(F,r)) for r in A];i=0
    for j in range(len(m[0])):
        z=next((z for z in range(i,len(m)) if m[z][j]),None)
        if z is None:continue
        m[i],m[z]=m[z],m[i];a=m[i][j];m[i]=[v/a for v in m[i]]
        for z in range(i+1,len(m)):
            a=m[z][j]
            if a:m[z]=[v-a*w for v,w in zip(m[z],m[i])]
        i+=1
    return i
def run():
    raw=json.loads((SRC/'exact_template_obstruction.json').read_text());atoms=raw['atoms']
    masses=[F(a['mass']) for a in atoms];banks=[row_banks(a['bits'],a['d']) for a in atoms]
    results=[]
    for k,field in [(0,'slacks'),(1,'old234_slacks')]:
        names=list(banks[0][k]);assert set(names)==set(raw[field])
        sl={n:sum((m*b[k][n] for m,b in zip(masses,banks)),F(0)) for n in names}
        assert sl=={n:F(v) for n,v in raw[field].items()} and min(sl.values())>=0
        results.append(dict(rows=len(sl),all_saved_slacks_equal=True,minimum=str(min(sl.values())),tight=sum(v==0 for v in sl.values())))
    W=sum((m*int(any(a['bits'][:5])) for a,m in zip(atoms,masses)),F(0))
    O=sum((m*int(a['d']>0) for a,m in zip(atoms,masses)),F(0))
    assert W==1 and O==F(raw['O']) and O-2*W==F(raw['O_minus_2W'])>0
    tight=[n for n in banks[0][0] if F(raw['slacks'][n])==0]
    matrix=[[b[0][n] for b in banks] for n in tight]+[[int(any(a['bits'][:5])) for a in atoms]]
    rr=rank(matrix);assert rr==len(atoms)==29
    template=SRC/'joint_paths.py'
    assert hashlib.sha256(template.read_bytes()).hexdigest()==raw['template_sha256']
    out=dict(status='PASS_NEW_DEFINITION_LEVEL_EXACT_TEMPLATE_POINT',atoms=29,coefficient_evaluations=29*(240+234),
             W=str(W),O=str(O),O_minus_2W=str(O-2*W),banks=results,
             tight_equations_with_W_rank=rr,template_source_sha_matches=True,
             boundary='Specified 240/234 row banks only; no matching dual, LP optimum, actual OPT or complete SPE claim')
    (HERE/'exact-template-definition-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
