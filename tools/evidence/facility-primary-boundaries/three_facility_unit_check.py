"""Definition-level check for one two-site, two-client, three-label instance."""
from fractions import Fraction as Q
from itertools import product
import json
weights=(Q(1),Q(1)); covers=({0},{1}); k=3; m=2

def profile(layout):
    rows=[]
    for allowed in covers:
        access=[f for f,s in enumerate(layout) if s in allowed]
        rows.append([Q(1,len(access)) if f in access else Q(0) for f in range(k)])
    return rows

def check(layout,p):
    comparisons=0
    for i in range(2):
        access=[f for f,s in enumerate(layout) if s in covers[i]]
        assert len(p[i])==k and all(x>=0 for x in p[i])
        assert sum(p[i])==(1 if access else 0)
        assert all(p[i][f]==0 for f in range(k) if f not in access)
        costs={f:weights[i]+sum(weights[j]*p[j][f] for j in range(2) if j!=i) for f in access}
        for f in access:
            if p[i][f]>0:
                for g in access:
                    assert costs[f]<=costs[g]
                    comparisons+=1
    return comparisons

def loads(p):
    return [sum(weights[i]*p[i][f] for i in range(2)) for f in range(k)]
allrows=[];total=0
for s in product(range(m),repeat=k):
    p=profile(s);total+=check(s,p);L=loads(p);dev=[]
    for f in range(k):
        t=list(s);t[f]=1-s[f];p2=profile(t);check(t,p2);d=loads(p2)[f]
        dev.append({'facility':f,'target':t[f],'deviation_load':str(d),'ratio':str(d/L[f])})
    factor=max(Q(1),*(Q(x['ratio']) for x in dev))
    assert factor==(3 if len(set(s))==1 else 1)
    allrows.append({'layout':s,'probabilities':[[str(x) for x in row] for row in p],'loads':list(map(str,L)),'deviations':dev,'actual_factor_with_this_complete_rule':str(factor)})
selected=next(r for r in allrows if r['layout']==(0,0,1))
assert selected['loads']==['1/2','1/2','1']
assert [x['deviation_load'] for x in selected['deviations']]==['1/2','1/2','1/3']
assert total==48
print(json.dumps({'status':'passed','scope':'one exact two-site, two-unit-client instance with three labeled facilities; not an exhaustive general instance search','labeled_layouts':8,'on_path_NE_cost_comparisons':total,'actual_deviations_at_selected_layout':3,'all_symmetric_continuations_exact_NE':True,'all_collocated_selected_rule_factor':'3','repeated_two_site_layout_exact_SPE':True,'general_sst_claim_proved_by_this_check':False,'layouts':allrows},indent=2))
