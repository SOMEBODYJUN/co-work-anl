# 第三阶段：从内到外建立超边

本次身份：Boss【用户指定唯一编号】。未给先问，不自选或借号，内部worker沿用父Boss。你连接已登记数学，交出研究者能用的解释性超边：哪些前提共同承重、条件与量词是什么、反驳指哪条陈述、还欠什么。

## 启动与持续协作

先核本地目录、Git状态、remote及远端，保全并恢复已有身份、clone和未完任务。附件start --help若无--workflow-run/curator，只借其认证能力恢复https://github.com/SOMEBODYJUN/co-work-anl.git的rebuild/research-v2，再用clone根work.py，不拿旧start登记或覆盖仓库文件。已有clone若绑定旧阶段或另一对话，保留并另建本阶段独立clone；同阶段同对话才恢复原clone。

```sh
python <当前work.py> --repo <独立clone> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外凭据>
cd <独立clone>
python work.py doctor
```

此后只用clone根程序。任务/身份research/operations/map-v2，公屏wcg/board-map-v2。读AGENTS.md、research/IMPLEMENTATION.md、research/PHASE3_READINESS.md、实际registry/登记出口；worker自行读prompts/03-map-worker.md。全仓构图以registration-check --final的真实登记为输入；明确partial的稳定已登记区域可先做，不称全图完成。

先map list --owner self恢复本人未完，再lead show与实际公屏。有lead接其任务，无lead时lead claim；唯一集成人同时做数学。默认gpt-6.1-sol/ultra，以用户明确配置为准，尽快用满实际并发。Boss和全部worker都实读、比较、写边，不设常驻汇报或审批者，同clone Git由Boss串行；已有6个处理者就由他们直接做，不再每人向下启动6个。

持续循环：本人未完→填空位→读写整批→成熟即保存/pushed、批量done→lead持续跨层整合→接下一批。批内反馈原worker修订；done后立即补fork_turns:none的新fresh worker，给明确Boss号、clone绝对路径、本批任务路径、内部词与必要边界，Boss身份不变。用户明确继承/复用时扣已用或未知历史预留，不把上批历史当0。范围还有未处置对象、明确待比较关系或未整合批次就继续，不以一轮、一次提交、一次check/build、暂时队列空或自设预算结束。

## 关联与预算分批

3A先对象内部承重链、同子档对象族，3B同档跨批/跨子档，3C明确跨档映射，3D统一投影。篇数由数学关联和文本预算决定，可以几篇、十几篇或更多，不固定3–5、9篇或对象配额。

```sh
python work.py sync
python work.py research map-draft --stage 3A --output map/planned-tasks.json
python work.py map plan --record-file map/planned-tasks.json
python work.py map claim-next --count <当前实际worker空位数>
```

仅在尚无这批已发布计划或确有新比较范围时生成/发布草稿；已有任务先恢复，不重复plan同一批。回执0任务就恢复已发布队列或整合，不plan空表。sync保本地正文/registry一致，绑定阶段planner另读最新轻量队列metadata排重；同名候选直接刷新，已发布任务不覆盖。审草稿的真实读取范围后发布；引用只是找关系的线索，不自动成边。object_ids是本批核心覆盖，read_object_ids共享只读，input_pins覆盖两者，write_paths独立。只给当前owner仍为本Boss且已确认pushed的任务派worker；领取摘要给任务路径，worker只取本批完整定义。新增已登记端点用map read-add TASK --object-ids ID...继续原任务；真改版才handoff后定向重派。需要遗漏对象送lead做登记增量，不重清洗。

完整数学对象及必要证明是原子阅读单位；同页优先合读，独立sections可分包共享，不为去重合并Claim。共同定义/证据按实际区间去重。Sol官方500K窗口是规划起点，40%总预留随窗口同比缩放，500K时正文/元数据初值300K、预留200K，已用历史另扣，可调但不当实报剩余；字符不是token，其它模型不套500K。单对象过大保同任务按reading_passes/章节连续读写，不为每pass新增认领，不截断条件或证明。拆预算后仍保必要对照锚和未付前沿，不把跨档比较拆成互不相干的单边阅读。后续3B/3C只沿明确新联系；map-draft --stage 3B/3C必须用重复--object-id或--objects-file给出实际比较frontier，不能无条件重扫全registry。3D由lead整合，不用map-draft。

## 交付可使用的数学关系

每边含稳定edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。写清每项前提提供什么、变量如何对应、共同模型/量词与怎样得到结论。{A,B}⇒C是一条ALL超边，不拆成各自足够的二元边；独立证明分OR支持。equivalent_to是ALL(source)⇔ALL(target)，反向也保全部targets。

推导、反驳、特化、迁移、等价，与启发、引用、来源、实现、检查、纠错、替代分开。反驳精确指向被否陈述，多目标逐项有证据，不能把否定合取当每项为假；辅助桥失败不冒原题反例。迁移写明确映射与保留/丢失条件，有限阴性不作普遍反驳。定义通常作条件/引用，有真实数学作用才建边，不机械造模型hub或逐数字节点。

作者实读后可accepted，不设逐边固定二审流水。先定最终status、reviewed_by及具体review_note，再edge-bind填三项绑定，edge-check核独立交付；之后改条件、文字、端点或证据要重核。程序不代数学判断，proposed保未付条件，rejected保精确失败理由，不为完成率解完所有未知或强行接受。

worker直接写本批独立边和coverage收据。每个核心对象给object_pin、真实comparison_scope、reason及linked/isolated-after-review/needs-decision；linked列真实accepted incident边。明确open/proposed可准确完成比较，不等于身份needs-decision；无已知成立联系就如实留孤立与范围，不强连。

成熟边/收据只列本次明确路径，一次checkpoint确认pushed，Boss把当前成熟task_id/receipt_file自动组成ready数组，map done --record-file <ready文件>一次批交；单项done仍可用。ready仅本次输入，确认pushed后删，失败保原输入。成熟几个交几个，不等整轮。独立边不等总registry先挂边；原样canonical边以精确SHA共享复用，不占写锁。

lead持续collect→保全并sync→assemble，合唯一边清单与coverage/integration候选，不自动接受或编数学理由。旧实质说明保留，改版只标受影响范围复核；同队列替换已done批用supersedes明确旧资产去向，新批done再退出旧批。过期未领/已交接任务由lead withdraw，claim-next跳过并报具体重派项，不堵其他工作。

lead实写各档/子档archive_reviews及cross_archive_review；最终清身份、版本、来源和交付疑点，准确开放数学可留图。research check --final及build --final后，按回执projections逐个显式checkpoint准确投影路径，连同registry、coverage和integration确认pushed；默认保存范围不含archives内投影，不能漏交或整档乱提。

研究Main之后search→show/context取完整支持、条件、证据、反驳与开放义务，导航距离不截断证明；入口prompts/research-runtime.md，本阶段不提前启动Solver。全范围准确完成才收尾；真实暂停map handoff --all --reason保草稿/共享情况/下一步，lead另交接。真实硬边界保本地和原请求，准确报告pushed/仅本地/未完，不虚称后台继续。
