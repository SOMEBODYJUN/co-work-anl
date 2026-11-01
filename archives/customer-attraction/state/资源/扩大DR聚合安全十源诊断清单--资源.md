---
id: customer-attraction/expanded-dr-aggregate-security-ten-source-ledger
kind: resource
type_tag: 资源
title: 扩大DR聚合安全十源诊断清单
status: ten-sources-read; exact-boundary-retained; floating-diagnostics-retained-without-CAG-upgrade
summary: 十份 aggregate_security JSON 已逐一读取并与 P=161/v=56 的精确扩大DR边界及现有 CAG 对象对照。只有 dr_boundary_exact.json 是有理有限证书；其余九份是固定策略、固定查询或固定随机参数的扩大模型浮点诊断，不能证明或反驳 Q-CAG-HALF-6。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/aggregate_groups_dr_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/aggregate_groups_monotone_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_boundary_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_cag_policy_n5k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_diagthird.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_harmonic_diagonals.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_harmonic_diagonals2.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_harmonic_span_third.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_rational_query.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_groups_rational_query2.json
related_objects:
  - ../障碍/单调递减边际势的强安全聚合障碍--障碍.md
  - ../资源/边际势预算与全局正矩原稿的精确证据层次--资源.md
  - ../../tools/evidence/coverage-moment-and-potential-ledger-primary/related/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_boundary.md
---

# 读取与共同模型边界

十个源均来自同一冻结路径 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/`，固定六动作、三人、截断总数至三的扩大势模型。文件自身的 `status` 都是 `floating diagnostic in an enlarged model, not CAG evidence`，包括文件名含 `cag` 的 `dr_cag_policy_n5k4.json`。这些文件以 `Phi` 的删除位边际或分组策略 LP 作为输入，没有共同单位客户、客户均分、support 不变总收益或 Q-CAG-HALF-6 的全历史量词。

可复用的精确锚点是已有障碍对象：`dr_boundary_exact.json` 的有理证书与现有正文一致，路径 034，效用 `(0,105,56)`，总收益 `P=161`，两对手静态安全值 `v=56`；因而 `P-3v=-7`、`P-(5/2)v=21`，首两位 `105<112`。根级 verifier 还逐项核了 84 个势值、168 个单调差、252 个 DR 差、43 个有序 SPE 节点和 258 个比较，并直接标记 `not_a_CAG_input=true`。这只反驳扩大单调 DR 势模型中的强聚合桥，不反 CAG 的半覆盖命题。

## 十源逐项处置

| source id / 文件 | 实际参数与输出 | 与精确锚点的关系 | 处置 |
|---|---|---|---|
| `c8aa86cb9fff28595e0d` / `aggregate_groups_dr_n3k6.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；`best_objective=-0.00028858831866522723`；root `[0,3,4]`；浮点 `p≈(.26957854,0,.25995712,0,.22133670,.24912764)`；`value_lower≈.00258700515`、`welfare≈.00747242713`；`completed=1`。 | 组策略固定在同一 root，但浮点势/目标没有提供 84 值有理表、静态对偶或全策略量词；与 P=161/v=56 证书不是同一证据层。 | `retained` 浮点搜索诊断；独有参数与 witness 摘要入证据包，不升级。 |
| `de2d259f0873ec7f385e` / `aggregate_groups_monotone_n3k6.json` | 与上一项同 `k,n,trials,seed,policy,first`，但 `no_dr=true`；`best_objective=-0.0012265763671518558`；root `[0,3,4]`；`p≈(.22907233,0,.30046333,0,.21884828,.25161606)`；`value_lower≈.01099545329`、`welfare≈.03175978350`；`completed=1`。 | 去掉 DR 约束后的更负浮点目标只说明约束集合不同；它不构成 DR 反例，也没有 CAG 客户实现。 | `retained` 诊断；与上一项成对比较，标明 `no_dr` 差异。 |
| `e3b588abb45e1b524654` / `dr_boundary_exact.json` | `scope=Exact counterexample in monotone DR marginal-potential games, NOT CAG`；84 states、168 monotonicity、252 DR、43 nodes、258 comparisons；path `[0,3,4]`，utilities `[0,105,56]`，`W=161`，`security_value=56`，强缺口 7、弱缺口 21；query `4/15,0,4/15,0,1/5,4/15`；列出 21 个背景原/对偶值与 9 个负三阶差。 | 与现有 `单调递减边际势的强安全聚合障碍` 逐字段相符；pure diagonal witness `Phi(11)=Phi(1)=161` 破坏 CAG support 预算。 | `integrated` 到既有障碍对象；原 JSON 的精确摘要与 verifier summary 另存证据包。 |
| `9be3c9ec40db2d086b6a` / `dr_cag_policy_n5k4.json` | `k=4,n=5,trials=300,seed=22108,no_dr=false,policy=cag`；`best_objective=0.0`；`completed=300`，无 witness、无 exact certificate。 | 文件名虽含 CAG，正文 status 明确仍是 enlarged-model floating diagnostic；零目标是 300 次固定程序完成，不是 CAG 全称或无反例证明。 | `retained` 负信息/有限运行计数；不把 0 当 exact equality。 |
| `b6b1d089b32cec26f38d` / `dr_groups_diagthird.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `4/15,0,4/15,0,3/15,4/15`；`harmonic_diagonals=true,harmonic_repeats=false,third_positive=true,iterations=1`；`best_objective=-0.0002650208603540826`；root `[0,3,4]`，浮点 `p=(4/15,0,4/15,0,1/5,4/15)`；`completed=1`。 | 这是有限条件叠加下的浮点近零点；与精确 P=161/v=56 使用同一比例 query，但未输出有理势表或 exact check。 | `retained`；作为有限条件诊断并回链既有障碍/资源对象。 |
| `873a5ba24fd8ad9d0fe1` / `dr_groups_harmonic_diagonals.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `1/4,0,1/4,0,1/4,1/4`；`harmonic_diagonals=true,iterations=1`；`best_objective=0.0`；`completed=1`。 | 只有一个零浮点目标，没有 witness、势表、对偶或全策略枚举；不能解释为“存在精确无缺口”。 | `retained`；仅记录 query/条件/零目标。 |
| `60536949b37d8cc9b805` / `dr_groups_harmonic_diagonals2.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `27/100,0,26/100,0,22/100,25/100`；`harmonic_diagonals=true,iterations=1`；`best_objective=-0.0002582074389830061`；root `[0,3,4]`，`p=(.27,0,.26,0,.22,.25)`，`value_lower≈.00228083238`、`welfare≈.00658428969`。 | 与 rational_query2 仅约束开关不同（此项打开 harmonic diagonals）；两者都在同一固定组策略上给浮点近零差异，不是精确反例。 | `retained`；保存差异开关及浮点 witness 摘要。 |
| `20aa4c0a3b9dabb27a13` / `dr_groups_harmonic_span_third.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `4/15,0,4/15,0,3/15,4/15`；`harmonic_diagonals=false,harmonic_repeats=true,third_positive=true,iterations=1`；`best_objective=0.0`；`completed=1`。 | 与 `diagthird` 交换 `harmonic_diagonals`/`harmonic_repeats` 开关；同 query 仍只有浮点零目标，不能据此断言纯对角或三阶条件已足够。 | `retained`；作为开关对照，不重复复制数学对象。 |
| `fd6184f0d23198d919b8` / `dr_groups_rational_query.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `1/4,0,1/4,0,1/4,1/4`；`harmonic_diagonals=false,iterations=1`；`best_objective=0.0`；`completed=1`。 | 与 `harmonic_diagonals.json` query 相同但关闭 harmonic diagonals；零目标仍无 exact witness，说明仅查询/开关诊断不决定模型真值。 | `retained`；与上一项作重复参数对照。 |
| `af603eb58910860e9a46` / `dr_groups_rational_query2.json` | `k=6,n=3,trials=1,seed=22112,no_dr=false,policy=groups,first=0`；query `27/100,0,26/100,0,22/100,25/100`；`harmonic_diagonals=false,iterations=1`；`best_objective=-0.0002927880925814152`；root `[0,3,4]`，`p=(.27,0,.26,0,.22,.25)`；`value_lower≈.00258629482`、`welfare≈.00746609636`。 | 与 `harmonic_diagonals2.json` 同 query/p，但关闭 harmonic diagonals 后 objective 略变；两份都只是固定策略浮点输出。 | `retained`；成对保留开关差异，不升级。 |

## 定义域、量词、假设与证书字段的比较

精确对象的定义域是多重集势 `|q|≤3`，每个动作删除边际给效用，且穷尽所有截断格单调/DR 差和完整有序历史偏离。其静态安全值对所有 21 个含重复竞争背景取最小，并给出有理 query、背景值、对偶背景和 exact value。十源中的九份 JSON 只固定一个分组/策略生成器、一个 query（有时是随机 seed 与一次 iteration），输出浮点 `best_objective`、`value_lower`、`welfare` 和 `completed`；它们没有全策略量词、没有客户非负重数、没有有理原/对偶证书，也没有可验证的 CAG support 条件。

`no_dr=true/false`、`harmonic_diagonals`、`harmonic_repeats`、`third_positive` 等只是程序约束开关；开关变化造成目标的微小差异不能解释成数学边界。所有九份共同保留 `status` 的扩大模型警告。尤其 `dr_cag_policy_n5k4` 的 `policy=cag` 只表示生成器模式，不能覆盖单位客户均分模型。

## 缺口和接续

这些诊断没有提供从扩大势到合法共同客户集合的编译。exact JSON 自己的 `Phi(11)=Phi(1)` 与 `P(1)=161,P(11)=0` 已给出 support 预算冲突：在 CAG 中同一 support 的总收益应相同，且 `2Phi(11)=3Phi(1)`；因此不得将其 `P=161,v=56` 称为 CAG half 反例。浮点 `0.0` 也没有符号等式含义，负的 `best_objective` 更没有在扩展策略空间中证明普遍失败。

后续若要复用，唯一可靠路线是回到既有障碍的有理表和 verifier；若要证明 CAG 结论，则必须另行给出客户类型、均分收益、完整历史纯 SPE 和所有离轨平局的证书。当前十源的新增信息限于 query/seed/trial/开关及有限浮点目标，未升级六人半覆盖结论。
