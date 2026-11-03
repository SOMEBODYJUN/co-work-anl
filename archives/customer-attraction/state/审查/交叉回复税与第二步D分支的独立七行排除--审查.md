---
id: customer-attraction/crossed-reply-tax-and-second-to-D-seven-row-review
kind: review
type_tag: 审查
title: 交叉回复税与第二步D分支的独立七行排除
status: general-tax-identity-accepted; fixed-old-primal-D7-extension-excluded; once-original-audit
summary: 保独审的64符号会员恒等式与512新分型精确包络；一般税和固定D7互不推导，后续去对角/锚定公式另注明推导与审查时态。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/peer_relations_independent_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/audit_peer_relations.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/peer_relations_independent_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/crossed_reply_tax.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/separate_second_D.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/separate_second_D.json"
---

# 两项独立审查对象与证据时态

3908B原peer review全文实读，3715B audit全文实读；父方又按冻结源导出7491B crossed_reply_tax.md、2831B separate_second_D.py、2030B其JSON作比较依赖，未额外认领/done。两项对象分别用下列#crossed-reply-tax与#d7-fixed-primal定位，不把一般税引理与一个旧点的延拓排除接成互相推导。

原审者先读同行数学/七式，再从模型重构，无优化器/同行代数helper导入；不是未读稿盲审，也非外审。本次只原样执行其标准库审计一次，输出494B同原字节，exit0/stderr0。它是同一独立实现的重放，不增加一位独审者；完整原件、八依赖、命令/环境/SHA见[证据](../../tools/evidence/direct-coverage-source-resumed-boss3/README.md)。

## crossed-reply-tax

固定原模型的一份完整历史纯SPE、任意恰剩三人的有序历史h，旧负载b_x为非负整数。任取q≥1个合法查询T_i，允许重复；其真正后继为R_i,S_i，d_i=U_b(T_i;R_i,S_i)。定义
\[
 V_b(X;Y,Z)=\sum_{x\in X}\frac1{b_x+1+1_Y+1_Z},\quad
 F_i(X)=\sum_{x\in X}\frac1{b_x+1+1_{T_i}},
\]
\[
 g_i(X,Y)=\sum_{x\in X\cap Y}\frac1{(b_x+1+1_{T_i})(b_x+2+1_{T_i})},
 \quad\tau_i=g_i(R_i,R_i)-g_i(S_i,R_i)\ge0.
\]
τ_i是在R_i\S_i上的和，且F_i(X)−g_i(X,Y)=V_b(X;T_i,Y)。空主题、零客户和所有平局均保。

本税证明复制的是R_j，故记K^R_(ij)=σ_last(h,T_i,R_j)，区别[直接可信诊断](../引理/真实第三位交叉查询的可信末回复门槛--引理.md)复制S_j的K^S。三条真IC slack为
\[
 L^1_{ij}=V_b(R_i;T_i,S_i)-V_b(R_j;T_i,K^R_{ij}),
\]
\[
 L^2_{ij}=V_b(K^R_{ij};T_i,R_j)-V_b(S_j;T_i,R_j),quad
 L^3_{ij}=V_b(S_i;T_i,R_i)-V_b(K^R_{ij};T_i,R_i),
\]
全部非负，分别是真第四位改R_j、真末位K^R对S_j、原末位S_i对合法K^R。共同目录使这些主题在各精确有序节点合法，未把旧人收益搬枝。

令两主题增量调和势Φ_b(X,Y)=Σ_x Σ_(k=1)^(1_X+1_Y)1/(b_x+k)。逐客户精确恒等式为
\[
 d_i-V_b(T_i;R_j,S_j)=L^1_{ij}+L^2_{ij}
 +F_i(S_i)-F_i(K^R_{ij})+\Phi_b(R_j,S_j)-\Phi_b(R_i,S_i),\tag{1}
\]
\[
 F_i(S_i)-F_i(K^R_{ij})=L^3_{ij}+g_i(S_i,R_i)-g_i(K^R_{ij},R_i).\tag{2}
\]
i,j独立同分布时两Φ项平均抵消。加E_iτ_i后，剩余为
\[
 \Delta+E_i\tau_i=E_{ij}(L^1+L^2+L^3)
 +E_{ij}[g_i(R_i,R_i)-g_i(K^R_{ij},R_i)]\ge0,\tag{3}
\]
其中Δ=E_i d_i−E_(ij)V_b(T_i;R_j,S_j)。最后余项是在R_i\K^R上的非负和。uniform给
\[
 \sum_i d_i-\frac1q\sum_{ij}V_b(T_i;R_j,S_j)+\sum_i\tau_i\ge0.\tag{4}
\]
原独审认可这条带税去相关及同一概率律的加权版本；未认可无税Δ≥0或ROW3。

代码对(t_i,r_i,s_i,r_j,s_j,k)六会员位的64组合，把所有表达写成1/(b+1)、1/(b+2)、1/(b+3)的有理系数，并用1/[(b+k)(b+k+1)]=1/(b+k)−1/(b+k+1)。每个系数都精确为零，因此恒等式涵盖全部符号背景b，不是有限b抽样。IC的合法性仍靠前面的真实节点说明，64个代数零式本身不使任意伪收益表成为SPE。

### 后续同行稿的去对角与锚定补充

所取得的比较稿还含后补式，原494B独审报告未逐项另列它们；本页重构以下短推导，不把旧审查范围倒写。

相同精确历史给K^R_(ii)=S_i，所有L和查询差/Φ差在i=j均0。删这些对角，再平均，得uniform税可减为
\[
 \sum_i d_i-\frac1q\sum_{ij}V_b(T_i;R_j,S_j)
 +\frac{q-1}{q}\sum_i\tau_i\ge0.\tag{5}
\]
任意概率ρ_i同理将税换为Σ_iρ_i(1−ρ_i)τ_i。q1时两边0；重复查询造成更多历史重合也不破坏此充分式。系数是已展示的改进，不主张普遍最小税。

五查询单客户(t_i,r_i,s_i)、j_T=Σt_i的行系数是
\[
 \sum_i\frac{t_i}{b+1+r_i+s_i}
 -\frac{j_T}{5}\sum_i\frac1{b+1+r_i+s_i}
 +\frac45\sum_i\frac{r_i(1-s_i)}{(b+t_i+1)(b+t_i+2)}.
\]
全局求客户和非负；各单客户系数不必非负。实际第三位背景b∈{0,1,2}时可按三元联合直方图表示，但没有抹去有序历史。

若同一前缀的原实际三尾为C,D,E、u=V_b(C;D,E)，令τ_C在D\E上以b+1_C为背景定义。将(5)的q2应用于(T_i,C)，乘2后得
\[
 d_i+u-V_b(T_i;D,E)-V_b(C;R_i,S_i)+\tau_i+\tau_C\ge0.
\]
对五i求和，τ_C出现5次。锚定须同一前缀和同一σ的真实C枝；隐藏回复是σ_last(h,T_i,D)和σ_last(h,C,R_i)，不是冻结D/E。该式仍需共同实际资金支付，不能把多份互斥尾利润直接认作W。

## d7-fixed-primal

另一个输入是旧437行索引点five_player_indexed_bound.json，77420B、SHA 18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1。它有64正有理原子，十位ABCDEUVWXY；AE_hist为五个(t,r,s)三元直方图，second_hist为五个(t,h,i,j)四元直方图。三族的查询重数都相同；独审逐原子核此一致性。本批只消费该旧JSON的primal质量/会员与相关直方图，不重新审437行、对偶或别的字段资格。

实际第二位由B改为实际第四位合法D，真实新路径为(A,D,R,S,T)。新主题会员用ρ,σ,τ；旧实际总负载M=a+b+c+d+e，新总z=a+d+ρ+σ+τ。零分子份额统一0。定义旧AE与second族的已知量
\[
 A_4=\sum_i\frac{r_i}{a+e+t_i+r_i+s_i},\quad
 C_{AE}=\sum_i\frac1{a+e+t_i+2},
\]
\[
 H_3=\sum_i\frac{h_i}{a+t_i+h_i+i_i+j_i},\quad
 H_4=\sum_i\frac{i_i}{a+t_i+h_i+i_i+j_i},
\]
\[
 C_3=\sum_i\frac1{a+t_i+3},\quad C_4=\sum_i\frac1{a+t_i+h_i+2},\quad j_T=\sum_i t_i.
\]
七条逐客户行依次为
\[
 b/M-d/z,\quad \tau/z-e/(a+d+\rho+\sigma+1),\quad
 5\tau/z-j_T/(a+d+\rho+\sigma+1),
\]
\[
 A_4-\rho C_{AE},\quad A_4-\sigma C_{AE},\quad
 H_3-\tau C_3,\quad H_4-\tau C_4.\tag{6}
\]
全局客户和都非负。第一条是真第二位IC；二/三条是新真实末位对E及五最优槽的完整BR；四/五条是原AE第四位分别查新R/S的安全分母；六/七条是原(A,T_i,...)第三/四位查新T。安全分母只上界未来覆盖者，未冻结后继。

冻结非负乘子为

|行|λ|
|---|---:|
|F2D|25623/31250|
|last:E|80557/1000000|
|last:sumopt|211/100000|
|AE4:R|5221/200000|
|AE4:S|5221/200000|
|second3:T|3963/250000|
|second4:T|3667/125000|

这些是发现器float dual四舍五入后的有理提案，和1000001/1000000；非延拓证书只需各λ≥0，不需归一化或最优。对每旧原子α，令m_α为其正质量，枚举(ρ,σ,τ)∈{0,1}³并设γ_α=max Σ_kλ_k row_k。原独审从单位会员重新写七式、不导同行seven helper或优化器，全部64×8=512型精确求值，64个γ都等于冻结列表，且
\[
 \sum_\alpha m_\alpha\gamma_\alpha
 =-\frac{336525906357864252494704662357779526105596687}
 {24837228663957176671172182423497877773536000000}<0.\tag{7}
\]
任一真实延拓只能把每个旧原子质量拆到这八型，其七行非负加权和必≥0，却≤(7)，矛盾。忽略主题碰撞和历史重合只扩大八型域，仍负就足以排真实延拓。结论只否定保此旧点数据的second→D延拓；不是增强系统全域上界、精确minimax最优、五人或六人SPE反例。

同行发现器的numeric minimax0.013551301796009557与有理(7)约−0.013549253457823079分别是发现值和可核证书，不能按正负相反便称精确相等。本次未调用其NumPy/SciPy优化器，也未取其third_D_completion依赖；七式及旧输入在独审源码中已自含。

# 与现行结果和后续工作的关系

[根饱和不相容](../障碍/五人索引松弛点的根饱和不相容--障碍.md)和[去对角菜单](../引理/真实菜单去对角比较与五人索引点分离--引理.md)早已用别的合法条件排同64点；D7保独有的新分支/新主题消元证书，不重复认领旧点或旧437认证。一般税与D7可各自复用，均没有解决ROW3；当前五人主定理已有另证，当前焦点六人仍需相应真历史与共同预算。阶段三应分别给税恒等式、实现/独审、固定点非延拓与范围比较关系，不能把三条同输入分离互造依赖。没有外审、新颖性或全松弛锐性声明。
