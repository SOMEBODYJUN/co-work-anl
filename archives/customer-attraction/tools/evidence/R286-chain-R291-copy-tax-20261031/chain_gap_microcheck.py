from fractions import Fraction
from itertools import product

def sh(n,d): return Fraction(n,d) if n else Fraction(0)
def minimum(k,L,p,ell,lam,eta,alpha,beta,link):
    out=None; arg=None
    for ts in product((0,1), repeat=L):
      for mids in product(list(product((0,1), repeat=k-2)), repeat=L):
       for ys in product((0,1), repeat=L):
        if link and any(ts[q+1] != ys[q] for q in range(L-1)): continue
        Ds=[]; src=[]; end=[]
        for q in range(L):
          d=p+ts[q]+sum(mids[q])+ys[q]
          Ds.append(d); src.append(sh(ts[q],d)); end.append(sh(ys[q],d))
        f=sum(lam[q]*src[q]+alpha[q]*sh(ys[q],ell+1)+beta[q]*ys[q] for q in range(L))
        for q in range(L-1):
          b=mids[q][-1]
          f += eta[q]*(sh(b,p+ts[q+1]+sum(mids[q+1])+b)-end[q+1])
        if out is None or f<out: out,arg=f,(ts,mids,ys)
    return out,arg

# A strict identity gain for k=3, L=3. The free minimum separately
# eliminates each source-reply identity; the linked minimum retains it.
k,L,p,ell=3,3,0,0
lam=[Fraction(1),Fraction(3),Fraction(2)]
eta=[Fraction(4),Fraction(1)]
alpha=[Fraction(1)]*3
beta=[Fraction(1)]*3
linked,la=minimum(k,L,p,ell,lam,eta,alpha,beta,True)
free,fa=minimum(k,L,p,ell,lam,eta,alpha,beta,False)
assert linked == -1 and free == -2 and linked > free
print({'linked': str(linked), 'free': str(free), 'gap': str(linked-free),
       'linked_arg': la, 'free_arg': fa})
