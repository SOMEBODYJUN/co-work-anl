"""Recover an exact >2 primal for exactly the joint_paths.py row template.

This is a template obstruction, never a complete-history SPE counterexample.
Uses the discovery row generator only to identify this specified template;
all inequalities are subsequently checked with Fraction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
import json,hashlib
import joint_paths as j

def old234(bits,d):
    """Exact reconstruction of the cited earlier 234-row source."""
    r={};pays=[]
    for tag,path,start in [('actual',range(5),0),('maxroot',range(5,10),1)]:
        path=list(path);load=sum(bits[z] for z in path);u=[j.q(bits[z],load) for z in path];pays.append(u)
        for pos in range(start,5):
            p=sum(bits[z] for z in path[:pos]);k=5-pos
            for z in range(10):r[f'{tag}:node{pos+1}:floor{z}']=u[pos]-F(bits[z],p+k)
            r[f'{tag}:node{pos+1}:sumopt']=5*u[pos]-F(d,p+k)
            if k in (2,3,4):
                comp=sum((comb(d,count)*comb(5-d,k-count)*F(count,p+count) for count in range(1,k+1) if count<=d and 0<=k-count<=5-d),F(0))
                beta={2:F(3,2),3:F(5,3),4:F(1499,750)}[k]
                r[f'{tag}:tail{k}:opt_profit']=comb(5,k)*beta*sum(u[pos:])-comp
            if k==2:
                H=sum(u[pos:])+F(bits[path[pos]],(p+1)*(p+2))
                r[f'{tag}:tail2:exact_tax_opt']=10*H-comp
                for a,b in combinations_with_replacement(range(10),2):
                    c=bits[a]+bits[b];r[f'{tag}:tail2:exact_tax{a},{b}']=H-j.q(c,p+c)
    r['root_IC_max']=pays[0][0]-pays[1][0]
    for z in range(10):r[f'max_size{z}']=F(bits[5]-bits[z])
    r['max_size_opt_average']=5*F(bits[5])-d
    for i in range(5):r[f'actual{i+1}:global_size_cap']=5*pays[0][i]-bits[5]
    assert len(r)==234
    return r

def exact_unique(A,y):
    m=[list(map(F,a))+[F(b)] for a,b in zip(A,y)];n=len(A[0]);r=0;piv=[]
    for k in range(n):
        i=next((i for i in range(r,len(m)) if m[i][k]),None)
        if i is None:continue
        m[r],m[i]=m[i],m[r];z=m[r][k];m[r]=[x/z for x in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][k]:
                z=m[i][k];m[i]=[x-z*y for x,y in zip(m[i],m[r])]
        piv.append(k);r+=1
    assert len(piv)==n,'support equations not unique'
    assert all(any(row[:n]) or row[n]==0 for row in m)
    return [m[piv.index(k)][n] for k in range(n)]

def run():
    here=Path(__file__).resolve().parent; raw=json.loads(here.joinpath('joint_paths.json').read_text());s=raw['support']
    cols=[j.rows(tuple(t['bits']),t['d']) for t in s];names=list(cols[0]);guess=[t['mass'] for t in s]
    tight=[n for n in names if abs(sum(c[n]*g for c,g in zip(cols,guess)))<1e-7]
    A=[[c[n] for c in cols] for n in tight]
    rhs=[0]*len(A); A.append([int(any(t['bits'][:5])) for t in s]);rhs.append(1)
    masses=exact_unique(A,rhs);assert min(masses)>=0
    slacks={n:sum(c[n]*g for c,g in zip(cols,masses)) for n in names};assert min(slacks.values())>=0
    O=sum(m*int(t['d']>0) for t,m in zip(s,masses));W=sum(m*int(any(t['bits'][:5])) for t,m in zip(s,masses));assert W==1 and O>2
    old=[old234(tuple(t['bits']),t['d']) for t in s];os={n:sum(c[n]*g for c,g in zip(old,masses)) for n in old[0]};assert min(os.values())>=0
    out={'status':'exact-template-obstruction','scope':__doc__,'template_sha256':hashlib.sha256(here.joinpath('joint_paths.py').read_bytes()).hexdigest(),'old_source':'R-cd789330fc7141299ac491bbb3ffa420/round13/parent/max_root_actual_pressure.py/json','old234_minimum_slack':str(min(os.values())),'old234_tight_rows':sum(x==0 for x in os.values()),'rows':len(names),'W':str(W),'O':str(O),'O_minus_2W':str(O-2),'minimum_slack':str(min(slacks.values())),'tight_rows':sum(x==0 for x in slacks.values()),'atoms':[dict(bits=t['bits'],d=t['d'],mass=str(m)) for t,m in zip(s,masses)],'slacks':{n:str(x) for n,x in slacks.items()},'old234_slacks':{n:str(x) for n,x in os.items()}}
    here.joinpath('exact_template_obstruction.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('atoms','slacks','old234_slacks')},indent=2))
if __name__=='__main__':run()
