# Round48银行根半安全值的正式定向修复

本包承接 `customer-attraction-3a-3a-65ec03f362378017` 的24个同pin核心覆盖，源依赖中只有银行反族从v2/finite勘误到v3/proved。正式勘误只改version与truth_status，完整正文、statement和其余38个输入pin均未变。当前任务 `boss6-bank-status-repair-repair-b1ba63e69ea963cc` owner为Boss6，request `5cc6a2aa826f4568b11b285fa85b28ee`，definition pin为 `253800254660d1ee54d02d53f3acbad21a06c8305fd2bf219547672b5434c4aa`。本worker直接核当前39个登记pin；Git、远端及队列写入均由Root负责。

## 实读与继承

本次独立全文实读206行银行反族body、130行目标共用body、129行CAG定义，以及目标与源的完整当前登记记录、旧bank canonical边、全部旧receipt和旧任务声明。完整目标body同时载有PF候选；本次不声称对其全部旧证据重作审计。旧任务完整结构已解析，53项reading-ref声明均作为元数据检查；不是把这些引用的全部科学正文当作新实读。旧24条边的数学字段与嵌入的review均逐项读取，23条不受影响关系按原SHA与当前绑定承接。具体每core继承理由及每asset去向见reading-ledger与新receipt。

独立source-status review已全文读取。本次仍直接从正文重构承重论证，没有把历史独审身份冒作新外审，也没有运行LP、科学脚本、全树或旧证书。其它定向修复不在本包范围。

## 同一完整控制器的已付证明

银行目录是m个经济单例与m−1个互不相交双客户银行块的全部配对。真实玩家仍为m名单位提供者，客户也均为单位。一个主题(a,b)的终局收益恰为1/n_a+2/n_b。

从根的任意实际行动重锚BASE，使根所有偏离都沿同一预先固定σ的真实后继评价。BASE非末位规定使用fresh银行并复制根经济，收益2+1/(m−1)>2。非规定行动若银行fresh，则进入PUNISH，恰由末位复制该已发生银行，故偏离者银行至多1、经济至多1；若复用银行，则其银行份额已经至多1，后继进入EXIT也不改变上界。只改一坐标或联合改两坐标都包含。

PUNISH目标固定为模式进入时已经发生的过去银行，不能移动到后来fresh玩家。深度t过去银行全异时剩r=m−t人、fresh银行恰r−1个；非末位规定者独享两坐标得3，为裸上界。末位面对每个银行恰一旧用户，fresh经济加任一银行复制得2，为真实最佳回复。若再次偏离复用银行就进入EXIT。EXIT的银行重复永久保持，深度t已有种类至多t−1，因而fresh银行至少m−t个，够全部剩余玩家；经济也够。规定者收益3达裸上界，所有再偏离后仍合法。这些不变量覆盖全部有序历史。

根任意(a,b)后的BASE真实完成使根经济由m−1人共享、根银行由两人共享，所以每个根行动收益都为u1=1+1/(m−1)，规定行动是最佳回复。m=2没有中间玩家，根与末位仍完整合法。故这一控制器对全部整数m≥2确为完整纯SPE，证明不来自有限扫描。

## 真正静态整数安全值的固定对手

目标精确定义为v_m=max_p min_B Σ_A p_A f_B(A)，B有m−1个整数静态竞争主题，不能观察查询抽样实现。取一份固定B_j=(j,j)，j=0,…,m−2。银行各一次、经济各异，全乘积目录保证全部合法。对每个查询A=(a,b)，银行两客户各分1/2，合计1；经济贡献为1/2或1。因此所有查询同时满足f_B(A)≤2，对任意p也有min_B′ E_p f_B′≤E_p f_B≤2，取max_p得v_m≤2。

所以每m≥2都有u1=1+1/(m−1)>1≥v_m/2。这里仅用上界，不宣称v_m=2；没有用自由分数背景δ_m，也没有引入extra竞争槽或额外真实玩家。源正文m≥5对DIRECT的较强门槛失败，与本精确弱式的严格成立兼容。

## 边作用域与仍开放的义务

新边 `boss6-r48-bank-proved-controller-root-half-safety` 为accepted/unconditional、premises_mode:all。其普通参数域与指定已证σ不是未证前提；源当前proved，旧conditional唯一显式finite依据已经正式勘误。边保留contribution.result/remaining，不写whole_result。

当前目标仍是全部有限共同目录和每份完整纯SPE的原空根u1≥v_m/2一般open问题。本包只验证指定全参数银行族及指定控制器，未量化该实例上的所有其它SPE；其它目录、其它完整σ以及一般原根比较仍需证明或同一弱式的严格反例。正深度逐人加强、聚合安全及全人数half各保其原量词；本边不支付它们。

## 原覆盖、资产和overlap处置

24个核心pin全部相同，旧coverage的数学结论继续有效。23个条目逐字承接，目标条目保留旧末两位边，仅将旧bank edge ID替为新ID并说明这次独立复核。覆盖仍为19 linked、5 isolated-after-review、0 needs-decision。23条旧canonical边均未以银行反族为端点；逐条旧SHA、endpoint/evidence/review绑定均精确核过，文件原位保留，不复制或重写。

旧24 assets逐项在supersession内处置：23 retained并在新assets中列同一path/SHA；旧bank边replaced到新独立path，replacement_paths确在新assets。没有额外retired资产。旧任务恰有三项in-packet overlap（枢轴/中继的两项、两人税的一项），原对应边继续保留。原任务及receipt没有follow-up任务或closed对，本successor亦未声明follow-up，因此不伪造closed_overlaps或承接task ID。

manifest只hash新edge、ledger、review、validation，不hash自身或receipt；receipt再引用manifest及其它新资产。只有正式edge JSON使用顶层edge_id。校验记录使用reviewed_edge_id，避免被当作额外数学边。Root安装后仍应走正式edge-bind/edge-check、checkpoint、done与assemble。
