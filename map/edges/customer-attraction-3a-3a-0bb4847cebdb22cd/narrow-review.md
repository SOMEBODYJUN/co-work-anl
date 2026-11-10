# 数量标签勘误后的当前窄续审查

本轮沿用 Boss6 身份，仅接续 `customer-attraction-3a-3a-0bb4847cebdb22cd`。当前 request 为 `996524f8d60240de8dc9bd27b57f7558`，definition pin 为 `183eedecd7c1c04fd5329d27fab7f444ffd8e0dd6127b490b8da7cd8617da0de`。六个输入的当前登记 pin、全部登记 body/evidence 的原始字节及唯一标题已独立重核；精确结果在 `binding-snapshot.json` 和 `source-refresh-check.json`。

本目录的 `mathematical-review.md`、`reading-ledger.json` 和 `record-only-correction-proposal.json` 逐字保留 round45 历史原件；其旧 request、旧 v1 pin、当时的新计算范围以及待勘误流程只描述当时状态。`finite-tail-interface-check.py/json` 也逐字保留为该轮成熟证据，代码本轮没有执行。当前绑定、实际新读范围和已解决勘误的处置以本稿、`narrow-reading-ledger.json` 及当前 receipt 为准。没有把旧大范围实读或旧计算改称本轮重做。

## 本轮确切改变

当前 M-99341ce9d6544f5fa702a372e617f03b 为 v2，pin `13b73ac9158fc6cb4735c192e87cb4ce7b24c3df0cfd427af384b7601fdea8f1`。与已审 v1 的字段差别恰为 version 和 statement；statement 仅把 p2 的“尾收益差0”和 p3 的“差0”分别改成“新增覆盖Δ=0”。它与 Root 已发布的精确 proposed record 完全一致，原 body/evidence 引用全同且实际文件 SHA 全部匹配。

实际尾收益仍为 p2 的 (10,11)、p3 的 (12,13)，末首差都为 1。成熟审计的 `tail_Delta=0` 表示原前缀未覆盖客户的实际新增覆盖，不是两人收益差。两份 source 及报告原已给正确数量，故没有改变数学输入、定理、完整策略、完整 IC 或亏损结论。M-be4510d9c7b844f0830fb90f34bfe7af 保持 v2 与既有 pin；其 k! 系数本来已正确，其余四个只读对象的 pin 也全部不变。

## 继承的有限数学与保留的一条贡献边

完整读旧 review、贡献边、两条 coverage 和既有尾接口代码/JSON 后，本轮确认它们的承重关系如下。源一般族给六标签 A,B,T,Q,R,S、十个兴趣类型的完整合法尾 SPE。把 p 取 2、3，十类重数逐型正好给同一 85、126 客户输入，人数分别 6、8。背景 h=A^pB^p 后，a=2p+6、b=a+1，实际尾 AB 给 P=4p+13、Δ_cov=0、fresh OPT₂=4p+14，因此每个实 λ 都有 P+λΔ_cov−fresh OPT₂=−1。原根实际路径分别 AABBAB、AAABBBAB，W/OPT 分别 63/85、100/126；两根仍满足半覆盖，不能据此否定根 half、RM-gap 或 UR-gap。原 52 客户 W34 精确主 Claim 也是另一个完整根对象，不能由这两个有限根推出它的特定编码与全部 IC。

保留且只保留 `cag0bb-legal-tail-family-specializes-finite-p2-p3-tail-payload`：accepted、unconditional、specializes、premises_mode=all，继续使用 contribution 而非 whole_result。它支付源全参数合法尾机制在 p2/p3 的完整局部特化和数值；目标指定完整根的全部有序节点 IC、实际 h 可达性与根数值仍由原 SHA 绑定的独立根证书支付，不从合法尾局定理凭空推出。当前 edge 的数学内容沿用成熟审查，仅移除已解决操作勘误并明确既有 p≥4 边界。

## 已完成的同终局子树替换为何充分

原根在 h 后的六末回复为 (B,S,S,S,S,R)，手写尾局为 (B,R,R,R,S,R)，只在 hB、hT、hQ 三个离轨末节点有同值平局差别。两者从 h 的实际继续均为 AB。旧 Fraction 报告已经在每参数支付 36 项末位和 6 项首位比较，共 84 项，确认手写尾为同一 h 子博弈 SPE；本轮只实读代码/结果并核 SHA，没有重跑。

对任一合法有序历史 h，用另一完整子博弈 SPE 替换原完整 SPE 的整个 h 子树，若 h 后实际继续的完整终局相同，则得到完整根 SPE。证明覆盖全部合法有序节点：h 子树内 IC 由新尾 SPE 支付；与 h 不可比的节点及其全部后继未改；在 h 的任一严格祖先 g，对每个当前候选行动沿相应同一完整策略真实完成，路径若不进 h 就完全未改，若进入 h 就在同一 h 后达到同一完整终局。因此 g 的每个行动完成收益和其指定行动逐项不变，原 IC 保持。这个证明不把历史按负载合并，也没有只检查实际根路径。

保持各祖先行动者的 h 后终局收益已经是足够条件；在固定 h 的 CAG 中，相同最终标签计数或相同逐客户最终负载也足够。本包采用更强的完整有序终局 hAB 相同。仅同福利、同覆盖数或仅剩余两名玩家收益相同不能一般地保证祖先 IC。引理本身只要求 h 合法；本包进一步使用原根实际到达 h 且 h 前动作不变，才保留派生根的实际可达性。

原策略加三位置 S→R 已完整确定派生策略：p2 的零基位 1598/1599/1600，派生编码 SHA `213d84dff5c1262dc7bfdde85ee732c5504defdfb240474d405a1ae27f41b67a`；p3 的 56246/56247/56248，SHA `6fd1f00fe8567a2a9aa3767b5898a70598bf179c17302bf3da437a9451ed757f`。这些位置及 SHA 是旧报告的成熟附件，本轮未重新生成补丁或编码。上述三分证明和 Root/独立 splice 审查已经充分，不需要新增 60 项祖先路径核验。结论只接本包 p2/p3；一般 p≥4 的实际根可达解析证明仍未付。

## 固定查询正核的准确边界

M-be451 v2 的结论针对固定查询集合 A、同一背景 b 及给定加入主题格，允许重复主题：

(−1)^k Δ_(R₁)…Δ_(R_k) U(A;b) = k! Σ_(x∈A∩R₁∩…∩R_k) 1/∏_(ℓ=1)^(k+1)(b_x+ℓ) ≥0。

单步 R=A 正是已定义分母差税，四角比较仅剩 A\B。它没有给同一完整 σ 的各真实偏离后缀 f_ij 与原实际后缀 r_i 之间的共同坐标序。真实差为 Σ_(x∈T_j)(f_ij−r_i)/[(b_i+1+r_i)(b_i+1+f_ij)]，分子可正可负，不能先取正部再保原等式，也不能把互斥分支拼成一条共同加入负载链。

令 D_adapt=Q−P_query，固定同一最优比较索引元组时 P_query−(OPT−W)=E−D_adapt。E≥W/m 是下界；actual IC 只给 P_query≤W，均未支付存在最优元组使 D_adapt≤E。故保留 M-be451 的 isolated-after-review 覆盖；本轮没有新增一般共同付款逻辑边。Δ_cov 与 D_adapt、尾利润与根查询 P 都各守自己的定义。

## 本轮执行和后续接口

本轮新工作只有定向实读、两数量标签/version 的记录比较、六端点 pin 与登记来源 SHA/标题核验，以及只读 binding preview。没有执行旧 84 尾 IC、祖先路径 IC、全树、LP、矩阵或生成器。成熟原根 9331/335923 个有序节点和 55986/2015538 项 IC 合同与原始策略 SHA 已继续匹配，全部计算仍按旧精确证据复用。

任务没有声明 follow-up 对；deferred 候选不冒作必须关闭的 overlap。closed_overlaps 与 follow_up_tasks 保持空。没有发现新依赖或源错误，当前记录勘误已解决。Git、队列、canonical 和 clone 本轮均未写；镜像留给 Root 串行安装、最终 bind/write/check、刷新资产哈希、checkpoint pushed 与 done。
