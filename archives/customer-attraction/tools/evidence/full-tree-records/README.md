# 完整树保存记录的精确单点核验

本目录支持[完整树保存运行与恢复版本边界](../../../state/计算/完整树保存运行与恢复版本边界--计算.md)及[后继超额保留的最小收益价格桥](../../../state/候选/后继超额保留的最小收益价格桥--候选.md)。历史发现、当前源码、清洗时新增的核验分别保存，不能把同目录当作同一执行版本。

## 固定来源和依赖

[PROVENANCE.json](PROVENANCE.json)列12份固定字节：

- original/的八个本批来源：2026-10-22说明、audit_console、六份保存运行JSON。其中五份含完整策略候选，一份四人加限制超时记录无候选。
- comparisons/的两份已全文比较说明：零降幅局部桥与正深度floor反例。本批不替这两源done，不执行它们引用而未纳入本目录的证书。
- 前批full-history-selection/original/credible2/中的固定full_tree_milp.py与full_tree_milp_audit.json。前者用于当前行数、恢复距离cut的版本比较，后者用于console逐字节重复核验；本批均不执行。

全部来自冻结提交68fad804ec5946cb296f77dc5b336308a66abf12，清单保存原路径、源ID、实际字节数、SHA-256与使用角色。它们不包含执行时源码绑定：原保存运行JSON没有runtime source hash，当前代码不能自动承接其历史执行身份。

## 本次实际运行

[verify_saved_points.py](verify_saved_points.py)是Boss3本轮新写的标准库实现，不导入原StrategyCone、客户收益模块或canonical solver。程序按每名单位客户直接计算全部有序历史下的真实后继收益，验证五份完整策略所有1120个非自身行动比较，并保留每个比较的实际终局、收益与精确松弛。

唯一实际运行命令为：

~~~sh
python3 -E -B archives/customer-attraction/tools/evidence/full-tree-records/verify_saved_points.py --output-dir archives/customer-attraction/tools/evidence/full-tree-records/verification
~~~

运行环境Python3.12.14，约0.02244965秒，退出码0。源码SHA-256为c6ae4e61c35119d6698c7f33bca996a8e296203ec91bb4dd9cb897f72af2338e。该程序先核全部12份固定字节；共266节点、1120比较、56严格正松弛和1064平局，五点全部通过。六份记录的元数据、候选存在性、实际根路径、计数、查询、目标缺口、W、OPT、不同物理主题及全部两两距离都按所存内容检查。

[verification/verification.json](verification/verification.json)保存总表和每点结果；同目录五份*-all-comparisons.json保存所有节点与偏离。canonical_solver_root_checked=true仍只是原JSON内历史标记，本次canonical调用0次。历史发现执行0次、原680/20/20有限回归重跑0次、LP和MILP调用0次。

复现请选择一个不存在的新目录，不加-O以保留断言：

~~~sh
python3 -E -B archives/customer-attraction/tools/evidence/full-tree-records/verify_saved_points.py --output-dir NEW_SAVED_POINT_CHECK
~~~

目录已存在时入口拒绝覆盖。程序只用标准库、读以上固定文件，输出新核验JSON，不联网、不下载依赖、不更改冻结原件。除wall_seconds外结果应按相同定义重现；若原件身份不符，hash断言先失败。

## 证据能说明什么

五份整数客户点的完整SPE与保存目标值得到新的直接精确核验；全部客户数、路径与策略保留。最优覆盖用不同标签的 \(\min(p,m)\) 元组合枚举，非负覆盖允许补齐，故与允许重复的m主题最大覆盖一致。它不枚举所有策略或所有客户权重。

这些特殊实例由互不交叠的客户块组成，完整价格可解析为 \(\sum_j(n_j-v)_+\)。核验程序据此记录实际全局最小收益位置的尾部超额候选余量；没有把p=6的普适顶点枚举或全锥价格证书当作已执行。

m3p6_hull_distinct的原恢复候选只有两种物理覆盖，最小归一距离0，违反原头部0.001限制。README已经记载当时恢复LP漏距离cut；当前代码有该cut，但仍须区分有理重构之后精确距离终检的另一缺口。普通四份记录行数比当前代码公式少p，与当前p条冗余根保证相容；仅计数不能识别历史代码版本。

audit_console与前批原审计JSON逐字节相同，均为6508字节、SHA-256为8d5a3d03261d1684243fa2478e968cb94338f55f042610040a938370b77f216a。本次复制保全其来源身份，不增加独立实验次数。

原候选没有任何精确正gap；浮点成功或时限状态也不是严格上界证明。本批没有重跑阴性发现、默认模型、随机种子、无候选记录或六人搜索。完整数学对象、版本判断及后续义务在链接正文中，不以本目录文件齐全代替数学判断。
