# 加权拥塞的结构方法：端点、共同尺度与稳定核实现

2026-10-25 投稿接续：仓库内的 TEAC 审稿源码与 PDF 已补 AI 研究使用说明及四处指称/记号精度，并重新编译；另按 MOR 官方模板制成私有匿名 32 页审稿包，含正文、附录、参考文献。新的选刊与模板事实、真实审查覆盖、哈希和剩余作者义务分别见本目录 VENUE_TEMPLATE_REVIEW_round2.md、REFEREE_REPORT_round2.md、WRITING_STATE.md。下文的旧轮 TEAC 选择是历史记录，不覆盖这次 MOR 投稿准备。

本专题从真实拥塞费用中抽取可复用接口：端点与面积给出局部设计预算，共同玩家尺度把局部势拼成全局证书，稳定核实现把受限结构连接到完整游戏。正向保证、成本选择和接近次数的坏游戏分别使用这些接口，并各自保留全部假设。

连续论文现按主人指定的四节组织：引言与模型、结构工具、显式全状态反例族、正向稳定与社会成本应用。现用 TEAC `acmart` 单栏审稿格式；[第二轮选刊与模板核验](VENUE_TEMPLATE_REVIEW_round2.md)记录官方版本、文献归属、开发版编译范围及投稿前缺项。[第二轮证明和英文复核](REFEREE_REPORT_round2.md)按冻结源码版本区分独立数学攻击、差分核验与表述审读。旧审查只覆盖其冻结版本；本次重组和真实核验分别记录在[写作状态](WRITING_STATE.md)、[修订记录](REVISION-NOTES.md)及[三稿核验](../../../manuscripts/MANUSCRIPT_REVIEW.md)，恢复三篇成文工作从[总入口](../../../manuscripts/README.md)进入。

八份自足数学正文已有完整证明和四份实际独立整合审查。审查为知悉稿后的独立重推/攻击，按真实覆盖登记；它与连续论文审读、有限精确审计、外部评审和新颖性是不同状态。精确身份见[命题账本](../../../weighted_congestion_frontier/CLAIMS.md#结构重建的精确身份2026-10-21)及[五轴状态](../../../review_status.json)。历史概述只说明来源，不承担证明前提。

| 文件 | 数学对象、用途与边界 |
| --- | --- |
| [endpoint_area_principle.md](endpoint_area_principle.md) | 任意网格端点面积误差、同权窗口有限收缩证书、局部阈值与真实小原子份额积分势。窗口总质量与采样分辨率独立；局部收缩不证明全状态非存在。 |
| [shared_scale_gluing.md](shared_scale_gluing.md) | 跨资源共同类型尺度、类型森林平方根保证、环失配谱及统一包络合同的准确门槛。合同NO不是原游戏无均衡。 |
| [instance_interval_calibration.md](instance_interval_calibration.md) | 扫描实际人数插入，给非负双排序字典的精确尺度区间、乘积环证书与森林最小合同倍率。其最优性限于明示字典及共同尺度。 |
| [repair_and_core_transfer.md](repair_and_core_transfer.md) | 完整锚定门的全部稳定集合、近似容差、有限有理实现及前沿社会成本恒移。扩充游戏与原基体、近似稳定与精确稳定分别陈述。 |
| [socially_descending_repair.md](socially_descending_repair.md) | 支付基体社会外部性后，修复同时降低完整总加权成本并压缩社会OPT；S7联合共同尺度正则化、前沿包络、全局核心最小化及RD/SD，给完整稳定性和社会质量保证。 |
| [parameterized_allstate_family.md](parameterized_allstate_family.md) | 对每固定c<1及全部充分大整数d，覆盖全部前沿与非法状态的有理同次反例；实际玩家高度恰g+1=O_c(log d)。 |
| [additive_near_degree_lower_bound.md](additive_near_degree_lower_bound.md) | 新身份WC-ADDITIVE-NEAR-DEGREE-ALLSTATE-v1：每整数d≥2²⁰都有无[d−1200⌈log₂d⌉²]-PNE的纯d次游戏。重新统一证明n(d)条件，不把固定c阈值非法代入可变c。 |
| [weight_depth_threshold.md](weight_depth_threshold.md) | 旧高度势的精确反演、实际改善闭词的长链见证及最少权类/潜在玩家高度的Θ_c(log d)正反桥。高深度不是失稳充分条件；固定c不可换任意c(d)→1。 |

连续英文[完整PDF](structural_methods_article.pdf)、[LaTeX主文](structural_methods_article.tex)及[BibTeX](structural_methods_article.bib)已经整合；[全文与PDF产物核查](../../../reviews/weighted_congestion/structural_reconstruction/structural_methods_article_review.md)记录实际最终版本、引用、真实审查覆盖与逐页检查。全状态近次数结果沿用单独新Claim；[旧d/10证明](../linear_degree_allstate_lower_bound.md)及其冻结审查仍有独立工具价值，原身份不改。

## 已发生的独立审查

| 审查 | 实际覆盖 |
| --- | --- |
| [端点整合审查](../../../reviews/weighted_congestion/structural_reconstruction/endpoint_integration_review.md) | 冻结端点正文、旧端点审查、非减凸误差、小真实份额及有限局部证书；未替代全状态或最终连续论文审读。 |
| [近次数独立攻击](../../../reviews/weighted_congestion/structural_reconstruction/additive_near_degree_review.md) | 统一n(d)取整、全部相位与前沿、同次非法态修复及全部一般量词；源稿版本与真实运行见记录。 |
| [尺度与深度整合审查](../../../reviews/weighted_congestion/structural_reconstruction/scale_depth_integration_review.md) | 共同玩家乘子、环失配和实际区间的不同最优域、玩家图高度反演；固定c的上方向继承完整参数族审查状态。 |
| [稳定核与社会质量整合审查](../../../reviews/weighted_congestion/structural_reconstruction/positive_repair_integration_review.md) | 完整稳定容差、前沿恒移、社会外部性反边界、SD最优压缩及S7正则化联合保证；含独立第二实现。 |

原有[端点审查](../../../reviews/weighted_congestion/structural_reconstruction/endpoint_review.md)、[可变n逐式攻击](../../../reviews/weighted_congestion/structural_reconstruction/near_unit_review.md)、[尺度审查](../../../reviews/weighted_congestion/structural_reconstruction/shared_scale_review.md)、[环谱独立复构](../../../reviews/weighted_congestion/structural_reconstruction/cycle_independent.md)与[深度独立检查](../../../reviews/weighted_congestion/structural_reconstruction/depth_independent.md)保留各自真实发生时的覆盖及来源版本。旧记录中的scratch路径或程序短名不被当作当前可执行入口；当前入口如下。

## 有限精确审计

| 核验代码 | 冻结记录与范围 |
| --- | --- |
| [endpoint_certificate.py](../../../../tests/audits/weighted_congestion/structural_reconstruction/endpoint_certificate.py) | [局部参数证书](../../../../evidence/runs/weighted_congestion/structural_reconstruction/endpoint_local_certificate.json)：有限有理端点/面积及严格余量。 |
| [near_degree_audit.py](../../../../tests/audits/weighted_congestion/structural_reconstruction/near_degree_audit.py) | [近次数审计](../../../../evidence/runs/weighted_congestion/structural_reconstruction/near_degree_audit.json)：端点、return、扭转、修复及二幂邻近取整；不证明无限尾部。 |
| [raw_resource_audit.py](../../../../tests/audits/weighted_congestion/structural_reconstruction/raw_resource_audit.py) | [实际资源审计](../../../../evidence/runs/weighted_congestion/structural_reconstruction/raw_resource_audit.json)：显式资源侧的相位、非法位串与稳定集合恒等式。 |
| [repair_cost_audit.py](../../../../tests/audits/weighted_congestion/structural_reconstruction/repair_cost_audit.py) | [修复成本审计](../../../../evidence/runs/weighted_congestion/structural_reconstruction/repair_cost_audit.json)：门社会恒移与稳定选择的有限例。 |

[positive_repair_integration_audit.py](../../../../tests/audits/weighted_congestion/structural_reconstruction/positive_repair_integration_audit.py)及其[冻结记录](../../../../evidence/runs/weighted_congestion/structural_reconstruction/positive_repair_integration_audit.json)另从literal资源独立核对修复路径、OPT压缩和联合质量有限例。

这些运行帮助发现公式或资源关联转录错误，不生成巨大渐近实例，也不代替一般证明。[原决策方法专题](../decision_methods/README.md)继续提供共同尺度LP、成本正则化及显式有限求解接口；有限终止与精确校准本身不保证紧凑输入的位多项式均衡搜索。
