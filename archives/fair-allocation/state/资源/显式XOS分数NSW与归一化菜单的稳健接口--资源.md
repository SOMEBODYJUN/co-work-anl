---
id: FA-EXPLICIT-XOS-FRACTIONAL-NSW-ROBUST-INTERFACE-RESOURCE-v1
kind: mathematical-resource
type_tag: 资源
title: 显式XOS分数NSW与归一化菜单的稳健接口
status: reconstructed-scoped-mathematics; no-external-novelty-or-software-certification
summary: 重匹配修正、显式XOS完整确定化证明和普通UM结论的强度分别保存。
primary_source_id: fec6d30660294d4449dc
carrier_history: unrelated-machines-workspace-cross-family-navigation
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-ca2c8c2f564d4e2fa4b3b0949bb0b66a/README.md#all
---

## 模型和旧版范围

有限原物品U，n名无额外agent权的代理，显式二进制非负有理XOS `v_i(S)=max_a Σ_(j∈S)w_iaj`。分数配置y每行质量1、每原item总质量≤1，正质量配置有正价值；benchmark
\[
 B(y)=\exp\bigl(n^{-1}\sum_{i,S}y_{i,S}\log v_i(S)\bigr)>0.
\]
当前完整数学算法只输入显式XOS，同一个真实allocation对**每个**正分数benchmark同时给常数NSW，无需输入y。它不是一般次可加value-oracle算法，也不是输入一个有界支撑y后才成立。

旧七源合并正文在当时只将重匹配A视为证明完、B–E/backend条件；后续当前两份完整审查已重构作者v4/v5的实现化证明，不能把历史“尚未独立复核”当永久数学缺口。相反，数学上的det-bit-poly算法仍不等于已有端到端可执行backend，本批未运行它、未重读71631B作者原Proof全稿。实际本批全文材料是旧核心、当前完整重构、v4-v5增量及比例纠错四份，范围精确记录。

## 分数重匹配引理及必要补假设

取|H|=n、B=U\H、V_i≥0、A={i:V_i>0}，单调次可加v。除所有B上分数配置族z均满足
\[
 \sum_{i\in A,T\subseteq B}z_{iT}v_i(T)/V_i\le cn
\]
外，必须有 **i∉A⇒v_i(B)=0**。原旧独立A段漏写此条件，已交最小proposal；后续算法取A={v_i(B)>0}而满足它。于是存在且可找H上的最大正乘积匹配π，使
\[
 \Bigl(\prod_i[V_i+v_i(\{\pi(i)\})]\Bigr)^{1/n}\ge B(y)/(c+1).
\]
证明对配置S写T=S∩B、k=|S∩H|，m=max(V_i,最大H singleton)。次可加给v_i(S)≤m(v_i(T)/V_i+k)，inactive残余因补假设为0。分数残余界与H列cap使括号平均≤c+1，Jensen给log损失≤log(c+1)。把配置质量送到最大H singleton，缺口只在active行；用运输补双随机，Birkhoff/Hall得一置换至少该平均log。物品不复制。

遗漏假设确实使原A假：n=1，U={h,b}、H={h}、V=0、A空，additive v(b)=1,v(h)=0，y只给{b}。残余不等式空真而A4左0、右1/(c+1)>0。该反例不反后续XOS构造。

最大乘积不是无理oracle：正因子有理，两个不同匹配乘积的log间隔≥2^(−poly(input bits))；二进制缩放后用log级数求有理近似至小于间隔/(4n)，普通有理最大权匹配即求真最大乘积。零边先删，正边完美matching由上述前提保证。

## 完整显式XOS确定化的承重链

1. 在**全U**找正singleton matching；Hall失败则不存在正分数benchmark或正NSW allocation，可返回空bundles、最优NSW为0。否则找真最大正singleton-product matching τ，令其H为预留items；不能仅在一个已固定H上局部最优。原v_i(B)>0者为active。显式clause固定lift R用λ,z、z≤λ、列cap表示residual；它包含所有分数配置utility向量，反向以nested-prefix有限分布恢复多项式支撑，故不是仅整数福利domination。
2. 令active数a、归一化W_i=v_i(B)。有理barrier迭代保持x_i≥1/(4a)，取h=1/(32a²)；线性oracle `M=max_(u∈R)Σu_i/x_i`，更新至M≤2a，给所有residual分数族共同A2、c=2。终止步数、分母编码和LP basic解均按输入总位poly，不用实数优化精确性作为免费假设。A空单独重匹配。
3. 对正支撑配置support-respecting舍入：候选bundle/clause先固定，用有限CDF逐item条件期望保归一化welfare≥当前人数1/2。每次条件后重新使用条件分布，不沿用未条件概率。对大价值行V_i≥6ν_i（ν_i residual最大singleton）split，份价值在[V_i/3−ν_i,V_i]，取松弛d=5/2。
4. 所有round candidates先固定，再给**原item**唯一有限label/mask；候选不是新item。candidate-local Q=210|B|格、shift β_i=ν_i/V_i，Bernoulli shifted inverse≤1/M与有理卷积DP给每项误差预算，所有候选总误差≤1。未移位inverse在零事件失效，旧SA尾界漏3因子不追认为正确。
5. 对所有比较双射π同时作rematching充要不等式，关键反事实matching可以使用全U最优τ；最后按原v重新最大乘积匹配。常数链 `60000×3×(5/2)^2=1125000`，给真实allocation NSW≥B(y)/1125000（保守合同可用2250000）。同一个输出同时控制所有正y，未把给定y的选择塞入算法。

这些步骤的真实依赖是显式XOS、全分数包含、finite-support/bit bounds、candidate先固定、shifted DP及全U rematching。当前重构逐段给数学证明；无新全pipeline软件审计、外部评审或全球新颖性认证。

## norm1 FSLP、repair与高低比例互补

norm1正support FSLP给benchmark1；保守ρ=2²⁴足够。若v_i≤1且NSW≥ρ⁻¹，价值小于 `q_η=ρ^(−ceil(1/η))` 的组数严格少于ηn（边界按严格低值计）。同n原groups的singleton repair数D，任一分配至多救D个原groups；不能增加分母或只数剩余组。把repair与原菜单lift合成显式LP，可得相应promise判定；它不替普通UM输出全机sub2。

稳健NO若写“价值≥δ的高组数<γ_hi n”，等价“价值<δ的低组数>(1−γ_hi)n”。因此当δ≤q_η且γ_hi≤1−η时，NSW所得低组<ηn与NO严格冲突，**两个等号也有效**。旧“低组至少γ_lo n”参数不能直接改名γ_hi。门控福利的对应near-perfect条件为 `(5/8)(1−η)≥γ_hi+(1−γ_hi)δ`；各桥各有域，不把福利F2冒NSW全域。

UM还原对好组有较小selected-root负载，但少数坏组仍可能接近2；全部machines只保证≤2。几乎所有组好、或LP排除特定robust NO，不等于所有机器统一(2−ε)近似，更不完成一般UM正反面。

## 实读比较正文与来源定位

下列是相关既有数学正文的全文比较，编号对应本包 comparison-manifest；同页其它模型不扩称本入口独有内容。旧错误段的最小勘误另有before/proposed，引用不追认其错误措辞。

- 50 [部分激活菜单福利地板--定理](../../../unrelated-machines/state/定理/部分激活菜单福利地板--定理.md)。
- 51 [部分激活菜单福利地板范围审查--审查](../../../unrelated-machines/state/审查/部分激活菜单福利地板范围审查--审查.md)。
- 67 [分数重匹配与归一化XOS稳健缺口边界--定理](../../../unrelated-machines/state/定理/分数重匹配与归一化XOS稳健缺口边界--定理.md)。
- 68 [显式XOS分数NSW的确定化合同与真实审读链--审查](../../../unrelated-machines/state/审查/显式XOS分数NSW的确定化合同与真实审读链--审查.md)。
- 69 [分数重匹配显式XOS-v4-v5增量--审查](../../../unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md)。
- 70 [归一化菜单高低比例互补的实质纠错及修复边界--审查](../../../unrelated-machines/state/审查/归一化菜单高低比例互补的实质纠错及修复边界--审查.md)。
