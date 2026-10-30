---
id: customer-attraction/same-context-safe-net-coupons-and-maximal-scalar-clipping
kind: theorem
type_tag: 定理
title: 同节点安全净券与最大标量剪枝
status: proved-local-netting-and-clipping-global-capacity-open
summary: 同一真实context的N和actual IC松弛可从当前整行安全退券；最大标量取消只留(v−u)+传播，重算后不增旧gross正负载但不保证旧net下降。fresh分母只接fresh源，角色cap未证。
truth_status: proved-stated-structural-results; universal-role-capacity-open
review_level: analytic-source-reconstruction-and-internal-self-check; no-external-review
scope: 有限单位客户；有限非空共同目录；任意m≥1；每份完整有序历史纯SPE
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round6/credible/safe_coupon_netting.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round6/credible/safe_coupon_netting.md
---

# 同节点安全净券与最大标量剪枝

## 原模型与同一context的全部金额

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、$m\ge1$名单位提供者顺序行动、终局覆盖者均分。固定全部有序历史上的纯SPE $\sigma$，实际叶$Z$、覆盖$C$、actual收益$u_i$。空主题、重复选择、零客户及任意离轨平局全部保留。

natural context $t=(g,i)$的规定动作为$a=\sigma_i(g)$，规定叶$B_t=\operatorname{finish}_\sigma(g)$，actual-prefix reset叶为$A_t=\operatorname{finish}_\sigma(Z_{<i},a)$。固定

\[
v_t=u_i(B_t),\quad D_t=u_i(A_t),\quad e_t=u_i-D_t\ge0.
\]

对$x\in a$，每个$j\ne i$、$x\in(A_t)_j\setminus(B_t)_j$给正价$1/[c_{A_t}(x)c_{B_t}(x)]$，相反消失coverer给负价；按客户及角色求和为$q^+_{tj}(x)$、$P_t$、$N_t$。逐客户计数给

\[
v_t-D_t=P_t-N_t,\qquad D_t-N_t>0\quad(a\ne\varnothing).
\tag{LOSS}
\]

具体地，写$a_x=c_{A_t}(x),b_x=c_{B_t}(x)$、$r_x$为从$B_t$消失的coverer数，则每客户$D_x-N_x=(b_x-r_x)/(a_xb_x)$，分子恰是两叶共同coverer数且至少为1。求和得第二式；它也常记为$J_t+L_t$。正future价进入$A_t$上的真实更深prescribed context；正past价$j<i$只落actual $(j,x)$券，因为$A_{t,j}=Z_j$。不能用改枝后过去玩家的利润购买其IC。

给合法来源注入$b_t\ge0$，按严格future角色图递推$h_t=b_t+\sum_{s\to t}\beta_s q^+_{st}$、$\beta_t=h_t/v_t$。只在$v_t>0$定义；空动作无正输入或正边。past边是终点，故有限DAG。用同一完整actual-prefix IC乘标量$\beta_t$，守恒恒等式是

\[
\sum_tb_t=\sum_t\beta_t[u_i+P_t^{<}-N_t-e_t].
\tag{LEDGER}
\]

这里尚无总费用不超过$W$的结论；本页只将这份signed账改写为合法非负金额。

## 同一当前整行安全退款

LOSS与actual完整IC给

\[
0\le N_t\le D_t\le u_i,\qquad F_t:=N_t+e_t\in[0,u_i].
\]

从该context的gross当前整行券$\beta_tu_i$，在每个实际$(i,x)$份额上统一退系数$\beta_tF_t/u_i\le\beta_t$，净系数为

\[
\kappa_t=\beta_t(D_t-N_t)/u_i\ge0.
\tag{SAFE}
\]

于是

\[
\sum_tb_t=\sum_t\kappa_tu_i+
\sum_{t,j<i,x}\beta_tq^+_{tj}(x).
\tag{POSITIVE}
\]

所有金额非负。$N/e$只与**同一context**当前整行相消，past正券保持原标签；没有将负$q^-$假配给不存在的actual同客户券。整行IC仍使用原$\beta$，不能把$\kappa$称为新的IC系数，也不能退$e$后让剩券再支付整份$\beta D$。

若$u_i=0$，IC强制$D=N=e=0$；非空正context本来给$D>0$，故不可能产生正付款。零量统一取系数0，不作$0/0$。

保留past标签、以actual份额$1/c_Z(x)$为券单位时，来源已有负载$\Lambda^{src}$加上新净负载为

\[
\Lambda^{net}_{j,x}=\Lambda^{src}_{j,x}+
\sum_{t:i(t)=j}\kappa_t+
 c_Z(x)\sum_{t:i(t)>j}\beta_tq^+_{tj}(x),\quad x\in Z_j.
\]

SAFE证明这些量非负，不证明它们至多1或2，更不证明同角色多context合计已付。

## 最大标量取消与重新计算

对固定context，从原正recipient边删去任意总价$0\le c\le\min(P_t,F_t)$，同时退款改成$F_t-c$。新的当前净金额$u_i-F_t+c$仍在$[0,u_i]$，外送价为$P_t-c$，和仍为$v_t$。取消允许不同客户间的标量质量互换；若要求严格保留每客户血缘，不能原样使用此加强。

取$c=\min(P_t,F_t)$即得

\[
P'_t=(v_t-u_i)_+,\qquad F'_t=(u_i-v_t)_+,\qquad
u_i-F'_t=\min(v_t,u_i).
\tag{CLIP}
\]

上式左端的$u_i$是原actual收益，非fresh分母。可以先删past正边，使保留past最小为$(P_t^{<}-F_t)_+$，future保留$\min\{P_t^{>},(v_t-u_i)_+\}$。各边仍是原正边子容量，允许分数保留。

固定所选子边$q'\le q$后，必须从同一原注入$b$重新递推$h',\beta'=h'/v$。严格角色归纳给$\beta'\le\beta$，但新的current可能增加；其净系数是

\[
\kappa'_t=\beta'_t\min(v_t,u_i)/u_i=h'_t/\max(v_t,u_i).
\tag{MAX-DENOM}
\]

于是$\sum b=\sum_t\beta'_t[\min(v_t,u_i)+P_t'^{<}]$。不能混领旧退款与新剪枝，不能只因$\beta'$下降便声称新net负载逐坐标不增。

在保持原past客户标签时，成立的是$\kappa'\le\beta'\le\beta$、$\beta'q'\le\beta q$，所以新正负载不超过旧**gross**正负载（同一source常数一起加入）。没有证明不超过旧net。若以后把past金额在角色内pooling，只有角色总额保持，不自动继承这项原客户逐坐标比较。

固定$\beta=h/v$并要求当前整行系数不超过$\beta$时，任意守恒非负支付至少外送$\beta(v-u)_+$；CLIP达到该下界。所以它是固定当前gross系数上限下的**局部最少传播**，不是全图净cap最优。

也可用线性金额表示这一自由：每原正边发送$f\in[0,\beta q]$，$h=\beta v=b+$future incoming，current $\ell=h-\sum f$满足$\beta(D-N)\le\ell\le\beta u$。这等价于上述合法标量取消；它仍不保证任何actual客户券或共同角色cap可行。

## 仅fresh利润分母的独立合同

只对$a\setminus C$计算正负价，设

\[
\nu_t=u_i(B_t;N\setminus C),\quad D_t^F=u_i(A_t;N\setminus C),
\quad Y_t=u_i(A_t;C).
\]

在$\nu_t>0$的活动节点，fresh LOSS为$\nu-P=D^F-N>0$；$\nu=0$时无fresh正边或合法正fresh输入，直接略去。完整actual IC给$u_i=D^F+Y+e$，故

\[
\nu-P=u_i-Y-N-e>0,\qquad0\le Y+N+e\le u_i.
\]

同一整行可安全退$Y+N+e$，但现在必须使用$\beta=h/\nu$及这份fresh图重新计算。正价由fresh客户见证接收context的$\nu>0$；无past出口。只接受fresh来源，通常为$R=O\setminus C$或其残源，**不能把包含$C$的全$O$来源塞进此图**。广播可重采另一个fresh客户，不保持原来源客户身份。

CLIP同样只保$(\nu-u_i)_+$传播。其好处是未把off-history $C$利润$X$纳入分母，账内无正$X$迁移；代价是$\nu\le v$，同输入的$\beta$和后续量可能更大，不能声称费用或负载不增，也不能与旧$v$核SOURCE/DIAGONAL合领。$Y$是同query退款，不是可反复领取的actual $I/G$库存。全局共同资金仍未证。

## 同角色pooling与全比较来源的条件cap

past正金额$z$先按原标签核其确实属于actual角色$j$，则$u_j>0$。之后可在该角色的实际客户份额上统一给系数$z/u_j$，总额仍为$z$。这是同一个实际钱包内分配，不购买过去IC，不跨角色退款。

若每个最优客户的一单位在合法owner查询的全部真实coverer间均分，past/current进相应actual付款、future进上述**全客户**核，全部终端角色净金额$A_j$非负且$\sum_jA_j=|O|=\mathrm{OPT}_m$。零actual收益的角色没有合法正付款。故$A_j\le2u_j$对全部$j$是half的一个充分ROLE-CAP2条件；它比每个固定原客户券单独cap更宽，但**尚未证明普遍成立**。full-$O$初始化不能改用仅fresh核。

## 来源、关系与接续

本次逐字节核对既存同SHA副本后，全文实读7448字节主源，见[主清单](../../tools/evidence/net-coupon-primary/source-manifest.json)。旁读fresh归一化和按陈述的净化审查完整保存在[related清单](../../tools/evidence/net-coupon-primary/related-manifest.json)；原审查先获公式/提示再重构，不称严格盲题发现或外审。本批解析逐式核；四主源均为Markdown，无程序来源，未运行数学扫描或把历史审查当作本次独立执行。

本定理提供[角色命中与来源后缀界](净券跨节点角色命中与来源后缀界--定理.md)所需的非负守恒核，也支持[固定净券归属钱包](../候选/分数归属与实际净券的共同钱包--候选.md)预先固定列矩阵的合同；它不自动给那里的OWNER-NET。与[同客户密度流](同客户来源保持流的加强初始化与节点密度--定理.md)的归一化不同，后者逐客户$f$可改变边幅，不一般属于本CLIP子核。局部安全、有限终止、真实IC域与最终角色共同容量必须分别判断，六人half未由本定理闭合。
