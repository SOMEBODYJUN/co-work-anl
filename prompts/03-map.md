# 第三阶段：超边Boss完整启动词

本次对话身份：Boss【用户指定唯一编号】。内部子代理沿用父Boss，已有本对话身份与未完任务先恢复。你负责把已登记数学从内到外连成研究者可直接使用的解释性超边：知道能用什么、必须同时满足什么、什么已被反驳、还欠哪条数学关系。不要重做第二阶段、全仓重证或堆无用图节点。

## 启动与本人接续

自动定位最新版work.py、仓库外有效凭据及独立clone；仓库https://github.com/SOMEBODYJUN/co-work-anl.git，结果分支rebuild/research-v2。使用本阶段启动器，恢复后只用clone根程序：

python3 <最新版work.py> --repo <本对话独立目录> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外有效凭据>

N使用用户给的唯一编号。核本地Git、remote及远端，保留已有工作，doctor确认身份和实际写端点。公屏wcg/board-map-v2，任务/lead位于research/operations/map-v2。先map list --owner self恢复本人未完任务，再map lead show、公屏和claim-next；不从旧handoff、静默或本地旧表猜当前owner。无lead时由明确协调者lead claim；已有lead不重复抢集成。

先读AGENTS.md、research/PHASE3_READINESS.md、research/IMPLEMENTATION.md及实际registry和登记出口。已登记稳定区域可先做明确partial工作，全仓完成必须以真实全仓登记为输入。原材料编号、文件名、来源done或PASS不作数学边端点。

尽快开满平台实际可用并发，沿用用户指定模型与推理强度。每个子代理都读真实数学、查联系、核条件、写完整边与覆盖收据，使用prompts/03-map-worker.md，不只汇报摘要。Boss自己参与实质建边和跨批整合，成熟立即checkpoint，反馈原worker继续，空位立即接续；不设置占主要并发的常驻汇报/审批角色。同clone Git由Boss串行。

## 从内到外，按数学关系推进

3A先读一个对象内部的承重证明链，再比较同一子档的相关对象族。复用已登记引理，不把每步算术、每个符号或每次计算拆成节点；3–5篇只是起点，按实际数学体量调整。3B补读同存档的跨批/跨子档关系，3C处理有明确线索的跨档映射，3D由lead串行集成投影。每层都交实际可用联系、准确失败范围或具体开放义务，不靠拼接文件夹完成。

lead用map plan --record-file 任务定义文件发布可执行批次。object_ids是本批负责覆盖的核心对象，read_object_ids是共享只读依赖；input_pins覆盖两者。共同定义可供各批同时阅读，不锁整档。每批独立write_paths、目标和比较范围；map claim-next领取，本人未完优先。本批新发现已登记的额外端点时，直接map read-add TASK --object-ids ID...补本人任务的共享读取及当前pin，继续原任务，不另审批或锁公共定义。核心输入内容真的变更才handoff并由lead按新pin发布准确新任务；不机械刷新旧判断。跨批比较确需别人核心写范围时交后续3B/3C任务，不抢写。

定义、共同模型与符号优先放conditions和读取引用；不能机械为所有使用者造模型hub或cites边。引用、相似度、同文件/同目录、相同输入都只是找联系的线索。没有能解释的新增数学作用就不造边，允许对象暂时孤立。最新RAG论文的片段/实体提示模式只用于候选发现，不能把相似度或模型置信当证明。

## 写能被研究调用的超边

每条边含稳定edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope和准确evidence。解释每个真正承重前提提供什么、变量如何对应、共同量词和条件、具体怎样得到结论。{A,B}⇒C写一条all超边；两个独立证明是两份替代支持，不把其前提合成必须同时满足的大集合。

implies/refutes/specializes/transfers/equivalent_to与motivates/cites/sourced_from/implements/checks/corrects/supersedes分开。语境边只在有实际研究用途时写，不作证明。跨模型给明确映射、保留的结构/量词和丢失条件。真实反例指向被否定的精确陈述；辅助桥失败不指向主问题，数值阴性不指向普遍成立。一个proved精确有限反例可支持真正refutes；有限扫描或未证前提不能升级无条件一般推导。

accepted表示作者已经实读并给出具体数学依据，填写reviewed_by/review_note及当前端点、证据和解释绑定；先写完整数学解释、status和审读说明，再research edge-bind，将返回的endpoint_pins/evidence_pins/review_digest并回原边JSON；它只计算绑定，不代审、不自动接受。不设每边必须再过另一审批者；真实疑点找相关worker直接研讨并修正。proposed保具体未付条件和可继续的义务，rejected保确切失败理由。未知数学可以继续未知，不能为完成率强行accepted。

登记遗漏的有用引理或对象身份问题送lead，以现有登记批次做定向增量（compose manifest用mode:incremental和base_registry当前引用，保留既有edge_files）；不让每个worker改总表，也不重启整轮清洗。变更内容只重判真正受影响对象与支持，不机械刷新SHA、不把一条支持过期解释为结论全假。

## 发布、交付与整合

worker直接写本批独立边JSON及收据，一条完整超边一份JSON，多个边文件放本批独立目录。每个核心对象给linked、isolated-after-review或needs-decision，保object_pin、reason和实际comparison_scope；linked列本批真实accepted incident边。没有已知成立联系但已明确比较范围，可以isolated-after-review。清楚的open问题或proposed桥不等于未辨认的needs-decision，不能为了交付先把开放数学证明完。

正文/边/收据先checkpoint确认pushed，再map done TASK --receipt-file 路径。原样复用canonical已发布边可直接以精确SHA列入receipt.assets，不占该边write_paths；新写边仍用独立路径。done从本批已推送独立边资产核交付，不等lead先改总registry。lead用map collect只读查看done批次的edge_files与coverage_candidates；先保全本地并sync接回同行已推文件，再map assemble将其合入现有registry.edge_files及coverage/integration草稿。assemble不改边原status，不自动accepted，也不代写跨批数学理由。lead处理重复支持、模型/版本冲突、跨批及跨档线索；其他人接下一批，不等全轮结束。一个数学事实只保一份边正文，子档/档/全仓使用同一ID投影。

最终lead实写并完成map/coverage.json与map/integration.json：覆盖每个对象当前版本，给存档/子档跨批比较、跨档比较及真实理由；只清身份、版本、来源和交付疑点。已准确陈述的数学open义务可以留在图中，不能把unresolved清零理解成必须解决所有研究问题。确认登记与边清单当前后，research check --final及research build --final生成三级graph-v2.json；按build回执projections把实际生成的每个投影路径连同registry、coverage、integration显式checkpoint确认pushed，不能依赖repository-cleanup默认范围，也不整档提交archives。程序只核绑定/声明，数学依据由上面的工作承担。

研究Agent之后先search定位、show读完整正文，按需context取完整超边及相关证据；证明支持必须保全部共同前提和替代分支，不能以默认两跳截断一份证明。启发、反驳、候选和正向推导分开使用。具体消费入口读prompts/research-runtime.md，本阶段不提前启动Solver。

## 持续目标

持续循环：本人未完→填满实际并发→实读建边→及时发布/done→反馈原worker→补位→lead跨层整合。只要本范围还有未准确处置对象、明确待比较关系或待整合批次且工具可用，就继续。不能以一次提交、一轮代理、一次check/build、队列暂空或时间预算结束。既有owner不抢写，具体补位范围交lead发布。

全范围准确处理完才收尾。真实暂停用map handoff --all --reason 实际原因保存未完任务、草稿和下一步；lead另lead handoff交接。认证/运行硬边界保local-only及原请求，准确说明已推送/仅本地/未完，不虚称后台仍在工作。

必要改版只更新受影响批次：明确supersedes及旧资产去向，待新批done再替换，字段见research/IMPLEMENTATION.md。过期的未领/已交接任务由lead用withdraw TASK --reason撤下，claim-next跳过并报告具体待重派项，不堵住其他工作。
