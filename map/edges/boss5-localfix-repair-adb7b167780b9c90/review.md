# 三色固定 palette 硬度 v3：完整关系保持与来源增量修复

## 本轮结论与当前输入合同

本交付对应任务 `boss5-localfix-repair-adb7b167780b9c90`，替代旧任务 `unrelated-machines-3a-3a-8091c8950447d8fa`。只读核验时 HEAD 与 origin/rebuild/research-v2 均为 `e096fa9ffa1aa598b09aa106e52067d37681ac0e`，当前 task owner 为 Boss6、state 为 claimed，claim request 为 `bcdc0d1670284bb3812ab5e87e2975bf`。三个 `research show` 返回的 registration_pin 与任务 input_pins 逐一相同，body/evidence 均 current。

| 端点 | 当前版本 | 当前 registration_pin |
| --- | --- | --- |
| `M-d007675a9ed240898c90e831af80b092`：三色固定 palette 目标 | 3 | `568c2356602c664bf481424bd361d25375f32b1d853c9f21952c4237a96092b5` |
| `M-ab4a576ed0be482b89d4a646ffc102b9`：perfect exact4 源 | 3 | `74280017a599b84a48878085e8d9869d16d657aa712f51458f820383ad826072` |
| `M-922feb7b429f49d4b5f13ca51b34aae7`：八色小独立集源 | 3 | `9d9c5ff02a494c05d6cd44d8a20732d81d72852f26938f3bee195c24192887be` |

核心的整条目标为：对每个预先固定整数 k≥3，有限无向图上，区分 YES“存在合法完整三着色”与 NO“不存在合法 k 着色”是 NP-hard。它也可精确表达为 PCSP(K3,Kk) 的 promise G→K3 对 G↛Kk；这里不新增模型节点。YES 不是仅有 1−τ 比例的可着色顶点。NP-hard 本身是归约结论；再推断不存在多项式算法时才附 P≠NP。

本轮保留两个独立的完整充分证明，分别以一个源对象为 ALL 前提，均为 accepted/unconditional/whole。两条并非联合必要输入；没有只推出目标的一步后冒称整句。旧两条 canonical 的文字和数学仍有效，但其 endpoint_pins 绑定 v2，不能将旧绑定当成当前 v3 绑定。本包因此在新 task 目录建立独立新 ID，并由 Root 在最终语义确定后 native bind/check；不改旧 done 资产。

## 继承的成熟证明与本轮实际阅读

旧任务 review、reading-ledger、receipt 与两条 canonical proof-bearing 字段均已完整实读；成熟 `comparison-proof.md` 与当前共享正文亦完整实读。上一包对 FMW 冻结 PDF 的具体段落实读、GS20 正式 12 页全文实读和 Root 核验记录，作为有明确 SHA 的历史证据继承。历史 ledger 全量嵌入本包 ledger 的 `inherited_reading_records[0].record`；旧 review 全文在本文末尾以历史原记录保留。

本 worker 没有重新抽取/渲染 FMW 或 GS20 PDF，没有声称本轮重新审读 119 页 FMW、重新读 GS20 全文或重新复证其所有技术引理。本轮新增数学工作是核当前端点的完整陈述与量词、独立检查精确 source delta、核 MZ 冻结文本的连续小范围，并据此判定旧的两个 whole 结果在 v3 是否仍完整。父 Boss 既有 `remote-mz-pgate-s3-delta-review.md` 完整实读并作为单独历史审查证据；本轮只复核与本 task 有关的 F1 增量，不接管其另两个 foreign-task。

## 第一条完整关系：perfect exact4 支付三色固定 palette 目标

源对象 `M-ab4a576ed0be482b89d4a646ffc102b9` v3 给出：每个固定非退化 0<ε<1，存在常数字母表界 r，使有限二部 exact4-to-1 约束多重图的 val=1 与 val≤ε 承诺区分 NP-hard。FMW Definition1.1 每边将左字母表分成四元块、右字母表分成对应单元块，故 |ΣL|=4|ΣR|；脚注明许平行边。r 是字母表界，不是 Condition3.12 的同名内部参数。YES=1、exact4 和边重数都保留。

历史成熟证明核过附录 B 的 exact 化：先从 sub-4 gap ε/2 出发，取 h=ceil(4/ε)，左右标签均乘 Z/hZ，每条旧约束放 h 个带独立约束的平行边。旧完美标签均取同一新坐标，严格保 val=1；不满足旧约束的标签对至多通过两个新约束，故新 val≤旧 val+2/h≤ε。新标签界 hr、约束数 h|E|；h,r 均先固定。既没有把 sub4 默当 exact4，也没有去重约束或声称常数最大度。

GS20 Theorem1 的2020原文条件于某固定 d 的 exact d-to-1 conjecture，其 Conjecture3 所需的完美 YES、任意小固定 soundness、标签比和多重图合同，在 d=4 由 FMW Theorem1.6 全部支付。应用已证的 GS20 §2.1 induced-list 源桥与 Theorem9，取 q=2d=8。满足源标签 σ 给 long-code 顶点 x 颜色 x_{σ(w)}，边两端颜色不同，故得到完整8着色 YES；大独立集则经 influence/list decoding 在正比例源顶点内满足全部约束，与源 promise 矛盾。

此处保留历史审查的安全常数处理：坐标阈值 δ0/d、总 degree-ds 影响≤ds 时，可取列表界 ceil(d²s/δ0)，不使用 §3.3 显示的较小精确常数；d 固定，不改变 Theorem9。若独立集密度≥η，密度≥η/2 的 block 至少占 η/(2−η)≥η/2；Theorem7 按 η/4 调用可满足严格门槛。所有这些均是继承的已支付论证，不是本轮新造的条件。

对每个目标 k，GS20 Lemma8 的有限 arc-graph 归约链需要某固定源 palette C0(k)。取固定整数 C≥max{8,k,C0(k)}，再取固定 0<δ<1/C；若源 NO 图可 C 着色，则某颜色类至少占 |V|/C>δ|V|，与独立集 gap 矛盾。因此该源也满足所需的 non-C0(k) promise。Lemma8 使用 b(n)=binom(n,floor(n/2)) 及4→3的有限末段，把固定8色 YES 的任意常数 palette 硬度降为完整3色 YES、non-k 色 NO。

量词顺序是 k→固定 C/有限归约链→固定 δ→FMW 固定 soundness/字母表→实例规模。由已证源硬度与已证归约组成确定性多项式归约，支付核心全部目标。FMW Corollary1.7 给同一完整 promise。没有遗留未证 d-to-1 猜想，没有把近完美 2-to-1 或 MZ imperfect completeness 代入，也未调用 FMW Remark1.8 的稍超多项式版本。

## 第二条完整关系：八色小独立集 gap 支付三色固定 palette 目标

源对象 `M-922feb7b429f49d4b5f13ca51b34aae7` v3 的合同为：每个固定 δ>0，区分 YES“8-colorable”与 NO“α(G)/|V(G)|<δ”是 NP-hard。本调用取上段固定 0<δ<1/C≤1/8，确保两个 promise 不相交；不依赖较大 δ 的退化区间。

给定目标固定整数 k≥3，先固定 GS20 Lemma8 对 q=8、目标 k 所需的 C0(k)，再取固定整数 C≥max{8,k,C0(k)} 和固定 δ<1/C。源 YES 保完整8着色；源 NO 如可 C 着色，至少一个颜色类为比例≥1/C>δ的独立集，矛盾，故源 NO 非 C 色且非 C0(k) 色。于是源提供 Lemma8 所需的固定8色 YES 对 non-C0(k) NO，归约输出完整3色 YES 对 non-k 色 NO。

C、δ、arc 变换次数及所有 PCP 常数在输入规模之前已按 k 固定。因此该条单独支付核心整句，是另一条 accepted/unconditional/whole 蕴含；它不把输入的同一张8色图说成3色图，也不需要再把 exact4 对象加成其共同前提。FMW Corollary1.9 是源定理的既有证明入口；GS20 Lemma8 是图 promise 的已证归约。外部原始 arc-graph 定理以及 GS20 导入的 DMR09/invariance 输入沿历史完整证据入口使用，没有声称本轮另审原始论文。

## 唯一来源增量：MZ Claim3.2 不进入两条支持链

本轮独立执行只读 `git diff --unified=15`，精确比较 base `56650ea6813513decee236e0353647e07ff7cc63` 与 remote `724c402aeef432b2e6848fe1b1b67a0ddae33ba3` 的共享正文。该文件只新增 §3.2 内关于 MZ Claim3.2 的一段（连同空行为2 insertions / 0 deletions），FMW §2.1、两条图应用及现有成熟 comparison-proof 均无内容变化。base blob 为 `b0ca7bb5977540232e44e52623a57b43c03e34ee`，SHA-256 `0e1f9f27706ce17087037ef05c6265d8f3d2e6ede5801cdbe87b559c4ff9f2ac`；remote/当前 blob 为 `0322caaf852b786f77dd438ae096c226f25f7915`，SHA-256 `6d5be138de6825a1208776cbb485316c5b0e9d197870e32ab7c1d8ca5cf2f746`。base 仅读精确差分上下文并核完整字节 SHA，不称 base 全文重审。

冻结 MZ 文本实际连续阅读820–953、1315–1342、2988–3021行。按 §3.1.3/§3.1.4，暴露事件 E_i={U_i≠V_i 且 r 份 advice 全零} 的概率是 βq^(−r)。原句“U_i=V_i，或 U_i≠V_i 且 advice 全零”实际概率 1−β+βq^(−r)；把后半改成“advice 并非全零”才是 E_i 的补事件，概率 1−βq^(−r)。取 m=ceil(q^r/β)，无暴露坐标的块概率≤(1−βq^(−r))^m≤e^(−1)，故有暴露坐标的概率有绝对正常数下界。取首个暴露坐标并对其它问题固定作平均，保留标准 variable-versus-equation 策略解码和块失败率 η≥cε 的结论，其中 c>0 为绝对常数；该 η 不与最终源完备误差混用。

令 Ψ=G_{β,r}^{⊗m}、t=floor(k/m)。因 mt≤k，丢掉尾部 k−mt 次测试只会增加最大成功率，故 val(G_{β,r}^{⊗k})≤val(G_{β,r}^{⊗mt})=val(Ψ^{⊗t})≤2^(−Ω(ε²t))。q^r/β≥1 给 m≤2q^r/β；当 k≥2m，t≥k/(2m)≥βk/(4q^r)，得到原结论显示的 2^(−Ω(ε²q^(−r)βk))。不能把块长 m 误当重复块数，也不能把这一步写成原错误的等式。

原参数式(7)/§7.1 给 k=q^(2(1+c)ℓ)、β=q^(−2(1+2c/3)ℓ)，故 βk/q^r=q^(2cℓ/3−r)。r 和正 c 先固定，充分大 ℓ 支付 k≥2m；源完备误差随后取 η_source≤τ/k。该修复不增加对 η_source 的反向依赖，也不泛称对任意参数 k 的无门槛结论。

新增段落修复的是 MZ 不完美完整性的重复证明；上述两个图着色支持链用 FMW Theorem1.6/Corollary1.9 与 GS20，不调用 MZ Claim3.2、MZ Theorem1.3、MZ Theorem7.2 或其近最优 alphabet/soundness 公式。因此更新共同 body 的全文件 SHA 会刷新三对象 pins，但没有改变三对象的数学合同、没有引入新的前提、也没有把两条 whole 关系降为 contribution。

## 比较边界与全部对象对处置

本 task 没有 `overlap_comparisons` 中的 follow-up 对。两个实际比较对均闭合：核心与 perfect exact4 源由第一条 whole 关系支付；核心与八色小独立集源由第二条 whole 关系支付。没有尚须发布的3B/3C数学义务，`follow_up_tasks` 为空。对两对均在 receipt `closed_overlaps` 给出结论与数学理由，避免把一般阅读线索写成待办。

反向逐实例桥“non-k-colorable 推出小独立集密度”不成立：固定 k，取 K_(k+1) 与 N 个孤立点的不交并，χ=k+1 而 α/|V|=(N+1)/(N+k+1)→1。这仅否定该直接桥，不否定任何已登记硬度定理，也不声称不存在专门反向归约。GS20 已明确其三色结果没有得到更强的三色独立集硬度。本包不造 refutes/equivalent_to 边、不推出3色小独立集 gap、随输入增长的 k、常数最大度、调度、SPE 或其它无桥模型的结论。

## 旧四资产的精确替代及共享关系协调

旧 receipt 的四个 assets 全部明确 replaced；两条旧边实际分别位于19cf和542f目录，不能误列到8091目录。原路径与 SHA 保留为历史出处，不覆盖其字节。新资产路径均在本 task write_paths 新目录内。

| 旧资产 | 旧 SHA-256 | 本包 replacement |
| --- | --- | --- |
| `map/edges/unrelated-machines-3a-3a-19cf10a88593d40b/perfect-four-to-one-to-three-color-constant-palette.json` | `97eac092b022b11c8a303a5c3e5beb6c64342433c1e826290260aaed94e2f73b` | `map/edges/boss5-localfix-repair-adb7b167780b9c90/exact4-to-three-color-fixed-palette-v3.json` |
| `map/edges/unrelated-machines-3a-3a-542f8a304e2a6ccf/eight-color-independent-set-to-three-color-gap.json` | `c8bc2d5efd3b33c41c7fa15730785b5fa562592c1f7cbfd8987ba37618287917` | `map/edges/boss5-localfix-repair-adb7b167780b9c90/eight-color-independent-set-to-three-color-v3.json` |
| `map/edges/unrelated-machines-3a-3a-8091c8950447d8fa/review.md` | `e7fe237e5dd9c815953daa9efacb9e67c7fd8445050d05793c6a308b2ee64997` | `map/edges/boss5-localfix-repair-adb7b167780b9c90/review.md` |
| `map/edges/unrelated-machines-3a-3a-8091c8950447d8fa/reading-ledger.json` | `59a925bdade8ade66af21f7ae3571b54a18f734ff26c8f4a6bdf4977ebffc8f1` | `map/edges/boss5-localfix-repair-adb7b167780b9c90/reading-ledger.json` |

队列定向核验同时发现 `boss5-localfix-repair-abad7a282f127942` 为 available（核心 exact4、supersedes19cf），以及 `boss5-localfix-repair-8c728e95a224313d` 为 claimed/Boss5（核心八色、supersedes542f）。它们共享同两条已成熟关系，并非新的独立数学证明。本 worker 已将精确任务及两条本包新 ID/path 通知 Root；由 Root 串行协调先发布者的当前 canonical 供另包精确 SHA 复用。本包不修改这些任务，不重复原 edge_id，也不把共享只读端点当互斥核心。若 Root 发布前发现对方已先发布同一当前关系，应完整实读对方 canonical 后改为精确复用，不能并列复制同一证明身份。

本轮只作读取、SHA/差分核验和当前记录的数学比较，未作科学 replay、旧程序/LP/SPE/IC/BI/有限证书重跑，也未在 clone 执行任何 Git/queue/work.py 写入或 native edge-bind/check。结构核验只验证交付闭合；当前 v3 的最终 binding、edge-check、checkpoint、push、done 与 assemble 由 Root 串行进行。edge 最终绑定后须相应刷新 receipt 的 edge asset SHA。

## 历史原 review 全文留存（非本轮新读 PDF 声明）

以下仅为旧 review 的历史原记录，字节身份由上表及 ledger 的旧 review 引用固定。其“本包/本轮/当前”均指旧任务8091的 v2 时点，不转写为本轮的新阅读或当前 pins。

```text
# 三可着色图对任意固定色数的硬度：定向审读与 canonical 复用

## 本包结论及实际输入

任务 `unrelated-machines-3a-3a-8091c8950447d8fa` 的唯一核心为 `M-d007675a9ed240898c90e831af80b092` v2。实际读取任务时 owner 为 Boss6、state 为 claimed；Root 已确认本包两个共享端点的 read-add pushed（request `e518be09f3c843b1aec58093511d7960`）。本包重新核了三对象当前完整登记与 input pins，核心 pin 为 `3ce12eb8694b9825d6c06c796d23e6aacacf0c6a05a850ed9c0c2f1f0447e6ab`。

核心整句是：每个预先固定整数 k≥3，有限无向图上，YES 为有合法完整三着色，NO 为不存在合法 k 着色，区分该 promise 是 NP-hard。等价写作 PCSP(K3,Kk) 的决策 promise：G→K3 对 G↛Kk；这只是本对象模型的精确表达，不新增定义节点或 minion 归约边。YES 不是仅能给 1−τ 比例顶点着色。NP-hard 是归约结论；若另说不存在多项式算法，才需附上 P≠NP。

当前 canonical 已有两条 incident-core、accepted、unconditional 的完整目标关系，本包逐条核对后保原 SHA 复用，不另造同义边：

1. `perfect-four-to-one-to-three-color-constant-palette`，exact4-to-1 完美完整性硬度到核心。
2. `eight-color-independent-set-to-three-color-gap`，八可着色图的小独立集承诺硬度到核心。

两条边各自完整，不是必须把两条 source 合在一起才成立；不同既有充分证明保留各自 ALL 关系。

## exact4-to-1 源前提与条件硬度的支付

`M-ab4a576ed0be482b89d4a646ffc102b9` v2 的实际模型为有限二部约束多重图；FMW Definition1.1 的脚注明确允许平行边，exact4 关系按每边将左标签分为四元块、右标签分为对应单元块，故 |ΣL|=4|ΣR|。Theorem1.6 为 ∀固定 ε>0，∃常数字母表界 r，Gap-4-to-1_r(1,ε) NP-hard。实际非退化调用均取 0<ε<1。这里的 r 是字母表界，不是 Condition3.12 的内部同名字母。

FMW Theorem3.3 先得 sub-4-to-1 源。附录B从 soundness ε/2 起，取 h=ceil(4/ε)，左右字母表均乘 Z/hZ，每条旧边放 h 个带独立约束的平行边。旧可行标签均取同一新坐标，保严格 val=1；任意不满足旧约束的标签对至多通过其中两个新约束，所以新 val≤旧 val+2/h≤ε。新标签界 hr、约束数 h|E|；所有参数先固定，未删重边也未得到常数最大度。这一附录完整实读，确认不是把“at most4”默当“exact4”。

GS20 Theorem1 在2020年原文中明确条件于某固定 d 的 exact d-to-1 conjecture。其 Conjecture3 的完美 YES、任意小固定 soundness、标签比与多重图合同，在 d=4 由 FMW Theorem1.6 支付。因此这里引用 GS20 是已证明的条件归约加上已证明的源硬度，不是遗留未证猜想的条件结论。FMW Corollary1.7 本身亦逐句给出核心完整 promise。没有把近完美的2-to-1结果或近最优字母表交易替换为完美完整性。

FMW 的外层、中层及 Grassmann 内层成熟技术证明，本包沿当前正文及既有 comparison-proof 的完整入口复用；本包没有声称重新逐句复证119页论文。实际新读范围在 reading-ledger 中分列。

## 八色独立集到三色 promise 的归约及量词

`M-922feb7b429f49d4b5f13ca51b34aae7` v2 的可用源为：每个固定足够小 δ>0，YES 8-colorable，NO α(G)/|V(G)|<δ 的 NP-hard gap。FMW Corollary1.9 原文与此对应；实际调用统一取 δ<1/C 且 C≥8，从而两个 promise 不相交，不依赖大 δ 的退化表述。

GS20 §2.1 从 exact d-to-1 变为 d-to-d induced-list 源，Theorem9 取 q=2d；§3.2 的对称 Markov 链仅连接不交的 d 元组，§3.3 的长码构图使全满足源标签 σ 对应颜色 x_{σ(w)}，每条输出边两端颜色不同，故 d=4 得完整8着色。大独立集在正比例 long-code blocks 上给两个均正密度的指示函数；独立性令相关内积为0，Theorem7 和 Lemma6 解码出有界列表，在正比例诱导源顶点集内满足所有约束，与 d-to-d 源 promise 矛盾。这里 q、列表界与字母表均先固定，所以长码大小是归约规模的常数因子。

核过原文显示的列表常数：在坐标阈值 δ0/d 和 degree-ds 总影响≤ds 下，可安全取列表大小上界 ceil(d²s/δ0)，足以替代 §3.3 排版处较小的 ds/δ0；d 是固定数，因此这不改变 Theorem9。若独立集密度至少 η，取 block 密度至少 η/2 的集合，顶点比例至少 η/(2−η)≥η/2；Theorem7 按 η/4 调用可满足其严格密度门槛。两条 canonical 均没有依赖错误的精确列表常数，旧八色任务收据也已记录这一安全界，所以不修改其边字节。

核心目标 k 先固定。GS20 Lemma8 给固定 q 的任意常数 palette 硬度向 q=3 的 promise 归约：b(n)=binom(n,floor(n/2)) 的 arc-graph 关系，加上4→3的有限末段。对目标 k，先固定该有限归约链需要的源 palette C=C(k)，可增大至至少8；再取固定 0<δ<1/C。若源 NO 图有 C 着色，某颜色类是至少 |V|/C>δ|V| 的独立集，矛盾。因此八色小独立集 gap 支付 Lemma8 所需的8色对非C色源，归约输出3色对非k色目标。顺序为 k→C→δ→PCP soundness/字母表→输入规模；不是把 k 作为免费输入参数，亦未采用 FMW Remark1.8 的稍超多项式归约。

这支付核心整句，两个复用边的 whole_result 范围准确。输出图并非原八色图本身，归约保留的是着色 promise，不承诺新的三色小独立集密度结论。

## 比较边界、异议及后续处置

反向若仅从“NO 图非k色”推“小独立集”不成立。固定 k，取 K_{k+1} 与 N 个孤立点的不交并：χ=k+1，但最大独立集比例 (N+1)/(N+k+1) 趋近1。这只否定上述逐实例反向桥，不是任何已登记硬度定理的反例；本包不造错误的 refutes/equivalent_to 边，也不声称不存在别的专门反向归约。GS20 p62:2 明确说其三色结果没有得到更强的三色独立集硬度。

精确 core 和两端点已有完整 canonical 比较，本包无未闭推导缺口、无需要新的定向3B/3C任务的已确认问题。任务没有 follow-up overlap，所以 closed_overlaps 与 follow_up_tasks 均为空。没有从这些图着色结果推出 unrelated-machines 实际调度、六人 SPE、普通 CSP 或任意给定 minion 同态的结论。

仅执行了读取、SHA核对和既有PDF的 pdftotext 抽取；没有重跑历史数学程序、LP、SPE、IC、BI、有限实验或证书。没有在本worker执行 native edge-bind/edge-check、推送、队列 done 或 assemble；发布和最终校验由 Root 串行办理。
```
