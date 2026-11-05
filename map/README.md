# 从内到外建立可供研究调用的超边

当前只使用v2流程：[第三阶段完整Boss词](../prompts/03-map.md)、[固定阶段入口](../research/PHASE3_READINESS.md)、[字段与命令](../research/IMPLEMENTATION.md)。对象由2.5第三步登记，完整数学仍在正文；原graph.json不是当前正式图，不从旧图或旧manifest自动准入。

## 工作顺序

对象内部承重链 → 同子档对象族（3A）→ 同存档跨批/跨子档（3B）→ 有明确数学映射的跨档（3C）→ lead统一三级投影（3D）。内层先完成就继续向外，不让文件夹边界截断数学；不按边数、连通率或图外观完成。没有已知关系的对象允许孤立，比较范围和理由要准确。

lead发布任务，各Boss恢复本人未完后claim-next；内部代理各写独立边与收据。核心object_ids及输出路径排他，read_object_ids共享只读，公共定义不阻塞并行。同批新发现已登记依赖，用map read-add TASK --object-ids ID...补共享读取和pin后继续。独立批次先checkpoint确认pushed即可done，不等总registry集成。当前任务和lead在research/operations/map-v2；公屏wcg/board-map-v2。阶段任务的真实命令读完整Boss词。

## 什么值得成为超边

一条有用边回答：什么结论，哪几个事实必须同时用，各提供什么，哪些模型/量词/条件必须保留，为什么成立，依据在哪里，研究者怎样调用。共同定义与符号放条件/引用，不自动形成遍连全档的hub；目录、同名、共现、相似度和引用只提供发现线索。不能解释新增数学作用就不造边。

- all联合前提保在一条超边中；两个独立证明是两份替代支持。
- 推导、反驳、特例、迁移、等价与启发/来源/实现/有限检查分别表达。
- 跨模型关系写明映射与保留/丢失条件；反驳针对精确被否命题。
- accepted有具体作者审读、证据及当前绑定；proposed保未付义务，rejected保失败理由。状态和hash不自动证明数学。

字段使用JSON的edge_id、kind/status、source_ids/target_ids、premises_mode:all、relation_mode、conditions、roles、explanation、scope、evidence。绑定由research edge-bind计算，schema及完整例子见IMPLEMENTATION。不再使用旧Markdown关系模板/endpoint_hashes作为v2接口。

## 交付与研究使用

覆盖记录逐对象写当前pin、比较范围、理由和linked/isolated-after-review/needs-decision。明确数学open或proposed联系可以保留；最后要解决的是身份/版本/交付不明，不是强迫证明所有候选。lead用map collect查看完成批，sync后map assemble保留既有边并合入独立边、coverage和待实写的integration草稿；边status不自动提升。lead持续整合跨批、跨子档、跨档，完成map/coverage.json、map/integration.json后唯一生成三级graph-v2.json；边正文只维护一份。

研究者通过research search/show/context按需读完整知识。导航相邻不等于推导；调用一条证明支持要取齐全部共同前提、条件、证据和缺口，替代支持不混成一份ALL。局部对象变化定向重判，过期支持不等于结论全假。候选发现提示与作者实现依据见[UPSTREAM_ADAPTATION](../research/UPSTREAM_ADAPTATION.md)。
