# Santa 受限桥与归一化菜单双源审查

## 来源身份与阅读范围

本批完整读取并比较两个冻结来源：

- `ba67e7eebfe21013c7ae`，`research/current/unrelated_machines/santa_restricted_bridge_boundary.md`，blob `141ef70391270288d7dc61c30e2f1fd263570c43`，SHA-256 `4897f3af52d7c51085fcdff6195d616493b4a5913660291298e41efea2a5d366`；
- `737121825175bccceb42`，`research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md`，blob `8222ee967d0e2b85a942cfd4723dcac80bcf63a4`，SHA-256 `ce1c320ecd4d3833030307e4b4e3f4959ecd187281187c5914e80bddae8d13c5`。

两源均冻结于 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。同时读取了 Santa 条件反面、BLMRS/Haeupler–Saha–Srinivasan 文献事实、需求树桥梁、归一化 menu、XOS 规模障碍及相关审查。第一源关闭“restricted Santa 可直接接需求树桥”的模型误读；第二源给出一般加性菜单到 Santa 的精确值桥、实际 UM 调度互逆和同资源宇宙的逐玩家菜单规模下界。

## 一、restricted Santa 与需求树桥梁不保真

一般 max-min allocation 允许任意非负有理 (v_{ci})；restricted Santa 要求每个物品有固有值 (p_i)，所有非零端点均等于 (p_i)。Haeupler–Saha–Srinivasan 的 restricted 结果和 BLMRS 对一般 Santa 的开放问题不能混写。

需求树桥梁中正需求点 (v) 的外送任务在父端处理时间 (1/k_v)，在孩子端为1；只要某 (k_v>1) 且 (d_v>0)，同一物品就有两个不同的非零端点，不存在单一固有值。最小反例是 (k_v=2,d_v=1)，端点值 (1/2,1)。因此桥梁输出一般 max-min/不相关机实例，而不是 restricted Santa。若强行要求所有 (k_v=1)，矩阵才进入 restricted 类，但需求出度退化为至多一，树评分仅有0或1，无法表达近二路线所需的连续需求层。

准确后果是：restricted Santa 的常数算法既不能直接给一般 UM-TARGET 正面算法，也不能替代 Santa 条件反面中的一般 max-min 无常数假设。任何 Santa 归约必须逐任务核对所有有限端点的非零值，而不能只核对支持图。此处是模型边界证明，非一般 hardness。

## 二、归一化完整菜单的精确值桥

`UM-WEIGHTED-MENU-STATE-DUMMY-SC-v1` 的输入是有限 groups (G)，每组 (K_g\ge1) 个 indexed states；每 state 的资源集 (S_{gs}) 上非负有理权总和恰为1，state 有 private parent、每个资源有真实资源机，selector 只能去本组 state parent，incidence job 在 parent 用原权或在资源机用1。定义
\[
a_{gs}(B)=\sum_{u\in B\cap S_{gs}}p_{gsu},qquad f_g(B)=\max_s a_{gs}(B),
\]
\[
V=\max_{B_g\text{ pairwise disjoint}}\min_g f_g(B_g).
\]

构造 Santa：每 indexed state 成为一个 agent；原资源是 real item，价值为该 agent 的权；每组增添 (K_g-1) 个只对本组 state agents 价值1的 dummy items。每个 Santa 分配至少 (t) 的分配，在每组 (K_g) 个 agents 中必有一个没有本组 dummy，因而其 real bundle 给出 (a_{gs}(B_g)\ge t)，且不同组 bundle 不交。反向从不交 bundle 选达到 (f_g) 的 state，把其资源 incidence 导出到真实资源机，其余 incidence 留 private；峰值为 (2-a_{gs}(B_g))。于是
\[
\operatorname{OPT}_{SC}=V,qquad \operatorname{OPT}_{UM}=2-V.
\]
对任意给定 (t\in[0,1])，Santa 存在所有 agent 效用至少 (t) 当且仅当原 UM 存在峰值至多 (2-t) 的完整实际调度。(V=0)、(V=1)、(K_g=1) 和峰值2边界均由同一互逆证明覆盖；不输入未知 OPT，也不复制同一组多个 state agent 的资源。

这是一条精确条件编译，而不是 source hardness：一般 additive 源必须已经满足每 state 总权1、完整 state 显式列出、资源不可拆和非负值。若源只有 (W\le1)，需在增广资源上重定义 (V) 后再用桥；保留旧未增广 (V) 会错，例如零工作 state 可能给 (V=0) 而 UM 最优为1。

## 三、逐玩家归一化菜单的规模障碍

`UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2` 固定 (U) 为 (2t) 个资源，(d=\lfloor\eta t\rfloor)，(k=\max\{1,\lceil d/\eta\rceil\})。每个显式 clause 在全部 (U) 上总权1，要求每个 (t)-子集 (T) 的 max 值为1，而每个不超过 (d) 的集合值至多 (eta)。令 (Theta(2t,t,k)) 为最小 (k)-子集族，使每个 (t)-集包含某个族成员，则
\[
K_{\min}=\Theta(2t,t,k),qquad
K_{\min}\ge\frac{\binom{2t}{t}}{\binom{2t-k}{t-k}}.
\]
任意菜单可把每个 clause 的 support 规约为 (k)-子集上的均匀 (1/k) 权；反向覆盖族直接给菜单。锐端点为 (d=0) 时 (K_{min}=t+1)，以及 (eta t\) 为正整数时 (K_{min}=\binom{2t}{t})。固定 (eta) 且 (d\ge1) 时，(K_{min}\ge4^t/((2t+1)(2t)^c))，其中 (c=\lceil1/\eta\rceil-1)。

计数依赖全部 (t)-子集阈值、非负归一化显式 clauses 和同一资源宇宙。它排除逐玩家、同资源、完整保留所有 subset 阈值的低规模 XOS shortcut；不声称 (2^{\Omega(\text{源位长})})，不排除辅助资源、全局耦合、部分完备性、隐式表示或允许改变源义务的归约，也不是一般 Santa/UM hardness。

## 比较、证据和第三阶段接续

restricted-bridge 来源独有的是端点值 (1/k_v:1) 的逐任务模型反例、(k_v=1) 的退化边界和对 Santa 文献适用范围的纠正。归一化 menu 来源独有的是 exact value bridge、给定 allocation/schedule 的可逆构造、dummy-free agent 证明、(V=0/1) 边界和 XOS menu 的覆盖数锐界。两源共同要求保留完整 state 身份和实际资源互斥，不能把支持图、局部 restricted 价值或分数边际当作全局解码。

有限脚本与文献事实只作证据；归一化桥的公式和覆盖计数为一般结构证明。后续 mapper 应检查：每个 state 是否总权恰1、所有资源是否在同一显式宇宙、是否错误采用 restricted Santa 算法、以及源的 NO/YES 是否真的在同一 (V) 桥上保持。两源不包含客户目录、六提供者历史、终局均分或任意平局语义，`UM-TARGET-v1` 和六人 SPE 覆盖目标保持独立开放。

## 处置

两源均 `integrated`。第一源写入 restricted 模型边界与需求树不保真证明；第二源写入精确 Santa 值桥与逐玩家 XOS 规模障碍。条件结论、一般证明、有限证据和未闭合义务已分开记录。
