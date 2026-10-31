---
id: "customer-attraction/true-final-reply-push-sharp-curvature-and-two-branch-identity"
kind: "lemma"
type_tag: "引理"
title: "末位真实回复推送的锐曲率与双分支式"
status: "proved-for-one-final-BR-with-arbitrary-real-background; multi-reply-extension-false"
summary: "完整保任意p的精确余量、确定性两分支式、总BR而非逐客户符号、全等号条件和逐参数锐族；34客户强式失败与actual收益松弛分别核算，不扩到half。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/two_player_full_terminal_pushforward.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/two_player_full_terminal_pushforward.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/two_player_pushforward_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/two_player_pushforward_review.md"
---

# 末位真实回复推送的锐曲率与双分支式

## 完整输入和独立审查身份

[6035B发现稿](../../../../tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary/original/6c84043505685faee8ec/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/two_player_full_terminal_pushforward.md)及[5009B实际独审](../../../../tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary/related/38f33a2ab903eb816fc8/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/independent_pushforward/two_player_pushforward_review.md)全部实读。后者先只据陈述盲重构、再读发现稿对照，是历史审查方法；本次读双方后归档不重新冒称盲证、外审或新颖性。此前DY已保存部分平均式；这里补全确定性双分支、全等号条件及逐参数锐族。

有限单位客户、有限非空共同目录，固定一个合法有序过去，其负载b_x为非负整数。恰有两位剩余；首位强制B后，原策略在该完整有序历史的末位最佳回复记rho(B)=R。任意平局可选不同主题。**不要求首位行动自身最优**，只要求每个相关末位节点真实BR。代数还允许任意实b_x≥0；这扩大数学接口，不把实b冒作原单位历史的合法前缀。

任取合法主题law p。B~p，A~p独立于产生竞争槽的(B,R)。定义

\[
D=\mathbb E_B\sum_{x\in B}\frac1{b_x+1+\mathbf1_R(x)},\quad
C=\mathbb E_{A,B}\sum_{x\in A}
\frac1{b_x+1+\mathbf1_B(x)+\mathbf1_R(x)}.
\]

D是真实根强制收益均值，C是独立查询面对**完整两槽**(B,R)的插入价。不能删B，不能把A=B同一次抽样，也不把R看成与B独立。令p_x=Pr(x∈B)、q_x=Pr(x∈R)、j_x=Pr(x∈B∩R)，w_x=1/[(b_x+1)(b_x+2)]。

## 精确非负分解

独立再抽B'~p，R'=rho(B')。共同目录使R'在固定B后的真实末位节点也可作为合法偏离。由逐节点BR，

\[
L=\mathbb E_{B,B'}[U_b(R,B)-U_b(R',B)]\ge0,
\quad U_b(X,Y)=\sum_{x\in X}\frac1{b_x+1+\mathbf1_Y(x)}.
\]

写f(X)=Σ_X1/(b+1)、g(X,Y)=Σ_{X∩Y}w，则U=f−g。R,R'同分布使裸值相消，B与R'独立，故

\[
L=\sum_xw_x(p_xq_x-j_x).
\]

非负性只对完整主题比较的**总和**成立，逐客户项可以为负，不假设每名客户负相关。二元membership直接展开得

\[
D_x=\frac{p_x}{b_x+1}-w_xj_x,
\quad C_x=p_x\left[\frac1{b_x+1}-w_x(p_x+q_x)
+\frac{2w_xj_x}{b_x+3}\right].
\]

相减、取出L并用0≤j_x≤p_x，得到

\[
\boxed{D-C=L+\sum_x\frac{p_x^2}{(b_x+2)(b_x+3)}
+\sum_x\frac{2w_xp_x(p_x-j_x)}{b_x+3}.}\tag{PUSH}
\]

所以D−C≥Σp_x²/[(b_x+2)(b_x+3)]≥0。空主题、p_x=0和零客户均不除零；有任何p_x>0时D−C严格正，p只支持空覆盖时D=C=0。若当前首位也满足SPE，则actual u≥D，才进一步给C≤u；首位最优性不是PUSH本身的前提。

## 等号条件和精确锐性

相对曲率下界取等，恰需L=0且每个p_x>0的客户j_x=p_x。后一条件指源覆盖的每个正概率客户几乎必然也被回复覆盖；L=0等价于每个正概率(B,B')的rho(B')在固定B后同样是BR，因为其单项均非负。不能把L=0误写为逐客户p_xq_x=j_x。

单客户x，目录{空主题,{x}}，任意实b≥0，两个首行动后末位均选{x}，且这是唯一BR。令p({x})=t∈[0,1]，其余为空，则p=t,q=1,j=t，L及PUSH末项都为0，

\[
D=\frac t{b+2},\quad
C=\frac{t(1-t)}{b+2}+\frac{t^2}{b+3},\quad
D-C=\frac{t^2}{(b+2)(b+3)}.
\]

每个b,t均取等，故一般量词下曲率系数不能统一增大。这是解析族，不是有限抽样锐性证据。

## 确定性的两条真实分支

取任意首主题A,T，真实回复R=rho(A)、S=rho(T)。定义G_X(Y,Z)=Σ_(x∈X)1/[b_x+1+1_Y(x)+1_Z(x)]，r_x=1_R(x)、s_x=1_S(x)。准确有

\[
U_b(A,R)+U_b(T,S)-G_T(A,R)-G_A(T,S)
=[U_b(R,A)-U_b(S,A)]+[U_b(S,T)-U_b(R,T)]
\]
\[
\qquad+\sum_{x\in A\cap T}\left[
\frac1{(b_x+1+r_x)(b_x+2+r_x)}
+\frac1{(b_x+1+s_x)(b_x+2+s_x)}\right]\ge0.\tag{PAIR}
\]

两个方括号分别是历史A、T下末位对另一个合法回复的真实BR松弛。逐客户分首membership00/10/01/11：00零，10及01给w乘对应回复membership差，11剩显示的正曲率项；所以是逐客户恒等式，不把一枝的回复搬到别枝当最佳。独立A,T~p后平均PAIR并除二，正好恢复PUSH。

[最大裸回复纯列](../引理/两名剩余完整终局菜单的纯列封顶--引理.md)则先取一个B*同时封顶全部行；这里对每个p用同p推送的Q=p并保锐余项。两者都是正确的恰一后继接口，抽样与结论不同，不能换名当一般人数证明。

## 三人强式失败及实际收益松弛

源引用的[7992B完整34客户输入](../../../../tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary/related/f218c3c894b4635ecca2/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json)也全文读，包括13类型、七标签含空主题6、全部57有序动作及附带字段。它同SHA已由既有父方单位审计成功核342个非自身比较，本次[现行审计记录](../审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md)及其执行记录已完整比较，**不复跑全树**。

p只在主题2给1/10、空主题6给9/10。强制2叶(2,3,4)，根d2=29/3、自插入K22=13/2；强制空叶(6,0,1)，根0、查询2价K26=32/3。于是

\[
D=\frac1{10}\frac{29}3=\frac{29}{30},\quad
C=\frac1{10}\left[\frac1{10}\frac{13}2+\frac9{10}\frac{32}3\right]=\frac{41}{40},
\quad D-C=-\frac7{120}.
\]

actual u=29/3，因此u−C=1037/120>0。空行0不可能与正价行同时作为这一p的META-Nash正支持；它不是低值meta-Nash或Mfull失败证据。它只否定多后继无条件D≥C；源所说一般C≤u仍OPEN是历史状态，当前[银行完整根菜单](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)另已否定普遍实际u桥，不能从这个正松弛例反向恢复它。

本批只新增一次固定根算术，核原输入SHA及这些价/差，见[新报告](../../../../tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary/runs/new-branch-arithmetic-001/report.json)；原CLI/全历史复演0次。原较大的representation/terminal_pushforward_D_lt_C_exact.json仅按发现稿引用保其独立来源；本批未读取该较大输入，不把它与本34客户输入合并。一般half、实际路径聚合预算及可自由改选对手分布各有不同量词，未由PUSH或这个失败例解决。
