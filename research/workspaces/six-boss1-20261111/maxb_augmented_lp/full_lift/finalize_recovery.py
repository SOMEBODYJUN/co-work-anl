"""Freeze the two exact optimum certificates and their complete provenance."""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
REPO = WORK.parents[2]
R = HERE / 'recovery'
C = HERE / 'compact_projection'


def read(path): return json.loads(path.read_text())


def sha(path): return sha256(path.read_bytes()).hexdigest()


def main():
    verify = read(R / 'certificate_verification.json')
    compact_verify = read(C / 'certificate_verification.json')
    assert verify['status'] == compact_verify['status'] == 'EXACT_OPTIMUM_VERIFIED'
    assert verify['W'] == compact_verify['W']
    for record in read(HERE / 'actions_request.json')['required_inputs']:
        assert sha(REPO / record['path']) == record['sha256']
    prior = read(HERE / 'prior_single_cut_stage_manifest.json')
    for record in prior['assets']:
        assert sha(HERE.parent / record['path']) == record['sha256']
    old_face_manifest = read(HERE / 'old_optimum_face/manifest.json')
    for record in old_face_manifest['assets']:
        assert sha(HERE / 'old_optimum_face' / record['name']) == record['sha256']
    discovery = HERE / 'actions_discovery'
    for record in read(discovery / 'output_manifest.json')['files']:
        assert sha(discovery / record['name']) == record['sha256']
    assert sha(discovery / 'floating_solver_arrays.npz') == sha(R / 'floating_solver_arrays.npz') == 'b7de225dc0f6bd19efe0c9000d915f9cbf5d360ea0c7531c0ac869bce84eaf3e'
    analysis = read(R / 'optimality_analysis.json'); activity = read(R / 'new_row_activity.json')
    point = read(R / 'augmented_lp_exact.json'); primal_audit = read(R / 'primal_exact_audit.json')
    dual = read(R / 'exact_dual_certificate.json'); strict = read(HERE / 'old_optimum_face/strict_lower_bound_derivation.json')
    numerical = read(discovery / 'numerical_result.json')
    executions = {name: read(R / ('execution_' + name + '.json')) for name in ('freeW', 'dual', 'verify')}
    assert all(record['exit_code'] == 0 for record in executions.values())
    assert not (R / 'execution_sameW.json').exists()
    w = F(verify['W']); old_w = F(analysis['old_W']); low = F(strict['new_lower'])
    assert w > low > old_w and 1 - 2 * w > 0
    gamma = F(activity['gamma'])
    families = activity['family_counts']
    family_table = '\n'.join(f"| `{name}` | {d['rows']} | {d['tight']} | {d['strict']} | {d['positive_dual_rows']} |" for name, d in families.items())
    weight_table = '\n'.join(f"| {r['row']} | `{json.dumps(r['name'], ensure_ascii=False, separators=(',', ':'))}` | `{r['weight_divided_by_gamma']}` |" for r in sorted(activity['positive_new_dual_rows'], key=lambda x: x['row']))
    x_table = []
    for h in analysis['common_X_histogram_masses']:
        if F(h['X_mass']):
            bits = point['columns'][h['hist_column']]['actual_bits']
            x_table.append(f"| {h['hist_column']} | `{bits}` | {float(F(h['hist_mass'])):.12f} | {float(F(h['X_mass'])):.12f} | {'等于hist' if h['X_full_hist'] else '严格部分'} |")
    free_table = '\n'.join(f"| {primal_audit['recovery']['support'][j]} | `{value}` |" for j, value in primal_audit['recovery']['free_values'])
    artifacts = [
        (HERE / 'exact_matrix.json.gz', '完整X精确矩阵'),
        (R / 'floating_solver_arrays.npz', '不可变原始发现数组'),
        (R / 'augmented_lp_exact.json', '完整X精确原始点'),
        (R / 'exact_dual_certificate.json', '完整X精确对偶'),
        (R / 'certificate_verification.json', '完整X独立核验'),
        (R / 'optimality_analysis.json', '目标与对偶投影分析'),
        (R / 'new_row_activity.json', '全部新增行活动/权数'),
        (C / 'augmented_lp_exact.json', '单cut投影原始点'),
        (C / 'exact_dual_certificate.json', '单cut投影对偶'),
        (C / 'certificate_verification.json', '单cut独立核验'),
    ]
    hash_table = '\n'.join(f"| {label} | `{p.relative_to(HERE)}` | `{sha(p)}` |" for p, label in artifacts)
    report = f'''# 完整共同 X 及单投影行的精确最优：已认证完成

状态：**本有限LP义务精确完成，冻结释放。** 完整共同X提升22297×21021已有匹配的有理原始/对偶；原先准备的20911×20585单compactcut系统也由精确投影得到同一最优值。全程只有一次Actions数值求解，未另跑单cut LP，精确恢复0次优化。原六人共同有限非空目录、单位客户、全部有序历史纯SPE的 `2W≥OPT6` 义务仍 **OPEN**。

本正文接续已冻结的 `report.md` 与上层单行准备正文，不改其字节。它同时接回 `old_optimum_face/report.md` 的整旧最优面排除与严格下界，给出完整最优性闭合；后续加强420个虚拟overlap为真实共同交叠属于另一个系统，不在本次证书范围内。

## 1. 两个系统的精确最优值

归一 `O=1`，精确值为

`W* = {verify['W']}`，约 **{float(w):.16f}**。

| 系统 | 行数 | 列数 | 精确最优 |
|---|---:|---:|---|
| 冻结20910基线＋一条17项compactcut | 20911 | 20585 | 同一W* |
| 冻结20910基线＋完整1387行/436列共同X提升 | 22297 | 21021 | 同一W* |

相对旧第九精确值 `W9≈{float(old_w):.16f}`，提高约 **{float(w-old_w):.16g}**。完整精确差为

`Δ = {str(w-old_w)}`。

但 `1−2W* = {str(1-2*w)}`，约 **{float(1-2*w):.16g}>0**。这是固定16hist必要LP中的精确可行值；并无完整共同客户律、有限目录和全历史策略证书，故不是原题SPE反例。

## 2. 原始/对偶为何证明完整最优

完整原始向量写出全部21021列，逐项非负，`O=1`，全部22297行余量非负、最小精确为0。2898个正列分为348个正原坐标、2337个正旧aux、86个正共享624隐藏坐标、6个正X质量、121个正新min。原16hist和所有零质量hist均未删；新点仍有列1、59、366、449、524、574这六个零hist。

完整对偶给出

`objective = W*·normalization + Σ λ_i·row_i + residual`，

其中463个列出的行权严格正，所有21021个residual非负。每条行互补项及每列互补项精确为0，归一乘子恰等原始目标W*。弱对偶给所有可行点目标至少W*，而原始点达到，故精确最优成立。

独立标准库 verifier 不导入装配、恢复、数值库或max-B构造器。它再次逐字面重建1387新增行/87264系数、核全部旧20910行与20585旧描述符保持、全新436描述符与完整Farkas投影；再核全部22297原始余量和21021对偶残差、原始/对偶非负、归一、目标、互补、所有选定恢复方程以及11164个规范辅助量。状态 **EXACT_OPTIMUM_VERIFIED**。

## 3. 新共同X行的活动性与正对偶权

全部新增行活动性如下。紧是有理余量等于0，不使用浮点tol：

| 新行族 | 总行数 | 紧行 | 严格松行 | 正对偶行 |
|---|---:|---:|---:|---:|
{family_table}

17条 `maximum-B` 全部严格松，最小余量约0.006922901445238134；其对偶权都为0。这是本最优点与本证书的活动性事实，不证明这些行在整个系统中冗余。

两个紧 `X-caps-query` 恰是A6查询与C轨道；唯一紧SAFE是实际第六位查询X；容量 `K−Σx_h` 紧。共同RC仅轨道142 `(B1,C1)` 和170 `(C1,B1)` 紧，只有142正对偶；它们是对称势的两个有序轨道。`X≤hist` 紧行对应hist列1、59、250、366、449、499、524、574，其中正权在59、250、366、449、499。

把全部新正对偶权除以共同正因子

`γ = {str(gamma)}`，约 `{float(gamma):.16g}`，得到很小的精确权数：

| 完整行号（从0起） | 行名 | 权/γ |
|---:|---|---:|
{weight_table}

共有451个旧正行和12个新正行。两条正权overlap上界分别是 `y20721≤x175`（hist175的R/family0/off/000,000）及 `y20751≤x200`（hist200的R/family1/diag/000,000）。全部精确行权、420对上界以及490个RC的余量在 `recovery/new_row_activity.json`，无需从表内小数重建。

## 4. 为何单compactcut与完整提升在本目标下同值

从完整对偶只取新增1387行的非负权，并加全部436个新列的非负residual项，逐列消元得到

`Σ_new λ_i row_i + Σ_new-columns r_j e_j = γ·C`，

其中C就是原17项 K归一compactcut。436新列系数全部精确抵消，15736旧辅助列系数均为零，剩余17系数逐分数恰等γC。这个是通用行向量恒等式，不是固定点上的数值相等。

于是完整对偶立即给单cut系统的合法对偶：保451个旧正行，给追加cut行权γ，保旧20585个非负残差。完整原始点取前20585列也满足单cut系统，C在新点精确为0。两者仍同目标W*，所以单cut的最优性也闭合，共452个正行权。

该投影原始/对偶保存于 `compact_projection/`，用早已冻结的单cut独立verifier再次核全20911行、20585列和10744旧规范辅助量，实际exit0、**EXACT_OPTIMUM_VERIFIED**。没有为单cut调用第二次求解器。

这里只证明两个必要系统对当前目标及归一的最优值相同。没有证明它们的投影可行域相等，也没有把完整X提升或其零对偶行判为全局冗余。

## 5. compactcut取零与此前严格下界的区别

此前 `old_optimum_face/` 给出整个旧W9最优面上的恒等式 `C·x=α<0`。它来自旧531个正对偶行、旧正残差列及O=1，不限制于cb45的正支持，已严格排除整个旧最优面。

再沿该 signed identity 对旧对偶作一次最大保号步长，得到精确下界 `L≈{float(low):.16f}`。它严格高于W9，但只是固定旧对偶方向上的可证下界，没有达到L的原始点。完整发现与恢复把旧行权也重新调整，得到当前更高的W*。

| 数值 | 精确身份 |
|---|---|
| `W9≈{float(old_w):.16f}` | 旧20910系统精确最优 |
| `L≈{float(low):.16f}` | 无优化构造的严格新对偶下界 |
| `W*≈{float(w):.16f}` | 本次完整提升及单cut的精确最优 |

`W*−L≈{float(w-low):.16g}`。新最优点满足C=0，是其原始活动性；新对偶消元恰成γC才进一步认证单cut也达到同最优。这两条依据都不同于此前旧面恒负的 signed identity。

## 6. X质量及规范辅助量的准确含义

新X有六个正hist质量（表内仅显示近似值；完整分数在点和analysis中）：

| hist列 | actual六位 | hist质量 | X质量 | 状态 |
|---:|---|---:|---:|---|
{chr(10).join(x_table)}

它们合计等于K≈0.2403767216318519。新420个overlap均按本必要系统的单调性规范为 `min(X_h,旧查询边缘)`：261个tie、59个X-bound、100个query-bound。原浮点数组有89个正新overlap，规范化后精确点有121个正新overlap；这不改变核心目标，并已核所有完整行。

这420个量仍是虚拟上界，不是实际共同交叠。若后续引入X与R/Z或H1/H2的共同八格、真实own约束或其他含y的负项，必须重新检查该单调性并将相应y纳入核心未知量；不能直接沿用本次420个min的恢复合同。原10744规范辅助量的证明也应按其自身不变行域使用。

## 7. 唯一云发现与真实精确执行记录

实际Actions run **43091082992**、job **130768110298**、artifact **13889091562**，source commit `ef43da7b2a1bdf1bdaa06e302586dc4a3748a13a`，request `C-six-boss1-maxb-full-lift-22297-01`。原始ZIP SHA为 `17eae6d1b6d1c89d33baab3434f772893b213fa56584a75419e0320469b13160`。Main的接收审计在 `compute_dispatch/maxb-full-artifact-audit.json`；本恢复又核运行清单中的5个文件及清单自身共6输入、完整output_manifest和实际源码快照，原始10产物保持原字节。

唯一 `highs-ds` 用时{numerical['solver_seconds']:.6f}秒、{numerical['nit']}迭代，浮点目标{numerical['W_float']:.16f}；Python3.12.16、NumPy2.3.5、SciPy1.17.0。数值最小未缩放行余量约−5.93e−15只作来源记录，不承担证书。

旧值W9已被严格下界排除，因此直接freeW，未尝试sameW。freeW用了440核心未知（348原、86共享624、6X），733去重方程，秩428，12自由原坐标。所有11164辅助量重算后全部完整行精确可行。对偶464未知、742方程，秩464，无自由变量。

| 实际阶段 | 退出码 | 秒数 | 新优化次数 |
|---|---:|---:|---:|
| freeW原始恢复 | 0 | {executions['freeW']['elapsed_seconds']:.6f} | 0 |
| 对偶恢复 | 0 | {executions['dual']['elapsed_seconds']:.6f} | 0 |
| 完整X独立核验 | 0 | {executions['verify']['elapsed_seconds']:.6f} | 0 |
| 单cut独立核验 | 0 | {read(C/'execution_verify.json')['elapsed_seconds']:.6f} | 0 |

12个自由原始坐标仅挑选同活动面的精确原始点；W*由活动方程确定：

| 原始列 | 选定精确自由值 |
|---:|---|
{free_table}

每阶段都保真实argv、源码/依赖SHA、源码快照、stdout/stderr、UTC、Python3.12.14和退出码。本次原始与对偶首次精确恢复均成功，无活动面失败、无数值修复、无数值重跑。上层单行准备中曾有只读NPZ预检的真实中断130记录，随后在冻结前改为一次加载数组；该历史记录保原字节，与本次数值或精确恢复失败无关。

实际恢复命令：

```sh
python3 -B research/workspaces/six-boss1-20261111/maxb_augmented_lp/full_lift/run_recovery_stage.py freeW
python3 -B research/workspaces/six-boss1-20261111/maxb_augmented_lp/full_lift/run_recovery_stage.py dual
python3 -B research/workspaces/six-boss1-20261111/maxb_augmented_lp/full_lift/run_recovery_stage.py verify
python3 -B research/workspaces/six-boss1-20261111/maxb_augmented_lp/verify_certificates.py --output research/workspaces/six-boss1-20261111/maxb_augmented_lp/full_lift/compact_projection
```

## 8. 冻结入口与交付边界

| 产物 | 相对full_lift路径 | SHA256 |
|---|---|---|
{hash_table}

全资产冻结入口为 `recovery/freeze_manifest.json`。它重核六输入、旧单cut24资产、旧最优面严格下界12文件及不可变云产物，列出本阶段源码、输入、完整原始/对偶、独立审计、执行记录与本正文。冻结准备正文、矩阵、原始云数组和旧来源均未修改。

可供接续研究的新点是 `recovery/augmented_lp_exact.json`，完整系统及虚拟辅助语义以本报告和冻结矩阵为准。下一明确扩充应另建新系统与恢复合同；本次有限LP义务完成，不改core、不补入下一阶段行。原模型的完整SPE付款或全历史反例义务继续OPEN。
'''
    report_path = HERE / 'discovery_recovery_report.md'
    assert not report_path.exists(); report_path.write_text(report)
    freeze_path = R / 'freeze_manifest.json'; assert not freeze_path.exists()
    assets = [{'path': str(p.relative_to(REPO)), 'sha256': sha(p), 'bytes': p.stat().st_size}
              for p in sorted(HERE.rglob('*')) if p.is_file() and p != freeze_path]
    freeze = {
        'status': 'EXACT_OPTIMA_VERIFIED_FROZEN_RELEASED', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Full22297/21021 common-X and preserved20911/20585 compactcut fixed16-hist necessary LPs; original six-player SPE half OPEN.',
        'W': str(w), 'W_float': float(w), 'old_W': str(old_w), 'exact_increase': str(w-old_w),
        'strict_half_gap': str(1-2*w), 'only_numerical_solve': {'run': 43091082992, 'job': 130768110298, 'artifact': 13889091562,
            'commit': 'ef43da7b2a1bdf1bdaa06e302586dc4a3748a13a', 'method': 'highs-ds', 'optimizer_calls': 1,
            'arrays_sha256': sha(discovery / 'floating_solver_arrays.npz')},
        'postprocessing_optimizer_calls': 0, 'full_verification_sha256': sha(R / 'certificate_verification.json'),
        'compact_verification_sha256': sha(C / 'certificate_verification.json'),
        'report_path': str(report_path.relative_to(REPO)), 'report_sha256': sha(report_path),
        'preserved_single_cut_assets': prior['assets'], 'assets': assets,
        'subsequent_core_or_constraints_changes_require_new_system_and_canonicalization_review': True}
    freeze_path.write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': freeze['status'], 'W': str(w), 'W_float': float(w), 'assets': len(assets),
                      'report_path': str(report_path.relative_to(REPO)), 'report_sha256': sha(report_path),
                      'freeze_path': str(freeze_path.relative_to(REPO)), 'freeze_sha256': sha(freeze_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
