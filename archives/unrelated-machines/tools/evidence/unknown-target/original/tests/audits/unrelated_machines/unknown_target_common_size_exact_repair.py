from fractions import Fraction
from collections import deque

# Exact tiny audit of the common-size threshold predicate.
def feasible(f, q, elig, B):
    m=len(f); n=len(elig)
    if B < max(f, default=Fraction(0)):
        return False
    cap=[max(0,(B-f[i])//q) for i in range(m)]
    # augmenting-path bipartite matching with machine capacities
    match=[[] for _ in range(m)]
    for j in range(n):
        seen=set(); parent={j:None}; Q=deque([j]); end=None
        while Q and end is None:
            u=Q.popleft()
            for i in elig[u]:
                if i in seen or len(match[i])>=cap[i]:
                    continue
                seen.add(i); end=i; break
                
            if end is None:
                for i in elig[u]:
                    for v in match[i]:
                        if v not in parent:
                            parent[v]=u; Q.append(v)
        if end is None:
            return False
        # Reconstruct by swapping along parent; compact capacity matching via DFS fallback
    # use maxflow-style DFS for robustness
    match=[[] for _ in range(m)]
    def aug(j,seen):
        for i in elig[j]:
            if i in seen: continue
            seen.add(i)
            if len(match[i])<cap[i]: match[i].append(j); return True
            for old in list(match[i]):
                if aug(old,seen):
                    match[i].remove(old); match[i].append(j); return True
        return False
    return all(aug(j,set()) for j in range(n))

def brute_opt(f,q,elig):
    n=len(elig); best=None
    def rec(j,loads):
        nonlocal best
        if j==n:
            v=max(loads,default=Fraction(0))
            best=v if best is None or v<best else best; return
        for i in elig[j]:
            loads[i]+=q; rec(j+1,loads); loads[i]-=q
    rec(0,list(f)); return best

# common size, disconnected components, and zero jobs
cases=[
    ([Fraction(1),Fraction(0)],Fraction(1),[[0,1],[1]],Fraction(1)),
    ([Fraction(1,3),Fraction(2,3)],Fraction(1,6),[[0],[0,1],[1]],None),
    # Frozen core may exceed B even when every new job fits elsewhere.
    ([Fraction(2),Fraction(0)],Fraction(1),[[1]],Fraction(2)),
    # Empty new-job set still has to pay the largest frozen-core load.
    ([Fraction(2),Fraction(0)],Fraction(1),[],Fraction(2)),
]
for f,q,e,_ in cases:
    opt=brute_opt(f,q,e)
    S=sorted({f[i]+q*t for i in range(len(f)) for t in range(len(e)+1)})
    assert next(B for B in S if feasible(f,q,e,B))==opt
    for B in S:
        assert feasible(f,q,e,B) == (opt <= B)
print('ok')
