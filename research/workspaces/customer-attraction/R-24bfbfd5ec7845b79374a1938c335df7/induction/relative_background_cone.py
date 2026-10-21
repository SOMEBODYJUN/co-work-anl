import sys,random,json,itertools,time
sys.path.insert(0,'/workspace/scratch/255f7bc2eb33/co-work-anl-boss3')
from customer_attraction import Instance,CustomerType,ExactSPESolver
from scipy.optimize import linprog
import numpy as np

def coeff(mask,terminal,action):
    return (1/sum(terminal[t] for t in range(len(terminal)) if mask>>t&1)) if mask>>action&1 else 0.

def generate_gamma(solver,pref,target):
    k=len(pref);g={}
    def inc(p,a):return p[:a]+(p[a]+1,)+p[a+1:]
    def rec(h,p,desired):
        if sum(p)==solver.instance.players:return
        floor=solver.threshold(p)
        actions=[a for a in range(k) if desired in solver.outcomes(inc(p,a)) and solver._utility(desired,a)>=floor]
        a=min(actions,key=lambda a:solver._utility(desired,a));g[h]=a
        for x in range(k):
            p2=inc(p,x)
            des=desired if x==a else min(solver.outcomes(p2),key=lambda f:(solver._utility(f,x),f))
            rec(h+(x,),p2,des)
    rec((),pref,target);return g

def gb(b,d):
    # Concave linear interpolation of n/(b+n), with g_0(d)=min(1,d).
    if b==0:return min(1.,d)
    n=int(d)
    q=d-n
    return (1-q)*n/(b+n)+q*(n+1)/(b+n+1)

def attack(k,pref,g,r,zs):
    masks=list(range(1,1<<k));M=len(masks);term={}
    def terminal(h):
        q=list(pref);hh=h
        for a in hh:q[a]+=1
        while len(hh)<r:
            a=g[hh];q[a]+=1;hh+=(a,)
        return tuple(q),hh
    for h in g:term[h]=terminal(h)
    actual,actual_path=term[()];v=np.array([coeff(mask,actual,g[()]) for mask in masks]);new=[actual[a]-pref[a] for a in range(k)]; bmask=[sum(pref[a] for a in range(k) if mask>>a&1) for mask in masks]; nmask=[sum(new[a] for a in range(k) if mask>>a&1) for mask in masks]; w=np.array([n/(b+n) if b+n else 0. for b,n in zip(bmask,nmask)])
    rows=[]
    for h,a in g.items():
        on,_=term[h]
        for t in range(k):
            off,_=terminal(h+(t,))
            rows.append([coeff(mask,off,t)-coeff(mask,on,a) for mask in masks])
    # first actual mover must be minimum newcomer
    for a in actual_path[1:]:rows.append([v[j]-coeff(mask,actual,a) for j,mask in enumerate(masks)])
    A=np.array(rows)
    for z in zs:
        tau=sum(z);obj=np.array([gb(b,sum(z[a] for a in range(k) if mask>>a&1)) for mask,b in zip(masks,bmask)])-tau*v-w
        sol=linprog(-obj,A_ub=A,b_ub=np.zeros(len(rows)),A_eq=[np.ones(M)],b_eq=[1],bounds=[(0,None)]*M,method='highs')
        if sol.success and -sol.fun>1e-8:return {'gap':-sol.fun,'k':k,'pref':pref,'gamma':{str(h):a for h,a in g.items()},'weights':[(mask,float(x)) for mask,x in zip(masks,sol.x) if x>1e-8],'z':z,'actual':actual_path}
    return None

def main(rounds):
    rg=random.Random(339);start=time.time();count=0
    for trial in range(rounds):
        k=rg.choice([4,5,6]);r=3;bg=rg.choice([0,1,2,3,5,8,13]);pref=[0]*k
        for _ in range(bg):pref[rg.randrange(k) if rg.random()<.25 else 0]+=1
        pref=tuple(pref);m=bg+r
        types=[]
        for mask in range(1,1<<k):
            x=rg.randrange(5) if rg.random()<.6 else 0
            if x:types.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),x))
        ins=Instance(tuple(map(str,range(k))),tuple(types),m);solver=ExactSPESolver(ins)
        zs=[tuple(int(mask>>a&1) for a in range(k)) for mask in range(1,1<<k)]
        zs += [tuple(rg.choice([0,.5,1,1.5,2]) for a in range(k)) for _ in range(20)]
        for target in sorted(solver.outcomes(pref))[:3]:
            g=generate_gamma(solver,pref,target);out=attack(k,pref,g,r,zs);count+=1
            if out:
                print(json.dumps({'FOUND':out,'trials':trial,'cones':count}));return
        if trial%10==0:print(json.dumps({'trial':trial,'cones':count,'seconds':time.time()-start}),flush=True)
    print(json.dumps({'none':True,'cones':count,'seconds':time.time()-start}))
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 50)
