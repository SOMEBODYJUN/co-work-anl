# 标签资源的大需求碰撞界与平方池的精确锐性

本页继续反面归约的实际整数一致性检查。[低重数地板](bounded_collision_label_resource_floor.md)只用资源处关联着色给 \(1/\Delta\)。下面把**变量束整体分组**、缺陷着色势与真实资源匹配联结，给出更强的有限参数界；在一个平方池族上，含根整数上取整的界精确达到真实最优值。它约束四层资源束 gadget，不是一般 UM 近二困难性。

## 1. Exact Statement 与对象

沿用 `UM-DAG-DEGREE-MODEL-v1`：原正需求点在输出树中成为叶仍收费，零需求仅限原终端，真实根树的每个非根点恰一个父点，评分
\[
b(H)=\min(\{1\}\cup\{\deg_H^+(v)/d_v:v\in H,d_v>0\}).
\]
给定 \(q\ge1\) 个显式非空资源束 \(B_x\subseteq R\)，\(K_x=|B_x|\ge1\)。在根需求 \(q\)、变量需求一、私有标签需求 \(K_x\)、资源需求零的四层 DAG \(r\to x\to e_x\to R\) 中，标签 \(e_x\) 至少包含 \(B_x\) 的所有资源邻居。各层不交、各变量标签节点不同，资源在一束内无重复。允许额外标签及额外资源边，本算法只使用给定的完整选择。定义
\[
\Delta=\max_{u\in R}|\{x:u\in B_x\}|,
\quad I=\sum_xK_x,
\quad K_{\min}=\min_xK_x.
\]
无关联资源不影响最大值；因束非空，\(1\le\Delta\le q\)。所有规模按显式关联和二进制整数身份的合计位长计，不把隐式巨大束作为输入。

**UM-LARGE-BUNDLE-COLLISION-FLOOR-v1。** 对每个这样的输入及每个整数 \(1\le c\le q\)，有确定性总位多项式算法输出真实根树 \(H_c\)，满足
\[
D_c=1+\frac{\Delta-1}{c},\qquad
a_x(c)=\left\lfloor\frac{K_xc}{c+\Delta-1}\right\rfloor,
\]
\[
\boxed{
b(H_c)\ge\Lambda_c
:=\min\left\{
\frac{\lceil q/c\rceil}{q},\
\min_x\frac{a_x(c)}{K_x}
\right\}.
}
\tag{1}
\]
可以对全部 \(c\le q\) 运行并取实际评分最好者，仍总位多项式；也可与旧 \(1/\Delta\) 构造取优。不需要最优树、分数配置、源问题见证或求最小碰撞选择的 oracle。给定完整束承重，不把总位复杂度变成按巨大二进制需求数值展开。

同一身份的**有限锐例**：对每个整数 \(t\ge1\)，令 \(q=\Delta=K_x=t^2\)，资源集恰为同一 \(t^2\) 元资源池，每变量仅有一个标签且该标签的完整邻域恰为此池，无额外边。则
\[
b^*=\max_{1\le c\le q}\Lambda_c=1/t.
\tag{2}
\]
当 \(t\ge2\) 时 \(c=t+1\) 已达到式(2)；\(t=1\) 用 \(c=1\)。这不是一般实例上 \(b^*=\max_c\Lambda_c\) 的主张。

## 2. 整束重染色与整数势

将每个变量束染为 \(c\) 色之一。令 \(d_z(u)\) 为资源 \(u\) 的颜色 \(z\) 所有者数。考虑非负整数势
\[
\Psi=\sum_{u,z}\binom{d_z(u)}2.
\tag{3}
\]
从固定初始颜色开始，按固定变量和颜色次序，执行首个严格降低 \(\Psi\) 的单束重染色，直至无此移动。权重仅为实际资源交集计数。

固定终态变量 \(x\)，颜色为 \(o\)。记
\[
A_o(x)=\sum_{u\in B_x}(d_o(u)-1),\qquad
A_z(x)=\sum_{u\in B_x}d_z(u)\quad(z\ne o).
\]
把 \(x\) 从 \(o\) 改为 \(z\) 的势变化恰为 \(A_z-A_o\)。终态给 \(A_o\le A_z\)，求和得
\[
cA_o\le A_o+\sum_{z\ne o}A_z
=\sum_{u\in B_x}(d(u)-1)\le K_x(\Delta-1).
\]
因此
\[
\sum_{u\in B_x}d_o(u)=K_x+A_o\le K_xD_c.
\tag{4}
\]
这不是原资源处单射着色；同色可以共享资源，但式(4)同时控制每个束的同色碰撞总量。

## 3. 同色容量 Hall 与实际资源分配

固定任一颜色 \(z\)。每枚被此色使用的资源在其 \(d_z(u)\) 个所有者间等分，每条关联给 \(1/d_z(u)\)。资源总质量为一。对颜色 \(z\) 的每个束 \(x\)，由 Cauchy 和式(4)，
\[
\sum_{u\in B_x}\frac1{d_z(u)}
\ge\frac{K_x^2}{\sum_{u\in B_x}d_z(u)}
\ge K_x/D_c\ge a_x(c).
\tag{5}
\]
所以任意同色束子集 \(S\) 都满足
\[
\sum_{x\in S}a_x(c)
\le\sum_{x\in S}\sum_{u\in B_x}1/d_z(u)
\le\left|\bigcup_{x\in S}B_x\right|.
\tag{6}
\]
每束复制 \(a_x(c)\) 个单位槽、每个资源容量一，式(6)就是覆盖所有槽的 Hall 条件。确定性增广路匹配输出真实且互不重用的资源，实际槽数至多 \(I\)。此处只从显式束复制不超过其大小的槽，不能把二进制巨大需求作为伪多项式循环。

选择变量数最多的颜色，其变量数至少 \(\lceil q/c\rceil\)。保留这些 \(r\to x\to e_x\) 及其匹配资源边，得到真实根树：标签私有、资源匹配单父、所有路径从根可达。根比例至少 \(\lceil q/c\rceil/q\)，变量比例一，标签比例 \(a_x/K_x\)，证明式(1)。若某配额零，正需求输出叶仍收费零，\(\Lambda_c=0\)；可以直接输出默认根单点，不能把它当免费终端。

## 4. 总位复杂度与退化边界

势的全过程满足
\[
0\le\Psi\le\sum_u\binom{d(u)}2
\le(\Delta-1)I/2.
\tag{7}
\]
每次严格改善至少降一，故改善步数多项式；每轮至多扫描 \(qc\) 个重染色候选，每次只处理显式关联。配额匹配的增广次数至多 \(I\)，每次扫描有限二部图；整数、有理评分及资源身份比较的位长受输入控制。固定遍历和平局保持确定性。枚举全部 \(q\) 个颜色数不破坏多项式界。

\(c=1\)、\(\Delta=1\)、单资源和配额零都在式(1)范围内。\(\Delta=1\) 时取 \(c=1\)，每束分到全部资源，真实满比例一。若另允许空束族 \(q=0\)，按原需求模型根是零需求终端，单点树评分一；规范 API 仅对此分支用 \(c=0\) 并返回一，不代入式(1)除以零。空的单个正需求束不符合“给定完整选择”的前提。

## 5. 平方资源池的有限精确锐性

取式(2)的共同池。任意正评分 \(\beta\) 的真实树若选 \(s\) 个变量，则 \(s\ge\beta q\)，每个标签至少使用 \(\beta q\) 枚资源。单父约束给
\[
s\beta q\le q,
\qquad\beta^2q\le1,
\qquad\beta\le1/t.
\]
选 \(t\) 个变量，每个分 \(t\) 枚不同资源，则根和标签比例都为 \(1/t\)，达到真实上界。

当 \(t\ge2,c=t+1\) 时，\(c\le q\) 且
\[
\left\lceil\frac{t^2}{t+1}\right\rceil=t,
\quad
\left\lfloor\frac{t^2(t+1)}{t+1+t^2-1}\right\rfloor=t.
\]
故式(1)的两项都为 \(1/t\)。任意 \(c\) 的已证下界不可能大于真实 \(b^*\)，所以 \(\max_c\Lambda_c=1/t\)。\(t=1\) 直接得一。**保留根的整数上取整是有限锐性的关键**；若仅用较弱 \(1/c\)，该共同池在 \(t\ge2\) 时的公式最优值只有 \(1/(t+1)\)：当 \(c\le t\) 时配额至多 \(t-1\)，故标签比至多 \((t-1)/t^2<1/(t+1)\)；当 \(c\ge t+1\) 时根项至多 \(1/(t+1)\)，在 \(c=t+1\) 达到。较弱公式不能冒充有限精确值。

经既有 `UM-DAG-DEGREE-TOKEN-IDENTITY-v1`，平方池的真实调度最优值恰为 \(2-1/t\)，且本构造输出达到它的实际分配。该族显式可解，没有编码 NP 源问题；近二最优值本身不是近二困难性。

## 6. 大需求范围及 NO 侧碰撞必要量

取 \(c=\lceil\sqrt\Delta\rceil\le q\)，有 \(D_c\le c+1\)。忽略有利的根上取整，式(1)给
\[
b(H_c)\ge
\min\left\{\frac1c,\frac1{c+1}-\frac1{K_{\min}}\right\},
\tag{8}
\]
右侧负值可用零替代。若 \(K_{\min}\ge2(c+1)\)，可读的充分界为 \(1/[2(c+1)]\)，并非锐门槛。对任意实例序列，若 \(\Delta\to\infty\) 且 \(K_{\min}/\sqrt\Delta\to\infty\)，则
\[
\liminf\sqrt\Delta\,b(H_c)\ge1.
\]
共同平方池使 \(b^*=1/\sqrt\Delta\)，故此大需求序列范围的阶与系数一都不能统一提升。

还有不依赖 \(K_{\min}/\sqrt\Delta\) 预设的精确必要不等式。若原 DAG 的真实 \(b^*\le\eta\)、\(0<\eta<1\)，则完整选择中的任一个满束单独可给 \(b\ge1/q\)，所以 \(q\ge1/\eta\)。取
\[
c_\eta=\lceil1/\eta\rceil-1\in[1,q],\qquad1/c_\eta>\eta.
\]
由于式(1)的根项严格大于 \(\eta\)，某个标签配额比例必须不超过 \(\eta\)。而所有标签配额比例均至少 \(1/D_c-1/K_{\min}\)，故
\[
\boxed{
\Delta\ge1+c_\eta\left(\frac1{\eta+1/K_{\min}}-1\right).
}
\tag{9}
\]
这对**每个给定局部完整选择**成立。沿 \(\eta\to0\)、\(\eta K_{\min}\to\infty\) 的序列，式(9)给 \(\liminf\eta^2\Delta\ge1\)，共同平方池 \(\eta=1/t,K_{\min}=t^2\) 达到系数一。对近二充分归约合同 \(\eta=\varepsilon/2\)，沿 \(\varepsilon\to0\) 且 \(\varepsilon K_{\min}\to\infty\) 的序列，相应必要量为 \(\liminf\varepsilon^2\Delta\ge4\)。没有大需求或趋零参数条件时，不能无条件声称这一渐近平方碰撞障碍；旧 singleton 锐例仅有 \(1/\Delta\)。

一般输入的高碰撞选择仍可能可解；这些必要条件均不充分，不证明困难性。真正未解的是源相关的整数一致性与任意低比例树的解码，且需每固定 \(\varepsilon\) 的位多项式 YES/NO 归约。

## 7. 依赖、机制与证据等级

证明只用本页整数势、Cauchy、容量 Hall 与既有真实任务桥梁；与低重数着色是不同的整体分组机制。交多重图边权 \(|B_x\cap B_y|\) 下，式(3)就是经典缺陷着色/局部最大割势；不称新技术。

**Paper Fact 比较，非导入前提。** Fuchs–Kuhn，*List Defective Colorings: Distributed Algorithms and Applications*，[DISC2023正式原PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol281-disc2023/LIPIcs.DISC.2023.22/LIPIcs.DISC.2023.22.pdf)，PDF第4页/印22:4明确将图分解与势函数机制追溯 Lovász1966。这里只核该机制归属；该文不是本页需求树公式来源，也未承重调用其分布式算法。取得及未内化范围在专题 manifest。全球新颖性、独立论文价值及外部评审未认证。

规范实现：[large_bundle_collision_floor.py](../../../tests/audits/unrelated_machines/large_bundle_collision_floor.py)。独立实现：[large_bundle_collision_independent.py](../../../tests/audits/unrelated_machines/large_bundle_collision_independent.py)。冻结审查：[large_bundle_collision_floor_review.md](../../reviews/unrelated_machines/large_bundle_collision_floor_review.md)。冻结运行：[large_bundle_collision_square_root_audit.json](../../../evidence/runs/unrelated_machines/large_bundle_collision_square_root_audit.json)。

有限精确枚举、实际匹配/树/任务负载与一般证明分开；代码不调用组合最优 oracle。存在仍成立的 fatal objection 时不提升状态。`UM-TARGET-v1` 及其反面均未解决。
