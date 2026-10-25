# 五人反例方向：最优单会员遗漏与目录外保险

2026-10-25。**没有构造 HALF(5) 反例；也没有证明无条件 HALF(5)。** 本分支由父方授权直接攻击二倍；没有再扩 E3×J2 或 H4 族。

可复用主资产是 [最优遗漏的查询次数必要条件](optimal_incidence_necessary.md)：从既有真实前缀预算细化出一般 `W≥α_(m,q)(C_Q+J_Q)`。五人反例每个最优元组都必须有大量元组内单会员遗漏，精确门槛见正文 (6)。它是既有方法的需求细化，作者推导尚待父方独审，不认领新一般付款技术。

反例机制专门利用这一剩余方向：5 个遗漏块 X_i 各只属于最优 T_i，而目录外十个 K5 配对保险 R_ij 覆盖 X_i∪X_j。银行客户属于部分实际主题及一个 T_i；后续再让一部分银行客户也加入某个 R。其全树可信性、静态安全松弛及真正 SPE 被严格区分。

| 文件 | 精确用途和边界 |
|---|---|
| `insurance_security_lp.py/.json` | 全 actual/T/R 查询的必要安全 LP。AABBC 只能 L≤W；五个实际主题全异时，精确有理点 W137、L150、OPT287。后者不是 SPE |
| `diagnose_private_insurance.py/.json` | 原始有理点清成287单位客户；完整20主题整数BI（所有分母清为60），53130计数状态/42504终局。目标非SPE，真正最差SPE福利233；逐前缀强制偏离的失败点精确保存 |
| `partial_insured_bank_lp.py/.json` | 针对上述实际失败，把一半银行质量也挂到某个保险。只生成一个有目的的整数候选；额外加25名普通银行客户吸收舍入误差后，全部必要安全行精确通过，仍不把该点称SPE |
| `diagnose_partial_insurance.json` | 对该银行保险修复候选的同一定义级完整树诊断 |
| `diagnose_specialist_insurance.json` | 另一个有目的的银行修复：K5加五个单块银行specialist，目标W145/OPT295，仍非SPE；25主题142506计数状态/118755终局。末二新块选择严格压过specialist，是其失败原因 |
| `diagnose_private_insurance_canonical.json` | 规范 Fraction solver 对首个287客户输入的交叉核，root45、最差SPE233与numpy整数实现一致；不称外部独审 |
| `diagnose_cycle_insurance.json` | 从K5删到5-cycle以减少尾部新块选择的精确修复检验；根仍45、最差SPE233，未解决末二偏离 |
| `edge_insurance_attack.py/.json` | 保险本身 K5 五人精确BI：任一首个pair的真根minmax均1。此有限子局不外推加银行后的门槛单调性 |
| `cycle_bank_attack.py/.json` | 最初循环双会员遗漏机制的精确必要条件阻碍；被一般查询次数关系吸收，无需继续扩点 |
| `path_incidence_obstruction.py/.json` | 查询次数不等式的有限型有理算术QA；LP原始点不声称 SPE 可实现 |
| `full_insurance_bank_attack.py/.json` | 首个 AABBC 完整策略锥修复的浮点发现记录；限定为候选生成，未用于任何普遍上界或真正反例声明 |

上述计算都是指定机制的设计/诊断，不是无目的随机扫描或“未找到即成立”证据。完整SPE子树按集合值BI的现行全有序历史合同恢复；计数缓存只恢复全集，不强制匿名平局。脚本没有删除空主题/重复/零客户等原量词来主张一般结果。精确计算是有限证据，查询次数推导才是全输入关系。
