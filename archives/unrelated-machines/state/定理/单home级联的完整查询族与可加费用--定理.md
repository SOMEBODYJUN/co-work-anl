---
id: unrelated-machines/single-home-cascade-query-cube
kind: theorem
type_tag: 定理
title: 单home级联的完整查询族与可加费用
status: proved-with-explicit-witness-input
summary: 同一矩阵给定两份严格调度、初态全部正小端任务留home时，可用同一组不交支持按需实现全部查询子集，负载至多1加剩余查询的逐home质量。
legacy_ids:
  - UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v1
  - UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2
review_status: historical-internal-review-and-current-source-reconciliation
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/single_home_cascade_query_separation.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/single_home_cascade_query_separation.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_cube_v2_author_proof.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_cascade_query_cube_v2_independent_review.md
---

# 对象、承重假设与量词

考虑有限非空机器集 \(M\) 上一个显式普通 unrelated-machines 矩阵 \(P\)。有限处理时间为二进制非负有理数，其余端不可用（\(\infty\)）；无释放时间、先后约束或额外联合容量。任务恰分为不交的 \(U,J\)。每枚 \(u\in U\) 至少有一个有限端，所有有限端时间均为1。每枚 \(j\in J\) 恰有一个正且严格小于1的端，记作 \(h(j)\)，时间 \(a_j\in(0,1)\)；其余有限端只能为0或1，端数任意，允许没有零端或没有unit端。

**强home初态**是输入的一份完整合法分配 \(\sigma_0\)，满足 \(C_{\max}(\sigma_0)\le1\) 且所有 \(J\) 留在各自home。另输入同一 \(P\) 的完整合法分配 \(\sigma_1\)，也满足 \(C_{\max}(\sigma_1)\le1\)。给非空 \(Q\subseteq J\)，要求 \(\sigma_1\) 将每枚query送到其处理时间为1的端。两份见证是已给定的实际分配，不是LP、配置分布，也不是算法承诺会找到的未知YES解。

定义
\[
D=\{j\in J:p_{\sigma_1(j),j}=1\},\qquad
Z=\{j\in J:p_{\sigma_1(j),j}=0\}.
\]
有 \(Q\subseteq D\)、\(D\cap Z=\varnothing\)，而 \(J\setminus(D\cup Z)\) 在 \(\sigma_1\) 必留唯一home。对 \(S\subseteq Q\)，令
\[
\delta(S)=\max_{i\in M}\sum_{q\in Q\setminus S:h(q)=i}a_q,
\qquad \delta=\delta(\varnothing)\in(0,1].
\]
查询可共home，其home也可处于其它query的级联域内；这里始终使用同home全部剩余query的总量。非查询费用仅给 \(D\setminus Q\) 上非负有理权 \(w_j\)，\(W=\sum_{j\in D\setminus Q}w_j\)。下文费用只计实际走unit端的这些原任务，不计query、\(U\) 重排、零端移动或其它物理成本。

# 完整查询族定理

对上述每个输入，可确定性地在总位多项式时间预处理一组两两不交、与费用权无关的 \(A_q\subseteq D\setminus Q\)。给任意显式 \(S\subseteq Q\)，可按需在总位多项式时间输出一份完整原任务调度 \(\tau_S\)，并且**同一组** \(A_q\) 对所有 \(S\) 同时满足：

1. \(J\) 中走unit端的任务恰为 \(S\cup A(S)\)，其中 \(A(S)=\bigcup_{q\in S}A_q\)，均使用各自 \(\sigma_1\) 原端。特别地，query模式恰为 \(S\)。
2. \(Z\) 始终使用 \(\sigma_1\) 原零端，其余 \(J\) 回唯一home；每枚 \(U\) 只用自己 \(\sigma_0,\sigma_1\) 中的原端。所有原任务各分配一次。
3. 全机同时满足
\[
C_{\max}(\tau_S)\le1+\delta(S)\le1+\delta.
\tag{1}
\]
   \(S=\varnothing\) 与 \(S=Q\) 的输出本身均严格 \(C_{\max}\le1\)。
4. 写 \(c_q=\sum_{j\in A_q}w_j\)，则
\[
\operatorname{fee}(\tau_S)=\sum_{q\in S}c_q,
\qquad \sum_{q\in Q}c_q\le W.
\tag{2}
\]
   因而至少一个单query输出费用不超过 \(W/|Q|\)。

这里输出的是多项式大小的支持和按需生成器，不列出指数多份调度。式(2)是这一个构造族的费用等式，未声称各模式的最优费用函数可加。

# 单位匹配、单parent闭包与完整证明

令 \(H=\{h(j):j\in J\}\)。每个 \(i\in H\) 在 \(\sigma_0\) 已有正负载，而 \(U\) 的时间为1，故严格初态使 \(\sigma_0(U)\cap H=\varnothing\)。因此 \(M_0=\sigma_0|_U\) 是避开 \(H\) 的任务—机器匹配。另一方面，\(M_1=\sigma_1|_{U\cup D}\) 也是匹配，因这些任务在 \(\sigma_1\) 全部耗1。

在 \(M_0\triangle M_1\) 中，每枚 \(d\in D\) 仅有一条 \(M_1\) 边，其连通分量是从任务 \(d\) 出发、结束于某个 \(M_0\) 未占机器 \(e(d)\) 的增广路 \(\Pi_d\)。它不能结束于另一枚 \(D\)：任务侧到任务侧路径长为偶数，而交替路首尾都为 \(M_1\) 边要求奇数长度。\(U\) 在两匹配均被覆盖，也不能作为另一端。因此各 \(\Pi_d\) 顶点不交，\(e:D\to M\) 单射。

对任意 \(B\subseteq D\)，只翻转 \(\Pi_d,d\in B\)，其余仍用 \(M_0\)，得到恰覆盖 \(U\cup B\) 的匹配 \(M(B)\)。每条被选路径中的所有任务采用其 \(M_1\) 原端。由于 \(M_0\) 避开所有home，增广路一旦到达 \(H\) 便必须结束；所以 \(M(B)\) 使用的home恰为 \(\{e(d)\in H:d\in B\}\)。共同匹配边或不含 \(D\) 的交替分量无需翻转。

若 \(e(d)=i\in H\)，\(\sigma_1\) 已在 \(i\) 放一枚unit，严格性及 \(a_j>0\) 迫使所有 \(h(j)=i\) 的 \(J\) 在 \(\sigma_1\) 离开home，即属于 \(D\cup Z\)。在顶点 \(D\) 上定义
\[
\operatorname{Ch}(d)=\{j\in D\setminus Q:h(j)=e(d)\}.
\tag{3}
\]
由home唯一、\(e\) 单射，每枚非query顶点至多一个parent；query完全不作child，所以都是零入度根。令 \(B_q\) 为从 \(q\) 沿children可达的顶点，含 \(q\)，并置 \(A_q=B_q\setminus\{q\}\)。

不同 \(B_q\) 不相交：若两根首次汇合，汇合点有两个parent；若一根可达另一根，后者不再零入度。根也不能进入有向圈，因为首次进入点同时有圈内和圈外parent。图中其它无根圈可以存在，只是不被采用。因此全部 \(B_q\) 两两不交，且 \(B(S)=\bigcup_{q\in S}B_q=S\cup A(S)\) 对非query children闭合。

现在用 \(M(B(S))\) 安排 \(U\cup B(S)\)，把 \(Z\) 放在原 \(\sigma_1\) 零端，其余 \(J\) 放home，得到 \(\tau_S\)。所有有限端来自原矩阵，每枚任务恰执行一次，unit-export集合正好是所述集合。逐机检查：

- \(i\notin H\)：没有正小端任务在此执行，匹配至多一枚unit，其余只有零负载，故负载至多1。
- \(i\in H\) 且匹配不用 \(i\)：只有 \(\sigma_0\) 的home任务子集及零任务，故负载至多1。
- \(i\in H\) 且匹配使用 \(i\)：唯一某 \(d\in B(S)\) 满足 \(e(d)=i\)。该home全部任务属于 \(D\cup Z\)；\(Z\) 归零，全部非query \(D\) 是 \(d\) 的children并已导出，\(S\) 也已导出。唯一可剩的正负载来自 \(Q\setminus S\)，于是
\[
L_i(\tau_S)=1+\sum_{q\in Q\setminus S:h(q)=i}a_q\le1+\delta(S).
\]

这证明(1)。全query时余量为0；空query时没有翻转，\(U\) 用 \(M_0\)，\(J\setminus Z\) 回home，仅从初态删除正负载，因此两端模式都严格。费用恰对 \(A(S)\) 求和；支持不交和非负权立即给(2)。

完整时间表可由完整分配直接生成：每机零时间任务置时刻0，其余按固定任务顺序串行运行，开始时刻为有理部分和，makespan等于最大负载。原程序输出完整分配、逐机负载及任务清单，不显式输出开始时刻；这是实现输出格式与数学可构造性之间的准确区别。

# 直接机器图证明与原程序的关系

另一条等价证明将每枚 \(d\in D\) 画为 \(h(d)\to\sigma_1(d)\)，每枚 \(u\in U\) 画为 \(\sigma_0(u)\to\sigma_1(u)\)，保留任务标签。\(\sigma_1\) 的unit目标互异给总入度至多1；删去全部query弧后，每个 \(\sigma_1(q)\) 是互异的零入度根，可达域两两不交。根域内非query全部导出、\(U\) 沿原弧重排，域外只是 \(\sigma_0\) 减负；域内留下的正home任务恰为未选query，故得到相同余量式。压缩其中连续的 \(U\) 路径，便得到上面 \(e(d)\) 和children图。

原审计程序实际实现的是增广路路线：`_construct_paths` 沿 \(M_1\) 边和 \(M_0\) 逆边构造路径；`_construct_closures` 切掉query child边并计算固定闭包；`construct` 对显式请求的 \(S\) 翻转路径，再从原处理矩阵用Fraction逐机回算。两种图的无根环都无需采用，不应误写成整个输入图是DAG。

理论预处理与按需输出均是总位多项式：两个匹配、增广分量和children总规模为 \(O(|U|+|J|+|M|)\)，支持总大小至多 \(|D\setminus Q|\)。原Python为每个 \(d\) 检查终点home下的所有 \(J\)、为每份输出扫描原任务/机器，仍为多项式，未承诺上述线性最优实现。有理运算位长受输入分母位长总和控制，不按 \(1/\min a_j\) 或 \(2^{|Q|}\) 迭代。

# 用途、限制与比较

若每home的全部query小质量至多 \(\eta<1\)，且某固定费合同要求**所有**峰值至多 \(1+\eta\) 的单query模式都付非query unit费至少 \(F>0\)，则本族每个单query都符合该弱阈值，迫使 \(c_q\ge F\)，故 \(W\ge|Q|F\)。这约束在同一矩阵的两strict模式间复用固定标签费的做法。

强home不能省略。一般双见证的锐例令 \(q_1,q_2\) 从各自tiny初端送到 \(A,B\)，\(x_1,x_2\) 从 \(A,B\) 的unit端送到共同home \(R\) 的时间 \(1/2\)，另有 \(f\) 从 \(R\) 的时间 \(1-\gamma\) 送到 \(S\) 的unit端。两完整模式均严格；对任意 \(B_0<3/2\)，取 \(0<\gamma<\min(1/2,3/2-B_0)\)，任一单query在阈值 \(B_0\) 都强迫同一 \(f\) 迁移。每任务仍只有一个正小端，然而初态把 \(x_1,x_2\) 预先导出了home，恰违反本定理。一般双见证结论只保证每个单query的阈值染色支持，不能替代本定理的全子集同组构造，反向也不能把本定理扩到该锐例。

\(\delta=1\) 时统一界可以为2；零移动、\(U\) 重排或退款后的净成本不在(2)内。多正小端、只给弱阈值见证、未知strict见证搜索、源相关外部联合容量均须新论证。零时间原端已允许，但 \(a_j=0\) 不在正小端核心域，空 \(Q\) 也不在声明域内。

本对象仅研究普通UM的完整实际调度及指定费用，与六人共同目录SPE的客户覆盖模型无共同量词。它没有给一般UM近二算法、近二困难性、最优费用可加性或一般源decoder，也未升级任何主目标状态。

# 证据与审查身份

历史v1只陈述单query；v2由root提出同组任意子集和 \(\delta(S)\) 加强，独立审查者先按所获精确描述重构机器图证明，再核v2 Exact，之后读作者增广路证明。最终组合审查当时明确软件pending；后续root已审读实际代码并运行冻结14机14任务、3query的8模式实例。两个时点不能互相覆盖。

本轮先读原程序和review，随后读canonical及冻结证明、历史审查与旧成功输出；这是来源核对和直接数学复核，不宣称本轮blind审查。旧成功run的脚本/输入SHA均与原字节相符，未重复构造器运行；本轮另有从旧证书独立回算所有原任务和机器负载的结果，范围见[原程序与审查证据](../计算/单home级联原程序与分层审查证据--计算.md)及[证据包](../../tools/evidence/single-home-cascade-originals/README.md)。一般量词来自上述证明，8个显式模式仅是有限回归。外审和全球新颖性均未认证。
