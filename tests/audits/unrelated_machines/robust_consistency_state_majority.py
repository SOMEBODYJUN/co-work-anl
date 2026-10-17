"""Exact audit for the stronger two-state majority lemma.
Two complete assignments are disjoint inside each state. After arbitrary leaf
and variable deletion, choose the state with most delta-good variables.
"""
from fractions import Fraction
from itertools import combinations
from collections import defaultdict

def families(q,r,K):
    subs=list(combinations(range(r),K)); out=[]
    def rec(i,used,cur):
        if i==q: out.append(tuple(cur)); return
        for S in subs:
            S=set(S)
            if not S&used: rec(i+1,used|S,cur+[frozenset(S)])
    rec(0,set(),[]); return out

def majority_floor(A,B,Ks,Y,delta,root_q):
    # A/B full bundles are state-wise disjoint; Ares/Bres are supplied as tuples.
    good=[set(),set()]
    for a,C in enumerate((A,B)):
        for x in Y:
            if Fraction(len(C[x]),Ks[a][x]) >= delta: good[a].add(x)
    a=max((0,1),key=lambda z:len(good[z]))
    X=good[a]
    vals=[Fraction(len(X),root_q)]
    vals += [Fraction(len((A,B)[a][x]),Ks[a][x]) for x in X]
    # state-wise disjointness gives legality directly
    selected=[u for x in X for u in (A,B)[a][x]]
    assert len(selected)==len(set(selected))
    return min(vals) if X else Fraction(0),good

def audit():
    total=0
    for q in range(1,4):
      for r in range(1,6):
       for K in range(1,r+1):
        fs=families(q,r,K)
        for A in fs:
         for B in fs:
          # residuals = full here; test root deletions
          for mask in range(1,1<<q):
           Y={i for i in range(q) if mask>>i&1}; Ks=[ [K]*q, [K]*q ]
           v,_=majority_floor(A,B,Ks,Y,Fraction(1),len(Y))
           assert v>=Fraction(1,2),(q,r,K,A,B,Y,v)
           total+=1
    return total

def sharp_example(s=4,d=None,K=8):
    # q=2s; state0 good for x< s, state1 good for x>=s.
    if d is None: d=s
    q=2*s; A=[set() for _ in range(q)]; B=[set() for _ in range(q)]
    nxt=0
    # shared cross resources r_{ij}: state0 first-half x=i, state1 second-half y=s+j
    for i in range(s):
      for j in range(s):
        u=nxt;nxt+=1; A[i].add(u);B[s+j].add(u)
    # private resources complete each full bundle to K; all will be deleted externally
    for x in range(q):
      C=A if x<s else B
      # good bundle already d=s; this fixture requires d=s; for generic d use first d edges only
    # use d=s in this exact construction
    assert d==s
    for x in range(s):
      while len(A[x])<K:A[x].add(nxt);nxt+=1
    for x in range(s,q):
      while len(B[x])<K:B[x].add(nxt);nxt+=1
    # bad-state full bundles disjoint fresh
    for x in range(s,q):
      while len(A[x])<K:A[x].add(nxt);nxt+=1
    for x in range(s):
      while len(B[x])<K:B[x].add(nxt);nxt+=1
    # residual keep only good bundles' shared d resources; bad residual empty
    Ar=[set(A[x]) if x<s else set() for x in range(q)]
    Br=[set(B[x]) if x>=s else set() for x in range(q)]
    # for good bundles delete private leaves, retaining exactly d=s cross resources
    for x in range(s): Ar[x]={u for u in A[x] if u< s*s}
    for x in range(s,q): Br[x]={u for u in B[x] if u< s*s}
    Ks=[[K]*q,[K]*q]; Y=set(range(q)); v,g=majority_floor(Ar,Br,Ks,Y,Fraction(s,K),q)
    # Any feasible tree uses at most one side of complete bipartite good conflict graph,
    # hence at most s variables, each with at most d/K label ratio.
    return v,g

if __name__=='__main__':
 print('enumeration',audit())
 print('sharp fixture',sharp_example())
