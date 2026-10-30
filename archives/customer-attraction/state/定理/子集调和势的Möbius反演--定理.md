---
id: "customer-attraction/boolean-harmonic-potential-inversion"
kind: "theorem"
type_tag: "定理"
title: "任意有理子集势的唯一调和客户反演"
status: "complete"
truth_status: "proved"
review_level: "self-contained-algebraic-reconstruction-and-exact-replay"
scope: "p≥1个主题标签；F:2^P→Q且F(空集)=0；有符号重数仅为辅助代数"
legacy_ids:
  - "CA-MOBIUS-BOOLEAN"
summary: "调和核H_|B∩S|在归零子集函数空间形成一组基；两次Möbius变换唯一恢复所有非空客户类型的有符号重数，并给完整计数扩张和边际收益。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/mobius_compiler.md#1-任意有理子集势的唯一有符号实现"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/mobius_compiler.md#6-实现规模及核验界限"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/customer_attraction/mobius_compiler.md#1-任意有理子集势的唯一有符号实现"
---

# 任意有理子集势的唯一调和客户反演

## 子集表与辅助计数势

令主题标签集 $P=\{0,\ldots,p-1\}$、$p\ge1$。给定任意有理函数 $F:2^P\to\mathbb Q$，要求 $F(\varnothing)=0$。置 $H_0=0$、$H_j=\sum_{i=1}^j1/i$。对每个非空兴趣类型 $B\subseteq P$ 引入有符号有理数 $x_B$，并对任意非负整数主题计数 $q\in\mathbb Z_{\ge0}^P$ 定义

$$
\Phi_x(q)=\sum_{B\ne\varnothing}x_BH_{\sum_{a\in B}q_a}.
\tag{1}
$$

这是[共同目录均分模型](../定义/共同目录完整历史模型--定义.md)的调和势形式，但 $x_B<0$ 时只是辅助代数，不是合法客户。非负整数重数才可以直接展开为不同单位客户；[正偏置与完整历史编译](无重复辅助博弈的完整历史编译--定理.md)另行处理合法化。

**M1。** 存在唯一一组 $x_B\in\mathbb Q$ 使

$$
\Phi_x(\mathbf1_S)=F(S)\qquad\forall S\subseteq P.
$$

其显式公式为：对非空 $A,B$，

$$
c_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}F(T),\qquad
z_A=(-1)^{|A|+1}|A|c_A,
$$
$$
\boxed{x_B=\sum_{A\supseteq B}(-1)^{|A|-|B|}z_A.}
\tag{2}
$$

空集客户类型完全不出现，也不通过给 $x_\varnothing$ 另加自由度改变结论。

## 完整反演与唯一性证明

归零子集函数有唯一多线性展开

$$
F(S)=\sum_{A\subseteq S}c_A,
$$

其中 $c_\varnothing=0$，其余系数正是(2)第一式。固定非空 $B$，函数 $S\mapsto H_{|B\cap S|}$ 的单项式 $A$ 系数在 $A\not\subseteq B$ 时为零；若 $A\subseteq B$、$k=|A|\ge1$，系数为

$$
\begin{aligned}
\sum_{j=0}^k(-1)^{k-j}\binom{k}{j}H_j
&=-\int_0^1\frac{(t-1)^k}{1-t}\,dt\\
&=\frac{(-1)^{k+1}}k.
\end{aligned}
\tag{3}
$$

第一步使用 $H_j=\int_0^1(1-t^j)/(1-t)\,dt$；常数部分由二项式交替和为零消去。因而(1)在 Boolean 计数上的 $A$ 系数是

$$
\frac{(-1)^{|A|+1}}{|A|}\sum_{B\supseteq A}x_B.
$$

要与 $c_A$ 相等，充要条件为 $\sum_{B\supseteq A}x_B=z_A$。上集 Möbius 反演唯一给出(2)，证明存在与唯一性。$F(\varnothing)=0$ 是必要条件，因为每个调和核在空集均为零；也是上述构造充分的唯一归一化条件。

## 从子集势到真正的边际收益对象

对任意计数 $q$ 和满足 $q_a>0$ 的标签 $a$，定义该标签一位玩家的辅助收益

$$
u_a^x(q)=\sum_{B\ni a}\frac{x_B}{\sum_{b\in B}q_b}.
$$

由 $H_d-H_{d-1}=1/d$ 逐类型得到

$$
\boxed{u_a^x(q)=\Phi_x(q)-\Phi_x(q-e_a).}
\tag{4}
$$

非零分子时分母至少一。若 $q=\mathbf1_S$，则收益恰为 $F(S)-F(S\setminus\{a\})$。因此M1可编译任意归零子集势所定义的边际收益游戏；它没有允许任意指定全部玩家收益表。

对早期顺序玩家，原动作与偏离的真实后继可能到不同计数 $q,r$。相应比较是(4)的两个势差，而不是 $\Phi_x(q)$ 与 $\Phi_x(r)$ 的大小。完整有序历史及任意离轨平局仍须单独处理。

M1还唯一固定了所有重复计数的调和扩张 $\Phi_x(q)$；不能在 Boolean 表已定后任意补填重复势值。具体相容性障碍、非负可实现性及单调次模反例见[匿名计数势相容性](../障碍/匿名计数势的客户相容性--障碍.md)。

## 精确算法、规模和位长

对显式长度 $2^p$ 的有理表，可先作下集快速 Möbius 变换得到 $c_A$，逐非空坐标乘 $(-1)^{|A|+1}|A|$ 得 $z_A$，再作上集快速 Möbius 变换得到 $x_B$。两变换共 $O(p2^p)$ 次精确加减，辅助空间 $O(2^p)$ 个有理数。实现把空类型坐标归零，其值不被当成客户。

设输入表所有分母的公倍数为 $D$，可先对 $DF$ 反演；(2)只有整数加减及乘整数，所以输出为整数 $Dx_B$。取分母乘积已经给 $\log D$ 不超过显式输入各分母位长之和，无需把 $D$ 当作数值大小多项式。对 $|F(S)|\le L$ 的整数表，有

$$
|c_A|\le2^{|A|}L,\quad |z_A|\le p2^pL,\quad
|x_B|\le p4^pL.
$$

所以反演、清分母及充分偏置的整数位长对显式表输入位长为多项式。这里没有关于主题数 $p$ 单独的多项式输入或运行时间承诺，因为完整子集表本身长 $2^p$。压缩整数重数只需写其二进制表示；若逐名展开单位客户，人数可以很大，不能把两种输出规模混用。

## 证据、来源和接续

[精确核验资源](../计算/子集势编译的精确核验--计算.md)保全原字节程序及冻结报告，本轮复跑核验24份确定种子表、全部 Boolean 值、8976项计数边际、1284项无重复偏置收益。有限回归检查实现；普遍结论由(2)–(4)证明。

来源 `mobius_compiler.md` §§1、6，源ID `4310a8b619c1e3dc40ba`；两冻结版本相同。原稿将双反演原型归于上传 `exact_spe.py::auxiliary_counterexample`，该实现的历史比较已有[完整求解器资源](../计算/完整历史求解器的精确复现--计算.md)登记。本对象保存原稿自足证明，不从“仓内未检索到同构造”推出全球新颖性；无外部同行评审认证。

本定理是[完整历史编译](无重复辅助博弈的完整历史编译--定理.md)的代数前提；后者再引入正偏置和严格fresh支配。既有[真实菜单障碍](../障碍/自适应后继与真实菜单安全值--障碍.md)使用其特定两组子集势应用，不穷尽本定理的输入。后续可据此设计辅助势，但必须继续核实合法客户、所有真实续局和福利失真，而非把有符号表当作原模型反例。
