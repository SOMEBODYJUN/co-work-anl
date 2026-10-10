# 顺序客户吸引博弈：共同目录的半覆盖猜想

**活跃目标：** [Q-CAG-HALF](../../questions/customer_attraction_half_coverage.md)：
任意人数、任意有限共同主题目录，全部有序历史依赖的纯 SPE 都覆盖最优的一半。
这个任意人数目标尚未证明，也没有本轮目标反例。
恰三人已由 [CA-THREE-SHARP-5-3](three_player_sharp.md)完整证明锐界：
全部纯 SPE 的 `OPT_3≤(5/3)W`，下界达到，包含全部历史依赖平局。
经两路独立内部审查；外部审查、新颖性未认证。
恰四人已有 [CA-FOUR-UPPER-1499-750](four_player_bound.md)：`OPT_4≤(1499/750)W`；
合法根偏离与后继节点比较闭合精确非负恒等式，经过独立内部审查。
一般目录的目标现只剩五人及以上；零背景总税仍开放。

新 [客户极大关联层级定理](laminar_incidence_bound.md)严格扩大 sunflower 目录类：
客户在极大主题间的关联集合为 laminar 时，任意人数、任意内部子主题、全部历史纯SPE
都有锐界 `OPT_n≤|C|+(2−1/n)(W−|C|)`。这不是一般目录结论。
[聚合θ反例](aggregate_theta_counterexample.md)证明每个n≥3都可能 `W<nθ_n`；
36客户三人证书经独立精确核验。[混合安全值](oblivious_security.md)仍有锐下界
`v_n≥OPT_n/(2n−1)`，但可信顺序续局下的逐人或总预算桥保持开放。

本分支使用 [CAG-MODEL](model.md)：客户价值固定均分，没有客户侧优化。
它与仓库原来的主动原子客户设施模型独立。不能借用原模型的因子 2 存在性，
也不能把静态 CAG 的 Nash 结论自动用于顺序 SPE。

## 定义和依赖地图

`CAG-MODEL` → `CA-EXACT-PURE-SPE-ALL` → 有限实例的全部终局及完整有序历史证书。
最后这一步是算法正确性，不是 `Q-CAG-HALF` 的普遍福利证明。

`CA-SPE-NON-PNE` 排除静态 Nash 的直接导入。
`CA-HISTORY-TIES` 排除未经证明的匿名平局与收益次序简化。
`CA-RESIDUAL-NO` 排除逐人遗漏收益保证及其平均化替代。
`CA-PORTFOLIO-MATCHING-NO` 进一步排除最优主题与真实单步偏离的足额匹配收费。
这些失败证书限制相应证明路线，不反驳主目标。

`CAG-MODEL` → `CA-TWO-REMAINING-TAX` 严格控制任意固定历史下恰两位剩余玩家的
收益损失；无背景时重构文献 $3/2$。税预算可以望远镜，但任意人数的首步机会成本桥已被
[CA-TAX-BRIDGE-NO](tax_bridge_counterexample.md)在空背景三人否定，
一般合法背景的总税也被 [CA-GENERAL-TAX-NO](general_tax_counterexample.md)否定。
零背景总税仍开放；不能沿旧逐层桥推出任意人数半覆盖。

`CAG-MODEL` + `CA-TWO-REMAINING-TAX` → `CA-THREE-UPPER-142-81`，
加入实际末位节点比较和根偏离的逐客户保底后，得到完整三人上界。
`CA-STRATEGY-CONE` → 固定完整策略下全部客户重数的精确线性优化及对偶证书；
样本策略不涵盖全部策略锥，不能作一般人数上界。


`CA-COVERAGE-OPPORTUNITY-NO` 进一步排除用当期收益各自支付当期最优补全损失。
[在轨AAB反例](coverage_opportunity_counterexample.md)保留完整历史策略。
全局望远镜余额仍是精确表示，需允许跨步骤支付，尚无一般证明。

`CAG-MODEL` + `CA-TWO-REMAINING-TAX` → `CA-FOUR-UPPER-1499-750`，
其独立于三人定理；证明明确保留根偏离后的三个后继主题及其各自最优性。
`CA-LAST-NODE-OPT-TAX` 在税页§6定位根税反例的必要末位收益条件。

`CAG-MODEL` → `CA-THREE-SHARP-5-3`：八类实际和真实离轨节点比较，
配对membership消去及双线性非负表给三人完整锐界。它不依赖税桥。
旧 `CA-THREE-UPPER-142-81` 提供不同的固定背景两人税应用机制，保留为可复用推导。

`CA-DISJOINT-MAXIMA-2M1` 用完整singleton机制及严格扩张的真实续局，
证明共同核心删除后极大花瓣互不相交类的任意人数锐界；内部子主题可任意交叠。
`CA-UNIFORM-PORTFOLIO-TWO` 给任意背景恰两剩余人的平均真实偏离恒等式；
`CA-UNIFORM-ROOT-GAP` 保留更强的任意人数平均接口为开放义务。
`CA-FIVE-LIFT-ROWS-NO` 排除指定五人460行松弛模板，辅助O不是实际OPT。
`CA-CREDIBLE-CONTINUATIONS` 的菜单构造覆盖全部完整策略；有限采样和联合MILP候选
仍需精确核验，不能从所选锥推断全部目录。

`CA-LAST-TWO-FLOOR` 在任意固定历史给最后两人分别保底局部θ(P)，
由它和每人K/n推出 `CA-ALL-N-WELFARE-4N` 的较弱通用界。
`CA-LAST-FLOOR-ALL-PLAYERS-NO` 用独立重放的四人完整策略否定把θ保底扩至所有人。
上传代码的递推与 `CA-EXACT-PURE-SPE-ALL` 相同；Möbius客户重数构造是本仓库新增接口，
其通用范围由下一项独立证明，不能仅由这个有限反例推广。

[Möbius编译](mobius_compiler.md)现已单独证明子集势的唯一signed客户反演、
安全正偏置下所有完整历史的无重复行动嵌入，以及正偏置不能保坏福利比的边界。
它不是任意匿名计数收益表编译；一般猜想没有由此升级。
[三剩余人背景利润锐界](three_remaining_profit_bound.md)给 `F3(b)≤(5/3)R_b(实际)`；
[四剩余人背景利润界](four_remaining_profit_bound.md)给 `F4(b)≤(1499/750)R_b(实际)`。
四人推广的比较聚合需要新背景校正，不能裸移根税。
两者均经独立内部审查；非零背景的剩余利润与根覆盖严格区分，五人根目标仍开放。

## 文件地图

| 路径 | 数学资产与何时使用 |
| --- | --- |
| `research/current/customer_attraction/model.md` | 定义单位客户均分、完整历史 SPE 和最优覆盖；任何证明或实验先核对量词。 |
| `research/questions/customer_attraction_half_coverage.md` | 主目标、已知文献边界、当前收费义务；继续研究时先读。 |
| `research/current/customer_attraction/exact_solver.md` | 集合值逆向归纳的必要性、充分性及全历史证书重构；修改枚举器时必须重读。 |
| `research/current/customer_attraction/literature.md` | 一手文献模型条件及不可直接导入的桥梁；静态/顺序、共同/异目录不能混淆。 |
| `research/current/customer_attraction/continuation_lemmas.md` | 已确认小反例、收益保证和失败机制；攻 residual 或匿名平局路线前必读。 |
| `research/current/customer_attraction/portfolio_matching_counterexample.md` | 唯一最优组合的两种真实偏离匹配均不足额；重新采用最优组合收费前必读。 |
| `research/current/customer_attraction/two_remaining_tax.md` | 固定背景两人税界的非负恒等式、条件性归纳及式 (9) 被反例否定的边界；当前证明路线入口。 |
| `customer_attraction/` | 本模型唯一规范有限精确实现；返回全部纯 SPE 终局，不声称多项式时间或普遍福利。 |
| `tests/test_customer_attraction.py` | 独立完整有序策略枚举 oracle、定义级证书检查和边界回归。 |
| `tests/audits/customer_attraction_search.py` | LCM 缩放整数的独立有限攻击，固定种子及重数参数；新的搜索不能冒充证明。 |
| `evidence/runs/2026-10-09/customer_attraction_search.json` | 冻结的有限搜索范围和摘要；零反例只对所列输入成立。 |
| `history/source/notes/customer_attraction/origin_2026-10-09.md` | 原始目标、核对位置和恢复基线；不保存聊天或认证信息。 |

| `research/current/customer_attraction/three_player_bound.md` | 三人142/81完整代数证明、逐客户系数与合法SPE比较；四人以上推广前先读。 |
| `research/current/customer_attraction/tax_bridge_counterexample.md` | 空背景首步税桥失败及总根税等号；排除再次使用旧逐层归纳。 |
| `research/current/customer_attraction/general_tax_counterexample.md` | 实际到达非零背景的总税失败、无限族、同主题根边界；区分剩余利润与覆盖。 |
| `research/current/customer_attraction/strategy_cone.md` | 固定完整策略重数锥、紧截面及精确Farkas证书；有限攻击和全锥认证的差别。 |
| `research/current/customer_attraction/literature_followup.md` | 追加一手文献时间模型与目录条件核查；set packing和短视反应不能直接导入。 |

| `research/current/customer_attraction/coverage_opportunity_counterexample.md` | 十一客户完整SPE否定逐期最优覆盖补全收费；保留多步余额及全局望远镜身份。 |

| `research/current/customer_attraction/four_player_bound.md` | 四人1499/750完整真实偏离证明、全部128非负系数与一般合法比较接口；探索五人以上时先读，不能只沿实际路径推导。 |
| `tests/audits/customer_attraction_four_player.py`、`tests/audits/customer_attraction_four_player_independent.py` | 互不导入的精确系数与最优覆盖比较核验，冻结结果在同名evidence/runs路径；不是有限策略代替全称证明。 |
| `research/current/customer_attraction/three_player_sharp.md` | 三人锐5/3完整证明、真实L_i/Q/R回复、八类SPE比较和非负余项表；当前三人结论首读入口。 |

| `research/current/customer_attraction/disjoint_maxima_bound.md`、`tests/audits/customer_attraction_disjoint_maxima.py` | 任意人数结构子类完整证明与独立完整有序策略审计；删除共同核心后的极大花瓣条件不可省略。 |
| `research/current/customer_attraction/global_new_uniform_portfolio_two.md`、`tests/audits/customer_attraction_uniform_portfolio.py` | 任意背景两剩余人真实偏离平均恒等式；任意人数推广仍开放。 |
| `research/current/customer_attraction/five_player_lift_obstruction.md`、`tests/audits/customer_attraction_five_lift.py` | 指定460行模板障碍及23mask有理证书，O为辅助变量而非实际OPT。 |
| `research/current/customer_attraction/credible_continuations.md`、`tests/audits/cone_attack_credible_variants.py`、`tests/audits/cone_attack_joint_milp.py` | 完整可信菜单、两棵所选策略及联合候选接口；精确原始/对偶和全历史核验边界。 |

## 复现入口

新增接口与对应精确审计：

- [上传工具审计](uploaded_tool_audit.md)：`tests/audits/customer_attraction_uploaded.py`。
- [末两人逐人保底](last_two_floor.md)：`tests/audits/customer_attraction_last_two_floor.py`。
- [Möbius编译](mobius_compiler.md)：`tests/audits/mobius_compiler_audit.py`。
- [三剩余人利润界](three_remaining_profit_bound.md)：`tests/audits/customer_attraction_three_remaining_profit.py` 和 `customer_attraction_three_remaining_independent.py`。
- [四剩余人利润界](four_remaining_profit_bound.md)：`tests/audits/customer_attraction_four_remaining_profit.py` 和 `customer_attraction_four_remaining_independent.py`。
- [极大关联层级锐界](laminar_incidence_bound.md)：`tests/audits/customer_attraction_laminar_incidence.py`。
- [聚合θ反例](aggregate_theta_counterexample.md)：`tests/audits/customer_attraction_aggregate_theta.py` 和 `customer_attraction_aggregate_theta_independent.py`。
- [混合安全值锐界](oblivious_security.md)：`tests/audits/customer_attraction_oblivious_security.py`。
- [真实顺序的根税边界](two_remaining_tax.md)：`tests/audits/customer_attraction_ordered_tax_boundary.py`。

以上审计默认只打印新输出，`--output` 拒绝覆盖冻结报告；已登记报告见 `evidence/runs/2026-10-10/`。

从仓库根运行：

```sh
python3 -m unittest tests.test_customer_attraction -v
python3 tests/audits/customer_attraction_continuations.py
python3 tests/audits/customer_attraction_portfolio_matching.py
python3 tests/audits/customer_attraction_tax.py
python3 tests/audits/customer_attraction_three_player.py
python3 tests/audits/customer_attraction_four_player.py
python3 tests/audits/customer_attraction_four_player_independent.py
python3 tests/audits/customer_attraction_three_player_sharp.py
python3 tests/audits/customer_attraction_tax_bridge.py
python3 tests/audits/customer_attraction_general_tax.py
python3 tests/audits/customer_attraction_coverage_opportunity.py
python3 tests/audits/customer_attraction_strategy_lp.py --self-test
python3 tests/audits/customer_attraction_disjoint_maxima.py
python3 tests/audits/customer_attraction_uniform_portfolio.py
python3 tests/audits/customer_attraction_five_lift.py
python3 tests/audits/cone_attack_credible_variants.py --verify evidence/runs/2026-10-09/cone_attack_credible_selected.json
python3 tests/audits/cone_attack_joint_milp.py --self-test
python3 -m customer_attraction examples/customer_attraction/residual_counterexample.json --verify evidence/certificates/customer_attraction/residual_counterexample.json
```

完整策略随历史树增长，有限求解器不是计算复杂度突破。直接有理数反例证明
和算法正确性的完整归纳已经写出；主目标的全部人数论证仍缺，外部同行评审未记录。

## 上传包复核入口（2026-10-10）

- [uploaded_tool_audit.md](uploaded_tool_audit.md)：原保存策略、精确θ/OPT、实现机制比较；采用逐客户定义重放全部离轨历史，区分构造新增与枚举同机制。
- [last_two_floor.md](last_two_floor.md)：任意背景的局部末两人逐人保底、通用较弱福利界及所有量词边界；尝试推广逐人保证时先读反例。
- `history/source/notes/customer_attraction/uploaded_2026-10-10/`：本轮上传原稿、构造代码、完整策略和原校验值，保留原始字节；原稿的Git失败报告是来源历史，不代表当前仓库状态。

```sh
python3 tests/audits/customer_attraction_uploaded.py
python3 tests/audits/customer_attraction_last_two_floor.py
```

## 新表示与固定背景接口（2026-10-10）

`CA-MOBIUS-BOOLEAN` 给任意有理子集势唯一signed客户重数；其重复计数扩张也被固定。
`CA-MOBIUS-FULL-HISTORY-EMBED` 在p≥n、足够大均匀正偏置下，保留禁止重复的边际收益游戏
在合法历史上的全部SPE，并正确处理所有重复离轨历史。
`CA-MOBIUS-BIAS-BARRIER` 证明这个安全编译器的福利偏置过大，输出自身严格满足半覆盖。
它是策略/收益障碍构造工具，不是一般反例编译器；小偏置必须另审完整策略。

`CA-THREE-REMAINING-PROFIT-5-3` 在任意合法背景、每个完整历史纯SPE上证明剩余三人的
总利润达到同背景最优的3/5。零背景回到旧三人锐界；一般末三人的组合接口保留
最优主题重数d和背景b，但尚不能闭合根半覆盖。

| 完整路径 | 资产及使用时机 |
| --- | --- |
| `research/current/customer_attraction/mobius_compiler.md` | 双反演唯一性、全历史fresh归纳、正化的保持范围、福利偏置与匿名count障碍；设计客户重数或声称保策略时先读。 |
| `tests/audits/mobius_compiler_audit.py`、`evidence/runs/2026-10-10/mobius_compiler_audit.json` | 编译、势差、完整策略投影和重复历史的精确检查；不是一般福利搜索。 |
| `research/current/customer_attraction/three_remaining_profit_bound.md` | 三剩余人真实Li/Q/R'比较、任意背景二次非负系数及末三人组合接口；使用背景利润预算时读取。 |
| `tests/audits/customer_attraction_three_remaining_profit.py`、`tests/audits/customer_attraction_three_remaining_independent.py` | 分别从显式余项多项式和原始八类slack重构全部系数，冻结JSON同名位于`evidence/runs/2026-10-10/`；修改恒等式时必须复跑。 |

```sh
python3 tests/audits/mobius_compiler_audit.py
python3 tests/audits/customer_attraction_three_remaining_profit.py
python3 tests/audits/customer_attraction_three_remaining_independent.py
```

## 2026-10-10：全sunflower与通用superset席位

[Sunflower极大目录](sunflower_maxima_bound.md)覆盖任意内部子主题，甚至遗漏共同核心；任意至多两个不同极大主题均在类内。
`CA-SUNFLOWER-MAXIMA-2M1` 通过superset支配与席位归纳给任意人数锐界，无需SPE→PNE。
同稿 `CA-MAXIMA-SUPERSET-SEATS` 给任意目录每人≥第n大私有/共享混合席位，尚缺一般共享union预算；
`CA-SUNFLOWER-PRIVATE-GAP` 单独给额外私有缺口下的全历史极大行动与singleton PNE。
独立审查见 `research/SUNFLOWER_MAXIMA_REVIEW_2026-10-10.md`，精确复现 `python3 tests/audits/customer_attraction_sunflower_maxima.py`。
