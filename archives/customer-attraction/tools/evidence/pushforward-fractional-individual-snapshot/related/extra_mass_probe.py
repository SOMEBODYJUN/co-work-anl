"""Discovery only: one-extra-unit fractional background leader floor.

All policy rows are actual complete local ordered-history deviations. Past
topic counts are fixed legal histories, not arbitrary customer-weight loads.
Floating cones and nonlinear optimization never certify a positive result.
"""
from pathlib import Path
import sys,json,math,itertools,random,time
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog,minimize

OUT=Path(__file__).resolve().parent

def game_policy(w,member,r,past,rng):
    k=len(member);b=np.array(past)@member
    L=math.lcm(*range(1,sum(past)+r+1))
    @lru_cache(None)
    def util(q):
        den=b+np.array(q)@member
        return member@(w*(L//np.maximum(den,1)))
    @lru_cache(None)
    def solve(q):
        if sum(q)==r:return frozenset([q])
        children=[solve(tuple(x+int(a==j)for j,x in enumerate(q)))for a in range(k)]
        threshold=max(min(util(z)[a]for z in ch)for a,ch in enumerate(children))
        return frozenset(z for a,ch in enumerate(children)for z in ch if util(z)[a]>=threshold)
    zero=(0,)*k;rootset=solve(zero)
    # Prefer the lowest attainable root utility, then root welfare.
    opts=[]
    for a in range(k):
        ch=solve(tuple(int(a==j)for j in range(k)))
        threshold=max(min(util(z)[aa]for z in solve(tuple(int(aa==j)for j in range(k))))for aa in range(k))
        opts.extend((util(z)[a],rng.random(),a,z)for z in ch if util(z)[a]>=threshold)
    _,_,roota,target=min(opts)
    actions={};terminals={}
    def expand(h,q,desired):
        terminals[h]=desired
        if len(h)==r:return
        children=[solve(tuple(x+int(a==j)for j,x in enumerate(q)))for a in range(k)]
        threshold=max(min(util(z)[a]for z in ch)for a,ch in enumerate(children))
        admissible=[a for a,ch in enumerate(children)if desired in ch and util(desired)[a]>=threshold]
        a=roota if not h else rng.choice(admissible)
        assert a in admissible
        actions[h]=a
        for aa,ch in enumerate(children):
            if aa==a:z=desired
            else:
                low=min(util(z)[aa]for z in ch);z=rng.choice(sorted(z for z in ch if util(z)[aa]==low))
            expand(h+(aa,),tuple(x+int(aa==j)for j,x in enumerate(q)),z)
    expand((),zero,target)
    rows=[]
    def row(a,z):return member[a]/(b+np.array(z)@member).clip(1)
    for h,a in actions.items():
        for aa in range(k):
            if aa!=a:rows.append(row(a,terminals[h])-row(aa,terminals[h+(aa,)]))
    G=np.unique(np.round(rows,13),axis=0)
    return G,row(roota,target),actions,target

def frac(w,member,b,mass,p=None,qstart=None):
    k=len(member)
    q0=np.ones(k)/k if qstart is None else qstart
    def den(q):return b+1+mass*(q@member)
    if p is not None:
        alpha=p@member
        ans=minimize(lambda q:np.dot(w*alpha,1/den(q)),q0,
          jac=lambda q:-mass*member@(w*alpha/den(q)**2),bounds=[(0,1)]*k,
          constraints=[{'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)}],
          method='SLSQP',options={'ftol':1e-11,'maxiter':500})
        if not ans.success:raise RuntimeError(ans.message)
        return ans.x,float(ans.fun)
    def g(q):return member@(w/den(q))
    def dg(q):return -mass*(member*(w/den(q)**2))@member.T
    ans=minimize(lambda z:z[-1],np.r_[q0,max(g(q0))],jac=lambda z:np.r_[np.zeros(k),1.],
      bounds=[(0,1)]*k+[(0,None)],constraints=[
        {'type':'eq','fun':lambda z:z[:-1].sum()-1,'jac':lambda z:np.r_[np.ones(k),0.]},
        {'type':'ineq','fun':lambda z:z[-1]-g(z[:-1]),'jac':lambda z:np.c_[-dg(z[:-1]),np.ones(k)]}],
      method='SLSQP',options={'ftol':1e-10,'maxiter':500})
    if not ans.success:raise RuntimeError(ans.message)
    pp=np.maximum(ans.multipliers[1:],0);pp/=sum(pp)
    q,v=frac(w,member,b,mass,pp,ans.x[:-1])
    assert abs(v-ans.x[-1])<1e-5
    return pp,v,q

def challenge(G,c,w,member,past,r,rounds=5):
    k=len(member);b=np.array(past)@member;mass=r
    p,v,q=frac(w,member,b,mass);qs=[*np.eye(k),np.ones(k)/k,q]
    best=v/(c@w);record=None
    for step in range(rounds):
        for cut in range(150):
            R=(p@member)[None,:]/(1+b[None,:]+mass*np.array(qs)@member)
            obj=np.r_[np.zeros(len(w)),-1.]
            ans=linprog(obj,A_ub=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[-R,np.ones(len(R))]]),b_ub=np.zeros(len(G)+len(R)),A_eq=np.r_[c,0.][None,:],b_eq=[1.],bounds=[(0,None)]*(len(w)+1),method='highs')
            assert ans.success,ans.message
            ww=ans.x[:-1];q,v=frac(ww,member,b,mass,p)
            if ans.x[-1]-v<2e-6:break
            qs.append(q)
        else:raise RuntimeError('cut budget')
        p,v,q=frac(ww,member,b,mass);qs.append(q)
        if v>best:best=v;record={'weights':ww.tolist(),'query':p.tolist(),'q':q.tolist(),'ratio':v,'past':past,'r':r}
        if v>1+1e-6:return best,record
    return best,record

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=30);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--remaining',type=int,default=3);ap.add_argument('--seed',type=int,default=210071);ap.add_argument('--rounds',type=int,default=5);ap.add_argument('--past-max',type=int,default=5);a=ap.parse_args()
    rng=random.Random(a.seed);k=a.topics;member=np.array([[(B>>i)&1 for B in range(1,1<<k)]for i in range(k)],dtype=float);best=0;start=time.time();rows=[]
    for j in range(a.games):
        past=[0]*k
        for _ in range(rng.randrange(a.past_max+1)):past[rng.randrange(k)]+=1
        w=np.array([rng.randrange(1,8)if rng.random()<.35 else 0 for _ in range((1<<k)-1)],dtype=int)
        if not np.any(w):continue
        try:
            G,c,actions,target=game_policy(w,member,a.remaining,past,rng)
            ratio,rec=challenge(G,c,w.astype(float),member,past,a.remaining,a.rounds)
            rows.append({'game':j,'ratio':ratio,'past':past,'policy_rows':len(G)})
            if ratio>best+1e-8:
                best=ratio;print(json.dumps(rows[-1]),flush=True)
            if ratio>1+1e-6:
                rec.update({'status':'FLOATING CANDIDATE ONLY','actions':[{'history':list(h),'action':aa}for h,aa in actions.items()],'target':target,'initial_weights':w.tolist()})
                (OUT/'extra_mass_candidate.json').write_text(json.dumps(rec,indent=2)+'\n');break
        except Exception as e:print(json.dumps({'game':j,'error':str(e)}),flush=True)
    result={'status':'finite floating discovery only','seed':a.seed,'topics':k,'remaining':a.remaining,'best':best,'elapsed':time.time()-start,'runs':rows}
    (OUT/f'extra_mass_scan_{k}_{a.remaining}_{a.seed}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='runs'}),flush=True)

if __name__=='__main__':main()
