---
id: "customer-attraction/last-slot-value-and-catalog-counting"
kind: "lemma"
type_tag: "引理"
title: "末位最坏背景值、前缀嵌入与目录计数界"
status: "complete"
truth_status: "proved"
review_level: "semantic-and-algebraic-reconstruction"
scope: "有限非空共同目录、单位客户；任意正剩余人数；非负整数背景"
summary: "区分纯背景最坏最佳回应θ与隐藏抽样安全值v，证明θ的前缀嵌入、根覆盖下界及同背景最优剩余利润界。"
legacy_ids:
  - "CA-LAST-TWO-FLOOR:last-slot-numerical-lemma"
  - "CA-LAMINAR-INCIDENCE-THETA:LI12-LI13"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/last_two_floor.md#1-全局末位保底"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/laminar_incidence_bound.md#6-a-universal-immediate-payoff-counting-bound"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/extreme_maximal_membership_floor.md#任意合法背景的最优剩余利润"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/oblivious_security.md#4-与末位-θ-的区别以及尚缺的-spe-桥"
---

# 末位最坏背景值、前缀嵌入与目录计数界

## 1. 对象与量词

使用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。设客户集有限，目录
$\mathcal S$ 有限非空，客户及提供者均为单位权。背景负载为 $b_x\in\mathbb Z_{\ge0}$，尚有 $r\ge1$ 人。
对一个由 $r-1$ 个合法主题组成的有序元组 $H$，记客户负载为 $d_H(x)$，定义

$$
f_{b,H}(A)=\sum_{x\in A}\frac1{b_x+1+d_H(x)},\qquad
\theta_r(b)=\min_{H\in\mathcal S^{r-1}}\max_{A\in\mathcal S}f_{b,H}(A).
\tag{1}
$$

$r=1$ 时元组域只有空元组。这里对手先选一个确定竞争组合，查询者再选择最佳主题；
历史顺序不影响式(1)的数值，但**不因此限制完整SPE在相同负载历史使用相同回复**。
重复主题、空主题及同覆盖不同标签均保留。背景无需来自均衡路径；下面静态代数甚至对任意非负整数向量成立。

若根总人数为 $n$，写 $\theta_n=\theta_n(0)$，并令
$K=\max_{A\in\mathcal S}|A|$、$O=\operatorname{OPT}_n$。
每个长度 $n-1$ 的合法历史后，真实末位的最佳回应收益至少为 $\theta_n$。
这个事实本身不给早期玩家最终收益的下界 $\theta_n$。

## 2. 固定真实前缀的嵌入

任取合法主题 $A$ 和 $r\ge2$，有

$$
\theta_{r-1}(b+\mathbf1_A)\ge\theta_r(b).\tag{2}
$$

左侧只把式(1)中的竞争元组限制为包含固定首项 $A$ 的元组，故最小化域变小。
反复应用即得任意较长真实前缀的相应下界。该比较保留“先定竞争组合，再取最佳查询”的量词顺序；
没有将两条有序历史的策略拼接。

## 3. 空背景的两个数值下界

对每个 $n\ge1$，

$$
\boxed{\theta_n\ge\frac O{2n-1}},\qquad
\boxed{\theta_n\ge\frac{2O-(n-1)K}{2n}}.\tag{3}
$$

固定长度 $n-1$ 的历史 $H$，令 $h_x=d_H(x)$，
$M(H)=\max_A\sum_{x\in A}1/(h_x+1)$。取达到 $O$ 的 $n$ 个合法比较主题，令其客户重数为 $o_x$。
逐客户有 $(o_x+h_x)/(h_x+1)\ge\mathbf1_{o_x>0}$，故

$$
O\le nM(H)+B(H),\qquad B(H)=\sum_x\frac{h_x}{h_x+1}.\tag{4}
$$

同一历史的每一项仍是合法查询，且按出现次数计入，因而

$$
B(H)=\sum_{j=1}^{n-1}\sum_{x\in H_j}\frac1{h_x+1}
\le(n-1)M(H).\tag{5}
$$

另一方面，整数 $h\ge0$ 满足 $h/(h+1)\le h/2$，所以

$$
B(H)\le\tfrac12\sum_xh_x
=\tfrac12\sum_{j=1}^{n-1}|H_j|\le\tfrac12(n-1)K.\tag{6}
$$

分别把(5)、(6)代入(4)，再对 $H$ 取最小，得到(3)。第二个下界允许为负，不添加虚假的正性假设。
同样的计数还给任意长度 $t$ 的前缀 $h$：

$$
(n+t)\max_A\sum_{x\in A}\frac1{1+h_x}\ge O.\tag{7}
$$

这正是最优组合与已选合法主题在同一分母下的联合预算。

## 4. 非零背景比较的是剩余利润

定义同背景的最优剩余利润

$$
F_r(b)=\max_{Q\in\mathcal S^r}\sum_{x:c_Q(x)>0}\frac{c_Q(x)}{b_x+c_Q(x)}.
$$

则在任意目录上都有

$$
\boxed{F_r(b)\le(2r-1)\theta_r(b)}.\tag{8}
$$

取任意比较组合 $Q$ 和静态竞争组合 $H$，逐客户写 $c=c_Q(x)$、$d=d_H(x)$、$b=b_x$。
当 $c=0$，左侧贡献按零处理；当 $c\ge1$，

$$
\frac{c+d}{b+d+1}-\frac c{b+c}
=\frac{c(c-1)+bd}{(b+d+1)(b+c)}\ge0.\tag{9}
$$

对客户求和，第一项是 $r$ 个比较主题及 $r-1$ 个竞争主题在同一背景下的查询值之和，
至多 $(2r-1)\max_A f_{b,H}(A)$。先取最优 $Q$，再取达到 $\theta_r(b)$ 的 $H$，即得(8)。
只有 $b=0$ 时 $F_r(0)=\operatorname{OPT}_r$；非零背景不能把剩余利润误称完整覆盖。

## 5. 与混合安全值及已整理税接口的关系

另一不同对象是

$$
v_r(b)=\max_{p\in\Delta(\mathcal S)}\min_{H\in\mathcal S^{r-1}}
\sum_Ap_A f_{b,H}(A).
$$

竞争组合不得观察抽样主题的实现。有限minimax或弱对偶给 $v_r(b)\le\theta_r(b)$。
两不交单客户主题、两人、空背景时，$\theta_2=1$，而对称混合给 $v_2=3/4$；
若查询主题1的概率为 $p$，两列期望为 $1-p/2$ 与 $(1+p)/2$，其较小值最大恰在 $p=1/2$。
故不能用一个符号替换另一个。源 `oblivious_security.md` 另以有限minimax和Jensen证明
$v_n(0)\ge O/(2n-1)$；这个更强静态安全值结论仍不自动提供观察偏离后的SPE收益桥。

式(4)与[末位收益税诊断](末位收益税诊断--引理.md)的 $O\le nv+\tau$ 是同一末节点计数，
本对象保留对**全部合法背景**取最小后的数值界与一般背景利润扩展。
[末两人逐人保底](../定理/末两人逐人保底与全人数弱福利界--定理.md)可使用(2)、(3)；
将保底传播到所有玩家需要额外结构或新的真实续局论证。

零客户、全空目录均给全部值为零；本文不定义 $0/0$ 效率比。
本次逐式核对整数性、分母和固定前缀嵌入；没有将有限枚举结果当作普遍证明。
