# r1-3d-covk：三个 COV-K 对象的共享 3D 实质数学复核

结论：在本次精确输入版本上，未发现三个对象的数学错误；三条既有 canonical 关系的方向及 whole/partial 范围正确。可由 Boss7 在确认相关 pins 未变后，仅接回这三个对象的数学审查并清其对象 pending。本 worker 未写 clone、Git、任务队列、registry、coverage 或 integration，未新增主覆盖 claim 或边。

## 精确输入及实际读取

本次 clone：`/workspace/scratch/d5435ebfeb39/co-work-anl-boss7`，读取 HEAD 指向提交 `9a47c49133643527bcdaf8ca2c24d9a89cc262b4`（只读 .git/HEAD 与 ref 文件，没有执行 Git 命令）。

已完整读根 `AGENTS.md` 与 `research/IMPLEMENTATION.md`。后者要求 accepted 逻辑边区分目标整条结论和局部贡献；只完成原目标分片时保留 contribution.result / remaining，不提升全目标真值。

数学全文完整读取七份文件：共同定理、COV-K 候选、共同目录完整历史模型、固定背景两人税引理、固定背景剩余收益与税定义、verify.py、replay.json。共同定理的四人粗行节亦已读全，但本次审查不是四人弱行障碍对象的新主覆盖或一般四人 COV-K 的证明。三条 canonical 边和对应 3A、3B 收据完整实读；另实读弱四人收据以确认既有比较范围没有误用本三个对象。

七份全文字节 SHA、六个相关对象精确 registration_pin、三条 canonical 边 SHA/pin、两份收据 SHA/pin、snapshot 文件 SHA 均在同目录 `review.json`。所有正文和 evidence 引用与当前字节相符，相关 endpoint_pins、evidence_pins、integration 的 object/edge/receipt pins 均匹配。须区分原文件 SHA 与规范 JSON semantic pin，二者本来不同。

三个待审对象均为 v1：

| 对象 | 当前 registration_pin | 真值 |
|---|---|---|
| customer-attraction/cov-k-actual-menu-nonconvexity | bd345c4a8d5cfb53342b391bc209f339dac1652f4d5ee4fc7bcceac75fb303bf | proved |
| customer-attraction/cov-k-scaled-actual-up-to-three | 00e6c3c6e2ed0845e8017d252e9e81131cc04afa3c0af5ce49c0358d7b14b35d | proved |
| customer-attraction/cov-k-true-menu-universal-convexity | a97dd0319bf93b5df1886601f38cf530750a93aeece997e9560401778e139f4e | refuted |

共同定理全文 SHA：`c2889e135218262c7aca12166afa9df9f049b7ccab15002e0e5d837ce7f58173`。

## J、K 与原 SPE 的同一性

共同模型保有限单位客户、有限非空共同标签目录、空覆盖、同覆盖不同标签、重复动作和所有有序历史上的离轨平局。固定一份完整纯 SPE σ，位置 i 的强制动作发生在其实际前缀，强制之后按照同一 σ 的改变后有序历史真实完成；删的是当前槽，保留其余 m−1 槽。故

`K=(1/m) Σ_i conv{ℓ_i(A): A 合法}`

确为本份原策略的真实删槽菜单域，没有以一般合法分数背景代替它，也没有冻结实际后继。

每一行选实际标签 B_i，得到列 `c−1_(B_i)`，求平均严格给 `L⁰=(m−1)c/m∈K`。不同实际标签可以相同覆盖，不影响此等式。

逐查询函数 `J_(m,Q)(L)=Σ_x [m1_(x∈Q)+L_x]/(1+L_x)` 的最大值，正是同一 L 上的 `mγ(L)+T(L)`。对任意最优 m 元组及并集 C，用 `1=t_x+L_xt_x`、非负 L、并集的查询重数至少一，得到 `OPT_m≤J_m(L)`。这是静态覆盖上界，不需要 J 在 K 上凸，也不反向表明 half 与 COV-K 等价。

## 两人税精确式及 m≤3 预算

实际末两人写 B,C，合法前缀负载 b；令 R 是同一策略在倒二改选 C 后的真实末回复。在税引理精确式(3)中取实际 (B,C)、比较 (C,Q)，再从左右扣掉同一个显式 `g_b(C,Q)`，得到

`E=u_B+u_C−f_b(C)−f_b(Q)+g_b(C,Q)+g_b(B,B)`

`=[u_B−U_b(C,R)]+[U_b(R,C)−U_b(Q,C)]+[u_C−U_b(R,B)]+[g_b(B,B)−g_b(B,R)]≥0`。

前三项分别由倒二实际节点、强制 C 的真实离轨末节点、实际末节点的 SPE IC 支付。末项逐客户非负。这里不是仅从较弱的 T2 不等式随意扣掉一个非负量；原对象 statement 本身含精确三 IC 加两余项分解，正文亦完整承载它。强式的使用在对象和边两层都有支持。

实际末位强制 Q 给 `D=u_C−Σ_Q 1/(1+b+1_B)≥0`。m=3 时根实际 A；根强制任意查询标签后，每个该标签客户最终最多三人共享，故其真实偏离收益至少查询规模/3，得到 R_B、R_C、R_Q 三行非负。此根保底不要求冻结后继。

对任意客户实际命中 n、查询会员 q，`P=[m²q+(m−1)n]/[m+(m−1)n]−2·1_(n>0)`。本次用独立 Fraction 代码重建全部 8+16 列，未调用或导入原 verify.py，并与冻结 replay.json 逐值相等：

* m=2：`P+(6/5)d+(4/5)e` 的未覆盖列为 0；全部覆盖列最大 `−7/15`。
* m=3：`P+(1/20)r_B+(1/2)r_C+(4/5)r_Q+(17/10)d+(31/30)e` 的未覆盖列为 0；全部覆盖列最大 `−1/15`。

因为各乘子及其全客户总行量非负，求和得到 `J_(2,Q)(L⁰)−2W≤−7W/15` 和 `J_(3,Q)(L⁰)−2W≤−W/15`。Q 任意，故分别得到 `J₂(L⁰)≤23W/15`、`J₃(L⁰)≤29W/15`。此证明是对全部客户类型的有限穷尽代数证书，不是有限实例扫描外推。

m=1 时删槽列全零，K={0}；根 SPE 选择最大主题，故 `J₁(0)=W=OPT₁`。零客户时各量零，亦成立。m≥4 及系数锐性没有由此得到。

另用 b=0、1 和全部 B,C,Q,R 会员位独立逐列核对上述 E 的精确四项分解，共 32 个有理恒等式。此检查服务当前 m≤3；非负 IC 的全称性来自完整 SPE 定义。

独立计算结果已保存 `independent-checks.json`；没有重跑大实验。

## 真实两人非凸反例

仅两个标签 A、B，覆盖不交且规模 3、2。A 后末位 B 的收益 `2>3/2`，B 后末位 A 的收益 `3>1`；根沿这两真实后继的收益分别 `3>2`。故完整纯 SPE 严格唯一：根 A、A 后 B、B 后 A。本次独立检查二标签全部 8 份完整策略，也仅此一份满足全部三个节点的 IC。

根强制 A、B 后删根槽得到 1_B、1_A；末位实际前缀是 A，无论强制哪个标签再删末位槽均得 1_A。两行平均的整个真实域恰为

`K={L_s=(1−s)1_A+s1_B:0≤s≤1/2}`。

不是只在 K 内找到一条假定线段，而是已列尽全部行列并算出整个 K。两主题价格 `3/(2−s)`、`2/(1+s)` 在 `s=1/5` 相等，最大值与背景价相加给正文两支 J₂。左支导数严格负，右支严格正，唯一最小点为 `s=1/5`，`min_K J₂=5=W=OPT₂`。

右支内点 `s=1/4` 的二阶导数为

`384/343−256/125=−39808/42875<0`。

该点附近没有查询切换，J₂ 光滑，因此负二阶导数严格排除 K 上凸性。一个真实 m=2 完整 SPE 的反例足够反驳目标 `∀m≥2、∀实例、∀完整SPE、所有同K线段` 的全称凸性；它不证明每个指定较大人数都非凸。

同例 `min J₂=5≤2W=10`，所以它满足 COV-K。非凸性不推出覆盖付款失败，也不否定 half；这与 m≤3 的普遍预算完全相容。

## canonical 边与既有交付的实际范围

三条相关边全部已在当前 `registry.edge_files`，均 accepted、unconditional、premises_mode=all，且本次没有新增相关边 pending：

1. `boss5-cov-k-tax-and-spe-pay-small-populations`：`CA-TWO-REMAINING-TAX → cov-k-scaled-actual-up-to-three`，whole。税精确式联合明列的同模型 SPE 条件/根保底/末位 IC，完整得到 m=1,2,3 固定 L⁰ 的定量结论。原始边文件 SHA `4bd6906000a5d08cd7edc35d2284af053239f907cb6d266281206cab2b0f90b8`。
2. `boss5-cov-k-real-two-player-example-refutes-universal-convexity`：`cov-k-actual-menu-nonconvexity refutes cov-k-true-menu-universal-convexity`，whole。否定的是全称凸性，非预算。原始边文件 SHA `d9fe4504f22bb0671ccf27d523ffd58dc7323e2152850c9072b32317da8cf43b`。
3. `boss5-cov-k-small-population-contributes-open-budget`：`cov-k-scaled-actual-up-to-three → shared-menu-direct-coverage-objective-and-signed-curvature`，partial，明确 contribution.result 仅 m≤3，remaining 保 m≥4。原始边文件 SHA `84e4f8bcae757c84fed4dc13a62ed0f231bc7ec6f1c87527f22d506a8c21dda4`。

两份正式 done 收据为 Boss5 的 `ca-cov-k-small-actual-menu-comparison-3b-582a6a954f2e2057` 和 `ca-cov-k-small-primary-3a-a6564508d8d573cb`。3B 引用全部三条边；3A 复用原路径/原 SHA 的税 whole 与反驳 whole，没有重复制造相同关系。当前 coverage 已合两份实际比较，三个核心均 linked，pin 与当前 registry 一致。integration 中两 receipt pins 及三 edge pins 亦已匹配现有内容；本轮待补的是三个对象的共享数学集成审查，不是缺少 canonical 资产。

共同页四人例只说明所列粗必要行不能支付指定 L⁰，实际路径不满足 SPE：在 (A,B,Q) 后唯一末回复 D，倒二由 C 改 Q 得 `18>25/2`。即使固定 L⁰ 有正预算缺口，也没有真实完整 SPE 与整个真实 K 的反例。此节不能把第三条 partial 升级成全称 refutes。

## 集成建议

建议接入以上三对象的已完成审查，在确认 `review.json` 的三个 registration_pin 及共同正文 SHA 仍相同时，仅从 `pending_changes.object_ids` 移除这三个对象。保持原 proved/proved/refuted 状态；保原三条 canonical 边及两收据，不新增重复主覆盖，不提升全人数 COV-K 的 open 状态。

本次 pending 中其余四个对象、三条 rook 边及 weighted-congestion / customer-attraction 的其他审查由各自实际范围继续处理；本 worker 没有为它们给出清除授权。特别是 archive_scopes 不能仅凭本三个对象已审就全清。完整 pending 快照留在 `review.json`。
