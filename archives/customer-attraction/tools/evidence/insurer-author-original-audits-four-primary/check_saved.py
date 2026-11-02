"""Structural/data selfcheck only. Does not import source programs or solve BI/LP."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import gzip, hashlib, json, re, sys
sys.dont_write_bytecode=True
from read_frozen_certificates import parse_certificate

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def check():
 manifest=read(HERE/'manifest.json');source_checks=[]
 for s in manifest['sources']:
  p=ROOT/s['preserved_as'];b=p.read_bytes()
  assert len(b)==s['size'] and sha_bytes(b)==s['sha256']
  blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  assert blob==s['blob']
  source_checks.append({'id':s['id'],'sha256':s['sha256'],'size':len(b),'git_blob_matches':True})
 d=read(HERE/'original/disjoint_insurer_audit.json')
 catalogue=[json.loads(line) for line in (HERE/'disjoint-input-catalogue.jsonl').read_text().splitlines()]
 assert len(catalogue)==len(d['records'])==d['cases']==340
 for i,(x,r) in enumerate(zip(catalogue,d['records'])):
  sets=list(map(frozenset,x['topics']));core=frozenset.intersection(*sets);union=frozenset().union(*sets)
  assert x['row_index']==i and x['m']==r['m']
  assert len(sets)==len(set(sets))==r['p']==r['root_cases']
  assert len(core)==r['core'] and len(union)==r['units'] and len(union)>0
  petals=[T-core for T in sets];maximal=[T for T in petals if not any(T<U for U in petals)]
  assert all(not(T&U) for j,T in enumerate(maximal) for U in maximal[j+1:])
  assert r['count_states']==comb(r['m']+r['p'],r['m'])-1
  assert F(0)<=F(r['max_scaled_customer_spread'])<=F(1)
  assert (r['minimum_three_slack'] is None)==(r['positive_spread_pairs']==0)
  if r['minimum_three_slack'] is not None:assert F(r['minimum_three_slack'])>=0
 assert sum(r['root_cases'] for r in d['records'])==d['root_cases']==1499
 assert sum(r['positive_spread_pairs'] for r in d['records'])==d['positive_spread_pairs']==323
 assert sum(r['count_states'] for r in d['records'])==d['count_states']==51403
 assert d['all_passed'] is True and sum(r['positive_spread_pairs']>0 for r in d['records'])==136
 summary=[]
 for m in range(2,7):
  rs=[r for r in d['records'] if r['m']==m]
  vals=[F(r['minimum_three_slack']) for r in rs if r['minimum_three_slack'] is not None]
  summary.append(dict(m=m,cases=len(rs),root_cases=sum(r['root_cases'] for r in rs),positive_spread_pairs=sum(r['positive_spread_pairs'] for r in rs),count_states=sum(r['count_states'] for r in rs),positive_pair_cases=sum(r['positive_spread_pairs']>0 for r in rs),max_scaled_customer_spread=str(max(F(r['max_scaled_customer_spread']) for r in rs)),minimum_three_slack=str(min(vals))))
 saved_summary=read(HERE/'report-summary.json');assert saved_summary['disjoint_summary']==summary
 padded=read(HERE/'original/padded_insurer_audit.json');assert saved_summary['padded_report']==padded
 cert_rows=read(HERE/'certificate-manifest.json')['certificates'];assert len(cert_rows)==4
 cert_checks=[]
 for row,r in zip(cert_rows,padded['cases']):
  raw=(ROOT/row['path']).read_bytes();assert len(raw)==row['compressed_size'] and sha_bytes(raw)==row['compressed_sha256']
  b=gzip.decompress(raw);assert len(b)==row['uncompressed_size'] and sha_bytes(b)==row['uncompressed_sha256']
  c=json.loads(b);m=c['m'];p=c['p'];assert m==r['m'] and p==r['topics']==2*m
  units=list(map(frozenset,c['unit_customer_interests']));assert len(units)==r['unit_customers']==3*m-1
  expected=[frozenset(range(m,p)) for _ in range(m)]
  for a,w in enumerate((2,m-1)+tuple(1 for _ in range(m-2))):expected.extend([frozenset((a,m+a)) for _ in range(w)])
  assert units==expected
  histories=set()
  for a in c['actions']:
   h=tuple(a['history']);assert h not in histories and len(h)<m and all(isinstance(v,int) and 0<=v<p for v in h)
   assert isinstance(a['action'],int) and 0<=a['action']<p
   histories.add(h)
  # Valid distinct histories plus exact cardinality cover the complete ordered tree.
  assert len(histories)==len(c['actions'])==r['ordered_decision_histories']==sum(p**j for j in range(m))
  assert r['comparisons']==p*len(histories) and r['minimum_slack']=='0'
  assert c['path']==[0]+[m+1]*(m-1)
  assert c['root_payoff']==r['root_payoff']=='2'
  assert c['root_deviations']==['2']+['1']*(m-1)+['2']*m
  assert c['W']==r['W']==2*m+1 and c['OPT']==r['OPT']==3*m-1
  assert r['old_root_defect']==r['s']=='1' and r['old_W']==r['old_OPT']==m
  assert r['insurer_W']==m+1 and r['insurer_OPT']==2*m-1 and r['insurer_half_dilution']==3
  assert c['OPT']-2*c['W']==-m-3
  cert_checks.append(dict(m=m,ordered_decision_histories=len(histories),all_histories_legal_unique_and_complete=True,unit_interests_match_source_input=True,compressed_and_raw_hashes_match=True))
 assert sum(r['comparisons'] for r in padded['cases'])==116068
 assert sum(r['ordered_decision_histories'] for r in padded['cases'])==11744
 frozen_manifest=read(HERE/'frozen-certificate-source-manifest.json')
 frozen_reading=read(HERE/'frozen-certificate-reading-data.json')
 assert frozen_manifest['primary_source_count']==len(frozen_manifest['sources'])==len(frozen_reading)==4
 assert frozen_manifest['primary_bytes']==1178612
 frozen_checks=[]
 for entry,reading in zip(frozen_manifest['sources'],frozen_reading):
  source=entry['source'];raw=gzip.decompress((ROOT/entry['preserved_via_existing_gzip']).read_bytes())
  assert len(raw)==source['size']==entry['existing_gzip_uncompressed_size']
  assert sha_bytes(raw)==source['sha256']==entry['existing_gzip_uncompressed_sha256']
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==source['blob']
  assert reading['source']['id']==source['id'] and reading['source']['sha256']==source['sha256']
  parsed=parse_certificate(raw)
  assert parsed==reading['raw_read_view']
  assert parsed['full_json_reconstructed_byte_identically'] is True
  assert len(parsed['classes'])==entry['unique_subtree_classes']
  assert parsed['action_records']==entry['ordered_action_records']
  assert parsed['metadata']['scope']==entry['source_json_scope']
  frozen_checks.append(dict(id=source['id'],sha256=source['sha256'],size=len(raw),git_blob_matches=True,unique_gzip_reused=True,all_fields_and_actions_losslessly_reconstructed=True,subtree_classes=len(parsed['classes'])))
 assert [r['subtree_classes'] for r in frozen_checks]==[3,6,10,13]
 assert manifest['all_primary_source_count']==8 and manifest['all_primary_bytes']==1270100
 event_checks=[]
 by_name={Path(s['path']).name:s for s in manifest['sources']}
 for mode in ('disjoint','padded'):
  ev=read(HERE/'runs'/mode/'event.json')
  assert ev['exit_code']==0 and ev['original_entry_calls']==1 and ev['source_function_extra_calls']==0 and ev['canonical_solver_calls']==0 and ev['discovery_or_LP_calls']==0
  assert ev['input_sha256']==by_name[ev['entry']]['sha256']
  assert ev['report_exact_bytes_equal_frozen'] and ev['frozen_report_sha256']==by_name[ev['report_name']]['sha256']
  assert (HERE/'runs'/mode/'stderr.txt').read_text()==''
  report_entry=next(r for r in ev['generated'] if r['path']==ev['report_name'])
  assert report_entry['sha256']==ev['frozen_report_sha256']
  if mode=='padded':
   for row in cert_rows:
    name=Path(row['path']).name.removesuffix('.gz');generated=next(r for r in ev['generated'] if r['path']==name)
    assert generated['size']==row['uncompressed_size'] and generated['sha256']==row['uncompressed_sha256']
  event_checks.append(dict(entry=ev['entry'],exit_code=0,original_entry_calls=1,frozen_report_exact_bytes=True))
 comparisons=read(HERE/'comparison-and-relationships.json')['comparison_reading']
 for row in comparisons:
  p=ROOT/row['preserved_as'];assert p.is_file() and sha_bytes(p.read_bytes())==row['sha256']
 payload=[]
 for row in manifest['payload']:
  p=ROOT/row['path'];assert p.is_file() and p.stat().st_size==row['size'] and sha_bytes(p.read_bytes())==row['sha256']
  payload.append(row['path'])
 known_targets={row.get('path') for row in comparisons if row.get('path')}
 missing=[];controls=[]
 for p in ROOT.rglob('*.md'):
  if 'comparison' in p.relative_to(ROOT).parts or 'context' in p.relative_to(ROOT).parts:continue
  b=p.read_bytes();bad=[x for x in b if x<32 and x not in (9,10,13)]
  if bad:controls.append(str(p.relative_to(ROOT)))
  text=b.decode()
  for link in re.findall(r'\]\(([^)]+)\)',text):
   if '://' in link or link.startswith('#'):continue
   dest=(p.parent/link.split('#')[0]).resolve()
   try:rel=str(dest.relative_to(ROOT))
   except ValueError:missing.append(dict(file=str(p.relative_to(ROOT)),link=link));continue
   if not dest.exists() and dest != HERE/'verification.json' and rel not in known_targets:missing.append(dict(file=str(p.relative_to(ROOT)),link=link))
 assert not missing and not controls
 return dict(all_pass=True,source_fingerprints=source_checks,frozen_certificate_source_fingerprints=frozen_checks,disjoint=dict(cases=340,root_cases=1499,positive_spread_pairs=323,count_states=51403,input_rows_bound_without_solver=340,per_m=summary),padded=dict(cases=4,ordered_decision_histories=11744,node_action_comparisons=116068,certificates=cert_checks),current_original_events=event_checks,comparison_snapshots_checked=len(comparisons),payload_files_checked=len(payload),missing_links=missing,control_character_files=controls,selfcheck_method='bytes, data arithmetic, input binding, and certificate structure only; source entry/function, BI, canonical solver, LP, discovery calls all 0')
if __name__=='__main__':
 result=check();(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('source_fingerprints','frozen_certificate_source_fingerprints','disjoint','padded')},ensure_ascii=False))
