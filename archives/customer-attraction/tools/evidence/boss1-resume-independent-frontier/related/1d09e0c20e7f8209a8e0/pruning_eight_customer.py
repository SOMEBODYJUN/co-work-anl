from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from customer_attraction import Instance, ExactSPESolver, verify_certificate

OUT=Path(__file__).parent
full=Instance.from_topic_sets([{0,1},{2,3,4,5},{0,1,6},{0,1,7}],3,('A','B','C','D'))
small=Instance.from_topic_sets([{0,1},{2,3,4,5},{0,1,7}],3,('A','B','D'))
records={}
for label,inst in [('full',full),('delete_C',small)]:
    sol=ExactSPESolver(inst)
    records[label]={'instance':inst.to_dict(),'outcomes':sorted(sol.outcomes()),'ordered_paths':list(sol.ordered_outcomes()),'minimum_welfare':sol.minimum_welfare(),'optimum':inst.optimal_welfare()}
    if label=='full':
        cert=sol.certificate(on_path=(0,1,1))
        verify_certificate(inst,cert).assert_valid()
        records[label]['certificate']=cert.to_dict()
    for counts in sorted(sol.outcomes()):
        print(label,counts,'W',inst.welfare(counts),'payoffs',inst.topic_payoffs(counts))
    print(label,'paths',records[label]['ordered_paths'])
# independent direct backward induction on all ordered histories, keeping all subgame strategies.
def payoffs(inst,history):
    return tuple(sum((F(c.multiplicity,sum(a in c.topics for a in history)) for c in inst.customers if history[i] in c.topics),F(0)) for i in range(inst.players))
def enumerate_ordered(inst):
    def subgame(prefix):
        if len(prefix)==inst.players:
            return {prefix}
        child=[subgame(prefix+(a,)) for a in range(inst.topic_count)]
        i=len(prefix)
        threshold=max(min(payoffs(inst,h)[i] for h in possible) for possible in child)
        return {h for possible in child for h in possible if payoffs(inst,h)[i]>=threshold}
    return subgame(())
for label,inst in [('full',full),('delete_C',small)]:
    independent=enumerate_ordered(inst)
    assert independent==set(map(tuple,records[label]['ordered_paths']))
    records[label]['independent_ordered_BI']=True
(OUT/'pruning_eight_customer.json').write_text(json.dumps(records,indent=2))
