"""Lossless structural reader for four exported frozen JSON certificates; no solver."""
from pathlib import Path
from collections import Counter
import argparse, gzip, hashlib, json


def strict_object(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d


def parse_certificate(raw):
 d=json.loads(raw,object_pairs_hook=strict_object)
 m,p=d['m'],d['p'];A={}
 assert isinstance(d['actions'],list)
 for row in d['actions']:
  assert list(row)==['history','action']
  h=tuple(row['history']);a=row['action']
  assert h not in A and len(h)<m and all(type(x) is int and 0<=x<p for x in h)
  assert type(a) is int and 0<=a<p
  A[h]=a
 assert len(A)==sum(p**j for j in range(m))
 classes={};nodes=[];frequencies=Counter()
 def visit(h):
  if len(h)==m:return -1
  children=tuple(visit(h+(a,)) for a in range(p))
  signature=(A[h],children)
  if signature not in classes:
   classes[signature]=len(nodes);nodes.append(dict(id=len(nodes),action=A[h],children=list(children)))
  i=classes[signature];frequencies[i]+=1
  return i
 root=visit(())
 rebuilt={}
 def expand(h,i):
  if i==-1:
   assert len(h)==m
   return
  node=nodes[i];rebuilt[h]=node['action']
  for a,ch in enumerate(node['children']):expand(h+(a,),ch)
 expand((),root)
 rebuilt_actions=[dict(history=list(h),action=a) for h,a in sorted(rebuilt.items())]
 assert rebuilt_actions==d['actions']
 reconstructed={k:rebuilt_actions if k=='actions' else v for k,v in d.items()}
 assert (json.dumps(reconstructed,indent=2)+'\n').encode()==raw
 for node in nodes:node['ordered_history_multiplicity']=frequencies[node['id']]
 return dict(metadata={k:v for k,v in d.items() if k!='actions'},source_json_key_order=list(d),root_class=root,terminal_class=-1,classes=nodes,action_records=len(A),full_json_reconstructed_byte_identically=True)


def runs(xs):
 out=[]
 for x in xs:
  if out and out[-1][1]==x:out[-1][0]+=1
  else:out.append([1,x])
 return out


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--sources-root',type=Path,required=True);parser.add_argument('--plan',type=Path,required=True);parser.add_argument('--evidence',type=Path,required=True)
 a=parser.parse_args();plan=json.loads(a.plan.read_text());a.evidence.mkdir(parents=True,exist_ok=True)
 cert_manifest=json.loads((a.evidence/'certificate-manifest.json').read_text());view=[];data=[]
 view.extend(['# 四份冻结完整证书的无损结构阅读视图','','本视图来自父方正式导出的实际冻结JSON：读取全部字段和每一条history/action，再将完全相同的有序子树合并。没有执行原程序、BI、收益回放、LP或新参数测试。','',
 '每类保当前行动及全部p个有序孩子；孩子按动作标签0至p−1排列，`[重复次数,子类ID]`逐段展开，−1为长度m终局。类的“出现次数”是完整有序树中的前缀数。根类递归展开可还原每个历史动作，再按history字典序排回源actions；其余字段全部原值和源键序也列出。恢复后以原indent=2序列化，要求与实际源JSON逐字相等，而不只相同摘要或节点数。',''])
 for s,c in zip(plan,cert_manifest['certificates']):
  source=a.sources_root/s['path'];raw=source.read_bytes();assert len(raw)==s['size'] and hashlib.sha256(raw).hexdigest()==s['sha256']
  blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert blob==s['blob']
  preserved=a.evidence/'certificates'/Path(c['path']).name;assert gzip.decompress(preserved.read_bytes())==raw
  parsed=parse_certificate(raw)
  row=dict(source=s,local_export_path=str(source),existing_unique_gzip=c['path'],byte_equal_to_current_generated_certificate=True,raw_read_view=parsed)
  data.append(row);m=parsed['metadata']['m']
  view.extend([f'## m={m}：{s["id"]}', '',f'冻结路径：`{s["path"]}`。原件{len(raw)}B，SHA256 `{s["sha256"]}`；Git blob也吻合。现有唯一gzip解压与源逐字相同。','',
   '源顶层键顺序：`'+','.join(parsed['source_json_key_order'])+'`。除actions以外全部字段如下：','','```json',json.dumps(parsed['metadata'],ensure_ascii=False,indent=2),'```','',
   f'actions共{parsed["action_records"]}条，根类{parsed["root_class"]}；完整无损子树表：','',
   '| 类ID | 当前联合行动 | 有序孩子的[次数,类ID]段 | 出现次数 |','|---:|---:|---|---:|'])
  for n in parsed['classes']:view.append(f'| {n["id"]} | {n["action"]} | `{json.dumps(runs(n["children"]),separators=(",",":"))}` | {n["ordered_history_multiplicity"]} |')
  view.extend(['',f'已从上表展开全部{parsed["action_records"]}条actions并恢复源全部字段、键序和缩进，JSON重建逐字同原件：true。',''])
 (a.evidence/'frozen-certificate-full-reading-view.md').write_text('\n'.join(view)+'\n')
 (a.evidence/'frozen-certificate-reading-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([dict(id=r['source']['id'],size=r['source']['size'],sha256=r['source']['sha256'],ordered_action_records=r['raw_read_view']['action_records'],unique_subtree_classes=len(r['raw_read_view']['classes']),full_json_reconstructed_byte_identically=r['raw_read_view']['full_json_reconstructed_byte_identically']) for r in data],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
