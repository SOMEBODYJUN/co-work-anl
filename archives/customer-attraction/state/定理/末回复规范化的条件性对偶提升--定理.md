---
id: "customer-attraction/terminal-reply-conditional-dual-lift"
kind: "theorem"
type_tag: "定理"
title: "末回复规范化的条件性对偶提升与有向无环转移"
status: "complete"
truth_status: "conditional-theorem-proved-universal-input-certificate-open"
review_level: "algebraic-reconstruction-and-two-exact-replays"
scope: "任意n≥2；有限非空共同主题标签目录；全部有序历史形式纯策略；全部非空客户兴趣类型"
legacy_ids:
  - "CA-TERMINAL-REPLY-DUAL-LIFT"
summary: "保留根覆盖的末层规范化，其早期激励误差恰是incumbent份额转移；给定规范化证书且余项足以支付该张量时，可显式提升到原完整策略。转移图为DAG，非代表守恒仅是零债的充分机制。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/terminal_reply_transport.md#1-末节点的真实行与-incumbent-转移"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/terminal_reply_transport.md#3-ca-terminal-reply-dual-lift-的精确陈述和构造"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/terminal_reply_transport.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/terminal_transport_source.md#5-构造式-dual-提升引理"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/terminal_transport_source.md"
---

# 末回复规范化的条件性对偶提升与有向无环转移

## 全类型行与完整历史量词

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。有限单位客户、有限非空共同主题目录、单位权提供者依次观察全部有序历史各选一个主题；空主题、重复行动、零客户和任意离轨平局均保留。以下用有限标签集 $\mathcal L$ 表示目录，亦可处理同覆盖不同标签的表示扩展；对原集合目录选唯一标签即可。

固定 $n\ge2$ 和定义于全部有序历史的**形式**纯策略 $\sigma$，暂不假定它在某实例上是SPE。每个非空兴趣类型 $T\subseteq\mathcal L$ 的质量为 $w_T\ge0$；整数质量表示不同单位客户，有理质量可清分母展开。完全不喜欢目录中任何主题的客户贡献零。所有向量恒等式均在全部类型列上成立，先于代入任何质量；有符号辅助质量不属于合法客户输入。

令 $z_h$ 是从有序节点 $h$ 沿原 $\sigma$ 完成的终局，$z_{ha}$ 是当前改选 $a$ 后仍沿同一原策略真实完成的终局。当前玩家位置为 $|h|+1$，其真实收益比较行为

\[
\Gamma_{h,a;T}
=\frac{\mathbf1_{\sigma(h)\in T}}{\operatorname{load}_{z_h}(T)}
-\frac{\mathbf1_{a\in T}}{\operatorname{load}_{z_{ha}}(T)}.
\]

零分子项为零，非零分子时终局含该玩家行动，分母为正。于是 $w\ge0,\Gamma w\ge0$ 恰是给定完整策略的SPE客户锥，见[完整策略锥](固定完整策略的客户重数锥--定理.md)。比较时所有中间玩家均按偏离历史上的原真实行动执行，绝不冻结在轨后继。

对末位前缀 $\ell\in\mathcal L^{n-1}$ 定义

\[
p_{\ell,T}=\sum_{j<n}\mathbf1_{\ell_j\in T},\qquad
a_\ell=\sigma_n(\ell),\qquad
L_\ell(b)_T=\frac{\mathbf1_{b\in T}}{p_{\ell,T}+1}.
\]

若 $\ell,g$ 有相同**主题计数**，则全部类型的 $p_\ell=p_g$，且

\[
\Gamma_{\ell,a_g}=L_\ell(a_\ell)-L_\ell(a_g)
=-\Gamma_{g,a_\ell}. \tag{1}
\]

因此此互反向量的任意实数倍均可由这两条原真实行用非负乘子表示：正倍用第一行，负倍用第二行。在原SPE客户锥中，两行各自非负且互为相反，故总收益slack均为零。若仅在某个给定实例的正质量客户上同负载，只能推出该实例的末位收益相等，不能推出全类型式(1)。

## incumbent转移、覆盖恒等式及锐预算

把前缀 $\ell$ 的末回复从 $a$ 换成 $b$。对前缀中已选主题 $S$ 的一位玩家，其新最终收益减旧最终收益为

\[
\delta_{\ell,S}(a\to b)_T
=\frac{\mathbf1_{S\in T}(\mathbf1_{a\in T}-\mathbf1_{b\in T})}
{p_{\ell,T}(p_{\ell,T}+1)}. \tag{2}
\]

分子为零取零；非零时 $S$ 确实出现在 $\ell$ 中，故 $p_{\ell,T}\ge1$。记 $q_\ell(S)$ 为前缀中 $S$ 的出现次数。将所有前缀玩家计入，包括重复主题的各个位置，得到

\[
\Delta P_\ell=\sum_Sq_\ell(S)\delta_{\ell,S}
=\mathbf1_{p_\ell>0}\frac{\mathbf1_a-\mathbf1_b}{p_\ell+1}.
\]

这里 $P$ 是全部前缀玩家的**最终收益之和**。若末位收益变化为 $\Delta L=L_\ell(b)-L_\ell(a)$，完整覆盖向量满足

\[
\boxed{\Delta c_\ell=\Delta L+\Delta P_\ell
=\mathbf1_{p_\ell=0}(\mathbf1_b-\mathbf1_a).} \tag{3}
\]

证明只需逐类型区分 $p=0$ 和 $p>0$：前者没有前缀份额，后者覆盖不变、末位与前缀份额变化相反。故并列末位收益相同，并不意味着终局覆盖相同。

若 $a,b$ 在某个合法质量 $w$ 上均为末位最佳回复，设共同末位收益为 $v$，前缀覆盖客户集为 $C_\ell$，则

\[
|\Delta W_\ell|
\le\sum_{T:p_{\ell,T}>0}\frac{w_T}{p_{\ell,T}+1}
\le |C_\ell|/2. \tag{4}
\]

因为 $\Delta L\cdot w=0$，对式(3)中的 $\Delta P$ 取绝对值即可。该预算属于**这个可能离轨的前缀**，其客户可以包含根路径遗漏的最优客户，不能直接记入根实际 $W$。

对单个incumbent，若旧最终收益系数为 $u_{S,old,T}$，式(2)进一步给逐类型的**不对称**预算

\[
(-\delta_{\ell,S,T})_+\le u_{S,old,T}/2,\qquad
(\delta_{\ell,S,T})_+\le u_{S,old,T}. \tag{5}
\]

损失是分母 $p\to p+1$，损失/旧收入为 $1/(p+1)\le1/2$；增加是分母 $p+1\to p$，增加/旧收入为 $1/p\le1$。将全部玩家、客户的正负转移分别求和为 $G,L$，旧前缀总收益为 $P_{old}$，则并列末回复下

\[
G\le\min\{v,P_{old}\},\qquad
L\le\min\{v,P_{old}/2\}. \tag{6}
\]

其中 $G$ 的客户贡献等于旧末位在这些旧覆盖客户上的份额，$L$ 等于新末位在这些客户上的份额，分别至多 $v$；式(5)给另两界。不能把两方向都改为 $v/2$。

**锐例。** 两人、两个不交主题 $A,B$，大小为 $2m,m$，$m\ge1$。根选 $A$；在 $B$ 后末位选 $A$；在 $A$ 后选 $A$ 或 $B$ 都给完整SPE。末位在 $A$ 后的两查询均得 $m$，在 $B$ 后选 $A,B$ 分别得 $2m,m/2$；根在两策略中选 $A$ 的收益分别为 $m,2m$，改选 $B$ 都得 $m$。两个终局 $AA,AB$ 覆盖为 $2m,3m$，末位收益同为 $m$，覆盖转移 $m=|C_A|/2$，调和势均为 $3m$。静态安全值恰 $v_2=m$：查询 $A$ 可保证 $m$，固定竞争者 $A$ 又使任意查询至多 $m$。因此单叶覆盖转移可为 $v_2$，不能按 $v_2/2$ 封顶；反向转移达到 $L=v=P_{old}/2$。此例仍满足弱安全值桥，亦非half反例。

## 保留根覆盖的末层规范化

对长度 $n-1$ 的每种主题计数 $q$ 选代表有序历史 $g(q)$。根实际末位前缀为 $\ell_0$，特别选 $g(q(\ell_0))=\ell_0$。令 $b_q=\sigma_n(g(q))$。定义 $\bar\sigma$：前 $n-1$ 位在**每个历史**的行动保持原值，末位在 $\ell$ 改选 $b_{q(\ell)}$。根实际早期路径及实际末回复都保持，故

\[
\bar c=c \quad\text{逐类型成立。} \tag{7}
\]

在原策略锥内，由式(1)，规范化后的末节点仍最佳回应；早期节点未必最佳回应。以下固定
$\delta_{\ell,S}=\delta_{\ell,S}(a_\ell\to b_{q(\ell)})$，代表历史上的所有 $\delta$ 都为零。

在早期节点 $h$，令 $S_h=\sigma(h)$；$\ell_h$ 是从 $h$ 沿原策略到末位前的前缀，$\ell_{ha}$ 是在 $h$ 改选 $a$ 后沿原策略到末位前的前缀。所有中间动作仍是真实续局。由式(2)，

\[
\boxed{\bar\Gamma_{h,a}=\Gamma_{h,a}
+\delta_{\ell_h,S_h}-\delta_{\ell_{ha},a}\quad(|h|<n-1).} \tag{8}
\]

在末位节点 $\ell$，写 $g=g(q(\ell))$，则

\[
\boxed{\bar\Gamma_{\ell,t}=\Gamma_{\ell,t}+\Gamma_{g,a_\ell}.} \tag{9}
\]

第二行相加就是 $L_\ell(b_q)-L_\ell(t)$；两项都是原策略真实行，系数均为 $+1$。式(8)的早期incumbent变化才是未必非负的误差，末位的互反行已经完全支付。

## 条件性提升定理及显式构造

固定任意目标类型向量 $d$。假设已经给出规范化**形式**策略的恒等式

\[
d=\bar\Gamma^{\mathsf T}\lambda+r,\qquad\lambda\ge0,\quad r\ge0.
\]

不要求 $\bar\sigma$ 在原质量上为SPE。令

\[
E(\lambda)=\sum_{|h|<n-1,a}\lambda_{h,a}
(\delta_{\ell_h,S_h}-\delta_{\ell_{ha},a}). \tag{10}
\]

**定理。** 若 $r+E(\lambda)\ge0$ **逐类型**成立，则可显式构造 $\lambda'\ge0$，满足

\[
\boxed{d=\Gamma^{\mathsf T}\lambda'+r',\qquad
r'=r+E(\lambda)\ge0.} \tag{11}
\]

构造从零乘子开始：每个早期行 $(h,a)$ 的 $\lambda_{h,a}$ 加到原同一行；每个末行 $(\ell,t)$ 的乘子，同时加到原行 $(\ell,t)$ 和 $(g(q(\ell)),a_\ell)$。收到多份的原行相加，全部乘子非负。对式(8)–(9)按原乘子求和，即得到(11)。这个证明不调用Farkas，不以目标已真来保证输入证书存在，也不把各历史的偏离预先平均。

目标可取 $d=2c-o$，其中 $o$ 是任意 $n$ 个合法比较主题的并集向量；式(7)保证规范化未更换根覆盖目标。亦可取

\[
d=c-\alpha\sum_BQ_B\beta_B(p),\qquad
\beta_B(p)_T=\frac{p(T)}{1+\operatorname{load}_B(T)}.
\]

这里 $p$ 是查询主题分布，$Q$ 是不观察本次查询的合法 $n-1$ 主题元组分布；提升保持同一 $Q,p$，包括 $\alpha=n-1/2$。定义和一般对偶接口见[完整策略锥静态安全值对偶](完整策略锥的静态安全值对偶--定理.md)。本定理没有给所有策略和目标构造输入 $\lambda,r,Q$。

## 转移图与DAG不变量

以 $(\ell,S)$ 为顶点，要求 $S$ 出现在 $\ell$。每个早期真实偏离行给有权边

\[
(\ell_{ha},a)\longrightarrow(\ell_h,S_h),\qquad
\text{权重 }\lambda_{h,a}.
\]

记入流减出流为 $\kappa_{\ell,S}$，则

\[
E(\lambda)=\sum_{\ell,S}\kappa_{\ell,S}\delta_{\ell,S}. \tag{12}
\]

所有非代表顶点若满足 $\kappa=0$，代表顶点因 $\delta=0$ 可提供或吸收净流，便有 $E=0$。这是跨多个节点消去转移债的一种**充分条件**，不是必要条件；非代表顶点自身也可能 $\delta=0$，不同张量也可能抵消。一般只需要式(10)与 $r$ 合并非负。[三客户例](../反例/保留根覆盖的末回复规范化破坏SPE--反例.md)具体给一条非代表源边而 $E=0$。

定义相对于原策略的偏离次数

\[
D(\ell)=|\{j<n:\ell_j\ne\sigma_j(\ell_1,\ldots,\ell_{j-1})\}|.
\]

由于到达 $h$ 后的两个分支都继续沿原策略执行，

\[
D(\ell_h)=D(h),\qquad
D(\ell_{ha})=D(h)+\mathbf1_{a\ne S_h}. \tag{13}
\]

所以从图源 $\ell_{ha}$ 到图目标 $\ell_h$，每条非自偏离边使 $D$ 恰下降一；自行动行是同一顶点的零行。此图无非平凡有向循环，每条非平凡路径长至多 $n-1$。若采用非代表守恒机制，非零净源、净汇只能位于代表历史；不能靠一个假想全局循环自动消债，也不能把这一充分机制反说为零 $E$ 的必要条件。

[末两人回复循环运输](末两人回复循环静态运输恒等式--定理.md)的循环发生在主题图 $a\mapsto\sigma_n(Pa)$。其平稳概率 $\pi$ 给

\[
u_{n-1}(P)-\sum_a\pi_a f_{P+a}(t)
=\sum_a\pi_a(\Gamma_{P,a}+\Gamma_{Pa,t}). \tag{14}
\]

它用两人收益差的单主题函数差消去局部误差，与式(13)的DAG是两张不同的图。若先规范化、再按规范化回复图选择 $Q$，式(8)还会产生 $E$；不能默认原回复图自己的合法 $Q$ 会支付规范化 $Q$ 的转移。联合使用时尚需控制不同前缀间的 $Q$ 质量转移和incumbent张量。

## 边界、状态和接续

$n=1$ 不需规范化：对比较主题 $t$，$\Gamma_{\varnothing,t}=c-o$，故 $2c-o=\Gamma_{\varnothing,t}+c$，是显式非负证书。任意 $n$ 的根福利 $W=0$ 情形，根偏离任一主题至少得该主题大小除以 $n$；SPE使全部主题大小为零，故 $\operatorname{OPT}_n=0$，无需定义 $0/0$。

完整[三客户SPE](../反例/保留根覆盖的末回复规范化破坏SPE--反例.md)说明即使逐类型保留根覆盖，规范化仍可把早期比较变为负值。式(10)中实际分支 $\ell_h$ 的**损失**可按半旧收入计，但偏离分支 $\ell_{ha}$ 的**增加**带负号，只能用全旧收入界。实际分支是图目标，偏离分支是图源，两套称呼不能混淆。

剩余的实质义务是：对每个原完整策略及比较portfolio构造规范化输入 $\lambda,r$，并证明 $r+\sum\kappa\delta\ge0$；或改用其他机制。没有这样的一般构造，条件定理不是普遍half或安全值桥证明。静态[锐目录计数](静态混合安全值的锐目录计数界--定理.md)使 $W\ge(n-1/2)v_n$ 足以half，但本模块没有支付这项总预算。主目标仍是任意六人完整纯SPE的 $2W\ge\operatorname{OPT}_6$。

[双实现资源](../计算/末回复转移与条件提升的精确核验--计算.md)保存七份冻结原件、全部有限检查及本轮重放，区分普遍代数证明和有限系数回归，并记录数学审查中一项current文件SHA不匹配。原推导与最终页已修正图源/目标反置、代表端点必要性过强两处措辞；本轮逐式核对最终文本，不声称外部同行评审、全球新颖性或反例最小性。第三阶段关系应分别记录条件提升、规范化反例、局部循环比较及有限实现，不能把任何一项画成已完成一般六人证明。
