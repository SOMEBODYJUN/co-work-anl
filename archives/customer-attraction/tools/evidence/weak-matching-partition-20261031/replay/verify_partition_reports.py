from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source'

def sha(p): return len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest()
expected={
 'partition_examples_seed104216.json': {'id':'acba20524372cf3f45ea','size':62093,'sha':'ef35c725d0996aa2c9c40ab82405452c5f46a06f186596221abba3a803804225','cones':47,'records':217,'success':191,'failed':26,'params':{'topics':6,'players':4,'games':48,'seed':104216,'query_mode':'partition'},'best':{'game':11,'mode':'uniform_credible','target':[0,1],'rows':21,'actual':[4,3],'min_matching_ratio':1.0000000000000002}},
 'partition_p6m4_seed104213.json': {'id':'bc533ffdcb3a1e45d173','size':207963,'sha':'c19849a3127d73a8fa72ba985446d6e23a195a1973f49869fc938eb940d401ca','cones':196,'records':588,'success':575,'failed':13,'params':{'topics':6,'players':4,'games':200,'seed':104213,'query_mode':'partition'},'best':{'game':88,'mode':'max_credible_payoff','target':[0,1,2,3],'rows':280,'actual':[2,2,2,2],'min_matching_ratio':1.0000000000000002}},
 'partition_p7m5_seed104214.json': {'id':'b04e4dc3e95e6066048a','size':476792,'sha':'fc4ddd68b1542d0ca342ccb66677c7c81c9a1af9d54b7ccf9ccaba1f3a14ea4e','cones':99,'records':297,'success':268,'failed':29,'params':{'topics':7,'players':5,'games':100,'seed':104214,'query_mode':'partition'},'best':{'game':3,'mode':'uniform_credible','target':[0,1,3,4,5],'rows':1260,'actual':[0,0,0,0,0],'min_matching_ratio':1.0000000000000002}},
}
for name,e in expected.items():
 p=SRC/name; assert sha(p)==(e['size'],e['sha']), (name,sha(p))
 d=json.loads(p.read_text()); assert d['status']=='no_floating_separator_in_finite_policy_sample'; assert d['policy_cones']==e['cones']; assert len(d['records'])==e['records']
 for k,v in e['params'].items(): assert d['parameters'][k]==v,(name,k,d['parameters'][k],v)
 ok=[r for r in d['records'] if r['success']]; bad=[r for r in d['records'] if not r['success']]; assert (len(ok),len(bad))==(e['success'],e['failed'])
 b=d['best'];
 for k,v in e['best'].items(): assert b[k]==v,(name,k,b[k],v)
 assert len(b['weights'])==(2**len(b['instance']['topics'])-1)
 assert len(b['certificate']['actions'])==sum(len(b['instance']['topics'])**j for j in range(b['instance']['players']))
 # partition mode's separator threshold is 1; values may be below 1, but no successful value may exceed it by the source's 1e-7 early-stop margin.
 assert max((r['min_matching_ratio'] for r in ok),default=-1) <= 1+1e-7
for name, expected_best in [('p6_partition_one_game.json',0.8139652647966064),('p7_partition_one_game.json',0.7999822727070177)]:
 d=json.loads((ROOT/'replay'/name).read_text()); assert d['status']=='no_floating_separator_in_finite_policy_sample'; assert d['policy_cones']==1; assert len(d['records'])==3; assert d['best']['min_matching_ratio']==expected_best
print(json.dumps({'status':'PASS','reports':{k:{'policy_cones':v['cones'],'records':v['records'],'success':v['success'],'failed':v['failed'],'best':v['best']['min_matching_ratio']} for k,v in expected.items()},'one_game_replays':{'p6':'PASS','p7':'PASS'},'scope':'partition query finite reports and one-game replays; no universal SPE or integer-client claim'},ensure_ascii=False,indent=2))
