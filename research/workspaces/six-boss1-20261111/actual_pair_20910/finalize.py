"""Package the audited finite family and freeze only this task's own files."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import csv
import gzip
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = HERE.parents[3]


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def read(p):
    if p.name.endswith('.gz'):
        with gzip.open(p, 'rt') as f:
            return json.load(f)
    return json.loads(p.read_text())


def write(name, data):
    p = HERE/name
    assert not p.exists(), str(p)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


v = read(HERE/'independent_verification.json')
s = read(HERE/'build_summary.json')
l = read(HERE/'labels_and_orbits.json')
rows = read(HERE/'symbolic_rows.json.gz')['rows']
compared = read(HERE/'matrix_positive_proportional_comparison.json')
boolean = read(HERE/'boolean_upper_audit.json')
assert v['status'] == 'PASS' and not v['negative_orbits']
assert (v['label_count'],v['ordered_pair_orbits'],v['literal_ordered_pairs']) == (158,490,24964)
assert min(F(r['exact_slack']) for r in rows) == F(v['minimum_slack']) > 0
assert s['zero_orbits'] == 0 and s['optimizer_calls'] == v['optimizer_calls'] == 0
receipts = {}
for stage in ('build','verify'):
    r = read(HERE/f'execution_{stage}.json')
    assert r['exit_code'] == 0 and r['optimizer_calls'] == 0
    assert sha(HERE/f'{stage}.py') == r['source_sha256']
    assert sha(HERE/f'{stage}.stdout.txt') == r['stdout_sha256']
    assert sha(HERE/f'{stage}.stderr.txt') == r['stderr_sha256']
    receipts[stage] = r
point = WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
matrix = WORK/'full624_augmented_lp/recovery/exact_matrix.json.gz'
assert sha(point) == v['point_sha256'] and sha(matrix) == v['matrix_sha256']

sources = [
    ('archives/customer-attraction/state/引理/共同末位报价与隐藏回复投影--引理.md','full text; strong overlap PAIR and explicit self-tax'),
    ('archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md','full text; three true IC decomposition and upper-bound scope'),
    ('research/workspaces/six-boss1-20261111/old_r_joint.md','sections 3 and 4: exact descriptor and R/Z ordered-history meanings'),
    ('research/workspaces/six-boss1-20261111/main_20910_audit.json','full JSON; exact new input identity and Main full-matrix PASS'),
    ('research/workspaces/six-boss1-20261111/main_exact_two_tail_contract.md','full text; contrast only with finite instantiated-directory TT criterion'),
]
write('source_reading.json',dict(sources=[dict(path=p,sha256=sha(REPO/p),read_scope=sc) for p,sc in sources],
     input_point=dict(path=str(point.relative_to(REPO)),sha256=sha(point)),
     input_matrix=dict(path=str(matrix.relative_to(REPO)),sha256=sha(matrix)),
     construction_imports_other_research_modules=False,verification_imports_constructor=False))

matches = {r['orbit_id']:r['existing_rows'] for r in compared['matches']}
with (HERE/'exact_orbit_results.tsv').open('w',newline='') as f:
    writer = csv.writer(f,delimiter='\t',lineterminator='\n')
    writer.writerow(['orbit_id','Q','R','orbit_size','S6_repetitions_per_literal_pair',
                     'exact_slack','slack_decimal','existing_positive_proportional_rows','signature'])
    for o,r in zip(l['ordered_pair_orbits'],rows):
        writer.writerow([o['id'],*o['representative_names'],o['size'],o['S6_repetitions_per_member'],
                         r['exact_slack'],format(float(F(r['exact_slack'])),'.17g'),
                         json.dumps(matches[o['id']],ensure_ascii=False,separators=(',',':')),
                         json.dumps(o['signature'],ensure_ascii=False,separators=(',',':'))])

rules = defaultdict(list)
for o,r in zip(l['ordered_pair_orbits'],rows):
    a,b = [l['labels'][i] for i in o['representative']]
    if a['id'] == b['id']:
        rule = 'identical-label'
    elif a['id'] < 24 and b['id'] < 24:
        rule = 'two-static-bits'
    elif a['id'] < 24 or b['id'] < 24:
        rule = 'static-times-marginal'
    elif 'node' in a and 'node' in b and a['node'] == b['node']:
        rule = 'same-node-own-RZ'
    elif a['id'] >= 156 and b['id'] >= 156:
        rule = 'same-B4-joint'
    else:
        rule = 'unknown-Frechet'
    rules[rule].append(o['id'])
rule_records = []
for name,ids in rules.items():
    minimum = min(F(rows[i]['exact_slack']) for i in ids)
    minimizers = [i for i in ids if F(rows[i]['exact_slack']) == minimum]
    rule_records.append(dict(rule=name,orbit_count=len(ids),
        literal_pair_count=sum(l['ordered_pair_orbits'][i]['size'] for i in ids),
        exact_minimum=str(minimum),minimum_float=float(minimum),minimizer_orbits=minimizers,
        minimizer_labels=[l['ordered_pair_orbits'][i]['representative_names'] for i in minimizers],
        all_exact_slacks=[dict(orbit_id=i,slack=rows[i]['exact_slack']) for i in ids]))
assert sum(r['orbit_count'] for r in rule_records) == 490
assert sum(r['literal_pair_count'] for r in rule_records) == 24964
write('rule_summary.json',dict(point_sha256=v['point_sha256'],rules=rule_records))

def ray(row):
    data = [(j,F(a)) for j,a in row['sparse_original4849_row']]
    scale = abs(data[0][1])
    return tuple((j,a/scale) for j,a in data)
copy_rays = {ray(rows[i]) for i in range(490) if matches[i]}
all_rays = {ray(r) for r in rows}
assert len(copy_rays) == 102 and len(all_rays) == 264
assert len(all_rays-copy_rays) == 162
minimum = rows[v['minimum_orbits'][0]]
dense = ['0']*4849
for j,a in minimum['sparse_original4849_row']:
    dense[j] = a
write('closest_row_exact.json',dict(**minimum,dense_original4849_row=dense,
      same_minimum_orbits=v['minimum_orbits'],point_sha256=v['point_sha256'],
      existing_positive_proportional_copies=matches[minimum['orbit_id']],
      all_auxiliary_coefficients_zero=True,is_separating=False))

write('execution_notes.json',dict(optimizer_calls=0,successful_receipts=receipts,
      retained_implementation_failures=[
        dict(stage='build',source='failed_zero_normalization_build.py',
             stdout='failed_zero_normalization_build.stdout.txt',stderr='failed_zero_normalization_build.stderr.txt',
             cause='Ray comparison reached an explicitly stored zero wallet coefficient before normalization.',
             repair='Filter zero coefficients; rerun the complete build and exact matrix comparison.'),
        dict(stage='verify',source='failed_old_hist_id_verify.py',
             receipt='failed_old_hist_id_execution_verify.json',
             stdout='failed_old_hist_id_verify.stdout.txt',stderr='failed_old_hist_id_verify.stderr.txt',
             cause='The independent parser initially asserted old hist IDs equal current expanded column IDs.',
             repair='Use current hist blocks and verify the one-to-one old-ID map; rerun the full independent audit.')],
      no_optimization_no_strategy_enumeration=True,
      write_scope=['research/workspaces/six-boss1-20261111/actual_pair_20910/',
                   'research/workspaces/six-boss1-20261111/actual_pair_20910.md']))

rule_chinese = {'identical-label':'同一标签（含重复查询）','two-static-bits':'两个固定会员位',
                'static-times-marginal':'固定会员位 × 随机边缘','same-node-own-RZ':'同 e 的 own R/Z',
                'same-B4-joint':'同一 B4 的 H1/H2','unknown-Frechet':'其余未知交叠的 Fréchet 上界'}
rule_table = '\n'.join(f"| {rule_chinese[r['rule']]} | {r['orbit_count']} | {r['literal_pair_count']} | {r['minimum_float']:.15g} | "
    + '；'.join(','.join(pair) for pair in r['minimizer_labels']) + ' |' for r in rule_records)
orbit_sizes = Counter(o['size'] for o in l['ordered_pair_orbits'])
size_table = '\n'.join(f'| {k} | {orbit_sizes[k]} | {720//k} |' for k in sorted(orbit_sizes))
hash_names = ['labels_and_orbits.json','orbit_hist_frequencies.json.gz','symbolic_rows.json.gz',
              'exact_orbit_results.tsv','family_summary.json','rule_summary.json',
              'closest_row_exact.json','boolean_upper_audit.json','independent_verification.json']
hash_table = '\n'.join(f'| `{name}` | `{sha(HERE/name)}` |' for name in hash_names)
report = f'''# 新20910点：actual单一末两位源的158标签强PAIR完整审计

RUN：`six-boss1-20261111`；Boss1；内部任务 `/root/actual_pair_20910`。

状态：**该完整单源家族已精确核验完成，冻结释放；无负切。** 在新 `20910×20585` 精确点上，158个已具名合法查询标签产生的全部490个有序S6双标签轨道均严格为正，覆盖24,964个字面有序标签对，包含所有Q=R。所有16hist及6个零质量hist均保留。

全局最小值是

`{v['minimum_slack']}`

约为 **{v['minimum_slack_float']:.17g} > 0**，由同索引 `(B_i,C_i)` 及反向达到（轨道142、170；每个轨道6对）。两条行均是现有矩阵零基行号 **703**、名称 `old_1` 的 **1/6** 倍。本轮没有遗漏该单源已具名家族中的负行，也没有可追加的负切。这里关闭的是明确的单行强PAIR上包络家族；原六人完整纯SPE half义务仍 **OPEN**。

本槽只写 `actual_pair_20910/` 与本正文；未改Git、registry、RUN、token或其它冻结文件。新点未有D完成，所以目录不含D；没有使用旧100原子164目录作为新点客户实现。

## 1. 唯一精确输入与源钱包

精确点：`full624_augmented_lp/recovery/augmented_lp_exact.json`，SHA256
`{v['point_sha256']}`。

矩阵：`full624_augmented_lp/recovery/exact_matrix.json.gz`，SHA256
`{v['matrix_sha256']}`。

所有行都从同一真实源 `h=(A1,A2,A3,A4)` 出发，规定末两题是 `(A5,A6)`。逐客户 `P=a1+a2+a3+a4`，钱包严格为

`H = u5 + u6 + sum_x a5/((P+1)(P+2))`。

| 项 | 精确值 | 近似 |
|---|---|---:|
| actual u5 | `{v['source_u5']}` | {float(F(v['source_u5'])):.17g} |
| actual u6 | `{v['source_u6']}` | {float(F(v['source_u6'])):.17g} |
| A5自税 | `{v['source_self_tax']}` | {float(F(v['source_self_tax'])):.17g} |
| H | `{v['source_wallet']}` | {float(F(v['source_wallet'])):.17g} |

独立核验分别从真实份额 `a5/(P+a5+a6)`、`a6/(P+a5+a6)`，及 `f(A5)-g(A5,A6)`、`f(A6)-g(A5,A6)` 重建钱包，两种计算逐hist严格相同。没有省掉倒二税，没有混入B、R、Z或H分支的源收入。

已亲读两个指定正式引理的全部正文。`proof_audit.md` 写出三真IC加自税的完整恒等式、组平均合法性和未知交叠上包络证明；`source_reading.json` 绑定正文SHA。

## 2. 全158标签与准确历史身份

| 标签 | 数量 | 定义 |
|---|---:|---|
| A1,…,A6 | 6 | actual路径六题，S6不动 |
| T_i | 6 | 六个合法比较主题 |
| B_i | 6 | `sigma5(A1,A2,A3,T_i)` |
| C_i | 6 | `sigma6(A1,A2,A3,T_i,B_i)` |
| R_(0,i,j)，i≠j | 30 | `sigma6(A1,A2,A3,T_i,B_j)` |
| R_(1,i,j)，全部i,j | 36 | `sigma6(A1,A2,A3,T_i,C_j)` |
| Z_e，全部66个e | 66 | `sigma6(A1,A2,A3,A4,R_e)` |
| H1,H2 | 2 | 同一分支 `(A1,A2,A3,A6,H1,H2)` 的真实两位后继 |

`R_(0,i,i)=C_i` 是准确历史别名，已经通过只保留非对角R0处理。B4的第三位 `ell/6` 仍只是目录均值，不作行动。不同字面标签即使具有相同旧词或相同覆盖也保名保历史；没有把同组平均边缘解释成同一主题。

S6同步移动T/B/C的索引和R/Z的两个索引，actual与H保持不动。独立程序逐个代表枚举全部720个置换，共352,800个像，并验证轨道两两不交、并集恰为158²。

| 轨道大小 | 有序轨道数 | 每个字面对在720置换中重复次数 |
|---:|---:|---:|
{size_table}

完整158项映射、490个轨道的代表、全部成员、反向轨道和158×158轨道映射均在 `labels_and_orbits.json`。`exact_orbit_results.tsv` 按每条轨道给精确有理余量、代表、频数与现有矩阵副本；`family_summary.json` 保留全部225个有序种类组合的精确最小值及所有最小者。

## 3. 交叠处理与每类结果

对任意合法Q,R使用

`H − sum_x [(q+r)/(P+1) − qr/((P+1)(P+2))] >= 0`。

相同标签用自身边缘，同一e的R/Z用own11，同B4的H1/H2用同一八态联合量，固定会员位与随机主题用位乘边缘。其它交叠在每个hist和完整词型/索引关系频数组中取 `min(qmass,rmass)`。固定当前较小边缘后，该符号表达式在任何合法边缘点上仍是交叠上界；并不声称各行或各客户的上界能同时实现。

| 交叠规则 | 有序轨道数 | 字面有序对数 | 最小余量（近似） | 最小代表 |
|---|---:|---:|---:|---|
{rule_table}

全部6类的**精确**最小分数、所有最小轨道以及各轨道精确余量完整写入 `rule_summary.json`；无任何负值或零值。未知交叠的180个轨道也全部严格正，其最小约0.009620729882684934，因此本次全局最小来自完全已知的旧词交叠。

原4849列全部保留，未用点值替代符号rhs；所有15736个辅助列系数均为0。1306个旧 `overlap` 上包络列未当成真实交叠数据。完整490条稀疏原列向量在 `symbolic_rows.json.gz`，未列原列明确为0；最接近零的完整4849列稠密向量另存 `closest_row_exact.json`。

## 4. 为何不是把组平均错当字面边缘

旧own四态只存 `(family,same,w_i,w_j)` 的组平均。本实现先形成整个字面pair轨道，再按双方token及固定交叠关系分组。每个组内，一个给定随机描述符的每个字面成员拥有相同伙伴次数；因此对任意真实会员赋值，字面边缘之和严格等于次数乘保存的组平均。

独立程序完成336,448个这种符号会员系数检查，覆盖39,376个hist/轨道词型分组。每组同时保留实际字面对、720置换频数、两侧符号边缘、所选交叠符号上界与固定选择。全部记录在 `orbit_hist_frequencies.json.gz`，包括6个零质量hist的选择。

未知随机交叠逐Boolean状态验证：两个不同own父源用4×4组合，own与B4用4×8组合；同父源直接用同一联合态。250个不同真值表共3310个不同Boolean组合，展开到全部分组为454,584次。上界减真实乘积始终非负，已固定交叠始终精确相等。没有用这些局部枚举构造或假设一个共同Fréchet实现。

## 5. 正比例去重与独立审计

490条有序轨道行合为 **264条不同非零正比例射线**。其中193个轨道、102条射线在当前20910矩阵已有正比例副本；297个轨道、162条射线没有逐行正比例副本。后者只是没有这种副本，**未宣称线性独立、锥独立或全局非冗余**。

`matrix_positive_proportional_comparison.json` 保存全部20910行扫描的比对结果、具体旧行号/名称/正比例倍数及本族内归并。存在辅助系数的矩阵行不可能是本族的单行正比例副本；没有用这个事实排除非负多行组合表示。

`verify.py` 不导入构造器、优化器或旧特征模块，独立重建标签、全S6像、literal源钱包、own/B4边缘、未知上界、原4849列系数、490条精确点积与全部副本关系。独立结果为 **PASS**。它还分别检查所有225类最小值及对应最小者。

## 6. 执行、冻结与精确停界

成功执行均使用Python {platform.python_version()}与标准库有理数，无优化器、无旧参数网格、无完整策略扫描：

```sh
python -B research/workspaces/six-boss1-20261111/actual_pair_20910/run_stage.py build
python -B research/workspaces/six-boss1-20261111/actual_pair_20910/run_stage.py verify
```

| 阶段 | 退出码 | 实际秒数 |
|---|---:|---:|
| 完整构造与正比例比对 | 0 | {receipts['build']['elapsed_seconds']:.6f} |
| 独立字面/Boolean/符号全核验 | 0 | {receipts['verify']['elapsed_seconds']:.6f} |

两次实现阶段错误及原日志已保留：首次构造在最后的射线归一中未滤一个显式零系数；首次独立解析错误地假定旧hist编号等于现行扩展列编号。分别修正并完整重跑后通过。它们没有产生被接受的负切或改变最终钱包与最小余量；`execution_notes.json` 给出原错误、修正与真实成功receipt。

本家族严格非负不等于实际末两位可实现，更不等于全历史SPE。此前164标签100原子的失败属于另一个旧客户完成；本次未使用它替代新点。此刻只可关闭：**新20910点、actual前四真实源、158已具名标签、全部有序S6双标签轨道、精确固定交叠加逐组单行Fréchet上包络**。共同耦合及其它真实源义务不在这次闭合结论中。

## 7. 核心产物身份

| 文件 | SHA256 |
|---|---|
{hash_table}

`freeze_manifest.json` 绑定本正文、证明审查、全部程序、输入、完整输出与实际执行记录。本具体任务已完成并释放；原六人half仍OPEN。
'''
reportpath = WORK/'actual_pair_20910.md'
assert not reportpath.exists()
reportpath.write_text(report)
write('status.json',dict(status='FROZEN_SINGLE_SOURCE_FAMILY_CLOSED_RELEASED',
      completed=True,released=True,point_sha256=v['point_sha256'],
      labels=158,ordered_pair_orbits=490,literal_ordered_pairs=24964,
      every_slack_strictly_positive=True,minimum_slack=v['minimum_slack'],minimum_orbits=v['minimum_orbits'],
      new_negative_rows=0,independent_verification='PASS',optimizer_calls=0,general_six_half='OPEN',
      scope=s['scope']))
manifest = dict(status='FROZEN_SINGLE_SOURCE_FAMILY_CLOSED_RELEASED',utc=datetime.now(timezone.utc).isoformat(),
      argv=[sys.executable,*sys.argv],cwd=str(Path.cwd()),python=platform.python_version(),
      source_sha256=sha(Path(__file__)),point_sha256=v['point_sha256'],matrix_sha256=v['matrix_sha256'],
      result=read(HERE/'status.json'),successful_receipts=receipts,assets=[])
for p in sorted(HERE.iterdir()):
    if p.is_file() and p.name not in ('freeze_manifest.json','freeze_receipt.json','finalize.stdout.txt','finalize.stderr.txt'):
        manifest['assets'].append(dict(path=str(p.relative_to(REPO)),sha256=sha(p),bytes=p.stat().st_size))
manifest['assets'].append(dict(path=str(reportpath.relative_to(REPO)),sha256=sha(reportpath),bytes=reportpath.stat().st_size))
write('freeze_manifest.json',manifest)
receipt = dict(status=manifest['status'],manifest_sha256=sha(HERE/'freeze_manifest.json'),
      report_sha256=sha(reportpath),independent_verification_sha256=sha(HERE/'independent_verification.json'),
      assets=len(manifest['assets']),minimum_slack=v['minimum_slack'],
      no_negative_rows=True,general_six_half='OPEN')
write('freeze_receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2),flush=True)
