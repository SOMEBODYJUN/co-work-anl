"""Adopt the explicitly reviewed v5 hypergraph proof on a native assembly.

Only the current three endpoints and the same stable edge are discharged.
Other pending changes, including new CAG source-domain work, remain visible.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'tools'))
import research_runtime as rr

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def add(obj,key,note):
    if note not in obj.get(key,''): obj[key]=obj.get(key,'')+'\n'+note

report=HERE/'hypergraph-v5-review.md'
binding=HERE/'hypergraph-v5-bindings.json'
assert sha(report)=='2f9bccee26e1d692c33851e84e9ec2adc78a4f2971c486e144019d835a8f17b8'
assert sha(binding)=='ab96af84cbce44e9e254d142a9d302d7f3ef78dd3e5f884c44be42ad53147f25'
b=read(binding); frozen=b['bindings']
reg=read(ROOT/'research/registry.json'); objects={o['object_id']:o for o in reg['objects']}
d=read(ROOT/'map/integration.json')
assert d['registry_pin']==rr.pin(reg)
for key in ['proof','edge','receipt']:
    x=frozen[key]; assert sha(ROOT/x['path'])==x['sha256'],key
edge=read(ROOT/frozen['edge']['path']); eid=edge['edge_id']
assert frozen['edge']['path'] in reg['edge_files']
assert rr.pin(edge)==frozen['edge']['rr_pin']==d['edge_pins'][eid]
reviewed={x['object_id'] for x in frozen['endpoints']}
for x in frozen['endpoints']:
    assert rr.pin(objects[x['object_id']])==x['rr_pin'],x['object_id']
t=read(ROOT/frozen['task']['path']); rc=read(ROOT/frozen['receipt']['path'])
assert t['state']=='done' and t['receipt']==rc
assert all(rr.pin(objects[oid])==pin for oid,pin in t['definition']['input_pins'].items())
assert d['task_receipt_pins'][b['task_id']]==rr.pin(rc)==frozen['receipt']['rr_pin']
for a in rc['assets']: assert sha(ROOT/a['path'])==a['sha256'],a['path']
assert edge['endpoint_pins']=={x['object_id']:x['rr_pin'] for x in frozen['endpoints']}

note=('Boss1已完成新版超图3D采用：新proof和edge全文实读，独立重推rho(X;(Y,Z))=sqrt(theta)、'
      '原子xi=theta/(r*2^r)、支撑图连通和Y/Z精确Fourier谱；两类尾界、正确Gaussian下标与'
      'finite-h后统一T、zeta、最后源字母表全部闭合。perfect exact4与保perfect近值双正规化保ALL，'
      'typed约束ID/顶点两种测度、真三元支撑及整数cloud保完整无权目标。当前0<delta<=1/2含端点'
      '均为分离promise；delta>1/2的原字面承诺不能沿用。proof SHA '+frozen['proof']['sha256']+
      '、edge SHA '+frozen['edge']['sha256']+'及三端pin逐项匹配，旧11资产原SHA retained、旧1边replaced。'
      '新报告在research/workspaces/map-v2/Boss1/session-1a53a6eb65ea/hypergraph-v5-review.md，'
      '精确绑定在同目录hypergraph-v5-bindings.json。当前修复整条关系成立，没有新增开放前提；'
      '目标对象的独立主3A覆盖不由本3D接管。此前本轮保留该新版待审的观察至此已精确解决。')
add(d,'review_note',note)
if 'Boss1' not in d.get('reviewed_by',''):d['reviewed_by']=d.get('reviewed_by','')+'; Boss1'
u=d['archive_reviews']['archives/unrelated-machines']
add(u,'comparison_scope','当前超图v5局部解析修补与原完整组合归约的精确接合，保目标独立主覆盖。')
add(u,'outcome',note)
add(d['cross_archive_review'],'outcome','本次3D采用保perfect源及正规化到三一致超图的完整桥；其范围为当前图类承诺硬度，没有据名称相近加入调度或CAG结论。')

published=json.loads(subprocess.run(['git','show','HEAD:map/integration.json'],cwd=ROOT,check=True,text=True,capture_output=True).stdout)
p=d.get('pending_changes',{}); old=published.get('pending_changes',{})
po=(set(p.get('object_ids',[]))|set(old.get('object_ids',[])))-reviewed
pe=(set(p.get('edge_ids',[]))|set(old.get('edge_ids',[])))-{eid}
for x in pe:po.update(d.get('edge_endpoints',{}).get(x,[]))
affected={s for oid in po for s in d.get('object_scopes',{}).get(oid,[])}
ps=set(p.get('archive_scopes',[]))|set(old.get('archive_scopes',[]))
unscoped=any(not d.get('edge_endpoints',{}).get(x) for x in pe)
if 'archives/unrelated-machines' not in affected and not unscoped:
    ps.discard('archives/unrelated-machines')
    u['unresolved']=[x for x in u.get('unresolved',[]) if x!='Updated inputs/relations require this preserved comparison to be reviewed again']
d['pending_changes']={'object_ids':sorted(po),'edge_ids':sorted(pe),'archive_scopes':sorted(ps|affected)}
(ROOT/'map/integration.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
result={'status':'CURRENT_HYPERGRAPH_V5_ADOPTED','task':b['task_id'],'edge':frozen['edge'],'reviewed_objects':sorted(reviewed),'remaining_pending':d['pending_changes']}
Path('/workspace/scratch/1a53a6eb65ea/hypergraph-v5-integrated-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
