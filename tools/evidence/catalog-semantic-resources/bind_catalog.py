#!/usr/bin/env python3
"""New exact full catalogue byte binding; no old-module/Git execution.

This checks representation only. Actual2099semantic reading is separately logged.
"""
from pathlib import Path
import ast,hashlib,json,posixpath
B=Path(__file__).resolve().parent
catalog=json.loads((B/'original/research/catalog.json').read_text())
assets=json.loads((B/'related/research/assets.json').read_text())
def literal_values(p,names):
 out={}
 for node in ast.parse(p.read_text()).body:
  if isinstance(node,ast.Assign):
   for target in node.targets:
    if isinstance(target,ast.Name) and target.id in names:out[target.id]=ast.literal_eval(node.value)
 return out
const=literal_values(B/'related/research/build_catalog.py',{'TOPICS','ROLES','PACKAGE_TITLES'})
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
lines=["# 研究资产总目录：按数学问题找名字、正文与证据", "",
"这里登记当前数学稿、问题、审查和已整合的拥塞核验资产。每个名称和用途经过逐文件整理；文件名、提交者代号与目录位置都不代替数学身份。",
"先从下表选择问题，再进入专题的阅读路线。历史原稿按需从 [历史入口](../history/README.md) 与 [来源对应](source_crosswalk.md) 查询；规范程序和人类讲义从 [全仓资产入口](../ASSETS.md) 进入。", "",
"证明、内部审查、外部审查和实现的真实状态分别保存在 [五轴账本](review_status.json)；精确量词在 [命题登记](current/claims.md) 和 [拥塞命题账本](weighted_congestion_frontier/CLAIMS.md)。下表只说明文件角色，不为整份文件授予统一的‘已证明’标签。关联命题由所在资产包汇总，不能解释为该文件逐一证明全部所列命题；逐命题依据回到精确账本和正文。", "",
"| 数学专题 | 首读入口 | 逐文件目录 |", "| --- | --- | --- |"]
for key,title,entry in topics:
 if any(r['topic']==key for r in catalog['entries']):lines.append(f"| {title} | [研究说明]({entry}) | [中文资产名与用途](#{key}) |")
lines += ["", "维护方法：先在 `catalog.json` 写具体名称和用途，再运行 `python3 research/build_catalog.py`；`--check` 同时拒绝漏登记、缺文件、无中文名称和过时生成稿。新增候选按原等级保存，不能为通过目录检查而升级结论。", ""]
for key,title,_ in topics:
 if any(r['topic']==key for r in catalog['entries']):lines += [f'<a id="{key}"></a>', "", f'## {title}', "", topic_rows(key,'research')]
expected='\n'.join(lines).rstrip()+'\n';actual=(B/'original/research/CATALOG.md').read_bytes();eb=expected.encode()
report={'scope':'new representation binding only, not2099semanticread or proof/role/independencecertification','entries':len(catalog['entries']),'all1596733bytes_equal':actual==eb,'actual_bytes':len(actual),'expected_bytes':len(eb),'actual_sha256':hashlib.sha256(actual).hexdigest(),'expected_sha256':hashlib.sha256(eb).hexdigest(),'topic_counts':{key:sum(r['topic']==key for r in catalog['entries']) for key,_,_ in topics},'role_labels':roles,'topic_order':topics,'package_label_dictionary':pt,'asset_claim_index_input':'related/research/assets.json, dependencyonlynotextrasourcedone'}
(B/'full-md-binding.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['role_labels','topic_order','package_label_dictionary']},ensure_ascii=False))
