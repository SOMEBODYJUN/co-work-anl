"""Exact full-orbit test of the previously proposed common threshold completion.

The completion is only a specified candidate.  A negative query rejects that
candidate, not the input's full transportation feasibility.  Use all literal
labels, including distinct nodes with the same marginal group.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import json
from common import (HERE,NODES,STATES,add,dump,marginal,metadata,node_group,
                    pair_class,parse,sha,words)


def main():
    point,cols,masses,hist,groups=parse()
    terms=Counter(pair_class(e,f) for e in NODES for f in NODES)
    totals=defaultdict(F)
    free=defaultdict(F)
    per_hist=defaultdict(dict)
    intervals=[]
    for hi,h in hist.items():
        H=masses[hi]
        ws=words(h)
        ng={e:node_group(e,ws) for e in NODES}
        vals={g:marginal(hi,ids,masses) for g,ids in groups[hi].items()}
        moments={g:(p[2]+p[3],p[1]+p[3],p[3]) for g,p in vals.items()}
        nodes=[]
        cuts={F(),H}
        for e in NODES:
            q,v,t=moments[ng[e]]
            assert 0<=t<=q<=H and 0<=q+v-t<=H
            cuts.update((q,t,q+v-t))
            nodes.append({'literal':e,'group':ng[e],
                          'R':[['0',str(q)]],
                          'Z':[['0',str(t)],[str(q),str(q+v-t)]]})
        cuts=sorted(cuts)
        atoms=[]
        for left,right in zip(cuts,cuts[1:]):
            assert left<right
            u=(left+right)/2
            rz=[]
            for e in NODES:
                q,v,t=moments[ng[e]]
                rz.append((int(u<q),int(u<t or q<=u<q+v-t)))
            atoms.append({'left':str(left),'right':str(right),
                          'mass':str(right-left),'states':rz})
        # Verify every literal own marginal directly from common atoms.
        for j,e in enumerate(NODES):
            check=tuple(sum((F(a['mass']) for a in atoms if tuple(a['states'][j])==s),F()) for s in STATES)
            assert check==vals[ng[e]]
        p=sum(map(int,h['actual_bits'][:4]));D=(p+1)*(p+2)
        local=defaultdict(F)
        for e in NODES:
            qe,ve,te=moments[ng[e]]
            for f in NODES:
                cl=pair_class(e,f)
                if e==f:
                    continue
                qf,vf,tf=moments[ng[f]]
                J=min(qe,tf)+max(F(),min(qe,qf+vf-tf)-qf)
                value=(ve-vf)/(p+1)+(J-te)/D
                upper=(ve-vf)/(p+1)+(min(qe,vf)-te)/D
                assert value<=upper
                local[cl]+=value
                totals[cl]+=value
                free[cl]+=upper
        for cl in terms:
            per_hist[cl][hi]=local[cl]
        intervals.append({'hist_column':hi,'actual_bits':h['actual_bits'],
                          'hist':h['hist'],'mass':str(H),'P':p,
                          'nodes':nodes,'common_atoms':atoms})
    records=[]
    for cl in sorted(terms):
        records.append({'class':cl,'literal_pairs':terms[cl],
                        'orbit_sum_slack':str(totals[cl]),
                        'individual_slack_after_full_S6_average':str(totals[cl]/terms[cl]),
                        'free_upper_sum':str(free[cl]),
                        'per_hist':[[hi,str(per_hist[cl][hi])] for hi in hist]})
    out=metadata()|{'source_path':str(Path(__file__)),'source_sha256':sha(Path(__file__)),
        'scope':'One explicit full-S6-averaged 66-node threshold completion; failure is not a separation',
        'symmetrization':'Use all 720 index permutations, each mass 1/720; keep all 66 literal nodes distinct',
        'W':point['W'],'literal_nodes':len(NODES),'ordered_queries':66*66,
        'self_queries':66,'classes':len(terms),
        'negative_classes':sum(totals[cl]<0 for cl in terms),
        'zero_classes':sum(totals[cl]==0 for cl in terms),
        'minimum_individual_slack':str(min(totals[cl]/terms[cl] for cl in terms)),
        'candidate_passes_all_ZZ':all(v>=0 for v in totals.values()),
        'own_marginals_exactly_verified':True,
        'records':records,'completion':intervals}
    dump(HERE/'threshold_audit_19556.json',out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','completion')},ensure_ascii=False))
    print('negative',[(r['class'],float(F(r['individual_slack_after_full_S6_average']))) for r in records if F(r['orbit_sum_slack'])<0])


if __name__=='__main__':
    main()
