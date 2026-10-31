# 单根树全局重数的精确 CONFIG gap：陈述先行独立重构

本记录由内部研究者 pcsp_occurrence 写于 scratch；不操作 Work、Git 或公屏。只读了作者 Exact 文件，未读作者证明、cover 稿或 root 推导。已知背景是旧 raw-q 子可加、三叉 rainbow NP 锚点；下面仍把用到的子可加性与实际 P 回算重新给出。没有新颖性认证、没有软件运行认证。

实际读取的 Exact 文件：`single_pinned_tree_multiplicity_exact_gap_v1_exact_statement.md`，SHA256 `32469690f6f96128c1e56a9080787f83345553623492e18819f29a600f7b692b`。

Claim ID：UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1。

结论：**独立重构闭合；未发现 standing fatal objection。** 以下构造只需在每个最底 internal parent 的 d 个叶孩子里按 µ 个一组重色，不需要跨层复杂标签。

## 1. 所有 U 的真实 OPT 公式，包含全部 jobs

固定输入完整 d 叉树（d≥2，h≥1）。令 q 为其最大 rainbow 满 q 叉、同深 rooted 子树分叉数。任取一条 root-leaf 路径已经给 q≥1。

给定一个 rainbow 满 q 叉见证，把且仅把其中树边 jobs 向下安排：internal child 端 time1，leaf color 端 time1；其余每枚树边 job 全部安排在原 parent，time1/d。root pin 安排在其唯一 root 端。于是：

- root 和每个 active 非叶 internal machine 恰有一枚 unit job（root 为 pin，其余为父边），以及 d−q 枚留在本机的 small jobs，负载 `1+(d−q)/d=2−q/d`；
- 每个 inactive internal machine 收全部 d 枚本行 small jobs，没有父边 unit，负载1；
- 每个 color resource machine 收到至多一枚叶边 unit job，因为选出的所有叶色互异，负载≤1。

没有未安排的树边、没有复制 job；所有目的地都是原 P 的合法有限端。因此 OPT≤2−q/d<2。

反向取任意完整实际调度，若 C≥2 则自然 C≥2−q/d；只需看 C<2。每个资源 machine 至多收一枚 unit 叶 job；每个 internal machine 也至多收一枚 unit incoming job。root 由 pin 保证 active。任一 active internal machine 最多留 `floor(d(C−1))` 枚 small，故至少

\[
r_C=d-\lfloor d(C-1)\rfloor=\lceil d(2-C)\rceil\ge1
\]

枚 child-edge jobs 向下。逐 active node 留其中 r_C 条，得到 full r_C 叉深 h 子树；所有其叶 jobs 在实际 σ 中都到 color resources，各颜色至多一次，故 rainbow。于是 q≥r_C≥d(2−C)，即 C≥2−q/d。结合正向得到所述精确等式。

## 2. 全局重数界和确定性真实 σ

设实际最大颜色出现次数 m≤µ。对每种颜色的各次 occurrence 确定性排序，把其第 j 次放入 bucket j。只用 m 个非空 bucket；每个 bucket 内所有叶色互异，且各 bucket 分割全部叶。

为叶子集合 S 定义 raw q(S)：最大的 r∈[0,d]，使 S 含一个 full r 叉、深 h 的 rooted 子树的全部叶；不存在路径时为0。高度0处的 DP 值取 d（叶属于 S）或0（不属于 S）；更高 node 的值为其 d 个 child 值的 h-index，即最大的 r 使至少 r 个 child 值≥r。此 DP 及见证抽取不求解 rainbow 难题，因为 S 已固定。

可从此 DP 自足证明 `q(A∪B)≤q(A)+q(B)`。设右边 a+b<d，若左边≥a+b+1，存在 a+b+1 个 child 的 union-rank≥a+b+1。按归纳，每个这类 child 的 A-rank≥a+1 或 B-rank≥b+1；但 root A-rank=a 说明前者 child 至多 a 个，后者至多 b 个，矛盾。a+b≥d 时不等式直接成立。高度0的0/d值也直接满足。

全叶 rank 为 d，所以 bucket ranks 之和≥d，至少一 bucket rank≥ceil(d/m)≥ceil(d/µ)。该 bucket 的见证本来 rainbow；按 §1 输出所有 jobs 的实际 σ，得到

\[
C\le2-\lceil d/\mu\rceil/d\le2-1/\mu.
\]

实现上可对每个 bucket 顺序做 DP，仅枚举实际存在的 m≤叶数个 bucket；总时间多项式于显式树/颜色 ID 的输入位长。µ 若二进制巨大也不按 µ 循环。每个树边/实际 color resource 和 root pin 都在输出中有一个确定目的地，Fraction 负载可逐机回算。ceil(d/µ) 用整数算术；不求未知 q_rainbow。

## 3. 独立下界族

固定 µ≥2、d≥2 且 µ|d。设 r=d/µ。对每个 depth h−1 的 internal node w，将它的 d 个叶孩子分成 r 个 block，每 block 恰 µ 叶，使用一个颜色 c_(w,b)。不同 w 或 b 的颜色 ID 均不同。

每个颜色在整个 ambient U 恰出现 µ 次，所有底层 parent 的颜色 palettes 两两不交。任何 rainbow 满 s 叉树在最后一层都必须从某个 parent 取 s 个不同颜色，故 s≤r。反之在所有非底层 active node 取任意 r 个孩子，最底层每 block 取一个叶，得到 full r 叉 rainbow 深 h 子树。故 q=r，实际 OPT=2−1/µ。

这适用于 h=1：只有 root 一个底层 parent，无额外层被假定存在。

## 4. 最小 Tconf 准确为 1+1/d

令 α=(d−1)/d，t_l=α^l（l=0,…,h）。若 µt_h≤1，以下是 **完整普通 configuration 证书**，不是仅 fractional load。

对 depth l 的每个 internal machine（root l=0）：

- 概率 `1−t_l` 取其 d 枚 child-edge small jobs 全集，load1；
- 对每个 child j，概率 `t_l/d` 取 incoming unit job 加恰好第 j 枚 child-edge small job，load1+1/d。root 的 incoming 是其单端 pin；其余 incoming 是原父边 job。

概率总和1。root 的第一种概率为0；pin 恰被覆盖1。父行 depth l 的任一 child edge 在 parent-small 端的边际为

\[
(1-t_l)+t_l/d=1-\alpha t_l=1-t_{l+1}.
\]

其下端（internal child 或 color resource）的边际为 t_(l+1)，故每枚原树边 job 两端边际合计恰1。

每个 resource 对其 µ 枚叶边 job 各取一个 singleton 配置，权重 t_h；取 empty 配置权重 `1−µt_h`≥0。全部 singleton load1。其概率和为1，且每枚叶边下端边际正是 t_h。因此 certificate 覆盖全部 jobs 且每个配置实际 load≤1+1/d。

为证最小性：T<1 不可能覆盖 root pin。对于 1≤T<1+1/d，任何可含 root pin 的配置均不能再含任一正 small job。因 pin 仅此一端，root 每个正权配置都含 pin，故所有 root-small 边际为0，其 d 枚边 job 必须各在下端边际1。递归，每个 internal child 的父边 unit 边际为1，正权配置均不能含 small，故所有后代树边的下端边际仍为1。最后每个颜色 resource 的 µ≥2 枚 unit jobs 都要求边际1，但 T<1+1/d≤3/2<2 使其任一配置最多含一枚 unit，矛盾。

此必要性也适用于普通 LP 用 coverage≥1 而非 =1 的惯例：唯一端 pin 和递归单个下端边际都至多1，故被迫等于1；不需要预先假定额外的 equality 归一化。故 Tconf=1+1/d。

配置数为每 internal node 至多 d+1、每 resource 至多 µ+1，总量按显式边/叶数多项式；t_l=(d−1)^l/d^l 的编码位长 O(h log d)。底层颜色 ID 可用二进制 parent/block 序号。没有声称从 binary(d,h) 快速展开 d^h 的树。

## 5. 高度条件、上确界与 µ=1

作者给出的充分选择 `h=d ceil(log2 µ)` 有效。对 d≥2，

\[
((d-1)/d)^d<1/2,
\]

例如对倒数用二项式下界 `(1+1/(d−1))^d≥1+d/(d−1)>2`。令 L=ceil(log2µ)，则 µ α^(dL)<µ2^(−L)≤1。这里仅是存在族的高度公式，不引入浮点判断；L 可由整数 bit-length 正确计算。

全类 Tconf≥1，由 §2 直接得 OPT/Tconf≤2−1/µ。上面 d 为 µ 倍数、d→∞ 的族有

\[
\frac{OPT}{Tconf}=\frac{2-1/\mu}{1+1/d}\longrightarrow2-1/\mu.
\]

所以 sup 精确，不要求某个有限 d 达到该 ratio。

µ=1 时所有叶色全局唯一，整个 full d 叉树 rainbow，q=d，§1 给真实 OPT=1；root pin 给 Tconf≥1，实际 σ 自身给 CONFIG1，故 OPT=Tconf=1。无需把 µ≥2 族在 µ=1 的无意义 µ 重色步骤里硬套。

## 6. 独立审查状态与范围

- Exact 三部分及所有列明边界均有以上自足重构；没有 standing fatal。
- q_rainbow 精确值一般仍 NP-hard；本页多项式算法只保证 ceil(d/µ) 分叉，未声称计算最优 q。
- global whole-tree multiplicity 是每个颜色在这同一棵完整输入树的总出现数。不能改成 per-state multiplicity 后把结论直接用于多状态、多 root 同资源森林。
- 下界族本身可显式求解；其 gap 不给 hardness，不否定 UM-TARGET-v1。µ 不受常数限制时本算法的 epsilon 随输入变化。
- 未读作者 proof；可在本稿冻结后接收其字节供 read-after 攻击。本页不认证独立发表新颖性。
