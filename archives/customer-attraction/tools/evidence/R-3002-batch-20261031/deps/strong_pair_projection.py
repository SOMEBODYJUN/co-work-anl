"""Source deviation with a jointly priced true terminal pair.
Necessary projected rows only; float discovery, exact Fraction cut verification.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import sys,json
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/three_certificate_comparison'
sys.path.insert(0,str(OLD))
from nested_horizon_refine import system
from six_copy_refine import decode,solve_exact_system,verify

def sh(n,d):return F(n,d) if n else F(0)

def specs():
    out=[('price',q) for q in ('middle','B','C')]+[('cap',q) for q in ('middle','B','C')]
    out += [('last',q) for q in list(range(6))+['avg']]
    out += [('pair',i,j) for i in range(6) for j in range(i,6)]
    out += [('pair',i,'avg') for i in range(6)]
    out += [('pair','diag'),('pair','off')]
    return out

@lru_cache(None)
def local(a,d,source,theme):
    k=6-source;t=a[theme];p=sum(a[:source]);ell=sum(a[:-1]);S=specs();out=[]
    for s,b,c in product(range(k-2),(0,1),(0,1)):
        z=p+t+s+b+c;background=p+t+s
        v=sh(t,z);last=sh(c,z)
        H=sh(b+c,z)+F(b,(background+1)*(background+2))
        def member(q):return F(d,6) if q=='avg' else F(a[q])
        costs=[]
        for spec in S:
            if spec[0]=='price':costs.append(F({'middle':s,'B':b,'C':c}[spec[1]],ell+1))
            elif spec[0]=='cap':costs.append(F({'middle':s,'B':b,'C':c}[spec[1]]))
            elif spec[0]=='last':costs.append(member(spec[1])/F(background+b+1)-last)
            elif spec[1]=='diag':costs.append(F(2*d,6*(background+1))-F(d,6*(background+1)*(background+2))-H)
            elif spec[1]=='off':costs.append(F(2*d,6*(background+1))-F(d*(d-1),30*(background+1)*(background+2))-H)
            else:
                qi,qj=member(spec[1]),member(spec[2])
                costs.append((qi+qj)/F(background+1)-qi*qj/F((background+1)*(background+2))-H)
        out.append(((s,b,c),v,tuple(costs)))
    return tuple(out)

def budgets(types,n,source):
    k=6-source
    last=sum(mass*sh(a[-1],sum(a)) for (a,d),mass in zip(types,n[:-1]))
    K=n[-1]
    b=[]
    for spec in specs():
        if spec[0]=='price':b.append((k-3 if spec[1]=='middle' else 1)*last)
        elif spec[0]=='cap':b.append((k-3 if spec[1]=='middle' else 1)*K)
        else:b.append(F(0))
    return b

def row(types,cut):
    source,theme=cut['source'],cut['theme'];alpha=list(map(F,cut['alpha']))
    k=6-source
    pu=sum(v*(k-3 if sp[1]=='middle' else 1) for sp,v in zip(specs(),alpha) if sp[0]=='price')
    pk=sum(v*(k-3 if sp[1]=='middle' else 1) for sp,v in zip(specs(),alpha) if sp[0]=='cap')
    coeff=[]
    for a,d in types:
        rhs=min(v+sum(x*y for x,y in zip(alpha,costs)) for option,v,costs in local(a,d,source,theme))
        coeff.append(sh(a[source],sum(a))+pu*sh(a[-1],sum(a))-rhs)
    coeff.append(pk)
    return 'source-pair:'+json.dumps(cut,sort_keys=True,separators=(',',':')),coeff

def separate(types,n):
    cuts=[];report=[]
    for source in range(4):
        for theme in range(6):
            groups=[(a,d,mass) for (a,d),mass in zip(types,n[:-1]) if mass]
            options=[local(a,d,source,theme) for a,d,mass in groups]
            flat=[(gi,option,v,cs) for gi,opts in enumerate(options) for option,v,cs in opts]
            b=budgets(types,n,source)
            eq=np.zeros((len(groups),len(flat)))
            for j,(gi,option,v,cs) in enumerate(flat):eq[gi,j]=1
            sol=linprog([float(v) for gi,option,v,cs in flat],A_ub=np.array([[float(cs[i]) for gi,option,v,cs in flat] for i in range(len(b))]),b_ub=list(map(float,b)),A_eq=eq,b_eq=[float(mass) for a,d,mass in groups],bounds=(0,None),method='highs')
            u=sum(mass*sh(a[source],sum(a)) for a,d,mass in groups)
            report.append({'source':source+1,'theme':theme+1,'status':sol.status,'gap':None if not sol.success else sol.fun-float(u)})
            if sol.success and sol.fun>float(u)+1e-8:
                alpha=[F(float(-v)).limit_denominator(10**7) for v in sol.ineqlin.marginals]
                assert min(alpha)>=0
                cut={'source':source,'theme':theme,'alpha':list(map(str,alpha))}
                name,coeff=row(types,cut)
                slack=sum(x*y for x,y in zip(coeff,n));assert slack<0,(source,theme,slack)
                cut['separation_slack']=str(slack);cuts.append(cut)
    return cuts,report

if __name__=='__main__':
    target=Path(__file__).with_suffix('.json')
    types,rows,diags=system()
    baseline=json.loads((OLD/'nested_horizon_refine.json').read_text())['certificate']
    if '--verify' in sys.argv:
        data=json.loads(target.read_text())
        for cut in data['cuts']:
            raw={k:v for k,v in cut.items() if k!='separation_slack'};rows.append(row(types,raw))
        verify(data['certificate'],types,rows);print('EXACT VERIFIED',data['certificate']['W'],len(rows),'rows')
    else:
        n=decode(baseline,types);allcuts=[];records=[];result=baseline
        for step in range(6):
            cuts,report=separate(types,n)
            print('STEP',step,'W',result['W'],'cuts',len(cuts),'maxgap',max((q['gap'] or 0) for q in report),flush=True)
            records.append({'step':step,'report':report,'W':result['W']})
            if not cuts:break
            for cut in cuts:
                raw={k:v for k,v in cut.items() if k!='separation_slack'};rows.append(row(types,raw))
            allcuts.extend(cuts)
            result,n=solve_exact_system(6,types,rows)
            target.write_text(json.dumps({'scope':'necessary conditions only, not SPE','cuts':allcuts,'records':records,'certificate':result},indent=2)+'\n')
        target.write_text(json.dumps({'scope':'necessary conditions only, not SPE','cuts':allcuts,'records':records,'certificate':result},indent=2)+'\n')
