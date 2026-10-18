# Degree-two weighted-menu v2：独立重构与实际后端

Exact：`low_group_degree_bounded_menu_joint_rounding_v2_exact.md`，SHA-256 `7435885c698e741f0dc762cd1fc79be270ad7de164859477645b37affbd9a298`。

读取次序：先实际核读 VW2010v1 PDF §5.1、Lemma 11、Theorem 12（PDF 10–11 / printed 9–10），冻结来源预核；随后才读取上述 Exact 并独立重构 A–E；在证明与位复杂度闭合后实现本后端。未读取新桥作者 Proof，未读取其它审查者的数学证明，未修改 repo、Work 或 Git。

**判定：限定结构类的完整后端已实现，列明审计通过。核心不接收 OPT/YES 见证，不调用枚举、LP、外部求解器或递归搜索。不能将此实现泛化为一般 UM 后端。**

## 1. 独立数学重构（实现前完成）

### 正规化精确保实际 OPT

G 非空且每 group 有 selector，故每个原完整调度的峰 C≥1。对每个 W_gs<1 的 state 加一个私有 bonus resource 和一枚 private time 为 1-W_gs、该 resource 端时间为 1 的 bonus incidence，所有 state 的总 private work 都成为 1。

任何原调度可把**全部** bonus jobs（包括未选 states 的）导出到各自不同的私有 resource，原 assignment 不变，新增机负载至多 1≤C；反向删 bonus 只减负。因此 OPT(N(P))=OPT(P)。只加每 state 至多一枚 job 和一台机器，不按数值复制。

### 正规化身份 OPT=2-V

所有 private jobs 留 home、每 selector 任取 state，给峰≤2；selector 又给 OPT≥1。对任意 C<2 的完整调度，每台 resource 最多一枚 unit。取每 group 实际 selector 所在 state，该 state 的 private 总和是 1，要把 state 峰压到 C，必须导出 private mass 至少 2-C。只记录这些选中 state 的 exports，得到跨 group 两两不交的 B_g，因此 f_g(B_g)≥2-C、V≥2-C。C=2 时下界 C≥2-V 由 V≥0 已然成立。

反过来对任意 disjoint B_g，每 group 只选一个最大化 a_gs(B_g) 的原 state，只导出该 state 中被分给 g 的 resource incidences，其它所有原 incidence 留自己 state。resource unit 不冲突；未选 state 峰为 1；选中 state 峰为 2-f_g(B_g)。故完整峰为 2-min_g f_g(B_g)，得到精确身份。零 private times 既不增加 clause mass，也不导致原 job 消失。

### group averaging 与共同后端

每 group 只有一个 additive agent，v_g(B) 是所有 K_g 个 state clauses 的平均值，满足 f_g(B)/K≤f_g(B)/K_g≤v_g(B)≤f_g(B)。对最优 XOS allocation 使用同一 B_g，可得 additive optimum A≥V/K。每个资源跨至多两个 group（不是“2K 个 state agents”），故 aux positive degree≤2；bonus degree 为 1。

VW 后端返回 min_g v_g(B_g)≥A/2。扫描原菜单选最大 clause，得到 min selected mass≥A/2≥V/(2K)，故 normalized schedule 峰≤2-V/(2K)。删 bonus 得

    C≤2-(2-OPT(P))/(2K)。

由于 OPT(P)≥1，右端≤(2-1/(2K))OPT(P)。这里没有给任意 NO 输入一个绝对 2-1/(2K) 上界；下述 near-two NO 审计实际输出 33/17，超过 K=1 的绝对 promise 阈值 3/2，符合陈述。

## 2. 实际实现接口

核心：`degree_two_weighted_menu_backend.py`。

输入 JSON 有显式 `resources` 与非空 `groups`；每 group 有唯一字符串 ID、非空 `states`；每 state 有唯一索引 ID 与显式 `incidences`，每 incidence 给 `resource`、`p`。p 仅接受显式整数或 `N/D` 字符串，不接受 float、科学记数法或数值隐藏展开。原资源名、state、resource machine、bonus resource 使用不同标签，不发生别名。

核心检查：资源/group/state ID 唯一；state 内无重复 resource；每 state W≤1；资源跨 group 数≤2（**即使对应 private value 为零也计原 incidence**）；私有时间非负；所有资源已显式列出。重复内容的 states 只要 index 不同仍保留。空 state/resource universe 允许；空 G 明确拒绝，因其不在冻结 Exact 域，不私自借用空实例约定。

处理流水线：

1. 每 state 显式构造 private bonus 与完整 normalized mass。
2. 在 group 层求平均 additive values，删除全零 aux items/edges。
3. 精确共同分母缩放，调用自主实现的 VW threshold oracle 与单向证书整数二分。
4. 每 group 选**一个**最大实际 allocated mass 的 state。
5. 输出全部原 selector、全部原 incidence 的唯一 assignment、processing time、start、finish；仅删除引入的 bonus jobs。
6. 独立验证原 job 集、资格边、原处理时间、正时长区间不重叠、全机负载和实际完工峰。normalized job accounting 也在核心逐机回算。

CLI 可运行：

    python degree_two_weighted_menu_backend.py weighted_menu_joint_bad_heavy_input.json

实际 CLI 已运行并解析输出：makespan=1，六枚原 jobs 全部输出。完整结果保存于 `weighted_menu_joint_bad_heavy_output.json`。

## 3. VW threshold 与未知 OPT 的真实实现

每个 retained aux item 有 1 或 2 个正端。singleton 直接归其唯一 agent；双端 item 的 A 列表按各端局部权降序、固定 item index 破同值排序。

forced-largest 阶段用 active item、每 agent 总和、排序列表指针与 deque。若总可用值<T 则拒绝；若去掉最大 item 后<T，则把它强制给该 agent，并从**两个端点**的 A 全局删除，再更新两个端点。每次删一 item，force 次数≤items。

剩余 occurrence 图是 same-item matching 与 local consecutive-pair matching 之并。用 deque BFS 二染色，未采用递归 DFS。每 item 由唯一黑色 occurrence 接收；每 local pair 接收一个，保证 value_i≥value(A'_i)/2+value(B_i)≥T/2。

二分不假装 oracle 精确：success 只给 T/2 解，failure 才证明 A<T。整数缩放后设 U=min_i 全部 aux 值总和，high=U+1 有直接拒绝证书，low=0 保存任取正端的 fallback。成功提高 low 并保存该实际 allocation，拒绝降低 high。high 始终>A；结束 high=low+1，整数 A 迫使 low≥A，因此保存解≥A/2。没有利用未证的 success 谓词单调性。A=0 时 low=0、fallback 完整分配 aux positive items 即可。

有限审计特别含四 agent K4 六 item：真实 A=1，但 T=2 oracle 成功、返回 min value=1。最终成功阈值是 2，失败阈值是 3，清楚证明实现未把 weak oracle success 当精确 T-feasibility。

## 4. 总位多项式实现论证

显式 incidence 数与 state 数控制全部新增 bonus 和 aux entries。group averaging 是显式有理加法及除 K_g；所得分母位长为输入总位长的多项式。共同整数分母用 lcm，位长不超过各 aux denominator 位长之和。没有按分母数值复制 items 或循环。

缩放后 U 的位长为多项式，二分 O(log(U+1)) 次。每次 threshold 的排序、force queue、local pointers、pairing 和 BFS 都只处理显式 agents/items/occurrences；每 item 强制至多一次、每 occurrence 图规模线性。Python 任意精度整数运算的位长保持多项式。菜单扫描、原 job 输出及开始时间部分和均为多项式。

这里保证自行实现的总位多项式，不冒称实现达到原文精细 O(|I|²) 时间。核心也未实现 succinct/exponential menu 接口。

## 5. 实际有限审计（不替代证明）

审计模块：`audit_degree_two_weighted_menu_backend.py`。它与核心单向分离：audit 导入 core，core 不导入 audit。完整 job assignment 枚举、additive optimum 枚举、XOS allocation 枚举只在该模块，核心 solve/vw 不调用任何 brute。

| 列明 weighted-menu 例 | 原 OPT | normalized OPT | 返回 C | 核对重点 |
|---|---:|---:|---:|---|
| joint_bad_heavy_yes | 1 | 1 | 1 | flexible group 选 diffuse，single-heavy group 获共享 heavy |
| near_two_single_state_no | 33/17 | 33/17 | 33/17 | 不是任意输入都落绝对 promise 阈值 |
| zero_work_empty_and_duplicate_states | 1 | 1 | 1 | W=0、empty S、零 incidence、重复空内容、不同 K_g |
| rational_unequal_menus_and_bonuses | 1 | 1 | 1 | 非统一有理 private weights、不同 K_g、全部 state bonuses |
| aux_opt_zero_fallback | 2 | 2 | 2 | A=V=0，无正成功阈值，仍输出完整原 schedule |

这五例的原实际 assignment 枚举分别为 32、16、12、768、4；normalized 分别为 32、16、192、24576、4。逐例核原/normalized OPT 相等、OPT=2-V、A≥V/K、实际 aux 值≥A/2、相对与 additive makespan 界，并核全部原 jobs 的实际时间表。

另外列明小后端例：even pairing cycle、weak success above OPT、asymmetric forced cascade、rational values、zero optimum、no positive items。其 small OPT 只在 audit 枚举。单独一个 1200-agent even occurrence cycle probe 未用 brute，迭代后端返回 min value=1，无递归栈限制。不是无目的海量枚举。

非法输入审计拒绝：空 G、三个 group 的同一 resource（即使全零权）、W>1、state 内重复 incidence、float、隐藏巨大指数表达。

实际运行输出 `all listed finite audits passed`，详细结果在 `weighted_menu_backend_audit_results.json`，所有 fixture 输出在 `weighted_menu_backend_fixture_outputs.json`，完整输入在 `weighted_menu_backend_fixtures.json`。

## 6. 范围与剩余事项

本实现只接受显式 group-degree≤2、W≤1 的 weighted menu 原始结构，含完整原任务 accounting；不接受一般 UM、degree 3、隐式大 menus 或其它外部端费用。它实现已发表 degree-two additive 后端在此新桥中的直接应用，不宣称外部新颖性或一般 UM 改善。

未核新桥作者 Proof；本记录独立重构范围为 Exact A–E 及其 promise/relative 后果。Exact F 中一般 tagged cube 记号的外围嵌入不由本通用 weighted-menu 输入解析器实现；给定具体 cube 输入仍须先验证它确实生成本域的完整显式实例。有限审计不替代量化证明。
