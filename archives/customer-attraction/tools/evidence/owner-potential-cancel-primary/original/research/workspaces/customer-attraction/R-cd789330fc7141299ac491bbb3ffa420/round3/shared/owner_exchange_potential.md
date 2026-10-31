# 最优并集的 owner 分块势：全部客户关联下的一次共同预算

2026-10-23，shared 提出；root 与 relay 在读正文前独立重构通过。一般单位客户、任意人数、任意有限共同目录、所有空及重复主题均保留。本文是自足的通用代数组件，不使用 SPE 推出额外最优性；跨真实 rollout 的支付仍未闭合，**Q-CAG-HALF 仍 OPEN**。无外审或新颖性认证。

## 1. owner 只薄化分析基线，不薄化真实动作

固定人数 m≥1、最优合法主题元组 T=(T_1,…,T_m)，其并集为 O、大小为 OPT_m。对每个 x∈O，固定一个含它的最优槽 o(x)，并令

\[
Q_i=\{x\in O:o(x)=i\}\subseteq T_i.
\]

Q_i 互不交，合并为 O。Q_i 可以不是合法目录主题。它们**只用于静态最优性基线**，从不作为玩家的偏离或规定行动；所有真实主题保留原来对每个客户的全部兴趣。

任取 m 个合法真实或虚拟终局动作 B=(B_1,…,B_m)，分析时允许部分槽为空。独立以概率 p 逐槽将 Q_i 替换成 B_i。把任一实现中的所有未替换 Q_i 扩为合法 T_i，并把虚拟空动作补为任意合法主题，覆盖只会增加；所得为合法 m 槽组合，覆盖不超过 |O|。所以每个 Q/B hybrid 的覆盖仍不超过 |O|，而全 Q 基线恰覆盖 O。

这是允许 owner 分块的关键。并未假定目录对取子集封闭，也未把实际遗漏变成全局私有客户。

## 2. 全局有限势

写 c_x=|{i:x∈B_i}|，H_c=Σ_{k=1}^c1/k，H_0=0。称 owner 已覆盖 x 当且仅当 x∈B_{o(x)}；即使其它动作覆盖了 x，owner 仍可能未覆盖。

Q/B hybrid 对 x∉O 的新增覆盖概率是 1−(1−p)^{c_x}。对 x∈O，若 owner 已覆盖，它永远不会丢失；否则丢失概率是 p(1−p)^{c_x}。因此

\[
\sum_{x\notin O}[1-(1-p)^{c_x}]
\le\sum_{\substack{x\in O\\x\notin B_{o(x)}}}
p(1-p)^{c_x}.
\]

对 0<p<1 除以 p 并积分得到

\[
\Phi_Q(B):=\sum_{x\notin O}H_{c_x}
-\sum_{\substack{x\in O\\x\notin B_{o(x)}}}\frac1{c_x+1}
\le0.
\]

定义

\[
F_Q(B)=|O|+\Phi_Q(B).
\]

F_Q(空)=0。它也等于 Q/B hybrid 相对 Q/空 hybrid 的期望覆盖增加量除 p 后的积分，所以 F_Q 单调且非负。故

\[
\boxed{0\le F_Q(B)\le |O|.}\tag{POT}
\]

这是所有真实叶共用的有限基线；不会随叶重置支撑。对固定硬币实现，其积分被积式是带固定基线的覆盖函数，所以 F_Q 还有单调次模的带槽动作扩展。上界(POT)仅要求输入槽数不超过 m；不对不可行的多动作同槽扩展声称此上界。

## 3. 精确的原单位收益分解

把 B 第 i 槽置空得 B^{−i}。定义真实单位边际

\[
\ell_i(B)=F_Q(B)-F_Q(B^{-i}),\qquad
e_i(B)=u_i(B)-\ell_i(B).
\]

只需看 x∈B_i，此时 c_x≥1。逐客户闭式如下；其它客户边际及收益都为零。

| 客户情形 | \(\ell_i(B;x)\) | \(e_i(B;x)\) |
| --- | ---: | ---: |
| x∉O | 1/c_x | 0 |
| x∈O，i=o(x) | 1/c_x | 0 |
| x∈O，i≠o(x)，owner 已覆盖 | 0 | 1/c_x |
| x∈O，i≠o(x)，owner 未覆盖 | 1/[c_x(c_x+1)] | 1/(c_x+1) |

前三种由调和差分或 owner 是否仍覆盖直接得到。最后一种的势变化为 1/c_x−1/(c_x+1)=1/[c_x(c_x+1)]。所以对任意真实单位槽

\[
\boxed{u_i(B)=\ell_i(B)+e_i(B),\quad
0\le\ell_i(B)\le u_i(B),\quad e_i(B)\ge0.}\tag{UNIT}
\]

e 仅由 O 内客户贡献；O 外的原单位收益被同一个全局势**精确**表示。

## 4. 同一个实际叶的 I/G 联合预算

令 C_B 为 B 的覆盖，I_B=C_B∩O、G_B=C_B\\O，定义

\[
\kappa_Q(B)=
\sum_{\substack{x\in I_B\\x\in B_{o(x)}}}\frac1{c_x}
+\sum_{\substack{x\in I_B\\x\notin B_{o(x)}}}\frac1{c_x+1}.
\]

由上表逐客户精确相加：owner 已覆盖时总边际为 1/c；owner 未覆盖时 c 个非owner边际之和为 1/(c+1)。因此

\[
\boxed{\sum_i\ell_i(B)=|G_B|+\kappa_Q(B),\qquad
\sum_i e_i(B)=|I_B|-\kappa_Q(B).}\tag{JOINT}
\]

两项相加恰为原福利 |G_B|+|I_B|，没有给两份利润分别各领一个 W。特别地，在实际 SPE 叶 B=Z 中，G、I 都是原实际客户集合，误差总信用严格为 I−κ，而不只是粗上界 I。

在同一叶还可写成直接保留遗漏 D_B=O\\C_B 的势式

\[
\Phi_Q(B)=\sum_{x\in G_B}H_{c_x}
-|D_B|-
\sum_{\substack{x\in I_B\\x\notin B_{o(x)}}}\frac1{c_x+1}.
\]

它只标定当前叶，不许可不同离轨叶各自领实际 G；离轨 O 外客户的支持可以不同。

## 5. first-owner 与合法 OPT 前缀的重复信用

现在固定 T 的顺序，把 o(x) 选成该顺序中首次覆盖 x 的槽。Y_i 是强制 T_1,…,T_i 后沿原完整策略的真实 rollout。当前查询仍是原**合法** T_i，不是 Q_i。设原最优元组对 x 的覆盖次数为 a_x。

第一次查询 x 的当前槽就是 owner，故 UNIT 给 e_i(Y_i;x)=0。以后第 k 次查询 x 时，较早 owner 槽已经被真实强制并覆盖 x，当前为非owner；其误差为 1/c_x(Y_i)，而 c_x(Y_i)≥k。于是

\[
\boxed{\sum_{i:x\in T_i}e_i(Y_i;x)
\le\sum_{k=2}^{a_x}\frac1k=H_{a_x}-1\le a_x-1.}\tag{REPEAT}
\]

a_x=1 时左端精确为零。该界比未薄化基线的 H_{a_x−1} 更小。证明只用真实最优前缀的固定槽，不限制后继主题；所有后继仍可沿原完整策略任意改变。

同叶(JOINT)和跨最优前缀(REPEAT)控制的是不同对象。后者不控制每个规定 rollout 的全部 e，也不把离轨 I_B 替成实际 I。

## 6. 对一般目标的接口与准确开放点

原完整 SPE 的每条真实比较可原样写成

\[
\ell_i(Z)+e_i(Z)\ge\ell_i(Y)+e_i(Y).
\]

这是原 IC 的代数分解，没有任意重加权被积式。现在有同一实际叶的一次 I−κ 与 G+κ 预算，以及真实最优前缀的比较重复信用。要推到

\[
|O\setminus C|\le|O\cap C|+2|C\setminus O|,
\]

仍须支付两条互斥真实 rollout 的 \(\Phi_Q\) 去槽差，或者构造不会重复访问实际单位收益容量的客户流。本文未证明该支付。

整个论证须固定一次全局 owner 与槽配对；若为了 first-owner 更换最优排列，应同时固定相应 owner 势。不能每条查询另挑 owner 后把不同势当作同一势望远镜。Q_i 始终仅为分析基线，不能拿它当合法偏离来调用 SPE。
