"""Five-player, two groups of five: exact-policy cone discovery.

The state retains the group of the second *ordered* action. Only this chosen
policy is compressed; the mathematical SPE quantifier is not restricted.
Customer type weights are invariant under within-group label permutations.
"""
import json, itertools, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from probe_availability import compositions

OUT=Path(__file__).parent
n=5;k=10;L=60
ms=list(range(1,1<<k));orbits=[(i,j) for i in range(6) for j in range(6) if i+j]
oi={t:i for i,t in enumerate(orbits)}
incs=np.array([[(m>>a)&1 for a in range(k)] for m in ms],dtype=np.int64)
obs=np.array([oi[((m&31).bit_count(),(m>>5).bit_count())] for m in ms])
states=[list(compositions(s,k)) for s in range(n+1)]
u={};wf={}
for q in states[n]:
    loads=incs@q
    u[q]=np.stack([np.bincount(obs,weights=incs[:,a]*np.array([L//d if d else 0 for d in loads]),minlength=len(orbits)) for a in range(k)]).astype(np.int64)
    wf[q]=np.bincount(obs,weights=loads>0,minlength=len(orbits))

def successor(q,a):
    qq=list(q);qq[a]+=1;return tuple(qq)

def newg(g,depth,a):return a//5 if depth==1 else g

def keys(depth):
    for q in states[depth]:
        for g in ([-1] if depth<2 else [0,1]):
            if g==-1 or sum(q[g*5:g*5+5]):yield q,g

def signed_weights():
    # Two exact Boolean Möbius transforms, independent of repository compiler.
    f=[0]*(1<<k)
    for s in range(1<<k):
        size=s.bit_count();mixed=bool(s&31) and bool(s>>5)
        if size==n and not mixed:f[s]=1
        elif size==n-1 and mixed:f[s]=-1
    c=f[:]
    for a in range(k):
        for s in range(1<<k):
            if s>>a&1:c[s]-=c[s^(1<<a)]
    z=[0 if not s else (-1)**(s.bit_count()+1)*s.bit_count()*c[s] for s in range(1<<k)]
    x=z[:]
    for a in range(k):
        for s in range(1<<k):
            if not s>>a&1:x[s]-=x[s|(1<<a)]
    M=sum(abs(x[s]) for s in ms);K=6*M+4
    weights=np.zeros(len(orbits),dtype=np.int64)
    for s in ms:weights[obs[s-1]]=x[s]+K
    assert all(weights[obs[s-1]]==x[s]+K for s in ms)
    return weights

def build_policy(weights):
    end={(q,g):q for q,g in keys(n)};policy={}
    for depth in range(n-1,-1,-1):
        for q,g in keys(depth):
            es=[end[(successor(q,a),newg(g,depth,a))] for a in range(k)]
            vs=[int(u[es[a]][a]@weights) for a in range(k)]
            bs=[a for a in range(k) if vs[a]==max(vs)]
            if depth==0:pref=0
            elif depth==1:pref=1-next(a for a in range(k) if q[a])//5
            else:pref=g
            a=min(bs,key=lambda a:(a//5!=pref,q[a]>0,a))
            policy[q,g]=a;end[q,g]=es[a]
    return policy,end

weights=signed_weights();policy,end=build_policy(weights)
rows=[];rhs=[]
for depth in range(n):
    for q,g in keys(depth):
        a=policy[q,g];base=u[end[q,g]][a]
        for b in range(k):
            alt=u[end[successor(q,b),newg(g,depth,b)]][b]
            if np.any(alt!=base):rows.append(alt-base);rhs.append(0)
for q,g in keys(n-1):
    rows.append(-u[end[q,g]][policy[q,g]]);rhs.append(-L)
zero=(0,)*k;actual=end[zero,-1]
print(json.dumps({'rows':len(rows),'variables':len(orbits),'actual':actual,'baseline_W':float(wf[actual]@weights),'baseline_theta':min(float(u[end[q,g]][policy[q,g]]@weights/L) for q,g in keys(n-1))}),flush=True)
rr=linprog(wf[actual],A_ub=np.array(rows),b_ub=np.array(rhs),bounds=(0,None),method='highs')
print(rr.message,flush=True)
if rr.success:
    data={'ratio':rr.fun,'orbits':orbits,'weights':rr.x.tolist(),'actual':actual,'policy':{','.join(map(str,q))+':'+str(g):a for (q,g),a in policy.items()},'note':'floating discovery; current policy compressed with second-action group retained'}
    (OUT/'availability_group_probe.json').write_text(json.dumps(data,indent=2))
    print(json.dumps({'ratio':rr.fun,'support':[(orbits[i],v) for i,v in enumerate(rr.x) if v>1e-7]}),flush=True)
