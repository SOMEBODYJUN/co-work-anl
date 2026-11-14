# 数学支持片段：整数弦、Bernoulli 支持与动态边界

## 精确可复用结论

设 (K\ge1) 个不交单客户主题、(r=qK+s) 个静态竞争槽，(0\le s<K)。对
任意不看 query 的联合背景 (Q)，查询 (j) 的付款为

\[
 g(H_j)=\frac1{1+H_j},\qquad \sum_{j=1}^K H_j=r.
\]

M64 的整数割线恒等式是

\[
g(h)-\left(\frac1{q+1}-\frac{h-q}{(q+1)(q+2)}\right)
 =\frac{(h-q)(h-q-1)}{(h+1)(q+1)(q+2)}\ge0
\quad(h\in\mathbb Z_{\ge0}).
\]

对所有查询求和并除以 (K)，得到

\[
\max_j\mathbb E_Q g(H_j)\ge
 V_{K,r}:=\frac{K-s}{K(q+1)}+\frac{s}{K(q+2)}.
\]

固定 (s) 个 (q+1) 负载、其它 (q) 负载，并均匀循环平移标签，给出一个相关
背景使每个查询恰为 (V_{K,r})。因此

\[
v_m=V_{K,r}
\]

对所有 (K,r) 成立。

对 product (p_1\otimes\cdots\otimes p_r)，若 cap 也等于 (V_{K,r})，上界余项
逐项取零，故 (H_j\in\{q,q+1\}) 几乎处处。每个 (H_j) 是跨槽独立 Bernoulli
和；若有两个非退化命中项，则和的中间整数带正概率，矛盾。于是每个主题恰有
 (q) 个确定命中槽及一个命中概率 (s/K) 的非退化槽。余下 (s) 槽的正支持两两
不交并覆盖 (K) 标签，每槽支持大小 (K/s)，所以 (s\mid K)。反向将标签分为
 (s) 个大小 (K/s) 的块并令每个余槽在其块内均匀，得到 product 取等。结论为

\[
v_m^{\rm prod}=v_m\quad\Longleftrightarrow\quad s=0\text{ 或 }s\mid K,
\]

若 (s\nmid K)，紧致性把“无取等 product”升级为严格 (v_m^{\rm prod}>v_m)。

## 可引用的特殊值与不应跨越的层级

在 (K=3,r=2)（(q=0,s=2)）时，(v_m=2/3)，而 product 取等被整除性排除。
证据中的

\[
t=(\sqrt{57}-5)/4,\quad
p_1=(t,1-t,0),\quad p_2=(0,1-t,t)
\]

使三个查询相等，并给出

\[
2/3<v_3^{\rm prod}\le(13-\sqrt{57})/8.
\]

这是 feasible upper bound，不能写成 product optimum。它只证明独立表示受限时的
严格损失；任意相关循环平移仍取到 (2/3)。

证据 JSON 的 product 校准为 30 个 ((K,r)) 参数、461 个计数向量、24 个构造
products、44 个有序输出；全称 iff 由上述解析证明承载，而非由这些有限数值推出。

## 与 SPE/half 的接口说明

M64 的变量是一次静态背景中的计数 (H_j)，没有有序历史或策略函数。要在动态
博弈中使用它，另一个端点必须给出：

1. 一个真实合法目录与完整纯 SPE；
2. 每个玩家的全部有序历史偏离及真实 continuation；
3. 将这些 IC/福利项逐项映射到同一 (Q) 或 product 的量词；
4. 该映射保持 (W)、(mathrm{OPT}_m) 与安全值的支付关系。

缺少这四步时，不能由 (v_m) 推 (W\ge mv_m)，也不能由 product gap 推
(mathrm{OPT}_m>2W)。本证据中的 13 客户两人记录虽有 2 份完整纯 SPE，且
`not_half_counterexample=true`；60 点重建虽有 2016 条静态行全部非负、10 条零行，
仍未给全策略 LP 或动态 half 证书。审查还明确 61 点的两条负行只是原记录复用，
本轮未重认证，不可拿来构造本对象的精确反例。

## 本次边的作用

本支持片段只承载 M64 自身的模型、全称分类、严格 gap 机制及证据边界。它可作为
其它已独立证明的 bank/menu 分解的静态安全基准；那些分解的前提、方向和 continuation
必须由各自端点承担。本包不把共同定义、有限审计或产品限制升级为一般 half/SPE
逻辑蕴含。
