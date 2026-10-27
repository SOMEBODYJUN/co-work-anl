# Boss32 六人研究接续简报（2026-10-27）

## 固定目标

研究 `Q-CAG-HALF-6`：任意有限客户集、有限非空共同目录、六名单位提供者按固定顺序观察全部有序历史选主题（允许空主题、重复、零客户、任意历史依赖平局）。对每份完整纯 SPE 终局，证明 `2W >= OPT_6`；若命题为假，必须给原模型中覆盖全部有序历史的完整纯 SPE 策略和可复现精确核验。当前状态 **OPEN**。

## 已确认的可复用地基

- `research/current/customer_attraction/model.md`：原模型、完整历史 SPE 量词和精确定义。
- `research/current/customer_attraction/five_player_half.md`：恰五人完整精确 half 证书；不含六人或任意背景五人利润版。
- `research/current/customer_attraction/priced_hidden_reply_projection.md`：真实源 IC、同一实际末位全目录报价、共同 K、分支真末位 IC 的任意尾长局部投影；同菜单末回复互查已加；尚无全局共同预算。
- `research/current/customer_attraction/same_source_reply_requery.md`：同源再查询七行投影，已切掉旧单回复坏点；尚未闭合。
- `research/workspaces/customer-attraction/R-2118664d5481486fb34eb4b7f788af5a/subagent-f/m6_two_early_A_half.md`（commit `5d05d3a09e4a396b30c75f4a761df3f95f33678e`）：若实际倒二主题 A 被前四中固定两名主题逐集合包含，则六人 half 成立；这是条件特例。
- `research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/threefold_penultimate_half.md`（commit `bf6118c5`）：若 A 中每客户被前四至少三名覆盖，则 half；与两固定包含条件不可比。
- `research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/`：同覆盖标签的历史商编译工具，保持根覆盖序列、收益、W、OPT 和完整 SPE；不证明 half。
- 至多六个 inclusion-maximal 主题的联合预算定理只适用于整个目录的极大数受限情形；不能删原目录或补极大后声称保留原 SPE。
- 四主题六人全部 `32767` 个二值类型实例、以及近期若干 `k=3/4` 精确有限搜索无 half 违例，均只是有限证据。

## 明确不能重复的路线

已有精确反例或障碍的桥：逐位置完整菜单 `M_i <= u_i`、逐人安全值/固定槽、强弱 iid 福利桥、固定实际缩放税、冻结前缀 `P+lambda Delta` 归纳、逐席 `seat(t,j,k)` 行、SPE 当静态 NE、跨互斥枝直接合并信用、旧五人索引松弛调常数、uniform-K 组合、只调静态势或末价。七极大逐席 LP 的完整 SPE 反例（B0 六私有客户、其余各一，常值选 B0，W=6、OPT6=11）只是否定非法行，不是目标反例。

## 仍真正开放的义务

1. 在 A 被前四包含 0/1 次的路由上，构造合法的早期—倒二—末位跨分支共同付款，或证明某种 order-statistic/aggregate 关系能闭合七极大 44 轨道；必须保留真实后继、旧玩家利润变化、共同 K 与目录外动作。
2. 完全换方法证明六人 half；或构造原模型全历史目标反例。任何松弛 LP 点、局部菜单、静态 NE/CCE、有限无反例都不算成功。

## 交付标准

每个新结果必须标明 exact statement、全部量词和定义、证据级别（解析证明/完整精确核验/条件结论/障碍/候选）、唯一正文路径、脚本/输入/输出和 commit。失败也要说明精确排除了什么、留下什么。不要重复已有阴性扫描；优先寻找能支付真实跨分支净差的关系或完整原模型反例。
