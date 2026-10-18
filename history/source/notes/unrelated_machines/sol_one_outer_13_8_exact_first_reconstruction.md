# 单 outer normalized-flat 的 13/8：新 Exact-first 独立重构

审查者：`sol_general_repair`，2026-10-18。只读新输入
`one_outer_normalized_flat_13_8_approximation_exact_v2.md`，预期 SHA256
`81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69`。
没有索取 root/identity 的新证明，没有读取 `negative_hardness_work/`。
已知背景包括先前独立给定点重构419df...、其后实际读作者给定点ε²/4证明，以及
自己构造的 CDF-max welfare 后端。本记录不是无背景 blind；**新 welfare 常数、
未知阈值生成、13/8 数值界均在下文重新独立闭合**。旧 Exact/review/read-after 不改。

**结论：** 在新 Exact 的 typed explicit one-outer 域内，没有发现 fatal；可明确构造
单一确定性总位多项式算法，在 Q 上生成全部矩阵及 primitive-SA1 LP、输出每原 job
的合法 assignment，并保证 \(C_{\max}\le(13/8)\operatorname{OPT}(P(Q))\)。
下文用自己的 CDF-max 后端，不把旧作者 uniform-winner 的1/2证明升级为5/8。

## 1. 从 Q 生成完整物理对象与全部 LP 行

令 \(G,S,I,U\) 为原组数、indexed-state数、全部**列出**的incidence数及资源集，
其中 \(I\) 包括零 incidence。生成 \(S+|U|\) 台机器、\(G+I\) 枚 jobs：每 indexed
state 一 private root，每 resource 一 resource machine；每组一个 unit selector，
有限端是该组每个 root；每 incidence job 的有限端是自己的 private coefficient
及对应 resource 的一。其余全部 cells 置 \(\infty\)。直接生成稠密矩阵也只有
\((S+|U|)(G+I)\) 项，是显式 typed Q 长度的多项式。全部原零 jobs、未选 states、
重复 indexed states、unused resources 原样有各自实体。

记菜单实际最小质量最优值为 \(v=V(Q)\in[0,1]\)。完整矩阵满足

\[
\operatorname{OPT}(P(Q))=2-v\ge1.
\tag{1.1}
\]

上界由 selected state 导出所领正 incidences、其余全部留 private；下界在峰值
\(C<2\) 时用 unit resource 至多一 job及selected root须导出至少 \(2-C\) 正质量。
全 private、selector任选本组一个state给峰值至多二，包含 \(v=0\) 端点。该类非空
unit selectors 排除零 OPT；这不是一般空/零-OPT UM 的扩展结论。

对每 \(\epsilon=k/128\)，\(k=1,\ldots,128\)，实际生成如下有限 LP。原 primitives
是每 state 的 \(A_{gs}\) 和每原列出incidence的 \(Z_{gsu}\)，总数 \(N=S+I\)。变量
为一阶 \(\mu_i\) 与共同对称二阶 \(Y_{ij}\)，对角 \(Y_{ii}=\mu_i\)。基行逐字为
state partitions、全部 box、\(Z\le A\)、每资源 \(\sum Z\le1\)，及每state
\(\sum_up_{gsu}Z_{gsu}-\epsilon A_{gs}\ge0\)。

具体生成规则：对任一基行 \(a_0+\sum_i a_iX_i\ge0\)，列出原行及对每原
primitive \(X_t\) 的两行

\[
a_0\mu_t+\sum_i a_iY_{it}\ge0,\qquad
a_0(1-\mu_t)+\sum_i a_i(\mu_i-Y_{it})\ge0.
\tag{1.2}
\]

等式同样线性化为等式，或用两方向不等式；重复变量按对角合并。不添三阶项，
不替换成各自重算的条件点。变量数 \(O(N^2)\)，行数 \(O(N(N+|U|))\)，系数是
输入有理数与常数 \(k/128\) 的有限线性组合。标准确定性**有理 LP 算法**求其点或
不可行证书，是明确构造后的可计算子程序，不是向用户索取 point/CONFIG/SDP oracle。
box localizers 界住所有 \(\mu,Y\in[0,1]\)；有理可行时有多项式位长点，标准LP的
运行时间及返回点编码长度均按所构造LP总位长多项式。

若 \(\epsilon\le v\)，取实际达到菜单分配的 attaining states、其选中态所领正资源的
0/1 claims，并置 \(Y\) 为该0/1向量的乘积，得到本LP可行点。物理上所有未选态
incidences可留private总一，不需导出。故

\[
\epsilon\le v\quad\Longrightarrow\quad\text{所生成SA1 LP可行}.
\tag{1.3}
\]

不使用可行性的逆命题。独立求这128个固定阈值，保留最大 feasible grid value
\(\widehat\epsilon\) 及其返回点；如无正阈值可行，直接输出全private峰二排程。
128是算法常数，不是精度输入或按分母数值循环。若 \(v\ge1/128\)，由 (1.3)

\[
\widehat\epsilon\ge v-1/128.
\tag{1.4}
\]

无需求最优参数 LP、未知实际 v、参数代数根或精确 supremum。

## 2. 给定所生成点的一次条件化：welfare benchmark 至少 epsilon²

这里重新核前一给定点重构需要的全部条件。对 helper own singleton，记state
primitive \(h\)、唯一正claim \(z\)。value行 \(z\ge\epsilon h\) 乘 \(1-z\)，结合
box与gate给 \(\mu_h=\mu_z=Y_{hz}\)。再把 \(h-z\ge0\) 乘任一原 \(r,1-r\)，得
\(Y_{rh}=Y_{rz}\)。全是二阶；正 \(\epsilon\) 与原 claim 补乘子不可省。

选任何正 marginal 的 outer state \(a\)，条件一次 \(r=A_{M,a}\)。对本行 helpers
获得 fallback masses \(\alpha_{js}\)、claims \(\zeta_{jsu}\)，它们都是同一原
\(Y\) 的 \(r\) 行除以 \(\mu_r>0\)。记 \(\tau_j=\sum_s\alpha_{js}\)，outer home
claim为 \(b_j\)。原逐state value、gate、partition和resource行都乘该 \(r\)，给

\[
\begin{gathered}
\sum_jw_jb_j\ge\widehat\epsilon,\quad
\tau_j\ge b_j,\quad 0\le\tau_j\le1,\quad
0\le\zeta_{jsu}\le\alpha_{js},\\
\sum_up_{jsu}\zeta_{jsu}\ge\widehat\epsilon\alpha_{js},\qquad
\sum_{j\in J_a,s}\zeta_{jsu}\le1\quad(u\in B).
\end{gathered}
\tag{2.1}
\]

这里 home singleton equality负责 \(\tau_j\ge b_j\)，其余外行和零claim可用非负性
从条件容量中丢去；稍后它们恢复home。于是

\[
W_{\rm frac}=\sum_{j,s,u}w_jp_{jsu}\zeta_{jsu}
\ge\widehat\epsilon\sum_jw_j\tau_j\ge\widehat\epsilon^2.
\tag{2.2}
\]

## 3. 新后端常数5/8，确定性实现不计算无理常数

独立按 \(\alpha_{js}\) 选择 helper state，余概率选empty；选 \(s\) 后虚拟请求u的
概率为 \(\zeta_{jsu}/\alpha_{js}\)，\(\alpha=0\) 的state跳过。资源score是请求者的
\(w_jp_{jsu}\) 最大值。对一资源及score层d，helper j的超层概率为
\(\beta_j=\sum_{s:w_jp_{jsu}\ge d}\zeta_{jsu}\)，总 \(q=\sum_j\beta_j\le1\)。

**有限常数证明。** 有n个helpers时，AMGM给
\(\prod_j(1-\beta_j)\le(1-q/n)^n\)。\(1-(1-q/n)^n\) 在 \([0,1]\) 上凹，故不小于
\(q[1-(1-1/n)^n]\)。n=1时此括号一；n>=2时令m=n-1，二项式前四项给

\[
\left(1+\frac1m\right)^{m+1}
\ge1+\frac{m+1}{m}+\frac{m+1}{2m}
 +\frac{(m+1)(m-1)}{6m^2}
=\frac83+\frac{3}{2m}-\frac1{6m^2}\ge\frac83.
\]

所以 \((1-1/n)^n\le3/8\)，得到

\[
\Pr[\max\mathrm{score}\ge d]
=1-\prod_j(1-\beta_j)\ge\frac58q.
\tag{3.1}
\]

对有限分值层作离散积分，score总期望至少 \((5/8)W_{\rm frac}\)。没有在算法里
计算exp、e、平方根或此后分析中的未知 v。

使用此前独立重构的CDF精确条件期望：对未固定helper，层概率是上面的 \(\beta_j\)；
固定positive-mass state s后改为 \(\mathbf1[w_jp_{jsu}\ge d]\zeta_{jsu}/\alpha_{js}\)，
empty时为零。期望为各resource、各不同正分值层的
\((d_k-d_{k-1})(1-\prod_j(1-\beta_j(d_k)))\) 之和。枚举下一个helper的有限正概率
选项，取期望最大者；加权平均恒等式保证不下降。全states固定后，每资源直接给
chosen-state分值 \(w_jp_{jsu}\) 最大的helper，零分值可空；这不小于虚拟请求子集
最大值的期望。最终selected-clause值 \(q_j\in[0,1]\) 满足

\[
S:=\sum_jw_jq_j\ge\frac58\widehat\epsilon^2.
\tag{3.2}
\]

层排序、候选扫描、有限有理乘积与和均多项式；正 \(\mu_r,\alpha\) 的除法增加
编码长度，不按倒数循环。所有中间乘积/和只含多项式个显式有理数，位长多项式。
初始(3.1)只需在未固定时用；固定state后不要求容量仍逐点不超一，条件期望本身
仍精确。此为CDF-max算法，不是均匀赢家DP的5/8升级。

## 4. 可计算的好组阈值，不用未知最优quality或平方根

枚举输出的每个不同正 \(q_j\) 作为threshold t。令

\[
R_t=\{j:q_j\ge t\},\quad W_t=\sum_{j\in R_t}w_j,\quad
Q_t=\min(t,W_t).
\]

选 \(Q_t\) 最大的t。保留 \(R_t\) 的fallback bundles；outer在state a领其home；
其他本行及所有其他外行helpers全领各自home。全部homes distinct且与B不交，所以
这是一份全组不交分配，最小质量至少 \(Q_t\)。所有 \(q_j\)、\(W_t\) 都是实际构造
的有理数；只需多项式排序/比较。\(S>0\) 保至少一个正threshold。

下列分析性质不要求算法知道h：若某 \(0<h\le1\) 满足

\[
S\ge h(2-h),
\tag{4.1}
\]

则集合 \(R=\{j:q_j\ge h\}\) 的weight W满足
\(S\le W+h(1-W)\)，故 \(W\ge h\)。该集合非空，其最小 \(q_j\) 是枚举中的某t
且 \(t\ge h\)、\(R_t=R\)，于是所选bestthreshold的质量至少h。

## 5. 13/8的全部区间与grid误差

若 \(v\le10/13\)，任何上述输出均有 \(C_{\max}\le2\)，故
\(C_{\max}\le(13/8)(2-v)\)。如无正grid点可行，(1.3)给 \(v<1/128\)，因此也
属于此分支。算法不用知道自己处在哪个分支。

若 \(10/13<v\le1\)，定义分析量

\[
h(v)=\frac{13v-10}{8}\in(0,3/8].
\]

有精确恒等式

\[
\frac58v^2-h(v)(2-h(v))
=\frac{209v^2-468v+260}{64}\ge\frac1{64}.
\tag{5.1}
\]

最后不等式因分子在 \([10/13,1]\) 上递减、在一处值为一。\(\delta=1/128\) 且
\(\widehat\epsilon\ge v-\delta>0\)，故

\[
S\ge\frac58(v-\delta)^2
\ge\frac58v^2-\frac54\delta
\ge h(v)(2-h(v))+\frac3{512}.
\tag{5.2}
\]

由§4，实际quality至少h(v)，从而

\[
C_{\max}\le2-h(v)=\frac{13}{8}(2-v)
=\frac{13}{8}\operatorname{OPT}(P(Q)).
\tag{5.3}
\]

128固定grid就足够，不需原系数共同分母、v离一的分离界或无限精度参数搜索。

## 6. 全部原jobs、总位长及攻击结论

选定原states后，每selector去其原private root；仅导出该selected state实际领取的
正 incidence jobs；每个其他原incidence job留自己的原private endpoint。未选态
全部jobs总负载一，selected root负载二减所领值；resource机每台至多一unit job。
零 jobs私时零、重复 indexed states各自保留jobs/root、unused machines可空。给
每个 \(G+I\) 原job都输出一个实际有限端，没有新增物理逻辑约束或删除原工作。

生成完整matrix和每个LP、128次有理LP、选一次positive outer state、CDF去随机化、
实际threshold扫描及全部job回填，全部在显式Q长度上绝对次数多项式。输入无point、
目标OPT或任何特殊oracle；一阶/二阶点由实际生成LP的标准有理求解取得。没有按
denominator、\(1/p\)、state组合数或accuracy参数枚举；候选states始终原有限显式表。

主动攻击的关键处均已闭合：5/8只用于max-score backend；全original A/Z及其补
保证singleton整化；perstate质量和完整条件容量来自共同数组；其他组确实都有独立
home能回填；grid误差有严格常数余量；不把C≤2当成所有OPT都够。所得结论只属
新Exact的typed one-outer presentation，不识别任意P，也不扩multipleouter/无home
辅助组。该记录尚未读新作者证明、不声称完整实现或实际执行128个LP/生成矩阵；
它给的是可逐行实现的独立算法重构及位复杂度证明。原一般 `UM-TARGET-v1` OPEN。
