# 三主源、十一相关源与一份原入口重放

本目录对应Boss1第二阶段的`independent_frontier`三份主源：README、`background_step_independent_audit.py`及其JSON。三源由`work.py clean show ID`全文读取并用`--out`导出；`primary-source-manifest.json`固定每一源的ID、双冻结定位、blob、大小及SHA-256，导出原件均与inventory逐字节一致，共26796B。

`related-source-manifest.json`另列十一份实际全文读取的相关源，共43542B，包括F/E剪枝原证明、独审最小域、parent_review、两份剪枝有限实现及报告、八客户诊断、有序弱诊断和初始计数probe。它们仅作比较依赖，不由本目录替代认领或完成。当前成熟正文的实读范围及hash另存`comparison-manifest.json`；五人定理仅作命题/状态核对，其余列入该manifest的数学正文为全文阅读。

正式数学对象是：

* [实际与唯一最优支持剪枝的全人数福利跃升](../../../state/障碍/实际与唯一最优支持剪枝的全人数福利跃升--障碍.md)：原完整族、唯一最优支持、剪枝后所有SPE的F/E同步归纳与根最小域、准确反驳量词。
* [独立前沿入口与大主题精确审计的范围](../../../state/资源/独立前沿入口与大主题精确审计的范围--资源.md)：原代码全部函数、20989B有限报告、历史审查先验、指定reserve台阶由OPEN改FALSE及其它路线的准确范围。

`replay/`是单独复制原2432B脚本的执行目录，不覆盖`primary/`里的原报告。一次普通Python执行退出0、stderr为空，生成20989B报告与冻结报告逐字节相同；`replay-report.json`记录本次真实argv、Python版本、时长、hash和输出大小，`replay/stdout.txt`只有摘要。该运行核r1…5的883个有序决策节点、4291项含自身行动比较（3408项非自身），100个整数公式和30个平方点；不是新独立实现、任意人数证明、外审或全球新颖性认证。

本三主源清洗未执行作者剪枝、随机probe、recursive_invariant及成熟499公式/69客户完整策略程序。同批general_payment清洗者的独审剪枝标准库程序另有一次重放，保存于其审查页，不属于本目录执行事件。一般证明来自正文解析归纳/精确代数，代码只对自己的有限输入承担实现证据。原JSON没有历史时长或程序hash，不能把本次元数据倒填成历史执行记录。

`relationship-review.json`给出第二阶段的人工作用/范围判断，不生成第三阶段超图。逐源处置位于`cleanup/workspaces/Boss1/resume-independent-frontier/receipts.json`；三主源与十一相关源范围严格分开。
