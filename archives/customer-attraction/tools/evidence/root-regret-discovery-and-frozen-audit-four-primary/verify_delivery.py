"""Verify frozen bytes, stored fields, domains and reversible views; no math replay."""
from pathlib import Path
import json,hashlib,itertools,re
from fractions import Fraction as F
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-root-regret-discovery-and-frozen-audit-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==4 and sum(x['size'] for x in rows)==20413
for x in rows:
 checked(S/x['stage_path'],x);o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256'];assert x['full_file_reviewed']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==12 and {r['id'] for r in rows}<=set(claim['ids']);assert claim['remote_tip']=='3d6d8f7832584460e2654c53ca6ca6d7bc446e04' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==1 and p['tracked']==[] and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='1e02ed40671d211709351e725373e4c3185803e3'
seedmanifest=read(E/'actual-related-seed-manifest.json');seeds=seedmanifest['rows'];assert len(seeds)==12 and sum(x['size'] for x in seeds)==175295 and seedmanifest['new_primary_count']==seedmanifest['new_done_count']==0
view=read(E/'seeds-reversible-reading.json')['sources'];assert len(view)==12;vmap={v['id']:v for v in view};raws={};actions_count=0
for x in seeds:
 checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and x['new_primary'] is False and x['new_done'] is False
 v=vmap[x['id']];raw=read(S/x['snapshot']);assert len(raw)==11 and raw['all_ordered_positive_depth_IC_verified_exactly'] is True and raw['kind']=='full root-only source plan; root may be suboptimal'
 z=dict(v['other_fields']);p=len(z['instance']['topics']);m=z['instance']['players'];assert p==m+2 and m in (3,4,5);ad={}
 for d,s in enumerate(v['actions_depth_lex_strings']):
  assert len(s)==p**d and all(str(i) in '0123456' for i in range(p));hs=list(itertools.product(range(p),repeat=d))
  for h,a in zip(hs,s):assert a.isdigit() and int(a)<p;ad[h]=int(a)
 assert len(ad)==sum(p**d for d in range(m));z['actions']=[[list(h),a] for h,a in sorted(ad.items())];assert z==raw;actions_count+=len(ad);assert raw['positive_depth_decision_histories']==len(ad)-1
 inst=raw['instance'];assert len(inst)==3 and all(type(c['multiplicity']) is int and c['multiplicity']>0 and c['topics'] and all(type(a) is int and a in range(p) for a in c['topics']) for c in inst['customers']);assert len(raw['actual'])==m and len(raw['root_deviation_payoffs'])==p;raws[v['file']]=raw
 cap=read(E/'related-normal-show-captures'/Path(x['actual_normal_show_capture']).name)
 if x['id']=='11b20b3cd0f9f814da06':assert cap['exit_code']==0 and cap['capture_mode'].startswith('already-observed') and cap['observed_normal_show']['source']['sha256']==x['sha256']
 else:assert cap['exit_code']==0 and json.loads(cap['stdout'])['source']['sha256']==x['sha256']
assert actions_count==12364
for name,num in [('runtime-dependency-manifest.json',4),('related-MD-manifest.json',2)]:
 rs=read(E/name);assert len(rs)==num
 for x in rs:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
assert sum(x['size'] for x in read(E/'related-MD-manifest.json'))==8874
D=read(S/rows[1]['stage_path']);A=read(S/rows[3]['stage_path']);assert list(D)==['purpose','seed','status','samples'] and D['seed']==791883 and len(D['samples'])==6;assert list(A)==['contract','scope','sources'] and len(A['sources'])==12
formal=S/'archives/customer-attraction/state/程序/常数三根缺陷原发现与十二完整计划的独立回放--程序.md';text=formal.read_text();cones=[];loopcount=0
for g in D['samples']:
 assert list(g)==['sample','players','topics','source_cones'] and len(g['source_cones'])==2;loopcount+=len(g['source_cones'])*len(list(itertools.combinations(range(g['topics']),g['players'])))
 for z in g['source_cones']:
  assert list(z)==['prescribed','source_terminal','exact_seed_source','numerical_max_repair_margin_per_W'];assert type(z['numerical_max_repair_margin_per_W']) is float;raw=raws[z['exact_seed_source']];p=g['topics'];assert z['prescribed']==raw['actual'][0] and z['source_terminal']==[raw['actual'].count(a) for a in range(p)]
  line='|'+g['sample']+'|'+str(g['players'])+','+str(g['topics'])+'|'+str(z['prescribed'])+'|`'+json.dumps(z['source_terminal'],separators=(',',':'))+'`|'+z['exact_seed_source']+'|`'+repr(z['numerical_max_repair_margin_per_W'])+'`|';assert line in text;cones.append(z)
assert len(cones)==12 and loopcount==184 and {z['exact_seed_source'] for z in cones}==set(raws)
for z in A['sources']:
 keys=['file','players','topics','ordered_histories','positive_depth_IC_rows','W','OPT_m','root_regret','exact_source_repair_margin'];assert list(z)==keys;raw=raws[z['file']];m=z['players'];p=z['topics'];assert z['ordered_histories']==sum(p**d for d in range(m)) and z['positive_depth_IC_rows']==(z['ordered_histories']-1)*p
 assert z['W']==raw['W'] and z['OPT_m']==raw['OPT_m'] and z['root_regret']==raw['root_regret'];assert F(z['exact_source_repair_margin'])==F(z['OPT_m']-2*z['W'])-3*F(z['root_regret']) # stored fields, not payoff/coverage computation
 assert '|'+'|'.join(str(z[k]) for k in keys)+'|' in text
assert sum(z['ordered_histories'] for z in A['sources'])==12364 and sum(z['positive_depth_IC_rows'] for z in A['sources'])==85192 and sum(z['topics'] for z in A['sources'])==72
cm=read(E/'formal-comparison.json');assert len(cm)==6
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==4 and {r['id'] for r in receipts}=={r['id'] for r in rows}
for x in receipts:
 assert x['disposition']=='retained' and all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all((S/p).is_file() for p in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
comparison_targets={x['path']:S/x['snapshot'] for x in cm}
for p in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in comparison_targets)),(p,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
allfiles=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());assert read(W/'copy-files.json')==allfiles
result=dict(status='pass',scope='frozen bytes/provenance/complete stored fields and tables/reversible seed data/domains only',primary_count=4,primary_bytes=20413,related_seeds=12,related_seed_bytes=175295,seed_action_tables_roundtrip=True,seed_actions=12364,seed_positive_depth_actions=12352,reported_positive_depth_self_included_IC=85192,root_payoff_stored_fields=72,inferred_original_LP_loop_count=184,original_discovery_runs=0,original_audit_runs=0,solver_runs=0,LP_runs=0,IC_replays=0,root_payoff_replays=0,OPT_replays=0,receipts_retained=4,relations=8)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
