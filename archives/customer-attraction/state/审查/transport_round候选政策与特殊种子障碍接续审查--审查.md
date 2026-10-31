---
id: customer-attraction/transport-round-policy-and-special-seed-obstacle-review-20261031
kind: review
type_tag: 审查
title: transport_round 候选政策与特殊种子障碍接续审查
status: complete-source-read-integrated-as-obstacle-not-skeptic-proof
truth_status: finite-policy-generation-and-negative-search-evidence; no SPE certificate or general half counterexample
review_level: full-source-read-comparison-with-early-security-and-stationary-transport-objects
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/n5_ten_attack_results.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/n5_ten_attack_results.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/policy_patterns.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/policy_patterns.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/two_special_seed_results.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/two_special_seed_results.json
evidence_paths:
  - archives/customer-attraction/tools/evidence/transport-round-obstacle-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/transport-round-obstacle-20261031/n5_ten_attack_results.json
  - archives/customer-attraction/tools/evidence/transport-round-obstacle-20261031/policy_patterns.py
  - archives/customer-attraction/tools/evidence/transport-round-obstacle-20261031/two_special_seed_results.json
related_objects:
  - ../计算/早期3227安全值增量证书--计算.md
  - ../定理/末两人回复循环静态运输恒等式--定理.md
  - ../审查/新策略安全锥与半顶点候选增量审计--审查.md
  - ../审查/逐人安全与全树流增量审查--审查.md
  - ../问题--问题.md

# transport_round 候选政策与特殊种子障碍接续审查

本审查完整读取三个冻结来源：`n5_ten_attack_results.json`、`policy_patterns.py`、`two_special_seed_results.json`，并与现行 CAG 安全值、末两人运输恒等式和新策略安全锥对象比较。三份来源都属于顺序单位客户/单位提供者主题均分模型；它们不是双设施客户负载模型，也没有给出六人 half 的一般结论。

## 1. 原件身份和证据副本

| source ID | 原路径 | blob | 字节 | SHA-256 |
| --- | --- | --- | ---: | --- |
| `0f19f68de85d151db2ce` | `history/source/notes/customer_attraction/transport_round/n5_ten_attack_results.json` | `dfcb38a5189ebb175313e8991c2cabc97a19d212` | 484 | `e5cd5c4e064f7d83cf63c33d5d8a3dd3f5b2614236d0f970a5e06fa145be598e` |
| `d5815c827837b12af614` | `history/source/notes/customer_attraction/transport_round/policy_patterns.py` | `5e402177d12bc314dc228d700fa3b2929022df77` | 6608 | `86d35720379e0d87dad1b8ef1654a7806fc1311d3f47043e5b009c352c8c9301` |
| `c54963f785a0ce87de2e` | `history/source/notes/customer_attraction/transport_round/two_special_seed_results.json` | `c077cd1e1502cc836a21bc9d06f3228f17776b5e` | 2249 | `5d237ce5fe98c34ed7f7047f94938b22a6760cc0ca568b9e9b68d3341221cec4` |

原件已保全到 `archives/customer-attraction/tools/evidence/transport-round-obstacle-20261031/`，manifest 记录双提交 source ref、字节与哈希。JSON 是结果记录，Python 是候选形式策略生成器；二者都不能单凭字段名升级为 SPE 证明。

## 2. `policy_patterns.py`：完整历史形式候选而非均衡证书

脚本定义 `GroupPolicy`，把主题分为若干 groups，并为**每个完整有序历史**定义动作。`pick` 在指定 group 的主题中按历史计数、固定旋转顺序取动作；`missing` 选择尚未出现的 group；`finish` 从给定前缀迭代到长度 `n`。候选包括：

* `cascade`、`ordered_cascade`：前缀阶段依次补缺 group，末段在某一 group 内轮转；
* `returning_minority`、`delayed_reversal`：在第二/第三层返回或延迟翻转 group；
* `first_deviator_chase`、`latest_deviator_chase`、`deviator_successor`：识别与 nominal 根路径不同的最早/最近偏离位置，改用相应 group 的旋转菜单；
* `ordered_pair_menu`：末段只在某 group 的两个主题间切换。

`candidates()` 实例化 9 棵形式策略：五人六/七/八主题的多组版本和六人八主题 cascade。脚本顶部明确写 `No equilibrium is asserted`，输出状态为 `FORMAL_POLICIES_ONLY_NOT_SPE_CERTIFICATES`。`summary` 只统计根终局、历史数、动作比较数、同计数不同动作见证和策略哈希；它不计算客户重数、收益、SPE 激励或安全锥。

该脚本的可复用内容是保持完整历史、重复主题和历史依赖平局的候选生成器。它不能替代 `Gamma` 全历史不等式、策略锥 LP 或完整证书；同计数历史出现不同动作见证正是不能压缩成匿名计数策略的证据。

## 3. `n5_ten_attack_results.json`：Gamma 攻击摘要

JSON 记录一个五人攻击批次：根候选为 `[4,5,6,7,8]`，`Gamma_rows=10661`，两个 aggregate trials 都为 `1.0`；三对 `double_trials` 的两个差值均为 `-0.0`。这些数值表示在该批输入和浮点/压缩计算下，聚合与双人尝试没有显示正向缺口或失败；它没有给出客户权重、完整策略证书、精确分母或 SPE 验证。

因此该 JSON 的数学用途是**负搜索证据**：在指定 Gamma 行域与测试策略下，没有找到可立即转成攻击的正残差。它不是“任意五人全历史均满足目标”的证明，也不是六人 half 反例。由于记录没有独立 source input，不能从 `Gamma_rows` 反推完整客户类型域。

## 4. `two_special_seed_results.json`：特殊种子扫描的失败状态

JSON 包含 10 组 `(q,d,e)` 参数。每条记录列出 `root_menus`、候选值 `v`、`best`、`desired_SPE` 和希望的均匀目标收益：

* `(q,d,e)=(3,1,0)`、`(4,1,0)`、`(5,1,0)` 的根菜单数为 6、50、158，`v` 约为 17.1211、17.8667、18.5750，`best=null`，`desired_SPE=false`；
* `(4,1,1)`、`(5,1,1)`、`(6,1,1)` 的根菜单数为 2、2、6，`v` 约为 18.5412、19.2846、20.0，仍无 `best`；
* `(8,2,0)`、`(9,2,0)`、`(8,2,1)`、`(9,2,1)` 的根菜单数为 6、50、20、2，均 `desired_SPE=false`、`best=null`。

希望收益向量在这些扫描中常高于 `v`，但来源没有给出能同时满足所有离轨历史的完整 SPE 策略；所以正确处置是“特殊种子尝试未找到目标”，不能写成存在一个低福利 SPE，也不能写成目标不可能。

## 5. 与现有安全值和运输对象的关系

现有 `早期3227安全值增量证书` 已保存同一 transport_round 方向的较早六主题三人有限证书，并明确只反驳两条一步 safety-value induction inequalities；`末两人回复循环静态运输恒等式` 则是任意形式策略下的解析定理，使用回复函数循环构造共同静态背景，和这些候选扫描不在同一证据层级。`新策略安全锥与半顶点候选增量审计` 已将固定 21 棵策略的精确 Gamma/LP 证书与浮点候选分开登记。

本批增量有三点：

1. `policy_patterns.py` 给出一组可重放的完整历史策略生成规则，并显式标注“不是 SPE 证书”；
2. `n5_ten_attack_results.json` 把 10661 条 Gamma 行和双试验零差值保留为负搜索结果；
3. `two_special_seed_results.json` 把 10 组特殊种子均未找到 `desired_SPE` 的事实保留为失败机制，而不是数学不可能性。

## 6. 接续和开放边界

若后续继续使用这些来源，应为每棵 `GroupPolicy` 先构造完整客户类型域、逐历史真实收益和 `Gamma` 行，再用精确有理 LP/锥证书验证；浮点 `v` 和 `best=null` 不能直接进入 theorem。需要连接当前六人目标时，必须额外处理空主题、重复主题、全部离轨平局和六位提供者完整历史；本批没有这些量词。

本批三源已实读、比较并保全。结论等级是“形式政策候选 + 负搜索/特殊种子失败记录”，不是 SPE 证书、一般半覆盖证明或完整反例。本批未执行 Git commit、push 或 `clean done`，Boss 串行 checkpoint 后再按 receipt 逐来源确认。
