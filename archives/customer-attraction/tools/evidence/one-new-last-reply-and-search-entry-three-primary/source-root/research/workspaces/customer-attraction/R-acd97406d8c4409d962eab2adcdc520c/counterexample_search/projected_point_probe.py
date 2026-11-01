"""Exact credible-completion probe of the published 437-row primal point.

A finite obstruction study, not a counterexample to Q-CAG-HALF.
"""
from pathlib import Path
import sys,json,time
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver
CERT=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
p=json.loads(CERT.read_text())['primal'];D=p['denominator'];atoms=p['atoms']
inst=Instance(tuple('ABCDEUVWXY'),tuple(CustomerType(frozenset(i for i,b in enumerate(a['bits']) if b=='1'),a['mass_numerator']) for a in atoms),5)
sol=ExactSPESolver(inst);target=inst.counts(tuple(range(5)),terminal=True)
report={'scope':'exact completion obstruction of one specified rational 437-row feasible point, after projection to its ten fixed original themes','full_spe_counterexample':False,'denominator':D,'original_welfare':str(F(inst.welfare(target),D)),'prefixes':[]}
for h in [(0,1,2,3),(0,1,2),(0,1),(0,),()]:
 t=time.monotonic();k=inst.counts(h);outs=sol.outcomes(k);thr=sol.threshold(k)
 a=len(h);actual=sol._utility(target,a)
 child=[]
 for b in range(inst.topic_count):
  kk=list(k);kk[b]+=1
  oo=sol.outcomes(kk);minimum=min(sol._utility(q,b) for q in oo)
  winners=[q for q in oo if sol._utility(q,b)==minimum]
  child.append({'action':inst.topics[b],'credible_minimum':str(F(minimum,D)),'minimizer_counts':min(winners)})
 row={'history':''.join(inst.topics[a] for a in h),'target_continuation_is_spe':target in outs,'actual_action':inst.topics[a],'actual_payoff':str(F(actual,D)),'threshold':str(F(thr,D)),'gap_threshold_minus_actual':str(F(thr-actual,D)),'children':child,'outcomes':len(outs),'elapsed_seconds':time.monotonic()-t}
 report['prefixes'].append(row);print(json.dumps(row),flush=True)
report['stats']=sol.stats.__dict__
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
