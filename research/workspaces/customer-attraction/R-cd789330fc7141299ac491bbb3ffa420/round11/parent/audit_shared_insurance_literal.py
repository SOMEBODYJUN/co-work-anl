"""Literal-unit independent audit; only actual-prefix menus/KKT/arithmetic.
Full-SPE theorem inherited from peer; no author imports/full-tree claim.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
M=6
TOPICS=list(product(range(M),range(M-1)))
SETS=[{a,6+2*b,7+2*b} for a,b in TOPICS]
def next_topic(h):
    if not h:return (0,0)
    anchor=h[0];state='normal';target=None
    for pos in range(1,len(h)):
        used={b for a,b in h[:pos]}; observed=h[pos]
        if state=='normal' and pos<M-1:
            if observed!=(anchor[0],min(set(range(M-1))-used)):
                if observed[1] in used:state='exit'
                else:state='punish';target=observed[1]
        elif state=='punish' and observed[1] in used:state='exit'
    ue={a for a,b in h};ub={b for a,b in h}
    freee=min(set(range(M))-ue)
    if len(h)==M-1:
        if state=='normal':return (freee,anchor[1])
        if state=='punish':return (freee,target)
    return ((anchor[0] if state=='normal' else freee),min(set(range(M-1))-ub))
def finish(h):
    z=list(h)
    while len(z)<M:z.append(next_topic(z))
    return z
def counts(z):
    return [sum(x in SETS[TOPICS.index(a)] for a in z) for x in range(16)]
def audit():
    z=finish([])
    assert z==[(0,0),(0,1),(0,2),(0,3),(0,4),(1,0)]
    menus=[];d=[]
    for i in range(M):
        row=[];pay=[]
        for j,a in enumerate(TOPICS):
            leaf=finish(z[:i]+[a]);col=counts(leaf[:i]+leaf[i+1:])
            row.append(col);pay.append(sum((F(1,1+col[x]) for x in SETS[j]),F(0)))
        menus.append(row);d.append(pay)
    u=[d[i][TOPICS.index(z[i])] for i in range(M)]
    assert sum(u)==12 and all(d[i][j]<=u[i] for i in range(M) for j in range(30))
    reports=[]
    cases=[('insurance_shared_covariance_m6_exact.json',list(range(30))),('insurance_shared_saddle_m6_exact.json',[j for j,(a,b) in enumerate(TOPICS) if a])]
    for filename,support in cases:
        packet=json.loads((HERE.parent/'aggregate'/filename).read_text())
        lc=list(map(F,packet['L']));L=lc[:6]+[v for v in lc[6:] for _ in (0,1)]
        q=[[(int(j),F(w)) for j,w in row] for row in packet['q']]
        assert all(sum(w for j,w in row)==1 for row in q)
        assert all(sum((w*menus[i][j][x]/M for i in range(M) for j,w in q[i]),F(0))==L[x] for x in range(16))
        rho=[F(sum(x in SETS[j] for j in support),len(support)) for x in range(16)]
        t=[1/(1+l) for l in L];weight=[rho[x]*t[x]**2 for x in range(16)]
        score=lambda i,j:sum((weight[x]*menus[i][j][x] for x in range(16)),F(0))
        for i in range(M):
            best=max(score(i,j) for j in range(30))
            assert all(score(i,j)==best for j,w in q[i] if w)
        Cmat=[[sum((t[x]**2*(menus[i][j][x]-L[x]) for x in SETS[j]),F(0)) for j in range(30)] for i in range(M)]
        Dmat=[[sum((t[x]**2*(menus[i][j][x]-L[x])**2/(1+menus[i][j][x]) for x in SETS[j]),F(0)) for j in range(30)] for i in range(M)]
        C=sum((Cmat[i][j]/len(support) for i in range(M) for j in support),F(0))
        D=sum((Dmat[i][j]/len(support) for i in range(M) for j in support),F(0))
        IC=sum(u)-sum((d[i][j]/len(support) for i in range(M) for j in support),F(0))
        gamma=sum((rho[x]*t[x] for x in range(16)),F(0))
        assert all(v==F(packet[k]) for v,k in [(C,'C'),(D,'D'),(IC,'IC'),(gamma,'F_optimum')])
        assert sum(u)-M*gamma==IC-C+D
        g=[sum(t[x] for x in s) for s in SETS]
        saddle=max(g)==gamma and all(g[j]==gamma for j in support)
        if len(support)==25:
            assert saddle and all(len({Cmat[i][j] for j in support})==1 for i in range(M))
        reports.append({'input':filename,'KKT':True,'F':str(gamma),'C':str(C),'D':str(D),'IC':str(IC),'balance':str(sum(u)-M*gamma),'saddle':saddle})
    return {'scope':'Independent literal16-unit client actual-prefix audit,180 menus; no full-tree re-audit','all_actual_prefix_IC':True,'reports':reports}
if __name__=='__main__':
    report=audit()
    with (HERE/'shared_insurance_literal_independent.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))
