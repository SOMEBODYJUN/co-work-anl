---
id: "customer-attraction/finite-real-dictionary-common-price-grid-and-signed-seed-LP"
kind: "theorem"
type_tag: "定理"
title: "有限真实字典的共同价格网格与有符号种子LP"
status: "proved-exact-finite-grid-epigraph-and-conditional-integer-implementation; no-strict-seed"
summary: "有限真菜单H的固定有理τ网格对所有w≥0同时精确，C有符号epigraph与ψ单调性给LP精确值min_w[B+C(Ψ−u)]；严格有理负点可有限同人数单位编译，非负只限相同字典/帽流程。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/root/pooled_dictionary_seed_lp.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/convex/pooled_dictionary_lp_independent_review.md"]
---

# 必须先给真实组件和全部正常前缀菜单

固定m≥2、非空有限字典t=1,…,T。每t是原有限单位客户/共同有限非空目录游戏，单位玩家次序相同；给合法目标z^t、各利润u_i^t、覆盖W_t与真OPT_m^t，目标仅要求末位BR，前面可不可信。令B_t=2W_t−OPT_m^t。组件客户不交复制，目标在同一产品按坐标并排。

每i<m固定同一目标有序前缀，当前强制A、下一强制B，保B后全部真正完整grandchild SPE终局z，d_z=u_i(z)、v_z=u_(i+1)(z)。B不预筛BR，含own动作；过去根/前缀保原分母。定义

\[
 \theta_{it}(A)=\max_B\min_{z\in R_{it}(A,B)}v_z,
\quad H_{it}(\tau)=\max_A\min_{B,z}[d_z-\tau(v_z-\theta_{it}(A))],
\]
\[
 \Psi_i(w)=\sup_{\tau\ge0}\sum_tw_tH_{it}(\tau).
\]

有限单位目录/纯策略给非空有限有理菜单。w≥0暂是复制比例/优化变量，不是非单位客户或玩家；有理权重才清分母成真实整数副本。不可用任意抽象d/v表、不完整必要点或不可信终局代替输入。固定非负整数背景的辅助子局可用相同代数，原half编译只用原实例真正合法前缀。

7066B父方稿和11700B独审全文主读。原审查已收到全部关键公式、单调性/放大提示和例子预期，先推导/手算再全文对父稿及pooled依赖，检索时还可见父稿摘要；是有提示独立核查，非无提示盲审、首次发现或外审。本页证明优化/实现合同，不提供负种子或一般half。

# 一个不依权重的有限网格覆盖全部半轴

每H由有限有理直线d−τ(v−θ)先min再max而成，连续且只有有限段，每段属于某条原线。取各t全部原线非负交点与0的并集P_i，平行/重合线不制造交点；它是全部实际折点的安全有限超集，所有点有理。

真实菜单还保证H有界上。对每A取达到θ的B，其每个真grandchild均v≥θ，故f(A,τ)≤任取该叶d≤全菜单max d，再max A仍有限。d≥0给H(0)≥0。因此H最终一段斜率不能正，否则向+∞。

固定任意w≥0，相邻P_i网格点间各H仿射，ΣwH亦仿射，区间最大在端点；最终斜率为非正斜率的非负组合，尾部最大在最后网格点，零斜率平台亦在起点达到。于是**同一个P_i对所有w同时**有

\[
 \boxed{\Psi_i(w)=\max_{\tau\in P_i}\sum_tw_tH_{it}(\tau).}\tag{GRID}
\]

没有折点时P_i={0}足够。网格不依随后选出的w，非有限采样近似；非负权重关键，不能扩为负组件数。Ψ≥0，真实退出帽qΨ+D不会成为负收入伪证书。全d_z0时H(0)0且H≤0，Ψ0、D0，亦无除d步骤。

# 保负缺陷的C及其精确epigraph

维数m−1，g可正可负。P=Σ(g_i)_+、N=Σ(−g_i)_+、p=max(g_i)_+、n=max(−g_i)_+，空正/负max为0。已证双侧真实修复的支持函数

\[
 C(g)=2P-N+p+n
 =\sum_i g_i+\sum_i(g_i)_++\max_i(g_i)_++\max_i(-g_i)_+.
\tag{C}
\]

线性项之外是正部和/最大值，故C凸、对非负比例齐次、次可加。C可负，例如C(−1,−1)=−1；不是客户数、复制数或玩家权重负。逐坐标将g_j增δ≥0，线性项增δ，两个正部项不减，max(−g)_+最多减δ，因此C不减；可能不严格。

给定g，引入h_i≥g_i、h_i≥0，p≥g_i且p≥0，n≥−g_i且n≥0（源把此全局n写作v）。则

\[
 \min_{h,p,n}\left[\sum_i(g_i+h_i)+p+n\right]=C(g).
\tag{EPI}
\]

h_i=(g_i)_+、p最大正部、n最大负部达到；p,n各一个全局变量，非逐角色分别计费。不加C≥0，不将g截正，也没有用带负系数的虚假正部松弛。

# 归一字典LP的精确值

变量w_t≥0、Σw=1；ψ_i、g_i为实变量，h_i,p,n满足(EPI)。约束

\[
 \psi_i\ge\sum_tw_tH_{it}(\tau)\quad(\tau\in P_i),\qquad
 g_i=\psi_i-\sum_tw_tu_i^t.
\]

最小化

\[
 \sum_tw_tB_t+\sum_i(g_i+h_i)+p+n.\tag{LP}
\]

由(GRID)固定w时ψ_i≥Ψ_i(w)，所以g≥Ψ(w)−u(w)。C单调给目标≥B(w)+C(Ψ(w)−u(w))；取ψ=Ψ和精确epigraph辅助量达到。故LP值**恰**

\[
 \boxed{\min_{w\ge0,\,\sum w=1}\{B(w)+C(\Psi(w)-u(w))\}.}\tag{VALUE}
\]

不能通过抬ψ取得更低值；但单调不严格，某些最优解可有松ψ，正确结论是**总可替换为一份ψ=Ψ的最优解**，非每份最优解都tight。ψ无显式上界亦不致向负无穷：VALUE是紧单纯形上的连续有限分段线性函数，最小达到，tight选择给原LP达到；有限有理LP可取有理最优；这不推出无限全实例通用价格λ有理或已找到。

# 严格负点如何变成原模型有限SPE

若一份**真实输入**的LP有精确有理可行点目标<0，网格重算Ψ(w)所得F(w)不更高，仍严格负。负种子只需严格负可行证书，不需全局最优；反向声称最优非负则需精确最优认证，正可行点/浮点输出不够。

令K为w分母公倍数，k_t=Kw_t整数非负且Σk=K>0。固定原字典的共同LP帽对权重齐次，a_i=Ψ_i(k)−u_i(k)，ε=−B(k)−C(a)=−KF(w)>0。再复制正整数q次，pooled真实退出合同对**每i、每joint强制含own**给真完整孩子且当前收益≤U_i=qΨ_i(k)+D_i。D_i是所有正类型、全部当前A的单组件利润范围，不随q；倒二可D_(m−1)=0。这里原类型帽Ψ_i(qk)=qΨ_i(k)对所有r成立，非断言r≥4的无约束joint H之sup齐次。

用C次可加/齐次与D≥0，

\[
 qB(k)+C(qa+D)\le-q\varepsilon+C(D),\qquad
 C(D)=2\sum_iD_i+\max_iD_i.
\]

取q=max(1,floor(C(D)/ε)+1)便严格负。D0时任何正整数q足够，只在ε>0时除ε，零最优值不是严格种子。接已有marked/LOW双侧分层并统一复制清分母，所有客户仍不同单位、人数m不变、共同目录有限完整Cartesian。正常目标末位BR，第一次任意联合异常后**所有坐标含未改者永久退出**至相应真实孩子，normal IC由总缺陷上界支付，退出后全history SPE；W、OPT按不交完整目录精确加。输出half差额为正倍该负预算，是真原反例的充分有限实现，非LP点自行变SPE。

依赖的全强制真U表/完整signed编译已自足见[共同后继接口](../资源/共同后继池的完整编译接口与分段勘误--资源.md)和[双侧供给](双侧有符号缺陷的真实供给修复与有限字典最小性--定理.md)。未找到这种负点。有限字典精确值非负，仅排该字典/真实菜单及所用共同一层帽的充分流程；actual joint M可低于上帽，其它类型/退出/修复未排，不是一般half证明。

# 端点与当前五人状态

零权重类型删、零客户类型可保；非空字典和Σw1排全零复制伪种子。m1主定理外，可另约C空向量0，LP=min B_t；末位BR单人W=OPT1，B=W≥0，p=n=0，不调用无下一角色菜单。全零当前d无需除它，Ψ=D0；正负缺陷集合空的max均0。

原五人“未证明所有字典非负”为旧路线状态；当前五人half另已证，由上面的真实有限编译反证可得**每份合法五人有限字典**VALUE≥0，未给具体通用λ，也不是原作者当时的新证明或任意背景五人界。六人/一般仍需真严格负预算或新普遍付款，LP线性化本身不解决它。证明、原审查先验/有限核及原件另保证据。

原件、准确程序缺件/0-run范围、关系和逐源处置见[本批证据](../../tools/evidence/finite-dictionary-epigraph-and-round7-ledger-primary/README.md)。
