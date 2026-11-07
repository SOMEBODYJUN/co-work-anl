# 0113：93条证据路由的数学比较与Boss3接证候选

本交付只处理旧0113 receipt中的93条pending_owner_routes。它们分布在13份混合审查、目录或计算页，指向73份主正文；不是93个新增数学对象。93条均已有实读语义比较、完整证明入口、准确主owner及接证边界。15条指向Boss3已正式own的0115对象，本次实际读接后形成18个既有对象的version 2证据候选，共19条新evidence ref；其余78条保持对外owner的实际读接请求。**完成比较不等于外owner已经接受，也不等于全页或新正式DONE。**

18对象的全部数学字段、truth_status、主body、旧evidence与sources逐字段保持，只把version 1升到2并加入准确证据。17项仍proved，WC-FULL-CORE-TRANSIENT-MASS-NECESSITY-v1仍conditional；无新ID、无新数学节点、无超边。旧DONE0113/0115 batch与receipt均未修改。

## 文件入口

| 文件 | 内容 |
|---|---|
| [route-comparison.json](route-comparison.json) | 93条完整旧route逐一保留，新增实读数学比较、角色/独立性、目标73正文及真实读段。 |
| [owner-evidence-fragments.json](owner-evidence-fragments.json) | 18对象的完整base record、逐对象准确接证范围、19条新增ref及完整候选record。 |
| [schema2-supplement-candidate.json](schema2-supplement-candidate.json) | 18对象version 2、27个完整材料替换row、edge_files为空；等待父/lead审查整合。 |
| [owner-routing-requests.json](owner-routing-requests.json) | 78条外owner请求；无外部accepted声明。 |
| [material-resolution-review.json](material-resolution-review.json) | 13混页needs-decision及14主body objects的全旧owner并集与未接边界。 |
| [reading-scope.json](reading-scope.json) | 13源页全文、73目标逐段实际阅读范围、旧源/未读链接资产及context计划边界。 |
| [verification.json](verification.json) | 独立SHA/真ATX、官方schema、字段差异及材料owner并集校验；不代数学证明。 |
| [deliverable-manifest.json](deliverable-manifest.json) | 最终文件SHA与18对象版本清单。 |

## 真实canonical与整合顺序

准备初期的2475对象旧snapshot仅为当时观察。冻结前重新读取实际canonical：`a0a4bee7e987be86a762e105f065fa405621cb0354730b256faec9634ad81fe4`，2613对象、3008材料；其中已包含原DONE0113/0115。18个当前canonical version 1逐字段等于不可变原115 base record。官方`validate_batch(ROOT,candidate)`直接使用这个真实canonical通过，未提供任何`peer_objects`，`reused_published_group_owners=[]`。这不是把claimed任务的草稿模拟为published atomic peer。此SHA是冻结时观察，registry后来变化时须作为历史观察理解。

父/lead应先复核本18对象的准确接证fragment，再作为增量审查version 2。27个材料row是替换候选：13个混页明确保needs-decision，14个主body保持objects；合并时必须显式保所有旧owner。外78条只有其精确主owner实际读对应完整范围并写record.evidence后才可接受。若接收时该owner已DONE，交lead新的owner-acceptance followup，不能覆盖旧DONE。已有0116 ledger对113的26/26与对115的21/21接证仍保留，未重新列未接。

## Boss3实际接证的18个既有对象

| 对象ID | 版本 | 新增ref | 实际接受范围 |
|---|---:|---:|---|
| `WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1` | 1 → 2 | 1 | 只接FR20：从给定完整二动作双扫环、真实B/η/权谱δ及所列充分D预算到新游戏全状态出口。其他FR的条件编译/时钟障碍未接此身份。 |
| `WC-ANTICHAIN-CORE-NORMAL-FORM-v1` | 1 → 2 | 1 | 只接FR22：不依倍率核心化与固定单向均衡lift，保反链/空交/次数和允许删玩家。 |
| `WC-R2-RESOURCE-POWER-BRIDGE` | 1 → 2 | 1 | 只接FR11：逐资源幂矩/降序边际方法仍共用w_i^p玩家尺度，K、Q看全部潜在用户；不把动态换势或全局幂混合障碍并入。 |
| `WC-R1-MULTIPLIER-BARRIER` | 1 → 2 | 2 | 接FR13和旧候选2：先选有限w再量化全部F,h的多尺度夹逼障碍。旧双源审查1/3/4节既有115接证保留，不重复冒称新接受。 |
| `WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1` | 1 → 2 | 1 | 只接FR18：近次数真实环排任意全边下降势，同时全空PNE存在；不得由此接无PNE或把2^E直接交二动作编译。 |
| `WC-DEGREE-LOCAL-COST-COMPRESSION-v1` | 1 → 2 | 1 | 只接FR30中固定次数全成本空间维数/正资源数量压缩，不接旁边小用户支持失真。 |
| `WC-FULL-CORE-TRANSIENT-MASS-NECESSITY-v1` | 1 → 2 | 1 | FR34仅proper严格坏环输入→完整proper锥植入及所有对偶正暂态质量；保conditional及输入坏环/proper合同。 |
| `WC-TRANSIENT-PARITY-SELECTOR-DUAL-v1` | 1 → 2 | 1 | FR34仅原始低阶奇偶抵消可行的完全暂态对偶；原始二循环另有对偶，故本身份不声称必要暂态。 |
| `weighted-congestion/optimal-nonuniform-right-quadrature` | 1 → 2 | 1 | FR45中单项式给定格数最优非均匀严格划分唯一性、递推与固定格数不能统一给cd增益；未接实际clone实现。 |
| `weighted-congestion/right-endpoint-area-quadrature` | 1 → 2 | 1 | FR45中任意网格右端面积误差/效率/凸细化，作为局部数值接口；同段最优非均匀采样由独立身份接。 |
| `WC-ENDPOINT-AREA-WINDOW-CERTIFICATE-v1` | 1 → 2 | 1 | FR45中同权窗口的H>0、κΓ<1及严格有限网格阈值/余量；不接完整游戏无均衡、重端点/return未付部分。 |
| `M-e7929cadcd154450adc13350a49c66f9` | 1 → 2 | 1 | FR48中六玩家RD为真、完整社会最优全在前沿外和指定个体费降/W升反例；不能吞正向SD定理或三人正向例。 |
| `WC-SOCIALLY-DESCENDING-REPAIR-v1` | 1 → 2 | 1 | FR48中全社会费用分解和SD支付真实社会外部性后修复下降/完整OPT压缩正结论；RD反例由独立M-ID接。 |
| `WC-REGULARIZED-CORE-REPAIR-QUALITY-v1` | 1 → 2 | 1 | FR48中前沿共同尺度、完整W包络、有限η全局最小及目标RD+SD联合转移，未接仅局部最小质量或更早完整域正则化。 |
| `WC-R1-ORDINAL-COPY-BRIDGE` | 1 → 2 | 1 | 旧候选3中跨全部游戏的统一规则与完整复制合同；不能改为同一个G任意选F或仅某个全局最小。 |
| `M-4ae04fa3f5dc4436a5869f82003945b7` | 1 → 2 | 1 | 独立攻击源完整读序节中verify.py那个8人16资源、256态2048真偏离的固定例与准确一般证明/有限实现分工；不接1949例、其它三程序全部输出。 |
| `M-dec88dc2302a46e384b5111e8e5ed2a2` | 1 → 2 | 1 | 唯一ATX“这两份新源的独有数学去向”中旧s≥6二进制族的floor、常数、任意m≥s和单调补全一行；不是同页d≥4096均匀族或113 linear-reset。 |
| `weighted-congestion/odd-ring-uniform-fixed-hub-amplification-family` | 1 → 2 | 1 | 唯一ATX“这两份新源的独有数学去向”中d≥4096、奇3≤m≤d显式族一行，保G≥16/e的全参数证明和巨大人数限制；不把dyadic或linear-reset当同族。 |

每条新ref都指真实path/full SHA/唯一真实ATX外层section。FR编号或scope_locator是段内范围说明，未冒充ATX锚点。没有把fenced内部Claim标题当section；已有完整主body/完整承重入口始终保留。

## 外owner78条仍待实际接受

| 精确目标task | 主owner快照 | 路由数 | 当前观察 |
|---|---|---:|---|
| `register-ab98f323ad-0094` | Boss2 | 3 | claimed；0094 PK四个相符draft已读，非正式record |
| `register-ab98f323ad-0112` | Boss1 | 18 | claimed；未观察到正式batch/receipt |
| `register-ab98f323ad-0114` | Boss2 | 16 | claimed；未观察到正式batch/receipt |
| `register-ab98f323ad-0116` | Boss2 | 9 | claimed；未观察到正式batch/receipt |
| `register-ab98f323ad-0117` | Boss2 | 20 | claimed；未观察到正式batch/receipt |
| `register-ab98f323ad-0118` | Boss2 | 12 | claimed；存在0118 batch候选但无receipt，非正式DONE |

0094 matching PK四记录、0118 matching十记录只作为确有草稿比较，未代其owner接受新source。未有正式record的多命题页列明逐Claim/模型/量词拆分请求：路径峰值、稳定成本全行LP与社会切线；高度反演、线性过渡与真实闭词深度；Faulhaber两点纠错与字面目标两态反例。容器/文献/审查页ID不因此成为新数学Claim ID。需要新ID时由父/lead一次分配；本worker分配0个。

批内修订已按Boss1公屏seq139确认：route86/target68采用0112正主维护的精确ID `M-1dcdccb089bb405c952eb842055c98d3`，原 `weighted-congestion/three-hub-degree-ten-exact-finite-threshold` 仅保alias。这是身份确认，仍pending目标owner实际接此source；未将该ID写作canonical、peer或材料已接owner。两个增长族的新增evidence均准确指向唯一ATX“这两份新源的独有数学去向”，分别接其d≥4096均匀族行和s≥6二进制族行；原route内容完整保留。

## 必须保留的模型与版本边界

1. **分叉、unique-light、跨源multi-light是三个模型。** 分叉割：每side恰一light和一target hub，hub可异权，d≥2、α≥T_d及弱UF；割最小配反位得α-PNE。unique-light截断side：hub共同权u、side可含任意hub子集；AS+B直接预算和UF阈值推论是两个合同。跨源共享side则明确允许同side多个light和多个source、hub共同权u，四版域依次为τ=α≥1+√d、(τ−1)(α−1)≥d、α(τ−1)≥d、ατ≥d（各自τ/α下界完整保正文）。不能把第三个误标成unique-light。

2. **GlobalR只逼近固定R损失。** 对每R>1和1≤α<R，等人数heavy/light hub全分离构造的两个全局最小点都坏；真实改善比nR/(R+n)从下趋R，GlobalR恒等式覆盖全部状态。R=1排除，不能改成固定R任意大损失。游戏仍有精确PNE。

3. **三种两列对象不合并。** 现成H/L多项式归约保持人数n、α>1；副费用端点子引理保持P且0<w≤1；完整拓扑v3从无α-PNE出发、要求α≥(1+√3)/2，可改变人数。0113旧route的WC-R3-FULL-TOPOLOGY-REDUCTION缺版本；当前0118确有候选为WC-R3-FULL-TOPOLOGY-REDUCTION-v3，需保这个版本，不能覆盖v1/v2。

4. **真实环、全状态非存在与选态障碍分开。** 循环窗口2^E游戏仍有全空PNE；原始奇偶暂态可行不等于暂态必要；完整proper锥必要质量保严格坏环/proper输入。16态FIP但无共同尺度旧Claim与9态有PNE仍留环的固定游戏继续独立。

5. **三个odd-ring对象与两个有限游戏分开。** 113 OC-AMPLIFIER、LIMIT、ENVELOPE独立；112二阶对象是d/(ln d+1)−1/2+o(1)，不能改成d/ln d−1/2。T_d=U_d还需后来的撤UF实际上界，旧充分接口障碍不给这一结论。1949人手选系数例的1434444625245301/707371943476824只属手选例，同几何中点系数不同；8人256态的M-4ae04fa3f5dc4436a5869f82003945b7是另一个具体游戏。均匀d≥4096族与二进制s≥6族亦各保完整参数证明，不以有限Decimal/三样本替代。

6. **社会目标与门条件分开。** 完整W、可动W_M、不加权U不同。SD支付真实社会外部性，RD和前沿恒移单独不保证OPT压缩；六人RD反例、SD正结论与FRONT-SOCIAL-COST-SHIFT保持各身份。正则化核心须目标βη的RD+SD及完整W基线，不能用局部最小代全局质量。

7. **保留正确的两玩家对象，隔离具体坏表。** 0114单环四态是权(1,2)、费用x²,(9/2)x,4,71/4，全部八偏离及72/71弱端点自足正确；它不同于父已确认0118《两玩家二策略无纯均衡》具体费用/数值错误。未接受后一个坏四态例为proved，也未因此否掉其他正确两玩家Claim。

8. **近次数结果的主模型不按同名拼接。** TARGET合同由0117；healthy sweep/front原模型由0118；统一可变n尾部给d−1200ceil(log2 d)^2负向下界，普遍阈值比趋1的正向上界来自独立三角势，不由负向构造单独证明。

## 材料层仍有未接范围

| 原0113混页 | 原route数 | 仍待外owner条数 | 新候选disposition |
|---|---:|---:|---|
| 拓扑放大与时钟编译的失败边界--审查.md | 25 | 23 | needs-decision |
| 势与成本表示失效的准确量词--审查.md | 30 | 21 | needs-decision |
| 有限稳定决策的实现审计与版本范围--审查.md | 6 | 6 | needs-decision |
| Pro派生简报的逐项数学范围与版本审查--审查.md | 1 | 1 | needs-decision |
| 加权拥塞旧候选目录与后续数学状态--审查.md | 10 | 8 | needs-decision |
| 十四资源构造与缩权族的精确复现--计算.md | 1 | 1 | needs-decision |
| 两攻击源包络的审查与诊断范围--审查.md | 2 | 2 | needs-decision |
| 两列与互补符号列主稿的完整归属及零费见证--审查.md | 1 | 1 | needs-decision |
| 保守两攻击端点归约的精确复现与范围--计算.md | 5 | 5 | needs-decision |
| 局部权带份额与选择器的作者精确核验--计算.md | 1 | 1 | needs-decision |
| 局部Shapley包络与尾部冻结的审查范围--审查.md | 1 | 1 | needs-decision |
| 奇环放大器的独立攻击与来源范围--审查.md | 9 | 7 | needs-decision |
| 边际乘子障碍与多项式端点归约双源审查--审查.md | 1 | 1 | needs-decision |

14个主body row均保objects，包括八人反例主body所在《奇环四程序》。该页完整保原均匀/二进制/八人及113 AMPLIFIER三个身份；父115最新review的1949人/接口/二阶未接边界原文并入，objects不宣告整页接受。社会分解页亦保FRONT-SOCIAL-COST-SHIFT旧owner。

## 阅读与静态验证的真实边界

实际完整读13源页；73目标中30份全文、43份按明确连续段比较，其中14份Boss3主正文均全文。其余成熟主证明保完整入口，只有具体疑点才深入，不为登记重证全部旧结果。逐文件读段见reading-scope。未声称新读/渲染论文PDF/TeX、未声称全部原始代码/证书/报告已逐一打开，未运行任何旧数学程序。

独立检查1603次字典ref出现，去重174个path/SHA/section引用，涉及125文件；全部SHA相符，56个不同section均为fence外唯一真实ATX。官方schema验证直接用当前canonical通过。逐字段校验确保18对象数学状态/正文/旧证据不删，93原route准确保全，13混页/14主body所有旧owner并集保留。静态通过不认证外owner实际接受、外审、新颖性或全范围数学完成。

context沿原task官方默认500K的300K源/元数据阅读、200K保留规划，按实际新增读段记录历史；平台未给出token余量实测，未把字节或字符当token。所有中间比较/构建/独立检查脚本仅置于.git/boss3-runtime/0113-evidence-closure；本worker不操作Git/queue/board/new-id。
