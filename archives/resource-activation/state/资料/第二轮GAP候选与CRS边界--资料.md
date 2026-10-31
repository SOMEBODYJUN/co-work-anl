---
id: resource-activation/second-round-gap-candidates-and-crs-boundaries
kind: resource
type_tag: 资料
title: 第二轮GAP候选与CRS边界
status: retained-candidate-map-with-c01-resolved-and-c17-c19-open
truth_status: provenance-and-scope-classification; no-new-theorem
review_level: full-source-read-cross-archive-comparison
scope: "GAP/舍入第二轮的 C01/C06/C08 结果、C17/C18/C19 新候选及其文献/证据边界"
summary: "完整实读 gap_tools.md。C01 的两射线分类已由现有 resource-activation 证明对象承接；C06 是旧配置覆盖与 pipage 基线回收，C08 的 fixed-x uniformization 和 Bernoulli 拆分路线有精确障碍；C17 coverage 下尾、C18 q=2 OCRS、C19 低支持路径 CRS 保留为候选，均未完成新颖性和全称证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/gap_tools.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/gap_tools.md"
---

# 第二轮 GAP 候选与 CRS 边界

本文完整读取冻结来源 gap_tools.md（17,515 bytes，SHA-256 c0a45d319b0a4e59b01834c889392f9c31451a845149333bd8ec9ad3525db780），并与现有[启用值的两价格分裂与二维三射线禁形](证明/启用值的两价格分裂与二维三射线禁形--证明.md)、[两列射线启用值的二维分类与全维充分性](资料/两列射线启用值的二维分类与全维充分性--资料.md)和[两尺寸固定激活的类内统一权重障碍](../../../contention-resolution/state/资料/两尺寸固定激活的类内统一权重障碍--资料.md)比较。来源把作者原题、作者建议方向和本轮派生候选分开；有限实验和文献排雷不升级为新定理。

## 1. C01：已由现有对象承接的两射线分类

来源的 C01 固定 \(A\in\mathbb R_+^{2\times n}\)，对所有 \(b,w\ge0\) 定义

\[
\varphi(S)=\max\{w^\top x:Ax\le b,\ 0\le x\le\mathbf1_{i\in S}\}.
\]

二维命题是：所有容量和利润下 \(\varphi\) 子模，当且仅当非零列至多两条正比例射线。充分性由二维价格映射、第一象限楔形锥对 coordinatewise min/max 封闭和对偶 hinge 的递减性给出；必要性由三条不同射线的中间列构造严格三列反例。来源的二维三射线禁形、两射线对偶格证明和高维两射线充分性已经被[resource-activation 证明对象](证明/启用值的两价格分裂与二维三射线禁形--证明.md)逐式保存，且高维两射线的价格分裂不再需要可逆价格映射。

第二轮的新增判断是：三资源、两轮廓切口并非独立开放题。对任意维度的两射线列，原对偶价格投影只需二维，互补系数把两个原对偶解分裂成 min/max 并保持 \(b^\top y\) 之和；高维 \(I_3\) 的三射线值函数却是模函数，故“二维三射线禁形”不能无条件高维化为必要性。随机 300 个六物品两射线实例和全部64个启用集只作历史观察，不承担证明或新颖性。

## 2. C06：opening-cost GBAP 的基线回收

候选输入是有限配置 LP 解 \(x\)：每个 bin 配置和不超过1、每件物品总边际不超过1、opening budget 不超过 \(B\)，目标是配置覆盖函数 \(g(A)=\sum_i\max\{\text{covered profit}\}\)。沿同 bin 配置的 \((1,-1)\) pipage 到单一非零，再沿成本保持方向 \((1/c_\ell,-1/c_k)\) 到至多一 fractional 配置；覆盖目标在异号方向凸，取不下降端点。最终整数集和 fractional singleton 都 budget-feasible，得到一个约为 \((1-1/e)/2\) 的 LP 值下界。

这条推导是可审查的旧配置 coverage 与两阶段 pipage 组合，主要价值是澄清 baseline 和模型合同；它没有给出比现有明确 baseline 更强的泛常数新结果，也不能把通用 matroid+knapsack 近似直接当成相同 LP 舍入。来源将泛常数改进淘汰，除非新增模型约束或真正超过 baseline 的算法。

## 3. C08：两尺寸 knapsack 的精确障碍

候选原路线想把两尺寸 knapsack gap 归约到固定 \(x\) 下的类内统一权重，再用 Bernoulli splitting/Poisson 化。来源给出两项精确障碍：

1. 容量1，大尺寸 \(7/10\)、小尺寸 \(2/5\)，激活向量

\[
x=(3/5,13/50,17/100,17/50,23/50)
\]

自然 LP 成本为 \(99/100\)。对固定 \(x\)，允许每尺寸类统一正权并任意零权 sub-support，连续权比的分段线性分式最小值仍为 \(52726561/84062500\)，而一般权向量 \((2,2,1,1,2)\) 的 ratio 为 \(117253/187500\)，后者严格更小。全部32个激活集、sub-support 和四个端点权比均用 Fraction 覆盖；这只否定 fixed-\(x\) 类内统一化，不否定同时改变 \(x\) 的全局猜想。
2. Bernoulli 拆分不保证降低期望比值：确定激活一件大物、两件小物各以 \(1/10\) 激活时，拆分一件小物为两件 \(1/20\) 后，期望最优从 \(1.01\) 升至 \(1.012\)，而分母和期望尺寸保持。不能把“无限拆分至 Poisson”当自动改进。

此外，2025 后续 knapsack CRS 已把普通非单调 \(>.279\) 目标覆盖到至少 \(1/3\) 的基线；是否满足 monotonicity 需逐条核查，不能从 theorem statement 擅自添加。C08 因而降为储备方向，不能继续沿已反驳的 fixed-\(x\) 引理推进。

## 4. C17：AW 舍入到非线性 coverage 的下尾候选

来源提出：若 AW 输出 \(S\) 对线性 \(a\in[0,1]^n\) 有已知下尾界，能否对归一、单调 coverage 函数 \(f\)（单物品边际不超过1）证明

\[
\Pr\!\left[f(S)\le cF(x)/(k+1)\right]
\le C\exp\!\left(-c'F(x)/(k+1)^3\right),
\quad F(x)=\mathbb E[f(R(x))].
\]

这不是把线性定理的 \(a\) 直接替换成 coverage：高度重叠的 coverage atoms 下，固定 modular lower bound 可能远小于 \(F(x)\)。首要义务是通过随机边际/exposure 过程控制 conditional drift 和 quadratic variation；先在 disjoint 或 bounded-overlap coverage 得到真实 variance lemma，再考虑一般 coverage/submodular。当前无完整证明、无新颖性认证。

## 5. C18：batch size \(q=2\) 的 random-element OCRS

来源以已有 \(L\)-resource random-element OCRS 的 \(1/(L+1)\) barrier 为背景，提出固定每 batch 至多 \(q=2\) 个互斥 alternatives、batch 独立、产品占至多 \(L\) 个 unit resources 的新切口：是否存在 \(\epsilon_L>0\) 的 \((1/(L+1)+\epsilon_L)\)-selectable OCRS，或给出 q=2 的 tight construction。

q=2 不等于 \(L\)-partite；\(L=2\) 的已有 hard example 不能直接覆盖 \(L\ge3,q=2\)。首要义务是把 q=2 约束代入原 pair-blocker 分析，先对 \(L=3\) 找正的 blocker lemma 或最小 hard LP，再决定是否能扩到全 \(L\)。不能将一般 matchoid random-order 常数直接包装成此结构的 sharp 结果。

## 6. C19：路径/环路低支持 arrival permutations

来源提出固定循环路线、至多 \(2r\) 个 cyclic rotations/reverse orders 的 rank-1 knapsack CRS：order distribution 可依已知 \(x\) 选择但不依 activation，先研究 \(r=2\) 的四个 orders，求 sharp selectability \(\alpha_r\) 及 small-LP dual obstruction。该问题与 C08 的 offline weighted gap 不同，核心是受限 arrival entropy、route 结构和公平服务。

只有证明 \(\alpha_2\) 严格超过已有两-order 基线，或证明固定有限 \(r\) 仍卡在同一常数并解释机制，才形成独立成果。低支持 order 文献可能已有覆盖，当前只作储备；不能从源文未检索到同定理推出新颖性。

## 7. 处置和模型边界

C01 已由现有证明对象承接，三资源两轮廓切口回收为高维两射线充分性扩展；C06 处置为 baseline，C08 处置为保留障碍；C17、C18、C19 保留为候选地图，尚无总定理、sharp 常数或算法实现。所有有限实验、脚本和文献接口都只支持对应局部量词。

这些对象属于资源启用/CRS/舍入模型，与 BMKP 的中央两容量 max-min、weighted-congestion 的玩家资源成本、facility-games 客户负载和 CAG 顺序 SPE 分离。第三阶段应建立“已承接证明、障碍、候选迁移、文献排雷”关系，不能将 C01 的子模分类、C17 的下尾候选或 C18/C19 的 CRS 设想自动迁移成 BMKP 或均衡定理。
