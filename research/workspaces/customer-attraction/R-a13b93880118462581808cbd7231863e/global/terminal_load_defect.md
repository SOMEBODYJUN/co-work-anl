# 末两主题负载支配的精确缺口预算

状态：2026-10-21，自足解析观察；可作为结构性充分条件使用。没有证明一般缺口预算，不解决 Q-CAG-HALF。本文仅保存在个人工作区。

采用 CAG-MODEL。固定 m≥2 和任一完整历史依赖纯 SPE，真实终局为 (S_1,...,S_{m−2},A,B)。对客户 x，记 p_x 为前 m−2 人的真实负载，a_x=1_A(x)，b_x=1_B(x)，c_x=p_x+a_x+b_x。记末两位真实收益 u_A,u_B，早期总收益 P，W=P+u_A+u_B，s=min(u_A,u_B)。

任取 α,β≥0 且 α+β=m−2，定义

\[
D(\alpha,\beta)=\sum_{x:c_x>0}\frac{(\alpha a_x+\beta b_x-p_x)_+}{c_x},
\quad
R(\alpha,\beta)=\sum_{x:c_x>0}\frac{(p_x-\alpha a_x-\beta b_x)_+}{c_x}.
\]

两量均非负。若 c_x=0，则 p_x=a_x=b_x=0，故不会遗漏任何非零项。由 t=t_+−(−t)_+，逐客户相除后求和精确得到

\[
P=\alpha u_A+\beta u_B+R-D,
\qquad
W=(\alpha+1)u_A+(\beta+1)u_B+R-D.
\tag{1}
\]

所以不使用任何额外均衡性质，已有

\[
W\ge m s-D.
\tag{2}
\]

令 θ(h) 为固定真实早期有序前缀 h 的两剩余人最坏末位最佳回复值。已有末两人保底给 u_A,u_B≥θ(h)，全局静态安全值 v_m 满足 θ(h)≥v_m≥OPT_m/(2m−1)。因而若存在 α,β 使

\[
D(\alpha,\beta)\le s/2,
\tag{3}
\]

则由 (2)

\[
W\ge(m-\tfrac12)s\ge(m-\tfrac12)v_m\ge\operatorname{OPT}_m/2.
\]

保留 (1) 中的 R 和末两位超出 θ(h) 的富余，还得到更精确的充分判据

\[
D-R\le \tfrac12\theta(h)
 +(\alpha+1)(u_A-\theta(h))+(\beta+1)(u_B-\theta(h)).
\tag{4}
\]

不过 (4) 代入 (1) 后等价于 W≥(m−1/2)θ(h)；其正负缺口分解本身没有证明这个全局不等式。因此不把参数化恒等式称作一般支付机制。判据 (3) 是可以不先知道 v_m 或 OPT_m 而由真实主题、负载及末两收益检查的结构性充分条件；它允许少量点态支配违例。

若原末两支配条件 p_x≥αa_x+βb_x 逐客户成立，则 D=0，直接恢复 terminal_pair_load_security.md 的条件结果。一般 D≤s/2 仍未证明；D 可以由给定终局计算，但仅因它可计算，并不能推出一般 half。本文不提供对 D 的跨真实分支上界，也没有有限搜索外推。

边界：零客户时全部量为零；空主题、重复主题和任何历史平局均保留；m=2 时 α=β=0，D=R=P=0。若 s=0，已有尾两保底及有限目录分母迫使全部主题为空，目标乘法不等式成立。

依赖：research/current/customer_attraction/model.md、last_two_floor.md、oblivious_security.md；同工作区 security/terminal_pair_load_security.md 仅用于比较原 H 条件。
