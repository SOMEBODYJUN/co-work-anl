# 研究资产总目录：按数学问题找名字、正文与证据

这里登记当前数学稿、问题、审查和已整合的拥塞核验资产。每个名称和用途经过逐文件整理；文件名、提交者代号与目录位置都不代替数学身份。
先从下表选择问题，再进入专题的阅读路线。历史原稿按需从 [历史入口](../history/README.md) 与 [来源对应](source_crosswalk.md) 查询；规范程序和人类讲义从 [全仓资产入口](../ASSETS.md) 进入。

证明、内部审查、外部审查和实现的真实状态分别保存在 [五轴账本](review_status.json)；精确量词在 [命题登记](current/claims.md) 和 [拥塞命题账本](weighted_congestion_frontier/CLAIMS.md)。下表只说明文件角色，不为整份文件授予统一的‘已证明’标签。

| 数学专题 | 首读入口 | 逐文件目录 |
| --- | --- | --- |
| 加权原子拥塞博弈 | [研究说明](current/weighted_congestion/README.md) | [中文资产名与用途](#weighted_congestion) |
| 共同目录双设施 | [研究说明](current/shared/README.md) | [中文资产名与用途](#shared) |
| 异构目录双设施 | [研究说明](current/heterogeneous/README.md) | [中文资产名与用途](#heterogeneous) |
| 双设施局部均衡与精确算法 | [研究说明](current/local_and_exact/README.md) | [中文资产名与用途](#local_and_exact) |
| 任意设施数与完整盒构造 | [研究说明](current/multi_facility/README.md) | [中文资产名与用途](#multi_facility) |
| 顺序客户吸引与半覆盖 | [研究说明](current/customer_attraction/README.md) | [中文资产名与用途](#customer_attraction) |
| 公共定义与精确命题登记 | [研究说明](current/README.md) | [中文资产名与用途](#foundation) |
| 设施模型的独立审查 | [研究说明](reviews/README.md) | [中文资产名与用途](#facility_review) |
| 客户吸引的独立审查 | [研究说明](reviews/README.md) | [中文资产名与用途](#customer_attraction_review) |
| 历史投稿判断与旧方向选择 | [研究说明](../history/README.md) | [中文资产名与用途](#publication) |

维护方法：先在 `catalog.json` 写具体名称和用途，再运行 `python3 research/build_catalog.py`；`--check` 同时拒绝漏登记、缺文件、无中文名称和过时生成稿。新增候选按原等级保存，不能为通过目录检查而升级结论。

<a id="weighted_congestion"></a>

## 加权原子拥塞博弈

### 研究入口、精确状态与文件合同

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [加权原子拥塞：奇环下界、工具与一般门槛缺口地图](<current/weighted_congestion/README.md>) | `research/current/weighted_congestion/README.md` | 先读精确模型与奇环共同机制，再按目标选择结构势、非对称机制或候选障碍；不能把局部证书包络当全类上界。 | 阅读导航；真值查精确正文及账本；关联 `WC-ENVELOPE-CEILING`、`WC-R1-DAG-STEP`、`WC-R1-HET-ENDPOINT-REDUCTION`，[命题合同（共 10 项）](assets.json) |
| [拥塞待审候选与未闭合义务地图](<questions/weighted_congestion/README.md>) | `research/questions/weighted_congestion/README.md` | 查固定乘子势、序势、端点与两列轨道稿的真实证据等级和缺失审查，选可接续的准确义务。 | 阅读导航；真值查精确正文及账本 |
| [加权拥塞共同研究与协作入口](<weighted_congestion_frontier/README.md>) | `research/weighted_congestion_frontier/README.md` | 数学阅读进入 current 的证明地图；阶段保存时核对命名、账本和地图共同提交，运行程序时再进入启动和协议。 | 阅读导航；真值查精确正文及账本 |
| [拥塞逐成果包资产链：中文名称、正文、审查与证据](<weighted_congestion_frontier/FILES.md>) | `research/weighted_congestion_frontier/FILES.md` | 按数学成果包找到具体文件作用，追踪主稿到独立攻击、实际核验与冻结结果，不先读路径字典序清单。 | 阅读导航；真值查精确正文及账本 |
| [加权原子拥塞精确模型与普遍门槛目标](<weighted_congestion_frontier/MODEL.md>) | `research/weighted_congestion_frontier/MODEL.md` | 核对正权、有限策略、非负多项式费用及弱不等式近似 PNE 的全类量词，防止偷偷缩小目标模型。 | 定义与模型；不隐含跨模型定理 |
| [拥塞精确命题账本：目标、局部成果与候选版本](<weighted_congestion_frontier/CLAIMS.md>) | `research/weighted_congestion_frontier/CLAIMS.md` | 引用团队结果前核对稳定 ID、版本、定义域、假设、结论、证据和 objection；范围变化要另建版本。 | 精确命题登记；摘要不替代原陈述 |
| [拥塞当前前沿、已保存工具和下一证明义务](<weighted_congestion_frontier/RESEARCH_STATE.md>) | `research/weighted_congestion_frontier/RESEARCH_STATE.md` | 接续研究时核对当前已知与未解，避免使用原稿时点状态或旧公屏代替共同账本。 | 精确命题登记；摘要不替代原陈述 |
| [拥塞失败机制、局部证书边界与可回收结果](<weighted_congestion_frontier/FAILED_ROUTES.md>) | `research/weighted_congestion_frontier/FAILED_ROUTES.md` | 选择势方法、固定小构造或源族调参前查失败的准确量词；方法失败不得升级为全类不可能。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |
| [加权拥塞近似纯均衡的文献基线与核验范围](<weighted_congestion_frontier/LITERATURE.md>) | `research/weighted_congestion_frontier/LITERATURE.md` | 查原文真实模型、上界、下界和开放问题；文献事实、团队解释与尚未认证的新颖性分别引用。 | 文献核对；与团队新结果分别引用 |
| [拥塞前人机制与可复用技术资产](<weighted_congestion_frontier/PRIOR_ASSETS.md>) | `research/weighted_congestion_frontier/PRIOR_ASSETS.md` | 选择势函数、下界构造或桥梁时查前人已经提供的对象、方法和适用限制，避免重复宣称发现。 | 文献核对；与团队新结果分别引用 |

### 奇环全状态下界、有限实现与精确证书包络

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [奇数环总证明：全状态非存在、精确包络与同次数构造](<current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md>) | `research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md` | 从真实资源策略建立严格局部测试及正系数乘积判据，证明精确包络、有限有理同次数下界，并处理多项式与单成员子类。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同（共 5 项）](assets.json) |
| [奇数环线性重置：显式下界与完整证明链](<current/weighted_congestion/odd_ring_linear.md>) | `research/current/weighted_congestion/odd_ring_linear.md` | 整合奇环全状态覆盖、权重闭环、线性重置放大及显式下界；说明与同次数包络的关系及全类上界缺口。 | 数学正文；按关联命题分别核对证明及审查；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 25 项）](assets.json) |
| [有向奇数环：资源策略与正系数闭环接口](<current/weighted_congestion/odd_ring_linear/README.md>) | `research/current/weighted_congestion/odd_ring_linear/README.md` | 完整定义可变次数的有向奇环资源策略、全部纯状态覆盖与正系数可行性乘积条件，保留原稿时点状态。 | 数学正文；按关联命题分别核对证明及审查；精确范围见本页正文 |
| [线性重置放大器：构造随次数增长的非存在下界](<current/weighted_congestion/odd_ring_linear/general_lower_bound.md>) | `research/current/weighted_congestion/odd_ring_linear/general_lower_bound.md` | 给出有限重置/放大块的构造推导及其标量包络，作为现行线性重置总稿的详细机制来源。 | 数学正文；按关联命题分别核对证明及审查；精确范围见本页正文 |
| [奇数环正系数接口：渐近放大能力的上限](<current/weighted_congestion/odd_ring_linear/INTERFACE_BARRIER.md>) | `research/current/weighted_congestion/odd_ring_linear/INTERFACE_BARRIER.md` | 证明指定充分系数接口的必要标量不等式，限制该证书的渐近常数，不推出实际游戏或全类存在上界。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |
| [奇数环精确包络：必要性、充分性与端点独立审查](<reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md>) | `research/reviews/weighted_congestion/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md` | 在全状态奇环还原基础上独立重构正乘积证书的包络、端点和标量关系；不推出全类存在上界。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环资源策略：逐负载、全状态覆盖与闭环独立审查](<reviews/weighted_congestion/odd_ring_independent/REVIEW.md>) | `research/reviews/weighted_congestion/odd_ring_independent/REVIEW.md` | 先由资源策略重建真实偏离成本与局部不等式，再审查成长参数；独立于原构造程序。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环线性实现：真实资源成本独立攻击](<reviews/weighted_congestion/odd_ring_linear/independent_attack.md>) | `research/reviews/weighted_congestion/odd_ring_linear/independent_attack.md` | 以资源级成本和人数压缩状态检查指定奇环证书及给定次数实例；一般证书与有限检查分开。 | 实际审查记录；只覆盖所列版本与义务 |
| [奇数环线性重置：显式下界与渐近常数审查](<reviews/weighted_congestion/odd_ring_linear_audit/asymptotic_review.md>) | `research/reviews/weighted_congestion/odd_ring_linear_audit/asymptotic_review.md` | 核对原二进参数、恢复的线性重置证明及更强显式下界，记录与标量包络的关系。 | 实际审查记录；只覆盖所列版本与义务 |
| [奇数环下界：文献基线与机制碰撞检索记录](<reviews/weighted_congestion/odd_ring_linear_audit/literature_review.md>) | `research/reviews/weighted_congestion/odd_ring_linear_audit/literature_review.md` | 核对指定一手文献、模型和可比较下界；有限检索未发现碰撞不认证世界优先权。 | 实际审查记录；只覆盖所列版本与义务 |
| [奇数环证书：状态覆盖、条件必要性与参数恢复审查](<reviews/weighted_congestion/odd_ring_linear_audit/state_review.md>) | `research/reviews/weighted_congestion/odd_ring_linear_audit/state_review.md` | 独立从策略还原成本，检查全状态充分证书、系数可行性和后续恢复的重置/接口结论。 | 实际审查记录；只覆盖所列版本与义务 |
| [奇数环与异权群组：多项式拥塞文献核对](<reviews/weighted_congestion/odd_ring_literature/notes.md>) | `research/reviews/weighted_congestion/odd_ring_literature/notes.md` | 记录已查固定版本的模型、存在/非存在基线及奇环机制参照；不提供穷尽新颖性认证。 | 实际审查记录；只覆盖所列版本与义务 |
| [奇数环单成员群组：实际游戏存在界的独立证明](<reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md>) | `research/reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md` | 由单冲突状态图重建每组一名群组玩家的存在界，明确不覆盖一般多成员群组。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-ODD-RING-SINGLETON-UPPER-v1`，[命题合同](assets.json) |
| [奇数环参数包络：精确最值与有理特殊块审查](<reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md>) | `research/reviews/weighted_congestion/odd_ring_parameters/exact_envelope_review.md` | 独立优化正乘积接口并核对有理特殊块的实现；以另行证明的全状态还原为前提。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环多项式形状：不扩大正测试包络的审查](<reviews/weighted_congestion/odd_ring_parameters/polynomial_envelope_review.md>) | `research/reviews/weighted_congestion/odd_ring_parameters/polynomial_envelope_review.md` | 检查非负多项式混合、常数项及零形状边界，证明规定共享形状下的证书包络不变。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1`，[命题合同](assets.json) |
| [奇数环线性实现：独立真实成本攻击程序](<../tests/audits/weighted_congestion/odd_ring_linear/attack.py>) | `tests/audits/weighted_congestion/odd_ring_linear/attack.py` | 以 Fraction 从策略和资源计算成本；人数压缩状态代表相应的带标签状态，默认只审明示实例。 | 有限计算核验；不代替一般证明 |
| [有向奇数环：精确系数证书与压缩状态核验](<../tests/audits/weighted_congestion/odd_ring_linear/verify_ring.py>) | `tests/audits/weighted_congestion/odd_ring_linear/verify_ring.py` | 检查闭环系数并枚举所报告实例的 hub 位和群组人数状态，Decimal 仅用于展示。 | 有限计算核验；不代替一般证明 |
| [奇数环重置审查：有限有理回归与包络诊断](<../tests/audits/weighted_congestion/odd_ring_linear_audit/audit_checks.py>) | `tests/audits/weighted_congestion/odd_ring_linear_audit/audit_checks.py` | 核对原候选与线性重置实例，并将 Decimal 包络诊断与精确证书检查分开。 | 有限计算核验；不代替一般证明；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [线性重置放大器：独立有理证书回归](<../tests/audits/weighted_congestion/odd_ring_linear_audit/verify_linear_reset.py>) | `tests/audits/weighted_congestion/odd_ring_linear_audit/verify_linear_reset.py` | 不导入原奇环程序，精确重建有限重置证书及拒绝边界；Decimal 内容单列诊断。 | 有限计算核验；不代替一般证明；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [奇数环状态审查：逐资源成本与巨大参数证书核验](<../tests/audits/weighted_congestion/odd_ring_linear_audit/verify_state_review.py>) | `tests/audits/weighted_congestion/odd_ring_linear_audit/verify_state_review.py` | 从策略重新构造负载，不用证书余量公式评估实际成本；巨大放大族只检查已证明的系数证书。 | 有限计算核验；不代替一般证明；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [奇数环精确包络：标量恒等式与同次数证书核验](<../tests/audits/weighted_congestion/odd_ring_independent/verify_envelope.py>) | `tests/audits/weighted_congestion/odd_ring_independent/verify_envelope.py` | 使用整数/Fraction 检查包络恒等式、同次数可行证书和显式下界分离，任意参数结论由审查证明承担。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环独立资源审查：小实例全枚举与成长证书核验](<../tests/audits/weighted_congestion/odd_ring_independent/verify_literal.py>) | `tests/audits/weighted_congestion/odd_ring_independent/verify_literal.py` | 从资源策略计算成本；仅明示小实例全枚举，巨大成长族按已证明局部证书检查。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环精确包络：有理特殊块构造核验](<../tests/audits/weighted_congestion/odd_ring_parameters/check_exact_envelope.py>) | `tests/audits/weighted_congestion/odd_ring_parameters/check_exact_envelope.py` | 使用精确算术检查实现包络的有限有理特殊块及所报告参数。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环整数成长族：首项常数与精确证书核验](<../tests/audits/weighted_congestion/odd_ring_parameters/check_integer_family.py>) | `tests/audits/weighted_congestion/odd_ring_parameters/check_integer_family.py` | 以整数算术检查独立推出的首项常数为一的成长族参数及证书。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环独立参数族：精确整数可行性核验](<../tests/audits/weighted_congestion/odd_ring_parameters/check_parameters.py>) | `tests/audits/weighted_congestion/odd_ring_parameters/check_parameters.py` | 检查独立推导的成长参数配方和整数系数条件，不扩张有限测试的量词。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环多项式包络：混合、常数项与零形状核验](<../tests/audits/weighted_congestion/odd_ring_parameters/check_polynomial_envelope.py>) | `tests/audits/weighted_congestion/odd_ring_parameters/check_polynomial_envelope.py` | 用有理算术检查混合费用的凸恒等式、常数单项式因子、零形状排除及包络上方失败。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1`，[命题合同](assets.json) |
| [奇数环单成员群组：单冲突状态图与真实成本核验](<../tests/audits/weighted_congestion/odd_ring_parameters/check_singleton_graph.py>) | `tests/audits/weighted_congestion/odd_ring_parameters/check_singleton_graph.py` | 精确核对单冲突状态转换图、玩家偏离成本及所报告零费用/反向映射边界。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-SINGLETON-UPPER-v1`，[命题合同](assets.json) |
| [奇数环总证书：标量身份、构造证书与小游戏核验](<../tests/audits/weighted_congestion/odd_ring/verify.py>) | `tests/audits/weighted_congestion/odd_ring/verify.py` | 用有理算术检查局部恒等式、构造参数及明示小游戏；巨大族仅按已证明局部测试检查。 | 有限计算核验；不代替一般证明；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [有向奇数环：原精确实例与系数检查记录](<../evidence/runs/weighted_congestion/odd_ring_linear/exact_evidence_20261014.json>) | `evidence/runs/weighted_congestion/odd_ring_linear/exact_evidence_20261014.json` | 保存原奇环候选的实际有理算术测试案例及证书范围。 | 冻结输入、证书或结果；不原位覆盖 |
| [奇数环重置审查：原候选、重置与包络记录](<../evidence/runs/weighted_congestion/odd_ring_linear_audit/audit_checks.json>) | `evidence/runs/weighted_congestion/odd_ring_linear_audit/audit_checks.json` | 冻结原候选、线性重置及包络诊断的检查结果和局限。 | 冻结输入、证书或结果；不原位覆盖；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [线性重置放大器：精确案例与拒绝边界记录](<../evidence/runs/weighted_congestion/odd_ring_linear_audit/linear_reset_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_linear_audit/linear_reset_verification.json` | 记录精确重置案例、拒绝边界、源包络回归和非证明性的渐近诊断。 | 冻结输入、证书或结果；不原位覆盖；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [线性重置原稿恢复：来源提交与重放溯源记录](<../evidence/runs/weighted_congestion/odd_ring_linear_audit/recovery_provenance.json>) | `evidence/runs/weighted_congestion/odd_ring_linear_audit/recovery_provenance.json` | 记录被恢复源文件、原 pending 标签、来源提交和重放命令；本文件是溯源证据，不是数学审查结论。 | 冻结输入、证书或结果；不原位覆盖；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [奇数环状态审查：真实成本与参数配方冻结记录](<../evidence/runs/weighted_congestion/odd_ring_linear_audit/state_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_linear_audit/state_verification.json` | 保存 hub 失效见证、真实状态审计、有理放大配方核验、程序哈希与覆盖限制。 | 冻结输入、证书或结果；不原位覆盖；关联 `OC-AMPLIFIER-ENVELOPE-v1`、`OC-AMPLIFIER-LIMIT-v1`、`OC-INTERFACE-BARRIER-v1`，[命题合同（共 5 项）](assets.json) |
| [奇数环精确包络：恒等式与同次数样例冻结记录](<../evidence/runs/weighted_congestion/odd_ring_independent/envelope_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_independent/envelope_verification.json` | 保存包络身份、全部次数相同的有限证书样例、显式包络分离检查及范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环独立资源审查：小实例与成长参数冻结记录](<../evidence/runs/weighted_congestion/odd_ring_independent/verification.json>) | `evidence/runs/weighted_congestion/odd_ring_independent/verification.json` | 分开保存小型逐资源全状态实例及大族参数证书样本，避免混称巨大状态空间枚举。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环精确包络：有理特殊块冻结记录](<../evidence/runs/weighted_congestion/odd_ring_parameters/exact_envelope_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_parameters/exact_envelope_verification.json` | 记录有理特殊块的精确样例与证据范围，不替代连续参数包络证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环独立参数族：整数可行性冻结记录](<../evidence/runs/weighted_congestion/odd_ring_parameters/exact_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_parameters/exact_verification.json` | 冻结独立参数配方的实际整数案例及算术范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环整数成长族：精确参数冻结记录](<../evidence/runs/weighted_congestion/odd_ring_parameters/integer_family_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_parameters/integer_family_verification.json` | 保存整数成长族各明示参数的可行性检查及其范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |
| [奇数环多项式包络：混合与退化边界冻结记录](<../evidence/runs/weighted_congestion/odd_ring_parameters/polynomial_envelope_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_parameters/polynomial_envelope_verification.json` | 保存次数、种子、非零形状对、正分子条件、常数和零形状检查；一般证明另见正文与审查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1`，[命题合同](assets.json) |
| [奇数环单成员群组：状态图与玩家成本冻结记录](<../evidence/runs/weighted_congestion/odd_ring_parameters/singleton_graph_verification.json>) | `evidence/runs/weighted_congestion/odd_ring_parameters/singleton_graph_verification.json` | 记录单成员奇环的有限状态图与成本检查；端点连续包络结论依赖一般证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-SINGLETON-UPPER-v1`，[命题合同](assets.json) |
| [奇数环总证书：局部身份、参数与小游戏冻结记录](<../evidence/runs/weighted_congestion/odd_ring/verification.json>) | `evidence/runs/weighted_congestion/odd_ring/verification.json` | 保存程序哈希、实际构造样例、逐资源小游戏和核验局限。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-ODD-RING-CERTIFICATE-v1`、`WC-R3-ODD-RING-ENVELOPE-v1`、`WC-R3-ODD-RING-LOWER-v1`，[命题合同](assets.json) |

### 文献源族的锐包络与渐近

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [文献两攻击公式：参数上确界的锐渐近证明](<current/weighted_congestion/source_envelope/sharp_asymptotic_envelope.md>) | `research/current/weighted_congestion/source_envelope/sharp_asymptotic_envelope.md` | 在原整数重数、正轻权及次数域内证明源两测试参数上确界的匹配渐近，保留取整与全部参数序列分析。 | 数学正文；按关联命题分别核对证明及审查；关联 `R3-SOURCE-SHARP-ASYMPTOTIC-v1`，[命题合同](assets.json) |
| [文献两攻击公式：锐渐近成果与阅读入口](<current/weighted_congestion/source_envelope/README.md>) | `research/current/weighted_congestion/source_envelope/README.md` | 指向锐渐近主证明、相应独立审查和分开标识的整数次数/连续代理数值诊断；旧时点标签不覆盖现行账本。 | 数学正文；按关联命题分别核对证明及审查；精确范围见本页正文 |
| [文献两攻击公式：适用于全部参数的机制上限](<current/weighted_congestion/source_ceiling/README.md>) | `research/current/weighted_congestion/source_ceiling/README.md` | 由两攻击倍率的耦合关系推出统一渐近上限，限制指定正测试；Decimal 检查仅为诊断。 | 方法障碍；否定范围以正文为准；关联 `WC-ENVELOPE-CEILING`，[命题合同](assets.json) |
| [文献两攻击公式：锐渐近的另一份候选推导](<questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md>) | `research/questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md` | 保存独立提出的源公式锐渐近候选；另一路已审证明不自动替代本稿尚未完成的审查。 | 候选或未闭合义务；保存不升级状态；关联 `WC-R1-LF-SHARP`，[命题合同](assets.json) |
| [文献两攻击公式统一上限：独立重构与反向审查](<reviews/weighted_congestion/source_ceiling_review/independent_review.md>) | `research/reviews/weighted_congestion/source_ceiling_review/independent_review.md` | 在合法源参数域中独立还原两倍率耦合与渐近上限，只审指定证书机制。 | 实际审查记录；只覆盖所列版本与义务 |
| [文献两攻击公式锐渐近：上下两侧独立攻击](<reviews/weighted_congestion/source_envelope/review.md>) | `research/reviews/weighted_congestion/source_envelope/review.md` | 先重建整数参数下界和上界消元，再逐式核对锐渐近主稿及源全状态覆盖。 | 实际审查记录；只覆盖所列版本与义务 |
| [另一份锐渐近候选：原文版本与公式核对](<reviews/weighted_congestion/source_envelope_candidate/source_audit.md>) | `research/reviews/weighted_congestion/source_envelope_candidate/source_audit.md` | 核对所用原论文版本、两攻击表达及其参数域；本源事实核对不等于候选锐渐近证明已完成独立审查。 | 实际审查记录；只覆盖所列版本与义务 |
| [源两攻击统一上限：代数回归与 Decimal 诊断](<../tests/audits/weighted_congestion/source_ceiling/verify.py>) | `tests/audits/weighted_congestion/source_ceiling/verify.py` | 对必要代数条件使用有理检查，对对数界使用非区间 Decimal 数值诊断；不替代全参数证明。 | 有限计算核验；不代替一般证明 |
| [源锐渐近候选：有限状态核验与高精度样本](<../tests/audits/weighted_congestion/source_envelope_candidate/verify.py>) | `tests/audits/weighted_congestion/source_envelope_candidate/verify.py` | 用 Fraction 复现有限游戏，用 Decimal 给出渐近诊断；后者不是区间证书或一般证明。 | 有限计算核验；不代替一般证明 |
| [源公式锐渐近：整数取整与超大次数 Decimal 诊断](<../tests/audits/weighted_congestion/source_envelope/verify_logs.py>) | `tests/audits/weighted_congestion/source_envelope/verify_logs.py` | 稳定计算高精度对数、整数前驱及取整；明确区分真实整数次数与连续代理，结果非区间证书。 | 有限计算核验；不代替一般证明；关联 `R3-SOURCE-SHARP-ASYMPTOTIC-v1`，[命题合同](assets.json) |
| [源两攻击统一上限：精确检查与数值诊断记录](<../evidence/runs/weighted_congestion/source_ceiling/verification.json>) | `evidence/runs/weighted_congestion/source_ceiling/verification.json` | 分开保存精确代数回归、Decimal 诊断、适用限制与来源哈希。 | 冻结输入、证书或结果；不原位覆盖 |
| [源锐渐近候选：精确有限检查与诊断样本](<../evidence/runs/weighted_congestion/source_envelope_candidate/verification.json>) | `evidence/runs/weighted_congestion/source_envelope_candidate/verification.json` | 保留候选稿自身的精确检查与高精度采样，不能借另一份已审证明提升其审查状态。 | 冻结输入、证书或结果；不原位覆盖 |
| [源公式锐渐近：整数次数与连续代理诊断记录](<../evidence/runs/weighted_congestion/source_envelope/verification.json>) | `evidence/runs/weighted_congestion/source_envelope/verification.json` | 保存高精度环境、整数次数行和连续代理行；不作为普遍参数上界的证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `R3-SOURCE-SHARP-ASYMPTOTIC-v1`，[命题合同](assets.json) |

### 对称两列拓扑的完整还原

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [完整对称两列拓扑：高倍率非存在还原至源公式](<current/weighted_congestion/source_topology/symmetric_two_column_reduction.md>) | `research/current/weighted_congestion/source_topology/symmetric_two_column_reduction.md` | 对任意正共同轻权和两类非负多项式，在精确倍率范围内把实际非存在还原到源两测试；不覆盖异权或非对称费用。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-FULL-TOPOLOGY-REDUCTION-v3`，[命题合同](assets.json) |
| [对称两列游戏：完整状态商与保守证书损失候选](<questions/weighted_congestion/two_column_orbits/two_column_orbit_candidate.md>) | `research/questions/weighted_congestion/two_column_orbits/two_column_orbit_candidate.md` | 将每个对称同轻权游戏的实例最优倍率化为人数轨道公式，并给保守两攻击与真实阈值的差异；所引独立审查原件未找到。 | 候选或未闭合义务；保存不升级状态 |
| [完整对称两列拓扑：三个版本的还原审查](<reviews/weighted_congestion/source_topology_review/review.md>) | `research/reviews/weighted_congestion/source_topology_review/review.md` | 独立重建状态瓶颈并核对第三版倍率范围、权重互换、平移和非负多项式还原。 | 实际审查记录；只覆盖所列版本与义务 |
| [对称两列状态商：真实资源与人数轨道交叉核验](<../tests/audits/weighted_congestion/two_column_orbits/verify.py>) | `tests/audits/weighted_congestion/two_column_orbits/verify.py` | 独立以 Fraction 重算所有明示实例的真实资源偏离，对照人数轨道、反向检查及保守证书损失。 | 有限计算核验；不代替一般证明 |
| [完整对称两列拓扑：真实状态与还原接口核验](<../tests/audits/weighted_congestion/source_topology/verify.py>) | `tests/audits/weighted_congestion/source_topology/verify.py` | 用有理算术核对人数轨道、实际偏离、权重互换、平移及多项式端点还原；不从样本推普遍性。 | 有限计算核验；不代替一般证明；关联 `WC-R3-FULL-TOPOLOGY-REDUCTION-v3`，[命题合同](assets.json) |
| [完整对称拓扑：独立真实状态与还原审计](<../tests/audits/weighted_congestion/source_topology_review/check_review.py>) | `tests/audits/weighted_congestion/source_topology_review/check_review.py` | 独立实现资源状态预言及高倍率还原接口，只把明示参数测试作为有限证据。 | 有限计算核验；不代替一般证明；关联 `WC-R3-FULL-TOPOLOGY-REDUCTION-v3`，[命题合同](assets.json) |
| [对称两列状态商：真实阈值与保守证书冻结记录](<../evidence/runs/weighted_congestion/two_column_orbits/evidence.json>) | `evidence/runs/weighted_congestion/two_column_orbits/evidence.json` | 保存参数域、真实状态/偏离、反向检查、实例阈值与保守证书的有限比较；所引独立审查仍缺失。 | 冻结输入、证书或结果；不原位覆盖 |
| [完整对称两列拓扑：轨道、平移与还原冻结记录](<../evidence/runs/weighted_congestion/source_topology/results.json>) | `evidence/runs/weighted_congestion/source_topology/results.json` | 保存种子、有限游戏/状态/偏离数及高倍率还原、非零平移和权重互换检查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-FULL-TOPOLOGY-REDUCTION-v3`，[命题合同](assets.json) |
| [完整对称拓扑：独立倍率与还原结果记录](<../evidence/runs/weighted_congestion/source_topology_review/review_results.json>) | `evidence/runs/weighted_congestion/source_topology_review/review_results.json` | 保存所用倍率、有限游戏和状态、左右方向非存在检查及适用范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-FULL-TOPOLOGY-REDUCTION-v3`，[命题合同](assets.json) |

### 固定次数源族的精确区间证书

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [文献两攻击公式：三十二次参数上界与整数符号证书](<current/weighted_congestion/source_degree32/symmetric_source_interval_certificate.md>) | `research/current/weighted_congestion/source_degree32/symmetric_source_interval_certificate.md` | 消去幅度参数并严格约化整数重数，再以 Bernstein 系数符号证书覆盖全部合法实参数。；配套 [十四资源分离：真实策略与符号叶证书第二重构](<../tests/audits/weighted_congestion/crossover/main_check.py>) | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-SOURCE32-178-v1`，[命题合同](assets.json) |
| [源公式三十二次界：Bernstein 整数符号证书核验](<../tests/audits/weighted_congestion/source_degree32/verify.py>) | `tests/audits/weighted_congestion/source_degree32/verify.py` | 只用标准库整数/有理算术检查冻结 Bernstein 覆盖叶与负系数；显式新路径才生成新证书。 | 有限计算核验；不代替一般证明；关联 `WC-R3-SOURCE32-178-v1`，[命题合同](assets.json) |
| [源公式三十二次界：完整 Bernstein 覆盖证书](<../evidence/certificates/weighted_congestion/source_degree32/certificate.json>) | `evidence/certificates/weighted_congestion/source_degree32/certificate.json` | 记录整数重数约化、每个必要多项式的区间覆盖与 Bernstein 叶符号，用于有限实域严格证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-SOURCE32-178-v1`，[命题合同](assets.json) |
| [源公式三十二次界：符号证书执行与哈希记录](<../evidence/runs/weighted_congestion/source_degree32/verification.json>) | `evidence/runs/weighted_congestion/source_degree32/verification.json` | 冻结多项式/叶计数、细分深度、精确算术、程序文件哈希和本次符号核验范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-SOURCE32-178-v1`，[命题合同](assets.json) |

### 资源支持对固定小构造的限制

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [资源潜在用户支持：总成本最小点给出的存在界](<current/weighted_congestion/resource_support.md>) | `research/current/weighted_congestion/resource_support.md` | 证明每资源潜在用户数上限给出相同因子的纯近似均衡，允许零费用、空策略和任意非递减费用；不提供多项式时间界。；配套 [互补符号列：三玩家与四玩家全状态有理核验](<../tests/audits/weighted_congestion/signed_columns/verify.py>)；配套 [互补符号列：有限实例有理证书冻结记录](<../evidence/runs/weighted_congestion/signed_columns/verification.json>) | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R1-RESOURCE-SUPPORT`，[命题合同](assets.json) |
| [双人资源互补网络：显式势函数保证二倍均衡](<current/weighted_congestion/odd_ring_linear/pair_obstruction/PAIR_OBSTRUCTION.md>) | `research/current/weighted_congestion/odd_ring_linear/pair_obstruction/PAIR_OBSTRUCTION.md` | 在相同费用副本、任意正权和非负私有费用下证明二倍均衡；说明只有两名战略用户的资源不能单独产生增长下界。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |

### 稀疏权谱、密度势与矩界

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [资源局部权密度：锐矩不等式与纯近似均衡](<current/weighted_congestion/weight_density.md>) | `research/current/weighted_congestion/weight_density.md` | 先证明半开乘法区间密度约束下的锐矩估计，再将其用于共享幂成本势的实例结构存在界。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R2-DENSITY-MOMENT`、`WC-R2-WEIGHT-DENSITY`，[命题合同](assets.json) |
| [资源局部权密度：锐矩估计与势函数独立审查](<reviews/weighted_congestion/weight_density/review.md>) | `research/reviews/weighted_congestion/weight_density/review.md` | 独立核对潜在用户半开权区间密度、矩估计与共享幂成本势下降，处理空策略和零费用。 | 实际审查记录；只覆盖所列版本与义务 |
| [资源权密度与锐矩估计：定义级有理审计](<../tests/audits/weighted_congestion_density.py>) | `tests/audits/weighted_congestion_density.py` | 使用可由有理幂表示的权和精确整数幂比较检查矩与游戏势不等式；不使用浮点根误差。 | 有限计算核验；不代替一般证明；关联 `WC-R2-DENSITY-MOMENT`、`WC-R2-WEIGHT-DENSITY`，[命题合同](assets.json) |
| [资源权密度与锐矩估计：有限审计冻结记录](<../evidence/runs/2026-10-14/weighted_congestion_density.json>) | `evidence/runs/2026-10-14/weighted_congestion_density.json` | 保存参数、种子、矩样例、实际游戏和边界计数、程序哈希及任意实权推广的证据限制。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R2-DENSITY-MOMENT`、`WC-R2-WEIGHT-DENSITY`，[命题合同](assets.json) |
| [资源外部性与权密度：初始推导来源记录](<../history/source/notes/weighted_congestion/density_externality.md>) | `history/source/notes/weighted_congestion/density_externality.md` | 保留权密度势的原始外部性计算与研究起点；规范加强证明与独立审查另见现行资产。 | 来源或历史判断；不作为现行结论；关联 `WC-R2-DENSITY-MOMENT`、`WC-R2-WEIGHT-DENSITY`，[命题合同](assets.json) |

### 资源局部势拼接与异质接口

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [资源局部势拼接：共享乘子、两尺度障碍与两权组锐界](<current/weighted_congestion/power_bridge.md>) | `research/current/weighted_congestion/power_bridge.md` | 统一登记资源级稀疏权谱拼接、固定次线性幂乘子的路径障碍、线性费用两权组的锐平方根跨度界。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R2-AFFINE-TWO-TYPE`、`WC-R2-POWER-PATH-OBSTRUCTION`、`WC-R2-RESOURCE-POWER-BRIDGE`，[命题合同](assets.json) |
| [线性费用两权组：分片势与锐平方根跨度界](<current/weighted_congestion/power_bridge/affine_two_type.md>) | `research/current/weighted_congestion/power_bridge/affine_two_type.md` | 为两个精确权组构造分片二次集合势，证明边际夹逼的最优统一因子及人数增长下的锐性。 | 数学正文；按关联命题分别核对证明及审查；精确范围见本页正文 |
| [固定次线性幂乘子：两尺度路径比障碍](<current/weighted_congestion/power_bridge/path_obstruction.md>) | `research/current/weighted_congestion/power_bridge/path_obstruction.md` | 用重先轻后与轻先重后的两条插入路径，否定固定次线性幂乘子在任意密集权谱上的统一常数夹逼。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |
| [资源局部势拼接：强化边际下界与共享乘子独立审查](<reviews/weighted_congestion/power_bridge/independent_review.md>) | `research/reviews/weighted_congestion/power_bridge/independent_review.md` | 指出弱边际下界不足的推理，并重建更强下界以修复指定资源缩放与共享乘子接口。 | 实际审查记录；只覆盖所列版本与义务 |
| [两尺度路径障碍：固定幂乘子的独立重构审查](<reviews/weighted_congestion/power_bridge/path_review.md>) | `research/reviews/weighted_congestion/power_bridge/path_review.md` | 独立重建两个权组的路径比反例，明确审查依据为收到的精确公式，未假称已读尚未出现的候选文件。 | 实际审查记录；只覆盖所列版本与义务 |
| [线性费用两权组：分片边际与路径比有理核验](<../tests/audits/weighted_congestion/power_bridge/verify_affine_two_type.py>) | `tests/audits/weighted_congestion/power_bridge/verify_affine_two_type.py` | 不用浮点线性规划，以 Fraction 检查分片集合势、插入边际和子集路径比。 | 有限计算核验；不代替一般证明 |
| [资源局部势拼接：幂乘子路径与两权组独立核验](<../tests/audits/weighted_power_bridge.py>) | `tests/audits/weighted_power_bridge.py` | 用有理算术检查幂乘子路径、资源拼接和线性两权组势；任意实权结论依赖正文证明。 | 有限计算核验；不代替一般证明；关联 `WC-R2-AFFINE-TWO-TYPE`、`WC-R2-POWER-PATH-OBSTRUCTION`、`WC-R2-RESOURCE-POWER-BRIDGE`，[命题合同](assets.json) |
| [资源局部势拼接：幂路径与两权组冻结记录](<../evidence/runs/2026-10-14/weighted_power_bridge.json>) | `evidence/runs/2026-10-14/weighted_power_bridge.json` | 记录检查项、幂路径表、算术、程序哈希、重放命令和不由有限计算建立的结论。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R2-AFFINE-TWO-TYPE`、`WC-R2-POWER-PATH-OBSTRUCTION`、`WC-R2-RESOURCE-POWER-BRIDGE`，[命题合同](assets.json) |
| [共享幂乘子与两尺度路径：原始机制来源记录](<../history/source/notes/weighted_congestion_frontier/power_path_discovery.md>) | `history/source/notes/weighted_congestion_frontier/power_path_discovery.md` | 保留从多尺度资源拼接义务发现路径障碍的原始推导；现行完整证明在 power_bridge 主稿。 | 来源或历史判断；不作为现行结论；关联 `WC-R2-AFFINE-TWO-TYPE`、`WC-R2-POWER-PATH-OBSTRUCTION`、`WC-R2-RESOURCE-POWER-BRIDGE`，[命题合同](assets.json) |

### 局部窄权带、Shapley 势与选择器边界

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [资源局部窄权带：Shapley 存在界与跨带拼接障碍](<current/weighted_congestion/weight_bands/README.md>) | `research/current/weighted_congestion/weight_bands/README.md` | 给出局部权比存在界、指定势选择器锐性、跨权带归一化的混合差分障碍及标准势的线性损失。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-BAND-CURL-v1`、`WC-R3-BAND-LINEAR-v1`、`WC-R3-DENSE-LOCAL-v1`，[命题合同（共 5 项）](assets.json) |
| [资源局部窄权带：Shapley 份额与存在界独立审查](<reviews/weighted_congestion/weight_bands_review/independent_review.md>) | `research/reviews/weighted_congestion/weight_bands_review/independent_review.md` | 从模型和原始子集 Shapley 定义重建份额夹逼、局部权比存在界与相关接口。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-BAND-CURL-v1`、`WC-R3-BAND-LINEAR-v1`、`WC-R3-DENSE-LOCAL-v1`，[命题合同（共 5 项）](assets.json) |
| [局部窄权带：原始子集 Shapley 定义独立审计](<../tests/audits/weighted_congestion/weight_bands_review/independent_check.py>) | `tests/audits/weighted_congestion/weight_bands_review/independent_check.py` | 从子集份额定义核对权序、份额夹逼和效率恒等式；默认只读比对冻结输出。 | 有限计算核验；不代替一般证明；关联 `WC-R3-DENSE-LOCAL-v1`、`WC-R3-DENSE-SHARE-v1`，[命题合同](assets.json) |
| [局部窄权带：份额界、混合差分与坏选择器回归](<../tests/audits/weighted_congestion/weight_bands/verify.py>) | `tests/audits/weighted_congestion/weight_bands/verify.py` | 精确检查 Shapley 份额、份额次序、混合差分、密度增强、线性损失与锐选择器样例。 | 有限计算核验；不代替一般证明；关联 `WC-R3-BAND-CURL-v1`、`WC-R3-BAND-LINEAR-v1`、`WC-R3-DENSE-LOCAL-v1`，[命题合同（共 5 项）](assets.json) |
| [局部窄权带：独立 Shapley 份额审计记录](<../evidence/runs/weighted_congestion/weight_bands_review/independent_verification.json>) | `evidence/runs/weighted_congestion/weight_bands_review/independent_verification.json` | 保存有限权向量、单项式次数、份额界和效率检查的确切范围。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-DENSE-LOCAL-v1`、`WC-R3-DENSE-SHARE-v1`，[命题合同](assets.json) |
| [局部窄权带：存在势与跨带障碍冻结记录](<../evidence/runs/weighted_congestion/weight_bands/verification.json>) | `evidence/runs/weighted_congestion/weight_bands/verification.json` | 记录种子、有理份额样本、多资源游戏、curl、线性障碍和锐选择器的有限检查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-BAND-CURL-v1`、`WC-R3-BAND-LINEAR-v1`、`WC-R3-DENSE-LOCAL-v1`，[命题合同（共 5 项）](assets.json) |

### 可选用户填充与密度参数边界

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [潜在用户密度填充：逐倍率保持均衡的投影与提升](<current/weighted_congestion/density_padding/optional_user_density_padding.md>) | `research/current/weighted_congestion/density_padding/optional_user_density_padding.md` | 通过新增空策略/单资源玩家任意提高已占权重区间的用户数，同时保持原玩家全部偏离成本和有限倍率均衡存在性。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |
| [潜在用户密度填充：投影、提升与占权区间独立审查](<reviews/weighted_congestion/density_padding/review.md>) | `research/reviews/weighted_congestion/density_padding/review.md` | 独立证明所有有限倍率的双向保持，澄清密度下界只针对含潜在用户权重的区间，并检查零费用边界。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |
| [潜在用户填充：定义级投影与提升独立枚举](<../tests/audits/weighted_congestion/density_padding/independent_check.py>) | `tests/audits/weighted_congestion/density_padding/independent_check.py` | 直接枚举全部有限状态及偏离，不用强制空策略捷径，检查均衡投影/提升及费用边界。 | 有限计算核验；不代替一般证明；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |
| [潜在用户填充：双向保持与阶跃边界回归](<../tests/audits/weighted_congestion/density_padding/verify.py>) | `tests/audits/weighted_congestion/density_padding/verify.py` | 有限精确核验填充前后的均衡投影与提升，并保留非多项式阶跃边界的限制。 | 有限计算核验；不代替一般证明；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |
| [潜在用户填充：独立状态与倍率冻结记录](<../evidence/runs/weighted_congestion/density_padding/independent_verification.json>) | `evidence/runs/weighted_congestion/density_padding/independent_verification.json` | 记录有限游戏、倍率、增强状态组合、投影/提升及阶跃边界反例的实际检查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |
| [潜在用户填充：均衡保持与边界冻结记录](<../evidence/runs/weighted_congestion/density_padding/verification.json>) | `evidence/runs/weighted_congestion/density_padding/verification.json` | 冻结增强游戏样例、投影/提升结果与阶跃费用边界核验，不建立一般证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-POTENTIAL-DENSITY-PADDING-v1`，[命题合同](assets.json) |

### 非对称有限构造、缩权族与极限运输

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [十四资源缩权族：极限偏离锥与有限有理运输](<current/weighted_congestion/crossover/limit_family.md>) | `research/current/weighted_congestion/crossover/limit_family.md` | 研究固定四玩家拓扑的缩权极限、原振幅与重调振幅、严格端点及由极限运输回有限多项式游戏的条件。 | 数学正文；按关联命题分别核对证明及审查；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [非对称十四资源例与对称两列拓扑的有限次数分离](<current/weighted_congestion/crossover/separation.md>) | `research/current/weighted_congestion/crossover/separation.md` | 结合源公式三十二次上界和完整拓扑还原，严格区分非对称实例与全部指定对称两列游戏。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1`，[命题合同](assets.json) |
| [四玩家十四资源非对称构造：三十二次全状态证书](<current/weighted_congestion/crossover/README.md>) | `research/current/weighted_congestion/crossover/README.md` | 给出固定有理权、十四资源的完整实例与全状态偏离证书，并记录固定参数提高次数的失效边界。 | 反例；仅否定正文明确的命题；关联 `WCF-R3-CROSS32-AUDIT-v1`、`WCF-R3-FIXED-DEGREE-FAIL-v1`，[命题合同](assets.json) |
| [十四资源缩权族：布尔极限与有限运输独立审查](<reviews/weighted_congestion/crossover_limit_review/review.md>) | `research/reviews/weighted_congestion/crossover_limit_review/review.md` | 独立重建极限辅助游戏、偏离锥和有限多项式游戏，核对缩权与重调振幅结论，不替代另一个固定次数实例审查。 | 实际审查记录；只覆盖所列版本与义务；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源分离：真实策略与符号叶证书第二重构](<../tests/audits/weighted_congestion/crossover/main_check.py>) | `tests/audits/weighted_congestion/crossover/main_check.py` | 不导入两份候选核验器，直接重建策略成本并核对源公式 Bernstein 叶证书。 | 有限计算核验；不代替一般证明；关联 `WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1`、`WC-R3-SOURCE32-178-v1`、`WCF-R3-CROSS32-AUDIT-v1`，[命题合同（共 4 项）](assets.json) |
| [十四资源有限实例：独立逐资源 Fraction 核验](<../tests/audits/weighted_congestion/crossover/verify_degree32.py>) | `tests/audits/weighted_congestion/crossover/verify_degree32.py` | 不使用搜索实现或缓存矩阵，重算固定实例、次数失效和极限记录；默认比对冻结输出。 | 有限计算核验；不代替一般证明；关联 `WCF-R3-CROSS32-AUDIT-v1`、`WCF-R3-FIXED-DEGREE-FAIL-v1`，[命题合同](assets.json) |
| [十四资源缩权族：有限证书与有理误差界核验](<../tests/audits/weighted_congestion/crossover/verify_limit.py>) | `tests/audits/weighted_congestion/crossover/verify_limit.py` | 独立实现缩权族成本、有限参数证书和运输误差界；默认比较冻结结果而不覆盖。 | 有限计算核验；不代替一般证明；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源缩权族：极限与有限游戏独立重构程序](<../tests/audits/weighted_congestion/crossover_limit_review/check_independent.py>) | `tests/audits/weighted_congestion/crossover_limit_review/check_independent.py` | 不导入构造者的核验代码或证据，分别实现辅助极限和有限多项式成本及形式见证。 | 有限计算核验；不代替一般证明；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源三十二次实例：全部状态有理证书](<../evidence/certificates/weighted_congestion/crossover/degree32_certificate.json>) | `evidence/certificates/weighted_congestion/crossover/degree32_certificate.json` | 保存固定非对称游戏的每状态真实成本、改善见证、精确最优倍率和取得状态。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-CROSS32-AUDIT-v1`，[命题合同](assets.json) |
| [十四资源固定参数四十次：原非存在主张失效证书](<../evidence/certificates/weighted_congestion/crossover/degree40_failure_certificate.json>) | `evidence/certificates/weighted_congestion/crossover/degree40_failure_certificate.json` | 保存固定权与振幅仅增次数后的全部状态成本和较低因子均衡，用于精确否定该外推。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-FIXED-DEGREE-FAIL-v1`，[命题合同](assets.json) |
| [十四资源固定参数：有限次数扫描记录](<../evidence/runs/weighted_congestion/crossover/fixed_degree_scan.json>) | `evidence/runs/weighted_congestion/crossover/fixed_degree_scan.json` | 保存固定权和振幅下各所列次数的实例倍率；有限扫描不建立全部次数定理。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-FIXED-DEGREE-FAIL-v1`，[命题合同](assets.json) |
| [十四资源固定权极限：有限布尔费用证书](<../evidence/certificates/weighted_congestion/crossover/fixed_weight_limit_certificate.json>) | `evidence/certificates/weighted_congestion/crossover/fixed_weight_limit_certificate.json` | 记录保持原权和振幅时的极限辅助成本及最优倍率，限定固定参数次数外推能力。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-FIXED-DEGREE-FAIL-v1`，[命题合同](assets.json) |
| [十四资源缩权族：原振幅与重调振幅有限扫描](<../evidence/runs/weighted_congestion/crossover/limit_evidence/finite_scans.json>) | `evidence/runs/weighted_congestion/crossover/limit_evidence/finite_scans.json` | 记录两套固定振幅下明示整数参数的有限全状态核验，不替代全部参数运输证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源重调缩权族：指定整数参数全状态证书](<../evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json>) | `evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json` | 冻结指定重调振幅、有限次数、逐状态成本、严格见证余量及实例最优倍率。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源缩权族：两套振幅的极限费用记录](<../evidence/runs/weighted_congestion/crossover/limit_evidence/scaled_limits.json>) | `evidence/runs/weighted_congestion/crossover/limit_evidence/scaled_limits.json` | 保存原振幅与重调振幅辅助极限游戏的精确比较结果。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源缩权族：严格见证的统一误差界记录](<../evidence/runs/weighted_congestion/crossover/limit_evidence/uniform_bounds.json>) | `evidence/runs/weighted_congestion/crossover/limit_evidence/uniform_bounds.json` | 保存有限多项式向极限运输所用的有理界与所报告参数范围，证据限于记录的检查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |
| [十四资源分离：实例、固定参数失效与源界复核记录](<../evidence/runs/weighted_congestion/crossover/main_check_results.json>) | `evidence/runs/weighted_congestion/crossover/main_check_results.json` | 记录第二重构对非对称实例、次数外推失败及源参数符号界的实际检查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1`、`WC-R3-SOURCE32-178-v1`、`WCF-R3-CROSS32-AUDIT-v1`，[命题合同（共 4 项）](assets.json) |
| [十四资源缩权族：独立极限见证与有限运输记录](<../evidence/runs/weighted_congestion/crossover_limit_review/independent_evidence.json>) | `evidence/runs/weighted_congestion/crossover_limit_review/independent_evidence.json` | 保存辅助极限、形式见证、有限实例及所报告统一参数范围的独立有理核验。 | 冻结输入、证书或结果；不原位覆盖；关联 `WCF-R3-SCALED-ORIGINAL-v1`、`WCF-R3-SCALED-RETUNED-v2`、`WCF-R3-SCALED-TEMPLATE-v1`，[命题合同](assets.json) |

### 二次源族的标量包络

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [文献两攻击公式：二次参数包络的有理上界](<current/weighted_congestion/quadratic_source/source_family_envelope.md>) | `research/current/weighted_congestion/quadratic_source/source_family_envelope.md` | 在原整数重数和实参数域上证明两攻击倍率的共同上界，处理零分母边界；结论只属于指定源公式。 | 数学正文；按关联命题分别核对证明及审查；精确范围见本页正文 |
| [二次源公式参数域：一手文献核对](<reviews/weighted_congestion/quadratic_source/source_audit.md>) | `research/reviews/weighted_congestion/quadratic_source/source_audit.md` | 核对固定文献版本的玩家成本约定、弱均衡定义及原式整数/实参数域；不是一般数学证明审查。 | 实际审查记录；只覆盖所列版本与义务 |
| [源公式二次包络：精确多项式核对与有限探索](<../tests/audits/weighted_congestion/quadratic_source/verify.py>) | `tests/audits/weighted_congestion/quadratic_source/verify.py` | 分开执行精确代数恒等式检查和有限参数探索；数值结果不承担全参数上界的证明。 | 有限计算核验；不代替一般证明；关联 `WC-R1-SOURCE-D2-ENVELOPE`，[命题合同](assets.json) |
| [源公式二次包络：有理网格与数值探索记录](<../evidence/runs/weighted_congestion/quadratic_source/verification.json>) | `evidence/runs/weighted_congestion/quadratic_source/verification.json` | 冻结精确检查、有理网格和另行标识的数值探索，范围限所报告参数。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R1-SOURCE-D2-ENVELOPE`，[命题合同](assets.json) |

### 三玩家二次整数障碍与来源欠账

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [三玩家六资源整数实例：二次费用的精确最优倍率](<current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md>) | `research/current/weighted_congestion/quadratic_triad/three_player_integer_obstruction.md` | 保存固定整数权和一次/二次费用游戏的完整成本表、全部偏离与端点均衡；所引独立审查原件缺失另列。 | 反例；仅否定正文明确的命题；精确范围见本页正文 |
| [三玩家六资源整数例：全部状态与偏离核验](<../tests/audits/weighted_congestion/quadratic_triad/verify.py>) | `tests/audits/weighted_congestion/quadratic_triad/verify.py` | 用标准库有理算术直接重建资源负载、全部状态成本及端点近似均衡。 | 有限计算核验；不代替一般证明；关联 `WC-R1-INTEGER-TRIAD`，[命题合同](assets.json) |
| [三玩家六资源整数例：最优倍率与端点证书](<../evidence/runs/weighted_congestion/quadratic_triad/verification.json>) | `evidence/runs/weighted_congestion/quadratic_triad/verification.json` | 冻结精确权重、资源、全部状态表、最优倍率、端点均衡与比较限制。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R1-INTEGER-TRIAD`，[命题合同](assets.json) |

### 补列、多列逃逸与非分离来源缺口

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [互补多列拓扑：二倍近似均衡与三列锐性](<current/weighted_congestion/multicolumn/complement_column_escape.md>) | `research/current/weighted_congestion/multicolumn/complement_column_escape.md` | 证明共同轻权不超过重权的指定互补多列游戏总有二倍均衡，并给三列常数的渐近锐性。 | 方法障碍；否定范围以正文为准；关联 `WC-R1-MULTICOLUMN-2`，[命题合同](assets.json) |
| [互补多列拓扑：二倍存在证明独立审查](<reviews/weighted_congestion/multicolumn_review/REVIEW.md>) | `research/reviews/weighted_congestion/multicolumn_review/REVIEW.md` | 从真实列人数成本重建组合缺口，核对一般非减费用下的二倍均衡与三列边界。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R1-MULTICOLUMN-2`，[命题合同](assets.json) |
| [互补多列二倍界：真实资源与占用人数回归](<../tests/audits/weighted_congestion/multicolumn/verify.py>) | `tests/audits/weighted_congestion/multicolumn/verify.py` | 精确核对资源成本公式、轻人数状态、平衡均衡及锐性样例，有限回归不替代一般证明。 | 有限计算核验；不代替一般证明 |
| [互补多列二倍界：独立精确状态审计](<../tests/audits/weighted_congestion/multicolumn_review/verify_multicolumn.py>) | `tests/audits/weighted_congestion/multicolumn_review/verify_multicolumn.py` | 不用比值作为断言，独立核对单调费用样本、直接资源配置及较大整数实例。 | 有限计算核验；不代替一般证明 |
| [互补多列二倍界：存在与锐性样例冻结记录](<../evidence/runs/weighted_congestion/multicolumn/evidence.json>) | `evidence/runs/weighted_congestion/multicolumn/evidence.json` | 保存直接资源公式、人数状态、平衡轻玩家均衡和锐性有限检查的实际范围。 | 冻结输入、证书或结果；不原位覆盖 |
| [互补多列二倍界：独立审计冻结结果](<../evidence/runs/weighted_congestion/multicolumn_review/exact_test_results.json>) | `evidence/runs/weighted_congestion/multicolumn_review/exact_test_results.json` | 记录独立资源配置与较大整数实例的确切覆盖范围，不把有限穷举称全类证明。 | 冻结输入、证书或结果；不原位覆盖 |

### 多项式三负载曲率与三点包络

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [非负系数多项式：三负载比值的精确凸包络](<current/weighted_congestion/polynomial_curvature/three_point_polynomial_envelope.md>) | `research/current/weighted_congestion/polynomial_curvature/three_point_polynomial_envelope.md` | 精确求解三个正负载上的费用比值权衡，识别相邻单项式最优解、最小可行次数与曲率指数。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R1-THREELOAD-ENVELOPE`，[命题合同](assets.json) |
| [前缀阶跃模拟：非负系数多项式的曲率障碍](<current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md>) | `research/current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md` | 核对源前缀游戏的三个真实可达负载，并用对数负载凸性排除保持阶跃平台形状的直接多项式模拟。 | 方法障碍；否定范围以正文为准；关联 `WC-R1-PREFIX-SMOOTHING`，[命题合同](assets.json) |
| [前缀阶跃模拟：三负载曲率的独立反向审查](<reviews/weighted_congestion/polynomial_curvature/review.md>) | `research/reviews/weighted_congestion/polynomial_curvature/review.md` | 用单项式概率权重和凸性独立重构局部曲率障碍，核对真实负载、次数与适用边界。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R1-PREFIX-SMOOTHING`，[命题合同](assets.json) |
| [三负载精确凸包络：相邻单项式有限回归](<../tests/audits/weighted_congestion/polynomial_curvature/extension_verify.py>) | `tests/audits/weighted_congestion/polynomial_curvature/extension_verify.py` | 核对三负载包络公式和相邻次数支撑的有限有理样例，不替代一般优化证明。 | 有限计算核验；不代替一般证明 |
| [前缀阶跃曲率：真实负载与多项式有理回归](<../tests/audits/weighted_congestion/polynomial_curvature/verify.py>) | `tests/audits/weighted_congestion/polynomial_curvature/verify.py` | 精确检查源前缀策略的可达负载、系数向量、曲率不等式、必要次数及零/常数边界。 | 有限计算核验；不代替一般证明 |
| [前缀阶跃曲率：负载、曲率与次数边界记录](<../evidence/runs/weighted_congestion/polynomial_curvature/results.json>) | `evidence/runs/weighted_congestion/polynomial_curvature/results.json` | 冻结种子、实际权/系数域、几何与真实负载计数、曲率和次数检查及适用范围。 | 冻结输入、证书或结果；不原位覆盖 |

### 异权端点的精确还原

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [异权端点强制证书：还原为单一轻玩家权重](<current/weighted_congestion/heterogeneous_endpoint/endpoint_reduction.md>) | `research/current/weighted_congestion/heterogeneous_endpoint/endpoint_reduction.md` | 在指定两类端点强制不等式下选取一个轻权并取整重数，得到同次数同权星形反例；不涵盖所有异权无均衡游戏。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R1-HET-ENDPOINT-REDUCTION`，[命题合同](assets.json) |
| [异权端点还原：权重选择与重数取整独立审查](<reviews/weighted_congestion/heterogeneous_endpoint/review.md>) | `research/reviews/weighted_congestion/heterogeneous_endpoint/review.md` | 先独立重构端点强制命题，再核对权重选取、整数重数和有限精确程序；只覆盖该受限还原。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R1-HET-ENDPOINT-REDUCTION`，[命题合同](assets.json) |
| [异权端点还原：有理密度选择与取整回归](<../tests/audits/weighted_congestion/heterogeneous_endpoint/verify_endpoint_reduction.py>) | `tests/audits/weighted_congestion/heterogeneous_endpoint/verify_endpoint_reduction.py` | 以 Fraction 核对端点输入、轻权选择、实/整数重数、输出倍率和零主资源样例。 | 有限计算核验；不代替一般证明 |
| [异权端点还原：输入输出与取整分支冻结记录](<../evidence/runs/weighted_congestion/heterogeneous_endpoint/verification.json>) | `evidence/runs/weighted_congestion/heterogeneous_endpoint/verification.json` | 保存被核对的有理权、端点比值、所选索引、整数重数、输出倍率及边界样例。 | 冻结输入、证书或结果；不原位覆盖 |

### 辅助阶跃依赖 DAG 及迁移限制

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [辅助阶跃依赖游戏：有向无环图的精确阈值](<current/weighted_congestion/step_dag/step_dependency_threshold.md>) | `research/current/weighted_congestion/step_dag/step_dependency_threshold.md` | 以有向路径计数给出指定阶跃费用辅助模型的振幅最优阈值和端点取得；未把阶跃费用迁入多项式全类。 | 数学正文；按关联命题分别核对证明及审查；关联 `WC-R1-DAG-STEP`，[命题合同](assets.json) |
| [辅助阶跃依赖模型：树与有向无环图独立重构](<reviews/weighted_congestion/step_dag/independent_review.md>) | `research/reviews/weighted_congestion/step_dag/independent_review.md` | 独立核对源前缀策略并证明阶跃图模型阈值，覆盖零振幅、空图和严格负载边界；不声称多项式迁移。 | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R1-DAG-STEP`，[命题合同](assets.json) |
| [辅助阶跃图模型：独立逐资源成本与阈值审计](<../tests/audits/weighted_congestion/step_dag/independent_audit.py>) | `tests/audits/weighted_congestion/step_dag/independent_audit.py` | 不导入原证明或核验器，以整数缩放的正二进权从策略重建树/DAG 阶跃负载和偏离。 | 有限计算核验；不代替一般证明 |
| [辅助阶跃依赖模型：真实资源与递推阈值回归](<../tests/audits/weighted_congestion/step_dag/verify.py>) | `tests/audits/weighted_congestion/step_dag/verify.py` | 用精确资源成本检查明示 DAG 游戏及路径计数递推，不使用浮点、随机或外部核验器。 | 有限计算核验；不代替一般证明 |
| [辅助阶跃依赖模型：路径计数与边界冻结记录](<../evidence/runs/weighted_congestion/step_dag/verification.json>) | `evidence/runs/weighted_congestion/step_dag/verification.json` | 保存参数、实际精确样例与检查计数；仅支持阶跃辅助模型，不是多项式迁移证书。 | 冻结输入、证书或结果；不原位覆盖 |

### 固定边际势与任意乘子候选障碍

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [任意玩家乘子势：有限多尺度边际夹逼障碍候选](<questions/weighted_congestion/marginal_potentials/arbitrary_multipliers.md>) | `research/questions/weighted_congestion/marginal_potentials/arbitrary_multipliers.md` | 候选推广允许乘子依赖整个有限权向量；研究单资源全部子集上的边际夹逼，不是游戏均衡非存在。 | 候选或未闭合义务；保存不升级状态；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [按玩家权重校准的边际势：线性障碍候选](<questions/weighted_congestion/marginal_potentials/fixed_marginal_potential_obstruction.md>) | `research/questions/weighted_congestion/marginal_potentials/fixed_marginal_potential_obstruction.md` | 用有限两种插入次序给出权重校准边际夹逼的次数线性障碍；保留尚待进一步独立审查状态。 | 候选或未闭合义务；保存不升级状态 |
| [权重校准边际势：两种插入次序精确证书核验](<../tests/audits/weighted_congestion/marginal_potentials/verify.py>) | `tests/audits/weighted_congestion/marginal_potentials/verify.py` | 用 Fraction 比较有限权向量的两条插入路径；Decimal 仅用于显示，不由优化或样本提升一般障碍。 | 有限计算核验；不代替一般证明 |
| [任意玩家乘子：有限多尺度压缩证书核验](<../tests/audits/weighted_congestion/marginal_potentials/verify_multipliers.py>) | `tests/audits/weighted_congestion/marginal_potentials/verify_multipliers.py` | 精确检查允许任意正玩家乘子的多尺度有限压缩证书，不替代候选一般证明的独立审查。 | 有限计算核验；不代替一般证明；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [权重校准边际势：路径比与证据限制冻结记录](<../evidence/runs/weighted_congestion/marginal_potentials/evidence.json>) | `evidence/runs/weighted_congestion/marginal_potentials/evidence.json` | 保存有限两序列证书、精确路径比与本次运行没有建立的结论；正文仍按候选状态使用。 | 冻结输入、证书或结果；不原位覆盖 |
| [任意玩家乘子：多尺度有限证书冻结记录](<../evidence/runs/weighted_congestion/marginal_potentials/multiplier_evidence.json>) | `evidence/runs/weighted_congestion/marginal_potentials/multiplier_evidence.json` | 保存明示参数下任意乘子障碍的有限精确证书，不能把入库本身当作候选通过审查。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |

### 序势候选、稠密桥与方法限制

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [资源可分序势的线性障碍：任意乘子与同一有限游戏](<current/weighted_congestion/separable_ordinal_obstruction.md>) | `research/current/weighted_congestion/separable_ordinal_obstruction.md` | 在尝试全类上界时，读取有限多尺度乘子矛盾和同一游戏资源束桥的完整现行证明；区分全改善边势证书与真正均衡存在。；配套 [依游戏可分序势障碍：冻结证明的独立重构与攻击](<reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md>)；配套 [有限资源束桥：路径和、严格取整与非匿名平均核验](<../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py>)；配套 [有限资源束桥：独立有理审计冻结结果](<../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json>) | 方法障碍；否定范围以正文为准；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [依游戏选择的资源可分序势：线性障碍候选](<questions/weighted_congestion/ordinal_potentials/game_specific_separable_ordinal_barrier.md>) | `research/questions/weighted_congestion/ordinal_potentials/game_specific_separable_ordinal_barrier.md` | 允许每个资源集合函数在看到完整游戏后选择，研究全部严格改善边下降的可分势障碍；所构游戏仍有精确均衡。 | 候选或未闭合义务；保存不升级状态；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [玩家成本幂和目标：全局最小点的无界改善反例](<questions/weighted_congestion/ordinal_potentials/power_of_total_cost_obstruction.md>) | `research/questions/weighted_congestion/ordinal_potentials/power_of_total_cost_obstruction.md` | 对非一次成本幂和给出仿射费用有限游戏，使唯一目标最小点存在任意大改善；不否定均衡本身。 | 候选或未闭合义务；保存不升级状态 |
| [普适资源可加序势：由复制规则推出局部边际夹逼](<questions/weighted_congestion/ordinal_potentials/universal_additive_ordinal_bridge.md>) | `research/questions/weighted_congestion/ordinal_potentials/universal_additive_ordinal_bridge.md` | 在规则不能依赖策略族和其他资源的精确条件下，将全游戏序势下降要求还原为共享玩家乘子的局部夹逼。 | 候选或未闭合义务；保存不升级状态 |
| [非可分选择目标：幂和、乘积与对数目标反例审查](<reviews/weighted_congestion/multicolumn_review/NONSEPARABLE_REVIEW.md>) | `research/reviews/weighted_congestion/multicolumn_review/NONSEPARABLE_REVIEW.md` | 审查指定目标的坏全局最小点族；原 frontier 证明/程序缺失需单列，此审查记录不冒充完整原资产。 | 实际审查记录；只覆盖所列版本与义务 |
| [资源可分序势与成本幂目标：内部审查记录](<reviews/weighted_congestion/ordinal_potentials/REVIEW.md>) | `research/reviews/weighted_congestion/ordinal_potentials/REVIEW.md` | 逐项记录成本幂目标、普适复制桥与游戏依赖可分势候选的内部审查覆盖；不认证一般存在或非存在。 | 实际审查记录；只覆盖所列版本与义务 |
| [依游戏可分序势障碍：冻结证明的独立重构与攻击](<reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md>) | `research/reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md` | 核查冻结commit/hash、任意乘子依赖、先固定资源数的量词、取整严格性与零成本边界；只覆盖所列方法障碍。；配套 [资源可分序势的线性障碍：任意乘子与同一有限游戏](<current/weighted_congestion/separable_ordinal_obstruction.md>)；配套 [有限资源束桥：路径和、严格取整与非匿名平均核验](<../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py>)；配套 [有限资源束桥：独立有理审计冻结结果](<../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json>) | 实际审查记录；只覆盖所列版本与义务；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [成本幂和目标：坏最小点的真实资源有理核验](<../tests/audits/weighted_congestion/ordinal_potentials/verify_power_objective.py>) | `tests/audits/weighted_congestion/ordinal_potentials/verify_power_objective.py` | 重建有限仿射游戏成本；半次幂目标使用精确根式比较，其余比较使用 Fraction。 | 有限计算核验；不代替一般证明 |
| [有限资源束桥：路径和、严格取整与非匿名平均核验](<../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py>) | `tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py` | 用Fraction直接幂和对照压缩实现，检查严格束大小界和资源置换平均；不枚举巨型游戏或替代一般证明。；配套 [资源可分序势的线性障碍：任意乘子与同一有限游戏](<current/weighted_congestion/separable_ordinal_obstruction.md>)；配套 [依游戏可分序势障碍：冻结证明的独立重构与攻击](<reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md>)；配套 [有限资源束桥：独立有理审计冻结结果](<../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json>) | 有限计算核验；不代替一般证明；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |
| [成本幂和目标：有限坏最小点冻结记录](<../evidence/runs/weighted_congestion/ordinal_potentials/power_objective_exact_checks.json>) | `evidence/runs/weighted_congestion/ordinal_potentials/power_objective_exact_checks.json` | 保存逐实例的精确成本与目标比较，支持指定目标选择失败，不作为均衡非存在证据。 | 冻结输入、证书或结果；不原位覆盖 |
| [有限资源束桥：独立有理审计冻结结果](<../evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json>) | `evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json` | 保存实际运行命令、确定性参数范围、代码及依赖hash与检查数量，使后续审计能独立重放有限实现范围。；配套 [资源可分序势的线性障碍：任意乘子与同一有限游戏](<current/weighted_congestion/separable_ordinal_obstruction.md>)；配套 [依游戏可分序势障碍：冻结证明的独立重构与攻击](<reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md>)；配套 [有限资源束桥：路径和、严格取整与非匿名平均核验](<../tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py>) | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER`、`WC-R1-MULTIPLIER-BARRIER`，[命题合同](assets.json) |

### 保守多项式端点候选与侧列还原

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [保守两攻击证书：任意多项式向单项式的还原候选](<questions/weighted_congestion/polynomial_endpoint/conservative_endpoint_candidate.md>) | `research/questions/weighted_congestion/polynomial_endpoint/conservative_endpoint_candidate.md` | 对指定对称两列的两条保守严格证书同时约化主副多项式与轻权；不把充分证书当完整拓扑必要条件。 | 候选或未闭合义务；保存不升级状态 |
| [保守两攻击证书：副资源多项式的端点还原](<questions/weighted_congestion/polynomial_endpoint/side_polynomial/Q_ENDPOINT_REDUCTION.md>) | `research/questions/weighted_congestion/polynomial_endpoint/side_polynomial/Q_ENDPOINT_REDUCTION.md` | 保持主资源多项式和合法轻权，将可行副资源多项式改为最高次单项式；其本地内部复核与整体候选状态分别读取。 | 候选或未闭合义务；保存不升级状态 |
| [副资源端点还原：显式系数与余量有理回归](<../tests/audits/weighted_congestion/polynomial_endpoint/side_polynomial/check_q_endpoint.py>) | `tests/audits/weighted_congestion/polynomial_endpoint/side_polynomial/check_q_endpoint.py` | 检查保守两攻击证书中副资源端点替换的系数及严格余量恒等式，仅覆盖有限参数。 | 有限计算核验；不代替一般证明 |
| [保守两攻击多项式还原：有理参数与边界回归](<../tests/audits/weighted_congestion/polynomial_endpoint/verify.py>) | `tests/audits/weighted_congestion/polynomial_endpoint/verify.py` | 检查端点替换、可行证书还原、边界和保守证书适用范围样例；不使用浮点优化。 | 有限计算核验；不代替一般证明 |
| [保守两攻击多项式还原：端点与边界冻结记录](<../evidence/runs/weighted_congestion/polynomial_endpoint/verification.json>) | `evidence/runs/weighted_congestion/polynomial_endpoint/verification.json` | 保存有限有理还原计数、具体例、边界及保守证书和实际游戏范围的区分。 | 冻结输入、证书或结果；不原位覆盖 |

### 带符号列、三元组与扩展候选

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [互补符号列：有限证书与增长支持族的开放扩展](<questions/weighted_congestion/signed_columns/TRIAD_AND_EXTENSION.md>) | `research/questions/weighted_congestion/signed_columns/TRIAD_AND_EXTENSION.md` | 保存三玩家机制、四玩家有限有理证书和增长支持构造；浮点筛选仅用于发现，尚无新的渐近全状态证明。 | 候选或未闭合义务；保存不升级状态 |
| [互补符号列：增长支持的浮点筛选程序](<../tests/audits/weighted_congestion/signed_columns/search_layers.py>) | `tests/audits/weighted_congestion/signed_columns/search_layers.py` | 用浮点 MILP 筛选全支持符号列候选；发现结果须经独立有理成本计算，不是精确证书。 | 有限计算核验；不代替一般证明 |
| [互补符号列：三玩家与四玩家全状态有理核验](<../tests/audits/weighted_congestion/signed_columns/verify.py>) | `tests/audits/weighted_congestion/signed_columns/verify.py` | 直接重算互补资源构造，检查原三玩家、取整四玩家及筛选后有理化实例。 同时有限核验真实偏离的资源支持势不等式，支持界不是独立的一般证明。 | 有限计算核验；不代替一般证明；关联 `WC-R1-RESOURCE-SUPPORT`，[命题合同](assets.json) |
| [互补符号列：浮点筛选候选记录](<../evidence/runs/weighted_congestion/signed_columns/screening.json>) | `evidence/runs/weighted_congestion/signed_columns/screening.json` | 保存增长支持搜索的发现数据；只有另行通过有理核验的条目可作有限非存在证据。 | 冻结输入、证书或结果；不原位覆盖 |
| [互补符号列：有限实例有理证书冻结记录](<../evidence/runs/weighted_congestion/signed_columns/verification.json>) | `evidence/runs/weighted_congestion/signed_columns/verification.json` | 记录三玩家、四玩家取整例及有理化筛选候选的精确核验，不建立增长族一般结论。 同时有限核验真实偏离的资源支持势不等式，支持界不是独立的一般证明。 | 冻结输入、证书或结果；不原位覆盖；关联 `WC-R1-RESOURCE-SUPPORT`，[命题合同](assets.json) |

### 协作、保存、启动与许可入口

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [拥塞匹配上界命题的唯一完成标准与交付验收](<weighted_congestion_frontier/ACCEPTANCE.md>) | `research/weighted_congestion_frontier/ACCEPTANCE.md` | 判断全类匹配上界命题是否已获一般肯定或严格否定证明；核对规模无关常数、独立攻击、残余异议与完整入库，不把局部材料当题目完成。 | 阅读导航；真值查精确正文及账本 |
| [拥塞协作贡献规则与阶段保存要求](<weighted_congestion_frontier/AGENTS.md>) | `research/weighted_congestion_frontier/AGENTS.md` | 加入该研究目录前核对适用工作规则、子 agent 协作方式及数学入库和状态升级的边界。 | 阅读导航；真值查精确正文及账本 |
| [阶段成果一键保存：提交范围、失败恢复与远端确认](<weighted_congestion_frontier/CHECKPOINT.md>) | `research/weighted_congestion_frontier/CHECKPOINT.md` | 已有可复用阶段文件后选择正确路径运行保存，遇到同步冲突或断网时按实际失败状态恢复。 | 阅读导航；真值查精确正文及账本 |
| [研究公屏协议：具体交流、版本与来源](<weighted_congestion_frontier/PROTOCOL.md>) | `research/weighted_congestion_frontier/PROTOCOL.md` | 需要跨对话讨论发现、异议或合作问题时查消息语义和冻结版本；公屏不代替规范研究资产。 | 阅读导航；真值查精确正文及账本 |
| [共同研究操作手册：恢复、读屏、同步与保存](<weighted_congestion_frontier/RUNBOOK.md>) | `research/weighted_congestion_frontier/RUNBOOK.md` | 实际操作协作程序时查入口和认证配置；不把程序回归或网络状态当作数学结果。 | 阅读导航；真值查精确正文及账本 |
| [异步公屏的定位、读取入口与资产边界](<weighted_congestion_frontier/board/README.md>) | `research/weighted_congestion_frontier/board/README.md` | 需要查看实时研讨时进入独立公屏分支；重要可复用成果必须另存 main 并连接真实正文。 | 阅读导航；真值查精确正文及账本 |
| [拥塞可复用工具的提取与使用合同](<weighted_congestion_frontier/toolbox/README.md>) | `research/weighted_congestion_frontier/toolbox/README.md` | 从失败和中间推导提取工具时查原作者、精确假设、证明与复用场景，不能把改名本身当新工具。 | 阅读导航；真值查精确正文及账本 |
| [匹配上界唯一题目的共同研究启动词](<weighted_congestion_frontier/prompts/TEAM.md>) | `research/weighted_congestion_frontier/prompts/TEAM.md` | 新对话判定全类匹配上界命题，固定模型与完成门槛；规定中文命名、分层地图、生成检查及完整提交，缺少可选程序附件也能恢复。 | 阅读导航；真值查精确正文及账本 |
| [同级研究者交流提示词：自主研究与异步研讨](<weighted_congestion_frontier/prompts/PEER.md>) | `research/weighted_congestion_frontier/prompts/PEER.md` | 需要组织跨对话数学交流时使用，允许同题独立探索和多路线合作，不以任务认领限制研究。 | 阅读导航；真值查精确正文及账本 |
| [数学工具提取者提示词：从中间结果回收结构](<weighted_congestion_frontier/prompts/EXTRACTOR.md>) | `research/weighted_congestion_frontier/prompts/EXTRACTOR.md` | 独立重建可复用引理、表示、障碍或桥梁，保留出处和承重条件，提供实际复用场景并诚实验收。 | 阅读导航；真值查精确正文及账本 |
| [论文整理者提示词：真实贡献、完整论证与成稿核验](<weighted_congestion_frontier/prompts/PAPER_WRITER.md>) | `research/weighted_congestion_frontier/prompts/PAPER_WRITER.md` | 出现足够成果后组织论文叙事、证明与图表，执行写作和逐页检查；包装不能改变精确范围或证据等级。 | 阅读导航；真值查精确正文及账本 |
| [子 agent 模型配置、实际能力与来源记录](<weighted_congestion_frontier/prompts/MODELS.md>) | `research/weighted_congestion_frontier/prompts/MODELS.md` | 启动独立探索或审查时查实际可用模型与配置的记录要求，不能把模型自评当成数学可信度。 | 阅读导航；真值查精确正文及账本 |
| [协作与写作参考原文的固定版本及许可](<weighted_congestion_frontier/SOURCES.md>) | `research/weighted_congestion_frontier/SOURCES.md` | 修改提示词或核对外部设计来源时查固定 commit、引用范围和许可证，区分原设计与本仓定制。 | 来源与恢复指针；不代替缺失证明 |

<a id="shared"></a>

## 共同目录双设施

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [共同选址目录的模型、精确续局与菜单充分条件](<current/shared/model.md>) | `research/current/shared/model.md` | 固定共同目录、同址、强制参与和独立混合约定；引用黄金比结果前先核对对象与续局量词。 | 定义与模型；不隐含跨模型定理 |
| [共同目录黄金比存在性、构造与证书的分离陈述](<current/shared/theorems.md>) | `research/current/shared/theorems.md` | 分别登记普遍存在性、位多项式构造、局部强弦和单实例证书，防止混用数学保证。 | 精确命题登记；摘要不替代原陈述；关联 `SC-PHI-A`、`SC-PHI-E`、`SC-PHI-SHARP`，[命题合同](assets.json) |
| [共同目录黄金比上界的全局证明主链](<current/shared/proof.md>) | `research/current/shared/proof.md` | 组织受保护修复、坏回应环、严格支配与双锚覆盖；由各分支页补齐具体推导。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-PHI-A`、`SC-PHI-E`，[命题合同](assets.json) |
| [重客户对的容量约束与三角回应环排除](<current/shared/heavy_pairs.md>) | `research/current/shared/heavy_pairs.md` | 展开 G1 的重客户对容量界、同对回应边矛盾和三角闭集严格下降。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-PHI-A`、`SC-PHI-E`，[命题合同](assets.json) |
| [星心与双锚覆盖的黄金比闭环证明](<current/shared/star_anchors.md>) | `research/current/shared/star_anchors.md` | 展开 G2/G3 的首边、星心、中心引理、锚点选择及两支终局。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-PHI-A`、`SC-PHI-E`，[命题合同](assets.json) |
| [配额精确均衡与局部强弦的完整构造](<current/shared/local_chord_full.md>) | `research/current/shared/local_chord_full.md` | 完整重建 L1/L2 的可行性分支、端点交换、多项式迭代和位长，补足主证明局部接口。 | 数学正文；按关联命题分别核对证明及审查；关联 `LOCAL-CHORD-IFF`、`LOCAL-CHORD-POLY`、`SC-PHI-A`，[命题合同（共 4 项）](assets.json) |
| [黄金比有限菜单搜索与完整续局证书规范](<current/shared/algorithm.md>) | `research/current/shared/algorithm.md` | 说明固定 P/E/T/C 菜单、搜索伪代码、验证语义、复杂度及实现边界。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-PHI-A`、`SC-PHI-E`，[命题合同](assets.json) |
| [黄金比尖锐性的六地点下界与有理扰动](<current/shared/sharp_phi_lower.md>) | `research/current/shared/sharp_phi_lower.md` | 给共同目录全布局偏离下界和统一有理化；与已登记上界合成尖锐阈值。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-PHI-SHARP`、`SC-SPARSE-3`、`SC-SPARSE-4`，[命题合同（共 4 项）](assets.json) |
| [实例最优倍率的同址正规形与异址交叠参数](<current/shared/instance_complexity_barriers.md>) | `research/current/shared/instance_complexity_barriers.md` | 用共同目录正规形缩减精确支持枚举；分开两地点、等 reach、稀疏两 reach 与多交叠障碍。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-DIAG-NORMAL`、`SC-EQUAL-REACH-EXACT`、`SC-OFFDIAG-FPT`，[命题合同（共 6 项）](assets.json) |
| [共同目录单交叠的小地点数尖锐门槛](<current/shared/small_sparse_catalogs.md>) | `research/current/shared/small_sparse_catalogs.md` | 在不同地点单交叠条件下，分别给至多一、二、三、四、五地点的尖锐门槛 1、1、√2、∛4、φ，不能扩至多共有客户。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-SPARSE-3`、`SC-SPARSE-4`、`SC-SPARSE-5`，[命题合同](assets.json) |
| [三地点固定倍率判定的弱 NP 完全性与守卫边界](<current/shared/three_site_exact_hardness.md>) | `research/current/shared/three_site_exact_hardness.md` | 对每个固定有理 1≤a<(1+√3)/2 给全布局弱 NP 完全性，并记录向更高倍率延伸的严格权重预算障碍。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-THREE-DEC1-HARD`、`SC-THREE-DECa-HARD`，[命题合同](assets.json) |
| [五地点全部亚黄金比固定倍率的弱 NP 完全性](<current/shared/five_site_exact_hardness.md>) | `research/current/shared/five_site_exact_hardness.md` | 对每个固定有理 1<a<φ，以三态源、桥宏原子和全部带标签布局给弱 NP 完全性及位界；构造器与审计分开。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-FIVE-DECa-HARD`，[命题合同](assets.json) |
| [四共同地点实例最优倍率的无 FPTAS 间隙](<current/shared/four_site_no_fptas.md>) | `research/current/shared/four_site_no_fptas.md` | 在正整数权与所有实概率精确续局下建立全局 PARTITION 间隙；PTAS 问题仍开放。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-FOUR-NO-FPTAS`，[命题合同](assets.json) |
| [原子粒度、可拆分对照与实例敏感近似续局](<current/shared/atomic_granularity.md>) | `research/current/shared/atomic_granularity.md` | 由原子局部误差构造完整近似续局，并识别固定坏倍率输入所需的宏原子。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-GRANULAR-APPROX`，[命题合同](assets.json) |
| [固定重客户支持的近平衡精确均衡补全](<current/shared/near_band_completion.md>) | `research/current/shared/near_band_completion.md` | 给四个完整局部分支与位长；可作实例最优 EPTAS 候选的工具，不等于通用 EPTAS。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-TWO-NEAR-BAND-REP`，[命题合同](assets.json) |
| [共同目录双设施：黄金比主链、尖锐下界与复杂度地图](<current/shared/README.md>) | `research/current/shared/README.md` | 依次进入模型、黄金比完整证明和构造，再选择尖锐下界、小目录复杂度或局部补全工具。 | 阅读导航；真值查精确正文及账本 |
| [共同目录双设施实例最优倍率的 EPTAS 候选义务](<questions/shared_alpha_eptas.md>) | `research/questions/shared_alpha_eptas.md` | 使用少量重支持与近带精确补全，检查全局近似误差、精确客户均衡和位复杂度，不能报作完整算法定理。 | 候选或未闭合义务；保存不升级状态 |
| [共同目录双设施实例最优倍率判定的原问题与现行边界](<questions/instance_complexity.md>) | `research/questions/instance_complexity.md` | 固定倍率全局弱 NP 完全性已获内部结果；恰三四地点的高倍率细分类及新输入倍率合同仍须单独立项。 | 问题记录；开放/已闭合部分见用途及正文 |

<a id="heterogeneous"></a>

## 异构目录双设施

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [异构目录因子二候选的四种子纯均衡算法](<current/heterogeneous/four_seed_algorithm.md>) | `research/current/heterogeneous/four_seed_algorithm.md` | 从局部纯修复连接全目录威胁和离轨选择；一般上界仍按内部候选使用。 | 数学正文；按关联命题分别核对证明及审查；关联 `HC-2-LOW`、`HC-2-SHARP`、`HC-2-UP`，[命题合同](assets.json) |
| [四种子候选算法的任意长度交替回应环论证](<current/heterogeneous/full_catalog_cycle.md>) | `research/current/heterogeneous/full_catalog_cycle.md` | 给全环最大原子与统一客户身份压缩的关键不等式，是一般因子二候选的承重步骤。 | 数学正文；按关联命题分别核对证明及审查；关联 `HC-2-LOW`、`HC-2-SHARP`、`HC-2-UP`，[命题合同](assets.json) |
| [异构目录趋近因子二的六顶点整数下界族](<current/heterogeneous/sharp_two_lower.md>) | `research/current/heterogeneous/sharp_two_lower.md` | 以严格占优和唯一客户续局计算实例最优倍率；不单独证明普遍因子二上界。 | 数学正文；按关联命题分别核对证明及审查；关联 `HC-2-LOW`、`HC-2-SHARP`、`HC-2-UP`，[命题合同（共 4 项）](assets.json) |
| [单交叠且一侧短目录的尖锐 ρ 阈值](<current/heterogeneous/restricted_rho.md>) | `research/current/heterogeneous/restricted_rho.md` | 在跨对至多一共有客户且至少一目录至多两个行动时证明纯上界与唯一续局下界。 | 数学正文；按关联命题分别核对证明及审查；关联 `HC-RHO`，[命题合同](assets.json) |
| [任意长单交叠异构目录的尖锐 ρ 阈值](<current/heterogeneous/sparse_unbounded_rho.md>) | `research/current/heterogeneous/sparse_unbounded_rho.md` | 以首个高区到低区入口、同一客户身份及三次式闭合全长上界，接短目录下界。 | 数学正文；按关联命题分别核对证明及审查；关联 `SPARSE-RHO-ALL`，[命题合同](assets.json) |
| [单交叠坏回应环的低 reach 必经与平衡子类](<current/heterogeneous/sparse_high_reach_barrier.md>) | `research/current/heterogeneous/sparse_high_reach_barrier.md` | 给任意环长的高区严格下降和平衡 reach 子类上界，是全类 ρ 证明的前置引理。 | 数学正文；按关联命题分别核对证明及审查；关联 `SPARSE-BALANCED-R`、`SPARSE-HIGH-ACYCLIC`、`SPARSE-RHO-ALL`，[命题合同](assets.json) |
| [全目录回应核心提升与纯客户费用单调迁移](<current/heterogeneous/core_lift_and_monotone.md>) | `research/current/heterogeneous/core_lift_and_monotone.md` | 说明独立续局选择如何保留全目录威胁，并限定纯构造向单调费用迁移的适用域。 | 数学正文；按关联命题分别核对证明及审查；关联 `CORE-LIFT`、`HC-MONOTONE`，[命题合同](assets.json) |
| [单交叠目录不存在统一短精确回应核心](<current/heterogeneous/sparse_long_cycles.md>) | `research/current/heterogeneous/sparse_long_cycles.md` | 显式构造任意长全目录精确威胁闭核心，否定固定大小核心压缩；不反驳 ρ 存在性。 | 方法障碍；否定范围以正文为准；关联 `SPARSE-LONG-CYCLE`，[命题合同](assets.json) |
| [全部亚 ρ 倍率的真实坏长环与版本边界](<current/heterogeneous/sparse_bad_long_cycles.md>) | `research/current/heterogeneous/sparse_bad_long_cycles.md` | 保留旧 3/2<r<ρ 版本及新 1≤r<ρ 版本；真实坏倍率、唯一 NE 与任意长回应环不削弱 ρ 上界。 | 方法障碍；否定范围以正文为准；关联 `SPARSE-BAD-LONG`、`SPARSE-BAD-LONG-ALL`，[命题合同](assets.json) |
| [异构目录双设施：一般候选、单交叠锐界与长环地图](<current/heterogeneous/README.md>) | `research/current/heterogeneous/README.md` | 先分清一般多交叠候选、短目录和任意长单交叠的证明范围，再选择真实回应环和边界工具。 | 阅读导航；真值查精确正文及账本 |
| [任意长单交叠异构目录的锐阈值原问题与证明入口](<questions/sparse_catalogs.md>) | `research/questions/sparse_catalogs.md` | 原锐阈值已由全类单交叠证明内部闭合；保留量词、原探索路线和真实 NE 区间供复核。 | 问题记录；开放/已闭合部分见用途及正文 |

<a id="local_and_exact"></a>

## 双设施局部均衡与精确算法

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [双设施固定布局的精确均衡谱与配额强弦](<current/local_and_exact/local_geometry_and_chord.md>) | `research/current/local_and_exact/local_geometry_and_chord.md` | 从客户最佳回应推导支持单元完备性，并连接双配额可行性与强弦构造的完整证明。 | 数学正文；按关联命题分别核对证明及审查；关联 `LOCAL-CHORD-IFF`、`LOCAL-CHORD-POLY`，[命题合同](assets.json) |
| [实例最优精确算法、局部困难性与费用扩展](<current/local_and_exact/exact_algorithms_and_extensions.md>) | `research/current/local_and_exact/exact_algorithms_and_extensions.md` | 统一支持枚举、整数 DP、MITM、参数算法及二次等价、多面体续局；分别标明已实现和未实现部分。 | 数学正文；按关联命题分别核对证明及审查；关联 `DP-W`、`EXACT-KAPPA`、`FPT-D`，[命题合同（共 10 项）](assets.json) |
| [任意设施数原子均衡与 Wardrop 负载的尖锐误差](<current/local_and_exact/atomic_wardrop_gap.md>) | `research/current/local_and_exact/atomic_wardrop_gap.md` | 以运输耦合比较固定布局原子客户 NE 与可拆分负载；链族给坐标误差取等，不推出全局 SPE。 | 数学正文；按关联命题分别核对证明及审查；关联 `LOCAL-ATOM-WARDROP-k`，[命题合同](assets.json) |
| [双设施局部均衡：支持几何、强弦与精确求解地图](<current/local_and_exact/README.md>) | `research/current/local_and_exact/README.md` | 固定布局需要全部均衡收益、局部配额或精确证书时读；不能将局部结果直接充作全局存在性。 | 阅读导航；真值查精确正文及账本 |
| [立方期望客户费用下的双设施普遍阈值问题](<questions/cubic_costs.md>) | `research/questions/cubic_costs.md` | 费用改为实现负载立方的期望后，重建局部均衡与配额；已知纯单调迁移不保证混合均衡等价。 | 问题记录；开放/已闭合部分见用途及正文 |

<a id="multi_facility"></a>

## 任意设施数与完整盒构造

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [任意设施数共同目录的模型与完整续局量词](<current/multi_facility/model.md>) | `research/current/multi_facility/model.md` | 固定带标签设施、真实条件成本、同址独立均匀随机化和默认续局；所有多设施结论的定义入口。 | 定义与模型；不隐含跨模型定理；关联 `MF-CONT-COMPLETE`、`MF-PACK-2`、`MF-PURE-CAP`，[命题合同（共 7 项）](assets.json) |
| [任意设施数因子二及算法边界的精确命题账本](<current/multi_facility/claims.md>) | `research/current/multi_facility/claims.md` | 逐项给命题身份、依赖、证据与范围；区分普遍存在、有限构造、结构类多项式算法和障碍。 | 精确命题登记；摘要不替代原陈述；关联 `MF-FROZEN-OVERLOAD-POLY`、`MF-PURE-CAP-POLY`、`SC-K-ADAPTIVE-DOUBLE-LPT-2`，[命题合同（共 55 项）](assets.json) |
| [任意设施数因子二存在性的完整证明](<current/multi_facility/uniform_two.md>) | `research/current/multi_facility/uniform_two.md` | 以全局字典序极大、转移预算、原子装箱及离轨精确均衡组装完整续局；不声称一般多项式构造。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-CONT-COMPLETE`、`MF-PACK-2`、`MF-PURE-CAP`，[命题合同（共 48 项）](assets.json) |
| [因子二存在证明的逆向重构与实质异议审查](<current/multi_facility/reverse_review.md>) | `research/current/multi_facility/reverse_review.md` | 从目标离轨上界反推证明义务，记录独立实现证据和异议；不等于外部同行评审。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-CONT-COMPLETE`、`MF-PACK-2`、`MF-PURE-CAP`，[命题合同（共 7 项）](assets.json) |
| [任意规范贪心占位的完整盒均衡与有限构造](<current/multi_facility/greedy_box_global_progress.md>) | `research/current/multi_facility/greedy_box_global_progress.md` | 交错阈值势与归家计数证明完整盒总有精确客户 NE，修复过程有限终止；一般步数无多项式界。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-K-BOX-STRUCTURED-POLY-2`、`SC-K-GREEDY-BOX-EXISTS`、`SC-K-GREEDY-BOX-FINITE-2`，[命题合同](assets.json) |
| [因子二位多项式构造的算法族、接口与障碍](<current/multi_facility/polytime_frontier.md>) | `research/current/multi_facility/polytime_frontier.md` | 分开在轨选择与离轨补全；集中登记全局优化困难、PLS 局部搜索、贪心预算、重数类算法及具体反例。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 48 项）](assets.json) |
| [等重可移动轻客户的无约束流均衡构造](<current/multi_facility/equal_light_flow.md>) | `research/current/multi_facility/equal_light_flow.md` | 证明无约束全局势最小解自动保完整盒和 H，给规范 Bellman–Ford 实现与位界；不同轻权仍开放。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-K-EQUAL-LIGHT-FLOW-2`、`SC-K-EQUAL-LIGHT-FLOW-BOX`，[命题合同](assets.json) |
| [盒均衡的客户类型压缩与参数化精确算法](<current/multi_facility/type_compression.md>) | `research/current/multi_facility/type_compression.md` | 以目录和权值类型压缩客户状态，给固定参数选择及有界目录、权值多样性的 XP 因子二构造。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [有界关联树宽与客户度的盒均衡动态规划](<current/multi_facility/bounded_incidence_box.md>) | `research/current/multi_facility/bounded_incidence_box.md` | 在固定个体关联树宽和双侧客户度下精确选择完整盒 NE；站点邻接有界不能替代个体度约束。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 46 项）](assets.json) |
| [站点树宽与局部权值多样性下的盒均衡动态规划](<current/multi_facility/local_weight_box_dp.md>) | `research/current/multi_facility/local_weight_box_dp.md` | 固定站点 primal 树宽和每站点关联轻权种类时给精确位多项式选择；每条边客户数可无界。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 46 项）](assets.json) |
| [开站有向轻图深度至多二的盒均衡存在性](<current/multi_facility/height_two_box.md>) | `research/current/multi_facility/height_two_box.md` | 覆盖分叉、汇合和不等轻权；给存在论而非一般多项式受限势选择器，后由全盒定理扩展。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [三站不等轻权开站链的盒均衡存在性](<current/multi_facility/three_site_chain_box.md>) | `research/current/multi_facility/three_site_chain_box.md` | 用上游原客户池的势交换证明盒内均衡；不独立给多项式选择器。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [三轻客户汇合四站路径的有界步盒均衡构造](<current/multi_facility/converging_path_box.md>) | `research/current/multi_facility/converging_path_box.md` | 在汇合点下盒紧等条件下给有限步构造，处理非单向链取向；与后续四步扩展分别保留。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [汇合四站轻路径的四步严格改善构造](<current/multi_facility/converging_four_moves.md>) | `research/current/multi_facility/converging_four_moves.md` | 在每边一名轻客户条件下移除旧构造的汇合点紧等与部分重数相等假设。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [指向晚开中心的不等轻权星形盒均衡算法](<current/multi_facility/inward_star_box.md>) | `research/current/multi_facility/inward_star_box.md` | 以队列处理朝晚开中心的轻边；容许中心任意多不同轻权，补足另一取向星形算法。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-PURE-CAP-POLY`、`SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2`、`SC-K-BOX-NE-FPT-TYPES`，[命题合同（共 43 项）](assets.json) |
| [自适应原池重置与强制客户下界的离轨补全](<current/multi_facility/adaptive_reset_floor.md>) | `research/current/multi_facility/adaptive_reset_floor.md` | 由纯均衡的强制客户 floor 放宽源删除上界，严格扩展双 LPT 识别；无全输入识别保证。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-K-ADAPTIVE-DOUBLE-LPT-2`、`SC-K-ADAPTIVE-RESET`、`SC-K-FORCED-FLOOR`，[命题合同](assets.json) |
| [冻结静止超载与偏离者专属上界的多项式补全](<current/multi_facility/frozen_overload_completion.md>) | `research/current/multi_facility/frozen_overload_completion.md` | 允许非偏离设施保留高负载客户，以剩余强制 floor 和保持最大值的修复完成离轨均衡。 | 数学正文；按关联命题分别核对证明及审查；关联 `MF-FROZEN-OVERLOAD-POLY`、`SC-K-FROZEN-OVERLOAD-2`，[命题合同](assets.json) |
| [共单例仿射搜索到真实贪心盒的保真归约](<current/multi_facility/complement_search_reduction.md>) | `research/current/multi_facility/complement_search_reduction.md` | 保留重数、偏离和指定动力学；两速度有源位多项式归约，一般输出带区间另论，不提供通用求解器。 | 数学正文；按关联命题分别核对证明及审查；关联 `SC-K-BOX-BOUNDED-COMPLEMENT`、`SC-K-COMPLEMENT-GREEDY-REDUCTION`，[命题合同](assets.json) |
| [混合设施重数不能直接当作相关并行链速度](<current/multi_facility/restricted_related_link_boundary.md>) | `research/current/multi_facility/restricted_related_link_boundary.md` | 对比真实条件成本与相关链成本并给整数不一致例；正确共单例接口不等于一般复杂度下界。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |
| [固定字典序极大占位本身可逼近因子二](<current/multi_facility/lexmax_boundary.md>) | `research/current/multi_facility/lexmax_boundary.md` | 即使改选全部客户均衡和离轨续局，该选定占位仍可接近因子二，而另一占位有精确 SPE。 | 反例；仅否定正文明确的命题；关联 `SC-K-LEXMAX-BARRIER`，[命题合同](assets.json) |
| [对称续局菜单的无界假威胁反例](<current/multi_facility/symmetric_menu_obstruction.md>) | `research/current/multi_facility/symmetric_menu_obstruction.md` | 全重数族使对称菜单威胁无界但原模型最优倍率为一，排除把菜单受限失败当作模型下界。 | 方法障碍；否定范围以正文为准；关联 `SC-K-SYMMETRIC-MENU-OBSTRUCTION`，[命题合同](assets.json) |
| [深度三贪心树击败完整盒势最小选择器](<current/multi_facility/depth_three_box_boundary.md>) | `research/current/multi_facility/depth_three_box_boundary.md` | 给盒内均衡存在但特定受限势选择器失败的严格实例；不反驳贪心盒普遍存在性。 | 反例；仅否定正文明确的命题；关联 `SC-K-DEPTH-THREE-BOX-POTENTIAL-NO`，[命题合同](assets.json) |
| [完整盒内字典序极大分配未必是客户均衡](<current/multi_facility/boxed_lexmax_boundary.md>) | `research/current/multi_facility/boxed_lexmax_boundary.md` | 给严格贪心输入的特定字典序选择反例，限定在轨选择器而非一般因子二目标。 | 反例；仅否定正文明确的命题；关联 `SC-K-BOX-LEXMAX-NO`，[命题合同](assets.json) |
| [任意设施数：因子二、完整盒和高效构造前沿地图](<current/multi_facility/README.md>) | `research/current/multi_facility/README.md` | 先读一般因子二和完整盒有限构造，再按输入结构选择算法；一般位多项式时间仍单列为义务。 | 阅读导航；真值查精确正文及账本 |
| [一般输入的位多项式完整盒客户均衡构造义务](<questions/greedy_box_polytime.md>) | `research/questions/greedy_box_polytime.md` | 完整盒可行和有限改善已内部证明后，固定显式有理输入、总运行时间及完整续局输出的剩余算法目标。 | 问题记录；开放/已闭合部分见用途及正文 |
| [多设施统一常数原问题、恰三设施与特殊布局缺口](<questions/three_facilities.md>) | `research/questions/three_facilities.md` | 统一因子二存在和有限构造已内部闭合；最佳统一常数、恰三设施锐值及指定布局形式分别保持准确义务。 | 问题记录；开放/已闭合部分见用途及正文 |

<a id="customer_attraction"></a>

## 顺序客户吸引与半覆盖

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [顺序客户吸引模型：主题、均分收益与完整历史纯 SPE](<current/customer_attraction/model.md>) | `research/current/customer_attraction/model.md` | 定义单位客户、共同目录、全部有序历史上的纯策略及最优覆盖；进入任何证明或实验前核对模型与量词。 | 定义与模型；不隐含跨模型定理；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [顺序半覆盖猜想的文献与模型导入边界](<current/customer_attraction/literature.md>) | `research/current/customer_attraction/literature.md` | 核对客户吸引、效用系统、单资源拥塞及 Shapley 覆盖的一手来源；解释静态 Nash 结论不能直接导入顺序 SPE。 | 文献核对；与团队新结果分别引用；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [顺序福利文献的目录条件与量词复核](<current/customer_attraction/literature_followup.md>) | `research/current/customer_attraction/literature_followup.md` | 补核两人证明、顺序集合打包及短视反应的适用条件；其检索记录不构成“没有后续结果”的证明。 | 文献核对；与团队新结果分别引用；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [有限纯 SPE 终局全集与完整策略证书](<current/customer_attraction/exact_solver.md>) | `research/current/customer_attraction/exact_solver.md` | 给集合值逆向归纳的必要性、充分性和全历史证书重构；计数缓存返回终局全集，默认重构不枚举所有完整策略。 | 算法与构造；适用类及复杂度见正文；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [非极小可信续局与完整策略的联合构造接口](<current/customer_attraction/credible_continuations.md>) | `research/current/customer_attraction/credible_continuations.md` | 补全默认极小续局采样之外的合法菜单，保存两棵可重放完整策略及联合候选接口；不把所选策略锥当作全部 SPE。 | 表示或证书接口；不自动给出待求系数；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [固定完整策略的客户重数锥与精确优化](<current/customer_attraction/strategy_cone.md>) | `research/current/customer_attraction/strategy_cone.md` | 把每个真实有序节点的偏离写成有理锥，给紧截面和 Farkas 证书；固定策略或标签数的结论不扩大成任意策略结论。 | 表示或证书接口；不自动给出待求系数；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [子集势的 Möbius 反演、单位客户编译与重复主题边界](<current/customer_attraction/mobius_compiler.md>) | `research/current/customer_attraction/mobius_compiler.md` | 给唯一有符号重数表示、安全正偏置下的全历史嵌入，以及福利偏置和匿名计数的限制；辅助负重数不作为合法客户。 | 表示或证书接口；不自动给出待求系数；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [外来求解工具与末位保底推广的独立审计](<current/customer_attraction/uploaded_tool_audit.md>) | `research/current/customer_attraction/uploaded_tool_audit.md` | 核验上传工具与规范递推的关系，并以完整四人策略否定把末位最坏回复保底推广到每位玩家；原包只是来源。 | 实际审查记录；只覆盖所列版本与义务；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意目录三人的锐福利界](<current/customer_attraction/three_player_sharp.md>) | `research/current/customer_attraction/three_player_sharp.md` | 恰三人、任意完整历史纯 SPE 的 OPT₃≤(5/3)W 及达到下界；当前三人结论的首读正文。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意目录四人的真实根偏离福利界](<current/customer_attraction/four_player_bound.md>) | `research/current/customer_attraction/four_player_bound.md` | 恰四人、零根背景的 OPT₄≤(1499/750)W；保留原策略的根偏离与后继节点比较，不声称常数尖锐。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意目录五人的索引最优偏离福利界](<current/customer_attraction/five_player_indexed_bound.md>) | `research/current/customer_attraction/five_player_indexed_bound.md` | 恰五人、零根背景的当前较强上界 β≈2.061695；真实索引续局与有理非负证书仍未达到半覆盖。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [五人的三个真实最优回复菜单福利界](<current/customer_attraction/five_player_reply_bound.md>) | `research/current/customer_attraction/five_player_reply_bound.md` | 保留最优主题重数及三个真实末位菜单，给约 2.101243 的五人界；作为独立菜单机制保留，不是当前最强五人界。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [五人的两条真实中途偏离福利界](<current/customer_attraction/five_player_bound.md>) | `research/current/customer_attraction/five_player_bound.md` | 给约 2.209867 的五人上界及独立的两人税组合机制；后续上界更强，本稿原 claim 身份与推导仍保留。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [三人的两人税组合福利界](<current/customer_attraction/three_player_bound.md>) | `research/current/customer_attraction/three_player_bound.md` | 给旧 142/81 上界及从固定背景两人税到根覆盖的推导；三人最佳界已由独立的锐界正文替代。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意合法背景下恰三名剩余玩家的利润界](<current/customer_attraction/three_remaining_profit_bound.md>) | `research/current/customer_attraction/three_remaining_profit_bound.md` | 把三人真实回复恒等式扩至非零背景，比较同背景的剩余利润并给 5/3 界；该利润不等于全局覆盖。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意合法背景下恰四名剩余玩家的利润界](<current/customer_attraction/four_remaining_profit_bound.md>) | `research/current/customer_attraction/four_remaining_profit_bound.md` | 给四人背景利润的 1499/750 界和必要聚合校正；不能裸移零背景根税，也不能直接称为一般根半覆盖。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [末四人背景利润界向任意总人数的合法提升](<current/customer_attraction/tail_profit_lift.md>) | `research/current/customer_attraction/tail_profit_lift.md` | 利用真实前缀与索引子集比较，将四人背景定理提升为一般弱福利界；没有闭合人数无关的常数二。 | 精确归约；方向和编码合同见正文；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [共同核心与不交极大花瓣的锐顺序福利界](<current/customer_attraction/disjoint_maxima_bound.md>) | `research/current/customer_attraction/disjoint_maxima_bound.md` | 重构单资源席位机制，并在删除全目录共同核心后极大花瓣不交的类中给任意人数锐界；极大花瓣内允许交叠子主题。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [极大覆盖为向日葵的任意人数锐福利界](<current/customer_attraction/sunflower_maxima_bound.md>) | `research/current/customer_attraction/sunflower_maxima_bound.md` | 极大覆盖共享核心且花瓣不交；内部子主题可遗漏核心，给带核心的锐界及通用超集席位保底，额外私有缺口另列。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [客户极大关联集合成层级族时的锐福利界](<current/customer_attraction/laminar_incidence_bound.md>) | `research/current/customer_attraction/laminar_incidence_bound.md` | 客户在极大覆盖间的关联集合满足层级条件，允许内部子主题任意；严格扩展向日葵类，给带核心的任意人数锐界。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [至多三个极大覆盖的静态席位半覆盖界](<current/customer_attraction/three_maxima_bound.md>) | `research/current/customer_attraction/three_maxima_bound.md` | 给任意人数半覆盖、共享客户加权席位和实例敏感预算；同时定位四极大静态并集收费的失败，机制区别于动态路由。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [动态极大覆盖路由预算与至多五极大半覆盖](<current/customer_attraction/dynamic_maxima_bound.md>) | `research/current/customer_attraction/dynamic_maxima_bound.md` | 给任意极大主题数的全历史动态保底、私有与共享混合包络，并闭合至多五极大的任意人数半覆盖及适用的核心强化。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [至多六个极大覆盖的联合预算半覆盖界](<current/customer_attraction/six_maxima_joint_bound.md>) | `research/current/customer_attraction/six_maxima_joint_bound.md` | 任意人数、任意私有与共享关联、全部内部子主题的半覆盖；五人起给并集 U≤2W，不普遍声称额外减去共同核心。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [六极大无全局私有客户的强化界与九人以上推论](<current/customer_attraction/six_maxima_no_private.md>) | `research/current/customer_attraction/six_maxima_no_private.md` | 无全局私有非核心客户时给任意人数半覆盖及五人起的核心强化；另给不限制私有客户的九人以上核心强化。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [恰七个极大覆盖、七人以上的来源证明与重构边界](<current/customer_attraction/seven_maxima_checkpoint.md>) | `research/current/customer_attraction/seven_maxima_checkpoint.md` | 连接 n≥7 的完整来源证明与独立审查；现行页仅重建依赖概述，n=5、6 的尚缺系数分支明确保留。 | 来源与恢复指针；不代替缺失证明；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [固定前缀下恰两名剩余玩家的税界](<current/customer_attraction/two_remaining_tax.md>) | `research/current/customer_attraction/two_remaining_tax.md` | 在任意合法背景保留三个真实行动比较，给恰两人剩余利润税界；一般首步桥与根总税不能由此递推。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意历史的末两人逐人保底与全人数弱福利界](<current/customer_attraction/last_two_floor.md>) | `research/current/customer_attraction/last_two_floor.md` | 定义末位最坏最佳回复值 θₙ，证明最后两人各有保底并组合一般弱界；不能把 θₙ 保底扩至全部玩家。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意背景两名剩余玩家的平均跨分支偏离恒等式](<current/customer_attraction/global_new_uniform_portfolio_two.md>) | `research/current/customer_attraction/global_new_uniform_portfolio_two.md` | 对两个比较主题与两个实际玩家作真实偏离平均，给合法跨分支接口；任意人数的平均支付仍缺证明。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [不观察随机查询的混合安全值及其锐下界](<current/customer_attraction/oblivious_security.md>) | `research/current/customer_attraction/oblivious_security.md` | 固定静态对手不能观察所抽主题，给 vₙ≥OPTₙ/(2n−1)；顺序后继可观察偏离，向 SPE 收益支付该值另需桥梁。 | 数学正文；按关联命题分别核对证明及审查；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [残余覆盖、静态均衡与匿名平局的三个失败桥梁](<current/customer_attraction/continuation_lemmas.md>) | `research/current/customer_attraction/continuation_lemmas.md` | 保存逐人及聚合残余收益反例、SPE 终局非静态 PNE 及历史平局边界，并保留仍成立的直接下界。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [最优主题组合的真实偏离匹配收费反例](<current/customer_attraction/portfolio_matching_counterexample.md>) | `research/current/customer_attraction/portfolio_matching_counterexample.md` | 两人实例的唯一最优组合中，两种匹配偏离收益都不足以支付漏覆盖；只排除该匹配接口。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [空背景三人的首步机会成本税桥反例](<current/customer_attraction/tax_bridge_counterexample.md>) | `research/current/customer_attraction/tax_bridge_counterexample.md` | 完整三人 SPE 已否定逐步税递推；该例整条根税恰取等，须与后来根总税反例区分。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [实际非零背景中的一般总税反例](<current/customer_attraction/general_tax_counterexample.md>) | `research/current/customer_attraction/general_tax_counterexample.md` | 在完整根 SPE 实际到达的背景给总税失败及无限族；恰两人局部税和背景利润对象仍按各自条件使用。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [逐期最优覆盖补全损失的当期收费反例](<current/customer_attraction/coverage_opportunity_counterexample.md>) | `research/current/customer_attraction/coverage_opportunity_counterexample.md` | 完整三人策略否定仅用当期收益支付当期最优补全损失；保留多步余额与全局望远镜恒等式。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [四人完整策略中的负前缀余额反例](<current/customer_attraction/prefix_balance_counterexample.md>) | `research/current/customer_attraction/prefix_balance_counterexample.md` | 保存二十二客户证书，否定所有实际前缀余额非负；终局全局余额不由此前缀反例判定。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [任意四人以上的负首步余额族与固定权重障碍](<current/customer_attraction/prefix_balance_family.md>) | `research/current/customer_attraction/prefix_balance_family.md` | 为每个 n≥4 构造完整 SPE 的负首步余额，并排除用小于二的固定首位权重统一修复；半覆盖与该族根税仍成立。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [四人完整 SPE 的空背景根总税反例](<current/customer_attraction/root_tax_counterexample.md>) | `research/current/customer_attraction/root_tax_counterexample.md` | 六主题、六十一单位客户在真实根顺序中否定 OPT≤W+τ；一般半覆盖、恰两人税与末位比较仍不被否定。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [末位最坏最佳回复值的聚合收益桥反例](<current/customer_attraction/aggregate_theta_counterexample.md>) | `research/current/customer_attraction/aggregate_theta_counterexample.md` | 给每个 n≥3 的完整策略构造使 W<nθₙ；它针对末位最坏回复值，不是静态混合安全值的聚合桥。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [自适应后继、真实菜单与安全值的跨分支失败边界](<current/customer_attraction/continuation_security_barriers.md>) | `research/current/customer_attraction/continuation_security_barriers.md` | 给单后继去相关恒等式、多后继失败及真实根菜单反例；菜单 minimax 与真正静态安全值不能混同。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [三人完整 SPE 中逐人混合安全值保底的反例](<current/customer_attraction/individual_security_counterexample.md>) | `research/current/customer_attraction/individual_security_counterexample.md` | 三十四单位客户与唯一安全最优分布否定 uᵢ≥vₙ；本例聚合安全桥和半覆盖均仍成立。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [总去相关、激励松弛与全分布补偿预算的失败边界](<current/customer_attraction/global_security_budget_boundaries.md>) | `research/current/customer_attraction/global_security_budget_boundaries.md` | 重构覆盖减独立查询的精确恒等式，排除总去相关及对所有分布的补偿预算；真正聚合安全桥另行保留。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [独立同分布静态基准与完整树节点平均的障碍](<current/customer_attraction/iid_security_and_flow_barriers.md>) | `research/current/customer_attraction/iid_security_and_flow_barriers.md` | 给静态凹势与安全值基准，同时以分离向量限制节点内平均支付模板；该分离向量不是完整 SPE。 | 方法障碍；否定范围以正文为准；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [三个指定完整策略的全重数安全值证书](<current/customer_attraction/selected_security_cones.md>) | `research/current/customer_attraction/selected_security_cones.md` | 对三棵固定形式策略的整个非负客户重数锥给静态对偶证书；五个固定游戏的全集枚举与任意策略结论分开。 | 证书与核验正文；验证范围见合同；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [二十一棵新策略的安全锥证书与五人逐人失败](<current/customer_attraction/policy_security_checkpoints.md>) | `research/current/customer_attraction/policy_security_checkpoints.md` | 保存指定完整策略全重数锥的聚合证书及另一五人逐人安全值反例；不排除其他策略中的聚合攻击。 | 证书与核验正文；验证范围见合同；关联 `CA-DYNAMIC-IID-DEBT-INTERFACE`、`CA-FIVE-INDIVIDUAL-SECURITY-NO`、`CA-LOCAL-SECURITY-INDUCTION-NO`，[命题合同（共 9 项）](assets.json) |
| [均匀正偏置编译的安全值差额与反例生成限制](<current/customer_attraction/compiler_security_barrier.md>) | `research/current/customer_attraction/compiler_security_barrier.md` | 在指定充分正偏置条件下给逐人及聚合安全值的正差额；只限制该编译器，较小偏置与其他构造须另审。 | 方法障碍；否定范围以正文为准；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [唯一最优主题组合的末节点查询总额收费反例](<current/customer_attraction/optimal_last_query_counterexample.md>) | `research/current/customer_attraction/optimal_last_query_counterexample.md` | 完整四人策略中，唯一最优组合的真实末节点查询和超过实际福利；改换最优组合不能修复该查询支付接口。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [随机最优主题排列的前缀席位交换反例](<current/customer_attraction/random_position_exchange_boundary.md>) | `research/current/customer_attraction/random_position_exchange_boundary.md` | 三人五客户完整策略否定随机比较前缀中的位置可交换步骤；随机排列不能替代真实后继回复控制。 | 反例；仅否定正文明确的命题；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [完整策略锥与静态安全值的对偶支付接口](<current/customer_attraction/security_cone_duality.md>) | `research/current/customer_attraction/security_cone_duality.md` | 把固定策略的安全值支付写成有限 minimax 与 Farkas 精确等价；这是已有工具的组合接口，普遍支付义务仍开放。 | 精确归约；方向和编码合同见正文；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [安全值链的全局债务接口与局部归纳反例](<current/customer_attraction/security_chain_and_local_boundary.md>) | `research/current/customer_attraction/security_chain_and_local_boundary.md` | 给足以推出半覆盖的全路径债务条件，并以完整策略否定逐步局部归纳；全局债务不等式尚未成立。 | 精确归约；方向和编码合同见正文；关联 `CA-DYNAMIC-IID-DEBT-INTERFACE`、`CA-FIVE-INDIVIDUAL-SECURITY-NO`、`CA-LOCAL-SECURITY-INDUCTION-NO`，[命题合同（共 9 项）](assets.json) |
| [动态独立查询的债务接口与弱局部漂移反例](<current/customer_attraction/dynamic_iid_debt_boundary.md>) | `research/current/customer_attraction/dynamic_iid_debt_boundary.md` | 给合法背景中的静态凹势、最优性条件与租金恒等式；真实五人路径否定弱逐步漂移，较弱全局桥仍开放。 | 精确归约；方向和编码合同见正文；关联 `CA-DYNAMIC-IID-DEBT-INTERFACE`、`CA-FIVE-INDIVIDUAL-SECURITY-NO`、`CA-LOCAL-SECURITY-INDUCTION-NO`，[命题合同（共 9 项）](assets.json) |
| [末两人回复循环的静态运输证书与指定核障碍](<current/customer_attraction/stationary_pair_transport.md>) | `research/current/customer_attraction/stationary_pair_transport.md` | 从真实末回复图循环构造共同静态背景及系数恒等式，并给两种指定核失败反例；不排除其他全局运输。 | 表示或证书接口；不自动给出待求系数；关联 `CA-DYNAMIC-IID-DEBT-INTERFACE`、`CA-FIVE-INDIVIDUAL-SECURITY-NO`、`CA-LOCAL-SECURITY-INDUCTION-NO`，[命题合同（共 9 项）](assets.json) |
| [末回复规范化的条件性对偶提升与有向无环转移](<current/customer_attraction/terminal_reply_transport.md>) | `research/current/customer_attraction/terminal_reply_transport.md` | 将规范化证书的早期误差写为有符号份额转移，给转移图不变量及不对称预算；一般净债尚未支付。 | 表示或证书接口；不自动给出待求系数；关联 `CA-DYNAMIC-IID-DEBT-INTERFACE`、`CA-FIVE-INDIVIDUAL-SECURITY-NO`、`CA-LOCAL-SECURITY-INDUCTION-NO`，[命题合同（共 9 项）](assets.json) |
| [真实末端平局行的商空间支付与二次判别](<current/customer_attraction/terminal_tie_quotient.md>) | `research/current/customer_attraction/terminal_tie_quotient.md` | 允许相反真实末行的有符号组合，严格扩大逐类型余项接口；有限成功证书和条件性提升不等于普遍半覆盖。 | 表示或证书接口；不自动给出待求系数；关联 `CA-TERMINAL-TIE-FIXED-LIFT-NO`、`CA-TERMINAL-TIE-LOCAL-QUADRATIC`、`CA-TERMINAL-TIE-QUOTIENT-LIFT`，[命题合同](assets.json) |
| [自然半覆盖证书保留早期乘子提升的障碍](<current/customer_attraction/terminal_tie_lift_obstruction.md>) | `research/current/customer_attraction/terminal_tie_lift_obstruction.md` | 即使目标为 2c−o、加入全部同计数末回复等式，原定早期乘子也未必可保留；不排除重选乘子或一般全局证书。 | 方法障碍；否定范围以正文为准；关联 `CA-TERMINAL-TIE-FIXED-LIFT-NO`、`CA-TERMINAL-TIE-LOCAL-QUADRATIC`、`CA-TERMINAL-TIE-QUOTIENT-LIFT`，[命题合同](assets.json) |
| [五人两条根偏离的线性必要条件模板障碍](<current/customer_attraction/five_player_lift_obstruction.md>) | `research/current/customer_attraction/five_player_lift_obstruction.md` | 指定四百六十行松弛不能推出半覆盖；O 是辅助变量，可行点没有完整策略，不能称为 SPE 反例。 | 方法障碍；否定范围以正文为准；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [五人索引续局模板的精确最优值与半覆盖障碍](<current/customer_attraction/five_player_indexed_obstruction.md>) | `research/current/customer_attraction/five_player_indexed_obstruction.md` | 同一四百三十七行必要条件的有理原始点与对偶匹配；认证的是松弛模板最优性，不是原游戏达到最坏比率。 | 方法障碍；否定范围以正文为准；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [六极大动态超集席位的合法路径收费障碍](<current/customer_attraction/six_maxima_seat_obstructions.md>) | `research/current/customer_attraction/six_maxima_seat_obstructions.md` | 给五至八人合法路径的动态预算失败及九人以上相关审计；这些路径不声称为 SPE，不反驳六极大半覆盖。 | 方法障碍；否定范围以正文为准；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [顺序客户吸引：福利界、完整策略工具和失败桥地图](<current/customer_attraction/README.md>) | `research/current/customer_attraction/README.md` | 围绕一般半覆盖选择小人数、极大覆盖结构或证书工具，明确辅助桥反例与主问题反例的区别。 | 阅读导航；真值查精确正文及账本；关联 `CA-ACTUAL-ROOT-TAIL-MENU-NO`、`CA-ADAPTIVE-DECORRELATION-NO`、`CA-AGGREGATE-DECORRELATION-NO`，[命题合同（共 63 项）](assets.json) |
| [顺序客户吸引：任意完整纯 SPE 的一般半覆盖问题](<questions/customer_attraction_half_coverage.md>) | `research/questions/customer_attraction_half_coverage.md` | 固定全部历史、任意共同目录与单位客户模型，区分已证小人数和结构类，精确记录一般福利保证的缺口。 | 问题记录；开放/已闭合部分见用途及正文 |
| [一般半覆盖的两条攻坚接口：全局安全债务与真实分支转移](<questions/customer_attraction_general_handoff.md>) | `research/questions/customer_attraction_general_handoff.md` | 在不增加目录结构限制下研究全局补偿或直接覆盖证书；保留已有反例对逐人、逐步和冻结续局方法的限制。 | 问题记录；开放/已闭合部分见用途及正文 |

<a id="foundation"></a>

## 公共定义与精确命题登记

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [全仓研究总目录：按问题选择资产与阅读路径](<README.md>) | `research/README.md` | 进入仓库后选择模型和研究问题，区分数学正文、候选、审查、计算与历史；查清各登记分别负责什么。 | 阅读导航；真值查精确正文及账本 |
| [新研究入库规范：对象、命题、程序与证据的生产合同](<GROWTH.md>) | `research/GROWTH.md` | 创建或修改可复用资产之前核对放置目录、精确身份、共同前提、状态分轴和同步登记要求。 | 阅读导航；真值查精确正文及账本 |
| [仓库生产、按需读取与共同保存规则](<REPOSITORY_GUIDE.md>) | `research/REPOSITORY_GUIDE.md` | 需要安全同步、阶段保存或分支收口时读取；把文件角色、数学等级与协作交流分开管理。 | 阅读导航；真值查精确正文及账本 |
| [当前全仓研究路线与未闭合证明义务](<ROADMAP.md>) | `research/ROADMAP.md` | 选下一步研究时查真正开放的目标、已有工具和阻碍；旧设施路线只从历史快照追溯。 | 阅读导航；真值查精确正文及账本 |
| [旧研究分支收口与来源恢复记录](<BRANCHES.md>) | `research/BRANCHES.md` | 仅在追溯分支处置、原提交可达性或旧会话迁移时读取；不作为当前数学结论的证据。 | 来源与恢复指针；不代替缺失证明 |
| [设施选址与顺序吸引的失败机制及回收边界](<FAILED_ROUTES_FACILITY.md>) | `research/FAILED_ROUTES_FACILITY.md` | 研究局部菜单、算法复杂度、续局量词或安全值桥前，核对已经被否定的准确断言和可保留信息。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |
| [当前数学正文的模型分流与证明链入口](<current/README.md>) | `research/current/README.md` | 决定进入拥塞、两阶段设施选址或顺序客户吸引；避免把相邻目录误认成同一模型的结论。 | 阅读导航；真值查精确正文及账本 |
| [两阶段设施选址公共模型：精确独立 NE 与完整续局](<current/model.md>) | `research/current/model.md` | 引用共同、异构或多设施结果前核对输入、实际负载成本、独立随机化与完整续局的量词。 | 定义与模型；不隐含跨模型定理；关联 `HC-2-LOW`、`HC-2-SHARP`、`HC-2-UP`，[命题合同（共 7 项）](assets.json) |
| [全仓精确命题登记：范围、依赖与状态位置](<current/claims.md>) | `research/current/claims.md` | 引用或变更某条命题时查稳定 ID、精确输入和证据；不以导航摘要替代原有量词。 | 精确命题登记；摘要不替代原陈述 |
| [全仓问题目录：开放义务、候选与已闭合原合同](<questions/README.md>) | `research/questions/README.md` | 开始攻坚前分清正在缺的证明和已获内部答案的旧任务；从准确问题页进入实际资产。 | 阅读导航；真值查精确正文及账本 |
| [独立审查总入口：冻结版本、覆盖范围与异议](<reviews/README.md>) | `research/reviews/README.md` | 按拥塞、设施或顺序吸引选择实际发生的审查，核对哪些义务被攻击、哪些来源仍缺失。 | 阅读导航；真值查精确正文及账本 |

<a id="facility_review"></a>

## 设施模型的独立审查

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [五共同地点固定倍率弱 NP 完全性：范围、独立逆审与价值边界](<reviews/facility/five_site_fixed_factor_hardness.md>) | `research/reviews/facility/five_site_fixed_factor_hardness.md` | 审查 SC-FIVE-DECa-HARD 的精确模型、固定有理倍率归约、全部布局守卫与有限复核；保留当时文献和价值判断，不以旧开放表覆盖现行账本。 | 实际审查记录；只覆盖所列版本与义务 |
| [任意设施数共同目录因子二：存在性证明与有限构造审查](<reviews/facility/arbitrary_facility_factor_two.md>) | `research/reviews/facility/arbitrary_facility_factor_two.md` | 审查 SC-K-2-E 的完整续局、超重原子隔离、独立精确枚举及布局规则障碍；区分有限构造、一般位多项式目标和尖锐性。 | 实际审查记录；只覆盖所列版本与义务 |
| [等权轻客户无约束费用流：自动保盒与精确续局核验](<reviews/facility/equal_weight_light_customer_flow.md>) | `research/reviews/facility/equal_weight_light_customer_flow.md` | 记录 SC-K-EQUAL-LIGHT-FLOW-BOX 的自动保盒与 H 性质、规范流实现及三类精确复核，说明相对旧等权选择器的增量与异权端点障碍。 | 实际审查记录；只覆盖所列版本与义务 |
| [共单例均衡搜索归约：负载区间、全状态保真与实现审查](<reviews/facility/complement_search_reduction.md>) | `research/reviews/facility/complement_search_reduction.md` | 审查 SC-K-COMPLEMENT-GREEDY-REDUCTION 和 SC-K-BOX-BOUNDED-COMPLEMENT 的输入编码、策略取补、全状态保盒、偏离差与精确有限核验；不声称新的困难性或求解算法。 | 实际审查记录；只覆盖所列版本与义务 |
| [四共同地点实例最优倍率无 FPTAS：全支持归约的独立审查](<reviews/facility/four_site_no_fptas.md>) | `research/reviews/facility/four_site_no_fptas.md` | 记录 SC-FOUR-NO-FPTAS 的实概率全部支持、十六带标签布局、逆多项式间隙、显式输出合同及两份独立精确有限审计；与客户近似均衡、PTAS 和一般搜索区分。 | 实际审查记录；只覆盖所列版本与义务 |

<a id="customer_attraction_review"></a>

## 客户吸引的独立审查

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [顺序客户吸引的向日葵极大目录福利与超集席位：独立内部审查](<reviews/customer_attraction/sunflower_maxima_and_superset_seats.md>) | `research/reviews/customer_attraction/sunflower_maxima_and_superset_seats.md` | 独立审查 CA-SUNFLOWER-MAXIMA-2M1、CA-MAXIMA-SUPERSET-SEATS 的全部前缀、平局、core 和锐性边界，并保留私有缺口附加性质及有限攻击范围。 | 实际审查记录；只覆盖所列版本与义务 |

<a id="publication"></a>

## 历史投稿判断与旧方向选择

| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |
| --- | --- | --- | --- |
| [设施选址成果的投稿组合与内部审查：2026-10-01 历史评估](<../history/source/notes/publication/facility_publication_assessment_2026-10-01.md>) | `history/source/notes/publication/facility_publication_assessment_2026-10-01.md` | 保存当时共同目录 φ、单交叠 ρ、异构因子二候选与精确算法的贡献/投稿判断及审查快照；后续五地点复杂度、多设施和优先权核验已改变部分背景，按历史判断读取。 | 来源或历史判断；不作为现行结论 |
| [设施选址论文拆分、定理顺序与投稿门槛：2026-10-02 编辑决定](<../history/source/notes/publication/facility_journal_decision_2026-10-02.md>) | `history/source/notes/publication/facility_journal_decision_2026-10-02.md` | 保存两篇论文方案、期刊适配、精确续局措辞和待核优先权清单；内部编辑意见不作为当前数学或外审状态。 | 来源或历史判断；不作为现行结论 |
| [设施选址成果链与投稿审查任务：2026-10-02 历史交接](<../history/source/notes/publication/facility_journal_handoff_2026-10-02.md>) | `history/source/notes/publication/facility_journal_handoff_2026-10-02.md` | 保存共同目录、异构交叠、长坏环和精确计算层的当时英文编辑说明及独立团队问题；只用于恢复早期组稿理由。 | 来源或历史判断；不作为现行结论 |
| [设施选址成果与正式发表的文献对标：2026-10-05 历史评估](<../history/source/notes/publication/facility_publication_benchmark_2026-10-05.md>) | `history/source/notes/publication/facility_publication_benchmark_2026-10-05.md` | 保存一手论文的精确模型比较、2025 博士论文读取范围和投稿价值判断；包括后续评估修正过的五地点困难性价值解释，不作为新颖性认证。 | 来源或历史判断；不作为现行结论 |
| [设施选址全成果的贡献、优先权与投稿组合：2026-10-06 历史评估](<../history/source/notes/publication/facility_publication_assessment_2026-10-06.md>) | `history/source/notes/publication/facility_publication_assessment_2026-10-06.md` | 保存当时成果包和期刊建议，解释同模型五地点困难性、广义 φ 猜想目录范围、超载孤立原子合同修正；不提升候选或外部评审状态。 | 来源或历史判断；不作为现行结论 |
| [双设施实例最优倍率 EPTAS 的选题辩驳与初探：2026-10-09 历史决定](<../history/source/notes/publication/facility_eptas_direction_debate_2026-10-09.md>) | `history/source/notes/publication/facility_eptas_direction_debate_2026-10-09.md` | 保存由无 FPTAS 转向精确客户 NE 下 EPTAS 的当时选题论证、近带补全试探、误差与精度编码合同；现行定理或候选状态应另查当前账本。 | 来源或历史判断；不作为现行结论 |
