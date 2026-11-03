"""Exact credibility audit of a legitimate catalog materialized from a relaxed
ROW3 motif. Rounded positive weights are integers; no assertion that the rounded
catalog preserves every aggregate relaxed row is needed or made.
"""
import itertools,json,sys
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
BASE=Path(__file__).resolve().parent
rows=json.loads((BASE/'frozen_row3_source_support.json').read_text())['support']
weights={};scale=120*10**8
for item in rows:
 p,c,d,e,h=item['state'];assert p==0
 atoms=tuple(itertools.chain.from_iterable([[(j//4,(j//2)%2,j%2)]*n for j,n in enumerate(h)]))
 perms=set(itertools.permutations(atoms));assert 120%len(perms)==0
 orbit_mass=int(item['integer_orbit_weight']);assert orbit_mass%len(perms)==0
 z=orbit_mass//len(perms)
 for types in perms:
  mask=c+2*d+4*e
  for j,(t,r,s) in enumerate(types):mask|=(t<<(3+j))|(r<<(8+j))|(s<<(13+j))
  weights[mask]=weights.get(mask,0)+z
labels=('C','D','E')+tuple(f'T{j}' for j in range(5))+tuple(f'R{j}' for j in range(5))+tuple(f'S{j}' for j in range(5))
I=Instance(labels,tuple(CustomerType(frozenset(a for a in range(18) if m>>a&1),w) for m,w in sorted(weights.items()) if w),3)
def count(xs):return I.counts(xs)
def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def u(q,a):return I.topic_payoff(a,q)
S=ExactSPESolver(I); root=(0,)*18;outs=S.outcomes();actual=count((0,1,2));opt=tuple(range(3,8));O=sum(w for m,w in weights.items() if m&sum(1<<a for a in opt))
# count(opt) is not a legal 3-player profile, so compute the 5-topic comparison
# union directly. This deliberately is arbitrary-q ROW, not OPT_3.
querymin=[min(u(z,a) for z in S.outcomes(inc(root,a))) for a in opt]
best=None
for z in outs:
 for a in range(18):
  if z in S.outcomes(inc(root,a)) and u(z,a)>=S.threshold(root):
   row=sum(querymin)+((u(z,a)-querymin[a-3]) if a in opt else 0)
   slack=row+I.welfare(z)-O
   if best is None or slack<best[0]:best=(slack,z,a,row)
child_audits=[]
for j in range(5):
 h=(3+j,);q=count(h);motif=count((3+j,8+j,13+j));k=(j+1)%5
 last_h=(3+j,13+k)
 vals=[u(count(last_h+(a,)),a) for a in range(18)]; mx=max(vals);brs=[a for a,v in enumerate(vals) if v==mx]
 fallback=min(u(count(last_h+(a,)),13+k) for a in brs)
 child_audits.append({'query':labels[3+j],'motif_is_child_SPE':motif in S.outcomes(q),'motif_first_tail_profit':str(u(motif,8+j)),'child_floor':str(S.threshold(q)),'credible_deviation':labels[13+k],'unique_last_BR':[labels[a] for a in brs],'deviation_first_tail_profit':str(fallback),'strict_gain':str(fallback-u(motif,8+j))})
certificate=S.certificate(best[1]);verification=verify_certificate(I,certificate);verification.assert_valid()
report={'status':'exact finite credibility diagnostic; no five-player counterexample or ROW3 proof','scale':scale,'topic_count':18,'customer_types':len(I.customers),'unit_customers':I.customer_count,'comparison_union':O,'target_CDE_welfare':I.welfare(actual),'target_CDE_is_SPE':actual in outs,'target_C_payoff':str(u(actual,0)),'true_root_floor':str(S.threshold(root)),'query_minima':[str(v) for v in querymin],'true_SPE_outcomes':len(outs),'best_true_row_slack':str(best[0]),'best_true_row_slack_normalized':str(best[0]/scale),'child_audits':child_audits,'full_certificate_checked_histories':verification.checked_histories,'full_certificate_checked_deviations':verification.checked_deviations,'certificate_terminal_history':[labels[a] for a in verification.terminal_history]}
(BASE/'materialized_row3_catalog.json').write_text(json.dumps(I.to_dict(),indent=2)+'\n')
(BASE/'materialized_row3_true_spe.json').write_text(json.dumps(certificate.to_dict(),indent=2)+'\n')
(BASE/'exact_materialized_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
