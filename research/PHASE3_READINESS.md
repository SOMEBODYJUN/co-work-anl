# 2.5第三步与第三阶段执行入口

2.5第二步的已发布成果作为输入，不再重复清洗。登记与正式图在真实执行时产生；prepared配置、程序审查和私有演练不表示全仓数学任务已经完成。

用户每阶段只需本分支最新版work.py、仓库外凭据和一份完整Boss词。内部worker词与字段由执行者自动读取，不让用户另收集Project文档。

| 阶段 | 完整Boss词 | 内部worker | workflow-run / role / 公屏 |
| --- | --- | --- | --- |
| 2.5第三步：登记 | [02.5-3-register.md](../prompts/02.5-3-register.md) | [登记worker](../prompts/02.5-3-worker.md) | p25-register-v2 / curator / wcg/board-registration-v2 |
| 第三阶段：超边 | [03-map.md](../prompts/03-map.md) | [构图worker](../prompts/03-map-worker.md) | map-v2 / mapper / wcg/board-map-v2 |

## 稳定身份与持续协作

原来源ID追溯版本，object_id标识精确数学对象，edge_id标识解释充分的关系；Boss/task/run只管协作。沿用已有精确Claim ID，不从路径、类型或全文hash造身份。一页可有多个对象，多篇可共同支持一个对象；代码、证书和数值不是自动生成的命题节点。

每个对话使用用户明确给出的唯一Boss编号及独立clone，继续原对话先恢复原身份和未完任务。各阶段任务、people和lead位于research/operations/<workflow-run>，工作区位于research/workspaces/<workflow-run>/<Boss>，不改绑旧curation/clean clone。公屏用于交流结果和依赖，认领/交付由当前远端队列确认。

登记用registration-task，构图用map，二者共用协作引擎而保持运行域隔离。lead通过CAS取得唯一集成权，发布任务并参与数学；每个Boss带子代理做实际阅读、登记或建边。用满用户要求且实际可用并发，批内反馈交原worker，完成一包及时保存、推送、done，下一包补fresh worker，lead持续整合，不等待整轮。本人未完优先，不预占将来批次。

持续到本范围准确处理完或真实工具硬边界；一次提交、一次检查、暂时队列空或自设时限不能替代完成。普通竞争自动重选，响应未知核原request_id；暂停handoff，lead另交接集成。claimed不证明进程仍活着，静默不自动转移所有权。具体命令与收据见[IMPLEMENTATION](IMPLEMENTATION.md)。

## 2.5第三步：对象登记独立闭合

lead先依据第二步真实已发布出口生成path/SHA清单，freeze固定baseline并推送，再发布独立登记批次。repository范围核真实Git材料分母，稀疏缺页须恢复，不能以可见文件数冒充全仓。局部工作明确partial及实际路径；必要附件显式列入。

完整可复制启动顺序只保留在本阶段Boss词：先恢复/取得lead，发布inputs与baseline，再batches-draft、plan和批领。其它Boss恢复本人未完并领取已发布包；这里不再维护第二套启动脚本。

登记批次包含预算内几十/百份材料，可一次领交多个包，不逐材料远端认领。worker复用成熟正文，实读精确身份、陈述、模型、量词、假设、边界及来源owner，有疑点再深读承重证明；不重新清洗或重证全部旧成果。直接写独立schema:2批次；一份文件里的不同Claim不吞并，多份正文的同一对象不重复造身份。批次和收据先checkpoint确认pushed，再done；lead用compose/register持续收拢唯一registry，不让多人覆盖总表。

完整定义、一般/条件结论、有效反例、构造、可复用方法、算法保证、猜想、具体障碍与开放义务都可登记。精确有限反例若有完整证明可proved，普通扫描为finite。明确open数学不是身份needs-decision；excluded只记登记去向，不执行删除。

完成以本轮全仓输入逐项准确处置、稳定身份及完整正文/证据可读、owner明确和跨批冲突消解为准。registration-check --final只验登记，不要求超边。新材料字节另冻baseline，incremental/base_registry保现有数学和边；不重启全仓清洗。

## 第三阶段：从内到外解释关系

3A先对象内部承重链，再同子档对象族；3B同档跨批/跨子档；3C有明确线索的跨档映射；3D唯一lead集成三级投影。稳定已登记区域可先做明确partial比较，全仓完成以真实全仓登记为输入。

初始3A用research map-draft生成候选预算包，再map plan；3B/3C只对明确新比较frontier生成计划，不无条件全仓两两枚举。正文+元数据默认按Sol官方500K窗口预留200K后规划300K，这是估计而非本会话容量实报；同页独立Claim及共享证据按实际完整区间计。

任务object_ids是负责覆盖的核心，read_object_ids共享只读，input_pins覆盖两者，输出路径独立。增加已登记依赖用read-add，不锁共同定义或重派整批。对象/材料编号、文件名、相似度和来源done不能作推导依据。

一条ALL边保全部共同前提、端点作用、条件、量词、数学解释和证据；独立证明分开，等价关系保两个方向。定义通常作为条件和引用，不机械造模型hub。反例精确指向被否陈述，迁移写明映射与丢失条件，引用/启发不当证明。作者实读后accepted，不加逐边常驻审批；edge-bind只算绑定，edge-check保留为独立交付检查。

本批独立边先推送即可done，不等总表先挂边。lead用collect→sync→assemble连续汇总，保已有数学说明，定向复核受影响内容。每个对象保真实比较范围及linked/isolated-after-review/needs-decision；proposed桥与准确open义务可留下，不为完成率造边或强证开放题。

最终map/coverage.json覆盖当前对象版本，map/integration.json记录各档/子档跨批及真实跨档比较；只消解身份、版本和交付疑点。research check --final与build --final生成graph-v2三级投影；按projections显式checkpoint所有输出及registry/coverage/integration确认pushed，不漏archives内投影。

## 研究Agent和计算如何接续

研究Main按[研究流程](RESEARCH_WORKFLOW.md)及[完整Main词](../prompts/research-runtime.md)启动真实Solver。登记/构图阶段按实际并发工作，不提前运行求解团队；当前自由数学研究RUN的固定三Solver配置只适用于后续研究。

registry定位正文，context返回完整ALL支持、分开的替代OR、条件与未付前提；refutes和研究线索不当正向证明，导航hops不截断已选证明。按需读完整正文/证据，反馈原Solver继续，保存packet、笔记、事件和具体下一步。局部变化只重判有关支持，不因无关旧边重扫全仓。

普通批计算优先已有云端或适合的现成算力，短计算可在当前环境运行；Codespaces用于确需持续交互或特殊环境，不作普通计算默认入口。具体云请求、实际run/产物取回与当前状态见[GITHUB_RESOURCES](GITHUB_RESOURCES.md)。配置和API接受不等于计算完成，数学价值由实际论证与输出判断。
