"""Independently materialize integer unit customers and verify 33 last nodes.
No LP, no discovery row functions. This verifies only a partial terminal skeleton.
"""
from fractions import Fraction as F
from itertools import permutations
from math import lcm,gcd
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
source=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())
report=json.loads((HERE/'joint_terminal_lp.json').read_text())
atoms=source['primal']['atoms'];weights=list(map(F,report['exact_reweighting']));refs=report['refinements']
fixed=list('ABCDEUVWXY');families=['T','L_actual','L_second','L_third','AB_R','AB_S','AE_R','AE_S','second_H','second_I','second_J']
labels=fixed+[g+str(i) for g in families for i in range(5)];label_to_id={name:i for i,name in enumerate(labels)}
triples=[(t,r,s) for t in (0,1) for r in (0,1) for s in (0,1)]
scale=lcm(*(120*w.denominator for w in weights if w));customers={}
for mass,ref in zip(weights,refs):
    if not mass:continue
    atom=atoms[ref['parent_atom']];AB=[bits for n,bits in zip(atom['AB_hist'],triples) for _ in range(n)]
    menus={'T':[b[0] for b in AB],'AB_R':[b[1] for b in AB],'AB_S':[b[2] for b in AB],'AE_R':[b[1] for b in ref['AE']],'AE_S':[b[2] for b in ref['AE']],'second_H':[b[1] for b in ref['second']],'second_I':[b[2] for b in ref['second']],'second_J':[b[3] for b in ref['second']]}
    menus.update({g:v for g,v in zip(('L_actual','L_second','L_third'),ref['L'])})
    count=int(mass*scale/120);assert F(count)==mass*scale/120
    for perm in permutations(range(5)):
        mask=sum(int(b)<<i for i,b in enumerate(atom['bits']))
        for g in families:
            for i in range(5):mask|=menus[g][perm[i]]<<label_to_id[g+str(i)]
        customers[mask]=customers.get(mask,0)+count
common=gcd(*customers.values());customers={mask:count//common for mask,count in customers.items()};scale//=common
likes={mask:[a for a in range(65) if (mask>>a)&1] for mask in customers}
patterns={}
for a,label in enumerate(labels):
    pattern=tuple(bool((mask>>a)&1) for mask in customers)
    patterns.setdefault(pattern,[]).append(label)
duplicates=[v for v in patterns.values() if len(v)>1]
assert not duplicates,duplicates

def all_utilities(history):
    q=[label_to_id[label] for label in history];values=[0]*65
    for mask,count in customers.items():
        denom=1+sum((mask>>a)&1 for a in q)
        share=count*(60//denom)
        for a in likes[mask]:values[a]+=share
    return values
nodes=[(['A','B','C','D'],'E'),(['A','E','U','V'],'W'),(['A','B','E','X'],'Y')]
for i in range(5):
    nodes += [(['A','B','C','T'+str(i)],'L_actual'+str(i)),(['A','E','U','T'+str(i)],'L_second'+str(i)),(['A','B','E','T'+str(i)],'L_third'+str(i)),(['A','B','T'+str(i),'AB_R'+str(i)],'AB_S'+str(i)),(['A','E','T'+str(i),'AE_R'+str(i)],'AE_S'+str(i)),(['A','T'+str(i),'second_H'+str(i),'second_I'+str(i)],'second_J'+str(i))]
node_results=[]
for history,action in nodes:
    vals=all_utilities(history);actual=vals[label_to_id[action]];assert actual==max(vals),(history,action)
    node_results.append({'history':history,'action':action,'utility':str(F(actual,60)),'best_replies':[labels[a] for a,v in enumerate(vals) if v==actual]})
W=sum(count for mask,count in customers.items() if mask&31);Tmask=sum(1<<label_to_id['T'+str(i)] for i in range(5));O=sum(count for mask,count in customers.items() if mask&Tmask)
assert F(O,W)==F(report['exact_primal_value']);assert O>2*W
out={'scope':'Legal integer unit-customer instance and only the 33 specified final-player nodes. No complete SPE is asserted. O is coverage of T1..T5, not claimed exact OPT.','topic_count':len(labels),'topics_pairwise_distinct':True,'customer_types':len(customers),'customer_count':sum(customers.values()),'scaling':scale,'W':W,'comparison_cover':O,'comparison_ratio':str(F(O,W)),'verified_last_nodes':len(nodes),'deviation_comparisons_including_own':len(nodes)*65,'all_nodes_best_replies':True,'node_results':node_results}
HERE.joinpath('audit_joint_terminal_materialization.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='node_results'},indent=2))
