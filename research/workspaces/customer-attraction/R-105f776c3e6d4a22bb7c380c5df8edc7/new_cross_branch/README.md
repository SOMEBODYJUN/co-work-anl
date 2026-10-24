# 跨枝共同付款：零在轨误差不控制可信福利修复

2026-10-24。子任务个人备份，仅在本目录写入，无共享文件修改、git操作。
唯一研究目标仍为一般 Q-CAG-HALF；**OPEN**，本轮没有一般半覆盖证明或目标反例。

新增精确结果见 [自足证明](zero_regret_welfare_repair_obstruction.md)：
合法背景一位选 A、两名尾部玩家的十八单位客户共同目录，原完整尾部 SPE 投影福利17；
删除 A 后保留旧完整策略，两个旧实际节点 regret 均为零，但**每个**删后完整 SPE
福利恰16。整数复制使所需福利修复损失任意大，实际 regret 向量仍为零。
这严格排除只依赖旧实际节点误差、在零向量处有限的一般绝对福利修复费。
作者定义级验证和父方独立原始输入回放均确认；外审与新颖性未认证。

**准确范围：** A 是合法离轨前缀，原空背景三人实际根唯一为 B，非 A。
所以这是一般背景 DR-only 修复桥的反例，不是实际根单删版本的反例，也不反驳
ASD/VR 本身或可利用新枝、原 W、被删者收益的修复。已有五客户零 regret 例
只说明旧策略可能不再 SPE；本例额外证明允许重选全部策略仍不能无损。

| 文件 | 用途 |
| --- | --- |
| [zero_regret_welfare_repair_obstruction.md](zero_regret_welfare_repair_obstruction.md) | 精确一般桥、十八客户证明、完整末回复表、复制族与范围限制 |
| [zero_regret_repair_witness.json](zero_regret_repair_witness.json) | 明确单位客户类型、旧背景、原/新完整尾部策略 |
| [audit_zero_regret_repair.py](audit_zero_regret_repair.py) | 无仓库求解器的逐单位客户完整策略枚举；输出拒绝覆盖 |
| [zero_regret_repair_complete_audit.json](zero_regret_repair_complete_audit.json) | 两游戏各1024完整策略及原三人根分类的冻结结果 |
| [zero_regret_repair_audit.json](zero_regret_repair_audit.json) | 原始较窄审计，不覆盖冻结字节 |
| [search_zero_repair.py](search_zero_repair.py)、[初始候选](zero_repair_candidate.json) | 检验该明确一般修复候选的发现过程，非主目标反例搜索 |
| [simplify_zero_repair.py](simplify_zero_repair.py)、[简化记录](zero_repair_simplified.json) | 将已找到桥反例缩为十八单位客户；证明不依赖优化器 |

复现只需从仓库根执行：

    python3 research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/audit_zero_regret_repair.py --output replay.json

有一次附加候选特异的实际根筛选已完成，50000个随机四主题整数输入中没有发现
实际根版本见证；这既不证明该版本成立，也不对一般 half 作推断，已停止此类扫描。
目前未找到可付一般净缺口 `OPT-W` 的共同钱包。后续需要的新信息是修复后的真实
离轨菜单信用，而不是继续累加旧实际叶的零误差；不继续特殊人数项目或重复阴性扫描。
