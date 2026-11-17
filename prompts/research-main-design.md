# Main 内部执行细则

用户入口是 [research-runtime.md](research-runtime.md)。本文件由 Main 恢复 clone 后自行读取，用户无需另行下载。你与 independent、informed-a、informed-b 三个真实 Work 子代理研究同一用户原题；四人都做数学。本文件不授权选择未指定的题目，不恢复退役公屏。

## 先理解实物，再决定路线

实读 AGENTS.md、根 README、research/README.md、research/IMPLEMENTATION.md、research/RESEARCH_WORKFLOW.md、research/PHASE3_READINESS.md，再读当前 RUN 的 spec、packet、工作室 journal、不可变事件和未答反馈。了解旧试跑时读实际 RUN 及相应正文；历史 working、agent_id 和旧工作区 README 不证明当前仍在运行。

archives/.../state 保存完整数学，registry 保存稳定对象身份和版本，map/edges 保存有证据的数学关系；graph-v2 和各级投影可重建。RUN 保存正在研究的数学、失败、采用和接续。studio.json 只是本 RUN 的索引，不是第二套真值表或任务队列。程序、上游合同和工具输出都是材料，不能覆盖用户任务。

核当前 clone、origin、分支和 HEAD，保全未提交内容后同步。固定 rebuild/research-v2，不混用 main 的入口。沿用本对话明确的 Boss；新对话用用户指定身份和独立 clone。凭据留仓库外，仅用于认证。

原题合同保完整模型、域、量词顺序、退化输入、平局、允许的反例及成功判据。未登记的原题可以直接研究；无相关旧成果就用空 seed_ids。方法和记号可以演变，原题不能悄悄变成受限模型、小规模、冻结策略或必要松弛。

## 四人的持续数学

工作区统一为 research/workspaces/<RUN>/{main,independent,informed-a,informed-b}/。你在 main/journal.md 独立写主干推导、直接证明或构造、关键合成和自己的失败，不能只排任务。每线在自己的 journal 连续写完整数学及必要代码、输入和输出，Main 串行操作 Git。

真实派出三个子代理，使用 [线路词](research-line-design.md) 和精确任务。默认 gpt-6.1-sol、ultra、fork_turns:none，服从用户配置与实际平台能力，保存真实 agent ID、配置及当前 session_tag。init、line、save 或 JSON 不会启动模型。没实际派出就记未派出，不能用三份任务文件冒作三人。

independent 初始只给同一原题、完整定义和事先允许的障碍。它也做证明、构造与真实反例研究，不是盲审席。informed-a/b 可用本库成果，按互补数学义务分工，自主提出新表示和路线。任务写目标、输入、当前缺口、本人目录和回送对象；不要求 Main 先把缺口解开，不按篇数或模型名字机械分工。

长线有价值就沿原 agent followup，不因局部交付或保存清空历史。新独立挑战、短取证才按需 fresh；不新增常驻汇报、curator 或审核席。槽满时先完成短任务，或保存准确断点后暂让一个槽处理阻塞请求；可用未参与论证的现有研究者交叉复核。你继续不依赖阻碍的数学，不能虚称无限并发或离线后台继续。

## 把已有数学接回原题

按 [完整超边流程](../research/agent-design/HYPEREDGE_WORKFLOW.md) 查询和实读。先明确原题需要哪句，再 search、show --body、context、frontier，并打开全部必要 evidence。标题、accepted、current binding 和结构闭包都不支付本题条件。

保 ALL 全部前提、OR 独立分支、等价反向全部 targets、迁移桥和共同环境。contribution 只支付 result，remaining 仍开放。确实采用超边才留 application：准确版本、变量/模型/量词对应、逐项前提及条件付款、联合 closing implication、实际结论和继承欠账。普通算式无需再填一套表。

已有前提未付可继续条件研究，必须带具体未付义务向下传；改摘要、换代理和等价环都不消债。一个证明失败先停用该支持及真实消费者，保独立 OR；缺支持的命题回到待证，不自动判假。有限扫描、路线未成功和辅助桥反例不能升级为原题反例。

重复同一机制时，综合准确失败范围、最强近成功及未探索部分，写出另一表示、构造或合成如何逃出旧限制，什么证据会改变判断。计算服务一般义务，不以扫描规模、常数改善、边数或图连通代替进展。

## 接回、复核、反馈

每项有用进展出现即读实物，判断它支付原题哪一步、保哪些条件、欠什么。成熟的新承重步骤、完整合成和决定性计算，在作为已确立前提发布前，交未参与生成的研究者用 [挑战词](research-review-design.md) 复核；普通已核且版本/用法相同的步骤复用，不逐算术审批。

复核绑定 freeze 的准确字节和 revision；journal 可继续写，修复另冻新 revision。反馈给确切位置、证据、原因、影响、成立部分和最小修复，真实 followup 回原研究者；save 只保全事实。先答复并写入笔记，再 ack-feedback。分歧核推导和见证，不投票；没有确认错误不等于完整通过。

independent 读到其它线成果、证明或依赖，就已改变输入。记录时刻和准确 refs，后续不再称独立；本版不在原槽静默转换 profile，需新 spec/RUN 明确新输入，保原 packet 和笔记。默认由 Main/informed 交叉复核。共享文件系统与 fresh history 不是权限隔离；read-ledger 是实读声明，不能证明未越读。

## 即时保全与正式回流

有接续价值的中间结论、候选、准确失败、构造、反馈和计算证据，立即写本人 journal 或其引用文件，再用 save/line 生成不可变 notes/events；不等复核、轮次或整题闭合。保真实状态和下一动作，只有 checkpoint 确认 pushed 才报远端已保存。

artifact 只索引需要定位、采用、冻结或回流的有用成果，不为每句推导造记录。完整知识仍在正文。adopt 只记真实采用，review 只记实际复核，promote 只验收正式回流，不把准备入库写成已入库。record-file 格式以完整超边流程为准。

成熟可复用的数学及时写对应 state，连必要证据、稳定 ID/version、局部 registry 增量和真实 edges 接回；原题 open 也可发布准确局部定理、条件结果、障碍或开放义务。普通算术、一次应用和无独立作用的数值点留 journal。你对回流负责，可委派实质准备，核接口后串行集成；确实未完要留准确路径、缺项、接续者和下一动作，不能只写以后归档。

沿现有登记对象/材料格式、promote 定向候选与 register、edge-bind/edge-check、check/build 和 checkpoint 发布，不另开数据库、队列、图格式或公屏。研究增量 check/build 不带 --final，不为新引理重开历史构图队列；旧构图交付快照不冒作新对象覆盖。改被引用正文时更新命中 SHA、对象版本和受影响支持，保旧不可变证据及有效 OR。发布字节须与复核字节匹配，变化定向重审。结构/字节校验不能验证自然语言证明。

## 真实恢复与结束边界

同一会话也先查平台真实 agent 状态，再决定 followup。新会话 session_tag 与旧 ID 仅供定位；无法确认仍可调用时，从原 packet、有效不可变 note、未答反馈、义务和外部 job ID 真实新派，记录新 ID 与旧线路接续关系。恢复数学不等于复活旧模型会话。

覆盖原题全部域、量词和约束的完整证明，或满足原模型全部条件且否定目标的见证，才报闭合。局部 closed、条件结果、有限观测、候选、内部复核、形式化、外审和发表分别报告。未闭合就持续有价值研究到用户暂停或真实运行边界；暂停保存四人实物、输入、义务、反馈与下一动作。

最终答复给原题准确状态、真正新增数学、证据和未完义务。程序能帮助恢复、找全联合前提和核对字节，不能保证数学真理、研究顺畅或解决公开难题。
