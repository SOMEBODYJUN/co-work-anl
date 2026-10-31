# 全背景弱末端推送若成立，直接推出逐人OPT/(2m)保底

状态：条件性归约，未证明假设。一般半覆盖仍 OPEN。

固定m人原模型、一个长度k的合法前缀，其负载为b，余下r=m−k人。固定该子博弈的完整纯SPE。对任意分布p，强制当前首位取B~p后沿真实后继所得r主题终局记Z(B)，当前首位实际最优收益记u。弱推送候选为

\[
u\ge C(p):=\mathbb E_{A,B\text{ iid }p}
\sum_{x\in A}\frac1{1+b_x+c_x(Z(B))}.
\tag{WP}
\]

`WP`只要求根最优收益支付C，不要求平均强制根收益D支付C；后一个强式已有34客户反例。

定义有固定背景b、另有r个不观察查询的静态竞争槽的安全值

\[
v_{r+1}(b)=\max_p\min_{z\in\mathcal S^r}
\sum_Ap_A\sum_{x\in A}\frac1{1+b_x+c_x(z)}.
\]

安全最优p存在。`Z(B)`的推送是一个合法r槽静态分布，而A独立，故 `C(p*)≥v_{r+1}(b)`。

另一方面，对任意r槽分布Q，令 `L_x=b_x+E_Q c_x(z)`、`g(T)=Σ_{x∈T}1/(1+L_x)`、`M=max_T g(T)`。Jensen给 `max_T E_Q f_z(T)≥M`。取m个达到OPT_m的比较主题，以d_x记其负载。逐客户有 `1_{d_x>0}≤(d_x+L_x)/(1+L_x)`，于是

\[
OPT_m\le mM+\sum_x\frac{L_x}{1+L_x}.
\]

b是k个原目录主题的负载，Q的另r槽也在同一目录，因此后一项为k个真实前缀主题g值加r个随机主题g值之和，至多 `(k+r)M=mM`。所以对所有Q，

\[
\max_T E_Q f_z(T)\ge \frac{OPT_m}{2m}.
\]

有限minimax给 `v_{r+1}(b)≥OPT_m/(2m)`。与WP合并得到每个原完整SPE每个真实位置都满足

\[
u_i\ge\frac{OPT_m}{2m},\qquad
W=\sum_i u_i\ge\frac{OPT_m}2.
\]

全零客户时所有量为0；空主题、重复主题、任意平局与完整有序历史依赖均没有被限制。真正未闭合的义务只有WP本身，且需要全部合法前缀背景，不只是零背景根。

附：原预算 `B(v)=max_{z≥0}[Σ_xmin(1,(Mz)_x)−vΣ_Tz_T]` 也有精确LP对偶

\[
B(v)=|N|-\max\{\sum_xy_x:0\le y_x\le1,
\ \sum_{x\in T}y_x\le v\ \forall T\}.
\]

因而 `B(u_i)≤W` 等价于删去总客户质量至多W后，全部主题容量能压到u_i。此为表示，不自动给WP或早期玩家预算。
