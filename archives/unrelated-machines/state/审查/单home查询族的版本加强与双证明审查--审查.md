---
id: unrelated-machines/single-home-query-cube-version-proof-history
kind: review
type_tag: 审查
title: 单home查询族的版本加强与双证明审查
status: five-frozen-history-sources-integrated
summary: 精确保留v1单query陈述、v2固定不交支持的全子集加强、原增广路论证与历史独立机器图推导的对应关系和实际读取顺序。
truth_status: proved-restricted-normal-form-with-supplied-strict-witnesses
review_status: historical-independent-reconstruction-and-current-read-after-reconciliation
legacy_ids:
  - UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v1
  - UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_v1_exact.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_v1_proof.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_cube_v2_exact.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_cube_v2_author_proof.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_cube_v2_independent_review.md
---

本页合入五份历史主源，完整原文已在前批作为比较依赖实读，本批逐份复核同SHA、逐源比较独有内容。主定理及完整证明已见[单home完整查询族](../定理/单home级联的完整查询族与可加费用--定理.md)，原规范程序与有限证据见[原程序和分层审查](../计算/单home级联原程序与分层审查证据--计算.md)。这里保存版本增量、两种证明的接口及历史审查义务，不再建立第二个同义一般定理。

| 主源ID | 文件 | 字节数 | 本批独有内容的正文位置 |
|---|---|---:|---|
| `eb85a9b372087655b0b8` | v1 Exact | 3991 | 第1–2节的原候选身份、单query量词、原费用/零端与distinct-home充分条件 |
| `752926edf480850141f0` | v1 Proof | 6685 | 第3节的原增广路—单parent构造、原符号与逐机论证 |
| `8aa47fae201fa5f5be47` | v2 Exact | 4385 | 第2、4节的同组任意子集、精确余量、端模式strict与简洁输出合同 |
| `9ed0c86b10493ca498a3` | v2作者Proof | 5562 | 第3–4节同一匹配支持并集为何同时合法、真实任务和费用族 |
| `77490976a145b0fed350` | v2独立review | 7654 | 第5节直接机器图、真实读取顺序和10项逐点攻击 |

两个冻结提交分别是 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；各源在两提交的字节相同，不算两次证明或审查。逐份SHA、原路径和保真原件位置见[历史证据清单](../../tools/evidence/single-home-cascade-history/source-manifest.json)。

# 1. 五源共同的严格输入合同

机器集 \(M\) 有限非空，处理矩阵 \(P\) 显式给出；有限时间为非负有理数，正式UM输入按二进制编码，不可用端为 \(\infty\)。普通调度无释放时间、先后约束或额外外部联合容量。任务恰分为不交 \(U,J\)：每枚 \(U\) 至少一个有限端，全部有限时间为1；每枚 \(j\in J\) 有唯一正小端 \(h(j)\)，\(a_j\in(0,1)\)，其余有限端只能为0或1，端数不限。

输入同一 \(P\) 的两份完整实际分配 \(\sigma_0,\sigma_1\)，每机负载均至多1；\(\sigma_0\) 把全部 \(J\) 留在home。非空 \(Q\subseteq J\) 在 \(\sigma_1\) 全走unit端。定义
\[
D=\{j\in J:p_{\sigma_1(j),j}=1\},\quad
Z=\{j\in J:p_{\sigma_1(j),j}=0\},\quad
\delta=\max_i\sum_{q\in Q:h(q)=i}a_q.
\]
因此 \(Q\subseteq D\)、\(Q\cap Z=\varnothing\)、\(0<\delta\le1\)，其余 \(J\setminus(D\cup Z)\) 在 \(\sigma_1\) 必留home。\(D\setminus Q\) 上给非负权 \(w_j\)，\(W=\sum_jw_j\)。费用仅计这些非query原任务实际走unit的权，不含 \(U\) 重排、query、零端移动和其它成本。

五源没有把strict实际见证换成LP、未知最优解、不同实例的两个YES，或只有较大阈值的模式。\(\sigma_0\) 全部正小端任务留home是承重条件，不能缩为“query留home”。零端可以原生存在，\(Z\) 始终使用 \(\sigma_1\) 原零端。纯unit/zero任务若预先固定到零端并删除，只保证负载不增；若外部仍对这项移动收费，费用结论不随该预处理自动成立。\(a_j=0\) 不属于核心域，不能把免费零home任务当本Claim的query。

# 2. v1到v2的真实加强

v1 Exact 的状态为“精确候选陈述，冻结给独立statement-first攻击，证明另存”。其量词是在每个合格输入上构造固定不交 \(A_q\subseteq D\setminus Q\)，再为每个 \(q\in Q\) 输出完整 \(\tau_q\)：\(J\) 中unit集合恰为 \(\{q\}\cup A_q\)，\(Z\) 固定原零端，其余 \(J\) 回home，\(U\) 可合法重排，峰至多 \(1+\delta\)。原单query族费用满足
\[
\sum_{q\in Q}\operatorname{fee}(\tau_q)
=\sum_{q\in Q}\sum_{j\in A_q}w_j\le W.
\tag{1}
\]
支持不依赖权，所以同一构造对全部非负权成立。v1 Exact 没有陈述任意多query的支持并集都可以同时使用；不能因后续证明更强而追溯改写旧版本。

v2 Exact 保持完全相同的严格输入域，但将输出改为：先构造**同一组** \(A_q\)，再给显式 \(S\subseteq Q\) 按需生成完整 \(\tau_S\)。写
\[
A(S)=\bigcup_{q\in S}A_q,\qquad
\delta(S)=\max_i\sum_{q\in Q\setminus S:h(q)=i}a_q.
\]
所有 \(S\) 同时满足
\[
\begin{aligned}
\{j\in J:p_{\tau_S(j),j}=1\}&=S\cup A(S),\\
C_{\max}(\tau_S)&\le1+\delta(S),\\
\operatorname{fee}(\tau_S)&=\sum_{q\in S}c_q,
\quad c_q=\sum_{j\in A_q}w_j,\quad\sum_qc_q\le W.
\end{aligned}
\tag{2}
\]
\(Z\) 仍在原零端，\(Q\setminus S\) 和其它未导出 \(J\) 回home。全query输出严格，因为 \(\delta(Q)=0\)；空query输出本身也严格，虽然显示式 \(1+\delta(\varnothing)\) 可能宽松。费用可加只针对本构造族，不是各模式最优费用函数的模加性。

| 项目 | v1冻结陈述 | v2冻结陈述 |
|---|---|---|
| 同一支持的使用范围 | 全部singleton | 全部 \(S\subseteq Q\) |
| 负载显示界 | \(1+\delta\) | \(1+\delta(S)\) |
| 输出规模 | 可列 \(|Q|\) 份完整分配 | 多项式支持和按需生成器，未列 \(2^{|Q|}\) 份 |
| 空/全端模式 | 未作为输出族单列 | 两端输出本身都strict1 |
| 费用 | singleton总费至多 \(W\) | 所有 \(S\) 的构造费精确可加，总支持费至多 \(W\) |
| home质量的充分条件 | Exact举query homes互异且每件 \(a_q\le\eta\) | 只需每home全部query总质量至多 \(\eta\) |

最后一行不是v2新允许共home：v1输入本来允许共home，v1 Proof末段也已经明确按每home总质量表述用途。v2 Exact 将这一准确的聚合条件写进完整族推论。若每个singleton在峰至多 \(1+\eta\) 都必付指定费 \(F>0\)，两版都推出 \(W\ge|Q|F\)，但v2额外控制全部子集。

从(2)取 \(S=\{q\}\)，再用 \(\delta(\{q\})\le\delta\)，即蕴含v1所述结论。这是版本加强关系。单凭一个抽象v1存在性陈述，不能把未知的各 \(\tau_q\) 直接拼在一起证明v2；还需下面的共同匹配与闭包结构。

# 3. 原作者两版证明的承重接口

v1 Proof 已给出两版共有的构造。令 \(H=\{h(j):j\in J\}\)，\(M_0=\sigma_0|_U\)，\(M_1=\sigma_1|_{U\cup D}\)。每home在初态有正负载，故 \(M_0\) 避开 \(H\)；两严格见证使 \(M_0,M_1\) 都是单位任务匹配。这里正性、全home初态和strict1分别承担职责，缺一不能沿用该论证。

\(M_0\triangle M_1\) 中每枚 \(d\in D\) 产生增广路 \(\Pi_d\)，终点 \(e(d)\) 是 \(M_0\) 未占机器。含 \(d\) 的分量不可能是环；也不能连到另一枚 \(D\)，因为任务侧两端要求偶数路径长，而首尾均 \(M_1\) 边要求奇数长度。所有 \(U\) 在两匹配均已覆盖，也不能作为未匹配另一端。因此各 \(\Pi_d\) 顶点不交，\(e\) 单射。

对任意导出集 \(B\subseteq D\)，只翻转对应 \(\Pi_d\) 得匹配 \(M(B)\)，覆盖恰 \(U\cup B\)，不丢 \(U\)、不额外匹配别的 \(D\)。若路径到达home，那里没有 \(M_0\) 边，必在该处结束；所以翻转所用home恰为 \(e(B)\cap H\)。共同匹配边和不含 \(D\) 的多余交替分量仍用 \(M_0\)，不必先无代价补成某个预选export模式。

若 \(e(d)=i\in H\)，\(\sigma_1\) 在 \(i\) 有unit，迫使该home全部正小端任务离开，即属于 \(D\cup Z\)。定义
\[
\operatorname{Ch}(d)=\{j\in D\setminus Q:h(j)=e(d)\}.
\tag{3}
\]
home唯一、\(e\) 单射给每枚非query至多一个parent；所有query都被从child中切掉，是零入度根。每根闭包两两不交且不能进入有向圈；其它无根圈允许存在，不必声称整个图为DAG。v1把含根闭包记作 \(S_q\)，v2改记 \(B_q\)，两版 \(A_q\) 都是去掉根后的闭包。

原文v1第1节的 \(M(S)\) 中 \(S\subseteq D\) 是**任意导出集**，不能与v2第2节的query子集 \(S\subseteq Q\) 混同。本页统一将前者改记 \(B\)，而不改原件字节。

对singleton，v1安排 \(M(B_q)\)、\(Z\) 原零端及其它 \(J\) 的home，并分三类机器：非home至多一个unit；未被匹配占用的home只是初态子集；被占home为唯一某 \(e(d)\)，所有非query child已导出，只剩其它query。该第三类原论证已经得到
\[
L_i(\tau_q)\le1+\sum_{r\in Q\setminus\{q\}:h(r)=i}a_r,
\]
再放宽为 \(1+\delta\)。这说明精确余量加强与原负载机制相容；它不改变v1冻结陈述的历史身份。

# 4. v2为何无需换支持便能得到全部子集

v2作者Proof的独有步骤是显式取
\[
B(S)=\bigcup_{q\in S}B_q=S\cup A(S),
\]
用 \(M(B(S))\) 安排 \(U\cup B(S)\)。这不是只凭 \(A_q\) 不交而随意相加：**任务层**有不交根闭包，**机器层**另有不交原增广路径，二者共同保证同时翻转没有新冲突。\(B(S)\) 对所有非query children闭合，而其它query已被切断，所以query模式恰为 \(S\)。

任一被匹配占用的home为唯一 \(e(d)\)，\(d\in B(S)\)；其正小端任务全属 \(D\cup Z\)。\(Z\) 归零，非query children全部导出，\(S\) 也已导出，剩余正任务恰是 \(Q\setminus S\) 中以该机为home的query，故
\[
L_i(\tau_S)=1+\sum_{q\in Q\setminus S:h(q)=i}a_q.
\tag{4}
\]
其它home为初态子集，非home至多一个unit。这样逐机同时得到(2)，包括多个query共home、query home位于别根域内等交叉。没有把每件query小于 \(\eta\) 错换成同home总量小于 \(\eta\)。

费用是实际导出的原任务 \(A(S)\) 求和，不交性给精确加法，非负权给总和不超过 \(W\)。原 \(U\) 在每条选中路径中用自己的 \(\sigma_1\) 端，未选中则用 \(\sigma_0\) 端，因此证明实际还给出比“在合法unit端重排”更明确的两见证原端合同；不是凭新添资格完成输出。

v1可以输出全部 \(|Q|\) singleton调度，长度至多 \(O(|Q|(|U|+|J|))\)。v2预处理总支持量至多 \(|D\setminus Q|\)，按给定 \(S\) 扫描任务输出一次完整分配；没有要求写出指数多份结果。验证 \(\delta(S)\)、原负载、费用和有理开始时刻只用多项式次加法比较，分母位长受输入分母位长总和控制，不按时间数值、\(1/\min a_j\) 或 \(2^{|Q|}\) 迭代。

# 5. 历史独立机器图、读取顺序与十项攻击

独立review所述的顺序是：先据父任务给出的精确加强描述重构直接机器图并落scratch；再读取冻结v2 Exact核SHA、确认范围；最后首次读v2作者Proof，逐点核增广路。记录明确未读v1作者Proof、未读其它agent文件、未操作Git或登记Work。父描述最初只给统一 \(1+\delta\)，审查者在读作者Proof前已从逐机余量得到 \(\delta_{res}(S)\)，之后确认它等于Exact的 \(\delta(S)\)。因此应保留“父描述先行→Exact→作者Proof”的完整历史，不能缩成完全无上下文的盲读。

直接机器图将 \(d\in D\) 画成 \(h(d)\to\sigma_1(d)\)，将 \(u\in U\) 画成 \(\sigma_0(u)\to\sigma_1(u)\)，保留原任务标签。\(\sigma_1\) 的unit目标互异给总入度至多1。删除全部query弧后，各 \(r_q=\sigma_1(q)\) 是互异零入度根，其可达域 \(R_q\) 不交且不能进入圈。令
\[
A_q=\{d\in D\setminus Q:h(d)\in R_q\}.
\]
对 \(R(S)=\bigcup_{q\in S}R_q\)，只移动 \(S\)、home在该域的非query \(D\)、初态端在该域的 \(U\)；\(Z\) 原零端，其余回home。域内每机恰接一枚所选unit，只剩未选query的home质量；域外没有新unit进入，是 \(\sigma_0\) 减去正home负载。因此同样得到(4)及域外至多1。

压缩连续 \(U\) 迁移链便得到作者的终点 \(e(d)\)，对应 \(\operatorname{Ch}\) 闭包；未被根激活的额外交替成分可保持初态。两条证明共享unit目标入度和home正性，但直接证明不先构造匹配对称差。这是历史当轮独立推导路线，不是另一个UM模型或一般困难性结果。

| 原review攻击项 | 保留下来的承重检查 |
|---|---|
| 1 | \(M_0\) 避全部home同时用到 \(a_j>0\)、初态全home、strict1。 |
| 2 | 含 \(D\) 的交替分量不能是圈或 \(D\) 到 \(D\)，原任务侧奇偶性不可省略。 |
| 3 | 路径不交和 \(e\) 单射；共同匹配边不会暗中连接两路。 |
| 4 | 任意导出子族翻转仍覆盖全部 \(U\)，不添其它 \(D\)。 |
| 5 | 所用home只能是路径终点，不能遗漏路径内部另一个需清空home。 |
| 6 | 被unit占用home的所有正任务都在 \(D\cup Z\)，非query children全部导出。 |
| 7 | query永不作child；无根环/自环不被根触达；即便 \(e(q)=h(q)\)，切query child仍正确。 |
| 8 | 不交闭包与不交机器路径两层均需保证，同home/cross-home残余由(4)统一计。 |
| 9 | \(Z\) 零端原生保留；零任务置时刻0、unit先排、home任务按固定次序串行，可输出全部开始时刻，位长多项式。 |
| 10 | 构造费可加不等于最优费可加；总 \(\delta=0\) 不在非空正query域，但 \(\delta(Q)=0\) 合法且全开strict。 |

源结论是v2 Exact与Proof通过，未发现致命缺口；只对应此限定normal form。作者Proof与独立review引用文件名中的 `_claim.md` 是当轮陈述名；库存冻结条目实际名为 `_exact.md`，由其SHA `975f43d6c5708a3c37f1fb4675ddc1c108856d3306f6186e376d6e2981d879d3` 绑定，不按字符串名误造另一份未知Exact。

本轮已经读过程序、canonical和两版证明，只能称读后来源/数学核对，不复演历史Exact-first或blind身份。历史record的独立性按其实际文字保留，不能扩成外部同行评审或全球新颖性认证。

# 6. 与既有正文、相邻方法和软件证据的边界

[主定理](../定理/单home级联的完整查询族与可加费用--定理.md)已经完整吸收两种证明的一般数学，本批五源的独有去向是本页的版本比较、原符号、严格输入各自职责、双层不交与十项审查，而非重复记五个新定理。已有[共居SAT与单home审查](共居查询SAT与单home级联查询分离双源审查--审查.md)针对canonical，[单端口与单home审查](单端口向下闭集与单home级联双源审查--审查.md)针对旧JSON；它们都不能替代五份历史文件的实际版本身份。

已实际对读[一般双见证的冻结证明审查](双见证查询分离的染色证明与冻结审查边界--审查.md)：其v2阈值染色适用任意矩阵/端时间，支持只保证singleton的 \(\max\{3T/2,T+\delta_q\}\)。它不自动给本页全子集合同；其作者/typed锐例中两个blocker初态已离开共同small home，违反本页强home，而general审查的另一个五机例甚至给blocker两个正小端。共同使用两个strict见证和可加费用，不足以互换量词。

[批量插值v4](双见证批量插值与成束耦合细分边界双源审查--审查.md)对任意两实际见证及合法指定固定任务，使用一次slot整数流输出一份共同调度，逐机界为 \(t_i+(L_i^0+L_i^1+d_i)/2\)。它不需本页单home，却没有预先固定不交 \(A_q\) 后实现全部 \(S\) 的同一费用分解。不同方法给不同输出合同，不以“都能混合两见证”自动合并为本页的版本推广。

五份历史源是数学陈述/证明/审查，不是运行日志。本批没有新增或重复执行原构造器、没有重跑前批已通过的旧证书读取器，也没有把原成功run重新计数。历史最终组合当时软件pending、后续root真实14机14任务8模式run、前批140归属/140全机负载独立回算，均在[计算页](../计算/单home级联原程序与分层审查证据--计算.md)分别保留。当前五主源不含最终组合页；该页仅为比较依赖。

多正小端、初态预导出、弱阈值见证、其它费用、未知YES搜索和一般源decoder仍未被覆盖；\(\delta=1\) 只给2，不能当固定改善。这里没有一般UM近二算法/困难性，也与六人共同目录SPE的每完整历史覆盖量词无推导关系。下一步若使用该合同，先对具体矩阵验证强home、两strict、query目标、残余总量和实际费用对象。
