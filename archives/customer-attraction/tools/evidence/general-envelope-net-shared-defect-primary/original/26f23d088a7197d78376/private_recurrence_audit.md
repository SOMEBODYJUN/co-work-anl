# private 负载递推的精确勘误与可回收控制式

**身份与范围。** 对用户附件 `upload/01-markdown-1-md` 中的单调递推作自足解析审计。采用全部 CAG-MODEL 量词；不证明一般 half，也不构成其反例。不运行新扫描，不认领新颖性。被审 `f_j` 定义来自 `research/current/customer_attraction/dynamic_maxima_bound.md` §§1–3，而不是另造函数。

令 `B_1,...,B_s` 为全部不同包含极大主题，每个合法行动固定路由至一个包含它的 `B_j`。客户 maximal incidence 为 `I`、重数为 `w_I`，过去路由计数为 `p`，`p_I=Σ_{k∈I}p_k`，尚余 `r` 人。core `I=[s]` 另记，不放入下式；`s=1` 的唯一极大主题情况已平凡。既有定义为

\[
 f_j(p,r)=\frac{w_{\{j\}}}{p_j+1}
 +\sum_{\substack{I\ni j\\2\le|I|\le s-1}}
 \frac{w_I}{p_I+r}.
 \tag{1}
\]

## 1. 被提议的单调性在 private 项严格反向

对 `r≥2` 及任意 `k`，直接相减得精确式

\[
\begin{aligned}
 f_j(p+e_k,r-1)-f_j(p,r)
 ={}&-\mathbf1_{k=j}\frac{w_{\{j\}}}{(p_j+1)(p_j+2)}\\
 &+\sum_{\substack{I\ni j,\ 2\le|I|\le s-1\\k\notin I}}
 \frac{w_I}{(p_I+r-1)(p_I+r)}.
\end{aligned}
\tag{2}
\]

若 `k∈I`，共享分母的新值为 `p_I+1+r-1=p_I+r`；若 `k∉I`，其分母减一；private 分母仅在 `k=j` 时由 `p_j+1` 增至 `p_j+2`。特别地

\[
 \boxed{f_j(p+e_j,r-1)=f_j(p,r)
 -\frac{w_{\{j\}}}{(p_j+1)(p_j+2)}.}
 \tag{3}
\]

因此只要 `w_{ {j} }>0`，用户所写 `f_j(p+e_k,r−1)≥f_j(p,r)` 就在合法转移 `k=j` 上严格失败。最小例是两名提供者、两个不交 singleton 主题 `B_1={a},B_2={b}`：`f_1(0,2)=1`，而 `f_1(e_1,1)=1/2`。这是公式的解析反例，不需选定特殊 SPE。

单调性在 `k≠j` 或 `w_{ {j} }=0` 时成立；全无 private 的目录满足全部这些单步单调性。它恰不能被用来自动跨越正 private 的 singleton 余域。

## 2. 合法的单步亏损、望远镜控制与补偿势

无条件可用的替代为

\[
 f_j(p+e_k,r-1)\ge f_j(p,r)
 -\mathbf1_{k=j}\frac{w_{\{j\}}}{(p_j+1)(p_j+2)}.
 \tag{4}
\]

若经过 `q≤r−1` 步、路由增量为 `a∈Z_{≥0}^s`、`Σa_k=q`，则共享分母变化为 `a_I−q≤0`，从而

\[
 \boxed{f_j(p+a,r-q)\ge f_j(p,r)
 -w_{\{j\}}\left(\frac1{p_j+1}-\frac1{p_j+a_j+1}\right).}
 \tag{5}
\]

全部新路由都为 `j` 时取等。`p_j=0` 且 `a_j` 增长时，private 损失可趋近整个块质量，不能笼统视为低阶误差。

等价地，

\[
 \Phi_j(p,r)=f_j(p,r)+w_{\{j\}}\left(1-\frac1{p_j+1}\right)
 =w_{\{j\}}+\sum_{\substack{I\ni j\\2\le|I|\le s-1}}\frac{w_I}{p_I+r}
 \tag{6}
\]

满足 `Φ_j(p+e_k,r−1)≥Φ_j(p,r)`。这是正确的补偿势，但补偿的 private 信用尚未由一份真实福利预算支付；势单调本身不能推出收益或覆盖的 half 界。若沿此思路推进，一项明确义务是对式 (5) 的 private 总损失作不重复使用 `W` 的共同付款。

## 3. 此勘误不否定已有后缀包络归纳

既有 dynamic-maxima 证明没有使用被审的错误单调式。它把 raw floor 换为在全部后续深度上的 suffix minimum，再对全部真实有序历史逆向归纳：当前偏离整个 `B_j` 后，无后继再路由至 `j` 时直接用式 (1)；存在这样的后继时，当前 `B_j` 包含该后继的真实主题，故同一终局上当前偏离者收益至少为该后继收益，再应用后继的归纳保底。

后续若细化递推，必须保留路由/私有块状态或显式损失，不能把“shared 部分不降”换成全部 `f_j` 不降。与末位 maximality、active-maxima 约化和旧谱的共享缺陷推论相关的范围审查见同目录 `architecture_audit.md` 与 `review_shared_defect.md`；这里没有另加这些结论。
