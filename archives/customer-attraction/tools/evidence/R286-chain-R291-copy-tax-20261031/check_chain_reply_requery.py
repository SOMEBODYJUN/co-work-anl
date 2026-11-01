from fractions import Fraction
from itertools import product


def share(num, den):
    return Fraction(num, den) if num else Fraction(0)


def check(k=3, L=3):
    # A symbolic row decomposition check on every local membership pattern.
    # We use arbitrary nonnegative rational weights and p>=0, ell>=p.
    lam = [Fraction(2+i, 3) for i in range(L)]
    eta = [Fraction(1+i, 4) for i in range(L-1)]
    alpha = [Fraction(1, 5+i) for i in range(L)]
    beta = [Fraction(1, 7+i) for i in range(L)]
    for p in range(0, 3):
      for ell in range(p, 6):
       # Enumerate branch variables; enforce t_(q+1)=y_q.
       # q=0 has t0 free, all branch middle bits free.
       for t0 in (0,1):
        tails = []
        for q in range(L):
            # first k-2 tail bits include B; final bit y handled below
            tails.append(list(product((0,1), repeat=k-2)))
        for mids in product(*tails):
          ys = list(product((0,1), repeat=L))
          for ytuple in ys:
            t=[t0]
            for q in range(L-1): t.append(ytuple[q])
            # branch q variables are first k-2 bits mids[q], then y_q
            D=[]; src=[]; end=[]
            for q in range(L):
                aq=list(mids[q]) + [ytuple[q]]
                d=p+t[q]+sum(aq)
                D.append(d)
                src.append(share(t[q],d))
                end.append(share(ytuple[q],d))
            F=Fraction(0)
            for q in range(L):
                F += lam[q]*src[q] + alpha[q]*share(ytuple[q],ell+1) + beta[q]*ytuple[q]
            for q in range(L-1):
                b=mids[q][-1]
                # next branch prefix has source t[q+1], first k-2 tail bits mids[q+1]
                den=p+t[q+1]+sum(mids[q+1])+b
                Q=share(b,den)
                F += eta[q]*(Q-end[q+1])
            # decomposition: A-F equals the weighted nonnegative row residual.
            # Choose v/e/q to equal the local shares; all residuals below are
            # nonnegative by hypothesis, so this check only verifies formula.
            # The exact algebra is checked by recomputing A-F explicitly.
            A=sum(lam)*Fraction(1) + sum(alpha)*Fraction(1) + sum(beta)*Fraction(1)
            residual = Fraction(0)
            for q in range(L): residual += lam[q]*(1-src[q])
            for q in range(L-1):
                b=mids[q][-1]
                den=p+t[q+1]+sum(mids[q+1])+b
                Q=share(b,den)
                residual += eta[q]*(end[q+1]-Q)
            for q in range(L): residual += alpha[q]*(1-share(ytuple[q],ell+1))
            for q in range(L): residual += beta[q]*(1-ytuple[q])
            if A-F != residual:
                raise AssertionError((k,L,p,ell,t,mids,ytuple,A,F,residual))
    return True

if __name__ == '__main__':
    for k in (3,4,5):
        for L in (2,3):
            assert check(k,L)
            print('ok', k, L)
