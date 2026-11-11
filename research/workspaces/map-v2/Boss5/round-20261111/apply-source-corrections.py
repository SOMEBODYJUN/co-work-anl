"""Apply three exact, mathematically reviewed source corrections; root runs serially."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

changes = {
 'archives/unrelated-machines/state/文献/结构参数下的指派限制调度--文献.md': [
  (r'\operatorname{tw}_{p}\ge \max_i|J(i)|,', r'\operatorname{tw}_{p}\ge \max_i|J(i)|-1,'),
  (r'\operatorname{tw}_{d}\ge \max_j|M(j)|,', r'\operatorname{tw}_{d}\ge \max_j|M(j)|-1,'),
  ('这些是约束满足文献中的结构关系在此模型上的应用，不是新的调度近似界。', '这些是约束满足文献中的结构关系在此模型上的应用，不是新的调度近似界。冻结 PDF 的 Remark 7 本身遗漏上述两个 −1；按其第5页的标准树宽定义，团大小为 r 只能推出树宽至少 r−1。单任务单机器的零树宽也直接排除原字面不等式；这不影响四项算法定理。'),
  (r'取 (L\le\mathrm{OPT}) 或 (L\le2\max_i|J(i)|)', r'在判定阈值 T 下只保留负载不超过 T 的状态，取 (L\le T+1)；或用每机子集和数界 (L\le2^{\max_i|J(i)|})'),
  ('最优值不变，而 primal 和 dual 图都变成完全图，rankwidth 为 1；因此这两个图的 rankwidth 可被人为压低，不能作为有效结构参数。', '最优值不变，dual 图确实变成完全图，rankwidth 为 1。原文还称 primal 图同样完全，但该构造只向旧 primal 图加入一个全邻接的新任务，不会使原本不相邻的旧任务相邻；例如两个互不相邻旧任务加新任务后是三点路径。故此段不认证 primal 图完全或任意 primal rankwidth 归一到1的主张。下文 incidence rankwidth 的 PTAS 由独立的类型计数 DP 和 Rounding Lemma 给出，不依赖这句背景断言。'),
  (r'(\delta^2B/n)', r'(\delta^2B)'),
 ],
 'archives/unrelated-machines/state/审查/归一化菜单福利与配置证书双源审查--审查.md': [
  ('从 β* 见证构造全任务调度：选中组 connector 放 gate、selector 放达到 state 的 private，所领正 incidence 导出资源机；未选 state 与全部其他 jobs 留各自 private。', '从 β* 见证构造全任务调度：root pin 留 root；选中组 connector 放 gate、selector 放达到 state 的 private，所领正 incidence 导出资源机；其余全部 incidence jobs（含未选 states 和零 jobs）留各自 private；未选组 connector 留 root、selector 去 gate。'),
 ],
 'archives/unrelated-machines/state/审查/私有汇点高阶上负相关精确尾概率最终独立审查--审查.md': [
  ('其它 q? 选取不同组各一件送 sink', '从其它 k−q 个不同组各选一件送 sink'),
 ],
}

registry = json.loads((ROOT/'research/registry.json').read_text())
records=[]
for name, pairs in changes.items():
 p=ROOT/name; original=p.read_text(); revised=original
 for old,new in pairs:
  if revised.count(old)!=1: raise ValueError((name,old,revised.count(old)))
  revised=revised.replace(old,new)
 records.append({'path':name,'old_sha256':sha(p),'new_sha256':hashlib.sha256(revised.encode()).hexdigest(),'replacements':[{'old':a,'new':b} for a,b in pairs]})
for row in records:
 p=ROOT/row['path'];text=p.read_text()
 for pair in row['replacements']:text=text.replace(pair['old'],pair['new'])
 p.write_text(text)
objects=registry['objects']; objects=list(objects.values()) if isinstance(objects,dict) else objects
affected=[o['object_id'] for o in objects if any(ref['path'] in changes for ref in [o['body'],*o.get('evidence',[])])]
edges=[]
for ref in registry['edge_files']:
 name=ref if isinstance(ref,str) else ref['path'];e=json.loads((ROOT/name).read_text())
 if set(e.get('source_ids',[])+e.get('target_ids',[])) & set(affected) or any(x['path'] in changes for x in e.get('evidence',[])):edges.append({'path':name,'edge_id':e['edge_id']})
tasks=[]
for p in (ROOT/'research/operations/map-v2/tasks').glob('*.json'):
 t=json.loads(p.read_text());d=t['definition']
 if t['state']!='withdrawn' and set(d['object_ids']+d.get('read_object_ids',[])) & set(affected):tasks.append({'task_id':d['task_id'],'state':t['state'],'owner':t.get('owner')})
write(OUT/'source-correction-impact.json',{'reviewed_by':'Boss5','source_changes':records,'affected_objects':affected,'affected_edges':edges,'affected_tasks':tasks,'previous_baseline':registry['baseline']})
baseline=json.loads((ROOT/registry['baseline']['path']).read_text())
newhash={x['path']:x['new_sha256'] for x in records}
for row in baseline['materials']:
 if row['path'] in newhash:row['sha256']=newhash[row['path']]
baseline['coverage_note']='Full current denominator; exact structural formulas, complete gated job placement, and higher-NC law wording corrected; mathematical endpoint statements retained.'
write(OUT/'source-corrected-inputs.json',baseline)
print(json.dumps({'source_files':len(records),'affected_objects':len(affected),'affected_edges':edges,'affected_tasks':tasks},ensure_ascii=False))
