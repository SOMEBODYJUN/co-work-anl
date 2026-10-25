# 仓库整理盘点审计：恢复路径、唯一来源与个人区状态

盘点对象 `/workspace/scratch/ad730879ba4e/co-work-anl`。**Git基线4b57ec59与本轮本地工作树分开统计**：父任务用Git树验证该基线的可见非缓存个人区是6142文件、113 actor、707 README；本审计本地观测另含本轮新建2文件、1 actor、1 README。本审计不运行 Git、不读凭据、不发远端消息、不修改仓库共享文件。统计采用 Python pathlib，排除任一以点开头路径组件及 Python 缓存。文件盘点、入口状态筛查和数学证明已审是三件事；本审计不重做全部数学证明。

## 最重要的可执行结论

1. 默认读取链应收束成根四入口、AGENTS、模型、短地图和一份短衔接上下文。长一般稿、逐项总账、逐文件数学地图、个人区恢复索引均改为按当前义务查阅。根页保留目标 OPEN、精确范围、断点与链接，不复制成果长表。
2. 旧个人区索引不是当前“全部”库存：旧最终集合74 actor/4130原始路径；同一可见非缓存口径4129。Git基线 **113 actor、6142文件、707份README**，同口径比旧快照新增2013路径、39 actor、无删除；本轮本地工作树另含1 actor/2文件/1 README，故本地观测是114/6144/708。须保留旧哈希快照为历史证据，再增加当前精简路由，不能覆盖旧原字节或继续称旧表为全部现状。
3. 总账也有范围漂移：旧首段声称71数学正文+1 README，而当前数学目录为73正文+1 README。总账遗漏 `incidence_lp_dynamic_budget.md` 与 `optimal_first_action_branch_gap.md`；逐文件数学README已出现全部74个文件。补两条准确分类和来源即可，无需另造一份总账。
4. 所有个人README应作为带历史上下文的恢复入口，不能把其中旧OPEN或旧研究指令当现行权威。至少已有静态最优匹配、弱iid、fresh覆盖归纳、实际分数税和逐位置菜单的明确旧状态；须由共享读取层给更正路由，不擅自批量改别人的历史来源。
5. 6144个人文件中2120份Markdown的SHA-256逐字重复组为0。主要问题是同机制反复重述、滚动摘要过时和查找链过长，不能用删同字节副本解决。

## Python实测规模

本地盘点时全仓 **9379文件、348502450字节、3689份Markdown、839份README**，这是本地工作树测量，不能冒称Git截止纯树。该本地customer-attraction个人区占6144文件、218899972字节，含2120份Markdown；Git基线个人区另按父方核验的6142/113/707记录。其余模型独立保存，不加入当前一般半覆盖的默认读取链。

| 顶层分区 | 文件数 | 字节数 |
|---|---:|---:|
| customer_attraction | 6 | 32482 |
| design | 3 | 128893 |
| docs | 9 | 39534 |
| evidence | 635 | 36490976 |
| examples | 122 | 6516018 |
| facility_spe | 20 | 98562 |
| history | 831 | 37910468 |
| learning | 48 | 16003584 |
| multi_facility_spe | 6 | 51889 |
| research | 7129 | 246474096 |
| tests | 562 | 4696954 |

当前相关共享分区：`research/current/customer_attraction/`74文件，`research/customer_attraction/`14文件，`research/reviews/customer_attraction/`17文件。其他current目录：unrelated_machines 135、weighted_congestion 82、shared 16、multi_facility 24、heterogeneous 10、local_and_exact 4、positive_kernels 2。目录数与文件数量不表示数学结论的成熟度。

整理前的入口负担（实测UTF-8字节）：根四入口合计22259；本题短地图5297；一般工作稿35319；成果总账49602；个人区总索引39098；逐文件数学地图34894；SYNTHESIS 16799；本题RESEARCH_STATE 20154。仅这些入口合计已超过默认恢复所需的目标、范围和当前义务。具体数量以机器清单的测量时刻为准。

## 唯一来源与三级读取

| 阅读级别 | 文件/类别 | 应保留的唯一职责 |
|---|---|---|
| 默认 | 根README、CLAIMS、RESEARCH_STATE、FAILED_ROUTES | 分别负责目标/入口、身份路由、真实当前断点、失败机制索引；不复述逐项成果 |
| 默认 | AGENTS、`model.md` | 当前授权合同、完整数学对象和量词 |
| 默认 | 本题短地图、短SYNTHESIS | 下一轮实际阅读顺序、已证全范围关系和精确未付款步骤 |
| 按需 | `general_half_proof.md` | 连续推导的工作正文；各引理回原唯一证明，不把汇编当新全审 |
| 按需 | 本题RESULTS_LEDGER | 按范围和审查身份查一项成果；保留条件与反例对象 |
| 按需 | current数学README | 逐文件用途与来源；不作为定理证明本身 |
| 按需 | `current/claims.md`、review_status、assets、graph | 分别核精确身份、五轴状态、资产合同和真实依赖；导航不另造真值 |
| 按需 | WORKSPACE_RESULTS、当前精简清单、个人README | 按数学义务恢复原文、审查和证据，个人阶段资产不自动升级 |
| 按需 | RUNBOOK、工具源码、tests、examples、evidence | 操作、实现及精确证据；有限验证不替代一般证明 |
| 历史/不默认 | history、旧快照、旧角色提示词、各个人区旧轮次 | 保留可恢复原件和纠错关系；不继承过期任务 |
| 其他模型/不默认 | 不相关机、加权拥塞、两阶段设施、正核等独立分区 | 保持模型、状态和证据隔离；从research总入口按用户明确任务进入 |

最小整理不要求搬动6144个个人文件或重命名稳定数学正文。应优先修短入口、给过时索引加明确截止、增加精简当期路由、修真实漏项和断链，并运行原仓库的链接/目录合同检查。不得为了导航迁移改冻结证据原字节。

## 现有入口的具体重复与风险

- 根README、本题短地图、SYNTHESIS、RESEARCH_STATE以及一般稿均重复模型、OPEN声明、特殊研究停止规则和多个地基列表；一般稿负责真正连续推导，其余以短指针恢复即可。
- current数学README、成果总账和个人区总索引都声称“全部”或“完整”；它们实际分别是现行正文地图、旧基线分类和旧个人区快照。需把覆盖边界和截止放在第一段。
- current数学README第3行“工作稿的已证关系已经独立内部检查”会诱发整个汇编统一全审的误读。应改为每项关系按对应真实审查范围；总账第111行本来已经作此准确区分。
- 最新 Mfull 逐位置加强已由既有零根保险族反驳，Mpath聚合仍OPEN；实际分数税反例本身不能替代这个菜单反证。弱iid桥已失败，真正安全值聚合仍OPEN。必须保留这些对象区分，不能用“安全值路线已失败”大词压平。
- R-febfdd个人区记录其本会话用户只攻m=5，是局部会话历史/授权记录。全局当前默认只攻一般命题不能反向把它描述为证明错误或已经收到全仓转向命令；下一轮不从个人历史继承指令。

## 个人区全覆盖筛查与重点抽查

本地114个actor（含本轮新建1区）的根README路径和SHA-256已记录于 `cleanup_inventory_manifest.json`。两名子审计员按actor字典序各57个，覆盖全部708个递归README的索引、链接和状态关键词筛查；114份根README均进入人工状态阅读或抽读；其中后半57份根README全文阅读，前半以成果/状态为重点抽读并逐项浏览子README状态句。嵌套README按相关状态与新增来源重点抽查。该覆盖不意味着阅读全部2120份Markdown正文，更不意味着审完全部证明。

子报告分别为 `workspace_readme_audit_a.md` 与 `workspace_readme_audit_b.md`；其具体发现需要按源定义引用，不能只凭文件名提升Claim。

### 应优先修正读取状态的准确路径

1. `research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/independent_audit/README.md` 第22—46行把静态最优匹配“存在最优m元组与排列使Σ_i u_i(Tπ(i),z_-i)≤W”列OPEN。`R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md` 第14—46行已报告同定义反例：三人、六主题、1953单位客户完整SPE，W1735、OPT1740，所有最优排列最小1736。它不否定动态SM-opt-exists；原文及独立审计须保留。
2. `R-2fc8878b4bdd4328bbc1bcf1df8ca831/background_induction/README.md` 第8—9、32行的GLOBAL=`P+Δ≥freshOPT_r(b)`仍OPEN；`R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md` 第7—20行已给同定义真实四人SPE前缀反例：P17、Δ0、freshOPT2=18。
3. `R-7e9f44beea424d469713364afe7dd180/README.md` 第17行及 `aggregate_security/strong_iid_failure.md` 第3、87行保留“弱iid未反驳”的旧断言；其Z确为同一静态调和势最大者的iid覆盖，而共享 `iid_security_and_flow_barriers.md` 第116—122行已记录同定义弱桥的全人数反族。不能把其失败移植到真正v_m。
4. `R-18e993ca519949aba29e030d3d7b15b3/README.md` 顶部已纠正2W≥(m+1)u_m失败、且声明后文历史保留；后文旧OPEN只是历史句的阅读负担，应由显眼“后文历史”提示与现行失败索引解决，不应把它报告成尚未解决的当前数学矛盾。

以上actor相对路径均在 `research/workspaces/customer-attraction/` 下；实际税/菜单旧OPEN及重要新增恢复资产见以下补充表和两份已完成子报告。


### 补充状态与新增来源路由

- `R-d7f409d6a5914bdeb09875ab32618466/README.md:21` 仍把精确实际负载税 `mM≤W+G_C` 列未证；反证在 `R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md`。`R-fa8dd4ddea574a74a634ebc71e6f9ccb/README.md:22` 的terminal_credit旧“未被反驳”表述须按精确α/公式核到同源，不能只凭路线名字强合。
- `R-c4732bee2f7b4e50a70568170e3334ae/README.md:61` 的round4弱iid旧OPEN由现行iid共享正文覆盖。`R-d22a706a03c5499d941a6a97f94128a8/README.md` 与其induction子入口的逐位置Mfull/弱逐人付款，须先看一般稿§8的零根完整反族；Mpath聚合仍OPEN。
- `R-d1dc7a18aded4304a25a87486681fb21/security_continue/README.md:3` 将LAST与真正安全值、half并列OPEN，需要逐桥纠正，不能把LAST比较代数和其付款条件混成一条已失败命题。

四份旧恢复文件未按精确路径覆盖的个人一般组件，适合做按需delta源表，不宜全部塞进默认上下文：

| 机制 | 唯一源路由（均在customer-attraction个人区） | 限制 |
|---|---|---|
| 同策略删除regret及全删位后缀预算 | `R-105f776c3e6d4a22bb7c380c5df8edc7/parent/deletion_regret_envelope.md`、`average_suffix_deletion.md` | 不使删除后的策略成为SPE，不能免费归纳 |
| 前j位可信退出与异质保险 | `R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md`；`R-3bc48d936f044f12b0fa743482ff5eb0/credible/heterogeneous_prefix_repair.md` | 修复成本工具，稳健half门槛未越过 |
| 统一signed价格等价与双侧修复 | `R-ab4b3c24c8f949198e194dd45bb66105/construction/uniform_signed_defect_prices.md`、`mixed/signed_credible_repair.md` | 尚未构造统一价格或负seed；实际独审需连同版本读取 |
| 全深度共同末位租金编译 | `R-d1dc7a18aded4304a25a87486681fb21/credible_continue/shared_terminal_rent_compiler.md` | 不是根常数三修复的相同合同，仍有稀释成本 |
| 同query全部history库存 | `R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/jointflow/same_query_history_aggregation.md` | 跨不同query的整行共同付款仍未闭合 |
| 共同后继IC和一次舍入 | `R-d3981c0168644971803a9c3380ed687c/round7_general/signed/pooled_successor_transfer.md` | 无严格负seed，无新福利界 |
| 产品IC转移与末层cap2 | `R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md`；`R-5a15745a45ba44adb7d26c0557faacb7/parent/terminal_amount_cap.md` | 产品工具有旧来源；cap2仅末层/代数，深层与初始化仍开 |

完整15条源路径已加入机器清单；子审计A/B保留实际审查指针和各项精确边界。这些是需要恢复的个人资产，不等于本轮已审或新canonical。

### 三个准确断链与两个占位恢复入口

1. `research/workspaces/customer-attraction/R-b08ddd5d8c8e4554ad54b4ee147e128a/README.md` → `dynamic_induction/nonconvex_screen.md`。
2. `research/workspaces/customer-attraction/R-e5d83af532dc495c966f99cf70cda2a2/README.md` → `uncovered_profit/README.md`。
3. 同一R-e5d83根README → `direct_global/README.md`。

不存在目标不得补造内容，应改为实际已保存文档或标为未物化历史方向。`R-f399f831353446a49502f49d8abd2cb7` 和 `R-b28b3013e6464e70862b4993359a6964` 各有18文件，根README仍占位，不能推断无研究资产；应补最短子入口。R-f399的 `recursive_state/README.md:29` 有覆盖拆分的疑似差集/交集笔误，需先核定义再引用，不能把筛查发现当已经完成数学纠错。

## 交付与边界

`cleanup_inventory_manifest.json` 是约103KB的当期轻量清单：113个Git基线actor的统计、根README路径/hash、旧快照同口径差集；本轮父方新建 `R-d5b468f0c01140e79be5afef669bc0e5` 的README与workspace.json两文件另列，不算基线。全仓分区明确为本地盘点时工作树，未冒称本审计执行Git验证；没有再复制6144文件巨表。旧snapshot及原证据留在原处。

本审计未研究新数学、未提升任何命题、未通读全部证明。完成后父任务可据此实际改共享短入口与路由；个人来源纠错与正式Claim升级应分别依据精确定义和真实审查，不由清单自动完成。
