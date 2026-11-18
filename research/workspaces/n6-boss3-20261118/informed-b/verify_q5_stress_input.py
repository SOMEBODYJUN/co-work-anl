"""Exact semantic and static-exposure check for a fixed catalogue JSON.

Input syntax matches exact_tail.py. Static loss scans three successors from
only the five genuine extra covers, either with repeats or pairwise distinct.
It has no successor best-response constraints and proves no SPE statement.
"""
from fractions import Fraction as F
from itertools import product,combinations
import json,sys
from pathlib import Path


def verify(data):
    K=data['K']; labels=data['labels']; n=data['clients']
    cov=[set(v['clients']) for v in labels];anchors=cov[:6];extras=cov[6:]
    assert n>=0 and K>0 and len(labels)==11
    assert all(len(a)==K for a in anchors)
    assert all(anchors[i].isdisjoint(anchors[j]) for i in range(6) for j in range(i))
    assert all(0<=x<n for c in cov for x in c)
    assert max(map(len,cov))==K
    assert all(extras) and len(set(map(frozenset,extras)))==5
    assert all(e not in anchors for e in extras)
    assert data['prefix_labels']==['T4','T5']
    assert data['prefix_counts']==[0,0,0,0,1,1,0,0,0,0,0]
    rows=[]
    def loss(anchor,actions):
        return sum((F(sum(x in extras[a] for a in actions),1+sum(x in extras[a] for a in actions)) for x in anchor),F())
    for j in range(4):
        repeated=max(((loss(anchors[j],actions),actions) for actions in product(range(5),repeat=3)))
        distinct=max(((loss(anchors[j],actions),actions) for actions in combinations(range(5),3)))
        assert distinct[0]>F(K,2)
        rows.append({'anchor':j,'max_arbitrary_loss':str(repeated[0]),'arbitrary_followers':list(repeated[1]),
                     'max_distinct_extra_loss':str(distinct[0]),'distinct_followers':list(distinct[1]),
                     'distinct_loss_exceeds_half_K':True})
    return {'K':K,'clients':n,'original_label_count':11,'distinct_anchor_covers':6,
            'distinct_nonempty_covers':len(set(map(frozenset,cov))),'extra_nonempty_cover_count':5,
            'all_extras_distinct_and_nonanchor':True,'all_catalogue_sizes_at_most_K':True,
            'OPT6':6*K,'static_exposure':rows,
            'scope':'Static successor-action relaxation; even distinct-extra follower sequences have no SPE or best-response certification.'}

if __name__=='__main__':
    print(json.dumps(verify(json.loads(Path(sys.argv[1]).read_text())),indent=2))
