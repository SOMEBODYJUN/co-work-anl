# 任意 owner 的最优前缀调和误差预算

2026-10-24，Boss21/random_portfolio 工作稿。适用任意有限单位客户、任意有限非空共同目录、任意人数、重复与空主题及所有完整历史纯 SPE。下面预算甚至不需要 SPE：它适用于任意满足所写前缀约束的叶族。**Q-CAG-HALF、TB、SM-opt-exists 均未闭合。** 这是旧 owner 插入式的任意固定 owner 前缀信用推论，只放松既有 first-owner 选择限制，不声称已支付跨真实分支的势漂移，也不声称新颖性。

## 1. 复用的 owner 势与单位误差

固定任意合法比较元组 `T=(T_1,...,T_m)`，并集为 `O`。给每个 `x∈O` 固定任意一个 owner `o(x)`，满足 `x∈T_o(x)`。它不必是第一个含 x 的比较槽。记 `Q_i={x:o(x)=i}`，这里只是分析分块，不把 Q_i 当合法主题。

对一个 m 槽 profile B（允许形式空槽），记 `c_x(B)=#{i:x∈B_i}`。既有 owner 势是

\[
F_Q(B)=|O|+\sum_{x\notin O}H_{c_x(B)}
-\sum_{\substack{x\in O\\x\notin B_{o(x)}}}\frac1{c_x(B)+1}.
\]

若 T 最优，则旧 owner-hybrid 证明给 `0≤F_Q(B)≤OPT_m`。对当前含 x 的槽 i，令 `ell_i=F_Q(B)-F_Q(B^{-i})`、`e_i=u_i-ell_i`。其逐客户展开为

| 条件（始终 x∈B_i） | e_i(B;x) |
| --- | ---: |
| x∉O，或 i=o(x) | 0 |
| i≠o(x)，owner 槽覆盖 x | 1/c_x(B) |
| i≠o(x)，owner 槽不覆盖 x | 1/(c_x(B)+1) |

这些是旧 UNIT 身份；来源为 `R-cd789330fc7141299ac491bbb3ffa420/round3/shared/owner_exchange_potential.md` §§1–4。下文只加强该文 §5 的 first-owner 前提。

## 2. 任意 owner 仍给同一个 H_a−1 上界

对每个 i，令 Y_i 是任意满足

\[
(Y_i)_j=T_j\qquad(1\le j\le i)
\]

的 m 槽合法 profile。各 i 的后缀可以完全不同。特别地，可以取在原同一完整策略中强制 `T_1,...,T_i` 后的真实完成叶。

固定一个 `x∈O`。令含 x 的比较槽依次为 `i_1<...<i_a`，owner 是 `i_k`。则

\[
e_{i_\ell}(Y_{i_\ell};x)\le
\begin{cases}
1/(\ell+1),&\ell<k,\\
0,&\ell=k,\\
1/\ell,&\ell>k.
\end{cases}\tag{RANK}
\]

证明：若 `ell<k`，前缀已固定 ell 个覆盖者。若未来 owner 槽在该叶覆盖 x，它是另一个覆盖者，所以 `c≥ell+1`、误差 `1/c≤1/(ell+1)`；若 owner 槽不覆盖，误差为 `1/(c+1)≤1/(ell+1)`。若 `ell=k`，当前正是 owner，误差为零。若 `ell>k`，owner 已被强制覆盖 x，`c≥ell`，误差 `1/c≤1/ell`。

于是对任意 owner 秩 k，

\[
\boxed{\sum_{i:x\in T_i}e_i(Y_i;x)
\le\sum_{\ell<k}\frac1{\ell+1}
+\sum_{\ell>k}\frac1\ell
=H_a-1.}\tag{ANY-OWNER-REPEAT}
\]

这正是旧 first-owner 的数值预算，但不再要求 owner 为 first hit。它允许先为实际叶、Hall 路由或其它全局目标选 owner，再沿同一比较前缀使用该误差界。不能在不同叶各换一次 owner 后将不同 F_Q 望远镜；owner 仍须对整份推导固定一次。

branch_budget 的独立重构给出更短证明：对任何非owner查询，旧 INSERT 身份就是 `e_i(x)=1/(1+k_nonowner(Y_i))`。将 x 的 a−1 个非owner查询按时间排列，第 s 次时前缀已固定 s 个非owner覆盖者，故 `e_i≤1/(s+1)`；总和为 `H_a−1`。这个证明也说明该结论是旧一般 INSERT 的直接推论，而非新增一项后继理性或新动态预算。对应独审见 `../branch_budget/review_arbitrary_owner_harmonic_path.md`。

## 3. 随机排列与固定实际端点的 count-only 平均势

若 T 最优，先均匀随机排列其 m 个带索引槽；再对每个客户 x，在含 x 的最优索引中均匀选择一个为 owner。每个 x 的 owner 位置边际均匀分布于 `[m]`。因此对**不依赖这些随机源的固定 profile B**，逐客户平均得到

\[
\boxed{\mathbb E F_Q(B)
=\bar F(B):=
\sum_{x\in O}\frac{(m+1)c_x(B)}{m(c_x(B)+1)}
+\sum_{x\notin O}H_{c_x(B)}
\le\operatorname{OPT}_m.}\tag{SYM}
\]

例如 c=0 时 O 内贡献为零；c>0 时 owner 在 B 覆盖槽的概率为 c/m，故其平均贡献为 `1−(1−c/m)/(c+1)`。上界通过逐实现旧 POT 再取期望得到。

对固定 B 的同叶误差总和还有

\[
\boxed{\mathbb E\sum_i e_i(B)
=\sum_{\substack{x\in O\\c_x(B)>0}}
\frac{m c_x(B)-1}{m(c_x(B)+1)}.}\tag{SYM-ERR}
\]

所有随机实现都保留 §2 的 ANY-OWNER-REPEAT。**但中间真实 Y_i 会依赖比较排列，不能在那里将条件 owner 平均偷换成 SYM 的无条件 count-only 公式。** SYM 当前只合法规范化固定实际初端点，或作为独立的静态势上界。

若直接把 bar F 当同一个固定势使用，它的 O 内单位边际为 `(m+1)/[m c(c+1)]`，误差为 `(mc−1)/[m c(c+1)]`。其沿比较前缀的直接误差界是

\[
\sum_{i:x\in T_i}\bar e_i(Y_i;x)
\le H_a-\frac{(m+1)a}{m(a+1)}
=H_a-1+\frac{m-a}{m(a+1)}.
\]

这里 m≥2 时误差随正整数 c 非增，因为相邻差是 `(mc−2)/[m c(c+1)(c+2)]≥0`；m=1 直接为零。这个较松界与 `bar F(T)` 距 |O| 的端点缺额对应，不能把较紧 ANY-OWNER-REPEAT 免费赋给 bar F。

## 4. 接到一般 half 的实际位置与仍缺的付款

本项放松旧 first-owner 条件，使全局 owner 可以为实际终局容量或随机端点均衡而选择，而不增加真实最优前缀的查询重复误差。它没有支付规定叶之间的去槽势差，也不把互斥离轨叶的总利润替成原实际 W。特别地，误差上界出现在某项负号时，不能用上界当作有利扣除量。

Potential 同组代理已根据 UNIT 展开独立重构 RANK 与两个固定端点平均式；branch_budget 也独立通过任意 owner 推论并核对旧文范围。配套 `audit_arbitrary_owner_budget.py` 对 188302 个单客户前缀状态、1793 项任意 owner 预算与510项固定端点均值作确定性精确回归，全部通过；它仅校对公式，不是一般证明的依据。
