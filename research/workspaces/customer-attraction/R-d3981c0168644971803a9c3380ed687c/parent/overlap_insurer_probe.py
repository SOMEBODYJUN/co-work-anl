"""A single finite diagnostic of the newly relevant effective insurer amplitude.

A high-root SPE continuation has payoff h, while every deviating joint root can
be sent to minimizer suffixes. Their maximum is M=the exact root SPE threshold.
Only e=h-M, not an arbitrary same-root spread, is universally usable. Test D<3e
on saved instances, with all true suffix outcomes retained; no general inference.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver
HERE=Path(__file__).resolve().parent
names=['root_tax_failure','eight_cce_welfare_gap','aggregate_theta_failure','fractional_actual_load_failure','individual_security_failure','prefix_balance_failure','portfolio_matching_failure']
records=[]
for name in names:
 I=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
 S=ExactSPESolver(I);z=(0,)*I.topic_count;M=S.threshold(z);O=I.optimal_welfare();best=None
 for a in range(I.topic_count):
  child=list(z);child[a]=1
  for q in S.outcomes(tuple(child)):
   h=I.topic_payoff(a,q)
   if h<M:continue
   e=h-M;D=2*I.welfare(q)-O;score=3*e-D
   if best is None or score>best[0]:best=(score,a,q,h,e,D)
 score,a,q,h,e,D=best
 rec={'instance':name,'players':I.players,'topics':I.topic_count,'minimum_SPE_root':str(M),'best_3e_minus_D':str(score),'root':a,'terminal':q,'high_root':str(h),'effective_amplitude':str(e),'half_dilution':D,'scope':'This finite fixed instance; no statement about all customer multiplicities or catalogs.'}
 records.append(rec);print(json.dumps(rec),flush=True)
 if score>0:
  cert=S.certificate(q,on_path=next(p for p in S.ordered_outcomes(q) if p[0]==a))
  rec['high_certificate']=cert.to_dict()
  print('POSITIVE_EFFECTIVE_INSURER_CRITERION',name,flush=True)
(HERE/'overlap_insurer_probe.json').write_text(json.dumps({'criterion':'3(h-M)-(2W_H-OPT)>0','records':records},indent=2)+'\n')
