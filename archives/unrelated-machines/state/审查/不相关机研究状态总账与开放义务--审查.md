---
id: "unrelated-machines/research-state-ledger-20261031"
kind: "review"
type_tag: "审查"
title: "不相关机研究状态总账与开放义务"
status: "integrated-state-ledger-with-route-deduplication"
truth_status: "research-ledger; scoped-assets-and-open-UM-target"
review_level: "full-112KB-source-read-cross-archive-deduplication"
scope: "research/unrelated_machines/RESEARCH_STATE.md 的全量研究状态、正面限域接口、反面边界、路线矩阵、失败机制与 UM-TARGET-v1 开放义务"
summary: "完整读取 112,223 B 研究总账，按数学对象重组其日期分段、Claim 入口、有限证据、局部正面接口、反面障碍、复杂度边界和路线去重。总账的稳定结论是：大量限域构造与精确障碍已建立，但任意输入的共同容量提取、全机整数输出、sound FAIL⇒OPT>T、统一 epsilon 和位多项式进展仍未闭合，UM-TARGET-v1 保持 OPEN。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/RESEARCH_STATE.md"
  - "clean:0ea1e3525ab50e70127a"
related_objects:
  - "../资料/不相关机研究入口与文献状态--资料.md"
  - "../审查/续审交接-20261030.md"
  - "../审查/近单位PCSP蕴含与物理复制义务最终范围审查--审查.md"
  - "../审查/任意汇点价格覆盖与共同占位联合舍入最终审查--审查.md"
  - "../审查/私有组退出池共同宏任务与有界profile联合选择最终审查--审查.md"
  - "../审查/前缀原子证书解码桥与full-degree生成义务审查--审查.md"
  - "../审查/五机树Markov再耦合补全反例最终审查--审查.md"
  - "../审查/鲁棒双端环共享背景最终范围与三半锐界审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/research-state-20261031/original/research_state.md"
---

# 来源身份与读取范围

本页处理 clean source `0ea1e3525ab50e70127a`，原路径为 `research/unrelated_machines/RESEARCH_STATE.md`，冻结 blob `62850f2a14b65db410bd97f60041e847425b4435`，源 SHA-256 `25cf388cba05e48e03b22c092e08301719d2cad9f3311c7227ada6f8429cf151`，大小 112,223 B。原文已逐字复制到 `evidence_paths` 所列目录，并按章节、日期、Claim、有限 evidence 和开放义务逐段全文读取。

这是持续研究状态总账，不是单一 theorem。它混合了：

- 已有正式数学对象及其 proof/read-after 状态；
- 有限 Fraction/整数程序和冻结 audit；
- candidate obstruction、方法失败和路线复盘；
- 研究方向、用户决定、路线矩阵和后续义务。

因此本页将“已证明的限域对象”“有限实验”“候选障碍”“尚未闭合的主目标义务”分开，不能仅凭总账中的“已闭合”“PASS”“new Claim”标签把任意路线升级为一般 UM theorem 或 hardness。

# 1. 总账的主命题与当前研究方向

主目标 `UM-TARGET-v1` 是：对任意合法 unrelated-machines 输入和每个固定 `epsilon>0`，提供统一确定性位多项式 `(2−epsilon)` 调度算法，或给出在准确复杂度假设下的真实近二整数 OPT gap/不可近似归约，并让低负载完整调度能够解码源问题。总账在所有日期段反复确认：该目标及其一般反面仍 OPEN。

2026-10-19 的用户决定把研究方向改为“全体反面总攻”：对固定改善量 `epsilon` 构造接近 2 的实际整数 OPT gap，或同等强度的 hardness；反面归约必须使用可计算的绝对阈值，不能以未知 NO-OPT 的近似倍数作 decoder 条件。正面资产继续保留为障碍/工具，不改其真值。

总账把全输入共同桥梁精确定义为：对任意 `P,T` 生成共同容量状态或可验证 `FAIL⇒OPT>T`，并一次性输出所有机器同时合法的整数调度；该过程还必须控制统一余量、任务身份、资格、零/∞边和总位长。固定 `K/q/home/sink`、给定 tree/support/moment、有限 menu、未知 OPT promise 或已知 witness 的正面接口，都不能默认为一般输入步骤。

# 2. 经典地基和复杂度筛选

## 2.1 LST/ST、配置和离散化

总账保留 LST/ST 槽舍入、configuration gap 和有限处理时间字母表等经典地基，但不把配置 gap 当作一般 hardness。对正有限处理时间的有理输入，`g(P)` 是最大有理公因子、`B(P)` 是最大有限端，缩放 LST 给

\[
C_{\max}\le \left(2-\frac{g(P)}{B(P)}\right)OPT.
\]

固定正时间集合或始终满足 `g(P)/B(P)≥beta>0` 的族不能承载固定 `2−epsilon` hardness；真正近二反面必须让 `g/B→0`。零边、禁边、大分母和显式稠密整数正规形已被单独核算，极大分母本身不是困难性来源。

总账还记录固定 `d=3,n=2,m=3,b=4` 的 pDM 阈值编译：即使无完美匹配，也存在 `OPT/T=13/12` 的低负载调度（648 个合法分配全枚举），所以 `OPT≥bd+1` 不能直接变成近二 NO；二值 MaxMin 经因子关系得到的 makespan 常数也只有 `1+1/(pq)`。

## 2.2 Source hardness 与物理 compiler 分离

PCSP 线的 `A_k→B_{k,r}+AMO/ONE` minion/strong-fixing 和一般 promise-PCSP NP-hardness 已闭合，但物理任务复制、端口类型、每 job 出现次数、完整低调度 decoder 和总位多项式 compiler 尚未闭合。普通 BCG/BLMRS/Bamas 的 SA、MaxMin、MMDA 或 Santa 结论不能自动换成单根树或普通 UM 的 near-two gap。

总账重复强调：配置/SA gap 是局部放松障碍；必须另证真实 YES 调度、所有低负载 NO 调度的 source 解码以及完整整数负载。`P≠NP`、`NP⊄BPP` 或其他假设必须在最终 reduction 中明确写出。

# 3. 已闭合或可复用的正面限域接口

以下接口都具备明确输入合同和实际输出，但不覆盖一般 UM：

| 对象 | 输入/结论 | 仍缺的部分 |
|---|---|---|
| **共同 sink / private group / price-cover** | 唯一 home、私有组、逐件资格和共同 sink；cover FPTAS + 共同宏匹配 + MW + 单侧基舍入；给 `L_h≤(1+tau)T`、`L_z≤[1+eta+b_0]T`，或 `OPT≤T` 时 one-sided FAIL | 从一般矩阵提取 home/组/宏/资格；任意多 sink、跨 home 和混尺寸结构 |
| **宏退出 / bounded profile pool** | 宏任务可共同选择 home 或 exit；profile `a_z c_j≤p_zj≤rho a_z c_j`, `p_zj≤beta T`；虚拟单 sink work + 实际最小负载恢复给 pool `≤[rho(1+eta)+beta]T` | 无 profile 上包络时的多 pool 容量；一般结构提取 |
| **Hall joint group flow** | 同组共同资格、等端体积、组负载下界；q-Hall 见证、一次全局整数流和前缀收费；给 `r=q(2+delta)/(q+1)` | 同组异资格、跨 home、异端时间、任意资格恢复 |
| **DAG/token/tree bridges** | 给定支撑或树，真实调度恒等式 `OPT=2-b*`、root/forest 解码、固定支撑整数流和参数化搜索 | 从输入选择好支撑/树；无界高点选择和共享分支 |
| **prefix atomic law** | 给定共同非负守恒前缀 law 和完整原子 localizer，O(E) 选正孩子得到 T-feasible 调度，存在性等价 `OPT≤T` | 任意 `(P,T)` 生成 law、可靠 FAIL、full-degree oracle |
| **robust cycle phase** | 给定 strict T witness、disjoint two-endpoint cores 和 context，任意 phase 切换 `Cmax<3T−B`，B≥3T/2 时弱 B；三半阈值锐 | 未知 strict witness、第三端、共享 core machines、多环/一般 decoder |
| **multi-outer/single-state** | typed normalized-flat 输入、tiny home 权、shared fallback；19/10 或相近常数实际算法，LP/CDF/variance/CE 全 jobs 回填 | 一般 multi-state/multi-home/ordinary UM |
| **normalized flat/menu CONFIG** | positive-support FSLP ↔ CONFIG(1) ↔ state-dummy SC；SC path 后 rowtotal/item degree 有界 | actual OPT≥1 下的一般常数算法、general finder |
| **unit readout/DAG forest** | 给定 actual 调度或固定 support，root forest/leaf flow/slot path 可实际解码 | 从一般输入生成 support、共同 capacity 和实际输出 |

这些对象的证据包括解析证明、有限 audit、独立 read-after、精确代码和实际分配，但证据层级必须保持分离。

# 4. 主要反面边界和失败机制

## 4.1 固定局部修复、槽和逐坐标路线

- `UM-STRICT-SUB2-BATCH-BARRIER-v1`：三机族有 `OPT=1`、坏态 `2−1/(8k)`；每步至多 `k` 件且全程严格 `<2` 时，坏态无出口，首个合法出口需 `k+1` 件。说明严格次二局部修复必须允许 `Omega(1/epsilon)` 同步动作、跨 2 或全局重求解。
- `OPT-HULL-LONG-CHAIN`、`cyclic_batch_repair` 和固定工作凸势族：真实最优凸包或最佳固定槽输出仍趋 2；逐坐标或固定槽局部 repair 会锁死。它们不排接收机增载、多目的地重开或全局修复。
- `configuration_preserving_elimination_support_loss`：真 `OPT=1`、CONFIG1 和全部局部负载等式仍可能因永久删零端失去次二补全；需要安全方向或恢复删端。

## 4.2 配置、矩、条件探针和共同 law

- 裸 C2、弱 H2 和强 H2 族区分：裸 C2 的配置 gap 近 2；弱 H2 共享同一一阶点后仍有精确 gap；强 H2 共享二阶后该族阈值恰为 OPT。低阶/独立探针不能自动给全局共同 law。
- `diluted_shared_terminal_raw_k2_gap` 和固定阶 row extension：同机 CONFIG first/pair、global M2、affine localizers 仍有真实 gap 上确界 2，但不构成 hardness；更强共同 CONFIG/M2 或联合 pricing 仍未求解。
- Tree Markov 五机反例：保单机和生成树 pair marginals 的再耦合会产生补全峰 2，尽管原分布 `OPT=1`。非树相关性不能丢掉。
- Prefix/relative-Gram：给定 law 可 O(E) 解码，但 full-degree localizer、N 叶质量和满行秩条件不能由低阶 Gram 免费提供。

## 4.3 复制、标签、bundle 和 source bridge

- 完整 clone multiset/periodic copying、两状态多数 floor、低重数 label floor、bundle matching floor、square-root multiplicity 等都给出资源地板或复制反放大；它们只排具体接口，不给一般 hardness。
- 3DM demand floor、k-uniform bundle floor、单层 quota、PCSP、Santa restricted bridge 均暴露跨层整数一致性；直接 root→hyperedge→resource 需求树常有 `t`-层配额地板，不能只看 full K matching。
- Rainbow/ternary tree：低重数 2 全 YES、重数 3 受限 NP-complete、五半配置 gap；张量/纯收缩的 gap 会趋近 1，不能自然放大到 near 2。
- Affine line/tuple global dummy、XOS/menu、two-level label fee、robust phase、shared sink 等编译器有明确逃逸或三半上界；不能从有限列表 NO 或 local menu 直接得到 actual near-two。

# 5. 当前共同容量/选择路线矩阵

总账的路线矩阵给出如下去重后的承重关系：

| 路线 | 已确定 | 不可升级的缺口 |
|---|---|---|
| 大边/小边、条件块 | 专族共享逃逸可切；固定阈值选择已有 NP 难障碍 | 任意输入共同块分离、联合整数输出、sound FAIL |
| 批量 repair/分流 | 固定参数局部终止；逐坐标/单目的地被 gap 族击穿 | 多目的地合流、接收机增载、统一进展势 |
| 联合迁移/槽 | 最佳固定槽也可能近二；宏任务必须共同重选 | 一般跨槽/跨宏迁移、总位进展 |
| 受限 home/sink/group | 单 sink、Hall、profile、weighted group 各有正面算法 | 一般输入结构提取、任意资格、混尺寸容量 |
| 矩/需求树 | 给定 support/moment 的实际 bridge、参数化流 | support/共同矩可计算提取、共享分支/合流 |
| 反面 source | clone/bundle/PCSP/MinRep/3DM/Santa 各有边界或抽象 hardness | 每固定 epsilon 的真实 OPT gap、YES 保持、低调度 decoder |
| Prefix/full-degree | 给定 law 的 O(E) 解码、精度/秩边界 | law generator、可靠 FAIL、低阶到 full-degree 生成 |

团队当前共同门槛是：任意合法 `P,T` 下，产生共同容量状态或可验证 `FAIL⇒OPT>T`，一次性输出所有机器同时合法的整数调度，且不把 `K,q,r,n` 或数值精度偷偷当循环次数。

# 6. 研究状态中的修复和纠错

总账保留多项真实修复，不以旧冻结稿覆盖：

- threshold cover/支持释放：旧固定前缀恢复和 FPTAS 上界曾有出口超支/未知 OPT 漏洞，已改为同一覆盖见证、完整上界和截断成本 DP，并重新审查；旧冻结结果不覆盖新修复。
- LST support release：旧 `OPT=T=1` 标签撤回，新增 `r` 独立块确保 `OPT=1` 后再给 `2−1/m`；不把旧标签当一般结论。
- price cover：空模式类不保 full rank，已补 `H_Q` 覆盖全部 `B`；不把首稿漏洞当定理，也不把修复升级一般 UM。
- robust cycle：不同 core machine-disjoint 条件澄清，Overlap 反例保留为域外；三半和 `3T−B−e` sharpness 只在明确域内。
- tree Markov：五机坏态可以通过迁移 `a`、换树或择态修复；反例只针对冻结树任务、无迁移 completion 合同。
- prefix precision：数值 `N` 可能很大但二进制位长可多项式；不能把 `1/N` 误写成指数 bit complexity 下界。

# 7. 有限证据、证据等级与去重规则

研究状态汇总了大量代码和 JSON，但每项必须保持以下分层：

1. **解析限域证明**：例如 robust phase、Hall flow、prefix given-law decode、shared sink/profile、DAG token 恒等式；这些证明只在明示合同内成立。
2. **有限精确 audit**：Fraction/整数枚举、有限 matrix、局部 sharpness、独立 code paths；它们支持回归和边界，不替代 universal theorem。
3. **候选障碍**：小图、固定参数、局部 repair、bundle floor、clone、tensor；必须保留“candidate/not hardness”标签。
4. **文献/标准工具**：LST/ST、VW/BLMRS、BCG/Bamas、BBKO、Feder/KKR 等只作为已读背景，不能把来源中的 gap、算法或开放问题直接改写成仓库新定理。

总账中的 route matrix 已指定去重入口：`joint_matching_completion_and_block_cuts` 统一大边/条件块；`cyclic_batch_repair_and_fork_obstruction` 统一循环/分流/真实凸包；`shared_sink_joint_macro_assignment` 统一单 sink 宏任务；`rooted_dag_degree_token_bridge` 统一需求树 token；`private_graft_and_resource_repetition` 统一 clone/接线障碍。新增审查应更新入口或建立真实独有对象，不复制同族微小实例。

# 8. 当前状态结论与下一义务

**已确定：** 研究已收紧大量错误路线的精确失败机制，也建立了多类可复用限域正面接口。包括共同 sink/home/profile、Hall/q-flow、robust phase、prefix atomic、tree token、normalized menu CONFIG、multi-outer typed algorithms、bundle/clone/rainbow floors、raw K2/H2/SA barriers。

**仍未确定：**

- 任意 ordinary UM 输入的共同容量状态、home/sink/profile 或 tree/support 结构生成；
- 一次性全机整数输出与统一 `epsilon`，尤其混尺寸、多个 sink、多个 home、跨层/跨模块相关性；
- 可靠 `FAIL⇒OPT>T` 证书，而不是 LP/CONFIG 不可行或有限枚举失败；
- 对每个固定 `epsilon` 的真实 integer OPT gap、完整 YES 保持和低负载调度 source decoder；
- 全阶 moment/prefix law、shared integer ownership、non-tree correlation 的可计算生成；
- 外部同行评议、全球新颖性和一般复杂度主张。

下一阶段应使用 `JC-THRESHOLD-epsilon(T)` 工作合同：若 `OPT≤T`，输出实际分配且峰值≤`(2−epsilon)T`；否则输出可独立验证的 `D` 证明 `OPT>T`。`T=0`、零处理时间、不可用边、极大分母和所有机器同时容量必须同一语义。任何新路线在两树、长链、共享小端、多行条件、zero/∞边和 mixed-size 输入上若不能降低这些承重义务，应登记为边界并停止同类微调。

# 9. 结论

`RESEARCH_STATE.md` 是一份完整研究状态账本，而非单一 theorem。它的最稳健摘要是：受限结构下已有许多真实算法、精确恒等式、sharp barriers 和有限审计；但这些对象都依赖显式 home/sink/profile、给定 witness/support/moment、固定配置、bounded degree、单 sink、有限层级或其它结构 promise。一般 `UM-TARGET-v1` 及其无条件近二反面仍 OPEN。

本页按数学对象重组了实际定义、结论、证据、失败机制和开放义务，并保留历史修复与 route deduplication。后续引用不得把研究状态中的路线判断、有限审计、标准文献或内部“已闭合”标签升级为一般调度 theorem、hardness、外审或新颖性证明。
