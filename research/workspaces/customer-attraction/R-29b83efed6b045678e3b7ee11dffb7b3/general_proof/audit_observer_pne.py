"""Exact auxiliary-bridge counterexample; not a Q-CAG-HALF counterexample."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
k=6
w={2:7,16:1,20:6,26:4,29:1,31:1,33:5,35:5,39:6,45:5,47:7,55:1,58:4,62:1}
A=1

def utility(a,seq):
    return sum((F(n,sum(mask>>j&1 for j in seq)) for mask,n in w.items() if mask>>a&1),F(0))
def v(a,b): return tuple(utility(j,(A,a,b)) for j in (A,a,b))
pay={(a,b):v(a,b) for a,b in product(range(k),repeat=2)}
br={a:[b for b in range(k) if pay[a,b][2]==max(pay[a,c][2] for c in range(k))] for a in range(k)}
assert all(len(x)==1 for x in br.values())
continuation=[br[a][0] for a in range(k)]
first=[pay[a,continuation[a]][1] for a in range(k)]
assert first[0]==max(first)
pnes=[(a,b) for a,b in product(range(k),repeat=2) if b in br[a] and pay[a,b][1]==max(pay[c,b][1] for c in range(k))]
assert pnes==[(2,5),(5,2)]
assert pay[0,1][0]==F(44,3)
assert all(pay[a,b][0]==21 for a,b in pnes)
result={
 'model':'CAG-MODEL; one fixed earlier player A=1, two rational sequential tail players',
 'claim_tested':'For each fixed old player A and every tail SPE z, some static tail PNE zprime has old payoff no greater than at z',
 'status':'FALSE, auxiliary bridge only; no claim about full-root equilibrium or half coverage',
 'unit_customer_count':sum(w.values()),'topic_count':k,'types':w,'fixed_old_topic':A,
 'last_reply_by_first_tail_action':continuation,
 'first_tail_true_deviation_payoffs':[str(x) for x in first],
 'tail_prescription':[0,1],
 'realized_payoffs_old_first_second':[str(x) for x in pay[0,1]],
 'static_tail_pnes':[{'tail':list(z),'payoffs_old_first_second':[str(x) for x in pay[z]]} for z in pnes],
 'all_terminal_payoffs':{f'{a},{b}':[str(x) for x in pay[a,b]] for a,b in product(range(k),repeat=2)},
 'all_last_deviation_payoffs':[[str(pay[a,b][2]) for b in range(k)] for a in range(k)]
}
path=Path(__file__).with_name('observer_pne_exact.json')
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['unit_customer_count','last_reply_by_first_tail_action','first_tail_true_deviation_payoffs','realized_payoffs_old_first_second','static_tail_pnes']},ensure_ascii=False,indent=2))
