# 真实兄弟激励的联合曲率恒等式与尾重置

2026-10-24，tree8。原 CAG-MODEL 的全部输入与完整历史量词不变。以下关系由同一原策略的真实 IC 与逐客户代数证明，不依赖有限计算。它没有证明新的福利界；Q-CAG-HALF 仍 OPEN。此前 round2 `mixed/two_query_cross_child_boundary.md` 与 round3 `global/full_depth_substitution.md` 已识别跨历史删除势债；本页把同一困难改写为任意兄弟分支耦合下的 reciprocal Hessian / topic correlation 关系，不认领为新的支付机制。

## 1. 同一个真实父节点及全部真实下一角色行

固定一个合法有序前缀 h，客户背景负载为 b。至少还有两位行动者。用 a 作为有限索引，A_a 是父节点可以强制选择的合法主题；索引可以重复主题。强制 A_a 后，原 σ 规定下一位行动者选 B_a，此后真实有序尾部为 C_a。C_a 可为空；其客户负载记 c_a(x)。

在前缀 (h,A_a) 强制下一行动者改选 B_b 后，原 σ 的真实尾部记 C_ab，负载 c_ab(x)。四类对象全部使用同一原完整策略，不把兄弟尾部搬入另一前缀后称为真实续局。

对任意合法主题 T 和任意合法尾元组 C，定义静态数值

    f_a(T,C) = Σ_(x in T) 1/[b_x + 1_(x in A_a) + 1 + c_C(x)].

因此下一角色的真实 IC 是

    γ_ab := f_a(B_a,C_a) − f_a(B_b,C_ab) >= 0.       (IC)

另定义查询特定的真实尾重置

    Δ_ab := f_a(B_b,C_ab) − f_a(B_b,C_b).           (RESET)

RESET 末项是合法 profile 的静态评估，通常不是该前缀的 prescribed completion。Δ 可以为正或负。逐客户有精确式

    Δ_ab = Σ_(x in B_b)
       [c_b(x)−c_ab(x)] /
       { [b_x+1_(x in A_a)+1+c_ab(x)]
         [b_x+1_(x in A_a)+1+c_b(x)] }.            (RCP)

全部分母至少为一；空主题和空尾不需要例外。

## 2. 任意对称耦合的一份共同恒等式

令 π_ab>=0、Σ_ab π_ab=1，且 π_ab=π_ba。其共同边际为 p_a=Σ_b π_ab。置

    α_ax := 1_(x in A_a),
    s_ax := b_x + 1 + c_a(x),
    v_ax := 1_(x in B_a) / [s_ax(s_ax+1)].

则精确有

    E_π[γ_ab + Δ_ab]
      = −(1/2) Σ_x E_π[(α_ax−α_bx)(v_ax−v_bx)].   (HESS)

证明：IC 与 RESET 相加后，左边是

    Σ_ab π_ab [f_a(B_a,C_a)−f_a(B_b,C_b)].

利用 π 对称，第二项重标为 Σ_ab π_ab f_b(B_a,C_a)。对每个 x∈B_a，两个分母只差 α_ax 与 α_bx。二者相同时差为零；二者不同时公共乘积恰为 s_ax(s_ax+1)。所以

    f_a(B_a,C_a)−f_b(B_a,C_a)
       = Σ_x v_ax(α_bx−α_ax).

再次按 a,b 对称化即得 HESS。没有对逐客户收益分别使用 IC；IC 只以非负 π_ab 权重整行组合一次。

由于 E_π γ>=0，HESS 给真正的共同关系

    (1/2) Σ_x E_π[(α_ax−α_bx)(v_ax−v_bx)]
        <= −E_π Δ_ab.                             (JOINT)

所有兄弟分支在同一 π 下共同出现，不能为不同客户各选一份 π 后仍宣称共享 IC 金额。

特别取 iid π_ab=p_ap_b，得到 covariance 形式

    −Σ_x Cov_p(α_ax,v_ax)
        = E_(p⊗p)γ_ab + E_(p⊗p)Δ_ab.              (COV)

## 3. 末位端点与一般深度的确切区别

若下一行动者已经末位，则 C_a 与 C_ab 均为空，Δ=0，且 1/[s_ax(s_ax+1)] 只依赖 x。于是

    −Σ_x [1/((b_x+1)(b_x+2))]
           Cov_p(1_(x in A_a),1_(x in B_a))
        = Eγ_ab >= 0.

这是已有同背景末位真实最佳回复反相关的逐客户 curvature 形式。一般深度不能撤掉两个变化：v_ax 内的 c_a(x) 依赖兄弟分支，而 Δ_ab 使用第三棵真实尾 C_ab。即使两个前缀经济计数相同，原 σ 仍可给不同有序历史不同尾部；不能按计数把 C_ab 与 C_b 识别。

因此 HESS 并未证明输入主题与 prescribed 响应主题总体反相关，也未证明每个 pair 有正确符号。允许反相关失败的准确量是 −EΔ；这不是已经付清的实际利润。将 RCP 每个正部独立送到相应分支的未来利润，会再次产生互斥叶共同容量问题。

## 4. 与第七轮坐标初始化的接口及停止处

第七轮 source 的第一接收者选择主题 B_a 时，跨兄弟影响出现在 α 与 v 的交项；HESS 可同时保留这组 off-history IC 的真实松弛，而非只比较单条 B/W 叶。它目前没有给 source 价格与 π 的一个合法共同选择，也没有给 EΔ 的 actual 残余预算。

故本页只保留一个可直接攻击的全范围共同式。真实待付仍是：在与最优比较库存和实际钱包兼容的同一耦合下，控制所有 RESET，使它们不重复使用不同完整叶的后继利润。没有该额外关系，JOINT 不能推出 `OPT<=2W` 或 round7 的 RESIDUAL-CAP。
