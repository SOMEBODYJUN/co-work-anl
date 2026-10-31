> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# C01-v2：两资源启用集 LP 的全权重子模分类

日期：2026-10-20。身份：本轮独立数学推导；**尚未完成新颖性去重，不能称为新定理投稿成果**。它加强了首轮只有反例的状态，提供一个完整的 genuinely fractional 自然分类。分类驱动，来源 C（受 Kulik–Sarpatwar–Schieber–Shachnai ESA2019 Theorem 1 的 scalar LP 子模性启发）。

后续版本：`C01_ARBITRARY_DIMENSION_TWO_RAYS.md`中的Claim C01-v3.1已把本稿充分方向推广到任意资源维数，并严谨处理effective price cost，不再停留于末尾crosspartial观察。本稿的d=2 iff保持原statement，高维不宣称两射线必要。

## 精确陈述

固定有限非负矩阵 A∈R_+^{2×n}。忽略零列。对任意 b∈R_+²、w∈R_+^n 和 S⊆[n] 定义

φ_{b,w}(S)=max{wᵀx:Ax≤b,0≤x_i≤1_{i∈S}}。

**Claim C01-v2.1.** 以下等价：

1. 对所有 b≥0 和所有 w≥0，φ_{b,w} 都是子模集合函数。
2. A 的非零列至多落在两条正比例射线上。

不是只对整数容量/整数多面体的陈述。全 b 量词是必要的；固定 b 时可能有冗余资源或三列永远不同时活跃，因此本分类不直接适用。零列贡献 ∑_{i∈S,A_i=0}w_i，是模函数，可剥离。

## 充分性：两种资源轮廓的价格格结构

首先假设恰有两个不同方向 u,v∈R_+²，因其非比例而线性独立。每列可写 A_i=s_i u 或 s_i v，s_i>0。LP 对偶为

φ(S)=min_{y≥0} bᵀy+∑_{i∈S}(w_i−A_iᵀy)_+。

令 p=uᵀy，q=vᵀy。线性映射 y↦(p,q) 可逆，故 y≥0 的像 K 是第一象限内由两个非负向量生成的闭凸楔形锥；bᵀy 是 (p,q) 的线性函数 ℓ(p,q)。

**价格域格引理。** 第一象限内任意由两个非负向量生成的闭凸锥 K，封闭于逐坐标 min 和 max。非轴向情形可写 K={p,q≥0:αp≤q≤βp}，其中 0≤α≤β≤∞，约束对 min/max 都保持。含坐标轴时分别把 α=0 或 β=∞，同一论证成立。

设 S,T 的最优价格为 z_S=(p_S,q_S)、z_T=(p_T,q_T)。最优对偶解存在：原 LP 可行且有有限最优值，有限维 LP 强对偶与达到性适用。令 z_∨=max(z_S,z_T)、z_∧=min(z_S,z_T)，则两者均在 K。

对第 i 件物品定义 h_i(z)=(w_i−s_i p)_+ 或 (w_i−s_i q)_+。它只依赖一个坐标且递减。因此：

- i∈S∩T 时，h_i(z_S)+h_i(z_T)=h_i(z_∨)+h_i(z_∧)；
- i∈S\T 时，h_i(z_S)≥h_i(z_∨)；i∈T\S 同理；
- 线性项满足 ℓ(z_S)+ℓ(z_T)=ℓ(z_∨)+ℓ(z_∧)。

相加并分别用 z_∨、z_∧ 作为 union、intersection 的可行对偶解，得到

φ(S)+φ(T)≥D_{S∪T}(z_∨)+D_{S∩T}(z_∧)≥φ(S∪T)+φ(S∩T)。

如果只有一条非零射线，资源约束归结为 ∑s_ix_i≤min_{r:u_r>0}b_r/u_r；一个价格变量的相同 min/max 证明成立。零条非零射线显然。

## 必要性：三种轮廓形成的严格交换障碍

若存在三条不同射线，按斜率选列 d,e,f，使中间方向 d 位于两端 e,f 的严格正锥内。交换资源坐标后可设

d=λe+μf，λ,μ>0，e₁/d₁>e₂/d₂，f₂/d₂>f₁/d₁。

中间列 d 的两个坐标均正。取

w_d=1，w_e=e₁/d₁，w_f=f₂/d₂，b=αd，

其中 0<α≤min{1,1/λ,1/μ}，其余物品权重可设零且不启用。

对 {d,e}，第一资源约束给 x_d+(e₁/d₁)x_e≤α，故目标≤α，取 x_d=α 达到；对 {d,f} 用第二资源约束同理。singleton {d} 也恰为 α。

在全集 {d,e,f} 中，取 x_d=0,x_e=αλ,x_f=αμ；此解恰消耗 αd，且上界 x≤1 由 α 的选择保证。它的利润为

α[λe₁/d₁+μf₂/d₂]
>α[λe₁/d₁+μf₁/d₁]=α。

所以 φ({d,e})+φ({d,f})=2α<φ({d})+φ({d,e,f})，违反子模性。证明完毕。

## 不夸大的价值判断与剩余工作

这是一个两资源、全容量与全权重的完整 iff，带线性时间识别：遍历非零列，按交叉乘积判断是否已有两条射线；出现第三条即给出三列证书。对于有理数输入，方向判断与 λ,μ,α、利润、反例容量都可用有理运算实现；位长为输入位长的多项式。

它比“TU/连续1矩阵不足”的反例更强，解释了为何两种资源轮廓保住价格 min/max，而第三种方向导致互补。它并非自动产生 GAP 新近似算法，也尚未排除已有 lattice programming / substitutes / parametric LP 文献把它作为一般定理特例。**仅此 iff 是否足够独立成稿尚未确认**；应先查一般 price-cone lattice characterization，再考虑 assignment-coupled 输入或固定容量 quantitative defect。

最强 objection：上述对偶格证明可能是 Topkis 型单调比较静态的直接特例；自然性明确，但若理论贡献只有套用一个现成格定理和三列反例，不能当作20天主目标。另一方面，它的必要性排除了把任意两资源 matrix 作为自然扩类的幻想。

辅助实验：`python battle_gap_tools/experiments/two_ray_search.py`。seed=20261020，300 个随机两射线、6 件物品实例，对所有64个启用集精确求浮点 LP 并枚举局部子模不等式，未发现反例。此实验不是充分性证明，上文对偶证明才是数学依据。

## 建议下一判别动作

1. 独立逐行审查对偶格证明，尤其零坐标、退化容量和对偶达到性。
2. 查 price cone closed under min/max、submodular LP value functions、gross substitutes with divisible goods；判断此 iff 是否已有完整覆盖。
3. 若未覆盖，尝试 r≥3 资源、两轮廓情形：价格域仍是二维楔形，但 bᵀy 不再由价格唯一确定。此时应分析最小价格实现成本 c_b(p,q)=min{bᵀy:Uᵀy=(p,q),y≥0} 是否子模；不能沿用“线性”一步。

## 本轮定向查重记录

2026-10-20用两套搜索引擎分别检索`linear programming submodular lattice value function`、`fractional knapsack gross substitutes`、`submodularity two resource linear`、`submodular two rays`、`submodularity linear programming optimal value upper bounds variables Topkis lattice dual`等。没有检索到上述两资源全b,w iff的精确statement；这只是搜索阴性，不是新颖性证明。

必须继续排查的primary近邻：Donald M. Topkis, **Minimizing a Submodular Function on a Lattice** (Operations Research,1978)，https://www.jstor.org/stable/169636 ；Francis Bach, **Submodular functions: from discrete to continuous domains**, Mathematical Programming (2019)，https://link.springer.com/article/10.1007/s10107-018-1248-6 。本证明的min/max方法显然是经典格优化机制，因此即使具体矩阵分类未见，也不能把它说成新的格定理。

另有 Morton, **Structural properties of network revenue management models: An economic perspective** (Naval Research Logistics,2006)，https://onlinelibrary.wiley.com/doi/abs/10.1002/nav.20166 ，讨论resource availability值函数在两资源模型中的sub/supermodularity。当前仅找到primary摘要，未读全文；其自变量是资源可用量，不等同当前启用item集合，不能据摘要认定覆盖或不覆盖。

三资源两轮廓切口的进一步objection：c_b是二维凸且一阶正齐次。光滑内点写c_b(p,q)=p h(q/p)，则∂²c_b/∂p∂q=−q h''(q/p)/p²≤0；分段线性情形可能以分布/有限差分延拓。因此该切口很可能仍是经典凸齐次函数子模性的直接结果，应先证明/查证这一点，再考虑其选题价值。
