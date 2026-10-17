# 列表 agreement 的度数预算与真实调度解码义务

读取目的：核查反面归约从实际低负载调度抽出的标签列表，是否真的足够短，能够调用 list-agreement soundness。本页给可构造的线性 agreement 下界和逐图锐的全 agreement 列表阈值；不是 Label Cover 或 UM 的新困难性结果。

## UM-LIST-AGREEMENT-DEGREE-BUDGET-v1

### Exact Statement

给显式有限简单二部图 (G=(A,B,E))，其中 (B\ne\varnothing)，每个左点度数为整数 (d\ge1)，每个右点度数为整数 (D\ge2)。给非空有限字母表 (\Sigma_A,\Sigma_B) 及每条边的显式总映射 (\pi_{ab}:\Sigma_A\to\Sigma_B)。假设每个右点都满足局部公共像条件

\[
\bigcap_{a\in N(b)}\pi_{ab}(\Sigma_A)\ne\varnothing.                 \tag{1}
\]

列表赋值是 (\Lambda_a\subseteq\Sigma_A)，大小至多二进制整数 (L\ge1)。右点 (b) 的 **agreement** 指存在两个不同邻居 (a,a') 及各自列表中的 (x,y)，使 (\pi_{ab}(x)=\pi_{a'b}(y))。记实际 agreement 比例为 (\operatorname{agr}(\Lambda))。则：

1. 存在确定性总位多项式时间算法，输出实际列表，满足

   \[
   \boxed{\operatorname{agr}(\Lambda)\ \ge\
   \frac{L(D-1)}{2d+L(D-1)}.}                                    \tag{2}
   \]

2. 若 (L\ge\lceil2d/D\rceil)，存在确定性总位多项式时间算法输出使全部右点 agreement 的实际列表。
3. 第2项的通用整数阈值对**每一张**上述简单正规图都锐：可以在该固定图上构造满足 (1) 的多项式大小字母表和总映射，使每个 (1\le L<\lceil2d/D\rceil) 的列表赋值均不能让全部右点 agreement。这里不声称第1项的分数下界也锐。
4. 若某个满足此对象域的 NO 源有 ((\le L,\alpha))-list-agreement soundness，即每个上述列表的 agreement 比例至多 (\alpha<1)，则必须

   \[
   \alpha\ge\frac{L(D-1)}{2d+L(D-1)}>0,
   \qquad L<\lceil2d/D\rceil,                                   \tag{3}
   \]

   并且

   \[
   \boxed{\frac dL\ge\frac{(D-1)(1-\alpha)}{2\alpha}.}             \tag{4}
   \]

### Objects / Domain / Quantifiers

量化全部满足上述显式编码、简单性、正规度数与局部公共像条件的输入，以及全部 (L\ge1)。锐性在每个固定图上构造一套地图，同时量化阈值以下的全部整数 (L)。字母表可随图增长。集合大小语义为“至多”，包括 (L>|\Sigma_A|)；不要求补成恰 (L) 个不同符号。

### Assumptions / Definitions

没有复杂度假设，也没有给全局满足赋值。局部公共像不等于全局 YES。不同右点可以对同一个左点要求不同原像。agreement 必须来自两个不同左邻居，不能把平行边计成两个人。

### Scope / Conclusion

式 (2) 是确定性可构造的源预算地板；第2–3项是全 agreement 的通用阈值锐界。式 (3)–(4) 是 soundness 必须满足的参数限制，不是源困难性、不是真实调度编译器，也不完成 UM-TARGET-v1 的正反面。

### Dependencies

本页显式定义、饱和点计数及标准整数二部容量流。全部证明如下。Moshkovitz 的文献定位仅说明要对接的源概念，不作为这四项组合结论的证明前提。

### Evidence / Counterevidence or Objections

仅陈述先行独立重构后，再读现行证明攻击；实际顺序见[审查](../../reviews/unrelated_machines/list_agreement_degree_budget_review.md)。没有用有限枚举替代一般证明，也没有实现新的源或调度求解器。

### Status / Related Files

限定范围证明完整，内部陈述先行及读后审查分别登记；外审与全球新颖性未认证。[专题账本](../../unrelated_machines/CLAIMS.md)。

## 1. 确定性 ticket 构造及线性界

从每个右点的公共像交集中确定性选一个 (\beta_b)，并为每条边选实际原像 (x_{ab})，使 (\pi_{ab}(x_{ab})=\beta_b)。这可直接扫描显式地图完成，不需要源的全局满足见证。

以一条选中关联为一张 ticket；同一个左点即使两张 ticket 最终使用相同符号，也分别计数。去重只会减少输出列表大小。

初始化每个左点 ticket 数 (t_a=0)，已服务右集 (S=\varnothing)。只要存在 (b\notin S) 有两个不同邻居 (a,a') 满足 (t_a,t_{a'}<L)，就给这两条关联各一张 ticket，计数各加一，并把 (b) 加入 (S)。所有选择按固定输入次序进行。最后 (\Lambda_a) 是 (a) 的 ticket 原像集合。于是每个列表大小至多 (t_a\le L)，每个 (b\in S) 真实 agreement；没有假定其余右点不 agreement。

设终止时饱和左集为 (F=\{a:t_a=L\})。每个未服务右点至多有一个未饱和邻居，所以

\[
(D-1)(|B|-|S|)\le |E(F,B\setminus S)|\le d|F|,
\qquad L|F|\le\sum_a t_a=2|S|.
\]

消去 (|F|) 得

\[
L(D-1)(|B|-|S|)\le2d|S|.
\]

除以正数 (|B|[2d+L(D-1)]) 即为 (2)，因为实际 agreement 数至少 (|S|)。算法使用 ticket 而非“当前已 agreement 数”计数，避免把一次加标签顺带产生的其他 agreement 当成额外付费步骤。

朴素实现每一步扫描全部未服务右点，至多 (|B|) 步。每个 (t_a\le d)，只需与二进制 (L) 比较；没有按 (L) 数值循环。若 (L>d)，无左点能饱和，算法直接服务全部右点，证明同样有效。

## 2. 全 agreement 的整数流

建立网络：源到每个 (b) 容量2，(b\to a) 对每条原关联容量1，每个 (a) 到汇容量 (min(L,d))。需要流量 (2|B|)。给每条关联分数流 (2/D)；每个右点流出2，每个左点流入 (2d/D)。当 (L\ge\lceil2d/D\rceil) 时分数流合法，而且 (D\ge2) 保证关联容量1合法、(lceil2d/D\rceil\le d)。

标准整数最大流给同值整数流，每个右点的两单位必流向两个不同邻居。把对应的实际 (x_{ab}) 放入列表，即让每个右点 agreement。容量均受显式度数约束；大二进制 (L) 先截成 (d)，不引入伪多项式循环。

## 3. 固定图上的阈值锐性

对任意满足对象域的固定图，令

\[
\Sigma_A=\{\ell_b:b\in B\},
\qquad\Sigma_B=\{0\}\cup\{p_a:a\in A\},
\]

所有 (p_a) 两两不同且不为0。对每条边定义总映射

\[
\pi_{ab}(\ell_c)=
\begin{cases}0,&c=b,\\p_a,&c\ne b.\end{cases}
\]

每个邻居的像都含0，所以 (1) 成立。不同邻居的私有符号不相等，因此 (b) agreement 当且仅当至少两个不同邻居的列表含 (\ell_b)。全部右点 agreement 需要至少 (2|B|) 张不同的“左点—右点符号”关联，而每个左列表至多供给 (L) 张，所以

\[
|A|L\ge2|B|=|A|\frac{2d}{D}.
\]

这迫使整数 (L\ge\lceil2d/D\rceil)。一次构造同时排除了全部较小 (L)。地图表有 (|E||B|) 项，两个字母表大小分别为 (|B|)、(|A|+1)，总编码多项式。若阈值为1，则低于阈值的 (L\ge1) 范围为空；没有伪造非空锐例。此人为地图不声称有全局 YES，也不声称组成困难性归约。

## 4. 源 soundness 的必要参数

把 (2) 的实际输出代入 NO soundness 就得 (3) 第一式及 (\alpha>0)。第2项排除 (L\ge\lceil2d/D\rceil) 时的 (\alpha<1)。正数交叉相乘

\[
2\alpha d\ge(1-\alpha)L(D-1)
\]

得到 (4)。例如 (L/d=1/D) 时，确定性界为

\[
\operatorname{agr}(\Lambda)\ge\frac{D-1}{3D-1}.
\]

右边在 (D=2) 为 (1/5)，随 (D\to\infty) 趋近 (1/3)。因此“左列表只占其发生次数的 (1/D)”仍不能与任意小 agreement soundness 配套。该地板不是第1项分数界的锐性声明。

## 5. 与真实调度解码的连接和缺口

Moshkovitz，*The Projection Games Conjecture and the NP-Hardness of ln n-Approximating Set-Cover*，ToC 2015最终版：Def4.5–4.6/Lemma4.7 在印页227，Cor4.8 在印页228，给 polylog 长左列表和固定素数幂右度数的 agreement 源；Claim4.10 在印页229以每个右测试收到的全部被选标签数 (s_b) 计费。该最终版的 set-cover 困难性不再依赖会议版 PGC 条件。原文取得与实际阅读范围在 manifest 登记。

这里不默认 Cor4.8 的输出自动满足本页简单、正规、局部公共像的全部条件。某个编译若要用本页参数，必须逐项核图结构；局部公共像为空可直接判定该源不可能全满足，不能把局部扫描接受当作全局 YES。

本次物理候选的未闭合点是：中等时间环/多标签路径被 clause 导出、补入打断后，每新增一个标签组件只收费一次，粗计只给总列表大小 (O(|B|))。这个量级本身不足。在任何满足本页对象域（包括两个不同邻居和局部公共像）的源上，每个右测试任取两邻居，并各放一个公共像原像，就已经能用总共至多 (2|B|) 个左标签使**全部**右点 agreement。该平凡构造不保证逐左列表短，正说明总预算不能直接替代逐左预算。

若实际解码只得到 (|\Lambda_a|\le L) 且 (L\) 与 (d/D) 同阶，式 (4) 又明确排除随意小的 soundness。能继续尝试的合同应提供更强的度数分离，或把每个新增标签组件收费到许多独立发生，或给源定理真正需要的逐右局部标签预算。当前没有构造这样的实际任务收费机制。

本页扣除的都是标准原像选择、饱和点计数和二部流。新增可复用内容是把它们合成精确参数检查及逐图锐的 all-agree 阈值；全球新颖性和独立论文价值未认证。不会把这个源计数结论画成调度困难性证明。
