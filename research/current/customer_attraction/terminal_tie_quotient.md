# 真实末端平局行的商空间支付与二次判别

2026-10-10。本页固定 [CAG-MODEL](model.md) 的单位玩家、单位客户、共同有限目录与
全部有序历史策略。给出 **CA-TERMINAL-TIE-QUOTIENT-LIFT** 和
**CA-TERMINAL-TIE-LOCAL-QUADRATIC** 两个自包含代数接口，并给出真实分支上的
有限成功证书及限制。任意人数的半覆盖证书仍未构造；本页不把有限成功、条件性
提升或形式策略例升级为一般半覆盖证明。外部同行评审及新颖性认证未完成。

## 1. 全部真实行中可显式使用的有符号子空间

固定人数 \(n\ge2\)、主题标签数 \(m\)、完整形式策略 \(\sigma\)。客户类型为
非空 \(T\subseteq[m]\)，客户质量 \(w_T\ge0\)。有理质量可清分母展开为不同单位客户。
每个 \(\Gamma_{h,a}\) 都是节点 \(h\) 的指定行动收益，减在该节点改选 \(a\) 后沿
同一原策略真实执行的收益。各历史、各偏离分别加权；没有节点内平均限制。

对每个长度 \(n-1\) 的主题计数 \(q\)，选一个有序代表 \(g_q\)，令

\[
b_q=\sigma_n(g_q),\qquad
A_q=\{\sigma_n(\ell):q(\ell)=q\},\qquad
p_q(T)=\sum_Sq(S)\mathbf1_{S\in T}.
\]

实际根末前缀选自身为代表。对于 \(a\in A_q\setminus\{b_q\}\)，再选一个原回复为
\(a\) 的真实末前缀 \(\ell(q,a)\)。定义

\[
R_{q,a;T}=\frac{\mathbf1_{a\in T}-\mathbf1_{b_q\in T}}{p_q(T)+1}.
\]

两条原真实末行直接给

\[
R_{q,a}=\Gamma_{\ell(q,a),b_q},\qquad
-R_{q,a}=\Gamma_{g_q,a}.\tag{1}
\]

因此显式子空间

\[
H_\sigma=\operatorname{span}\{R_{q,a}:a\in A_q\setminus\{b_q\}\}
\tag{2}
\]

的任意元素 \(z=\sum_{q,a}\theta_{q,a}R_{q,a}\)，都能用原真实末行的非负乘子表示：

- \(\theta_{q,a}\ge0\) 时，把 \(\theta_{q,a}\) 加到 \(\Gamma_{\ell(q,a),b_q}\)；
- \(\theta_{q,a}<0\) 时，把 \(-\theta_{q,a}\) 加到 \(\Gamma_{g_q,a}\)。

这只是可显式列出的相反行子空间；不声称它是全部原行锥的最大线性子空间。
在任何原完整 SPE 质量上，式 (1) 两行非负且互为负向量，所以
\(R_{q,a}\cdot w=0\)。质量不进入逐类型的式 (1)。

## 2. CA-TERMINAL-TIE-QUOTIENT-LIFT

令 \(\bar\sigma\) 只把每个末节点的回复改为 \(b_{q(\ell)}\)，此前行动不变。
根末前缀选自身，使原根覆盖 \(c\) 逐类型保持。
对原末前缀 \(\ell\) 中的一份主题 \(S\)，定义 incumbent 收益变化

\[
\delta_{\ell,S;T}=
\frac{\mathbf1_{S\in T}(\mathbf1_{\sigma_n(\ell)\in T}-\mathbf1_{b_{q(\ell)}\in T})}
{p_{q(\ell)}(T)(p_{q(\ell)}(T)+1)}.\tag{3}
\]

分子为零取零；分子非零时 \(S\) 在前缀中，分母正。
令 \(\ell_h,\ell_{ha}\) 分别是从 \(h\)、在 \(h\) 改选 \(a\) 后沿原策略走到末位前
得到的真实前缀。则 [末回复运输](terminal_reply_transport.md) 的行恒等式为

\[
\bar\Gamma_{h,a}=\Gamma_{h,a}
 +\delta_{\ell_h,\sigma(h)}-\delta_{\ell_{ha},a},\qquad |h|<n-1,
\tag{4}
\]

\[
\bar\Gamma_{\ell,t}=\Gamma_{\ell,t}+\Gamma_{g_{q(\ell)},\sigma_n(\ell)}.
\tag{5}
\]

给定任意逐类型恒等式

\[
d=\bar\Gamma^{\mathsf T}\bar\lambda+\bar r,\qquad
\bar\lambda\ge0,\quad\bar r\ge0,
\]

按式 (4) 保留早期乘子，按式 (5) 拆分末行，得到原真实行的非负支付
\(\Gamma^{\mathsf T}\lambda^0\)，以及

\[
E=\sum_{|h|<n-1,a}\bar\lambda_{h,a}
(\delta_{\ell_h,\sigma(h)}-\delta_{\ell_{ha},a}),
\qquad d=\Gamma^{\mathsf T}\lambda^0+\bar r+E.\tag{6}
\]

**提升定理。** 若给出实数 \(\theta_{q,a}\) 使

\[
r'=\bar r+E-\sum_{q,a}\theta_{q,a}R_{q,a}\ge0
\quad\text{逐类型成立},\tag{7}
\]

则按 §1 把该有符号和表示为原末行的非负支付 \(\Gamma^{\mathsf T}\mu\)，便有

\[
\boxed{d=\Gamma^{\mathsf T}(\lambda^0+\mu)+r',
\qquad\lambda^0+\mu\ge0,\quad r'\ge0.}\tag{8}
\]

这是显式构造。无需假定 \(\bar\sigma\) 在原质量上是 SPE，也不由待证半覆盖
调用 Farkas 来保证乘子存在。它严格扩大直接要求 \(\bar r+E\ge0\) 的旧提升条件。
对“保留已有支付，只再使用 §1 相反末行”的指定机制，式 (7) 正好是剩余义务：

\[
\bar r+E\in\mathbb R_+^{2^m-1}+H_\sigma.\tag{9}
\]

这并非完整原行证书存在的必要条件；允许重新选择早期乘子是更大的机制。

## 3. 自然目标 \(2c-o\) 的严格成功与不能任意提升

取三个主题 \(A,B,C\)，客户类型次序固定为

\[
(A,B,AB,C,AC,BC,ABC).
\]

原策略根选 \(C\)，第二位见 \(A,B,C\) 分别选 \(C,B,A\)；末回复表为

| 第一主题 / 第二主题 | A | B | C |
|---|---|---|---|
| A | C | C | B |
| B | C | C | C |
| C | C | B | B |

规范化只把 \(AC,CB\) 的回复改为 \(C\)。实际 \(CAC\) 保持。
比较主题取 \(A,B,C\)，故

\[
d=2c-o=(1,-1,1,1,1,1,1).
\]

两条关键相反行定向为

\[
\tau_{AC}=\Gamma_{AC,C}=(0,1,1/2,-1/2,-1/3,0,0),
\]

\[
\tau_{CB}=\Gamma_{CB,C}=(0,1/2,1/2,-1/2,-1/2,0,0).
\]

**严格成功。** 规范化早期乘子仅在 \((A,A),(C,B),(C,C)\) 非零，分别为 \(2,1,1\)。
直接从真实终局计算得到

\[
\bar r=(0,0,1,1/2,5/6,2/3,1)\ge0,
\]

\[
s:=\bar r+E=(0,-1/2,1/2,-1/2,1/2,2/3,1),
\]

\[
s-(-2\tau_{AC}+3\tau_{CB})=(0,0,0,0,4/3,2/3,1)\ge0.
\]

因此原真实证书除保留三条早期行，还加入 \(2\Gamma_{CA,B}+3\Gamma_{CB,C}\)。
原直接提升余项 \(s\) 含负坐标，新的商空间提升成功。

**同一自然目标的固定支付障碍。** 改用同三条规范化早期行的乘子 \(4,1,2\)，仍有

\[
\bar r_{bad}=(0,0,1,0,1,0,1)\ge0,
\]

\[
s_{bad}=\bar r_{bad}+E_{bad}
=(0,-1/2,1/2,-2,1/3,0,1).
\]

单位客户质量

\[
w=(0,0,1,1,0,1,0)
\]

给 \(A=\{x\},B=\{x,y\},C=\{y,z\}\)。原策略的全部 39 个真实行动比较均非负，
即它是完整 SPE；\(W=\operatorname{OPT}_3=3\)。然而

\[
s_{bad}\cdot w=-3/2<0.\tag{10}
\]

全部 \(H_\sigma\) 向量在此 \(w\) 上为零，所以式 (9) 失败。更强地，
\(s_{bad}\notin\{\Gamma^{\mathsf T}\nu+r:\nu,r\ge0\}\)，因为此锥内每个向量
与已验证原 SPE 的 \(w\) 内积非负。
给定的三条原早期支付已花费 \(9/2\)，目标总值仅 (3)，再加任何非负真实行也不能
修复。须减少或重选早期支付。成功例已证明本实例的自然目标可认证；式 (10) 只是
任意固定规范化证书不能自动提升的反例。

## 4. CA-TERMINAL-TIE-LOCAL-QUADRATIC：每个计数内的精确判别

早期行对应边 \((\ell_{ha},a)\to(\ell_h,\sigma(h))\)。令入流减出流为
\(\kappa_{\ell,S}\)，则 \(E=\sum_{\ell,S}\kappa_{\ell,S}\delta_{\ell,S}\)。
固定一个计数 \(q\)，写 \(b=b_q\)，把同原末回复的不同有序前缀聚合为

\[
K_{a,S}=\sum_{\substack{q(\ell)=q\\\sigma_n(\ell)=a}}\kappa_{\ell,S},
\qquad a\in A_q\setminus\{b\},\quad q(S)>0.
\]

其余 \(K\) 为零。令 \(x_i=\mathbf1_{i\in T}\)，定义

\[
p(x)=\sum_iq_i x_i,\quad
N(x)=\sum_{a,S}K_{a,S}x_S(x_a-x_b).
\]

则此计数贡献 \(E_q=N/[p(p+1)]\)；\(p=0\) 时定义为零。
任意局部相反行和写为 \(J(x)/(p+1)\)，其中

\[
J(x)=\sum_i\eta_i x_i,\qquad
\eta_i=0\ (i\notin A_q),\quad\sum_i\eta_i=0.
\]

**局部判别定理。** 给定这样的 \(\eta\)，逐类型等式
\(E_q=J/(p+1)\) 成立，当且仅当同时满足以下条件：

\[
\eta_i=0\quad\text{当 }q_i=0,\tag{11}
\]

\[
\sum_aK_{a,i}(\mathbf1_{a=i}-\mathbf1_{b=i})=q_i\eta_i
\quad(1\le i\le m),\tag{12}
\]

\[
\sum_a\big[K_{a,i}(\mathbf1_{a=j}-\mathbf1_{b=j})
 +K_{a,j}(\mathbf1_{a=i}-\mathbf1_{b=i})\big]
=q_i\eta_j+q_j\eta_i\quad(i<j).\tag{13}
\]

**证明。** \(p=0\) 的外部 singleton 列使左侧为零、右侧为 \(\eta_i\)，给式 (11)。
对 \(p>0\) 清分母得到 \(N=pJ\)。在 Boolean 输入上把 \(x_i^2\) 替成 \(x_i\)，
两边均是次数至多二的 squarefree 多项式；在 \(p=0\) 列 \(N,pJ\) 也自动均为零，
所以该多项式恒等式确实覆盖整个 Boolean 立方体。其一次及二次系数恰为式 (12)–(13)。
必要性也可直接由 singleton 和双元素列恢复全部系数。反向由这些系数等式给
\(N=pJ\) 于全部 Boolean 列，再由式 (11) 处理 \(p=0\) 列。证毕。

因此**每个计数内**是否能全部消去转移，可用 \(O(m^2)\) 个线性等式准确检验。
遗漏式 (11) 会出错：\(q=(1,0)\)、\(b=B\)、\(K_{A,A}=1\)、\(J=x_A-x_B\) 时，
\(N=pJ\) 恒成立，但在 \(B\)-only 列 \(E_q=0\)、\(J/(p+1)=-1\)。

逐计数消去给全局 \(E\in H_\sigma\) 的充分条件；**不是必要条件**。
不同计数的分母不同，其相反行仍可在全部类型列中共同支付，见 §6。
对一般 \(\bar r+E\)，局部零转移判别也不替代式 (7) 的非负余项预算。

## 5. 均匀净流以外的真实四边零转移

若 \(\kappa_{\ell,S}=k_\ell q(S)\)，则

\[
\sum_S\kappa_{\ell,S}\delta_{\ell,S}
=k_\ell R_{q,\sigma_n(\ell)}
-k_\ell\mathbf1_{p=0}(\mathbf1_{\sigma_n(\ell)\in T}-\mathbf1_{b_q\in T}).
\tag{14}
\]

此**均匀 incidence 情形**模相反行只剩此前未覆盖客户的覆盖差。
一般净流可以准确拆成共同部分与重分配部分。对每个末前缀定义

\[
t_\ell=\frac{\sum_S\kappa_{\ell,S}}{n-1},\qquad
\widehat\kappa_{\ell,S}=\kappa_{\ell,S}-t_\ell q(S),
\qquad\sum_S\widehat\kappa_{\ell,S}=0.
\]

令 \(a=\sigma_n(\ell)\)，以及
\(U_{\ell,T}=\mathbf1_{p=0}(\mathbf1_{a\in T}-\mathbf1_{b_q\in T})\)。
把 \(R_{q,b_q}\) 约定为零，则无需均匀假设，

\[
\boxed{\sum_S\kappa_{\ell,S}\delta_{\ell,S}
=t_\ell R_{q,a}-t_\ell U_\ell
 +\sum_S\widehat\kappa_{\ell,S}\delta_{\ell,S}.}\tag{14a}
\]

式 (14a) 由 \(\sum_Sq(S)\delta_{\ell,S}=R_{q,a}-U_\ell\) 直接得出。
模去相反末行后，准确的两部分是此前未覆盖客户债 \(-t_\ell U_\ell\)，以及
已覆盖客户的 incumbent 重分配债
\(\sum_S\widehat\kappa_{\ell,S}\delta_{\ell,S}\)。
平衡关系 \(\sum_S\widehat\kappa_{\ell,S}=0\) 不使后者自动归零；各主题在一个类型
上的命中不同。即使 \(a,b_q\) 都在旧前缀中，从而 \(U_\ell=0\)，仍可能留有
非零重分配债。这也是[独立审查](../../../evidence/runs/2026-10-10/terminal_tie_quotient_review.md)
区分的两个支付义务。一般非均匀 \(\kappa\) 不能只记未覆盖债。
均匀条件本身也远非一般消元所必需。

四人三主题的一个完整形式策略如下：根和未另列的全部节点选 \(C\)；

| 真实历史 | 指定行动 |
|---|---|
| A | A |
| AA | C |
| AC | B |
| B | B |
| BB | C |
| BA | C |
| ACB | A |
| BAC | B |

末前缀 \(ABC\) 选 \(C\) 为计数代表；除 \(ACB,BAC\) 外全部末回复都是 \(C\)。
规范化只改变这两叶，根 \(CCCC\) 保持。下列四条真实早期行各赋权 1：

| 行 | 末前缀图源 | 末前缀图目标 | 非零改变叶的误差 |
|---|---|---|---|
| \((A,C)\) | \((ACB,C)\) | \((AAC,A)\) | \(-\delta_{ACB,C}\) |
| \((AC,A)\) | \((ACA,A)\) | \((ACB,B)\) | \(+\delta_{ACB,B}\) |
| \((B,A)\) | \((BAC,A)\) | \((BBC,B)\) | \(-\delta_{BAC,A}\) |
| \((BA,B)\) | \((BAB,B)\) | \((BAC,C)\) | \(+\delta_{BAC,C}\) |

故两个改变叶的净 incidence 分别为

\[
\kappa_{ACB}=(0,1,-1),\qquad\kappa_{BAC}=(-1,0,1).
\]

共同负载 \(p=x_A+x_B+x_C\)，于是

\[
E=\frac{(x_B-x_C)(x_A-x_C)-(x_A-x_C)(x_B-x_C)}{p(p+1)}=0.
\tag{15}
\]

\(p=0\) 列两项都为零。它是由四条原真实分支产生的非均匀二次相消，图端点不是
凭空指定。四条行没有平均成一个偏离。此例及其任意共同旧前缀嵌入的代数机制均成立；
它没有给任意 \(2c-o\) 构造可用四边或证明所有转移都能路由成这种结构。

## 6. 跨计数支付确实扩大逐计数机制

四人两主题的完整形式策略：所有节点原行动为 \(B\)，只令末前缀 \(ABA,BAB\)
回复 \(A\)。代表 \(AAB,ABB\) 均回复 \(B\)；根 \(BBBB\) 保持。
对三种类型 \((A,B,AB)\)，两组相反行分别为

\[
R_1=\Gamma_{ABA,B}=(1/3,-1/2,0),\qquad
R_2=\Gamma_{BAB,B}=(1/2,-1/3,0).
\]

给真实早期行 \((AB,A)\) 权重 1；指定行动执行到 \(ABB\)，偏离执行到 \(ABA\)。
其规范化误差为

\[
E=-\delta_{ABA,A}=(-1/6,0,0)
=\tfrac25R_1-\tfrac35R_2.\tag{16}
\]

该误差不在 \(R_1\) 的一维空间内，故不能只用发生误差的计数支付。
全局使用原真实末行
\(\tfrac25\Gamma_{ABA,B}+\tfrac35\Gamma_{ABB,A}\) 就支付了 \(E\)，余项为零。
因此全局商空间要在共同的全部类型列上核对；§4 的局部二次判别不能被误称为
全局必要条件。此形式策略可以在仅全兴趣客户、同覆盖标签允许的实例上是完整 SPE；
本节不声称它给两两不同覆盖实例的福利反例。

## 7. 可达性与当前最小义务

对每个末前缀 \(\ell\)，令 \(j(\ell)\) 是相对于原策略最后一次非规定行动的位置。
真实边的方向严格降低偏离次数。更具体地：

- 若 \(j(\ell)\) 存在，\(\ell\) 仅能在标签 \(\ell_{j(\ell)}\) 上作为一条非自偏离
  边的图源；这条边的节点就是此前真实有序前缀。
- \(\ell\) 作为图目标的非自边，只能出现在最后一次偏离之后沿原策略执行的位置；
  入流标签是这些位置的规定行动。

这由每条边两侧在该玩家行动之后都沿同一原策略执行立即得到。因此不能先任意
指定 \(\kappa\)，再宣称非负 \(\lambda\) 自动能实现它。例如源标签未在随后规定
后缀中再次出现时，该改变叶不能单凭节点守恒接受任意正外流。§5 特别展示了一个
真实可达的非均匀相消结构。

对直接半覆盖，当前比旧逐类型非负提升更弱的**构造义务**是：给每个完整
\(\sigma\) 与每个合法比较 \(n\)-元组产生某个

\[
2c-o=\bar\Gamma^{\mathsf T}\bar\lambda+\bar r,\quad
\bar\lambda,\bar r\ge0,
\]

并一起构造有符号末端支付 \(\theta\)，使式 (7) 非负；或者直接重构原真实行证书。
必须允许重选早期乘子，§3 已否定“任意给定规范化证书保留早期支付后都能修复”。
局部多叶二次相消、跨计数相反行与已有非负余项可以联合使用；仍缺对任意树和
比较元组保证这些支付可达且足够的全局预算。

\(n=1\) 无末端商空间：比较主题 \(t\) 给
\(2c-o=\Gamma_{\varnothing,t}+c\)。全零合法客户时半覆盖直接成立。
空主题、重复行动、离轨并列与零质量类型均由逐类型定义涵盖。

## 8. 验证范围

[Fraction 审计](../../../tests/audits/customer_attraction_terminal_tie_quotient.py)
独立从完整有序终局构造每条真实行，不导入模型、优化器或其他审计。它复验
39 项原 SPE 比较、自然目标成功及固定支付障碍、四边构造的 840 项行类型恒等式、
跨计数有符号支付、8019 组局部系数判别与全部类型判别的等价性，并专查 \(p=0\)
漏项。[独立末端审计](../../../tests/audits/customer_attraction_terminal_tie_independent.py)
另从定义重构 §3 的两套自然目标证书、全部末行相反关系与 \(-3/2\) 分离值。

```sh
python3 tests/audits/customer_attraction_terminal_tie_quotient.py
python3 tests/audits/customer_attraction_terminal_tie_independent.py
```

默认只打印 JSON；`--output` 排他创建新记录。普遍结果的依据是 §1–2 与 §4 的
自包含代数证明；有限脚本检查这些接口和明确例子的实现，没有覆盖任意策略树。
