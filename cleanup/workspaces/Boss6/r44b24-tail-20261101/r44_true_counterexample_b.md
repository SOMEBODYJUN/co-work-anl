# R-44b24 true_counterexample 后三个源实读审查

审查者：/root/r44_true_counterexample_b
工作分支：rebuild/research-v2（仅读取；未改共享 clone、未执行远端 done）

## 冻结字节与实读证明

以下三个源均用当前结果分支的 `work.py clean show <id> --out` 导出并逐字段读取；导出 SHA 与冻结清单一致：

| source id | 路径 | 字节数 | SHA-256 | 读取结论 |
|---|---|---:|---|---|
| `ed08c69fb0ea8cc41db3` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/cold_m5p7.json` | 1219 | `cf52e511476e5e5f04d5232e678b2f226e10fa6dca315c562e78d9ec9ef2c5a5` | 一次受控 cold 热启动性能/状态对照 |
| `53354e0821f1a01abbd2` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/finite_search_summary.json` | 31253 | `dde588ce54a96fe631d57626d61736902fc31b8ddb8876e23ec0e3e9b51bc550` | 15 条有限运行摘要，逐条读完 |
| `30100bcc784963d0734e` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/manifest.json` | 1727 | `a47831ea2eb5e04c36f4c601a55b145ea4608a1e128064f348a8c1974c114cd9` | 原文件 SHA/路径/primary-related 闭包清单 |

同工作区的 README、warm_dag_search.py、audit_saved_policies.py、audit_warm_start.py、saved_policy_audit.json 及其已推送 canonical 证据已在全仓搜索中核对；本三源没有隐藏的独立定理或新的一般反例。

## `cold_m5p7.json`（ed08…）

字段显示：scope 是 `warm-start unrestricted full-history outcome DAG; floating search plus exact full-policy verification`，`universal_bound_proved=false`；seed=20261021，seed 根终局 7、seed exact optimum=9、seed welfare="5"，state counts 792/462/822；构造耗时 0.30534962600006565 秒。

这是 cold 对照：`warm_start_supplied=false`，最大约束残差 2.220446049250313e-16，seed 浮点目标 1.8；HiGHS 状态 `kTimeLimit`，25.019689760000006 秒，mip_nodes=0，mip_gap=null，`dual_bound_float_not_certificate=1.8`；MILP 为 7 topics/5 players、root_counts=[5,0,0,0,0,0,0]、42345 variables/41888 binary/77065 rows，status=1/time limit，floating_value=null，`floating_bound_not_a_certificate=true`。`exact_candidate=null`。

语义：没有可行 incumbent/精确候选，不证明无 SPE、无解或一般下界；仅说明同输入不提供 warm start 时的一次限时运行未返回策略。不能把 1.8、time limit 或 null dual 当数学证书。

## `finite_search_summary.json`（5335…）

共有 15 条记录；scope 14 条为 unrestricted full-history DAG，1 条为可选 subset restriction，全部 `universal_bound_proved=false`。记录逐条核对：

* cold_m5p7：同上，time limit、无浮点 incumbent、无 exact candidate。
* restricted_m5p7_221 与 _311：五人七主题、restrict_outcomes=true、time limit；精确固定候选分别 7/5，dual_optimal=true。
* restricted_m5p7_population 与 round2：根 [2,2,1]，受限菜单；一条 kOptimal、一条 time limit；两条精确候选均 8/5，dual_optimal=true。
* warm_m2p2 / warm_m2p2_final：2 人 2 主题，精确 3/2。
* warm_m3p4：3 人 4 主题，精确 4/3。
* warm_m5p7：5 人 7 主题，精确 9/5；这是既有已知保存策略，不是全模型普遍界。
* warm_m5p7_11111：time limit；返回一个 exact candidate 但 `dual_optimal=false`、`exact_dual_bound=null`，不能当上界证书。
* warm_m5p7_311：精确 7/5，dual_optimal=true。
* warm_m5p7_41 与 round2：精确 23/14，dual_optimal=true。
* warm_m5p7_population_full：五人七主题、restrict_outcomes=false、time limit；精确 8/5 且 dual_optimal=true，但仍是单个固定返回策略/有限运行。

摘要各条还含运行时、seed statistics、floating bound 等元数据；这些不是完整策略动作表。尤其 time limit、floating bound not a certificate、restricted_outcomes 或 local branching 都只描述算法子域/一次搜索，不能排除域外的 SPE、不能推出六人 half 命题或反例。有限 exact_candidate 只认证该返回策略（通常还需固定策略锥的 exact dual），不认证所有策略。

此文件与现有 `archives/customer-attraction/subarchives/six-providers/state/计算/五人热启动保存策略的单位客户与认证范围--计算.md` 的说明一致：该正文已逐字段读过 15 条记录，并明确 cold/有限摘要不具排除性数学含义；canonical evidence 已保存在 `tools/evidence/warm-population-snapshots-primary/related/finite_search_summary.json`。

## `manifest.json`（3010…）

manifest 的 `files_sha256` 覆盖 README、审计脚本、cold/finite 摘要、population gadget 文件、warm seeds、warm_dag_search.py 等 15 个文件；它的 note 明确最终实现 hash 可与早期运行版本不同。该文件是 provenance/闭包元数据，不是数学结论；其记录与现有 `warm-population-snapshots-primary/source-manifest.json` 及 related evidence 对应。未发现额外 claim、参数或独立策略。

## 与现有 canonical 的关系与建议处置

三源的全部语义已由下列既有对象和证据承载，未发现应新建数学对象的内容：

* `archives/customer-attraction/subarchives/six-providers/state/计算/五人热启动保存策略的单位客户与认证范围--计算.md`：明确 cold 对照、15 条有限摘要、精确/浮点/固定策略锥层级及适用域。
* `archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-population-snapshots-primary/related/cold_m5p7.json`。
* `archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-population-snapshots-primary/related/finite_search_summary.json`。
* `archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-population-snapshots-primary/related/manifest.json`。
* `archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-population-snapshots-primary/README.md` 与 source-manifest.json。

建议三条回执均为 `integrated`，目标为上述“单位客户与认证范围--计算.md”；三源的原字节已在 `warm-population-snapshots-primary/related/` 保留，不应重复制造新 canonical。manifest 同时可标注为 provenance-only：它只支持证据闭包/版本身份，不新增数学命题。

## 处置边界

不能把本组的 15 次有限搜索、cold time limit、任何浮点 dual bound、restricted/local-branching 子域、或某次 fixed-policy exact candidate 解释为一般五人/六人 half 结论。正式正文中保留 `universal_bound_proved=false`、time-limit、non-certificate 字段和缺失环境/参数字段；不补造未保存的命令行或动作表。该批适合逐源 `done`（integrated）而非 needs-decision。
