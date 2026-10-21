from fractions import Fraction as F
from random import Random
from customer_attraction import Instance,CustomerType,ExactSPESolver
import json

def residual(I,c,b):
    out=F(0)
    for typ in I.customers:
        cc=sum(c[a] for a in typ.topics)
        bb=sum(b[a] for a in typ.topics)
        if cc:out+=F(typ.multiplicity*(cc-bb),cc)
    return out

def run(seed=99,tries=500,k=4,r=2):
    rng=Random(seed)
    for z in range(tries):
        rows=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(5)) for mask in []]
        rows=[]
        for mask in range(1,1<<k):
            n=rng.randrange(5)
            if n:rows.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),n))
        for base in [(0,)*k]+[tuple(int(a==j) for a in range(k)) for j in range(k)]:
            I=Instance(tuple(map(str,range(k))),tuple(rows),sum(base)+r)
            S=ExactSPESolver(I)
            v=min((residual(I,c,base),c) for c in S.outcomes(base))
            for a in range(k):
                b=tuple(base[j]+int(a==j) for j in range(k))
                J=Instance(I.topics,I.customers,sum(b)+r)
                T=ExactSPESolver(J)
                w=min((residual(J,c,b),c) for c in T.outcomes(b))
                if w[0]>v[0]:
                    return dict(seed=seed,trial=z,instance=I.to_dict(),base=base,add=a,original=[str(v[0]),v[1]],added=[str(w[0]),w[1]],r=r)
    return dict(seed=seed,tries=tries,found=False,r=r)
if __name__=='__main__':
    print(json.dumps(run(),indent=2))

def check(rows,base,add,r):
    k=len(base)
    I=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),n) for mask,n in rows if n),sum(base)+r)
    S=ExactSPESolver(I)
    v=min((residual(I,c,base),c) for c in S.outcomes(base))
    b=tuple(base[j]+int(add==j) for j in range(k))
    J=Instance(I.topics,I.customers,sum(b)+r)
    T=ExactSPESolver(J)
    w=min((residual(J,c,b),c) for c in T.outcomes(b))
    return w[0]>v[0],I,v,J,w

def minimize():
    z=run();I=Instance.from_dict(z['instance']);base=tuple(z['base']);add=z['add'];r=z['r']
    rows=[(sum(1<<a for a in t.topics),t.multiplicity) for t in I.customers]
    changed=True
    while changed:
        changed=False
        for j,(mask,n) in enumerate(rows):
            if n:
                q=rows.copy();q[j]=(mask,n-1)
                if check(q,base,add,r)[0]:rows=q;changed=True
    ok,I,v,J,w=check(rows,base,add,r)
    return dict(instance=I.to_dict(),base=base,add=add,r=r,original=[str(v[0]),v[1]],added=[str(w[0]),w[1]])
