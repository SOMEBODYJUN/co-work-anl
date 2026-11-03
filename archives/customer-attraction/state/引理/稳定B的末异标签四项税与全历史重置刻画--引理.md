---
id: "customer-attraction/d1-stable-B-last-label-four-tax-and-full-history-reset-characterization"
kind: "lemma"
type_tag: "引理"
title: "稳定B的末异标签四项税、完整重置刻画与净保险界"
status: "proved-conditional-with-label-coverage-degeneracies-explicit"
summary: "精确保留最后不同标签及最后不同覆盖两版本；稳定不等式等价恒B全历史SPE，给路径可实现性和根最小利润；条件净保险界不推广到一般安全值。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/last_non_B_rigidity.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/last_non_B_rigidity.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/independent_continue/stable_B_trigger_blind_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/independent_continue/stable_B_trigger_blind_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/independent_continue/stable_B_net_insurance_corollary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/independent_continue/stable_B_net_insurance_corollary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_last_nonB_rigidity.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/menu/review_last_nonB_rigidity.md"
---

# 模型与稳定条件

有限单位客户、有限非空共同**标签**目录，标签 T 的覆盖仍简记 T。不同标签允许覆盖相同，空主题、重复行动、零客户和全部离轨弱平局均保留。固定非负整数客户负载 b 和整数 n≥1 名剩余玩家。以下解析式对任意这样的 b 成立；若要作为原游戏子局使用，再要求 b 来自合法前缀。完整策略仍读全部有序标签历史，不能只读负载。

固定合法标签 B，定义
\[
\alpha_T=\sum_{x\in T\setminus B}\frac1{b_x+1},\qquad
\beta_T=\sum_{x\in B\setminus T}\frac1{b_x+n}.
\]
稳定条件为
\[
\tag{H}\alpha_T\le\beta_T\quad\hbox{对每个目录标签 }T.
\]
它等价于在 B 重复 n−1 次后的末位，B 为一个允许平局的 BR。这里不假设所有 SPE 都选 B，也不从收益相等推出标签相等。

## 无稳定前提的四项恒等式

取任意完整子 SPE 的一条路径。若存在与 B 不同的标签，取最后一个，记它为 T；之前剩余玩家的 k 个行动为 P₁,…,P_k，客户负载 p_x，之后 r 个行动的标签全为 B，k+1+r=n。记 T 玩家真实利润 U，强制其改 B 后、沿同一完整策略真正续局的利润 D，并置
\[
G=\sum_{x\in B}\frac1{b_x+p_x+r+1}.
\]
B 偏离者之后至多再有 r 人覆盖每个 B 客户，所以 D≥G；IC 给 U≥D。逐客户展开
\[
\begin{aligned}
 A&=\sum_{T\setminus B}\left(\frac1{b+1}-\frac1{b+p+1}\right)\ge0,\\
 E&=\sum_{B\setminus T}\left(\frac1{b+p+r+1}-\frac1{b+n}\right)\ge0,\\
 \gamma&=U-D\ge0,\qquad \zeta=D-G\ge0,
\end{aligned}
\]
其中 E≥0 用 p_x≤k。交集的同终局分母相消，得到不需 (H) 的准确恒等式
\[
\boxed{\alpha_T-\beta_T=A+E+\gamma+\zeta.}\tag{1}
\]
γ 是**原真实偏离**的 IC 松弛，ζ 是该真实 child 相对裸 B 保底的超额。不能把这两项换成另一个任选续局或静态最差背景。

## 稳定时的刚性及正确的别名边界

在 (H) 下，式(1)左右夹零，所以 α_T=β_T，四项都零。由逐客户非负性：T\B 上 p_x=0，B\T 上 p_x=k。ζ=0 迫使真实 B-child 的每名后继覆盖全部 B；若某个后继覆盖严格超出 B，其标签 R 将有 β_R=0、α_R>0，违反 (H)。故那些后继的**覆盖恰等于 B**。

这最后一句不能加强为“后继标签必为 B”。当前目录允许同覆盖异标签。两种末点定义应分开使用：

| 末点定义 | 后缀 | 可得结论 |
|---|---|---|
| 最后一个标签不等于 B 的行动 | 后缀标签确为 B | 式(1)及刚性均成立；T 可能只是 B 的别名，所有差集和税均零 |
| 最后一个覆盖不等于 B 的行动 | 后缀覆盖均为 B，标签可不同 | 同一逐客户展开及刚性成立；若没有这种行动，整条路径物理覆盖已全为 B |

证明第二行时只用后缀的覆盖，故公式无需改动；策略触发器仍按标签历史，不随之商掉标签。B 为空时 (H) 迫使所有主题覆盖为空，但仍可有多个空标签及任意弱平局路径。“没有非 B 标签路径”在此不成立；正确的是没有覆盖不同于 B 的路径。零客户完全包括在这个退化中，δ=α−β=0、ε=0。

把这个末点局部的 T 改为 B，并贴回原真实 B-child，会保持该节点及以下的 SPE 性质和当前玩家利润；这**不是**对原祖先利润不变的断言。n≥2 时，每个其他剩余玩家都覆盖 B\T、避开 T\B，替换后每人恰损失
\[
\epsilon=\sum_{B\setminus T}\frac1{(b+n-1)(b+n)}
 \le\frac{\alpha_T}{n-1}.
\]
此式 n=1 不使用。旧背景玩家的总利润变化则是
\[
\Delta P_{old}=\sum_{T\setminus B,\ b>0}\frac1{b+1}
 -\sum_{B\setminus T}\frac b{(b+n-1)(b+n)}.
\]
因而尾部与旧人合计的福利变化为
\[
\Delta W=\Delta P_{old}-(n-1)\epsilon
=-|\{x\in T\setminus B:b_x=0\}|.
\]
旧背景玩家不共享同一个 ε 损失界。对 n≥2，刚性还给任何 SPE 尾部并集包含 B；n=1 时等值 BR 可以漏掉 B，不能保留这一额外结论。

## 恒 B 是每个有序历史的 SPE，当且仅当 (H)

在任意尾历史 h（长度 t，负载 p，余 r=n−t≥1）后，规定当前及以后都选 B，当前收益
\[
G(h)=\sum_B\frac1{b+p+r}.
\]
强制当前 T 后以后恒 B 的真实收益
\[
F_h(T)=\sum_{T\cap B}\frac1{b+p+r}
      +\sum_{T\setminus B}\frac1{b+p+1}.
\]
于是 G−F 是 B\T 的第一类和减 T\B 的第二类和。因 p≤t，第一类至少 β_T；第二类至多 α_T。因此 (H) 给全部历史、全部 T 的 G≥F，包括自身及覆盖相同的其他标签。反向只查 h=B^(n−1) 即还原 (H)。这一步没有假设过去也全选 B，交叉主题在 B 内外造成的 p 均已保留。

现在给定任意目标标签路径 a=(A₁,…,A_n)，前 i−1 位负载 p_i，目标真实叶利润 u_i。在 (H) 下，以下条件等价：

1. a 可实现为某份完整纯 SPE 的实际路径；
2. 对所有 i，\(u_i\ge G_i:=\sum_B1/(b+p_i+n-i+1)\)；
3. 对每个 i、每个合法 T，\(u_i\ge F_{h_i}(T)\)。

必要性由当前改选 B 后的任意真后继均不低于 G_i。由上述逐项比较，所有 F≤G，且 F(B)=G，故 2、3 等价。充分性用**完整有序标签触发器**：恰为 a 的正常前缀时走 a；第一次选了不同标签后永久恒 B。离轨子树按上一段是真 SPE；正常每个真实偏离值为 F_h(T)，由 3 排除。自身行动 A_i 不触发退出，但把 F_h(A_i) 也列入测试不额外收紧，因为它已≤G_i≤u_i。这纠正了源审查先疑其“自身多测过强”、后正式撤回的口头判断。

因此所有完整 SPE 中首位利润的准确最小值为
\[
\boxed{M=\min_{\sigma\in SPE}u_1(\sigma)=\sum_B\frac1{b+n}.}\tag{2}
\]
下界不依赖选择哪棵真子树；恒 B 完整策略达到。它是当前首位的最小值，不是旧背景玩家的钱包。

## 稳定 B 下的净保险充分界

记任意完整子 SPE 的首位利润 h、剩余总利润 P。定义静态 n 槽残余利润最优值
\[
F_n(b)=\max_{(T_1,\ldots,T_n)}\sum_x\frac{c_x}{b_x+c_x},
\]
c=0 的项规定为 0（即使 b=0），非空背景下它不是全体覆盖人数。令 d=(n−1)1_B，任意 c≥1 逐客户有
\[
\frac c{b+c}\le\frac{c+d}{b+d+1},
\]
清分母后的差分子为 c(c−1)+bd≥0；c=0 时左零，右亦非负。对任意 n 个比较主题求和，(H) 使背景 b+d 下每个主题的额外查询收益至多 M；d 的 n−1 份 B 也各为 M。因此
\[
F_n(b)\le(2n-1)M.\tag{3}
\]
对真实 SPE 每位玩家，在其节点的 B 保底至少 M，故其利润≥M。n≥2 时末位还可选择首位实际主题 A：与真实首位所处终局相比，改变末位使每个 A 客户的正分母最多加 1，故末位至少得 h/2。首、末和另外 n−2 位是不同玩家，给
\[
P\ge\tfrac32h+(n-2)M,
\qquad
\boxed{2P-F_n(b)\ge3(h-M).}\tag{4}
\]
n=1 时 h=M=F₁(b)，同样成立；全空/零质量时全为零，不除以 M。空根 b=0 才把 P 识别为实际福利。

这证明原净保险猜想在 (H) 这个可核充分域成立，未证明一般目录总有稳定 B，也未允许把 M 换成另一个混合安全值。完整主目标恰六人，原一般人数开放问题与该条件引理须分别保存。

## 来源、比较与接续

四份主稿分别给四项刚性、稳定触发器盲重构、净保险推论、独立 menu 审查。本轮逐段比较后重新给出上述自足证明，并修正同覆盖标签与空 B 的边界；没有运行枚举器。原条件不提供跨互斥 root 源的共同容量。共享租金和两个真实 child 的五项账本见[分支税与共享容量](../障碍/两个真实孩子的五项税与共享终局租金容量--障碍.md)，原件及精确身份见[证据](../../tools/evidence/d1-stable-reset-and-shared-rent-primary/README.md)。
