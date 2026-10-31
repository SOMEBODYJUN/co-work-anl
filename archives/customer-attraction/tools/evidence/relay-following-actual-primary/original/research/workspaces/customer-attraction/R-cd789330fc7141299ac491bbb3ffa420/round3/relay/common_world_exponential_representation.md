# 同一 owner 势的共用角色优先级表示

2026-10-23。一般有限共同目录、任意人数、所有完整有序历史保留。**这是既有 HYB/owner 势的等价表示，不是新的跨树付款或 half 证明。** 确定性 layer-cake 与 Exp 期望公式已由 root 独立重构核对；尚无条件化原 IC 的定理。

相关自足对象见 `optimal_exchange_potential_and_query_credit.md`、shared 的 `../shared/owner_exchange_potential.md`，以及 credible 的 `../credible/owner_hybrid_transport.md`。本页只统一同一随机世界，不新增实例或数值扫描。

## 1. 固定 owner 后的一条确定性不等式

令 T 为最优 m 槽元组，O=union T。一次性固定分割 Q_i subset T_i，令 o(x) 为 x in O 的 owner。Q_i 仅是分析库存，不要求为合法动作。对任意合法 profile B，最优性的全部子集 hybrid 给

    |union_(i in J)(B_i outside O)|
      <= |{x in O:o(x) in J，且 x 不被 J 内任何 B_i 覆盖}|。    (HYB)

给各角色任意非负实数 z_i，定义空最大值为0，并写

    M_x(B;z)=max_(i:x in B_i) z_i。

对 (HYB) 取 J_t={i:z_i>=t}，在 t>=0 上积分。左端逐客户为 M_x，右端逐客户为 (z_o(x)-M_x)_+，故

    sum_(x outside O) M_x(B;z)
       <=sum_(x in O)(z_o(x)-M_x(B;z))_+。            (MAX-HYB)

等价地，定义

    F_z(B)=sum_(x outside O)M_x(B;z)
              +sum_(x in O)min{z_o(x),M_x(B;z)}，

就有

    0<=F_z(B)<=sum_(x in O)z_o(x)。                  (CAP)

同一个固定 z 可用于所有合法 B 及所有原 sigma 的真实 rollout；这不是给互斥叶重新抽签。每项是 weighted max 或截断 weighted max，所以 F_z 对带槽标签的动作 token 单调、次模。形式空槽可填合法主题后用单调性处理，不调用删人 SPE。

## 2. 独立 Exp(1) 角色钟精确恢复旧势

现在令 z_1,...,z_m 为独立 Exp(1)，并让所有客户、所有叶共用这一组角色钟。owner 分割及槽配对均先于抽钟固定。若客户有 c 个覆盖槽，则

    E M_x=H_c，    H_0=0。

证明可用尾积分 E M=integral_0^infty[1-(1-exp(-t))^c]dt=H_c。这里只需要同一客户的不同角色钟独立；没有假设不同客户的随机值独立。

若 x in O 且 owner 槽覆盖它，min(z_owner,M_x)=z_owner，期望为1。若 owner 不覆盖它，M_x 是 c 个非owner钟的最大值，与 z_owner 独立，所以

    E min(z_owner,M_x)
      =integral_0^infty exp(-t)[1-(1-exp(-t))^c]dt
      =c/(c+1)。

因此严格有

    E F_z(B)=F_Q(B)。                               (EXPECT-F)

此等式逐个固定 B 成立，也可对预先固定的原策略树全部有限叶同时采用同一个随机空间。

定义原采样调和势 H_z(B)=sum_x M_x(B;z)，以及

    Psi_z(B)=sum_(x in O)(M_x(B;z)-z_o(x))_+
       =sum_(x in O)[max{z_o(x),max_(i!=o(x):x in B_i)z_i}-z_o(x)]。

则逐样本精确有 H_z=F_z+Psi_z；若 k_x 是非owner覆盖数，

    E Psi_z(B)=sum_(x in O)[H_(1+k_x)-1]=Psi_Q(B)。   (EXPECT-INSERT)

对角色 i 的形式去槽边际，原真实收益恰为

    u_i(B)=E[H_z(B)-H_z(B_-i)]，

因为每个当前覆盖客户的期望边际为 H_c-H_(c-1)=1/c。这同时恢复旧的 u_i=ell_i^Q+e_i^Q，不新增一份福利。

## 3. 原 IC 仍只是不带条件的期望比较

在一个固定原历史 h，令 B^- 为规定动作后沿原 sigma 的终局，B^+ 为一个固定合法偏离后沿原 sigma 的终局。原 SPE 只保证

    E[(H_z(B^-)-H_z(B^-_-i))
        -(H_z(B^+)-H_z(B^+_-i))]>=0。              (IC-EXPECT)

它不保证括号逐 z 非负，也不保证按观察 z 后选取的非负权重重乘仍非负。可无条件使用的是完整原 IC 的非负常数线性组合。若 owner、查询主题、节点选择或购买 IC 的系数依同一 z 适应，必须另证相应条件化或解耦关系；不能由 (CAP) 或同核外观推出。

确定性 (MAX-HYB) 对每个 owner 分割本身都真，但 (EXPECT-F)/(EXPECT-INSERT) 的这些计数公式要求分割先固定。不能观察钟后挑 owner，再仍沿用这里固定 owner 的期望公式。

## 4. 尚未证明的 cap 中继接续想法

root 提出一个与真实递增角色捕获流相符的样本级候选解释。对原实际遗漏客户 x，其 owner 查询的当前角色 i 获得初始 cap z_i；该叶的其他覆盖者全在未来。令 M 为这些未来覆盖者的最大钟，则可将 cap 拆成

    (cap-M)_+ 当前吸收，    min(cap,M) 送至最大钟的未来覆盖者。

若 cap<=z_i，当前吸收不超过采样真实收益边际 (z_i-M)_+。接收 cap 不超过接收角色的钟。把接收角色重置到它的原实际前缀真实查询叶后，可再次拆分；角色严格递增，cap 不增，因而样本级过程有限终止。

仅对第一次、未经筛选的查询，cap=z_i 且 c 个覆盖角色的钟对称：当前期望吸收为1/c，每个未来覆盖者的期望接收也为1/c（总未来接收期望 (c-1)/c）。它确实复现原首轮真实份额。

**这还不是对后续原 IC 的合法付款。** 之后接收角色、查询及 cap 均已依同一组钟选择，不能再无条件套用 (IC-EXPECT)。若重新抽独立 ghost 钟计价，需要真正的解耦或记忆性上界，并证明它保持共同付款；当前没有该关系。这里只保留这一准确接续想法，不声明中继具有已付期望费用，也不重复扩写恒等式代替缺口。

## 5. 边界与当前等级

零客户、空 owner 块、空主题、重复主题都按原槽索引处理。c=0 时 max=0、H_0=0，owner未覆盖项期望0；非负确定性钟可以为0并可固定处理并列。Exp 钟几乎处处无并列，选最大角色时仍可预定按索引破平局。

本页增加的是一个**同一既有势的共用世界表示**。尚未增加能够支付 credible 当前 K_i^in 的 whole-IC 兼容关系，也没有证明新的 half 充分条件成立。一般目标仍 OPEN。
