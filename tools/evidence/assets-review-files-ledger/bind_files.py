"""New whole-FILES static byte binding. Never import/execute old check programs."""
from pathlib import Path
import ast,hashlib,json,posixpath
E=Path(__file__).resolve().parent
catalog=json.loads((E/'related/catalog/original/research/catalog.json').read_text());assets=json.loads((E/'original/research/assets.json').read_text())
def constants(p):
 result={}
 for node in ast.parse(p.read_text()).body:
  if isinstance(node,ast.Assign):
   for t in node.targets:
    if isinstance(t,ast.Name) and t.id in {'TOPICS','ROLES','PACKAGE_TITLES','SCOPE'}:result[t.id]=ast.literal_eval(node.value)
 return result
c=constants(E/'related/catalog/related/research/build_catalog.py');roles=c['ROLES'];pt=c['PACKAGE_TITLES'];claims={};names={r['path']:r['title'] for r in catalog['entries']}
for a in assets['entries']:
 for role in ['proof','tests','records','examples','reviews','candidates','sources','implementation']:
  for p in a.get(role,[]):claims.setdefault(p,set()).update(a['claims'])
def cell(v):return v.replace('|',r'\|').replace('\n',' ')
def rows_render(rs,base):
 out=['| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |','| --- | --- | --- | --- |']
 for r in rs:
  p=r['path'];ids=sorted(claims.get(p,[]));state=roles[r['role']]
  if ids:
   vis='、'.join('`'+q+'`' for q in ids[:3]);suffix=f'（共 {len(ids)} 项）' if len(ids)>3 else '';state+=f'；关联 {vis}，[命题合同{suffix}]({posixpath.relpath("research/assets.json",base)})'
  elif r['role'] in {'account','obstruction','counterexample'}:state+='；精确范围见本页正文'
  label=cell(r['title']).replace('[',r'\[').replace(']',r'\]');purpose=cell(r['purpose'])
  for q in r.get('related_paths',[]):purpose+=f'；配套 [{cell(names[q]).replace(chr(91),chr(92)+chr(91)).replace(chr(93),chr(92)+chr(93))}](<{posixpath.relpath(q,base)}>)'
  out.append(f'| [{label}](<{posixpath.relpath(p,base)}>) | `{p}` | {purpose} | {state} |')
 return out
def topic_rows(topic,base):
 rs=[r for r in catalog['entries'] if r['topic']==topic];packages=list(dict.fromkeys(r.get('package','') for r in rs));packages.sort(key=lambda p:list(pt).index(p) if p in pt else len(pt));out=[];order=['navigation','definition','ledger','account','algorithm','reduction','representation','certificate_account','counterexample','obstruction','candidate','question','literature','review','audit_code','frozen_evidence','source_guide','source']
 for package in packages:
  selected=[r for r in rs if r.get('package','')==package];selected.sort(key=lambda r:order.index(r['role']))
  if package:out+=['### '+pt.get(package,package),'']
  out+=rows_render(selected,base)+['']
 return '\n'.join(out)
old=ast.parse((E/'related/research/check_wc_assets.py').read_text());render=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name=='render');assignment=next(n for n in render.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='lines' for t in n.targets));parts=[]
for item in assignment.value.elts:
 if isinstance(item,ast.Constant) and isinstance(item.value,str):parts.append(item.value)
 elif isinstance(item,ast.Call) and isinstance(item.func,ast.Name) and item.func.id=='render_topic':parts.append(topic_rows('weighted_congestion','research/weighted_congestion_frontier'))
 else:raise ValueError(ast.dump(item))
expected='\n'.join(parts).encode();actual=(E/'original/research/weighted_congestion_frontier/FILES.md').read_bytes();result={'scope':'new complete representation binding only; prior501 catalog semantics actually fully read; FILES shell actually read; no original check execution or mathematical proof certification','bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'expected_bytes':len(expected),'expected_sha256':hashlib.sha256(expected).hexdigest(),'entire_file_equal':actual==expected,'data_rows':sum(l.startswith('| [') for l in actual.decode().splitlines()),'nonrow_parts':parts[:7]+parts[8:],'real_dependencies':['original/research/assets.json','related/catalog/original/research/catalog.json','related/catalog/related/research/build_catalog.py','related/research/check_wc_assets.py']};(E/'full-files-binding.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='nonrow_parts'},ensure_ascii=False));assert actual==expected
