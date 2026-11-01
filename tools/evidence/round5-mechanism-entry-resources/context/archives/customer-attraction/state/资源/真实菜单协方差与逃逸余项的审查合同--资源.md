---
id: "customer-attraction/true-menu-covariance-coherence-and-escape-remainder-review"
kind: "resource"
type_tag: "资源"
title: "真实菜单协方差与逃逸余项的审查合同"
status: "complete-five-source-review; algebra-and-qualified-obstructions; common-payment-unproved"
summary: "保共同客户CC1…4和同全局终局域的COH换分布项、r2平稳基线/固定双不动点障碍、逃逸三非负余项及重复尾最小假设；两旧纠错/两块证明按精确对象duplicate，元均衡条件与当前银行反例分开。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/two_block_pure_menu_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/two_block_pure_menu_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/two_copy_pushforward_correction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/two_copy_pushforward_correction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/replicated_block_correction_and_menu_interface.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/replicated_block_correction_and_menu_interface.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_no_go/escape_budget_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_no_go/escape_budget_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_coupling/common_customer_covariance_and_stationary_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_coupling/common_customer_covariance_and_stationary_obstruction.md"
---

# 真实菜单协方差与逃逸余项的审查合同

## 五源的身份及域

五原稿4023/2182/3480/3659/9359B，共22703B，HF已经实际全文首读，HP核同SHA逐节比较。单位客户、单位提供者、有限共同非空目录，完整纯SPE在全部合法有序历史规定动作，保空主题、重复、零客户及任意离轨平局。旧一般OPEN不抹去当前五人half定理；六人目标未由本页闭合。

两块独立证书/分母纠错的完整数学已在[真实分支账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)及HF交付资源中保全，按准确对象duplicate。此页自足补共同客户随机变量与跨节点换菜单的精确债务、逃逸三余项和条件元均衡接口的现行状态，不新造同一实例或定理。

## CC1—CC4：同一客户、同一真实策略、同一列分布

固定合法有序前缀h，过去客户负载b_x≥0，余r≥1。对同一完整纯策略σ，强制当前根B后真后继Y_B，完整剩余列Z(B)=(B,Y_B)，含root共r槽。根分布p与额外查询独立；逐客户定义
\[
a_x(B)=\mathbf1_{\{x\in B\}},\quad k_x(B)=c_x(Y_B),\quad
v_x(B)=\frac1{b_x+1+k_x(B)},\quad
t_x(B)=\frac{a_x(B)}{(b_x+1+k_x(B))(b_x+2+k_x(B))},\quad p_x=\mathbb E_p a_x.
\]
当a1，v−t=1/(b+2+k)；当a0，v−t=v。故v−t正是同完整列后额外查询该客户的价格，不能把v本身当完整槽查询分母。真实根平均D与独立同p查询C为
\[
D(p)=\sum_x\mathbb E_p[a_xv_x],\qquad
C(p,p)=\sum_x p_x\mathbb E_p[v_x-t_x].
\]
逐客户加减p_x E_pv_x，严格得
\[
D(p)-C(p,p)=\sum_x\operatorname{Cov}_p(a_x,v_x)+\sum_xp_x\mathbb E_pt_x.\tag{CC1}
\]
若0<p_x<1，记μ_j=E_p[v_x|a_x=j]，则
\[
C_x-D_x=p_x(1-p_x)(\mu_0-\mu_1)
-p_x^2\mathbb E_p\!\left[\frac1{(b_x+1+k_x)(b_x+2+k_x)}\mid a_x=1\right].\tag{CC2}
\]
这里相反方向债务首项是源会员/真实后缀负载适应性，次项为插入正税。p_x=0或1直接用CC1，不定义空条件期望。

根实际收益u=max_B d_B，e(p)=u−D(p)≥0。对给定p，弱push C(p,p)≤u恰等价
\[
-\sum_x\operatorname{Cov}_p(a_x,v_x)\le e(p)+\sum_xp_x\mathbb E_pt_x.\tag{CC3}
\]
代数没有给左侧符号或支付机制。对另一个共同真实列分布Q，额外查询仍按p抽取，得
\[
C(p,Q)-D(p)=\sum_xp_x(\mathbb E_Qv_x-\mathbb E_pv_x)
-\sum_x\operatorname{Cov}_p(a_x,v_x)-\sum_xp_x\mathbb E_Qt_x.\tag{CC4}
\]
其换分布漂移未被支付。每个客户分别选便宜Q_x不能拼成一个所有客户共用的合法Q。CC1与[完整槽插入/根税恒等式](../引理/完整槽插入税与跨角色价格恒等式--引理.md)的ROOT是同一坐标，不重复认另一份一般支付；Gamma方差身份也不自动控制CC4。

## COH：子节点重新开菜单不是父菜单的条件律

本节只讨论尚有后继玩家的子节点hS（r≥2）；终端子节点没有新的行动菜单。为避免把r槽和r−1槽测试函数相减，把原稿简写的terminal统一为**同一个原游戏全局m槽终局域**。记
\(\widehat Z_h(B)=(h,B,\text{σ真实后继})\)，含固定过去h；Q_h是强制B~p_h、之后完全按σ所得的全局终局律。若p_h(S)>0，纯σ使
\[
\operatorname{Law}_{Q_h}(\widehat Z\mid B=S)=\delta_{\widehat Z_h(S)}.\tag{COH1}
\]
但子节点hS的新菜单是强制下一位C~p_{hS}再按σ，通常
\[
Q_{hS}=\operatorname{Law}_{C\sim p_{hS}}(\widehat Z_{hS}(C)),\tag{COH2}
\]
不是COH1。对任何同全局终局域的测试函数F，精确换基项为
\[
\mathbb E_{Q_{hS}}F-\mathbb E_{Q_h}[F\mid B=S]
=\mathbb E_{C\sim p_{hS}}F(\widehat Z_{hS}(C))-F(\widehat Z_h(S)).\tag{COH3}
\]
若只记剩余后缀，必须给child补回已经固定的S再放同域；不能无说明删原root比较槽数。此为本页对源COH1…3的域澄清，公式本身未赋符号。

p_h(S)=0时父菜单连该正概率条件律都没有，子节点作为合法历史仍有自己的σ/新菜单。把每个节点独立重采样的非负方差相加，不能当一个共同过滤下的全方差望远镜；必须先构造全树相容抽样律，并证明所用比较仍是原σ的真实续局。即使只随机一个根、较深真实历史揭示根后条件协方差为0，跨根条件均值之间的协方差仍保留，未凭零条件项消失。局部角色收益随深度变也不自动是同一个F。

## r=2的平稳正面基线与r=3反例不是同一命题

源b97的正面基线可由两人f−g代数自足展开。恰余2人，末位真实回复ρ(B)，令
\[
f(T)=\sum_{x\in T}\frac1{b_x+1},\quad
g(T,V)=\sum_{x\in T\cap V}\frac1{(b_x+1)(b_x+2)},\quad
U(T,V)=f(T)-g(T,V).
\]
完整槽核P_full=(I+P_ρ)/2；pP_full=p等价pP_ρ=p。对每个合法查询T，末位BR给U(ρ(B),B)≥U(T,B)。平稳使E f(ρ(B))=E f(B)，g对称，故E U(ρ(B),B)=E U(B,ρ(B))=D(p)≤u。又ρ(B)与B同分布，
\[
\mathbb E U(T,\rho(B))=\mathbb E U(T,B)\le D(p)\le u.
\]
左为只保真实末位槽的额外查询价；把原root B加回复整列只增负载，完整两槽查询更小。因此此stationary构造对r2安全，含空主题/零客户/任意合法过去。r1完整列查询也≤裸主题最大值u。这里是既有两人基线的解析展开，不新造定理/不运行程序；不能外推r≥3。

6286客户、六主题、三人的给定完整菜单在现账本及HF资源中有全部原始重数/策略：唯一平稳π=(1,1,0,1,1,0)/4，而query2价5765/4>u2821/2，self C=185785/192<u，五个纯列安全。原发现稿同时明确固定P,K的另一精确合同
\[
\exists p:\quad pP=p\quad\text{且}\quad (Kp)_T\le p^TKp\ \forall T.\tag{DFP}
\]
在此例也为假：唯一π已被query2击破meta最佳回复，不能改选stationary class。未排允许内生改变核的另一个新合同，不反该例stationary self strong-push或自由mixed，也不反half。

发现稿引用的四种材料身份分开：`stationary_full_slot_counterexample_6286.json`称存原客户/43动作/全K/准确范围；`probe_stationary_full_menu.py`称固定原形式策略、保全部SPE行优化指定核，重构有理点后精确核；`stationary_348_diagnostic.json`有query2和query5两条阳性，本正文只用query2，不能把query5当同一输入重复佐证；独立单位审计由round5_audit另一实现展开6286客户/重算全部比较。HP新读的是9359B数学原稿，不是这些代码或JSON；不因此升级原全IC/OPT认证或声称代码不可得。

## 自由真实菜单与内生元均衡：保条件归约、改旧OPEN

681源旧称“自由完整根菜单”，指在**同一σ真实根列**中自由混合，不指任意静态r主题元组。K_AB=Σ_(x∈A)1/(b_x+1+c_x(Z(B)))，root仍在列、查询独立，所有真根偏离d_B≤u。有限minimax给
\[
M_{full}=\min_Q\max_A(KQ)_A=\max_p\min_B(p^TK)_B.
\]
反FM需某个p使**每列**pᵀK[:,B]>u；只给pᵀKp>u一般不够。另构造对称两人元游戏：行收益K_AB、列收益K_BA，不要求K矩阵对称。任一对称NE(p,p)的value v=pᵀKp满足(Kp)_A≤v、支持内取等。若能对某个这样的p证u≥v，就可取Q=p得FM；这是充分条件，不说每个便宜Q都是meta-NE，亦不说真实顺序后继为meta最佳回复。

这组逻辑仍成立，旧一般OPEN状态却不能照抄。[真实零根银行列](../反例/银行完整根列的两查询最小分离--反例.md)在m4给u4/3、Mfull59/36>u，故对任何meta-NE都有value=max_A(Kp)_A≥Mfull>u，没有安全meta-NE。一般真正自由静态extra-one的逐人门槛另由同银行族和Jensen下界19/14≤v5反驳，见[静态预算条件归约](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)；不能仅由¬FM逻辑推出更弱自由背景命题为假。静态minimax/Nash的数学存在性不认证一个新求解算法、时间界或canonical实现。

## 逃逸预算：精确三非负余项及最小几何

固定k≥1，m=k+1，N恰为互不交X_i,Y_i,D之并，C_i=X_i、A_i=X_i∪Y_i及D是合法主题。给定完整SPE实际C_1…C_k,D，记x_i,y_i,d,S=Σx_i,Y=Σy_i，则W=S+d，k个A_i加D覆盖全N，OPT=S+Y+d。

实际i节点改A_i后，原真实末位选合法B_i，收益s_i；该末节点改D收益q_i；实际i改B_i后本人真实最终收益t_i。这里**不需要**B_i只在本地池支撑，不需要其分支末位指定A_i，也不要求两枝有可比较负载。只用
\[
x_i-t_i\ge0,\quad s_i-q_i\ge0,\quad d-x_i/2-y_i\ge0.
\]
令E=Σ_i[(s_i−t_i)+(d−q_i)]，则
\[
S-kd+E=\sum_i[(x_i-t_i)+(s_i-q_i)]\ge0.
\]
更强的完整恒等式为
\[
\begin{aligned}
&(3k+2)W+(2k+1)E-2(k+1)OPT\\
&=(2k+1)\sum_i[(x_i-t_i)+(s_i-q_i)]
+2(k+1)\sum_i[d-x_i/2-y_i]\ge0.
\end{aligned}\tag{ESC}
\]
由W/OPT展开即证，不需要E≥0；d−q_i≥0本来真，而s_i−t_i可负。只知真OPT>2W时，Y>S+d结合末位界Y≤kd−S/2，得S<2(k−1)d/3及E≥kd−S>(k+2)d/3。d0迫全局池空，k1迫S<0，都无严格half反例。E仍未被W支付，这只是该实际路径结构的必要条件，不是一般half证明。

## 重复尾模板的显式假设与两页最小提案

这是另一个有r≥1个尾追随者的具体方案，不套前述k+1人数率界。固定D=Z⊔R，局部核心X_i∪Y_i与D不交，B_i=X_i∪Y_i∪Z；除已指定实际C_i/偏离A_i和所列尾行动外，其他动作不覆盖核心或R。actual末端r次D，拟A_i枝末端r次B_i。实际末位D改B_i的公共Z项抵消，需|R|/r≥|X_i|/2+|Y_i|；拟分支末位B_i改D的公共Z同样抵消，未覆盖R首次得|R|，需(|X_i|+|Y_i|)/(r+1)≥|R|。非零核心a给r(r+1)≤2，r≥2不可能，r1强制Y_i空。

若Z/R重叠、其他中间行动预覆盖R或核心，写定分母即会改变；不能沿用这两比较。共同Z贡献在每次单节点比较中抵消，关键是R分离/未被其他未指定动作覆盖，不给一般E额外强加这些重复模板条件。

[两页最小提案](../../../../tools/evidence/covariance-menu-coherence-and-escape-review/hypothesis-clarification-proposals/replacement-manifest.json)给GS隔离页与HD资源各自完整before/SHA、完整proposed及零context patch，只补上述r/不交/其他动作条件及架构区分，公式和metadata不改。本代理不覆shared、旧包不重写；Root若另审读应用，以Root实际应用证据为准，原proposal仍保持创建时身份。此澄清不是把旧source/done整体判错。

## 两块独审与纠错的精确duplicate

90b稿的两块32客户/八人/八主题根表、13872DAG/7437决策节点/59496比较、整数BI840缩放/12870前缀/6435叶、B根另一候选(2,1,0,1)|q0不可实现，以及Q/p匹配851/280、Q自身为meta-NE均已HF全文保在资源。其数学主证明和输入已在既有账本自足；不把MD“单位审计通过”当HP新读DAG/程序或新run。

f325纠错撤销的是用旧D玩家13/4替额外查询137/60的阳性；q0另块37/10，两块uniformD的C359/120、gap−31/120。条件k块C_k=37/10−17/(12k)仅k≥4才超u；需全真实嫁接/全部root偏离。qD单块查询向量(16/5,23/15,59/20,137/60)有纯安全cap，但不能推出所有完整菜单必有纯列，后来的八人反例已否此一般桥。早期规范BI(q0,q0)不可实现与尚未独立证书是当时事实，后续独立重造DAG另保时点。全部独有数学/版本与撤销用途现已明确去向，duplicate不新造同一反例。

本批五份原文全部定义、公式、状态与代码/输出用途已分主对象和此资源保全；没有新数学程序/原CLI/LP/BI/随机/旧成功复跑。CC/COH没有付一般协方差或换菜单债务，ESC只在指定实际路径，局部负结果不反六人half，也不认证外审、新颖性或未交付算法。
