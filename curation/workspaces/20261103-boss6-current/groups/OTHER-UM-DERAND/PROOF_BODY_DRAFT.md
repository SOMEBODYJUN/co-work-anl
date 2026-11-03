# 模型与结论

设 \(U=\{j_1,\ldots,j_m\}\) 为显式有限 item 集，agent 集为 \([a]\)，\(m,a\ge0\)。标签为 \(\{0,\ldots,L\}\)，\(L\ge1\)；输入逐项给出非负二进制有理概率 \(\pi_{j,t}\)，每项各标签概率之和为一，随机标签 \(R_j\) 在不同 item 间独立。每个 agent \(i\) 有目标标签 \(t_i\in\{1,\ldots,L\}\)、集合 \(S_i\subseteq U\)、正二进制有理数 \(V_i,\nu_i\) 和非负权 \(w_{i,j}\)。给定正整数 \(Q\)，要求各权是 \(1/Q\) 的整数倍，且 \(\sum_{j\in S_i}w_{i,j}\le1\)；在 \(S_i\) 外令权为零。允许空集合、零权、概率 \(0/1\) 和不同 agent 的重复目标标签。对完整赋值 \(r\)，令

\[
W_i(r)=\sum_{j\in S_i}w_{i,j}\mathbf1[r_j=t_i],
\qquad
\Phi(r)=\sum_{i=1}^{a}\ln\frac{V_i}{\nu_i+W_i(r)}.
\]

对每个给定正有理 \(\varepsilon\)，有确定性算法返回同一组实际 items 的一个完整标签赋值 \(r\)，只选 \(\pi_{j,r_j}>0\) 的标签，且

\[
\Phi(r)\le\mathbb E[\Phi(R)]+\varepsilon.
\]

算法的总位复杂度为显式输入位长、\(a,m,L,Q\) 与 \(\log(1+1/\varepsilon)\) 的多项式；这里 \(Q\) 按**数值**收费。所有有效输入数据都是已给前件，本工具不求出这些概率、权或任何下游见证。以下势保证不要求集合不交；实物不交是后文额外前提下的结论。

若 \(m=0\)，返回空赋值，各 \(W_i=0\) 为常数；若 \(a=0\)，逐 item 取首个正概率标签，势恒为零。两支均有势与期望相等，不计算 \(\varepsilon/(2am)\)。以下令 \(m,a\ge1\)。

## 格点条件期望 DP

写 \(h_{i,j}=Qw_{i,j}\in\mathbb Z_{\ge0}\)，则每行 \(\sum_jh_{i,j}\le Q\)。去掉标签无关的常数 \(C=\sum_i\ln V_i\)，定义

\[
f_i(k)=-\ln(\nu_i+k/Q)\quad(0\le k\le Q),\qquad
\Psi(r)=\sum_i f_i\!\left(\sum_jh_{i,j}\mathbf1[r_j=t_i]\right).
\]

因此 \(\Phi=C+\Psi\)。取
\[
\alpha=\frac{\varepsilon}{2am},
\qquad
|\widehat f_i(k)-f_i(k)|\le\alpha,
\]
其中全部 \(\widehat f_i(k)\) 都是确定性预计算的有理数；其位长构造见下文。无需计算 \(C\)、真实势或一般无理的期望。

按输入顺序逐 item 固定标签。每次只选原概率严格正的标签，故每个已选 prefix 的事件概率严格正。由 item 独立性，条件于这个 prefix 后，未决 items 仍独立且保持原概率；不必除以 prefix 概率。记 agent \(i\) 已固定的整数质量为 \(b_i\)，未决集合为 \(J\)。剩余质量 \(Z_i\) 的概率生成多项式为

\[
\prod_{j\in J}\left((1-\pi_{j,t_i})+\pi_{j,t_i}z^{h_{i,j}}\right).
\]

它的次数不超过 \(Q\)。长度 \(Q+1\) 的数组从 \(N_0=1\)、其余为零、共同分母 \(D=1\) 开始。加入一个概率 \(\pi_{j,t_i}=P_j/D_j\) 的 item 时，用旧数组同时更新

\[
N'_k=(D_j-P_j)N_k+P_jN_{k-h_{i,j}},
\qquad D'=DD_j,
\]

越界旧系数按零处理。系数非负且总和恒为新共同分母，所以每个分子不超过 \(D'\)，分子及分母的位长至多为所用概率分母位长之和加常数。这给出精确有理概率，不按 \(1/\pi\) 展开。\(h=0\)、\(\pi=0/1\) 和空 \(J\) 都由同一递推覆盖；不同 agents 之间不需要独立。

设下一 item 为 \(j\)。对每个原概率 \(\pi_{j,t}>0\) 的候选标签 \(t\)，固定该标签，令
\[
b_i^{(t)}=b_i+\mathbf1[t=t_i]h_{i,j},
\]
再对 \(J\setminus\{j\}\) 做上述 DP，得剩余分布 \(q_{i,k}=\Pr[Z_i=k]\)。只对 \(q_{i,k}>0\) 的 support 求和：
\[
F_t=\mathbb E[\Psi\mid\text{prefix},R_j=t],\qquad
\widehat F_t=\sum_i\sum_{k:q_{i,k}>0}q_{i,k}\widehat f_i(b_i^{(t)}+k).
\]
行总量约束保证每个被访问的 \(b_i^{(t)}+k\le Q\)；不能为了零系数项访问表外索引。每个 agent 的概率总和为一，故
\[
|\widehat F_t-F_t|\le a\alpha.
\]

选择 \(\widehat F_t\) 最小的正概率标签，平局按固定输入顺序处理。记 parent 的真实条件期望为 \(F\)。全期望给出 \(F=\sum_{t:\pi_{j,t}>0}\pi_{j,t}F_t\)，故某个正概率 \(t^*\) 满足 \(F_{t^*}\le F\)。算法所取 \(\widehat t\) 满足
\[
F_{\widehat t}
\le\widehat F_{\widehat t}+a\alpha
\le\widehat F_{t^*}+a\alpha
\le F_{t^*}+2a\alpha
\le F+2a\alpha.
\]
这些比较都是有理估计的精确比较，不判定无理对数平局，也没有正概率下界假设。经过 \(m\) 次更新，terminal prefix 是实际输出 \(r\)，所以
\[
\Psi(r)\le\mathbb E[\Psi(R)]+2am\alpha
=\mathbb E[\Psi(R)]+\varepsilon.
\]
加回同一常数 \(C\) 得到所称势保证。保存逐步选中的标签即恢复完整输出，无需从各 agent 的边际分布分别拼装或重抽标签。

## 复杂度与物理不交边界

对数近似可直接用有理截断实现。对任意正有理 \(x\)，用位长及精确比较找整数 \(h\)，使 \(x=2^hy\)、\(1\le y<2\)。若 \(x\) 的分子分母共 \(B_x\) 位，则 \(|h|=O(B_x)\)，\(y\) 仍为多项式位长。设 \(z=(y-1)/(y+1)\in[0,1/3)\)，使用
\[
A_N(z)=2\sum_{n=0}^{N-1}\frac{z^{2n+1}}{2n+1},
\qquad
|\ln y-A_N(z)|\le\tfrac34\,9^{-N}\le9^{-N}.
\]
\(\ln2\) 使用同式的 \(z=1/3\)。于是 \(hA_N(1/3)+A_N(z)\) 对 \(\ln x\) 的误差至多 \((|h|+1)9^{-N}\)。以整数/有理比较选 \(N\ge1\) 使该值不超过 \(\alpha\)，只需
\[
N=O\!\left(1+\log(B_x+1)+\log(1+1/\alpha)\right)
\]
项。每项有理幂、分母 \(2n+1\) 和有限求和的位长均为 \(B_x,N\) 的多项式。代入 \(x=\nu_i+k/Q>0\) 并取负号，得到全表 \(\widehat f_i(k)\)；包括 \(k=0\)、极小 \(\nu_i\)、负 \(h\) 或 \(\alpha>1\)。不按 \(1/\nu_i\) 或 \(1/\varepsilon\) 数值循环。

共有 \(a(Q+1)\) 个表值。每个候选重算剩余 DP 的粗运算数也只有 \(O(am^2(L+1)(Q+1))\)。共同分母控制 DP 位长；有限有理表值相乘求和、比较仍保持总位多项式，且
\[
\log(1+1/\alpha)=O\!\left(1+\log a+\log m+\log(1+1/\varepsilon)\right).
\]
所以以上确为所称总位复杂度。巨大二进制 \(Q\) 下只有伪多项式保证；只有另已验证的 \(Q=4m\)、\(m\ge1\) 应用前件才把 \(Q\) 数值变为显式输入规模的多项式。空 item 分支不把 \(Q=4m=0\) 填入要求 \(Q>0\) 的常规合同。本文没有软件实现或运行认证。

若额外给定：每个固定目标标签 \(t\in\{1,\ldots,L\}\) 的集合族 \(\{S_i:t_i=t\}\) 两两不交，则
\[
T_i=\{j\in S_i:r_j=t_i\}
\]
跨全部 agents 两两不交。否则某实际 item 同时属于 \(T_i,T_h\)，其唯一全局标签迫使 \(t_i=t_h\)，而 \(j\in S_i\cap S_h\) 违反同标签类内不交。该证明包括零权 item；标签 \(0\) 不归任何 agent。没有附加不交前提，势保证本身不推出实物不交，也不能复制 items 或为各 agent 独立选择标签。

## 版本与证据层级

statement-only 源给合同；author-proof 展开 DP、误差和位复杂度；先行 independent-review 与读后 author-proof-read-after 在同一明确域内核对。原四源字节及 SHA 保留在证据 manifest，具体角色顺序见[独立核验与范围审查](../审查/有限格点标签势去随机化独立核验--审查.md)。本页恢复这些成熟论证，不另计新定理或新实现。

本对象不声称 NSW 常数、福利舍入、一般 unrelated-machines 近二算法、source hardness、六人纯 SPE 或 Q-CAG-HALF。下游必须另证给定数据确满足本页全部输入前件、\(Q\) 的实际数值及所需标签类不交条件；工具不生成或认证未给定的下游见证。
