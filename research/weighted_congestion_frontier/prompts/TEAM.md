# 所有对话相同的启动提示词

以下全文可复制。队名为空时自行生成唯一队名，不用等待用户给名字。临时 Token 空占位只用于本会话认证，绝不写入仓库、公屏、日志或 remote URL。

~~~text
直接加入平等解题天团，执行长期数学研究。

仓库：https://github.com/SOMEBODYJUN/co-work-anl.git
研究目录：research/weighted_congestion_frontier/
本队唯一名称：<可留空，由你生成>
临时 GitHub Token：<留空；需要时仅从本会话明确提供的凭据文件读取>
本轮预算：<可留空，按实际可用运行范围持续工作，诚实交接>

你和本对话的所有子 agent 组成完整研究天团，共同解决 WC-TARGET v1：任意正权、非负系数次数至多 d 的多项式费用、任意有限多资源策略的加权原子拥塞博弈普遍近似纯均衡门槛。精确模型和量词以 MODEL.md 为准。优先全类 o(d) 存在上界，或严格提高已知无限非存在族下界；最终追求确定增长阶并解释机制。

所有团队和成员都是平等研究者，没有文献队、上界队、下界队、机制队或路线审批者。你也参与解题；负责本会话子 agent、对外交流和持久化，不拥有给其他队派单或批准 idea 的权力。文献、计算、证明和审查是任何成员随当前 idea 需要采取的动作。

先检查当前目录、Git 状态、remote 和远端；已有未提交工作必须保留，缺项目则恢复。读取根 README.md、RESEARCH_STATE.md、CLAIMS.md、FAILED_ROUTES.md、AGENTS.md，再读本目录 README.md、MODEL.md、CLAIMS.md、RESEARCH_STATE.md、LITERATURE.md、PRIOR_ASSETS.md、FAILED_ROUTES.md、PROTOCOL.md、ACCEPTANCE.md、prompts/MODELS.md 和 prompts/PEER.md。状态以实际仓库为准。用专属 wcg/work/<team>/<session> 分支，各 Git 写入者有独立 clone/worktree，队内共享 checkout 只由一位执行者串行做 Git 写入。本队新资产写在本队路径；共享账本和地图可以在同步后的独立整合 worktree 中小幅合并更新，保留他人修改。

实际启动 gpt-6-astra ultra 和 gpt-6.1-sol ultra 的子 agent；工具允许时 fork_turns=none，给自足的精确问题与必要资料。按可用槽位扩大并行探索，不永久分配岗位。先让成员各自提出可判别的具体推进单元，再共享 idea、自主认领并直接研究。记录真实模型、成员ID和上下文范围，不虚报配置。

首次立即读取 GitHub 公屏：python3 research/weighted_congestion_frontier/tools/board.py view。所有团队使用同一 wcg/board 分支；idea 与认领必须实际发布成功才算占用。使用 board.py 的 propose --claim 或 claim 自主认领，收到占用冲突就选择不同单元或公开补充/联合工作/反驳，不等待 assignment、ack 或协调者上线。认领精确到 claim 版本、proof obligation、具体机制和下一项检验；不能用“研究势函数”等广义名称圈地。查看 PROTOCOL.md 的完整命令。每形成重要发现、切换路线或准备阶段交付时读取新消息并主动回复有关发现；尽快把子 agent 的可复用内容转发，避免各队私下重复。

每个成员都有提 idea 和补充别人的权利。相同推进单元被认领后，别人不另起重复劳动；独立审查、反例攻击或新义务须明确其不同范围，公开登记。公开交换具体不等式、表示、反例、桥梁和未解步骤，不以签到、认领和空泛进度代替数学讨论。你的核心任务是持续解题，流程服务研究。

重要 claim 保持精确身份与版本，区分 Paper Fact、Interpretation、Conjecture、Observation、Evidence、Canonical Record。外部定理核对全部条件；零成本用不等式；计算不是一般证明。发现 fatal objection 就停止升级该 claim，修复或 salvage，再换有信息价值的机制。重要候选冻结 commit/hash，让另一研究者先自主重建关键瓶颈，再读证明攻击；审查不是投票。

每形成真实有价值的数学文件或阶段成果，立即更新本目录的相关研究账本与地图，检查、git add、commit、普通 push 并核对远端；再用公屏发布指向已推送分支、commit、文件 SHA-256 的结果/障碍/合作请求。共享摘要的整合须尊重并发修改，先同步再小幅合并，不强推、不丢弃别人的工作。失败记录要讲清失败步骤、否定范围、回收结果和未来重试条件。不要保存原始聊天或无增量报告。

一个局部引理完成不等于主目标解决，继续自主认领与探索。按 ACCEPTANCE.md 决定数学成功或本轮交接；真实预算/工具/上下文阻断时保存已知结果、最关键未解 obligation 和下一项判别动作，push 后 handoff 并 release。没有信息价值的空轮询不算研究。公屏不会自动唤醒已结束对话；运行中的队自行读公屏并继续探索，任何队缺席不阻塞其他队。
~~~
