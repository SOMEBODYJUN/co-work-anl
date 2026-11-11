# 全可见真最大裸标签 C 联合层：准备完成

Boss1；RUN `six-boss1-20261111`。状态 **PREPARED_NO_OPTIMIZER**。标准库 Fraction 构建与独立字面预检全部通过；本阶段 **0 次优化器调用**。Main 已在输入冻结前收到实际范围、尺寸、SHA 和检查结果。数值求解等待 Main 单独明确释放。

## 精确范围与输入

原模型仍是有限单位客户、有限非空共同标签目录、恰六人完整有序历史纯 SPE，保留标签别名、空覆盖、重复行动、全部离轨弱平局。actual 动作为 A1,…,A6；X 是同一 actual 前四负载 P 下全目录 fP 最大合法标签；C 是达到全目录最大裸大小 K 的合法标签。没有令 C=X 或 C=Ai，也没有赋予 C 额外前缀潜力最大性。O 是 OPT6 六合法可重复查询的覆盖并，绝不作为合法行动。

保留全部512个 `(a1,a2,a3,a4,a5,a6,x,o,c)` 客户型。旧型 v 的 c=0、c=1 两列为 2v、2v+1，旧 K256 移到 K512，共513个非负列。目标是原 actual 覆盖 W，全部旧867 raw行、目标、归一化和 rhs 忠实拉回；所有零行及重复行继续保留。

最终准确维度为 **1002 raw 不等式 / 513非负列 / 2等式**。两条等式是

\[
\sum_v o_vz_v=1,\qquad \sum_v c_vz_v-K=0.
\]

| 零基 raw 位置 | 来源 | 行数 |
|---|---|---:|
| 0–866 | 冻结 v6 全867行忠实拉回 | 867 |
| 867 | ROOT30_B2_B4_CAPACITY_FEEDBACK | 1 |
| 868 | ROOT270_TRUE_BRANCH_P25 | 1 |
| 869–874 | SAFE_i(C)，i=1,…,6 | 6 |
| 875–876 | FMAX(C)、MX(C) | 2 |
| 877–885 | C 与 A1,…,A6,X,Omean,C 的 RC | 9 |
| 886–894 | 同九描述的 PAIR | 9 |
| 895–979 | actual i=1,…,5，各17个至少一边 C 的有序 P25 | 85 |
| 980–1000 | C 加旧七纯角色中任选五个的六合法并上帽 | 21 |
| 1001 | Main 冻结前明确追加的 K−O/6≥0 | 1 |

原准备合同1001 raw在 Main 的明确增量后成为1002。最后一行的直接支付是六个真实合法查询大小帽平均，加逐客户并计数余项：

\[
K-O/6=\frac16\sum_{j=1}^6(K-|Q_j|)
+\sum_vz_v(d_v-o_v)/6\ge0.
\]

不把这条行解释成 C 的实测均值；它本身也适用于任意六合法查询并。两根均使用 u1 系数为1的原行，标准257列来源逐字段拉回。旧有效正除数原样继承；85条新增P25保25ui原尺度、数值除25；其余50条新增原行数值除1。精确输入未缩放。

## 独立预检结果

独立 worker 亲读原模型、正式 RC/PAIR、旧 source/build/check 字面及 P25 完整证明，未导入 builder。检查结果为 PASS：

| 检查 | 数量与结果 |
|---|---|
| 旧867原行全部元数据、顺序、字面系数拉回 | 444771个列系数，PASS |
| 两标准根 | 1026个列系数，PASS |
| 132条新增C查询 | 67716个列系数，PASS |
| 新菜单K下限 | 513个列系数，PASS |
| 旧已存唯一行尺度 | 798个全部匹配 |
| 全部raw有效尺度 | 1002个全部匹配 |
| 行目录、列路由 | 1002行、513列全部匹配 |
| P25真实付款与闭式包络 | 456隐藏态、60精确最小值 |
| 新C钱包单均值 | 640个六索引会员状态 |
| 新P25两个混合方向 | 3840个六索引会员状态 |
| 旧钱包双均值36对、旧P25双均值30异索引对 | 320与960个状态，语义分别保留 |
| 菜单大小预算的 d≥o | 全64个六索引会员向量 |

所有混合均值都从六个真实标签索引展开，再利用 d≥o 弱化，没有分割或独立性假设。特别是 P25 的 `T=C,Q=Omean` 与 `T=Omean,Q=C` 分别构建；自对使用 c²=c。未增加 ROOT_RIG(C,*)、UP(C)、QX(C)、P31(C,*) 等未授权行。

旧零行 SAFE_6_6 仍在 raw45；69条完全重复仿射行全部保留。932个不同非零仿射行只是诊断统计，未进行删行。20份直接来源文件在生成前后 SHA 相同。没有发现系数、列路由、尺度或查询来源合同缺陷。

## 交付与精确绑定

核心文件：

- [exact_input.json](visible_maximum_joint/exact_input.json)：完整1002×513精确系数与两等式。
- [source_review.md](visible_maximum_joint/source_review.md)：正式源逐条实读、真实付款、均值方向及Main增量。
- [row_catalog.json](visible_maximum_joint/row_catalog.json) 与 [row_catalog.tsv](visible_maximum_joint/row_catalog.tsv)：全部原始行索引、来源、角色和尺度。
- [column_routing.json](visible_maximum_joint/column_routing.json) 与 [column_routing.tsv](visible_maximum_joint/column_routing.tsv)：完整512型及K列路由。
- [numerical_scaling.json](visible_maximum_joint/numerical_scaling.json)：全部1002原行的正数值除数。
- [build_input.py](visible_maximum_joint/build_input.py)：标准库Fraction准备程序，无求解入口。
- [independent_precheck.py](visible_maximum_joint/independent_precheck.py) 和 [independent_precheck_result.json](visible_maximum_joint/independent_precheck_result.json)：不导入builder的独立重建代码与结果。
- [literal_query_checks.json](visible_maximum_joint/literal_query_checks.json)：完整隐藏态及新C六索引平均的精确字面记录。
- [freeze_manifest.json](visible_maximum_joint/freeze_manifest.json)：冻结范围及所有准备产物SHA；[SHA256SUMS](visible_maximum_joint/SHA256SUMS) 可逐文件复查。

| 精确文件 | SHA256 |
|---|---|
| exact_input.json | `b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33` |
| independent_precheck.py | `9156b85d05aed6abdf25b2308e79202784e5ebc7cd4914fa8fded21a429e7c84` |
| independent_precheck_result.json | `4a3dba012a2915525eb4af3b83f337a64957d6d3db03acbfea8662f851a74767` |

本包是完整可见必要投影的准备成果，没有运行 LP、没有补全已排除的 v6 点或最优面、没有产生可行点、最优值、SPE构造或新的half结论。原六人 half 仍为 OPEN。
