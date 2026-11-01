# DG4 真末回复与税投影证据

实际成功10源事务[原回执](original-claim-receipt.json)全文保留，pushed/Boss4/synced `1591bf9946b573b39e542805b4342fad396bd2c5`。本包只取[输入manifest](original-local-source-manifest.json)的dummy_dg四交集，不处理DI4/RootDH2。先前原子失败15不计成功claim，详[authority](claim-intersection-authority.json)。

四主源14364B全读，逐SHA/字节及当前owner Boss4核实。源只取Root已核本地输入；比较用提供safe local helper或前批冻结缓存，无clean show/网络/懒加载、无shared Git写/claim/done/checkpoint。

主源：

- [4d420007d7e1fdcd53a3 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/README.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/README.md)，2226B，SHA `96eab60902bfba59d5f9f866c46b206191b1d0a9f220a5cde3f2ada5963c3727`。
- [ed1e280f6a90223093d5 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/true_reply_cap.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/true_reply_cap.md)，5020B，SHA `7b81eb4cbb300a2f2a5fbb30d2f531db14ab8a1256a5a40cc43d86ff82353bda`。
- [067620eb2026799b77e6 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/true_reply_overlap_family.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/true_reply_overlap_family.md)，3594B，SHA `2c50dce042b5a9cf28b2228c96bc3b73d37aa5dc91f3cca130f5e0dc6ba00fbe`。
- [0ad80e479630f258c2ec — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/tax_projection_barrier.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/tax_projection_barrier.md)，3524B，SHA `96627b1953b7cd17bf4c6df9d97b4099940b363bc38016438216eb5ef5e49c2c`。

比较原件（完整读，仅比较不抵primary done）：

- [46b1b3c7907ee8c886ce — examples/customer_attraction/individual_security_failure.json](comparison/examples/customer_attraction/individual_security_failure.json)，SHA `bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a`。
- [4617d18c9d098ce255c9 — evidence/certificates/customer_attraction/individual_security_failure.json](comparison/evidence/certificates/customer_attraction/individual_security_failure.json)，SHA `d5c8fc3abe3acf7b4b61b776a957a13e49dfe276df517ee9ba4a47093a2792ab`。
- [b8b34c8ffdb400a99e25 — research/current/customer_attraction/aggregate_theta_counterexample.md](comparison/research/current/customer_attraction/aggregate_theta_counterexample.md)，SHA `320fc22d12aa33c6215275f121b910bc9c97c31180a04866de520d0a5ce95222`。
- [c6493e0e417aa311abbd — research/current/customer_attraction/last_two_floor.md](comparison/research/current/customer_attraction/last_two_floor.md)，SHA `cc48c1d7d4646b79f114be078a1bbf669a58b72fb2cc8f14e794fde52fee2280`。
- [b312212275551b29955a — evidence/certificates/customer_attraction/aggregate_theta_failure.json](comparison/evidence/certificates/customer_attraction/aggregate_theta_failure.json)，SHA `cf08edab0813de8eccee8d5466d15b40bd42c980da9b0b68c925f4ae80991010`。
- [c838c11dfaa7a54dcca8 — examples/customer_attraction/aggregate_theta_failure.json](comparison/examples/customer_attraction/aggregate_theta_failure.json)，SHA `be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf`。
- [1a1bf1f73c14d766e93a — research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md](comparison/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md)，SHA `f7f5d496681a3952159aa1a1c4299234aa2f59e14d6858ea12f2df2a5314665b`。
- [308b28acffe3e6fd5ca8 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/penultimate_floor_exchange.md](comparison/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/penultimate_floor_exchange.md)，SHA `ab893bd1d86adaf17b1180f58c8f4a76a47484364f902314474f8e87f25053b3`。

| 证据 | 实际范围 |
|---|---|
[safe local export manifest](local-comparison-export-manifest.json) | 四成功local exports；cap原py/JSON缺blob，不fallback |
[新定义检查源码](verify_true_reply_data.py) | 无original import/solver/LP |
[新检查result](new-data-check/result.json) | 两完整43策略；各258IC/126RC/216β1/36β2、83势值；480 atoms；m4−14/3 |
[新检查事件](new-data-check/event.json) | 一次exit0，授权pre-read阶段比较检查，不冒primary完成 |
[旧CZ数学核验复用](reused-cz-tax-check/manifest.json) | 同tax公式/表/六组旧形式重构；失败与成功原字节均保留，本批新run0 |
[实际比较结论](comparison-findings.json) | 旧机制归属、完整目录F/fresh extrema、有限LP边界、当前half范围 |
[正式比较快照](formal-context/inventory.json) | old tax/PAIR/36反例全文，旧source不再done |

本批原程序入口新运行0、LP0；新独立DG checker一次exit0，未导入原缺失audit_reply_cap。每输入258包含43self、215真正改变行动比较；126=6倒二背景×21无序主题对，非216有序计数。β1各216有序T/S行，β2各36独立T行另列。全部原输入/证书真实读取，34安全certificate的LP primal/dual只旁读保存，不冒新优化验证。

税source上批为comparison，现才本批primary；此前CZ同公式/表的独立checker已有真实两attempt/一success，本包逐SHA复制其全部成功和失败记录，不重复造数量。该checker不是缺失original poly程序；本批明确没有原字节入口run。

原文的约2.08459、798/942/954行都是LP来源声明，未取得完整原LP数据，不补造精确可行点/最优性/策略树。true_reply_cap.py/json亦缺；本包用新独立定义检查验证两指定fixture，不能冒全字节复现原报告。

两篇自足正文完整保RC/β参数族/所有源位同Q、十poly/全参数正性/真回复排除、两旧full SPE势反例的不同合同与README所有未完成方向。缺输入/历史OPEN/作者停止方向不改成当前half或清洗停止结论。

若需要重做新检查，请另建空目录，以绝对路径运行helper，避免覆盖本次证据。旧CZhelper不再运行；缺失原件仅等纯本地恢复，不自动联网补取。

