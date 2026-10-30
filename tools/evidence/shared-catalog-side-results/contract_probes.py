from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'replay'))
from facility_spe.exact import shared_offdiag as exact
from facility_spe.cli import verify_phi as independent

def serial(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [serial(v) for v in x]
 return x

def direct(instance,rec):
 w=list(map(F,instance['weights']));S=list(map(set,instance['locations']));s,t=rec['layout'];p=list(map(F,rec['prob_first']));common=sorted(S[s]&S[t]);assert common==rec['shared'];a=sum((w[i] for i in S[s]-S[t]),F());b=sum((w[i] for i in S[t]-S[s]),F());x=a+sum((w[i]*z for i,z in zip(common,p)),F());y=b+sum((w[i]*(1-z) for i,z in zip(common,p)),F());assert list(map(F,rec['loads']))==[x,y]
 for i,z in zip(common,p):
  c1=a+w[i]+sum((w[j]*q for j,q in zip(common,p) if j!=i),F());c2=b+w[i]+sum((w[j]*(1-q) for j,q in zip(common,p) if j!=i),F());assert 0<=z<=1 and (not z or c1<=c2) and (z==1 or c2<=c1)

m=json.loads((HERE/'math-results.json').read_text());fixtures=[('simple',{'weights':[8,40,23],'locations':[[0,1],[2],[1]]},F(23,20)),('three',{'weights':[7071,2929,5000],'locations':[[0,1],[0],[2]]},F(7071,5000))]
for i,x in enumerate(m['sparse_exact_fixtures']['four_no_loss']):fixtures.append((f'four_no_loss_{i}',x['instance'],F(x['z'])))
x=m['sparse_exact_fixtures']['four_epsilon'];fixtures.append(('four_epsilon',x['instance'],F(6327,4000)))
base={'weights':[1236068,762932,381966,72949,18221,763932],'locations':[[0,5],[0,1],[0,2],[0,3],[1,2,3,4],[5]]};fixtures.extend([('six',base,F(499750,309017)),('five',{**base,'U1':list(range(5)),'U2':list(range(5))},F(499750,309017))])
records=[];layouts=0
for name,instance,wanted in fixtures:
 out=exact.solve(instance);assert out['alpha']==wanted;exact.verify(instance,out);cat=instance.get('U1',list(range(len(instance['locations']))))
 for s in cat:
  for t in cat:direct(instance,exact.continuation(instance,out,s,t));layouts+=1
 records.append({'name':name,'expected_alpha':wanted,'actual_alpha':out['alpha'],'local_calls':out['local_calls'],'distinct_overlap':out['distinct_overlap'],'layout':out['on_path']['layout']})
instance=fixtures[0][1];out=exact.solve(instance)
loose=deepcopy(out);loose['alpha']=F(2);assert exact.verify(instance,loose) is None
text=deepcopy(out);text['default_continuation']='unsupported arbitrary metadata';assert exact.verify(instance,text) is None
bad=deepcopy(out);bad['on_path']['loads']=[F(),F()];s,t=bad['on_path']['layout'];assert exact.continuation(instance,bad,s,t)['loads']==[F(),F()]
try:exact.verify(instance,bad)
except ValueError:pass
else:raise AssertionError('bad loads must be rejected by verifier')
# A hand-derived complete rule: all two clients independently flip fair coins.
ins={'weights':[1,1],'locations':[[0,1],[0,1]]}
def wit(pair):return {'layout':pair,'common':[0,1],'prob_first':['1/2','1/2'],'loads':[1,1]}
cert={'factor':1,'on_path':wit([0,1]),'deviations':[{'deviator':1,'witness':wit([1,1])},{'deviator':2,'witness':wit([0,0])}],'default_continuation':independent.DEFAULT_CONTINUATION}
assert independent.verify(ins,cert)
meta=deepcopy(cert);meta.update(response_cycle='unchecked',menu_threats='unchecked',guarantee='unchecked');assert independent.verify(ins,meta)
rejects=0
for mutate in ['bad_default','bad_NE','duplicate_deviation','too_large_factor']:
 c=deepcopy(cert)
 if mutate=='bad_default':c['default_continuation']='arbitrary text'
 if mutate=='bad_NE':c['on_path']['prob_first']=['1/4','3/4']
 if mutate=='duplicate_deviation':c['deviations'].append(deepcopy(c['deviations'][0]))
 if mutate=='too_large_factor':c['factor']='1619/1000'
 try:independent.verify(ins,c)
 except ValueError:rejects+=1
 else:raise AssertionError(mutate)
res={'scope':'Direct canonical module probes in the minimum hash-verified tree; NOT original unittest/script suites','exact_solver_fixtures':records,'complete_tagged_layout_profiles_directly_checked':layouts,'attainment_checker_accepts_larger_valid_alpha_2':True,'attainment_checker_does_not_validate_default_metadata':True,'continuation_does_not_automatically_validate_saved_records':True,'separate_verify_rejects_forged_loads':True,'independent_CLI_hand_rule_and_metadata_variant_accepted':2,'independent_CLI_semantic_mutants_rejected':rejects,'original_test_suites_run':False,'not_claimed':['original 753-game test script replayed','6/11 unittest suites replayed','missing code or fixtures reconstructed from formulas','universal theorem verified by these finite probes']}
(HERE/'contract-results.json').write_text(json.dumps(serial(res),ensure_ascii=False,indent=2)+'\n');print(json.dumps(serial(res),ensure_ascii=False,indent=2))
