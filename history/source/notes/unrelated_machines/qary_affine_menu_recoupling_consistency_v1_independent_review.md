# q 元 affine 菜单：Exact-only 独立证明与三域边界审查

候选 ID：`UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`。

日期：2026-10-18。此次只实际读取指定 Exact；没有读取作者 Proof、其它 agent 或 root 的推导。本文所有证明独立重构，所有文件操作仅新建 scratch 记录。

## 实际读取对象与结论

`/workspace/scratch/038d9dcc4cac/qary_affine_menu_recoupling_consistency_exact_v1.md`

实际字节数 `4,722`，实际核对 SHA256：

`9d5d0cebf3daa9c78217d32e95f71b80696cd4732f442a22beaf8b22ef50dbd6`

**PASS；未发现 fatal。** 全部 prime powers `q>=2`、全部整数 `t>=1` 上，A–D 均可独立闭合。cyclic 的下界确实允许奇异 a 层的任意全局 partial 分配；all-affine 上界涵盖所有 A,c；coordinatewise 上界涵盖任意非线性单坐标函数，不限制领取集合为 product。q>2 时不把 affine 上界升级到所有 nonlinear selectors。

以下把普通整数 `n=q^t` 记作每个所选 state 的资源数及组数。场中运算和普通整数/有理数计数严格区分。

## 1. 任意 affine selector 的精确 Hall 配额公式

固定任意 `A in F_q^{t x t}`、`c in F_q^t`，令 `ell(g)=Ag+c`。对每个 `a in F_q^t`，定义

\[
L_a=A-\operatorname{diag}(a),\qquad
\nu_a=\dim\ker L_a,
\qquad
\Lambda(A):=\sum_a q^{-\nu_a}.
\]

**独立中间结论：** 该固定 selector 的最大均匀整数领取配额恰为

\[
\tag{1}
k(A)=\lfloor\Lambda(A)\rfloor,
\qquad V(A,c)=k(A)/n.
\]

它不依赖 c。证明同时保留任意 partial 子集的自由，不预设领取按 a 或坐标分解。

对任意组子集 `F subseteq F_q^t`，a 层的资源邻域为

\[
\{(a,L_ag+c):g\in F\}.
\]

每个线性仿射 fiber 恰有 `q^{nu_a}` 个全域原像，所以该层像的大小至少 `|F|/q^{nu_a}`。不同 a 是资源身份的一部分，各层不交。因此

\[
\tag{2}
|N(F)|\ge |F|\sum_aq^{-\nu_a}=\Lambda(A)|F|.
\]

对整数 `k=floor Lambda(A)`，式(2)给所有 F 的 capacitated Hall 条件 `|N(F)|>=k|F|`，故能同时给每个组 k 个不同资源。使用 source-to-group 容量 k、group-to-member-resource 容量 1、resource-to-sink 容量 1 的整数 flow 可实际找出集合。

另一方面，对全部 n 组，每个 a 层的邻域大小恰为 `q^{t-nu_a}=n q^{-nu_a}`，故总并集恰为 `n Lambda(A)`。每组均领取至少 k 个资源必须有 `nk<=n Lambda(A)`，即整数 k 至多 `floor Lambda(A)`。这证明(1)。

特别地，所有配额 `0<=k<=floor Lambda(A)` 都可行；任意整数目标向量 `0<=h_g<=floor Lambda(A)` 也可由一个最大均匀分配删减得到。没有声称仅以全部组总资源数即可判定任意更大的非均匀目标向量：那仍需完整 Hall 条件。优化 min 配额时，(1)已经覆盖所有自由的非均匀 partial 分配，因为若 min 超过该整数界，每组都将至少多取一个资源而违反总并集界。

## 2. Cyclic selector：奇异层与精确 ceil

令 A 为 `(Ag)_i=g_{i+1}` 的循环置换矩阵，包括 `t=1` 时的 `A=[1]`。解 `L_a g=0` 等价于

\[
g_{i+1}=a_i g_i\quad(i\text{ cyclic}).
\]

当且仅当 `prod_i a_i=1` 时存在非零解。此时各 a_i 非零，任给 g_1，其余坐标唯一确定，核维数恰为 1。若乘积不是 1，递推只允许零解，核维数为零。这个递推对任何域特征都成立，不要求 characteristic 不整除 t。

奇异 a 的数量为

\[
s=(q-1)^{t-1}:
\]

前 t-1 个非零坐标任意，最后一个由乘积为 1 唯一决定。t=1 时仍得到 s=1、唯一奇异坐标 a_1=1。

故

\[
\Lambda_{\rm cyc}=n-s+s/q
=n-\frac{(q-1)^t}{q}.
\]

代入(1)即得

\[
\tag{3}
V_{\rm cyc}=\frac{n-\lceil(q-1)^t/q\rceil}{n}
=1-\frac{\lceil(q-1)^t/q\rceil}{q^t}.
\]

这里的除法、ceil 和 floor 都是普通有理数/整数运算，不是场中除法。

也可直接看出 Claim 没有粗暴丢弃全部奇异层：所有非奇异 a 层给每组各一个资源，共 n-s 个；奇异层的选定资源图左度 s、右度 q，Hall 可再给每组 `floor(s/q)` 个资源。因此整数配额为 `n-s+floor(s/q)`，与(3)完全相同。后一步是跨所有奇异层的共同 matching，不要求每个奇异层独立给每组资源，也不要求 B_g 为 product。

## 3. 全部 affine A,c 的上界

需要独立证明任何 A 的 `Lambda(A)` 都不超过 cyclic 值，而不是预设 A 的 rank、shape 或可对角化。

**小引理。** m 个场变量上的非零 polynomial，若每个变量次数至多 1，则至少在 `(q-1)^m` 个 `F_q^m` 点上非零。

证明按 m 归纳。m=0 是一个非零常数。写 `P=x_m P_1+P_0`。若 `P_1=0`，归纳于 `P_0` 并任选 x_m，得到至少 `q(q-1)^{m-1}` 个非零点。若 `P_1!=0`，至少有 `(q-1)^{m-1}` 个前 m-1 坐标使它非零；对每个这样的坐标，关于 x_m 的非恒定一次式恰有 q-1 个非零值。两种情形均给所需界。此引理适用于 q=2 及任意 prime power。

现在考虑

\[
P(a)=\det(A-\operatorname{diag}(a)).
\]

它逐变量次数至多 1，最高全乘积单项式系数为 `(-1)^t !=0`。把它视为关于 a_t 的一次式；a_t 的系数等于一个符号乘以去掉最后行列的 principal minor 的 diagonal determinant polynomial。这个系数 polynomial 的最高全乘积单项式系数非零，故确实不为零。

由小引理，至少有 `(q-1)^{t-1}` 个前 t-1 坐标使该系数非零。对每个这样的坐标，恰有一个 a_t 使 P=0。所以任意 A 至少有

\[
\tag{4}
\#\{a:\nu_a\ge1\}\ge(q-1)^{t-1}
\]

个奇异 diagonal perturbations。t=1 时空 minor 的 determinant 为 1，上述论证仍有效。

每个奇异 a 在 `n-Lambda(A)=sum_a(1-q^{-nu_a})` 中至少贡献 `1-1/q`。故

\[
\tag{5}
n-\Lambda(A)\ge(q-1)^{t-1}(1-1/q)
=\frac{(q-1)^t}{q}.
\]

cyclic 同时达到(4)的最小奇异数量且所有奇异核维数为 1，因而在(5)中达到等号。通过(1)取 floor，得到全部 affine 域的精确最优为(3)，cyclic 达到。c 只平移每个 a 层的 b，整个证明不受 c 影响。

## 4. 任意 coordinatewise functions：不把领取强制成 product

固定任意 `f_i:F_q->F_q`，不要求线性，也不要求不同坐标使用同一函数。第 i 维的 group slope h 给一条含 q 点的 affine line

\[
E_{i,h}=\{(a_i,b_i):b_i+h a_i=f_i(h)\}.
\]

不同 h 的斜率不同，任意两条线恰相交于一个点。把 q 条线依次加入并集：第一条有 q 点，之后每条至少与已包含的第一条相交一次，每次最多新增 q-1 点。因此对任意非线性 f_i 都有

\[
\tag{6}
\left|\bigcup_h E_{i,h}\right|\le q+(q-1)^2=q^2-q+1.
\]

全部组是所有坐标组合，所选 state 支持是 `prod_i E_{i,g_i}`，故全部所选资源的并集**精确等于**各坐标线并集的 product。因此

\[
\tag{7}
|N(G)|=\prod_i\left|\bigcup_h E_{i,h}\right|
\le(q^2-q+1)^t.
\]

任意自由全局 partial 分配若每组至少领取 k 项，就使用至少 nk 项不同资源。式(7)给

\[
k\le\left\lfloor\frac{(q^2-q+1)^t}{q^t}\right\rfloor
=\lfloor(q-1+1/q)^t\rfloor.
\]

这个上界只数真实资源总量，完全没有要求 B_g 自身按坐标分解。

达到上界可以选所有 `f_i=0`，即 affine 矩阵 A=0、c=0。此时 `nu_a` 是 a 的零坐标数，因而

\[
\Lambda(0)=\sum_a q^{-\#\{i:a_i=0\}}
=(q-1+1/q)^t.
\]

应用第1节的全局整数 Hall/flow 得到所需 floor 配额，证明

\[
\tag{8}
V_{\rm sep}=\frac{\lfloor(q-1+1/q)^t\rfloor}{q^t}.
\]

floor 在整个 t 次幂之外。若误将每坐标先取 floor 再相乘，将只得到一个更弱 allocation，不是本次所证模型。这里达到(8)的资源匹配是全局匹配。

## 5. 全部原 ordinary-UM jobs 的精确 makespan

先固定任意完整 selector 函数 ell，不论属于哪个域。写 `k(ell)=n V(ell)`，它是整数，因为所有 B_g 的项数均为整数，有限实例的最优 min 配额取得最大整数值。

**上界。** 取达到 k(ell) 的互异资源集合。每个 selector 放在指定 `(g,ell(g))` private state；只导出该选中 state 对应 B_g 的 incidence jobs；每个其它 incidence job，包括每个未选 state 的全部 jobs，都停在自己的 private machine。每资源峰至多 1，未选 private state 峰为 1，所选 private state 峰至多

\[
1+\frac{n-k(\ell)}{n}=2-V(\ell).
\]

每一原 job 恰执行一次且均走声明的合法机器，因此这是真实完整调度。

**下界，包含任意未选-state exports。** 任取满足指定 selector 函数的完整实际调度。若峰 C>=2，则当然 `C>=2-V(ell)`。若 C<2，每个资源机器最多容纳一件 external-time-1 job。令 B_g 为所选 state 实际导出的资源身份，则它们两两不交；未选 state 也导出的 jobs 只会占用更多资源，不会破坏所选 B_g 的互斥性或替所选根消去私人工作。第 g 个所选根的精确负载为

\[
1+\frac{n-|B_g|}{n}.
\]

所以 `C>=2-min_g |B_g|/n>=2-V(ell)`。这覆盖了所有未选 states 的任意合法 export 行为，未假定它们不导出以求下界。

因此固定 ell 的真实最优峰恰为 `2-V(ell)`。分别在 cyclic、all-affine、coordinatewise 域上优化，得到 Exact C 的三个公式；cyclic 和 coordinatewise 的上界实际见证分别由第2节、第4节的 flow 加上述 job reconstruction 给出。

这些 selector 域是额外供分析的全局选择条件，不是普通 P 中的免费 side constraints。证明不为 P 增添它们。

## 6. 端点和 q=2 的 nonlinear 边界

- `t=1` 时，cyclic 是 `ell(g)=g`，s=1，(3)给 `(q-1)/q`。coordinatewise 是任意单变量函数，但(6)–(8)仍给同样的最佳整数配额 q-1。二者一致，不需要 t>=2。
- `q=2,t=1` 时 cyclic/affine/coordinatewise 最优 V 均为 1/2，实际完整最优峰均为 3/2。
- `q=2` 时 `(q-1)^t=1`，ceil 为 1，故 cyclic/affine 值为 `1-2^{-t}`。本次还能独立闭合其无约束 nonlinear 上界：任意 ell 下，取 g 与逐坐标都不同的 `g+1`，两组选定 state 在每坐标的两条不同斜率线必相交，故整个支持必相交。于是所有组不可能都领取满 n 个资源。整数 min 配额至多 n-1，恰由 cyclic 达到。
- 同一“两个逐坐标都不同的 groups 必相交”对任意 q 都只给无约束 `V<=1-1/n`。q>2 时它通常弱于(3)的 affine 上界。第3节的 determinant polynomial 仅用于 affine ell，不能代入一般 nonlinear ell。这里不认证 q>2 无约束最优，仍属 OPEN。

所有 floor/ceil 只来自整数领取配额。没有在 field 中取 floor/ceil，没有把 `floor(x^t)` 改为 `floor(x)^t`，也没有忽略奇异 a 层可被 partial 利用的资源。

## 7. 固定 q 的极限与 repair 合同的实际否定范围

固定任意 q>=2，有

\[
0\le1-V_{\rm cyc}
\le\frac1q\left(\frac{q-1}{q}\right)^t+q^{-t}\longrightarrow0,
\]

而

\[
0\le V_{\rm sep}\le
\left(1-\frac1q+\frac1{q^2}\right)^t\longrightarrow0.
\]

因此 `V_sep/V_cyc ->0`。对任何 c>0，选择足够大的 t，并输入一个达到 cyclic 最优值的合法全局 partial allocation；任何 coordinatewise-selector allocation 的最小导出质量都低于 c 倍该输入值。由输出域中根本不存在足够高值分配，任意“对每个这样的输入总能事后改成 coordinatewise 并保常数倍”的合同都失败，即使不限制算法效率。

若合同对任意普通 P 高值分配都承诺如此，cyclic 见证已是普通 P 的合法分配，仍给反例。这里没有否定允许改变资源/玩家/模型、采用其它一致性、直接译码 nonlinear recoupling、或只处理另有 physical 结构之 compiler image 的合同。该实例本身提供接近 unit 的 cyclic 完整调度，不是 ordinary-UM 近二 NO 困难性源。

## 8. explicit 总位复杂度与见证恢复

令 n=q^t。groups n；每组 n 个 indexed states，所以 private machines n^2；resource machines n^2；每 state 支持 n 个资源，所以 incidence jobs n^3；selectors n。机器共 `2n^2`，jobs `n^3+n`。

每 incidence 有且仅有两个有限时间条目，selector 有 n 个有限资格，所以 sparse 有限条目数恰为 `2n^3+n^2`。若给 dense 矩阵，条目数为 `2n^2(n^3+n)`，对其真实输入长度计费即可。

private 时间是普通有理数 `1/n`，编码 `O(log n)=O(t log q)` 位。域元素、资源标签和 state/group 标签都有 `O(t log q)` 位。给定域表示及其多项式位时间基本运算，可通过显式枚举 `(g,ell,a)` 并计算 b 生成所有 incidences，时间多项式于完整显式大小；不声称 polynomial in `(t,log q)`。

最优 affine 域不需枚举 `q^{t^2}` 个 A：直接选 cyclic 最优见证。最优 coordinatewise 域不需枚举所有函数表：直接选 `f_i=0`。两者选中 state 图均有 n 个 group 顶点、至多 n^2 个资源顶点及恰 n^2 条 incidence edges。整数 flow 的 group demand 不超过 n，容量可二进制表示；无需按更大隐藏数值复制。随后逐个输出全部 `n^3+n` 个原 jobs 的机器标识，总输出位数亦多项式于完整显式输入。

即使为某个给定 A 验证(1)，也只需枚举显式的 n 个 a 并在 F_q 上求 t 阶矩阵 rank；证明 all-affine 最优不靠枚举所有 A,c。所有 floor/ceil 值可用 `O(t log q)` 位的整数幂及有理数计算。

## 9. 有限辅助检查及状态

独立 exact arithmetic 辅助检查枚举了以下全部 A：`(q,t)=(2,1),(2,2),(2,3),(3,1),(3,2),(4,1),(4,2),(5,1),(5,2)`，合计 1,504 个矩阵、24,664 次 diagonal-perturbation rank 计算；GF(4) 使用 modulus `x^2+x+1` 的二元域运算。每个矩阵均满足奇异数和 Lambda 上界，各域最大整数配额与 cyclic 公式吻合。

另对 q=2,3,4,5 枚举全部 3,412 个一维函数，线并集均至多 `q^2-q+1`，且最大值达到该界。有限计算只是辅助；全部 prime powers 和所有 t 的认证依据是上面的域上线性代数、polynomial 非零计数和 Hall 证明。

未读作者 Proof 或其它推导。未认证 novelty、外审、软件实现、q>2 无约束 nonlinear 最优、一般 UM 算法或 near-two hardness。源 Exact 未修改。
