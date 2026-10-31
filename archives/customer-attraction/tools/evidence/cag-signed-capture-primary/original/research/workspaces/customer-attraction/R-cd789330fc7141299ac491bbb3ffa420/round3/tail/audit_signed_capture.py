"""Definition-level Fraction audit of signed edges, joint refunds and capture flow.

Reuses two already complete SPE certificates. It is not a search and proves no
universal overload bound. Output is exclusively created, never overwritten.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import argparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]

def read_case(name):
    inst=json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    cert=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    strategy=cert.get('strategy',cert)
    policy={tuple(r['history']):r['action'] for r in strategy['actions']}
    customers=[frozenset(r['topics']) for r in inst['customers'] for _ in range(r['multiplicity'])]
    m=inst['players'];q=len(inst['topics'])
    def finish(h):
        h=tuple(h)
        while len(h)<m:h=h+(policy[h],)
        return h
    def pay(z,i):
        return sum((F(1,sum(a in x for a in z)) for x in customers if z[i] in x),F())
    checks=0
    for h in policy:
        z=finish(h);i=len(h)
        for a in range(q):
            assert pay(z,i)>=pay(finish(h+(a,)),i)
            checks+=1
    return inst,customers,policy,finish,pay,checks

inst,X,policy,finish,pay,source_checks=read_case('individual_security_failure')
m=inst['players'];q=len(inst['topics']);t=F(2411,246)
joint_checks=edge_checks=path_checks=0
for lam in (F(1,2),F(3,4)):
    # Exact joint identities with every actual old prefix, and any forced root.
    for depth in range(m-1):
        for h in product(range(q),repeat=depth):
            for a in range(q):
                z=finish(h+(a,));n=m-depth-1
                b=[sum(v in x for v in h) for x in X]
                p=[b0+int(a in x) for b0,x in zip(b,X)]
                c=[sum(v in x for v in z[depth+1:]) for x in X]
                rootold=sum((F(1,p0+c0) for x,p0,c0 in zip(X,p,c) if a in x),F())
                rootnew=sum((1/(F(p0)+lam*c0) for x,p0,c0 in zip(X,p,c) if a in x),F())
                gamma=rootnew-rootold
                oldB=sum((F(b0,p0+c0) for b0,p0,c0 in zip(b,p,c) if b0),F())
                dB=sum((b0/(F(p0)+lam*c0)-F(b0,p0+c0) for b0,p0,c0 in zip(b,p,c) if b0),F())
                V=sum((F(c0,p0+c0) for p0,c0 in zip(p,c) if c0),F())
                Vnew=sum((lam*c0/(F(p0)+lam*c0) for p0,c0 in zip(p,c) if c0),F())
                eta=V-n*t
                assert Vnew-lam*n*t-gamma==eta+n*(1-lam)*t-2*gamma-dB
                factor=n*(1-lam)/(1+n*lam)
                assert 2*gamma+dB<=factor*(2*rootold+oldB)
                if depth==0:
                    assert gamma<=factor*rootold
                    assert Vnew-lam*n*t-gamma>=eta+n*(1-lam)*(t-2*rootold/(1+n*lam))
                    if n*lam>=1 and rootold<=t and V>=n*t:
                        assert Vnew>=lam*n*t+gamma
                joint_checks+=1

    for root in range(q):
        def arrays(z):
            old=[pay(z,i) for i in range(m)]
            new=[old[0]]
            for i in range(1,m):
                new.append(sum((lam/(int(root in x)+lam*sum(a in x for a in z[1:]))
                                for x in X if z[i] in x),F()))
            tax=[F()]+[old[i]-new[i] for i in range(1,m)]
            assert all(k>=0 for k in tax)
            return old,new,tax
        for depth in range(1,m):
            for suffix in product(range(q),repeat=depth-1):
                h=(root,)+suffix;z=finish(h);u,pi,k=arrays(z);i=len(h)
                C=sum(k[i:],F());S=sum(u[i:],F())-(m-i)*t
                for a in range(q):
                    dz=finish(h+(a,));du,dpi,dk=arrays(dz)
                    ell=u[i]-du[i];assert ell>=0
                    gain=dpi[i]-pi[i]
                    Om=sum((dk[j]-k[j] for j in range(i+1,m)),F())
                    Pm=sum((dpi[j]-pi[j] for j in range(i+1,m)),F())
                    Xi=sum((du[j]-u[j] for j in range(i+1,m)),F())
                    dC=sum(dk[i+1:],F())-C
                    dS=sum(du[i+1:],F())-(m-i-1)*t-S
                    assert gain==k[i]-dk[i]-ell
                    assert gain+dC==Om-dk[i]-ell
                    assert Xi==dS+u[i]-t and Om==Xi-Pm
                    assert gain+dC-dS==dpi[i]-t-Pm
                    edge_checks+=1
        for suffix in product(range(q),repeat=m-1):
            h=(root,);initialC=sum(arrays(finish(h))[2][1:],F())
            totalgain=totalOm=totalknew=totalell=F()
            for a in suffix:
                i=len(h);u,pi,k=arrays(finish(h));du,dpi,dk=arrays(finish(h+(a,)))
                totalgain+=dpi[i]-pi[i]
                totalOm+=sum((dk[j]-k[j] for j in range(i+1,m)),F())
                totalknew+=dk[i];totalell+=u[i]-du[i]
                h=h+(a,)
            assert totalgain==initialC+totalOm-totalknew-totalell
            path_checks+=1

# One existing full SPE checks capture propagation and a genuine row overload.
inst,X,policy,finish,pay,matching_checks=read_case('portfolio_matching_failure')
m=inst['players'];q=len(inst['topics']);actual=finish(())
C={x for x in range(len(X)) if any(a in X[x] for a in actual)}
optimal=(1,3)
O={x for x in range(len(X)) if any(a in X[x] for a in optimal)}
R=O-C;G=C-O;u=[pay(actual,i) for i in range(m)]
incoming=defaultdict(F)
for x in R:
    owner=next(i for i,a in enumerate(optimal) if a in X[x])
    incoming[owner,optimal[owner],x]+=1
absorbed=defaultdict(F);A=defaultdict(F)
for i in range(m):
    for a in range(q):
        z=finish(actual[:i]+(a,))
        for x in R:
            mass=incoming[i,a,x]
            if not mass:continue
            assert a in X[x]
            covering=[j for j in range(i,m) if z[j] in X[x]]
            assert i in covering
            piece=mass/len(covering)
            A[i,a]+=piece;absorbed[x]+=piece
            for j in covering:
                if j!=i:incoming[j,z[j],x]+=piece
assert all(absorbed[x]==1 for x in R)
assert sum(A.values(),F())==len(R)
owner_of={x:next(i for i,a in enumerate(optimal) if a in X[x]) for x in O}
for x in R:
    o=owner_of[x]
    for i in range(o+1,m):
        assert sum((incoming[i,a,x] for a in range(q)),F())<=F(1,2)

def formal_phi(z):
    total=F()
    for x,likes in enumerate(X):
        c=sum(a in likes for a in z if a is not None)
        if x not in O:
            total+=sum((F(1,j) for j in range(1,c+1)),F())
        elif z[owner_of[x]] not in likes:
            total-=F(1,c+1)
    return total

rows=[F() for _ in range(m)];weightedslack=F();states=[]
nonpositive_high_weight_nodes=0
for (i,a),value in sorted(A.items()):
    z=finish(actual[:i]+(a,));d=pay(z,i)
    assert d>0
    w=value/d
    rows[i]+=w;weightedslack+=w*(u[i]-d)
    ell_by_x={};error_by_x={}
    for x,likes in enumerate(X):
        if a not in likes:continue
        c=sum(b in likes for b in z)
        r=F(1,c)
        if x not in O:ell=r
        elif i==owner_of[x]:ell=r
        elif z[owner_of[x]] in likes:ell=F()
        else:ell=F(1,c*(c+1))
        ell_by_x[x]=ell;error_by_x[x]=r-ell
    ell=sum(ell_by_x.values(),F());E=sum(error_by_x.values(),F())
    deleted=list(z);deleted[i]=None
    assert formal_phi(z)<=0
    assert ell==formal_phi(z)-formal_phi(deleted)
    assert ell+E==d
    ER=sum((error_by_x.get(x,F()) for x in R),F())
    EI=sum((error_by_x.get(x,F()) for x in O&C),F())
    assert E==ER+EI
    client_ell=sum((incoming[i,a,x]*ell_by_x.get(x,F()) for x in R),F())
    client_error=sum((incoming[i,a,x]*error_by_x.get(x,F()) for x in R),F())
    covariance=w*ell-client_ell
    assert covariance==client_error-w*E
    upper=(F(1,2)-w)*ER-w*EI
    assert covariance<=upper
    if w>=F(1,2):
        assert covariance<=0
        nonpositive_high_weight_nodes+=1
    states.append({'position':i+1,'action':inst['topics'][a],
                   'absorption':str(value),'real_query_profit':str(d),
                   'weight':str(w),'formal_marginal':str(ell),
                   'owner_error_R':str(ER),'owner_error_I':str(EI),
                   'scalarization_covariance':str(covariance),
                   'covariance_upper':str(upper)})
cost=sum((rows[i]*u[i] for i in range(m)),F())
assert cost==len(R)+weightedslack
assert rows==[F(35,38),F(49,44)]
assert cost==F(1701,38)
assert cost<=len(C)+len(G)
out={'scope':'definition-level checks only; no universal row-overload bound',
     'source_individual34_original_IC_checks':source_checks,
     'joint_refund_checks':joint_checks,'signed_edge_checks':edge_checks,
     'arbitrary_deviation_path_checks':path_checks,
     'capture_flow':{'source':'existing portfolio_matching_failure, 86 clients',
                     'original_IC_checks':matching_checks,'actual':list(actual),
                     'optimal':list(optimal),'W':len(C),'R':len(R),'G':len(G),
                     'absorbed_total':str(sum(A.values(),F())),
                     'states':states,'row_loads':list(map(str,rows)),
                     'paid_cost':str(cost),'weighted_original_IC_slack':str(weightedslack),
                     'high_weight_nonpositive_covariance_nodes':nonpositive_high_weight_nodes,
                     'interpretation':'L2>1 is real; G and signed credit cannot be omitted'}}
parser=argparse.ArgumentParser()
parser.add_argument('--output',help='new output filename in this workspace; existing files are refused')
args=parser.parse_args()
if args.output:
    destination=(HERE/args.output).resolve()
    assert destination.parent==HERE.resolve()
    with destination.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in out.items() if k!='capture_flow'},indent=2))
print(json.dumps(out['capture_flow'],indent=2))
