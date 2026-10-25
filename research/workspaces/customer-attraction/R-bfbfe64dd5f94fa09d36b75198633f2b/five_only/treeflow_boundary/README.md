# 五人共同源流：准确残差与两个完整 SPE 边界

状态：只讨论原 CAG-MODEL 的五名提供者、任意有限单位客户与共同目录、全部有序历史纯 SPE。本文没有证明 `OPT_5<=2W`，也没有目标反例。它固定了 uniform-net/copy-swap 路线必须支付的准确残差，并用两个无害的完整 SPE 排除两项曾被隐含使用的自动容量/换序假设。

## 1. Raw swap 的准确共同银行

始终固定同一份完整策略。对第 `i<=4` 行的查询主题 `A`，写原强制查询终局

\[
 z_i(A)=(h_i,A,B_i(A),Y_i(A)),\qquad
 d_i(A)=u_i(z_i(A)),\quad v_i(A)=u_{i+1}(z_i(A)).
\]

沿既有 uniform-net 域定义

\[
C_i(z)=d_i(z)+\sum_{k>i}[M(z_{<k})-u_k(z)],\qquad
r_i(z)=\eta_i+\mu C_i(z)-a\cdot\ell_i(z)\ge0
\]

（对每个 raw 有序终局成立），并令

\[
P_i(A)=a\cdot1_A+\mu M(h_i,A).
\]

把原尾部不变地交换前两动作，记 `s_i(A)=(h_i,B_i(A),A,Y_i(A))`。逐项展开得到

\[
2\mu(d_i-v_i)=r_i(z_i)-r_i(s_i)+P_i(B_i)-P_i(A). \tag{1}
\]

这里从未声称 raw swap 后仍为原策略的 SPE 续局。若原源质量为 `p_i(A)`，使用非负流量 `theta_i(A)`，令

\[
R=\sum p_i(A)r_i(z_i(A)),\qquad
L=\sum\theta_i(A)(d_i(A)-v_i(A)),
\]

则准确地

\[
2(R-\mu L)=\sum_{i,A}\big[(2p_i-\theta_i)r_i(z_i)
+\theta_i r_i(s_i)-\theta_i(P_i(B_i)-P_i(A))\big]. \tag{2}
\]

因此 `theta<=2p` 必须在每个精确源上成立；动作平衡也必须在同一精确行/前缀内成立。仅作全局动作平衡只能消去 `a` 部分，仍留下

\[
\mu\sum\theta_i(A)[M(h_i,B_i(A))-M(h_i,A)],
\]

没有一般符号。保留不利项时唯一自动得到的是

\[
\mu L\le R+\frac12\sum\theta\,\Delta P
+\frac12\sum(\theta-2p)_+r_i(z_i). \tag{3}
\]

## 2. 真正换序历史还有 signed mismatch

原策略在换序有序历史上的真实终局为

\[
w_i(A)=\operatorname{finish}_\sigma(h_i,B_i(A),A),\qquad
J_i(A)=r_i(w_i(A))-r_i(s_i(A)).
\]

于是 (2) 的真历史版本是

\[
2(R-\mu L)=\sum\big[(2p-\theta)r(z)+\theta r(w)
-\theta J-\theta\Delta P\big]. \tag{4}
\]

正的 `J` 是费用。把 `w=s` 等同会冻结两个不同有序历史之后的策略。反向查询 IC 本身仍合法，但其精确差为

\[
C_i(w)-C_i(x)=d_i(w)-d_i(x)+\Gamma
+S_{\rm desc}(x)-S_{\rm desc}(w), \tag{5}
\]

其中 `x=z_i(B_i(A))`、`Gamma=u_{i+1}(x)-u_{i+1}(w)>=0`，两个 descendant surplus 各自非负。使用 source-`B` 的那一份仍需要进入 `B` 的真实质量；它不是新钱包。

## 3. 完整 SPE 边界一：reverse-source 无有限支配

取六个互不相交的单客户主题、五名提供者。每个历史都选择一个尚未使用的主题；在深度一令下一动作是六主题的循环后继。任何未使用主题收益为一，已使用主题至多二分之一，所以这是覆盖全部有序历史的纯 SPE。

任意最优五元组恰遗漏一个主题。其均匀查询分布 `p` 在遗漏主题上为零，而根 first-follower 的六循环将某个正质量送到该遗漏主题。因此进入分布 `beta=pT` 对每个有限 `kappa` 都不满足

\[
\beta\le\kappa p.
\]

这对每个最优五元组都成立。该实例 `W=OPT_5=5`；它只否定自动 reverse-source capacity。

## 4. 完整 SPE 边界二：最优 row dual 下 `J` 仍有双符号

取八个互不相交的单客户主题。仍在每个历史选未使用主题；可在不同有序历史指定

\[
z=(1,2,3,4,5),\quad s=(2,1,3,4,5),\quad w=(2,1,6,7,8).
\]

所有 canonical threshold 为 `M=1`。raw 根终局中，进入主题重数为 `c` 时

\[
C=4+2/c-W.
\]

取 `mu=2, eta=-1`，并让 shadow 只支撑一个单客户主题：

\[
r=-1+2C-\ell_a\ge0
\]

对每个 raw 终局成立，且 `H=eta+mu u_1=1` 达到，故是该行 net-cap LP 的最优 dual。若 shadow 在主题 3，则 `J=r(w)-r(s)=+1`；若在主题 6，则 `J=-1`。所以 raw 定价最优性也不给真正换序尾部一个固定符号。

## 5. 与 half 账本的接口

沿既有 shared-saddle 记号

\[
G=\mu(I+S)+R,\qquad W=5\gamma+I+G+D-\mathrm{Cov},
\]

以及

\[
OPT_5=9\gamma-Q_{stat}-P_{opt}-Rep-Out.
\]

令 `H` 为 (2)/(4) 右侧，`S_stat=gamma+Q_stat+P_opt+Rep+Out`，则精确恒等式为

\[
2W-OPT_5=S_{stat}+2(1+\mu)I+2\mu S+2D
+H-2(\mathrm{Cov}-\mu L). \tag{6}
\]

未付项因此很具体：仍需构造 covariance-to-swap map，同时支付源过载、逐行 canonical 边界和正的 reverse-tail mismatch。不能把不同分支福利相加后称作同一份实际 `W`。
