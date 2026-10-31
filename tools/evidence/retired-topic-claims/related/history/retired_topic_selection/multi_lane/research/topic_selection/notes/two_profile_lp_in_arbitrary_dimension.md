> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# C01-v3：任意资源维数、至多两条列射线的充分性

日期：2026-10-20。独立数学推导，交给根部审查。**状态：证明已写全；新颖性未确认。** 本稿建立新 Claim/version，不修改或偷换 C01-v2 的两资源 iff 量词。

## 1. Exact Statement / Objects / Quantifiers

**Claim C01-v3.1（全维两射线充分性）.** 对任意有限整数 d,n≥1、固定非负矩阵 A∈R_+^{d×n}，若其非零列至多落在两条正比例射线上，则对所有容量 b∈R_+^d 和所有利润 w∈R_+^n，集合函数

φ_{b,w}(S)=max{wᵀx:Ax≤b, 0≤x_i≤1_{i∈S}}，S⊆[n]，

都是归一、单调、子模的。

允许 b 含零、A 含零行与零列、两条射线有零坐标；不要求A/TU、整数容量、polytope integrality、两射线线性独立或正资源系数。对有理输入，射线类别识别可用O(nd)次有理算术，位复杂度为输入位长的多项式。

**与v2的关系。** C01-v2.1是d=2时的必要充分分类；本稿把其充分方向推广到任意d。**不主张d≥3时两射线必要。** 例如A=I_3有三条坐标射线，却对所有b,w有φ(S)=∑_{i∈S}w_i min{1,b_i}，是模函数。

## 2. 一个处理全部边界的二维价格分裂引理

**Lemma C01-v3.L1.** 对任意 z,z'∈R_+²，存在λ,μ∈[0,1]使

z∧z'=λz+μz'，
z∨z'=(1−λ)z+(1−μ)z'，

其中∧、∨为逐坐标min、max。两个等式的右侧系数互补，因此可在更高维非负向量的任意线性像上同时实现，并保持两个原向量的和。

**证明。** 若z≤z'，取λ=1,μ=0；若z'≤z，取λ=0,μ=1。剩下只需交换命名使 z=(p,q),z'=(r,s)，p<r且q>s。因为p,s≥0，r,q>0，

D=rq−ps>0。

取

λ=s(r−p)/D，μ=p(q−s)/D。

显然非负。由s≤q得到λ≤1；由p≤r得到μ≤1。直接计算：

λp+μr=p，λq+μs=s。

于是λz+μz'=(p,s)=z∧z'。又z+z'=(z∧z')+(z∨z')，减去第一个等式即得第二个。

如果p=0或s=0，公式仍合法；两者同时零时λ=μ=0，min=0，max=z+z'。不存在需要除以p、s或价格斜率的步骤。∎

## 3. 全维充分性证明：直接分裂原对偶向量

### 3.1 剥离零列与保证对偶最优解达到

每个零列item i在启用时总可取x_i=1，贡献w_i。因此它们贡献模函数∑_{i∈S,A_i=0}w_i，剥离后证明其余部分即可。

令两种非零轮廓为u,v∈R_+^d，列A_i=s_i u或A_i=s_i v，其中s_i>0。若只有一种轮廓，可以令v=u、第二类为空；本证明仍适用，不需要另作极限论证。

对任意S，原LP可行（x=0）、可行域紧、目标有限。标准有限维LP强对偶和最优解达到性给

φ(S)=min_{y≥0} D_S(y)，
D_S(y)=bᵀy+∑_{i∈S}(w_i−A_iᵀy)_+。

这里用的是通常LP对偶min{bᵀy+∑_{i∈S}z_i:A_iᵀy+z_i≥w_i,y,z≥0}，消去z_i取hinge。存在至少一个达到最小值的y_S：完整对偶有有限最优解，消去z后其y仍最优。b有零和资源冗余均不影响这一点。

### 3.2 为union和intersection构造可行对偶解

固定任意S,T，选达到最优的y_S,y_T∈R_+^d。定义两类型价格

P(y)=(uᵀy,vᵀy)∈R_+²。

对z=P(y_S), z'=P(y_T)应用Lemma L1，取相应λ,μ∈[0,1]。令

y_∧=λy_S+μy_T，
y_∨=(1−λ)y_S+(1−μ)y_T。

二者非负，并满足

P(y_∧)=z∧z'，P(y_∨)=z∨z'，
y_∧+y_∨=y_S+y_T。

因此bᵀy_∧+bᵀy_∨=bᵀy_S+bᵀy_T。这里**没有**假定bᵀy能由(p,q)唯一确定；保留原d维向量后直接保持其和，绕开了三维及以上的非唯一价格实现问题。

### 3.3 逐item比较

记h_i(y)=(w_i−A_iᵀy)_+。因为A_i=s_i u或s_i v，h_i只依赖价格P(y)的一个坐标，且对该坐标递减。

- i∈S∩T：该坐标在y_∧、y_∨处恰为原两个坐标的min、max，故
  h_i(y_S)+h_i(y_T)=h_i(y_∧)+h_i(y_∨)。
- i∈S\T：P(y_∨)≥P(y_S)，故h_i(y_S)≥h_i(y_∨)。
- i∈T\S：同理h_i(y_T)≥h_i(y_∨)。

把这些不等式与完全相等的资源成本项相加：

φ(S)+φ(T)=D_S(y_S)+D_T(y_T)
≥D_{S∪T}(y_∨)+D_{S∩T}(y_∧)
≥φ(S∪T)+φ(S∩T)。

最后一步因为y_∨、y_∧分别是union和intersection对偶的可行解。归一性由φ(∅)=0、单调性由启用集增大而LP可行域扩大得到。证明完毕。∎

## 4. effective price cost的独立闭合（不是crosspartial猜想）

为对应此前提议，定义价格锥K=P(R_+^d)以及

c_b(z)=min{bᵀy:y≥0,P(y)=z}，z∈K。

K是第一象限内的有限生成闭凸锥。任意z∈K时上述LP可行、目标≥0且有限，所以最优解达到；z=0时y=0给c_b(0)=0。c_b是凸、正齐次函数，但不需要求导：

给z,z'的最优实现y,y'，用L1相同λ,μ构造y_∧、y_∨。它们实现z∧z'、z∨z'，所以

c_b(z∧z')+c_b(z∨z')
≤bᵀy_∧+bᵀy_∨
=bᵀy+bᵀy'
=c_b(z)+c_b(z')。

这同时证明K对min/max闭合和c_b在K上子模，处理了轴向、零价格和分段线性折点。不需光滑近似、不需把price cost错误当线性。

更一般地，同一个分裂引理直接证明：任何在第一象限凸锥上取有限值、凸且一阶正齐次的函数c均子模。因为convex+homogeneous给c(αz+βz')≤αc(z)+βc(z')，再把互补系数的两个不等式相加即可。

## 5. 本轮有限查重结果与引用边界

这一证明没有依赖任何未验证的外部定理。机制属于经典lattice optimization与partial minimization，而非新发明的格理论。

2026-10-20针对本义务补查：`linear program submodular two types`、`linear programming two types submodularity`、`fractional two types submodular`、`convex homogeneous submodular`、`packing two types submodular`、`two rays submodularity`、`two-dimensional homogeneous submodular convex`、`submodularity linear programs columns`。分别使用两套搜索引擎。**未找到精确的“任意d、两列类型/射线、对所有b,w的启用集LP子模”statement；不能把搜索阴性升级为新颖性。**

最接近的经典引用接口：

1. Donald M. Topkis, *Minimizing a Submodular Function on a Lattice*, Operations Research 26(2),1978，https://www.jstor.org/stable/169636 。公开primary摘要表明其研究参数化格最小化和isotone解；本轮全文reader只返回空壳，未核到能直接引用的具体编号theorem。因此不能写“由Topkis定理X直接得全维两类型结论”。
2. Francis Bach, *Submodular functions: from discrete to continuous domains*, Mathematical Programming175,419–459,2019（online2018），https://link.springer.com/article/10.1007/s10107-018-1248-6 。primary摘要核实其一般连续域子模理论；正文在publisher访问页未展开，未找到本specific LP类型定理。不能据其一般主题认定已覆盖。
3. Kulik–Sarpatwar–Schieber–Shachnai, *Generalized Assignment via Submodular Optimization with Reserved Capacity*, ESA2019，https://arxiv.org/html/1907.01745v2 ，Theorem1是scalar assignment LP值函数子模性的直接研究源头。本v3的对象是单启用集packing LP任意资源维数、至多两个资源轮廓，不应把它冒充原作者明确提出的问题，来源身份仍为C。

若后续发现一般二维convex homogeneous/sublinear cost子模性为教科书命题，充分性应表述为它与LP dual的直接应用；若已有two-type capacity valuation结论，则本稿回收为去重/教学工具，不制造新颖性。

## 6. 决策影响与停止范围

- 本义务已经闭合，不需要继续d=3大枚举。
- C16“查三资源两轮廓是否子模”已解决为肯定，不能再作为开放候选。
- C01-v2的d=2必要性仍有效；v3只加强充分性，不提出高维的iff。
- 仍未得到assignment-coupled新近似算法、固定b分类或新颖性确认；因此没有把简短定理自动升级为独立论文主目标。
