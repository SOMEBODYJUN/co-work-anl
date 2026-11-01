"""Independent definition-level Fraction checks for singleton-block theorem.

No import of the orbit LP, mathematical note's probability formula, or a SPE
engine. Explicit clients are all masks in one wreath-product orbit. This is a
finite implementation audit, not a proof for general parameters.
"""
import itertools, json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


def compositions(total,slots):
    if slots==0:
        if total==0: yield ()
        return
    if slots==1:
        yield (total,);return
    for first in range(total+1):
        for tail in compositions(total-first,slots-1): yield (first,)+tail


def audit(c,k,max_others):
    p=c*k;orbits=defaultdict(list)
    for mask in range(1,1<<p):
        key=tuple(sorted(sum((mask>>(g*k+j))&1 for j in range(k)) for g in range(c)))
        orbits[key].append(mask)
    records=0;exact_price_checks=0;worst=None;equalities=0
    for clients in orbits.values():
        n=len(clients);d=clients[0].bit_count()
        # Every theme has the required same size within this degree layer.
        size=[sum((mask>>a)&1 for mask in clients) for a in range(p)]
        assert len(set(size))==1 and p*size[0]==d*n
        for r in range(max_others+1):
            for others in compositions(r,p-k):
                counts=(1,)+(0,)*(k-1)+others
                loads=[sum(q for a,q in enumerate(counts) if (mask>>a)&1) for mask in clients]
                w=sum(load>0 for load in loads);missing=n-w
                utility=sum((F(1,load) for mask,load in zip(clients,loads) if mask&1),F(0))
                exclusive=sum(bool(mask&1) and load==1 for mask,load in zip(clients,loads))
                assert d*missing <= (p-d)*exclusive <= (p-d)*utility
                # One degree layer: uniform z with total p/d covers all clients.
                price=max(F(0),F(n)-F(p,d)*utility)
                slack=price-(w-utility)
                assert slack<=0
                worst=slack if worst is None else max(worst,slack)
                equalities+=slack==0
                records+=1
                # Directly enumerate more uniform price weights as a second check.
                for h in range(1,p+1):
                    z=F(1,h)
                    obj=sum((min(F(1),z*mask.bit_count()) for mask in clients),F(0))-p*z*utility
                    assert obj<=w-utility
                    exact_price_checks+=1
    return {'blocks':c,'topics_per_block':k,'orbits':len(orbits),
            'profiles_and_orbits':records,'uniform_price_checks':exact_price_checks,
            'max_price_minus_W_plus_u':str(worst),'price_equalities':equalities}


def main():
    settings=[(1,1,0),(1,3,0),(2,1,6),(2,2,6),(2,3,5),(3,1,6),(3,2,5),(4,2,4)]
    results=[audit(*q) for q in settings]
    output={'status':'passed','scope':'Finite direct-mask audit, not a general proof',
            'results':results,'total_profiles_and_orbits':sum(x['profiles_and_orbits'] for x in results),
            'total_uniform_price_checks':sum(x['uniform_price_checks'] for x in results)}
    target=Path(__file__).with_name('symmetric_singleton_audit.json')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
