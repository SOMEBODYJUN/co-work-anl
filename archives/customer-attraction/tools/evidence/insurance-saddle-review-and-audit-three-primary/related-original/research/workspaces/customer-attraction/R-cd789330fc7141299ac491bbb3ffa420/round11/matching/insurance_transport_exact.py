"""Exact named-packet role-query transport, with an integer Hungarian dual.

Tests only the parent's stronger sign candidate C_transport<=0 at a fixed
shared-load minimizer. No policy or customer cone is optimized or scanned.
The old insurance full-SPE theorem is inherited; menus are rebuilt here.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import lcm
import json

HERE=Path(__file__).resolve().parent
m=6
banks=m-1
acts=tuple(product(range(m),range(banks)))
ad={a:i for i,a in enumerate(acts)}
inc=[tuple(int(x==a) for x in range(m))+tuple(int(x==b) for x in range(banks))
     for a,b in acts]
weights=[1]*m+[2]*banks

@lru_cache(None)
def action(h):
    if not h:return (0,0)
    aa,ab=h[0]
    mode='BASE'; target=None; usedb={ab}
    for a in h[1:]:
        if mode=='BASE':
            prescribed=(aa,min(set(range(banks))-usedb))
            if a!=prescribed:
                if a[1] in usedb:mode='EXIT'
                else:mode='PUNISH';target=a[1]
        elif mode=='PUNISH' and a[1] in usedb:
            mode='EXIT'
        usedb.add(a[1])
    freea=set(range(m))-{a for a,b in h}
    freeb=set(range(banks))-usedb
    last=len(h)==m-1
    if mode=='BASE':return (min(freea),ab) if last else (aa,min(freeb))
    if mode=='PUNISH':return (min(freea),target) if last else (min(freea),min(freeb))
    return (min(freea),min(freeb))

@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish(h+(action(h),))

def hungarian(a):
    """Square integer min assignment; exact primal and feasible dual."""
    n=len(a)
    u=[0]*(n+1);v=[0]*(n+1);p=[0]*(n+1);way=[0]*(n+1)
    for i in range(1,n+1):
        p[0]=i;j0=0;minv=[None]*(n+1);used=[False]*(n+1)
        while True:
            used[j0]=True;i0=p[j0];delta=None;j1=0
            for j in range(1,n+1):
                if not used[j]:
                    cur=a[i0-1][j-1]-u[i0]-v[j]
                    if minv[j] is None or cur<minv[j]:minv[j]=cur;way[j]=j0
                    if delta is None or minv[j]<delta:delta=minv[j];j1=j
            for j in range(n+1):
                if used[j]:u[p[j]]+=delta;v[j]-=delta
                elif minv[j] is not None:minv[j]-=delta
            j0=j1
            if p[j0]==0:break
        while True:
            j1=way[j0];p[j0]=p[j1];j0=j1
            if j0==0:break
    match=[None]*n
    for j in range(1,n+1):match[p[j]-1]=j-1
    assert all(u[i+1]+v[j+1]<=a[i][j] for i in range(n) for j in range(n))
    assert sum(a[i][match[i]] for i in range(n))==sum(u[1:])+sum(v[1:])
    return match,u[1:],v[1:]

def main():
    raw=json.loads((HERE.parent/'aggregate/insurance_shared_covariance_m6_exact.json').read_text())
    L=[F(x) for x in raw['L']]
    t=[1/(1+l) for l in L]
    z=finish(())
    cols=[[[sum(inc[ad[b]][x] for j,b in enumerate(finish(z[:i]+(a,))) if j!=i)
             for x in range(len(L))] for a in acts] for i in range(m)]
    d=[[sum((F(weights[x]*inc[a][x],1+cols[i][a][x]) for x in range(len(L))),F(0))
        for a in range(len(acts))] for i in range(m)]
    u=[d[i][ad[z[i]]] for i in range(m)]
    C=[[sum((weights[x]*inc[a][x]*t[x]**2*(cols[i][a][x]-L[x])
             for x in range(len(L))),F(0)) for a in range(len(acts))] for i in range(m)]
    D=[[sum((weights[x]*inc[a][x]*t[x]**2*(cols[i][a][x]-L[x])**2/(1+cols[i][a][x])
             for x in range(len(L))),F(0)) for a in range(len(acts))] for i in range(m)]
    assert sum(sum(row) for row in C)/30==F(raw['C'])
    assert all(d[i][a]<=u[i] for i in range(m) for a in range(len(acts)))
    denominator=lcm(*(x.denominator for row in C for x in row))
    a=[[int(C[i//5][j]*denominator) for j in range(30)] for i in range(30)]
    match,ur,vc=hungarian(a)
    chosen=[sorted(match[5*i:5*i+5]) for i in range(m)]
    minC=sum((C[i][j]/5 for i in range(m) for j in chosen[i]),F(0))
    Ds=sum((D[i][j]/5 for i in range(m) for j in chosen[i]),F(0))
    IC=sum(u)-sum((d[i][j]/5 for i in range(m) for j in chosen[i]),F(0))
    alpha=[F(sum(ur[5*i:5*i+5]),5*denominator) for i in range(m)]
    beta=[F(v,denominator) for v in vc]
    assert all(alpha[i]+beta[j]<=C[i][j] for i in range(m) for j in range(30))
    assert sum(alpha)+sum(beta)/5==minC
    Fopt=F(raw['F_optimum'])
    assert sum(u)-m*Fopt==IC-minC+Ds
    report=dict(scope='one exact existing insurance m6 packet; named transported C<=0 sign candidate only',
                full_SPE='inherited old theorem; no new full-tree re-audit',
                actual=[list(a) for a in z],u=list(map(str,u)),
                p='uniform 30 themes',L=list(map(str,L)),fixed_L_KKT='inherited exact certificate',
                diagonal_C=raw['C'],minimum_transported_C=str(minC),
                candidate_has_feasible_nonpositive_C=minC<=0,
                transported_D=str(Ds),transported_IC=str(IC),W_minus_mF=str(sum(u)-m*Fopt),
                role_queries=[[[j,list(acts[j]),'1/5'] for j in js] for js in chosen],
                dual_alpha=list(map(str,alpha)),dual_beta=list(map(str,beta)),
                exact_dual_all_constraints=True,exact_primal_dual_equality=True,
                all_actual_prefix_IC_checked=True,integer_cost_denominator=denominator,
                general_half='OPEN',
                general_transported_sign='FALSE; active optimal-saddle packet in insurance_saddle_independent_review.md',
                universal_bound_proved=False)
    (HERE/'insurance_transport_exact.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:val for key,val in report.items()
                      if key not in ('role_queries','dual_beta','L')},indent=2))

if __name__=='__main__':main()
