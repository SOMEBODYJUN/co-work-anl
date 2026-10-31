"""Exact pure local NE and guarded quota-preserving repair.

Shared by the heterogeneous four-seed and shared P menus.
"""
from fractions import Fraction as Q


def load_pair(a,b,ws,p):
    x=a+sum((w*z for w,z in zip(ws,p)),Q(0))
    return x,a+b+sum(ws,Q(0))-x


def is_ne(a,b,ws,p):
    x,y=load_pair(a,b,ws,p)
    return all((z==0 or x-y<=w) and (z==1 or x-y>=-w)
               for w,z in zip(ws,p))


def guarded_repair(a,b,ws,seed):
    """Return the seed's quota-preserving repair, or None if unqualified."""
    p=list(seed)
    if is_ne(a,b,ws,p):
        return tuple(p)
    x,y=load_pair(a,b,ws,p)
    low=1 if x<y else 0
    gap=abs(x-y)
    if any(w<gap for w,z in zip(ws,p) if z==low):
        return None
    moves=0
    while True:
        x,y=load_pair(a,b,ws,p)
        oriented_gap=(y-x) if low==1 else (x-y)
        if oriented_gap<=0:
            break
        candidates=[i for i,(w,z) in enumerate(zip(ws,p))
                    if z!=low and w<oriented_gap]
        if not candidates:
            break
        index=max(candidates,key=lambda i:(ws[i],-i))
        p[index]=low
        moves+=1
        assert moves<=len(ws)
    assert is_ne(a,b,ws,p),"guarded repair must end at an exact pure NE"
    return tuple(p)
