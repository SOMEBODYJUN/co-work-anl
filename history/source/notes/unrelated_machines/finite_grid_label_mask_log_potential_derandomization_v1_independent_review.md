# 有限格点 label mask 对数势：独立 Exact-only 重构

Reviewer：bicriteria_set_packing_bridge，2026-10-18。仅据指定 statement-only Exact 推导，未读作者 Proof、其它新推导或 root 策略。只在 clone 外 scratch 新冻，不修改 repo、Git、Work 或旧文件。

实际全文读取的唯一作者文件：

`/workspace/scratch/038d9dcc4cac/finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md`

SHA256 `b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165`。

结论：**PASS。纯 Exact 的确定性 ε-加性条件期望构造、总位多项式界及附加全局资源不交结论均成立，未发现 fatal。** 时间必须按 Q 的数值收费；本记录不把它升级为任意巨大 binary Q 的位多项式，也不认证任何 NSW 或其它下游完整 Claim。以下为自足证明，不运行数值实验。

## 1. 精确对象与两个空分支

U 是显式 m-item set，agents 是显式 [a]，L>=1。每 item 的 labels 0,...,L 有非负 rational probabilities π_(j,t)，和恰为1，items之间独立。每 agent i 的 target t_i∈[L]、S_i⊆U、正 binary rationals V_i、ν_i，以及非负 w_(i,j)，满足各权是1/Q整数倍且总和<=1，Q是正整数。没有正weight或非空 S_i 的额外要求。

令 h_(i,j)=Q w_(i,j)，j不在S_i时令h=0。它是非负整数，且Σ_j h_(i,j)<=Q。因此所有完整或条件化的质量取值都在 {0,1/Q,...,1}，整数索引0,...,Q，而不是由数值小的ν或π决定的格点。

若 m=0，返回空assignment。各W_i=0为确定常数，Φ与其期望完全相等；无需计算任何log，所有S_i亦必为空。若 a=0，每item从其显式概率表中确定性找第一个π>0的label，返回该完整assignment；Φ=0与期望相等。两者可同时为空。正概率label存在于每item，因为概率和为1。以下只讨论 m>=1、a>=1，不在空分支除以m或a。

所有ν_i>0，所以ν_i+W_i始终正，semantic logs有限。V_i>0保证完整Φ语义合法。即使ν或正概率极小，也不以它们的数值倒数为运行长度。

## 2. 去掉 label-independent 常数

定义

\[
f_i(k)=-\ln(\nu_i+k/Q),\qquad 0\le k\le Q,
\]

\[
\Psi(r)=\sum_i f_i\left(\sum_jh_{i,j}\mathbf1[r_j=t_i]\right).
\]

则Φ(r)=Σ_i ln V_i+Ψ(r)。因此只需给Ψ的保证Ψ(r)<=EΨ+ε，再加回同一个数学常数即可得到所求Φ不等式。算法不必近似ln V_i、不必表示该常数或EΦ。该化简也说明V_i不能通过改变label choice给任何额外难度。

取误差尺度

\[
\alpha=\frac{\epsilon}{2am}>0.
\tag{1}
\]

对每个i和k=0,...,Q，预计算一个 rational \(\widehat f_i(k)\)，保证

\[
|\widehat f_i(k)-f_i(k)|\le\alpha.
\tag{2}
\]

这些近似的确定性位复杂度将在§5自足证明。可以全表预计算，共a(Q+1)个值；不按1/α创建格点。

## 3. 任意正概率 prefix 的精确格点 probability DP

按显式items顺序逐项决定labels。固定一个已选prefix，每个已选label均有正输入概率，因此prefix的事件概率严格正，conditional expectation语义存在。因为原items独立，给定prefix后，未决items仍相互独立且保持原π，不需除以prefix概率。

agent i 在prefix已取得的整数质量记为b_i。对未决item集合J，剩余整数质量是

\[
Z_i=\sum_{j\in J}h_{i,j}X_{i,j},\qquad
\Pr[X_{i,j}=1]=\pi_{j,t_i}.
\]

对固定i，items间的X独立；无需不同agents之间独立。概率生成多项式为

\[
\prod_{j\in J}\bigl((1-\pi_{j,t_i})+\pi_{j,t_i}z^{h_{i,j}}\bigr).
\tag{3}
\]

次数<=Q，系数非负、总和1，给出Pr[Z_i=k]，k=0,...,Q。以长度Q+1数组、按每个item的0/h平移递推计算，O(mQ)个rational运算足够。h=0的item只乘常数1，π=0或1均自然包含；不要求它们严格介于0与1。总h<=Q确保b_i+Z_i从不超过Q，不发生截断真实质量的问题。

为明确bitlength，可写π_(j,t_i)=P_j/D_j，0<=P_j<=D_j。用integer coefficient数组和共同分母维护式(3)：加入一个item时

\[
N'_k=(D_j-P_j)N_k+P_jN_{k-h_{i,j}},\qquad D'=D\cdot D_j,
\tag{4}
\]

越界系数为0。每一步Σ_kN_k=D，故每个非负N_k<=D，其bitlength<=Σ_j bitlength(D_j)+O(1)，受实际概率输入总位长控制。这避免用naive未约分fraction表达式的实现细节掩盖巨大分母；即使正π极小，仍只有其编码位长，不按1/π数值循环。

设下一个item为j，并尝试任一有π_(j,t)>0的label t。将它视为已固定，再对剩余items使用上面的DP。对agent i的base改成 `b_i+h_(i,j)`（t=t_i时），否则仍b_i。得到这一child prefix的semantic条件期望

\[
F_t=\mathbb E[\Psi\mid\text{prefix},r_j=t].
\]

用同一概率DP与表(2)求rational

\[
\widehat F_t=\sum_i\sum_k\Pr[Z_i=k]\widehat f_i(b_i+\mathbf1[t=t_i]h_{i,j}+k).
\tag{5}
\]

式(5)只对DP实际support中的k求和；任何零概率项直接省略。其base+k始终<=Q，因此不访问表外的log值，也不把0乘未定义表项。

DP确有总概率1，各agent误差<=α，故

\[
|\widehat F_t-F_t|\le a\alpha.
\tag{6}
\]

不必计算一般irrational的F_t或parent期望。remaining DP对不同candidate t仅base不同，可以复用；即使每个candidate重算也仍为所需多项式。

## 4. 正概率 label 决策与全局 ε 误差

算法只在π_(j,t)>0的labels中选择 \(\widehat F_t\) 最小者，ties按input order确定。因此返回的每个item label都有正输入概率。zero概率labels不纳入argmin，也没有把极小正probability按近似阈值误判为零。

记parent conditional expectation为F。由items独立与全期望公式，

\[
F=\sum_{t:\pi_{j,t}>0}\pi_{j,t}F_t.
\]

因此存在一个positive-probability label t*满足F_(t*)<=F。若算法取t_hat，式(6)给

\[
F_{\widehat t}
\le\widehat F_{\widehat t}+a\alpha
\le\widehat F_{t^*}+a\alpha
\le F_{t^*}+2a\alpha
\le F+2a\alpha.
\tag{7}
\]

这里不依赖child概率下界；每一步加性误差没有除以π或prefix概率。经过m步，terminal conditional expectation就是实际Ψ(r)，所以

\[
\Psi(r)\le\mathbb E\Psi+2am\alpha=\mathbb E\Psi+\epsilon.
\]

加回§2的label-independent常数得到Φ(r)<=EΦ+ε。所有计算可使用rational比较；近似ties不需对irrational logs精确判等。算法只返回一个完整r，同一个item未被各agent独立重抽或分别组装。

## 5. 对 positive binary rational log 的自足高精度算法

为免把任意小ν转化为1/ν循环，证明输入positive rational x的ln x能以对input bits与log(1+1/α)多项式的时间近似到absolute error α。

用integer bitlength和精确比较找h∈Z，使

\[
x=2^h y,\qquad1\le y<2.
\]

若x分子分母总位长为B，则|h|=O(B)，y仍有poly(B)位。可先由分子/分母位长差给h的常数范围候选，再比较，不需按x数值循环。

对y设z=(y−1)/(y+1)，0<=z<1/3。标准幂级数可直接由等比级数积分得到

\[
\ln y=2\sum_{n=0}^{\infty}\frac{z^{2n+1}}{2n+1}.
\tag{8}
\]

ln2用z=1/3的同一展开。取前N项，剩余绝对值<=

\[
2\sum_{n=N}^{\infty}z^{2n+1}
\le\frac34\,9^{-N}\le9^{-N}.
\tag{9}
\]

对lnx=hln2+lny采用这两个rational截断，误差<=(|h|+1)9^(−N)。确定性选择最小N>=1使9^N>=(|h|+1)/α即可；只需integer/rational比较。它的大小为

\[
N=O\bigl(1+\log(B+1)+\log(1+1/\alpha)\bigr).
\]

截断值由rational幂、整数2n+1的倒数和有限求和计算。rational powers的分子分母位长O(NB)，逐项共同分母的位长至多各项位长之和，为poly(B,N)；故精确计算截断和为总位多项式。h为负也只改变ln2项符号，absolute误差界用|h|照样成立。x=1时y1,z0、h0无需特殊数值近似；其余小/大x经range reduction统一处理。

代入x=ν_i+k/Q，其rational位长由ν输入与logQ多项式控制，严格正，包括k0。取负号即表(2)。若α>1，同一N比较照样合法，不强制生成1/α个对象。由α=ε/(2am)，

\[
\log(1+1/\alpha)\le O(1+\log a+\log m+\log(1+1/\epsilon)).
\]

因此precision只按所需bits收费，不按1/ε的数值收费。ε自身是输入positive binary rational，其编码位长也计入explicit input。

## 6. 整体 bit complexity 与 Q 的准确收费

设N为全部显式输入总位长，包括U、agents、labels/probabilities、S、weights、V、ν、Q和ε。读取、核查grid整数h及总量<=Q均是binary有理/整数运算；有效域的Q为正，不把int multiples输入误当任意real weights。

预计算a(Q+1)个log近似，每项的bitlength与时间由§5给poly(N,log(1+1/ε),logQ,log a,log m)。条件DP的integer probabilities由§3保持poly(N)位；将它们与有限rational log近似相乘、按至多a(Q+1)项求和，位长为poly(N,a,Q,log(1+1/ε))。可为每step每candidate从头计算，使用粗上界O(a m²(L+1)Q)个rational/整数运算即可，另加log表构造；各运算的operand bitlength为上述多项式。索引输出m个label、每个O(log(L+1))位，长度也多项式。

由此总体时间为explicit input length、a、m、L、Q及log(1+1/ε)的固定多项式。Q确按其**数值**收费；若Q任意巨大而只有logQ位输入，此为pseudo-polynomial grid DP，不是统一bit-polynomial。任务给定的应用Q=4m、m>=1时Q随显式m线性，因此自动成为真正总输入位多项式。m0已由§1直接处理，不把Q=4m=0与本合同Q正整数混用。

极小正π、ν、ε分别只贡献其编码位长或logprecision；不产生隐藏1/π、1/ν、1/ε展开。所有remaining Bernoulli DP采用独立items，agents间可能高度相关不会影响linear sum的条件期望求值。没有随机输出、额外sampling、oracle期待值或未知最优解输入。

## 7. 物理 allocation 的真正跨 ALL agents 不交

本附加结论严格依赖Exact的额外前提：每个fixed target label t∈[L]，具有t_i=t的S_i集合两两不交。对同一个完整r定义T_i={j∈S_i:r_j=t_i}。

假设某实际item j同时在T_i与T_h，i!=h。则同一个r_j必须同时等于t_i和t_h，因而t_i=t_h；且j∈S_i∩S_h，违反该fixed-label类内S pairwise-disjoint前提。因此T_i跨全部agents pairwise-disjoint。不同targets靠同一item只选一个label排除冲突，相同targets靠额外set条件排除冲突。

证明包括zero weight items（T_i按S和label定义，不先删zero weight）、空S_i、m0/a0，并且没有给agents各自独立生成一份r或复制items。label0不会等于任何t_i，可自然代表不分给任何agent。若没有该额外fixed-label disjoint前提，纯potential保证本身不推出physical disjoint；本记录没有把它扩成无条件结论。

## 8. Scope 与独立记录身份

本审查仅认证有限grid、任意显式independent item-label probabilities、norm-bounded weights与positive log offsets下的纯ε-加性derandomization合同，以及其明确额外条件下的全局资源不交推论。它不是对NSW、其它objective、完整下游随机mask归约、source困难性或general UM的认证；下游若采用此工具仍须独立验证这些输入前提、Q=4m和各ν/权/label边际的真实来源。

本 reviewer没有读取作者Proof、其它新推导或root策略，也没有运行finite numerics、实现或软件测试。该Exact-only记录及原statement SHA应保留；未来作者读后或canonical scope审查另冻，不覆盖本次先行独立记录。
