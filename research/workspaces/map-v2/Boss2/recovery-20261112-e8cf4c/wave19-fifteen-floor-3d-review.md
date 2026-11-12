# 十五份 fractional floor 锥记录：fresh 数学准备审查

本报告只准备后续正式 fresh worker 的数学比较，不是 receipt，不执行领取、read-add、队列或登记写入。只读 clone 为 `/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`，唯一新写文件为本报告。

## 当前合同与身份

本次始末读取的本地当前任务均为 `customer-attraction-3a-3a-a7dc194365f674bf`，`state=available`、`owner=null`，未改版；任务文件 SHA256 为 `10914d8903ee4870f2dcc29c1a19c3a1b9bf3f236afefd1886b3e6a3382947f8`。这只是所读 clone 的快照，不代替 Root 正式派工前的最新远端归属核对。

唯一核心为 `customer-attraction/fifteen-fractional-floor-cone-records-full-matrix-identity-and-single-client-zero-debt`，当前 v1、`kind=exact-finite-certificate`、`truth_status=proved`，task input pin 为 `231f2691fdfd4fa0e8c57da7ba48b19adbe6b51cab43b39fcba3a402c00aa0f7`。初始 `read_object_ids=[]`。正文 SHA、六份必要 evidence SHA 都与任务及当前登记一致。

核心的完整实际结论是：15 条原记录只有 initial/trace 分成两型，其余 12 字段相同；共同最终点只含 mask47 一个单位客户；共同完整策略在全部 259 有序决策节点成为 SPE；504 个计数动作比较去零去重为 306 条 63 维有理行，整数化矩阵 12Γ 与 15 份原浮点矩阵按原转换逐格一致；该点真正自由值 `t4=1/4`、根收益 `u1=1/4`、债 `δ=0`；原二进制 q 不精确归一，原 p/z 只给精确 Fenchel 下界 `1/4−2^-106`。它不是 15 个独立实例，不是整个固定锥的 floor 下界，也不是四人或六人全称福利定理。

最终所读 `research/registry.json` SHA256 为 `57f40e76c4bc4ce63f09ea2293a612da61a4f7453a67bff0fec8b23b34ca2271`，其中 `edge_files` 恰有 2285 路径。仅沿这份清单打开边并查其实际 `source_ids/target_ids`，没有任何 canonical 边以本核心为端点。因此没有可原封不动引用、已支付本核心的精确正式边；未把磁盘上的其他 JSON 或证据包 `relationship-review.json` 当成正式边。

## 已实读及复用范围

完整读了 AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md、当前任务定义、核心完整登记、核心全文、共同目录完整历史模型全文、证据 README、12475B 审计驱动全文及其 execution record。`exact-review.json` 全文件解析，读取所有字段、两组记录身份、全部 15 个记录的初值/trace/指纹，以及单独数学结果。压缩 ledger 完整解压和 JSON 解析，读取所有六个结构的域、维数、来源位置与有序历史记录；原 5494570B JSON 完整读入解析并核 SHA/15×14 字段及 policy/rows 域结构。未声称人工逐字重读 289170 个数值或重新独立认证这 289170 次转换。

本轮对成熟数学复用的是正文自足证明、已读驱动的精确算法及已存成功事件。没有执行原 producer、Search、BI、SPE/IC 验证器、LP/MILP/SLSQP、随机搜索或大证书重放；没有导入审计驱动。读取和解压不是新的一次数学审计成功事件。审计驱动 `run()` 末尾会重写成熟工件，故本轮只阅读其实现。

还实读了下列当前登记端点的核心合同及承重正文：

| 实际 ID | 版本/状态 | 本轮数学用途 |
|---|---|---|
| `CAG-MODEL` | v1 / definition | 全有序历史、真实偏离后继、弱平局、标签别名及根/背景区分 |
| `CA-STRATEGY-CONE` | v7 / proved | 真正完整 IC 锥的充要性、去零去重与有理清分母；固定规模有限表示不等于普遍上界 |
| `customer-attraction/free-fractional-background-security-floor` | v2 / definition | 全目录自由 q、竞争质量 r−1、b 的合法性 |
| `M-f3439db394f148d598fddb438c676f01` | v1 / proved | t≤v 与合法前缀嵌入；不支付逐人 FF |
| `customer-attraction/free-fractional-minimax-tangent-cover-price-bounds` | v1 / proved | 凸 minimax、精确切线下界及完整鞍点双边付款 |
| `M-b952a96f6aef4fd0a4bd5195fbb22c13` | v1 / proved | 根静态 OPT≤LP≤(2m−1)t 与 B 预算；顺序桥另付 |
| `customer-attraction/cartesian-bank-individual-fractional-floor-counterfamily` | v3 / proved | 已否一般逐人标准 FF，且明确不否聚合/half |
| `CA-SECURITY-CONE-DUAL` | v3 / proved | 固定 σ,p 的 (A)⇔(T) 及严格失败提取，不把有限实例作一般双向证明 |
| `customer-attraction/common-static-q-certificate-generator` | v1 / proved method | 同一个 Q 同时 cap 全查询的充分模板，尚无本源输出 |
| `customer-attraction/fractional-and-cone-auditor-contracts` | v2 / proved | 21 个指定完整策略锥的显式 Q/λ 证书；只作量词对照 |

六人目标当前正式 ID 是 `customer-attraction/six-providers/exact-six-full-history-half-cover`，v1、open。读了其完整登记合同；其必要数学目标与已经全文读过的共同模型一致。本报告没有把其余 46 份六人正文假称重读。

## full matrix 到完整 SPE：具体支付的步骤

真实模型是四名单位提供者、六个可区分共同标签 A/B/C/D/E/F，63 个非空兴趣类型。最终只有 `w47=1`，故 A/B/C/D/F 都覆盖同一客户 x，E 为空；其他 w 为正零或负零，数学值均零。五个相同覆盖标签仍是五个行动。六标签不是六玩家；空 E 仍是合法离轨动作。

保存 policy 的 84 个条目本来是 `(prefix count q, terminal target t, action a)`，一般不能忽略 target；本文件额外具备“总和 0…3 的每个六维计数前缀恰出现一次”的完整域性质：`1+6+21+56=84`。据此定义特定完整形式策略

`σ(h)=s(count(h))`。

默认动作 C，仅空/C/CC 改 B，CCF/CCC/ACC 改 D，CCE/CCD 改 F。因每个合法有序 h 都有唯一 count，动作图在全部 `1+6+36+216=259` 个决策历史有定义。这是本 σ 恰好可按计数描述的性质，未把一般完整 SPE 限制为 Markov 策略。

126 个终局索引按 `combinations_with_replacement(range(6),4)` 给出。成熟账本逐项认证 84 个保存 target 与沿上述 s 的真实完成叶一致；根 index71 是 `(0,1,3,0,0,0)`，有序根叶 BCCC。于是每个强制行动 b 后的真实完成叶是 `Z(q+e_b)`，不是把原实际后继冻结。一般 `(q,target)` DAG 若同 q 有多个 target 或缺动作孩子，本文件的简化不适用。

每个客户兴趣类型 M 的真正有理行是

\[
\Gamma_{q,b;M}=\frac{1_{s(q)\in M}}{c_M(Z(q))}
-\frac{1_{b\in M}}{c_M(Z(q+e_b))}.
\]

零分子定义零；正分子保证分母正。过去动作含 E 的效果保在真实总负载中。84×6=504 个计数比较含 84 个自身零行，420 个非零来源位置去重为 306 个有理行。四人分母整除 12，ledger 中 `H=12Γ` 是准确的 306×63 整数矩阵，字母表为 `{-12,-6,-4,-3,-1,0,1,2,3,4,6,12}`。成熟审计认证原 15×306×63=289170 个 float 系数等于这些有理系数按原 float 转换的值；这不是把十进制 `0.3333333333333333` 当作有理 1/3。

对任意 h，其当前动作、规定叶及每个偏离叶只取决于 count(h)，故 h 的完整有序 IC 正是相应计数行。展开只复制行，没有丢失一种真实偏离。由 `CA-STRATEGY-CONE` 的 CONE 定理：

\[
\{w\ge0:H w\ge0\}
\]

恰是使这份特定 σ 成为完整 SPE 的非负代数客户锥；整数点表示不同单位客户，有理点可齐次清分母。这个“全锥”陈述只认证资格域的准确性，不认证任何 nonlinear floor 目标在整个域上非负。原 producer 的 LP 另加实际叶 `W=1` 及去全兴趣坐标的 bound；这些不是一般锥定理假设。此保存点碰巧总客户质量也为一，不使“实际 W 归一”变成“总质量归一”。

保存单客户点的 SPE 还有短解析证明：在任意有序历史，令过去已有 v 位覆盖 x，尚余 r 位含当前。全部规定动作均覆盖 x，遵从得 `1/(v+r)>0`；改任意非空别名仍得同一数值，改 E 得零。故全部历史和任意弱平局都付款。成熟有序账本的 1554 次含自身比较中，259 次严格（改 E），1295 次平局；非自身 1295 次中有 1036 次平局。该解析证明与矩阵身份互相相容，没有重新执行这些比较。

因此 full matrix 付清的是“同一原完整 σ、全部有序历史、全部真实改变后续局”的定义义务，以及该单位点的 SPE 资格。它没有付清全部 σ，也没有付清本固定锥上 `u1−t4≥0` 的最小值，更没有把原数值搜索变成全局最优性证书。

## 单客户自由值、原二进制 q 与假负债

该点的完整自由背景仍是 `q∈Δ6`，非限制在实际 B/C 支持。唯一客户的覆盖边际为 `α(q)=1−q_E≤1`，所有非空查询收益为

\[
g_a(q)=1/[1+3\alpha(q)]\ge1/4,
\]

空 E 查询为零。因此全单纯形上的 `t4≥1/4`。另立有理背景

\[
q^*=(1/5,1/5,1/5,1/5,0,1/5)
\]

是精确可行概率，α=1，所有非空查询恰为 1/4，给 `t4≤1/4`。所以 `t4=u1=1/4`、`δ=0`，并且 W=OPT4=1。q* 是新标明的见证，最优背景并不唯一：所有 q_E=0 的概率都达到同值。未回写原 q/z。

这也确实是已登记切线定理的一个精确 specialization：取查询 `p=δ_A`、切线点 q*，则 `K=1/4`、五个非空标签的 `H_a=1/16`、`H_E=0`，所以 `Σq*_a H_a=max_a H_a=1/16`，LB 的补偿项为零。它给精确下界 1/4；q* 的全查询 cap 给匹配上界。静态定理提供下证书方法，完整 SPE 及 u1 值另由前节付款。两个步骤不互相冒充。

原保存 p 恰为 δ_A，二进制字面精确归一；原 q 的每项非负，但其精确和为

\[
1+\frac{155666615761993}{2535301200456458802993406410752}>1.
\]

其 E 坐标亦严格正。原 q 不是通过精确约束的背景证书，不能静默归一、不能称原 q*、不能因 SLSQP success 就将它当精确鞍点。另立 q* 只支付真正自由值，不修补历史原件。

原 `z47=1/4+2^-54`。生产程序页完整写明任意合法 p 和 z≥0 的 Fenchel 下界不要求原 q 合法，亦不要求 z 是原 q 的逆分母。因此仍可独立准确计算

\[
L=2z_{47}-4z_{47}^2=1/4-2^{-106},\qquad
\delta=u_1-t_4\le u_1-L=2^{-106}>0.
\]

这是债的正上界，不是负上界；也不能只靠该下证书推出 δ≥0。δ=0 是前述全域双边证明。原 trace 的 `root_value=1/4+2^-53` 导致 `actual_debt=−2^-53`，不是严格有理反例。每轮 `linear_upper` 使用当轮更新前冻结的 p/z，不能与最终保存 p/z 的 `2^-106` 上界逐轮强行同一化。两组原 initial/trace 的差别、全部负零和原运行日志缺项都保留；本轮未猜原 argv、seed 文件 SHA、计时或正常退出事件。

## 从该有限点到一般 floor、聚合与 half 仍欠什么

`free t` 是静态平均负载分母；真正整数混合安全值 v 保倒数的期望，已有 Jensen 只给 `t≤v`。二者更不是原完整策略在偏离后的自适应真实收益。标准 FF 是所有合法 b、余 r 人、每份完整 SPE 都有当前 u≥t_r(b)，它已被当前 v3 银行族在每个 m≥3 严格否定；例如 m3 根 `u1=3/2<t3=8/5`。本十五条零债点不能支持该普遍 FF，也不构成银行族的证据或新的严格反例。

若某份 m 人策略实际每个节点另有 u_i≥t_(remaining)(b_i)，嵌入才会给 `u_i≥t_m(0)`，合计 `W≥m t_m(0)`。静态根界另给

\[
OPT_m\le LP_m\le(2m-1)t_m(0).
\]

所以强聚合 `W≥m t_m(0)` 或较弱金额 `W≥(m−1/2)t_m(0)` 都足够 half。静态界、嵌入及该条件推导仍真；一般逐人 FF 已假，不再是尚待无条件证明的付款。银行族本身 `W−m t_m=m(m−1)/(2m−1)>0`，且 `2W−OPT=m+2>0`，还满足 W≥m v_m，故它不否聚合或 half。本单客户四人点同样不解决这些全称命题。

全锥安全证书确能比一个点多支付量词，但必须交其具体等式。当前 `CA-SECURITY-CONE-DUAL` v3 证明的是：固定 σ,p，整个 Kσ 上的 `(A)` 等价于存在 Q、λ,r≥0 的逐类型 `(T)`，Q 可依 σ,p，不能依客户 w；无精确证书时可提取严格违反聚合桥的有理点。它并未证明所有 σ,p 的证书存在。

共同 Q 模板更要求一个 Q 同时 cap 所有纯查询，每查询可用不同 λ。21 份成熟成功证书的确由

`c/n−E_Q f_B(a)−Γᵀλ_a≥0`

与任意锥点内积，支付各自全部非负客户质量上的 `W≥n v_n`。它们是 19 个 5人7题、1 个 5人8题和1 个 6人8题的指定策略；本文件是另一份 4人6题 σ，无其 Q/λ/逐列残差。它们不能迁为本锥的 floor 下界，亦不能作为一般 `(A)⇔(T)` 双向定理的逻辑 contribution；最多作 checks/context 的实例或本报告的量词对照。未重放这些大证书。

若要证明本锥所有 w 的 `u1≥t4`，仍需对本 Γ 和确切目标提供全 w 的数学证明或适当证书；单点 Hw≥0 和 t4 值均不够。若要 half，须支付恰六人、任意有限标签数、每份完整历史 SPE 的全部量词，或给覆盖这些量词的统一论证。当前六人正式问题仍 open。四人与六人、固定六标签与任意有限目录、一个客户点与整个锥、有限多个锥与所有策略均不可替换。

## 可交正式 worker 的候选边及应保留的零边判断

本报告不创建边 JSON，不写 receipt。下列两个候选是已付清的局部数学贡献建议，正式 worker 仍应按最新 task/registry、实际 read-add 和最终 edge-bind 检查。两者都不应写覆盖核心整条登记的 `whole_result`。

**候选一：CA-STRATEGY-CONE 到本核心的完整矩阵语义。**

- source ID：`CA-STRATEGY-CONE`；target ID：本核心。
- 建议 kind：`specializes`（或解释清楚的 `implies`）；数学关系为 unconditional 的局部 contribution。
- `contribution.result`：对正文指定 84 个唯一完整计数前缀策略，target 与真实完成叶一致使 σ(h)=s(count h) 在全部259有序历史有定义；每个有序 IC 行等于对应计数行；故精确 H=12Γ306 的非负客户可行域恰保持同一完整 SPE，特别保存 w=e47 是该域中真实单位客户点。
- `contribution.remaining`：CA 一般定理不推出 15 记录的逐字段身份、不自行认证 289170 个原 float 转换、不计算真正 t4、原 q/z 误差或零债；这些仍须本核心自足证明和成熟 ledger。没有整个锥 floor/最优性结论。
- 数学价值在于付款“压缩输出→全部有序历史真实 IC”，不只是共用模型 hub。必要证据为 CA 正文的“定理一：完整 SPE 的精确重数锥”、核心 §§3–4、当前 H/target ledger 与审计算法。

**候选二：自由分数 minimax/切线定理到本核心的单客户 t4 部件。**

- source ID：`customer-attraction/free-fractional-minimax-tangent-cover-price-bounds`；target ID：本核心。
- 建议 kind：`specializes`；unconditional 的局部 contribution。
- `contribution.result`：在当前 w=e47、b=0、r=4，取精确 p=δ_A、q* 五非空均匀，K=1/4、非空 H=1/16、E 的 H=0，LB 精确给 t4≥1/4；q* 全查询 cap 给 t4≤1/4，因而结合独立 u1=1/4 得 δ=0。原 p/z 的 Fenchel 仅给 `1/4−2^-106` 下界，支持原浮点负债不能当精确严格证书的解释。
- `contribution.remaining`：完整有序策略及 u1、15 记录身份、全部矩阵原系数绑定、原 q 精确和>1仍由本核心相应证据承担；不推出任何其它 w、σ、背景或人数的逐人/聚合合同。
- 最精简的边只保 q* 切线双边部件；若连原 p/z 也写进 contribution，必须同时引 producer 附件中“Fenchel冻结行为什么给全背景下界”的准确公式，不能把未写 z 公式的登记 statement 单独当证据。

必要 read-add 的最小逻辑端点是以上两个 source 实际 ID。为了将实际比较范围、当前模型和已知反驳完整 pin 住，建议同批另按真实阅读加入 `CAG-MODEL`、`customer-attraction/free-fractional-background-security-floor`、`M-f3439db394f148d598fddb438c676f01`、`M-b952a96f6aef4fd0a4bd5195fbb22c13`、`customer-attraction/cartesian-bank-individual-fractional-floor-counterfamily`。后三者只承载本报告的具体量词/half付款比较，不因读到它们就必须造边。`CA-SECURITY-CONE-DUAL`、共同Q生成器与21锥对象可作为已读语境端点；不需要为了方便 linked 全加成逻辑前提。

特别注意，生产者程序页 frontmatter ID `customer-attraction/free-fractional-epigraph-fenchel-policy-cone-probe-contracts` 当前不在 registry.objects，不能作实际 read-add/边端点。该页当前 materials disposition 为 attachment，owners 是 `M-326a39f56eab42ada20a3f1a507d73ca`、`M-45083ccacddf456690d2e260cf1ff3ab`、`cag-background-remaining-profit-fractional-floor-and-fixed-population-identities`。本比较可直接按准确 path/SHA 引该附件，不应为借程序名而错用 owners 的不同 theorem，或新造同义节点。

不应画的边包括：本核心 refutes 一般 FF（该点 δ=0，根本不是严格反例）；本核心 implies 一般 FF、聚合或六人half；银行族 refutes 本核心（不同输入，无矛盾）；21固定锥 implies 本锥/一般锥双向对偶；仅共用完整模型的定义 hub；浮点原 rows 以精确十进制系数直接 implies SPE；原 q、SLSQP success 或 `linear_upper<0` 单独 implies 精确负债。

已全文对照三个 canonical 近邻：

| canonical edge ID | path / SHA256 | 与本任务的区别 |
|---|---|---|
| `cag-1213ac-strategy-cone-to-complete-dag-reweighting` | `map/edges/boss6-cone-metadata-repair-98dddd240ce7e2a2/strategy-cone-to-complete-dag-reweighting.json` / `b1e189a41f7b3a4cb213d79c9e699ee5c3cbdf880d344bf4ec33c4c8169a1d1f` | 完整 (count,target) 后继模板，target 为另一七题五人程序对象；可比较展开证明，不能替代本84 target及矩阵身份 |
| `ca-e489-full-policy-cone-validates-fixed-row-dual-interpretation` | `map/edges/boss6-cone-metadata-repair-96749e83cb905a39/full-policy-cone-validates-fixed-row-dual-interpretation.json` / `7728b6db2a5203fadbb15076be8671eeb4433124f84c600f6392ed28982e557c` | 另一四人六题 σ、310行、mask49及252份ROW对偶；与本非恒动作306行、mask47 floor不同 |
| `cag-3be0-tangent-saddle-on-five-customer-support` | `map/edges/customer-attraction-3a-3a-3be0f02a605fe495/tangent-saddle-on-five-customer-support.json` / `d7d1075ca75bb292cd765187d67d08b999a42052d55c586d26ed55862ed6af5a` | 五客户二人三题的8/3及2两个分数cap；同一静态定理的其它特化，输入/目标不同 |

它们可以帮助写准确证明风格，不能按原 SHA 当成本核心正式逻辑边。若正式 worker 判断两个局部关系不值得新增，应在本核心比较范围和 reason 精确保留上述已读端点与未付量词，再交零边；不应为 linked 扩成 whole 结果。

## 证据路径与字节针

下表 paths 均相对本只读 clone；SHA 为本轮实际读字节计算。该表是审查定位，不是新登记清单。

| path | SHA256 |
|---|---|
| `archives/customer-attraction/state/计算/十五份自由分数地板锥记录的完整矩阵身份与单客户零债--计算.md` | `beb02f51c558cc199ad19a61d62cd9dcbdf519db7fd6157d43ab94ca009adb80` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/README.md` | `08db674de9799e6e313bb29a3b97ac735ab1f1b3a357dc12320876d1313e3dd1` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/audit_fifteen_records.py` | `bdbb5fa55c05803c703bbe6aff58fad7bfdba69428ac29baf5cd995eb2534d79` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/replay/execution-record.json` | `5b6869b7f3a9de80e2cd21e4e02ea528c151865bf3f3b3b112a7bbd89f4a0a28` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/replay/exact-review.json` | `bab2a2019a7b904c18f89ca6436c37e8b024bfb24e4471f556f2217586bb10ad` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/replay/complete-exact-ledger.json.gz` | `dcaa9b48b2c7858ae39eb2c5eae1983e0dd0837b3d878f5ca146549bbba1f71c` |
| 同 ledger 解压后的 117001B 原始字节（未另写文件） | `4667f6aa2b34c18efbde8c16eb71f76234cff3d9d3b27ee30bc327333b26a2a9` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/original/fractional_floor_cones_n4k6.json`（5494570B） | `7d3755c796965db4fb5c8e9217570a2a9e3c3b3b06d9f2109636cd3044451723` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/source-manifest.json` | `bc9c7ddaa5d3432bc451d1d4f484598e267ad3af1909a968a62fe1af334bae91` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/dependency-and-comparison-reading.json` | `786e1b6e8b323cd9d9f42c2cab8674925ffb3c101cb537c94e9a7361e39a37a9` |
| `archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/relationship-review.json` | `8f254cfe0798afd8756a78b9772dbe99dc4d7fb096284e20261d02d2539cd85a` |
| `archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md` | `ae4bcfd424eca8d4e3d79965f72182c0b2c8eefb72e74b44c2521b519f7aad39` |
| `archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md` | `0e2e6393acb153498a3b4d0a8091b3a10976f211945e612c96eb1b2d8982c2cd` |
| `archives/customer-attraction/state/定理/自由分数门槛的凸对偶与覆盖价格界--定理.md` | `2a12cd3e5699cda7dea1458f5a7432455dfbc438a8940572d1115a99d2ac5465` |
| `archives/customer-attraction/state/程序/自由分数门槛的上界求值与Fenchel策略锥探针--程序.md` | `299077b65457511ca60ab3115603a80aff294a9e1885a283122f5b62ceba1718` |
| `archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md` | `46c7a8df14fb3dd858e4fc827e2de7f000966d49ac4cd9ef7bb2b05777957a80` |
| `archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md` | `b279e1f63f08b961365a2cbc0173530de7090fd1c7beefc1a42c585ef6e58cf5` |
| `archives/customer-attraction/state/计算/共同静态Q证书生成器--计算.md` | `d45ad34630dca9e5afb82b882b5c2373b4b031fa0e2b6fb0283b8fe1967a5289` |
| `archives/customer-attraction/state/资料/客户分数负载覆盖与固定策略锥的审计合同--资料.md` | `0013a2a0986eb81e11735bc2a794e47e5f650cad43c173817a02a14f01ddb3aa` |

旧 `dependency-and-comparison-reading.json` 中银行正文记的是当时 `060f9ecc…` 版本；本轮比较用当前 registry v3 和实际 `46c7a8df…` 全文，未用旧比较清单冒当前银行针。核心自身上述七个正式 reading refs 没有发生 SHA 改变。

成熟 ledger 的实际六结构为：126 个终局索引、84 个 count/target 对账、259 个有序历史全动作记录、306×63 整数行、306 个保存点 slack、306 组行来源（总420个非零来源位置）。成功事件来自 2026-11-02T14:38:33.601371+00:00，elapsed 0.9154928940006357 秒，returncode0、断言开启、stderr空；本轮没有伪造第二次成功。最终报告保留所有必要数学边界，正式领取与资产写入留待 Root 另派 fresh worker。
