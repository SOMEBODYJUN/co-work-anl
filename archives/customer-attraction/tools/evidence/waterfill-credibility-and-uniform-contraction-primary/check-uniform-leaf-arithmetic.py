"""One separate data-only check: actual leaf spectrum/7 queries/two terminal buckets.
No original import/function calls, no full SPE or equilibrium search.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-waterfill-credibility-and-uniform-contraction-primary';assert json.loads((W/'primary-authorization-check.json').read_text())['status']=='pass-with-independent-sync-recovery'
rows=json.loads((E/'dependency-manifest.json').read_text())['rows'];ip=S/next(a['path'] for a in rows if a['id']=='0ebc828733fab492d2a5');sp=S/next(a['path'] for a in rows if a['id']=='2cd505cd05ed8ab77f21');I=json.loads(ip.read_text());A={tuple(a['history']):a['action'] for a in json.loads(sp.read_text())['actions']};customers=[frozenset(a['topics']) for a in I['customers'] for _ in range(a['multiplicity'])];tail=(0,3,4);counts=[sum(t in c for t in tail) for c in customers];spectrum=Counter(counts);assert dict(spectrum)=={1:6,2:15,3:11,0:21};fresh=[sum((F(1,k) for c,k in zip(customers,counts) if t in c),F()) for t in tail];assert fresh==[F(29,3),F(67,6),F(67,6)]
spectral=sum((F(k,(k+1)**2) for k in counts if k),F());assert spectral==F(331,48);lam=F(84796,85443);t=F(28481,2924);D=F(647,8772);assert fresh[0]/lam==t and fresh[0]-spectral==F(133,48)
credits=[sum((1/(1+lam*k)-F(1,1+k) for c,k in zip(customers,counts) if q in c),F()) for q in range(7)];pool=sum((1/(1+lam*k)-F(1,1+k) for k in counts),F());assert max(credits)==F(187117307516351,4918136562477105) and pool==F(206474219394865,3934509249981684)<D and 0<=min(credits)<=max(credits)<=pool
assert pool<=D-F(133,48)*(1/lam-1) and sum(fresh)-3*lam*t==3
sub=[(h,a) for h,a in A.items() if h and h[0]==6];assert len(sub)==57 and all(a!=6 for h,a in sub)
buckets=Counter()
for sign,z in [(1,(0,0,6,1)),(-1,(0,0,6,2))]:
 for c in customers:
  if z[3] in c:buckets[(int(z[0] in c),sum(v in c for v in z[1:]))]+=sign
buckets={k:v for k,v in buckets.items() if v};assert buckets=={(1,2):3,(0,1):-1};assert A[(0,0,6)]==1 and 3*lam/(1+2*lam)-1==F(-647,255035)
out=E/'uniform-leaf-arithmetic-check.json';assert not out.exists();report={'status':'pass-separate-data-only-actual-leaf-and-one-terminal-symbolic-comparison','entry_calls':1,'original_source_function_calls':0,'new_full400_SPE_scans':0,'new_2800_comparisons':0,'uniform_contraction_original_entry_calls':0,'input_hashes':{ip.name:hashlib.sha256(ip.read_bytes()).hexdigest(),sp.name:hashlib.sha256(sp.read_bytes()).hexdigest()},'actual_tail':tail,'actual_spectrum':{str(k):v for k,v in sorted(spectrum.items())},'original_fresh_utilities':list(map(str,fresh)),'a_star':str(min(fresh)),'S':str(spectral),'a_star_minus_S':str(min(fresh)-spectral),'lambda0':str(lam),'true_t0_from_source_matching_certificate':str(t),'D':str(D),'seven_query_credits':list(map(str,credits)),'max_seven_queries':str(max(credits)),'all_customer_H0':str(pool),'Vminus3lambda_t':str(sum(fresh)-3*lam*t),'P_child_decision_rows_inspected_without_IC':len(sub),'P_child_all_prescribed_actions_avoid_P':True,'two_terminal_leaves':[[0,0,6,1],[0,0,6,2]],'signed_terminal_buckets':[{ 'background_first_root_covered':b,'three_tail_coverage':k,'signed_customers':v} for (b,k),v in buckets.items()],'terminal_profit_gap_at_lambda0':'-647/255035','claimed36_other_tree_flips_not_recomputed':True,'root_seven_IC_not_recomputed':True,'general_n_lambda_c_proof_not_finite_sampling':True}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['input_hashes','seven_query_credits','signed_terminal_buckets']},ensure_ascii=False))
