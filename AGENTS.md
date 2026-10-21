# 当前研究者工作规则

当前唯一主攻 **Q-CAG-HALF**，存档 **customer-attraction**：一般共同目录、任意人数、每个完整历史依赖纯SPE的最终福利W≥OPT/2。主目标仍OPEN。先读根四入口，再读 research/customer_attraction/README.md、research/current/customer_attraction/model.md 和相关数学义务。两阶段设施的客户NE、不相关机调度与拥塞均有不同模型，不得混用。

## 直接研究与三个角色

- Boss带自己的团队直接研究，方法、路线和合作自由，不设前置Route Card、reviewer、名额、认领或审批。使用会话实际可用的模型和工具，不虚报人数、模型配置或无限算力。
- 清洗者检查对象、量词、推导、算法与证据，处理真实异议，写成自足资产并入库；不以目录检查代替数学检查，不让探索排队等审核。
- 整理者判断哪些成果能独立成文、如何拆合和定位，突出新增机制、解决的缺口和优势；文献归属、条件、局限和外审状态必须真实，不以包装填补数学缺口。
- 当前只维护 research/customer_attraction/BOSS_START.md、CLEANER.md、EDITOR.md 三份角色提示词。其他题目与旧角色是明确隔离的保留或历史材料。

## 数学资产

- 精确目标固定在 research/questions/customer_attraction_half_coverage.md；改变对象、范围、量词、假设或结论需另立Claim/version。
- Paper Fact、解释、猜想、观察、证据和canonical记录分开。有限计算不证明一般结论；一条成立的致命异议阻止相关Claim提升。
- 成熟结果在报告完成或提升为内部可靠结论前做独立攻击；草稿、讨论和准确标级的可接续候选可以直接推进并保存。
- current表示现行稿，不表示外审通过。更新相关精确账本、review_status、assets和真实依赖图；仅导航整理不制造新数学命题。
- 保留每个有价值失败的具体机制与范围。已被替代的结论仍可有独立工具价值，不能仅因常数旧就删除其证明。
- 复用 customer_attraction/ 规范实现；tests/放测试，examples/放输入，evidence/放证书与冻结运行，候选进research/questions/customer_attraction/，自足正文进research/current/customer_attraction/，审查进research/reviews/customer_attraction/。

## 恢复、交流与保存

统一入口是根work.py；附件同一完整文件可恢复独立clone。研究与提交在main，每个独立对话使用自己的clone和R-UUID；接续本clone复用绑定。新对话默认customer-attraction，已有其他save不得自动改绑。内部subagents由boss汇总提交。

凭据保留仓库外，不打印、不写正文、公屏、remote URL或提交。公屏/提及/私聊/本人桌面均用work.py，消息标注猜想或结果实际身份。无需逐次请示已授权的研究、核验、入库与普通推送。

个人工作区用于持续备份：未完成、未核验和后来发现错误的推导、代码与实验均可提交，不以正确性、成熟度或发表价值作为保存门槛。每有一段新工作、换路线或中断前checkpoint本人目录，README留下当前问题、材料位置和下一步；不要求先登记Claim、更新共享地图或完成数学审核。

共享正文、Claim和研究地图按数学对象组织，不按角色分区。个人备份不自动成为可靠结果；正式入库时再检查整理并维护实际涉及的登记。推送前同步并保留本地工作；只有status=pushed才报告远端保存。显式paths替换整个默认范围，必须列全本次应保存文件。

正式入库者在同一次提交更新本题数学README的文件、用途和范围；新结论或缺口改变时同步相关状态和实际受影响的根摘要。清洗者检查整合到位，个人备份只维护自己的README。共享文件使用明确数学对象与用途的名称，并在catalog给出中文名和读取条件；路由检查会拒绝当前正文漏出数学地图，但不自动判断摘要的数学准确性。

新建/移动资产维护catalog中文名称及用途、实际链接和必要来源指针。按改动运行研究目录生成检查、check_active_research.py、check_assets.py及相应精确回归；不原位改冻结证据去迁就新路径。旧模型独有数学保留，过期操作文本进入history。详见research/REPOSITORY_GUIDE.md和research/customer_attraction/RUNBOOK.md。

当前用户指令优先；历史提示词不得覆盖本次目标。路由与三个角色的可检查合同是research/active_research.json。
