"""Static saved-source/report checks only; no payoff, menu, IC, BI or LP calls."""
import ast
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODIES=[ROOT/'archives/customer-attraction/state/程序/双副本笛卡尔可信菜单的完整策略编译程序--程序.md',
 ROOT/'archives/customer-attraction/state/计算/四主题笛卡尔根门槛的凸化记录与双副本证书--计算.md']
IDS=['2a4c1bb0fcb32d9529b4','fc6467ce7399704e5efb','a974ce1883566859090a']

def read(p):return json.loads(p.read_text())

def fingerprint(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def same_content(p,item):
 f=fingerprint(p);assert (f['bytes'],f['sha256'])==(item['bytes'],item['sha256'])

def main():
 sources=read(HERE/'source-manifest.json')['sources'];assert len(sources)==7
 for s in sources:
  p=ROOT/s['preserved_path'];b=p.read_bytes()
  assert len(b)==s['size'] and hashlib.sha256(b).hexdigest()==s['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['blob']
 for p in HERE.rglob('*.py'):ast.parse(p.read_text())
 for p in HERE.rglob('*.json'):
  if p.name!='self-check.json':read(p)
 seed=read(HERE/'original/cartesian_convexification_k4.json');analysis=seed['analysis']
 packet=read(HERE/'original/cartesian_two_copy_exact.json')
 audit=read(HERE/'reported-data-audit.json')
 assert list(seed)==audit['source_top_fields'] and list(analysis)==audit['analysis_fields']
 assert list(packet)==audit['packet_fields'] and len(analysis)==len(packet)==18
 assert seed['sample']==186 and seed['drop']==8.5
 assert analysis['k']==4 and len(analysis['weights'])==15 and analysis['weights']==packet['base_weights']
 assert len(analysis['phi'])==len(analysis['root_minimizers'])==len(analysis['query'])==4
 assert len(analysis['actual_mix'])==len(analysis['opponent'])==3
 assert packet['base_clients']==72 and packet['copies']==2
 assert packet['phi']==['161/6','55/2','55/3','161/6']
 assert packet['base_root_minimum_guarantee']=='161/6' and packet['joint_root_minimum_guarantee']=='271/6'
 assert packet['root_floor_drop']=='17/2' and packet['actual_labels']==[11,14,15]
 assert packet['actual_components']==[[2,3],[3,2],[3,3]]
 assert packet['payoffs']==['146/3','146/3','110/3'] and packet['W']=='134'
 assert packet['ordered_histories']==273 and packet['all_comparisons']==4368 and packet['min_slack']=='0'
 assert len(packet['root_deviation_values'])==16
 assert packet['root_deviation_values'][11]=='146/3'
 assert all(str(Fraction(v))==v for v in packet['root_deviation_values']+packet['payoffs']+packet['phi'])
 game=packet['game'];assert list(game)==['players','topics','customers'] and game['players']==3
 assert game['topics']==[str(x) for x in product(range(4),repeat=2)]
 assert len(game['customers'])==144
 for customer in game['customers']:
  assert list(customer)==['topics','multiplicity'] and customer['multiplicity']==1
  assert customer['topics']==sorted(set(customer['topics'])) and all(0<=a<16 for a in customer['topics'])
 policy=packet['policy'];assert len(policy)==273
 assert all(list(r)==['history','action'] for r in policy)
 assert len({tuple(r['history']) for r in policy})==273
 assert [sum(len(r['history'])==d for r in policy) for d in range(3)]==[1,16,256]
 assert all(0<=r['action']<16 and all(0<=a<16 for a in r['history']) for r in policy)
 event=read(HERE/'replay/execution.json')
 assert event['returncode']==0 and event['assertions_enabled'] and event['removed_PYTHONOPTIMIZE']
 assert event['original_CLI_invocations']==1 and event['profile_or_trace'] is False
 assert event['inputs_before']==event['inputs_after'] and len(event['inputs_before'])==2
 assert all(event[k]==0 for k in ['functions_replaced','additional_original_calls','independent_SPE_audits','LP_calls'])
 for item in event['inputs_before']:same_content(HERE/'original'/Path(item['path']).name,item)
 same_content(HERE/'run_original_once.py',event['script_digest'])
 same_content(HERE/'original/cartesian_two_copy_exact.json',event['frozen_expected_report'])
 same_content(HERE/'replay/cartesian_two_copy_exact.json',event['generated_report'])
 assert event['generated_equal_frozen'] is True
 assert (HERE/'original/cartesian_two_copy_exact.json').read_bytes()==(HERE/'replay/cartesian_two_copy_exact.json').read_bytes()
 assert (HERE/'replay/stdout.txt').stat().st_size==event['stdout_bytes']==648
 assert (HERE/'replay/stderr.txt').read_bytes()==b'' and event['stderr_bytes']==0
 summary=read(HERE/'replay/stdout.txt')
 assert summary=={k:v for k,v in packet.items() if k not in ['game','policy','base_weights']}
 dataevent=read(HERE/'reported-data-execution.json')
 same_content(HERE/'audit_reported_data.py',dataevent['script']);same_content(HERE/'reported-data-audit.json',dataevent['report'])
 assert audit['status']=='PASS' and audit['new_data_arithmetic_entries']==1
 assert all(audit[k]==0 for k in ['original_entries','new_payoff_tables','LP_calls','new_IC_comparisons','BI_calls'])
 assert audit['rational_probability_recovery'] is False
 for item in audit['inputs']:
  p=HERE/'original'/Path(item['path']).name
  if not p.exists():p=ROOT/'archives/customer-attraction/tools/evidence/security-cartesian-and-disjoint-primary'/Path(item['path']).name
  same_content(p,item)
 comparison=audit['policy_data_comparison']
 assert comparison==dict(total_nodes=273,equal_actions=273,different_actions=0,differences=[],same_actual_path=True,same_actual_utilities=True,IC_recomputed=False)
 assert len(audit['root_mixture_literal_checks'])==4
 assert len(audit['static_literal_checks']['all10_background_values'])==10
 assert len(audit['static_literal_checks']['all4_query_values_against_opponent'])==4
 assert audit['actual_mixture_literal_check']['literal_second_surplus']=='-41/100000000000000000'
 review=read(HERE/'review-record.json')
 for item in review['bindings']:assert fingerprint(ROOT/item['path'])==item
 links=[]
 for p in BODIES+[HERE/'README.md']:
  s=p.read_text();assert not any(ord(c)<32 and c not in '\n\t' for c in s)
  assert s.endswith('\n') and not s.endswith('\n\n') and all(t.rstrip()==t for t in s.splitlines())
  for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',s):
   if '://' in link or link.startswith('#'):continue
   target=(p.parent/link.split('#',1)[0]).resolve()
   assert target.exists() or target==HERE/'self-check.json',(str(p),link)
   links.append(dict(source=str(p.relative_to(ROOT)),target=str(target.relative_to(ROOT))))
 for p in BODIES:
  front=p.read_text().split('---',2)[1]
  for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',front,re.M)
 receipts=[]
 for sid in IDS:
  p=ROOT/'cleanup/workspaces/Boss7/receipts-round20'/f'{sid}.json';d=read(p)
  assert d['id']==sid and d['disposition']=='integrated'
  assert all(d[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  assert all((ROOT/t).exists() or ROOT/t==HERE/'self-check.json' for t in d['targets'])
  receipts.append(fingerprint(p))
 result=dict(status='PASS',scope='Static files, stored fields and shapes only; no mathematical rerun',sources_verified=len(sources),
  primary_sources=3,comparison_bindings=len(review['bindings']),owned_fingerprints=[fingerprint(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='self-check.json'],
  bodies=[fingerprint(p) for p in BODIES],receipts=receipts,links_checked=len(links),links=links,
  original_entries=0,LP_calls=0,IC_comparisons=0,new_payoff_tables=0)
 (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 assert all((ROOT/t).exists() for sid in IDS for t in read(ROOT/'cleanup/workspaces/Boss7/receipts-round20'/f'{sid}.json')['targets'])
 print(json.dumps({k:v for k,v in result.items() if k not in ['owned_fingerprints','links']},ensure_ascii=False))

if __name__=='__main__':main()
