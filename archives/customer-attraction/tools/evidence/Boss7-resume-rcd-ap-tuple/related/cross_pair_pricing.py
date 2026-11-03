"""Add160 cross-family pair partitions that preserve exact separability.

Source AB or AE has background p_fixed+t, so shared optimal membership t
makes every query-cost sum determined by the target histogram alone.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json,time,sys
import numpy as np
from scipy.optimize import linprog
from full_pricing import Universe,HERE,SCALE,atom_key,sc
from partition_pair_closure import compact_costs,PARTITIONS

COUNTS=dict(zip(PARTITIONS,(1,4,4,4,12)))
FIELDS={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}

class CrossUniverse(Universe):
    def __init__(self,overlap=1):
        super().__init__(overlap);self.cross=[];self.cost={}
        for source in ('AB','AE'):
            for target in ('AB','AE','Sbranch'):
                if source==target:continue
                k=4 if target=='Sbranch' else 3
                for u,v in combinations_with_replacement(range(k),2):
                    for orb in PARTITIONS:
                        self.cross.append((f'crosspair:{source}:{target}:{u}{v}:{orb}',source,target,u,v,orb))
        self.names += [r[0] for r in self.cross]
        for k in (3,4):
            hh=self.H[k];tt=self.ty[k];B0=hh@tt[:,0]
            for p in range(3):
                pref=p+tt[:,0];D1=hh@sc([F(1,int(z)+1) for z in pref]);DG=hh@sc([F(1,(int(z)+1)*(int(z)+2)) for z in pref])
                for u,v in combinations_with_replacement(range(k),2):
                    B=hh@tt[:,u];C=hh@tt[:,v];K=hh@(tt[:,u]*tt[:,v])
                    bu=hh@sc([F(int(t[u]),int(z)+1) for t,z in zip(tt,pref)]);cv=hh@sc([F(int(t[v]),int(z)+1) for t,z in zip(tt,pref)])
                    bg=hh@sc([F(int(t[u]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,pref)]);cg=hh@sc([F(int(t[v]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,pref)]);bc=hh@sc([F(int(t[u]*t[v]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,pref)])
                    for orb,cost in {
                        'all_equal':bu+cv-overlap*bc,
                        'query_equal':(B+C)*D1-bu-cv-overlap*(K*DG-bc),
                        'first_branch':4*bu+C*D1-cv-overlap*(C*bg-bc),
                        'second_branch':B*D1-bu+4*cv-overlap*(B*cg-bc),
                        'all_distinct':3*((B+C)*D1-bu-cv)-overlap*((B*C-K)*DG-B*cg-C*bg+2*bc)
                    }.items():self.cost[k,p,u,v,orb]=cost
        self.crossweights=[];self.extra_cache={}
        print(json.dumps({'additional_cross_rows':len(self.cross),'total_rows':len(self.names)}),flush=True)

    def atom_rows(self,atom):
        rr=super().atom_rows(atom);bits=dict(zip('ABCDEUVWXY',map(int,atom['bits'])))
        pp={'AB':bits['A']+bits['B'],'AE':bits['A']+bits['E']};hh={tag:atom[field] for tag,field in FIELDS.items()}
        H={}
        for tag in ('AB','AE'):
            p=pp[tag]
            H[tag]=sum((n*(F(int(z[-2]+z[-1]),int(p+sum(z))) if z[-2]+z[-1] else F(0))+n*F(int(z[-2]),(int(p+z[0])+1)*(int(p+z[0])+2)) for n,z in zip(hh[tag],self.ty[3])),F(0))
        for name,source,target,u,v,orb in self.cross:
            k=4 if target=='Sbranch' else 3;hist=hh[target];ty=self.ty[k];B=sum(n*int(z[u]) for n,z in zip(hist,ty));C=sum(n*int(z[v]) for n,z in zip(hist,ty));K=sum(n*int(z[u]*z[v]) for n,z in zip(hist,ty))
            cost=sum((n*compact_costs(5,pp[source]+int(z[0]),int(z[u]),int(z[v]),B,C,K,overlap=self.overlap)[orb] for n,z in zip(hist,ty)),F(0))
            rr[name]=COUNTS[orb]*H[source]-cost
        return rr

    def family_score(self,bits,tag,weights,integer=False):
        key,const,vec,me,mh=super().family_score(bits,tag,weights,integer=integer)
        pp={'AB':bits[0]+bits[1],'AE':bits[0]+bits[4]};ekey=(tag,pp['AB'],pp['AE'])
        if ekey not in self.extra_cache:
            k=4 if tag=='Sbranch' else 3;extra=np.zeros(len(self.hist[k]),dtype=object if integer=='object' else np.int64 if integer else float)
            for _,source,target,u,v,orb,w in self.crossweights:
                if source==tag:extra+=w*(self.M[3,pp[tag]]['H'].astype(object) if integer=='object' else self.M[3,pp[tag]]['H'])*COUNTS[orb]
                if target==tag:
                    a=self.cost[k,pp[source],u,v,orb];extra-=w*(a.astype(object) if integer=='object' else a)
            self.extra_cache[ekey]=extra
        return (key[0],key,ekey),const,vec+[(1,self.extra_cache[ekey])],me,mh

    def price(self,lam,beta,**kw):
        integer=kw.get('integer',False);self.crossweights=[];self.extra_cache={}
        for row,w in zip(self.cross,lam[-len(self.cross):]):
            if abs(w)>1e-11:self.crossweights.append((*row,int(w) if integer else float(w)))
        return super().price(lam,beta,**kw)

def run(maxiter=100):
    U=CrossUniverse();src=json.loads((HERE/'exact_optimum_primal_overlap1.json').read_text());atoms=[];keys=set();cols=[];w=[];o=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return False
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key)
        w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])))
        return True
    for a in src['atoms']:add(a)
    add({'bits':'1111111111','AB_hist':[0]*7+[5],'AE_hist':[0]*7+[5],'second_hist':[0]*15+[5],'menus_lh':[(5,5)]*3})
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T
        out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
        assert out.success,out.message
        beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,contexts=U.price(lam,beta,batch=80)
        count=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':minimum,'new_columns':count,'score_contexts':contexts,'seconds':time.time()-t0};history.append(rec);print(json.dumps(rec),flush=True)
        (HERE/'cg_cross_pair.json').write_text(json.dumps({'scope':'717-row necessary-condition relaxation only; no SPE or trueOPT claim','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history},indent=2)+'\n')
        if count==0:break

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 100)
