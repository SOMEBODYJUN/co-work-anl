# 任意真实后继下的无拥挤响应缺口

2026-10-21，Boss2内部精确接口。来源：父分支提出F(h)及有符号Δ；本分支独立从三个节点收益相消验证。一般 Q-CAG-HALF 仍OPEN；Δ的全局支付没有在本页证明。

采用`terminal_responder_exchange.md`的单位客户共同目录模型、完整有序历史纯SPE和实际两两不交路径(C_1,…,C_k,D)，m=k+1≥2。现在完全取消早期后继冻结假设。

固定实际早期玩家i及合法查询T。记R是该真实偏离分支的末位主题；每个客户x上令

\[
a=1_{C_i}(x),\quad d=1_D(x),\quad t=1_T(x),\quad r=1_R(x),
\]

p=Σ_(j≠i)1_(C_j)(x)∈{0,1}，h'是偏离分支中除查询者和末位外全部m−2名玩家对x的覆盖数（0≤h'≤m−2）。p计入实际过去与实际未来，h'计入固定过去与原策略的真实未来，没有篡改顺序。

定义

\[
F_{t,r,d}(h)=\frac{r-t}{h+t+r}-\frac d{h+t+1},
\tag{1}
\]

第一个分式在r=t时定义为0（包含0/0情形）；其余分母均正。令

\[
\Delta_{i,T}=\sum_x(F_{t,r,d}(h')-F_{t,r,d}(p)).
\tag{2}
\]

这是有符号量。仍记U_T、U_R为真实偏离终局查询者、末位收益，V_D为该末位节点改D收益，E_R为实际末位节点改R收益。三个真实非负差g_i=|C_i|−U_T，g_R=U_R−V_D，g_D=|D|−E_R满足精确恒等式

\[
\boxed{\frac32|C_i|-L_{i,T}
=g_i+g_R+g_D+\frac12|C_i\setminus R|-\Delta_{i,T},}
\tag{3}
\]

其中

\[
L_{i,T}=|T\setminus U|+|T\cap C_i|+\frac12|T\cap(U\setminus C_i)|,
\quad U=\bigcup_j C_j\cup D.
\]

证明：客户x上的g_i+g_R+g_D=a+d−r/(p+a+1)+F(h')。将h'换成p恰为冻结后继的16会员恒等式，而差就是(2)。因此(3)对全部真实响应成立，特别给

\[
L_{i,T}\le\frac32|C_i|+\Delta_{i,T}.
\tag{4}
\]

令(T_1,…,T_m)是任意最优m元组，允许重复；Δ_tot=Σ_(i≤k,j≤m)Δ_(i,T_j)。沿同一非负并集收费得

\[
\operatorname{OPT}_m\le(2+1/k)P+L/2+\Delta_{tot}/k,
\quad
\operatorname{OPT}_m\le P/2+(k+1)L.
\]

与此前相同凸合得精确一般接口

\[
\boxed{\operatorname{OPT}_m\le\beta_kW+
\frac{2k+1}{2(k+1)^2}\Delta_{tot},
\qquad \beta_k=\frac{8k^2+11k+4}{4(k+1)^2}.}
\tag{5}
\]

因此Δ_tot≤[(5k+4)/(2(2k+1))]W是半覆盖的充分条件。然而此条件**并非所有合法完整SPE都满足**：`response_defect_budget_obstruction.md`给原3/2无拥挤族的合法平局填充，使Δ_tot=k(k−1)/2，k≥7即超过本预算。该失败只否定统一全查询缺口支付，不否定恒等式(3)、充分条件(5)或一般half。

逐客户核函数只有四类：t=r=0时−d/(h+1)；t=0,r=1时(1−d)/(h+1)；t=1,r=0时−1/(h+1)−d/(h+2)；t=r=1时−d/(h+2)。这显示正缺口可来自对查询主题/末位主题新增拥挤，或释放真实回复R的旧core；后者已足以造成二次增长。

审核脚本：`audit_response_defect.py`；一般恒等式依据本页代数。
