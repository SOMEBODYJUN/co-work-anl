"""Independent fixed-policy matrix/46 stored duals and P1/P2 arithmetic; no LP or original imports."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import hashlib,json
E=Path(__file__).resolve().parent;M=json.loads((E/'source-manifest.json').read_text());old=json.loads((E/'original'/next(x['path']for x in M if x['id']=='99b5fe51e039efd9f405')).read_text());obs=json.loads((E/'replay/fixed-cone/passive-observation.json').read_text());data=json.loads((E/'dependencies/evidence/certificates/customer_attraction/individual_security_failure.json').read_text())['strategy'];actions={tuple(x['history']):x['action']for x in data['actions']};types=[tuple(a for a in range(6)if mask>>a&1)for mask in range(1,64)];hist=[h for d in range(3)for h in product(range(6),repeat=d)];assert set(actions)==set(hist)
def finish(h):
 while len(h)<3:h=h+(actions[h],)
 return h
def pay(h,a):return [F(1,sum(b in t for b in h))if a in t else F(0)for t in types]
def comps(n,k):
 if k==1:return [(n,)]
 return [(a,)+q for a in range(n+1)for q in comps(n-a,k-1)]
H=[sum((F(1,j)for j in range(1,c+1)),F())for c in range(5)]
def phi(q):return [H[sum(q[a]for a in t)]for t in types]
A=[];index=[]
for h in hist:
 on=pay(finish(h),actions[h])
 for a in range(6):
  if a==actions[h]:continue
  off=pay(finish(h+(a,)),a);index.append({'row':len(A),'kind':'alternative-minus-prescribed-full-IC','history':list(h),'alternative':a,'prescribed':actions[h]});A.append([b-c for b,c in zip(off,on)]+[F(0)])
for q in comps(3,6):index.append({'row':len(A),'kind':'three-slot-potential-minus-P','counts':list(q)});A.append(phi(q)+[F(-1)])
eq=pay(finish(()),actions[()])+[F(0)]
assert [[str(x)for x in row]for row in A]==obs['exact_constraint_rows']and list(map(str,eq))==obs['exact_root_equality']and len(A)==271
certs=[]
for d in old['exact_dual_certificates']:
 ys={i:F(y)for i,y in d['inequality_multipliers']};ye=F(d['equality_multiplier']);c=[a-b for a,b in zip(eq[:-1],phi(d['q']))]+[F(1)];res=[c[j]-sum((A[i][j]*y for i,y in ys.items()),F())-eq[j]*ye for j in range(64)];assert len(ys)==len(d['inequality_multipliers'])and max(ys.values())<=0 and min(res)==F(d['minimum_nonnegative_variable_residual'])==0 and ye>=0
 certs.append({'q':d['q'],'equality_multiplier':str(ye),'max_gap_upper_bound':str(-ye),'nonzero_inequality_multipliers':len(ys),'residual_coordinates':64,'minimum_residual':str(min(res)),'status':'exact valid on fixed normalized cone'})
assert len(certs)==46 and [z['q']for z in certs]==[z['q']for z in old['candidate_results'][:-1]]
base=E/'replay/fixed-cone/source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/global';instance=json.loads((base/'pi_fixed_cone_counterexample.json').read_text())['instance'];customers=instance['customers']
def potential(z):return sum((row['multiplicity']*H[sum(a in row['topics']for a in z)]for row in customers),F())
P={str(n):max(potential(z)for z in combinations_with_replacement(range(6),n))for n in [1,2]};assert P=={'1':F(144),'2':F(246)}
knownbase=E/'replay/known-cases/source-root/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/global';report=json.loads((knownbase/'potential_increment_diagnostic.json').read_text());knownobs=json.loads((E/'replay/known-cases/passive-observation.json').read_text());oldknown=json.loads((E/'original'/next(x['path']for x in M if x['id']=='7778aef9866288463707')).read_text());assert report==oldknown==knownobs['actual_source_cases'];assert len(knownobs['threshold_returns'])==14 and knownobs['verify_certificate_calls']==knownobs['solver_certificate_calls']==0;assert all(F(x['P_r1'])-F(x['P_r'])==F(x['delta'])and F(x['root_floor_all_SPE'])-F(x['delta'])==F(x['margin'])>=0 for x in report)
fixedstdout=(E/'replay/fixed-cone/stdout.txt').read_text();line,rest=fixedstdout.split('\n',1);prefix='EXACT_PI_COUNTEREXAMPLE ';assert line.startswith(prefix);candidate=json.loads(line[len(prefix):]);summary=json.loads(rest);assert candidate==json.loads((base/'pi_fixed_cone_counterexample.json').read_text());assert summary=={k:v for k,v in old.items()if k not in ['candidate_results','exact_dual_certificates']}
knownstdout=[json.loads(line)for line in (E/'replay/known-cases/stdout.txt').read_text().splitlines()];assert knownstdout==report
newreport=base/'pi_fixed_cone_diagnostic.json';oldreport=E/'original'/next(x['path']for x in M if x['id']=='99b5fe51e039efd9f405');assert newreport.read_bytes()==oldreport.read_bytes()
results={'scope':'one independent data-only fixed-matrix and stored-dual verification; P1/P2 closed arithmetic; no LP, source import, solver, new policy or original rerun','matrix':{'types':63,'variables_including_P':64,'full_ordered_nodes':43,'nonself_IC_rows':215,'all_three_slot_potential_rows':56,'total_rows':271,'equals_passive_original_matrix':True,'residual_coordinates_checked':46*64},'old_report':{'candidates_tested':47,'candidate_total':126,'unvisited':79,'exact_nonpositive_duals_checked':len(certs),'zero_equality_multiplier_certificates':sum(F(x['equality_multiplier'])==0 for x in certs),'dual_certificates':certs,'positive_index1':47,'positive_counts':old['numeric_best_q'],'positive_float_gap':old['numeric_best_gap'],'exact_positive_gap_normalized':obs['last_exact_gap_normalized'],'old_false_all_tested_field_reason':'first46 exact nonpositive certified, last47 positive witness; false is not failure of those46 duals'},'primary_MD_extra_values':{'P1':str(P['1']),'P2':str(P['2']),'arithmetic_profiles_checked':27,'increments':['144','102','83','215/2'],'nonconcave_increase_4_vs_3':'49/2'},'known_report':{'rows':14,'equal_frozen_bytes':(knownbase/'potential_increment_diagnostic.json').read_bytes()==(E/'original'/next(x['path']for x in M if x['id']=='7778aef9866288463707')).read_bytes(),'threshold_returns':14,'actual_solver_certificate_calls':0,'actual_verify_certificate_calls':0,'zero_margins':sum(F(x['margin'])==0 for x in report),'min_margin':str(min(F(x['margin'])for x in report)),'negative_margins':0,'new_counterexample_output_exists':(knownbase/'potential_increment_counterexample.json').exists()},'stdout':{'fixed_first_line_exact_candidate_then_pretty_summary':True,'fixed_stdout_not_full_diagnostic':True,'known14_JSON_lines_reconstruct_full_report':True,'known_stdout_not_pretty_report_bytes':True},'new_original_calls_in_this_checker':0,'new_LP_calls_in_this_checker':0}
(E/'constraint-index.json').write_text(json.dumps({'variables':[list(t)for t in types]+['P'],'rows':index},ensure_ascii=False,indent=2)+'\n');(E/'stored-certificates-check.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in results.items()if k!='old_report'},ensure_ascii=False));print('duals',len(certs),'zero multipliers',results['old_report']['zero_equality_multiplier_certificates'])
