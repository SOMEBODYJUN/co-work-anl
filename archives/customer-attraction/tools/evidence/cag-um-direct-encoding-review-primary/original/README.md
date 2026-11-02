# Boss9：客户吸引半覆盖与不相关机近似的联系审查

研究存档：`customer-attraction`；发布身份：`R-c90acbef8c6a45f28bf33b5f639d6e99`。

## 当前研究与恢复

用户本轮要求检查 Q-CAG-HALF 和 UM-TARGET-v1 是否本质相同，并明确启动一个
GPT-6 Astra / ultra 子代理独立研究。根代理同步核对定义、文献、自然编码和目标保持。
本 clone 此前只作状态核对；本轮根 work.py start 生成并绑定上述独立 actor。
两个一般目标仍 OPEN，未建立它们的归约或等价，也未证明任意归约不可能。

## 已有材料与真实范围

| 文件 | 数学资产及接续用途 |
| --- | --- |
| [自然编码的精确 Claim 与证明](equivalence_audit/direct_encoding_claims.md) | 不交主题 CAG 与单位任务相关机顺序博弈在收益倒数下完整 SPE 同构；标准下界族的覆盖损失趋2而对应 makespan 恰最优，排除该同构保持效率比。另证分组配置的覆盖/调度可行性等价，并构造丢掉机器分组后全覆盖 SPE 仍对应阈值不可行的任意规模族。均仅限明示编码，不否定所有归约。 |
| [Astra 独立研究报告](equivalence_audit/astra_relationship_report.md) | 两题精确定义与目标、真实子类同构、自然配置/标记/均分/成本变换障碍、UM–Santa–MMDA 文献链、max-k-cover 骨架联系，以及仍缺的两向归约合同。根代理已重建核心自足证明并核到关键一手位置；不是无归约定理或难度分级。 |
| [Astra 对根代理五项 Claim 的独立审读](equivalence_audit/astra_independent_review.md) | 逐条核对量词、全部真实历史、OPT、配置容量和公共背景偏移；未发现致命异议。代码由根代理执行，子代理未冒称自行运行；内审、外审与新颖性分开。 |
| [定义级有限审计](equivalence_audit/verify_direct_encodings.py) | 仅标准库 Fraction；从单位客户和原处理时间重建全部有序历史比较、覆盖 OPT、相关机 OPT 和配置族。任意参数结论依赖正文解析证明。 |
| [冻结输出](equivalence_audit/encoding_audit.json) | 不交族 m=2..6、配置合并族 q=2..5 的实际完整历史和有限枚举范围；无随机 seed、无浮点、无项目求解器依赖。 |

## 当前缺口与下一步

已知 BLMRS 算法桥是 UM<2 ⇒ Santa Claus 常数近似；两值版本有双向联系。
Santa Claus 的最小个人所得、CAG 的总覆盖、全历史均衡和实际算法输出仍须分别处理。
本轮比较已完成：五项直接编码 Claim 具有自足证明、独立解析审读；有限核验实际范围如上。
另核到 max-k-cover→MMDA 的文献 gap 归约，所以中央最大覆盖骨架有实质联系；
该归约不包含完整 SPE，不能视为 Q-CAG-HALF 与 UM-TARGET-v1 等价。
后续只在出现具体新归约或需借用某机制时按精确合同接续；本轮没有给难度或求解成本作可靠预测。
外审及新颖性未认证，本区不是共享 canonical 状态提升，两个主目标保持 OPEN。

保存本人目录：python3 work.py checkpoint research/workspaces/customer-attraction/R-c90acbef8c6a45f28bf33b5f639d6e99 -m '阶段备份：两题自然编码与精确目标不保持'

## 交流与状态

可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。
