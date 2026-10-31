"""Independent exact audit of the two fixed-leaf owner transport statements.

No author code or SPE solver is imported.  The universal proof is a cut proof;
these finite cases check zero-load branches, all-J polynomial integrals and
separate rational augmenting-path feasibility of both networks.
"""
from collections import deque
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json


def H(c):
    return sum((F(1,k) for k in range(1,c+1)),F(0))


def union(profile):
    z=0
    for b in profile:
        z |= b
    return z


def maxflow(cap, source, sink):
    n=len(cap)
    residual=[r[:] for r in cap]
    total=F(0)
    while True:
        parent=[-1]*n
        parent[source]=source
        queue=deque([source])
        while queue and parent[sink]<0:
            v=queue.popleft()
            for w in range(n):
                if parent[w]<0 and residual[v][w]>0:
                    parent[w]=v
                    queue.append(w)
        if parent[sink]<0:
            return total
        v=sink
        path=[]
        while v!=source:
            path.append((parent[v],v))
            v=parent[v]
        delta=min(residual[v][w] for v,w in path)
        for v,w in path:
            residual[v][w]-=delta
            residual[w][v]+=delta
        total+=delta


# Arbitrary finite cases serve only the explicit all-input transport statements.
# Theme bitmasks encode individual, unit customers, with empty/duplicate labels.
CASES=[
    ("empty",1,(0,),(0,)),
    ("one-slot-outside",1,(0,1,2),(1,)),
    ("one-slot-cross",1,(3,5,10),(3,)),
    ("A-needs-role-edge",2,(3,12,20),(3,12)),
    ("overlap-owner-choice",2,(7,28,42),(7,28)),
    ("duplicate-labels",2,(0,0,3,3),(3,3)),
    ("three-owners",3,(3,12,48,69),(3,12,48)),
    ("repeated-optimal-slots",3,(0,3,5),(3,5,3)),
    ("four-owners",4,(3,12,48,192,277),(3,12,48,192)),
]

counts=dict(instances=0,owner_partitions=0,profiles=0,cuts=0,
            polynomial_integrals=0,maxflow_A=0,maxflow_B=0,
            zero_covered_O_customers=0,covered_missing_owner_customers=0,
            zero_outside_customer_terms=0)
summaries=[]
for name,m,topics,T in CASES:
    O=union(T)
    assert O.bit_count()==max(union(B).bit_count() for B in product(topics,repeat=m))
    universe=union(topics)
    N=range(universe.bit_length())
    Oclients=[x for x in N if (O>>x)&1]
    choices={x:[i for i,t in enumerate(T) if (t>>x)&1] for x in Oclients}
    owner_vectors=set()
    for selector in (lambda x,v:v[0],lambda x,v:v[-1],lambda x,v:v[x%len(v)]):
        owner_vectors.add(tuple(selector(x,choices[x]) for x in Oclients))
    counts['instances']+=1
    before=counts['profiles']
    for vector in owner_vectors:
        counts['owner_partitions']+=1
        owner=dict(zip(Oclients,vector))
        Q=[0]*m
        for x,o in owner.items():
            Q[o]|=1<<x
        assert union(Q)==O
        assert all((q&t)==q for q,t in zip(Q,T))
        for B in product(topics,repeat=m):
            counts['profiles']+=1
            C={x:[i for i,b in enumerate(B) if (b>>x)&1] for x in N}
            c={x:len(C[x]) for x in N}
            E=[x for x in Oclients if owner[x] not in C[x]]
            counts['zero_covered_O_customers']+=sum(c[x]==0 for x in Oclients)
            counts['covered_missing_owner_customers']+=sum(c[x]>0 for x in E)
            outside=[x for x in N if not ((O>>x)&1)]
            counts['zero_outside_customer_terms']+=sum(c[x]==0 for x in outside)
            sourceA=[sum((F(1,c[x]) for x in outside if i in C[x]),F(0)) for i in range(m)]
            sourceB=[sum((H(c[x])/c[x] for x in outside if i in C[x]),F(0)) for i in range(m)]
            A=[[F(0) for j in range(m+2)] for i in range(m+2)]
            Bnet=[[F(0) for j in range(m+2)] for i in range(m+2)]
            s,t=m,m+1
            for i in range(m):
                A[s][i]=sourceA[i]
                Bnet[s][i]=sourceB[i]
            for x in Oclients:
                o=owner[x]
                if c[x]==0:
                    A[o][t]+=1
                else:
                    for i in C[x]:
                        if i!=o:
                            A[o][i]+=F(1,c[x])
                if x in E:
                    Bnet[o][t]+=F(1,c[x]+1)
                    for i in C[x]:
                        assert i!=o
                        Bnet[o][i]+=F(1,c[x]+1)
            for mask in range(1<<m):
                J=[i for i in range(m) if (mask>>i)&1]
                Jin=set(J)
                counts['cuts']+=1
                k={x:sum(i in Jin for i in C[x]) for x in N}
                M=[x for x in Oclients if owner[x] in Jin and k[x]==0]
                outside_union=sum(k[x]>0 for x in outside)
                assert outside_union<=len(M)
                hleft=sum((H(k[x]) for x in outside),F(0))
                hright=sum((F(1,1+k[x]) for x in E if owner[x] in Jin),F(0))
                assert hleft<=hright
                # Integrate the directly enumerated nonnegative hybrid slack.
                coeff=[0]*(len(J)+1)
                for chosen_mask in range(1<<len(J)):
                    chosen={J[j] for j in range(len(J)) if (chosen_mask>>j)&1}
                    mixed=tuple(B[i] if i in chosen else Q[i] for i in range(m))
                    deficit=O.bit_count()-union(mixed).bit_count()
                    assert deficit>=0
                    z=len(chosen)
                    for r in range(len(J)-z+1):
                        coeff[z+r]+=deficit*((-1)**r)*comb(len(J)-z,r)
                assert coeff[0]==0
                integral=sum((F(v,d) for d,v in enumerate(coeff) if d),F(0))
                assert integral==hright-hleft
                counts['polynomial_integrals']+=1
                cutA=sum((A[i][j] for i in J for j in range(m+2) if j not in Jin and j!=s),F(0))
                cutB=sum((Bnet[i][j] for i in J for j in range(m+2) if j not in Jin and j!=s),F(0))
                supplyA=sum((sourceA[i] for i in J),F(0))
                supplyB=sum((sourceB[i] for i in J),F(0))
                assert supplyA<=outside_union<=len(M)<=cutA
                assert supplyB<=hleft<=hright<=cutB
                for x in E:
                    if owner[x] in Jin:
                        l=c[x]-k[x]
                        assert F(1+l,1+k[x]+l)-F(1,1+k[x])==F(k[x]*l,(1+k[x]+l)*(1+k[x]))
            assert maxflow(A,s,t)==sum(sourceA,F(0))
            assert maxflow(Bnet,s,t)==sum(sourceB,F(0))
            counts['maxflow_A']+=1
            counts['maxflow_B']+=1
    summaries.append(dict(name=name,players=m,topics=list(topics),optimal_tuple=list(T),
                          owner_choices=len(owner_vectors),profiles=counts['profiles']-before))

out=dict(status='PASS',scope='finite exact implementation audit; universal proof is analytic',
         counts=counts,cases=summaries)
target=Path(__file__).with_suffix('.json')
assert not target.exists(),f'refuse overwrite {target}'
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
