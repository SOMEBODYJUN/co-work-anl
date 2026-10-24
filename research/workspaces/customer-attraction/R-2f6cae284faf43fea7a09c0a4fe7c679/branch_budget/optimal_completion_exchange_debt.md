# 最优补全交换与真实分支的无重计债务分解

2026-10-24。对象固定为一般 Q-CAG-HALF：任意有限单位客户、共同有限非空主题目录、任意人数及每份完整历史依赖纯 SPE。空主题、重复行动、任意有序历史平局、零客户均允许。

**状态。** 以下交换关系与同枝债务恒等式是全输入代数关系；`relay` 分支已从定义独立重构交换不等式和分享分解。它们没有控制总债务，没有闭合 half，也不是对新固定人数或受限目录的正面研究。最后的跨枝义务仍 OPEN。没有声称相对全部旧资料的新颖性。

## 1. 每个真实前缀的最优补全

固定任意完整纯 SPE σ 及其实际路径 S₁,…,Sₘ。在位置 i，令 P 是前 i−1 个实际主题的并集，r=m−i+1，S=Sᵢ；定义

\[
 F_r(P)=\max_{T_1,\ldots,T_r\in\mathcal S}|P\cup T_1\cup\cdots\cup T_r|,
 \qquad F_0(P)=|P|,
\]

\[
 \delta_i=F_r(P)-F_{r-1}(P\cup S)\ge0.
\]

这是**总覆盖**补全，非增量覆盖。其沿真实路径望远镜满足 Σᵢδᵢ=OPTₘ−W。

任取达到 F_r(P) 的 r 元组 T=(T₁,…,Tᵣ)，记

\[
 O=P\cup\bigcup_{j=1}^rT_j,\qquad
 D_j=T_j\setminus\left(P\cup\bigcup_{\ell\ne j}T_\ell\right),
 \qquad e=|S\setminus O|.
\]

Dⱼ 是**该比较元组内**的私有客户，不要求全目录私有。不同 Dⱼ 不交，且全部避开 P。重复的比较主题可以使 Dⱼ 为空。

## 2. 两条通用交换约束

移除 Tⱼ、加入实际 S 后，余下 r−1 个比较主题是 F_(r−1)(P∪S) 的合法补全，并且

\[
 \left|P\cup S\cup\bigcup_{\ell\ne j}T_\ell\right|
 =F_r(P)+e-|D_j\setminus S|.
\]

因此对每个 j 都有

\[
 \boxed{\delta_i\le |D_j\setminus S|-e.}\tag{E1}
\]

另一方面，对任意合法主题 A，以 A 替换 Tⱼ 仍然是 r 槽可行解；最优性给

\[
 \boxed{|A\setminus O|\le |D_j\setminus A|.}\tag{E2}
\]

一般地，若 J⊆{1,…,r} 非空，定义

\[
 D_J=\left(\bigcup_{j\in J}T_j\right)
 \setminus\left(P\cup\bigcup_{\ell\notin J}T_\ell\right),
\]

并取任意 |J| 个合法主题的并集 A_J，则同样有

\[
 \boxed{|A_J\setminus O|\le |D_J\setminus A_J|.}\tag{E3}
\]

这些约束不依赖均分收益或 SPE。尤其若某 Dⱼ 为空，(E2) 迫使所有合法 A⊆O，因而 e=0；退化情形没有例外。

## 3. 保留真实后继的同枝分解

在当前**实际有序历史**强制玩家改选 Tⱼ，后继均沿原来同一份 σ。记该完整真实终局为 Zᵢⱼ，当前偏离者总收益为 dᵢⱼ，当前在 Tⱼ∖Dⱼ 的收益为 dᵢⱼ^out；记该枝所有后继在 Dⱼ 上取得的总利润为 Lᵢⱼ。

因为 Dⱼ 避开实际过去且当前 Tⱼ 覆盖全部 Dⱼ，客户价值全部在当前与后继之间均分。因此

\[
 |D_j|=(d_{ij}-d_{ij}^{\rm out})+L_{ij}.\tag{S1}
\]

完整 SPE 的当前真实比较给

\[
 \Gamma_{ij}=u_i-d_{ij}\ge0.\tag{S2}
\]

再把最优补全相对这次单主题交换的松弛完整保留：

\[
 \varepsilon_{ij}=F_{r-1}(P\cup S)
 -\left[F_r(P)+e-|D_j\setminus S|\right]\ge0.
\tag{S3}
\]

代入 δᵢ=|Dⱼ∖S|−e−εᵢⱼ 及 (S1)—(S2)，得到**精确恒等式**

\[
 \boxed{
 \delta_i-u_i
 =L_{ij}-d_{ij}^{\rm out}-|D_j\cap S|-e
   -\varepsilon_{ij}-\Gamma_{ij}.}
\tag{D}
\]

特别地，丢弃两项非负松弛后有

\[
 \delta_i\le u_i+
 \left[L_{ij}-d_{ij}^{\rm out}-|D_j\cap S|-e\right].\tag{Dweak}
\]

每个 i 只使用一条当前玩家真实比较、一次完整利润 dᵢⱼ≤uᵢ。d^out 与 Dⱼ 上当前份额从同一个 dᵢⱼ 中分离，不能再各自领取一份 uᵢ。Lᵢⱼ 则是**该强制枝**的尾利润，没有替换成实际路径的尾利润。

## 4. 总账与真正缺口

各位置任意选一个最优补全和一个 j 后，(D) 精确给

\[
 \boxed{
 \operatorname{OPT}_m-2W
 =\sum_i\left[L_{ij}-d_{ij}^{\rm out}-|D_j\cap S_i|-e_i
             -\varepsilon_{ij}-\Gamma_{ij}\right].}
\tag{TOTAL}
\]

TOTAL 是原目标的一种真实分支分解，**不是普遍支付的证明**。完全保留 ε、Γ 时，要求右边≤0就是原 Q-CAG-HALF 本身，不能把这个等价重写列为新闭合。

一个严格更强、尚未证明的充分义务是：能否在全部真实前缀选择最优补全与 j，使

\[
 \sum_i L_{ij}\le
 \sum_i\left[d_{ij}^{\rm out}+|D_j\cap S_i|+e_i\right]?\tag{B?}
\]

这允许单期欠债。已有三人十一客户完整 SPE 在第二位有 δ₂=3>u₂=5/2，故不能改回逐点 δᵢ≤uᵢ；来源为 `research/current/customer_attraction/coverage_opportunity_counterexample.md`。B? 的跨枝关键仍然是：如何将不同 Zᵢⱼ 中 Lᵢⱼ 的共享遗漏客户利润联合支付，同时让右端各个完整当前利润只付一次。没有证明 B?，也没有声称它是与原目标等价的必要条件。

## 5. 本轮重复诊断与边界

本目录另存 `check_individual_coverage_floor.py` 与 `individual_coverage_floor_test.json`。它们只检验既有完整策略锥中的精确一般候选 `(2m−1)u_i≥OPT_m`。根协调者指出此候选已由 `R-79a883d99127437ebe4f0423a181f01b/transport/` 多轮同锥检查；提醒到达时本轮五个旧策略检查已经完成。结果无负候选，**属于重复诊断，不是一般正面进展**，也不继续扩张扫描。

下一步应攻击 (B?) 或直接在 TOTAL 中利用真实后继理性支付总债；仅增加旧锥或特殊人数没有解决此义务。
