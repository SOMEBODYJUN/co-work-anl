"""Discovery for the shared-C two-branch projection. Not an SPE solver.

Every reported candidate is re-evaluated with Fraction before a mathematical
claim is recorded. The LP only chooses masses on local hidden membership types.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import json
import random
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent


def div(n, d):
    return F(n, d) if n else F(0)


LABELS = ('t', 'q', 'b', 'c', 'j', 'v')


@lru_cache(None)
def features(p, ell, t, q, b, c, j, v, s=0, ss=0, k=3):
    bits = dict(zip(LABELS, (t, q, b, c, j, v)))
    z1, z2 = p+t+s+b+c, p+c+ss+j+v
    out = {'sourceT': div(t, z1), 'sourceC': div(c, z2)}
    budgets = {'sourceT': (1, 0, 0), 'sourceC': (1, 0, 0)}
    for e in ('b', 'c', 'j', 'v'):
        out['price:'+e] = div(bits[e], ell+1)
        budgets['price:'+e] = (0, 1, 0)
        out['cap:'+e] = F(bits[e])
        budgets['cap:'+e] = (0, 0, 1)
    for name, qs, den, own, z in (
        ('last1', ('t','q','b','j','v'), p+t+s+b+1, c, z1),
        ('last2', ('t','q','b','c','j'), p+c+ss+j+1, v, z2),
        ('safeB', ('t','q','c','j','v'), p+t+s+2, b, z1),
        ('safeJ', ('t','q','b','c','v'), p+c+ss+2, j, z2),
    ):
        for e in qs:
            out[name+':'+e] = div(bits[e], den)-div(own, z)
            budgets[name+':'+e] = (0, 0, 0)
    for e, val in [('s',s),('ss',ss)]:
        out['price:'+e] = div(val, ell+1)
        budgets['price:'+e] = (0, k-3, 0)
        out['cap:'+e] = F(val)
        budgets['cap:'+e] = (0, 0, k-3)
    for br, beta, fst, lst, z in [(1,p+t+s,b,c,z1),(2,p+c+ss,j,v,z2)]:
        for X,Y in combinations_with_replacement(LABELS, 2):
            x,y=bits[X],bits[Y]
            name=f'pair{br}:{X},{Y}'
            # q may encode an average of pure queries. A diagonal pair then
            # averages q_l**2=q_l, not the square of its average.
            overlap=x if X==Y else x*y
            out[name] = div(x+y,beta+1)-div(overlap+fst,(beta+1)*(beta+2))-div(fst+lst,z)
            budgets[name] = (0,0,0)
    return out,budgets


BASE_NAMES = [n for n in features(0,0,0,0,0,0,0,0)[0] if not n.startswith('pair')]
ALL_NAMES = list(features(0,0,0,0,0,0,0,0)[0])


@lru_cache(None)
def hidden_configs(k):
    return tuple((*h,s,ss) for h in product((0,1),repeat=4)
                 for s in range(k-2) for ss in range(k-2))


def solve(visible, u, K, names=BASE_NAMES, k=3):
    # visible entries are (p,ell,t,q,mass), all exact rational.
    columns=[]
    coeff=[]
    for vi,(p,ell,t,q,mass) in enumerate(visible):
        for b,c,j,v,s,ss in hidden_configs(k):
            hidden=(b,c,j,v) if k==3 else (b,c,j,v,s,ss)
            f,bud=features(p,ell,t,q,b,c,j,v,s,ss,k)
            columns.append((vi,hidden))
            coeff.append([float(f[n]) for n in names])
    A=np.asarray(coeff).T
    rhs=np.asarray([float(bud[n][1]*u+bud[n][2]*K) for n in names])
    A=np.column_stack((A,[-bud[n][0] for n in names]))
    eq=np.zeros((len(visible),len(columns)+1))
    for ci,(vi,h) in enumerate(columns):
        eq[vi,ci]=1
    objective=np.zeros(len(columns)+1); objective[-1]=1
    res=linprog(objective,A_ub=A,b_ub=rhs,A_eq=eq,b_eq=[float(v[-1]) for v in visible],bounds=(0,None),method='highs')
    return res,columns,names


def exact_candidate(res, columns, visible, u, K, names):
    if not res.success:
        return None
    masses={i:F(float(x)).limit_denominator(10**7) for i,x in enumerate(res.x[:-1]) if x>1e-9}
    r=F(float(res.x[-1])).limit_denominator(10**7)
    totals=[F(0)]*len(visible)
    sums={n:F(0) for n in names}
    support=[]
    for ci,w in masses.items():
        vi,h=columns[ci]
        p,ell,t,q,mass=visible[vi]
        f,bud=features(p,ell,t,q,*h)
        totals[vi]+=w
        for n in names:sums[n]+=w*f[n]
        support.append({'visible':vi,'hidden':list(h),'mass':str(w)})
    slacks={n:bud[n][0]*r+bud[n][1]*u+bud[n][2]*K-sums[n] for n in names}
    return {'r':str(r),'support':support,'equalities_exact':totals==[v[-1] for v in visible],
            'feasible_exact':min(slacks.values())>=0,'slacks':{n:str(s) for n,s in slacks.items()}}


def dual_certificate(res, names, visible, u, K):
    # The minimization dual supplies r + sum(lambda price budgets)
    # >= sum_visible mass * min_hidden(sum lambda feature).
    if not res.success:return None
    theta={n:F(float(-x)).limit_denominator(10**7) for n,x in zip(names,res.ineqlin.marginals) if x < -1e-9}
    source=theta.get('sourceT',F(0))+theta.get('sourceC',F(0))
    if source==0:return {'error':'zero-source'}
    theta={n:w/source for n,w in theta.items()}
    minima=[]
    budget_u=budget_K=F(0)
    for vi,(p,ell,t,q,mass) in enumerate(visible):
        vals=[]
        for h in product((0,1),repeat=4):
            f,bud=features(p,ell,t,q,*h)
            val=sum((w*f[n] for n,w in theta.items()),F(0))
            vals.append((val,h))
        minimum=min(v[0] for v in vals)
        minima.append({'visible':vi,'value':str(minimum),'argmins':[list(h) for val,h in vals if val==minimum]})
    for n,w in theta.items():
        budget_u+=w*bud[n][1];budget_K+=w*bud[n][2]
    lower=sum((v[-1]*F(a['value']) for v,a in zip(visible,minima)),F(0))-budget_u*u-budget_K*K
    return {'theta':{n:str(w) for n,w in theta.items()},'u_coefficient':str(budget_u),'K_coefficient':str(budget_K),'minima':minima,'lower_bound':str(lower)}


def run():
    rng=random.Random(20261111)
    records=[]
    for iteration in range(3000):
        if iteration < 36:
            p=iteration//12;ell=(iteration//2)%6
            visible=[(p,ell,1,0,F(1)),(p,ell,0,1,F(1))]
        else:
            visible=[]
            states=rng.sample([(p,ell,t,q) for p in range(4) for ell in range(p,6) for t,q in product((0,1),repeat=2)],rng.randint(2,7))
            for v in states:visible.append((*v,F(rng.randint(1,4))))
        minK=max(sum(v[-1]*v[2] for v in visible),sum(v[-1]*v[3] for v in visible))
        if minK==0:continue
        K=minK*F(rng.choice([1,1,1,2,3]),rng.choice([1,1]))
        u=max(sum(v[-1]*div(v[2],v[1]+1) for v in visible),sum(v[-1]*div(v[3],v[1]+1) for v in visible))
        if u==0:continue
        base,columns,base_names=solve(visible,u,K)
        if not base.success:continue
        new,_,names=solve(visible,u,K,ALL_NAMES)
        if not new.success:continue
        gap=new.fun-base.fun
        if gap>1e-7:
            rec={'iteration':iteration,'visible':[[*v[:-1],str(v[-1])] for v in visible], 'u':str(u),'K':str(K),'base_value_float':base.fun,'joint_value_float':new.fun,'gap_float':gap,
                 'base_exact':exact_candidate(base,columns,visible,u,K,base_names),
                 'joint_exact':exact_candidate(new,columns,visible,u,K,names),
                 'joint_dual':dual_certificate(new,names,visible,u,K)}
            records.append(rec)
            (HERE/'discovery.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps({'iteration':iteration,'gap':gap,'r_base':rec['base_exact']['r'],'r_joint':rec['joint_exact']['r'],'u':str(u),'K':str(K),'support':len(rec['base_exact']['support']),'theta':rec['joint_dual']['theta'],'exact':(rec['base_exact']['equalities_exact'],rec['base_exact']['feasible_exact'],rec['joint_exact']['equalities_exact'],rec['joint_exact']['feasible_exact'])}),flush=True)
            if len(records)>=5:break
    print('records',len(records))


if __name__=='__main__':run()
