# 从已登记数学建立可调用的超边

使用[第三阶段完整Boss词](../prompts/03-map.md)；字段和收据见[IMPLEMENTATION](../research/IMPLEMENTATION.md)。正文保存完整数学，registry定位对象，超边解释真实关系，graph-v2只是可重建投影。正式构图以已发布登记为输入，不用旧图、文件名或来源done充当数学关系。

## 按数学联系从内到外

3A先做对象内部和同子档承重数学；3B补同档跨包或跨子档；3C比较有明确对象、映射和问题的跨档线索；3D边做边整合。常用定义可以共享读。

worker从证明的输入输出、共同结构、条件差异、反例目标和未付义务提出具体比较问题，实读后才定关系。任一Boss可据此继续3B/3C或补登记。

Boss和内部处理者都做实质数学。本人未完任务优先，成熟即保存交付，接下一包；任一Boss都能集成。完成以实际比较、覆盖和已推成果为准。

## 共享读取，独立写入

任务在research/operations/map-v2/tasks；公屏wcg/board-map-v2只交流真实成果与依赖，不代替所有权。核心object_ids负责本批覆盖，read_object_ids是共享依赖，input_pins覆盖两者，write_paths只保留实际输出。不同批次可同时读共同定义；增加已登记只读端点用read-add，不重派整批。

```sh
python work.py map list
python work.py map list --owner self
python work.py map claim-next --count 6
python work.py map read-add TASK --object-ids 已登记依赖ID
```

任一已登记Boss按完整Boss词用map-draft→plan发布实际比较。先接既有队列；没有合适批时可按当前子档起草。任务与结果确认pushed再交付；响应未知核原request_id。过期批交接重派或定向替代。

## 一条边保住什么

每条边保稳定ID、source_ids、target_ids、premises_mode:all、kind/status/relation_mode、每个端点的roles、共同conditions、explanation、scope及准确evidence。

- implies保全部承重前提；{A,B}⇒C是一条ALL边。不同独立证明是替代支持，分别写边。
- equivalent_to声明ALL(source_ids)⇔ALL(target_ids)，解释及证据必须支持两个方向；反向使用也保整组必要前提。
- refutes指向被否定的精确陈述；多个目标须逐项确有否定依据。辅助桥失败不指向原题。
- specializes/transfers保模型映射、量词、条件及丢失内容。引用、启发、实现和有限检查用语境关系，不作证明。

作者实读后才accepted，先写最终status、reviewed_by/review_note等语义字段，再edge-bind取得三项绑定，随后edge-check。绑定检查不证明数学正确；条件、解释、正文或证据变化只复核受影响关系。不另要求每边再过一个固定审批者。

前提尚未证成而条件推导已完整，可为accepted且relation_mode:conditional，未付前提仍须保留；推导自身缺桥才proposed，不能以accepted直接提升终点真值。

```sh
python work.py research edge-bind map/edges/实际边.json
python work.py research edge-check map/edges/实际边.json
python work.py checkpoint map/edges/实际边.json map/receipts/TASK.json -m '具体数学关系与范围'
python work.py map done TASK --receipt-file map/receipts/TASK.json
```

edge-check独立校验交付边，canonical边清单尚未更新也能交付。done核当前批次的已推送资产与覆盖，不让无关旧边拖住该批。linked列真实accepted incident边；无已知成立联系但比较范围清楚时可isolated-after-review。明确open数学或proposed桥可以保留，needs-decision只表示尚未辨明身份、版本、来源或交付去向。

认真比较后零边时，以现有coverage的comparison_scope/reason交清候选、范围和数学理由，收据可用assets:[]，不另造边或说明文件；完整边及零边收据见IMPLEMENTATION。登记阶段的batch_file资产要求不变。

## 汇总与最终交付

```sh
python work.py map collect
python work.py sync
python work.py map assemble
```

collect读取当前已done批次，任一Boss可assemble合入registry.edge_files并生成coverage/integration草稿。保留旧数学说明，重核受影响范围。待修旧批单列，不耽误其他有效交付。

最终research check --final与research build --final要求登记闭合、逐对象当前覆盖、各档/子档及跨档比较说明准确；数学开放问题可继续开放。build回执projections列出全仓、存档及子档输出，跨边界超边保全部端点。将这些实际生成路径连同registry、coverage、integration显式checkpoint确认pushed；repository-cleanup默认范围不含archives内投影，不能漏交，也不整档提交archives。

研究Main按search→show→context取完整正文和支持，ALL前提闭包不受导航hops截断，替代证明、未付前提、反驳和研究线索分别保留。图上可达、边数量和工具通过都不代替数学论证。
