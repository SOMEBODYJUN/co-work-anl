#!/usr/bin/env python3
"""New static dependency audit; no old-module import or execution."""
from pathlib import Path
import ast,collections,hashlib,json,os,posixpath,re
B=Path(__file__).resolve().parent
STAGE=B.parents[2]
related=json.loads((B/'related-manifest.json').read_text())
def bypath(path):
 r=next(r for r in related if r['path']==path)
 return STAGE/r['saved_path']
rows=[json.loads(s) for s in (B/'frozen-inventory.jsonl').read_text().splitlines()]
commits=['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']
indices={c:{r['path']:r for r in rows if any(s['commit']==c for s in r['sources'])} for c in commits}
def load(p):return json.loads(p.read_text())
def literal_values(p,names):
 out={}
 for node in ast.parse(p.read_text()).body:
  if isinstance(node,ast.Assign):
   for target in node.targets:
    if isinstance(target,ast.Name) and target.id in names:out[target.id]=ast.literal_eval(node.value)
 return out
catalog=load(bypath('research/catalog.json'));assets=load(bypath('research/assets.json'));integration=load(bypath('research/weighted_congestion_frontier/INTEGRATION.json'));active=load(B/'original/research/active_research.json')
const=literal_values(B/'original/research/build_catalog.py',{'TOPICS','ROLES','PACKAGE_TITLES'})
topics=const['TOPICS'];roles=const['ROLES'];pt=const['PACKAGE_TITLES']
claims={}
for a in assets['entries']:
 for role in ['proof','tests','records','examples','reviews','candidates','sources','implementation']:
  for p in a.get(role,[]):claims.setdefault(p,set()).update(a['claims'])
names={r['path']:r['title'] for r in catalog['entries']}
def cell(v):return v.replace('|',r'\|').replace('\n',' ')
def rows_render(rs,base):
 out=['| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |','| --- | --- | --- | --- |']
 for r in rs:
  p=r['path'];link=posixpath.relpath(p,base);ids=sorted(claims.get(p,[]));state=roles[r['role']]
  if ids:
   vis='、'.join('`'+c+'`' for c in ids[:3]);suffix=f'（共 {len(ids)} 项）' if len(ids)>3 else '';state+=f'；关联 {vis}，[命题合同{suffix}]({posixpath.relpath("research/assets.json",base)})'
  elif r['role'] in {'account','obstruction','counterexample'}:state+='；精确范围见本页正文'
  label=cell(r['title']).replace('[',r'\[').replace(']',r'\]');purpose=cell(r['purpose'])
  for other in r.get('related_paths',[]):
   otherlabel=cell(names[other]).replace('[',r'\[').replace(']',r'\]');purpose+=f'；配套 [{otherlabel}](<{posixpath.relpath(other,base)}>)'
  out.append(f'| [{label}](<{link}>) | `{p}` | {purpose} | {state} |')
 return out
def topic_rows(topic,base):
 rs=[r for r in catalog['entries'] if r['topic']==topic];packages=list(dict.fromkeys(r.get('package','') for r in rs))
 if topic=='weighted_congestion':packages.sort(key=lambda p:list(pt).index(p) if p in pt else len(pt))
 out=[]
 for package in packages:
  selected=[r for r in rs if r.get('package','')==package]
  if topic=='weighted_congestion':
   order=['navigation','definition','ledger','account','algorithm','reduction','representation','certificate_account','counterexample','obstruction','candidate','question','literature','review','audit_code','frozen_evidence','source_guide','source'];selected.sort(key=lambda r:order.index(r['role']))
  if package:out += ['### '+pt.get(package,package),'']
  out+=rows_render(selected,base)+['']
 return '\n'.join(out)
def data_rows(text):return [l for l in text.splitlines() if l.startswith('| [')]
actuals={p.name:p for p in B.rglob('*.md') if p.name in ['CATALOG.md','FILES.md']}
expected_catalog=[]
for k,_,_ in topics:
 if any(r['topic']==k for r in catalog['entries']):expected_catalog+=data_rows(topic_rows(k,'research'))
actual_catalog=data_rows(actuals['CATALOG.md'].read_text())
expected_wc=data_rows(topic_rows('weighted_congestion','research/weighted_congestion_frontier'));actual_wc=data_rows(actuals['FILES.md'].read_text())
canonical_bad=[r['path'] for r in catalog['entries'] if Path(r['path']).is_absolute() or any(p in {'','.','..'} for p in r['path'].split('/')) or '\\' in r['path'] or any(c in r['path'] for c in '\n\r<>')]
names_bad=[r['path'] for r in catalog['entries'] if not re.search(r'[\u3400-\u9fff]',r['title']) or r['title']==posixpath.basename(r['path']) or len(r['purpose'].strip())<12 or r['purpose'].endswith('接口或来源复验时')]
required_by_commit={}
for c,idx in indices.items():
 req={p for p in idx if p.endswith('.md') and (p.startswith(('research/current/','research/questions/','research/reviews/','research/customer_attraction/')) or p.startswith('research/weighted_congestion_frontier/') and 'upstream' not in p.split('/')[2:])}
 req.update(p for p in idx if p.startswith('research/') and '/' not in p[len('research/'):] and p.endswith('.md') and posixpath.basename(p) not in {'CATALOG.md','source_crosswalk.md'})
 req.update(v['path'] for v in integration['classification'].values() if 'path' in v)
 required_by_commit[c]={'required':len(req),'missing_catalog':sorted(req-set(names)),'catalog_absent_frozen_paths':sorted(set(names)-set(idx)),'renamed_old_still_present':[p for p in catalog['renamed_paths'] if p in idx]}
wc=[]
for old,item in integration['classification'].items():
 v={'old':old,'role':item.get('role'),'path':item.get('path'),'disposition':item.get('disposition')}
 if 'path' in item:
  p=item['path'];v['frozen_hash_matches_some_recorded_source']={c:bool(indices[c].get(p)) and indices[c][p]['sha256'] in {q['sha256'] for q in integration['source_files'][old]} for c in commits} if p.endswith(('.py','.json')) else 'old checker does not hash this suffix'
 else:v['explicit_retirement']=item.get('disposition')=='git_history_only' and bool(item.get('reason'))
 wc.append(v)
source_constants=[]
for p in B.rglob('*.py'):
 if p.name=='work.py':source_constants.append({'id':p.relative_to(B).parts[1],'path':'work.py','values':literal_values(p,{'DEFAULT_SAVE','RESEARCH_ENTRIES','ROLE_PROMPTS'})})
 elif p.name=='checkpoint.py':source_constants.append({'id':p.relative_to(B).parts[1],'path':'checkpoint.py','values':literal_values(p,{'DEFAULT_SAVE'})})
active_inputs=[]
for r in related:
 if r['path'] in active['active_entrypoints']+active['role_prompts']+[active['runbook'],active['mathematical_entry']]:
  p=STAGE/r['saved_path'];text=p.read_text();active_inputs.append({'id':r['id'],'path':r['path'],'source_commits':[s['commit'] for s in r['sources']],'target_substring_present':active['target_id'] in text,'save_substring_present':active['default_save'] in text,'explicit_Q_CAG_HALF_6_present':'Q-CAG-HALF-6' in text,'also_general_or_arbitrary_word_present':any(q in text for q in ['任意人数','一般人数','任意m','任意 `m','任意m>=1'])})
report={'scope':'new static contract/data-row/metadata audit; no original modules imported, no old suite executed, no linked mathematical proofs certified','catalog':{'entries':len(catalog['entries']),'renamed_paths':len(catalog['renamed_paths']),'duplicate_paths':len(catalog['entries'])-len(names),'canonical_bad':canonical_bad,'human_label_and_purpose_bad':names_bad,'unknown_topics_or_roles':[r['path'] for r in catalog['entries'] if r['topic'] not in {k for k,_,_ in topics} or r['role'] not in roles],'unnamed_related_paths':[q for r in catalog['entries'] for q in r.get('related_paths',[]) if q not in names],'required_frozen_metadata':required_by_commit,'generated_catalog_data_rows':len(actual_catalog),'generated_catalog_all_data_rows_exact_order_equal':actual_catalog==expected_catalog,'generated_WC_data_rows':len(actual_wc),'generated_WC_all_data_rows_exact_order_equal':actual_wc==expected_wc,'package_counts':dict(collections.Counter(r.get('package','') for r in catalog['entries'] if r['topic']=='weighted_congestion'))},'wc':{'source_files_count':len(integration['source_files']),'classification_count':len(integration['classification']),'equal_keysets':set(integration['source_files'])==set(integration['classification']),'rows':wc},'active':{'constants':source_constants,'actual_entry_input_checks':active_inputs,'target_substring_is_not_exact_scope_check':True}}
retirement=load(bypath('history/research_operations/customer_attraction_transition/manifest.json'))
retired=[]
for rr in retirement['entries']:
 pp=bypath(rr['archived_path']);actual_sha=hashlib.sha256(pp.read_bytes()).hexdigest();retired.append({'original_path':rr['original_path'],'archived_path':rr['archived_path'],'recorded_sha256':rr['sha256'],'actual_sha256':actual_sha,'equal':actual_sha==rr['sha256']})
report['active']['actual_retired_byte_checks']=retired
report['active']['substring_accepts_six_specific_target'] = active['target_id'] in 'Q-CAG-HALF-6'
# Parse every local link using the original input lexing rule, against immutable metadata.
active_lex=[]
all_paths=set(active['active_entrypoints']+active['role_prompts']+[active['runbook'],active['mathematical_entry']])
for rr in related:
 if rr['path'] not in all_paths:continue
 text=(STAGE/rr['saved_path']).read_text();prose=re.sub(r'(?ms)^(```|~~~).*?^\1\s*$', '', text);links=[]
 for match in re.finditer(r'(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)',prose):
  ref=match[1].strip('<>')
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',ref) or ref.startswith('#'):continue
  target=posixpath.normpath(posixpath.join(posixpath.dirname(rr['path']),ref.split('#',1)[0]));presence={}
  for cc in [ss['commit'] for ss in rr['sources']]:
   idx=indices[cc];presence[cc]=target in idx or any(p.startswith(target.rstrip('/')+'/') for p in idx)
  links.append({'href':ref,'target':target,'frozen_presence':presence})
 active_lex.append({'id':rr['id'],'path':rr['path'],'links':links})
report['active']['lexical_link_metadata_checks']=active_lex
(B/'contract-structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'catalog_entries':len(catalog['entries']),'catalog_data_rows':len(actual_catalog),'catalog_rows_equal':actual_catalog==expected_catalog,'wc_data_rows':len(actual_wc),'wc_rows_equal':actual_wc==expected_wc,'wc_classifications':len(wc),'source_constants_versions':len(source_constants),'active_entry_versions':len(active_inputs)},ensure_ascii=False))
