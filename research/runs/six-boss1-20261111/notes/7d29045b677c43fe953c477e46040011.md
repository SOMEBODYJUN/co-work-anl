# 真实末节点之间的条件运输付款

状态：逐客户域、真实 IC 与非负组合投影已推导；联合分离器正在实现。本文不是六人 half 证明，也不是 SPE 反例。

作者任务：`/root/tail_constraints`。只改本文及同名目录；不操作 Git。

## 1. 已核对的模型和重复定位

实读 `state/定义/共同目录完整历史模型--定义.md` 与六人问题页：有限单位客户、有限共同**标签**目录、完整有序历史纯 SPE、所有离轨和平局均保留。

对固定倒二历史，令背景为 b，记

\[
v_b(T)=\sum_{x\in T}\frac1{b_x+1},\qquad
d_b(T,R)=\sum_{x\in T\cap R}\frac1{(b_x+1)(b_x+2)}.
\]

真实末回复 R_i 对 T_i 满足所有跨回复查询。任意概率 λ_i 的这些查询给

\[
\mathbb E_i d_b(T_i,R_i)
\le \sum_x \frac{p_xq_x}{(b_x+1)(b_x+2)},
\quad p_x=\sum_i\lambda_i1_{T_i}(x),\quad
q_x=\sum_i\lambda_i1_{R_i}(x).
\]

这不是新切面。均匀六指标时，它和源 IC 相加恰是既有菜单行 `M=S+V/6`；已依 Main 提醒实读 `state/引理/真实末两人菜单交集消去--引理.md` 与 `state/计算/实际末主题分支分离器与四菜单补价原点核验--计算.md` 核准。不能把它重新计为 5692 系统之外的新信息。

以下真正新增的候选连接的是旧索引 R/Z 与指定新真实分支的主题/末位节点，不只重组 M/Z。

## 2. 所给完整策略中的真历史

actual 为 A_1,…,A_6，旧分支在 actual 前三 h 后强制 T_i，真续局为 B_i,C_i。旧边 e=(f,i,j) 指在 `(h,T_i)` 的第五位强制 B_j（f=0，i≠j）或 C_j（f=1，允许 i=j）；其真末回复为 R_e。随后在 actual 前四历史强制第五位 R_e，真末回复为 Z_e。

令客户的 actual 前三/四负载为 p/P。若旧索引词为 w_i=(t_i,b_i,c_i)、w_j=(t_j,b_j,c_j)，则 R_e 节点末位前负载为

\[
L_e=p+t_i+(w_j)_{1+f},
\]

而 Z_e 节点末位前负载为 P+r_e。因此旧两个真末收益分别是

\[
U_{R,e}=\sum_x\frac{r_e}{L_e+1},\qquad
U_{Z,e}=\sum_x\frac{z_e}{P+r_e+1}.
\]

新分支 F 是 actual 第 2/3/4 位强制 A_6 的真续局之一，或共同最大主题 M 的真根分支。其末位前负载为 L_F，真末主题会员为 c_F。新分支中每个具名 H_j、M，以及其六主题菜单的每个 Y_j，均是同一目录里的合法主题。

## 3. 精确条件耦合域

固定一个完整旧 hist h（含 actual 位和六个 `(t,b,c)` 的八格重数）、一个旧 group g=(f,diag,w_i,w_j)，以及新分支 F。旧四态质量记

\[
\rho_g^h(r,z),\qquad (r,z)\in\{0,1\}^2.
\]

01/10/11 来自已有 joint-reply 列，00 为 hist 质量减三者之和。新分支状态质量 η_F^h(s) 来自已有 family-state 列。两组总量均为同一 hist 客户质量 μ_h。

引入

\[
\pi_{g,F}^h(r,z,s)\ge0,\quad
\sum_s\pi(r,z,s)=\rho_g^h(r,z),\quad
\sum_{r,z}\pi(r,z,s)=\eta_F^h(s).\tag{T}
\]

真实客户联合必投影到 (T)。分别为各 group 允许不同耦合扩大了域；这不会引入伪必要条件。这里不声称一个可行的全部两边耦合可同时粘成所有 R/Z 的共同客户原子。

同一 group 中有名边的数量 n_g 只由 hist 决定。按轨道 o=(0,0),(1,0),(1,1) 平均时，权重分别为 n_g/30、n_g/30、n_g/6。新分支不随 i,j 改变，因此每个 group 的新状态边缘仍恰为 η，而不能随旧回复免费更换。

## 4. 同一 π 上的真实不等式

新真末位可分别查询 R_e、Z_e，旧 Z_e 真末位可查询新分支的任一合法主题 X：

\[
U_F\ge\sum_x\frac{r_e}{L_F+1},\qquad
U_F\ge\sum_x\frac{z_e}{L_F+1},\qquad
U_{Z,e}\ge\sum_x\frac{1_X}{P+r_e+1}.\tag{IC}
\]

所有比较都是末位当场最佳回复，完全没有冻结更早玩家偏离后的后继。互斥分支的 U_F、U_{Z,e} 也不认作 actual u_6 或 W。

在 (T) 中，同一 (r,z,s) 同时决定这三类成本。若 X 是菜单平均，取会员 ξ_X(s)=ℓ(s)/6；该成本对 ℓ 仿射，故原 0/6 端点凸化仍有效。这里不从 ℓ 端点反推出 Y_j 的自索引相关性或其自身终位利润。

## 5. 单查询的精确排序投影

对于旧 Z→X，给定 hist/group 的旧 R 质量 r、主题 X 质量 y，最小可能查询成本为

\[
\frac{y}{P+2}+\frac{\max(0,y-r)}{(P+1)(P+2)}.\tag{Z-min}
\]

证明：把尽可能多的 X 质量放在 R=1 的低价客户上，最多可放 r；剩余至少 max(0,y−r) 只能付 1/(P+1)。运输域允许此安排，故是精确最小值。

对于新末→旧 R（或 Z），给定旧回复会员总量 q 和新状态分布，精确最小成本是把 q 质量依次放到 L_F 最大的状态。等价阈值式为

\[
\min_\pi\mathbb E_\pi\frac{r}{L_F+1}
=\max_\theta\left\{\theta q+
\sum_s\eta(s)\min\!\left(0,\frac1{L_F(s)+1}-\theta\right)\right\}.
\tag{tail-min}
\]

每个阈值都是逐客户合法下界；最大值可取有限报价断点。这个式子只用于单行诊断，不代替下面的联合运输。

## 6. 联合多查询先合权、后运输

对每个轨道 o，令 a_o,b_o≥0 分别是新末查询 R/Z 的真行权，c_{o,X}≥0 是旧 Z 查询 X 的真行权。全部权是**整行统一常数**。给 group g 所属轨道 o，设 ω_g=n_g/|o|。其运输成本是

\[
C_{g}(r,z,s)=\omega_g\left[
\frac{a_or+b_oz}{L_F(s)+1}
+\sum_X c_{o,X}\frac{\xi_X(s)}{P+r+1}\right].\tag{C}
\]

总预算为

\[
B=\sum_o(a_o+b_o)U_F+
\sum_{o,X}c_{o,X}\overline U_{Z,o}.
\]

真实 IC 蕴含

\[
\boxed{B\ge\sum_{h,g}\min_{\pi\in T(\rho_g^h,\eta_F^h)}
\sum_{r,z,s}\pi(r,z,s)C_g(r,z,s).}\tag{J}
\]

同一 R/Z 四态与同一新状态共同出现在 (C) 中；先分别计算各真行的最小值通常丢失约束，不能用其替代 (J)。例如 R 与 Z 互斥时，两者无法同时把各自质量放在同一批低报价状态。

对每块运输选任意对偶势 α_g^h(r,z)、β_g^h(s) 满足

\[
\alpha_g^h(r,z)+\beta_g^h(s)\le C_g(r,z,s)
\quad\text{对全部四态及全部新状态},\tag{D}
\]

便得到纯原边缘线性必要行

\[
\boxed{B-\sum_{h,g}\left[\sum_{r,z}\alpha\rho+
\sum_s\beta\eta\right]\ge0.}\tag{CUT}
\]

β 在相同新状态列上须累加所有 group 的贡献，不能为每条 IC 重复领取一份新分支收入。α/β 可依 hist/group，因为它们只来自逐客户域的点态下界，而真实 IC 权 a,b,c 不依客户。

对于一个只记录 16 hist 的点，(CUT) 可作为该支持的精确线性切。若需写成全域必要行，可对未列 hist 取 α=β=0；因 (C) 非负，对偶可行性仍成立，但全域 B 的利润贡献必须照定义保留。

## 7. 依赖与当前边界

除上述模型和菜单页，已实读：同源末主题重查询方法；嵌套回复与同源再查询联合切面；同菜单真实末回复图盒消元程序；末两人强 PAIR；真实末主题分支与旧回复直方图条件联合；索引主题与实际第四步 B 分支联合必要图程序。另直接读原 `full_new_reply_closure.py`、`actual_fifth_nested.py` 解码 R/Z 真历史及 group，读 `audit_point_structure_and_prices.py` 核旧 hist 编号与四 family 列结构。

本次不重写、不认领这些旧结果。旧 R→新 H/M/Y 无新乘积线性行由 `/root/cross_branch_math` 负责；本文只处理 Z→新主题及新末→旧 R/Z，并要求联合合权运输。待 `/root/augmented_lp` 生成加入 24 已知不同切面的新点后，以新点为主要分离对象。
