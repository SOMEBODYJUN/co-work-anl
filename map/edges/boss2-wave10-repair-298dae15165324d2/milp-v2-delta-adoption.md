# fe146 的 MILP v2 定向采用与六资产保留

本记录服务 `boss2-wave10-repair-298dae15165324d2`，只处理已完成包 `customer-attraction-3a-3a-fe146ca92b8502da` 中唯一变版的登记摘要。当前任务定义 pin 为 `c49389c36ef7a4d9af547203a875ca473ab88a2b4fa02d3094cf6037de0a6715`；本地任务仍显示 owner Boss2、state claimed、claim request `9e5f62dfbc1445bcbdeaa80b2664b316`。这些是定向审读输入，不替代 Boss 的远端认领、checkpoint 或 done 确认。

## 实读、继承与精确来源

本轮 fresh formal worker 完整重读当前 MILP v2 登记合同、下列 MILP 正文、共同模型及冻结 `full_history_milp.py` 全文；源码只读，不 import 或运行该科学程序。另实读当前其余 18 对象的数学陈述、模型、量词、前提、范围与异议，完整旧 receipt 的 11 项 coverage、六份关系 JSON 的全部数学 payload 与绑定字段，并读独立 3D 报告的读取范围、六边数学重构、三个 isolated 判断、元数据更正和继承建议。

原包其余完整证明与原始历史证据的阅读，由旧 worker 的正式收据明确继承，不冒称本轮重新逐份全文审读。旧收据记录其对 11 core/8 read 的完整成熟证明阅读，及对 698 原记录、2801 原动作、大数组和旧自动机的有限继承边界。本轮保留这些原边界：没有重新认证这些原数组或执行 LP、MILP、SPE、全集、矩阵、秩扫描、审计或历史重放；新科学程序运行数为 0。

精确输入：

| 输入 | SHA256 |
| --- | --- |
| `map/receipts/customer-attraction-3a-3a-fe146ca92b8502da.json` | `b978d0c6d6a13557c40d662dede310e9647846a5811215533713f9270900c749` |
| `research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/fe146-delta-3d-review.json` | `a408a7c9ecd377280e55e76cbecb020af6e9a3910c9ccec6252b2140cf941363` |
| `research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/milp-threshold-v2-correction.json` | `5c64a722d0b1c4a3b083cf8c11661f05ba16a367e666b9a6a73b2d8c55d69a3e` |
| `archives/customer-attraction/state/程序/目标终局联合重数MILP的压缩见证与固定根记录--程序.md` | `c49a6a7ffeb62173aabc5d1c2cda3126bb67ffecad9cf65f921c415b07466a3f` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/tools/evidence/full-history-milp-and-fixed-root-status-five-primary/original/c5806a0a4985de93a5cb/research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/full_history_milp.py` | `30c569b6e9bf09fb81bbf719b8c53c50c9410b240898880fdb483ac4b5932144` |

当前 MILP object 为 `customer-attraction/target-terminal-joint-mass-milp-compressed-witness-and-fixed-root-records`，v2 registration pin `1498397d3a8b15ccd4f69d03c81c222a1561faba76f398eb2e94729b85fc46e7`。旧 v1 pin 是 `e0582d56619d2eb06da9a548fb08826798142863d5bdf2f3e0a954312cf86c71`。两个任务的 11 core/8 read 列表相同；独立重算的 19 个当前 pin 全与新任务一致，相对旧任务仅此一项改变。对这 19 对象的 82 个 body/evidence 引用（38 个不同文件）只作字节/section 完整性验证，全部通过；这项结构检查不扩张本轮人工全文阅读声明。

## 每个计数只有一个共享门槛

模型为有限单位客户、有限非空共同标签目录及任意覆盖映射、单位提供者和全部有序历史上的纯 SPE。弱平局、重复行动、同覆盖异标签、空覆盖和零客户均保留。非负实重数是线性延拓；有理点清分母后才对应有限单位客户。固定正福利请求根终局 q⁰ 后归一 W(q⁰)=1。

令 K={k≥0:|k|<m}，C(k)={q≥k:|q|=m}。对每个 (k,q)，A(k,q)=Σ_a y(k,q,a)≤1；开启 A=1 时选唯一动作 a，且非末层必须有 A(k+e_a,q)=1。每个非末层 (k,b) 另选唯一 x(k,b,d)=1，d∈C(k+e_b)，并要求 A(k+e_b,d)=1。

正文和源码都只为每个 k 创建一个 T_k∈[0,m]，供该计数的所有 b 与所有开启请求 q 共同使用。选中 y 时，u_a(q)≥T_k；每个选中敌对孩子满足 T_k≥u_b(d)；末层直接对每个合法 b 要求 T_k≥u_b(k+e_b)。源码 `self.T` 的键只有 k，所有选中动作下界、非末层孩子上界、末层比较与合法强化 L_b(k) 都写入同一 `self.T[k]`。

因此旧登记的 T(k,b) 不是冻结程序的实际变量索引。v2 修正这一摘要，不改变正文、源码、可行性、收益、证书或数值记录。若另建逐 b 门槛并让每个当前动作比较全部 b，可给等价冗余表示，但这不是本对象的原系统。

## 两个方向的完整历史存在性

给定重数 r，令 R(k) 为保留全部有序历史与所有平局后的可信终局全集。对每个 k,b，从非空有限集 R(k+e_b) 选使 u_b 最小的孩子 d(k,b)，再令

T_k = max_b min_{d∈R(k+e_b)} u_b(d) = max_b u_b(d(k,b))。

若 q∈R(k)，取一份实现 q 的真实子 SPE，其当前动作是 a。原 IC 对每个 b 的实际可信孩子收益成立，而该收益至少是相应 R(k+e_b) 上的最小值；故 u_a(q) 不低于全部这些最小值，因而 u_a(q)≥T_k。该动作子请求 q 也在 R(k+e_a) 中。所以非根所有可信请求可以同时开启，共享每个 (k,b) 的最低孩子与同一 T_k。根只开启指定 q⁰；如固定首动作，则须使用确能以该首动作实现 q⁰ 的根见证。没有要求同计数不同请求的动作一致。

反向，给定整数 y/x 可行见证，在每个原有序历史 h、计数 k 与当前请求 q 处选其唯一 y 动作 a；h+a 沿请求 q 继续，其余 h+b 沿所选敌对孩子 d(k,b) 继续；末层用唯一终局。深度严格增加，所有动作孩子均被开启依赖支持。当前真实收益至少共同 T_k，每个真正偏离孩子收益至多该 T_k，所以逐节点 IC 成立；对子树归纳得到完整有序历史纯 SPE，根终局为 q⁰。相同计数可以有不同请求并选择不同动作，故该压缩不要求原 σ 是计数统一策略，也不承诺逐动作保存某份给定 σ 的非极小离轨分支。

根偏离任意主题 b 至少得 s_b/m，实际根收益≤W=1，故 s_b≤m。非负质量给每 r_B≤m、被求值收益≤m；上面定义的 T_k 也在 [0,m]。未选 y/x 的 big-M=m 约束因此自动成立。L_b(k)=Σ_{B∋b}r_B/[k(B)+m−|k|] 是每个真实 b 后继的收益下界，强化整数见证时冗余而可紧化分数松弛，不能替代全部可信孩子。W=0 的 SPE 使全部主题覆盖为零，是单独平凡边界。

阈值数 N=|K|=binom(m+p−1,p)；m=5、p=7 时 N=330，客户变量 127、连续变量 127+330=457，二元 31850、总量 32307，全与原记录一致。此处只核正文公式和源码索引，不新建或运行模型。

## 维持 isolated 的具体比较

MILP 联合选择质量和存在性目标见证；固定完整策略锥先固定全有序 σ，再在线性 IC 锥内优化质量。这两个已登记整句在本包中不新增完整蕴含。源码提取动作后进入固定锥重新优化 r，所得精确可行点不保证保留原 MILP 质量向量、minimum 数值或联合最优值。两份五人运行均无 incumbent 的时限状态，13 个历史目标自测及 5/3 提取回归也没有普遍不可行、一般 half 或新效率定理的结论。本轮仍为 8 linked、3 isolated-after-review；其中 MILP 采用 v2 pin，其余结论继承旧收据。

本地当前 registry 的 2234 条 canonical 关系按 source_ids/target_ids 逐条检查，MILP incident edge 数为 0。六项既有资产均未以 MILP 为端点，因此本次元数据修正不产生边重绑或额外关系。

## 六项资产逐项原字节保留

下表六份资产均重新核字节 SHA、endpoint_pins、evidence_pins、review_digest 和 current canonical membership，全部相符。其完整 payload 已在本轮实读，原证明的额外全文阅读明确由旧收据与独立 3D 报告继承。没有修改、重绑或复制其中任何一边。

| 原资产路径 | 原 SHA256 | 保留范围 |
| --- | --- | --- |
| `map/edges/customer-attraction-3a-3a-fe146ca92b8502da/suffix-refund-to-causal-full-replay.json` | `daffc405a21a96038af6719d8b0b59442fdec6734738d10a5cd939498089bd2e` | whole causal plan；较早偏离后虚拟 σ_i 递归重选，τ_i 不要求 SPE；D 是被至少两人覆盖的实际客户数，每个客户全有向退款为 1，不是 Σ(c−1)。 |
| `map/edges/customer-attraction-3a-3a-fe146ca92b8502da/credible-floor-to-row3-necessary-constraints.json` | `47cc87a8da58a8c607479e1ab97abbfbd67a71315de15fdc0a92500910dac158` | 只交 ROW3 必要约束 step；保 max_j min_{完整 BR}、真实 K^S 历史、F_i(S_j)−F_i(K^S_ij) 与旧人利润 B_i−B_0；ROW3 仍 open。 |
| `map/edges/boss5-474257b8-customer203-repair-repair-092c774a6ef3a3fe/two-pruning-registrations-same-support-welfare-jump.json` | `d67f195e029f846617f5b3ed512e2c5182677f2b6138a6d7ca31b01ed2f4ed3d` | 同一 A/B/C/D 族删 B 的根命题等价；私有 a_i 和 d 补唯一最优支持；不合并更强后缀分类。 |
| `map/edges/customer-attraction-3a-3a-87d9e56f176d1d6d/off-support-slot-budget-to-actual-cap.json` | `ccd28a05cc3a2449f1f4d071479730ff773650b37175c08027413a4da87bceb4` | 正离轨预算排 actual-only 十二槽分布的 step；矩阵值 3 和完整目录 cap≤5/2 各有独立义务，6/25 的 T-only 取等不满足全部查询。 |
| `map/edges/customer-attraction-3a-3a-51c7cfc720bbb676/cap-cross-cell-qualification.json` | `21960cc4c99ce2283dcda504eae2bf4c806b2d2e8d55f024547f8ce131f7b4dc` | D_all 含实际行动的替代尾；跨格资格 step 不生产低价真尾、不支付 TAIL 或深层祖先条件。 |
| `map/edges/boss1-wave6-rank-scope-repair-880961ce1b4f6ef3/empty-background-rank-three-pair-slice.json` | `e6e8f81dc2b5a174727a0f11209f008f9c8b97ad9cedf1395e935eed884c79ae` | D空、M3 的 signed 等式完整核；目标局部质量反演和非负 iff 已另证，不是开放缺口；不扩张到全目录拼合或任意实质量的有限单位实现。 |

两个任务均无声明的 follow-up overlap。本轮比较放在 coverage 与 `completed_in_scope_comparisons`，`closed_overlaps` 保持空；没有新增科学 follow-up。本记录是定向采用说明，不是数学端点或新逻辑边。
