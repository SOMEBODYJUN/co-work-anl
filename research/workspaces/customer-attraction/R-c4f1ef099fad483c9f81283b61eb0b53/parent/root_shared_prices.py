"""Price the full two-copy maximum-root graph by actual-prefix and pair IC.

This explores a larger true-query graph than the old support-restricted priced
envelope. Floating optimization only; a cut is accepted only after integer
projection and Fraction evaluation. All hidden assignments are priced each step.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,sys
import numpy as np
from scipy.optimize import linprog
import mixed_pair as mix

HERE=Path(__file__).resolve().parent
OLD=mix.OLD
sp=importlib.util.spec_from_file_location('root_discover',OLD/'six_maxroot/discover.py')
rd=importlib.util.module_from_spec(sp);sp.loader.exec_module(rd)
bits,paths,names,base,ocoef,vt=rd.build(6,2)
BITS=bits.astype(np.int64)
BASE=np.rint(60*base).astype(np.int64).T
assert np.max(np.abs(BASE.T/60-base))<1e-12
OC=np.rint(60*ocoef).astype(np.int64)
VT=np.rint(60*vt).astype(np.int64)
COUNT=BITS.shape[1]
SPECS=[('root_graph',n) for n in names]+[('actual_root_IC',)]
SPECS += [('maximum_equality',s) for s in (1,-1)]
SPECS += [('actual_safe',i,j) for i in range(6) for j in range(COUNT)]
SPECS += [('actual_pair',i,j) for i in range(COUNT) for j in range(i,COUNT)]
CAP=np.zeros(len(SPECS),dtype=np.int64)
CAP[len(names)+1]=60;CAP[len(names)+2]=-60


def matrix(a,d):
    whole=sum(a);ell=sum(a[:4])
    h=mix.div60(a[4]+a[5],whole)+mix.div60(a[4],(ell+1)*(ell+2))
    rows=[BASE+OC[:,None]*int(d>0)]
    rows.append((mix.div60(a[0],whole)-VT)[None,:])
    rows.append(np.array([-60*BITS[:,0],60*BITS[:,0]]))
    actual=[]
    for s in SPECS[len(names)+3:]:
        if s[0]=='actual_safe':
            _,i,j=s
            actual.append(mix.div60(a[i],whole)-BITS[:,j]*(60//(sum(a[:i])+6-i)))
        else:
            _,i,j=s
            actual.append(h-(BITS[:,i]+BITS[:,j])*(60//(ell+1))
                          +BITS[:,i]*BITS[:,j]*(60//((ell+1)*(ell+2))))
    rows.append(np.array(actual))
    return np.concatenate(rows)


def separate(record):
    active=[(tuple(map(int,z['actual_bits'])),z['d'],F(z['weight'])) for z in record['support']]
    mats=[matrix(a,d) for a,d,n in active]
    mat=np.concatenate(mats,axis=1);counts=[x.shape[1] for x in mats]
    assert len(set(counts))==1
    offsets=np.cumsum([0]+counts);size=mat.shape[1]
    rng=np.random.default_rng(321)
    selected=set()
    for lo,hi in zip(offsets[:-1],offsets[1:]):
        selected.update(map(int,rng.choice(np.arange(lo,hi),size=48,replace=False)))
    for step in range(80):
        ids=np.array(sorted(selected));groups=np.searchsorted(offsets,ids,side='right')-1
        eq=np.zeros((len(active),len(ids)+1));eq[groups,np.arange(len(ids))]=1
        aub=np.c_[-mat[:,ids].astype(float),-np.ones(len(SPECS))]
        sol=linprog(np.r_[np.zeros(len(ids)),1.],A_ub=aub,b_ub=CAP*float(F(record['K'])),
                    A_eq=eq,b_eq=[float(z[2]) for z in active],bounds=(0,None),method='highs')
        assert sol.success,sol.message
        lam=-sol.ineqlin.marginals
        rc=-lam@mat-sol.eqlin.marginals[np.repeat(np.arange(len(active)),counts)]
        neg=np.flatnonzero(rc<-1e-8)
        print('root phase',step,'gap',sol.fun,'selected',len(ids),'negative',len(neg),flush=True)
        if sol.fun<1e-8 or len(neg)==0:break
        selected.update(map(int,neg[np.argsort(rc[neg])[:800]]))
    else:raise RuntimeError('column generation did not converge')
    report={'scope':'discovery full two-copy maximum-root graph with actual safe and strong pair prices',
            'phase_I_float':float(sol.fun),'row_families':len(SPECS),'full_columns':size,
            'selected_columns':len(selected),'seed':321,'all_columns_priced':True}
    if sol.fun>1e-8:
        weights=np.rint(np.maximum(lam,0)*10**10).astype(np.int64)
        maximum=[int((weights@mm).max()) for mm in mats]
        kc=int(weights@CAP)
        value=sum(n*v for (_,_,n),v in zip(active,maximum))+F(record['K'])*kc
        report.update(exact_discovery_slack=str(value),
                      weights=[{'spec':list(s),'integer':str(w)} for s,w in zip(SPECS,weights) if w],
                      K_integer=str(kc))
        if value<0:
            look={(a,o):int((weights@matrix(a,o)).max()) for a in product((0,1),repeat=6) for o in (0,1)}
            norm=60*int(weights.max())
            row=[F(look[a,int(d>0)],norm) for a,d in mix.TYPES]+[F(kc,norm)]
            report['all_coefficients']=[str(z) for z in row]
            return report,row
    return report,None


def main():
    types,rows=mix.load_system()
    old=json.loads((HERE/'mixed_pair_results.json').read_text())
    for i,s in enumerate(old['steps']):
        if 'coefficients' in s:
            row=[F(v,s['norm']) for v in map(int,s['coefficients'])]+[F(s['K_integer'],s['norm'])]
            rows.append(('mixed-pair:'+str(i),row))
    record=old['certificate'];mix.js.verify_primal(record,types,rows)
    report,row=separate(record)
    if row is not None:
        rows.append(('root-shared-full-prices',row))
        new,n=mix.js.solve_primal(types,rows)
        report['combined_exact_point']=new
    (HERE/'root_shared_prices.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('all_coefficients','weights','combined_exact_point')},indent=2),flush=True)


if __name__=='__main__':main()
