# 固定工作量及单边界森林：五原程序完整资源与复跑

AX实际认领pushed/Boss4/synced，tip6bff6a9880c80bc49f1623b352a74ec92ae308b2，[实际回执](claim-confirmation.json)。五primary经独立只读clean show完整实读/核SHA。另完整读12108B基线依赖、4旧森林JSON、7014B问题稿、26425B当前forest全稿（含不同身份双边界§9）。共有12冻结来源，不因同prefix混为一般UM算法。

## 自足对象与完整原件

1. [昂贵叶/medium原入口](../../../state/计算/私有昂贵叶与中任务标量原程序的精确范围--计算.md)：768赋值与平方势/三个scalar，不冒hinge/profile新跑。
2. [local floor/global ceil](../../../state/计算/单边界森林双向格点程序的真实负载与恢复--计算.md)：精确根与不同内部单位、全部恢复/有限范围，down末行parent键复用明示。
3. [crosscheck/族probe](../../../state/计算/单边界森林交叉核对与经典族原入口的真实调用--计算.md)：600同输入分歧、经典五阈值/四私有sink，import副作用准确归属。

双冻结提交68fad804ec5946cb296f77dc5b336308a66abf12与aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c，逐源read_scope在manifest。

| ID | 原路径 | 字节 | SHA256 | 保留件 |
|---|---|---:|---|---|
| bf086317be6e6dff2fda | tests/audits/unrelated_machines/fixed_work_and_medium_config_barriers.py | 2788 | `2ddd0c139102fc25cc7dcc03286dad50a8d29b17aa3c5b36cfb81daa1a6f2f1b` | [原件](original/tests/audits/unrelated_machines/fixed_work_and_medium_config_barriers.py) |
| 3caab4578b69327c5002 | tests/audits/unrelated_machines/forest_boundary_crosscheck.py | 2276 | `e81faeea5df317f2cfa937eca2dee9f4ef85c3db0cc77d7f825cb75e3bef0fee` | [原件](original/tests/audits/unrelated_machines/forest_boundary_crosscheck.py) |
| f2c6ca48b28fc0fcced1 | tests/audits/unrelated_machines/forest_boundary_downward.py | 6949 | `e3854ca048d40fe3b8a4eb8e3bd1e74b1f1ae5b212b154d185055fa27bf761c3` | [原件](original/tests/audits/unrelated_machines/forest_boundary_downward.py) |
| 849585c11e7483136ea6 | tests/audits/unrelated_machines/forest_boundary_family_probe.py | 2749 | `5ce30fcd6ca2d353120918731765a3e60a162577732874c1fce09a20dfa32a2d` | [原件](original/tests/audits/unrelated_machines/forest_boundary_family_probe.py) |
| bfb29f714c32ca4dd39a | tests/audits/unrelated_machines/forest_boundary_upward.py | 11820 | `95d52e10267c1c6b98e86276f5b30f3c3d63c5e947c2b0fb527de95d6fbe355c` | [原件](original/tests/audits/unrelated_machines/forest_boundary_upward.py) |
| e57947bc795251d373c3 | tests/audits/unrelated_machines/rounding_and_gap.py | 12108 | `5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a` | [原件](original/tests/audits/unrelated_machines/rounding_and_gap.py) |
| 5a826cef080e76b29d1a | evidence/runs/unrelated_machines/forest_boundary_crosscheck.json | 286 | `da9d35310682a80d41fea3a5dd74624b5a1284fd078873d7c19bc58c963169ea` | [原件](comparison/evidence/runs/unrelated_machines/forest_boundary_crosscheck.json) |
| 66ff673f61267dca5448 | evidence/runs/unrelated_machines/forest_boundary_downward_audit.json | 374 | `87ef33c148c5e42a724fed7c70bd5dccb3541b765ca8194d9e81ae051feac99c` | [原件](comparison/evidence/runs/unrelated_machines/forest_boundary_downward_audit.json) |
| 78f9754b93436c7544b7 | evidence/runs/unrelated_machines/forest_boundary_family_probe.json | 2073 | `655c09741e6bc1508054bd04282ee54c54416fb6812b5599f0f333ca9a33d8c4` | [原件](comparison/evidence/runs/unrelated_machines/forest_boundary_family_probe.json) |
| 98028825dc439a28358f | evidence/runs/unrelated_machines/forest_boundary_upward_audit.json | 1288 | `0a51b94fc2f7373907e2cad2e8b89cae491e7827fd74eb671354c4c70f84018e` | [原件](comparison/evidence/runs/unrelated_machines/forest_boundary_upward_audit.json) |
| a707d95d1e785d7fcec4 | research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md | 7014 | `7fa72fac9c785a2141923c0b7f11262a3021cff3b78dc4c77f5b8e5c73eaf08e` | [原件](comparison/research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md) |
| 00ef3bac6ce1ef8238b9 | research/current/unrelated_machines/forest_boundary_contraction.md | 26425 | `ea6fe38af8e2c9e849e8528131e97f4f81c9ce331c0545750e656496353cbc6a` | [原件](comparison/research/current/unrelated_machines/forest_boundary_contraction.md) |

[5 primary](source-manifest.json)、[1运行依赖](dependency-manifest.json)、[6比较源](comparison-manifest.json)。[旧维护snapshot](prior-comparison-snapshots.json)另保已读旧helper/summary/stdout，非冻结新增primary：[helper](prior-maintained/replay_fixed_work.py)、[summary](prior-maintained/fixed-work-run.json)、[旧原stdout](prior-maintained/fixed-work.stdout.txt)。旧768行state文件未新全读、不copy当本轮输出，旧R_B/R_all、706和hinge均未重跑。

## 真正的本轮执行和导入计数

五原CLI各一次全部exit0，**五数学进程、补充进程0**。crosscheck的runpy又执行未guard的downward整组审计一次：故down主体实际两次同seed同输入，不称5000独立新随机例，也不说第六个CLI。upward/rounding基线main guard使import不运行其audit；family仅baseline gap_instance三次（生成且验证CONFIG）。

| 原入口 | stdout | stderr | 实际记录 |
|---|---|---|---|
| fixed-work | [stdout](runs/fixed-work.stdout) | [stderr](runs/fixed-work.stderr) | [记录](runs/fixed-work.execution.json) |
| crosscheck | [stdout](runs/forest-crosscheck.stdout) | [stderr](runs/forest-crosscheck.stderr) | [记录](runs/forest-crosscheck.execution.json) |
| downward | [stdout](runs/forest-downward.stdout) | [stderr](runs/forest-downward.stderr) | [记录](runs/forest-downward.execution.json) |
| family | [stdout](runs/forest-family.stdout) | [stderr](runs/forest-family.stderr) | [记录](runs/forest-family.execution.json) |
| upward | [stdout](runs/forest-upward.stdout) | [stderr](runs/forest-upward.stderr) | [记录](runs/forest-upward.execution.json) |

完整命令/cwd/时长/原SHA见[执行manifest](runs/execution-manifest.json)，并发进程时长不充墙钟总时长。[精确执行scope](mathematical-execution-scope.json)和[16运行附件哈希](artifact-manifest.json)。原脚本无逐随机input dump；代码+seed/参数确定输入，本包不伪造500/600/2500矩阵或新768-state JSON。

## 新旧版本与数学边界

[五项历史比较](historical-comparison-and-version-scope.json)：四森林新stdout与旧JSON全结构同，fixed-work原stdout与旧维护原stdout全字节同。旧profile针对R_B/R_all/hinge的增量不当本轮原CLI；当前原问题稿错账和已有修正、medium标量与完整k4 matrix检查各自分开。

根不受容量限制，成功不等原T精确可行，down的34 extra返回不违反资源放大合同；cross的27状态/20根值分歧不证明两模型等价。down全300链≤11/10早先assert真实执行，末字段101/100仅按nested复用后parent键计算，源和历史JSON均保原样。稀疏m2^1000是两active标签API测试，非巨型显式矩阵。

5已读正式页snapshot及关系前提在[关系审查](relation-review.json)。26425B whole当前稿含双边界§9已读，不冒32295B raw e279 review本轮全读；未跑双边界程序。旧先验不当新blind，本轮blind/外审0，无一般挂件发现、外部隔离验证、核心选择或UM次二突破。

## 回执与精确复制

[5逐源receipt](../../../../../cleanup/workspaces/Boss4/r3-um-following-actual-source-primary/semantic-receipts.json)、[exact copy list](../../../../../cleanup/workspaces/Boss4/r3-um-following-actual-source-primary/copy-files.json)、[5实际下一候选](../../../../../cleanup/workspaces/Boss4/r3-um-following-actual-source-primary/next-candidates.json)。正文独立新写，不覆盖旧共享页，不写第三阶段超图。

[自查代码](verify_delivery.py)只核保存的字节/JSON/计数/链接与清单，不执行数学原码或import；stage精确比整个stage文件树，repo只核安全列出文件存在。实际[自查报告](delivery-self-check.json)不替代数学正确性。
