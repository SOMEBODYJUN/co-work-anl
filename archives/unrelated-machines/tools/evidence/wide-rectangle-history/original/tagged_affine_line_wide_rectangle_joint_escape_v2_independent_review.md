# Wide-rectangle tagged affine LINE v2：独立 Exact-only 重构

Reviewer：bicriteria_set_packing_bridge，2026-10-18。只读指定 v2 Exact 后独立推导；未读作者 Proof、v1 Exact 或 rainbow 的其它新推导，也未收到其证明策略。

唯一实际读取的作者合同：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_wide_rectangle_joint_escape_exact_v2.md`

SHA256 `6be53020ad2e0f8f810fa1cbc862fa0ba931378c04b60c2e7d81d34a564d9063`。

候选 ID：`UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2`。

结论：在 Exact 给定的完整显式、非空、tagged-plane 和 fixed distinct-intercept 输入域内，主合同、两个应用、D=1/M=0 端点、完整 ordinary 调度及总位多项式输出均可自足重构，未发现 fatal。证明不需要 state 分布或均匀标签边际。以下为本 reviewer 独立证明；不声称全球新颖性、作者实现认证或源 hard image 满足这些条件。

## 1. 精确域与记号核对

R 是任意素数、R>=2；所有线坐标运算在 F_R 中。G 非空，每个 X_g 是非空 distinct-variable 集，菜单 S_g 是非空显式 indexed states。unused variables 可以存在。变量资源块 U_x={x}×F_R² 彼此分离，每 state 在每个 x∈X_g 上恰有一条完整 line，因此每 state 内没有重复资源。

记 n=Σ_g|S_g|，m=Σ_g|S_g||X_g|R，u=|X|R²，h=|G|。它们分别是 private roots、incidence jobs、resource machines、selectors 的真实数量。因为每组涉及至少一个变量，至少有一个正 degree，故 D>=1、q>=1。每变量的 intercept 对不同 incident groups 单射，因而 d_x<=R，D<=R。逐组定义

\[
M_g=\sum_{x\in X_g}(d_x-1),\qquad M=\max_gM_g.
\]

每项非负，且 M<=q(D−1)。这些是实际输入中可算出的整数，不是隐藏参数或在运行中更改的 intercept。

对每个 (g,x)，A_{g,x} 是显式非空 slope 集，L=min|A_{g,x}|。输入保证其完整 Cartesian product 的每个 label vector 至少对应一个菜单中的 indexed state。该映射不要求唯一；相同 vector 可以对应不同 p 权、不同 marked 集。

每 state 权 p 非负且总和恰为 1。每 line 的显式 marked 子集 E_{g,s,x} 大小<=b；所有不 marked 的真实 cells 私时均<=β，β>=0。b 是 binary integer。条件 L>b(D−1) 按通常整数比较，而非场比较。

## 2. 一个旧 marked 点最多排除一个新 slope

固定变量 x，两个不同 incident groups g,h 的 intercept 分别 j_g、j_h，且 j_g!=j_h。设 Q=(x,z,y) 是 h 的某个已选 state 的 marked 点。因此 Q 在 h 的完整 line 上，若 z=0，则 y=j_h。

g 的候选 slope a 使其 line 经过 Q，当且仅当

\[
y=az+j_g.
\]

若 z!=0，该等式唯一解为 a=(y−j_g)/z；所以该点在 g 的候选集内最多禁掉一个 slope。若 z=0，则 y=j_h!=j_g，不存在任何解，因此禁掉零个 slope。无需修改 intercept，也不对 z=0 求逆。

此结论不涉及 h 的权值、不要求 Q 正权，亦不要求 marked 点在选择之前固定于 label vector；在 h 的 indexed state 选定以后，其实际列表即为固定列表。

## 3. 选态：按组扫描，保证全部 selected marked sets 两两不交

给 G 取任意确定性顺序。假设前面的 groups 已经各选定一个 indexed state，且其 selected marked 点均彼此不同。现在处理 g。

对每个 x∈X_g，收集所有较早且也涉及 x 的 groups h 的实际 selected marked 列表 E_{h,s(h),x}。每个点至多禁掉 A_{g,x} 中一个 slope；故被禁掉的不同 slopes 数至多

\[
\sum_{h\text{ earlier}:x\in X_h}|E_{h,s(h),x}|
\le b(d_x-1)\le b(D-1)<L\le |A_{g,x}|.
\]

因此可选一个不被禁掉的 a_g(x)∈A_{g,x}。对所有 x 各选一个，得到 rectangle 内的完整 vector a_g。由 containment，显式菜单中至少存在一个 indexed state s(g) 与这个 vector 相同。确定性取找到的第一个即可；此时才使用该 indexed state 自己的完整 p 权和 E 列表，绝不以另一同 label state 的权或 marks 代替它。

新 state 的每条完整 line 都避开了较早 groups 在该变量上的全部 marked 点。若新 state 的一个 marked 点与较早 state 的某个 marked 点相同，则新完整 line 会包含那个旧 marked 点，与 slope 的选择矛盾。变量 tag 不同的点不可能相同。因此归纳可完成全部 groups，并保证所有 selected marked 集两两不交。

这个过程允许新 marked 点位于旧 state 的 unmarked 点上；合同只要求该点归 marked owner。这里也未声称任意完整 supports 不交。新 state 的 marks 可以依赖整个选中 vector，甚至不同同 vector states 有任意不同 marks，因为选态只需要新完整 line 避免已经选定的旧 marked 点，不需要预测新 state 的 marks。

## 4. 联合整数 partial allocation 与逐组质量

固定上节输出。写 T_g=T_{g,s(g)}，E_g=⊔_{x∈X_g}E_{g,s(g),x}。定义该组的全部独占点

\[
Q_g=T_g\setminus\bigcup_{h\ne g}T_h,
\]

并直接取真实资源子集

\[
B_g=E_g\cup Q_g.
\tag{1}
\]

所有 E_g 两两不交；Q_g 的点根本不属于任何其它 selected support。因此各 B_g 两两不交，包含本组全部 selected marks，且包含本组全部独占点。若某点在 g 中 marked 而在 h 中 unmarked，则它是 shared 点、不在 Q_h，也不在 E_h，故只归 g；若多个 groups 仅以 unmarked 身份共享一个点，可以全部不领取。没有 fractional 分配或物品复制。

现在控制每组损失。固定 g 以及 x∈X_g。g 的 selected line 与其它每个涉及 x 的 selected line 至多相交一个点：intercepts 不同，若 slope 相同则是不同平行线，无交点；若 slope 不同，两个不同的一次式有唯一交点。跨变量 tag 不相交。故

\[
\left|T_g\cap\bigcup_{h\ne g}T_h\right|
\le\sum_{x\in X_g}(d_x-1)=M_g\le M.
\tag{2}
\]

即使同一其它 group 在几个变量上都与 g 相交，式(2)仍按不同变量资源分别计数；同一变量上多条其它 line 共点只会减少 union 的真实点数，不会破坏上界。

由式(1)，任何没被 g 领取的点都必须是 shared 且在 g 中 unmarked。因此其 private 权<=β，至多损失 M_gβ。归一化给出

\[
\sum_{u\in B_g}p_{g,s(g),u}\ge1-M_g\beta\ge1-M\beta.
\]

同时该和非负，所以逐组质量至少 v=max{0,1−Mβ}。这里不是期望保证；所有 groups 对同一完整选态和同一组 pairwise-disjoint 整数 B_g 同时满足保证。

v=0 时式(1)仍产生合法分配并包含 marks/独占点。β=0 时所有被丢弃的 unmarked cells 都为零权，因而每组领取质量恰为 1。b=0 时全部 marked 列表为空，上节没有被 marked 排除的 slope；条件化为 L>0，选态照常成立，质量界仍由式(2)给出。b=0、β=0 联合时 norm1 非空 state 不可能存在，此空输入子域不构成反例，也无需另作除法。

## 5. 全部 ordinary jobs 的实际 schedule

每 indexed state s∈S_g 的 private root 都是不同机器。每 tagged cell 是不同 resource machine。selector J_g 在本组任意 private root 的时间恰为 1；每 state-resource incidence 是一件独立 job，可在自己的 private 上用时 p，或在其对应 resource 上用时 1，只有这两个 finite options。私时零不删除 job。

输出全部任务的 assignment 如下：

1. selector J_g 放在本组所选 private root；
2. 选中 state 的 incidence 若对应 u∈B_g，放在该 u 的 resource machine；
3. 其它每件 incidence 均放在它自己的 private。这包括选中 state 的未领取 incidences、全部未选 states 的全部 incidences、全部零私时 jobs。

每件任务恰执行一次且使用 finite option。B_g 两两不交，同一 state 无重复资源，所以每台 resource machine 至多一件 unit job、负载<=1。每个未选 private 没有 selector，其全部 incidence 总私时恰为 1。每个选中 private 的负载为

\[
1+\sum_{u\notin B_g}p_{g,s(g),u}
=2-\sum_{u\in B_g}p_{g,s(g),u}\le2-v.
\]

由于 0<=v<=1，resource 与未选 private 的负载也<=2−v。得到完整实际 C_max<=2−v；这里没有遗漏 routing、未被访问状态或零 jobs，也没有只给 partial schedule。

对任意合法调度，至少一个 selector 必须在某台机器上用时 1，因此 OPT(P)>=1。在 v=1 的情形，上述算法给 C_max<=1，从而 OPT(P)=1；若要精确写 C_max=1，也由 selector 负载保证。

## 6. Sparse-positive 与 arbitrary-weight 两个应用

### 6.1 Sparse-positive

若每 state-variable line 至多 b 个正权点，令该 line 的全部正权点为 marked，取 β=0。所有其余点均为零权，满足输入要求。主合同在 L>b(D−1) 下给逐组质量 1；上节给全部原 jobs 的实际 C_max=OPT(P)=1。marked 即使含额外零权点，只要仍符合大小限制，也不影响证明。b=0 时不可能有 norm1 state，所以该特殊 sparse-positive 子域为空。

### 6.2 Arbitrary-weight half

设 D>1 且 L>2q(D−1)²。取

\[
\beta=\frac1{2q(D-1)},\qquad
b=\left\lfloor1/\beta\right\rfloor=2q(D-1).
\]

在每个 state-variable line 上，将 p>β 的点全部标记。每个 state 的总权为 1，所以其所有 p>β 的点数 N 满足 Nβ<=(其总权)<=1；若 N>0，由各项严格大于 β，实际有 Nβ<1。因此 N<=floor(1/β) 足够成立，逐 line 计数也不超过 b。若 1/β 为整数，真实可再省一个点，但本合同使用的松上界 b 仍正确。未标记点满足 p<=β，包括阈值等号。

给定不等式正是 L>b(D−1)。又 M<=q(D−1)，所以 Mβ<=1/2，v>=1/2。主合同给逐组质量至少 1/2 和完整实际 C_max<=3/2。β、b 均可由实际 q,D 做精确 binary 运算；只扫描实际表标记大于阈值的点，不构造 1/β 个额外对象。

## 7. D=1 / M=0、unused variables 与小参数

由于每个出现变量的 degree 至少为 1，D=1 时每变量至多被一个 group 使用；不同 groups 的整个 variable-tagged 资源块分离。任取 indexed state，取 B_g=T_g，即得质量 1 和实际 OPT=1，不需使用 threshold 或除法。

反之，若 M=0，却有某变量 degree>=2，那么任取使用该变量的 group，其 M_g 至少有一项 d_x−1>=1，矛盾。因此在本非空输入域 M=0 等价于 D=1。unused variables 的 degree 为 0，永远不属于任何 X_g，对 M_g 无负贡献；其资源机器空置即可。

q=1、R=2 或只有一组均无几何遗漏；不同 intercept 的 z=0 分支已在 §2 单独处理。部分应用不等式可能在小参数下无实例，这只表示该应用子域为空，不是把主合同扩张为该范围外的保证。

## 8. Rectangle 查验与完整显式位复杂度

Rectangle 合法性可以先核查。对每组，读取所有 indexed state 的完整 label vector，只保留每坐标都在相应 A_{g,x} 中的 vectors，并去重得到数量 c_g。令

\[
P_g=\prod_{x\in X_g}|A_{g,x}|.
\]

被计数的 distinct vectors 是 rectangle 的子集，故 containment 等价于 c_g=P_g。P_g 的 binary bitlength 至多 Σ_x log₂|A_{g,x}| 加常数，因此为显式输入位长多项式；即使其数值超过菜单条数，也只做整数乘法比较，不枚举这个过大的 product。重复 label states 不增加 c_g。选态算法所需的某个给定 vector 可扫描实际菜单找到第一个匹配 indexed state；其 p、E 始终与该 index 绑定。

输入合法性中的 E⊆对应 line、|E|<=b、全部 unmarked p<=β 也可扫描真实标记列表和 line 权表核查；normalize sum 和 fixed-intercept 单射可同样精确核查。素数 R 作为合法域前提，证明只使用该域的实际场运算。

处理一个 g 的一个变量时，只扫描已经选中的相关 marked 列表，按 §2 求其最多一个 forbidden slope，再在实际 A_{g,x} 列表中找一个未被禁止的 slope。哪怕不使用高效数据结构，逐项扫描和逐项比较的次数也由完整显式输入大小的固定次多项式控制。不能将 size<=b 的理论上界误作循环 b 次；只扫描列表真实长度。binary b 巨大也只增加整数比较所需位数。β 极小或为 0 同样只参与 exact rational 比较与 Mβ，不按其分母或 1/β 展开。

选好全部 states 后，扫描它们的实际完整支持，计算真实资源的出现次数和 marked owner，便可输出式(1)的 B_g；hash/排序或朴素比较均为多项式。随后逐项输出 §5 的全部 jobs assignment。

若 N 是全部资源 planes、state label tables、完整 line 权表、marks、rectangles、参数的总 binary bitlength，则 n,m,u,h 均是显式对象数，受 N 的多项式控制。场元素运算在 O(log R) 位整数上进行；inverse 用非零元素求逆，零坐标不求逆。全部 p 及 β 的精确运算可按标准整数/有理运算完成；有限个输入有理数的求和分子分母位长至多其输入总位长的多项式。每组的查表、禁 slope、资源集合操作及所有群组的循环数均为 poly(N)。不需要搜索未知最优值、分配证书或 source witness。

完整普通实例有 n+u 台机器、m+h 件 jobs、2m+n 个 finite entries；每 incidence 的两个 endpoint 属于不同 namespace，即使 p=0 仍恰两个 finite entries。dense 矩阵大小 (n+u)(m+h) 为展开输入的多项式。完整 assignment 包含 m+h 项，机器索引为 binary，输出位长亦多项式。

## 9. 一个严格边界核对及结论范围

仅为核对严格不等式不能在本尺度上任意改成弱不等式：取 R=2、一个变量 x、两个 singleton-state groups，intercepts 0、1；其唯一 slopes 分别 0、1，故两条 line 在 (x,1,0) 相交。两组均只给该点私权 1，并把它标记，其余完整 line cell 权 0。取各 A 为相应 singleton，则 L=1，b=1，D=2，M=1，β=0，恰 L=b(D−1)。marked 无法同时归两组，V=0，普通 OPT=2。此例不满足合同的严格 >，不反驳正文，也不证明所有参数的门槛全局 sharp。

本审查只认证 v2 Exact 的纯几何 wide-rectangle/label-slack 子域：任意合法固定 intercepts、完整输入 state-dependent 权和 marks、重复 label vectors、所有原 ordinary jobs 与上述 bitpoly 量词。未读取/认证作者 Proof；未读取 v1 或其它 reviewer 推导；未运行有限数值试验或程序实现。

此结果不说明 LST、Chan 或其它 hard image 都有满足界的 Cartesian rectangles；不证明一般 tagged-line、SC 或 UM 的改善，也不提供新 hardness。不能靠扩张 alphabet 自动把不满足前提的 compiler 纳入此域。后续作者 Proof read-after 或 canonical 范围审查应另冻，不修改本 Exact-only 记录。
