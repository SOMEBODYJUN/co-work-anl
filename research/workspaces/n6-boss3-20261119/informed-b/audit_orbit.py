"""Enumerate names of this fixed orbit only; all four branches share one coordinate map."""
from itertools import permutations
from collections import Counter
import json
from audit_candidate import HERE, PATTERN, read_point

_,k,gamma,counts,_ = read_point()
orbits=Counter()
representative=None
for anch in permutations(range(4)):
    for extra in permutations(range(5)):
        pattern=[None]*4
        for j,triple in enumerate(PATTERN):
            pattern[anch[j]]=tuple(extra[t] for t in triple)
        p=tuple(pattern)
        orbits[p]+=1
        if representative is None or p<representative[0]:
            representative=p,anch,extra
p,anch,extra=representative
new_counts={}
for (b,bits),n in counts.items():
    v=[None]*5
    for t,bit in enumerate(bits):
        v[extra[t]]=bit
    new_counts[anch[b] if b<4 else b, tuple(v)]=n
old_forced=[]
for j,(e,a,y) in enumerate(p):
    from fractions import Fraction as F
    gain=sum(F(n,1+bits[e]+bits[a]+bits[y]) for (b,bits),n in new_counts.items() if b==j)
    old_forced.append(gain)
    assert gain==gamma*k
assert len(set(orbits.values()))==1
report={"acting_group":"S4(new anchors) x S5(extra labels); old ordered prefix (T4,T5) fixed",
        "group_size":sum(orbits.values()),"orbit_size":len(orbits),"stabilizer":orbits[PATTERN],
        "lexicographic_representative":p,"old_to_new_anchors":anch,"old_to_new_extras":extra,
        "common_population_relabelled_once":True,"forced_anchor_payoffs_at_representative":list(map(str,old_forced))}
(HERE/"fixed-orbit.json").write_text(json.dumps(report,indent=2)+"\n")
print(report)
