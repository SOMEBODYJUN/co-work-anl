---
id: uniform-full-slot-pool-terminal-two-rows-and-common-Jensen-reserve
kind: lemma
type_tag: 引理
title: 均匀全槽池的末两行与共同Jensen储备
status: proved-terminal-payment-and-domain-directions; early-full-pool-payment-open
summary: "均匀位置K±与自由Mpath严格分域，末两完整列由真实BR/iid交换/插入税付清；全行Jensen只一份，早期债未付，浮点6/24/30×3阴性不证明一般候选。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/terminal_pooled_full_payment.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/README.md"]
---

# 均匀全槽池的末两行与共同Jensen储备

5561B全槽池主稿与1673B convex入口完整主读，并与完整终局推送储备全文比较。它准确修正均匀位置负载域与自由Mpath的比较，以原真末位的**整主题**最佳回复支付末两行，再留下一个只领一次的共同Jensen余量。没有把两行付款变成全路径/六人付款，不认领已有一后继去相关的新颖性。

## 固定原SPE的删除/完整负载域

有限单位客户、有限非空共同目录，m≥2单位玩家，固定每个有序历史都理性的纯SPE σ，actual叶z、利润u_i、W=Σu_i。空主题、重复、零客户和平局均允许。在原actual前缀i强制合法A、其后沿同一σ真实完成，完整m槽叶为Z_i(A)、负载向量C_i(A)。只从该叶静态删当前强制槽得到L_i(A)=C_i(A)−1_A，含m−1槽。

定义紧凸负载域
\[
\mathcal K^-={1\over m}\sum_i\operatorname{conv}\{L_i(A):A\in\mathcal S\},\quad
\mathcal K^+={1\over m}\sum_i\operatorname{conv}\{C_i(A):A\in\mathcal S\}.
\]
外层是**位置均匀**Minkowski平均，不是任意跨(i,A)权重的凸包。q_i是每个给定行菜单上的概率，不随机化原纯σ；它只是对原真实列作外部平均。相同q_i给
\[
\bar L^+(q)=\bar L^-(q)+{1\over m}\sum_iE_{A\sim q_i}1_A\ge\bar L^-(q).
\]
任意独立查询分布p，ρ_x=Pr_(T~p)(x∈T)，F_p(L)=Σ_xρ_x/(1+L_x)。因逐坐标递减，相同q的F_p(plus)≤F_p(minus)，所以各p的min_K+≤min_K−。

令
\[
\gamma^\pm=\min_{L\in\mathcal K^\pm}\max_{T\in\mathcal S}\sum_{x\in T}{1\over1+L_x}.
\]
紧性保证min达到。F_p对L凸、对p线性，有限查询/紧凸域有minmax等价γ=max_p min_L F_p(L)。可直接验证：查询成本向量的上闭包{v:某L使每F_T(L)≤v_T}闭凸，若常数向量c不在其中，非负分离权规范成p便给min_L F_p>c，反之显然。由相同q的单调比较得γ+≤γ−。

每个K+负载是合法主题指示的分数和，总槽权m；K−总槽权m−1。任意L=Σ_A w_A1_A、Σw=r≥0，记F=max_T F_T(L)，最优m主题并集O逐客户有
\[
OPT=\sum_{x\in O}\left[{1\over1+L_x}+{L_x\over1+L_x}\right]
\le\sum_{j=1}^mF_{T_j}(L)+\sum_Aw_AF_A(L)\le(m+r)F.
\]
故OPT≤2mγ+、OPT≤(2m−1)γ−。full-pool付款mγ+≤W足以half；弱deleted付款(m−1/2)γ−≤W也足以half。但γ+≤γ−**本身**不能由后一不同系数推出mγ+≤W；更强mγ−≤W才由同一大小关系蕴含full-pool。没有宣称这些候选一般成立。

## 均匀位置菜单值与自由Mpath方向

定义完整列核k_T(i,A)=Σ_(x∈T)1/[1+C_i(A)_x]。均匀位置旧菜单值
\[
M_{unif}=\min_{q_1,\ldots,q_m}\max_T{1\over m}\sum_iE_{A\sim q_i}k_T(i,A).
\]
任意q_i对负载取均值，reciprocal Jensen给F_T(平均C)≤平均k_T，所以γ+≤M_unif。自由位置Mpath则允许一个任意联合列分布Q(i,A)，没有位置边际必须1/m，因此Mpath≤M_unif。两条同向指向M_unif的界不能合成γ+≤Mpath。

若改用全部(i,A)完整负载的自由凸包，其域包含K+，同一任意Q的Jensen才给该**另一个域**的值≤Mpath。本页保原均匀Minkowski定义，不靠改域恢复错误比较。根完整m槽必须保留，不能把删除当前槽的对象混入此值。

原指定helper对每个p取q_i=p：
\[
\bar C(p)={1\over m}\sum_iE_{A\sim p}C_i(A),\qquad
mF_p(\bar C(p))\le W\quad\text{对全部p（PF?）}.
\]
若PF成立，则各p min_K+ F_p≤W/m，minmax给full-pool。它比自由挑q_i强；不是已证明的结论。完整独立查询的更强FTA：∀p Σ_iJ_i≤W，会通过Jensen推出PF；当前单根Mfull的银行反例不自动否定这类全位置预算。

## 末两行整主题IC与平均去相关

设β为actual前m−2位负载，倒二实际主题P、末位Q。倒二强制A后的原真实末位BR为B(A)。完整列
\[
C_{m-1}(A)=\beta+1_A+1_{B(A)},\quad C_m(A)=\beta+1_P+1_A.
\]
设U_β(X,Y)=Σ_(x∈X)1/[β_x+1+1_Y(x)]。对相互独立且同分布A,T~p，
\[
J_{m-1}=E_{A,T}\sum_{x\in T}{1\over1+C_{m-1}(A)_x},\quad
J_m=E_{A,T}\sum_{x\in T}{1\over1+C_m(A)_x}.
\]
它们是对**完整m槽外再加一个独立查询**的份额，不是原当前forced收益。当前真实IC给
\[
I_{m-1}=u_{m-1}-E_AU_\beta(A,B(A))\ge0,\quad
I_m=u_m-E_TU_\beta(T,P)\ge0.
\]
末位在原历史A后可合法选B(T)，因此整主题BR slack
\[
G(A,T)=U_\beta(B(A),A)-U_\beta(B(T),A)\ge0.
\]
这里不要求B(T)在A后也最佳，只是合法备选，且没有对客户重加权。

为完整推导DC，令w_β(X)=Σ_(x∈X)1/(β_x+1)。二主题对称交项给U_β(X,Y)−U_β(Y,X)=w_β(X)−w_β(Y)。对G两项应用此式，再用A,T iid互换，Ew_β(B(A))=Ew_β(B(T))，Ew_β(A)=Ew_β(T)，得到
\[
\boxed{E_AU_\beta(A,B(A))-E_{A,T}U_\beta(T,B(A))=E_{A,T}G(A,T).}\tag{DC}
\]
这是平均恒等式，逐客户G贡献可带符号，但整主题BR保证每份G非负。不同历史的末位平局允许各自按原σ选，不绑为静态统一动作。

## 完整槽插入税与精确尾付款

额外加入forced主题A把独立查询T分母再加1，仅在A∩T发生。定义
\[
Tax_{pen}(A,T)=\sum_{x\in A\cap T}{1\over(\beta_x+1+1_{B(A)})(\beta_x+2+1_{B(A)})},
\]
\[
Tax_{last}(A,T)=\sum_{x\in A\cap T}{1\over(\beta_x+1+1_P)(\beta_x+2+1_P)}.
\]
分母均正、税非负。删除forced槽的cross query减完整列query恰为该税，故
\[
\boxed{u_{m-1}-J_{m-1}=I_{m-1}+EG+E Tax_{pen}\ge0,}\tag{PENULT}
\]
\[
\boxed{u_m-J_m=I_m+E Tax_{last}\ge0.}\tag{LAST}
\]
不要求p静态最优/Nash/saddle，亦不要求其支持主题同价格；只用原真实当前/末位整行动IC、iid交换和代数。m2没有early行，因此PF直接成立；这不是一般人数的新福利因子。

与[已有完整推送尾储备](../资源/完整终局推送的自身折扣与末两位储备--资源.md)的符号比较：令η_x=Pr(x∈A∩B(A))≤ρ_x，则
\[
E Tax_{pen}=\sum_x\rho_x\left[{\rho_x-\eta_x\over(\beta_x+1)(\beta_x+2)}
+{\eta_x\over(\beta_x+2)(\beta_x+3)}\right]=V_{pen}+Q_{pen},
\]
其中旧V_pen=Σρ²/[(β+2)(β+3)]、Q_pen=Σ2ρ(ρ−η)/[(β+1)(β+2)(β+3)]；二者非负。EG是旧L，I是旧e；E Tax_last就是旧V_m。这些是同一已付款尾储备的重写，不能同时把新税和旧V/Q再领两份。

## 一份共同Jensen余量与真实未付早期债

全部原位置仍用同一个p及独立A,T，令J_i=E_(A,T)k_T(i,A)。定义
\[
\mathcal V(p)=\sum_iJ_i-mF_p(\bar C(p))\ge0.
\]
逐客户对所有位置/forcing A一起做1/(1+load)凸Jensen即可。它是**全行一份**共同余量，区别于上一段旧单倒二V_pen。

精确有
\[
W-mF_p(\bar C)=\sum_{i\le m-2}(u_i-J_i)
+I_{m-1}+I_m+EG+E Tax_{pen}+E Tax_{last}+\mathcal V.
\]
所以PF的准确早期义务为
\[
\sum_{i\le m-2}(J_i-u_i)\le I_{m-1}+I_m+EG+E Tax_{pen}+E Tax_{last}+\mathcal V.
\tag{EARLY?}
\]
早期后继是一段完整真实SPE，不能把它当一个玩家免费调DC；上式未付。全V已经含每行内部和行间Jensen差，若拆成逐行Jensen再合并行间差，其和正是V，不可另加原全V。m5仍有前三行，当前HALF5别证不自动证明PF/full-pool或EARLY；m6留前四行也未因此解决。

## 原有限审计、版本与停止点

|原资产|原稿/入口明确报告的范围|本批新增执行|
|---|---|---:|
|audit_terminal_pool.py/JSON|末两恒等式、原完整SPE、单共同Jensen的有限精确核；README未给数量，不借其它probe计数|0|
|pooled_full_probe.py/JSON|六份旧完整SPE先直接重放原IC，再多起点浮点攻指定q_i=p helper；未分离|0|
|attack_pooled_full_cone.py/JSON|24个完整ordered BI策略的全IC固定锥，W1归一，交替优化p和客户非负重数；有限浮点未分离|0|
|attack_shared_cone.py及两个JSON|30完整策略锥，每锥3固定p；原SHARED切平面保全IC、shared load凸全局最小化，未分离，共同core等号诊断弱|0|

六probe/24锥/30×3不是同一审计或一个统一量词，未分离不证明候选一般成立。原code/JSON不在这五MD闭包，本批不冒原复跑/精确dual/输入重建；也不把入口已读当这些程序primary done。原“无git/work.py/spawn”是其历史，不是本轮工具执行记录。source说没有新福利常数/目标反例/外审/新颖性，本页保此边界。

5561B主稿已自行纠正从跨列Jensen到自由Mpath的错误推论；旧天真比较不能因入口OPEN标签继续用。完整原字节与七份实际全文对照见[证据目录](../../tools/evidence/sumrow-external-wallet-and-terminal-pool-primary/README.md)。本页证明的是已知末两行付款及准确共同银行，早期债仍须新的真实全历史关系。
