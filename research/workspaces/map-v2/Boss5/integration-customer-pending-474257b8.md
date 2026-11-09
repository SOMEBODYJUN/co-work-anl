# Customer pending integration review · 474257b8

审查仅供 Boss5 串行整合。本 worker 只写本 Markdown 和同名 JSON；没有改动源正文、边、收据、registry、coverage、integration、队列或 Git，没有查询网络，也没有重跑任何旧求解器、审计或证书计算。下面的文件 SHA 是本地实读字节的 SHA-256；不将它们称为远端已刷新或新计算事件。

## 已读范围与结论

完整实读 AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md；两项当前任务及收据；旧 c335f597b7a5c0f6 任务、收据及唯一旧资产；两条新增边全文；两项任务声明的全部正文及必要 primary：单公共尾定理与资源全文，十八主题单标签障碍、联合停界、共同目录定义、有理恢复程序、实际遗漏席位谱、控制器程序、冻结 private JSON、audit_private.json、标准库 verify.py 全文。另实读 canonical 单 D 重复惩罚边及其障碍正文、private→ordinary 边、private→旧单标签接口边及旧接口正文；对照相关完整登记陈述。

两项 pending 均有一条 accepted / unconditional / implies 边，且 **whole_result 与当前目标完整陈述相符**。没有零边项，也没有需把这两条新边降成 partial 的未付步骤。这里的 unconditional 指关系在其明确模型与适用条件内已经证明；不是把“实现指定计数”或“冻结旧点和指定路径”从定理条件中删除。

## 1. 单公共尾：全顺序目标计数定理

任务 customer-common-tail-count-round13-3a-12c46343813f3480，核心 customer-attraction/single-common-tail-target-count-half-for-all-orders v2，只读 M-723b5ee6fbd8437eadfa97b816d04478 v1。新边 single-common-tail-terminal-and-true-deviation-pay-all-order-welfare 的 SHA 为 bd4fbfcf97997c25f2b4963a585bf64935e80ccbea163fca7586864833c9cea6。

模型为 m=k+r 个依次行动的单位玩家、完整有序历史纯 SPE、互不相交的 X_i,H_i,B,R 块，组间相同质量 x,a，以及唯一 D=B∪R。目录恰为 C_i=X_i、A_i=X_i∪H_i、B_i=X_i∪B 和 D。量词是每个非负整数 k,r、非负实块质量，以及每份实际恰各用一次 C_i、恰 r 次 D 的完整纯 SPE 的任意实际次序。它不要求所有模型实例均有这种 SPE。

全目标核对如下：

1. k=0 时只有 D，零人边界按空策略覆盖零理解；r=0、k≥1 时真正末 C_i 改 A_i、B_i、D 得 x+a、x+b、b+d，迫 a=b=0、d≤x，故 W=OPT_k=kx。零人只是当前 theorem 单独保留的软件/代数边界，不把 m≥1 的共同模型定义擅改为新的全称断言。
2. k,r≥1 且 a>0 时，末位不可能是 C_i，因此实际末 D。原末节点 lemma 的 b+d≥r(x/2+a)、d≥rx/2 可用于这个任意次序，因为该末位之前的动作多重集相同。这一步只给必要门槛。
3. 反设 a>x/2，取最后一个实际 C_i，强制改 D，必须跟踪同一完整策略的真实后继。令后继非 D 数量为 q。q=0 时源与末 D 同得 (b+d)/(r+1)≤x，但末可查未服务 A_i 得 x+a。q≥2 时源至少得 b/(r+1)+d/(r−1)，连同 d≥rx/2 推出 b+d≤rx，与实际末门槛的 b+d>rx 矛盾。q=1 且唯一非 D 不盖 B 同样给 b+d≤rx。
4. 剩下 q=1 且唯一非 D 为 B_j。源 D 得 b/(r+1)+d/r≤x。若末 D，改 A_i 得至少 x/2+a>x；若末 B_j，未服务 A_i 给 x+a，而 B_j 至多 x+b/(r+1)，所以 a≤b/(r+1)≤x−d/r≤x/2。两种真实末动作都矛盾，得到所有正 r 的统一 a≤x/2。
5. W=kx+b+d，OPT_m=k(x+a)+b+d（k 个 A 加 D 已用至多 m 槽盖全）。x=0 强制 a=0。否则 ka/[kx+r(x/2+a)] 随 a 增，代 a≤x/2 得 OPT_m/W≤1+k/[2(k+r)]≤3/2。a=0 直接最优，W=0 只用乘法福利不等式。故完整目标还包括 W≥OPT_m/2 以及 r=0 或 k=0 最优。

与现役相邻结果的关系：canonical cag-11da6a-single-public-topic-repeated-punishment（SHA f6b78494dc4543a10a75ccccb8d17415ab8e2cc46513810c81dca55289b3ad5e）主贡献仍是“单 D、r≥2、x>0 时，偏离后末 r 位全用同 B_i 的指定惩罚不可信”，其目标是更一般 D_j 障碍的局部特化，仍为 contribution。该旧边解释另外给出目标计数 half 与较弱的 a≤(1/2+1/r)x（r≥2）/a≤x（r=1）。新定理补上全部真实非 D 后继分类，严格加强该附带福利论证至 a≤x/2 和显式 3/2 以下参数界。新结果并不删除旧边的不同目标，也不反驳正文给出的 k=3,r=2、W=10、OPT=13 的混合惩罚 SPE；13/10 恰等于本模型相应参数上界 1+3/10。

仍开放且不在本次完成范围：给定参数的目标计数可实现性；其他实际计数；多个能覆盖 R 的不同 D 型；客户块交叠或异组质量的推广。原 probe 的 target_spe 是全根 outcomes 的 count membership；它不输出显示顺序证书，固定末节点门槛也不成为完整前缀充分条件。

## 2. 单标签 source repair：完整排除保持，席位背景修正

任务 round13-seat-repair-repair-87914631cf2a9079，核心 customer-attraction/eighteen-topic-private-point-one-new-label-obstruction v3，只读 M-4b6ebc6e36f341ff8c9f7bec506ae78d v4；明确 supersedes customer-attraction-3a-3a-c335f597b7a5c0f6。新边 cag-private-point-fixed-path-one-new-label-obstruction 的 SHA 为 a1e6094b610e3c63a920a6c0eb8dc8ad9d1f241cf76ee5b0c9f7fb12a42a1790。

固定六位玩家、十八旧标签、原 actual 有序路径 (0,1,2,3,4,5)、17 个 d=1 正对称类型加一个 d=2 类型，共 17×6+15=117 个物化正质量旧类型。只可从每个旧型质量 m_i 中任取实质量 z_i∈[0,m_i] 加入唯一新标签 Z；旧会员、总质量与旧路径不变。全策略与任意历史依赖弱平局可重选。

完整证明的承重链已逐式核对，不依赖把旧有限审计重跑一次：

- 新标签未在纯旧终局被选择，故这些终局利润与全部旧末位排序不变。原倒二改旧标签 5 或 12…17 对所有旧最佳末回复仍严格获利。要支持原路径，这七枝必须选择 Z 作末回复，因此产生 B_a。新旧平局也不能允许选旧回复，因为旧回复仍使倒二严格获利。
- S_j 是实际玩家改 Z 后的保守收益下界，分母 P_ij+6−j 确为当前加全部后继最多覆盖数。必要条件是此下界≤原 u_j，不能倒称实际偏离收益上界。
- 倒二改 Z 后的真实末回复 b 只能是十九个标签之一。U_b 是源不获利，R_b,a 是该末回复对旧动作 a 的真实最优性。旧回复 L_b 的截距及斜率由把 z_i 的负载从 p_i+1 增到 p_i+2 的差分精确得到；b=Z 时收益为 Σz_i/(p_i+2)，重复选 Z 的分母亦正确。
- 所列每组乘子均非负，c_s·z≤d_s 的组合给 C·z≤D，而独立盒下界为 Σm_i min(0,C_i)。表中的十九个正 gap 分组覆盖 b=0,1,2,3；4；5；6…11；12…17；Z，没有漏回复。verify.py 从同一冻结输入重建这些必要行并用 Fraction 验相同 gap；本 worker 静态核读公式、分组、输入与完整算法，未声称新执行或独立重算117型十九证书。

因此新边完整推出：整个实质量盒、每份完整纯策略和所有弱平局均不可能实现固定原路径。实域排除包含有理清分母和相应整数拆分。旧零新增标签的路径已被原七枝排除，故“至多一个”说法也成立。六个旧 comparison 标签已经覆盖所有冻结质量，OPT_6 为 1477223727431/726719158212，路径 W=1；加入 Z 不增客户质量，所以仍同一静态 OPT，但不能由此制造真实 SPE 的超二反例。

source repair 的精确变化：联合停界正文从旧 bab886eda3104f82eeaab86239c3c175526c6909b2a037831b8a17c28daac465 改为当前 3f09aade80c8e87f86f8ff8513888f7bbe99b53b848b06f0d28c1a0ff856bd43，纠正“108个带重数席位”与“按前六大席位导出的六条个体下界及一总预算”的区别。原恢复 LP 仅添加七条对称 private 预算，不是检查108行。原点、十九证书、单标签定理正文、verify.py、audit_private.json 未改。修复后的 edge 扩写明确该区分，并重绑新 source/target pin 与当前正文；没有扩大单标签数学结论。

旧任务唯一资产 9c1b7174f088f08152de4b310515a76d6b3e136095f8a267a94b82668fe423ef 应按收据 replaced 为上述 a1e609… 新路径，沿用相同 edge_id。**此 supersession 没有 retained 资产，也没有另一条待退休旧边。** 未变数学并非丢弃：它保存在新边相同完整 whole_result、相同冻结输入和证书中。

相邻结果的准确范围：

| 相邻边 | 当前观察/作用 | 本次影响 |
| --- | --- | --- |
| cag-saturation-round10-private-single-label-completion-obstruction | canonical，SHA 10e7bd4c7790d4a70c9ff427c300a6aa1c4471fe77d39598b6fabd18965b69dd；同一十九证书给旧单枝程序接口一个固定实例的 contribution | 与新 whole-result 边共享同一证明，不能算独立新反例；旧接口的一般线性等式、减税目标及原两步浮点报告仍各有独立证据。保此字节，不由本任务重复替代。 |
| cag-saturation-round10-private-projects-to-ordinary-obstruction | canonical，SHA b21cdb481028c4cac1553291c3d3e05e42c1be5fb57f0dab1cb44d6b019b4758；删除private附加条件后的固定点投影 contribution | 不给普通114型指定点的整条身份/数值证书，亦非从 private 点推出一般总势必要性。保原局部范围。 |
| cag-saturation-round10-seat-spectrum-check-on-private-point | 当前 round12 路径在本地存在，但已不在本地 registry canonical edge_files | 它最多贡献固定点上的108席位数值及六个体/一总预算核查；不能承担目标点其他超二、势与菜单结论。本 worker 不接管 root 正在处理的这条源摘要纠错，也不将其误列为本任务 retained 资产。 |

本次证书不使用原990行、100947势多重集、私有谱一般定理或扩目录后的私有性作为排除前提。它们只描述和核对冻结输入。多标签可以互为回复；改变旧质量、旧会员或实际路径均为新问题。一般六人 half、共同支付预算及共享遗漏没有被本结果解决。

## 可直接追加的 review 内容

archive_reviews[archives/customer-attraction] 的本地追加建议见同名 JSON 的 archive_review_append。局部 unresolved 为空，表示上述两条关系的数学比较已结清，不授权清除旧 archive_review 中其他尚未实读的 cross-batch pending 或全档 open 义务。open_mathematical_obligations 明确保留上述推广、可实现性和六人真实共同付款义务。

cross_archive_review 本轮只追加：实读的新增关系均保持顾客吸引档内同一共同目录、均分终局及完整有序历史模型；没有跨档端点映射，未建立跨档迁移。此处不以主题相似、程序称呼或有限矩阵制造 transfer。不要把本轮未发现映射写成已经排除所有未来跨档比较。

## 当前字节与冻结边界

本地观察时，两 pending receipt 尚不在 map/integration.json 的 task_receipt_pins；integration 已有旧 c335 和 round12-source-repair 的收据 pin。registry canonical edge_files 中也未包含这两条 pending 新资产。现存 archive_review 的文字已经提到全顺序与席位勘误，不能把文字提及等同于按当前两个 done 收据完成整合。统一 assemble、来源纠错和最终检查由 root 处理。

所有指定 task reading_refs 与新边 evidence_pins 的 SHA 均与本地实读字节吻合；新 receipt 的 asset SHA 亦与文件吻合。两任务输入 pin 对应当前登记版本的值已在 JSON 列明。未进行远端刷新。共享 registry、coverage、integration 的 SHA 只作观察快照，不应阻止 root 串行更新；若正文或端点之后变更，须按 JSON 记录的精确受影响范围定向复核。

冻结后 root 通知另有新 done 包 customer-attraction-3a-3a-182336763d88b54e。本审查没有读取或覆盖它；它须由后续实读审查接入，不能凭 done 状态或旧 review 文字计为本轮完成。
