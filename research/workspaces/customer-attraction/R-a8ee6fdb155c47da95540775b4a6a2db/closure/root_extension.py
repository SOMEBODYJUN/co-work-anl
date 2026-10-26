"""Test the new joint-atom marginals against the full maximum-root graph.

Root hidden themes remain independent of the R/Z themes conditional on actual
membership.  The 336 specified root row families share actual profits and K,
but contain no root-versus-R/Z cross comparisons.  No full-SPE claim is made.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json,sys,time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent'
sys.path.insert(0,str(OLD))
import root_shared_prices as rp
from six_stress import exact_solve

def source():
    data=json.loads((HERE/'joint_atoms_exact.json').read_text());mass=defaultdict(F)
    for c in data['atoms']:
        h=data['histograms'][c['hist_index']]
        mass[tuple(map(int,h['actual_bits'])),h['d']]+=F(c['weight'])
    return data,[(a,d,n) for (a,d),n in sorted(mass.items())]

def verify(report):
    data,active=source();K=F(data['K']);slack=[F(int(c))*K for c in rp.CAP]
    assert report['source_sha256']==hashlib.sha256((HERE/'joint_atoms_exact.json').read_bytes()).hexdigest()
    assert report['source_W']==data['W']
    assert report['root_paths']==rp.paths
    assert report['root_specs']==[list(s) for s in rp.SPECS]
    mats={(a,d):rp.matrix(a,d) for a,d,n in active}
    recovered=defaultdict(F)
    for atom in report['root_atoms']:
        a=tuple(map(int,atom['actual_bits']));d=atom['d'];mass=F(atom['weight']);ix=atom['root_assignment_index']
        assert mass>=0 and 0<=ix<len(rp.BITS)
        assert atom['root_bits']==list(map(int,rp.BITS[ix]))
        matrix=mats[a,d]
        slack=[s+int(matrix[i,ix])*mass for i,s in enumerate(slack)]
        recovered[a,d]+=mass
    assert dict(recovered)=={(a,d):n for a,d,n in active}
    assert min(slack)>=0
    return {'root_rows':len(slack),'minimum_integer_scaled_slack':str(min(slack)),
            'root_atoms':len(report['root_atoms']),'shared_K':str(K),'W':data['W']}

def main():
    target=HERE/'root_extension_exact.json'
    if '--verify' in sys.argv:
        print(json.dumps(verify(json.loads(target.read_text())),indent=2));return
    data,active=source();K=F(data['K']);start=time.time();mats=[rp.matrix(a,d) for a,d,n in active]
    mat=np.concatenate(mats,axis=1);counts=[x.shape[1] for x in mats];offsets=np.cumsum([0]+counts)
    rng=np.random.default_rng(321);selected=set()
    for lo,hi in zip(offsets[:-1],offsets[1:]):selected.update(map(int,rng.choice(np.arange(lo,hi),size=48,replace=False)))
    for step in range(80):
        ids=np.array(sorted(selected));groups=np.searchsorted(offsets,ids,side='right')-1
        eq=np.zeros((len(active),len(ids)+1));eq[groups,np.arange(len(ids))]=1
        sol=linprog(np.r_[np.zeros(len(ids)),1.],A_ub=np.c_[-mat[:,ids].astype(float),-np.ones(len(rp.SPECS))],
              b_ub=rp.CAP*float(K),A_eq=eq,b_eq=[float(z[2]) for z in active],bounds=(0,None),method='highs')
        assert sol.success,sol.message
        lam=-sol.ineqlin.marginals;rc=-lam@mat-sol.eqlin.marginals[np.repeat(np.arange(len(active)),counts)]
        neg=np.flatnonzero(rc<-1e-8)
        print('root current joint point',step,'phaseI',sol.fun,'selected',len(ids),'negative',len(neg),'seconds',time.time()-start,flush=True)
        if sol.fun<1e-8 or not len(neg):break
        selected.update(map(int,neg[np.argsort(rc[neg])[:800]]))
    if sol.fun>1e-8:
        weights=np.rint(np.maximum(lam,0)*10**10).astype(np.int64)
        maxima=[int((weights@mm).max()) for mm in mats];kc=int(weights@rp.CAP)
        cut=sum(n*v for (_,_,n),v in zip(active,maxima))+K*kc
        report={'scope':'fixed joint atom point maximum-root extension test; no reoptimization or full-domain half claim','phaseI':float(sol.fun),'exact_integer_cut_slack':str(cut),'weights':[str(x) for x in weights],'actual_support':[{'a':list(a),'d':d,'mass':str(n),'maximum':v} for (a,d,n),v in zip(active,maxima)],'K_integer':str(kc)}
        assert cut<0
        (HERE/'root_extension_separation.json').write_text(json.dumps(report,indent=2)+'\n');print('EXACT SEPARATION',cut,flush=True);return
    keep=np.flatnonzero(sol.x[:-1]>1e-9);keptids=ids[keep];vals=sol.x[keep];support=mat[:,keptids]
    equations=[]
    for row,cap in zip(support,rp.CAP):
        if abs(np.dot(row,vals)+int(cap)*float(K))<1e-8:
            equations.append([F(int(x)) for x in row]+[-int(cap)*K])
    for g,(a,d,mass) in enumerate(active):equations.append([F(int(offsets[g]<=ix<offsets[g+1])) for ix in keptids]+[mass])
    exact=exact_solve(equations,len(keep));assert min(exact)>=0
    atoms=[]
    for ix,mass in zip(keptids,exact):
        g=int(np.searchsorted(offsets,ix,side='right')-1);a,d,_=active[g]
        atoms.append({'actual_bits':''.join(map(str,a)),'d':d,'root_assignment_index':int(ix-offsets[g]),'root_bits':list(map(int,rp.BITS[ix-offsets[g]])),'weight':str(mass)})
    report={'scope':'exact extension of the new R,Z atom point to the specified 336 root row families by conditional product coupling; no cross comparisons between root themes and R/Z themes, no game or SPE claim','source_sha256':hashlib.sha256((HERE/'joint_atoms_exact.json').read_bytes()).hexdigest(),'source_W':data['W'],'root_atoms':atoms,'root_paths':rp.paths,'root_specs':[list(s) for s in rp.SPECS]}
    report['verification']=verify(report)
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['verification'],indent=2))

if __name__=='__main__':main()
