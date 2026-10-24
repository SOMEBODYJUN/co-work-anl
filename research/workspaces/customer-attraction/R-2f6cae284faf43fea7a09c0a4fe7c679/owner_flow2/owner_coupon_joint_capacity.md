# owner 自由与实际净券钱包的同一容量系统

2026-10-24，Boss21/owner_flow2。输入为任意有限单位客户、任意有限非空共同目录、任意人数与每份完整历史纯 SPE；空主题、重复主题、任意平局及零客户均保留。**Q-CAG-HALF 仍 OPEN。** 本页把任意 owner 前缀信用直接接到已知 SAFE/CLIP 净券与实际 Hall-A 钱包，不使用 owner 势端点改善作为付款。

状态须准确区分：§1--4 是现有一般组件的一份兼容合成；§5 给将 owner、实际 I 路由与 G 取消一起消元的解析对偶。本页没有证明最后的全价格不等式，不把这份表示当成 half 的正面闭合，亦不主张相对全部旧资料的新颖性。

## 1. 固定一次真实树与固定的合法净券核

固定完整历史纯 SPE sigma，实际叶 Z=(S_1,...,S_m)，覆盖 C、利润 u_j。固定一个最优有序比较元组 T=(T_1,...,T_m)，O=union T_i。置

    R=O\C, I=O intersect C, G=C\O,
    I_j=u_j(I), g_j=u_j(G), u_j=I_j+g_j.

这里 G 同时可按上下文记其大小。令 E_x={i:x in T_i}，对 x in O 非空；实际覆盖者集合 J_x={j:x in S_j}，c_x=|J_x|。

选择并固定一份合法的全客户 SAFE 净券核、fresh-profit SAFE 核，或其合法删正边/CLIP 版本。若用 fresh-profit 核，本页只往它注入 R 来源。每个 natural context 的利润、退款与转移子边均由原完整 sigma 的真实叶确定，**在选择本页来源 owner 与取消量之前固定**。随后输入流、归一化系数与输出净券对来源质量线性。不同核不能合领预算，CLIP 后须从头重算流。

对每个 x in R、i in E_x，单独从 actual-prefix 的合法 T_i query 注入一单位 x。当前真实份额进入 actual i；未来份额进入原 query 叶上的真实规定 context；再沿固定净券核传播。记最终 actual 角色 j 收到的非负金额为

    P_{j;ix} >=0.

已知 INIT 与 SAFE/CLIP 守恒直接给

    sum_j P_{j;ix}=1.                            (STOCH)

这与旧 capture-flow 的付款价格 p_{j;ix} 不同：旧 p 的列和可能大于 1，包含整条 IC 的 slack 过付；这里已经在同 context 安全退款，P 的列和精确为 1。P 是 actual 钱包的净需求分配，不是另一个 IC 系数。

fresh 来源因果序及全 context HIT 给

    P_{j;ix}=0 for j<i,
    sum_{j in K}P_{j;ix} <= |K intersect {i,...,m}|/
                              (1+|K intersect {i,...,m}|)
       if i notin K.                            (ORDER-HIT)

当 i in K 时只取上界 1。上述式子对相同实际树、相同 P 的所有角色集合同时成立。其原证明来源见 round6/relay/global_role_coupon_hitting.md 和 round7/coupling/fresh_source_order_and_suffix_hits.md；这里不重新认领这两项发现。

## 2. 分数 owner 不丢任意 owner 的前缀信用

对每个 x in O 取 alpha_ix>=0，支持于 i in E_x，sum_i alpha_ix=1。它只拆分析库存，不改游戏、玩家或 sigma。可先独立抽取每个客户的一个固定 owner，边际为 alpha，再对这些**各自固定全局 owner**的证明取平均。

任意固定 owner 在合法最优前缀叶 Y_k=finish_sigma(T_1,...,T_k) 上都满足

    sum_{k:x in T_k} e_k(Y_k;x) <= H_{|E_x|}-1.

因此同一 alpha 平均后的 F_alpha、ell_alpha、e_alpha 仍满足 UNIT、0<=F_alpha<=OPT，以及

    sum_{k:x in T_k} e^alpha_k(Y_k;x)
        <= H_{|E_x|}-1.                         (PREFIX-ALPHA)

这是 arbitrary_owner_prefix_budget.md 的直接平均推论。中间叶由 T 和原 sigma 决定，不需要在各叶重选 owner；不存在把依赖排列的中间叶代入固定端点 SYM 的偷换。

分数 owner 可同时用于下面的真实钱包系统。它不要求把一个分数可行解还原成一份整数 owner，也不把不同 owner 势当同一势望远镜。F_alpha 的任何端点提高都没有在下面记作收入。

## 3. 同一 alpha 的 actual Hall 路由、取消与净需求

给 x in I、i in E_x、j in J_x 设实际角色边流 f_ijx，容量

    0<=f_ijx<=alpha_ix/c_x.                     (I-CAP)

自环取零即可。边方向为 owner i 到 actual coverer j。给 x in R、i in E_x 写

    gamma_ix>=0, rho_ix>=0,
    sum_{i in E_x}(gamma_ix+rho_ix)=1.           (R-SPLIT)

此时 alpha_ix=gamma_ix+rho_ix。gamma 是 actual G source 沿实际 I 份额送到 R 库存的取消，rho 才进入净券核。每个角色必须使用同一份运输守恒：

    gamma_i+out_f(i)-in_f(i)=g_i,
    gamma_i=sum_{x in R}gamma_ix.               (HALL-BAL)

旧 Hall-A 对每个整数 owner 成立；平均整数 owner 分配及其可行流，便证明任意 alpha 均有非空可行 (gamma,f)。不在各个离轨叶重新领取 G。

实际净钱包仍恰为

    eta_j=I_j+gamma_j>=0, sum_j eta_j=W.          (ONE-WALLET)

因为 incoming f 不超过实际 I 利润，(HALL-BAL) 也保留原 ACT-CAP；不将 out、in 或 gamma 再加为第二份福利。

对相同 rho，线性净券需求为

    K_j=sum_{x in R,i in E_x}P_{j;ix}rho_ix,
    sum_jK_j=|R|-|G|.                           (NET-DEMAND)

一份共同的充分容量条件是

    K_j<=I_j+gamma_j for every j.               (OWNER-NET?)

若能共同选择 alpha、gamma、f 与合法固定净券核满足它，则 (ONE-WALLET)、(NET-DEMAND) 立即给 OPT<=2W。这里没有另收 source 初始化的 u_j；初始化已包含在 P 列里。也没有把旧 SOURCE-NET 的某个 delta 与本页另选的价格最优取消相加。

OWNER-NET 是分数 owner、净券版本的新明确接口，可能强于 half。未证明它对全部输入可行。特别是 STOCH 只说明总需求等于 |R|-|G|，并不说明它已被实际 W 容纳。

## 4. 真正的 owner 变动作用于净券列，而非势端点

固定 x in R，将 epsilon 的**残留**来源从 eligible owner i 移到 k，且保持本次 gamma、I-owner 与 f 不变时，

    Delta K_j=epsilon(P_{j;kx}-P_{j;ix}),
    sum_j Delta K_j=0.                          (OWNER-SWITCH)

只要 R-SPLIT 非负仍成立，这个变动完全合法且 HALL-BAL 不变。故 owner 自由真实能改变的量是不同 actual 钱包之间的需求分配；它不会制造总付款。若改变 gamma 的 owner，则必须同步满足同一实际 Hall 守恒，不能把 gamma_i 的改变单独当钱包增益。

PREFIX-ALPHA 在此变动前后都保留。它说明旧 first-owner 限制已被解除，因而允许对 P 列作平衡；没有从中推出这样的平衡必存在。

## 5. owner、I 容量与 G 取消同时消元的双价格式

下面给 OWNER-NET 的精确解析判别，避免“对每个价格各挑一个 owner，却假设同一 owner 通过全部价格”的量词错误。

固定角色非负价格 lambda_j。写单位残源的净券价

    q_ix(lambda)=sum_j lambda_j P_{j;ix}.

令 mathcal F 为 (I-CAP)、(R-SPLIT)、(HALL-BAL) 的全部可行选择，其中 I 的 alpha 也自由选择。该集合有限维、非空且紧。对固定 lambda，最小净超额为

    min_F sum_j lambda_j[K_j-I_j-gamma_j].

给任意实角色势 z_i，把 HALL-BAL 乘子取成 -z_i。对 R 客户，一单位可在 eligible i 作为残源、价 q_ix，或作为取消、价 z_i-lambda_i；其最小贡献为 min_{i in E_x}{q_ix,z_i-lambda_i}。对 I 客户，选择 owner i 后每条边最多 alpha_ix/c_x，负 Lagrange 边价为 z_i-z_j，因此最小贡献为

    -max_{i in E_x} [sum_{j in J_x}(z_j-z_i)_+]/c_x.

有限线性规划强对偶遂给

    min_F lambda dot(K-I-gamma)
      =sup_{z in R^m} Psi(lambda,z),             (JOINT-DUAL)

其中

    Psi(lambda,z)
      =-sum_i z_i g_i-sum_j lambda_j I_j
       +sum_{x in R} min_{i in E_x}{q_ix(lambda),z_i-lambda_i}
       -sum_{x in I} max_{i in E_x}
                     [sum_{j in J_x}(z_j-z_i)_+]/c_x.

最后一项只使用同一 actual I 客户的一份份额容量；max 是选一次 owner，不是每条边各选不同 owner。R 的 min 同样把 owner、取消和 residual 放在同一个单位库存里。

再对 lambda 位于非负单位单纯形做有限凸极小极大：

    min_F max_j(K_j-I_j-gamma_j)
      =max_{lambda>=0,sum lambda=1} sup_z Psi(lambda,z). (BALANCE)

因此 OWNER-NET 可行当且仅当右边<=0。这里一个 primal 选择须同时满足全部角色；不交换外层 owner 与价格的量词。

**两个必要的自校验。** 若 lambda_j=1，对所有 F 原目标函数恒为

    |R|-|I|-2|G|=OPT-2W.

在对偶取 z_i=2，STOCH 给 q_ix=1、I 差价项为零，Psi 也恰为同一量。因此本式没有把原 half 在常数价格方向悄悄证明掉。若 I 为空，对偶 I 项消失，但 g 取消与残源仍共用每个 R 单位库存，未给 G 第二份信用。

ORDER-HIT 可进一步把 q_ix 上界为同一角色价格的后缀包络 H_i^suffix(lambda)。将这个上界代入 Psi 给一个显式充分价格上界，因为 min 对 q 单调。但常数价格仍只剩 OPT-2W；HIT 本身不能支付此方向。

## 6. 当前实际承重点

已接通的关系是：任意 owner 的 H_a-1 前缀信用可与**一份**实际 Hall-A 取消、**一份**SAFE/CLIP 跨全部 context 的净券需求同时保留；净券下 owner 调节是列间搬运，所有需求与钱包都只计一次。JOINT-DUAL 进一步共同消除了 owner/I 路由/G 取消选择，未遗漏共享容量。

尚须从真实 off-history SPE 最优性或另一个一般机制证明某合法净券核使 Psi(lambda,z)<=0 对所有 lambda>=0、z成立，或构造更弱的总支付。现有 HIT、PREFIX-ALPHA、Hall 最优性都没有证明这一点。尤其最后的常数价格方向就是原 half，不能把对偶公式、非负核、端点优化或有限可行性当作新增福利不等式。

本稿没有进行固定人数或目录扫描，没有修改共享主状态或声明内部可靠提升；下一步应攻击这个共同价格式的原树激励来源，或改换一般付款机制。
