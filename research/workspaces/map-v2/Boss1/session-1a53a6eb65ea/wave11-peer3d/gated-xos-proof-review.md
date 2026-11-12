# GATED-XOS-3D：当前三条 canonical 边的有界实质复核

身份：Boss1。日期：2026-11-12。只读来源：`/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1`。本报告是指定既有三边的 3D 数学复核，不是新主覆盖、原 owner 交付或 pending 清理。未读凭据，未运行 Git、队列、历史 LP/科学程序或巨大枚举，未修改 clone 中任何文件。

结论：三边确实连成同一个显式 norm1 gated-menu 问题。XOS 边准确支付福利舍入 **contribution/STEP**；值桥边在补足一般 LP、精确条件期望、平衡提取和全 jobs 回填后支付目标 **whole**；robust 边实际调用源合同内的福利保证而非仅调用最终 13/8 近似比，支付两种 NO 合同的完整判别 **whole**。本轮未发现需要修订这三条 canonical 边的承重数学缺口。`accepted / unconditional / premises_mode:all` 与它们各自写明的域、条件和作用范围相容，不能把 XOS 局部边提升为单独的 13/8 整条证明。

本报告 fresh 读取当前 registry 中四端点的完整记录、三 canonical 边全文，当前承重审查正文、作者 Proof v2 全文以及冻结 DNS PDF 的第 8–9 页。没有把 Root 以前对 `um-normalized-welfare-to-general-ratio-value-bridge` 的审读计入本次。也没有继承此前 worker 的“全文已读”作为自己的阅读。每份实际正文、完整 SHA 和精确章节见 `refs.json`；对 endpoint 内有限程序、其它不承重附件的 references，本次只知道其合同入口，没有逐个阅读或重跑。

## 1. 精确身份、归属和当前绑定

三条边都从本轮读取的 `research/registry.json.edge_files` 精确查找 edge_id 得到，未用同名旧路径代替。

| 简称 | canonical edge_id | 路径 | 作用范围 | exact asset 的当前 done owner |
|---|---|---|---|---|
| X | `xos-independent-coefficient-rounding-to-gated-menu-welfare` | `map/edges/boss2-wave10-repair-eb1e136b282488e4/xos-rounding-to-gated-menu-welfare.json` | contribution/STEP | Boss2，`boss2-wave10-repair-eb1e136b282488e4` |
| V | `um-3f8b771c-gated-value-bridge-to-full-unknown-opt-ratio` | `map/edges/boss2-wave10-repair-df322e0f83658554/gated-value-bridge-to-full-unknown-opt-ratio.json` | whole | Boss2，`boss2-wave10-repair-df322e0f83658554` |
| R | `um-3f8b771c-gated-general-welfare-proves-robust-two-threshold-decider` | `map/edges/boss2-wave10-repair-df322e0f83658554/gated-general-welfare-proves-robust-two-threshold-decider.json` | whole | Boss2，同上 |

归属依据是本地当前任务快照的 `state:done`、`owner:Boss2`、`edge_paths` 与该任务 receipt 的 `assets` 中**同一路径和同一最终 SHA**，不是仅凭文件夹名或 reviewed_by 猜 owner。两个 task 的嵌入 receipt 均与独立 receipt 的 JSON 完全相等。本轮没有访问远端，故这只是当前共享 clone 中可核的 done 状态，不冒称另作了实时远端验证。

三个 canonical 文件的原始 SHA256 分别为：

- X：`b26eac988482efd678d354ba6a133598ddbd14730f410918b0a3ca183970327f`；native pin `0a8b1049a48a5bae2221bbb9ce0268219307ed9125241413da697a546fba33e7`。
- V：`00c7519192725ccaf751c85edf67dc8b79c37bca8656a7807a59e1ff8c8bf29b`；native pin `48d6ce5c125e14fef7af8ce753f9cee7fe1f8125054e13416364f457ed67b16b`。
- R：`1aa4800ffdb247dd315e09500b71524be24e40f84924a92088b075095d3ddd05`；native pin `d49d3cdaffd5af34338206d202e070666978881d0c0cebc0217ba4e94c53f628`。

native pin 按仓库 `research_runtime.pin` 的规范 JSON 算法独立重算；与原始文件字节 SHA、去掉绑定字段后的 review_digest 分列。三边的 endpoint_pins 均等于当前完整 registry record 的规范 pin，每个 direct evidence 的完整字节 SHA 也与磁盘一致，review_digest 均可重算相等。这些绑定核对只证版本一致，数学判断来自后续推导。

四个完整端点合同是 XOS 文献对象 `M-8fdee11afd164305a429734ee5ae705a` v2，以及 `UM-NORMALIZED-GATED-MENU-WELFARE-v1`、`UM-NORMALIZED-GATED-MENU-13-8-v2`、`UM-NEAR-PERFECT-NORMALIZED-ROBUST-SOURCE-v1` 各 v6。完整记录和各自 pin 保存在 `refs.json`。

## 2. 共同模型与 ALL 前提

共同输入为 n≥1 个组，有限资源，每组非空有限显式 indexed states；每 state 的非负二进制有理系数 p 的和为 1。同一 state 的资源身份互异，允许重复 indexed states、显式零和 unused resources。真实 bundles 全局两两不交，`v_g(B)=max_s Σ_{u∈B}p_gsu`，因此 `0≤r_g≤1`。没有额外 coherence、标签相容或共享内部任务条件。

一般福利 LP 为

\[
\sum_s z_{gs}=1,\quad 0\le x_{gsu}\le z_{gs},\quad
\sum_{g,s}x_{gsu}\le1,\qquad L=\max\sum_{g,s,u}p_{gsu}x_{gsu}.
\]

x 只设在正 incidence 足够；若保留零项变量，它们不改目标和论证。该表示选择不能删除物理零 jobs。任选每组一个 state、令 x=0，总可行。任何真实 allocation 逐组选 attaining state、相应 z=1、所领正资源 x=1 可嵌入，故 `W*≤L`；`x≤z` 与 norm1 给 `L≤n`。标准显式有理 LP 给确定性总位多项式算法和多项式位长最优点；有限 SciPy/Fraction 审计不是该通用后端的实现证明。

unit-FSLP 是更强的另一合同：`Σ_s λ_gs=1`，每资源 `Σ_{g,s:u∈P_gs}λ_gs≤1`，P 为正支撑。它通过 `z=λ、x=λ` 给 L=n，但一般 LP 不要求它。三组各只有同一个 unit resource 的单 state 是一个无需程序的边界例：一般 LP 可行且最优 L=1，unit-FSLP 却要求列和 3≤1，因而不可行；完整 gated 的 β*=1/3、OPT=5/3>13/8，说明全类绝对峰≤13/8 甚至不可能。V 只取 WELFARE 合同中**不需要 FSLP 的值恒等分支**，没有把它的 FSLP 条件福利/绝对峰分支偷渡到全类。

三边各只有一个 source_id，ALL 在形式上没有被拆分。实质共同前提——正确模型、精确可行点/最优 LP、跨组独立、正概率条件化、完整 P_gate——都保存在其条件、说明和承重正文里。X 的给定可行点输入是局部算法合同；V 补付从菜单求最优点，R 则只需求精确最优 L 作比较。不能将这三种输入量词混写。

## 3. X：DNS 独立系数引理及目标分布的准确迁移

冻结 DNS PDF 第 8 页 §3.2 明示 pre-allocation、maximizing XOS clause 和逐 item 最大系数分配；同页保 demand 与 XOS-clause 两种访问接口，并明确一般 XOS 下不知能否只用 demand 模拟 clause。Theorem 3.2/Lemma 3.3 的逐 item 承重证明在第 8–9 页。X 迁移的是该证明中的独立系数不等式，并非免费继承一个一般 XOS oracle 算法。

固定一个资源 u，将跨组独立的非负随机系数记为 a_i。令 `X_i=Pr(a_i>0)`，`V_i=E[a_i]/X_i`（X_i=0 的项删去），并按 V_i 递减排序；`Σ_i X_i≤1`。把资源交给第一个正系数组的辅助规则，其期望为

\[
T=\sum_i X_iV_i\prod_{h<i}(1-X_h)\le E[\max_i a_i].
\]

对前缀 `s_k=Σ_{i≤k}X_i∈[0,1]`，AM–GM 与 `f_k(s)=1−(1−s/k)^k` 的凹性及 `f_k(0)=0` 给

\[
1-\prod_{i\le k}(1-X_i)
\ge f_k(s_k)\ge f_k(1)s_k=c_k s_k\ge c_n s_k,
\quad c_k=1-(1-1/k)^k.
\]

最后一步因为 `(1−1/k)^k` 随 k 增大，故 c_k 递减。令 V_{n+1}=0，乘非负差 `V_k−V_{k+1}` 并 Abel 求和，得到

\[
E[\max_i a_i]\ge c_n\sum_i X_iV_i=c_n\sum_iE[a_i],
\qquad c_n\ge1-1/e.
\]

这不要求组内不同资源的独立性。n=1 时 c_1=1；零概率项可以删去，仍使用原 n 的较弱常数。

目标中独立按 z_g 选同一个原 state，再对其正 incidence 以 `x_gsu/z_gs` 提议。只在 z>0 时计算除法。固定 u，a_gu 是提议时的原 p，否则零；因此

\[
X_g=\sum_{s:p_{gsu}>0}x_{gsu},\quad \sum_gX_g\le1,
\quad E[a_{gu}]=\sum_sp_{gsu}x_{gsu}.
\]

映射 bidder→group、item→resource、additive clause→state 后，上述同一个引理给 `E[A]≥c_nL`，A 为各资源最大提议系数之和。每资源只给一个赢家，真实 bundles 不交；同组所有赢家系数来自它**同一次所选 state**，故所选 state 的加性值≤原 max-state 价值，逐样本 W≥A。所选 state 无需是最终随机 bundle 的 maximizing clause；它是一个有效加性下界已经足够。这个细节避免把原 XOS 的 clause 访问合同错误移植成目标的输入假设。

## 4. 有理去随机化并未由期望免费获得

每资源列出原系数的不同正 levels `0=b_0<⋯<b_k`。任一合法固定前缀下，跨组独立仍给精确有理式

\[
F=\sum_{u,\ell}(b_\ell-b_{\ell-1})
\left[1-\prod_g(1-Q_{gu}(b_\ell))\right].
\]

未固定组选态时 `Q=Σ_{s:p≥b}x`；选定正概率 state、coin 未定时 `Q=1[p≥b]x/z`；coin 已定为 0/1 时为相应指示量。先逐组枚举 z>0 的 states，父 F 为候选 F 按原 z 的平均，取最大不降；全部 state 固定后逐 coin，父 F 为 `(1−θ)F_0+θF_1`，取较大合法分支。θ=0/1 只走概率一分支。最后 F=A，故确定性输出 W≥A≥初始 E[A]≥c_nL。

条件化后 `Σ_gQ_gu(b)` 可以超过 1；这里只重算精确乘积，绝不重套初始容量弦界。按资源线性求和允许同一组内资源相关，乘积所需的独立性仅跨组。states、coins、levels 的数量均被显式输入规模控制。每次从原 p,x,z 及离散固定项重算，分母的位长由原有理数位长的多项式控制；没有递归平方旧 F，没有以最小正概率倒数迭代，没有枚举指数 bundle 支持，也不比较无理数 e。X 因而正确支付给定精确可行点的福利步骤；求 LP、平衡提取、值桥和全作业调度仍准确保在 contribution.remaining。

## 5. V：完整值桥、平衡化及 13/8 精确代数

完整 P_gate 的四类互异机器为 root R、gate X_g、state private M_gs、resource Q_u。jobs 包含 pin J0（仅 R，时间1）、connector（R 时间1/n、X_g 时间1）、selector（X_g 和本组所有 M_gs 时间1）、每一条 listed incidence（private 时间 p、resource 时间1），包括零项和未选 states。

给平衡值 b>0 的 witness H、原 bundles 和 attaining states：pin 留 root；H 的 connector 去 gate、selector 去所选 private、所领正 incidence 去 resource；未选 connector 留 root、selector 去 gate；其余**全部** incidence 留 private。root 负载 `2−|H|/n`，选中 private 为 `2−v_g(B_g)`，其它 private、gate、resource 均≤1，得峰≤2−b。b=0 另用全部 connector 留 root 的完整峰2基线。反向任意完整 C<2 调度，H 取 connector 真正在 gate 的组，root 给 `|H|/n≥2−C`；这些组 selector 必须去某 private，导出正质量≥2−C；resource 端每 incidence 是 unit，C<2 保全局独占。故 β*≥2−C，合成

\[
OPT(P_{gate})=2-\beta^*,\quad0\le\beta^*\le1.
\]

零 incidence 不能被删除，但可全部留 private 加零负载。C≥2 时仅用 β*≥0 的端点。该值桥不适用于 flat 或任意一般 UM。

取得确定性 allocation 的真实质量 r_g 后排序，扫描

\[
b=\max_k\min(k/n,r_{(k)}).
\]

达到的前 k 个组及其原 bundles 才是调度 witness。若 `h=#{r_g>b}>nb`，取 k=h 得 `min(h/n,r_(h))>b`，矛盾。因此

\[
W\le h+(n-h)b\le n(2b-b^2).
\]

最优 β* 的有限 attaining witness 至少覆盖 nβ* 组且各质量≥β*，故 `W*≥n(β*)²`。与 `W≥(1−1/e)L≥(5/8)W*` 合成

\[
b\ge1-\sqrt{1-5(\beta^*)^2/8},\quad
C\le2-b\le1+\sqrt{1-5(\beta^*)^2/8}.
\]

不能将总福利 W 直接当 b，也不能写 C≤2−W。平方根仅供分析，算法全程为有理 LP、条件期望、排序、扫描和回填。

对 β∈[0,1]，置 `D=(13/8)(2−β)−1=(18−13β)/8≥5/8>0`。直接展开

\[
D^2-(1-5\beta^2/8)=
\frac{209\beta^2-468\beta+260}{64}\ge\frac1{64}>0.
\]

分子导数 `418β−468≤−50`，最小在 β=1，分子为1；两边非负，故可比较平方根，推出 `C≤(13/8)(2−β*)=(13/8)OPT`。这些步骤由 V 的承重正文实际写出，并不是只从源 WELFARE 的 FSLP 绝对保证推断。V 的 whole 与“单一算法只输入菜单、不输入 OPT/β*/YES/LP 点”的量词相符。

## 6. R：两阈值、互补和等号角点

R 调用源 13/8 完整合同中更早的 `W≥(1−1/e)L`。只知道最终调度近似比并不足以直接替代它。参数为 `0≤η<1、0≤δ<1、0<γ≤1` 且

\[
\frac58(1-\eta)\ge\gamma+(1-\gamma)\delta.\tag{E}
\]

YES 有至少 `(1−η)n` 个 unit 组；同一个真实 allocation 嵌入一般 LP，故 `L≥(1−η)n`。判别器接受当且仅当精确最优 L 达该阈值。

NO_≥ 中 `h=#{r≥δ}<γn`，低组是 r<δ；NO_> 中分别取 `h=#{r>δ}<γn`，低组是 r≤δ。两版各自有

\[
W\le h+(n-h)\delta
=\delta n+(1-\delta)h
<[\gamma+(1-\gamma)\delta]n.
\]

最后严格号仅用 h<γn 与 δ<1。高端≥的准确互补为低端<，数量 `>(1−γ)n`；高端>的互补为低端≤。不能把高组参数 γ 与低组比例直接相等。

若 NO 被接受，则 `L≥(1−η)n>0`，而 `e>1+1+1/2+1/6=8/3` 严格给 `1−1/e>5/8`，存在真实 allocation 满足

\[
W>\tfrac58L\ge\tfrac58(1-\eta)n
\ge[\gamma+(1-\gamma)\delta]n,
\]

矛盾。故两个独立 promise 各自完整正确；实际判别不必运行 finder，且没有 n 的整除条件。

统一子域 `0<γ≤δ≤3/8、0≤η≤1/40` 中，右侧 `≤2δ−δ²≤39/64`，左侧 `≥(5/8)(39/40)=39/64`。所以 `η=1/40、γ=δ=3/8` 三重等号确实包含在内，严格舍入常数支付该边界。δ=0 时 NO_≥ 为空；NO_> 仍按自己的合同。η=1、δ=1 域外，γ=1 与 E 不相容。所有 NO 都必须量化全部真实 allocation，仅控制完整束或固定 labels 不能替代。

这证明显式 promise 可判，不提供 NP-hard 源的可靠编译。若另有 NP 完全语言的确定性 Karp 归约到这个完整 promise，复合判别才有 P=NP 的条件后果。本三边不解决一般 UM 或其它模型的原开放义务。

## 7. 当前零 job 勘误与未覆盖范围

当前共享审查 §二.1 已将 flat CONFIG(1) 的互补 private 配置写成“全部 incidence jobs（含零 jobs）”。权 λ 的 selector+zero 配置与权 1−λ 的全 incidence 配置使每零 job 覆盖 `λ+(1−λ)=1`；正 job 的 private/resource 覆盖为 `(1−λ)+λ=1`，资源正支撑容量未变。该修正属于 flat 配置证书，不是三条边中一般 state/coin 福利或完整 gated 值桥的新前提。X 直接引用该文件 §一但 SHA 绑定整文件，已正确刷新；V 同样已刷新整文件 SHA；R 没有将旧整文件 SHA 偷用为 direct 证据。本轮未对历史旧字节做反替换取证，差分历史只作为已读 source-delta-review 的来源说明；当前两配置覆盖式则已独立核实。

未发现需提交 owner 的强制最小补丁。本报告不改边、不改源、不更改 registry/coverage/integration，也不自动关闭 pending。原对象中“未有通用生产 LP 后端”是实现状态，不是上述数学存在性算法的证明缺口。其余有限审计、全部 PDF 页、其它旧跨对象边、全仓 owner 状态及全局 3D 完结均不在本轮认证范围。

交付为本报告与 `refs.json`。后者完整列出三边原始 SHA/native pin/review_digest/endpoint pins、拥有该 exact asset 的 done task、receipt path/SHA/pin、实际阅读区间和 endpoint 完整合同，可供 Root 在自己的整合流程中引用；本轮没有代替该流程作任何写入。
