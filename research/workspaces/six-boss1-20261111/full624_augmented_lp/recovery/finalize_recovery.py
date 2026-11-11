"""Freeze certified full624 optimum and the exact dual-wallet interpretation."""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip,json,platform,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
RUN=ROOT.parent
REPO=ROOT.parents[3]
def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=HERE/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

v=read(HERE/'certificate_verification.json')
assert v['status']=='PASS' and v['strictly_higher_optimum'] is True
assert (v['rows'],v['columns'],v['primal_rows_checked'],v['dual_columns_checked'])==(20910,20585,20910,20585)
assert v['minimum_primal_slack']==v['minimum_dual_residual']=='0'
assert sha(HERE/'augmented_lp_exact.json')==v['point_sha256']
assert sha(HERE/'exact_dual_certificate.json')==v['dual_sha256']
assert sha(HERE/'exact_matrix.json.gz')==v['matrix_sha256']
inputs=read(HERE/'recovery_input_manifest.json')
for record in inputs['all_cloud_original_output_sha256']:
    assert sha(REPO/record['path'])==record['sha256'],record['path']
oldfreeze=read(ROOT/'freeze_manifest.json')
assert sha(ROOT/'freeze_manifest.json')==inputs['frozen_local_manifest_sha256']
for record in oldfreeze['assets']:
    assert sha(REPO/record['path'])==record['sha256'],record['path']
receipts={}
for stage,exit_code in [('sameW',1),('freeW',0),('dual',0),('verify',0)]:
    r=read(HERE/('execution_'+stage+'.json'))
    assert r['exit_code']==exit_code and r['optimizer_calls']==0
    assert sha(HERE/r['source_snapshot'])==r['source_sha256']
    assert sha(HERE/(stage+'_stdout.txt'))==r['stdout_sha256']
    assert sha(HERE/(stage+'_stderr.txt'))==r['stderr_sha256']
    receipts[stage]=r
point=read(HERE/'augmented_lp_exact.json');dual=read(HERE/'exact_dual_certificate.json')
primal=read(HERE/'primal_exact_audit.json')
W,W0=F(v['W']),F(v['old_W']);delta=W-W0
assert delta==F(v['exact_increase'])>0
values=[F(c['weight']) for c in point['columns']]
slacks=list(map(F,primal['row_slacks']))
lam={i:F(w) for i,w in dual['row_multipliers']}
with gzip.open(HERE/'exact_matrix.json.gz','rt',encoding='utf-8') as f:matrix=json.load(f)
with gzip.open(RUN/'complete624_transfer/full_lift_bundle.json.gz','rt',encoding='utf-8') as f:bundle=json.load(f)
budget_weights={b['feature_name']:lam.get(b['row_index'],F()) for b in bundle['mapping']['budgets']}
compact_path=RUN/'complete624_transfer/compact_separating_row_exact.json'
rounded_path=RUN/'complete624_transfer/separating_row_exact.json'
assert sha(compact_path)=='faf330a074ff17a8c442d24329ae0a7a946d92c95a944c666f1a40f9e4949d46'
assert sha(rounded_path)=='c6c5896007f5280767f8d04953c2aa34ac8ec9474a059a43fe120e97d1647fc7'
compact=read(compact_path);primitive=compact['primitive_integer_weights']
factor=budget_weights['sourceT']/primitive['sourceT']
assert factor>0
assert all(w==factor*primitive.get(name,0) for name,w in budget_weights.items())
assert set(name for name,w in budget_weights.items() if w)==set(primitive)
projected=[]
for p in (compact_path,rounded_path):
    row=read(p)
    slack=sum((F(w)*values[j] for j,w in row['sparse_original4849_row']),F())
    assert slack>=0
    projected.append({'source':str(p.relative_to(REPO)),'sha256':sha(p),
        'old_point_slack':row['exact_slack'],'new_exact_slack':str(slack),'new_slack_float':float(slack)})
assert F(projected[0]['new_exact_slack'])==0
assert F(projected[1]['new_exact_slack'])>0
olddual=read(RUN/'union_augmented_lp/exact_dual_certificate.json')
oldlam={i:F(w) for i,w in olddual['row_multipliers']}
budget_rows=[]
for b in bundle['mapping']['budgets']:
    i=b['row_index'];w=lam.get(i,F())
    if w:
        assert slacks[i]==0
        budget_rows.append({'row':i,'feature':b['feature_name'],'weight':str(w),'weight_float':float(w),
            'primitive_integer_weight':primitive[b['feature_name']],'exact_primal_slack':'0'})
changes=[{'row':i,'name':matrix['row_names'][i],'old_weight':str(oldlam.get(i,F())),
    'new_weight':str(lam.get(i,F())),'delta':str(lam.get(i,F())-oldlam.get(i,F()))}
    for i in sorted(set(oldlam)|set(j for j in lam if j<19662)) if oldlam.get(i,F())!=lam.get(i,F())]
analysis={'status':'EXACT_CERTIFIED_STRICT_OPTIMUM_INCREASE','W':str(W),'old_W':str(W0),'exact_increase':str(delta),
    'increase_float':float(delta),'positive_dual_old_rows':sum(i<19662 for i in lam),
    'positive_dual_margin_rows':sum(19662<=i<20286 for i in lam),
    'positive_dual_budget_rows':len(budget_rows),'budget_rows':budget_rows,
    'primitive_integer_weights':primitive,'entire624_budget_weight_vector_is_positive_multiple':True,
    'exact_multiplier_of_primitive_integer_vector':str(factor),
    'exact_multiplier_of_normalized_compact_vector':str(factor*compact['normalization_integer_sum']),
    'external_wallet_times_primitive_multiplier':{'u4':str(factor*36170),'u6':str(factor*13970),'K':str(factor*1199)},
    'projected_row_regressions':projected,'old_reverse624_row':19661,
    'old_reverse624_new_slack':str(slacks[19661]),'old_reverse624_new_slack_float':float(slacks[19661]),
    'old_reverse624_new_dual_weight':str(lam.get(19661,F())),
    'old_row_dual_changes':changes,
    'primal_free_original_columns':[[primal['recovery']['support'][i],value] for i,value in primal['recovery']['free_values']],
    'dual_recovery_variables':dual['recovery']['variables'],'dual_recovery_rank':dual['recovery']['rank'],
    'dual_recovery_free_variables':dual['recovery']['free_variables'],
    'zero_histograms_preserved':v['zero_histograms_at_new_point'],
    'source_sha256':sha(Path(__file__)),'argv':[sys.executable,*sys.argv],
    'no_new_mathematical_scope':'Only actual4/R/family0-off original16hist necessary LP; no full SPE closure.'}
write('optimality_analysis.json',analysis)

source_table='\n'.join(f"| {b['feature']} | {b['primitive_integer_weight']} | {b['row']} |" for b in budget_rows)
free_table='\n'.join(f'| {j} | `{value}` |' for j,value in analysis['primal_free_original_columns'])
stages='\n'.join(f"| {s} | {r['exit_code']} | {r['elapsed_seconds']:.3f} |" for s,r in receipts.items())
hashnames=('exact_matrix.json.gz','floating_solver_arrays.npz','augmented_lp_exact.json',
    'exact_dual_certificate.json','certificate_verification.json','primal_exact_audit.json','optimality_analysis.json')
hash_table='\n'.join(f'| `recovery/{name}` | `{sha(HERE/name)}` |' for name in hashnames)
report=f'''# 完整624增广：云发现后的精确最优值与独立核验

状态：**已认证完成，冻结释放。** 完整 `actual4/R/family0-off` 共同隐藏系统确实把19662行基线的有限必要LP最优值严格提高。结论覆盖完整20910行、20585列，所有原16hist、零质量hist、4992隐藏列及10744旧aux均保留。原六人共同有限非空目录、单位客户、全部有序历史纯SPE的half义务仍 **OPEN**。

本恢复正文是此前本地超时交接正文的结果续篇。旧 `full624_augmented_lp.md` 及其freeze35资产全部保持原字节；本次全部新文件位于 `full624_augmented_lp/recovery/` 与本文件。此前的完整矩阵没有再增删行列，没有混入D提升或客户层结构。

## 1. 精确最优值

归一 `O=1` 下，完整624增广LP的精确最优值是

`W* = {W}`，约 **{float(W):.17g}**。

与原19662行精确最优值的差为

`Δ = {delta}`，约 **{float(delta):.17g} > 0**。

这个严格正差值由完整有理原始/对偶证书匹配证明，不依赖浮点tol，也不依赖某个旧点不可提升或同W活动面恢复失败。

同时 `1−2W* = {1-2*W}`，约 `{float(1-2*W):.17g}`，仍严格为正。这是有限必要条件LP的结果；低于half的点未补齐共同菜单及全历史SPE一致性，不构成原题反例。

## 2. 精确证书为什么排除整个旧最优面

完整原始点 `recovery/augmented_lp_exact.json` 在全部20585列上非负，满足 `O=1` 与全部20910行，最小行余量精确为0。新点有343个正原坐标、2288个正旧aux、85个正隐藏坐标；其余坐标均明确写为0，未删结构。仍有6个零质量hist。

完整对偶 `recovery/exact_dual_certificate.json` 给出

`objective = W* · normalization + Σ_i λ_i · row_i + residual`，其中全部 `λ_i ≥ 0`，20585个residual逐项非负。

对偶归一乘子与原始目标精确相同，所有行/列互补项精确为0。故每个增广LP可行点的目标都至少为W*，原始点又达到W*。因为W*−W0严格为正，整个旧W0最优面均被新必要系统排除。

531个严格正对偶权分为262条旧行、253条正/反边缘行、16条原始预算行。对偶恢复有532个未知、秩532、无自由变量。原旧对偶零扩展仍被独立复核，它继续给出旧下界，但本次以新对偶证明更高下界。

## 3. 与先前紧整数分离方向的精确关系

新增624预算的整个对偶权向量，逐项恰为先前紧整数16项向量的正比例倍数。比例精确为

`c = {factor}`。

因此预算外部钱包为 `c · (36170u4 + 13970u6 + 1199K)`。所有624预算都参加比例核验，未列预算权为0。

| 原始预算特征 | 紧整数权 | 增广行号 |
|---|---:|---:|
{source_table}

先前紧整数投影行在新点**精确取零**；此前第二条有理近似投影行的新点余量精确为 `{projected[1]['new_exact_slack']}`，约 `{projected[1]['new_slack_float']:.17g} > 0`。旧reverse624行19661的新点余量为 `{slacks[19661]}`，约 `{float(slacks[19661]):.17g}`，其新对偶权为 `{lam.get(19661,F())}`。

这里记录的是精确对偶方向、余量与活动性，不把零对偶权当作全局冗余，也不据此额外宣称单一投影行与完整提升在所有点上等价。所有精确权、旧行对偶变化和回归值保存在 `recovery/optimality_analysis.json`。

## 4. 从云原始数组到精确证书的实际过程

Main取回并核验的云运行是 run **43082081632**、job **130737029504**、artifact **13883693740**，提交 `1ccc0a5a5aaeb68a7b8b74297f0482ca668ba7b6`。下载ZIP SHA是 `d33e30c7bdfef2330a9532a4862467f0d065897c91d64a4261195c71a5c79cd5`。本次再次核全部26输入SHA、19输出SHA及旧freeze35资产；12个所需文件逐字复制到全新的recovery目录。原云数组、输入、日志、progress均未修改。

云端唯一 `highs-ds` 发现用时24.128509秒、49106迭代，浮点目标0.4930486396083479；Python3.12.16、NumPy2.3.5、SciPy1.17.0。此前本地170秒IPM超时及真实退出1继续保留。本恢复阶段 **0次浮点优化**，只使用同一云数组。

第一次sameW精确恢复使用428未知与736条选定方程。前735条活动/归一方程一致，最后固定旧W0的方程产生精确不一致，退出1。完整方程、支持、失败traceback和stdout/stderr均保留。这个失败本身不证明旧W0整体不可达。

随后freeW恢复去掉最后的旧目标等式，在同一支持上得到秩421、7个自由参数的精确点，并重算全部7954个canonical max与2790个canonical min辅助量，再精确检查所有完整行。对偶恢复在同一数组选择支持后按精确原始互补性裁剪，逐列消元得到满秩证书，最后检查全部20585个残差。没有进行任何新数值求解或数值修复。

采用的七个自由原始坐标如下；它们仅用于挑选可行的精确原始点，W*由活动方程固定：

| 原始列 | 精确自由值 |
|---:|---|
{free_table}

实际执行命令均由仓库根启动：

```sh
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/recovery/run_recovery_stage.py sameW
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/recovery/run_recovery_stage.py freeW
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/recovery/run_recovery_stage.py dual
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/recovery/run_recovery_stage.py verify
```

每次driver均保存真实子进程argv、实际执行源及依赖SHA、源码快照、UTC时间、环境设置、Python3.12.14、stdout/stderr、退出码。具体步骤为：

| 步骤 | 真实退出码 | 子进程秒数 |
|---|---:|---:|
{stages}

## 5. 独立全行全列核验

实际执行的是冻结的标准库 `verify_certificates.py`，不导入装配、恢复、浮点优化或同行特征模块。它独立检查完整输入/结构、所有20910行的有理余量、20585列的原始非负性与对偶残差、归一和目标、互补性、支持/自由参数、全部选定精确恢复方程、执行记录。

核验还从原描述符重建312符号边缘和624预算的原坐标系数，对完整新块逐项匹配SHA绑定的通用bundle，保留16hist、全部4992隐藏变量、10744旧aux和四条恒零middle预算，确认固定点rhs替换数为0。全部1248新增行中649条余量为0、599条严格为正。

独立核验状态 **PASS**。运行15.568602秒，内部核验15.054499秒。全部核心证书均可由有理数重新计算，不需信任solver状态或浮点容差。

## 6. 冻结入口与接续边界

| 产物 | SHA256 |
|---|---|
{hash_table}

`recovery/freeze_manifest.json` 给出本阶段完整资产清单、精确结论、输入绑定和真实执行记录。旧本地超时freeze与云原始19文件保持不变。后续分离可使用新点 `recovery/augmented_lp_exact.json`，并继续保留本轮完整20910行/20585列；原题全历史纯SPE half义务仍OPEN。本具体有限LP义务已完成，可释放。
'''
report_path=ROOT/'recovery_report.md';assert not report_path.exists()
report_path.write_text(report)
manifest={'status':'FROZEN_EXACT_OPTIMUM_CERTIFIED_RELEASED','utc':datetime.now(timezone.utc).isoformat(),
    'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),
    'source_sha256':sha(Path(__file__)),'scope':v['scope'],
    'result':{'W':str(W),'old_W':str(W0),'exact_increase':str(delta),'increase_float':float(delta),
        'strictly_higher_optimum':True,'primal_rows':20910,'dual_columns':20585,'below_half':True,
        'independent_verification':'PASS','recovery_optimizer_calls':0,
        'sameW_recovery_failed_and_retained':True,'general_six_half':'OPEN'},
    'original_local_manifest_sha256':sha(ROOT/'freeze_manifest.json'),
    'original_local_assets_unchanged':35,'original_cloud_outputs_unchanged':19,
    'actual_recovery_receipts':receipts,'assets':[]}
exclude={'freeze_manifest.json','finalize_stdout.txt','finalize_stderr.txt'}
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name not in exclude:
        manifest['assets'].append({'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size})
manifest['assets'].append({'path':str(report_path.relative_to(REPO)),'sha256':sha(report_path),'bytes':report_path.stat().st_size})
write('freeze_manifest.json',manifest)
print(json.dumps({'status':manifest['status'],'W':str(W),'exact_increase':str(delta),
    'point_sha256':sha(HERE/'augmented_lp_exact.json'),'dual_sha256':sha(HERE/'exact_dual_certificate.json'),
    'verification_sha256':sha(HERE/'certificate_verification.json'),
    'optimality_analysis_sha256':sha(HERE/'optimality_analysis.json'),
    'report_sha256':sha(report_path),'freeze_manifest_sha256':sha(HERE/'freeze_manifest.json'),
    'assets':len(manifest['assets']),'original35_and_cloud19_unchanged':True},ensure_ascii=False,indent=2))
