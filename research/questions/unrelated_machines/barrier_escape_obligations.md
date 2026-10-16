# 跨过配置间隙后仍须闭合的算法义务

唯一主目标为UM-TARGET-v1；精确模型与量词在[账本](../../unrelated_machines/CLAIMS.md)。此页是OPEN proof obligations，不是候选定理。

| 义务 | 需要给出的可检验内容 | 最便宜的反驳测试 |
| --- | --- | --- |
| 新下界/信息 | 定义B(P)、证明B≤OPT，并说明为何已知两树配置证书不能把它压到原T | 在同一两树族符号推导B；若B仍只等于配置值，不能仅据此保证统一改善 |
| 具体分配 | 每任务恰一台可用机器；负载按其真实p_ij相加；零最优值也满足 | 零任务、全零、只有一条有限边、极大有理数/分母和两端强非对称 |
| 全局负载 | 对全部机器同时成立，而非平均、期望局部或去掉少数任务 | 枚举小反例与两个瓶颈机器同时满载场景 |
| 统一余量 | 可核验ε>0与实例规模、尺寸比、精度和m无关 | 令m、树高、大小比增大，检查余量是否趋零 |
| 位多项式构造 | 精确变量位数、LP/oracle误差、搜索分支、循环次数与输出编码 | 不接受“每步多项式所以总时间多项式”、固定m或指数配置全列举 |
| 强化模型的求解 | 分离/近似分离及误差预算不会吞掉改善常数 | 将oracle误差逐项代回最终界；不能假设NP难oracle免费 |
| 若改走困难性 | 另定ρ、复杂度假设、完整归约和yes/no gap | 一个ρ<2的困难性下界本身不排所有小ε改善，勿与算法目标混同 |

无正式候选时保持本页精简。新证据出现后保存精确新Claim版本和真实失败机制，不能把本义务清单当作唯一允许的研究路线。

已新增[固定机器联合投影的长链障碍](../../current/unrelated_machines/long_path_coalition_gap.md)：每个coalition分别存在、只共享单机边际仍不足。完整三机交叠相容性在该树宽2族上精确；下一候选需说明如何保留跨见证的多机信息，并处理一般图的复杂度。不能把高围长误认作计算困难性，也不能用普通子问题makespan近似自动代替边界最小负载oracle。

具体已知限制：UM-CARDINALITY-CLOSURE-v1和二阶bundle cut能修原VW，却被任务细分绕过，完整pair coupling仍gap2。后续候选须给跨capacity-one中间机的信息消去/保持，且不能假设精确knapsack/configuration oracle免费。证明及真实范围见[现行正文](../../current/unrelated_machines/bundle_coupling_subdivision_barrier.md)。

## 已收窄的共同匹配容量义务

已证边界见[共同大边选择与条件块切面](../../current/unrelated_machines/joint_matching_completion_and_block_cuts.md)。大小分界固定原T/2。要攻主目标的一条充分路线是：选一个共同big匹配H，使未选任务有small分数解，总负载≤(1+δ)T；固定δ<1/2再接槽舍入给(3/2+δ)T。精确选择对每固定有理δ<1/3已NP完全，即使N空/唯一small，所以不能继续把低余量exact接口当免费oracle；旧归约未排该区间；正文新§3a的半单位身份现覆盖全部δ<1/2。

需要判别的具体问题已改变：上述共同见证的总确定性位多项式保证构造，在任何固定δ<1/2下均受P≠NP排除；不能继续作为未解正面义务。能否利用比负载加支撑max更精确的联合槽损失，或给可分离、可舍入的条件块强化？共享z族已被随B重算的末簇cut完全识别，但这只是专用族的有效接口。一般多small端、长链相关性、oracle精度、输出调度和目标搜索仍须同时闭合。

生成树pair提取也须证明非树任务残量仍可行；[五机真实分布反例](../../current/unrelated_machines/tree_markov_completion.md)否定“任意支持态+冻结树任务”合同。允许迁移和有信息择态仍是开放接口，不能据本例宣布这些路线失败。

消元路线新增准确接口：极小超载星可保T并从任意B逆恢复max(B,T)，但紧凑容量一族无触发点。q普通任务保全部残余profile的压缩已被boss4反驳；需要保任务身份的加权匹配或更强耦合。见[现行自足正文](../../current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md)，不将此表示障碍扩大到主目标。


当前条件LP路线应先区分：普通逐边LST（已被UM-DILUTED-SINK-PROBE-GAP-v1排除相对阈值统一改善）和每次探针内加大任务基数（可识别该族、一般保证OPEN）。候选须同时攻击共享z容量和稀释终端，说明约束是否在同一条件内守恒；下一目标是统一舍入或新反例，不是再验证旧族被切。


新增联合攻击基准UM-DILUTED-ESCAPE-PROBE-GAP-v1：配置＋现行GHMR＋全部普通LST边探针仍gap2。不能仅把这些独立测试叠加后宣称统一余量；须在每次条件内保留共同槽/小端容量。

[逐机两倍跨度联合舍入](../../current/unrelated_machines/joint_slot_prefix_rounding.md)已经给受限类3/2算法，显示半单位见证障碍可以绕过。剩余具体义务是：对任意行内尺度混合，保留tiny任务的覆盖及真实剩余容量，同时取得统一排序槽损失或可修复的联合状态。当前没有这样的归约或舍入证明，不能把额外行跨度假设当免费预处理。

独立条件配置的新边界为[UM-SPARSE-CONDITIONED-CONFIG-GAP-v1](../../current/unrelated_machines/sparse_conditioned_configuration_gap.md)：单边查询内已保持全部单机配置，仍不足以跨不同查询保留共同容量。下一步须明确多机交叠相关性、消元后保持或大小任务联合迁移的新机制；不能继续以更多彼此独立的单机证书充当统一舍入义务。完整四机器bag一致性在该族精确，但一般状态规模和构造复杂度未解决。

完整单机配置的独立LP延伸已被UM-MACHINE-CONFIG-PROBE-GAP-v1的紧凑族排除为充分信息。下个候选须说明如何让条件证书共享一个base（至少跨块逃逸的一阶矩），或绕过该证书架构直接联合舍入；不能把∀i∀C∃各自延伸误读成全局分布。

## 固定槽输出空间必须可改变

UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1说明即使x有真实最优凸分解，固定标准ST图也可不存在统一低于2的匹配。新联合舍入须明确如何允许逐机任务数突破ceil(Σx_ij)、保留凸分量的负载相关性，或怎样做跨槽repair。该族的一轮最优修复必须通过，但单族成功不证明一般余量/位多项式迭代。见[完整反例与修复](../../current/unrelated_machines/optimal_convex_fixed_slot_gap.md)。
