# 四个独立 UM 审计程序：原件、真实复跑与数学边界

claim已实际pushed/synced `4d403569f6efb29952b69f38fb144cb34b0e36a3`，本包实际primary4均在确认后完整读代码。四源有各自模型，目录不能产生共同假设或方法。外部独立stage交root串行copy/push/done，本页不自称已经推送。

## 自足计算对象

- [仿射有限见证](../../../state/计算/仿射互补计数反例的冻结程序与复跑--计算.md)：固定rho例与三个构造计数，不把人工OPT下界当程序穷举。
- [anchor见证与支撑前置](../../../state/计算/锚缺额见证舍入的三夹具与支撑前置--计算.md)：三给定joint witnesses/严格删机/全局ST，新增beta2合同probe揭示baseline正支撑p<=T条件，不改原source。
- [arbitrary-sink cover/MW](../../../state/计算/任意汇点价格覆盖与共同MW的独立有限审计--计算.md)：112静态、6MW分full/prefix/拒绝、3T0，明确最终matroid rounding未执行。
- [度二菜单structured审计](../../../state/计算/度二加权菜单外置夹具审计与后端版本--计算.md)：5菜单/6小raw/1200迭代/6拒绝、原jobs与bonus值桥、新旧CLI/依赖diff。

## 原始来源/依赖/比较逐项

runtime original树保留tests/audits与examples路径，使anchor原路径发现和菜单相邻import不需改字节。baseline只导入round_slots，其更大audit主程序本轮执行0次。大历史arbitrary JSON为完整结构解析/精确比较，不冒所有静态行均人工全文审核。

|角色|ID|大小|SHA256|原件|
|---|---|---:|---|---|
|primary|eeddfde504988cb91290|903|41cd56189f129fa60dbf97c5dad55c9cb283e9912910657a22a6c4b7adf65495|[原件](original/tests/audits/unrelated_machines/affine_complement_cardinality_boundary.py)|
|primary|6792d393686f9eeb99b1|6134|dbf9fcafd36a9b86d10bdda5f372d543188006ddeaf6c372b38b285252f3204a|[原件](original/tests/audits/unrelated_machines/anchor_deficiency_joint_rounding_audit.py)|
|primary|26e18e49fd85c8f7dd79|27461|bc555c5d6254884d3b9cb41a65b126d0b857021d3bac876edca967f97baa067b|[原件](original/tests/audits/unrelated_machines/arbitrary_sink_price_cover_mw_audit.py)|
|primary|af2ee631a5e5e8dfd2e2|9284|2a6b5b009ecedc417343fe42b44113aaf513b7e661756005fdd6738e71979a3d|[原件](original/tests/audits/unrelated_machines/audit_degree_two_weighted_menu_backend.py)|
|dependency|e57947bc795251d373c3|12108|5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a|[原件](original/tests/audits/unrelated_machines/rounding_and_gap.py)|
|dependency|bc7fbb3d9e7d1df6050e|16597|3ac389c7ab6bf1037c51d744d18e6191b5be8df1ba559e731fbbcaf4ebcc3c99|[原件](original/tests/audits/unrelated_machines/degree_two_weighted_menu_backend.py)|
|dependency|b88c0af63e1cab4774d1|4466|59501d74f2c092af8cbf56921987436b160274db325f4f30b69b058c10edf72f|[原件](original/examples/unrelated_machines/weighted_menu_joint_fixtures.json)|
|comparison|8088efef4cfbcec8c315|4111|c6d83b6b904f5d41546af16bfb06b19095de40e9cbe1d22e94ef64cd98f4197b|[原件](comparison/research/current/unrelated_machines/affine_complement_cardinality_boundary.md)|
|comparison|78b4b3116ebe9be9ccd3|14687|dd2e88af7ef222d0eecfd8ed0b1ac3c10f6da8ca41ae7c5f4ca46333c91ea779|[原件](comparison/research/current/unrelated_machines/anchor_deficiency_joint_rounding.md)|
|comparison|d7bf0f8e0e037822ff23|16556|6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580|[原件](comparison/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md)|
|comparison|c4f03674003e646df675|511|a143c9baefb87c82244e6a2cebcd0bc450df1a21df4b1a76ed72cab2ee0c0c7a|[原件](comparison/evidence/runs/unrelated_machines/affine_complement_cardinality_boundary_audit.json)|
|comparison|acb3c1e4d763176a59f2|2139|a0794109d414da24c4387fe88474ddc383395787159b8b5812291881f459da9f|[原件](comparison/evidence/runs/unrelated_machines/anchor_deficiency_witness_audit.json)|
|comparison|eb69b21ac2fc7ee61e94|101718|79551ed7245816b5918bd64ebb041ead4dfe15335de55c241b0138255262f842|[原件](comparison/evidence/runs/unrelated_machines/arbitrary_sink_price_cover_mw_audit.json)|
|comparison|187764f28fade96cc1ce|124138|fb82e4a9040d8bdadd1ee314653212b82b8ed61aed07f08aed0ceffe05d87c3a|[原件](comparison/examples/unrelated_machines/arbitrary_sink_price_cover_mw_cases.json)|

## 实际执行和旧证据

本轮4个原CLI各一次exit0，另1条beta2合同probe一次exit0（意为如实观测原wrapper ValueError），总5个数学程序过程。原CLI stdout/stderr、完整commands/cwd/版本、生成fixture/report与逐job输出均保留，不仅摘要。历史run不计为本轮；新run不是新独立实现或blind。

[原CLI执行manifest](runs/execution-manifest.json)、[补充probe输入/源码](probes/anchor-beta-support-boundary.py)、[probe实际输出](runs/anchor-beta-probe.stdout)、[精确运行范围与计数](mathematical-execution-scope.json)、[输出哈希清单](artifact-manifest.json)。

[cover/MW完整生成输入](runs/arbitrary-sink-output/price_cover_joint_independent_cases.json)、[cover/MW完整报告](runs/arbitrary-sink-output/price_cover_joint_independent_report.json)、[菜单实际报告](runs/menu-output/audit_results.json)、[菜单完整实际jobs](runs/menu-output/fixture_outputs.json)。

[历史精确比较及版本diff账](historical-comparison-and-version-diffs.json)、[core实际diff](menu-core-old-to-structured.diff)、[audit外置输入实际diff](menu-audit-old-to-external-fixtures.diff)。旧gzip解压core与当前frozen core非同SHA；本次使用指定当前依赖，未运行旧版写源码目录main。

arbitrary generatedcases与历史逐字相同，报告排除环境字段后逐结构相同；anchor只排历史额外proof指纹后相同；affine stdout相同；菜单report/完整jobs相同、fixture按精确rational规范化相同。原来源均未修改。

## 自查与关系

[源清单](source-manifest.json)、[依赖清单](dependency-manifest.json)、[比较清单](comparison-manifest.json)、[关系说明](relation-review.json)、[claim确认](claim-confirmation.json)、[交付自查脚本](verify_delivery.py)、[实际报告](delivery-self-check.json)。checker只核字节/版本diff/执行记录/输出SHA/回执/链接，不重新运行数学，也不代替证明或真实阅读。

原程序的通用LP、arbitrarysink最终matroid、anchor未知OPT、一般UM结构生成均不因finite PASS而完成。正式第三阶段超图未写；已有其它Boss正文未改。服务端实际available查询的下一5原样ID及scope在工作区next-candidates.json，原件未预读/写。
