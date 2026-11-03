---
id: customer-attraction/second-position-actual-D-seven-row-projected-envelope
kind: lemma
type_tag: 引理
title: 第二位复制实际D的七行投影包络
status: proved-universal-necessary-envelope; old-primal-exact-separation-reused-from-independent-review
summary: 固定完整五人策略的真第二位→D分支给七个非负整行，任意非负共同权经逐客户八态最大化得到必要包络；对称权可六态，旧点负证书复用不重跑。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/second_D_envelope.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/separate_second_D.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/separate_second_D.json"
---

# 真实分支与可见旧数据

采用[共同目录完整历史单位模型](../定义/共同目录完整历史模型--定义.md)，恰五位单位提供者、有限客户和共同有限非空目录，固定任意完整纯SPE。空主题、重复行动、零客户和所有有序历史平局保留。实际路径(A,B,C,D,E)，第二位收益u₂；任取五个合法比较槽T_i，可重复，记每客户j=Σ_i t_i。

同一原σ给真实分支(A,E,T_i,R_i^AE,S_i^AE)及(A,T_i,H_i,I_i,J_i)。再暴露第二位在真实(A)后改为实际第四位的合法D，原续局为(A,D,R,S,T)。只有这条分支是新对象；新R/S/T不等同任何旧索引主题。

对每客户旧会员a,b,c,d,e及各hist位，定义
\[
 K_{AE}=\sum_i\frac{r_i}{a+e+t_i+r_i+s_i},\quad C_{AE}=\sum_i\frac1{a+e+t_i+2},
\]
\[
 K_H=\sum_i\frac{h_i}{a+t_i+h_i+i_i+j_i},\quad
 K_I=\sum_i\frac{i_i}{a+t_i+h_i+i_i+j_i},
\]
\[
 C_H=\sum_i\frac1{a+t_i+3},\qquad C_I=\sum_i\frac1{a+t_i+h_i+2}.
\]
分子0项取0。新会员r,s,t用在以下新分支总负载a+d+r+s+t。七条客户系数依次为
\[
 \frac b{a+b+c+d+e}-\frac d{a+d+r+s+t},
\]
\[
 \frac t{a+d+r+s+t}-\frac e{a+d+r+s+1},\qquad
 \frac{5t}{a+d+r+s+t}-\frac j{a+d+r+s+1},
\]
\[
 K_{AE}-rC_{AE},\quad K_{AE}-sC_{AE},\quad
 K_H-tC_H,\quad K_I-tC_I.\tag{1}
\]
每一条**客户总和**均非负。首条是真第二位偏离比较；次两条是新真实末位对E及五T的BR；其余是原AE第四位和原(A,T_i)第三/四位对新合法R/S/T的安全分母比较。分母只上界未来覆盖者，不冻结未来行动；也不要求被强制D自己最优。

# 任意非负共同权的投影

取固定整行非负权(α,β,γ,δ,ε,ζ,η)，无需和1。对可见旧客户状态z，设
\[
\begin{aligned}
 M(z)={}&\alpha\frac b{a+b+c+d+e}+(\delta+\epsilon)K_{AE}+\zeta K_H+\eta K_I\\
 &+\max_{r,s,t\in\{0,1\}}\left\{
 \frac{-\alpha d+(\beta+5\gamma)t}{a+d+r+s+t}
 -\frac{\beta e+\gamma j}{a+d+r+s+1}\\
 &\hspace{42mm}-(\delta r+\epsilon s)C_{AE}-t(\zeta C_H+\eta C_I)
 \right\}.
\end{aligned}\tag{2}
\]
零分子即使分母0也取0；任何真非零项分母正。则对每份原完整五人SPE
\[
 \boxed{\sum_x M(z_x)\ge0.}\tag{3}
\]
证明：真实新分支给每客户一个特定(r_x,s_x,t_x)，将七个总slack按同一非负权相加≥0，正是未取max前的客户和；逐客户max只将它增大。局部max未必可由一张完整策略同时实现，扩大域仍保持必要性。不能用min替代max，也不能每客户自由选一套权却只借原七个全局slack。

旧AE_hist和second_hist及共同j已足够算全部K/C量，不需要隐藏的跨族配对。δ=ε时max只依k=r+s∈{0,1,2}及t∈{0,1}，可由八态缩成六态；未要求新R/S覆盖集相同。非对称权一般仍须八态。

# 旧点分离是本族的一组实例

冻结权分子按一百万分母为(819936,80557,2110,26105,26105,15852,29336)。它们与同目录separate JSON的约分形式一致，非负，和1.000001；非归一不影响(3)。代旧64正有理原子点得到
\[
 \sum_z m_zM(z)=
 -\frac{336525906357864252494704662357779526105596687}
 {24837228663957176671172182423497877773536000000}<0.
\]
此固定点的64×8精确计算、64 maxima、独立七式重构及一次真实运行已在[C2独立审查#d7-fixed-primal](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md#d7-fixed-primal)完整保存。本批两separate主源与C2比较原件逐SHA相同，复用那次完整阅读/认证，0重新运行或重授独审。

由(3)的全称必要性，这个旧点不能保持原数据延拓成真第二位→D分支。它并未给“增加本行后整个松弛”的最优值，更不是完整SPE反例。separate发现器使用NumPy/SciPy先找λ；最终负号用有理数与全部八态承担，不靠LP数值最优。其ROOT/SOURCE/THIRD/SECOND/sh实际导入third_D_completion，本批已将该依赖完整读入，不能把单个separate.py叫独立运行包。

# 与浮点补全及当前主问题的联系

[固定点补全](../计算/第三位与第二位复制D的固定点补全--计算.md)先有133行第三位→D双尾数值可行，再有283行联合第二位→D正最小最大违量；本七行是后一诊断的活动行精简，正确固定点非延拓由本精确证书承担。后续[564/908全型列生成](../程序/第二位D分支的列生成与完整主题定价--程序.md)在扩大旧类型域重新搜质量，不能把旧64点被排的结论授给所有新列。

5808B源正文的一般任意非负权包络、八/六态和原子max方向已自足保存；源说“root已请求审查”是旧时状态，C2 primary真实独审接受的范围另按其记录。当前五人half已另证，六人主目标未因此闭合。阶段三可登记“七真IC联合推出包络”“固定λ特例/精确分离”“数值活动行来源”，不将程序导入等同逻辑依赖或宣称外审/新颖性。
