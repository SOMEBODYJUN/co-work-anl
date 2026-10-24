# 一般半覆盖工作稿：后继势后悔与删位重置

目标 `Q-CAG-HALF`，仍 **OPEN**。本对话按附件程序建立独立 main 克隆；发布身份由程序生成，接续旧 `boss20/` 的数学资产但不覆盖其身份。所有新研究对象均为任意有限共同目录、任意人数、每份全历史纯 SPE。本文是 root 的实际一般推导；不是完整证明，也没有外审或新颖性认证。

## 1. 固定一般对象

沿一份完整 SPE 的实际位置 i，过去负载为 b。当前强制主题 A 后，同一完整策略给真实后继元组 B(A)，长度 n=m-i。记

\[
\Phi_b(q)=\sum_x[H_{b_x+c_x(q)}-H_{b_x}],\quad H_0=0,
\qquad d(A)=u_i(A,B(A)).
\]

所有背景负载都是非负整数。q 可以为空；调和差始终有定义。对任意分布 p，令 A,T 独立同分布 p，并定义

\[
D=\mathbb E_A d(A),\quad
C=\mathbb E_{A,T}\sum_{x\in T}\frac1{b_x+1+c_x(A,B(A))}.
\]

这里 C 是完整菜单的同分布推送查询价格；不是自由选列后的最小值。实际 SPE 给 D≤u_i。旧稿的条件倒数协方差恒等式适用，但没有自动给 C≤D。

## 2. 后继联合势后悔的精确分解

定义

\[
R=\mathbb E_{A,T}\big[\Phi_b(A,B(A))-\Phi_b(A,B(T))\big],
\]

\[
J=\mathbb E_{A,T}\sum_{x\in A\cap T}
\frac1{(b_x+c_x(B(A))+1)(b_x+c_x(B(A))+2)}\ge0.
\]

则对任意完整纯策略（不需要 SPE），

\[
\boxed{D-C=R+J.}\tag{POT}
\]

证明：先把 C 中的旧当前行动 A 删除，所得查询价格记为 C⁻。插入边际恒等式给

\[
D=\mathbb E_A[\Phi_b(A,B(A))-\Phi_b(B(A))],
\]

\[
C^-=\mathbb E_{A,T}[\Phi_b(T,B(A))-\Phi_b(B(A))].
\]

独立同分布交换 A,T 得 D−C⁻=R。逐客户比较保留/删除 A 的两个查询分母给 C⁻−C=J，得到(POT)。这没有改变后继或把另一个孩子当成本孩子的均衡。

若 n=0，R=0。若 n=1，固定 A 后只有一个后继，且

\[
\Phi_b(A,B(A))-\Phi_b(A,B(T))
=u_{i+1}(A,B(A))-u_{i+1}(A,B(T))\ge0.
\]

所以末两人位置 C≤D≤u_i。n≥2 时，B(T) 是合法元组，但其成员不能作为一个联合行动偏离；全历史 SPE 没有提供后继联合势最优性。不能把 R≥0 当成引理。

## 3. 用全部真实后继比较展开 R，剩余的是删位重置

固定 A,T，记 t=B(T)。对 j=0,…,n，Z_j 是在背景 b 后，当前根 A 与前 j 个后继 t₁,…,tⱼ 固定，其余后继按同一原策略走出的活动终局。因此 Z₀=(A,B(A))、Zₙ=(A,B(T))。j 从1开始时，在真实有序历史 (过去,A,t₁,…,tⱼ₋₁)，Zⱼ₋₁ 是规定行动续局，Zⱼ 是强制 tⱼ 后的真实续局。

记 Γⱼ 为该后继玩家的整主题真实 IC 松弛，故 Γⱼ≥0。用 Z\j 表示只从终局元组删除这名后继的行动（这仅是代数，不声称删位后仍为 SPE），定义

\[
E_j=\Phi_b(Z_{j-1}\setminus j)-\Phi_b(Z_j\setminus j).
\]

势插入边际给

\[
\boxed{\Phi_b(Z_{j-1})-\Phi_b(Z_j)=\Gamma_j+E_j,}
\quad
\boxed{R=\mathbb E\sum_{j=1}^n\Gamma_j+\mathbb E\sum_{j=1}^{n-1}E_j.}\tag{RESET}
\]

最后一位没有后继变化，所以 Eₙ=0。更早 Eⱼ 的两个终局删除当前行动后，其更晚行动仍来自原先两个不同历史；不能重新解释成删除后游戏中的真实 IC。这正是本表示的重置缺口。

## 4. 接到一般目标的位置与准确停止处

对每个实际位置分别定义 Rᵢ,Jᵢ,Dᵢ,Cᵢ；令 eᵢ=uᵢ−Dᵢ≥0，则

\[
\sum_i C_i-W=-\sum_i(e_i+R_i+J_i).
\]

这里必须在全部位置使用同一个 p。若对每个 p 都证明 ΣᵢRᵢ+ΣᵢJᵢ+Σᵢeᵢ≥0，将支付同分布推送菜单；后者又充分支付自由完整路径菜单。若只求半覆盖，一个额外槽静态安全最优 p 满足此式也足够，因为每个 Cᵢ(p)≥vₘ₊₁(0)，故 W≥m vₘ₊₁(0)≥OPTₘ/2。但这些量词均未证明。

全 p 推送预算比自由菜单所需更强，因为还没有使用自由选列收益 Lᵢ=Cᵢ−min_A Kᵢ(p,A)≥0，也没有允许各位置非均匀混合。不能因等价展开(RESET)而称该候选已经推进或闭合。

当前待判别：全部真实 Γ 是否足以共同支付负的删位重置；或完整 SPE 能否反驳这一加强候选，从而证明必须保留自由选列信用。本轮 covariance 分支负责这个明确加强的攻击，root 不做无目标有限扩样。

## 5. 复用已有完整见证划清界线

旧共享 `individual_security_counterexample.md` 的34客户、三人完整 SPE 已经否定 R≥0：在其根使用唯一三人静态安全最优分布 p*=(10,10,21,10,10,21)/82，旧已证数值 D=29/3、C⁻=2411/246 给

\[
R=-11/82<0.
\]

本轮只是按(POT)重算同一个已有见证，额外槽折扣为 J=40571/20172，C=52377/6724，因而 D−C=37865/20172>0。这不是新反例，也没有否定推送总预算；它证明即使全部真实后继均为 SPE，也不能单独要求后继联合势后悔非负。复算脚本 `root_potential_regression.py` 从共享原实例读取整数重数，重新核对全部43历史，记录精确输入 SHA-256，不依赖优化器。

本轮 covariance 分支另给四客户完整 SPE 与无平局七客户版本，严格否定逐客户 H⁰≤H¹ 及逐客户 Cₓ≤Dₓ。四客户实例经独立研究员先自行重构全部决策后审查，root 已重放两份独立 Fraction 程序并手核七客户严格比较。其总预算仍成立，因此不能把逐客户失败外推为一般 half 或自由菜单失败。正文见 `covariance/customerwise_covariance_boundary.md`，独审见 `independent_audit/review_covariance_tiny.md`。

POT/RESET 的一般代数已有独立重构，见 `independent_audit/review_potential_reset_identities.md`。这些审查只确认身份和代数，不填补剩余跨客户/跨子树支付。

继承入口：旧 boss20 的 `route_mpath/dynamic_query_debt_identity.md`、`route_flow/dual_owner_budget.md`、`clean_audit/owner_theta_audit.md`；共享一般工作稿 `research/current/customer_attraction/general_half_proof.md`。本文没有把旧资产、表示改写或文件保存计作一般证明的新闭合步骤。
