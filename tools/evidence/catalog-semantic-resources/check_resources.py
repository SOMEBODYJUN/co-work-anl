"""New finite artifact integrity audit, separate from semantic reading and mathematical truth."""
from pathlib import Path
import ast,collections,hashlib,json,re,sys
E=Path(__file__).resolve().parent;B=E.parents[2];repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def check(name,ok,details=None):
 checks.append({'check':name,'pass':bool(ok),'details':details});
 if not ok:raise AssertionError(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cell(s):return str(s).replace('|',r'\|').replace('\n','<br>')
x=json.loads((E/'original/research/catalog.json').read_text());records=json.loads((E/'catalog-semantic-records.json').read_text());ps=json.loads((E/'purpose-dictionary.json').read_text());pm={p['id']:p['text'] for p in ps};progress=json.loads((E/'reading-progress.json').read_text());dest=json.loads((E/'topic-destinations.json').read_text());src=json.loads((E/'source-manifest.json').read_text());binding=json.loads((E/'full-md-binding.json').read_text());a=json.loads((E/'related/research/assets.json').read_text());claims={}
for z in a['entries']:
 for k in ['proof','tests','records','examples','reviews','candidates','sources','implementation']:
  for path in z.get(k,[]):claims.setdefault(path,set()).update(z['claims'])
check('all semantic source records exact roundtrip',[r['source_record'] for r in records]==x['entries'])
check('all2099 indices unique ordered',[r['original_index'] for r in records]==list(range(2099)))
check('actual reading acknowledgment covers all2099',progress['catalog_complete_indices']==list(range(2099)))
check('wholeMD byte binding already completed',binding['all1596733bytes_equal'] and binding['actual_sha256']==sha(E/'original/research/CATALOG.md'))
for s in src:check('exact frozen source '+s['id'],sha(B/s['saved_path'])==s['sha256'] and (B/s['saved_path']).stat().st_size==s['size'])
pi={r['path']:i for i,r in enumerate(x['entries'])}
for z in records:
 i=z['original_index'];r=z['source_record'];page=(B/z['target']).read_text();cs=sorted(claims.get(r['path'],[]));row='| '+str(i)+' | '+cell(r['title'])+' | `'+cell(r['path'])+'` | `'+r['role']+'` | '+cell(r.get('package','∅'))+' | '+z['purpose_id']+' |'
 check('record '+str(i)+' complete semantic preservation',pm[z['purpose_id']]==r['purpose'] and row in page and '| '+z['purpose_id']+' | '+cell(r['purpose'])+' |' in page and z['md_display_claims']==cs[:3] and z['md_claim_total']==len(cs) and z['related_paths_indices']==[pi[p] for p in r.get('related_paths',[])] and z['related_indices']==[pi[p] for p in r.get('related',[])])
for d in dest:
 rr=[r for r in records if r['source_record']['topic']==d['topic']];check('topic '+d['topic']+' all record rows',len(rr)==d['count'] and all(r['target']==d['target'] for r in rr))
check('both relations and absence preserved',sum('related' in r['source_record'] for r in records)==14 and sum('related_paths' in r['source_record'] for r in records)==1148)
check('all14 related have no related_paths overlap',all('related_paths' not in r['source_record'] for r in records if 'related' in r['source_record']))
check('all unique purposes exact dictionary',len(ps)==1484 and set(pm.values())=={r['purpose'] for r in x['entries']})
check('all visible Claim identities exact',len({c for r in records for c in r['md_display_claims']})==479)
main=B/'archives/customer-attraction/state/资源/旧研究总目录的字段语义与版本边界--资源.md';mt=main.read_text();check('all35 rename pairs self contained',all('| `'+k+'` | `'+v+'` |' in mt for k,v in x['renamed_paths'].items()))
ids=[];links=0;pages=sorted((B/'archives/customer-attraction/state/资源').glob('*.md'))
for p in pages:
 t=p.read_text();check('frontmatter '+p.name,all(re.search(r'^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ids.append(re.search(r'^id: (.*)$',t,re.M)[1])
 check('no forbidden C0 controls '+p.name,all(ord(c)>=32 or c in chr(9)+chr(10) for c in t))
 check('no whitespace-only trailing lines '+p.name,not any(l and l.isspace() or l.rstrip()!=l for l in t.splitlines()))
 for href in re.findall(r'\]\(([^\n)]+)\)',t):
  if href.startswith(('http:','https:','#','source:')):continue
  q=(p.parent/href.split('#')[0]).resolve();rel=q.relative_to(B);check('local link '+p.name+' -> '+href,q.exists() or (repo/rel).exists());links+=1
check('13 resource IDs unique',len(ids)==13 and len(set(ids))==13)
for p in E.glob('*.py'):check('new helper syntax '+p.name,ast.parse(p.read_text()) is not None)
report={'scope':'New bounded resource completeness/representation check, not original suites or proof certification','passed':len(checks),'failed':0,'records':2099,'topics':12,'pages':13,'links_checked':links,'checks':checks}
(E/'self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
