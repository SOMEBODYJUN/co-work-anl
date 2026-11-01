"""Structural delivery check only; never reruns mathematical selfchecks."""
from pathlib import Path
import json,hashlib,re,sys

ST=Path(__file__).resolve().parents[3]
REPO=ST.parents[1]/'boss4-research'
E=ST/'tools/evidence/static-debt-and-target-union-primary'
WS=ST/'cleanup/workspaces/Boss4/r3-static-debt-and-target-union-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cap=json.loads((E/'actual-claim.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
sources=json.loads((E/'source-manifest.json').read_text())
assert len(sources)==5 and set(cap['ids'])=={r['id'] for r in sources}
owners=json.loads((E/'owner-snapshot.json').read_text())
assert len(owners)==5 and all(r['owner']=='Boss4' and r['disposition']=='in-progress' for r in owners)
for r in sources:
 p=ST/r['local_path'];b=p.read_bytes()
 assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 assert r['actual_full_read'] and len(b.splitlines())==r['actual_full_read_lines']
for r in json.loads((E/'comparison-inputs.json').read_text()):
 p=ST/r['local_path'];assert sha(p)==r['sha256'] and r['full_read'] and not r['primary']
for r in json.loads((E/'formal-comparison-manifest.json').read_text()):
 assert sha(ST/r['snapshot'])==r['sha256'] and r['actual_full_read']
receipts=json.loads((WS/'semantic-receipts.json').read_text())
assert {r['id'] for r in receipts}==set(cap['ids']) and len(receipts)==5
layout=json.loads((E/'formal-layout.json').read_text());assert len(layout)==6
stable=[];links=[]
for row in layout:
 p=ST/row['path'];s=p.read_text();assert s.startswith('---\n') and '\n---\n' in s[4:]
 front=s.split('\n---\n',1)[0]
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:
  assert re.search(r'^'+key+r':',front,re.M),(p,key)
 assert row['stable_id'] in front
 stable.append(row['stable_id'])
 assert not (REPO/row['path']).exists(),('overwrite forbidden',row['path'])
 for raw in re.findall(r'\]\(([^)]+)\)',s):
  if ':' in raw or raw.startswith('#'):continue
  target=(p.parent/raw.split('#',1)[0]).resolve()
  if not target.exists():
   rel=target.relative_to(ST);assert (REPO/rel).exists(),(p,raw)
  links.append(raw)
assert len(stable)==len(set(stable))
for p in (REPO/'archives').rglob('*.md'):
 text=p.read_text(errors='replace')
 for ident in stable:
  assert not re.search(r'^id: ["\']?'+re.escape(ident)+r'["\']?\s*$',text,re.M),('existing duplicate id',ident,p)
for r in receipts:
 assert r['full_file_reviewed'] and r['related_material_checked'] and r['unique_content_accounted_for']
 assert r['disposition']=='integrated' and r['targets'] and all((ST/q).exists() for q in r['targets'])
run=json.loads((E/'run-definition-check/report.json').read_text())
assert run['status']=='PASS' and len(run['debt_checks'])==64
assert len(run['prefix_LP_checks'])==99 and len(run['incidence_A_checks'])==36
assert run['stationary_flow']['weighted']=='-1/18'
assert json.loads((E/'run-definition-check-attempt1/attempt.json').read_text())['exit_code']==1
assert (E/'run-definition-check-attempt1/stderr.txt').read_text().endswith('AssertionError\n')
assert len(json.loads((E/'source-corrections.json').read_text())['corrections'])==2
assert (E/'run-definition-check/stderr.txt').read_text()==''
assert len(json.loads((E/'relation-evidence.json').read_text()))==16
for p in ST.rglob('*.json'):json.loads(p.read_text())
result={'status':'PASS','scope':'structural only; no mathematical program rerun','primary':5,
 'primary_bytes':sum(r['size'] for r in sources),'primary_lines':sum(r['actual_full_read_lines'] for r in sources),
 'formal_pages':6,'formal_lines':sum(len((ST/r['path']).read_text().splitlines()) for r in layout),
 'receipts':5,'relations':16,'local_links_checked':len(links),'original_program_entries':0,
 'new_definition_check_attempts':2,'R18_primary':0,'DN_new_done':0}
if '--final' in sys.argv:
 m=json.loads((WS/'copy-files.json').read_text());actual={str(p.relative_to(ST)) for p in ST.rglob('*') if p.is_file()}
 assert set(m['copy_paths'])==actual and len(m['copy_paths'])==len(actual)
 assert m['ready'] and m['primary_ids']==cap['ids']
 for r in m['files']:
  p=ST/r['path'];assert len(p.read_bytes())==r['bytes'] and sha(p)==r['sha256']
 assert {r['path'] for r in m['files']}==actual-{'cleanup/workspaces/Boss4/r3-static-debt-and-target-union-primary/copy-files.json'}
 result['copy_files']=len(actual)
else:
 (E/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
