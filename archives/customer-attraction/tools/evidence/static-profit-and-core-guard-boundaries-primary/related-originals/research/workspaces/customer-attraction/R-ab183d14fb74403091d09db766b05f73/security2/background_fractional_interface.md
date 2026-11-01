# 合法背景剩余利润与自由分数安全值：精确静态接口及同人数漂移

2026-10-22，个人研究备份。模型严格为CAG-MODEL：单位客户、单位提供者、有限共同目录、全部有序历史上的纯SPE和任意历史依赖平局。**一般Q-CAG-HALF、FF-LEADER及聚合安全值桥仍OPEN。** 本文的定理均为静态不等式或精确恒等式，不把它们声称为新的动态SPE支付证明。

自由分数值及其minmax、嵌入、Fenchel证书已见
`R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md`，不是本轮新候选。
本文将该静态接口接到非零背景的正确利润对象，并把自由分母与既有互惠K核的差写全。
§2的统一背景常数强化及两系数模板最优性由本轮recursion2提出；作者在此重构证明。
§2—3及§4—5主要代数已由本轮recursion2独立核对，确认端点、d=0、优化方向与弦差正确，并据其意见显式补足r≥2范围。全文外审或新颖性未认证。

## 1. 对象

固定合法过去背景客户负载b，剩r≥1名玩家。主题分布p、q的客户边际记为

\[
 \rho_x=\sum_{A\ni x}p_A,\qquad
 \alpha_x=\sum_{A\ni x}q_A,\qquad
 L_x=(r-1)\alpha_x.
\]

定义

\[
 g_{r,b,q}(A)=\sum_{x\in A}\frac1{b_x+1+L_x},\quad
 F_{r,b}(p,q)=\sum_x\frac{\rho_x}{b_x+1+L_x},\quad
 w_r(b)=\min_q\max_Ag_{r,b,q}(A)=\max_p\min_qF_{r,b}(p,q).
\tag{1}
\]

最后一个等式使用已有凸minmax接口。对于r个比较主题T_1,…,T_r，令d_x为其客户负载。正确的剩余利润为

\[
 Q_b(d)=\sum_{x:d_x>0}\frac{d_x}{b_x+d_x},\qquad
 Q_r^*(b)=\max_{T_1,\ldots,T_r}Q_b(d).
\tag{2}
\]

这不是含过去玩家的完整覆盖。实际终局的剩余r人收益和恰为Q_b(d)。

## 2. 背景越高时更强的静态门槛

先看r≥2。对B≥0定义

\[
 C_r(B)=\max_{1\le d\le r}\frac{d(r-d)}{B+d}.
\tag{3}
\]

如果存在一个达到Q_r^*(b)的比较元组，使其覆盖的所有客户均有b_x≥B，则

\[
 \boxed{Q_r^*(b)\le [r+C_r(B)]\,w_r(b).}
\tag{4}
\]

**证明。** 取c=C_r(B)/(r−1)。对b≥B、整数d∈{1,…,r}及L∈[0,r−1]有

\[
 \frac d{b+d}\le\frac{d+cL}{b+1+L}.
\tag{5}
\]

两边乘正分母后，右减左的分子为

\[
 d(d-1)+L[c(b+d)-d].
\tag{6}
\]

它对L仿射。L=0时非负；L=r−1时非负恰等价于
c(r−1)≥d(r−d)/(b+d)，由(3)保证。d=0时(5)另显然成立。
将(5)逐客户相加，并用L_x=(r−1)Σ_{A∋x}q_A，得到对每个q

\[
 Q_b(d)\le\sum_{j=1}^r g_{r,b,q}(T_j)
 +c(r-1)\sum_Aq_Ag_{r,b,q}(A)
 \le[r+C_r(B)]\max_Ag_{r,b,q}(A).
\tag{7}
\]

取最优比较组合并对q取最小即得(4)。r=1单独有Q_1^*(b)=w_1(b)。

取B=0时C_r(0)=r−1，故合法非零背景也总有Q_r^*(b)≤(2r−1)w_r(b)。
最直接的逐客户版本是

\[
 \frac d{b+d}\le\frac{d+L}{b+1+L},\qquad
 \frac{d+L}{b+1+L}-\frac d{b+d}
 =\frac{d(d-1)+bL}{(b+d)(b+1+L)}\quad(d\ge1).
\tag{8}
\]

正背景的额外bL余量应保留，不能先删除后声称得到精确预算。B大时
C_r(B)≤r²/[4(B+1)]，因此(4)趋于r而不是2r−1。
一般实际前缀仍可能有b_x=0，故这个强化本身不闭合根半覆盖。

**两系数逐客户模板的最佳性。** 仅考虑对所有b≥B、d=1,…,r、L∈[0,r−1]成立的模板

\[
 \frac d{b+d}\le\frac{A d+C L}{b+1+L},
\tag{9}
\]

其共同目录成本为rA+(r−1)C。d=1,L=0强制A≥1。对b=B,L=r−1，

\[
 rA+(r-1)C
 \ge\frac{d(B+r)}{B+d}+(r-d)A
 \ge r+\frac{d(r-d)}{B+d}.
\tag{10}
\]

取max d给成本下界r+C_r(B)，由(5)取得。这里只证明这个统一两系数模板的最优成本；**不声称Q_r^*(b)/w_r(b)本身达到该常数。**

## 3. 非均匀背景可保留逐客户折扣

本节设r≥2；r=1直接使用Q_1^*(b)=w_1(b)。令c_x=C_r(b_x)/(r−1)，定义

\[
 h_q(A)=\sum_{x\in A}\frac{c_x}{b_x+1+(r-1)\alpha_x}.
\]

同一证明给出更细且对每个q成立的接口

\[
 \boxed{Q_b(d)\le\sum_{j=1}^r g_q(T_j)
 +(r-1)\sum_Aq_Ah_q(A).}
\tag{11}
\]

固定一个比较组合时，还可在d_x>0处取
c_x=d_x(r−d_x)/[(r−1)(b_x+d_x)]，在d_x=0处取c_x=0。
它是依该整数比较负载选择的折扣，不能当作不依比较组合的通用c_x。

## 4. 固定查询/对手的同总人数前缀漂移

本节设r≥2。沿实际或任意合法前缀新增主题A，令z_x=1_{x∈A}，同时r减一；p、q暂保持不变。
设

\[
 d_x=b_x+1+(r-1)\alpha_x,\qquad
 d'_x=b_x+z_x+1+(r-2)\alpha_x.
\]

则精确有

\[
 \boxed{F_{r,b}(p,q)-F_{r-1,b+1_A}(p,q)
 =\sum_x\frac{\rho_x(z_x-\alpha_x)}{d_xd'_x}.}
\tag{12}
\]

正项仅出现在z_x=1，并且

\[
 \frac{\rho_x(1-\alpha_x)}{d_xd'_x}
 \le\frac{\rho_x}{(b_x+1)(b_x+2)}.
\tag{13}
\]

z_x=0处保留精确的负信用−ρ_xα_x/(d_xd'_x)。
设τ(b)=Σ_xb_x/(b_x+1)，则Δτ=Σ_{z_x=1}1/[(b_x+1)(b_x+2)]，因ρ_x≤1，

\[
 F_{r-1,b+1_A}(p,q)+\tau(b+1_A)
 \ge F_{r,b}(p,q)+\tau(b).
\tag{14}
\]

多个非负权重λ_j的固定核同时运输时，充分的逐客户容量为
Σ_j λ_jρ_{j,x}≤1（仅对新增主题命中的客户要求）。更精确的容量可用

\[
 \sum_j\lambda_j\frac{\rho_{j,x}(1-\alpha_{j,x})(b_x+1)(b_x+2)}{d_{j,x}d'_{j,x}}\le1.
\tag{15}
\]

因此分数对手在命中客户上的α能减少正税需求；仍不能给无界多个源各收一次完整τ。

**优化器改变时的精确余项。** 取根与下一背景的鞍点(p,q)、(p',q')，记w,w'。
则

\[
 w'-w=\underbrace{[w'-F_{r-1,b+1_A}(p,q')]}_{\gamma_{query}\ge0}
 +[F_{r-1,b+1_A}(p,q')-F_{r,b}(p,q')]
 +\underbrace{[F_{r,b}(p,q')-w]}_{\gamma_{opponent}\ge0}.
\tag{16}
\]

两余项非负分别用下一q'的max性质与根p的min性质。它们不能无声地置零。
已有背景嵌入直接给w'≥w；(12)—(16)只把变化的客户来源和选择余项展开。
它们没有证明当前真实玩家u满足u≥w，也没有证明
D=u+(r−1)w'−rw非负或其全路径净亏损可支付。

## 5. 与真实互惠K核的精确接点

在同一b、r下，采用已有K核

\[
 K(A,B)=\sum_x\left[\frac{1_{x\in A\cup B}}{b_x+1}
 +\frac{1_{x\in A\cap B}}{b_x+r}\right].
\tag{17}
\]

这里与`coupling/nested_prefix_reciprocal_transport.md`一致：它的重复席位数为r−1，终局总剩余人数为r。
对独立A∼p,B∼q，令f_b(q)=Σ_xα_x/(b_x+1)。reciprocal的精确弦差给

\[
 \boxed{\mathbb E K(A,B)=F_{r,b}(p,q)+f_b(q)+J_{r,b}(p,q),}
\tag{18}
\]

其中

\[
 J_{r,b}(p,q)=\sum_x
 \frac{\rho_x(r-1)^2\alpha_x(1-\alpha_x)}
 {(b_x+1)(b_x+r)[b_x+1+(r-1)\alpha_x]}\ge0.
\tag{19}
\]

证明是逐客户的

\[
 \frac{1-\alpha}{b+1}+\frac\alpha{b+r}
 -\frac1{b+1+(r-1)\alpha}
 =\frac{(r-1)^2\alpha(1-\alpha)}
 {(b+1)(b+r)[b+1+(r-1)\alpha]}.
\]

这使自由分母可接到原完整策略的真实末回复K运输，但源/汇两侧的f_b(q)与J必须一起保留。
运输后主题对一般变成相关分布；不能自动再将它写成独立p×q或新的w鞍点。
本式没有克服多源初始覆盖编码、终端利润吸收或早期真实分支接力的缺口。

**固定分布时弦差释放的精确形式。** 对§4的同人数前缀步，固定p,q令J,J'为前后弦差。
写t=b+1、l=r−1。每个客户都有J_x−J'_x≥0，且

\[
 J_x-J'_x=\begin{cases}
 \rho_x(1-\alpha_x)\left[\dfrac1{t(t+1)}-\dfrac1{(t+l\alpha_x)[t+1+(l-1)\alpha_x]}\right],&z_x=1,\\[4pt]
 \rho_x\alpha_x\left[\dfrac1{(t+l\alpha_x)[t+(l-1)\alpha_x]}-\dfrac1{(t+l-1)(t+l)}\right],&z_x=0.
 \end{cases}
\tag{20}
\]

方括号均非负，因为0≤α≤1、l≥1、t≥1。这个释放量恰解释了F正漂移比K并集税小的部分；
它是已有(12)、(17)—(19)的代数差，不是额外获得一份可重复收费的预算。

## 6. 单位K源的动态支付及不能免费放大的位置

本节接用本轮`coupling2/terminal_absorption_and_capacity.md`的单源终端吸收。
在m≥2人的零根背景完整SPE中，记全实际终局负载为c、τ_m=Σ_x c_x/(c_x+1)。
该吸收与嵌套前缀运输一起给出任意单位主题对源的

\[
 \mathbb E_\mu K_0(A,B)\le W+\tau_m.
\tag{21}
\]

理由是每条纯对路线都可汇到实际末主题的对角，单位总质量使每个前缀截面的逐客并集容量自动≤1。
到末端为2u_m+τ_(m−1)，再由实际倒二玩家复制末主题的合法偏离吸收到W+τ_m；
此处没有增加幽灵玩家。
根取w_m(0)的一对鞍点p,q，并令μ=p×q，(18)精确给出

\[
 \boxed{w_m(0)+f_0(q)+J_{m,0}(p,q)\le W+\tau_m.}
\tag{22}
\]

这是一个合法的动态单位源预算，但一般不足以支付最优m主题的覆盖。
若把该源放大λ倍，起始客户并集信用是λ(ρ_x+α_x−ρ_xα_x)，不必在最优并集每个客户都≥1；
同时每个中间截面的负担也相应放大，单位质量自动容量不再成立。
鞍点的KKT条件没有给出这些逐客覆盖下界或沿真实回复后的逐客容量上界。
真实K回复把μ变为相关主题对分布；强行重选为独立鞍点会改变这些信用与容量，不能免费进行。

因此(16)中的鞍点选择余项不是一个已经识别为负数、可以由税机械消掉的误差；其符号其实均非负。
尚缺的接口是将m级比较覆盖编码成可按实际不同玩家吸收的多源流，或把相关主题对的额外质量与负交集信用共同支付。
本节不从(22)推出W≥mw，也不推出OPT≤W+τ_m。

## 7. 检查与本轮未推进部分

`audit_background_fractional_interface.py`使用Fraction核对(5)、(8)、(12)、(18)—(19)的有限有理网格及边界；普遍结论依据以上代数证明，有限网格不扩大量词。

`background_cone_attack.py`生成合法非零前缀下的完整remaining-SPE锥，使用现成自由minmax/Fenchel方法攻击FF-LEADER与局部D。
对应json仅是数值探索；优化常落退化等号射线，没有提供新反例或一般支付证明。
不以阴性扫描次数作为数学成果。

另有`probe_floor_protection.py`及`static_floor_*.json`探索了“仅要求后继逐人达到自由w便可保护某个根主题”的静态松弛。
数值发现的288客户例已由recursion2给出的5客户、全部2子集目录解析例替代；只保留发现来源，不恢复浮点证书。
该松弛在w阈值下也失败，不能由后继保底归纳FF-LEADER；这些人为后继不是最佳回复，因而不否定FF-LEADER或一般半覆盖。
