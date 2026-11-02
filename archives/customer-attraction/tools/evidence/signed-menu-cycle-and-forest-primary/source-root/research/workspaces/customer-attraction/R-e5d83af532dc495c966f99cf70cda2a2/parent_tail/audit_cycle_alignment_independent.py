"""Independent exhaustive audit of the cycle deficit formula.

No discovery-code imports. The finite audit checks the implementation;
the general proof is the parity inequality and constructive greedy path.
"""
from itertools import product
from pathlib import Path
import json


def run(q, length, weights):
    sizes=[s.bit_count() for s in range(1<<q)]
    count=0
    groups=0
    for prefs in product((0,1), repeat=length):
        mins={}
        for masks in product(range(1<<q),repeat=length):
            ks=tuple(sizes[s] for s in masks)
            cost=0
            for r in range(length):
                s=(r+1)%length
                c=(masks[r]&masks[s]).bit_count()
                delta=(c-max(0,ks[r]+ks[s]-q) if prefs[r] else min(ks[r],ks[s])-c)
                assert delta>=0
                cost+=weights[r]*delta
            mins[ks]=min(mins.get(ks,cost),cost)
            count+=1
        for ks, value in mins.items():
            cap=sum(abs(q-ks[r]-ks[(r+1)%length]) if prefs[r] else abs(ks[r]-ks[(r+1)%length]) for r in range(length))
            raw=max(0,q-cap) if sum(prefs)%2 else 0
            assert raw%2==0
            expected=min(weights)*raw//2
            assert value==expected,(q,length,prefs,ks,weights,value,expected)
            groups+=1
    return {'q':q,'length':length,'weights':weights,'assignments_checked':count,'marginal_minima_checked':groups}


def greedy_check(q,length):
    calls=0
    for ks in product(range(q+1),repeat=length):
        original=set(range(ks[0]));current=set(original);down=0
        for old,new in zip(ks,ks[1:]):
            if new>=old:
                candidates=sorted(set(range(q))-current,key=lambda x:(x in original,x))
                current.update(candidates[:new-old])
            else:
                candidates=sorted(current,key=lambda x:(x not in original,x))
                current.difference_update(candidates[:old-new]);down+=old-new
            assert len(current)==new
        expected=max(0,ks[0]+ks[-1]-q,ks[0]-down)
        assert len(original&current)==expected,(ks,current,expected)
        calls+=1
    return calls


if __name__=='__main__':
    out={'status':'finite exact check passed; general proof separate',
         'cycle_checks':[run(2,5,[2,7,3,4,1]),run(3,4,[5,2,7,3]),run(4,3,[3,8,1]),run(3,3,[0,4,7])],
         'greedy_paths_checked':sum(greedy_check(q,5) for q in range(1,7))}
    Path(__file__).with_name('cycle_alignment_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
