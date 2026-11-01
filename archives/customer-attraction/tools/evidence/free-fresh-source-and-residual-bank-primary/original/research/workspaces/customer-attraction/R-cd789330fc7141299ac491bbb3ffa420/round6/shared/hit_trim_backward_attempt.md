# 自由 fresh source 合同与 HIT 残余银行

2026-10-24，shared。本轮只作一次一般解析尝试，不扫描。自由source合同已由root独立重构认可；残余银行式直接由已审fresh HIT推出。**没有证明费用≤W，Q-CAG-HALF仍OPEN。**

## 1. 固定原目标，source组合不必继续最优

固定原实例、原完整SPE、实际覆盖C和W；原OPT数值始终不变。令M=max(OPT_m−W,0)。M=0时目标直接成立。否则可选任意合法m主题组合B，只要求

\[
F_B=(\bigcup_i B_i)\setminus C,\qquad |F_B|\ge M.
\]

从F_B固定owner i使x∈B_i，再留ρ_x∈[0,1]、Σρ=M。所有source仍是actual前缀下的合法query，客户在实际前缀上负载零，合法INIT与自然fresh净图照用。若同一份方案付款≤W，就得到原M≤W及原OPT≤2W。

B不必仍是原最优元组；但绝不把目标改成新union大小−W。这里完全放弃Hall取消、η及SOURCE-NET，不另领取G信用。

精确地，从原最优T、并集O、R=O\\C、G=C\\O出发，以合法A替换T_j。令 \(E_j=T_j\setminus\bigcup_{k\ne j}T_k\)，则新fresh支持满足

\[
|R'|=|R|-|(E_j\cap R)\setminus A|
+|(A\setminus O)\setminus C|.
\]

因此可用删源余量是

\[
|R'|-M=|G|-|(E_j\cap R)\setminus A|
+|(A\setminus O)\setminus C|.
\]

非负时可重新留足M源；丢I本身不减少fresh支持。若净R损超过这**同一余量**，即使A是全局最大fresh主题也不能免费替换。多步替换须重算整个支持与同一个原M，不能每步重领原G；owner、价格和context输入也须共同重算。

## 2. 先扣 INIT current，再合账 captured 输入

固定一份source和trim。令α_i为role i在INIT的current精确吸收，b_t为INIT直接给natural context t的captured利润输入，B_j=Σ_(i(t)=j)b_t，H=ΣB_j。守恒给

\[
M=\sum_i\alpha_i+H.
\]

每role只有一个source主题B_i，故α_i≤D_i(B_i)≤u_i。先从原实际u_i扣α_i，留下u_i−α_i≥0；这不是旧η/SOURCE预付。

在固定fresh-only净图中，没有past终点，终端角色不早于输入context角色。对目标角色集K，记k_j=|K∩{j+1,…,m}|。从j∉K的输入最终进入K的比例至多k_j/(k_j+1)，从j∈K只用≤1。由[全图HIT](../relay/global_role_coupon_hitting.md)线性合账：

\[
A(K)\le\alpha(K)+B(K)+
\sum_{j\notin K}\frac{k_j}{k_j+1}B_j.
\tag{RESIDUAL-HIT}
\]

特别是

\[
A_i\le\alpha_i+B_i+\frac12\sum_{j<i}B_j.
\]

因此若能共同选择source/trim/输入，使

\[
B_i+\frac12\sum_{j<i}B_j\le u_i-\alpha_i
\quad(\text{全部 }i),\tag{BANK?}
\]

则同一实际钱包可全付。**本文没有证明BANK?总可实现。**

允许按rank密度账§6保持INIT current吸收不变，将captured总量任意分给该真实叶的future coverers，并进入其合法natural contexts，从而共同选择B_j。此时不再使用旧owner层面的INIT-HIT；只在选定b_t后的fresh净图上使用HIT，故RESIDUAL-HIT仍成立。β与所有券须按这份输入重算。

## 3. 停界

last原BR给每个合法主题的fresh大小≤u_m，但没有控制多个互斥source叶共同造成的B_m。自由source域移除了“新组合必须仍最优”的额外限制，却未证明能同时保足M源并满足残余银行容量。此处未新增一般福利上界，不把HIT上包络当actual券cap，也没有使用priority-world事后删源。
