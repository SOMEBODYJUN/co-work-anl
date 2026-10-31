---
id: bottleneck-knapsack/retired-gap-lane-candidate-boundaries
kind: review
type_tag: 审查
title: 退役 GAP 选题底稿与数学边界
status: retained-provenance-strategy-review; no-new-theorem
truth_status: review-record
review_level: complete-source-read-and-cross-compared
scope: retired topic-selection GAP/packing lane; candidate status, exact local certificates, literature deduplication and stopping obligations
summary: "完整读取 gap.md 的 15 项 GAP/舍入/公平候选与 P01--P11 primary 文献记录，保留其来源级优先级、精确局部证据和去重边界；C01 与两尺寸固定激活障碍已有独立对象，其他候选仍是开放义务或策略建议，不能从本稿推出总算法、新颖性或开放性。"
legacy_ids: [gap-lane-20261020, C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, C15]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/gap.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/gap.md
related_objects:
  - ../../../resource-activation/state/证明/启用值的两价格分裂与二维三射线禁形--证明.md
  - ../../../contention-resolution/state/资料/两尺寸固定激活的类内统一权重障碍--资料.md
  - ../资料/双容量BMKP候选的三模块与完整目标--资料.md
  - ../候选/双容量瓶颈背包的profile标签与完整枚举--候选.md
  - ../../../fair-allocation/state/审查/多线候选池实际比较与去重边界--审查.md
---

# 来源身份与阅读范围

`gap.md` 是 2026-10-20 的第一轮 GAP、预算/容量分配与舍入选题底稿。它自己明说不是已完成定理、不是确认无人研究的清单，也不是把候选作者问题升级为本仓库结论。本次逐字读取 29,238 字节冻结版本，并以 `cleanup/inventory.jsonl` 核对其 blob `3243b42ae49115c4bcf400e273349f1a38efb6ec`、SHA-256 `8e14e6d6525cc353091aa0484c6c72dc447f581d6227d6232fb3f960db06b68e`（历史清单中的完整值为 `8e14e6d6525cc353091aa0484c6c72dc447f581d6227d6232fb3f960db06b68e`）。`legacy-cleanup` 与 `main` 两份来源内容相同，因此不计两个数学对象。

底稿给出 11 篇 primary 文献（P01--P11）的定理位置、候选的 20 天停止条件和三个首轮优先项 C08、C06、C01。它同时保留 C02/C04 的 Group GAP 方向、C07 随机出现、C09 二项--Poisson 极值、C10 graphic matroid、C11 MBA 超图、C12 SGAP、C13 random-order GAP、C14/C15 公平分配候选。候选标签 A/B/C/X 只是当时的研究决策，不是成功概率、真值或外部新颖性。

## 已有独立对象与本稿的去向

### C01：两资源启用值的分类

底稿 §4 给出连续 1 列的三物品反例，并提出两资源、全容量、全权重的子模性分类。后续同源 `two_resource_lp_submodularity.md` 已把该命题加强为：二维固定非负矩阵的启用值对所有 \(b,w\ge0\) 子模，当且仅当非零列至多落在两条正比例射线；任意维度的“两射线”仅作充分性。仓库中的[两价格分裂与二维三射线禁形证明](../../../resource-activation/state/证明/启用值的两价格分裂与二维三射线禁形--证明.md)已逐式保留对偶达到性、零列/退化容量、全维分裂和三射线有理禁形。

因此，本源对 C01 的独有贡献是候选决策和文献去重边界：它明确该分类不自动给 GAP 近似算法，Topkis/Bach 等格优化近邻仍需新颖性核查，也不把未检索到解决文献写成开放性。数学证明不在本对象重复升级；这里的 C01 状态是“内部完整重构、novelty-unverified”。

底稿还保留一个 (\varepsilon\in[0,1)) 的连续反例族：把两端列改为 ((1,\varepsilon))、((\varepsilon,1))，三列全集值为 (2/(1+\varepsilon))，子模缺口为 ((1-\varepsilon)/(1+\varepsilon))。这是定量缺口证书，不是 scalar GAP 分数 LP 的反例；GAP 每条 assignment edge 只消耗一个 bin 的标量容量，不能偷换模型。

### C08：两尺寸固定激活的障碍

底稿 C08 针对容量 1、尺寸 (a\in(1/2,1]) 与 (b\in(1/3,1/2]) 的自然 LP correlation gap/CRS。它特别指出 (a+b>1) 时“一个大或至多两个小”的可行结构，以及自然 LP 不能换成整数可行集凸包。底稿的固定 \(x\) 类内统一权重反例已经独立归档为[两尺寸固定激活的类内统一权重障碍](../../../contention-resolution/state/资料/两尺寸固定激活的类内统一权重障碍--资料.md)：

- (a=7/10,b=2/5)，两件大、三件小；
- (x=(3/5,13/50,17/100,17/50,23/50))，(w=(2,2,1,1,2))，自然 LP 消耗 (99/100)；
- 全部 32 个激活集的 Fraction 证书给 \(\rho=117253/187500\)；
- 在每一尺寸类正权相同的限制下最小值为 (52726561/84062500)，严格相差 (237199/126093750)；
- 四个权重断点 (r=0,1,2,\infty) 的分段仿射比值论证覆盖连续的类内统一权重族；
- 一个小物品的 Bernoulli 拆分保持期望尺寸与分母却令期望最优值从 (1.01) 变为 (1.012)，排除“任意拆分都降低 ratio”的逐步 Poisson 证明路线。

这些证书只否定固定 \(x\) 的统一化引理和特定拆分路线；它们不否定允许同时改变 \(x\) 的全局极值归约，不反驳一般 knapsack CRS 猜想，也不等价于 BMKP 或 Q-CAG-HALF。底稿引用的 Sergeev 2020/2024 论文与后续 FB-CRS 基线必须重新核对，旧的 `.279` 数字不能当作当前一般差额。

### C03：reserved-capacity 小物品引理

底稿给出一个直接 greedy 计算：对单调子模 (f)、full budget (B)、物品成本至多 (\delta B)、返回成本至多 (\rho B) 且 (\rho>\delta)，按 marginal density 贪心并在不能加入时停止，则
\[
f(S)\ge [1-e^{-(\rho-\delta)}],\mathrm{OPT}.
\]
零成本元素先全取，\(f(\varnothing)>0\) 时先平移常数。该推导的每步只是 gap 乘积与 \(1-t\le e^{-t}\)，本稿也明确它可能是标准知识，不能作为新颖主结果；除非取得有限 \(\delta\) 的 tight envelope 与 matching lower bound 并实际改善 Group GAP，否则应保留为辅助/淘汰依据。

## 15 项候选的准确状态

| 编号 | 当时标签 | 精确对象与承重义务 | 本次处置与边界 |
|---|---|---|---|
| C01 | A | 两资源启用值全 \(b,w\ge0\) 子模性分类 | 证明已在 `resource-activation`；本源保留选题/去重 provenance；不宣称 GAP 算法。 |
| C02 | B | Group GAP 组总尺寸越过 \(m/2\)，需同组 all-or-nothing 的可行装箱 | 仍是候选；必须同时保 assignment profit 和组内互斥，不能只给无利润装箱。 |
| C03 | X/辅助 | reserved capacity 的有限小物品 tradeoff | 标准 greedy 引理；新颖性与 tight 有限界未证，不能单独立题。 |
| C04 | B | AGAP 保留容量修复能否超过 \(1/19\) | 保留为受限 rounding 候选；必须防止“移走再填”把同组物品放入同一 bin。 |
| C05 | X | 等 opening cost 的 GBAP/SAP 提升 | P09 的 continuous-greedy/pipage 与 bins 上 matroid 已覆盖工具层；P10 给快速 SAP；只可作 baseline/实现比较。 |
| C06 | A | 非均匀 opening cost 的 GBAP 联合 budget/item-contention rounding | 仍未证；需在两种 opening cost、稀疏 support 等小类给 exact worst case、matching obstruction 或严格消除乘法损失的 coupling；不得隐藏配置 oracle 复杂度。 |
| C07 | B | 随机出现物品的 ex-ante opening 与 ex-post recourse | 需明确决策时序、recourse-value 子模/近似子模或失败反例；不可把利润乘 \(p_j\) 当作非线性冲突的替代。 |
| C08 | A | 两尺寸 knapsack correlation gap/monotone CRS | 固定 \(x\) 统一化与拆分路线已有障碍；允许改变 \(x\) 的全局 sharp bound 仍未判定，不能写成反驳一般猜想。 |
| C09 | C/辅助 | Sergeev Conjecture 4.1 的 Binomial--Poisson 单调性 | 先核对是否由 convex order/旧定理一行推出；只有能改善 CRS 下界才有独立价值。 |
| C10 | B | cactus/series-parallel graphic matroid 的 correlation gap | cactus cycle matroid 的 direct-sum 只给已知 baseline；2-sum 的边缘耦合必须实证，不能把 treewidth 当黑箱充分条件。 |
| C11 | B | MBA graph-rounding 扩到稀疏大物品超图 | 目标是受限 3-uniform 类的配置 LP rounding 或 sharp obstruction；不等于一般 MBA 的 (3/4) 突破。 |
| C12 | C | SGAP 两尺寸原型与跨 bin 次模交互 | 需保留真正跨 bin 的次模效应；若可化为 SMKP 或已被 matroid+knapsack CRS 覆盖则淘汰。 |
| C13 | C | random-order GAP 的 one-overflow 修复 | 只在有结构 coupling 时有意义；不能把 fractional single-knapsack 的 tight (1/e) 当一般 GAP 改进。 |
| C14 | B | divisible FEF 与 Pareto 的兼容性 | 先两 agent/自然容量类给反例或存在+算法；要明确 charity、Pareto 和 zero-size/value 量词，不能用 envy-cycle 名称替代证明。 |
| C15 | B/C | matroid 约束下 exact FEFx 的 strongly-poly 边界 | P07 已有 pseudo-poly/FPTAS 方向；需要真正组合势或反例，binary value 的数值有界不能冒充强多项式新结果。 |

底稿给出的首轮排序是 C08、C06、C01；该排序只表示当时“可在短期形成可证伪切口”的判断，不是开放题清单，也不覆盖本仓库后来形成的正式对象。C14/C15 的公平分配材料应沿 `fair-allocation` 独立存档；不因同出一份 GAP lane 而与 BMKP 合并。

## Primary 文献去重与准确适用范围

本稿 P01--P11 不是仓库外部定理的重新证明，处置为来源级文献地图。实际可复用的去重点如下：

- P01 已给 scalar assignment LP 值函数的子模工具、reserved capacity 和 Group GAP 的具体阈值；P02 的 AGAP all-or-nothing 约束使同组互斥成为额外承重；P03 的 GBAP configuration LP、opening budget 与 interval capacity 给 C06/C07 的模型入口，但其算法界不是所有方法的最优界。
- P04 的 knapsack CRS 按尺寸类给障碍和 conjecture；不能把论文未证的 conjecture 写成仓库反例，也不能继续使用已被后续 FB-CRS 改善的旧 `.279` 作为现行基线。
- P05 的 matroid correlation-gap 结构问题、P06 的 graph MBA 配置舍入、P07 的 FEF/FEFx、P08 的 monotone submodular multiple knapsack、P09 的 continuous greedy/pipage 与任意 bins 上 matroid、P10 的 Poisson SAP 加速、P11 的 random-order GAP one-overflow，分别限定 C10--C15 的去重和适用范围。
- P09/P10 只消除 C05 的“等 opening costs 快算法”伪新颖性；它们不能自动解决非均匀 opening costs、随机 recourse、组内 all-or-nothing 或真正跨 bin 次模交互。反过来，C06 若只给更差的常数也没有价值，必须量化时间/实现或舍入耦合的改进。
- 文献链接、定理编号和 2025--2026 检索结果均是当时记录；本源明确说“未检索到”不等于开放性证明，摘要打不开的论文不能据摘要作解题判断。

## 证据、程序与未闭合义务

底稿引用的 `exact_vector_lp.py`、`search_lp_submodularity.py`、`two_ray_search.py`、配置归约边界笔记和 `round2_manifest.json` 是可复现入口。精确 Fraction 枚举支持 C01/C08 的局部证书；浮点随机搜索只是负面观察，不能当作正定理。已有独立对象保留原始脚本和输出的 provenance，本页不重写原文件。

本源没有证明任何 C02/C04/C06/C07/C09--C15 的总算法或 sharp bound，也没有完成全部文献全文的外部优先权审查。`candidate_pool.json`、`fair.md`、`FAILED_ROUTES.md` 是同一选题组的其他来源，需逐源单独处置；本页不把只读摘要、候选排序或公屏消息记为完成。

C01 的正式证明、C08 的固定 \(x\) 障碍、BMKP 三模块与公平分配审查已各有稳定对象；第三阶段可把本页与这些对象建“来源—候选—去重—边界”关系，但不能造出无条件的算法依赖边。若以后继续研究 C06/C08 全局量词，应新建增量对象并明确区分“固定激活概率”“允许同时改变边缘”“自然 LP”与“整数可行凸包”。

## 处置结论

本源处置为 **integrated 到本审查对象，并 retained 其来源级候选/文献/停止条件 provenance**。它的独有内容是 GAP lane 15 项候选的决策表、P01--P11 的具体去重用途、C01/C08/C03 的局部数学边界和每条候选的致死义务；C01 证明和 C08 反例的数学正文分别由 `resource-activation` 与 `contention-resolution` 对象承接。它不提出新的总定理、反例、近似保证或外部新颖性认证。
