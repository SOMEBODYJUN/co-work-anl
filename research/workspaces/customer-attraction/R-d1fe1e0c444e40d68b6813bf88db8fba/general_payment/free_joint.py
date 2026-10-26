"""Free joint same-source projection; local necessary rows, never SPE proof.

This extends the fixed seven-row requery with arbitrary nonnegative weights,
both terminal query menus, all four common terminal prices/capacities, and
penultimate safe-query menus. Hidden intermediate replies are retained by
their two count variables; all source comparisons refer to the same history.
"""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8'
sys.path[:0]=[str(OLD/'general_from_half5'),str(OLD/'three_certificate_comparison')]
from six_copy_refine import decode,verify
from six_stress import exact_solve
from nested_horizon_refine import system
from stress_nested_on_old_relaxation import query_distribution

def sh(n,d): return F(n,d) if n else F(0)

NAMES=['sourceT','sourceC']
NAMES += ['price:'+x for x in 'bcjv']
NAMES += ['cap:'+x for x in 'bcjv']
NAMES += ['last1:'+x for x in 'tqbjv']
NAMES += ['last2:'+x for x in 'tqbcj']
NAMES += ['safeB:'+x for x in 'tqcjv']
NAMES += ['safeJ:'+x for x in 'tqbcv']
# The preceding middle replies, if present, are uniformly priced/capped.
NAMES += ['price:s','price:ss','cap:s','cap:ss']
NAMES=tuple(NAMES)

@lru_cache(None)
def states(k,p,ell,t,q):
    result=[]
    for b,c,j,v in product((0,1),repeat=4):
        for s,ss in product(range(k-2),repeat=2):
            z1=p+t+s+b+c;z2=p+c+ss+j+v
            mem=dict(t=t,q=q,b=b,c=c,j=j,v=v)
            vals={'sourceT':sh(t,z1),'sourceC':sh(c,z2)}
            vals.update({'price:'+x:F(mem[x],ell+1) for x in 'bcjv'})
            vals.update({'cap:'+x:F(mem[x]) for x in 'bcjv'})
            vals.update({'last1:'+x:F(mem[x],p+t+s+b+1)-sh(c,z1) for x in 'tqbjv'})
            vals.update({'last2:'+x:F(mem[x],p+c+ss+j+1)-sh(v,z2) for x in 'tqbcj'})
            vals.update({'safeB:'+x:F(mem[x],p+t+s+2)-sh(b,z1) for x in 'tqcjv'})
            vals.update({'safeJ:'+x:F(mem[x],p+c+ss+2)-sh(j,z2) for x in 'tqbcv'})
            vals.update({'price:s':F(s,ell+1),'price:ss':F(ss,ell+1),'cap:s':F(s),'cap:ss':F(ss)})
            result.append(tuple(vals[x] for x in NAMES))
    return tuple(result)

def costs(k,ur,um,K):
    return tuple(ur if x.startswith('source') else
                 um*((k-3) if x in ('price:s','price:ss') else 1) if x.startswith('price:') else
                 K*((k-3) if x in ('cap:s','cap:ss') else 1) if x.startswith('cap:') else F(0)
                 for x in NAMES)

def weight_map(cut): return tuple(F(cut['weights'].get(x,'0')) for x in NAMES)

def make_row(types,m,cut):
    k=cut['k'];source=m-k;ti=cut['T'];qi=cut['Q'];weights=weight_map(cut)
    @lru_cache(None)
    def credit(p,ell,t,q):
        return min(sum(w*c for w,c in zip(weights,state)) for state in states(k,p,ell,t,q))
    uc=weights[0]+weights[1]
    pc=sum(w*((k-3) if x in ('price:s','price:ss') else 1) for w,x in zip(weights,NAMES) if x.startswith('price:'))
    kc=sum(w*((k-3) if x in ('cap:s','cap:ss') else 1) for w,x in zip(weights,NAMES) if x.startswith('cap:'))
    row=[]
    for a,d in types:
        val=uc*sh(a[source],sum(a))+pc*sh(a[-1],sum(a))
        val-=sum(prob*credit(sum(a[:source]),sum(a[:-1]),t,q) for prob,t,q in query_distribution(a,d,ti,qi))
        row.append(val)
    name='freejoint:'+json.dumps(cut,separators=(',',':'),sort_keys=True)
    return name,row+[kc]

def separate(types,m,n,k,queries=None):
    import numpy as np
    from scipy.optimize import linprog
    source=m-k;ur=sum(sh(a[source],sum(a))*v for (a,d),v in zip(types,n[:-1]));um=sum(sh(a[-1],sum(a))*v for (a,d),v in zip(types,n[:-1]));K=n[-1]
    cost=costs(k,ur,um,K);P=len(NAMES)
    queries=queries or ([(i,j) for i in range(m) for j in range(m)]+[(i,'avg') for i in range(m)]+[('avg',i) for i in range(m)]+[('diag','diag'),('off','off')])
    cuts=[];diagnostics=[]
    for ti,qi in queries:
        grouped={}
        for (a,d),v in zip(types,n[:-1]):
            if not v:continue
            for prob,t,q in query_distribution(a,d,ti,qi):
                if prob:
                    key=(sum(a[:source]),sum(a[:-1]),t,q)
                    grouped[key]=grouped.get(key,F(0))+prob*v
        groups=list(grouped);G=len(groups)
        count=sum(len(states(k,*group)) for group in groups)
        A=np.zeros((count+1,P+G));ix=0
        for gi,group in enumerate(groups):
            for state in states(k,*group):
                A[ix,:P]=[-float(z) for z in state];A[ix,P+gi]=1;ix+=1
        A[-1,:P]=1
        c=[float(x) for x in cost]+[-float(grouped[g]) for g in groups]
        sol=linprog(c,A_ub=A,b_ub=[0.]*count+[1.],bounds=[(0,None)]*P+[(None,None)]*G,method='highs')
        assert sol.success,sol.message
        diagnostics.append({'k':k,'T':ti,'Q':qi,'minimum_slack_float':float(sol.fun)})
        if sol.fun < -1e-8:
            weights=[F(float(x)).limit_denominator(1000000) for x in sol.x[:P]]
            assert min(weights)>=0
            cut={'k':k,'T':ti,'Q':qi,'weights':{x:str(w) for x,w in zip(NAMES,weights) if w}}
            name,row=make_row(types,m,cut)
            slack=sum(x*y for x,y in zip(row,n))
            assert slack<0,(cut,slack,sol.fun)
            cut['at_input_slack']=str(slack);cuts.append(cut)
    return cuts,diagnostics

def rawcut(cut):return {k:v for k,v in cut.items() if k not in ('at_input_slack','rounding_grid')}

def solve_exact_system(m,types,rows):
    import numpy as np
    from scipy.optimize import linprog
    w=[int(any(a)) for a,d in types]+[0];o=[int(d>0) for a,d in types]+[0]
    mat=np.array([[float(v) for v in row] for _,row in rows])
    sol=linprog(w,A_ub=-mat,b_ub=np.zeros(len(rows)),A_eq=[o],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    assert sol.success,sol.message
    for tol in (1e-9,1e-10,1e-11,1e-12,1e-8):
        stage='primal'
        try:
            support=[j for j,x in enumerate(sol.x) if x>tol]
            active=[i for i,row in enumerate(mat) if abs(row@sol.x)<tol]
            eqs=[[rows[i][1][j] for j in support]+[F(0)] for i in active]+[[F(o[j]) for j in support]+[F(1)]]
            exact=exact_solve(eqs,len(support));n=[F(0)]*len(sol.x)
            for j,v in zip(support,exact):n[j]=v
            assert min(n)>=0
            slacks=[sum(c*x for c,x in zip(row,n)) for _,row in rows]
            assert min(slacks)>=0
            val=sum(F(x)*y for x,y in zip(w,n))
            stage='dual'
            ds=[i for i,x in enumerate(sol.ineqlin.marginals) if x < -tol]
            eqs=[[rows[i][1][j] for i in ds]+[F(o[j]),F(w[j])] for j in support]
            dual=exact_solve(eqs,len(ds)+1)
            assert min(dual[:-1])>=0 and dual[-1]==val
            residual=[F(w[j])-val*o[j]-sum(v*rows[i][1][j] for i,v in zip(ds,dual)) for j in range(len(n))]
            assert min(residual)>=0
            result={'m':m,'n_types':len(types),'n_rows':len(rows),'W':str(val),'O':'1','K':str(n[-1]),'support':[{'actual_bits':''.join(map(str,a)),'d':d,'weight':str(n[j])} for j,(a,d) in enumerate(types) if n[j]],'min_slack':str(min(slacks)),'dual':{rows[i][0]:str(v) for i,v in zip(ds,dual)},'dual_nu':str(val),'dual_min_residual':str(min(residual))}
            return result,n
        except AssertionError:
            print('recovery tolerance failed',tol,stage,flush=True)
    raise RuntimeError('exact reconstruction failed; floating optimum '+str(sol.fun))

if __name__=='__main__':
    target=Path(__file__).with_suffix('.json')
    types,rows,_=system();m=6
    if '--verify' in sys.argv:
        data=json.loads(target.read_text())
        for cut in data['cuts']: rows.append(make_row(types,m,rawcut(cut)))
        verify(data['final'],types,rows)
        print('EXACT VERIFIED',data['final']['W'],len(rows),'rows; necessary relaxation only')
    else:
        base=json.loads((OLD/'three_certificate_comparison/nested_horizon_refine.json').read_text())['certificate']
        n=decode(base,types);allcuts=[];records=[]
        for step in range(12):
            cuts=[];diagnostics=[]
            for k in (3,4,5,6):
                new,diag=separate(types,m,n,k);cuts+=new;diagnostics+=diag
            records.append({'step':step,'W':base['W'],'n_rows':len(rows),'n_cuts':len(cuts),'diagnostics':diagnostics})
            print('JOINT',step,base['W'],float(F(base['W'])),len(cuts),'cuts',flush=True)
            if not cuts:break
            for cut in cuts:
                row=make_row(types,m,rawcut(cut))
                assert row[0] not in {name for name,_ in rows}
                rows.append(row);allcuts.append(cut)
            target.write_text(json.dumps({'scope':'necessary-row relaxation, not SPE proof','cuts':allcuts,'rounds':records,'input':base},indent=2)+'\n')
            base,n=solve_exact_system(m,types,rows)
            target.write_text(json.dumps({'scope':'necessary-row relaxation, not SPE proof','cuts':allcuts,'rounds':records,'final':base},indent=2)+'\n')
        target.write_text(json.dumps({'scope':'necessary-row relaxation, not SPE proof','cuts':allcuts,'rounds':records,'final':base},indent=2)+'\n')
