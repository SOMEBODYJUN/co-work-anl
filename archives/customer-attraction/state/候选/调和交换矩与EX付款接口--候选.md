---
id: customer-attraction/harmonic-exchange-ex-interface
kind: candidate
type_tag: 候选
title: 调和交换矩与 EX 付款接口
status: exact-static-identities; positive-loss-payment-open
truth_status: conditional-interface
---

# 调和交换矩与 EX 付款接口

设 \(m\ge1\)，实际 \(m\) 槽元组为 \(a\)，达到 \(\mathrm{OPT}_m\) 的元组为 \(o\)，覆盖集合分别为 \(A,O\)。记 \(c_x,d_x\) 为两元组对客户 \(x\) 的覆盖次数。从 \(o\) 均匀删除 \(r\) 个索引槽，独立地从 \(a\) 均匀选择 \(r\) 个索引槽插入，\(0\le r\le m\)；重复主题仍按不同槽位抽样。越界二项式取零，则
\[
Q_r(c)=\frac{\binom{m-c}{r}}{\binom mr},\qquad
P_r(d)=\frac{\binom rd}{\binom md}.
\]
静态最优性逐 r 给出
\[
\sum_{x\in A\setminus O}(1-Q_r(c_x))
\le
\sum_{x\in O}P_r(d_x)Q_r(c_x).
\]
定义 \(H_j=\sum_{i=1}^j1/i\)，\(H_0=0\)。对 \(r=1,\ldots,m\) 以 \(1/r\) 加权，利用 Vandermonde 恒等式，得到
\[
\sum_{x\in A\setminus O}H_{c_x}
\le
\sum_{x\in O\setminus A}\frac1{d_x}
+\sum_{x\in A\cap O}K_m(c_x,d_x),
\]
其中
\[
K_m(c,d)=
\frac{\binom{m}{c+d}}
{d\binom mc\binom md},
\]
且 c+d>m 时为0。反向对 \(r=0,\ldots,m-1\) 以 \(1/(m-r)\) 加权，得到对应的 \(H_m-1/c\) 与 \(H_m-H_d\) 行。这些是静态身份，不含 SPE 续局。

支持缩减可用当前负载 c 的单槽势增量 v_c(T)=Σ_{x∈T}1/(c_x+1)；对候选最优支持 S 定义 J_c(S) 为增量总和加当前覆盖交集，并在达到 OPT 的支持中取最小值。等槽删插交换给出 EX 关系，但交换矩只能重排已有静态行。

真正未闭合的是 positive coverage-loss payment：删除最优槽可能损失 A∩O 或 A\O 客户，静态 R_r/H_r 行只平均该损失，不能自动提供一个真实离轨 SPE 续局来支付它。因而任何 F≤W+E 或 L≤W+E 形式的 half 结论都需要额外 EX 条件或结构假设。恒主题全树续局是一个可验证特殊情形；一般共享历史不满足该条件。不能把候选的 F、L 名称升级为普遍定理。

## 来源入口

- [静态等槽交换与调和矩证明](../引理/最优覆盖等槽交换的调和矩--引理.md)
- [支持归约及仍开放的交换义务](signed-harmonic支持归约与交换义务--候选.md)
