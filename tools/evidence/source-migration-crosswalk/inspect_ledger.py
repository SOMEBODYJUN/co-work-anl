#!/usr/bin/env python3
"""New local-byte/metadata ledger check; no Git, old code or math suite."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,re
B=Path(__file__).resolve().parent
S=B.parents[2]
def load(rel):return json.loads((B/'original'/rel).read_text())
def sha(d):return hashlib.sha256(d).hexdigest()
m=load('research/path_migration.json');c=load('research/source_crosswalk.json');bc=load('research/branch_cleanup.json')
inv=[json.loads(l) for l in (B/'frozen-inventory.jsonl').read_text().splitlines()]
idx={r['path']:r for r in inv if any(s['commit']=='68fad804ec5946cb296f77dc5b336308a66abf12' for s in r['sources'])}
fields={}
for path in ['research/path_migration.json','research/source_crosswalk.json','research/branch_cleanup.json']:
 v=load(path);f=defaultdict(Counter);leaves=[]
 def walk(v,q):
  f[q][type(v).__name__]+=1
  if isinstance(v,dict):
   for k,w in v.items():walk(w,q+'.'+k)
  elif isinstance(v,list):
   for w in v:walk(w,q+'[]')
  else:leaves.append((q,v))
 walk(v,'$');fields[path]={'input_sha256':sha((B/'original'/path).read_bytes()),'fields':{k:dict(v) for k,v in f.items()},'ordered_scalar_count':len(leaves),'ordered_scalar_sha256':sha(json.dumps(leaves,ensure_ascii=False,separators=(',',':')).encode())}
(B/'json-field-census.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2)+'\n')
# Independently reconstruct all prose, table headers and exact ordered data rows.
lines=['# 逐文件来源解释表','','每一行把一个原始文件或旧代码入口连接到本轮重新撰写的现行数学内容。','历史手稿保留原状供核对；证据、测试和唯一代码在其专门目录。','这个表不把原稿自动当作已经证明的现行命题。','']
accounted=set()
for title,prefix in [('原手稿、笔记、审计与旧路线',('history/',)),('输入、证书与冻结记录',('examples/','evidence/')),('测试和审查代码',('tests/',)),('规范实现',('facility_spe/',))]:
 lines+=['## '+title,'','| 原始路径 | 当前保存位置 | 新写的解释 | 判断 |','| --- | --- | --- | --- |']
 for r in c['entries']:
  if not r['preserved_at'].startswith(prefix) or r['original'] in accounted:continue
  accounted.add(r['original']);old=r['original'].replace('|',r'\|');note=r['interpretation'].replace('|',r'\|');p=r['preserved_at'];target=r['rewritten_in'];lines.append(f'| `{old}` | [{p}](../{p}) | [{target}](../{target}) | {note} |')
 lines.append('')
if c['new_sources']:lines+=['## 新增来源（不属于旧路径迁移）','','对话摘录等新来源单独登记，不虚构原始文件路径或下载记录。','','| 保存位置 | 来源 | 新写的解释 | 判断 |','| --- | --- | --- | --- |']
for r in c['new_sources']:
 p=r['source'];target=r['rewritten_in'];provenance=r['provenance'].replace('|',r'\|');note=r['interpretation'].replace('|',r'\|');lines.append(f'| [{p}](../{p}) | {provenance} | [{target}](../{target}) | {note} |')
if c['new_sources']:lines.append('')
if c['historical_records']:lines+=['## 历史编辑判断与方向记录','','这些文件保留过去的投稿或方向判断。关联页用于理解当时背景，不表示该判断被重写成数学证明，也不覆盖现行目标、审查或新颖性状态。','','| 原位置 | 当前保存位置 | 相关研究背景 | 历史作用与边界 |','| --- | --- | --- | --- |']
for r in c['historical_records']:
 p=r['preserved_at'];links='、'.join(f'[{z}](../{z})' for z in r['related_accounts']);note=r['interpretation'].replace('|',r'\|');lines.append(f"| `{r['original']}` | [{p}](../{p}) | {links} | {note} |")
expected='\n'.join(lines).rstrip()+'\n';actual=(B/'original/research/source_crosswalk.md').read_text()
notes=list(dict.fromkeys(r['interpretation'] for group in ['entries','new_sources','historical_records'] for r in c[group]));noteids={note:f'G{i+1:03}' for i,note in enumerate(notes)}
records=[]
for group in ['entries','new_sources','historical_records']:
 for i,r in enumerate(c[group]):records.append({'record_id':{'entries':'E','new_sources':'N','historical_records':'H'}[group]+f'{i+1:03}','group':group,'index':i,'historical_note_id':noteids[r['interpretation']],**r})
(B/'normalized-records.json').write_text(json.dumps({'scope':'all historical ledger values retained; note IDs factor exact duplicate interpretations, not mathematical identity','notes':[{ 'id':noteids[n],'text':n} for n in notes],'records':records},ensure_ascii=False,indent=2)+'\n')
sha_rows=[]
for i,r in enumerate(c['new_sources']):
 tokens=re.findall(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])',r['provenance']);item=idx.get(r['source']);s=item['sha256'] if item else None;sha_rows.append({'index':i,'path':r['source'],'inventory_id':item['id'] if item else None,'inventory_sha256':s,'explicit_tokens':tokens,'matches_some_token':s in tokens if tokens else None})
archive_rows=[]
for i,r in enumerate(bc['archived_sources']):
 item=idx.get(r['archived_path']);archive_rows.append({'index':i,'archived_path':r['archived_path'],'recorded_bytes':r['bytes'],'recorded_sha256':r['sha256'],'inventory_id':item['id'] if item else None,'inventory_size':item['size'] if item else None,'inventory_sha256':item['sha256'] if item else None,'metadata_equal':bool(item) and item['size']==r['bytes'] and item['sha256']==r['sha256']})
refs=[]
for group in ['entries','new_sources','historical_records']:
 for i,r in enumerate(c[group]):
  fs=['preserved_at','rewritten_in'] if group=='entries' else ['source','rewritten_in'] if group=='new_sources' else ['preserved_at','related_accounts']
  for key in fs:
   for p in r[key] if isinstance(r[key],list) else [r[key]]:refs.append({'group':group,'index':i,'field':key,'path':p,'frozen_file_present':p in idx})
report={'scope':'all primary bytes/read semantics and new local text/metadata binding; no original program, Git lookup, remote, secret audit or linked-math certification','source_crosswalk':{'version':c['version'],'entries':len(c['entries']),'new_sources':len(c['new_sources']),'historical_records':len(c['historical_records']),'empty_sources':c['sources']==[],'all_md_bytes_equal_new_independent_reconstruction':expected.encode()==(B/'original/research/source_crosswalk.md').read_bytes(),'actual_md_bytes':len(actual.encode()),'actual_md_sha256':sha(actual.encode()),'expected_md_sha256':sha(expected.encode()),'exact_note_groups':len(notes),'all680_values_preserved_in_normalized':len(records)==680,'extra_archived_original_path_rows':[{'index':i,'path':r['archived_original_path']} for i,r in enumerate(c['entries']) if 'archived_original_path' in r],'all68_originals_match_migration':{r['original'] for r in c['entries']}==set(m['moved'])|set(m['retired_code_paths']),'missing_frozen_refs':[r for r in refs if not r['frozen_file_present']]},'migration':{'version':m['version'],'mapping_counts':{k:len(v) for k,v in m.items() if isinstance(v,dict)},'distinct_original_paths':len({p for v in m.values() if isinstance(v,dict) for p in v}),'distinct_targets':len({p for v in m.values() if isinstance(v,dict) for p in v.values()}),'retired_test_is_exact_moved_subset':all(m['moved'].get(k)==v for k,v in m['retired_test_entrypoints'].items())},'provenance_hash_metadata':{'rows':sha_rows,'with_explicit_hash':sum(bool(r['explicit_tokens']) for r in sha_rows),'explicit_without_match':[r for r in sha_rows if r['matches_some_token'] is False]},'branch_cleanup':{'branches':len(bc['branches']),'branch_file_counts':[{ 'name':r['name'],'count':len(r['files']),'history_preserved_in_main':r['history_preserved_in_main']} for r in bc['branches']],'archived_routes':len(archive_rows),'archived_metadata_mismatches':[r for r in archive_rows if not r['metadata_equal']],'archived_metadata_rows':archive_rows,'omitted_current_tree_items':len(bc['omitted_current_tree_items']),'archive_branch_counts':dict(Counter(r['branch'] for r in bc['archived_sources'])),'all_archived_statuses':dict(Counter(r['status'] for r in bc['archived_sources'])),'byte_binding_attempt':'cancelled; no completed141blobcheck; see cancelled-byte-binding-attempt.json','remote_inventory_checked':False,'old_secret_audit_repeated':False}}
(B/'ledger-structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exact_whole_MD':report['source_crosswalk']['all_md_bytes_equal_new_independent_reconstruction'],'rows':len(records),'note_groups':len(notes),'provenance_explicit_hash_rows':report['provenance_hash_metadata']['with_explicit_hash'],'provenance_metadata_mismatches':len(report['provenance_hash_metadata']['explicit_without_match']),'archived141_metadata_mismatches':len(report['branch_cleanup']['archived_metadata_mismatches']),'missing_frozen_crosswalk_refs':len(report['source_crosswalk']['missing_frozen_refs'])},ensure_ascii=False))
