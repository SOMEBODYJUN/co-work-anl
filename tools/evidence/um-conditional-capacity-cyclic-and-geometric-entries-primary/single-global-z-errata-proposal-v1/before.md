---
id: "unrelated-machines/diluted-shared-terminal-raw-k2-and-sink-probe-review"
kind: "review"
type_tag: "审查"
title: "稀释共享终端 raw K2 与终端探针共同间隙双源审查"
status: "complete-source-read-cross-integrated"
truth_status: "two stated-scope analytic gap constructions plus precise probe boundary; no general hardness or UM-TARGET closure"
review_level: "full-current-source-read-and-cross-archive-comparison"
scope: "raw K2 with complete first/pair CONFIG consistency, fixed-row-degree extension, diluted sink capacity, independent per-edge LST/star/GHMR probes, and shared-small-end escape"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/diluted_shared_terminal_raw_k2_gap.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/diluted_shared_terminal_raw_k2_gap.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/diluted_sink_probe_gap.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/diluted_sink_probe_gap.md"
source_inventory:
  - "id:9739957574111e83579a; blob:1d3cf8e4b5b3c16e69ac7ed7d7d776388530ffe3; sha256:fb705e62ae3344a24c95ca962d4fa2cfd83dbc57422eb59fd6285713e29a121b; path:research/current/unrelated_machines/diluted_shared_terminal_raw_k2_gap.md"
  - "id:07f075f376fc5aa958fe; blob:0e5eaf709216d025bfc5f9dce9cef281bf3f9363; sha256:08c7d787759fd48b65cada97c052bdab80556bedde1e14f4601b8e4447b52ffd; path:research/current/unrelated_machines/diluted_sink_probe_gap.md"
related_reviews:
  - "稀释逃逸行度与共享终端局部审计--审查.md"
  - "稀释终端独立重放与探针缺口有限审计--审查.md"
  - "重型匹配凸化与逃逸残余审计--审查.md"
  - "配置剥离与联合匹配有限审计--审查.md"
  - "C2前缀满载与单位多切片有限审计--审查.md"
  - "state/问题/任务级共同容量的算法义务--问题.md"
---

# 阅读范围和身份

本批通过 `clean show` 完整读取两份当前正文的全部章节、公式、边界和证据说明，并与同主题已有审查和冻结运行比较。两个来源都属于 unrelated-machines 的机器—作业—配置语义；它们不属于有限单位客户、共同非空目录、六提供者完整历史或终局覆盖均分的六人 SPE 模型。正文中列出的 raw K2、整行度、终端探针和 escape 身份均保持独立，不把同一构造的不同测试误写成一个更强的共同概率分布。

第一源 `9739957574111e83579a`（SHA-256 `fb705e62ae3344a24c95ca962d4fa2cfd83dbc57422eb59fd6285713e29a121b`）先给普通 UM 的显式稀释共享终端族，在精确定义的 raw K2 合同下把整数间隙推到 2；随后给固定行度 (d) 的整行 CONFIG 矩扩展，说明任意固定 (d) 仍可保持相同趋二边界。第二源 `07f075f376fc5aa958fe`（SHA-256 `08c7d787759fd48b65cada97c052bdab80556bedde1e14f4601b8e4447b52ffd`）攻击的是配置可行性、逐边普通 LST、重备选星匹配和 GHMR 固定点等独立前处理合同，并给出终端稀释和共享小端的容量机制。

两源共同保留的范围是：完整解析构造、条件算法的安全性、指定有限审计和方法边界均可归档；一般精确 SDP/CONFIG 求解、一般近二算法不存在性、复杂度 hardness、外部新颖性及 `UM-TARGET-v1` 仍开放。

# 一、稀释共享终端与 raw K2

## 1. 原始 raw K2 的对象

对每个整数 (k\ge2)，令
\[
 L=2k^2,\qquad M=1+60Lk^4=1+120k^6,\qquad a=1/M,\qquad T_0=1+1/k.
\]
有 (M) 个物理组件。组件 (i) 含一台 (U_i)、(L) 台 (B_{i,b}) 和 (k) 台 (Z_{i,t})。一个 selector job (h) 可在任意 (U_i) 用时 1；每个 (f_{i,j}) 在 (U_i) 用时 (1/k)，在每个 (B_{i,b}) 用时 1；每个 (e_{i,b,\ell}) 在 (B_{i,b}) 用时 (1/k)，在每个 (Z_{i,t}) 用时 1；未列边为无穷。所有 job 独立、不可分割并完整执行，未选中组件的 job 仍存在。

raw K2 的精确定义是：一个共同次数至多四的线性泛函 (F)，包含 Boolean/one-hot 商关系、全局 (M_2) PSD、每台原机器的完整 `CONFIG(T)` first/pair 分布（同一 (F) 的端点一阶和同机二阶矩），以及对涉及全输入全部端点的任意 affine (q) 的
\[
F[(T-load_v)q^2]\ge0.
\]
不同机器的 CONFIG 分布不要求来自同一个全局 schedule law；合同也不加入 `export<=activation`、`inactive-all-home`、精确 active-tail 计数或共同 Boolean 配置变量 λ_C 与全次数 links。这里的“raw”边界必须保留，否则会把本反例错误升级到更强的 joint-CONFIG-M2 系统。

## 2. 真实 OPT 和显式共同法则

任意 (T<2) 的真实调度中，selector (h) 必在某个 (U_i)。若该根最多保留 (lfloor k(T-1)\rfloor) 个 (f) 任务，则至少
\[
 r=k-lfloor k(T-1)\rfloor
\]
个 (f) 任务被送到不同 (B) 机器；每个被 unit 占用的 (B) 又至少把 (r) 个 (e) 任务送到不同 (Z) 终端。终端只有 (k) 台且每个 unit 负载为 1，故 (r^2\le k)。令 (s=\lfloor\sqrt{k}\rfloor)，得 (T\ge2-s/k)。选择一个组件、在 (U_i) 执行 (h)，把 (s) 个 (f) 送到 (s) 个不同 (B)，再由各自 (B) 把 (s) 个 (e) 送到 (s^2) 个互异终端，其他 job 留 home，达到该值。因此
\[
 \operatorname{OPT}(P_k)=2-\frac{\lfloor\sqrt{k}\rfloor}{k}.
\]

共同有限法则均匀选择组件 (I)。条件于 (I)，选中组件用 (H)，其余用 (Q)。(H) 均匀选择一个 injection，把各 (f) 送至不同 (B)，其余 (e) 留 home；(Q) 由全 home、单个 (f) 连同对应 (B) 的 (e) 完整送终端、以及单个 (e) export 三类组成，概率 (1/2,1/4,1/4)。每个样本都是完整实际赋值，(Q) 的机器负载至多 1，(H) 的 (U/Z) 至多 1，(B) 至多 2。令 (F) 为其期望，所有任意阶的 (M_2) 和 Boolean 等式自动成立；这支持 raw K2 的全局共同矩。

## 3. 每台机器 first/pair CONFIG 和 affine-localizer

(U_i) 与终端行的边际直接由上述有限法则给出合法 CONFIG。对 (B_{i,b})，设 unit incoming 指示为 (R_j)、home (e) 指示为 (Y_\ell)，取
\[
 p=ak/L,\qquad b_0=c_0=(1-a)/(4L).
\]
正文列出五类合法配置：一个 unit 加一个 home、一个 unit 无 home、无 unit 无 home、无 unit 恰遗漏一个 home、无 unit 全部 home。权重总和为1，所有 first/pair 恰与 (F(R_j),F(Y_\ell),F(R_jR_{j'}),F(R_jY_\ell),F(Y_\ell Y_{\ell'})) 匹配；(M-1=60Lk^4) 保证各权重非负。每个配置负载不超过 (T_0)。

全局 affine-localizer 的关键是按组件条件化。任意全输入 affine (q) 消去 home 后，写成 selector、各组件非 home heads 与 offset 的和。固定一个 (B) 后，Q 状态给任意单组件系数满足
\[
 E_Q[q^2]\ge\frac{\|c\|^2}{30Lk^3},
\]
选中组件 H 下
\[
 E_H[(T_0-load_B)q^2]\ge-2\|c\|^2.
\]
组件间独立，其他组件的中心化方差项非负；选中组件概率 (a=1/M) 又足够小，故
\[
 F[(T_0-load_B)q^2]
 \ge\left(\frac{1-a}{30Lk^4}-2a\right)\|c\|^2\ge0.
\]
(U) 与终端逐样本 slack 至少 (1/k)，所以它们的所有全局 affine localizer 也非负。正文还给出全部次数至多四矩和配置列表的确定性有理生成，输出相对于显式展开输入长度为多项式；这是“指定证书可生成”，不是一般 raw 可行性求解器。

因此 raw K2 在 (T_0) 有显式证书，而真实 OPT 与 (T_0) 的比值趋于 2。标准配置 first marginal 的两倍 assignment 舍入给任意 raw 可行目标 (T) 的 (OPT\le2T)，故该精确定义 raw 系统的全类 gap 上确界为 2。证书不代表真实 schedule，也不表示 canonical native C2、joint-CONFIG-M2 或更强跨行容量系统仍有该 gap。

## 4. 固定行度 (d) 的整行 CONFIG 扩展

正文后半段固定 (d\ge2)，对 (k\ge d) 令 (s=d-1)、
\[
 Z=\sum_{u=0}^{s}\binom ku,\quad A_{\max}=\binom{k-1}{s},\quad L=2k^2,
\]
\[
 M=1+120Lk^4+4kZA_{\max},\quad a=1/M,\quad T=1+s/k,
\]
并使用相同的 (U,B,Z) 机器和 job 类型。raw 合同把共同矩阶数提高到 (D=\max(4,d))：所有同机 endpoint 单项式、总次数至多 (d) 的矩与 (F) 一致；仍只要求 affine (q) 的 load-localizer，不引入 higher-degree (q) 或跨行共同配置变量。真实 OPT 仍是 (2-lfloor\sqrt{k}\rfloor/k)，缩放 (k/(k+s)) 后目标变为 1，固定 (d) 且 (k\to\infty) 时 gap 仍趋 2。

构造 (Q_{new}) 为 (Q_{old}) 与 `Rfill` 的均值。`Rfill` 随机选择一个 (B)、一个大小至多 (s) 的 home 子集，并选择 unit/no-unit，使低层状态提供足够质量。对任意具体 (S)（(|S|\le s)）使用有限差分系数
\[
 b_S=(-1)^{s-|S|}\binom{k-|S|-1}{s-|S|},
\]
恒等式
\[
 f(1,\ldots,1)=\sum_{|S|\le s}b_Sf(1_S)
\]
把 H 的整行值改写为一批具体合法 CONFIG。由于 (|b_S|\le A_{\max})，而 (M-1\ge4kZA_{\max})，修正后所有配置质量非负；每个 (C_{j,S}) 负载为 (1+|S|/k\le T)。这证明每台机器总次数至多 (d) 的整行矩与全局 (F) 一致。

固定 (B) 的 Qold 系数界再给
\[
 E_{Q_{new}}[(T-load_B)q^2]\ge\|c\|^2/(60Lk^4),
\]
而 H 的负下界仍为 (-2\|c\|^2)。选择 (M-1\ge120Lk^4) 后，条件于组件的方差分解给所有全输入 affine q 的 localizer 非负。每个固定 (d) 的 CONFIG 列表、degree-(D) 矩和 localizer 条目可按显式输入长度多项式生成；复杂度中的指数只依赖固定 (d)，不能改写成 (d) 作为二进制输入时的统一多项式。

正文明确保留更强系统的边界：对 (A_i) 与 (B_{i,b}) 的 incoming unit 指示，已有
\[
F[A_iC_{i,b}(T-load_B)]<0,
\]
所以加入有效的跨行二事件容量条件会切掉本点；自然 degree-((d+1)) 延伸也给出正的 mixed (R_j\prod Y_\ell) 而合法 CONFIG 给零。该事实说明行度 (d) 的合同仍不是任意更强高阶/跨行系统的全称间隙。

# 二、稀释终端探针合同及其精确失败

## 5. 逐边 LST 和重备选星匹配

第二源首先固定目标 (T) 和当前可用域 (D_j=\{i:p_{ij}\le T\})。对当前边 (e=(i,j))，定义所有其它任务 \(\ell\) 的大替代集合
\[
 F_i(j)=\{\ell\ne j:i\in D_\ell, p_{r\ell}>T/2\text{ 对所有 }r\in D_\ell\setminus\{i\}\}.
\]
将这些任务与其备选机器构成二分图，令 (W_i(j)) 为最大权部分匹配的收益；仅当
\[
B_i(j)=p_{ij}+\sum_{\ell\in F_i(j)}p_{i\ell}-W_i(j)>T
\]
才删边。若有真实 (T)-可行调度把 (j) 给 (i)，其余 (F_i(j)) 中被移走任务因每个处理时间严格大于 (T/2) 必须落在互异机器，形成合法匹配，故该调度的 (i) 负载至少 (B_i(j))。因此批量迭代安全；严格 (>T/2) 不能弱化为 (\ge T/2)。每轮至多 (mn) 个匹配和至多 (mn) 个删边轮次，位复杂度相对于展开输入多项式。

## 6. 终端容量稀释族

固定 (k\ge4)，令
\[
q=\frac{k}{k-1},\quad \alpha_r=\frac{q^{r-1}}{k-1},\quad
h=\min\{r:\alpha_r\ge1/2\},\quad N=k(k-1),\quad T=1+1/k.
\]
有两棵相同的 (k)-叉根树，层内边任务父端为 (1/k)、子端为 1；根间 bridge 在两根为 1。每个底层父 (v) 有 (N) 个专用终端，(k) 个普通任务 (b_\ell) 在 (v) 为 (1/k)、在各自终端为1；另有 (N-1) 个阻塞任务，每个在该组全部终端耗时1。树间和终端组相互独立，有限边只有 (1/k,1)。

若某实际调度峰值小于 (2-1/k)，bridge 使一根活跃；活跃父若只下传至多一个子任务，会留下 (1+(k-1)/k=2-1/k)，故必须继续产生活跃孩子并最终到一个底层父。底层终端因 (N-1) 个阻塞任务占据 (N-1) 个 unit slots，至多一个普通任务能去终端，底层父至少保留 (k-1) 个小任务，得到同一矛盾。路径调度达到 (2-1/k)，所以真实 OPT 恰为 (2-1/k)，而 (OPT/T=2-3/(k+1)\to2)。该族是显式有限 UM 实例；(h) 随 (k) 增长，正文不把其展开规模写成关于 (log k) 的多项式归约。

配置 LP 证书在树上按递推边际构造，根 bridge 的两端边际各为 (1/2)，终端组把普通任务和阻塞任务分配到配置列，所有配置负载不超过 (T)，任务覆盖和机器归一成立。对每条有限边，正文还分别构造普通剪枝 LST 证书：默认大端、按终端剩余容量比例填阻塞任务；固定被探测边时重新分配剩余阻塞任务，仍不超过 (T)，并令该边质量恰为 1。每个 LST 点是独立的，未声明共同分布。

在 (1/k<T/2<1) 下，星匹配过滤中的大任务集合只含耗时 1 的边。树内、根、终端的备选均可分别匹配到互异机器，得到 (W_i(j)=\sum_{\ell\in F_i(j)}p_{i\ell})，过滤式只剩 (p_{ij}\le1<T)，所以首轮无删边，迭代固定。机制是：每个独立 LST 点可以借用每组 (N(T-1)=k-1) 的分数余量，但配置证书把终端阻塞任务当作不可共享的 unit slots；星匹配只保证替代机器，未保留联合终端容量。

## 7. 加入大边基数不等式后的准确修复边界

第二源再加每台机器和候选目标 (C) 的有效线性约束
\[
\sum_{j:p_{ij}>C/2}x_{ij}\le1.
\]
在同一条件化 LP 内对每条边强制 (x_{ij}=1)，逐轮删不可行边。对上述终端族，它准确拒绝 (C<OPT=2-1/k)：(C<1) 时 bridge 无域；(1\le C<2-1/k) 时每终端的 (N-1) 阻塞任务占去 (N-1) 个大边槽，只剩普通任务总质量至多1，强制底层父接收其大入边后必须承担至少 (k-1) 个普通小任务，负载超过 (C)，删除逐层上传直到 bridge 失去两端。若 (C\ge OPT)，真实最优 0/1 调度同时证明配置和每条强制边的条件 LP 可行，安全性保证不删边。

该结果是本族的准确识别，不是一般 LP 求解器或一般近二算法；正文明确保留“配置可行性 + 同一条件内的大边基数/容量不等式”作为可能修复路线。

## 8. 共享小端逃逸扩展

第二源后半段另立 `UM-DILUTED-ESCAPE-PROBE-GAP-v1`。在每个终端组增加一台共享机器 (z)，所有阻塞任务在 (z) 的时间为 (1/2)，其余任务在 (z) 不可用。阻塞任务因此有 (N+1) 个端点；该族不承诺每 job 只有两或三条边。

对 (B<2-1/k) 的调度，bridge 激活一棵树；每个活跃内部父必须至少激活两个不同孩子，(h\ge3) 保证至少四个活跃底层父。每个底层组的 (N-1) 阻塞任务和至少两个普通终端任务一起迫使至少一个阻塞任务去 (z)；四个活跃组则使 (z) 负载至少 (4\cdot(1/2)=2>B)。因此 OPT 下界仍为 (2-1/k)，底座路径调度给出上界。配置证书在 (z) 取空配置；新增 (z) 边的逐边 LST 证书把该阻塞任务固定在 (z)，并在终端剩余容量中重新比例填充其余阻塞任务。

GHMR 首轮仍无删边：在 (T=1+1/k) 下耗时 1 是大边，(1/k) 和 (1/2) 是小边；树内大边的替代任务可匹配到互异孩子/终端，终端的大边查询无需替代，(z) 不承载大边。即使额外检查 (z) 的阻塞任务也可逐组匹配至终端，无法表达共享容量的联合拥塞。原重备选星匹配同样零删边。该扩展证明把配置、逐边 LST、GHMR 和星过滤同时通过仍不足以修复共享逃逸。

## 9. 证据和准确有限范围

已有《稀释逃逸行度与共享终端局部审计》已登记 k=4 完整展开的 427 台机器、521 个 job、4914 条资格边、(T=5/4)、构造值 (7/4)、逐边 probes、GHMR/star 证书，及 row-degree 四个有限案例、k=2 50 维 frame；《稀释终端独立重放与探针缺口有限审计》又登记 k=2/3/4 的 all-edge probe、k=4 独立重算和 k=2 双路径字节重放。本批当前正文提供的是这些有限审计背后的解析量词和扩展边界，不重复把有限输出升级为通用证明。

第一源的 k=2 finite audit 只枚举 121 个 weighted H/Q states、50 维 Gram/LDL；固定行度扩展的四例 ((d,k)=(2,2),(3,3),(4,4),(4,7)) 只逐枚举至 d 阶 square-free row monomials，不能替代任意 d、k 的解析推导，也没有 global (M_2) 或全局 localizer 枚举。第二源的脚本展开和 exact Fraction 核验限于 k=2,3,4，k=4..64 只做压缩公式检查；它没有把所有 k 的完整 assignment 展开，也没有实现一般 LP 求解器。软件 replay/byte identity 是可复现性证据，不是独立数学证明。

# 三、交叉处置和接续义务

* raw K2 的 first/pair CONFIG、固定行度的整行矩与终端探针的逐边 LST 是三个不同合同。不能把 per-machine CONFIG 分布自动视为共同全局分布，也不能把独立条件点拼成配置容量守恒。
* raw K2 和行度扩展都通过显式有限法则生成共同 (F)，但已知跨行二事件会给负 localizer，下一混合阶自然法则也被合法 CONFIG 切掉；加入这些更强有效约束后的 gap 必须另审。
* 终端探针族的星匹配安全性是必要条件算法；加入同一条件 LP 内的大边基数约束能在该族上准确识别，但没有一般 soundness/rounding 证明。共享小端 (z) 说明把 GHMR、配置、独立 LST 和星匹配叠加仍可能留下 gap；同一条件内的联合容量账本是后续义务。
* 两源都保留 raw/探针族的“原模型反例”身份：它们是普通 UM 的显式整数矩阵族，说明某个精确定义的松弛或前处理合同不足；它们不是 UM-TARGET-v1 的 hardness，也不触及六人 SPE 的覆盖 half 目标。
* 继续工作应补全更强系统的定义域、共同配置变量或跨行容量条件，给出真实输入到 witness 的统一解码，并区分显式展开复杂度与参数 (k,d) 的压缩表达；外部文献优先权和论文新颖性仍未认证。

# 来源去向

`9739957574111e83579a` 的 raw K2 v1、固定行度 (d) 扩展、精确真实 OPT、共同有限法则、CONFIG/affine-localizer 证明、缩放和证据边界均整合到本审查；原有有限审计继续保留其代码、运行和 replay SHA。`07f075f376fc5aa958fe` 的终端稀释引理、配置/逐边 LST/星匹配共同间隙、含大边基数的准确探针修复，以及增加共享小端 (z) 后的 GHMR/star 零删边扩展均整合到本审查。没有成熟内容因“不在主线”而丢弃；未证明的更强系统、一般算法、hardness 和六人 SPE 关系明确保留开放。
