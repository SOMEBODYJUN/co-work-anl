# Hall、重轻森林、价格凸化和匹配残余：五原程序资源

BE actual claim pushed/Boss4/synced，tip4492b986625e6f35ee2111d4ba145b7598646aa9，见[原回执](claim-confirmation.json)。5 primary 均独立 clean show 冻结导出核SHA；4原程序本批完整读，matching源码同SHA的AQ全读及BE主审计重读准确复用。另2依赖（Hall本批全读；baseline同SHA AX全读复用）与11比较来源，18份冻结原件。实际阅读不是只核whole SHA；manifest记逐份read_scope。

## 四个自足计算对象

1. [Hall双独立审计](../../../state/计算/Hall联合流与未知最优承诺双独立原程序--计算.md)：原任务阈值DFS与精确OPT/联合选择DFS分开，8123及301/122，恢复t与OPT、宏严格半阈值和δ0分支保真。
2. [关联森林整数性](../../../state/计算/重轻关联森林整数性原程序与标量趋二族--计算.md)：真实2机3任务、乘3缩放、一般关联树与非空heavy，实际标量检查不冒完整大矩阵。
3. [价格凸化/共同面](../../../state/计算/重轻价格凸化原程序的顶点对偶与共同重面核验--计算.md)：固定E_T/角色、13fixtures/5出口、k3共同5/3与目标4/3分开，精确最优价格全部流同big。
4. [安全GHMR与逃逸](../../../state/计算/大边匹配残余原程序的安全过滤与共享逃逸核验--计算.md)：所有真实T调度边保留、3375矩阵与实际171/265路径逃逸；AQ密化427/521不是同矩阵。

## 冻结原件、导入和历史

两个共同源提交68fad804ec5946cb296f77dc5b336308a66abf12、aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。

| ID | 原路径 | 字节 | SHA256 | 保留件 |
|---|---|---:|---|---|
| af4686084d064b7e5407 | tests/audits/unrelated_machines/hall_group_joint_flow_independent.py | 5485 | `fe1fd9f5f0ef1c83dd2681053fb0189070a1e846f1ce5374314a88340e0d296d` | [原件](original/tests/audits/unrelated_machines/hall_group_joint_flow_independent.py) |
| 5f96df68c24c9fd95b18 | tests/audits/unrelated_machines/hall_group_opt_promise_independent.py | 4756 | `2d684e9b61f052568ba8b82cc6cceee0697eaebc891c9da7acf5d00836ce7cdf` | [原件](original/tests/audits/unrelated_machines/hall_group_opt_promise_independent.py) |
| d0313ec00ee841aec13e | tests/audits/unrelated_machines/heavy_light_forest_integrality_boundary.py | 2132 | `7575f581c7eb2146369ae0bd2ab20677af19b8155110d5b921adc3070820ae75` | [原件](original/tests/audits/unrelated_machines/heavy_light_forest_integrality_boundary.py) |
| 470e4e74a976b65277e2 | tests/audits/unrelated_machines/heavy_light_price_convexification.py | 11885 | `d5515cc282f2dd64d15e701678c2cf881990da2862444a92d5469be20fdb2ee7` | [原件](original/tests/audits/unrelated_machines/heavy_light_price_convexification.py) |
| 2dd3413231d9b1499f4c | tests/audits/unrelated_machines/heavy_matching_residual.py | 14747 | `63f64a5497223e451374c74359dade6bec14ea507b3ed901d8f9495a699f2deb` | [原件](original/tests/audits/unrelated_machines/heavy_matching_residual.py) |
| 9fa5bc2e0157bd3693a9 | tests/audits/unrelated_machines/hall_group_joint_flow.py | 24011 | `ebcf08cbc82b841b86ab5c567d1abad79de0cf4b501bcffc24172fba3b94e46e` | [原件](original/tests/audits/unrelated_machines/hall_group_joint_flow.py) |
| e57947bc795251d373c3 | tests/audits/unrelated_machines/rounding_and_gap.py | 12108 | `5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a` | [原件](original/tests/audits/unrelated_machines/rounding_and_gap.py) |
| 5fc9e049f0a8a7aaaaed | evidence/runs/unrelated_machines/hall_group_joint_flow_independent.json | 439 | `083f190d1bc5f38cf8561204fa6aeabf29d90e095b188066f69e6b37d6815e44` | [原件](comparison/evidence/runs/unrelated_machines/hall_group_joint_flow_independent.json) |
| 2848badca09c5d4df4d8 | evidence/runs/unrelated_machines/hall_group_opt_promise_independent.json | 518 | `3ddfa89f6477203be0c1e31b2f799c89db0c70d5122e6b2d3521d0c0d01b7503` | [原件](comparison/evidence/runs/unrelated_machines/hall_group_opt_promise_independent.json) |
| 15369ef15836823a99b9 | evidence/runs/unrelated_machines/heavy_light_price_convexification_release_audit.json | 4545 | `82c5d76407d0f635f46b77671673b55f1d39b3cbc3984609b71f424d06fdc314` | [原件](comparison/evidence/runs/unrelated_machines/heavy_light_price_convexification_release_audit.json) |
| b13ff01a2215f76cad57 | evidence/runs/unrelated_machines/heavy_matching_residual_audit.json | 9849 | `7ec7968f54cff7bc46452cbcadbf6969e968eab1af970e7c6abed256bbde591a` | [原件](comparison/evidence/runs/unrelated_machines/heavy_matching_residual_audit.json) |
| 326d6af1da65fbe4ab4c | research/current/unrelated_machines/hall_group_joint_flow.md | 11876 | `10aabd8e9cc0eccf10974f94e23633f6d1034313348a69ceac003bb876af5b2b` | [原件](comparison/research/current/unrelated_machines/hall_group_joint_flow.md) |
| 3d6873791bece71f26a0 | research/current/unrelated_machines/heavy_light_forest_integrality_boundary.md | 4405 | `f1e62cf0b325b623cc827bb11c1aee2f7b930d7bc8112aba14f39a12a4e0b31f` | [原件](comparison/research/current/unrelated_machines/heavy_light_forest_integrality_boundary.md) |
| 5ba61c0ba5e619cdb3d2 | research/current/unrelated_machines/heavy_light_price_convexification.md | 16967 | `b63dd00ddb4f202b21988ce1703b19f90d4f703815bdf1e5982a4e7f5045d0b9` | [原件](comparison/research/current/unrelated_machines/heavy_light_price_convexification.md) |
| 483f65ab900b2bf9f8bf | research/current/unrelated_machines/heavy_matching_residual_and_escape.md | 13978 | `3a4541eca4b8edbe02a37c3558f934e092d27a175c4ed6786c66dbeebb2422df` | [原件](comparison/research/current/unrelated_machines/heavy_matching_residual_and_escape.md) |
| 389c9eda10e6ce9f39a4 | research/reviews/unrelated_machines/hall_group_joint_flow_review.md | 8846 | `7ddf4f1b7c4bfcd5003178e30723709bd00d4a00c11d5d9a999903f2544e96b8` | [原件](comparison/research/reviews/unrelated_machines/hall_group_joint_flow_review.md) |
| 943319840138764f0f61 | research/reviews/unrelated_machines/heavy_light_forest_integrality_boundary_review.md | 1760 | `ffecb4b1919896409322aa49b0138540ba68e8421607192df4cc8e6b7ee8ad64` | [原件](comparison/research/reviews/unrelated_machines/heavy_light_forest_integrality_boundary_review.md) |
| ad117632752525a91aa0 | research/reviews/unrelated_machines/heavy_light_price_convexification_review.md | 4945 | `d5c036abbefe330b9c37e25f1dc4019e49f97ef421346bd8f9c4caf75f7b14e1` | [原件](comparison/research/reviews/unrelated_machines/heavy_light_price_convexification_review.md) |

[5 primary](source-manifest.json)、[2依赖](dependency-manifest.json)、[11 comparison](comparison-manifest.json)。Hall两程序自行生成原任务并调用候选solve/solve_promise，候选main不运行；price和matching用baseline具体函数，baselinemain不运行。没有runpy无guard的隐含审计。matching文件AQ只被调用filter，本次standalone原审计是新增执行；同SHA源码阅读复用不等于伪造旧主审计运行。

## 本批真实5次原CLI，各一次、全exit0

| 入口 | stdout | stderr | 执行记录 |
|---|---|---|---|
| Hall joint independent | [输出](runs/hall-joint-independent.stdout) | [stderr](runs/hall-joint-independent.stderr) | [记录](runs/hall-joint-independent.execution.json) |
| Hall OPT promise independent | [输出](runs/hall-promise-independent.stdout) | [stderr](runs/hall-promise-independent.stderr) | [记录](runs/hall-promise-independent.execution.json) |
| forest integrality | [原Python repr](runs/forest-integrality.stdout) | [stderr](runs/forest-integrality.stderr) | [记录](runs/forest-integrality.execution.json) |
| price convexification | [输出](runs/price-convexification.stdout) | [stderr](runs/price-convexification.stderr) | [记录](runs/price-convexification.execution.json) |
| matching residual | [输出](runs/matching-residual.stdout) | [stderr](runs/matching-residual.stderr) | [记录](runs/matching-residual.execution.json) |

[完整argv/cwd/秒数/代码SHA](runs/execution-manifest.json)、[16个运行附件指纹](artifact-manifest.json)、[数学运行scope](mathematical-execution-scope.json)。补充数学进程0，导入主审计体0，完整Hall候选主审计与baselineaudit0。本包的JSON字段比较和完整性脚本不执行数学源。各随机/枚举输入由完整原码、精确参数和seed重建；原CLI没有全量dump所有原矩阵/每个DFS证书，不宣称本包含那些附件。

[历史全字段比较](historical-comparison-and-version-scope.json)：Hall2与matching三JSON全结构相等，包括matching61行；price新输出所有计算字段相等，旧另command/base_commit。forest无挪用另一族JSON，只保本次真实repr。旧独立审查者的背景/先Exact/读后身份属于历史，不倒填本轮blind。price最初hash到发布三nonfatal和forest乘3缩放都已按真实review核对。

## 关系、自查与复制

[关系审查](relation-review.json)含7份已读正式页的独立冻结快照：之后共享页如修provenance，不会使本批过去比较snapshot的SHA失效。程序安全、凸化的共同H缺口、关联森林整数性和特殊Hall构造不是一项一般UM算法；仅阶段二，不写第三阶段超图。

发现既有“重轻森林整数性与价格凸化冻结审查增量”页source_ids第一项串入frozenmacro、source_refs缺_review、第一evidence串源。数学段保持；另向root交独立最小errata proposed/patch供实读后应用，不改共享页、旧done或旧认领。

[5逐源receipt](../../../../../cleanup/workspaces/Boss4/r3-um-next-actual-audit-primary/semantic-receipts.json)、[精确copy清单](../../../../../cleanup/workspaces/Boss4/r3-um-next-actual-audit-primary/copy-files.json)、[实际下一5候选](../../../../../cleanup/workspaces/Boss4/r3-um-next-actual-audit-primary/next-candidates.json)。[自查代码](verify_delivery.py)只核保存字节、输出字段、链接和完整清单；stage严格tree=manifest，repo只核列出文件，实际[报告](delivery-self-check.json)不代替数学审查。没有修改任何其它Boss正文。
