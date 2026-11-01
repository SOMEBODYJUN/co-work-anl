"""Prepare scoped manifests/receipts after mathematical source review."""
from pathlib import Path
import hashlib
import json
import platform
import scipy
import numpy

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = 'archives/customer-attraction/tools/evidence/R-51-uniform-portfolio-probes'
PAGE = 'archives/customer-attraction/state/计算/真实前缀组合完整历史MILP与有限重放--计算.md'
PROBE = 'archives/customer-attraction/state/计算/真实前缀组合的最小续局精确探针--计算.md'
IDS = ['2bd1808c0c6f7a935fc6','c5036a7c5ea1e1e839ae','2328caaf40c8b1313a96',
       'c4d557d5a94bf4affacc','7cad09ff023607996bed','309f20a241511455554b']
inventory = [json.loads(line) for line in (ROOT/'cleanup/inventory.jsonl').read_text().splitlines()]
sources = [entry for ident in IDS for entry in inventory if entry['id'] == ident]
assert len(sources) == len(IDS)
for entry in sources:
    saved = ROOT/EVIDENCE/'original'/Path(entry['path']).name
    assert hashlib.sha256(saved.read_bytes()).hexdigest() == entry['sha256']
    entry['saved_path'] = saved.relative_to(ROOT).as_posix()
    entry.pop('progress',None)
manifest = dict(sources=sources, comparison_dependency='R18 full_tree_milp.py; frozen canonical customer_attraction package',
                environment=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__),
                finite_audits=['audit_reports.py: four exact reconstructions; 1103 comparisons including chosen actions',
                               'audit_query_gluing.py: one canonical certificate simultaneously realizes all path-query minima'],
                artifacts={p.relative_to(ROOT/EVIDENCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted((ROOT/EVIDENCE).rglob('*'))
                           if p.is_file() and '__pycache__' not in p.parts and p.name != 'MANIFEST.json'})
(ROOT/EVIDENCE/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
records=[]
for entry in sources:
    name=Path(entry['path']).name
    probe=name=='portfolio_probe.py'
    program=name=='portfolio_full_tree.py'
    read=("完整逐行阅读ExactSPESolver路径枚举、所有最优支持及支持内最便宜重复补槽、每首次偏离子局收益最小化、Fraction余量及负值输出；300样本重放和三例同证书查询粘合核验已保存。" if probe else
          "完整逐行阅读组合MILP包装器及R18基础生成器：全有序节点效用、one-hot动作、真实IC、归一及Big-M上界、固定路径/元组目标、连续客户类型和时限输出合同。" if program else
          "完整读取冻结JSON全部参数、类型向量和动作表，核对45秒status=1、fun、负dual bound、全部根效用；使用已实读生成器明确升序掩码映射，并独立恢复有理质量，重放每个有序历史全部动作的真实IC、W、OPT、查询和与UP余量。")
    records.append(dict(id=entry['id'],source_sha256=entry['sha256'],full_file_reviewed=True,
        related_material_checked=True,unique_content_accounted_for=True,read_note=read,
        comparison_note="实读R51全局入口、已有AAA/BCD数值候选、固定完整策略UP锥探针、真实前缀均匀组合候选及旧17样本/策略锥计算页、规范exact.py/certificate.py和R18完整树MILP。区分固定输入精确路径探针、连续类型MILP和全称UP；没有将有限成功、超时负下界或近零浮点值当成一般证明。",
        decision_note=("整合独有的最小续局与所有最优支持探针、300样本记录和支持内补槽。纠正草稿‘独立min无法粘合’：首次偏离子树不交，可同时实现；给出一般粘合理由并精确核验三份完整证书。仍只有有限输入证据，UP及六人half不变。" if probe else
                       "整合独有的包装器/四张冻结动作表和各自源指纹。四份报告恢复为有理实例并通过1103次全节点动作比较，分别得到12、0、4/3、0的归一UP余量；只认证这些恢复实例，没有认证原MILP最优性、全策略非负或六人half。"),
        disposition='integrated',targets=[PROBE if probe else PAGE,EVIDENCE+'/MANIFEST.json',entry['saved_path']]))
(ROOT/'cleanup/workspaces/Boss1/integration/portfolio-receipts.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(sources=len(sources),receipts=len(records),files=len(manifest['artifacts'])),ensure_ascii=False))
