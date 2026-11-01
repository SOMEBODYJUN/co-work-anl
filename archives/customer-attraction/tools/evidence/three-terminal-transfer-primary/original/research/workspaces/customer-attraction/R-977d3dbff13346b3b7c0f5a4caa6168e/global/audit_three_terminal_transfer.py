"""Exact certificate and symbolic-background audit for terminal-only transfer."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ZERO=(F(0),)*3
def add(*xs):return tuple(sum(v) for v in zip(*xs))
def scale(a,v):return tuple(a*x for x in v)
def neg(v):return scale(-1,v)
def div(num,k):
    """(b+1)(b+2)(b+3) * num/(b+k), coefficients low first."""
    if not num:return ZERO
    return scale(F(num),{1:(F(6),F(5),F(1)),2:(F(3),F(4),F(1)),3:(F(2),F(3),F(1))}[k])
def u(x,y,z):return div(x,1+y+z)
def tot(xs):return add(*xs) if xs else ZERO

def residual(a,b,c,T,L,Q,R,benchmark):
    s=a+b+c;d=sum(T);uc=u(c,a,b)
    target=add(scale(F(7,3),div(s,s)),
        tot([u(T[j],Q[j],R[j]) for j in range(3)]),
        tot([u(T[j],a,L[j]) for j in range(3)]),
        tot([u(T[j],a,b) for j in range(3)]),
        scale(-3,div(d,d) if benchmark=='portfolio_profit' else div(int(d>0),1)))
    slacks=[
        tot([add(u(L[j],a,T[j]),neg(u(c,a,T[j]))) for j in range(3)]),
        tot([add(u(R[j],T[j],Q[j]),neg(u(c,T[j],Q[j]))) for j in range(3)]),
        tot([add(uc,neg(u(T[j],a,b))) for j in range(3)]),
        tot([add(uc,neg(u(L[j],a,b))) for j in range(3)]),
        tot([add(uc,neg(u(Q[j],a,b))) for j in range(3)]),
        tot([add(u(L[j],a,T[j]),neg(u(R[k],a,T[j]))) for j in range(3) for k in range(3)])]
    coeff=[F(3,4),F(1,8),F(17,48),F(1),F(7,48),F(1,12)]
    return add(target,*[scale(-k,v) for v,k in zip(slacks,coeff)])

def main():
    out={}
    for benchmark in ('portfolio_profit','discounted_union'):
        minima=[None]*3;argmin=[None]*3;bad=[];n=0;rootmin=None
        table={''.join(map(str,abc))+':'+str(d):None for abc in product([0,1],repeat=3) for d in range(4)}
        for bits in product([0,1],repeat=15):
            a,b,c=bits[:3];T,L,Q,R=bits[3:6],bits[6:9],bits[9:12],bits[12:15]
            values=residual(a,b,c,T,L,Q,R,benchmark)
            n+=1
            for i,v in enumerate(values):
                if minima[i] is None or v<minima[i]:minima[i]=v;argmin[i]=bits
            root=values[0]/6
            if root<0:raise AssertionError(('root',bits,values))
            rootmin=root if rootmin is None else min(rootmin,root)
            key=''.join(map(str,(a,b,c)))+':'+str(sum(T))
            table[key]=root if table[key] is None else min(table[key],root)
            if any(v<0 for v in values) and len(bad)<5:bad.append({'bits':bits,'polynomial':list(map(str,values))})
        out[benchmark]={'membership_patterns':n,'root_minimum':str(rootmin),
            'background_polynomial_coefficient_minima':list(map(str,minima)),
            'background_polynomial_argmin':argmin,'first_negative_coefficient_patterns':bad,
            'root_compressed_minima':{k:str(v) for k,v in table.items()}}
    Path(__file__).with_name('three_terminal_transfer_exact.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
