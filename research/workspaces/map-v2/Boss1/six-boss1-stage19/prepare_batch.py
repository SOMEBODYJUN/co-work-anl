"""Prepare the reviewed, targeted replacement map batch after a clean map sync."""
from pathlib import Path
from hashlib import sha256
import copy
import json
import subprocess

R=Path('/workspace/scratch/b0fef5ec503f/co-work-anl-boss1-map')
P=R/'research/workspaces/map-v2/Boss1/six-boss1-stage19'
P.mkdir(exist_ok=False)
WS=R/'research/workspaces/six-boss1-20261111'
OLD='six-boss1-source-requery-map3b'
TASK='six-boss1-stage19-wallets-map3b'
NEW='customer-attraction/internal-safe-exact-domains-and-ordered-menu-projection'
ROOT='M-a90ca74cfdc848cb8f628fac8dd35f0a'
COMP='customer-attraction/six-providers/cross-branch-necessary-system-20261111'
JP='customer-attraction/ordered-middle-safe-joint-tail-projection'


def write(p,d):
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')


def digest(p):return sha256(p.read_bytes()).hexdigest()


oldplan=json.loads((R/'research/workspaces/map-v2/Boss1/six-boss1-source-requery/plan-correct-format.json').read_text())[0]
oldreceipt=json.loads((R/f'map/receipts/{OLD}.json').read_text())
registry=json.loads((R/'research/registry.json').read_text());objects={o['object_id']:o for o in registry['objects']}
assert len(registry['edge_files'])==2127
assert objects[ROOT]['version']==3 and objects[COMP]['version']==14 and objects[NEW]['version']==1
pins=copy.deepcopy(oldplan['input_pins'])
for oid,slug in [(NEW,'internal'),(ROOT,'root'),(COMP,'computation')]:
 d=json.loads((WS/f'registration/stage19-show-{slug}.stdout.json').read_text())
 assert d['object_id']==oid
 pins[oid]=d['registration_pin']
proc=subprocess.run(['python','work.py','research','show',JP],cwd=R,capture_output=True,text=True)
(P/'generic-jp-show.stdout.json').write_text(proc.stdout);(P/'generic-jp-show.stderr.txt').write_text(proc.stderr)
assert proc.returncode==0,proc.stderr
pins[JP]=json.loads(proc.stdout)['registration_pin']
assert len(pins)==17
write(P/'input_pins.json',pins)

plan=copy.deepcopy(oldplan)
plan['task_id']=TASK
plan['supersedes']=[OLD]
plan['object_ids']=oldplan['object_ids']+[NEW]
plan['read_object_ids']=oldplan['read_object_ids']+[JP]
plan['input_pins']=pins
plan['write_paths']=['map/edges/six-boss1-20261111',f'map/receipts/{TASK}.json']
question='保留旧八核心及其14条准确支持，接入完整内部参数域v1、根投影v3和计算v14：真实内部IC/CAP/SAFE如何支付ROOT270、完整3056及γ36；旧整结果边是否仍覆盖扩展目标。'
plan['goal']=question
plan['context_plan']={'comparison_question':question,'comparison_groups':[plan['object_ids']],
 'scope_note':'定向替代同Boss旧done批；保留6条逐字旧边，刷新8条条件/版本命中边并将旧source3 whole_result收窄为v2贡献，新增3条ALL联合边。九核心、八共享来源、17条关系；无其它存档审查或全仓完成声明。'}
write(P/'plan.json',[plan])

summary=json.loads((WS/'registration/stage19-registration-summary.json').read_text())
replaced=set(summary['affected_existing_edges']);newpaths=summary['new_edges']
assert len(replaced)==8 and len(newpaths)==3
assets=[];sup={};edges={}
for asset in oldreceipt['assets']:
 rel=asset['path'];actual=digest(R/rel)
 if rel in replaced:
  assert actual!=asset['sha256']
  sup[rel]={'disposition':'replaced','replacement_paths':[rel],
            'reason':'目标或前提正文改版后重新核实际范围、更新证据与端点pins；保留原承重数学，旧source3全结果声明收窄为v2贡献。'}
 else:
  assert actual==asset['sha256']
  sup[rel]={'disposition':'retained','reason':'本次改版未触及该关系的正文、端点或证据，保持已审旧SHA和准确贡献。'}
 assets.append({'path':rel,'sha256':actual})
for rel in newpaths:assets.append({'path':rel,'sha256':digest(R/rel)})
for asset in assets:
 edge=json.loads((R/asset['path']).read_text())
 assert edge['status']=='accepted' and edge['premises_mode']=='all'
 assert all(pins[k]==v for k,v in edge['endpoint_pins'].items())
 assert edge.get('whole_result') or edge.get('contribution')
 edges[edge['edge_id']]=edge
assert len(assets)==len(edges)==17
coverage=copy.deepcopy(oldreceipt['coverage'])
for oid,entry in coverage.items():
 entry['object_pin']=pins[oid]
 entry['comparison_scope']+=' Stage19仅改三项有独立新数学的owner；旧贡献仍限定原明列阶段，未因目标扩展自动支付新结论。九核心/八共享来源的本批模型条件与scope见comparison_review.md。'
coverage[ROOT]['reason']='C36/C30与ROOT36/30/CAP2的旧完整证明保留；原两前提边现在仅承认v2贡献。另加入完整内部域的第四源P25专门化，与真实模型和PAIR联合支付ROOT270及η|C\\O|，新ALL边覆盖v3整条结论。'
coverage[ROOT]['edge_ids']=list(dict.fromkeys(coverage[ROOT]['edge_ids']+[
 'ca-six-boss1-pair-and-internal-domains-pay-full-root-requery','ca-six-boss1-visible-C-true-wallets-to-global-gamma36']))
coverage[COMP]['reason']+=' Stage19新ALL边逐十正付款给全513列α3056、真实C分支的整面排除及γ36准确统一改善；固定16hist值仍仅局部有限LP，零权上帽未被推广。'
coverage[COMP]['edge_ids'].append('ca-six-boss1-visible-C-true-wallets-to-global-gamma36')
coverage[NEW]={'state':'linked','object_pin':pins[NEW],
 'comparison_scope':'一般JP保原身份；新增owner专门求准确锚域、最小帽、真实双锚λ、同菜单条件重数及δ连续无损有限化。模型为每个真实源节点逐项付IC/CAP/SAFE/BR；不把actual节点收益偷换到强制节点。',
 'reason':'正文COST逐项真付款；全状态余项给必要充分面，全部顶点/断点保闭边界与弱尾；q=(d−t)/5准确保持同菜单索引关联，连续d=1或全部条件分片另证。独立可用的是完整参数族，不重复登记一般JP。',
 'edge_ids':['ca-six-boss1-true-internal-wallets-to-complete-domains',
             'ca-six-boss1-pair-and-internal-domains-pay-full-root-requery',
             'ca-six-boss1-visible-C-true-wallets-to-global-gamma36']}
receipt={'coverage':coverage,'assets':assets,'supersession':{OLD:{
 'reason':'两旧owner追加已核数学并升版，新增一个完整参数域owner；只替代命中关系范围，旧核心与其余全部数学保持。','assets':sup}}}
assert len(coverage)==9
for entry in coverage.values():assert set(entry['edge_ids'])<=set(edges)
write(R/f'map/receipts/{TASK}.json',receipt)
write(P/'ready.json',[{'task_id':TASK,'receipt_file':f'map/receipts/{TASK}.json'}])

review='''# Boss1 Stage19 定向比较审读

本批承接 `six-boss1-source-requery-map3b`。Main保留旧八核心及七共享来源已经完成的逐证明审读；其中六条边的最终字节、端点与证据完全不变。只重判命中根投影v3/计算v14的八条关系，并加入新内部域owner及一般JP共享来源。共九核心、八共享来源、17条关系，精确pins在同目录 input_pins.json。

## 新旧身份与完整性

一般JP承载任意非负权同尾投影，新对象不重领其身份。新对象亲自展开COST：真实源IC、内部SAFE、尾CAP和末BR全部来自同一给定策略在各自有序历史的真实续局；自由C等式另列。完整固定帽/最小帽域、λ单缺和多缺余项、根六个双缺面、条件q=(d−t)/5及δ全部仿射弱态均有独立准确重建。

旧source3两前提边仍正确支付原v2的C36/C30、30索引增益与三条根线，不能仅刷新SHA后继续声称它支付扩展目标的全部结论。故其whole_result改为准确contribution。新增ALL边另付真实第四源P25，使ROOT270十预算、两个质量自由项和128客户余项完整相加；η|C\\O|对32个C外型准确支付。

## 福利合账的真实范围

完整3056必要LP含继承最优并上帽，所以O=OPT6且正OPT6才归一化。X一次选择为同一actual前四背景的全目录最大潜力标签，C才是最大裸大小标签。十条正付款全部重新核范围后，普遍福利证书可另用于任意六合法查询并；零权上帽不作为该推广的前提。

新正C行的全部弱尾必须与真实正CAP和正SAFE一起用：完整18零列面先给C⊆O，再给R3=R4=R5=C及N4=N5=K/5；结构差(1−K)/36严格正，故整个旧面不可实现。统一间隙另由真实δ切割、根C外余款、六actual SAFE(C)及完整64列旧余量给出，不能由“每实例严格”直接推出。γ36最终513列恒等式与独立K/自由EC全部Main核验。

新全局边只支付这些明确结论。BG、UP等若在3056正权中为零，不被列为其正付款来源；它们在旧阶段的正确付款仍按旧边范围保留。固定16hist的较高数值不是普遍福利界。所有原型都只是必要系统点，没有因此给出完整SPE反例；half仍开放。

## 保存和未决事项

三个新增正式owner版本与八条改边已在研究checkpoint推送。旧正式根v2/计算v13逐字版本及commit定位保留；旧冻结证据的SHA不改。部分含EOF空行或TSV空字段的证据以无损gzip保存，读取前运行原 restore_frozen_text.py。

本回执保留旧14资产中的6个准确SHA，8个同路径定向替换，再加入3条新边；不退休任何仍成立路线。不清除其他Boss、其他存档或未实际审查关系的pending状态。本次没有新增跨外档数学映射，不作全仓最终审核通过声明。
'''
(P/'comparison_review.md').write_text(review.rstrip()+'\n')
oldint=json.loads((R/'map/integration.json').read_text())
write(P/'preassemble_pending.json',{
 'pending_changes':oldint.get('pending_changes',{}),
 'archive_unresolved':{scope:row.get('unresolved',[]) for scope,row in oldint['archive_reviews'].items()},
 'cross_archive_unresolved':oldint['cross_archive_review'].get('unresolved',[])})
write(P/'preparation_result.json',{'status':'REVIEWED_TARGETED_REPLACEMENT_PREPARED','task_id':TASK,
 'core_count':9,'read_count':8,'input_pin_count':17,'assets':17,'old_assets_retained':6,'old_assets_replaced':8,
 'new_edges':3,'new_canonical_inclusion_yet':False,'registry_sha256':digest(R/'research/registry.json')})
(P/'prepare_batch.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'status':'PREPARED','task_id':TASK,'assets':17,'cores':9,'inputs':17},ensure_ascii=False),flush=True)
