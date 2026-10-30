# 全状态择证的单位速度障碍与循环支撑边界

本稿提供全状态择证的一项精确方法障碍：不能把合法对偶分布额外要求为确定性 selector 的单位速度平稳分布。这项限制连仿射费用的实例无关有限倍率都无法处理，尽管仿射费用具有精确纯均衡。它不证明或否定本题的全类 O(d/ln d)-PNE 命题。

## 命题身份

**ID/version：** `WC-SELECTOR-UNIT-SPEED-STATIONARY-BARRIER-v1`。

**中文数学名称：** 全状态择证中单位速度平稳分布的无界损失。

**Exact Statement。** 对每个实数 α≥1、每个整数 d≥1，存在有限正有理权向量、每名玩家两个动作标签的模板以及合法全状态 selector h，使不存在同时满足

\[
\lambda\ge0,\qquad \sum_s\lambda_s=1,\qquad
P_h^T\lambda=\lambda,\qquad B_h(\alpha)^T\lambda\le0
\tag{1}
\]

的向量。其中 P_h 是在每个状态以概率1跳到 h 所选真实单方偏离后状态的确定性转移矩阵；B_h(α) 是 `WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1` 对全部非空动作关联签名及全部次数0,…,d建立的矩阵。失败由一次项的一列见证。

更具体地，对下文整数 K 构造，P_h 只有一个有向循环，唯一平稳概率是该循环上的均匀分布；当 α<(2K+1)/3 时，它违反一条一次项 dual 不等式。但同一 h 在仅含次数0、1的完整签名矩阵上，α=1有显式非平稳 dual λ_*，并且所有列积均为0。对任意 α≥1，λ_*仍是该仿射子矩阵的 dual。更一般地，下文仿射循环重加权引理对任意有限动作模板及任意合法h给出这样的仿射dual，包括h选当前动作的自环。

**Objects / Domain / Quantifiers。** 状态空间是有限二元积空间；权重严格正、有理；α为任意有限实数；d为任意正整数。每个 h(s)指定恰好一名玩家和其另一个合法动作；在完整签名规范模型中，两标签可以由零费用的单点签名资源区分，因此确为不同资源子集策略。λ可依赖完整h，障碍只增加P_h^Tλ=λ这一限制。

**Assumptions / Definitions / Scope。** 费用、成本和偏离按 MODEL。状态中资源负载及偏离后负载各自重新计算。这里“平稳”精确指单位速度确定性链；不包括可另选状态相关持留率的时间变换。h不要求在任何某个预选费用向量下处处改善；有限择证替代本来就须量化全部合法h。

**Conclusion。** 额外要求单位速度平稳分布的 dual 方案不能给出任何只依赖d的有限普遍倍率。一般对偶方案、其他概率构造、全类均衡存在性均不在否定范围。

**Dependencies。** 有限动作完整签名矩阵的定义；下述有限确定性图结构；自足的仿射资源势恒等式。没有导入外部均衡定理。

**Evidence。** 下文对任意K的一般证明；配套Fraction审计在K=1,2,3,4逐状态检查h与唯一循环，逐全部非空签名和次数0、1检查单边恒等式及dual，并核验严格/等号边界。有限审计不替代任意K的一般证明。

**Counterevidence / Objections。** 本构造没有给出不存在α-PNE的游戏，不能用其推断主目标。所写λ_*只保证仿射列；不得默认为次数2,…,d的列也可行。允许状态相关持留率时，非平稳λ_*可以变成另一条链的平稳分布，故不能扩大为所有平稳概率方法的障碍。

**Status。** complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。已先独立重构并攻击冻结正文，实际覆盖见配套审查。未外审，全球新颖性未评估。Truth为所述额外条件障碍；Value为排除一条自然但过强的概率限制；Mechanism为权重引起的访问频率与势增量失配；Ambition为全状态dual研究工具，不是主目标解答。

**Related Files。**

- 既有接口：`research/current/weighted_congestion/template_certificates/finite_action_duality.md`。
- 配套代码：`tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py`。
- 审计参数与输入：全部由代码显式构造，无随机seed、无外部输入、无浮点误差或求解器容差。

### WC-AFFINE-SELECTOR-CYCLE-DUAL-v1 — 任意仿射择证的循环权重对偶

- **Exact Statement / Quantifiers：** 对任意固定有限正实权、有限动作数的MODEL模板、任意合法全状态selector h（允许选择当前动作且保留其玩家标签）、任意h图有向循环Q，令λ_s=w_(i(s))/Σ_(t∈Q)w_(i(t))（s∈Q），环外0，则对全部动作关联签名的次数0、1列，B_h(1)^Tλ=0。每个实α≥1均有B_h(α)^Tλ≤0。
- **Objects / Domain / Assumptions / Definitions / Scope / Conclusion：** 有限正权、真实偏离、完整签名成本；循环可为self-loop，不要求h处处改善。仅仿射列；次数≥2无此结论。正文§四给全部证明。
- **Dependencies：** 有限确定性图存在循环、资源仿射加权势差恒等式、环上望远镜；矩阵定义沿用既有接口。
- **Evidence / Counterevidence：** 先独立重构再冻结攻击；Fraction枚举含self-loop的tagged selectors。不声称λ必为单位速度链的平稳分布，亦不把该lemma推广到高次。
- **Status：** complete direct proof; independently reconstructed and exactly audited; unrefereed。Truth为显式dual；Value为仿射基准机制；Novelty未认证；Mechanism为移动者权重重加权；Ambition不含全类高次统一界。
- **Related Files：** 本文、配套review/code/frozen run如下。

## 一、矩阵与单位速度链

记玩家集合为N、每人的动作标签为0,1，状态空间Ω={0,1}^N。全部动作位置集合是N×{0,1}。每个非空签名σ是该位置集合的一个非空子集。令

\[
x_\sigma(s)=\sum_iw_i\mathbf1_{(i,s_i)\in\sigma}.
\]

h在s选择玩家i(s)及另一个标签，偏离后状态记H(s)。对于列(σ,k)，

\[
B_h(\alpha)[s,(\sigma,k)]
=\mathbf1_{(i(s),s_{i(s)})\in\sigma}x_\sigma(s)^k
-\alpha\mathbf1_{(i(s),H(s)_{i(s)})\in\sigma}x_\sigma(H(s))^k.
\tag{2}
\]

常数项按x^0=1处理；未使用资源时指示量消去其费用。令P_h[s,t]=1当t=H(s)，否则为0。本文研究的是将P_h^Tλ=λ附加到原dual的后果。

## 二、完整h构造及唯一循环

取整数K≥1。玩家为轻玩家1,…,K及重玩家H，按此顺序编号；权重是

\[
w_1=\cdots=w_K=\varepsilon=K^{-2},\qquad w_H=1,
\qquad W=\sum_iw_i=1+K^{-1}.
\]

用状态(L,b)表示当前动作1的轻玩家集合L⊆[K]和重玩家标签b。定义

\[
a_j=(\{1,\ldots,j\},0)\quad(0\le j\le K),
\qquad
b_j=(\{j+1,\ldots,K\},1)\quad(0\le j\le K).
\]

空集合按常规定义。a_j的重玩家标签为0，b_j的为1，同族内轻玩家集合彼此不同，所以这些2(K+1)个状态互异。在它们上定义

\[
H(a_j)=a_{j+1}\ (0\le j<K),\quad H(a_K)=b_0,
\]
\[
H(b_j)=b_{j+1}\ (0\le j<K),\quad H(b_K)=a_0.
\tag{3}
\]

各边依次插入轻玩家、插入重玩家、移除轻玩家、移除重玩家，均为恰好一名玩家的合法二动作偏离。这些状态构成循环Q。

**环外完整定义。** 若s∉Q，选择当前标签为1的最小编号玩家，把其标签改为0，定义H(s)为所得状态。这样的玩家一定存在：唯一没有1的状态是a_0∈Q。即使一次删去后进入Q的中间节点，也不产生问题，之后按(3)沿Q运行。

**所有环外轨道有限步进入Q。** 在首次进入Q之前，每步使用环外规则，使标签1的数目严格减少1。如果一直未进入Q，至多K+1步后即得到全0状态a_0∈Q，矛盾。因此每个状态至多K+1步进入Q，且Q是唯一有向循环。环外不存在另一个循环，因为它会使非负整数“标签1数目”沿一周严格下降。

**平稳概率唯一。** 由上述进入时间界，P_h^{K+1}把任意初始概率全部送入Q。因此若λ平稳，λ在Q外必为0。Q上每点唯一可能的正质量前驱是其Q内前驱，平稳方程于是强制各环点质量相等。归一化给出

\[
\lambda^{\mathrm{st}}_s=
\begin{cases}1/[2(K+1)],&s\in Q,\\0,&s\notin Q.\end{cases}
\tag{4}
\]

## 三、一次项列的无界违反

选择签名σ_*={(i,1):i∈N}与次数k=1，即每名玩家仅在动作1使用资源，费用为c(x)=x。记循环上各边原移动玩家费用的总和为D，真实偏离后移动玩家费用的总和为A。

插入轻玩家j的原费用为0，后费用为jε；插入重玩家的原费用为0，后费用为1+Kε。移除轻玩家j前的负载为1+(K−j+1)ε，后费用为0；最后移除重玩家的原费用为1，后费用为0。故

\[
\begin{aligned}
D&=1+K+\varepsilon K(K+1)/2
  =\frac{(2K+1)(K+1)}{2K},\\
A&=1+K\varepsilon+\varepsilon K(K+1)/2
  =\frac{3(K+1)}{2K}>0,
\end{aligned}
\]

以及D/A=(2K+1)/3。直接代回(2)、(4)得到

\[
\bigl(B_h(\alpha)^T\lambda^{\mathrm{st}}\bigr)_{(\sigma_*,1)}
=\frac{D-\alpha A}{2(K+1)}
=\frac{2K+1-3\alpha}{4K}.
\tag{5}
\]

给定α≥1，取整数K>(3α−1)/2（所以可取K≥2），(5)严格为正。因此唯一平稳概率不是dual，其他平稳概率不存在，证明(1)不可行。一次项列属于每个d≥1的完整列集，故结论对所有这些d成立。等号α=(2K+1)/3时本列积恰为0；我们不将该等号边界虚称为违反。

## 四、仿射循环重加权与显式非平稳dual

### 任意仿射模板的循环重加权引理

**精确陈述。** 固定任意有限正权玩家向量、任意有限非空玩家动作标签族、全部非空动作签名，并令h是任意合法全状态selector，允许选择当前动作。取H的一条有向循环Q'；每个s∈Q'所选玩家记i(s)，即使H(s)=s也保留其标签。定义

\[
Z=\sum_{s\in Q'}w_{i(s)}>0,\qquad
\widehat\lambda_s=
\begin{cases}w_{i(s)}/Z,&s\in Q',\\0,&s\notin Q'.\end{cases}
\tag{6a}
\]

则对全部签名和k=0,1，\(B_h(1)^T\widehat\lambda\)的该坐标恰为0；对任意α≥1，各该坐标≤0。不要求Q'包含所有玩家，不要求每名玩家移动相同次数，不要求动作二元。特别地，该引理依有限择证替代重建所有仿射模板的精确PNE存在；但不声称λ具有单位速度平稳性。

**证明。** 有限非空确定性图必含有向循环：从任一状态反复应用H，首次重复之间即给循环。任意单边的逐签名仿射势恒等式(8)不依赖二动作或特定Q，故以(6a)在Q'上求和，右侧望远镜为0。若Q'为自环，则两端状态相同，(2)在α=1每列为0；仍由相同公式处理。α增大时只减非负项。Z有限、严格正，故(6a)始终为合法概率。

### 障碍构造的具体分布

在前述Q中定义

\[
\lambda_*(s)=
\begin{cases}
w_{i(s)}/(2W),&s\in Q,\\
0,&s\notin Q.
\end{cases}
\tag{6}
\]

每名玩家在Q中恰移动两次，所以Σ_sλ_*(s)=2Σ_iw_i/(2W)=1。K≥2时轻重玩家权重不同，λ_*在Q上不均匀，由平稳概率唯一性它不是P_h的平稳分布。

固定任意签名σ，令U_σ(s)={i:(i,s_i)∈σ}。对任意U⊆N记x(U)=Σ_{i∈U}w_i，并定义

\[
F_0(U)=x(U),\qquad
F_1(U)=\frac{x(U)^2+\sum_{i\in U}w_i^2}{2}.
\tag{7}
\]

当i插入U时，F_0增量为w_i，F_1增量为w_i[x(U)+w_i]。移除时相应取负的移除前加权费用。如果i的两个动作都使用该资源或都不使用，则单方偏离不改变用户集、两端移动玩家费用相等。因此对于k=0,1的每一条边s→H(s)，均有

\[
w_{i(s)}B_h(1)[s,(\sigma,k)]
=F_k(U_\sigma(s))-F_k(U_\sigma(H(s))).
\tag{8}
\]

(8)处理真实两端负载，不冻结费用。用(6)在Q上求和，右侧沿循环望远镜，得到

\[
\bigl(B_h(1)^T\lambda_*\bigr)_{(\sigma,k)}=0
\qquad(k=0,1).
\tag{9}
\]

故λ_*是完整仿射签名矩阵的dual。对任意α≥1，(2)从α=1只减去(α−1)倍非负后费用，所以同一λ_*仍可行。此证明同时重建仿射游戏精确加权势，不需要导入外部存在定理。上述一般引理是同一逐边恒等式对任意selector循环的直接应用；其独立重构覆盖范围应在审查中另行记录。

## 五、准确限制与后续义务

1. 本构造的h在给定仿射游戏中不可能处处严格改善；仿射dual(9)正是排除这种覆盖的证书。它不是无均衡游戏或主目标的否定证明。
2. (9)只覆盖次数0、1。对d≥2，是否有其他λ满足全部次数列，应按原全状态对偶义务另证；本文既未假定也未否定。
3. 固定K≥2时，若允许在环点s以概率q_s出发到H(s)、以其余概率停留，并取q_s=c/λ_*(s)，其中0<c≤min_{s∈Q}λ_*(s)，则λ_*(s)q_s=c在环上守恒，λ_*成为这条时间变换链的平稳分布。故本文只排除单位速度P_h，不能扩大为一切带持留率的方法。
4. λ_*来自固定玩家权重乘子，仅示范原dual比单位速度平稳流更自由。它不能绕过仓库ρ_d∼d的任意玩家乘子障碍。全类匹配上界仍需控制全部签名、次数及完整selector，允许真正的状态依赖。

## 六、可复算合同

运行于仓库根：

    python3 tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py

代码默认stdout；`--output NEW_PATH`用独占创建拒绝覆盖。固定K范围是1,2,3,4；全部状态与全部非空签名穷举，无随机seed。依次有4,8,16,32个状态，以及30,126,510,2046个仿射列；还对环外边逐条核验(8)，覆盖零使用状态与常数项0^0约定。K=1是等权、加权dual实际平稳的退化端点，代码明确检查，不将其用作严格障碍。

代码另外对两玩家二动作的全部256个带玩家标签selector，在权向量(1,1)、(1,2)、(1/7,11/3)逐一验证一般仿射循环引理；合计768个selector，其中所选循环636个为自环。全部非空签名的23040个仿射列分别在α=1及3/2核验。

统一审计代码SHA-256：`611f7796d2649f6d1eaa77dc0199a7785aab30750cdd80d894256c4463eb971f`。代码摘要同时在每次JSON输出记录。正文冻结摘要由外部`sha256sum`计算；正文不自嵌自身摘要。


## 规范资产和已核范围

- 正文：`research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md`。
- 独立审查：`research/reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md`。
- 审计程序：`tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py`。
- 冻结结果：`evidence/runs/weighted_congestion/template_certificates/stationary_selector_obstruction_audit.json`。

一般循环重加权lemma另以两玩家二动作、三组正权的全部tagged selector核验，允许选择当前动作并记录其玩家身份；每个selector选一循环检查全部仿射列。输入、实际数量、Python版本、代码摘要及算术合同以冻结输出为准。新lemma为显式数学补充，审查单独覆盖，未悄悄记成初冻结稿的既有内容。


## 七、循环支撑对偶与全部改善终止的等价

### 第三项Claim的精确身份

**ID/version：** `WC-RECURRENT-SUPPORT-FIP-EQUIVALENCE-v1`。

**中文数学名称：** 循环支撑对偶与全部改善终止的等价。

**Objects / Domain。** 固定任意有限非空玩家集N、每名玩家有限非空动作标签集A_i、严格正实权w_i、次数上限d≥0、实数α≥1。令Ω=Π_iA_i。令J是全部非空动作关联签名与次数0,…,d配对组成的有限集的一个非空子集。每个a∈R^J_{≥0}给出一个MODEL博弈：J中列采用相应系数，其他列系数为0。可保留费用为0的全签名规范资源以区分原来可能成本相同的动作标签。

**Definitions。** 对每个合法selector h，h(s)=(i,t_i)允许选择当前动作；偏离后状态记H(s)。定义B_h(α)的J列为真实当前移动玩家费用基减α倍真实偏离后费用基，完全沿用全状态择证定义。令Rec(h)是H的所有有向循环上的状态之并，含自环。固定a的严格α改善图以Ω为顶点；若某次单方偏离满足C_i(s)>αC_i(t_i,s_{−i})，则有相应有向边。严格边不用费用比，零费用按原不等式处理。α-FIP意指该有限严格改善图无有向环，等价于不存在无限严格α改善序列。

**Exact Statement / Quantifiers / Conclusion。** 对每个上述固定模板、w,d,α,J，以下两项等价：

1. 对每个a≥0，所得游戏均满足α-FIP。
2. 对每个合法全状态selector h，存在λ≥0，Σ_sλ_s=1，满足B_h(α)^Tλ≤0，且λ_s=0对全部s∉Rec(h)成立。

更强地，第一项成立时，可把λ支撑在h的任意一条预先指定循环上。第二项并不要求λ单位速度平稳，也不要求λ在环上均匀。

**Assumptions / Scope。** 有限性保证确定性selector至少有一条循环、无环图有有限最大路径长；动作空间为积空间保证可在环外朝一个固定合法状态逐坐标路由。该等价适用于完整J及任意固定列子锥；不是对任意无结构矩阵预设某种博弈解释。α-FIP是全部改善终止，强于仅存在α-PNE。

**Dependencies。** `WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1`对有限行子矩阵的同一自足线性替代；下文积空间的显式路由和严格平均。没有外部定理导入。

**Evidence。** 下文一般双向证明；配套Fraction审计的小矩阵替代检查、全部768个两玩家仿射selectors的循环支撑dual、以及九状态二次费用实际fixture。有限核验只检查实现与边界。

**Counterevidence / Objections。** 不能从资源可分势的障碍推出α-FIP失败，因α-FIP允许任意依游戏非可分序势。若只知各游戏有α-PNE，不能据此断言存在循环支撑dual；下面固定列锥给严格分离。给定d≥2和α=C d/ln d时，完整J的这两项是否成立，本文未判定。

**Status。** complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。先独立重构后冻结攻击的实际覆盖见配套审查。Truth为等价与明确的分离fixture；Value为确定新对偶义务的准确强度；Novelty未评估；Mechanism为行限制替代及唯一循环路由；Ambition为概率方法边界，不是主目标结论。

**Related Files。** 同稿的单位速度平稳障碍与一般仿射循环重加权引理；`research/current/weighted_congestion/template_certificates/finite_action_duality.md`；`tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py`。

### 一、全部α-FIP给出任意指定循环上的dual

假定第一项。固定任意h及H的一条有向循环Q；循环上状态不重复，只在闭合时回到起点。令B_Q是B_h取Q中各行得到的子矩阵。

如果存在a≥0使B_Qa>0，则对应游戏在Q的每条h边上均严格α改善；这些边闭合成严格改善环，违反α-FIP。因此不存在这样的a。对有限矩阵B_Q应用原全状态择证证明中的同一线性替代，存在μ≥0、Σ_{s∈Q}μ_s=1使B_Q^Tμ≤0。把μ在Q外延为0便得到所需λ，且支撑已限制于预选Q。

若Q是自环，α≥1与费用非负已使该行逐坐标≤0，取该状态的点质量亦直接可行。没有漏掉只选当前动作的selector。

### 二、一个严格改善环排除全部循环支撑dual

反过来，假定第一项失败。存在系数a≥0及其游戏的一条严格α改善简单环Q。对Q中状态，定义h为这条改善环指定的玩家与偏离。固定q∈Q。

对s∉Q，因s≠q，至少存在一名玩家i使s_i≠q_i；选择最小编号的这样玩家，让其改为q_i。在首次进入Q之前，Hamming距离D(s,q)=|{i:s_i≠q_i}|每步严格减少1，故至多|N|步进入Q（可能先碰到Q的其他节点，这之后按Q运行）。因此Rec(h)=Q；环外不可能有别的循环。该路由使用每名玩家已有合法动作q_i，无额外动作或策略假设。

若第二项成立，对此h应有支撑于Q的dual λ。但每个s∈Q均有(B_ha)_s>0，且λ≥0、Σ_Qλ_s=1，于是

\[
0<\sum_{s\in Q}\lambda_s(B_ha)_s
=a^T B_h^T\lambda\le0,
\]

矛盾。最后不等式只用a≥0和dual逐列≤0。故第二项蕴含第一项。

在有限图上，α-FIP还等价于存在一个在每条严格α改善边上下降的任意实序势：无环时取Φ(s)为从s出发的最长有向路径长度，边s→t满足Φ(s)≥1+Φ(t)；反向由有限环上严格下降不可能立即成立。此处没有资源可分、固定乘子或可计算性限制。

### 三、精确分离：空策略保证PNE，循环支撑dual仍失败

取两名玩家权重w_1=1,w_2=2；每人有动作0,1及空动作2。四种资源单项式列如下，签名依次按(p1动作0,p1动作1,p2动作0,p2动作1)写；任何空动作均不使用资源。

| 资源 | 二元动作签名 | 次数k | 费用系数a |
| --- | --- | --- | --- |
| A | (0,1,0,1) | 1 | 13 |
| B | (0,1,1,0) | 2 | 3 |
| C | (1,0,0,1) | 2 | 3 |
| D | (1,0,1,0) | 1 | 13 |

所有费用c_e(x)=a_ex^{k_e}都是非负系数次数≤2的多项式。下表由真实负载逐资源直接相加得到：

| 状态 | C_1 | C_2 | 指定移动 | 移动前/移动后费用 |
| --- | --- | --- | --- | --- |
| (0,0) | 42 | 51 | 玩家1改为1 | 42/40 |
| (1,0) | 40 | 53 | 玩家2改为1 | 53/51 |
| (1,1) | 42 | 51 | 玩家1改为0 | 42/40 |
| (0,1) | 40 | 53 | 玩家2改为0 | 53/51 |

因此对每个1≤α<53/51，四个指定边构成严格α改善环Q。等号α=53/51时，玩家2两条边的margin为0；本例没有声称端点仍严格改善。

令J恰为表中的四列，允许其系数a任取非负值，则该固定列锥中**每个**游戏的全空状态(2,2)成本均为0，因而是精确PNE（任意偏离后费用非负）。所以“每个a游戏有PNE”不能替代Claim中的“每个a游戏α-FIP”。

在九个状态上，定义h在Q按表循环；在Q外选择最小编号的当前空动作玩家，把其改为0。环外每步使空动作人数减少1，所以Q是唯一循环。取α=52/51，则循环上按所示顺序的实际总费用margin是

\[
(62/51,\ 1,\ 62/51,\ 1).
\]

乘以对应玩家权重后为(62/51,2,62/51,2)。因每个原margin≥1，任何概率λ若只支撑Q，都有a^TB_h^Tλ≥1>0，从而不可能是J列dual。这无需数值LP或任何λ枚举。

另一方面，瞬态点质量λ=δ_{(2,2)}是该J列锥的dual。h在此选择玩家1从空动作改为0；J四列的dual积依次为

\[
(0,\ 0,\ -52/51,\ -52/51)\le0.
\]

它对四列之外任意签名没有作出断言。本例的分离准确发生在所写固定列锥，不把δ_{(2,2)}冒充所有三动作完整签名列的dual。

### 四、核验与冻结合同

统一代码已增加：九状态全部实际资源成本与真实选定偏离、h唯一循环、全部当前/后费用、无权及玩家权重乘margin、α=52/51严格margin、α=53/51弱边界、瞬态dual四列、循环上任意概率的严格正系数加权margin下界。另有两项极小有理矩阵的行限制primal/dual检查；一般等价依正文证明，不从这些有限检查外推。

运行：

    python3 tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py

最新版代码SHA-256：`611f7796d2649f6d1eaa77dc0199a7785aab30750cdd80d894256c4463eb971f`。

规范冻结JSON：`evidence/runs/weighted_congestion/template_certificates/stationary_selector_obstruction_audit.json`。代码与输入摘要由该输出保存。无随机seed，Fraction精确计算，无容差。它含此前K=1,…,4和768个任意仿射selector的核验；旧冻结JSON未改写。
