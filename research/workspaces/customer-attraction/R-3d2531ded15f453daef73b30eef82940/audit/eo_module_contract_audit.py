"""Independent exact local identities for the general EO module construction.

No solver and no imported game implementation. This verifies only the six-topic
module identities; the arbitrary-module SPE is established by the written state
induction and is not inferred from finite simulation.
"""
from fractions import Fraction as F
from itertools import product
import json

WEIGHTS={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,
         46:3,51:3,53:3,54:3,59:2}
O={0,1,3,4}
S={2,5}


def u(a, others):
    return sum((F(w,1+sum((mask>>b)&1 for b in others))
                for mask,w in WEIGHTS.items() if (mask>>a)&1),F(0))


def group(a):
    return range(3) if a<3 else range(3,6)


def pair_reply(a):
    return next(b for b in group(a) if b in O and b != a)


def last_reply(a,b):
    return next(c for c in group(b) if c not in (a,b))


def triple_second(a):
    return 3 if a<3 else 0


def last_value(a,b):
    return max(u(c,(a,b)) for c in range(6))


def audit():
    pairs=[]
    triples=[]
    for a in range(6):
        b=pair_reply(a)
        assert u(b,(a,)) == max(u(c,(a,)) for c in range(6))
        first=F(16) if a in O else F(31,2)
        second=F(16) if a in O else F(35,2)
        cap=F(32,3) if a in O else F(67,6)
        assert u(a,(b,))==first
        assert u(b,(a,))==second
        assert last_value(a,b)==cap
        excessive=[c for c in range(6) if u(c,(a,))>16]
        assert excessive == ([] if a in O else [c for c in group(a) if c in O])
        pairs.append([a,b,str(first),str(second),str(cap)])

        k=F(32,3) if a in O else F(67,6)
        assert min(last_value(a,c) for c in range(6))==k
        assert max(last_value(a,c) for c in range(6))<=F(47,3)
        b3=triple_second(a)
        c3=last_reply(a,b3)
        assert u(a,(b3,c3))==F(29,3)
        second3=u(b3,(a,c3))
        assert second3==(F(67,6) if a in O else F(35,3))
        assert u(c3,(a,b3))==second3
        for bdev in range(6):
            cdev=last_reply(a,bdev)
            assert u(cdev,(a,bdev))==last_value(a,bdev)
            assert u(bdev,(a,cdev))<=second3
        triples.append([a,b3,c3,str(u(a,(b3,c3))),str(second3)])
    # The only low-admission pair is an ordinary within-group distinct pair;
    # it is itself a two-person BR pair, so it can be downgraded if needed.
    for a,b in product(range(6),repeat=2):
        r=last_value(a,b)
        assert r>=F(32,3)
        if r<F(67,6):
            assert a in O and b==pair_reply(a) and r==F(32,3)
    return {"pair_rows_a_b_first_second_admission":pairs,
            "triple_rows_a_b_c_root_second_last":triples,
            "status":"exact local identities verified"}


if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
