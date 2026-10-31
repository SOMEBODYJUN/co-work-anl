---
id: budget-games/retired-nash-candidate-map-and-dynamic-selection-boundaries
kind: review
type_tag: 审查
title: 多线 Nash 候选卡与动态选择边界
status: retained-candidate-map; partially-integrated; unresolved-open-cards
truth_status: review-record
review_level: full-source-read-and-cross-archive-compared
summary: "完整读取退役 multi_lane 的 Nash/动态/选择第二轮候选卡；保留七个候选的精确模型、量词、证据等级、同日覆盖与淘汰更新，并把已进入 budget-games、weighted-congestion 的对象和仍未成文的开放卡分开。该页不是定理、新颖性认证或最新文献穷尽声明。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/nash.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/lanes/nash.md
related_objects:
  - ../定理/分段线性凹偏好的共享超梯度合并判别--定理.md
  - ../等价/共同形状可分凹偏好的对数边际规划--等价.md
  - ../资料/克隆识别与Leontief均衡的不同恢复接口--资料.md
  - ../../../weighted-congestion/state/审查/原子拥塞重选题与失败路线--审查.md
  - ../../../weighted-congestion/state/资料/原子拥塞候选线与37-33小证书--资料.md
  - ../../../weighted-congestion/state/资料/有限双权近似势与非对称精炼目标的不同合同--资料.md
evidence_paths:
  - ../../../weighted-congestion/tools/evidence/atomic-games/candidate_report.md
  - ../../../weighted-congestion/tools/evidence/atomic-games/candidates.json
---

# 来源身份与处置

本页对应冻结来源 `history/retired_topic_selection/multi_lane/research/topic_selection/lanes/nash.md`，原始提交有 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 两个定位。来源标题为“Nash/动态/选择：第二轮独立候选卡 v1”，日期为 2026-10-20，原文长度 16,446 字节；本次通过 `clean show` 完整导出并逐段阅读，再与当前结果分支中 budget-games、weighted-congestion 的正式对象和证据入口比较。

它是一个**选题审查与路线分诊源**，不是一份定理证明。卡片中的 A/B/C 分级表示作者原文明确问题、作者建议方向和团队派生限制；不表示真值、难度或新颖性。来源自己也提醒，检索没有找到后续不等于证明问题仍开放。本页保留卡片的模型定义、承重义务、反对意见和同日更新；已被本仓库完整对象吸收的部分只做准确映射，不重新包装为新贡献。

同一来源把 N7 归并入原子拥塞候选 AT03，把 N2 在同日核验后从“新算法题”降为已知 Fisher 接口，把 N3、N4 的有限几何材料与相应正式对象分开。以下仍按原始七卡列出，避免把候选路由的合并误写成数学等价。

## 七卡总览

| 卡片 | 精确对象和量词 | 当前证据等级 | 与结果树的关系 | 本次处置 |
|---|---|---|---|---|
| N1 / PS-CAC-v1 | 无权 player-specific singleton 拥塞；玩家各选两资源，资源—玩家图为简单 cactus；严格递增、无平局成本；均匀随机挑不满意玩家作 best response，问对所有初态/成本序的期望多项式改善步界 | 原文树与单环事实由候选卡转录；figure-eight 只是拟议 toy，未给证明或可重放证书；一般猜想后续状态未穷尽核实 | 与 weighted-congestion 的 player-specific/改善环文献相邻，但没有同量词正式对象 | 保留为未决候选卡；不得写成 cactus 上界或下界 |
| N2 / BA-WL-v1 | 正有理二进制预算总和 1；`u_i(delta)=min_{x:v_ix>0} delta_x/v_ix`；要求精确有理 NE 的输入位多项式算法，不能按分母复制玩家 | 来源先记录作者 open question，随后同日记录 Tao–Zheng、Brandt/Lindahl、Orlin/Fisher 接口及零价、same-v、spending profile 攻击 | 完整两向接口已在 `预算-games/资料` 对象中重构 | 保留为“候选被已知覆盖”的审查轨迹；不再主张新算法题 |
| N3 / BA-CLONE-v1 | 非负有理矩阵 `A` 的 `min_r a_r·delta`；对所有等预算 clones、外部环境和每一份 NE，合并后仍为 NE；求必要充分识别 | 三项目两 clone 的精确反例、可微正向引理、active-cell/共同超梯度 LP 识别及 m=2 边界已进入正式定理；coNP 证书另有资料页 | `分段线性凹偏好的共享超梯度合并判别--定理` 与克隆资料页承载承重数学；原候选卡只保路线和 objection | 视为已部分整合的候选来源；不把 `2^R poly` 识别写成一般 R 多项式或 coNP-complete |
| N4 / BA-ORDGRAD-v1 | `u_i(delta)=sum_x v_ix f_i(delta_x)`，先问共同/可统一的 log-gradient 形状何时等价全局凹规划、并给表示和近似位保证 | 共同 `f`、正估值的 KKT 等价及 aggregate 唯一性已写成条件等价页；player-specific `f_i` 分类、oracle、精确位复杂度和文献覆盖仍未闭合 | `共同形状可分凹偏好的对数边际规划--等价` 给出严格子类，不等于原宽候选 | 保留为“条件地基 + 查重义务”；不能把共同形状子类升为完整分类 |
| N5 / BA-L1-SELECT-v1 | 负 L1 距离、正有理 peaks 与预算；在非凸 NE 集合中最小化加权社会损失或判定阈值；先等预算、全项目，再找紧复杂度/参数边界 | 来源给作者 NE 算法、非凸中点例和固定项目数 XP 草图；未给硬度、全参数算法或可重放完整证书 | 当前树中没有把该选择问题写成已证定理；与 budget-games 的 NE 资料仅共享背景 | 保留为未决派生问题；非凸性是障碍/事实，不是 NP-hard 结论 |
| N6 / CG-PAIR2T-v1 | 无权、策略均为二资源子集、成本非负非降；两类玩家各有显式 pair-family；问任意纯 NE 的多项式算法或 PLS-hardness，并区分全局势最小与局部 NE | 母论文把一般 size-2 PNE 复杂度列为未来问题；两 type 限制为团队派生 C；候选卡无独立归约或证书 | weighted-congestion `atomic-games/candidate_report.md` 的 AG-01 覆盖更宽的 size≤2 局部 PNE 公开孔洞，但没有自动给 N6 结论 | 保留为独立窄化候选；不得把全局 MinPotential NP-hard 移植为 PNE 硬度 |
| N7 / FT-SMOOTH-v1 | 权重 `{1,2}`、非负二次成本；对非零系数作 bounded-density 噪声；按 `(64/59)(1+epsilon)`-improvement 的真实动态，要求 expected poly 步数和 bit 复杂度 | `64/59` 近似势与 smoothed FPTAS 截断倒数是两条已知工具接口；来源只给“可能短推论”的组合提醒，未给合并证明 | `有限双权近似势与非对称精炼目标的不同合同--资料` 保存 64/59；weighted-congestion 文献页保存势/动态边界 | 并入 AT03/附属工具方向；不把黑盒组合写成已证 smoothed weighted 算法 |

## N1：cactus 随机 best response

候选模型要求每个玩家只有两个 singleton 资源，资源为顶点、玩家为边形成简单 cactus；每个资源对每名玩家的成本严格随人数增加且没有平局。每一步只在当前不满意玩家中均匀取一人，执行其 best response；要计数的是实际改善步，不是抽到满意玩家的空步。主量词是对所有初态、成本序和图形的 `n^{O(1)}` 期望改善步界，首个切口为两个环共享一个割点、其余任意挂树。

来源把 Ackermann–Röglin 2008 的一般随机 best-response 猜想、树上任意序列 `O(n^2)` 和单环随机期望 `O(n^2)` 作为背景，并指出分叉 token 可能复制或吸收。它要求先逐边核查原 §5 gadget 是否真的属于 cactus；若 gadget 共享两个顶点或有多条独立路径，直接把它当 cactus 反例会改变题目。figure-eight Markov 链、regeneration cycle 和 Monte Carlo 只是拟议方法，不是证据。

本次交叉检查只确认结果树已有 player-specific/weighted 拥塞的改善环、严格均衡和全状态无均衡对象；没有在当前树发现一个与 `cactus + uniform random dissatisfied player` 完全同量词的定理或完整审计。因而 N1 的处置是保留为**未决候选/范围待核**：不能从“树、单环已有界”拼出 cactus 全类界，也不能从一个有限六玩家循环或 token 直觉推出超多项式下界。若后续接续，第一份证据应是原 §5 图的逐边清单和严格 cactus 验证，然后才是精确有限吸收链；最新文献状态需另行联网核验。

## N2：weighted Leontief 的覆盖纠错

原卡的输入是正有理预算 `b_i`（总和 1）和非负有理估值行 `v_i`，每人效用
`u_i(delta)=min_{x:v_ix>0} delta_x/v_ix`，要求按二进制输入位长输出精确有理 NE。候选卡正确地指出 equal-budget Leontief 的多项式结果不能冒充 weighted 版本，也指出直接按共同分母 `D` cloning 会产生伪多项式规模。

同日更新随后改变了路由：现有[克隆识别与 Leontief 均衡的不同恢复接口](../资料/克隆识别与Leontief均衡的不同恢复接口--资料.md)逐式保存了 public Leontief 与 private **linear** Fisher 的两向 spending 映射。给同一 `v,b`，public 贡献矩阵 `X` 的行和为预算、列和为 `delta`；private Fisher 价格为 `p=delta`、数量满足 `X_ij=p_j y_ij`。正支出恰落在 `argmax v_ij/p_j`，与 public 的 critical 坐标条件相同；反向以 `y_ij=X_ij/delta_j` 恢复。零预算行、全零列、same-v 和 exact spending 输出边界均在资料页中单列。Brandt/Lindahl、Tao–Zheng 和 Orlin 的接口被来源卡记录为**已知工具重构**，不是本仓库新算法。

因此本候选的正确状态是“候选题被已知覆盖而淘汰”，但原卡及其时间线仍有保留价值：它记录了作者稿仍写 open 与独立接口核验之间的冲突、以及为什么不能把 log-Nash 凸规划草图当作精确 bit-poly 证明。weighted Leontief 的其它效用、预算或输出约束若改变，须另立模型和量词。

## N3：polyhedral cloning invariance

原卡要求对有限非负有理矩阵 `A` 的 `u_A(delta)=min_r a_r·delta`，对所有等预算 clones、外部玩家、每一份 NE，合并 clones 后仍为 NE；它明确区分“每一份 NE”与“存在一份可合并 NE”。本仓库的正式定理已给出相同量词的点态判别：在 active rows `I` 的超梯度多面体 `P_I` 中，令 `U_delta` 为可由某个超梯度成为最大坐标的正支持坐标；合并当且仅当存在一个共同 `g` 使全部 `U_delta` 同时最大。

定理页还给出三项目两 clone 的精确反例：两 clone 各预算 `1/4`，效用
`min(2 delta_1 + 3 delta_3/2, 2 delta_2 + 3 delta_3/2)`，分别纯投项目 1、2；外部预算 `1/2` 只投项目 3。总分配 `(1/4,1/4,1/2)` 时两 clone 各获 `5/4` 且是 NE；合并后全投项目 3 获 `3/2`。同页给出可微共同梯度正向引理、active-cell LP 枚举和 m=2 全部保持边界。算法复杂度是 `2^R poly(m,R,L)`，不是一般 `poly(R,m,L)`；失败构造的等预算人数可能指数，但人数用二进制压缩，不能把这一点写成显式逐人多项式输出。

候选卡还记录了有限网格/`Fraction` 核验和原 `CLONING_AND_SEPARABLE_TOYS.md` 入口；这些路径在当前结果树未作为独立文件出现，故本页只把它们作为来源报告的有限证据，承重证明以正式定理页为准。资料页另给 coNP 失败证书包含，但没有 coNP-hardness、complete 或一般 R 的多项式识别。N3 已部分整合，仍需查一般效用分类、可读禁形和 coalition/clone 文献，不能把候选卡的“值得查重”写成新颖性。

## N4：非 binary 可分偏好与 log-gradient 规划

原卡的宽问题是 `u_i(delta)=sum_x v_ix f_i(delta_x)` 下，刻画哪些递增凹的 `f_i` 使 NE 等价某个全局凹规划，并给输入表示、近似 NE 和 bit 复杂度。它特别提出 `f'_i(t)=a_i g(t)^{b_i}` 的统一梯度族，但把共同 `f` 子类的证明明确标为地基而非完整分类。

结果树中的[共同形状可分凹偏好的对数边际规划](../等价/共同形状可分凹偏好的对数边际规划--等价.md)已经严格证明：当所有 `f_i` 是同一个 `C^2`、严格增且严格凹的 `f`，估值 `v_ij>0` 时，玩家 NE 恰等于凹函数
`P(x)=sum_j integral_0^{delta_j} log f'(s) ds + sum_{i,j} x_ij log v_ij`
的全局最大点，且总量 `delta` 唯一。该页同时保留边界：player-specific `f_i`、零估值、`f'` 的零点、函数 oracle、精确有理表示和近似精度都没有被自动解决；log、积分和最优点未必有有限有理表示。

因此 N4 的可交付内容是“共同形状条件等价 + 明确适用边界”，不是 player-specific 的必要充分分类，也不是精确 bit-poly 算法。需要继续做的是真实文献查重、统一 log-derivative 的可识别条件、最小坏例和 oracle/位复杂度合同；不能用“有一个势”替代这些义务。

## N5：非凸 NE 集上的社会成本选择

候选卡利用原文的 NE 刻画：负 L1 距离 peaks、正有理预算，NE 支出只落在不过供项目；作者给出任意一个 NE 的多项式构造，但 equilibrium distributions 的集合可以非凸。来源的两个 NE 中点不再是 NE，因此把选择问题写成一次凸可行性会出错。固定项目数时，可以枚举 peak threshold cells，再以流/LP 处理支持和分段线性社会损失，得到 `(n+1)^{O(m)}` 的 XP 草图；这只是候选路线，不是已交付算法。

本次全仓比较没有找到该具体 `min over all NE of weighted L1 social disutility` 的正式对象、紧复杂度或 hardness 证书。因而保留为**未决派生问题**，并明确三种状态分开：NE 构造是来源所述 paper fact；非凸中点是来源所述结构事实；固定 `m` 的 cell/flow 是未完成的算法草图。不得把“非凸”升级为 NP-hard，也不得把顺序 greedy 或任意正线性目标选择当作已证等价。

## N6：两类 pair-strategy 纯 NE 复杂度

N6 的模型是无权拥塞、每个策略恰为二资源子集、费用非负非降；玩家分为两类，每类共享一个显式 pair-family。目标是对所有这样的输入求任意 PNE 的多项式算法，或给同一受限类的 PLS-hardness。来源特别要求区分 global Rosenthal potential 最小点与 local minimum/PNE。

母论文 Bilò–Fanelli–Gourvès–Tsoufis–Vinci 的公开边界在当前树的 `weighted-congestion/tools/evidence/atomic-games/candidate_report.md` 中被重述：对称 size-2 的**全局**最小势可用 matching，而一般 size-2 全局问题 NP-hard；§6 把一般 size-2 PNE 复杂度列作未来问题。该全局 NP-hard 结果不能移植为局部 NE 的 PLS-hardness，matching 也不能自动保留两类玩家的配额约束。N6 仅是从公开孔洞派生出的两 type 限制，当前没有独立 reduction、算法或精确 toy 证书，故仍保留为候选/待核验。

接续时第一义务是严格恢复母文 Theorem 2 的 matching 归约，并追踪 type 标签和资源重复是否破坏增广回路；同时逐行核对 2025–2026 后续工作。若只解决不相交资源或公共必选资源，模型退化，不能宣称 N6。

## N7：有限双权势与 smoothed 动态的组合风险

N7 要求权重 `{1,2}`、非负二次成本，在非零系数上加入 bounded-density 噪声，按真实原博弈 `(64/59)(1+epsilon)`-改善动态证明期望多项式步数，并给 bit complexity。来源把它归并入原子拥塞 AT03，并明确指出：64/59 type-scaled 近似势和 Giannakopoulos 的 smoothed FPTAS 截断倒数/密度分析，可能只是短黑盒组合。

当前[有限双权近似势与非对称精炼目标的不同合同](../../../weighted-congestion/state/资料/有限双权近似势与非对称精炼目标的不同合同--资料.md)只承载 64/59 的全人数、非负多项式分项和有限终止；它不保证改善序列长度多项式。weighted-congestion 的文献资料页记录通用排序积分势、存在性与动态边界，但没有一个把相关/有界密度扰动直接接到 64/59 真实动态的完整证明。于是 N7 处置为附属工具候选：必须先写噪声模型、成本表示、扰动是否独立、真实成本与辅助势的停止条件、截断积分的下界和输出位复杂度；仅把两个 theorem 的名字接在一起不算完成。

## 证据等级、模型边界与接续

本来源包含四种不可互换的内容：

1. **文献事实转录。** 例如树/单环 best response 的已知界、Leontief/Fisher 的作者题源与后续接口、size-2 global matching/NP-hard 边界。当前页按“来源报告的事实”使用；需要对外宣称时仍应逐定理核对原论文。
2. **内部完整对象。** N3 的 active-cell 判别、三项目精确反例、m=2 边界和 `2^R` 识别，N4 的共同形状 KKT 等价，均以结果树正式页承重；候选卡不能扩大其量词。
3. **有限或拟议证据。** figure-eight Markov toy、N3 网格/`Fraction`、N5 固定项目 XP 草图、N7 64/59 与 smoothed 接口，只能作为复现入口或路线信号；没有把抽样、Monte Carlo、有限 LP 和“看起来可组合”升级成定理。
4. **开放与障碍。** N1 的 cactus 全类期望界、N5 的选择问题紧复杂度、N6 的两 type PNE 复杂度、N7 的真实动态组合以及一般 N3/N4 分类仍有明确缺口。N2 的原算法题则因 Fisher 接口被淘汰；这不是说所有变体已解。

第三阶段若建立关系，至少要保留以下边界：N3 与 N2 共享预算聚合背景但效用和量词不同；N4 的共同形状规划不推出 polyhedral cloning 分类；N6 的 local PNE 与 global potential minimization 不可互换；N7 的有限终止与 expected polynomial runtime 不可互换；N1 的 player-specific singleton 图和 weighted-congestion 的正成本多项式模型不自动相同。暂时没有证据的关系应记录“未建立”，不为图连通而造边。

## 逐源语义处置建议

对源 ID `a177ad0d3653d7eaf428`，建议在 `clean done` 记录中使用：

- `disposition: integrated`，目标为本页；
- `read: full-source`，说明已读 16,446 字节全文并核对 N1–N7；
- `compared: cross-archive`，列明 budget-games 三正式对象、weighted-congestion atomic candidate report、64/59 资料页和相关文献边界；
- `unique_content: candidate-map-and-same-day-routing`，保留七卡的原始量词、淘汰时间线、反对意见、最低成果与接续义务；
- `decision: retained-review-not-theorem`，明确 N2 已知 Fisher 覆盖，N3/N4 部分吸收，N1/N5/N6/N7 仍为候选/附属路线；
- `evidence: current-formal-pages-and-source-card`，不要把未找到后续文献、有限 toy 或未运行的外部脚本写成证明。

本页不作外部新颖性、作者优先权或 2026-10-20 之后最新文献状态的认证。若后续出现真实论文覆盖或新反例，应新增版本对象，保留本源的历史候选判断和它的模型边界。
