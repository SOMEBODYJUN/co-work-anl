历史预读草稿：创建时尚未确认DY认领；现只作本批构建输入，实际认领见actual-claim-receipt.json。

# 两名剩余完整终局菜单的纯列封顶

## 一般联合身份不提供一般符号

固定合法有序过去b，任意r≥1个剩余单位玩家，同一完整历史纯SPE。强制合法首主题A后的真实后继Y_A长r−1，排除A；完整剩余列Z(A)=(A,Y_A)。对有限主题元组定义Phi_b(Z)=sum_x sum_{j=1}^{c_x(Z)}1/(b_x+j)。令

\[
d_A=\Phi_b(A,Y_A)-\Phi_b(Y_A),\quad F_A=\Phi_b(Y_A),
\quad R_{AB}=\Phi_b(A,Y_B)-\Phi_b(A,Y_A),
\]
\[
K_{AB}=\sum_{x\in A}\frac1{b_x+1+c_x(B,Y_B)},\quad
\delta_{AB}=\sum_{x\in A\cap B}
\frac1{(b_x+1+c_x(Y_B))(b_x+2+c_x(Y_B))}.
\]

独立额外查询对完整r槽的精确COL为K_AB=d_A+F_A−F_B+R_AB−delta_AB。前三项加R先是A对仅Y_B的插入；把源首位B加回，在A∩B上恰少delta。多后继的R是联合势替换，单个玩家最佳回应不让它非正。

## 恰两人：末位真实BR和正交集税

r=2时写rho(A)=R_A，f(X)=sum_{x∈X}1/(b_x+1)，g_x=1/[(b_x+1)(b_x+2)]，h_x=2/[(b_x+1)(b_x+2)(b_x+3)]，U_b(X,Y)=f(X)−sum_{X∩Y}g_x。F_A=f(R_A)，d_A=U_b(A,R_A)，真实末位在A后可比较合法R_B，故

\[
R_{AB}=U_b(R_B,A)-U_b(R_A,A)\le0.
\]

更精确地

\[
d_A+f(R_A)-f(R_B)-K_{AB}
=[U_b(R_A,A)-U_b(R_B,A)]
+\sum_{x\in A\cap B}[g_x-h_x\mathbf1_{R_B}(x)].
\]

若x不在R_B，税为g_x；若在R_B，g_x−h_x=1/[(b_x+2)(b_x+3)]，因此一律不小于后者且严格正。这是源ef218侧审实际检查的分母差，不把包含当前首位的完整r槽错当后继Y。

## 最大裸回复的显式纯列

取B*使f(rho(B*))最大，有限目录保证存在。对每个查询A，同时

\[
K_{A,B^*}\le d_A-[f(\rho(B^*))-f(\rho(A))]
-\sum_{x\in A\cap B^*}\frac1{(b_x+2)(b_x+3)}\le d_A.
\]

若当前首位也最优，actual u=max_A d_A，故同一个完整两人终局(B*,rho(B*))给所有extra-query K≤u，不需先选查询分布、不需混合列。只用所有真实末位节点的BR，不依赖有利统一平局；重复主题、空主题、零客户和离轨历史保留。代数对任意非负实b同样成立；原单位历史应用仍只用可由合法过去产生的整数b。

边B→A若K_AB>d_A，则f(rho(A))>f(rho(B))，所以严格标量上升图无环。任何循环沿COL相加，F差望远镜，剩余不超过负交集税。把阈值换成更高的actual u也成立。这是恰一位后继的机制，不可把r≥3联合R删去。

另一个真实两人纯列选择是全局最大Phi_b(A,R)的合法主题对。该A后的任何原末位BR仍达同一全局最大势，所以所得原真实叶是静态PNE。额外插入查询T的利润不超过把首位A换成T、只面对R的利润，后者由PNE≤d_A≤u。这条势选择与最大裸回复选择都只在r2闭合；一般SPE叶不自动是PNE。

## 与已交全人数价格边界及任意p推送的关系

ef218的全人数m、实际过去k、余r、两不交主题(mL,L)的完整SPE及全部比率已在DM完整插入税对象自足保留。本批按同SHA精确复用；其真正失败的是固定r背景无关alpha付款，不是Mfull/全p强推送/half。同一family中K两列均(L,L/2)，C≤L≤D，W=OPT=(m+1)L，不能因称价格反例就改写被反驳命题。

任意p的两人定量推送是另一接口：独立根A,B~p，R=rho(B)，D=E_B d_B为真实混合根收益，C=E_(A,B)K_AB为独立完整两槽查询价；p_x=Pr(x∈B)、q_x=Pr(x∈R)、j_x=Pr(x∈B∩R)、w_x=g_x。真实末位BR给L=sum_x w_x(p_xq_x−j_x)≥0，而

\[
D-C=L+\sum_x\frac{p_x^2}{(b_x+2)(b_x+3)}
+\sum_x\frac{2w_xp_x(p_x-j_x)}{b_x+3}\ge0.
\]

这是对每个p推送Q=p的曲率余项，不等同先挑一个固定B*同时封顶所有行。r≥3的强D≥C已有完整反例；一般弱全p C≤u与Mfull/低值Nash的旧OPEN也不能覆盖当前银行反例。原ef218仅旁审两人身份，没有复跑相关数值审计或二环；本批同样不用缺失/未读审计冒充解析证明。
