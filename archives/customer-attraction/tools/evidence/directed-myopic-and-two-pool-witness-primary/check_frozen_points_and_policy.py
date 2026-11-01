"""New deterministic exact check, not either original search main.

Import the unchanged integer Engine and Fraction DP for four saved points.
Check the complete saved two-pool policy by nine expanded unit customers and
the canonical certificate verifier. Never call RNG, linprog, milp, or Git.
"""
from pathlib import Path
import sys,json,importlib.util,itertools
from fractions import Fraction as F

HERE=Path(__file__).resolve().parent
ROOT=HERE/'replay-source-root'
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,StrategyCertificate,verify_certificate

def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
raw=HERE/'original/research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/credible'
source=ROOT/'research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/credible/myopic_directed_attack.py'
spec=importlib.util.spec_from_file_location('unchanged_original_directed_engine',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
Engine=module.Engine
from myopic_ceiling_dp import MyopicCeilingFloor

def check_saved_DP_points():
 frozen=read(raw/'myopic_directed_m4p6.json')
 assert frozen['m']==4 and frozen['p']==6 and frozen['rounds_requested']==frozen['rounds_done']==6000
 assert frozen['best_instance']==frozen['improvements'][-1]['instance'] and len(frozen['improvements'])==4
 engine=Engine(6,4);assert engine.L==12 and len(engine.states)==210 and len(engine.nonterm)==84 and len(engine.terminal)==126
 expected=[(6,'36',62,'18/31'),(799,'40',69,'40/69'),(1348,'37',64,'37/64'),(1438,'36',63,'4/7')]
 cases=[]
 for old,(iteration,G,opt,ratio) in zip(frozen['improvements'],expected):
  assert (old['iteration'],old['G'],old['OPT'],old['ratio'])==(iteration,G,opt,ratio)
  ins=Instance.from_dict(old['instance']);r=[0]*63
  for c in ins.customers:r[sum(1<<a for a in c.topics)-1]+=c.multiplicity
  assert all(isinstance(v,int) and 0<=v<=200 for v in r)
  assert engine.instance(r).to_dict()==old['instance']
  actual=engine.solve(r);dp=MyopicCeilingFloor(ins);root=dp.root();optimum=ins.optimal_welfare()
  assert actual==F(ratio)==root/optimum and root==F(G) and optimum==opt and actual>F(1,2)
  H,cost,floor,allowed=engine.last;states=[]
  for i,b in enumerate(engine.states):
   integer_H=frozenset(engine.states[engine.terminal[int(t)]] for t in H[i])
   assert integer_H==dp.terminals(b) and F(int(cost[i]),engine.L)==dp.cost(b)
   row={'counts':list(b),'terminal_counts':sorted(map(list,integer_H)),'scaled_G':int(cost[i]),'G':str(dp.cost(b))}
   if sum(b)<4:
    assert F(int(floor[i]),engine.L)==dp.floor(b) and tuple(allowed[i])==dp.allowed[b]
    row.update({'scaled_floor':int(floor[i]),'floor':str(dp.floor(b)),'allowed':list(allowed[i])})
   states.append(row)
  cases.append({'iteration':iteration,'r_by_masks_1_to_63':r,'customer_count':sum(r),'G':str(root),'OPT':optimum,'G_over_OPT':str(actual),'G_minus_half_OPT':str(root-F(optimum,2)),'count_states':210,'nonterminal_count_states':84,'terminal_count_states':126,'all_H_floor_allowed_G_match':True,'states':states})
 return {'frozen_search_rounds_reported_not_replayed':6000,'original_random_main_entries':0,'saved_distinct_points':4,'best_instance_is_duplicate_last_point':True,'LCM':12,'bounded_int64_contract':{'r_max':200,'masks':63,'coefficient_max':12,'each_dot_upper':151200,'G_upper':604800,'below_int64_max':True},'total_count_states_compared':840,'total_nonterminal_count_states_compared':336,'total_terminal_count_states_compared':504,'not_ordered_policy_histories':True,'cases':cases}

def check_nine_unit_policy():
 report=read(raw/'two_pool_inverse.json');point=report['exact_witness'];ins=Instance.from_dict(point['instance']);cert=StrategyCertificate.from_dict(point['strategy'])
 assert ins.players==3 and ins.topic_count==6 and len(cert.actions)==43
 units=tuple(c.topics for c in ins.customers for _ in range(c.multiplicity));assert len(units)==9
 masks={sum(1<<a for a in c.topics):c.multiplicity for c in ins.customers}
 assert masks=={1:1,15:2,16:1,18:2,32:1,36:2}
 assert point['parameters']=={'x':2,'a':1,'b1':2,'d1':1,'b2':2,'d2':1}
 assert F(point['a_minus_half_x'])==F(masks[1])-F(masks[15],2)==0
 actions=dict(cert.actions)
 expected={h for d in range(3) for h in itertools.product(range(6),repeat=d)}
 assert set(actions)==expected
 def finish(h):
  while len(h)<3:h=h+(actions[h],)
  return h
 def payoff(path,i):
  return sum((F(1,sum(a in T for a in path)) for T in units if path[i] in T),F())
 def welfare(path):return sum(bool(set(path)&T) for T in units)
 audit=[];slacks=[]
 for h in sorted(expected,key=lambda q:(len(q),q)):
  chosen=actions[h];branches=[finish(h+(a,)) for a in range(6)]
  values=[payoff(path,len(h)) for path in branches]
  current=values[chosen];ds=[current-v for v in values];assert min(ds)>=0
  slacks.extend(ds)
  audit.append({'history':list(h),'chosen':chosen,'terminal_branches':list(map(list,branches)),'profits_by_action':list(map(str,values)),'chosen_minus_each_action':list(map(str,ds))})
 canonical=verify_certificate(ins,cert);canonical.assert_valid()
 assert canonical.checked_histories==43 and canonical.checked_deviations==215 and canonical.terminal_history==(3,4,5) and canonical.terminal_counts==(0,0,0,1,1,1)
 root=finish(());profits=tuple(payoff(root,i) for i in range(3));W=welfare(root)
 optimum=max(welfare(a) for a in itertools.product(range(6),repeat=3))
 assert root==(3,4,5) and profits==(F(2),F(3),F(3)) and W==8 and optimum==9 and welfare((0,4,5))==9 and sum(profits)==W
 assert audit[0]['profits_by_action']==['2']*6 and actions[(3,4)]==5 and actions[(4,3)]==2
 last=[next(x for x in audit if x['history']==[a,b])['profits_by_action'] for a in range(6) for b in range(6)]
 second=[next(x for x in audit if x['history']==[a])['profits_by_action'] for a in range(6)]
 last_best=[[str(max(map(F,last[6*a+b]))) for b in range(6)] for a in range(6)]
 return {'unit_customers':9,'players':3,'labels':6,'complete_ordered_histories':43,'action_comparisons_including_self':len(slacks),'nonself_comparisons':215,'minimum_slack':str(min(slacks)),'canonical_valid':canonical.valid,'canonical_histories':canonical.checked_histories,'canonical_nonself_deviations':canonical.checked_deviations,'actual_root_path':list(root),'root_profit_by_action':audit[0]['profits_by_action'],'actual_player_profits':list(map(str,profits)),'W':W,'OPT3':optimum,'optimum_witness':[0,4,5],'W_over_OPT':str(F(W,optimum)),'two_W_minus_OPT':2*W-optimum,'a_minus_half_x':'0','not_count_Markov_policy':{'history34_action':5,'history43_action':2},'last_best_value_matrix_rows_first_columns_second':last_best,'second_profit_matrix_rows_first_columns_action':second,'all_history_action_tables':audit,'original_MILP_or_LP_entries':0,'floating_optimal_zero_not_certified_as_upper_bound':True}

assert len(sys.argv)==2 and not sys.flags.optimize
out=Path(sys.argv[1]);assert not out.exists(),'preserve one actual new deterministic execution'
result={'identity':'new exact frozen-point and complete-policy check; no original search main','saved_DP_points':check_saved_DP_points(),'two_pool_complete_policy':check_nine_unit_policy(),'original_search_main_entries':0,'old_successful_original_entries_rerun':0,'new_deterministic_exact_entry':1,'random_search_LP_MILP_entries':0}
write(out,result)
print(json.dumps({'status':'PASS','DP_saved_points':4,'DP_count_states':840,'complete_policy_histories':43,'all_action_comparisons_including_self':258,'canonical_nonself_deviations':215,'root_W':8,'OPT3':9,'original_search_main_entries':0,'new_deterministic_exact_entry':1}))
