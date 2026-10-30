"""Exact finite checks for the DAG endpoint-leakage degree budget.

All rational z>1 are paired with epsilon=z**(-degree), so root extractions
are avoided. These tests corroborate algebra; they do not prove the theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
import argparse
import hashlib
import platform
from pathlib import Path


def paths(n, edges):
    out=[[] for _ in range(n)]
    for u,v in edges: out[u].append(v)
    # p[u][k] is the number of k-vertex paths beginning at u.
    p=[[0]*(n+1) for _ in range(n)]
    for u in range(n-1,-1,-1):
        p[u][1]=1
        for v in out[u]:
            for k in range(1,n): p[u][k+1]+=p[v][k]
    return out,[sum(p[u][k] for u in range(n)) for k in range(1,n+1)]


def min_weights(n,out,z):
    w=[F(0) for _ in range(n)]
    for u in range(n-1,-1,-1):
        w[u]=z-1+z*sum((w[v] for v in out[u]),F(0))
    return w


def poly(a,x): return sum((c*x**k for k,c in enumerate(a)),F(0))


counts={"graphs":0,"graph_z_cases":0,"degree_endpoint_cases":0,
        "arbitrary_positive_weights":0,"polynomial_cases":0,
        "q_comparison_cases":0,"strict_boundary_cases":0,
        "slack_vector_cases":0,"quadratic_boundary_cases":0}
examples=[]
zs=[F(101,100),F(11,10),F(3,2),F(2)]
degrees=[1,2,5,20]
for n in range(1,6):
    possible=list(combinations(range(n),2))
    for bits in product((0,1),repeat=len(possible)):
        edges=[e for e,b in zip(possible,bits) if b]
        out,P=paths(n,edges)
        counts['graphs']+=1
        for z in zs:
            w=min_weights(n,out,z)
            total=sum(w,F(0)); tau=z-1
            S=sum((F(pk)*z**k for k,pk in enumerate(P)),F(0))
            assert total==tau*S
            assert all(w[u]-sum((w[v] for v in out[u]),F(0))>0 for u in range(n))
            feasible=z*tau*S<=1
            assert feasible==(total<=1/z)
            for d in degrees:
                eps=z**(-d)
                # Every satellite is exactly at the endpoint leakage ratio.
                for u in range(n):
                    L=1+sum((w[v] for v in out[u]),F(0))
                    H=1+w[u]
                    assert H==z*L and (L/H)**d==eps
                assert (total**d<=eps)==feasible
                counts['degree_endpoint_cases']+=1
            # Test arbitrary positive perturbations of minimum weights by
            # propagating strictly positive slack in reverse topological order.
            for slack in (F(0),F(1,100),F(1,3)):
                wp=[F(0) for _ in range(n)]
                for u in range(n-1,-1,-1):
                    wp[u]=tau+z*sum((wp[v] for v in out[u]),F(0))+slack*(u+1)
                assert all(wp[u]>=w[u] for u in range(n))
                assert sum(wp,F(0))>=tau*S
                # The exact residual vector b=(I-zA)w-tau*1 and its
                # propagated contribution have the stated nonnegative form.
                b=[wp[u]-z*sum((wp[v] for v in out[u]),F(0))-tau for u in range(n)]
                assert b==[slack*(u+1) for u in range(n)]
                extra=[F(0) for _ in range(n)]
                for u in range(n-1,-1,-1):
                    extra[u]=b[u]+z*sum((extra[v] for v in out[u]),F(0))
                assert [wp[u]-w[u] for u in range(n)]==extra
                assert (not any(b))==(sum(extra,F(0))==0)
                assert (sum(wp,F(0))<=1/z)==(sum(extra,F(0))<=1/z-tau*S)
                counts['slack_vector_cases']+=1
                counts['arbitrary_positive_weights']+=1
            # At any rational comparison r>=1, the path contribution bound
            # implies the asserted q bound whenever its quadratic premise holds.
            B=1/(z*tau)
            for r in (F(1),F(3,2),F(2),F(3),F(10),F(100)):
                lhs=r*(r-1)
                weighted=sum((F(pk)*r**(-k) for k,pk in enumerate(P)),F(0))
                assert weighted<=S
                if feasible and lhs>=B:
                    q_rhs=1+sum((F(pk)*r**(-k-1) for k,pk in enumerate(P)),F(0))
                    assert q_rhs<=r
                counts['q_comparison_cases']+=1
            if feasible and len(examples)<3:
                examples.append({'n':n,'edges':edges,'z':str(z),'weights':list(map(str,w)),
                                 'P':P,'total':str(total),'budget':str(z*tau*S)})
            counts['graph_z_cases']+=1
# Monomial dominance for genuinely mixed nonnegative polynomials,
# including constant terms and high-degree leading coefficients equal to zero.
for d in range(1,8):
    for aa in product((0,1,3),repeat=d+1):
        if not any(aa): continue
        for L,H in ((F(1,3),F(1)),(F(1),F(3,2)),(F(11,10),F(2))):
            assert poly(aa,L)*H**d>=poly(aa,H)*L**d
            counts['polynomial_cases']+=1
# An exact endpoint example, neither an epsilon=1 nor an illicit zero-shape case:
# edgeless n=2, z=3/2 has z(z-1)*n=3/2>1 and is impossible;
# n=1,z=3/2 is feasible with weight1/2 and root leakage strictly below epsilon.
for n,z,ok in ((1,F(3,2),True),(2,F(3,2),False),(2,F(5,4),True)):
    out,P=paths(n,[]); w=min_weights(n,out,z)
    assert (sum(w,F(0))<=1/z)==ok
    counts['strict_boundary_cases']+=1
# Exact algebraic equality boundary for a one-vertex graph. A Q(sqrt(5))
# pair (a,b) represents a+b*sqrt(5); no floating comparisons or roots occur.
def q5mul(x,y):
    a,b=x; c,e=y
    return (a*c+5*b*e,a*e+b*c)
def q5pow(x,k):
    if k<0:
        a,b=x; norm=a*a-5*b*b
        return q5pow((a/norm,-b/norm),-k)
    y=(F(1),F(0))
    for _ in range(k): y=q5mul(y,x)
    return y
phi=(F(1,2),F(1,2)); inv_phi=(F(-1,2),F(1,2))
assert q5mul(phi,inv_phi)==(F(1),F(0))
for d in degrees:
    # z=phi, w=z-1=1/z, S=1: both endpoint tests attain equality.
    eps=q5pow(phi,-d)
    assert q5pow(inv_phi,d)==eps
    assert q5mul(q5pow(phi,d),eps)==(F(1),F(0))
    counts['quadratic_boundary_cases']+=1
result = {'status':'passed','arithmetic':'fractions.Fraction and exact Q(sqrt(5)) pairs',
                  'parameters':{'topological_vertex_counts':[1,2,3,4,5],
                                'z_values':list(map(str,zs)),'degrees':degrees,
                                'seed':None,'randomization':'none; exhaustive finite products'},
                  'scope':'finite implementation checks; no general proof inference',
                  'counts':counts,'examples':examples}
result.update(python=platform.python_version(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
parser=argparse.ArgumentParser(description=__doc__)
group=parser.add_mutually_exclusive_group()
group.add_argument('--output',type=Path)
group.add_argument('--check',type=Path)
args=parser.parse_args()
if args.output:
    with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
elif args.check:
    assert json.loads(args.check.read_text()) == result, 'Recomputation differs from frozen record'
else:
    print(json.dumps(result,ensure_ascii=False,indent=2))
if args.output or args.check: print(json.dumps({k:result[k] for k in ('status','counts','code_sha256')}))
