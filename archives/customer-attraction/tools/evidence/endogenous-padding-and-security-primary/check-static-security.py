"""Verify one finite integer-opponent v4 primal/dual certificate exactly; no LP or SPE oracle."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import hashlib,json
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text())
def primary(i):
 x=next(x for x in M if x['id']==i);p=E/'original'/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'];return json.loads(p.read_text()),x
ins,xi=primary('0ebc828733fab492d2a5');cert,xc=primary('8dc3d81738c6ed662858');assert ins['players']==cert['players_in_static_security']==4 and len(ins['topics'])==7 and cert['topics']==ins['topics'];clients=[(frozenset(x['topics']),x['multiplicity'])for x in ins['customers']];assert sum(n for t,n in clients)==53 and len(clients)==14
p=list(map(F,cert['primary']));q=[(tuple(x['rivals']),F(x['probability']))for x in cert['dual']];t=F(cert['value']);assert len(p)==7 and min(p)>=0 and sum(p)==1 and len(q)==7 and all(len(z)==3 and all(a in range(7)for a in z)and v>=0 for z,v in q)and sum(v for z,v in q)==1
profiles=list(combinations_with_replacement(range(7),3));assert len(profiles)==84
def payoff(a,z):return sum((F(n,1+sum(b in likes for b in z))for likes,n in clients if a in likes),F())
matrix=[[payoff(a,z)for z in profiles]for a in range(7)];columns=[]
for i,z in enumerate(profiles):
 value=sum((p[a]*matrix[a][i]for a in range(7)),F());margin=(value-t)*70176;assert value>=t and margin.denominator==1
 columns.append({'rivals':list(z),'expected_primal_payoff':str(value),'margin_above_value':str(value-t),'integer_margin_scale70176':int(margin)})
dualrows=[sum((v*payoff(a,z)for z,v in q),F())for a in range(7)];assert min(F(x['expected_primal_payoff'])for x in columns)==max(dualrows)==t and all(x==t for x in dualrows)
tight=[x['rivals']for x in columns if F(x['expected_primal_payoff'])==t];assert all(list(z)in tight for z,v in q if v>0)
out={'scope':'one53-unit4-player static security game: unit query vs3 nonadaptive integer opponent themes; exact matrix and primal/dual verification, no dynamic SPE claim','input_primary_ids':[xi['id'],xc['id']],'input_sha256':{xi['id']:xi['sha256'],xc['id']:xc['sha256']},'unit_customers':53,'topics':ins['topics'],'query_actions':7,'opponent_slots':3,'integer_opponent_multisets':84,'matrix_entries':588,'value':str(t),'primary_probabilities':list(map(str,p)),'primary_sum':'1','primal_minimum':str(min(F(x['expected_primal_payoff'])for x in columns)),'primary_column_results':columns,'tight_opponent_profiles':tight,'dual_distribution':[{'rivals':list(z),'probability':str(v)}for z,v in q],'dual_sum':'1','dual_pure_query_payoffs':list(map(str,dualrows)),'dual_maximum':str(max(dualrows)),'primal_margin_integer_scale':70176,'value_times_scale70176':int(t*70176),'full_matrix_query_rows':[[str(v)for v in row]for row in matrix],'matrix_columns':list(map(list,profiles)),'exact_optimality_proved':True,'new_LP_calls':0,'new_SPE_solver_calls':0,'new_original_program_calls':0,'interpretation':'Four includes the querying player; not four rivals, fractional rivals, adaptive query-observing rivals, or a per-history SPE payoff floor'}
(E/'static-security-exact.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'value':str(t),'columns':84,'entries':588,'tight_columns':tight,'dual_payoffs':list(map(str,dualrows)),'value_integer_scaled':out['value_times_scale70176'],'new_LP_calls':0,'new_SPE_solver_calls':0},ensure_ascii=False))
