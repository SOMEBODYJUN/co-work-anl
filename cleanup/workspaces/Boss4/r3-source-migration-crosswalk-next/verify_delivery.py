#!/usr/bin/env python3
"""New delivery integrity checks only, no Git or historical program execution."""
from pathlib import Path
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];E=S/'tools/evidence/source-migration-crosswalk';W=Path(__file__).resolve().parent;R=S.parent.parent/'boss4-research';PRIOR=S.parent/'r3-research-index-builders'
checks=[]
def ck(name,v,detail=None):
 checks.append({'check':name,'pass':bool(v),'detail':detail})
 if not v:raise AssertionError(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['source-manifest.json','comparison-manifest.json']:
 for r in json.loads((E/name).read_text()):
  p=S/r['saved_path'];ck(name+':'+r['path'],p.is_file() and p.stat().st_size==r.get('size',r.get('bytes')) and sha(p)==r['sha256'])
source=json.loads((E/'source-manifest.json').read_text());ck('four exact IDs',{r['id'] for r in source}=={'48efc2103c109f9bffd3','014668282ad7a97a0116','5f719b81313dfcf26cb5','60a01a03bbce857246d8'});ck('source984125bytes',sum(r['size'] for r in source)==984125)
for p in [*E.rglob('*.py'),Path(__file__)]:ast.parse(p.read_text());ck('AST parse only '+str(p.relative_to(S)),True)
for p in E.rglob('*.json'):json.loads(p.read_text())
ck('all evidence JSON parses',True)
c=json.loads((E/'original/research/source_crosswalk.json').read_text());m=json.loads((E/'original/research/path_migration.json').read_text());b=json.loads((E/'original/research/branch_cleanup.json').read_text());n=json.loads((E/'normalized-records.json').read_text());a=json.loads((E/'ledger-structural-audit.json').read_text());ac=a['source_crosswalk'];failed=json.loads((E/'cancelled-byte-binding-attempt.json').read_text())
ck('all457647MDbytes independently equal',ac['all_md_bytes_equal_new_independent_reconstruction'] and ac['actual_md_bytes']==457647 and ac['actual_md_sha256']==ac['expected_md_sha256'])
ck('680 records187 exact note groups',len(n['records'])==680 and len(n['notes'])==187)
for group in ['entries','new_sources','historical_records']:
 rrs=[r for r in n['records'] if r['group']==group];ck('all original record values preserved '+group,len(rrs)==len(c[group]) and all(all(r[k]==v for k,v in orig.items()) for r,orig in zip(rrs,c[group])))
ck('all normalized note links exact',all(next(g['text'] for g in n['notes'] if g['id']==r['historical_note_id'])==r['interpretation'] for r in n['records']))
ck('mapping5 exact counts',a['migration']['mapping_counts']=={'moved':58,'retired_code_paths':10,'first_curation_retired':8,'retired_test_entrypoints':7,'reestablished_root_docs':3})
ck('79origins67targets/testexactsubset',a['migration']['distinct_original_paths']==79 and a['migration']['distinct_targets']==67 and a['migration']['retired_test_is_exact_moved_subset'])
ck('530 provenance hashes only metadata',a['provenance_hash_metadata']['with_explicit_hash']==530 and not a['provenance_hash_metadata']['explicit_without_match'])
ck('141archives metadata only and42omitted',a['branch_cleanup']['archived_routes']==141 and not a['branch_cleanup']['archived_metadata_mismatches'] and len(b['omitted_current_tree_items'])==42)
ck('six branch complete file arrays preserved',len(b['branches'])==6)
ck('no frozen crosswalk reference missing',not ac['missing_frozen_refs'])
ck('cancelled byte attempt no results claimed',failed['reported_results'] is None and 'exit130' in failed['observed_end'])
rec=json.loads((W/'semantic-receipts.json').read_text());ck('four complete receipts',len(rec)==4 and {r['id'] for r in rec}=={r['id'] for r in source} and all(all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(r[k] for k in ['read_note','comparison_note','decision_note','disposition','targets']) for r in rec))
formal={p for r in rec for p in r['targets']}
for target in sorted(formal):
 p=S/target;t=p.read_text();h=t.split('---',2)[1]
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:ck('frontmatter '+p.name+':'+k,re.search('^'+k+':',h,re.M) is not None)
 ck('two commits '+p.name,all(c in h for c in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']))
 ck('no trailing whitespace derived '+p.name,all(line==line.rstrip() for line in t.splitlines()))
 ck('no BEL/CR derived '+p.name,'\a' not in t and '\r' not in t)
 clean=re.sub(r'(?s)```.*?```','',t);clean=re.sub(r'`[^`]*`','',clean)
 anchors=set(re.findall(r'<a id="([^"]+)"',t))
 for href in re.findall(r'\]\(([^)]+)\)',clean):
  if href.startswith('#'):ck('internal anchor '+p.name+':'+href,href[1:] in anchors);continue
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href):continue
  dest=(p.parent/href.split('#',1)[0]).resolve();rel=dest.relative_to(S.resolve());ck('local link '+p.name+':'+href,dest.exists() or (R/rel).exists() or (PRIOR/rel).exists())
p=S/'archives/customer-attraction/state/资源/来源解释账本的历史语义与当前校正--资源.md';t=p.read_text()
ck('all680 formal row identifiers exactly once',all(len(re.findall(r'^\| '+r['record_id']+r' \|',t,re.M))==1 for r in n['records']))
ck('all187 full historical note texts retained',all(g['text'] in t for g in n['notes']))
ck('currentN031 corrected while original intact','N031的弱iid桥' in t and c['new_sources'][30]['interpretation'] in t and '(39/40)Z_{20}>40=W' in t)
p=S/'archives/customer-attraction/state/资源/退役分支的逐项来源保全与恢复边界--资源.md';t=p.read_text();ck('all6 original files arrays exact fenced values',all('\n'.join(r['files']) in t for r in b['branches']));ck('all141 archive expected hashes and paths retained',all(r['sha256'] in t and r['archived_path'] in t and r['original_path'] in t for r in b['archived_sources']));ck('all42 omitted branch/path retained',all(r['branch'] in t and r['path'] in t for r in b['omitted_current_tree_items']))
out={'scope':'new integrity and bounded semantic representation checks only; no historicalsuite, Git lookup,141bytePASS, referencedmath/remote/secret/visual certification','passed':len(checks),'checks':checks,'formal_pages':len(formal),'formal_bytes':sum((S/p).stat().st_size for p in formal),'receipts':4,'source_bytes':984125}
(W/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
