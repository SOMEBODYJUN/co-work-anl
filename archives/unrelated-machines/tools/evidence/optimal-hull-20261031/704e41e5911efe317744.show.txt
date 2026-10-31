# 真实最优凸包长链局部缺口的冻结正文与实现独立审查

## 审查身份、冻结对象与结论

审查者：内部独立子研究者 `chain_review`。本审查由精确 statement-first 攻击开始：在阅读构造前独立重构了“根过载沿链传播、后缀预处理可能恶化 lex”的瓶颈，并指出最优凸包中的大任务基数约束会阻止简单的“两件大任务叠加”构造。随后阅读实际构造、独立推导并穷举，最后才阅读本次正式冻结正文和实现。

实际审查的精确 Claim 为 `UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1`。正式对象为：

- 正文 `research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md`，完整阅读第10节；文件 SHA256 为 `ca07779d4d5bc5a8c8bc268a42dd13ef8766a744b42bbcf259deb9774d559feb`。
- 规范实现 `tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py`，完整阅读并实际重跑；SHA256 为 `98f52cbb67f2b5ee4994414c29b44eac80da0f92e4aa91710b3531249d1ded68`。
- `potential_attack` 的最终 canonical 独立实现 `tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py` 及 `evidence/runs/unrelated_machines/optimal_hull_long_chain_independent.json`，完整阅读并重跑；脚本 SHA256 为 `e0a4d4f99396cdfa42a07dac191431fc8c439f76b033a1df555ab3a16f573149`，冻结 JSON SHA256 为 `f6c885a6262ba3974a5918ac1c1f11e5528cb0ca5a42736d4aeedc68388f35d9`。

最终 canonical 代码及证据指针如下，均实际读取并核对；这里没有用旧 scratch hash 代替最终文件 hash。

| 角色 | 最终仓库路径 | SHA256 |
|---|---|---|
| 规范代码 | `tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py` | `98f52cbb67f2b5ee4994414c29b44eac80da0f92e4aa91710b3531249d1ded68` |
| 独立代码 | `tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py` | `e0a4d4f99396cdfa42a07dac191431fc8c439f76b033a1df555ab3a16f573149` |
| 规范冻结运行 | `evidence/runs/unrelated_machines/optimal_hull_long_chain_audit.json` | `e4b15778a93f79c026fe7c94b69e95d8ecd993ebf4257da8d9c2d38668826a04` |
| 独立冻结运行 | `evidence/runs/unrelated_machines/optimal_hull_long_chain_independent.json` | `f6c885a6262ba3974a5918ac1c1f11e5528cb0ca5a42736d4aeedc68388f35d9` |

结论：该冻结正文第10节的精确数学陈述、承重证明和所审实现通过本次内部独立审查。没有发现仍成立的 fatal objection。结论依赖下面逐项重构的证明，不依赖有限核验或其他研究者赞同。此次没有重新审查第1–9节的全部旧命题，没有认证全球新颖性、独立论文价值或外部同行评审，也没有证明主目标。

## 精确陈述与范围复核

正文保持了量词 `∀整数 k≥3,d≥1，∃显式 P,x,σ`。输入有限处理时间均为正有理数，每件任务恰好两台可用机器，属于原 UM 模型的合法子族。两个最优调度的完整凸分解是输入证书的一部分，不是由若干边际检验冒充的最优凸包归属。

标准 ST 排序按处理时间非增，tiny 的平局顺序任意固定。正文允许平局次序改变被激活链的标签，但所有结论对每种固定次序成立。采用正长度区间交的 ST 支撑边：仅端点接触不能形成边。第10.3节的严格正交长和首槽陈述与此一致。

实际重分配 τ 不受原槽图限制。H 统计归属变化的任务；V(H) 是这些任务的旧、新 owner 端点并集。因此下界涵盖任意合法实际重分配，包括若干机器负载变化互相抵消的情况，而不是只数净负载变化机器。

对于机器预算 r 和任意 ε>0，可取 d+2>r 且 k>1/ε，使初始比值严格大于 2−ε，同时不存在预算内的严格 lex 下降。这是固定坏输出上的局部邻域限制。正文没有据此声称排除一般算法、其他初始化、最优凸分量的直接返回或 weak-makespan 单调路径。

## 承重证明的独立重构

### 最优凸包和输入规模

记 δ=1/k、a=1−1/(2k)、D=d+2k−1。S0、S1 均逐机负载至多1；macro 在两个可用端点的处理时间都为1，所以每个合法调度的最大负载至少1。故 OPT=1，S0、S1 确为最优。

x=δS0+(1−δ)S1 的每条可用边质量均正。每台机器在两个调度中的任务集合直接给出支持于负载不超过1配置的分布，故配置可行性没有隐藏问题。这里不沿用第7节旧分数点违反大任务基数约束的异议。

对象计数 m=kd+k+D+2、n=m−1 正确。因为 k≥3,d≥1，计数为 O(kd+k)；若输出稠密矩阵，正文明确按实际 mn 计。数字编码位长为 O(log k)。这只是显式反例族和路径构造的规模结论，不含求解一般 UM 实例的声明。

### ST 可实现性及所有最低成本输出

root 总分数质量为 k−1+1/k，恰有 k 个非空槽。macro 的区间与排序首 tiny 的区间共同恰好填满槽0，二者均不能进入其他槽。其余排序第 j 个 tiny 与槽 j 有正长度交，因此正文给出的 σ 存在合法槽注入。

每台链 home 的总分数质量恰为1。rootjob 一旦离根，链首唯一槽被占，迫使自有任务下传，逐台递推强制整链下传。未激活链只可能额外下传某个后缀；每个这样的任务使总处理时间增加 1−a>0。

W0 在这里仅为全 home 实际分配的成本参照，并未被假装成 ST 可实现分配。至少一个 rootjob 必离根。每次 tiny 激活增加

`c_t=1−δ+d(1−a)=(d+2k−2)/(2k)>0`；

macro 激活增加

`c_b=D(1−a)=c_t+1/(2k)>c_t`。

已构造 σ 的总成本恰为 W0+c_t。因此所有最低成本 cover matching 都恰激活一条 tiny 链、无额外后缀。macro 留根以后，首槽冲突迫使离根 tiny 正是排序首 tiny。结论是唯一实际机器分配；一般证明不需要槽级匹配唯一。

### 任意实际重分配的精确支持下界

设 B=2−δ。严格 lex 改善首先蕴含新最大负载不超过 B。关键不等式为 1+a=2−δ/2>B。由于每件链任务只有 home 和下一台两个端点，在 Cmax≤B 的任意实际分配中，下传比特只能形成后缀；rootjob 离根则强制整条链下传。

若没有新的原 rootjob 离根，则原 active tiny 不能返回 root，否则 root 负载变成2；故旧 active 链保持完全下传。每条其他链或者不变，或者迁移一个非空后缀。长度 l 的后缀将 l 个负载 a 和一个0换成 l 个1和一个0；多个后缀组合也只会增加负载1的数量、减少 a 的数量，保持原 root 峰值 B 和零的数量。因此排序向量严格变大，或完全不变；不能严格 lex 改善。

所以每个严格 lex 改善都新激活至少一条链。该链在 σ 中完全 home，τ 中 rootjob 与全部链任务都改变 owner。tiny 链至少贡献 d+1 件任务及 root、d 个不同 home、sink 共 d+2 台机器；macro 链更长。证明并非只展示一条长路径，而是覆盖所有合法 τ。

另激活一条 tiny 链并保持原 active 链，恰改变 d+1 件任务及 d+2 台机器。root 新负载为2−2/k>1，其余负载至多1；每个源只迁出一件任务。因此两项支持下界均精确达到。

### weak Cmax 路径的正向边界

第10.5节准确给出本族的修复路径：对一条 inactive tiny 链，从 sink 端逆序逐件下传，最后把 root 上该 tiny 迁入链首。每步只涉及两个任务端点；前 d 步的全局最大负载保持 B，但降序 lex 向量变坏；最后一步最大负载下降 δ。

从 σ 继续激活其余 tiny 链，(k−1)(d+1) 个单任务步骤得到 S0，整个过程中 Cmax 不增加。故本族确实有容易的 weak-makespan 单调修复，不是只因为未分析这种算法而保留可能性。正文明确写入这一边界，避免把严格 lex 局部搜索限制偷换为 Cmax 非增路径限制。

## 实现阅读、实际重跑与有限覆盖

规范实现全部使用 Fraction。阅读覆盖：实例及两调度构造、分数边际、负载、正长度槽交、一般增广槽注入、精确残量最短路最低成本匹配、精确修复支持计数及 weak-makespan 单任务路径。

实际运行：

`python3 tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py > /workspace/scratch/189af9cda7c4/optimal_hull_chain_normative_rereview.json`

结果通过。最低成本流实际覆盖 k=3,...,8 与 d=1,...,4 的24个案例；另有 (3,20)、(16,1)、(32,2) 三个构造/修复边界案例，其 `mincost_optimized=false`，没有将其误报为最低成本流核验。五个非法参数测试均拒绝。重跑输出 SHA256 为 `e4b15778a93f79c026fe7c94b69e95d8ecd993ebf4257da8d9c2d38668826a04`。

规范最低成本流核验只返回一个最优匹配，不能单靠它证明所有最低成本输出同一；该全称部分来自正文的严格成本分解。规范有限参数核验也不能证明一般支持下界。

`potential_attack` 的独立脚本不导入规范构造或核心函数；使用带标签完整二进制 owner 枚举、整数缩放负载、Fraction 槽区间及逐机增广匹配。审查先读取并重跑了 clone 外原版，随后实际完整读取并重跑最终 canonical 文件，核对 canonical 相对原版仅增加 shebang 和一行中文 docstring；最终重跑 JSON 与最终 canonical 冻结 JSON 相同。原版脚本/JSON 的旧 hash 仅是审查历史，分别为 `c129810df9f73f33110e2d5e72d8a3c1063c94522cef0d2b82ba3b9b82de83fb` 和 `3c828ce92c751ca526422376a7bd22187bd596d3ff83f0dafa101e47b1c1d9cd`，不作为最终 canonical 指针。它完整检查下面三个有限实例的全部合法分配，并获得下表结果。

审查者还保存并重跑第三份独立脚本 `optimal_hull_chain_reviewer_enumeration.py`：任务编号采用“每个 rootjob 后立即放本链任务”的交错方式，区别于前两份脚本的 rootjobs 集中编号；从两份调度重建 x 和槽区间，对每个机器的槽匹配使用子集 DP 计数。该脚本既不导入前两份代码，也不使用链强迫或成本公式来判定匹配可实现性。它直接统计实际 cover matching，而不仅是 owner 分配；三个实例的最小 cover matching 数均为1。这是有限案例中的更强观察，不提升成一般唯一槽匹配结论。

| (k,d) | 完整合法分配数 | OPT | 初始 Cmax | 严格 lex 改善分配数 | 最小改变任务数 | 最小参与机数 | 最低槽总成本 |
|---|---:|---:|---:|---:|---:|---:|---:|
| (3,1) | 8192 | 1 | 5/3 | 76 | 2 | 3 | 31/3 |
| (3,2) | 131072 | 1 | 5/3 | 144 | 3 | 4 | 83/6 |
| (4,1) | 131072 | 1 | 7/4 | 378 | 2 | 3 | 107/8 |

每份完整枚举审计实际覆盖270336个分配。审查者独立脚本 SHA256 为 `5561827f8cfed3db564d84f36bff8aafa9402d0ae22b4cd202526c202d250f7f`，结果 `optimal_hull_chain_reviewer_enumeration.json` SHA256 为 `2984227db80d29eddf108208f61add3b2e690bf4be67d61a249756cce51ec283`。实际命令为：

`python3 tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py > /workspace/scratch/189af9cda7c4/optimal_hull_chain_canonical_independent_rereview.json`

`python3 optimal_hull_chain_reviewer_enumeration.py > optimal_hull_chain_reviewer_enumeration.json`

运行环境均为 Python 3.12.14；负载采用2k整数缩放，槽区间采用 Fraction，无浮点误差、随机 seed 或数值容差。有限完整枚举不是所有 k,d 的一般证明。

## 未解异议与本审查没有覆盖的内容

本次精确 Claim 内没有仍成立的实质异议。此前提出的“最优凸包大任务基数约束”“只证 Cmax 不降而漏 lex 改善”“参与机器计数漏掉 sink/新旧端点”“最低成本只核验某个输出”“中性 Cmax 预处理可能修复”均已分别由构造、全分配分类、端点并集、严格成本分解及第10.5节正向路径处理。

仍未完成的是全球新颖性认证、外部同行评审和一般近似算法；这些不是本精确局部 Claim 的未解证明义务。此次也未审查根地图和所有账本的登记一致性、原始文献来源完整性、Git 推送状态或其他旧正文的全部证明。

本审查文件在 clone 外生成，未修改正文、账本或公屏，未提交 Git。一般结论的采用范围以正文第10节精确陈述为准；任何正文 hash 改变都应重新界定复核范围。

## 持久化的审查者补充复现指针

上述第三份独立脚本与输出已按原字节保存为 `tests/audits/unrelated_machines/optimal_hull_long_chain_reviewer.py` 与 `evidence/runs/unrelated_machines/optimal_hull_long_chain_reviewer.json`，SHA256与上文完全一致。只是将实际审查的 scratch 产物归入规范目录，没有改写脚本、冻结结果或扩大审查范围。
