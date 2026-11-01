# 单阈值 Santa Claus 的分块配置压缩与归一化类型匹配接口

本稿是既有 SC→UM 归约的独立自足重构与边界分析，不给新近似比例、新困难性或新颖性认证。分块压缩由 migration_packages 先于阅读文献研究者证明独立重构；类型匹配恒等式由 literature_frontier 直接提取并证明。原始文献字节保持不变，`UM-TARGET-v1` 仍 OPEN。

已读原件：Bamas–Lindermayr–Megow–Rohwedder–Schlöter，[arXiv:2307.08453v1 PDF](https://arxiv.org/pdf/2307.08453v1)、[HTML](https://arxiv.org/html/2307.08453v1)、[CWI 原稿](https://ir.cwi.nl/pub/36041/36041.pdf)。Lemma11及AppendixB在印9、20–22页；selector/resource后端Lemmas12–14在印9–11页。本文第一定理重构其已知单阈值合同，使用另一种更短的计数证明，不声称原文采用这种分块法。

## 1. Exact A：单阈值分块类型配置

**ID：`UM-SC-BLOCK-TYPE-PROFILE-RECONSTRUCTION-v1`。**

固定任意正有理 ε。输入显式二进制有理矩阵 v∈Q_(≥0)^(m×n)，m≥1、n≥0。资源不可分、可闲置；合法 partial allocation 是两两不交的资源子集 A_i⊆[n]。原值为 val_i(A_i)=Σ_(j∈A_i)v_ij；OPT_SC 为最大共同最小值。

存在确定性算法，在原输入总位长的多项式时间内输出同维矩阵 v'、公共正值调色板 a_0,…,a_(t−1) 及每玩家一个显式整数 count-profile 集 C_i，满足：

- 0≤v'_ij≤min(v_ij,1)，每正值属于调色板，t=O_ε(log(n+1))。
- 每 c∈C_i 满足0≤c_k∈Z、Σ_k c_k≤n、c_k≤N_ik:=|{j:v'_ij=a_k}|≤n，且 W(c):=Σ_k a_kc_k≥γ:=1/(1+ε)。零值资源不计入 profiles。
- 对每位 i 和**每个** A⊆[n]，若 val_i(A)≥1，则存在 A'⊆A，逐类型完整匹配某 c∈C_i，且 v'_i(A')=W(c)≥γ。因此 OPT_SC(v)≥1 时存在一份不交实际分配匹配 C、每玩家舍下效用至少γ。
- 任意 v' 下的实际分配在原 v 下逐玩家效用不减。
- 每个 |C_i|≤binom(H+t,t)=(n+1)^(O_ε(1))，下文给 H 及直接枚举器。算法不输入未知最优分配，不求共同 profile 选择，也不判定 OPT_SC(v)≥1；C_i 允许为空。

固定 ε 的限定不可省：未声称复杂度对 bit(ε) 统一多项式、FPTAS或低指数。n=0时输出空矩阵、空调色板和每 C_i=∅；m≥1使该端点OPT=0，YES前提为空。没有玩家的 min 另由模型入口处理，不在本ID范围内。

## 2. Exact A 的构造、证明与总位复杂度

n≥1时置 δ=ε/[4(1+ε)]∈(0,1/4)、τ=δ/n。先 cap 值 w_ij=min(v_ij,1)；小于τ的值置零，其余向下舍入至 a_k=(1+δ)^(-k)。取 K 为 a_K≤τ 的最小非负整数，完整调色板 k=0,…,K，t=K+1。留下的正端满足

\[
 w_{ij}/(1+\delta)\le v'_{ij}\le w_{ij},\qquad
 a_K>\frac{\delta}{n(1+\delta)}.                 \tag{1}
\]

等于τ的值保留，等于grid值精确保留。逐次乘除固定有理数可算grid，无浮点对数；数学上 t≤2+log(n/δ)/log(1+δ)=O_ε(log(n+1))。

定义每type整数块长与共同块数预算

\[
 b_k=\max\{1,\lfloor\delta/(t a_k)\rfloor\},\qquad
 H=\lceil4t/\delta\rceil.                       \tag{2}
\]

枚举 h∈Z_(≥0)^t、Σh_k≤H，令 c_k=b_kh_k，仅保留通过 Exact 的总count、逐type可用量和价值γ过滤的向量。DFS第k坐标只枚举

\[
0\le h_k\le\min\{H-\sum_{\ell<k}h_\ell,
                    \lfloor N_{ik}/b_k\rfloor\}.
\]

全部叶子≤binom(H+t,t)，全部前缀≤(t+1)倍该数；没有先枚举无总预算的计数直积。

**分块引理。** 每块价值 b_ka_k≥δ/(2t)。令 u=δ/(t a_k)；u<2时b_k=1给严格不等式，u≥2时floor(u)≥u/2。对任一整数type件数d_k、总舍下值V=Σa_kd_k<2，取c_k=b_kfloor(d_k/b_k)。b_k=1时无损；b_k≥2时每type损失

\[
0\le(d_k-c_k)a_k<b_ka_k\le\delta/t.
\]

所以总损失≤δ，且由每块价值下界得

\[
 \sum_k h_k\frac{\delta}{2t}\le\sum_k a_kc_k<2,
 \quad\text{故}\quad\sum_k h_k<4t/\delta\le H.    \tag{3}
\]

**对全部实际资源子集的completeness。** 若v_i(A)≥1，cap后总值仍≥1：有原值≥1的项时单件cap即1，否则不变。从A任取顺序、首次cap总值达到1即停，得到B⊆A且1≤w_i(B)<2。此步只用于证明，构造算法不读取A。

从B删tiny总损失≤nτ=δ，再几何舍下后，剩余正资源集合D有

\[
\frac{1-\delta}{1+\delta}\le v'_i(D)<2.             \tag{4}
\]

对其实际type counts执行分块引理，每type只保留c_k件，得到A'⊆D。count及可用量自动合法，式(3)给H合法；价值满足

\[
v'_i(A')\ge\frac{1-\delta}{1+\delta}-\delta
 =1-\frac{\delta(3+\delta)}{1+\delta}
 \ge1-3\delta
 >\frac1{1+\varepsilon}=\gamma.                   \tag{5}
\]

故c通过全部过滤，属于C_i。分别作用于任一不交YES分配只删资源，仍不交，且完整匹配profiles。不要再加回闲置资源破坏exact count。

**数量与位长。** H+t≤(2+4/δ)t，故

\[
\binom{H+t}{t}\le[e(2+4/\delta)]^t
 =\exp(O_\varepsilon(t))=(n+1)^{O_\varepsilon(1)}. \tag{6}
\]

固定δ下K=O_ε(log(n+1))。若1+δ=s/r既约，则a_k=r^k/s^k，共同分母可取s^K；所有grid、价值和与比较的整数位长多项式。由(1)，δ/(t a_k)<n(1+δ)/t，所以b_k仅O_ε(log(n+1))位。H也为多项式位长。原输入极大分子/分母仅用于cap及grid区间精确比较，不能导致数值循环；count过滤保每个profile最多n件，后端复制也按显式资源数收费。

## 3. 原文cutoff的准确纠错范围

v1 AppendixB印20 step2写tiny cutoff为1/((1+η)n)，印21继而声称删除仅损失因子1+η。这个**特定字面删除断言**不成立：一位玩家、n=101，100件各9/1000、另1件1/10，总值1。η=1/10时cutoff=10/1111>9/1000，删除后只剩1/10<10/11。后续向下舍入无法恢复。该字样已在本地原PDF与arXiv HTML交叉核读；未冒称已核2024会议最终排版的同一位置。

原机制改cutoff为η/((1+η)n)即可使删除损失≤η/(1+η)，类型数仍O_η(log n)。本文另一构造直接用τ=δ/n及明确加性损失δ。两者都局部修复该步；没有据此断言原主定理不成立。另，略高于cutoff的值向下舍入后可低于cutoff，故完整grid留到最小a_K≤τ，不能免费声称全部正舍下值仍≥τ。原PDF字节保持不变。

## 4. Exact B：归一化类型匹配的真实值恒等式

**ID：`UM-NORMALIZED-TYPE-MATCHING-RANK-VALUE-IDENTITY-v1`。**

输入任意显式非空玩家集、非空资源集R、非负二进制有理类型估值v'_ij，以及每位玩家显式非空indexed类型profile菜单C_i。每c的c(v)为非负整数、Σ_(v>0)c(v)≤|R|、c(v)≤|{j:v'_ij=v}|，并有W(c)=Σ_(v>0)vc(v)>0；零类型不产生token。重复indexed profiles允许。对B⊆R定义

\[
 f_{ic}(B)=\frac1{W(c)}\sum_{v>0}v\min\{c(v),|\{j\in B:v'_{ij}=v\}|\},
 \quad F_i(B)=\max_{c\in C_i}f_{ic}(B),
 \quad V=\max_{B_i\text{两两不交}}\min_iF_i(B_i).    \tag{7}
\]

每f_ic是显式加权partition-matroid rank估值，f_ic(R)=1；F_i可按显式菜单确定性位多项式精确求值，但不自动次模。可确定性总位多项式构造普通UM矩阵S，使

\[
             \operatorname{OPT}_{UM}(S)=2-V.        \tag{8}
\]

更强地，给任意不交B_i，可输出S的**全部jobs实际调度**，峰恰2−min_iF_i(B_i)；给S任意实际调度峰C，可输出不交实际资源子集，使每F_i≥max(0,2−C)。包括V=0、OPT=2、重复states、所有未选profiles；不输入OPT，不借未知LP证书或免费matroid oracle。S的selector/token jobs均是不可拆分原jobs，普通机器仅累加真实处理时间。

## 5. Exact B 的完整矩阵、证明及规模

每(i,c)一台private机器Q_ic，每实际资源j一台R_j。每玩家一枚selector J_i，仅在自己的全部Q_ic耗1。每positive type v建c(v)枚不同token jobs，每枚在Q_ic耗v/W(c)，在所有满足v'_ij=v的R_j耗1；其余∞。这是合法一般UM；token可以有多个resource端，不能暗改为two-end flat菜单。每profile全部token的private总负载恰1。

给不交B_i，为每玩家选达到F_i(B_i)的profilec。逐type从B_i取min(c(v),可用数)枚不同实际资源，匹配等数不同tokens外送；其余tokens留private。所有未选profiles全部tokens留各自private。selected private负载2−f_ic(B_i)，未选private负载1，资源负载≤1。因F≤1，全部jobs恰一次、峰恰2−min_iF_i(B_i)。

反向给实际峰C<2，每resource最多一枚unit token。取每selector实际所在profilec_i，以该selected profile实际外送占用资源为B_i；不同玩家B_i不交。外送归一化总权E_i恰f_ic_i(B_i)，selected private负载2−E_i≤C，所以F_i(B_i)≥2−C。未选profile外送tokens可以忽略，不能从矩阵中删除jobs来构造前向调度。C≥2时输出空bundles，满足非负目标0。

所有分配有限、最优达到。上两方向给OPT≤2−V和任何调度C≥2−V，证明(8)，没有在C=2端点误用resource独占。若需起止时刻，各机固定顺序串行，精确部分和仍位多项式。

每profile≤|R| tokens，每token至多扫描|R|个resource端。总机器、全部jobs、dense矩阵及给定解转换均为输入**显式菜单长度**多项式；v/W(c)有理位长按总输入位长收费，不按1/v、分母或数值复制。ExactA出现空菜单时可先报告该目标无YES见证，不把空菜单送入本定理。

## 6. 非次模反例、匹配结构与剩余义务

**max-profile非次模。** 一位玩家有资源a,b,c,d，值分别1/4、1/2、1/2、3/4。菜单取这些资源上全部实际子多重集总值≥1的类型profiles，并按(7)归一化。令A={a,b}、B={a,c}，则

\[
 F(A)=F(B)=3/5,\quad F(A\cup B)=1,\quad F(A\cap B)=1/4.
\]

理由：含a,b且达到1的最小可用profile为a,b,c，总值5/4，给(3/4)/(5/4)=3/5；只用b一型最多1/2，其余profile不更好。含a的最小可用profile为a,d、总值1，故F({a})=1/4。union本身就是profile，值1。因此6/5<5/4，违反次模不等式。该反例是ExactB通用菜单域的边界，不冒称ExactA的每个固定ε生成菜单都取这些精确数值。

BLMRS的多项式“配置”只记录value-type counts；每个profile还保留按type的截断匹配选择。它不能免费替换成一个具体资源子集。若要求同资源宇宙的explicit norm1 additive菜单展开，会遇到仓库既有[规模障碍](normalized_weighted_menu_santa_value_and_size.md)；本稿不重复建立另一个XOS计数claim。每profile各自次模，不足以对max-profile直接调用次模算法。

**两个Exact的直接组合界。** C来自ExactA且全部非空时，W(c)≥γ给出对全部实际B的界F_i(B)≤v'_i(B)/γ≤v_i(B)/γ。ExactA的子集性质又给v_i(B)≥1⇒F_i(B)=1。因此

\[
 \operatorname{OPT}_{SC}(v)\ge1\ \Longrightarrow\ V=1,
 \qquad V\le\operatorname{OPT}_{SC}(v)/\gamma.       \tag{9}
\]

结合(8)，真实SC的YES OPT≥1/NO OPT≤ζ承诺，得到UM的YES OPT=1/NO OPT≥2−ζ/γ。这里只传递另行证明的源gap，不提供ζ任意小的困难性。如果某C_i为空，由ExactA已知SC的YES前提不成立；完整gap编译器在此分支输出一台机器、两枚该机耗1的jobs，固定OPT=2，仍满足NO下界2−ζ/γ（ζ≥0）。其余分支按ExactB构造S。这是完整普通UM编译器的退化分支，不把空菜单送进ExactB，也不在该分支使用(8)或(9)。

ExactA关闭了该归约“隐含指数多个count profiles”的位复杂度疑点，ExactB给出了实际值/全部任务解码，但一般全局选择仍未解决。可继续攻击的具体义务是：对ExactA生成的shared-type rank菜单，在真实V=1的承诺下找绝对δ_0>0并位多项式输出互不交bundles、每F_i≥δ_0；或者建立具有全partial匹配soundness的真实YES V=1/NO V≤δ_0源。CONFIG反例不能充当这份源。

即使完成这一像类正向算法，也不能自动称解决一般UM。BLMRS Theorem1给一般UM的(2−1/α)算法⇒一般SC的(α+ε)算法，α≥2；一般反向不是已给定结论，Theorem2只在两种正值的类有等价。其matroid变体约束每job/resource自己的基，也不等同本稿的max-profile估值。本文未重构该文全部matroid局部搜索或声称外部审查、全球优先权认证。

独立证据：分块Exact先由migration_packages独立重构，再由literature_frontier读取并逐支攻击；rank Exact先交global_algorithm盲审，随后读后攻击单列。任何有限算例仅核公式，不承担上述一般证明。


运行与实际审查：[分块审计](../../../tests/audits/unrelated_machines/santa_block_type_profiles.py)、[独立类型匹配审计](../../../tests/audits/unrelated_machines/type_matching_rank_bridge.py)、[冻结审查](../../reviews/unrelated_machines/type_profile_compression_and_rank_bridge_review.md)。有限结果与原始文献事实分别登记，不升级主目标。
