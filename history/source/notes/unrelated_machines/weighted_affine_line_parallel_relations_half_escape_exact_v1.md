# 任意 state 权重的仿射线菜单：并行线性 NO 关系的半值逃逸

候选 ID：`UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。

Exact-first scratch freeze，2026-10-18。本文件只陈述精确对象、量词、结论与范围，不附 Proof。root 已收到作者口头策略，因此 root 的后续核对不得记作对本候选的盲审；可另安排未读策略的 reviewer。原 LST uniform 合同和全部旧源不修改。

## 1. 现行 source 约定及本族的精确 specialization

沿用已实际重读的 LST affine-line source 合同：`lst2025_affine_line_source_uniform_menu_compilation_exact_v1.md`，SHA256 `a1334a82f1acf7fd9562c2d44e6620b84b5a1acd37993ce3c7131b81a8e56472`。group 是 constraint，state 是该 constraint 的一个允许 tuple；不是把所有 tuples 各自当group。

取任意 **prime R>=2、整数 k>=2**。有限域严格为 `F_R=Z/RZ`。变量恰为相同 k 个不同变量 `x_1,...,x_k`，groups 为 `g_j`、j遍历全部F_R。每项constraint均涉及这相同的k个变量，各位置不重复；每变量的constraint-degree恰R。给所有变量使用相同的注入incidence indices

\[
j_{x_i}(g_j)=j\in\mathbb F_R.
\]

第j组的允许关系是**全部**满足下式的tuple，不删减或指定其中一个：

\[
\tag{1}
A_j=\{a=(a_1,\ldots,a_k)\in\mathbb F_R^k:
\sum_{i=1}^k a_i=j\}.
\]

每个菜单非空，恰有 `R^(k-1)` 个indexed states。同一k变量可视为k-partite CSP每part一个变量。这一族的原CSP value精确为 `1/R`：任何完整赋值只能满足恰一项不同右端constraint。

资源有显式变量tag：

\[
U_i=\{x_i\}\times\mathbb F_R^2,
\qquad U=\biguplus_{i=1}^kU_i.
\]

第j组state a的完整支持严格为

\[
\tag{2}
S_{j,a}=\biguplus_{i=1}^k
\{(x_i,z,a_i z+j):z\in\mathbb F_R\}.
\]

label a_i 是slope，constraint index j是intercept。每变量tag有R²项，每state恰kR个不同资源。同一state对每个变量恰一条line，没有资源重数或跨变量身份识别。

## 2. 任意 state-dependent 非负归一化权重

对**每个** `j,a,u`、a∈A_j、u∈S_{j,a}，输入任意显式binary rational

\[
w_{j,a,u}\ge0,\qquad
\sum_{u\in S_{j,a}}w_{j,a,u}=1.
\tag{3}
\]

允许零系数。各state的权可以完全不同，可依赖整个tuple a、group j、variable和cell；不要求共同item权、line内均匀、各变量质量相同、某种对称性、small最大单项或输入分布。没有概率抽样输入承诺。

定义

\[
\tag{4}
V(w)=\max_{a(j)\in A_j,\ B_j\subseteq S_{j,a(j)},\ B_j\text{两两不交}}
\min_j\sum_{u\in B_j}w_{j,a(j),u}.
\]

B_j始终是完全自由的global partial subsets，不要求它是每变量或每坐标的product，也不要求全部state choices来自一个一致的CSP赋值。

## 3. 待独立审查的主 Exact

**对所有R,k及所有满足(3)的完整显式权表，都有**

\[
\boxed{V(w)\ge1/2.}
\tag{5}
\]

更具体，可以将达到该保证的state choices限在下列affine-in-j族中：存在向量 `c,d in F_R^k`，满足

\[
\sum_i c_i=1,\qquad\sum_i d_i=0,
\qquad a(j)=cj+d\quad(j\in\mathbb F_R),
\tag{6}
\]

以及pairwise-disjoint真实资源子集B_j，使每组取得质量至少1/2。式(6)保证a(j)∈A_j，但不声称这些tuples构成某个全局一致的CSP赋值。

有确定性算法按完整显式输入总位长多项式输出这样的state choices和B_j。不输入OPT、源YES witness、未知allocation、额外随机性假设或implicit权值oracle；不把fractional物品当成最终allocation。

不主张1/2是所有权表或此族最优的统一常数，不主张每一种affine-in-j choice都达到1/2，也不主张任取local states都有该保证。k>=2是本Exact正式输入条件，不扩成k=1。

## 4. 实际全部原 ordinary-UM 矩阵

对上述每个weighted菜单建立P：

- 每 `(j,a)` 一台独立private机器M_{j,a}；
- 每 `u in U` 一台global resource机器R_u，所有variable tags及private/resource namespaces互异；
- 每g_j恰一件selector J_j，时间1、eligible private machines恰为本组全部states；
- 每 `(j,a,u)` 恰一件不同incidence job，仅可在M_{j,a}时间w_{j,a,u}，或在R_u时间1。

其余时间infinity，无其它jobs、preloads、guards、free一致性或拒绝。零私时job仍是原job；全部未选states的全部jobs也在实例内并必须执行。

(5)的constructive witness可转换为全部原jobs的合法实际调度：每selector放在所选state；仅把B_j对应incidences导出；所有其它incidences留自身private，包括全部未选state。由此

\[
\boxed{\operatorname{OPT}(P)\le3/2.}
\tag{7}
\]

每资源峰至多1，每未选private峰1，每选中private峰至多3/2。selector给OPT>=1。该结论是这同一明确族对任意state-dependent权的absolute上界，不是对所有weighted LST relations的上界。

## 5. 不可遗漏的对照与范围

### 5.1 arbitrary relations 下确可由权重制造零 partial value

以下只是scope示例，不是hardness Claim。仍取相同k变量、R组、degreeR、index j、tagged resources和式(2)，但把允许关系改成 singleton

\[
A'_j=\{(j,0,\ldots,0)\}.
\]

在每组唯一state中，把总权1放在共同资源 `(x_1,-1,0)`，所有其它权为0。归一化成立，原CSP value仍1/R，而weighted partial最小值为0，完整普通P的OPT精确2。

所以“所有任意relations／所有权重仍有半保留”不成立。主Exact需要式(1)的完整all-tuples关系，而不是只需要degree与line几何。k=1时，式(1)自己就退化为此singleton情形，因此不能把(5)的k>=2删掉。

此易判singleton例只展示权能破坏uniform半保留；不提供NP-hard源、polynomial reduction soundness或困难性。

### 5.2 主Exact对真实source的准确义务

主族为degreeR、alphabetR的k-partite CSP，原value1/R；对k>=4、充分大R，它的值处于原primary theorem的low-value数量级。但这个族本身易判，不把它误作已知hard子像。

如果一个**只改式(2)内incidence weights、不改groups/states/resources/eligibilities**的接口声称对整个相应CSP NO promise域都保证所有partial allocation某组质量小于1/2，则式(1)本族使该接口失败，不论它如何选(3)的权。若构造只处理另一个有额外结构、且避开本族的hard image，或允许预处理并输出不同gadget，本Exact不排除该路线。

对一般fully satisfiable source，full-set packing见证一旦资源全不交，每state总量1的任意非负权都可由完整领取保unit。这是full-support YES的机械保留，不给任意low-value source的weighted partial soundness。本页没有提供normalized YES1／NO任意tiny的复杂性源，也不从这个边界推一般UM算法或反面。

## 6. 显式计数与位复杂度合同

groups为R；states/private机器为 `R^k`；resource机器为 `kR^2`；incidence jobs为 `kR^(k+1)`；selectors为R。有限时间条目数

\[
2kR^{k+1}+R^k,
\]

dense矩阵则有 `(R^k+kR^2)(kR^(k+1)+R)` 项。全部权表与有限资格显式列出，以其真实总binary bitlength计费；不是poly(k,logR)的succinct接口。

场运算在prime R模域按位多项式计算；所有负号、加乘、式(6)都为场运算。质量和1/2、private负载和ratio则为普通有理运算。权分子分母精确操作及全部machine assignment输出的位长为总输入长度多项式；没有按更大隐藏数值或分母复制对象。

本Exact不附Proof、不列随机数值实验、无实现/外审/全球新颖性认证。任何未来Proof或独立记录另冻；不改现有源字节。
