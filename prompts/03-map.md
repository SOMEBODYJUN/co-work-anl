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
python work.py board-init
```

此后只用clone根程序，公屏wcg/board-map-v2。读AGENTS.md、实际registry/登记出口及research/IMPLEMENTATION.md的边、coverage和零边示例；worker读prompts/03-map-worker.md。全仓构图接真实完成的登记；稳定局部可明确partial先做。

所有Boss平权。先map list --owner self恢复未完，按实际空位领合适的包。任何Boss可以发计划、补办、回收和集成。同一批写入由当前认领者负责，共享定义和证据可同时读。每包用fork_turns:none的fresh worker，给Boss号、clone绝对路径、任务路径和内部词；批内反馈找原worker，完成一包立即补新worker。

队列没有可领时看实际归属和缺口。能推进的子档直接发包。确定原Boss无法接续时，可用 `map reclaim <任务ID> --reason <原因>`，或 `map reclaim --owner BossN --reason <原因>` 一次释放该Boss未完包。按已推送的证据和草稿接续。

## 每包怎样做数学

**读清对象。** 按object_ids/read_object_ids读精确陈述、模型、域、量词、条件、objections和必要完整论证，确认已成立与未付部分。正文仍是Markdown，端点使用登记object_id。

**提出具体比较。** 从结论可否作另一证明的前提、共同假设/结构、模型特化/变换、反例目标、所用工具及未付条件，检索相关登记并读原文。没有旧链接也要主动提出有数学理由的比较。额外已登记端点由Boss用map read-add加入，共享读取不抢他人核心范围。

**决定关系和粒度。** 一条边可承载完整多步论证；常规代入、记账和算术写进explanation及证据，不逐步造节点，不为自足证明造自环。确有独立复用价值的缺漏引理，才给Boss精确陈述、条件、完整出处及单独登记理由。

{A,B}⇒C保一条ALL边，交清各前提作用、条件、变量对应和推导；独立证明分OR。equivalent_to须证双向，反向保全部targets。refutes逐项指明确被否命题，辅助桥失败不冒原题反例。迁移交清对象、允许选择、约束、量词和目标怎样对应、保留/损失什么；只证单向就保单向。引用、启发、实现及有限观察保语境身份，不作一般证明。

**区分关系成立和前提成立。** 推导完整但前提未证，可accepted+relation_mode:conditional，写明未付前提，不提升终点真值；推导本身缺桥才proposed，写准确缺步。作者实读后可accepted，无固定二审；先定status、reviewed_by/review_note，再用 `research edge-bind <边文件> --write` 写回绑定，接着edge-check。某证明缺步只撤具体支持，保有效替代证明；命题被反例否定另作判断。文字/证据变化定向重核。

## 从最相关的数学做到跨档

3A先从一个子存档里已知的承重关系做起，比如同一证明链、同一反驳目标、同一模型下可直接复用的引理；没有子存档时从该存档的本地对象族做起。同一子档的几个小组可以一次认领，组内实质比较。3B用已核对的对象做同一存档内的跨包、跨子档比较。3C有明确的两方对象、映射和数学问题时才跨存档。局部稳定就接下一层，3D贯穿全程整合已有成果。

已有计划先恢复。没有合适批次时从当前子档开工，下面的scope用实际目录。0任务时转恢复、补比较范围或整合。

```sh
python work.py sync
python work.py research map-draft --stage 3A --scope <archives/存档/subarchives/子存档> --task-prefix <子档短名> --output map/planned-tasks.json
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next --prefix <同一子档短名> --count <实际worker空位数>
```

3B/3C用重复 `--object-id` 或 `--objects-file` 给具体对象，再用 `--comparison` 写要验证的数学问题。可用 `map claim <任务ID>` 直接接这个前沿。按关联和上下文预算整包读取，共同证据去重。超大正文在同任务分章节接着读。机器证书读规范、相关记录、检查器和必要核验结果，按具体数学疑点决定是否复算。

发现原文确有错，给出原位置、准确改法和受影响对象。发现者可以直接做最小勘误，把原文、相关SHA/版本、冻结清单和总表一次推送。确有独立价值的缺漏对象也由发现者或接续Boss补登记，细节按PHASE3_READINESS。

同步新登记后，只加依赖用read-add；在领包的输入改版时保草稿并handoff，重派改版包。已done的包有待定或过时输入时，用 `research map-draft --repair-task <旧任务ID>` 定向替代，保留仍有效的比较，逐项交代旧边去向。其余包继续推进。

## 写出产物，成熟即交，持续做到准确出口

按write_paths写独立边JSON及coverage收据JSON，完整模板见IMPLEMENTATION。每个core对象说明实际比较过谁、成立或不成立的理由及仍欠什么。linked要有核实的逻辑关系；isolated-after-review要完成实际比较。身份、版本或交付疑点写needs-decision。

本包可多边或零边。linked只列核实过的逻辑关系。引用、实现和计算可以保存为语境边；只发现语境边时，实读比较后以isolated-after-review交付并写清数学理由。零边写实际比较范围和结果，收据assets:[]。同端点的独立证明各保完整推导。

成熟几个交几个，不等整轮。checkpoint本次准确产物确认pushed，Boss自动组成task_id/receipt_file的ready数组，用map done --record-file批交，单批done仍可用。未知回执沿原请求核远端；认证失败保local-only并停止新认领，参数按IMPLEMENTATION。

任何Boss都可边收边sync、assemble，写本次涉及的archive_reviews及cross_archive_review。若远端先有新成果，按新快照重组并接上已完成的实质审读。当前对象、明确比较线索和交付都处置后，用research check --final、build --final，按projections明确checkpoint所有投影及registry/coverage/integration。

持续循环：恢复未完→补空位→实读比较→成熟保存和交付→接下一层或下一包。队列空时继续核对未处置对象、明确数学线索和待整合成果。开放问题可以保留，写清已成立部分和未付条件。真实暂停用map handoff --all --reason保存草稿、共享状态及下一步。
