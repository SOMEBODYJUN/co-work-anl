# 七态原星规范 v2：最终全文实读及四条范围核对

2026-10-18，scratch 最终 actual-read 记录。正文只读，未改 repo、未做 Git 或登记。本票不改原 Exact-first、作者读后或新边界的任何冻结字节。

## 1. 最终目标与实际阅读顺序

实际目标是 `co-work-anl-boss11/research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md`。

我先实际全文读旧版 180 行、18172 bytes，读取时核得 SHA256 `1c2053ae9bc95b7fb575fd22176dc8db4cb4f25035d5f8f41c6fe2cf5884a30b`。root 随后通知其三处修正。此后我又从第 1 行到第 180 行完整读取新最终正文，核得：

SHA256 `218a5c4e5b346c8c4816b609a98073958186cb222390839b54229aa5c4beecb6`；18177 bytes，180 lines。

本票对新 218a5c 是全文实际阅读，不仅三行定向阅读。新旧完整 diff 另逐项核过；将下面三个改动精确反向恢复（保留旧第 106 行两个空格）后，旧字节的 hash 重新精确为 1c2053，故没有其他字节改动：

1. 第 13 行 `Lhat(X−f)²=0` → `Lhat[(X−f)²]=0`。
2. 第 106 行 `      <  (eta/40) sum_(five classes) q_class^2.` → `      <= (eta/40) sum_(five classes) q_class^2.`。
3. 第 154 行 `Lhat(X−f)²0` → `Lhat[(X−f)²]=0`。

两处 Gram 修正明确了平方在 functional 内。Cauchy 改为非严格号正确处理五个 q_class 全零的情况，不改变结论。

## 2. 我的审查身份和未读范围

kernel 的先行记录是仅看原 Exact 939a 的 224 行独立重构 7d61，随后才实际全文读 86 行作者 Proof d560，另冻 100 行读后 7549。这两个旧记录及其阅读顺序未回写。

仿射分类和 AND 边界由我写作者 Exact/Proof，并已与 root、global 交流，所以我在这两项上是知情作者的最终正文核对，不是新的独立审查者。其 literal 先行及作者读后的身份不由本票冒领。

新 §7 的 root 原 Exact、global 的 65 行先行稿、root 递归 Proof、相关 29 行读后记录，我本轮均未打开。这里只依据新正文的 Fisher–Yates/消列证明独立核其完整算法与位复杂度，不代签这些 source 文件。

没有打开或运行 §6 的 audit 程序/JSON，也没读审查链接下未交给我的其他材料。正文关于 root 的源码全文阅读、fresh CLI、12 参数、3 个 small 全矩及输出字节一致性的陈述，是正文/已有消息报告；本票不将其记为我的软件执行或源码认证。

## 3. 四个对象的范围划分

全文明确分出以下身份，未把它们当作同一个算法或硬源：

* `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2`：原 OPT=1 小星的同一真实 law/M3/全部 global q2/row CFG pair，新增显式有限配置支持的总位生成。
* `UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1`：所有显式 d、0≤h≤d 的定基数 first/pair 稀疏支持；不是高阶矩或共同 law 稀疏化。
* `UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1`：base≤4、共同 M3、线性 Gram 关系下的 covered endpoints 分类和条件 owner 界。
* `UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1`：base≤5、共同 M3、忠实二次 AND Gram 关系、原 v load 不变时的负 q2 见证。

新 LOCAL-v2 支付了比旧 kernel Exact 更强的显式配置输出，不倒改旧 Exact 或旧审票。辅助 Claim 对 d=1、h=0/d 也陈述边界；原星仍只对偶 d,s、2≤s≤d/2。

## 4. 原 jobs、共同 PSD 和全部 global q

全部有限处理时间确为 R 在 u/v 时间一、各不同 j_l 在 v 时间 1/d 或其不同 z_l 时间一；其余无穷。每个 P 样本完整执行所有原 jobs，没有匿名 token、拆分或侧约束。R 给实际 OPT≥1，全部 jobs 回 home 给 OPT≤1。

七类质量均正且总和一，真实 P 给全部原 Boolean/one-hot 和共同 M3。P 的坏样本峰二，概率 p=η³/1000；这是归一参数 η 的维数无关表达，不是实际 near-two gap。

任意全局原二次 q 用端点仿射代换仍是 C,Y 上的次数二函数。正 slack 类别的 Jensen 与坏类别全一的置换不变性覆盖非对称部分，未遗漏其他机器变量。对称均值的 active/inactive 二次项系数相同，五点评估恒等式及系数平方和 4λ²−4λ+3≤16/η² 正确。每个对应正权≥η/40，而 16η/1000≤η/40，故新版非严格链对包括 q=0 在内的所有实 q 成立。其他原机器逐样本负载≤1，因此全部机器使用同一个 L 的 global q2 检验通过。

v 行 pair trade 用 C,H,CH,H(H−1) 四统计量，损失 p d(d−s) 与增量 u0d²/4 精确抵消，包含所有原对角及异 pair。u/z 的 Bernoulli 配置支持合法；没有将这些逐行 law 拼称另一个共同 assignment law。

## 5. 新 §7：自足算法核查

对 h-subset A，φ(A) 包含常数一、d 个 singleton 和 binom(d,2) 个异 pair，D=1+d+binom(d,2)。标签置换在线性特征空间中只是坐标置换。

从单个 A0 出发，依次 i=d,…,2 均匀交换标签 i 与 j∈[i]，完整过程产生 uniform permutation，所以原未压缩过程最终产生 uniform h-subset。每个阶段的期望是固定线性算子，因此在阶段末仅保 φ 均值不影响任何后续阶段的最终 φ 均值。这一理由足够，不要求保留完整阶段分布。

阶段入口支持≤D，展开仅有≤iD 个实际 h-subsets；无需枚举全部 binom(d,h) 集合。候选>D 时，从至多 D+1 列选有理依赖并取整数依赖 u。可先精确求独立列/行，再用基本依赖的 minors，0/1 矩阵的 Hadamard 界给非零系数位长 O(D log(D+1))，且该求法有确定性多项式位成本。

常数坐标迫 Σu=0，所以非零 u 有正负号。以同分母正权 a_l/Q 表示，选正 u_k 中最小比 a_k/u_k。正文更新

    Q'=Q u_k,  a'_l=a_l u_k−a_k u_l

保证每个 a'_l≥0、Σa'_l=Q'、至少 k 项为零，且 φ 均值保持。依赖范围外可令 u_l=0，更新同样保持其权值。移除零项后反复进行，最终支持≤D，保留的每项都是已展开出的实际合法 subset。

各阶段至多 iD 个候选，消列总数 O(d²D)。分支共同分母只乘 i，全部阶段成本 log(d!)；每次消列分母只乘 O(D log(D+1))-bit 的正 u_k。故总位增量 O(d²D² log(D+1))，分子在 0 与当前分母之间，同样为 poly(d)。所有整数消元、比值比较及 subset 列表存储都在多项式总位成本内；没有 quadratic pricing 或 oracle。

d=1 无异 pair；h=0、h=d 可直接输出唯一集合，不出现 pair 分母的边界问题。最终 singleton 为 h/d，存在异 pair 时为 h(h−1)/[d(d−1)]。所以辅助 Claim 对其完整输入域成立。

## 6. 显式 row CFG 与全部矩的总位输出

对 K_v 的六个固定 (C,H) 类别分别调用 §7。每类 C/H 固定，payload first/pair、CY pair 及实际负载全部保持；每类至多 D 个实际 subsets，故 K_v 至多 6D 个真实原配置及有理权。类别质量本身只有 O(log d) 位，与 §7 权相乘仍为多项式位长；每配置可显式列原 job IDs。u/z 两点 Bernoulli 支持同样可明确列出。

共同 L 仍是七态 uniform-subset law。用下降阶乘及固定次数补端点展开，可生成全部次数≤6 原矩；变量数 O(d)，矩个数 O(d^6)，每个 fixed-degree 矩有理位长 O(log d)。负载二次局部化 entries 次数至多五，同样可精确生成。显式原输入已包含 d 枚 jobs，故这是相对于实际输入长度的确定性总位多项式输出，不是关于 log d 的时间声明。

稀疏配置只保 row first/pair，未替换共同 L，也不保三阶以上矩；两套对象在正文中区分清楚。§7 新增输出主张因而获得自足证明，无需依赖所述未读 source 或未运行软件。

## 7. 仿射/AND 边界、外部压力与证据顺序

§8 的实系数分类完整覆盖 h=1、d=4 及 h=d/4；两系数层的 subset 计数宽度、唯一低层在全一处取值≥3 的排除均正确。共同 M3 的线性零向量与 degree≤3 正交，支付四次幂转移及 E_P[(f²−f)²]=0；base≤4 与非负真实期望恰好足够。同行 pair 只约束被覆盖的不同原 jobs，最多两个正 owners 时必须互补；没有扩大为全部原资格度。

§8 的随机 β 例子确实用 N 枚不同原 unit jobs，各只有公共 w 和 private u_a 两端，完整分配。每个背景一个可能 owner，积分后 N 个正边际但 pair 仍零，正确限制了条件结论的范围。未条件化 M3 不被免费当成任意条件点。

§9 保持 base≤5 与原 v 负载公式，先以 Boolean Z 降 q²，再将二次 Gram-null 乘 degree-three Q，最后只用第五次基础矩，严格得负值。Z 是新增真实端点/明定 Boolean 坐标，没有仅把 CY_i 改名后降次数；物理例子不把 AND 当成 UM 资格强制逻辑。该边界不排全部非仿射依赖。

§5 已将此前作者稿需澄清的 v 无新增 payload 条件写实；孩子 payload 和合并 unit 头的压力有明确负值/pair 说明。各行共同收费、递归 law 和实际低载调度 decoder 仍被保留。

§10 中我本人的 kernel 先行/作者读后顺序与实际一致，且把 root 的插值参与记为非另一盲审。其他先行记录在正文中被分开列明，未用我的本轮 final-read 替代其独立性；我未打开那些原件，不额外认证其字节/过程。软件身份与数学证明分开，本文也未声称软件实现 §7 或递归。

## 8. 最终结论

对最终 218a5c 正文所列四个精确范围，未发现仍成立的 fatal；全部数学证明及新 §7 显式总位生成在正文中自足。原输入 OPT=1，不能据此称 relaxation gap、hardness、general UM 算法或 growing-depth 共同证书。本人对两条新边界是作者读后核对，对 §7 是首次完整正文攻击；软件和未读来源均未代签。旧冻结文件保持原样。
