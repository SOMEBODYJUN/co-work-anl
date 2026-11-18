"""Turn each independent-tail LP atom vector into one legal 9-label menu.
This is a finite exact discriminator; it is not a universal SPE proof.
"""
from fractions import Fraction as F
from functools import reduce
from math import lcm
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
src=ROOT.parent/'informed-b/probe-bc-tail-lp-output.json'
records=[]
for case in json.loads(src.read_text()):
    s,t=case['s'],case['t']
    atoms=[]
    for atom in case['atoms']:
        block,e,a,y=atom['type']; mass=F(atom['mass']).limit_denominator(100000)
        if block=='target': blocks=[(0,mass)]
        elif block=='other': blocks=[(j,mass/(s-1)) for j in range(1,s)]
        else: blocks=[(None,mass)]
        for j,q in blocks:
            mask=(0 if j is None else 1<<j)|(e<<6)|(a<<7)|(y<<8)
            atoms.append((mask,q))
    for j in range(s,6):atoms.append((1<<j,F(1)))
    scale=reduce(lcm,(q.denominator for _,q in atoms),1)
    integer_atoms=[(mask,int(q*scale)) for mask,q in atoms]
    sizes=[sum(mass for mask,mass in integer_atoms if mask>>a&1) for a in range(9)]
    prefix=[0]*9
    for j in range(s,6):prefix[j]=1
    prefix[6]=t
    prefix[0]+=1 # current fourth provider was forced to target anchor0
    assert sum(prefix)==4
    def payoff(a,b):
        counts=prefix.copy(); counts[a]+=1;counts[b]+=1
        loads=[sum(counts[j] for j in range(9) if mask>>j&1) for mask,_ in integer_atoms]
        up=[sum(F(mass,load) for (mask,mass),load in zip(integer_atoms,loads) if (mask>>j&1) and load)/scale for j in range(9)]
        return up
    branches=[]
    for a in range(9):
        values=[payoff(a,b) for b in range(9)]
        best6=max(v[b] for b,v in enumerate(values))
        replies=[b for b,v in enumerate(values) if v[b]==best6]
        floor5=min(values[b][a] for b in replies)
        branches.append({'fifth_action':a,'true_last_best_replies':replies,'minimum_fifth_payoff_over_true_replies':str(floor5),
                         'last_best_payoff':str(best6)})
    tau=max(F(b['minimum_fifth_payoff_over_true_replies']) for b in branches)
    candidate=payoff(7,8)
    candidate_counts=prefix.copy();candidate_counts[7]+=1;candidate_counts[8]+=1
    candidate_W=sum(mass for mask,mass in integer_atoms if any(candidate_counts[j] and (mask>>j&1) for j in range(9)))
    witness=[b for b in branches if F(b['minimum_fifth_payoff_over_true_replies'])>candidate[7]]
    records.append({'s':s,'prefix_E_multiplicity':t,'normalization_scale':scale,'integer_customer_total':sum(q for _,q in integer_atoms),
                    'normalized_label_sizes':[str(F(q,scale)) for q in sizes],
                    'catalog_label_names':['T0','T1','T2','T3','T4','T5','E','A','Y'],
                    'integer_atoms':[{'mask':mask,'count':q} for mask,q in integer_atoms],
                    'candidate_final_welfare_normalized':str(F(candidate_W,scale)),'OPT6_normalized':'6','candidate_welfare_ratio':str(F(candidate_W,6*scale)),
                    'candidate_current_payoff':str(candidate[0]),'candidate_fifth_payoff':str(candidate[7]),'candidate_last_payoff':str(candidate[8]),
                    'Y_is_actual_last_best_reply':8 in branches[7]['true_last_best_replies'],
                    'subgame_fifth_security':str(tau),'strict_fifth_deviations':witness,
                    'all_fifth_action_subtrees':branches,
                    'conclusion':'Only this symmetric one-menu completion is tested; failure does not rule out nonsymmetric completions or the original half target.'})
(ROOT/'tail-completion-probe.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k not in ('integer_atoms','all_fifth_action_subtrees')} for r in records],indent=2))
