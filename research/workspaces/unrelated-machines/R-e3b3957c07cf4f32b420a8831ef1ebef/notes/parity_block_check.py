from itertools import product, combinations
from fractions import Fraction

def inst(d,s=1):
    X=[(g,a) for g in range(s) for a in (0,1)]
    labels=[]
    for g,a in X:
        for b in product((0,1), repeat=d):
            if (a+sum(b))%2==1:
                S={(g,j,b[j]) for j in range(d)}
                labels.append((g,a,b,S))
    return X,labels

def nu_t(d,s,t):
    X,L=inst(d,s)
    byx={x:[] for x in X}
    for g,a,b,S in L:
        byx[(g,a)].append(S)
    best=0
    for r in range(1,len(X)+1):
      for xs in combinations(X,r):
        def rec(k,used):
          if k==len(xs): return True
          x=xs[k]
          for S in byx[x]:
            for B in combinations(S,t):
              B=set(B)
              if used.isdisjoint(B) and rec(k+1,used|B): return True
          return False
        if rec(0,set()): best=r
    return best

if __name__=='__main__':
  for d in [2,4,6]:
    for s in [1,2]:
      q=2*s
      vals=[nu_t(d,s,t) for t in range(1,d+1)]
      b=max(min(Fraction(v,q),Fraction(t,d)) for t,v in enumerate(vals,1))
      print(f'd={d},s={s}: nu={vals}, b={b}, OPT={2-b}')
