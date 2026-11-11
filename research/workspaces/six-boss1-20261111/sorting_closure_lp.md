# 全部单查询排序闭包与新早期切面的必要 LP

RUN：`six-boss1-20261111`；实际内部计算代理：`/root/sorting_closure_lp`。

## 任务与严格范围

在第 2 轮的 5764×4849 固定 16hist 必要系统上，稀疏拼接 `tail_constraints/single-query-epigraph.json` 的 8035 行及 7954 个非负辅助变量，并加入 `cross_branch_math/round3_candidate_cuts.json:selected_rows` 的新早期切面；按完整有理系数向量去重。原 4849 列含义与顺序保持不变。

目标是保存实际输入身份、完整浮点结果，并尽可能给出全部行有理可行性与精确对偶界。浮点求解/精确恢复失败不表示不可行。任何本系统的可行点与最优值都只属于该有限必要投影，不是六人共同目录完整历史纯 SPE 见证、游戏反例或全模型福利下界。原题 `2W≥OPT6` 仍 OPEN。

## 初始状态

已实读根 `AGENTS.md`、本 RUN 的 `main.md`、`augmented_lp.md` 与 `tail_constraints.md`，包括其 §5 排序公式和 §10 epigraph 正部完成的证明。当前阶段只写本文件与 `sorting_closure_lp/`；不操作 Git 或共享运行登记。

基准点和矩阵是 `augmented_lp/round2/augmented_lp_exact.json` 与 `augmented_lp/round2/exact_matrix.json.gz`。预期拼接后为 12803 列、13799 条基准加排序闭包行，另加实际去重的新早期行。恢复优先利用稀疏消元及 epigraph 的 canonical 正部结构，避免建立 13k×12k 稠密 Fraction 矩阵。

初始状态为核对输入与恢复脚本；下文记录随后实际完成的求解和精确证书。

## 实际输入与完整拼接

| 输入 | SHA-256 |
| --- | --- |
| `augmented_lp/round2/exact_matrix.json.gz` | `f4cdf6054a52273b4317ef2592d06295002c0e7cf62f757667b4b0f3e52e656d` |
| `augmented_lp/round2/augmented_lp_exact.json` | `2d1468157a11059ddcc95bf63cd3e869595901bfc0475ec2609df4470fd2ca99` |
| `tail_constraints/single-query-epigraph.json` | `964ef22c37f9338a5e29423ff6009611256f5720b5f0b7016bb55940e570a94c` |
| `cross_branch_math/round3_candidate_cuts.json` | `2783ac52153fe336c3cbbf93cb8fa6e1ae732c625d463257586d8a463b8fd96a` |

`sorting_closure_lp/solve_full.py` 核 epigraph 与 cut 包的输入点 SHA 均等于上列第二轮点，原列逐描述符相等，且去 weight 的规范元数据 SHA 与 epigraph 一致。旧点对原 5764 行全部 Fraction 回代通过；epigraph 的每个新变量恰有一个系数为 +1 的阈值行，并只在一个预算中以负系数出现。按阈值直接重算的 canonical 正部完成与输入包保存的 7954 个值逐项相等；旧点确有 12 条负预算。

拼接顺序及零基行号是：

- 0–5763：第二轮的 5764 条原行；
- 5764–13798：全部 8035 条 epigraph 行，没有按输入点正支撑裁域；
- 13799–13852：`selected_rows` 的 54 条切面。

这 54 条记录在第二轮有理点的保存负 slack 均重新 Fraction 计算一致；按完整有理向量查重，它们彼此相异，亦不与已拼接行重复。最终是 **13853 行、12803 列、854194 个非零系数**。所有 7954 新列非负，目标和归一化系数严格为 0。完整精确稀疏矩阵在 `sorting_closure_lp/exact_matrix.json.gz`，原 4849 列前缀不动。

## 浮点发现与有理原始恢复

2026-11-11 16:58:52 UTC 完成稀疏矩阵；HiGHS 随后用约 75.88 秒、56107 次迭代报告 Optimal，浮点 W≈`0.4911650507957936`。先保存完整浮点点与求解器数组，未等待有理恢复。最小缩放行余量约 `−1.414×10^−16`；该数仅作数值诊断，不承载严格可行性结论。

浮点解的原 4849 列有 349 个正坐标，另有 1507 个正辅助坐标。`recover_full.py` 没有对全部 12803 列建立稠密有理方程：先把各辅助按浮点所处正部区间代入预算，并把数值零阈值作为原变量上的活跃等式，形成原正支撑上的 587 个不同非零方程（含 191 个不同零阈值方程）。全稀疏 Fraction 消元得到 rank 349，无自由变量。

恢复出原变量后，每个辅助都重新取精确 `max(0,−原阈值部分)`，而非沿用浮点辅助。随后对全部 13853 行、全部 12803 列非负、归一化 O=1 逐项精确验证，最小余量为 0。原始恢复与输出见 `primal_exact_audit.json`、`augmented_lp_exact.json`。

## 精确最优值与对偶

本轮已认证精确值为

```text
W₃ = 535943112516612323388180134957528955068113928895980836490
     / 1091167035700664643394178459971917560459998093287045039353
   ≈ 0.4911650507957935
```

严格 half 缺口是

```text
1−2W₃ = 19280810667439996617818190056859650323770235495083366373
        / 1091167035700664643394178459971917560459998093287045039353
      > 0.
```

相对第二轮精确最优值严格提高约 `0.00048037493429531347`。完整有理差值已保存在 `result_summary.json` 与 `certificate_verification.json`。

精确对偶恢复使用 129 个正行权和 1 个归一化乘子；从 11905 个数值零约化成本列得到 161 个不同非零方程，稀疏消元 rank 130，无自由参数。最终逐列核验

`objective = W₃ × normalization + Σᵢ λᵢ rowᵢ + residual`

中全部 λᵢ≥0、全部 12803 个 residual≥0，且归一化乘子恰为原始点 W₃。因此 **W₃ 是此次有限必要 LP 的精确最优值**，不只是一个可行点上界。完整证书在 `exact_dual_certificate.json`；恢复全程约 7.75 秒，没有构造 13k×12k 稠密 Fraction 矩阵。

### 排序闭包在本最优点的位置

全部 81 个 canonical 单查询预算都**严格为正**，其最小余量为

```text
895275835882678982318279856018619602857276209562341973921
/ 130940044284079757207301415196630107255199771194445404722360
≈ 0.006837295960740181.
```

对应地，本证书的所有 8035 条 epigraph 行权均为 0。129 个正行权包括第二轮基准行中的 127 条，以及 54 条新行中的以下两条：

| 零基行 | 新早期切面 | 精确对偶权 |
| --- | --- | --- |
| 13803 | `new-theme-requery:0:3:B3:H1:H2` | `187721945044482229702393605459671296804818801771592757064 / 1091167035700664643394178459971917560459998093287045039353` |
| 13813 | `new-theme-requery:0:3:B4:H0:H1` | `144234298353421948566690893671522065417914596014241310976 / 1091167035700664643394178459971917560459998093287045039353` |

两行都取 source seed 0、actual source 零基 3、参数 `(4/7,1/7,1/14,3/28,1/28,2/7)`；具体真实性证明仍归跨分支数学正文。由于上述原始点投影到原 4849 列后满足基准加两行，而对偶也只使用这两个新增行，**基准 5764 行仅加这两行的有限 LP 已有相同最优值 W₃**。这不表示 epigraph 在整个可行域冗余；第二轮点本身已被它的 12 个预算排除。

## 独立文件算术核验与后续接口

已另行执行原 `augmented_lp/verify_certificates.py sorting_closure_lp`，不导入构造器且仅用标准库 Fraction，从保存文件重新计算全部行余量、非负性、O/W 和全部对偶列残差；exit 0，耗时约 6.93 秒。结果为 `certificate_verification.json`。它是独立的保存文件算术核验，不是对全部继承行的第二套数学推导。

| 本轮证据 | SHA-256 |
| --- | --- |
| 完整 `exact_matrix.json.gz` | `42d37c6d255152fcccc74645c1d84cf1feafbfa1af67b9f069db53db406b79a7` |
| 完整 `augmented_lp_exact.json` | `6bfe2ff663803e80aa30b900f609b300617ee6f62f02f898349e2bb4c95a8f07` |
| `exact_dual_certificate.json` | `3af96cced95c9b2d849e18e7d00677ec01a8d2fd1ce02a22fd2953a7d9c99601` |

新浮点与精确点已通知 Main、`tail_constraints`、`cross_branch_math` 和 `common_coupling_math`；后续分离必须从该点重新计算，不能沿用第二轮负 slack。新点全部前 4849 个描述符和原含义不变，其后才是辅助变量。真正 R/Z 四态联合运输与跨边共同 Boolean 一致性仍由各自代理另核，不从单查询的严格余量推断这些更强完成。

复现入口（仓库根；已有结果正常应先核验，避免覆盖）为：

```bash
python3 -B research/workspaces/six-boss1-20261111/sorting_closure_lp/solve_full.py
python3 -B research/workspaces/six-boss1-20261111/sorting_closure_lp/recover_full.py
python3 -B research/workspaces/six-boss1-20261111/augmented_lp/verify_certificates.py research/workspaces/six-boss1-20261111/sorting_closure_lp
```

本轮状态：原始/对偶严格匹配且保存文件独立核验完成。原题 OPEN；该点不是完整 SPE，也不是全模型 half 反例或全模型福利下界。
