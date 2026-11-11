"""Arbitrary-horizon same-source requery, exact local and m6 row checks.
The final LP records are necessary-row relaxations, not genuine SPEs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json,sys
from stress_nested_on_old_relaxation import ROOT
WORK=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5'
sys.path.insert(0,str(WORK))
from six_copy_refine import bridge_system,parametric_row,add_query_family,solve_exact_system,verify,decode

def sh(n,d):return F(n,d) if n else F(0)

def value(k,p,ell,t,q,b,c,j,v,s,ss):
    return (sh(2*t-c,p+t+s+b+c)+sh(3*c-v,2*(p+c+ss+j+v))
            +F(b,2*(p+c+ss+j+1))+F(j,4*(ell+1))
            +F(5*v,12*(ell+1))+F(v,12)+F(q,p+t+s+b+1))

@lru_cache(None)
def phi(k,p,ell,t,q):
    return -min(value(k,p,ell,t,q,b,c,j,v,s,ss)
                for b,c,j,v in product((0,1),repeat=4)
                for s in range(k-2) for ss in range(k-2))

def literal(k,p,ell,t,q):
    vals=[]
    for first in product((0,1),repeat=k-1):
        for second in product((0,1),repeat=k-1):
            b,c=first[-2:];j,v=second[-2:]
            vals.append(value(k,p,ell,t,q,b,c,j,v,sum(first[:-2]),sum(second[:-2])))
    return -min(vals)

def system():
    types,rows=bridge_system(6)
    old=json.loads((WORK/'six_copy_free_results.json').read_text())
    for c in old['cuts']:rows.append(parametric_row(types,6,{k:v for k,v in c.items() if k!='separation_slack'}))
    oldn=decode(old['final'],types);diagnostics=[]
    for k in range(3,7):
        source=6-k
        def psi(a,t,q,k=k,source=source):return -F(2,7)*phi(k,sum(a[:source]),sum(a[:-1]),t,q)
        oldcount=len(rows)
        add_query_family(rows,types,6,f'nested-horizon-{k}',source,psi,F(1,42),((5,F(4,21)),))
        slacks=[sum(c*v for c,v in zip(row,oldn)) for _,row in rows[oldcount:]]
        diagnostics.append({'remaining':k,'source_provider':source+1,'new_rows':len(slacks),'negative_at_old_point':sum(s<0 for s in slacks),'minimum_normalized_slack':str(min(slacks))})
    return types,rows,diagnostics

if __name__=='__main__':
    target=Path(__file__).with_suffix('.json')
    if '--local' in sys.argv:
        checks=0
        for k in range(3,7):
            for p,ell,t,q in product(range(3),range(4),(0,1),(0,1)):
                assert phi(k,p,ell,t,q)==literal(k,p,ell,t,q);checks+=1
        print('EXACT compressed-vs-binary minima',checks)
    else:
        types,rows,diagnostics=system()
        if '--verify' in sys.argv:
            data=json.loads(target.read_text());verify(data['certificate'],types,rows);assert data['old_point_diagnostics']==diagnostics
            print('EXACT VERIFIED',data['certificate']['W'],len(rows),'rows; relaxation only')
        else:
            data,_=solve_exact_system(6,types,rows)
            target.write_text(json.dumps({'scope':'exact necessary-row relaxation, not SPE proof','old_point_diagnostics':diagnostics,'certificate':data},indent=2)+'\n')
            print(json.dumps({'diagnostics':diagnostics,'new_W_over_O':data['W'],'n_rows':len(rows)},indent=2))
