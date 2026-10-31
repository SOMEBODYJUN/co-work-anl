# R-2fc global_proof 八源证据包（2026-10-31）

本包承接 `research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/` 下八个已认领库存源。用户消息将 `background_regret_probe.py` 写成 `3086d1200c57312720a`；冻结 inventory 的实际 ID 是 `3086d1200c57312720e2`，本包只使用后者，不创建伪 ID。

## 来源和读取状态

| ID | 文件 | 冻结大小 / SHA-256 | 本地 clean show | 原字节 | 处置边界 |
|---|---|---:|---|---|---|
| `484d7024f388657d79d9` | `audit_collision_free_family.py` | 3034 / `9a5ec3d9a979d075235a505d0ae63362a1dfb79333a1280d7d8e535e48b0d7c1` | 失败：`bad object` | 未物化 | 相关 family 独立实现已复跑；缺原脚本全文 |
| `2c9581cd1e1a35237ff2` | `audit_collision_free_obstruction.py` | 2155 / `00678532fbff9f0179dee108c7ad792dcfdb59e7ac55af8610a1149a17de5a2c` | 失败：`bad object` | 未物化 | 冻结 JSON 可读且独立 Fraction 实现通过；缺原审计脚本 |
| `da6d610ba50965200a82` | `audit_truncated_potential.py` | 2472 / `c0b76546ad9cb545d22413fe460b9cbdbd8488354884fe067eac33d74406ca95` | 失败：`bad object` | 未物化 | 关联十一客户精确势障碍全文已读；缺原审计脚本/78客户输出 |
| `3086d1200c57312720e2` | `background_regret_probe.py` | 3186 / `0d2e76e18c540183ac37f52559f5a57f427517822d01a25ad81533c4e49c2cb9` | 成功，返回码 0 | 已保存 | 完整源、编译、q6/r3 100棵与20棵运行 |
| `1121e1bd7ded184bd117` | `collision_free_family_audit.json` | 1344 / `d4b13f887e50a909c943d769b08d550a2d4c9be62a92f707bba064f8f24b5a17` | 失败：`bad object` | 未物化 | 关联独立 family JSON（不同 SHA）已复跑，不能冒充原 JSON |
| `531860b3798ce2ad5665` | `collision_free_obstruction_audit.json` | 954 / `dd946143d6d4aee7f381b69b6ab59be775ea2a35029aee42fb841ef9661287e9` | 成功，返回码 0 | 已保存 | 全文 JSON 读取、独立 Fraction 复核、输出逐字节一致 |
| `e5a0724f34d98235f952` | `collision_free_ratio_best.json` | 3448 / `952a153b846b2664bbe923d9b9ea6a9dfc22187dfaa71b4f49fe95bd9be933bd` | 失败：`bad object` | 未物化 | README 中约 1.116279 的有限探针摘要仅作 related |
| `181f33c049afe9962dba` | `collision_free_ratio_probe.py` | 3116 / `aec4685b0609e5826f91f678f28f893f8b537ebc00d26b006e257ca181ab8b0f` | 失败：`bad object` | 未物化 | 缺探针源码；不声称重跑500棵 |

每个 `clean show` 的完整命令、退出码和原始 stderr/stdout 均在 `clean-show/<id>.log`。成功的两个输出也保存在 `clean-show/` 和 `source/`。`metadata/source-summary.json` 保存 inventory 行、两个冻结提交、Git blob、大小、SHA 和读取状态。失败原因是当前 partial clone 没有这些 blob，且浏览器代理不可达；没有把网络失败改写成数学判断。

## 已运行复核

- `background_regret_probe.py`：Python 3 `py_compile` 通过；独立副本执行 `--q 6 --r 3 --trials 100 --seed 29393` 和 20 棵 smoke run，均退出码 0、stderr 为空、`best=0.0`、没有生成候选 JSON。结果保存在 `replay/background_regret/`。这只支持固定随机种子和浮点 LP 的有限 no-hit 事实。
- 关联 `audit_collision_free_family_independent.py`：Python 标准库 Fraction 程序覆盖 k=1,2,3 的全部有序历史，退出码 0；生成 JSON 与关联冻结报告逐字节一致（1183 B）。该程序 SHA `d8656e…`、报告 SHA `8e63bb…` 与缺失的 3034/1344 B 原件不同，故仅作独立复核。
- 关联 `audit_collision_free_occupancy_independent.py`：退出码 0；生成的 954 B JSON 与库存中 `531860...` 的冻结 JSON 逐字节一致。另用 `replay/obstruction/independent_verify.py` 按不同 `Fraction` 实现复算 5 个决策历史、20 项比较、W=4、OPT=5、负载 `(1,1,0,1,1)`、Phi=4，结果 `status=pass`。

## 关联数学材料

`related/` 保存已全文读取的 global_proof README、碰撞自由 k 族、五客户障碍、推广失败记录、十一客户调和势障碍、既有 family/occupancy 独立实现及背景程序副本。它们共同支持以下精确范围：

1. 五客户两人完整纯 SPE 的实际终局是两个不交主题，W=4、OPT=5；实际负载全为0/1，所以任何 `f(0)=0,f(1)=1` 的可加纯负载支配桥都失败。2W=8>5，故不是一般 half 反例。
2. 对任意 k 的碰撞自由族存在完整纯 SPE，W=2k+2、OPT=3k+2，比率趋 3/2；它迫使任何普适纯负载支配桥满足 f(1)≥3/2，但不提供充分性，也不反驳一般 half。
3. 十一客户三人路径的实际普通/截断调和势均为 21/2，OPT=11，仍有 2W=16>11；它只否定调和势加强桥。
4. `background_regret_probe.py` 的 100 棵固定 Markov-LP no-hit 是有限浮点筛查，不是合法全目录/全 SPE 的证明。ratio/truncated 缺失原程序与输出，README 数值不升级为本批复跑结论。
5. 将 t=2 碰撞自由族直接推广到 t>2 的目标终局被末位单偏离击穿；这只排除该推广。

一般六人 Q-CAG-HALF 仍 OPEN；本包没有外部同行审查、新颖性认证、全目录穷举或所有 SPE 量词结果。

## 恢复动作

待六个缺失 blob 可访问后，先逐源再次运行 clean show 并按库存 SHA/大小核对；随后运行原 family、truncated 和 ratio 脚本，保存 stdin/stdout/stderr、依赖版本和 JSON 对比，再更新对应 receipt 的 `full_file_reviewed` 与 disposition。当前本包可供数学接续阅读，但六源 raw 缺口使整批暂不称 source-level checkpoint-ready。

同时保留 `related/collision_free_family_scope_resource.md`、`related/promoted_punishment_terminal_obstruction.md` 和 `related/actual_prefix_global_budget_counterexample.md`，分别用于全仓资源范围、直接 t>2 推广失败和后续 52 客户 GLOBAL 反例的交叉核对。它们不是本批八源的替代原件，但用于防止把局部首步、实际占用、GLOBAL 和根 half 量词混写。

`metadata/replay-manifest.json` records commands, exit codes, output paths, byte-equality checks and Python/NumPy/SciPy versions for every replay.
