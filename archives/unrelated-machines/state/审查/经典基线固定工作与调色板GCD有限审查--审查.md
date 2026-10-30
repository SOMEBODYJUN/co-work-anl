---
id: "unrelated-machines/classical-baseline-work-gcd-finite-review-20261030"
kind: "review"
type_tag: "审查"
title: "经典基线、固定工作不变量与调色板 GCD 有限审查"
status: "finite-audits-classified"
truth_status: "exact-fraction-source-read-with-explicit-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
source_refs:
  - "source:10e5aa2e18c0425894f0:evidence/runs/unrelated_machines/classical_baseline_audit.json"
  - "source:69ee0bf3ef1f323dad3d:evidence/runs/unrelated_machines/identical_work_invariant_audit.json"
  - "source:8e850e2f9cc0ce939add:evidence/runs/unrelated_machines/finite_palette_gcd_barrier_audit.json"
evidence_manifest: "../../tools/evidence/classical-baseline-work-gcd-20261030/source-manifest.json"
---

# 1. 本批对象和阅读口径

本批逐字读取三份 `clean show` 导出的冻结 JSON，并将原字节、来源 ID、SHA-256 和逐源证据保存到 `tools/evidence/classical-baseline-work-gcd-20261030/`。三源都使用 `fractions.Fraction` 或精确整数；它们的模型、量词和证据层级不同，不能合并成一个 unrelated-machines 定理。

- `10e5aa2e18c0425894f0` 是 classical baseline 的有限矩阵/Oracle/压缩 DP 审计。
- `69ee0bf3ef1f323dad3d` 是固定总工作量的 identical-machine 族不变量和局部势审计。
- `8e850e2f9cc0ce939add` 是十个小矩阵上的有限调色板 GCD、共同分母和端点算术审计。

本批的共同处置等级是“有限精确证据”：程序字段与 `passed`/`status` 只说明该运行输出的内部声明，不能替代一般量词、一般 LP 可行性或调度构造证明。

# 2. 经典基线：矩阵、展开缺口与压缩族

## 2.1 定义域和实际运行规模

来源声明 `schema_version=1`、Python 3.12.14、`arithmetic=fractions.Fraction, exact; no floating point solver`，随机种子为 20261016，原始输入 SHA-256 为 `5ba0dc52...cbd75a`。实际检查计数为：`matrix_cases=3375`、`oracle_assignments=13824`、`rational_cases=150`、`invalid_cases=6`。这些是冻结运行的有限输入集合；没有给出任意机器数、作业数或任意处理时间矩阵的量词。

toy 字段只重算一个小例：OPT=3、指定坏分配 makespan=5、比值 5/3，枚举 2187 个 assignment。来源自己明确写明“仅检查 OPT 和坏调度；不声称重现某本教材的 matching”。因此该 5/3 是该 toy 的有限见证，不是经典算法下界或文献复现结论。

## 2.2 展开 gap 案例

三项 `expanded_gap_cases` 的数据为：

| k | height | root alpha | OPT | certified LP upper | gap lower bound | machines/jobs | 独立枚举 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | 3/2 | 3/2 | 1 | 4/5 | 32 assignments，independent OPT=3/2 |
| 3 | 1 | 1/2 | 5/3 | 4/3 | 5/4 | 4/7 | 128 assignments，independent OPT=5/3 |
| 4 | 3 | 16/27 | 7/4 | 5/4 | 7/5 | 74/169 | 未给独立全分配计数 |

“certified LP upper”与“gap lower bound”在 k=3、4 上并不相等；它们只能按来源各自语义记录，不能把 `gap lower bound` 当成已证的 LP 整数间隙，也不能把有限 DP 当成一般求解器。k=4 的 7/5 与已有 `配置剥离与联合匹配有限审计` 中的 bundle-subdivision 边界相邻：后者已指出朴素 subdivision 会把目标抬高，本批不能删除该障碍或声称保值。

## 2.3 压缩 gap 家族

四项 `compressed_gap_cases` 给出显式对称 VW 树族的有限参数表：

| k | height | root alpha | OPT | certified LP upper | gap lower bound |
|---:|---:|---:|---:|---:|---:|
| 5 | 5 | 625/1024 | 9/5 | 6/5 | 3/2 |
| 8 | 11 | 1073741824/1977326743 | 15/8 | 9/8 | 5/3 |
| 16 | 33 | 340282366920938463463374607431768211456 / 647159824910983792506158351898193359375 | 31/16 | 17/16 | 31/17 |
| 32 | 88 | （完整有理数保存在原 JSON） | 63/32 | 33/32 | 21/11 |

这些项目只对“明确的对称 VW tree family”运行压缩 DP；来源明确说大 k 的 full graph 未 materialize。故可复用内容是该家族的有限参数/端点算术，不能升级成一般配置 LP、通用精确算法、统一近似比或 hardness。

## 2.4 失败机制和用途

来源的限制字段列出四个边界：有限检查不是普适证明或 novelty certificate；没有 generic LP solver，rounding 接收的是已经可行的 x；compressed DP 只适用于显式对称 VW tree；大 k 未展开。对后续研究，k=3 的“LP upper=4/3 而实际 OPT=5/3”是应保留的目标错位提醒；k=4 及压缩族是配置/整数 gap 的候选边界资料。它们不能直接移入 CAG 六人目录覆盖模型。

# 3. 固定工作量 identical-machine 族

## 3.1 量词和模型

来源 `status=passed`、`arithmetic=Fraction`、`randomness=none`，并引用 `rounding_and_gap.py`、`cyclic_batch_repair.py` 和 `optimal_convex_fixed_slot_gap.md` 的 SHA。它检查的是一个预先指定的 identical-machine fixed-work family：总工作量固定，机器数与作业规模按 m 的显式案例增长；不是任意 unrelated-machines 输入。来源明确说 arbitrary-m identity 在数学说明中证明，而 family/convex decomposition 沿用既有 Boss7 材料，不能当成本批新证。

## 3.2 七个案例的精确输出

| m | n | 初始 makespan | true OPT | 总工作量 | 独立 assignments | same-work checks | 坐标不增且负载相等的 assignments | 一步移动 makespan |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 4 | 4/3 | 1 | 2 | 16 | 16 | 3 | 1 |
| 3 | 9 | 3/2 | 1 | 3 | 19683 | 19683 | 560 | 5/4 |
| 4 | 16 | 8/5 | 1 | 4 | 0 | 0 | 0 | 7/5 |
| 5 | 25 | 5/3 | 1 | 5 | 0 | 0 | 0 | 3/2 |
| 6 | 36 | 12/7 | 1 | 6 | 0 | 0 | 0 | 11/7 |
| 7 | 49 | 7/4 | 1 | 7 | 0 | 0 | 0 | 13/8 |
| 8 | 64 | 16/9 | 1 | 8 | 0 | 0 | 0 | 5/3 |

这里“0 independent assignments”表示后续规模没有执行全 assignment 穷举，不能误解为没有合法分配。`optimizer_iterations=0` 也不是优化算法的普遍收敛证明；它只是该固定输入输出的字段。

数学用途是保留两个可验证模式：总工作量给出平均负载 1 的基准，初始向量在一跳动作下可有非减坐标/严格上升的二次势；这些数据与已归档的 `固定工作凸局部最小有限审计` 同方向，但本源独有的是 m=2..8 的这组 exact row counts 及依赖 SHA。它不延伸到独立“one-destination fork obstruction”，也不说明配置导出的初始化必有相同性质。

## 3.3 可接续的问题

若要把 arbitrary-m identity 升为正式定理，应在正文中显式写出处理时间、总工作量不变量、可行 move 集合和势函数的量词，并证明每个 m 的初始化确属同一族。若要研究 unrelated-machines，则须另给机器相关处理时间矩阵；不能用 identical-machine 反例替代。若要比较配置 LP，需单独计算 T_conf，当前来源没有该字段。

# 4. 有限调色板 GCD 障碍

## 4.1 对象、量词和运行范围

来源 claim 为 `UM-FINITE-PALETTE-GCD-BARRIER-v1`，命令为 `python3 tests/audits/unrelated_machines/finite_palette_gcd_barrier.py`，代码 SHA-256 为 `aea8a506...17e1`。它对十个小矩阵做 exact Fraction enumeration，检查 GCD/LCM、integral load grid 和 endpoint arithmetic；来源明确“不求解 LST LP，也不是普适证明”。平台为 Linux 6.18.55，Python 3.12.14，种子 20261019。

## 4.2 十个实例的保留数据

| name | B | machines/jobs | all-finite assignments | common denominator bits | g | g/B | opt | rho | grid targets |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| zero_edges_and_infinity | 4 | 3/5 | 72 | 2 | 1/2 | 1/8 | 1 | 15/8 | 2 |
| fixed_palette | 5/2 | 3/6 | 216 | 2 | 1/2 | 1/5 | 2 | 9/5 | 2 |
| coprime_rationals | 19/17 | 2/6 | 16 | 41 | 1/1236789689135 | 1/1382294358445 | 332/221 | 2764588716889/1382294358445 | 3 |
| large_denominator | 7/D | 2/5 | 8 | 333 | 1/D | 1/7 | 8/D | 13/7 | 3 |
| random_0 | 12 | 3/7 | 972 | 11 | 1/1260 | 1/15120 | 14/5 | 30239/15120 | 2 |
| random_1 | 4 | 3/7 | 648 | 11 | 1/1260 | 1/5040 | 61/18 | 10079/5040 | 2 |
| random_2 | 16 | 3/7 | 432 | 9 | 1/360 | 1/5760 | 37/8 | 11519/5760 | 2 |
| random_3 | 10 | 3/7 | 1458 | 10 | 1/840 | 1/8400 | 59/21 | 16799/8400 | 2 |
| random_4 | 14 | 3/7 | 486 | 10 | 1/840 | 1/11760 | 4 | 23519/11760 | 2 |
| random_5 | 17 | 3/7 | 216 | 10 | 1/840 | 1/14280 | 113/42 | 28559/14280 | 2 |

其中 large-denominator 的 (D) 是原 JSON 中展示的 333-bit 大整数；manifest 与原副本保留其完整精确值。十个实例均 `zero_only=false`，即来源没有把这些行简化为只有零边的特例。

## 4.3 数学解释的安全边界

这些结果表明：在所选有限矩阵和网格端点上，最小正 GCD 间隔可非常小，且共同分母位数可达 333；因此任何依赖固定常数调色板、固定小分母或无视 ∞ 边的舍入论证都必须额外证明其输入限制。它们没有证明“任意输入的 GCD 都小”或“任意调度 LP 都有整数网格解”。`rho` 只是该审计定义下的 exact ratio 字段，应按源语义引用，不能改写成 LST 的普遍 integrality gap。

后续若要用此障碍构造一般反例，需要给出：处理时间输入编码、允许的零/∞边、目标 T 的量词、LP 约束、从 Fraction 网格到不可行整数调度的明确归约。当前十行数据只足以作为条件候选和测试集。

# 5. 与已有档案的关系、独有内容和处置

1. 与 `固定过载固定sink与凸局部最小有限审计`：本批的 fixed-work 表与其 m=3/4/5/8/12 family 有交叠主题，但本批独有 m=2..8 行、依赖 SHA 和“初始 makespan / one-move makespan / assignment count”字段；两者合并成“有限固定工作证据”，不互相升级量词。
2. 与 `固定阶向量贪心与q13线性缺口增量审计`、`配置剥离与联合匹配有限审计`：classical baseline 的 k=3/4 gap 和 compressed VW family 可作为有限配置目标边界；它不提供 q=13 向量贪心的 source/order，也不替代 bundle-subdivision 的保值缺口。
3. 与 `私有菜单树有界叶重数配置界`、`单强制根树精确配置间隙`：本批 classical 的对称 VW 压缩族在对象上相邻，但来源没有完整树定义、重数约束或全任务调度证明，因此仅保留有限运行，不并入那两个已声明定理。
4. 与 `C2前缀满载与单位多切片有限审计`、`前缀原子有限精度与相对Gram审计`：GCD/共同分母障碍属于同一“有限精确算术”方法层，但机器/任务资格不同，不能移植结论。
5. 与当前 CAG 六人半覆盖问题：三源都没有客户目录、完整历史或纯 SPE 量词，保持 unrelated-machines 独立身份。

逐源处置为：

- `10e5...`：集成到本页第2节，保留 toy、expanded/compressed 表和四项未实现边界；不是重复旧配置定理。
- `69ee...`：集成到本页第3节，保留 m=2..8 的独有行、依赖哈希和未执行的全 assignment 范围；不是一般 invariant 的新证明。
- `8e850...`：集成到本页第4节，保留十实例 GCD/分母/ratio 全字段和 333-bit 极端；不是 LST LP 或 hardness 结论。

# 6. 后续接续清单

- 若继续 classical VW 方向：先补齐 k=4 的实际调度/配置证书量词，再处理 k>4 的 full graph materialization，避免把 compressed DP 误写成一般 solver。
- 若继续 fixed-work 方向：把 arbitrary-m identity 的证明稿完整读入并明确 move/势函数定义，随后才可讨论从有限族到任意 m 的升级。
- 若继续 GCD 方向：构造一个带零边、∞边和大分母的参数族，并把网格障碍翻译成整数调度不可行性或舍入失败的正式命题；单凭十个小矩阵不够。

本批没有关闭任何一般 unrelated-machines 近似、LP 整数性或 hardness 问题；保留的是可复用的精确有限算术与明确缺口。
