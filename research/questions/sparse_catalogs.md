# Q-SPARSE：单公共客户、任意大小异构目录的尖锐阈值

状态：**本轮数学闭合，尚未经外部同行评审。** [SPARSE-RHO-ALL](../current/heterogeneous/sparse_unbounded_rho.md) 在双方目录任意长时给完整纯续局 `ρ` 上界，原 HC-RHO 六客户 `2×2` 下界属于本类，因此普遍尖锐阈值为 `ρ`。以下保留原问题量词与探索路线作为审查记录；旧的开放表述均须按新定理解释。入口：[路线](../ROADMAP.md)、[增长规则](../GROWTH.md)。

## 1. 实例类与完整量词

恰好两个带标签设施，非空有限目录 \(U_1,U_2\)，可不同、相交或不交。有限客户集，正原子权重，地点覆盖 \(C_s\)，覆盖后强制参加，客户最小化包含自己重量的实现负载期望，设施最大化期望服务重量。客户可独立混合。额外条件为

\[
|C_s\cap C_t|\le1\qquad\text{对每个 }(s,t)\in U_1\times U_2.
\]

该条件限制**客户人数**，不是公共总重；同一客户可以覆盖多个地点。若 \(s\in U_1\cap U_2\)，合法共址对也须满足它，所以 \(|C_s|\le1\)。两目录大小均无上界。

现已解决的目标：是否对每个该类实例，都存在 \((s,t)\) 及为全部 \(U_1\times U_2\) 带标签布局各指定精确客户 NE 的规则 \(\sigma\)，使

\[
L_1(\sigma(r,t))\le\rho L_1(\sigma(s,t))\quad(r\in U_1\setminus\{s\}),
\qquad
L_2(\sigma(s,r))\le\rho L_2(\sigma(s,t))\quad(r\in U_2\setminus\{t\}).
\]

零收益仍按未除法的不等式检查。结论为 `α_sp=ρ`。存在性允许正实权重；精确算法及可执行反例使用显式覆盖、正二进制有理权重。

## 2. 已有边界与可直接使用的精确接口

**证明转折。** [SPARSE-HIGH-ACYCLIC 与 SPARSE-BALANCED-R](../current/heterogeneous/sparse_high_reach_barrier.md) 处理双方**任意长**目录：若两侧每一地点的 reach 均至少为本方最大 reach 的 `1/r`，固定纯 NE 规则下存在完整目录 `r`-稳定布局。反过来，若根本没有 `r`-稳定布局，该规则的每个全目录最佳回应环都必须进入某方低 reach 区。新[全类证明](../current/heterogeneous/sparse_unbounded_rho.md)进一步在 `r=ρ` 排除了**首个**高到低边，故不需要控制低区内回返。精确[审查脚本](../../tests/audits/sparse_high_reach.py)与[冻结有理记录](../../evidence/runs/2026-10-01/sparse_high_reach.json)攻击了平局、零 reach、完整 off-path 及两个必要假设。

按[受限 \(\rho\) 页](../current/heterogeneous/restricted_rho.md)，HC-RHO 的上界同时需要单公共客户与 \(\min(|U_1|,|U_2|)\le2\)。其六客户下界族已经属于本题，给 \(\alpha_{\mathrm{sp}}\ge\rho\)。先前[任意异构上界](../current/heterogeneous/full_catalog_cycle.md)只给 \(\alpha_{\mathrm{sp}}\le2\)；本轮独立于短目录提升的新证明把上界降为 `ρ`。这些上、下界沿用各自的内部研究证明状态。

固定布局、地点覆盖重 \(R_s,R_t\)，若无公共客户，负载强制为 \((R_s,R_t)\)。若唯一公共客户重 \(w\)，其两条件成本为 \(R_s,R_t\)：

| 情况 | 全部 NE 第一设施负载集合 |
| --- | --- |
| \(R_s<R_t\) | 单点 \(\{R_s\}\)，客户纯选设施 1 |
| \(R_s>R_t\) | 单点 \(\{R_s-w\}\)，客户纯选设施 2 |
| \(R_s=R_t=R\) | 整个区间 \([R-w,R]\)，任意独立混合概率 |

记这些区间为 \([a_{st},b_{st}]\)，总服务重 \(V_{st}=R_s+R_t-w\)（无公共时令 \(w=0\)）。真实威胁为

\[
D_1(t)=\max_{s\in U_1}a_{st},\qquad
D_2(s)=\max_{t\in U_2}(V_{st}-b_{st}).
\]

逐布局最小化 \(\max\{1,D_1(t)/x,D_2(s)/(V_{st}-x)\}\)，在威胁和为正时最优第一负载为

\[
x^*_{st}=\operatorname{clamp}_{[a_{st},b_{st}]}
\frac{V_{st}D_1(t)}{D_1(t)+D_2(s)}.
\]

两威胁均零时任取区间点；正分子/零分母视为无穷，零分子贡献零。全布局最小值即该实例允许全部独立混合续局的最优因子。这一精确接口已经实现于 [`single_overlap.py`](../../facility_spe/exact/single_overlap.py)，允许双方目录任意大，不能据其适用范围扩大 HC-RHO 的定理范围。

## 3. 历史探索关口：完整 3×3 稀疏核心

先研究 \(|U_1|=|U_2|=3\)，这是未被短目录上界覆盖的最小尺寸。客户覆盖在跨目录矩阵上形成矩形 \(A_i\times B_i\)，其中 \(A_i=\{s\in U_1:i\in C_s\}\)、\(B_i=\{t\in U_2:i\in C_t\}\)。单公共条件要求不同客户的这些非空矩形**不共享格子**。按这个约束生成真实 incidence，再分配正有理权重；不能自由填写九格收益，把未必可由共同客户覆盖实现的矩阵当成实例。

对每个候选重算全体九格区间、两侧全部真实威胁与精确最优值。先枚举或解析严格 reach 次序，再处理 reach 平局及其整段混合 NE。若得到 \(\alpha^*>\rho\)，用有理隔离区间或 \(q(z)=z^3-z^2-2z+1\) 在 \(z\ge\phi\) 时的严格单调性作精确比较；仅有浮点近似大于 \(1.80194\) 不足。

证明 3×3 上界本身不会推出任意目录定理。[CORE-LIFT](../current/heterogeneous/core_lift_and_monotone.md)保留**全目录**极小收益威胁，但[SPARSE-LONG-CYCLE](../current/heterogeneous/sparse_long_cycles.md)反驳无条件短核心。新全称证明利用“固定纯规则没有 `r` 稳定布局”的假设直接排除首个低区入口，不需要旧的未取得证明的“至多两种重客户身份”候选。反例搜索只输出一次失败菜单不具否定力；真正反例需上述全 NE 区间的最优性证据。

## 4. 现有代码、证据与必须保留的负例边界

从仓库根目录运行：

```sh
python3 -m facility_spe.exact.single_overlap examples/heterogeneous/rho_lower.json
```

2026-10-01 重跑得到实例最优因子 \(80193772/44504187\)，并输出在轨 NE、两项实际偏离 NE 及默认规则。`verify` 直接检查的是**达到证书**；该结果的最优性另来自本页完整区间分析与全布局扫描，不能由短证书自身推出。原输入是靠近 \(\rho\) 的一个有限例，不是单个达到无理阈值的有理实例，也不是 \(>\rho\) 反例。

| 资产 | 可复用/限制 |
| --- | --- |
| [受限 \(\rho\) 证明](../current/heterogeneous/restricted_rho.md) | 单客户局部分类、严格 2×2 四环、下界族可用；按每行最佳列缩减依赖只有至多两行 |
| `facility_spe/exact/single_overlap.py` | `parse` 检查全部跨对；`local` 给真实区间；`solve` 扫全部布局。平局时必须保留混合 |
| `facility_spe/exact/bounded_overlap.py` | 可作同一线性模型的小规模独立支持枚举对照；先确认两个实现未共享被测求解核心 |
| `tests/test_heterogeneous.py` 与[历史运行](../../evidence/runs/2026-09-30/heterogeneous_all_singletons.json) | 核查一般异构构造及有限实例；记录中的菜单 “singletons” 指种子方式，不等于单公共客户假设 |

**两个范围负例需要保留：**[整数 sharp-2 族](../current/heterogeneous/sharp_two_lower.md)每合法对有两名公共客户，能逼近 2，却不属于本题。`examples/heterogeneous/six_cycle.json` 也不是本题输入：布局 \((0,6)\) 有公共客户 \(\{2,3,4\}\)，`single_overlap` 的全输入检查会拒绝；该文件中的长回应环不能被当作单公共客户六环证据。2026-10-01 已重跑确认该拒绝，未修改原例。

## 5. 原验收计划与现行结果

以下记录原先的探索计划，路径并非全部已创建；实际闭合证明在 [`sparse_unbounded_rho.md`](../current/heterogeneous/sparse_unbounded_rho.md)：

| 产物 | 路径与验收要求 |
| --- | --- |
| 3×3 第一结果 | `research/questions/sparse_3x3_result.md`；可实现的 incidence、严格序和平局、结论覆盖范围 |
| 新定理或严格反例 | 已完成 `research/current/heterogeneous/sparse_unbounded_rho.md`；新 ID SPARSE-RHO-ALL，未静默扩大 HC-RHO |
| 搜索及独立检查 | `tests/audits/sparse_catalogs.py`；精确数据生成、全 NE 目标表、对照、种子和搜索边界 |
| 输入和排除证据 | `examples/heterogeneous/sparse/`、`evidence/certificates/heterogeneous/sparse/`；每布局 \(a,b,V,D_1,D_2,x^*,\alpha^*_{st}\)，以便完整重算 |
| 冻结运行 | `evidence/runs/<新运行标识>/sparse_catalogs.json`；记录输入哈希、代码版本、规模、成功/拒绝及未探索类，不覆盖旧记录 |

新普遍上界覆盖任意大目录、平局、目录相交与零收益，且结合旧同类下界给尖锐值。有限搜索仍仅是攻击证据；尚无外部审稿或文献优先权判断。新成果按增长规则同步目录、claims、assets、graph。
