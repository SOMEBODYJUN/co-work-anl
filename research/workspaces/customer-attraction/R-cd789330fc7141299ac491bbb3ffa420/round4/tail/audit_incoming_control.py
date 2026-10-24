"""One old complete SPE audits freely reassigned incoming controls.

Fraction arithmetic; no solver, no new instance, no catalogue/strategy search.
It checks the new route's dominance and predictable activation identities, not
any universal capacity bound. Existing outputs are never overwritten.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
from functools import lru_cache
import argparse
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
name='global_decorrelation_failure'
inst=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
policy={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
X=[frozenset(r['topics']) for r in inst['customers'] for _ in range(r['multiplicity'])]
m=inst['players'];k=len(inst['topics'])
def finish(h):
    h=tuple(h)
    while len(h)<m:h=h+(policy[h],)
    return h
def pay(z,i):
    return sum((F(1,sum(a in x for a in z)) for x in X if z[i] in x),F())
checks=0
for h in policy:
    z=finish(h);i=len(h)
    for a in range(k):
        assert pay(z,i)>=pay(finish(h+(a,)),i)
        checks+=1
actual=finish(())
u=[pay(actual,i) for i in range(m)]
C={x for x in range(len(X)) if any(a in X[x] for a in actual)}
covered=lambda z:{x for x in range(len(X)) if any(a in X[x] for a in z)}
best=max(len(covered(z)) for z in combinations_with_replacement(range(k),m))
# One fixed optimal order deliberately exposes the known shared omitted type
# {3,4} at source 4, whose natural reply later uses 3. No policy/weight search.
T=(4,0,2,3)
assert len(T)==m and len(covered(T))==best
O=covered(T);R=O-C;G=C-O
owner={x:next(i for i,a in enumerate(T) if a in X[x]) for x in O}
Y={(i,a):finish(actual[:i]+(a,)) for i in range(m) for a in range(k)}
D={(i,a):pay(Y[i,a],i) for i in range(m) for a in range(k)}
followers={(i,a,x):tuple(j for j in range(i+1,m) if Y[i,a][j] in X[x])
           for i in range(m) for a in range(k) for x in R if a in X[x]}

@lru_cache(None)
def natural(i,a,x):
    foll=followers[i,a,x];c=1+len(foll)
    return (u[i]/D[i,a]+sum((natural(j,Y[i,a][j],x) for j in foll),F()))/c

value={};choice={};forced={}
for i in range(m-1,-1,-1):
    for x in R:
        options=[]
        for a in X[x]:
            f=len(followers[i,a,x])
            selected=tuple(sorted(sorted(range(i+1,m),key=lambda j:(value[j,x],j))[:f]))
            v=(u[i]/D[i,a]+sum((value[j,x] for j in selected),F()))/(1+f)
            forced[i,a,x]=(v,selected)
            options.append((v,a,selected))
        v,a,selected=min(options)
        assert v>=1
        value[i,x]=v;choice[i,x]=(a,selected)

rows=[];free_abs=defaultdict(F);plain_in=defaultdict(F)
for x in sorted(R):
    i=owner[x];a=T[i]
    v,selected=forced[i,a,x]
    old=natural(i,a,x)
    assert v<=old
    incoming=defaultdict(F);incoming[i,a]=F(1)
    paid=absorption=F()
    for j in range(i,m):
        for b in range(k):
            q=incoming[j,b]
            if not q:continue
            if (j,b)==(i,a):outlets=selected
            else:
                chosen,outlets=choice[j,x]
                assert b==chosen
            f=len(followers[j,b,x]);assert len(outlets)==f
            piece=q/(f+1)
            paid+=piece*u[j]/D[j,b];absorption+=piece
            free_abs[j,b]+=piece;plain_in[j,x]+=q
            for nxt in outlets:
                incoming[nxt,choice[nxt,x][0]]+=piece
    assert absorption==1 and paid==v
    for j in range(i+1,m):assert plain_in[j,x]<=F(1,2)
    rows.append({'unit_customer':x,'likes':sorted(X[x]),'owner_role':i+1,
                 'source_action':a,'natural_price':str(old),
                 'free_price':str(v),'saved':str(old-v),
                 'source_surrogate_roles':[j+1 for j in selected]})

# Exact probability polynomials for the same prechosen surrogate outlets.
def add(a,b):
    ans=[F()] * max(len(a),len(b))
    for j,v in enumerate(a):ans[j]+=v
    for j,v in enumerate(b):ans[j]+=v
    return ans
def mul(a,b):
    ans=[F()] * (len(a)+len(b)-1)
    for i,u0 in enumerate(a):
        for j,v in enumerate(b):ans[i+j]+=u0*v
    return ans
def omp(n):
    ans=[F(1)]
    for _ in range(n):ans=mul(ans,[F(1),F(-1)])
    return ans
def integral(a):return sum((v/F(j+1) for j,v in enumerate(a)),F())

activation=[];act_abs=defaultdict(F);beta_checks=0
for x in sorted(R):
    i=owner[x];a=T[i];_,source_outlets=forced[i,a,x]
    visits=defaultdict(lambda:[F()]);visits[i,a]=[F(1)]
    total=fee=F();entry_by_role=[F() for _ in range(m)]
    for j in range(i,m):
        for b in range(k):
            z=visits[j,b]
            if not any(z):continue
            if (j,b)==(i,a):outlets=source_outlets
            else:
                chosen,outlets=choice[j,x];assert b==chosen
            f=len(followers[j,b,x]);assert len(outlets)==f
            amount=integral(mul(z,omp(f)))
            assert amount>=0
            total+=amount;fee+=amount*u[j]/D[j,b]
            act_abs[j,b]+=amount;entry_by_role[j]+=integral(z)
            if j>i:
                assert amount<=F(1,(f+1)*(f+2))
                beta_checks+=1
            for rank,nxt in enumerate(outlets):
                trans=mul([F(),F(1)],omp(rank))
                bnext=choice[nxt,x][0]
                visits[nxt,bnext]=add(visits[nxt,bnext],mul(z,trans))
    assert total==1
    for j in range(i+1,m):assert entry_by_role[j]<=F(1,2)
    activation.append({'unit_customer':x,'total_absorption':str(total),
                       'whole_IC_fee':str(fee),
                       'integrated_entries':list(map(str,entry_by_role))})

def role_cost(absorptions):
    w=[F() for _ in range(m)]
    for (i,a),v in absorptions.items():w[i]+=v/D[i,a]
    return [w[i]*u[i] for i in range(m)]
source_cost=sum((F(1,1+len(followers[owner[x],T[owner[x]],x]))
                 *u[owner[x]]/D[owner[x],T[owner[x]]] for x in R),F())
nat_total=sum((F(row['natural_price']) for row in rows),F())
free_total=sum((F(row['free_price']) for row in rows),F())
assert sum(role_cost(free_abs),F())==free_total
out={'scope':'one old complete SPE; new control implementation only; no universal incoming bound',
     'instance':name,'customers':len(X),'players':m,'original_IC_checks':checks,
     'actual':list(actual),'payoffs':list(map(str,u)),'W':len(C),
     'optimal_tuple':list(T),'OPT':best,'R':len(R),'G':len(G),
     'source_cost_unchanged':str(source_cost),'prices':rows,
     'natural_total':str(nat_total),'free_total':str(free_total),
     'strict_price_improvement':free_total<nat_total,
     'free_role_cost':list(map(str,role_cost(free_abs))),
     'activation_beta_checks':beta_checks,'activation':activation,
     'activation_role_cost':list(map(str,role_cost(act_abs)))}
parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
if args.output:
    dest=(HERE/args.output).resolve();assert dest.parent==HERE
    with dest.open('x') as file:json.dump(out,file,indent=2);file.write('\n')
print(json.dumps(out,indent=2))
