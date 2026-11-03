# 空根连续分数预算：非线性对偶与未付义务

2026-10-24。工作备份，未独立审查。此页只给静态表示和准确的开放义务；**不记作新增一般正向付款**，也不把等价变形当作 half 进展。

## 1. 可留下的弱化目标

仍用 [前页](fractional_background_floor_corollary.md) 的 f_m(0)。任意背景个体式已被原 PB-extra 构造分离；下列原根聚合式是不同的候选：

\[
W\ge m f_m(0).\tag{RF?}
\]

已证静态 OPT_m≤2m f_m(0)，所以 (RF?) 足以推出 half。f_m(0)≤v_(m+1)(0)，故它比真正 extra-slot 安全值聚合还弱；不能由个体安全值、任意背景或 iid 桥失败直接否定它。

本分支没有证明 (RF?)，也没有给出反例。把它直接代入 m=5，只有正确的条件蕴含 OPT_5≤10 f_5≤2W；第二个不等式仍是未付义务，不能称五人压力测试已过。

## 2. 一个精确的非线性静态对偶

对 p∈Δ(S) 记 a_x=Σ_(T∋x)p_T。对任意非零向量 h≥0，记 H=Σ_x h_x 及 L(h)=max_TΣ_(x∈T)h_x。则

\[
\boxed{
f_m(0)=\max_{p\in\Delta(S),\ h\ge0,\ h\ne0}
\frac{\left(\sum_x\sqrt{a_x h_x}\right)^2}{H+mL(h)}.
}\tag{1}
\]

全零客户时双方定义为零。无覆盖客户可删去，不影响该式。此式不使用 SPE。

证明先对有限查询单纯形与分数负载单纯形用凸凹 minimax：

\[
f_m(0)=\max_p\min_q\sum_x\frac{a_x}{1+m q_x}.
\]

再用逐客户恒等式

\[
\frac{a}{1+t}=\max_{y\ge0}\{2\sqrt a\,y-(1+t)y^2\}.
\]

所有 a≤1、t≥0，逐坐标最大点 y=√a/(1+t)≤1，因此换序时可先限制 y∈[0,1]^N，得到合法紧凸域；也可由统一 coercivity 截断后换序。于是对固定 p，

\[
\min_q\sum_x\frac{a_x}{1+m q_x}
=\max_{y\ge0}\left[
2\sum_x\sqrt{a_x}\,y_x-\sum_xy_x^2
-m\max_T\sum_{x\in T}y_x^2\right].
\]

写 y_x=√(t h_x)，先对尺度 t≥0 最大化，目标是 2√t A−t(H+mL)，其最大值 A²/(H+mL)。这就是 (1)。

因此 (RF?) 精确地等价于以下全部 p,h 的容量不等式：

\[
m\left(\sum_x\sqrt{a_x h_x}\right)^2
\le W\,[H+mL(h)].\tag{2?}
\]

这种表示把整数背景或它的独立随机化换成了平方根耦合的客户价格；仍没有任何真实 SPE 比较付款。尤其不能从 (1) 的 minimax 或最优性条件循环推出 (2?)。

## 3. 本轮没有形成的连接

曾尝试在真实根菜单 Z(A) 上取均值负载，并控制

\[
C_{\rm frac}(p)=\sum_x
\frac{a_x}{1+\mathbb E_{A\sim p}c_x(Z(A))}.
\]

但没有解析证明 u_root≥C_frac(p)，更没有从单个根推广到原全部实际位置。强式 E_A d(A)≥C_frac(p) 也不能凭直觉使用：既有带空主题的 34 客户强推送反例，其小概率查询机制在一阶上仍适用于分数均值分母。

具体地，p(E)=1−ε、p(T)=ε 时

\[
\mathbb E d(A)=\varepsilon d(T),\qquad
C_{\rm frac}(p)
=\varepsilon\sum_{x\in T}\frac1{1+c_x(Z(E))}+O(\varepsilon^2).
\]

原例 T=X2 有 d(T)=29/3，插入 Z(E) 的值32/3，故对足够小正 ε，强式仍严格失败。来源是
`R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_D_lt_C.md`。
这不是 (RF?) 或以根最大利润 u_root 付款的反例。

另一个临时加强“任意 m 个比较主题的真实根强制收益和至少为其并集一半”立即被目录 {B,E}、全历史选 B 的 SPE 否定：m≥3、比较元组 (B,E,…,E) 的和仅 |B|/m，且它本身仍最优。故不能不检查重复和冗余就从个体 max 目标换成任意 tuple 平均目标。该观察没有否定有利选最优 tuple 的版本，也不影响原根 u_i≥OPT_m/(2m) 候选。

上述静态对偶、根聚合和一阶诊断没有组成新的付款机制；本轮一般主线的已证范围不变。
