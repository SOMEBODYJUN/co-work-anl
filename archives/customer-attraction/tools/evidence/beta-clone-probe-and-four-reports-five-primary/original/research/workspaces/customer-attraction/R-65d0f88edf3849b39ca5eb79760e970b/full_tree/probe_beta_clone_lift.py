"""One exact targeted attack on fresh-clone SPE lift; no negative evidence claim."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import factorial as fac
import json, random
from pathlib import Path

HERE=Path(__file__).parent

def add(q,a):
    s=list(q);s[a]+=1;return tuple(s)

def reachable(k,m,pay):
    @lru_cache(None)
    def R(q):
        if sum(q)==m:return frozenset([q])
        children=[R(add(q,a)) for a in range(k)]
        bound=max(min(pay(z,a) for z in children[a]) for a in range(k))
        return frozenset(z for a in range(k) for z in children[a] if pay(z,a)>=bound)
    return R((0,)*k),R

def original_pay(types):
    @lru_cache(None)
    def pay(q,a):
        return sum((F(w,b+sum(q[j] for j in range(len(q)) if B>>j&1))
                    for B,b,w in types if B>>a&1),F(0))
    return pay

def clone_pay(types,clones):
    @lru_cache(None)
    def per(b,own,others):
        if b==0:return F(1,own+sum(others))
        d=len(others)+1
        value=F(0)
        for mask in range(1<<len(others)):
            s=mask.bit_count()
            mass=F(b*fac(s+1)*fac(b+d-2-s),fac(b+d))
            value+=mass/F(own+sum(v for j,v in enumerate(others) if mask>>j&1))
        return value
    @lru_cache(None)
    def pay(q,a):
        total=F(0)
        for B,b,w in types:
            if not B>>(a//clones)&1:continue
            others=tuple(v for j,v in enumerate(q) if j!=a and v and B>>(j//clones)&1)
            total+=w*per(b,q[a],others)
        return total
    return pay

def fresh(q,clones):
    return tuple(int(j<n) for n in q for j in range(clones))

def main():
    rng=random.Random(2601024)
    checked=0
    # This finite attack addresses one explicit general lift claim, not half.
    for n in [2,3]:
        for case in range(150):
            types=tuple((B,rng.randint(1,4),rng.randint(0,9)) for B in range(1,1<<n))
            types=tuple(t for t in types if t[2])
            op=original_pay(types); cp=clone_pay(types,3)
            original,_=reachable(n,3,op)
            cloned,_=reachable(n*3,3,cp)
            checked+=1
            failed=[q for q in original if fresh(q,3) not in cloned]
            repeated=[q for q in cloned if max(q)>1]
            if failed or repeated:
                out={"status":"candidate_found","n":n,"m":3,"clones":3,
                     "types":types,"original_spe":sorted(original),
                     "fresh_lift_failures":sorted(failed),"repeated_clone_spe":sorted(repeated),
                     "checked":checked,"scope":"Exact finite attack on fresh-clone implementation, not half."}
                (HERE/'beta_clone_probe.json').write_text(json.dumps(out,indent=2))
                print(json.dumps(out));return
    out={"status":"no_candidate_in_finite_batch","checked":checked,
         "scope":"No general conclusion; fixed candidate test only."}
    (HERE/'beta_clone_probe.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out))

if __name__=='__main__':main()
