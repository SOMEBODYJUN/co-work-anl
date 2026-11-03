---
id: "unrelated-machines/normalized-gated-menu-log-palette-finite-review-20261030"
kind: "review"
type_tag: "审查"
title: "归一化门菜单福利与对数调色板 padding 有限审查"
status: "finite-audits-classified"
truth_status: "exact-fraction-finite-replay-with-explicit-model-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
source_refs:
  - "source:86f59227811df6eaaa43:evidence/runs/unrelated_machines/normalized_gated_menu_welfare_audit.json"
  - "source:076d098cf0e1aba55e87:evidence/runs/unrelated_machines/normalized_gated_menu_welfare_independent_audit.json"
  - "source:ddfaa6d35eddd7d24ab6:evidence/runs/unrelated_machines/logarithmic_palette_padding_equivalence.json"
evidence_manifest: "../../tools/evidence/gated-menu-20261030/source-manifest.json"
---

# 归一化门菜单福利与对数调色板 padding 有限审查

本页逐字读取三份冻结 `clean show` 导出，并将原字节复制到 [证据目录](../../tools/evidence/gated-menu-20261030/)。三源都使用精确整数或 `Fraction` 字段，但它们描述的对象不同：前两源是同一归一化 gated-menu 福利审计及其独立重放，第三源是对数调色板与 padding 的压缩分类。它们可以共同说明有限算术、舍入和边界测试的证据链，不能合并成一个一般 unrelated-machines 定理，也不能迁移到当前六人 SPE 目录模型。

## 1. 读序、版本和定义域

本批对象在实际认领后通过 `clean show` 完整导出；JSON 原件保存在证据目录，manifest 记录来源 ID、路径、内容 SHA-256、程序/证明 SHA-256 和运行范围。三源中第一、第二源共用代码 SHA `31aeb2b57bbf78e0f980f552bd5985e4f0a15b57f98f93f46be1296a19b156f6`，第三源代码 SHA 为 `6f3b3c11815f82eb51f03ae63e529288898ddd4fab2022656f3af36b1e242391`，证明材料 SHA 为 `1cbb777776fc4047a70e00396b7b12903ac890343ef6d3f0ee15c0d7bf10512b`。

门菜单 JSON 明示 `scope = finite exact arithmetic only`、`production_lp_solver = false`、`source_hardness = false`。因此此处的定义域是 JSON 实际列出的有限组数 (n)、有限资源/坐标数 (m)、有限状态数 (K) 及有限有理菜单矩阵；`menu`、`lambda`、`z`、`x` 等数组都按源的门菜单语义逐项存在，零项、重复项、零 incidence job 仍是合法输入。`welfare`/`welfare_opt`、`beta_opt`、`output_welfare`、`initial_expectation`、`peak` 和 `ratio` 只按源字段含义记录，不把它们替换成另一个模型的社会福利或 makespan 定义。第三源也自己限定为“给定有限矩阵上的 low-load padded schedules 与 active assignments 的完整压缩分类”；没有 materialize 全部 padded matrix，没有实现或执行 B，也没有 hardness claim。

旧档案《裸菜单读后与保值降度及调色板障碍》已将裸 Cartesian menu 的三态/资源度三正规形与三叉树末层 palette tensor 明确分域；本批的 gated menu 和对数 padding 只作新有限证据，不覆盖那份档案的证明范围。`经典基线、固定工作与调色板 GCD 有限审查` 的十个小矩阵也是有限算术警示，可供方法比较，但没有同一输入语义。

## 2. `86f59227811df6eaaa43`：归一化 gated-menu 福利审计

### 2.1 实际运行分层

冻结 JSON 的种子为 20261018，计数为：support cases 36、general cases 72、deliberate optimal nonbasic coin cases 3、brute-force UM cases 12、large-denominator cases 2。摘要还给出 `general_fractional_state_cases = 2`、`general_nontrivial_incidence_cases = 0`、`nontrivial_coin_decisions = 20`，以及有限运行中观察到的最大 `ratio = 153/130`。这组数字是覆盖矩阵的运行计数，不是对任意 (n,m,K) 的量词。

support 族的每行都给出完整 `menu` 和 `lambda`，并同时回报精确 welfare、initial expectation、peak、机器/作业/有限边数、zero-incidence jobs、`beta_hat` 和 active groups。代表性行如下：

| (n,m,K) | welfare | initial expectation | peak | machines/jobs/finite edges | zero-incidence jobs | `beta_hat` |
|---:|---:|---:|---:|---:|---:|---:|
| 1,1,1 | (1) | (1) | (1) | 4 / 4 / 7 | 0 | (3/8) |
| 2,3,2 | (2) | (1727/1000) | (1) | 10 / 17 / 35 | 6 | (3/8) |
| 3,5,3 | (3) | (4065129/1464320) | (1) | 18 / 52 / 109 | 30 | (3/8) |
| 4,4,1 | (4) | (4) | (1) | 13 / 25 / 49 | 12 | （原字段保留） |

这些行可作为 exact Fraction 回归和支持结构的有限见证；不能由 `peak=1` 或 (n) 个例子推出统一 welfare 公式。

### 2.2 一般有限 LP 证书和两条分数态

72 个 `general_cases` 每行均附 `lp_certificate`：变量数、上界行/等式行、精确 primal/dual 向量、objective、正 z 数、分数 z 数、分数 incidence coin 数，并同时枚举有限 allocations。大多数行输出 `output_welfare = welfare_opt`、`ratio = 1`，但两个明确分数态行必须保留为边界而非抹平：

| case 索引 | (n,m,K) | `welfare_opt` | `output_welfare` | `initial_expectation` | peak | ratio | `fractional_z` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 43 | 2,5,3 | (431/255) | (21/13) | (99933/68068) | (18/13) | (153/130) | 4 |
| 67 | 2,3,2 | (12/7) | (5/3) | (809/560) | (4/3) | (28/27) | 4 |

两行都报告 `fractional_incidence_coins = 0`；差别发生在 state-level (z) 的分数性。它们说明：源程序在有限 exact LP certificate 与输出 rounding 之间确实能出现可量化的输出差距；“有 primal-dual certificate”不等于“所有 rounding 输出都达到 certificate objective”。这正是后续若要写一般舍入定理必须补的机制。其余 70 行的有限一致性不能替代此缺口。

### 2.3 非基本 coin、全 UM 穷举、负控制和大分母

三条 deliberate optimal nonbasic coin 行都满足 `output_welfare = welfare_opt = 1`，但初始期望较低、需要明确 coin steps：

| (n,m,K) | 初始期望 | welfare/output | `beta_opt` | coin steps | peak | machines/jobs/edges |
|---:|---:|---:|---:|---:|---:|---:|
| 2,1,1 | (3/4) | (1) | (1/2) | 2 | (3/2) | 6 / 7 / 13 |
| 3,2,1 | (19/27) | (1) | (1/3) | 6 | (5/3) | 9 / 13 / 25 |
| 4,3,1 | (175/256) | (1) | (1/2) | 12 | (7/4) | 12 / 21 / 41 |

12 条 `brute_um_cases` 对有限 UM 资源分配作完整搜索；首三条代表值为 ((eta_{m opt},UM_{m opt})=(1,1),(1/2,3/2),(1,1))，对应 search nodes 5、13、6，且每行均有 `completed_better_schedules` 和 `resource_allocations`。它们证明的是列出的 12 个小实例已经完成搜索，不是通用 UM solver。

`flat_negative_control` 是一个应单独标记的反例机制：两组、每组一个 state、一个资源、所有 private time 为 1 时，flat optimum 为 2（4 个原始 assignments），gated optimum 为 (3/2)（搜索 13 个节点）。因此 gated menu 在该控制实例上可改善 flat 值；这不能被写成所有 gated menus 都改善，也不能反向证明一般近似下界。

两条 large-denominator fixtures 使用分母 (2^{200}+1)（201 位）；第一条 welfare/peak/beta 为 (1,1,1)，nontrivial coin steps 为 0，机器/作业/边为 7/9/18，zero-incidence jobs 为 2；第二条 welfare 为 1、peak (3/2)、beta (1/2)、coin steps 2，机器/作业/边为 6/7/13。它们的用途是压力测试有理数表示和 coin 逻辑，而不是给出随分母位数增长的复杂度结论。

### 2.4 证据分级

- **完整证明：** JSON 中每行的 exact primal-dual 数字、枚举结果和分母均为可复核证据；它们是列出实例的完整证书。
- **条件结论：** 若固定输入确实属于该菜单语义、LP 行和 rounding 前提均满足，则相应行的 welfare/beta/peak 数值可按证书使用。
- **有限实验：** 36 support、72 general、3 coin、12 brute、2 large-denominator 全部属于 finite exact replay。
- **障碍：** 两个 fractional-(z) 行显示输出和 LP objective 的差距；`production_lp_solver=false` 明示没有一般 LP 求解器。
- **候选：** 负控制和大分母可作为以后构造门菜单失败族、分数态舍入压力测试的候选，但当前不是参数族或定理。
- **原模型反例：** flat-versus-gated 的 (2) 对 (3/2) 只属于该控制输入；不能移植到裸 Cartesian、三叉树 palette 或 CAG 模型。

## 3. `076d098cf0e1aba55e87`：独立重放的增量内容

第二源声明 scope 为“Replay of the named frozen data; not a general solver”，代码 SHA 与第一源一致。它独立重算 75 个 semantic primal-dual certificates、113 个带独立 outcome expectation 的 rounding cases、904 次 independent expectation calls 和 113 次 all-jobs load rechecks；另有 12 个完整 UM 实例，完整合法 schedule 数量为

\[
8,64,16,256,24,576,96,9216,8,64,16,256,
\]

总和 10600。故它不是简单重复第一源的摘要，而是把证书、期望、逐作业负载和完整 schedule 的重算分开计数。负控制再次得到 flat optimum 2、4 个 flat assignments、gated optimum (3/2)、64 个 gated assignments；两条大分母 fixture 也被重放。

最有用的独有字段是 `existing_output_rejected_exit = 2` 与 `existing_output_sha256_unchanged = 2b40b0bc6e3b11a3bf1a3b6f678873873d0a12ec6d29e404cbfd8f41b30ebe86`：独立程序拒绝已有输出后，确认第一份冻结输出字节未被覆盖。这支持证据保全和重放独立性，但不增加一般量词。其处置为与第一源**集成**为同一 gated-menu 证据链，保留其独立计数和拒绝/哈希检查，不把两份 JSON 当作两个不同数学模型。

## 4. `ddfaa6d35eddd7d24ab6`：对数调色板与 padding 压缩分类

### 4.1 对象和有限分类

第三源 `status=passed`、`arithmetic=fractions.Fraction and exact integers`、seed 20261019。运行计数为：empty original case 1、palette H values 130、scalar boundary probes 2481、matrix-k pairs 1574、exact-zero branches 184、threshold-grid points 9038、good thresholds 1390、active assignment patterns 10890、retained active patterns 3762、every qualifying output pattern 2993、complete private-block classifications 1390、sentinel active patterns 7128、earlier candidate sentinel patterns 3666、fixed-k ratio-and-padding identities 999。

这些名称应按程序定义理解：它是对给定有限 H、threshold、matrix-k 和 padded schedule 的压缩枚举，保留 active assignment pattern、private-block 分类和 exact-zero 分支；不是把“universal_bound”自动提升成任意 H 的普适上界。代表性 palette 行为：

| H | distinct | `universal_bound` | `grid_exponents` |
|---:|---:|---:|---:|
| 2 | 2 | 3 | 0 |
| 4 | 3 | 4 | 1 |
| 16 | 3 | 10 | 7 |
| 64 | 4 | 34 | 31 |
| 128 | 8 | 66 | 63 |
| 257 | 36 | 130 | 127 |
| 513 | 100 | 258 | 255 |
| 1025 | 266 | 514 | 511 |

### 4.2 padding 样例和边界

padding 样例明确给出 `original_n`、固定 (k)、`N_is_2_to_power`、`actual_H`、palette distinct/bound、active grid length 和 sentinel bitlength：

| original_n | fixed_k | (N) | actual_H | palette distinct/bound | active grid length | sentinel bitlength |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 256 | 257 | 36 / 130 | 47 | 513 |
| 2 | 2 | 320 | 321 | 52 / 162 | 59 | 641 |
| 5 | 2 | 448 | 449 | 84 / 226 | 74 | 897 |
| 5 | 3 | 1344 | 1345 | 384 / 674 | 119 | 2689 |

这些样例保留了 padding 对 H、palette 和 sentinel 大小的精确关系；它们没有把 sentinel bitlength 解释成调度复杂度，也没有证明任意 (n,k) 的对数界。空原始实例明确存在，不能在后续写作中悄然加入“原实例非空”假设。

### 4.3 分类级证据和缺口

- **完整有限分类：** 对源列出的 130 个 H、9038 个 threshold-grid points 和 1574 个 matrix-k pairs，active assignments 与 private blocks 被程序枚举并以 exact integer/Fraction 统计。
- **条件结论：** 在给定矩阵和 low-load/padding 前提下，某个 `good_threshold`、`retained_active_pattern` 或 fixed-k identity 可按源输出复查。
- **候选：** 999 个 fixed-k ratio-and-padding identities、130 个 H 样例和四条 padding 行是构造参数族或证明对数边界的候选数据。
- **障碍：** scope 明确写出“no full padded matrix materialized, no B implemented or executed, no hardness claim”。因此没有完整矩阵级算法、B 的正确性或复杂度结论。
- **原模型反例：** 当前 JSON 没有一个可直接命名为一般调度反例的字段；若后续将某个 sentinel/threshold 失败模式写成反例，必须再给出完整输入、量词和不可行性证明。

## 5. 与既有档案的比较

1. 《裸菜单读后与保值降度及调色板障碍》处理的是裸 Cartesian menu 的真实选择树/路径降度合同，以及另一种完整三叉树末层至多两色的 palette tensor。它已证明这两个旧模型的失败机制不同。本批 gated-menu 福利审计使用自己的 `menu/lambda/z/x` 有限语义，不能把 (2) 对 (3/2) 控制数值或两个 fractional-(z) 行移入三叉树矩阵；同样，第三源的 padding H 也不能被当作旧 palette tensor 的高度。
2. 《经典基线、固定工作与调色板 GCD 有限审查》展示过大分母与 GCD 细网格的有限算术障碍。本批第一源的 (2^{200}+1) 分母和第三源的 sentinel bitlength 与之相邻，但处理对象和证书字段不同；不能把它们合成“所有调色板都有共同分母障碍”。
3. 其它 `配置剥离与联合匹配`、`固定过载固定sink` 等档案含有配置/负载的有限审计；本批没有读取出新的通用 LP、EPTAS、近似比或 hardness 证明，故保持 unrelated-machines 独立身份，也不并入六人 SPE 目录覆盖问题。

## 6. 逐源处置与后续接续

- `86f59227811df6eaaa43`：**integrated**。其 36/72/3/12/2 分层、两个 fractional-(z) 行、负控制和两条大分母 fixture 已写入本页，原 JSON 复制到证据目录。后续若要声称一般 gated-menu rounding，必须先解释索引 43/67 的输出缺口。
- `076d098cf0e1aba55e87`：**integrated**。其 75/113/904/113/12/10600 的独立重放、负控制、旧输出拒绝和 SHA 未变字段已写入本页；它是第一源的独立审计证据，不是第二个模型。
- `ddfaa6d35eddd7d24ab6`：**retained**。其 130 个 H、9038 个网格点、10890/3762/2993 个 pattern 计数和四条 padding 行作为独立的有限候选/障碍资料保留；由于没有 full padded matrix、B 或 hardness，暂不并入任何一般调色板定理。

本页没有关闭任何开放的 gated-menu 舍入、一般 LP 求解、对数 padding 等价性或调色板 hardness 问题。可接续工作是：(i) 对两个 fractional-(z) 实例给出 rounding 失败/成功的完整调度和量词；(ii) 从第三源的 fixed-k identities 中抽取一个明确参数族，先 materialize 小矩阵再证明递推；(iii) 若需要将 palette padding 与旧三叉树模型连接，另写转换并逐任务核验，不能只凭同名的 H、palette 或 sentinel 字段。
