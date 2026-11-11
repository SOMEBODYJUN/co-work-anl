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
