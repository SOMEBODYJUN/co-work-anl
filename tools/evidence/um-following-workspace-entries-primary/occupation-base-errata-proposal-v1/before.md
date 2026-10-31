# 失真组联合槽舍入与固定汇点占位双源审查

## 来源身份与阅读范围

本页完整读取并比较两个冻结来源：

- `bdd4c9c864096e4caa4e`，`research/current/unrelated_machines/distorted_group_joint_slot_rounding.md`，blob 与 SHA 按冻结 inventory 核对；
- `82af0ae2f147b7c28726`，`research/current/unrelated_machines/fixed_sink_occupation_rounding.md`，同按冻结 inventory 核对。

两源冻结于 legacy-cleanup 提交 68fad804ec5946cb296f77dc5b336308a66abf12 与 main 提交 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。第一源允许组内各任务的 home/sink 比例不同，并以同一 LP 共同决定宏位置与组出口；第二源固定 K 个共享汇点，把每个私有组压成有限模式，再用 occupation transversal matroid 和少量侧约束恢复整数调度。两者都是受限结构结果，未给一般 UM-TARGET-v1 算法或六人 SPE 结论。

## 一、组内异端畸变的共同槽合同

### 1. 定义域与精确保证

机器分成显式不交 homes H 与 sinks Z。宏任务只在 homes 有限，且有限宏端时间严格大于 T/2；私有组 J_h 的任务只可在 home h 和该组共同资格 sink 集 E_h 上执行。home 时间为 w_j，sink 时间 q_hzj。给定参数 delta < 1/2、kappa >= 1、Bbar >= 0，所有任务满足

b_hz w_j / kappa <= q_hzj <= b_hz w_j，且 0 <= b_hz <= Bbar。

另取 1/2 <= r < 1-delta。若每组总 home 量 W_h <= T、每个 w_j <= delta T，并保留宏端剪枝，则确定性位多项式算法或者返回 FAIL，或者输出完整实际分配，使 home 负载不超过 (1+r+delta)T，sink 负载不超过 (kappa+Bbar(1-r))T。若 OPT <= T，必成功；因此合同内 FAIL 蕴含 OPT > T。成功不判定任意原输入的 T 可行性。

在 promise 版本中不输入 OPT，承诺 W_h <= OPT、w_j <= delta OPT、宏端都大于 OPT/2，则可用整数网格二分找最小接受阈值 t，输出峰值不超过 alpha(r) OPT，其中 alpha(r) 是上述两个系数的最大值。若 delta < 1/2 且 kappa + Bbar delta < 2，取两条直线交点并夹到 [1/2,1-delta]，得到固定结构类的 alpha < 2。这个改善只属于该 promise 结构，不能写成一般 R||Cmax 近似。

### 2. 必要 LP 与宏、出口的共同选择

对每组定义 d_h(T) = max(W_h-rT,0)，c_hz(T)=b_hz d_h(T)。LP 变量 a_bh 决定宏任务的 home 匹配，y_hz 决定组出口，另有 d_h=0 时的零成本旁路。约束为每个宏恰选一个 home、每个 home 至多一个宏、每组出口质量等于占用 home 质量，并且每个 sink 的 c 加权总量不超过 kappa T。

任意真实 T 调度都给出该 LP 见证：宏端大于 T/2 保证每个 home 至多一个宏；占用 home 的私有任务送往各 sink 的 home 总量 e_h 大于 W_h-rT。若 d_h>0，以 e_hz/e_h 归一化；若 d_h=0，走旁路，避免 0/0。上下包络同时用于证明必要性和恢复性，不能只保留一侧不等式。

按每个 sink 的实际成本 c_hz 非增排序，把 y 区间切成单位槽，形成一个共同的分数槽流。整数增广流同时选宏 home 和 sink 槽；第一个槽至多多付一个最大成本，其余完整槽按前一槽成本收费。于是 sink 总成本不超过 [kappa+Bbar(1-r)]T。该共同流不能拆成先做宏匹配、再独立拼接接受证书。

### 3. 真实前缀恢复和复杂度

占用 home 的私有任务按固定编号依次撤出，直到留下不超过 (r+delta)T 的 home 量。最后撤出的任务至多 delta T，因此总出口小于 d_h；上下包络保证它在选中共同资格 sink 上的实际成本不超过槽预算。未占用 home 保留全部私有任务，负载至多 T。所有原任务均保留身份、只执行一次。

LP、排序、槽网络和前缀扫描均按显式输入位长多项式；不按大分母或参数数值循环。未知 OPT 搜索把所有有限处理时间分母取积为 Q，负载落在 1/Q 网格，按整数二分而非枚举 Q 个阈值。零任务、OPT=0、零时间端、空组、无 sink 和巨大分母均分支处理。有限审计用 Fraction 核验随机矩阵、非整数末槽、边界和高 W 家族，但没有实现通用 LP 后端或把审计提升为定理。

## 二、固定 K 共享汇点的占位拟阵合同

### 1. 模式菜单和 occupation 多面体

固定整数 K。宏任务只可在 homes H，且有限宏端时间严格大于 T/2；每个私有组 J_h 的任务只可在 h 与共享 sinks Z 的子集上执行。令 N 为私有任务总数，s=T/(4N)。对每组做多维 DP：sink 时间向上取整到整数，状态向量坐标不超过 floor(T/s)+n_h；每个状态只保留最小真实 home 负载的一条任务身份回溯。模式 q 带 occupied/empty 标签、完整任务分配和 sink 上界向量 w(q)。原 T 可行调度的每组模式一定在菜单中。

宏任务可用 home 集合构成 transversal matroid。令 P(Q) 为每 home 选一个模式、occupied 指示 x 属于该 matroid 独立集多面体的凸包。用宏边变量 z 展开成二分匹配流表达，P(Q) 是整数 occupation base 与每 home 模式的联合凸包；算法不需要枚举可能很长的凸组合。

### 2. 少量侧约束与 heavy 模式

对 P(Q) 加 K 个 sink 预算不等式。任一顶点 y 的正支持中，含两个以上正模式的 home 数至多 2K。证明把 occupied/empty 混合 home 集 F 放在宏 matroid 的最小面：交替匹配路径给出 F 内成对交换方向，面维数至少 |F|/2；模式纤维维数再加上 pure/mixed 支持自由度，若混合 home 数超过 2K，K 个侧约束无法把正维面压成顶点。

设 beta=1/(8K)，总出口权重大于 beta T 的模式为 heavy。原 T 可行模式的总出口至多 K(1+gamma)T，因此 heavy home 数有固定 O(K²) 上界。枚举 heavy home 及其具体模式，删除其他 heavy 模式，再对每个分支解有理 LP。逐坐标 lex 最小化保证得到 y 投影多面体的顶点，避免把扩展流多面体顶点的投影误称为 y 顶点。

### 3. 整数回溯和三半界

保留正支持模式，解带下界的宏匹配流覆盖所有宏任务和强制 occupied home；每个 home 依 occupation 标签回溯一条完整私有组分配。只有至多 2K 个非积分 home 会改变模式，且这些模式总出口不超过 beta T。固定模式的 sink 预算为 (1+gamma)T，新增至多 2K beta T；取 gamma=1/4 得 sink 负载不超过 3T/2。empty home 私有负载不超过 T，occupied home 私有负载不超过 T/2，再加宏端至多 T，也不超过 3T/2。

这是固定 K 下的确定性总位多项式算法，次数依赖 K；K 随输入增长时 DP 和 heavy 枚举呈 N 的 K 次方，不是统一多项式。模式不记录具体宏任务身份，若模式依赖宏边大小或身份，occupation 只有一个基拟阵的结构会失效。若一个私有任务可访问多个 home，组间不交和任务唯一性也失效。

来源另给含 OPT promise 的二分版本：当每个宏端严格大于 OPT/2 时，取最小宏边 a，令 U=2aD-1，在分母网格上调用给定 T 算法并维护“低于 OPT 的失败、成功上界不变”不变量。接受集合不必单调，也能以 O(log U) 次调用得到 3/2 OPT 调度。该身份依赖含 OPT 的 promise，不是一般输入算法。

## 比较、证据、处置和接续

第一源独有的是组内不同 sink/home 比例的上下包络、宏与组出口共同 LP、按实际成本排序的槽流、home 支付所有离散误差以及未知 OPT 的单调二分。第二源独有的是固定 K 的 occupation 基拟阵、K 个侧约束给出的 2K 非积分 home 界、heavy 模式枚举、lex 投影顶点和三半回溯。两者共同说明：任务必须按不交私有组保留身份；多 sink 预算要共同决定；固定低维侧约束可以支持受限正面算法，但不能代替一般结构选择。

两源的完整证明、条件 promise、有限证据和失败机制已分层。下一阶段应检查固定 K、唯一 home、上下包络、显式共同资格和宏端区间是否真的成立；不能把固定 K 三半合同或失真组 alpha<2 写成一般 UM 突破。六人 SPE 客户目录、完整历史、均分规则和任意平局语义不在本对象内，UM-TARGET-v1 与 SPE 覆盖目标仍开放。
