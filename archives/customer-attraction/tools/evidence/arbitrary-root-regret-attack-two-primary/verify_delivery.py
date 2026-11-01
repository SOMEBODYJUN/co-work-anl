"""Byte/provenance and lossless stored-field checks only; never import attack/LP."""
from pathlib import Path
import json,hashlib,itertools,re
from fractions import Fraction
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-arbitrary-root-regret-attack-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
manifest=read(E/'actual-source-manifest.json');rows=manifest['rows'];assert len(rows)==2 and sum(x['size'] for x in rows)==492924
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'];owner=read(E/'local-progress-at-read'/(x['id']+'.json'));assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==6;assert claim['remote_tip']=='e3076230395d39af8467f8d7b65ef0dcb847c452';assert {x['id'] for x in rows}<=set(claim['ids']);assert claim['local_sync']['status']=='needs-attention'
proof=read(E/'claim-sync-preservation.json');assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and proof['missing']==proof['different']==[] and not proof['unmerged'] and proof['stash_kept'];assert proof['stash']=='48503c90846a171e6c88dd68999096249a5284ac'
inputs=read(E/'runtime-input-manifest.json');deps=read(E/'runtime-dependency-manifest.json');md=read(E/'related-MD-manifest.json');assert len(inputs)==8 and sum(x['size'] for x in inputs)==45059 and len(deps)==5 and len(md)==2 and sum(x['size'] for x in md)==6331
for x in inputs+deps+md:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
report=read(S/rows[1]['stage_path']);sparse=read(E/'report-sparse-reading.json');view=read(E/'report-interned-reading.json');pool=view['dictionary'];cols=view['record_columns'];assert len(pool)==465
assert {k:v for k,v in sparse.items() if k not in ('results','value_encoding')}=={k:v for k,v in report.items() if k!='results'}
recovered={k:v for k,v in sparse.items() if k not in ('results','value_encoding')};recovered['results']=[]
for g,ig,raw in zip(sparse['results'],view['groups'],report['results']):
 assert {k:v for k,v in ig.items() if k!='records'}=={k:v for k,v in g.items() if k!='records'}
 decoded=[{k:pool[str(i)] for k,i in zip(cols,z)} for z in ig['records']];assert decoded==g['records']
 rs=[]
 for r in decoded:
  z={k:v for k,v in r.items() if k not in ('values_length','nonzero_mask_values')};a=['0']*r['values_length'];seen=set()
  for i,v in r['nonzero_mask_values']:assert 1<=i<=len(a) and i not in seen and v!='0';seen.add(i);a[i-1]=v
  z['values']=a;rs.append(z)
 q={k:v for k,v in g.items() if k not in ('records','best_record_index')};q['records']=rs;q['best']=rs[g['best_record_index']];assert q==raw;recovered['results'].append(q)
assert recovered==report
assert [len(g['records']) for g in report['results']]==[90,16,120,4]
assert [g['records'].index(g['best']) for g in report['results']]==[0,3,15,2]
assert [g['best']['value'] for g in report['results']]==['7/4','2','149/103','5/4']
formal=S/'archives/customer-attraction/state/程序/任意指定根四后续策略锥的原攻击与全部有理记录--程序.md';text=formal.read_text();action_total=0
for g in report['results']:
 p,m=g['topics'],g['players'];ports=list(itertools.combinations(range(p),min(p,m)));domain=[(a,port) for a in range(p) for port in ports];assert [(r['actual_root'],tuple(r['support'])) for r in g['records']]==domain
 for r in g['records']:
  assert list(r)==['status','certified','values','value','dual_bound','dual_optimal','dual_support','support','actual_root'];assert r['status']=='exact_primal' and r['certified'] is True and r['dual_optimal'] is True and r['value']==r['dual_bound'];assert len(r['values'])==(1<<p)-1 and all(isinstance(x,str) for x in r['values'])
  ds=r['dual_support'];assert all(type(i) is int and i>=0 and isinstance(mu,str) for i,mu in ds) and [i for i,mu in ds]==sorted(set(i for i,mu in ds))
 assert g['best']==max(g['records'],key=lambda r:Fraction(r['value'])) # stored literal comparison, no LP
 lookup={(r['actual_root'],tuple(r['support'])):r['value'] for r in g['records']}
 for port in ports:assert '|`'+json.dumps(port,separators=(',',':'))+'`|'+'|'.join(lookup[a,port] for a in range(p))+'|' in text
 model=read(E/'original/examples/customer_attraction'/(g['source']+'.json'));cert=read(E/'original/evidence/certificates/customer_attraction'/(g['source']+'.json'));cert=cert.get('strategy',cert);acts=cert['actions'];a={tuple(x['history']):x['action'] for x in acts};assert len(a)==len(acts)==sum(p**d for d in range(m));assert set(a)=={h for d in range(m) for h in itertools.product(range(p),repeat=d)} and all(type(v) is int and 0<=v<p for v in a.values());action_total+=len(a);assert len(model['topics'])==p and model['players']==m
assert action_total==408
for x in read(E/'formal-comparison.json'):assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==2 and {x['id'] for x in receipts}=={x['id'] for x in rows}
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and x['disposition']=='retained';assert all((S/p).is_file() for p in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
for p in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and (R/q.relative_to(S)).is_file()),(p,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
all_files=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file());assert read(W/'copy-files.json')==all_files
result=dict(status='pass',scope='bytes/provenance/all stored fields/lossless views/domains/formal tables and links only',primary_count=2,primary_bytes=492924,report_records=230,all_original_report_fields_roundtrip=True,all_four_best_copies_roundtrip=True,input_files=8,input_bytes=45059,input_actions=408,dependency_modules=5,related_MD_count=2,related_MD_bytes=6331,formal_comparison_count=7,receipts_retained=2,relations=8,original_program_runs=0,LP_runs=0,IC_replays=0,primal_dual_residual_replays=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
