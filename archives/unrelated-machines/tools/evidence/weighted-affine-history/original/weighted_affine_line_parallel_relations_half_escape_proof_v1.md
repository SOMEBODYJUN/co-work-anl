# 并行线性关系上任意 state 权重的半值逃逸：作者 Proof

候选 ID：`UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。

作者 Proof scratch freeze，2026-10-18。对应且不修改 Exact：

`weighted_affine_line_parallel_relations_half_escape_exact_v1.md`

SHA256 `780454f7a404d2fd17edf2adbf2e8e2fdd8318f98686478547a3be58d4433c7e`。

本 Proof 仅交 root hold；rank 此时仅持 Exact 并独立重构。root 已听过作者口头机制并自行核对，不能记作此候选的盲审。本文件不宣称独立 review 已完成，不修改 repo、Work 或任何旧冻结源。

## 1. 输入、对象与要证结论

固定任意 prime `R>=2` 和任意输入整数 `k>=2`，均不预设为常数。所有场运算在 `F_R=Z/RZ` 中进行。groups 是 `g_j`，`j` 遍历整个 `F_R`；每组涉及同样的 k 个不同变量 `x_1,...,x_k`，每变量的 constraint-degree 恰为 R，且在第 j 组的 incidence index 是 j。

第 j 组的完整允许关系为

\[
A_j=\{a\in\mathbb F_R^k:\ \sum_i a_i=j\}.
\]

菜单确实包含此关系中的每个 tuple。资源宇宙为互不相交的 variable-tagged 并

\[
U=\biguplus_{i=1}^k(\{x_i\}\times\mathbb F_R^2),
\]

而 state `(j,a)` 的支持是

\[
S_{j,a}=\biguplus_{i=1}^k\{(x_i,z,a_i z+j):z\in\mathbb F_R\}.
\]

每个 state 恰含 kR 个不同资源；同一变量 tag 内恰有一条 slope `a_i`、intercept j 的 line。同一 state 没有重复资源，变量间没有身份合并。对所有这些 incidences，完整输入显式给出非负 binary rational `w_{j,a,u}`，且每 state 的权总量恰为 1。允许权为 0，允许依赖整个 state；不使用额外对称性或最大单项上界。

要证可以确定性地选择一个允许 state `a(j)`/group，及两两不交的真实资源子集 `B_j subseteq S_{j,a(j)}`，使每组取得权至少 1/2；还要给出全部 ordinary jobs 的实际调度及总位多项式算法。以下的随机变量只用于证明有限候选集内存在可行见证，最终算法不随机。

## 2. Affine state 候选与准确条件分布

定义两个 affine hyperplanes

\[
\mathcal C=\{c\in\mathbb F_R^k:\ \sum_i c_i=1\},\qquad
\mathcal D=\{d\in\mathbb F_R^k:\ \sum_i d_i=0\}.
\]

它们的大小均为 `R^(k-1)`：前 k−1 个坐标任取，最后一个坐标由和式唯一确定。分别、独立、均匀取 `c in C` 和 `d in D`，并对全部 j 定义

\[
a(j)=cj+d.
\]

由于 `sum_i a_i(j)=j sum_i c_i+sum_i d_i=j`，每个 `a(j)` 确实属于完整允许关系 `A_j`。

固定任意一组 j。映射

\[
\mathcal C\times\mathcal D\longrightarrow\mathcal C\times A_j,
\qquad(c,d)\longmapsto(c,cj+d)
\]

是双射：给定 `(c,a)` 的唯一逆像是 `d=a-cj`，且 `sum_i d_i=j-j=0`。所以随机对 `(c,a(j))` 在 `C times A_j` 上均匀。特别地：

1. `a(j)` 在 `A_j` 上均匀；
2. 对任意固定 `a in A_j`，条件 `a(j)=a` 下，c 仍在 C 上均匀；
3. 因此 c 与这一组的整个已选 state `a(j)` 独立。这一独立性不是对各组 state 之间的独立性主张。

还需逐坐标均匀性。固定 i 和任意 `b in F_R`。因 `k>=2`，条件 `c_i=b` 后，另外 k−1 个坐标须满足一个指定和式；其解数恰为 `R^(k-2)`。与 `|C|=R^(k-1)` 相比，有

\[
\Pr[c_i=b\mid a(j)=a]=1/R.
\tag{8}
\]

不要求不同 `c_i` 相互独立。式(8)对 `R=2` 同样成立。`k=1` 时 c 被固定为 1，式(8)失效；这正是不能删掉该输入限制的原因。

## 3. 固定候选的全部相交结构

现固定任意 `c in C,d in D`。在变量 tag i 中，第 j 组的已选 line 为

\[
y=(c_i j+d_i)z+j=d_i z+j(c_i z+1).
\tag{9}
\]

若 `c_i=0`，这些 R 条 line 均为 slope `d_i`、不同 intercept j，故两两不交。

若 `c_i!=0`，它们全部经过唯一共点

\[
P_i=(x_i,-1/c_i,-d_i/c_i).
\tag{10}
\]

并且任意不同组 j、h 的这两条 line 只能在该点相交：从式(9)相减，交点须满足

\[
(j-h)(c_i z+1)=0.
\]

因 `j-h!=0`，只能有 `z=-1/c_i`，再代入得到式(10)。这包括恰有两组的 `R=2` 情形。

记

\[
H(c,d)=\{P_i:c_i\ne0\}.
\]

不同 i 的 `P_i` 因 variable tags 而互异。H 中的每个资源都属于每一组的已选支持；H 之外的每个资源至多属于一组的已选支持。因而，删除 H 后的所有已选支持两两不交。这里删的是实际资源而不是 fractional 质量；没有复制共点或合并变量。

## 4. 删权的条件期望与总损失至多 1 的候选

对固定 `c,d`，定义第 j 组删去的质量

\[
L_j(c,d)=\sum_{i:c_i\ne0}w_{j,a(j),P_i}.
\tag{11}
\]

H 的点各异且位于已选 state，故 `0<=L_j<=1`。现在固定 j，并条件于这个组所选的整个 tuple `a(j)=a`。此时 d 被写作 `a-cj`，于是对 `c_i!=0`，共点在这一固定 state 的 line 上的坐标可写成

\[
z=-1/c_i,\qquad
-d_i/c_i=-(a_i-c_i j)/c_i=a_i z+j.
\]

映射 `c_i -> z=-1/c_i` 是 `F_R^*` 上的双射。由式(8)，固定任意非零 z，其对应 `c_i=-1/z` 的条件概率恰为 1/R。因此线性期望给出

\[
\begin{aligned}
\mathbb E[L_j\mid a(j)=a]
&=\frac1R\sum_{i=1}^k\sum_{z\in\mathbb F_R^*}
 w_{j,a,(x_i,z,a_i z+j)}\\
&\le\frac1R\sum_{u\in S_{j,a}}w_{j,a,u}
=\frac1R.
\end{aligned}
\tag{12}
\]

不等号仅省略 `z=0` 的非负权；没有假设权与 tuple 无关。先条件于整个 state，再用 c 的条件均匀性，正是任意 state-dependent 权也成立的理由。对 a 再取期望，并对 R 个组相加，得到

\[
\mathbb E\Big[\sum_{j\in\mathbb F_R}L_j(c,d)\Big]\le1.
\tag{13}
\]

有限均匀候选集 `C times D` 中必存在一对 `c,d` 满足

\[
\sum_jL_j(c,d)\le1.
\tag{14}
\]

以下仅使用这样一对确定候选。

## 5. 唯一例外与全部 shared resources 的真实回填

由非负性和式(14)，至多一个组可满足 `L_j>1/2`。若所有组均 `L_j<=1/2`，置

\[
B_j=S_{j,a(j)}\setminus H\quad\text{for all }j.
\]

这些集合两两不交，且每组获得质量 `1-L_j>=1/2`。

若存在唯一例外组 h，置

\[
B_h=S_{h,a(h)},\qquad
B_j=S_{j,a(j)}\setminus H\quad(j\ne h).
\]

H 之外不存在跨组重叠，而 H 全部只交给 h，故这些 B_j 仍两两不交。例外组取得质量 1，其余组仍取得 `1-L_j>=1/2`。无需为不同共点选择不同例外；可以把所有共点一起交给同一个 h。部分或全部共点在某组上权为 0 不影响此论证。

阈值等号也已覆盖：`L_j=1/2` 的组不算例外；若两组恰各损失 1/2，均由第一分支保留恰 1/2 即可。最终 B_j 是完整的资源子集，没有拆分任何一个资源。于是 Exact 的 `V(w)>=1/2` 及 affine-in-j witness 结论成立。

## 6. 确定性枚举与可变参数的总位多项式界

设 `s=R^k` 为完整显式输入中的 states 总数。通过前 k−1 个坐标枚举 C 和 D，候选对数恰为

\[
R^{2k-2}=s^2/R^2\le s^2.
\tag{15}
\]

此处不是固定 k 复杂度分析。输入列出全部 `R^k` 个 states 的全部 `kR` 个权，故 s 本身不大于完整输入长度的一个线性尺度；候选枚举是显式输入长度的多项式。仅有简洁关系公式或权 oracle 的 succinct 输入不在合同内。

对每个候选，计算全部 `a(j)`、H，以及式(11)的精确有理数，测试总损失是否至多 1。式(13)保证枚举中至少一个候选通过；确定性地取首个通过者，再按 §5 输出其 B_j。可以索引显式权表，也可以每次扫描表寻找相应条目；二者均保持多项式。无须计算 V 或 OPT，也不输入源 YES witness。

令 N 为完整输入的总 binary bitlength，包括参数、state/resource 索引、权分子分母和资格。每次总损失至多相加 kR 个输入权条目（每组至多 k 个）。精确相加可使用分母乘积或标准有理数算法；其分子分母位长不超过这些条目总位长的多项式，因而为 `poly(N)`。与 1 和 1/2 的比较也为精确位多项式运算。不同候选间无需累积分母或运行求期望的符号运算。

场元素始终以模 R 的整数表示；加乘、求逆及坐标计算的位复杂度为 `poly(log R)`。候选枚举次数与每次运算数均为 `poly(N)`，故整个算法确定性总位多项式。N 包含本问题要求的完整显式表，不把 `R^{2k-2}` 误称为 `poly(k,log R)`。

输出各组所选 state 及每个已分配资源只需 `O(RkR)` 个索引以内，故位长多项式。若进一步输出下节的全部 job-to-machine assignment，长度也由显式 jobs 数多项式控制。

## 7. Ordinary UM：全部原 jobs 的实际合法调度

实例按 Exact 建立。每个 indexed state `(j,a)` 有不同 private machine `M_{j,a}`；每个真实资源 u 有不同 resource machine `R_u`。每组 selector 的 eligible machines 是本组所有 private，时间 1；每个 incidence `(j,a,u)` 是一件独立原 job，只能在自身 private 上用时 `w_{j,a,u}`，或在资源 u 的机器上用时 1。其它时间均 infinity，无其它 jobs。

由上述 state choices 与 B_j，输出如下完整 assignment：

1. 把 selector `J_j` 放在 `M_{j,a(j)}`；
2. 若 incidence 属于所选 state 且 `u in B_j`，把它放在 `R_u`；
3. 把其它每件 incidence 放回其自身 private。这包括所选 state 中未导出的 incidences、全部未选 states 的全部 incidences，以及私时为 0 的全部原 jobs。

每项均使用其真实 finite entry；没有遗漏未被访问 state 的工作。B_j 两两不交且同一 state 的资源无重，所以每台 resource machine 至多接收一件 unit job，负载至多 1。任何未选 private 的全部 incidences 总量恰为 1，没有 selector，故负载恰 1。每个选中 private 的负载是

\[
1+\sum_{u\in S_{j,a(j)}\setminus B_j}w_{j,a(j),u}
=2-\sum_{u\in B_j}w_{j,a(j),u}
\le3/2.
\]

即使 B_j 内有零私时 incidence，将它导出也只占该独占 resource 的单位负载，不破坏界；也可将这些零 job 留回 private。所有原 jobs 均被合法执行一次。因此这是实际 `Cmax<=3/2` 的完整调度，且 `OPT(P)<=3/2`。selector 的任何 eligible 时间均为 1，所以 `OPT(P)>=1`；本页不从绝对上界推断困难性或 LP gap。

计数也直接核对如下：每组 `R^(k-1)` 个 states，总 states/private 为 `R^k`；tagged resource machines 为 `kR^2`；每 state 有 kR 件 incidences，总计 `kR^(k+1)`；selectors 为 R。每 incidence 有恰两个不同机器的 finite entries，selectors 的 finite entries 总数为 `R^k`，所以 finite entries 恰为 `2kR^(k+1)+R^k`。dense 矩阵项数为 `(R^k+kR^2)(kR^(k+1)+R)`。全部计数与输出位长均依据真实完整对象。

## 8. Source value、k=1 及 arbitrary-relations 对照

对主族，任何完整源赋值 `b in F_R^k` 的坐标和是唯一 field element j，故恰满足那一项 constraint `sum_i b_i=j`。共有 R 项，所以原 source value 精确为 `1/R`。这仅是本显式易判族的准确 value，不是 NP-hard image 认证。

对于 Exact §5.1 的 singleton 关系 `A'_j={(j,0,...,0)}`，每个允许 tuple 的第一变量 line 是 `y=jz+j`，故所有组的第一变量 line 共含 `(x_1,-1,0)`。给这同一个真实资源权 1、其余所有权 0。因 R 至少为 2，两两不交的 B_j 最多使一组取得正质量，所以 V=0。源赋值至多等于一组的 singleton tuple，并可取某一 tuple 达到一组，故 source value 仍为 `1/R`。

对应普通矩阵中，全部 incidences 放 private、selectors 各放唯一 private 给出峰值 2。若存在完整调度峰值严格小于 2，则每组那一件私时为 1 的共点 incidence 都必须导出：否则它与本组必在唯一 private 的 selector 同处而负载 2。于是同一 resource machine 上至少有 R 件 unit jobs，因 R>=2 而负载至少 2，矛盾。故该例实际 OPT 精确为 2，含全部零私时 jobs。

当 `k=1` 时，主关系 `A_j={a_1=j}` 就是上述 singleton 族，因而 V=0 的例子已经说明主定理不延伸到 k=1。`R=2,k>=2` 则没有任何退化缺口，§2 的坐标均匀和后续全部论证仍成立。

最后，任何一般 source 若确有按组选择且完整 supports 两两不交的 full-set packing，任意非负 norm1 权都能保 unit：每组选取那一 state 并取得其全部 support，质量恰 1。实际 ordinary assignment 则导出全部所选 incidences、把未选 incidences留 private；selectors/private/resource 峰值均至多 1。这是 YES full-support 的机械保留，不能替代 weighted NO soundness。

## 9. 结论范围与未主张事项

此 Proof 证明完整 all-tuples 平行线性关系族在任意 state-dependent 非负 norm1 incidence 权下均有半值 partial allocation，且可以确定性总位多项式输出全部 ordinary jobs 的实际 3/2 调度。故只改权、保留这些 groups/states/resources/eligibilities 的接口，不能对包含此族的整个对应 source NO 域一概强制 `V<1/2`。

此族本身易判，singleton 对照也易判；本 Proof 不提供困难性源，不排除额外结构避开本族的 hard image，不排除改动关系或 gadget 的 compiler，不给 arbitrary relations 的半值定理，也不证明一般 UM 的近 2 反面。没有运行有限数值实验，也没有程序实现认证或全球数学新颖性认证。Exact 与 Proof 分别冻结，后续独立核对和作者读后记录必须另存。
