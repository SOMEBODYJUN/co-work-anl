from pathlib import Path
import json,hashlib
stage=Path(__file__).resolve().parents[4]
base=stage/'archives/unrelated-machines/state'
def put(kind,name,s):
 p=base/kind/(name+'--'+kind+'.md');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n');return str(p.relative_to(stage))
paths=[]
paths.append(put('资源','容量一星族的全机器对原入口与符号耦合',r'''
---
id: capacity-one-star-original-all-pair-audit
kind: resource
type_tag: 资源
title: 容量一星族的全机器对原入口与符号耦合
status: integrated
truth_status: symbolic-family-proof-and-finite-exact-program
review_level: full-primary-code-read-and-frozen-run-binding
summary: 保全旧k块容量一星族的实际原入口、全部两机配置公式及因子化计数，区别后来共享逃逸族和全局联合分布。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/capacity_one_star_pair.py
---

# 原入口的数学对象

原件 [capacity_one_star_pair.py](../../tools/evidence/capacity-half-slot-and-row-reviews/original/capacity_one_star_pair.py) 为 7067 字节，SHA-256 `f2a47ff47c9b03e5eaa2f5e747aa97908ebf35f031677251dbf8257cf489732f`。它不是通用配置求解器：`build(k)` 直接生成特定族，`explicit_pair` 返回有理耦合，`audit(k)` 核对全部机器对，main 仅运行整数 k=3,…,12。只导入 collections、fractions、itertools、json、platform，无外部输入文件、第三方依赖、随机数或容差。`build` 的代码前提仅是 `assert k>=2`，没有实现一般输入类型验证；不把这个断言当作健壮的公共 API。

固定整数 k≥2。机器是 V_a（0≤a<k）、G_g（0≤g<k−1）、R_(a,ℓ)（0≤ℓ≤k）。每块有 X_a、k 个 Y_(a,h)、k 个 Z_(a,r)。X 在自身 V 和所有 G 上时间1；Y 仅在本块全部 R 上时间1；Z 在自身 V 上时间1/k、在本块 R 上时间1，其余不可用。故 m=k²+3k−1，n=2k²+k，有限资格数 2k³+4k²，最小任务资格数 k。这里没有共享逃逸机 z，也不是后来 N=2k²、G=N−2k 的族。

在目标1，V_a 的两配置为 {X_a} 权1/k、全部 Z_a 权(k−1)/k；每个 G 对每个 X_a 给单项权1/k；每个 R 对每个 Y 给单项权1/(k+1)，对每个 Z 给单项权1/[k(k+1)]。机器归一；X 总覆盖1/k+(k−1)/k=1，Y 总覆盖1，Z 总覆盖(k−1)/k+1/k=1；全部配置真实负载≤1。代码逐配置、逐任务验证，而非只验证行负载。受支持配置总数 2k+k(k−1)+2k²(k+1)=2k³+3k²+k。

# 完整两机合同与四种非乘积公式

GPC₂ 要求每机完整配置边际和每对机器的联合配置分布，边际正确且正质量的两配置不共享任务；任务可有多端，因此不要求任意机器对内部恰覆盖每个任务一次。不同 pair 不要求拥有同一个三机以上联合分布。

所有 h,r,a 的移位按模 k。代码配置索引在 V 为 X、全Z，在 R 为全部 Y 后全部 Z，在 G 为 X_a。下列是完整非乘积表，未列 pair 的支持任务集互不相交，取边际乘积。

| 机器对 | 配置对及质量 |
|---|---|
| G–G | ({X_a},{X_(a+1)})：1/k |
| 同块 R–R | ({Y_h},{Y_(h+1)})：1/(k+1)；({Z_r},{Z_(r+1)})：1/[k(k+1)] |
| V_a–R_(a,ℓ) | ({X_a},{Z_r})：1/[k(k+1)]；({X_a},{Y_h})：1/[k²(k+1)]；(全Z_a,{Y_h})：(k−1)/k² |
| V_a–G | ({X_a},{X_b}),b≠a：1/[k(k−1)]；(全Z_a,{X_a})：1/k；(全Z_a,{X_b}),b≠a：(k−2)/[k(k−1)] |

对 V–R，X 行和为1/(k+1)+1/[k(k+1)]=1/k；每 Y 列和为1/[k²(k+1)]+(k−1)/k²=1/(k+1)，每 Z 列和为1/[k(k+1)]。对 V–G，X 行和1/k，每个右列和1/k。循环移位无固定点，其他正质量项也不双选同一任务。k=2 时末项为0，代码允许保留零质量项，并只对正质量检查不相交。

`audit` 对全部无序机器对实际迭代。四类显式 pair 数依次为 binom(k−1,2)、k·binom(k+1,2)、k(k+1)、k(k−1)。乘积 pair 不展开全部笛卡尔项，而是断言两侧支持并集不交、分别归一，并验证乘积边际；记录的 represented entries 是被因子化表示的条目数。不能把这个数当作程序逐条展开检查数量，也不能把全部 pair 当作全局联合证书。

# 整数值、消元边界及证明身份

整数最优 θ_k=2−1/k。假设峰值小于 θ_k<2，则每个 G/R 仅能接一个单位任务。k 个 X 面对 k−1 个 G，至少一个 X_a 留中心。该块 k 个 Y 只能占 k 个 R，最多留一个 R 接 Z，所以中心保留至少 k−1 个 Z，负载≥θ_k，矛盾。上界选一个中心留 X 和 k−1 个 Z、外送一个 Z，其余 X 双射至 G；各块 Y 各占一个 R，其他中心留全部 Z。峰值恰 θ_k。

原程序输出 `proved_integer_optimum` 仅计算有理公式，不搜索整数调度。最优性来自上述一般证明和相关正文，不是该字段本身。k≥3 时没有 T=1 极小超载星规则起点：V 总和2删最小后2−1/k>1，G 总和k删一后k−1>1，R 总和2k删一后2k−1>1。程序用“总和≤1或存在某一项删除后仍>1”精确检查不可触发，断言恰当且仅当 k≥3；k=2 的 G 可触发，不能把不可约域扩大到它。最小资格数 k≥3 也使单/双域基数闭包没有起点。

GPC₂ 投影为配置 LP，标准有序槽给任意接受目标 T 的实际峰值≤2T；若先极小星消元，逆恢复为 max(2T,T)=2T。本族 T<1 时 Y 无有限保留边，T=1 通过，θ_k→2。因此只有这个接受合同在正 OPT 域的上确界 gap 为2，不是一般调度近似困难性、完整 SA/SDP 下界或多项式 GPC₂ oracle。已有[极小星与最小工作面审查](../审查/极小超载星容量耦合与最小工作面支撑障碍有限审查--审查.md)承载一般消元及其他 Claim；这里保存原入口和未在旧页展开的完整公式，不重新授予那些已吸收定理。

# 真实历史运行与有限范围

[冻结聚合结果](../../tools/evidence/capacity-half-slot-and-row-reviews/historical-runs/minimal_star_capacity_audit.json) 的 `reports.capacity_pair_reproduced.json` 保存实际 stdout 对象，base_commit 为 `974813e88ff9f80cdda9a1f817be990ce1d90816`，Python3.12.14，Fraction 精确运算，代码 SHA 与本原件相同。历史命令为 `python3 tests/audits/unrelated_machines/capacity_one_star_pair.py`。本批复用这次充分执行，不新增原入口运行；历史 JSON 未记数值退出码或耗时，不补造。

| k | m / n | 全机器对 | 显式pair | 实际显式条目 | 因子化pair / represented条目 |
|---|---|---:|---:|---:|---:|
|3|17 / 21|136|37|249|99 / 2460|
|4|27 / 36|351|75|656|276 / 12504|
|5|39 / 55|741|131|1410|610 / 44440|
|6|53 / 78|1378|208|2658|1170 / 126060|
|7|69 / 105|2346|309|4571|2037 / 305844|
|8|87 / 136|3741|437|7344|3304 / 661360|
|9|107 / 171|5671|595|11196|5076 / 1309104|
|10|129 / 210|8256|786|16370|7470 / 2415780|
|11|153 / 253|11628|1013|23133|10615 / 4211020|
|12|179 / 300|15931|1279|31776|14652 / 7001544|

公式来自原研究者重构、frontier_algorithms 独立精确核验；不能因代码写有 independent 就称全部数学零信息盲发现。后来 compact_count_escape 只复用本代码块内 R–R/V–R，另改总块数及 G–G/V–G；本源作为前批 dependency 已读不等于此前已经 primary done。当前以原程序的完整域、函数义务及真实历史输出完成独立处置。
'''))
paths.append(put('资源','半单位奇偶实例的实际槽匹配与完整容量回溯',r'''
---
id: parity-half-unit-actual-slot-primary-audit
kind: resource
type_tag: 资源
title: 半单位奇偶实例的实际槽匹配与完整容量回溯
status: integrated
truth_status: one-exact-instance-with-self-contained-optimum-proof
review_level: full-primary-code-read-and-frozen-input-certificate-check
summary: 保存十机十四作业半单位奇偶实例的全部输入、分数点、有序槽算法与实际分配，区分有限回溯和一般三半证明。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/half_unit_joint_slot.py
---

# 实际输入而非抽象槽玩具

原件 [half_unit_joint_slot.py](../../tools/evidence/capacity-half-slot-and-row-reviews/original/half_unit_joint_slot.py)，4018字节，SHA-256 `c07f31788f7aad244a781468a439e1cbcb565f839a8e5695bb9fa9d73ce0c763`。脚本顶层直接构造、检查并打印一个实例，没有 CLI、通用 LP 求解、项目导入、外部矩阵、随机 seed 或第三方依赖；只有 Fraction、combinations、json。导入此脚本也会执行全部断言，本批验证只解析 AST 和已冻结输入，不导入或重复运行它。

三元组集合 E={(0,0,0),(0,1,1),(1,0,1),(1,1,0)}。机器按固定顺序为 R_0,R_1,S_000,S_011,S_101,S_110,Y_0,Y_1,Z_0,Z_1。作业依次为 A_(0,t),t=0,1,2；A_(1,t),t=0,1,2；再按 E 顺序列 I_(a,1),I_(a,2)，共14项。

| 作业 | 全部有限资格及真实时间 | 分数证书 |
|---|---|---|
| A_(x,t) | R_x：1/2；两个 a_0=x 的 S_a：各1 | R_x：2/3；这两个 S：各1/6 |
| I_(a,1) | S_a：1/2；Y_(a_1)：1 | 两端各1/2 |
| I_(a,2) | S_a：1/2；Z_(a_2)：1 | 两端各1/2 |

其他边不可用，共34条有限资格。各任务分数和1。R_x 接三个 A 的分数负载3·(1/2)(2/3)=1；S_a 接三 A 的负载1/2和两个 I 的负载1/2，合计1；每个元素机接两个 I 的单位端质量1/2，也为1。机器数10，任务数14，全部处理时间仅1/2和1。

# 前缀断言和实际槽算法

每行 γ 取最小正有限时间，max p≤2γ。目标 T=1，逐行断言时间>1/2的质量≤1、时间>1/3的质量≤2，以及 T<4γ 时总质量≤floor(1/γ)。R 的总质量2、全为1/2；S 的单位质量1/2、总质量3/2；Y/Z 的单位质量和总质量均1。故所有前缀与 floor 条件均真。

代码按每机时间非增、同时间按 job 编号排序，依次把 x 质量装入从0开始的单位槽，只在片段正交长时建立 job→slot 边。R 各2槽，S 各2槽，四元素机各1槽，总16槽；14个任务的覆盖匹配无须使用全部槽。递归 augment 按列表顺序扫描槽，用每次独立 seen 集防止重复；若槽已有任务则递归重配，全部14次增广成功。最后把每个任务的 matched slot 还原为原机器并按真实 p 求和。

冻结结果的机器编号赋值为 `[0,0,3,4,1,1,2,2,7,3,6,4,5,5]`，按上述作业顺序解释。实际负载为 `[1,1,1,3/2,3/2,1,1,1,0,0]`。所有作业恰分配一次且资格合法；这是完整普通 UM 任务调度，不是把局部允许槽独立挑选后拼接。

# 最优值3/2的自足解释与回溯实际义务

E 中任意两不同三元组都共享一个坐标，没有完美3DM匹配。若有峰值≤1调度，每个 R_x 最多接两个 A，故每个 x 至少一个 A 送 S；一个 S 最多接一个 A。凡接 A 的 S 不能再接任一 I，所以它的两个 I 必送对应 Y/Z。四元素机各最多接一个单位 I，因此至多两个 S 接 A，且为每个 x 各一个。这两个三元组的 Y/Z 坐标也必须互异，构成完美3DM，矛盾。于是不存在峰值1调度。

所有真实负载均为半整数，因此不存在峰值<3/2调度。上界可把全部 A 留各自 R（负载3/2），两个 I 留各自 S（负载1），元素机空；也可用上面的实际槽匹配。因此 OPT=3/2。

脚本另用 `has_schedule(cap)` 做完整有限域赋值回溯：按每作业资格数排序，逐一尝试全部合法端，仅在机器当前负载加 p≤cap 时递归，失败退回负载。检查 cap=1 返回 False、cap=3/2 返回 True。它不依赖槽图求不可行性，且没有启发式裁剪遗漏；但代码没有输出节点数或“枚举了全部多少调度”，不能补造统计。该有限精确搜索不是多项式通用调度算法，也没有搜索所有参数化3DM输入。

# 与一般三半算法、旧审查和后续结构类的关系

行内[γ_i,2γ_i]的一般证明用整数前缀保持：时间>a的质量≤整数 r，则这些片段全在前 r 槽，任意覆盖匹配至多选 r 件。目标 T 与 γ_i 的比 t 分四段：t<2总数≤1；2≤t<3总数≤2且至多一件>T/2；3≤t<4总数≤3且最大≤2T/3、第二≤T/2、第三≤T/3；t≥4用加性 ST 的负载≤分数负载+最大项≤3T/2。故在该额外跨度域，全体任务一次联合匹配可同时守3T/2。一般有理 LP 和目标搜索由相关正文证明，不由本脚本实现。

旧冻结 [joint_slot_prefix_audit.json](../../tools/evidence/capacity-half-slot-and-row-reviews/historical-runs/joint_slot_prefix_audit.json) 保存主正文旧 SHA `8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00`、本代码 c07、Python3.12.14 和完整 input/x/assignment。当前相关正文 SHA 为 ab1a6cd8…，其新增§7的共同 b、每行至多两枚正 small 是另一合同。本实例的 R_x 有三枚1/2资格，因而**不属于** b=1 下每行至多两 small 的新域；后者使用没有本 R 源机的另一3DM编译。不能因两者均有半单位值就混成同一输入类。

旧审查先见仅显式负载断言的早版，再自行只读核前缀、floor和输出计数；作者随后加入当前断言，审查者读并重跑最终 c07。更早代码字节未保存在本批，不能杜撰其 SHA；最终源与旧冻结 run 已精确对齐。本批复用这次充分历史执行，新增原程序运行0，旧记录无数值退出码/耗时。原审查主源属于 Boss2，本页只用已保存比较材料确认版本语境，不替它记 primary done。

本资源给一个真实全局输入的精确证书和有限最优值，不认证全球新颖性、全部 LP、一般 UM 的统一低于2算法，也不把精确中间见证障碍解释成实际近似调度困难。容量一星族随 k 的跨度无界，不能直接套此跨度2正面推论。
'''))
paths.append(put('审查','全局行计数审查的原冻结范围与多行追加证明',r'''
---
id: global-row-count-review-frozen-and-multirow-append
kind: review
type_tag: 审查
title: 全局行计数审查的原冻结范围与多行追加证明
status: integrated
truth_status: proof-review-with-explicit-version-and-finite-scope
review_level: full-primary-review-read-and-code-record-comparison
summary: 保存独立重构后读稿的全局计数审查及后来尖锐多行预算追加，不把初始审查扩成后来的完整配置证明。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/row_count_escape_review.md
---

# 冻结版本和实际先验

[原审查](../../tools/evidence/capacity-half-slot-and-row-reviews/original/row_count_escape_review.md) 13640字节，SHA-256 `ad9425cfa968a654d586d3cec11d80940eb0cdb23278842197947ee96bee5f7b`。其独立攻击者先从精确候选重构安全性、全池支配、整数与匹配机制，再读冻结正文和实现；不是事前不知道候选的盲发现。初始正文 row_count_escape_gap 的§1–5 SHA 为 `78b9b5b9ee288a783b07925834ee064e7bbee2737d306bf69771559887a5cc50`。旧审查“每配置延伸”指的是其余行仅计数的真实任务分配，不能读成后来完整配置 LP 的(MP)。

审查列出的实现为 row_count_probe `9b334965…`、compact_count_escape `c2602531…`、independent_row_count_escape `f5de5fc8…`，以及仅复用局部公式的 capacity_one_star_pair `f2a47ff4…`；相应原件和完整 SHA 见[manifest](../../tools/evidence/capacity-half-slot-and-row-reviews/manifest.json)。旧 minimal-star 正文受审 SHA 为 be27a3e9…，旧条件块稿为96289781…，均不是当前增补后整文件身份。审查明确未重做全部经典 ST/LST 或文献证明。

# 安全查询、精确权优化与全池量词

合法非负有理输入 P，目标 T≥0；当前 D_j 保留 p_ij≤T 的资格。每机器空行 c_i=0、含零最小值 c_i=n，其他 c_i=min(n,floor(T/h_i))，h_i 为当前行最小有限时间。固定存活边 j→v，把其他任务分为必须外送 Q={a≠j:v∉D_a} 和可留/外送 B={a≠j:v∈D_a}。在除 v 外机器上守 c_i，先匹配全部 Q，再最大化匹配 B 的任务权 p_va。若无覆盖 Q 的匹配或最小 v 负载 p_vj+Σ_(a∈B)p_va−W>T，同步删此边，重算行界。

若 σ 是当前 T 调度且 σ(j)=v，σ 的外送部分给覆盖 Q 的容量匹配，σ 在 v 的负载至少上述最小值。因此该边不被删；同步处理与重算 row-min 仍保 σ，归纳至稳定。拒绝保证 OPT>T，接受没有调度保证。零权、T=0、空任务、单可用机器和大分母都不破坏此证明。

每机器复制≤n个槽，匹配地集是横截拟阵，覆盖 Q 后的 B 是收缩/限制拟阵；按任务权降序逐项尝试增广给最大总权，不能推广成任意目的边权贪心。每查询≤n次增广，槽≤mn、边≤ne；总查询≤e(e+1)。有理公分母位长≤输入分母总位长，floor 精确且容量截断，故总输入位长多项式。

固定同一组全行有效 H_i/c_i 时，对任意池 R⊆M\{v}，只保留 D_a⊆R 的必选任务及 v∈D_a、D_a\{v}⊆R 的可选任务。全局匹配限制到这些任务仍落在 R，未匹配可选子集的非负权≤全局未匹配总权，所以全局通过蕴含每子池通过；全池本身也是一个池，故等价。若每池另按不同局部任务重新提高 H，就不在此支配合同内。

# 旧紧凑族和全部独立计数见证

k≥2，N=2k²，G=N−2k。N 个中心 V_a、G 个全局机、每块 k+1 个 R、共享 z；X_a 在自身 V/全部 G 上1，Z 在自身 V 上1/k/本块 R 上1，Y 在本块 R 上1/z上1/k。m=2k³+6k²−2k+1，n=4k³+2k²，有限资格数8k⁴+4k³+2k²。显式编码多项式，不能将边数误写 O(k³)。

峰值 B<θ_k=2−1/k 迫至少2k个 X 留中心；每活跃中心至少两个 Z 外送本块 R，k+1单位 R 槽遂迫至少一个 Y 去 z，合计 z≥2>B。选择2k个活跃中心各仅外送一个 Z、其余 X 给 G，z空，可达θ_k。配置证书：V 以1/k选X、(k−1)/k选全Z，G对每X权1/N，R对每Y权1/(k+1)/每Z权1/[k(k+1)]，z空。全任务恰覆盖；G–G 用 N 循环、R–R/V–R只用块内k，V–G 用1/[k(N−1)]、1/N及1/N−1/[k(N−1)]补足边际。pair 无全局联合要求。

初始 count cap 在 V/z 为k、G/R为1。基线选2k活跃块，各中心有 X+k−1Z 共k项。避开 V_a：选其他2k活跃、X_a给G，本块kZ占kR、一个Y占余R、其余k−1Y去z；避开G：改2k+1活跃；避开R_(a,ℓ)：令a非活跃，全部Z留V、kY用其余kR；避开z：基线。k=2时全部数目也合法。把任一可用 j 从该 avoid-v 全分配移回 v，v只收j且真实负载≤1；把任意合法完整 C 移回 v 也同理，其他机只减计数。这是每个(v,C)各有完整任务见证，并不共同守其他中心真实容量。

极小星及单/双域闭包无起点；最小资格数≥4。接受合同含配置投影，标准槽及极小星恢复给≤2T，一族θ_k→2使其正 OPT 上确界 gap 恰2。它只排这种信息合同的统一相对 T 改善，不是一般困难性；接受单调、阈值 oracle 都不由它免费得到。

旧条件块 cut 可修复这族。对1≤B<θ_k，r_B=k−floor(k(B−1))≥2。X 在 V 迫≥r_B个 Z 外送，再迫≥r_B−1个 Y 去z，所以 Σ_s x_(z,Y_as)≥(r_B−1)x_(V_a,X_a)。G 槽给Σ_a x_(V_a,X_a)≥2k，z负载≥2(r_B−1)≥2>B。B=θ_k 时 r_B=1，上界调度可行。系数必须随 B 变化，不能把低目标系数搬到θ_k。一般识别/分离/联合舍入仍缺。

# 后加多行真实负载的独立证明及代码差异

追加审查只认证 UM-COMPACT-MULTIROW-EXTENSION-v1。被审整稿 SHA `da4737f6408b59c87a4c1c986c365cd6558ccf3651f5e13ce17d3b6b6b498c6f`；审查者从提交957f04b取回的旧字节 SHA仍78b9…且为追加稿完整前缀。代码 multirow_count_extension SHA `10d4387a560e5c025292adf634f2e9153161dd55bd23763c2855fcfaeb9767a3`，仅动态导入独立稀疏族的 build_family，不导入主探针。

给任意 U，要求其全部真实负载≤1，全机仍守上述 count cap，固定 v∈U 精确取得任意 C∈C_v(1)。若 |U∩V|≤G，对每个(U,v,C)存在完整任务分配；预算 G 尖锐。令 O=V\U，至少2k中心；基线只激活 O 中2k个。若空G或必须避开一个 O 中心导致缺一个可用激活，取 U 中心 b 仅收X，全部 kZ去R、k−1Y去z，另一个Y占余R；b真实负载1，z负载(k−1)/k。只有 |O|=2k 时才需此唯一补位，不把 z 重复借给多个分支。

V pin X：该中心完整卸载、另选2k−1个O活跃；V pin r个Z：本块外送d=k−r个Z，只需max(0,d−1)个Y去z，另2k活跃都选O。G pin指定X：避开它的块选2k活跃，必要时补b；G空需2k+1活跃。R空要本块非活跃，必要时补b；R pinY/Z 可直接在活跃基线重排：指定Y占目标R、原单外放Z改另一R，指定Z就选它为该外放项。若本块非活跃，X原在G，指定Z只减少中心一个Z，不另增G需求。独立代码则统一令该 R 块非活跃，必要时用b补位，两种实际构造均合法且身份不同。z pin任意≤k个Y直接从无z基线移来。

尖锐边界：取 G+1 中心入U，并含z，固定 z空。任一 U 中心若接X，为守≤1必须把全部kZ外送，与kY共2k单位任务挤入k+1个R，不可能。因此 N 个X只能用G个全局机加2k−1个U外自身中心，共N−1槽，Hall不足1。这个结论是存在一个失败pin，不是所有超过预算pin都失败。代码必要匹配秩 k=2为7<8、k=3为17<18，不是一般全调度搜索。任意固定r、ε可同时取G≥r且1/k<ε，所以固定数量真实容量探针仍不够；不同见证无共同一致性。

# 实际有限运行、同期更新及未覆盖部分

原审查明确实际执行 row_count_probe、compact_count_escape、independent_row_count_escape，后来执行 multirow_count_extension；stdout先写scratch，再汇总冻结。对应[行计数结果](../../tools/evidence/capacity-half-slot-and-row-reviews/historical-runs/row_count_escape_audit.json)与[多行结果](../../tools/evidence/capacity-half-slot-and-row-reviews/historical-runs/multirow_count_extension_audit.json)的实际范围是：

| 路径 | 实际有限域 |
|---|---|
| 主查询 | 7344合法小矩阵、34344独立全分配oracle查询、26624个T可行保边调度、5边界、8非法fixture |
| 主族 | k2..5配置/全部pair；仅k2实际优化全部168资格，较大k查询数0表示未执行 |
| 独立族 | k2..5逐机器avoid分配；k2..4全部pair分类并重标号复用局部代表公式；k2..8在1/k整数网格上实际任务转移的R占用置换商DP |
| 多行 | k2全部163中心子集、50319完整见证、2012760逐任务核验、每U有137种z配置；k3一个12中心边界的30结构病例、3780逐任务检查 |

商 DP 只商去同块 R 置换，仍转移真实 Z/Y，因此给所列有限k的精确OPT；不是全调度枚举。全部运算Fraction/整数，Python3.12.14，无随机容差。本批不重跑已充分同SHA旧程序，亦不补造历史退出码。

同期半单位结果并入条件块稿后整文件SHA改8cf637…，审查记录§4承重cut逐字不变，不把新§3a追溯纳入旧初审。后来稀疏条件配置的四机交集、逐机两倍跨度三半结果也只记录主研究者实际读后的关系：前者合同更强而不同，后者行跨度额外假设在本族k无界时不满足。它们均不改多行代码/Claim。当前 row_count_escape_gap 最终a075…另含(MP)§7，不属于本原初审查的独立发现范围。

本页吸收的是审查的独有版本、先验、论证分支和有限证据，与[既有全局基数审查](全局基数与逐行均匀相关读出边界有限审查--审查.md)互补，不再命名一次主定理。一般近似、共同条件分布、条件LP、统一ε、全球新颖性、外部评审及论文价值均未认证；UM-TARGET-v1仍OPEN。
'''))
paths.append(put('审查','完整单机配置审查的均匀装配与共同基点范围',r'''
---
id: machine-config-review-uniform-assembly-and-base-scope
kind: review
type_tag: 审查
title: 完整单机配置审查的均匀装配与共同基点范围
status: integrated
truth_status: reviewed-general-extension-proof-with-finite-audit-and-prior-disclosure
review_level: full-primary-review-read-and-frozen-section-comparison
summary: 保存非零信息独立审查的真实顺序、均匀完整配置装配、错误拒绝合同纠正、共同base一阶矩解释和冻结节号链。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/machine_config_probe_review.md
---

# 实际先验与所审合同

[原审查](../../tools/evidence/capacity-half-slot-and-row-reviews/original/machine_config_probe_review.md) 9057字节，SHA-256 `27dcb95d02dc0935892a2cae7801ae7f638cf0fe2f41930c3239a6da8254036d`。先收到两树/路径终端候选时，审查者未读草案就报告条件质量沿树衰减与整数共享 z 碰撞的区别；随后读既有 diluted_sink 稿、公屏168/173，核路径修复。临时深树代码未登记为本次规范资产。

转向紧凑族后，审查者已读既有构造并收到候选配方，再独立推出全局 X 槽总量和每块真实单位需求、攻击所有类型、编写不导入主生成器的完整证书程序；最后才读新增证明。不能称不知道候选配方的独立发现，亦不能把先前路径临时代码当成本源正式实现。

族仍为 k≥2、N=2k²、G=N−2k：X在自身V/全G上1；k个Z在自身V上1/k、同块k+1台R上1；k个Y在R上1、共享z上1/k。原始完整配置 LP 要每机分布归一、每个正质量配置真实负载≤1、每任务总覆盖恰1。被审性质为

\[
\forall i\ \forall C\in\mathcal C_i(1)\ \exists y^{i,C}:\quad
 y^{i,C}\in\mathrm{CONFIG}(1),\quad y^{i,C}_{i,C}=1.
\]

不同(i,C)分别用不同完整 y，不提供同一base、条件恒等式、跨探针兼容、SA/LS联合分布，也未证明每个延伸共同满足GPC₂或嵌套过滤。整数OPT=2−1/k：低于该值迫≥2k个中心收X、每块≥2Z外送、≥1Y去z，z负载≥2矛盾；每活跃块只外送1Z则达到上界。统一 gap 上确界上界另用标准 ST≤2T，不是有限实验推出。

# 独立重构的真实配置装配

令 a_b 为 X_b 在 V_b 的边际，普通 V 以 a_b 选X、1−a_b 选全部Z。每个Z的R需求为a_b。X的总剩余需求Σ(1−a_b)必须由G个单位槽承接，所以Σa_b≥2k；G一台空置改为≥2k+1。固定某台G接X_a时先扣掉该任务的单位需求。

若本块有e_b个Y整项送z，普通块的R总需求为 k+ka_b−e_b，须≤k+1。关键是所有本块Y/Z都与全部R完全相邻：给q台未固定R、每任务需求d_j∈[0,1]且D=Σd_j≤q，在每台R放单项配置{j}权d_j/q、空配置权1−D/q。归一、容量及每任务覆盖同时成立。固定R先扣掉被固定任务需求并移除该机器，再均匀装配；G同法。这里构造的是完整配置，不把负载点冒充配置点，也不把分数拆分解释成整数任务可拆。

# 所有本地配置与逐类攻击

未说明的普通块取a=1/k。中心合法配置只有{X}或任意Z子集，G只有空或单X，R只有空或单Y/Z，z为任意≤k个Y，所以以下穷尽全部类型。

| pin | a的修改及固定项 | z和真实R需求 |
|---|---|---|
| V_a={X_a} | a_a=1，其余(2k−1)/(N−1)<1/k；和2k | 本块kZ外送，送k−1Y去z，R总量k+1；其他块ka<1无需逃逸 |
| V_a为r个Z，0≤r≤k | a_a=0，确定保该子集；另b取2/k，其余1/k；和2k | 本块外送d=k−r个Z，送max(d−1,0)个Y；b块再送1Y；总≤k。空中心边界恰用满z |
| G={X_a} | a_a=0、另b取2/k；固定G完整承担X_a | b送1Y；扣X_a后余X需求恰G−1 |
| G空 | k个块取2/k、其余1/k；和2k+1 | 这k块各送1Y，z恰满；余X需求G−1 |
| R_(a,ℓ)空/单Y | a_a=0、中心保全Z；另b取2/k | b送1Y；a仅kY，可避空R或先扣固定Y再装配 |
| R_(a,ℓ)单Z | 同前但中心只保除该Z外的全部Z | 固定Z占该R，kY用其余kR；不能由a_a=0误推该指定Z仍留中心 |
| z=C，任意≤kY | 基线全部a=1/k，z确定取C | 从原R配置删去C中的Y质量转空，其他覆盖不变 |

k=2时G=4、G−1>0且2/k=1，所有配方仍合法；(2k−1)/(N−1)<1/k等价k>1。不同pin只各借一次z，不要求它们同用一个逃逸集合。给显式(i,C)，均匀实现正支持O(GN+Nk²)=O(k⁴)，系数分母由k、N−1、G或G−1、k+1等多项式量相乘，位长O(log k)。主稿贪心填槽是另一合法装配。证书生成多项式不意味着枚举z全部配置或通用CONFIG求解多项式。

# 审查纠正的拒绝语义与共同base解释

(MP)不是一般T整数可行的必要条件：可行实例也可能有不能延伸的本地C。失败探针只可安全删除该C——若某T调度使用C，其Dirac配置点就会延伸C，因此不存在这样的调度。不能因任意一个失败C拒绝整个目标。本族全部C起初均可延伸，故反复删无延伸配置没有第一次删除。这个表述异议在冻结7.1（原6.1）已纠正。

共同base增量同样严格：条件V_a={X_a}时，该块kZ+kY的2k单位需求面对k+1个R槽，Y去z的总边际≥k−1。若各条件点来自同一base，且至少对这些逃逸坐标满足按V配置的混合恒等式，非负性给 base 的该块Y逃逸≥a_a(k−1)。全局X容量给Σa_a≥2k，故z负载≥(k−1)Σa_a/k≥2(k−1)>1，矛盾。只需这些一阶坐标恒等式，不必先假设完整全局分布；它是已有条件块cut机制的直接解释，不另冒充一个新Claim。没有共同base时每个完整延伸仍真实可行，两者没有矛盾。

原审查另称用Fraction核k2..128的该共同base计数式及反算；该人工附加计算的原命令/输出未保存在本批，保留为原文历史叙述，不混同规范独立程序的127个scalar检查。实际代码的scalar主检查是配方/保留Z/容量及严格界，不含一条显式2(k−1)>1断言。

# 完整运行与真实独立边界

独立代码 SHA `9f31076a1adb4c665dad2af1f3f723017aae8e8cf43a4c20edece3dcff3aff89`，只标准库、不导入主程序。历史命令 `python3 tests/audits/unrelated_machines/compact_config_probe_independent.py`，结果见[冻结JSON](../../tools/evidence/capacity-half-slot-and-row-reviews/historical-runs/compact_config_probe_audit.json)的 independent 字段，Python3.12.14、Fraction无容差。

k2的实际稀疏P有37机40任务，全部333个本地配置逐个生成完整y，V/G/R/z分型40/36/120/137；逐机核合法支撑、真实负载、归一，逐任务恰覆盖1，固定配置权1。k3..8仅一个代表V的全部Z子集/X、代表G空/X、代表R空/Y/Z以及seed20261016每种大小0..k的z子集；完整扩展数为18/27/44/77/142/271，最大权位长7/8/8/9/10/11。k2最大位长5。另有k2..128共127个标量参数检查，不展开这些完整P。

第一次审计有空sum返回int、后续除法变float的实现错误，改Fraction起始值后完整重跑通过。旧错版原字节未冻结，不能声称本批重现了它；它不是数学反例。主实现 SHA `fff7336087f055a399ffdc45b633304ba1b65738d0006c7628c63540eed46910` 原审查仅核hash，**没有逐行审主实现**。本次/前批清洗者实际读主实现不能倒填旧审查先验，也不能把主实现run归为该独立审查的个人运行。主run独有951/2907查询等由自己的冻结字段另承担。

# 精确版本链及并行数学归属

| 历史版本 | 实际变化/覆盖 |
|---|---|
| 63fa15647111e5300cf63f0c2057c969ddf6a917f0ce1c213bf521c96514f859 | 初审新增原§6及其构造/整数/基线依赖 |
| 52b1987db1d2c91687e5cef3157173ece7b9f33250f42cc8190770459105b1d0 | 再审共同base一阶矩增量，完整受审推导身份 |
| 95f4873702d73ca8b76d7b1aab4d9eb27b5f5ddee2bb683830a5ae7cf08d5db3 | 为同行多行§6留位，仅将本节改号§7 |
| 028314a66eb613a1f132a14cc745c3f9a2a070317cceb8e82fe1f348bcad7e37 | 合入同行9a64903/4c810f4多行§6，§7字节不变 |
| a075bf8984891b4c557aa491329f087a3b0d539e5de2babe6bec2e3f7b83aa1e | 首段导航改指§7，当前冻结整稿 |

当前§7完整字节 SHA `8037f85bb3b67b6a9f57553d36367388ec4d0e2597a5b348ee5f5828eaf0c2dc` 与原冻结字段精确相同，本批提取实际节并验证。旧整稿各中间版本仅有原审查记录的SHA，未凭空制造对应字节。同行多行§6不在本独立证明范围；主研究者另读其构造/尖锐反例/追加审查，不能把并行合稿当成本审查重做了同行数学。

本页保留的是独有审查顺序、均匀装配证明、异议纠正和版本边界，与完整原实现资源互补，不再把已吸收的(MP)结论立一次新定理。未认证全球新颖性、论文价值、外审、一般近似、共同条件分布或完整层级；UM-TARGET-v1仍OPEN。
'''))
(stage/'cleanup/workspaces/Boss4/r3-capacity-half-slot-and-row-reviews/object-paths.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'objects':paths},ensure_ascii=False))
