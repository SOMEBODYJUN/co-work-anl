# CZ 背景交换六主源完整证据

原9源事务回执[原样保全](original-nine-claim-receipt.json)，pushed/Boss4/synced `8f745454c2c7b5f51fe4663f6b90c47102a154ef`。本包只取[local manifest](original-local-nine-source-manifest.json)的dummy_cz六交集，不处理root_cy三源，详[authority](claim-intersection-authority.json)。

六主原件29851B全部逐节实读并核SHA。原件仅使用Root已纯本地导出；本地比较以Git cat-file blob、GIT_NO_LAZY_FETCH=1及protocol.allow=never读取。缺blob后未clean show/未网络/未懒加载/未shared Git写，不重试认证。

主源：

- [30233aa3dc390de50cbd — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/README.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/README.md)，2785B，SHA `3a92c6260151d59140838eafa31e991b965ade25984c06c1f627faad0b143de6`。
- [c1f1893c098fea173461 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/any_player_exchange_v2.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/any_player_exchange_v2.md)，5506B，SHA `4ed31079f8448b62342d7dab107fe48469024fcd88dbb8a2a7d54527eebb3f21`。
- [4dcb7a026edd930bc08d — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/global_aggregation_obstruction.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/global_aggregation_obstruction.md)，3378B，SHA `694ce6de895b71998d24cdd8238d7aa6de63f979af23611ac08e0be3921bb519`。
- [55bf4c47a20768752313 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/outcome_orbit_quotient_review.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/outcome_orbit_quotient_review.md)，7870B，SHA `ef6b66e8ac40387913de87eb4477b50d9a1fc355235e903802923a4c0fe2726f`。
- [308b28acffe3e6fd5ca8 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/penultimate_floor_exchange.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/penultimate_floor_exchange.md)，7771B，SHA `ab893bd1d86adaf17b1180f58c8f4a76a47484364f902314474f8e87f25053b3`。
- [d9911ecd909a9613bbb1 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/root_review.md](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/root_review.md)，2541B，SHA `e326e1bdc022d69dd1ff75e679256102c717fa9e85050081b32d434a74f51e6c`。

已完整读取比较原件（仅比较，不抵primary done）：

- [4d420007d7e1fdcd53a3 — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/README.md](comparison/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/round2/README.md)，SHA `96eab60902bfba59d5f9f866c46b206191b1d0a9f220a5cde3f2ada5963c3727`。
- [0ad80e479630f258c2ec — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/tax_projection_barrier.md](comparison/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/background_exchange/tax_projection_barrier.md)，SHA `96627b1953b7cd17bf4c6df9d97b4099940b363bc38016438216eb5ef5e49c2c`。
- [9c75087e540ebd1d488a — research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/outcome_orbit_quotient.md](comparison/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/outcome_orbit_quotient.md)，SHA `8d10c5e87e9742f335c70f274be5c1845a18d36c416ab10bf66d7ad1645c842a`。
- [1a1bf1f73c14d766e93a — research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md](comparison/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md)，SHA `f7f5d496681a3952159aa1a1c4299234aa2f59e14d6858ea12f2df2a5314665b`。

| 证据/检查 | 真实范围 |
|---|---|
[缺本地比较清单](missing-local-comparison-inputs.json) | 7个缺blob，特别global质量表/审计代码；未读未跑 |
[新checker源码](verify_exchange_and_orbit_examples.py) | 独立标准库；不导入原程序/优化器 |
[第一次失败事件](data-check-initial-failed/event.json) | exit1；空交集多项式add缺零分支，源码/日志原样保存 |
[修正后事件](new-data-check/event.json) | 新空目录一次exit0；不是原入口重跑 |
[成功结果](new-data-check/result.json) | 98有限六组、10形式poly恒等式、m4 82>68、同时轨道/选择器例 |
[比较结论](comparison-findings.json) | 当前五人已证与一般/六人OPEN分开，root-v1/v2/root-review时态 |
[formal-context范围](formal-context/inventory.json) | 两全文旧正式对象、两只scope/精确结论比较，不代签整证书 |

**本批新原入口0**。原稿root声称运行过两个原audit，但缺本地代码/成功stdout/event，不将自报提升为本次执行。新独立helper共2尝试（首次失败保全，修复后成功），不虚称一次全程成功；一般全m证明是解析推导，poly用形式系数，不有限外推。

五人global点：只retain原稿W1/O/K/1100行及最小slack的精确声明。质量group_mass缺失，未独立验证其可行/最优，不是SPE。source-read-map和receipt对该主源明确retained、缺失比较不强勾；仍完整保全源内每个数学语义单元。

交换资源完整包含i固定过去/i=P/i=L、c_m锐保留行及非SPE真偏离；轨道review完整包含阈值递归/子集/同时群作用/稳定子群纤维/无等变确定选择器/normalize M1。没有程序搜索、外审、新颖性或half认证。

要复现新checker请使用另一个新空目录运行绝对路径，避免覆写当前logs/result。缺原件只等待纯本地恢复，不自动下载。任何后续global质量补证需另行明确实际输入及行域；本次不填虚构group_mass。

