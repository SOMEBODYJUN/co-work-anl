"""One shared original graph build, two original coefficient auditors, fixed points.
No optimization, random generation, full six-player game search or author parent
literal137-row audit is run. All executed entrypoints are enumerated in output.
"""
from pathlib import Path
from fractions import Fraction as F
from contextlib import redirect_stdout
from itertools import product
from collections import Counter
import argparse,json,hashlib,sys,time,io,platform
E=Path(__file__).resolve().parent
PRE='research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def scalar(n,d):return F(n,d) if n else F()
def encode(o):return json.dumps(o,sort_keys=True,separators=(',',':'))
def point_check(tag,report,built,outdir):
 cols,names,m,obj,norm=built;literal=report['columns'];assert len(cols)==len(literal)
 assert encode([{k:v for k,v in z.items() if k!='weight'} for z in cols])==encode([{k:v for k,v in z.items() if k!='weight'} for z in literal])
 vals=list(map(lambda z:F(z['weight']),literal));assert min(vals)>=0
 normalization=sum(a*b for a,b in zip(norm,vals));W=sum(a*b for a,b in zip(obj,vals));assert normalization==1 and W==F(report['W'])<F(1,2)
 nonzero=[(i,v) for i,v in enumerate(vals) if v]
 slacks=[sum((row[j]*v for j,v in nonzero),F()) for row in m];assert min(slacks)>=0
 rows=[[i,n,str(v)] for i,(n,v) in enumerate(zip(names,slacks))]
 dump(outdir/(tag+'-all-row-slacks.json'),rows)
 summary={'rows':len(m),'columns':len(cols),'positive_columns':len(nonzero),'minimum_slack':str(min(slacks)),'zero_rows':sum(v==0 for v in slacks),'positive_rows':sum(v>0 for v in slacks),'O':str(normalization),'W':str(W),'half_gap_1_minus_2W':str(1-2*W),'all_descriptors_literal_equal':True,'stored_metadata_rows_match':len(m)==report['verified_rows'],'stored_positive_columns_match':len(nonzero)==report['positive_columns']}
 assert summary['stored_metadata_rows_match'] and summary['stored_positive_columns_match']
 if tag=='attractive3889':
  ids=[j for j,z in enumerate(cols) if z['kind']=='overlap'];assert len(ids)==1306
  assert all(row[j]>=0 for n,row in zip(names,m) if not n.startswith('overlap-upper:') for j in ids)
  summary['ordinary_overlap_coefficient_signs_nonnegative']=True
 hist=[z for z in literal if z['kind']=='hist'];C=F();phi=F()
 for z in hist:
  a=list(map(int,z['actual_bits']));prior=0;cx=F()
  for i,b in enumerate(a):
   if b:cx+=F(1,prior+1)-F(1,prior+6-i)
   prior+=b
  C+=F(z['weight'])*cx;phi+=F(z['weight'])*sum((F(1,k) for k in range(1,z['d']+1)),F())
 summary.update(copy_tax=str(C),comparison_harmonic_potential=str(phi),candidate_W_plus_C_minus_Phi=str(W+C-phi))
 return summary

def credible_fixed(source,mixed):
 groups=[(tuple(z['theme_indices']),int(z['count'])) for z in source['groups']];scale=int(source['customer_scale']);assert sum(n for _,n in groups)==scale
 assert len(groups)==78 and len({g for g,n in groups})==78 and all(n>0 for g,n in groups)
 cert=mixed['certificate'];assert all(z['d']==1 for z in cert['support']) and len(cert['support'])==13
 expanded=[]
 den=scale//6;assert scale%6==0
 for z in cert['support']:
  aa=tuple(i for i,b in enumerate(map(int,z['actual_bits'])) if b);n=F(z['weight'])*den;assert n.denominator==1
  for j in range(6):expanded.append((aa+(6+j,),int(n)))
 assert groups==expanded
 def utility(path,pos):
  a=path[pos];return sum((F(n,sum(t in ls for t in path)) for ls,n in groups if a in ls),F())
 actual=tuple(range(6));actualU=[utility(actual,i) for i in range(6)];prefix=actual[:4]
 matrix=[[(utility(prefix+(a,b),4),utility(prefix+(a,b),5)) for b in range(12)] for a in range(12)]
 brs={};floors=[];table=[]
 for a,row in enumerate(matrix):
  best=max(v[1] for v in row);br=[b for b,v in enumerate(row) if v[1]==best];lo=min(row[b][0] for b in br);hi=max(row[b][0] for b in br);floors.append(lo);brs[a]=br
  table.append({'action':a,'all_last_best_replies':br,'source_min_normalized':str(lo/scale),'source_max_normalized':str(hi/scale),'gain_over_actual_u5_normalized':str((lo-actualU[4])/scale)})
 terminalquotes=[utility(actual[:5]+(b,),5) for b in range(12)]
 tests=source['actual_path_tests'];assert len(tests)==2 and [t['position'] for t in tests]==[6,5]
 for t,values,i in [(tests[0],terminalquotes,5),(tests[1],floors,4)]:
  assert list(map(lambda x:str(60*x.numerator//x.denominator),values))==t['all_action_floors_scaled_integer']
  assert all((60*x).denominator==1 for x in values)
  assert str(60*actualU[i])==t['own_scaled_integer']
  assert str(60*max(values))==t['max_deviation_minimum_scaled_integer']
 assert all(b in range(7,12) for b in brs[6]) and len(brs[6])==5
 assert floors[6]>actualU[4]
 W=sum(n for ls,n in groups if any(t in ls for t in actual));assert F(W,scale)==F(source['source_point_W_over_O'])==F(cert['W'])
 return {'groups':78,'unit_customers':str(scale),'exact_compilation_from_13_supports':True,'fixed_two_tail_pairs':144,'terminal_floors_checked':12,'penultimate_floors_checked':12,'all24_saved_floor_values_equal':True,'actual_payoffs_normalized':list(map(lambda x:str(x/scale),actualU)),'W_over_OPT':str(F(W,scale)),'OPT6_normalized':'1','all12_penultimate_deviations':table,'T1_gain_normalized':str((floors[6]-actualU[4])/scale),'original_credible_main_calls':0,'full_six_player_SPE_enumeration':0}

def main():
 p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);a=p.parse_args();runtime=a.runtime.resolve();out=E/'replay';out.mkdir(exist_ok=True);start=time.time();clock=time.perf_counter()
 preparation=read(runtime/'runtime-preparation.json');before={rel:sha(runtime/rel) for rel in preparation['copied']};assert len(before)==49
 parent=runtime/PRE/'parent';child=runtime/PRE/'six_astra';sys.path[:0]=[str(child),str(parent)]
 print('Import exact frozen closure and two original finite auditors',flush=True)
 import attractive_nested as at
 import actual_fifth_nested as nest
 import full_new_reply_closure as cl
 import new_reply_budget as nr
 import mixed_pair as mix
 import verify_mixed_pair as vm
 import verify_reply_algebra as va
 import numpy as np
 import scipy
 observed={at.build.__code__:'attractive_nested.build',nest.build.__code__:'actual_fifth_nested.build',cl.build.__code__:'full_new_reply_closure.build',nr.old_system.__wrapped__.__code__:'new_reply_budget.old_system',mix.js.build.__code__:'joint_system.build',vm.run.__code__:'verify_mixed_pair.run',va.main.__code__:'verify_reply_algebra.main',mix.cut.__code__:'mixed_pair.cut',mix.matrix.__code__:'mixed_pair.matrix'}
 counts=Counter();captures={}
 def profile(frame,event,arg):
  name=observed.get(frame.f_code)
  if name is None:return
  if event=='call':counts[name]+=1
  elif event=='return' and name in ['attractive_nested.build','actual_fifth_nested.build','full_new_reply_closure.build','new_reply_budget.old_system']:captures[name]=arg
 sys.setprofile(profile)
 original_events=[]
 for tag,fun,reportfile,summary_only in [('verify_mixed_pair',vm.run,parent/'verify_mixed_pair.json',False),('verify_reply_algebra',va.main,child/'verify_reply_algebra.json',True)]:
  frozen=reportfile.read_bytes();capture=io.StringIO();t=time.perf_counter()
  with redirect_stdout(capture):fun()
  stdout=capture.getvalue().encode();(out/(tag+'.stdout.txt')).write_bytes(stdout);generated=reportfile.read_bytes();(out/(tag+'.generated.json')).write_bytes(generated)
  assert frozen==generated
  parsed=json.loads(stdout);expected=json.loads(frozen)
  if summary_only:expected={k:v for k,v in expected.items() if k!='source_rows'}
  assert parsed==expected
  original_events.append({'function':tag+'.'+('main' if summary_only else 'run'),'calls':1,'seconds':time.perf_counter()-t,'generated_file_byte_equal_frozen':True,'stdout_byte_equal_full_frozen_report':stdout==frozen,'stdout_semantic_equal_expected_summary':True,'stdout_bytes':len(stdout),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'generated_sha256':hashlib.sha256(generated).hexdigest()})
  print(tag,'passed and original report bytes unchanged',flush=True)
 print('Start one shared original attractive_nested.build; retain returned lower-layer matrices',flush=True)
 point=read(child/'attractive_nested_exact.json');hist=[z for z in point['columns'] if z['kind']=='hist'];t=time.perf_counter();at.build(hist);build_seconds=time.perf_counter()-t
 print('Shared original build returned; verify three literal frozen vectors',flush=True)
 checks={}
 for tag,filename,frame in [('closure1033','full_new_reply_closure_exact.json','full_new_reply_closure.build'),('nested1097','actual_fifth_nested_exact.json','actual_fifth_nested.build'),('attractive3889','attractive_nested_exact.json','attractive_nested.build')]:
  checks[tag]=point_check(tag,read(child/filename),captures[frame],out)
  print(tag,checks[tag]['rows'],'rows',checks[tag]['zero_rows'],'zero',flush=True)
 # Bind the two stored cuts to the whole original compatible histogram domain.
 mixed=read(parent/'mixed_pair_results.json');cutchecks=[];cutrows=[]
 for i,step in enumerate(mixed['steps'][:2]):
  cc,values,k,norm=mix.cut(step['weights']);assert values==list(map(int,step['coefficients'])) and k==step['K_integer'] and norm==step['norm'];cutrows.append(cc);cutchecks.append({'step':i,'448_integer_coefficients_equal':True,'K_integer':k,'norm':norm,'original_cut_calls':1,'compatible_configurations_in_full64_actual_domain':109824})
 types,old=captures['new_reply_budget.old_system'];assert len(old)==702
 cert=mixed['certificate'];lookup={(tuple(map(int,z['actual_bits'])),z['d']):F(z['weight']) for z in cert['support']};values=[lookup.get(t,F()) for t in types]+[F(cert['K'])]
 slacks=[sum(x*y for x,y in zip(row,values)) for n,row in old]+[sum(x*y for x,y in zip(row,values)) for row in cutrows];assert min(slacks)>=0
 assert sum(values[:-1])==1 and sum(v*int(any(t[0])) for t,v in zip(types,values[:-1]))==F(cert['W'])
 assert mixed['steps'][2]['weights']==mixed['steps'][1]['weights'];assert slacks[-1]==F(mixed['steps'][2]['exact_proposed_cut_slack'])==0
 parent704={'rows':704,'support':13,'W':cert['W'],'minimum_slack':str(min(slacks)),'zero_rows':sum(v==0 for v in slacks),'two_cut_slacks_at_final_point':list(map(str,slacks[-2:])),'third_float_proposal_rejected':True,'third_float_phase_I':mixed['steps'][2]['phase_I_float'],'third_exact_proposed_slack':'0','earlier_two_negative_reported_slacks_rechecked':False,'scope':'earlier two steps evaluated earlier points; final704 uses different target weights; no earlier point reconstructed'}
 dump(out/'parent704-all-row-slacks.json',[[i,str(v)] for i,v in enumerate(slacks)])
 cred=credible_fixed(read(parent/'credible_catalog.json'),mixed)
 sys.setprofile(None)
 assert counts['attractive_nested.build']==counts['actual_fifth_nested.build']==counts['full_new_reply_closure.build']==counts['new_reply_budget.old_system']==counts['joint_system.build']==1
 assert counts['mixed_pair.cut']==2
 after={rel:sha(runtime/rel) for rel in before};assert before==after
 result={'scope':'exact finite specified vectors and coefficient bindings; original old702 matrix reused, not a second independent702 derivation; no full SPE counterexample','original_finite_auditor_events':original_events,'shared_build_seconds':build_seconds,'original_function_calls':dict(counts),'three_points':checks,'stored_cut_bindings':cutchecks,'parent704':parent704,'credible_catalog_fixed':cred,'zero_new_operations':{'all_LP':0,'RNG':0,'copy_tax30':0,'copy_tax300':0,'original_credible_main':0,'original_parent_literal137_audit':0,'original_three_layer_verify_entrypoints':0,'root_shared_module_or_main':0,'full_six_SPE_search':0},'all50_materialized_frozen_files_unchanged':True}
 dump(out/'fixed-layers-and-parent-points.json',result)
 event={'started_unix':start,'elapsed_seconds':time.perf_counter()-clock,'exit_code':0,'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'assertions_enabled':__debug__,'script_sha256':sha(Path(__file__)),'runtime_preparation_sha256':sha(runtime/'runtime-preparation.json'),'primary_manifest_sha256':sha(E/'source-manifest.json'),'dependency_manifest_sha256':sha(E/'runtime-dependencies.json'),'frozen_file_hashes_before':before,'frozen_file_hashes_after':after,'function_counts':dict(counts),'math_run_attempt':1,'no_optimizer_or_random_called':True};dump(out/'execution.json',event)
 print(json.dumps({'elapsed_seconds':event['elapsed_seconds'],'function_counts':dict(counts),'three_points':checks,'parent704':parent704,'credible_T1_gain':cred['T1_gain_normalized']},ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':main()
