"""One exact decimal-data comparison using an existing exact payoff table.

No original imports, new payoff construction, SPE/IC audit, or optimization.
The decimal probabilities are evaluated literally, without rational recovery.
"""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
OLD=Path('/workspace/scratch/c0ab78c47566/boss7-cleaner/archives/customer-attraction/tools/evidence/security-cartesian-and-disjoint-primary')
OUT=HERE/'reported-data-audit.json'
if OUT.exists():raise SystemExit('Already completed; do not rerun data arithmetic')
def digest(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(v) for v in x]
 return x
started=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
seedfile=HERE/'cartesian_convexification_k4.json';packetfile=HERE/'cartesian_two_copy_exact.json'
oldfile=OLD/'new-product-and-security-check.json'
data=json.loads(seedfile.read_text(),parse_float=F);s=data['analysis'];packet=json.loads(packetfile.read_text())
old=json.loads(oldfile.read_text())['cartesian']
assert s['k']==4 and s['weights']==packet['base_weights']==[0,0,5,9,5,4,7,9,6,3,8,9,1,6,0]
assert sum(s['weights'])==old['unit_customers_base']==72
pay={tuple(r['triple']):tuple(map(F,r['utilities'])) for r in old['base_payoffs']}
assert len(pay)==64
br={(r['a'],r['b']):r['last_best_replies'] for r in old['L']}
phi=tuple(map(F,old['phi']));g=F(old['g'])
root=[]
for a,mix in enumerate(s['root_minimizers']):
 mass=sum((p for z,p in mix),F(0))
 assert all(z[0]==a and z[2] in br[z[0],z[1]] and p>=0 for z,p in mix)
 u=tuple(sum((p*pay[tuple(z)][i] for z,p in mix),F(0)) for i in range(3))
 root.append(dict(a=a,literal_terms=mix,literal_mass=mass,mass_minus_one=mass-1,literal_payoffs=u,
     literal_second_surplus=u[1]-phi[a]*mass,root_mean_minus_saved=u[0]-s['root_floor_by_action'][a],
     exact_preexisting_g=old['g_details'][str(a)]['g'],preexisting_dual_lambda=old['g_details'][str(a)]['dual_lambda']))
actual=[(tuple(r['terminal']),r['probability']) for r in s['actual_mix']]
assert len(actual)==3 and all(z[2] in br[z[0],z[1]] and p>=0 for z,p in actual)
mass=sum((p for z,p in actual),F(0))
u=tuple(sum((p*pay[z][i] for z,p in actual),F(0)) for i in range(3))
second=sum((p*(pay[z][1]-phi[z[0]]) for z,p in actual),F(0))
actual_result=dict(literal_terms=actual,literal_mass=mass,mass_minus_one=mass-1,literal_payoffs=u,
    payoff_minus_saved=[v-z for v,z in zip(u,s['actual_payoffs'])],literal_W=sum(u),W_minus_saved=sum(u)-s['relaxed_W'],
    literal_second_surplus=second,saved_second_surplus=s['actual_second_surplus'],
    literal_root_margin_against_exact_g=u[0]-g*mass,saved_first_margin=s['actual_first_margin'])
B=list(combinations_with_replacement(range(4),2))
query=s['query'];qmass=sum(query,F(0))
query_values=[dict(background=b,value=sum((query[a]*pay[(a,)+b][0] for a in range(4)),F(0))) for b in B]
opponent=[(tuple(r['background']),r['probability']) for r in s['opponent']]
omass=sum((p for b,p in opponent),F(0))
opponent_values=[sum((p*pay[(a,)+b][0] for b,p in opponent),F(0)) for a in range(4)]
static=dict(query=query,query_mass=qmass,query_mass_minus_one=qmass-1,all10_background_values=query_values,
    literal_query_min=min(r['value'] for r in query_values),opponent=opponent,opponent_mass=omass,
    opponent_mass_minus_one=omass-1,all4_query_values_against_opponent=opponent_values,
    literal_opponent_max=max(opponent_values),saved_security=s['security'],
    literal_gap_from_saved_W_and_security=s['relaxed_W']-3*s['security'],saved_gap=s['gap'],
    note='Literal decimal-weight linear forms only; masses are not silently normalized, no exact value certification or rational recovery.')
original_policy={tuple(r['history']):r['action'] for r in packet['policy']}
old_policy={tuple(r['history']):r['action'] for r in old['all273_policy_entries']}
assert original_policy.keys()==old_policy.keys() and len(original_policy)==273
differences=[dict(history=h,author_action=a,previous_independent_action=old_policy[h])
    for h,a in original_policy.items() if a!=old_policy[h]]
assert packet['actual_components']==old['actual_component_actions']
assert packet['payoffs']==old['actual_utilities'] and F(packet['W'])==old['W']
summary=dict(status='PASS',new_data_arithmetic_entries=1,original_entries=0,new_payoff_tables=0,
    LP_calls=0,new_IC_comparisons=0,BI_calls=0,rational_probability_recovery=False,
    inputs=[digest(p) for p in [seedfile,packetfile,oldfile]],
    source_top_fields=list(data),analysis_fields=list(s),packet_fields=list(packet),
    root_mixture_literal_checks=root,actual_mixture_literal_check=actual_result,static_literal_checks=static,
    shared_exact_results=dict(phi=old['phi'],g=old['g'],G1=old['G1'],G2=old['G2'],
       old_policy_origin=old['policy_origin'],OPT=old['OPT'],OPT_witness=old['OPT_witness'],
       base_v3_upper=old['base_v3_upper'],joint_strong_aggregate_slack_lower=old['joint_strong_aggregate_slack_lower']),
    policy_data_comparison=dict(total_nodes=273,equal_actions=273-len(differences),different_actions=len(differences),
       differences=differences,same_actual_path=True,same_actual_utilities=True,IC_recomputed=False),
    scope='Only reported decimal mixture arithmetic and full action-map data comparison using a previously certified exact table; no new finite equilibrium or optimization audit.')
OUT.write_text(json.dumps(enc(summary),ensure_ascii=False,indent=2)+'\n')
event=dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.perf_counter()-clock,
    script=digest(Path(__file__)),report=digest(OUT),original_entries=0,LP_calls=0,new_IC_comparisons=0,
    new_data_arithmetic_entries=1,new_payoff_tables=0)
(HERE/'reported-data-execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc(dict(status='PASS',policy_differences=len(differences),root_mass_deltas=[x['mass_minus_one'] for x in root],
    actual_mass_delta=mass-1,actual_second_surplus=second,query_mass_delta=qmass-1,opponent_mass_delta=omass-1,
    source_analysis_fields=len(s),packet_fields=len(packet),wall_seconds=event['wall_seconds'])),ensure_ascii=False))
