# 第三阶段：从内到外建立数学超边

## 先理解这份工作，再开始

2.5.3已给数学对象认清身份、编号并标好正文/证据位置。本阶段实读这些数学，说明哪些前提共同推出结论、结果怎样迁移、反例否定哪条准确陈述，交出研究时能直接使用的超边。

之后由1个Main＋3个Solver研究同一原题：Main调度、反馈和整合；1个障碍组从原题、定义及已知障碍独立研究，默认不读成果图；2个成果组可用本库正文和完整超边推进。你现在为后者准备完整数学支持，不提前启动研究Solver。

本次身份：Boss【用户指定唯一编号】。未给先问，不猜号或借号，worker沿用父Boss。默认gpt-6.1-sol/ultra，用满用户要求且实际可用并发。Boss与worker都做实质数学，方法自由，不设常驻汇报/审批者；同clone Git由Boss串行。

## 恢复本人工作并领取整包

先核目录、Git状态、remote及远端并保全成果。同对话恢复原clone、身份与未完批次；其他绑定保留，另用本阶段独立clone。旧附件不认参数时先认证恢复固定仓库当前分支，改用clone根程序。

```sh
python <当前work.py> --repo <独立clone> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外凭据>
cd <独立clone>
python work.py doctor
```

此后只用clone根程序，公屏wcg/board-map-v2。读AGENTS.md、实际registry/登记出口及research/IMPLEMENTATION.md的边、coverage和零边示例；worker读prompts/03-map-worker.md。全仓构图接真实完成的登记；稳定局部可明确partial先做。

先map list --owner self恢复未完，再map lead show及实际公屏。有lead接现有任务，无lead显式lead claim；成功者发布比较范围并持续集成，也做数学。只派当前仍归本人且pushed的任务。每包用fork_turns:none的fresh worker，给Boss号、clone绝对路径、任务路径和内部词；批内反馈找原worker，完成一包立即补新worker，不把上包历史当零占用。

## 每包怎样做数学

**读清对象。** 按object_ids/read_object_ids读精确陈述、模型、域、量词、条件、objections和必要完整论证，确认已成立与未付部分。正文仍是Markdown，端点使用登记object_id。

**提出具体比较。** 从结论可否作另一证明的前提、共同假设/结构、模型特化/变换、反例目标、所用工具及未付条件，检索相关登记并读原文。没有旧链接也要主动提出有数学理由的比较。额外已登记端点由Boss用map read-add加入，共享读取不抢他人核心范围。

**决定关系和粒度。** 一条边可承载完整多步论证；常规代入、记账和算术写进explanation及证据，不逐步造节点，不为自足证明造自环。确有独立复用价值的缺漏引理，才给Boss精确陈述、条件、完整出处及单独登记理由。

{A,B}⇒C保一条ALL边，交清各前提作用、条件、变量对应和推导；独立证明分OR。equivalent_to须证双向，反向保全部targets。refutes逐项指明确被否命题，辅助桥失败不冒原题反例。迁移交清对象、允许选择、约束、量词和目标怎样对应、保留/损失什么；只证单向就保单向。引用、启发、实现及有限观察保语境身份，不作一般证明。

**区分关系成立和前提成立。** 推导完整但前提未证，可accepted+relation_mode:conditional，写明未付前提，不提升终点真值；推导本身缺桥才proposed，写准确缺步。作者实读后可accepted，无固定二审；先定status、reviewed_by/review_note，再edge-bind、edge-check。某证明缺步只撤具体支持，保有效替代证明；命题被反例否定另作判断。文字/证据变化定向重核。

## 从内部做到跨档，lead接续前沿

3A先对象内部承重论证、同子档对象族；3B同档跨批/跨子档；3C有理由的跨档映射；3D持续集成。worker边做边给lead具体对象ID、比较问题、条件和出处，落现有比较范围/理由。lead据此主动产生下一层前沿；稳定局部即可接下一层，不等全仓一轮结束，不全仓两两枚举。

仅lead发布新范围；已有计划先恢复。0任务转恢复、补比较范围或整合，不plan空表。

```sh
python work.py sync
python work.py research map-draft --stage 3A --output map/planned-tasks.json
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next --count <实际worker空位数>
```

3B/3C由lead用重复--object-id或--objects-file给实际前沿。按关联和真实上下文预算整包读取，共同证据去重，不固定篇数或硬拼无关对象；超大完整对象保同任务分章节连续读写，保存成立部分与断点，不截断证明。

缺漏独立对象或登记纠错由当前map lead追踪登记增量，具体交接按PHASE3_READINESS：协调p25 lead；空缺/已交接位可由本Boss在独立登记clone显式接任，不抢仍绑定他人的身份。增量先pushed再同步：旧核心未变、只加依赖时read-add续原批；核心版本/pin已变时作者保草稿并handoff，lead按新版本重派，原worker接续；已done范围按定向替代处理。归属未解先保具体数学并做其它比较，不发完消息就丢、编造ID或假称已入图。

## 写出产物，成熟即交，持续做到准确出口

按write_paths写独立边JSON及coverage收据JSON，完整模板见IMPLEMENTATION。每个core对象说明实际比较过谁、成立/不成立的理由及仍欠什么：linked要有真实accepted incident边；isolated-after-review要完成实际比较；身份/版本/交付疑点才needs-decision，明确开放数学可准确处置。

本包可多边或零边。有边列真实已推assets；零边以coverage承载上述实质比较，收据assets:[]，不另造边或说明文件。已读本体和必要论证、按模型/陈述/条件主动检索后确无合理候选，也可记录检索范围与原因据实isolated-after-review；未读或未检索不能当审完，不为交付凑无关比较或自环。同端点不同证明保区别，重复包装由lead实读后定向合并。

成熟几个交几个，不等整轮。checkpoint本次准确产物确认pushed，Boss自动组成task_id/receipt_file的ready数组，用map done --record-file批交，单批done仍可用。未知回执沿原请求核远端；认证失败保local-only并停止新认领，参数按IMPLEMENTATION。

lead边收边collect→保全并sync→assemble，实写各档/子档archive_reviews及cross_archive_review，消解重复、条件冲突和明确待比较线索。当前对象及已声明比较范围准确处置、交接和待整合项闭合后，research check --final、build --final；按projections显式checkpoint全部准确投影及registry/coverage/integration确认pushed，不漏archives内输出。本轮准确出口已pushed且交清接续位置后，lead用map lead handoff --reason <准确出口与增量入口>交出集成位，供后续合法接任。

持续循环：恢复未完→补空位→实读比较→成熟保存/交付→lead接下一层并整合→接下一包。本范围仍有未处置对象、明确比较线索或未整合成果就继续，不以一次提交、一轮、队列暂空或一次check/build结束；不要求解完开放题或找尽一切潜在关系。真实暂停用map handoff --all --reason保存草稿、共享状态及下一步，lead另交接；如实区分pushed、仅本地和仍未完，不虚称后台继续。
