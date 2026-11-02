# fresh 剩余：共同 reset 列与真实离轨 IC 的未完成尝试

2026-10-24，round3_general/residual。研究对象严格为原 CAG-MODEL 的任意有限单位客户、共同有限目录、任意人数以及每个完整有序历史上的纯 SPE。允许重复选择、空主题、零客户及任意平局。**Q-CAG-HALF、原 RESIDUAL-CAP 和本轮 FRESH-RESIDUAL 均未解决。** 本页保存未完成推导，不作新增福利界或可靠新定理。

## 1. 固定同一张账与两个量词

沿用 `../../next_general/global_credit/coordinate_residual_attack.md` 和 `../../next_general/credible/coordinate_support_attack.md` §0：实际叶为 B，实际收益 u，实际覆盖 C；比较最优元组 T 的并集 O，I=O∩C、R=O\C。同一次坐标选择先付 current d 和固定实际客户券 H，再从 H 的未花 I 份额付 J。故

    d_l≤u_l， H_l+J_l≤u_l(B;I)，
    |O|=Σ_l(d_l+H_l+J_l+K_l)。

R 来源必须以新输入从头接 fresh 利润核 ν；K 是该次重算的非负净终端，不得沿用旧 full-v 流。实际未付目标仍为

    存在同一最优 T、合法坐标剪枝、I 直接付款与 fresh 路由，
    对全部 l 同时有 K_l≤2u_l−d_l−H_l−J_l。       (FR?)

原限定 RESIDUAL-CAP 只许原 full-SAFE/合法 CLIP 及其出口；I 直接付款加 ν 重算本身已是扩展接口。即使扩展接口将来成功，也不能称其自动在原限定路由量词内实现。反之，一个固定 T、固定比例剪枝或固定 ν 路由的失败不反驳上述存在性。

## 2. 真正发生合流的位置

固定角色 k 和经济动作 a。设 Γ 是全部已生成自然 context t=(g,k) 中 prescribed 动作同为 a 的那些节点。它们的 prescribed 叶 V_t=finish(g) 可以不同，但 actual-prefix reset 叶完全相同：

    A=finish(B_<k,a)。

所有源在相同真实 context 先合并，然后定义 β_t=h_t/ν_t。
对 fresh 客户 x∈a\C，记 c_A(x)、c_t(x)=c_{V_t}(x)。从 Γ 送到 A 中角色 j>k 的同一 fresh 客户份额为

    F_(Γ,j,x)=Σ_(t∈Γ) β_t 1_(x∈A_j\V_(t,j))/(c_A(x)c_t(x))。

若以 A 中 j 的客户份额 1/c_A(x) 计密度，恰为

    Λ_(Γ,j,x)=Σ_(t∈Γ) β_t 1_(x∈A_j\V_(t,j))/c_t(x)。       (MERGE)

这是真正跨旧历史、同新叶的列；不是把主题相同的旧 context 识别成同一节点。Γ 中每个旧历史上的逐行 q≤ν、初始 owner 唯一以及单一来源库存守恒，均不能直接代入 MERGE 的整列和。

原 ν 核会在下一 context 按全部 fresh 利润重新采样。因此即使给每条入边保留 origin 标签，MERGE 的客户 x 也可能不属于原 origin 的 T_i。若改用客户保留核，β_x 而非 β_t 缩放边，已改变路由族；需要重证其共同实际钱包容量，不能借客户标签直接宣称占用了 actual(l,x) 份额。

## 3. ell 的共同 reset 精确账

令

    X_t=u_k(V_t;C)，
    W_t=finish(g,B_k)， w_t=u_k(W_t)，
    ell_t=ν_t+X_t−w_t≥0。

这是 g 上返回实际主题 B_k 的真实完整 IC。因为 B_k⊆C，w_t 完全是 C 上利润；没有 fresh 部分。对 Γ 任意非负 β 加权，得到准确的共同约束

    Σ_(t∈Γ)β_t w_t
      =Σ_(t∈Γ)h_t+Σ_(t∈Γ)β_t X_t−Σ_(t∈Γ)β_t ell_t。       (ELL-GROUP)

此式确实保留同一个 Γ 的真实返回孩子，而不是冻结它们的后继。它仍没有控制 MERGE 的列密度：w_t 与 X_t 都来自不同旧历史上的 C 份额；它们不能被改名成 Γ 共享的一份 actual u_k 或同一份 actual I/G。特别地，ELL-GROUP 的方向是对 prescribed ν+X 的下界，不能直接把 ell 写成固定 ν 图的额外终端退款。

同一 reset 动作 a 的 actual-prefix 查询 fresh 利润 f=u_k(A;N\C)、C 利润 Y 和 actual slack e=u_k−u_k(A) 都是 Γ 的共同量，但 N_t 可随旧叶变化。其净券为

    K_Γ=Σ_(t∈Γ)β_t(ν_t−P_t)
       =f Σ_(t∈Γ)β_t−Σ_(t∈Γ)β_t N_t
       =(u_k−Y−e)Σ_(t∈Γ)β_t−Σ_(t∈Γ)β_t N_t。       (RESET-GROUP)

因此只证明 ell_t≥0 仍没有得到所需的 Σβ 共同上界或等价的带 N 抵扣上界。

## 4. 固定 ν 图里不能再白退 ell

在固定 h_t=β_tν_t 和固定出边 β_tq_tj 下，非负守恒唯一指定 current 金额为

    h_t−Σ_jβ_tq_tj=β_t(ν_t−P_t)。

若再把 β_t ell_t 从该金额扣掉，缺的质量没有合法出口；这并非使用了额外 IC 的证明。若改分母或扩大边系数，则 h/ν、全部后续合流及 K 都必须重算，并明确是另一种路由。旧 round5 关于 shrink denominator 的可选记账并未给出固定图费用改进；不能把那个备注与本图叠加成一次免费退款。

这一点仅排除本次尝试中的重复退款步骤。它不排除 ell 通过改变图、构造跨节点抵扣或与其它完整 IC 联用而产生真正共同约束。

## 5. 尝试改用其它源主题；缺口移到二次偏离孩子

单独返回 B_k 只看 C，因此继续考虑 g 上对每个其它源主题 T_i 的完整 IC：

    ν_t+X_t≥u_k(finish(g,T_i))。                  (SOURCE-IC)

这条比较可以真正看见其它源的 fresh 客户，方向比仅返回 actual 主题更适合限制不同 owner 的竞争。它不能用 `finish(B_<k,T_i)` 代替右端：g 通常仍带较早源的首偏离；g 后又强制 T_i 所得叶有两个指定动作。其在较早角色的利润也不能假称那个角色的 prescribed 利润。

对任意查询分布 p，SOURCE-IC 可以合法平均成一次完整 IC 的非负线性组合；但目前没有把这些二次偏离叶的请求合并到原实际客户份额的容量定理。逐个投影回自然利润会引入共同请求和可能的循环，不能丢弃未付的旧叶项。**本次未取得从 SOURCE-IC 到 FR? 的联合不等式。**

## 6. 子分支的非零核检查与使用边界

`offhistory/positive_fresh_candidate.json` 保存子分支定向反例检查得到的一份完整纯 SPE。它只作为合法自然 ν 核确有正 fresh 边的定义级种子；其所有客户类型重数均代表不同单位客户。

该例 m=4、五个主题，实际 (3,4,2,2)，u=(114,106,199/2,199/2)，W=419，实际 fresh 仅19。自然历史 g=(0) 的下一角色规定动作1，其 prescribed 叶为 (0,1,2,2)，reset 叶为 (3,1,2,0)；到第四角色的 fresh 原价 q=1、ν=10、真实 ell=29/4。

这份 seed 并没有反驳 FR?：在 R-only 极大 current 初始化下每个 fresh 源行库存至多19，而各实际 u≥199/2，故所有 fresh 来源均在源处吸收，这条正 ν 边没有被该初始化激活。不可把“自然 context 有正边”写成“同一最优坐标输入下发生了正传播”。完整审计和子分支最终状态见其 README。

## 7. 当前可接续合同

真正需要的新关系是：利用 SOURCE-IC 或其它真实全树约束，把 MERGE 中多来源请求和 RESET-GROUP 的实际费用控制在同一张剩余钱包里；只控制任意外生注入、只换分母或只证明局部守恒均不够。本轮没有可提升的成熟付款定理，因此没有发起独立定理审核。

下一位研究者不应以本页 ELL-GROUP、MERGE 或新名字作为新增 half 进展；它们的作用是定位这次实际使用过的 ell 推导及尚未关闭的二次偏离账。
