# 四源共同 X 隐藏尾：独立数学来源审计

Boss1；RUN `six-boss1-20261111`；审计席 `early_shared_x_source_audit`。

## 1. 审计结论与准确命题

**来源审计通过。** 四个 actual source 共用一次选定的全目录最大标签 X，分别保存真实强制 X 后继的方案，是原完整有序历史纯 SPE 模型的必要层。所交付的 **1920 个非负隐藏变量、128 条质量等式、436 条不等式** 的历史、钱包、分母与查询范围均有下述独立推导。没有发现把 actual 收益搬到离轨分支、把索引均值误当行动、把不同 X 分支的未知交叠当作已知，或逐客户重新选择最大者的错误。

这里审计的是如下命题：对任意原模型实例、任意一份完整纯 SPE、任意一次选定的 actual 前四背景全目录最大标签 X，真实客户分组产生的隐藏变量满足本页全部通用行。具体 `symbolic_append.json.gz` 只把这些公式限制到旧核心给定的 16 个 hist；所以其必要性是**对于旧投影位于该支持的实例**。此矩阵不表示所有任意客户类型的 SPE，也不是充分条件。零客户实例单独平凡成立，不放进总质量为 1 的归一化矩阵。

本审计重读原模型、原 MX/RC owner、原 PAIR owner，以及当前未改写的前缀最大标签证明；未把 builder 的测试通过或本轮数值点作为数学来源。没有读取点权重、运行优化器、修改 Git/RUN/registry 或他人文件。本包不重复 builder 已承担的 1920 列逐系数审计。

## 2. 原模型、共同选择与完整有序历史

原定义是有限单位客户集 N、有限非空共同**标签**目录 L、任意覆盖映射，以及六位提供者的完整纯策略

\[
\sigma_j:\mathcal L^{j-1}\longrightarrow\mathcal L.
\]

每个有序历史、每个合法偏离都按同一份 \(\sigma\) 的真实后继比较。原终局收益是客户价值在全部覆盖者间均分；给定客户的终局覆盖位为 \(a_1,\ldots,a_6\)，则 actual 第 j 人贡献是

\[
u_j(c)=\begin{cases}a_j/\sum_{k=1}^6a_k,&a_j=1,\\0,&a_j=0.\end{cases}
\]

分子为零的客户不执行除法。令 actual 标签为 \(A_1,\ldots,A_6\)，并定义

\[
b_i(c)=\sum_{j<i}a_j(c),\qquad
P(c)=\sum_{j=1}^4a_j(c),\qquad
f_P(Q)=\sum_c\frac{q_c}{P(c)+1}.
\]

目录有限非空，故可以先固定一次

\[
X\in\arg\max_{Q\in\mathcal L}f_P(Q),\qquad F_X=f_P(X).
\tag{X}
\]

这个 X 不随 source、客户、hist、查询 Q 或离轨背景改变。它不必在较早 source 的背景下最大，也不必是较早玩家的均衡选择。

对 \(i=1,2,3,4\)，置 \(r_i=7-i\)、\(m_i=5-i=r_i-2\)。只在原 actual 历史 \(h_i=(A_1,\ldots,A_{i-1})\) 强制第 i 人选 X，之后沿原策略递归得到

\[
Y_{i,1},\ldots,Y_{i,m_i},T_i^*.
\tag{B}
\]

这里 \(Y_{i,m_i}\) 总是第五位的真实选择，\(T_i^*\) 总是第六位的真实选择。\(T_i^*\) 与原六元比较菜单的 \(T_k\) 不同，代码名是 `T_at_sourcei`。

| source | 最后两位前的真实有序历史 | 真实末位前的有序历史 |
|---:|---|---|
| 1 | \((X,Y_{1,1},Y_{1,2},Y_{1,3})\) | 再接 \(Y_{1,4}\) |
| 2 | \((A_1,X,Y_{2,1},Y_{2,2})\) | 再接 \(Y_{2,3}\) |
| 3 | \((A_1,A_2,X,Y_{3,1})\) | 再接 \(Y_{3,2}\) |
| 4 | \((A_1,A_2,A_3,X)\) | 再接 \(Y_{4,1}\) |

每个左列历史长度恰为四，右列长度恰为五。即使强制 X 的最初动作在该节点不是最优，之后各玩家仍在原策略规定的真实子博弈中行动；完整 SPE 正是保证这些离轨节点的 IC 仍成立的量词。

承重原定义：[共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)。同一 X 可同时用于较早源的直接证明也见 [main_prefix_safety_maxx_family.md](main_prefix_safety_maxx_family.md) §1、§2、§4；本页不依赖正在升级的 formal-prefix 登记正文。

## 3. 直方图、原词序和真实隐藏测度

原六元菜单的三个词位是

\[
(t_k,b_k,c_k)=\bigl(1_{T_k},1_{B_k},1_{C_k}\bigr),
\]

其中 \(B_k=\sigma_5(A_1,A_2,A_3,T_k)\)，\(C_k=\sigma_6(A_1,A_2,A_3,T_k,B_k)\)。原 `fourth_indexed_projection.py` 的 `PATTERNS=product((0,1),repeat=3)` 与 `new_reply_budget.py` 的 `(t,b,c)` 拆包共同给定顺序

`000,001,010,011,100,101,110,111`。

若 hist 的八桶数记作 \(n_{000},\ldots,n_{111}\)，则

\[
\begin{aligned}
d_T&=n_{100}+n_{101}+n_{110}+n_{111},\\
d_B&=n_{010}+n_{011}+n_{110}+n_{111},\\
d_C&=n_{001}+n_{011}+n_{101}+n_{111}.
\end{aligned}
\tag{W}
\]

这是按字面六索引计数，不依赖任何会员独立性。actual 位与这八桶共同定义旧 hist h；\(H_h\) 是其客户质量，\(x_h\) 是该类内属于**同一个** X 的质量。

对 source i，按该客户的 \((h,x,y_1,\ldots,y_{m_i},t)\) 分组，定义真实非负质量

\[
\mu_{i,h,x,y_1,\ldots,y_{m_i},t}.
\]

单位客户时它是整数计数；统一正缩放后是同比例质量。直接按分组定义，有

\[
\sum_{y,t}\mu_{i,h,1,y,t}=x_h,\qquad
\sum_{y,t}\mu_{i,h,0,y,t}=H_h-x_h.
\tag{M}
\]

因此每个 source/hist 恰两条等式，四源共享原来的 x 列，没有另建四个可分别选择的 X。每 hist 的状态数是 \(2^{m_i+2}\)，依次为 64、32、16、8；16 个 hist 给 \(16(64+32+16+8)=1920\) 个非负变量，\(4\cdot16\cdot2=128\) 条等式。

可以在每个正质量 \((h,x)\) 单元上用条件乘积把四份边缘扩成一个抽象测度；质量 M 为零时四份边缘都为零。这只是边缘测度的兼容。它没有证明目录标签身份、原 R/Z 联合律或全部历史策略兼容；下文从未用这个条件乘积计算真实的跨分支交叠。

## 4. 从终局均分直接重建三个分支收益

固定 source i 的一个客户，简写 \(b=b_i(c)\)、\(x=1_X\)、\(y=(y_1,\ldots,y_m)\)、\(t=1_{T_i^*}\)。强制分支的真实总负载是

\[
b+x+\sum_{\ell=1}^m y_\ell+t.
\]

所以 source i 的偏离收益贡献、该分支末位收益贡献、该分支第五位收益贡献，分别由原均分定义给出

\[
v_i(c)=\frac{x}{b+1+\sum_\ell y_\ell+t},\qquad
w_i(c)=\frac{t}{b+x+\sum_\ell y_\ell+1},
\tag{S1}
\]

\[
s_i(c)=\frac{z}{b+x+\sum_{\ell<m}y_\ell+1+t},\qquad z=y_m.
\tag{S2}
\]

这些式子中把自己的位换成 1，只在分子包含该位时进行：位为 1 时分母等于真实总负载，位为 0 时整个项为零。故它们没有对零覆盖执行 0/0。

令

\[
p_i(c)=b_i(c)+x_c+\sum_{\ell<m_i}y_{i,\ell}(c),\qquad d_i(c)=p_i(c)+1.
\tag{P*}
\]

这是表中真实四步历史留下的负载，因此 \(0\le p_i\le4\)、\(1\le d_i\le5\)。它通常不同于 actual P。\(s_i,w_i\) 都从 source i 的 \(\mu_i\) 求和，决不能用 actual 的 \(u_5,u_6\) 替代。

### 4.1 四条原 source IC

在原 actual 源 \(h_i\)，完整策略的偏离比较直接给

\[
u_i-\sum\mu_i\frac{x}{b_i+1+\sum y+t}\ge0.
\tag{IC}
\]

这里只支付原 source i 自己的收益；没有把它再充作任意后继玩家的钱包。四条 source-IC 对应 \(i=1,2,3,4\)。

### 4.2 全六个 actual source 对 14 个尾标签角色的 SAFE

这四条分支共产生 \(5+4+3+2=14\) 个**命名标签角色**，不假设它们是 14 个互异目录标签。取其中任意 Q，任意 actual source \(j=1,\ldots,6\)，在 \((A_1,\ldots,A_{j-1})\) 真改 Q 后，令该玩家的真实收益为 \(V_{j,Q}\)。在属于 Q 的客户处，之后至多 \(6-j\) 人继续覆盖，因此

\[
V_{j,Q}\ge\sum_c\frac{q_c}{b_j(c)+7-j}.
\]

于是

\[
u_j-\sum_c\frac{q_c}{b_j(c)+7-j}
=\underbrace{(u_j-V_{j,Q})}_{\text{该原源真实 IC}}
+\underbrace{\left(V_{j,Q}-\sum_c\frac{q_c}{b_j(c)+7-j}\right)}_{\text{逐客户非负份额差}}
\ge0.
\tag{SAFE}
\]

Q 的会员可以从产生它的 \(\mu_i\) 读取，但 \(V_{j,Q}\) 沿 source j 改 Q 后**自己的**真实后继计算，并不冻结 source i 的 X 分支。j=6 时没有后继，第二项恒为零，正好是实际末位对 Q 的真实查询。数量为 \(6\cdot14=84\)。

### 4.3 同一 P 的 MAX 与目录容量

由 (X)，每个尾标签角色 Q 都满足

\[
F_X-f_P(Q)=F_X-\sum\mu_i\frac{q}{P+1}\ge0.
\tag{MAX}
\]

定义 \(K\ge\max_{L\in\mathcal L}|\operatorname{cov}(L)|\)，使用旧核心同一尺度的 K 列，则

\[
K-|Q|=K-\sum\mu_i q\ge0.
\tag{CAP}
\]

各 14 条。MAX 的全客户和非负，不是每个客户的 \(x-q\) 非负；P 始终是原 actual 前四负载。

## 5. 真实末位 BR 与三组六索引均值

在 source i 的真实五步历史后，第六位选择 \(T_i^*\)。对任意合法 Q，末位 IC 与 (S1) 直接给

\[
\sum\mu_i\frac{t-q}{b_i+x+\sum y+1}\ge0.
\tag{BR}
\]

查询域是 X、六个 actual 标签、source i 的全部 m 个中间标签、三组原六索引菜单的平均。每源 \(1+6+m+3=10+m\) 条，四源为 \(14+13+12+11=50\)。末标签本身的自查询恒为零，不在这一域中额外计数。

均值的来源是六条合法纯查询 IC 以固定权 \(1/6\) 相加。分母只依赖无索引真实分支及该客户，故

\[
\frac16\sum_{k=1}^6\frac{t-q_k}{b_i+x+\sum y+1}
=\frac{t-d_Q(h)/6}{b_i+x+\sum y+1}.
\tag{AV1}
\]

这没有引入分数行动，也无需将 q 与 x、y 或 t 独立化。即使 X 恰与某个旧索引标签相同，式 (AV1) 仍是同一客户上的字面等式。

## 6. 真实末两人 TP 的完整付款与对角项

固定表中的真实四步前缀，记其背景为 p、\(d=p+1\)。对纯合法标签 L、R，定义

\[
f(L)=\sum_c\frac{l_c}{d_c},\qquad
g(L,R)=\sum_c\frac{l_cr_c}{d_c(d_c+1)}.
\]

由布尔会员位，均分收益满足

\[
U(L,R)=\sum_c\frac{l_c}{d_c+r_c}=f(L)-g(L,R).
\tag{U}
\]

令该前缀的真实第五、六位为 Z、T，收益分别为 \(s=U(Z,T)\)、\(w=U(T,Z)\)。第五位真改 L 后的真实末回复记为 \(J_L=\sigma_6(h,L)\)。逐项展开 (U)，得到

\[
\begin{aligned}
TP(L,R)&:=s+w+g(Z,Z)-f(L)-f(R)+g(L,R)\\
&=[s-U(L,J_L)]\\
&\quad+[U(J_L,L)-U(R,L)]\\
&\quad+[w-U(J_L,Z)]\\
&\quad+[g(Z,Z)-g(Z,J_L)]\ge0.
\end{aligned}
\tag{TP}
\]

前三项依次是该真实第五源的 IC、其改 L 后末位的 IC、该真实末位原节点对合法 \(J_L\) 的 IC。三项引用**同一个** \(J_L\)。最后项逐客户为

\[
\frac{z(1-j_L)}{d(d+1)}\ge0.
\]

前三个 IC 只在全客户求和后非负。本推导不要求强制 source i 的 X 动作最优，也不将 \(s,w\) 认作实际路径的 \(u_5,u_6\)。这与原 [跨族末两人菜单 PAIR owner](../../../archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md) 的三 IC 加 self-tax 差完全一致；[early3_pair_cone.md](early3_pair_cone.md) §4 提供相同正确历史的专门实例。

直接把 (S1)、(S2) 代回，局部钱包是

\[
\Psi=\frac{z}{d+t}+\frac{t}{d+z}+\frac{z}{d(d+1)}.
\]

所以三个保留的 TP 系数必须是

\[
\begin{array}{ll}
TP(Q,X):&\displaystyle\Psi-\frac{q+x}{d}+\frac{qx}{d(d+1)},\\[1ex]
TP(Q,Q):&\displaystyle\Psi-\frac{2q}{d}+\frac{q}{d(d+1)},\\[1ex]
TP(X,X):&\displaystyle\Psi-\frac{2x}{d}+\frac{x}{d(d+1)}.
\end{array}
\tag{TC}
\]

Q 的域为六个 actual、同源 m 个中间标签、三组旧菜单均值；另有一份 \(TP(X,X)\)。各源数量 \(2(6+m+3)+1\) 为 27、25、23、21，总计 96。

对于 indexed Q，\(TP(Q,Q)\) 是 \(\frac16\sum_kTP(Q_k,Q_k)\)。因此交叠使用

\[
\frac16\sum_kq_k^2=\frac16\sum_kq_k=\bar q,
\]

绝不是 \(\bar q^2\)。与固定 X 的交叠为 \(\frac16\sum_kxq_k=x\bar q\)。例如 \(d=3,\bar q=1/2\) 时，正确对角系数比使用 \(\bar q^2\) 大 \(1/48\)；这是实质系数差，当前生成器正确使用前者。

## 7. 实际第五源 MX 与 RC 的独立重建

现在回到原 actual 四步历史 \(h^a=(A_1,A_2,A_3,A_4)\)，背景为 P，钱包是原实际 \(u_5\)。定义

\[
g_P(L,R)=\sum_c\frac{l_cr_c}{(P_c+1)(P_c+2)},\qquad
U_P(L,R)=f_P(L)-g_P(L,R).
\]

### 7.1 共同 X 封顶，不是额外赠送一个收益

令 \(V=\sigma_6(h^a,X)\) 为实际第五源真改 X 后的末回复。对任意合法 Q，原份额代数给

\[
\begin{aligned}
u_5-U_P(Q,X)
={}&[u_5-U_P(X,V)]\\
&+[U_P(V,X)-U_P(Q,X)]\\
&+[F_X-f_P(V)]\ge0.
\end{aligned}
\tag{MX}
\]

第一项由实际第五源 IC 支付；第二项由真实偏离历史 \((h^a,X)\) 的末位 BR 支付；第三项由**全目录**最大性支付，V 也在该目录中。代数消项使用 \(g_P(X,V)=g_P(V,X)\)。这既重建了旧 owner 的最大主题特例，也验证了同一个 X 对全部 Q 同时封顶。

对十四个新尾角色 Q，\(U_P(Q,X)\) 的精确 μ 系数是

\[
\frac{q}{P+1}-\frac{qx}{(P+1)(P+2)}=\frac{q}{P+1+x}.
\tag{MC}
\]

所以 14 条 `actual-MX-cap` 的钱包确为 \(u_5\)，并非某个强制分支的第五位收益。这里不需要把 V 加作另一组显式变量：它只在普遍证明中出现并恰好消去。

### 7.2 RC 的实际钱包为 \(u_5+F_X\)

对任意纯合法 Q、R，令 \(V_Q=\sigma_6(h^a,Q)\)。仍从原份额展开，得到

\[
\begin{aligned}
u_5+F_X-f_P(Q)-f_P(R)+g_P(Q,R)
={}&[u_5-U_P(Q,V_Q)]\\
&+[U_P(V_Q,Q)-U_P(R,Q)]\\
&+[F_X-f_P(V_Q)]\ge0.
\end{aligned}
\tag{RC}
\]

这是两条真实 IC 加一条全目录 MAX。它没有使用实际 \(u_6\)，也没有 self-tax 钱包；与上一节 TP 的三个 IC 不可混账。原 [共同潜力上限 owner](../../../archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md) “共同目录 F 的全配对上限”节已经证明此式及 MX 特例；[terminal_response_cycles.md](terminal_response_cycles.md) §3.2 给出同一 X 的显式消项。本层复用该旧引理，不产生其新颖性主张。

在同一 source i 的 μ 中，任意两个尾角色 Q、R 的位 q、r 都已保存，故局部查询系数是

\[
-\frac{q+r}{P+1}+\frac{qr}{(P+1)(P+2)}.
\tag{RCc}
\]

同源尾角色的无序含自对数量为 \(\binom62+\binom52+\binom42+\binom32=15+10+6+3=34\)。自对的 \(q^2=q\) 自动保留。

另取每个新尾 Q 与六个 actual 标签或三组旧 indexed 平均 R 比较，共 \(14(6+3)=126\) 条。actual 位在 h 中固定；均值交叠按字面计数为

\[
\frac16\sum_k q r_k=q\frac{d_R(h)}6.
\tag{AV2}
\]

q 是 μ 单元内保存的无索引尾会员位，\(d_R(h)\) 是该客户旧词的已知计数。式 (AV2) 不是独立性假设，也不使用某个跨客户平均数代替该客户的计数。故 actual RC 总计 160 条。

来自不同强制 X 分支的两个新尾角色，一般需要尚未保存的真实联合位。当前包没有给它们添加 RC/PAIR 查询，也没有以条件乘积给出假交叠，这是正确的范围限制。

## 8. 标签别名、排序、零质量与完整量词

**标签角色可以重合。** 14 是角色数，不是要求目录新增 14 个互异行动。若 \(X=A_i\)，source i 的强制历史就是 actual 历史，其全部后继等于对应 actual 后继；若 source 4 的 \(X=T_k\)，则 \(Y_{4,1}=B_k\)、\(T_4^*=C_k\)。不同角色也可同标签、同覆盖或不同标签但同覆盖。真实实例自动满足所有相关等式。当前松弛没有显式编码所有条件别名，允许额外伪解；删掉这些兼容条件不会破坏必要性，却不允许声称得到完整可实现性。

**有序历史不按负载合并。** 表中的四步、五步前缀均保留原动作顺序。即使两条前缀负载相同，原策略仍可选不同后继。末位 BR 和 TP 只在各自指定历史上使用原策略。源间不得交换中间标签顺序来减少状态；μ 保留全部有序中间位。

**X 的选择不是逐客户最大化。** 式 (X) 在整份实例上选一个合法标签，其会员在所有 source 和 hist 中一致。旧六索引置换只是对查询表达式取平均，actual、X 与四条强制分支的标签保持固定；无需声称构造另一份对称 SPE。

**弱平局、空标签和零质量均保留。** 全部 IC 是非严格式；没有人为删除弱平局或要求唯一回复。份额分母是 1 至 6 的正整数，交叠税分母是相邻正整数的乘积；没有除以标签大小、收益、客户数或缺额。若 \(H_h=0\)，则旧 \(0\le x_h\le H_h\) 与 (M) 使四源对应的全部 μ 都为零，无需删列。当前包保留元数据中的六个零 hist 及其所有隐藏状态。

**固定支持不扩大论域。** 通用公式可对任意客户分型求和。具体 16-hist 矩阵只是其限制，旧投影落在别的 hist 上的实例没有被该有限矩阵表示。固定一个旧精确向量再验证隐藏层，仅审查该向量、该 X 边缘及其原辅助边缘的扩展；不可行不能自动排除重选 X 或重选旧边缘后的其他点，可行也不提供完整 SPE。

## 9. 数量、来源锚点与冻结

| 行族 | 独立计数 | 钱包 |
|---|---:|---|
| 原 source 改 X | 4 | 各自 actual \(u_i\) |
| 全六 actual source 的 SAFE | \(6\cdot14=84\) | 各自 actual \(u_j\) |
| 同一 P 的 MAX | 14 | \(F_X\) |
| 目录 CAP | 14 | K |
| actual MX 封顶 | 14 | actual \(u_5\) |
| 真分支末位 BR | \(14+13+12+11=50\) | 各自 \(w_i\) |
| 真分支最后两位 TP | \(27+25+23+21=96\) | 各自 \(s_i+w_i+g_i(Z_i,Z_i)\) |
| actual RC | \(34+126=160\) | actual \(u_5+F_X\) |
| 合计 | **436** | |

本页按原终局份额独立导出了 (S1)、(S2)、(SAFE)、(TC)、(MC)、(RCc)，并核对实际包的历史、查询 provenance 与计数。生成器已实现上述式子；未发现需改变矩阵的数学错误。对“14 个尾标签”仅提出更准确的角色/别名表述，builder 已获通知。

不变来源锚点：

| 来源 | SHA-256 |
|---|---|
| 原完整历史模型 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `main_prefix_safety_maxx_family.md` | `4d3f24e686ae38a8593b62abe1807249de6bd3884b428d52198180798ea73b81` |
| 原共同潜力 MX/RC owner | `f358a161eed5f02f243223bc590a41b3247834f842ab251060e380f5cd1fed39` |
| 原跨族末两人 PAIR owner | `8caa0131fc5a517bbdf8001a44bc00cc6741bb5255a35e413016e4a7319779ba` |
| 被审计 `symbolic_append.json.gz` | `1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0` |

具体来源文件、源码字节、查询域与独立结构核对记录保存在 [source_audit.json](early_shared_x_source_audit/source_audit.json)，本审计包的最终字节冻结在 [freeze_manifest.json](early_shared_x_source_audit/freeze_manifest.json)。所有新增写入限于本稿和同名目录；本数学来源义务完成后即释放，不等待云端或新的优化结果。
