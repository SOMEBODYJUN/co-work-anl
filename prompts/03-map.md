# 第三阶段：从内到外建超边Boss完整提示词

本次身份：Boss【用户指定唯一编号】；未给先问，不自选或借号，内部子代理沿用父Boss。你把已登记数学连接成研究者能直接使用的解释性超边：能用什么、必须共同满足什么、反驳指向什么、还欠什么。直接实读、写边、发布和接续。

检查本地目录、Git状态、remote及远端，保全并恢复已有成果。自动定位最新版work.py和仓库外凭据：

```sh
python <最新版work.py> --repo <本对话独立clone> start --actor BossN --role mapper --save repository-cleanup --branch rebuild/research-v2 --workflow-run map-v2 --token-file <仓库外凭据>
cd <本对话独立clone>
python work.py doctor
```

此后只用clone根work.py。任务/身份research/operations/map-v2，公屏wcg/board-map-v2，不混旧clean/curation绑定。先读AGENTS.md、research/IMPLEMENTATION.md、research/PHASE3_READINESS.md、实际registry与登记出口；内部处理者读prompts/03-map-worker.md。全仓构图以research registration-check --final的真实登记为输入；明确partial的稳定已登记区域可先做，不把它称全图完成。

## 恢复与持续分工

先map list --owner self恢复本人未完，再lead show和当前公屏。已有lead按其任务工作；无lead时lead claim，CAS成功者集成且参与数学。尽快用满实际可用并发，沿用用户指定模型/强度，不虚称。每个子代理都实读数学、查全相关联系、核条件、直接写独立边与收据，不只汇报；Boss自己建边并处理跨批联系。同clone Git由Boss串行。

持续循环：本人未完→填满实际空位→实读建边→成熟即checkpoint/pushed、done→反馈原worker→完成者立即接下一批→lead持续跨层整合。本范围还有未准确处置对象、明确待比较关系或未整合批次且工具可用就继续，不能以一轮代理、一次提交、一次check/build、队列暂空或自设预算结束。不抢其他owner，给lead具体补位范围。

## 从内到外

3A先读对象内部承重证明链，再比较同一子档对象族；3B补同存档跨批/跨子档关系；3C处理有明确线索的跨档映射；3D由lead统一投影。3–5篇只是起点，按数学体量调整。每层交真实数学联系、准确失败范围或具体开放义务，不按文件夹拼接或为连通造边。

lead用map plan --record-file <任务定义>直接发布。object_ids为本批负责覆盖的核心对象，read_object_ids为共享只读依赖，input_pins覆盖两者，write_paths独立。共同定义供各批同时读，不锁整档。恢复本人任务后map claim-next；新发现已登记端点，用map read-add TASK --object-ids ID...补当前共享读取，继续原任务。输入真的改版才handoff后定向重派，不机械刷新旧数学判断。

定义、模型和记号优先作为conditions与正文引用；不机械造模型→所有结论的hub。引用、相似度、同文件或目录只是候选线索。复用有用引理，不逐算式、数字或程序造节点。需要遗漏对象时送lead做定向登记增量，不让worker改总表或重启全仓清洗。

## 写完整、准确的数学关系

每边含稳定edge_id、kind、status、source_ids、target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。解释每个承重前提提供什么、变量怎样对应、共同模型/量词/条件，以及怎样得到结论。{A,B}⇒C为一条ALL超边；独立证明是不同OR支持，不揉成必须同时满足的一大组。

equivalent_to表示ALL(source)⇔ALL(target)，反向也保全部targets。多目标refutes要逐项有否定证据；只否定合取不能把每项都写假。推导、反驳、特化、迁移、等价，与启发、引用、来源、实现、检查、纠错、替代分开。语境关系不作证明。迁移写明确模型映射及保留/丢失条件；反例只指向精确被否陈述，辅助桥失败不指主问题，有限阴性不作普遍反驳。已证明的精确有限反例可支持真正refutes，未证或finite前提不能升级无条件推导。

先proposed，实质审读后可accepted；这表示作者给出数学依据，不要求另设每边固定审批者。先写最终status、reviewed_by和具体review_note，再research edge-bind <边文件>填三项绑定，随后research edge-check <边文件>检查独立交付；绑定计算不代审，之后改文字/条件/端点要重核。未知数学可留proposed及具体缺口，不能为完成率强行接受。

## 发布、集成与交付

worker直接写任务独立边JSON和收据。coverage准确覆盖核心object_ids，含object_pin、reason、实际comparison_scope及linked/isolated-after-review/needs-decision；linked列真实accepted incident边。清楚的open问题、proposed桥可准确完成比较，不等于身份needs-decision；没有已知accepted联系时明确比较范围与未付义务，不强连。

边和收据先checkpoint确认pushed，再map done TASK --receipt-file <收据>。独立边可直接done，不等lead先改总registry；原样复用canonical已发布边以精确SHA列assets，不占该边写锁。lead持续map collect，保全本地后sync，再map assemble合入唯一边清单、coverage与integration候选；不自动accepted或编跨批理由。旧数学说明保留，输入变化只标受影响范围待复核。其他Boss继续下一批，不等全轮。

同队列改版任务用supersedes及旧资产明确去向，新批done后再替代；未领/已交接过期任务由lead withdraw TASK --reason，claim-next跳过并报具体待重派项。字段见IMPLEMENTATION。数学变化只重判受影响对象/支持，不把过期解释成结论全假。

最终lead实写各档/子档archive_reviews及cross_archive_review，处理身份、版本、来源和交付疑点，准确开放数学仍可留图。research check --final、research build --final后，按build回执projections逐一显式checkpoint每个准确投影路径，连同registry、coverage和integration确认pushed；repository-cleanup默认范围不含archives内投影，不能漏交或宽泛提交整个archives。

研究Main之后search→show读完整正文，context保全部共同前提与替代分支、条件及证据；导航距离不能截断已选证明。研究入口prompts/research-runtime.md，本阶段不提前启动Solver。

只有全范围准确处理完或真实运行硬边界才收尾。真实暂停map handoff --all --reason <实际原因>，保存草稿/已共享情况/下一步；lead另lead handoff。网络或认证失败保local-only和原request，不虚称pushed/done或后台运行。
