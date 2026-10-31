# BN-CLONE-v2：一般R的多项式失败证书与coNP归属

2026-10-20。作者的一般utility cloning分类问题为A（Becker等 arXiv:2509.08767v3 §8）；本显式min-of-linear矩阵识别问题及以下复杂性归属是研究者派生C。本结论是**coNP上界**，没有给coNP-hardness、coNP-completeness或tight complexity。数学证明自足，文献新颖性仍待核查。

## 1. 判定语言与所有量词

输入：二进制编码的非负有理R×m矩阵A，所有行向量a_r∈Q_+^m；令 `u_A(delta)=min_{r∈[R]} a_r·delta`，delta位于m项目的总预算1 simplex。输入大小L为完整矩阵及维度编码的位长。

语言CLONE-INVARIANT包含恰好满足如下性质的A：

对每个整数D≥1、每个1≤k≤D、任意有限外部玩家及其正有理预算（总和1−k/D；k=D允许没有外部玩家）、任意这些外部玩家的utility functions、由k个utility均为u_A且预算**均为1/D**的clones与这些外部玩家组成的budget-aggregation game，**该游戏的每一个NE profile**在把k个clones合并为一个预算k/D、utility为u_A、策略取原k个策略之和的玩家后仍为NE。

外部utility不需满足凹性；本判定只关心同偏好clones的合并是否破坏NE。失败证书构造中的外部utility甚至可选系数全1的线性utility。若要求其他原玩家也全部复制为1/D预算，同样可实现，见§4。

**Theorem.** 对任意R,m，`CLONE-INVARIANT ∈ coNP`。具体地，A不满足该性质，当且仅当存在下列总编码长度poly(L)的有理证书，可仅用poly(L)次有理算术和比较验证。

## 2. 证书格式与确定性验证

证书为 `(I,S,delta,z,(xi^(j))_{j∈S},y)`：

1. 非空active row index集合 `I⊆[R]`、非空coordinate集合 `S⊆[m]`。
2. 有理delta∈Q_+^m，sum_j delta_j=1；有理z。要求
   - `a_r·delta=z` 对所有r∈I；
   - `a_r·delta>z` 对所有r∉I；
   - `delta_j>0` 对所有j∈S。
3. 对每个j∈S，有理凸组合系数 `xi^(j)∈Q_+^I`，sum_r xi_r^(j)=1。记 `g^(j)=sum_{r∈I} xi_r^(j) a_r`。要求 `g_j^(j)≥g_s^(j)` 对每个s∈[m]。它认证纯投j的clone是best response。
4. 有理非负向量 `y=(y_{j,s})_{j∈S,s∈[m]}`。定义矩阵M，行索引(j,s)、列索引r∈I：

   `M_(j,s),r=a_rs−a_rj`。

   要求 `M^T y ≥ 1`（逐列），即对每个r∈I均有

   `sum_{j∈S,s∈[m]} y_{j,s}(a_rs−a_rj)≥1`。

第四项是**共同supergradient LP不可行的归一化Farkas证书**。这里不用验证S恰好为全部可实现最大坐标U_delta：任何这样一个失败子集S就足够。这避免额外的全称量词。

共同LP是

`xi≥0, 1^T xi=1, M xi≤0`。

若它可行，则 `y^T M xi≤0`，但 `M^T y≥1` 又给 `y^T M xi≥1^T xi=1`，矛盾。因此没有一个g∈conv{a_r:r∈I}能让S全部成为最大坐标。

反过来，此共同LP不可行时Farkas替代给这样的y。可直接从标准式推导：将不等式写作 `M xi+t=0, t≥0`，连同 `1^T xi=1, xi≥0`。不可行证书为y≥0、标量tau<0且 `M^T y+tau·1≥0`；除以−tau得到上述 `M^T y≥1`。

## 3. Soundness：证书确实产生失败

delta处凹superdifferential为 `P_I=conv{a_r:r∈I}`。对每个j∈S，第三项给g^(j)∈P_I且j为最大坐标。选整数D足够大，令eta=1/D<min_{j∈S}delta_j且|S|/D<1。放|S|个utility均为u_A、预算eta的clones，第j个纯投项目j。supergradient inequality对该clone的每个可行偏离给

`u_A(delta−eta e_j+x)≤u_A(delta)+g^(j)·(x−eta e_j)≤u_A(delta)`。

所以每个clone都是best response。剩余向量r=delta−eta·sum_{j∈S}e_j由一个预算1−|S|/D的outside玩家提供，其utility为 `sum_x delta_x`，因此其任意策略均最优。当前profile是NE。

合并clones后的策略support正好S。对有限polyhedral凹utility在simplex上的最大化，KKT必要充分条件是存在g∈P_I使该策略的全部正坐标均为g的最大坐标；第四项排除了这样的共同g。因此合并后的玩家不是best response，profile不再是NE。等预算反例成立。

## 4. Completeness与所有证书的位长

若CLONE-INVARIANT失败，取一个失败NE，并记其总分配delta0、active set I；S为被合并clones全部正支出坐标的并集。每个j∈S有delta0_j>0。某个原clone正投j，其best response的polyhedral KKT给一个g^(j)∈P_I，使j为最大坐标。合并后不是best response，故共同LP不可行。S最多m个坐标，即使原失败实例的clones很多，也不需要把它们列入证书。

原delta0可以是irrational，不能直接拿它作NP证书。改用如下有理margin LP，变量(delta,z,epsilon)：

`delta≥0, sum delta=1, 0≤epsilon≤1;`

`a_r delta=z (r∈I); a_r delta≥z+epsilon (r∉I);`

`delta_j≥epsilon (j∈S); maximize epsilon.`

delta0使某个epsilon>0可行，因为有限个strict active gaps及正support坐标有正的共同下界。LP的delta与epsilon有界，z由某一active row约束决定也有界，故最优值达到且>0。选一个最优basic feasible solution，获得**poly(L)位长的有理delta,z及正epsilon**。

位长理由不需要任何数值容差：将每行的有理分母清除后，系数整数的位长仍为poly(L)；basic solution由至多poly(L)阶非奇异子矩阵确定，Cramer法则与Hadamard determinant界给每个分子/分母poly(L)位长。

每个xi^(j)的可行域是有理simplex与有限线性半空间的交，非空紧多面体；选其basic feasible solution，同样有poly(L)位长。共同LP的Farkas系统 `y≥0,M^T y≥1` 非空有理，且非负正交象限中的多面体为pointed，故有basic feasible solution，Cramer/Hadamard同样给poly(L)位长y。共有至多m个xi^(j)，y至多m²个分量，故**全部证书总位长仍为poly(L)**。

可选D为一个2的幂，满足 `D>max(2|S|,2/min_{j∈S}delta_j)`。由于delta的位长poly(L)，D的**二进制位长**也为poly(L)。外部预算及r亦有poly(L)位长。若要求全体玩家都预算1/D，把线性outsider分成D−|S|个相同utility的clones，将r任意分解为这些预算的策略向量即可；所有这些玩家仍最优。我们以二进制D和r压缩描述这一组，**不输出D个玩家，不把数值D误认为poly(L)**。

验证证书只需检查索引、非负性、有限有理等式/严格不等式及矩阵向量乘法，所需操作次数和中间整数位长均poly(L)。因此补语言在NP，原语言在coNP。证毕。

## 5. 一个完全有理的Farkas证书toy

对

`A=[[2,0,3/2],[0,2,3/2]]`，

取I={1,2}、S={1,2}、delta=(1/4,1/4,1/2)、z=5/4；xi^(1)=(1,0)、xi^(2)=(0,1)。取 `y_(1,3)=y_(2,3)=1`，其余y为0。于是对两行r都得到

`(a_r3−a_r1)+(a_r3−a_r2)=1`。

这正是 `M^T y=(1,1)`，无需浮点solver或严格间隙猜测。可以选D=4，两个目标clones各预算1/4；outside预算1/2。`verify_cloning_conp_certificate.py/json`实际用Fraction检验全部证书约束。

## 6. 结论的限度

coNP归属是前一几何接口的标准rational-polyhedral证书推论，只能当可靠的复杂性上界和后续hardness基线。它不说明识别polytime，也不说明coNP-hard；不能与按R的2^R算法合起来宣称tight分类。公开原题A问一般utilities的分类；本有限矩阵语言C并非作者原题的全部范围。
