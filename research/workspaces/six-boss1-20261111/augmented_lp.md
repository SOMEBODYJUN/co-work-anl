# 5692 行加三包 24 个不同切面的必要 LP 重算

运行：`six-boss1-20261111`；内部计算代理：`/root/augmented_lp`。

## 已完成的数学义务与范围

在原固定 16hist、4849 列的 5692 行必要系统中，加入三包 27 条历史记录对应的 24 个不同有理系数向量，重新最小化归一化福利 W。回答新系统是否仍有严格低于 1/2 的精确可行点，以及新最优值是否严格高于旧点的 W。若新可行点较旧点高，只有额外核验精确对偶下界后才声称严格提高；浮点最优状态和新可行点自身均不足以单独作该断言。

模型仍是六人共同目录完整历史纯 SPE 的必要投影，只固定现有 16 个 hist。任何新可行点不是 SPE 或博弈反例；即使该支持域达到 half，也不证明全模型。

## 已实读与输入身份

已实读根 `AGENTS.md`、`共同目录完整历史模型--定义.md`、`实际末主题分支分离器与四菜单补价原点核验--计算.md`、`同源再查询与容量报价的三份冻结切面包--计算.md`，及原构造器、材料化器和独立切面重建的定义代码。

原点：`archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json`；SHA-256 `46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e`。旧 W 为

`1905769909616898376137238949200623274593168205/3898693540058852735821709960049703833207552519`。

切面输入：`archives/customer-attraction/tools/evidence/requery-capacity-cut-packs-boss3/runs/all-sparse-row-coefficients.json`。27 条记录均仅使用前 1905 坐标，其余 2944 坐标补精确零；按完整有理稀疏向量去重，目标为 24 条。

## 材料化 schema 问题与适配

确实先执行了封包 `b-family-menu-prices-boss3/materialize_runtime.py`，目标为本人子目录的 `augmented_lp/runtime`。基材料化器完成 47 份文件的大小/SHA 校验和复制；外层随即在 `rec['stored_path']` 抛出 `KeyError: 'stored_path'`，退出 1。

当前 `source-manifest.json` 实际是 8 条：使用 `local_original` 或 `local_replay`，目的路径使用 `path` 或 `basename`，与该脚本预期字段不同，也与正文所称覆盖 9 条不一致。本人没有修改封包。局部 `augmented_lp/prepare_runtime.py` 先复核已复制的全部 47 条，再逐条核实际 8 条的 SHA/size，将它们映射至已知 `research_2` 运行路径。适配执行成功，记录见 `augmented_lp/materialization.json`。运行树是完全可重建的中间产物，不需要整树推送。

## 执行过程与恢复入口

`augmented_lp/solve_augmented.py` 已实际执行，stdout/stderr 写在同目录。它调用未经修改的 `B_menu_prices_master.build(all_families=True)`；核原点全部 4849 个非 weight 描述符；调用封包 `audit_cut_packs.independent_row` 的字面后继实现重新构造全部 27 条，并逐系数比对；然后建立 5716 行稀疏矩阵并求 LP。

程序在任何有理恢复前先保存 `augmented_lp_float.json` 和完整求解器数组。之后以原 `exact_solve`、原 `exact_point` 的支持/活跃阈值恢复有理点，省略全零方程但不删除任何待核不等式；全部 5716 行及非负/归一化都用 Fraction 回代。最后恢复精确对偶并逐列核非负剩余系数，以认证有限系统的最优性。实际发生的失败均保存准确 traceback 和浮点候选，不把失败称为严格界。

主要输出包括：`inputs.json`、`cut_records.json`、`old_point_audit.json`、`exact_matrix.json.gz`、`augmented_lp_float.json`、`augmented_lp_exact.json`、`primal_exact_audit.json`、`exact_dual_certificate.json`、`status.json`、`stdout.txt`、`stderr.txt`、`progress.jsonl`。

首轮构造已得到 5692×4849，但描述符比较因 Python tuple 与 JSON list 的序列化差异停止。失败保在 `attempt1_*`。仅将描述符按 JSON 值规范化后，第二轮构造与全部描述符精确通过；未更改任何数学坐标。

第二轮原 5692 行有 402049 非零系数。原点全部 5692 行用 Fraction 回代通过。27 条切面从字面后继实现重建后逐系数相同，去重为 24；它们在原点共有 12 条不同负行，而正文此前只针对 pending 五条单独报告其中两条不同负行。

2026-11-11 16:49 UTC，新 5716×4849 稀疏 LP 求得浮点最优 W≈`0.4900905644294647`，333 正列，HiGHS optimal。完整浮点点及求解器数组先行保存并交给两位数学代理进一步检查。随后对 333 个变量、485 条非平凡活跃方程使用原 `exact_solve`，完成下文的有理原始/对偶认证。

## 5716 行系统的已认证结果

有理原始点已成功恢复，全部 5716 行、4849 列非负、O=1 均精确通过，最小行余量 0，333 个正质量。其精确值为

```text
W = 704411216277628808540143217398883648372637675548323143582131
    / 1437308259745143088183769028895907055958667440445592671664969
  ≈ 0.4900905644294647
```

`1-2W = 28485827189885471103482594098139759213392089348946384500707 / 1437308259745143088183769028895907055958667440445592671664969 > 0`。因此加上三包所有 24 个不同切面后，固定支持域仍有严格低于 half 的必要系统完成。

第一轮对偶恢复仅在 333 个正原始列上立等式，因欠定触发原 `exact_solve` 的满列秩断言。失败原样留在 `status.json`/`stdout.txt`。`recover_dual_free.py` 随后加入全部 3724 个零约化成本列，得到 199 个不同非零方程，156 个变量满秩，无自由变量。155 个行乘子全部非负；对所有 4849 列核

`objective = W * normalization + Σ lambda_i * row_i + residual`

中 `residual >= 0`，且其归一化乘子恰等原始点 W，故 **W 是本 5716 行固定 16hist 必要 LP 的精确最优值**。新最优值与旧 W 的严格正差为

```text
2368208726822657263136593907437574860932023505765513039614863013358905239955597246429906194474316442448
/
1867874809113873642527617744069599342887088301170542734174512517239990441788956793759154897526060413335637
```

完整证书在 `exact_dual_certificate.json`。标准库 `verify_certificates.py` 已另行读压缩矩阵和原始/对偶证书，完全重新计算全部行余量与所有列残差，exit 0；结果在 `certificate_verification.json`，耗时约 3.02 秒。这是对原构造器输出的独立算术核验，不是第二套全矩阵的数学推导。

新增 24 行中，对偶恰使用原 requery 包第 5 条 `(R,orb=(1,0),query=11)` 与第 7 条 `(R,orb=(0,0),query=8)`；它们在完整矩阵零基行 5696、5698。其余新增行有用作可行性约束，但本证书对偶权为零。

## 已接续的第二轮

两位数学代理在上述严格新点重新检查，而未复用旧点 slack：跨枝早期投影给 40 条不同负行，固定已知第一枝的同源机制给 4 条负行，联合运输给 4 条完整域已核负切。`refine_cached.py` 已将这 48 记录逐一核绑定输入 SHA、Fraction 回代负值、完整向量去重，确有 48 个新不同向量，并完成 5764×4849 系统求解。输出在 `augmented_lp/round2/`；父目录 5716 证书保持原身份。该轮仍只固定 16hist 必要系统。

第二轮随后已在约 23.47 秒内完成浮点优化、有理原始恢复与精确对偶。其精确最优值为

```text
W₂ = 420934245428361927618274118225039626351971250244531479574
     / 857850807525882173729363702459520484628961998666766105455
   ≈ 0.49068467586149817
```

`1-2W₂ = 15982316669158318492815466009441231925019498177703146307 / 857850807525882173729363702459520484628961998666766105455 > 0`。

因此两轮都有严格低于 half 的精确最优必要点；第二轮比第一轮严格提高约 `0.0005941114320335`，总计比旧 5692 点提高约 `0.0018619740935286`。这里“最优”严格限于各自保存的有限必要 LP。

第二轮共 337 正列，按 K/hist/joint-reply/overlap/B-family/M-root 为 `1/11/104/135/61/25`。全部 5764 行最小余量 0。对偶有 154 个正行权，3590 个零约化成本坐标给出 192 个不同非零方程，155 个变量满秩，无自由变量。所有 4849 个列残差均非负，最小 0，归一化乘子恰等 W₂。

第二轮新增 48 行中，对偶使用第 5730、5731、5740、5745、5752 行（零基），均来自新主题早期投影；其完整行名和精确权在 `round2/exact_matrix.json.gz` 与 `round2/exact_dual_certificate.json`。4 条固定首枝及 4 条运输切在此份对偶的权为零，这不否定其合法性或它们对第一轮具体点的严格分离，只说明当前有一份不使用它们的最优性证书。

`verify_certificates.py` 已对第二轮另行读文件、用标准库 Fraction 计算全部行和列余量，exit 0，耗时约 3.45 秒；报告 `round2/certificate_verification.json`。没有将本次算术核验称作独立重推 5764 个数学必要行。

### 第二轮输入引用

全部输入在 `round2/inputs.json` 保存实际字节 SHA，且每条导入切在基准精确点的负 slack 均再次精确回代：

- 基准点：`augmented_lp/augmented_lp_exact.json`，SHA `334889b7971e677fb32c9470c9d9bba0d390816def49b5e5088423e3a79cf5fc`。
- 基准矩阵：`augmented_lp/exact_matrix.json.gz`，SHA `f6dddecb5082f38f31b2bb8879a11e01548e84d6087edcb0ef4f1a6ab88effad`。
- `cross_branch_math/new_theme_early_at_5716.json` 的 `selected_rows`：40 条。
- `cross_branch_math/observed_first_at_5716.json` 中严格负的 `rows`：4 条。
- `tail_constraints/augmented5716-transport.json` 的 `families[*].certificate.sparse_original_row`：4 条。

这些相对路径均相对于 `research/workspaces/six-boss1-20261111/`。跨代理切面的真实行推导和完整运输域证明归相应代理正文；本计算层核输入身份、行向量、旧点负值与新增有限 LP 的可行/最优证书。

## 可复用交接入口

本次子代理按 Main 指令在两轮证书完成后停止，没有启动第三轮。后续完整排序 epigraph 增列或新负切由 fresh 计算代理接续同一 RUN。

最新严格点和矩阵的绝对路径是：

```text
/workspace/scratch/b0fef5ec503f/co-work-anl-boss1/research/workspaces/six-boss1-20261111/augmented_lp/round2/augmented_lp_exact.json
/workspace/scratch/b0fef5ec503f/co-work-anl-boss1/research/workspaces/six-boss1-20261111/augmented_lp/round2/exact_matrix.json.gz
```

最新点 SHA `2d1468157a11059ddcc95bf63cd3e869595901bfc0475ec2609df4470fd2ca99`；最新矩阵 SHA `f4cdf6054a52273b4317ef2592d06295002c0e7cf62f757667b4b0f3e52e656d`。同目录有精确对偶、标准库重核报告、全行余量、浮点完整点及 primal/dual/scales 数组；不需再构建原 5692 行稠密矩阵。

- `solve_augmented.py`：从原构造器重建第一轮，独立重建 27 切面，再求 LP 与恢复原始点；首次对偶接口故意保留实际欠定失败历史。最终对偶用下一入口恢复。
- `recover_dual_free.py [结果目录]`：从缓存矩阵和求解器数组恢复全部零约化成本面上的精确对偶，并逐列核验。两轮均满秩，实际没有任取自由参数。
- `recover_dual_free.affine_solve(equations,n,seed)`：可直接复用的稀疏精确阶梯消元；允许欠定时将自由变量选为接近 seed 的有理数，但只有最后全部不等式精确通过才认证。
- `refine_cached.py BASE_DIRECTORY OUTPUT_DIRECTORY EXTRA_JSON ...`：在固定列布局下读取完整精确矩阵，支持 `selected_rows`、带负 slack 的 `rows` 和每 family 主 `certificate` 三种已用切面格式。它要求所有 extra 的 source/input SHA 等于基准精确点的 SHA，不会把旧 slack 当新 slack。当前入口不读取 `additional_single_certificates`，不直接执行 epigraph 增列；新计算代理可复用其稀疏优化和精确恢复内核扩展。
- `verify_certificates.py [结果目录]`：不依赖 NumPy/SciPy 的完整文件算术核验；维数从保存矩阵读取，可用于后续扩展矩阵（需遵守同字段合同）。

复核最新证书的命令（仓库根）：

```bash
python3 -B research/workspaces/six-boss1-20261111/augmented_lp/verify_certificates.py research/workspaces/six-boss1-20261111/augmented_lp/round2
```

重新生成第二轮的完整实际命令保在 `execution_records.json`，参数为基准 `augmented_lp`、一个新的输出目录，以及上述三份 `*_at_5716`/运输 JSON。`refine_cached.py` 拒绝覆盖已存在的结果目录。第一轮和第二轮的运行 stdout/stderr 均保全；`final_manifest.json` 列可保存文件的 SHA/size，明确不列可重建的 `runtime/`。

Main 后来已修复共享材料化器并核验 9 个源文件的原 SHA；未来应使用修复后的正式入口。本文早先 47+8 适配记录仅保存本次实际执行历史，原矩阵已通过完整描述符及旧5692点回代，不是未来必须继续使用的绕行方案。

恢复命令（仓库根）：

```bash
python3 -B research/workspaces/six-boss1-20261111/augmented_lp/solve_augmented.py
```

正常已有运行时不要重复启动；先查 `status.json`/`progress.jsonl` 与活动进程。给后续同源及跨枝代理的优先接口是两个完整 4849 列新点 JSON。
