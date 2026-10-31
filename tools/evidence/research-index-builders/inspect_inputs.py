#!/usr/bin/env python3
"""New all-field/index binding census. Never executes the historical programs.

Reference presence/hashes below are checked against the exact frozen inventory
index. They do not claim a materialized old working tree, mathematical truth,
successful old subprocess suites, or compliance with current stage-three rules.
"""
from pathlib import Path
from collections import Counter,defaultdict
import ast,hashlib,json,posixpath,re
BASE=Path(__file__).resolve().parent
REL=BASE/'related'
def read(path):return (REL/path).read_text()
def load(path):return json.loads(read(path))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(path,data):(BASE/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
index=json.loads((BASE/'frozen-path-index.json').read_text())
files={x['path']:x for x in index['files']}
dirs={posixpath.dirname(p) for p in files}
for p in list(dirs):
 while '/' in p:p=posixpath.dirname(p);dirs.add(p)
def exists(path):return path in files or path in dirs
jsons={str(p.relative_to(REL)):json.loads(p.read_text()) for p in REL.rglob('*.json')}
census={}
for path,data in jsons.items():
 fields=defaultdict(Counter);leaf=[]
 def visit(v,where):
  fields[where][type(v).__name__]+=1
  if isinstance(v,dict):
   for k,w in v.items():visit(w,where+'.'+k)
  elif isinstance(v,list):
   for w in v:visit(w,where+'[]')
  else:leaf.append((where,v))
 visit(data,'$')
 census[path]={'bytes':(REL/path).stat().st_size,'sha256':sha((REL/path).read_bytes()),'fields':{k:dict(v) for k,v in fields.items()},'scalar_count':len(leaf),'ordered_scalar_digest':sha(json.dumps(leaf,ensure_ascii=False,separators=(',',':')).encode())}
save('json-field-census.json',census)
g=load('research/graph.json');review=load('research/review_status.json');migration=load('research/path_migration.json');cross=load('research/source_crosswalk.json');assets=load('research/assets.json');catalog=load('research/catalog.json');learning=load('learning/manifest.json')
nodes={x['id']:x for x in g['nodes']};edges={x['id']:x for x in g['hyperedges']};states={x['id']:x for x in review['entries']}
refs=[]
def ref(owner,field,path):refs.append({'owner':owner,'field':field,'path':path,'frozen_file_present':path in files,'frozen_path_present':exists(path)})
for group in ['nodes','hyperedges']:
 for x in g[group]:
  for p in x['refs']:ref(x['id'],'graph.'+group+'.refs',p)
for x in assets['entries']:
 for field in ['implementation','proof','sources','tests','records','examples','reviews','candidates']:
  for p in x.get(field,[]):ref(x['id'],'assets.'+field,p)
for x in catalog['entries']:
 ref(x['path'],'catalog.path',x['path'])
 for p in x.get('related_paths',[]):ref(x['path'],'catalog.related_paths',p)
for group,fields in [('entries',['preserved_at','rewritten_in']),('new_sources',['source','rewritten_in']),('historical_records',['preserved_at','related_accounts'])]:
 for i,x in enumerate(cross[group]):
  for field in fields:
   v=x[field]
   for p in v if isinstance(v,list) else [v]:ref(f'{group}[{i}]','crosswalk.'+field,p)
save('reference-census.json',{'basis':'frozen inventory metadata, not materialized historical filesystem','total_references':len(refs),'unique_paths':len({x['path'] for x in refs}),'missing_files':[x for x in refs if not x['frozen_file_present']],'entries':refs})
before,after=read('research/current/claims.md').split('## 逻辑使用规则',1)
declared=set();unrecognized=[]
for line in before.splitlines():
 if not line.startswith('| '):continue
 cell=line.split('|',2)[1].strip()
 if cell=='ID' or cell.startswith('---'):continue
 pieces=[x.strip() for x in cell.split(' / ')]
 for p in pieces:
  ident=p if p in nodes else pieces[0].rsplit('-',1)[0]+'-'+p
  if ident not in nodes:unrecognized.append({'cell':cell,'expanded':ident})
  declared.add(ident)
ignored=[line for line in after.splitlines() if line.startswith('| ')]
used={p for e in g['hyperedges'] for p in [*e['premises'],e['conclusion']]}
incoming={e['conclusion'] for e in g['hyperedges']}
graph_checks={'nodes':len(g['nodes']),'hyperedges':len(g['hyperedges']),'duplicate_node_ids':len(g['nodes'])-len(nodes),'duplicate_edge_ids':len(g['hyperedges'])-len(edges),'node_kinds':dict(Counter(x['kind'] for x in g['nodes'])),'node_tracks':dict(Counter(x['track'] for x in g['nodes'])),'edge_kinds':dict(Counter(x['kind'] for x in g['hyperedges'])),'edge_tracks':dict(Counter(x['track'] for x in g['hyperedges'])),'declared_prefix_ids':len(declared),'review_ids':len(states),'declared_not_review':sorted(declared-set(states)),'review_not_declared':sorted(set(states)-declared),'unrecognized_prefix_ids':unrecognized,'isolated_nodes':sorted(set(nodes)-used),'claim_nodes_without_incoming':sorted(x['id'] for x in g['nodes'] if x['kind']=='claim' and x['id'] not in incoming),'missing_edge_endpoints':[e['id'] for e in g['hyperedges'] if not set([*e['premises'],e['conclusion']])<=set(nodes)],'status_mismatch':[k for k in states if k in nodes and states[k]['graph_status']!=nodes[k]['status']],'review_axis_counts':{k:dict(Counter(x.get(k) for x in review['entries'])) for k in ['source_proof','current_proof','internal_review','external_review','implementation']},'ignored_claim_table_rows_after_logic_heading':ignored,'ignored_row_ids_in_graph':{re.match(r'\|\s*`?([^`| ]+)',s)[1]:re.match(r'\|\s*`?([^`| ]+)',s)[1] in nodes for s in ignored},'customer_attraction_nodes_in_extensions':[x['id'] for x in g['nodes'] if x['track']=='extensions' and any(p.startswith('research/current/customer_attraction/') for p in x['refs'])]}
tree=ast.parse((BASE/'original/research/build_map.py').read_text());template=next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HTML' for t in x.targets))
actual=read('research/index.html');payload=json.dumps(g,ensure_ascii=False,separators=(',',':')).replace('</','<\\/');expected=template.replace('__GRAPH_DATA__',payload)
graph_checks['static_generated_html_exact_bytes_equal']=actual==expected
graph_checks['actual_html_sha256']=sha(actual.encode());graph_checks['expected_template_and_payload_sha256']=sha(expected.encode())
records={x['original']:x for x in cross['entries']};origins=set(migration['moved'])|set(migration['retired_code_paths']);crosschecks={'schema_version_not_checked_by_old_renderer':cross.get('version'),'moved':len(migration['moved']),'retired_code_paths':len(migration['retired_code_paths']),'source_entries':len(cross['entries']),'new_sources':len(cross['new_sources']),'historical_records':len(cross['historical_records']),'original_set_equal':set(records)==origins,'duplicate_originals':len(cross['entries'])-len(records),'target_mismatches':[k for k,v in {**migration['moved'],**migration['retired_code_paths']}.items() if k not in records or records[k]['preserved_at']!=v],'record_shapes':{group:[{'fields':list(k),'count':v} for k,v in Counter(tuple(sorted(x)) for x in cross[group]).items()] for group in ['entries','new_sources','historical_records']},'unused_top_level_sources_count':len(cross.get('sources',[]))}
# Compare every actual generated table row to its real input record. No source program is imported.
tick='`';lines=[];accounted=set()
for prefix in [('history/',),('examples/','evidence/'),('tests/',),('facility_spe/',)]:
 for x in cross['entries']:
  if x['preserved_at'].startswith(prefix) and x['original'] not in accounted:
   accounted.add(x['original']);old=x['original'].replace('|',r'\|');note=x['interpretation'].replace('|',r'\|');p=x['preserved_at'];new=x['rewritten_in'];lines.append(f'| {tick}{old}{tick} | [{p}](../{p}) | [{new}](../{new}) | {note} |')
for x in cross['new_sources']:
 p=x['source'];new=x['rewritten_in'];provenance=x['provenance'].replace('|',r'\|');note=x['interpretation'].replace('|',r'\|');lines.append(f'| [{p}](../{p}) | {provenance} | [{new}](../{new}) | {note} |')
for x in cross['historical_records']:
 p=x['preserved_at'];links='、'.join(f'[{z}](../{z})' for z in x['related_accounts']);note=x['interpretation'].replace('|',r'\|');lines.append(f"| `{x['original']}` | [{p}](../{p}) | {links} | {note} |")
outrows=[line for line in read('research/source_crosswalk.md').splitlines() if line.startswith('| ') and not line.startswith('| ---') and line not in ['| 原始路径 | 当前保存位置 | 新写的解释 | 判断 |','| 保存位置 | 来源 | 新写的解释 | 判断 |','| 原位置 | 当前保存位置 | 相关研究背景 | 历史作用与边界 |']]
crosschecks['all680_generated_rows_in_exact_order_equal']=outrows==lines;crosschecks['actual_output_rows']=len(outrows);crosschecks['expected_output_rows']=len(lines);crosschecks['all_originals_classified']=accounted==origins
learning_links=[]
for module in learning['modules']:
 path=module['path'];content=read(path);clean=re.sub(r'(?s)```.*?```|(?<!\\)\$\$.*?(?<!\\)\$\$|\\\[.*?\\\]','',content);clean=re.sub(r'(?<!\\)\$(?!\$)[^$\n]+(?<!\\)\$|\\\(.*?\\\)','',clean)
 for m in re.finditer(r'(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)',clean):
  href=m[1]
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href) or href.startswith('#'):continue
  target=posixpath.normpath(posixpath.join(posixpath.dirname(path),href.split('#',1)[0]));learning_links.append({'source':path,'href':href,'target':target,'frozen_exists':exists(target)})
runchecks=[]
for path,report in jsons.items():
 if not path.startswith('evidence/runs/2026-10-01/'):continue
 row={'path':path,'required_metadata_present':all(report.get(k) for k in ['schema_version','python_version','base_commit','replay_commands','source_sha256','limitations']),'source_hash_field_type':type(report.get('source_sha256')).__name__,'input_certificate_bindings':[]}
 for k in ['input','certificate']:
  if k in report:
   p=report[k];entry=files.get(p);row['input_certificate_bindings'].append({'role':k,'path':p,'expected_sha256':report.get(k+'_sha256'),'frozen_inventory_sha256':entry.get('sha256') if entry else None,'equal':bool(entry) and entry['sha256']==report.get(k+'_sha256')})
 runchecks.append(row)
assetchecks={'asset_entries':len(assets['entries']),'duplicate_asset_ids':len(assets['entries'])-len({x['id'] for x in assets['entries']}),'asset_fields_all_shapes':[{'fields':list(k),'count':v} for k,v in Counter(tuple(sorted(x)) for x in assets['entries']).items()],'asset_claim_ids_missing':[x['id'] for x in assets['entries'] if not set(x['claims'])<=set(nodes)],'graph_claims_without_asset_route':sorted({x['id'] for x in g['nodes'] if x['kind']=='claim'}-{p for x in assets['entries'] for p in x['claims']}),'catalog_entries':len(catalog['entries']),'catalog_topics':dict(Counter(x['topic'] for x in catalog['entries'])),'catalog_roles':dict(Counter(x['role'] for x in catalog['entries'])),'learning_modules':len(learning['modules']),'learning_unknown_claims':[x['path'] for x in learning['modules'] if not set(x['claims'])<=set(nodes)],'learning_links':learning_links,'historical_run_manifests':runchecks,'retired_old_paths_still_present':[p for p in [*migration['moved'],*migration['retired_code_paths'],*migration['first_curation_retired']] if exists(p)],'current_stage_tree_not_replayed':'Historical scripts expect research/current, history, examples, canonical package roots and old Git index; current archives/map/cleanup layout differs intentionally. No stub or partial dependency replay performed.'}
save('input-structural-audit.json',{'scope':'new all-record metadata/field/reference and actual generated-byte binding only; no historical program execution, mathematical truth or current stage-three acceptance','graph':graph_checks,'crosswalk':crosschecks,'assets':assetchecks,'all_json_files':len(jsons),'field_census':'json-field-census.json','reference_census':'reference-census.json'})
print(json.dumps({'json_inputs':len(jsons),'nodes':len(nodes),'edges':len(edges),'registered_prefix':len(declared),'review':len(states),'ignored_claim_rows':len(ignored),'html_static_bytes_equal':actual==expected,'crosswalk_rows_equal':outrows==lines,'crosswalk_rows':len(lines),'asset_entries':len(assets['entries']),'catalog_entries':len(catalog['entries']),'learning_links':len(learning_links),'historical_run_manifests':len(runchecks),'reference_occurrences':len(refs),'unique_reference_paths':len({x['path'] for x in refs}),'missing_frozen_reference_occurrences':sum(not x['frozen_file_present'] for x in refs)},ensure_ascii=False))
