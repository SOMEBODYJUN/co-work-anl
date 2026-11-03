# 数学关系图：只读取明确准入的数学对象

> 设计状态：以下为上一版工具/提示词原型。用户已将2.5分成材料定性、对象群整理、重新登记；本轮只设计前两步。2.5第三步、第三阶段超边结构及数学研究Agent由用户与另一AI另定。本文件的manifest、一页一ID、模型配置、超边字段与启动流程尚不作为最终决定，暂不按此启动第三阶段。新边界见[CURATION](../research/CURATION.md)。

图服务于研究者理解命题、调用证明、检查反例和识别缺口。文件存在、来源done、审计PASS或元数据齐全都不构成数学对象准入。纯工作区身份与执行履历不成为节点。必要代码、输入、证明证书和输出由数学对象引用，不各自包装成数学命题。

第二阶段半先按[准入执行协议](../prompts/02.5-research.md)保护成熟数学、删除非数学包装、修复条件和纠错、拆分不同真值/依赖的结论。第三阶段只读取 `research/curation/manifest.json` 明确放行且内容指纹仍一致的数学正文；[程序契约](../research/CURATION.md)说明部分与最终完成的区别。

## 节点和证据

节点是一个有明确模型、量词和状态的数学对象。文件是正文地址；同一页的独立结论若有不同依赖或真值，先拆成独立稳定ID。`bundle-pending-split` 仅是部分阶段的阅读容器，导出状态为 `unresolved-bundle`，不能用作已接受逻辑边端点，不能通过2.5最终验收。开放问题、精确猜想和具体失败机制可以保留，不能因未证而删除，也不能当已证前提。

本地证据须为准入数学正文或有数学owner的附件，并绑定当前内容指纹。`source:<完整commit>:<路径>#段落` 可引用固定清单中的冻结证据；它不自动成为逻辑前提。程序不会判断一个证据是否足够承担证明。

## 超边契约

联合前提 `A1,...,Ak` 到结论 `B` 保留为一条多源超边，不能拆成每个前提单独足够的二元边。边说明每个对象提供什么、共同条件/变量对应、合法推理或精确反驳范围以及证据。目录相邻、同名、引用或共有输入不是逻辑依赖。

- `source_ids`、`target_ids`：稳定命题身份。
- `kind`：逻辑类 `implies/refutes/specializes/transfers/derived_from/equivalent_to`；其它已登记类 `motivates/cites/sourced_from/implements/checks/corrects/supersedes`。新类型在语义明确前保持proposed，不能靠改拼写避开逻辑限制。
- `explanation`、`conditions`、正文：为何能联系、各前提作用、适用域及缺失条件。
- `evidence`：精确证明、反例或附件位置。
- `status`、`reviewed_by`：proposed/accepted/rejected和实际关系审读者。accepted只声明关系已经审读，不为端点自动赋真值。
- `relation_mode: conditional`：逻辑边有未证、已否或条件性前提时必须显式声明；即使结论另有独立证明，也不能把本边冒作无条件证明。
- `endpoint_hashes`、`evidence_hashes`、`reviewed_content_sha256`：端点、证据及关系自身的内容绑定。任一改变都须重新判断相关关系，不能静默沿用旧审读。

字段模板见[关系模板](../cleanup/templates/联系--关系.md)。这些约束检查声明、路径和版本，不提供形式化正确性或独立数学认证。

## 命令和三层投影

```sh
python3 work.py curate scan
python3 work.py curate freeze --manifest-out research/curation/manifest.json
python3 work.py curate check
python3 work.py curate check --final
python3 work.py map check --structural
python3 work.py map check
python3 work.py map fingerprints archives/真实档/map/edges/真实关系.md
python3 work.py map impact 实际变化的对象ID
python3 work.py map build --draft
python3 work.py map build
```

`freeze` 建立原文基线和全pending骨架，不裁定数学。`--structural` 仅诊断当前正式候选格式，排除历史证据副本；默认 `map check` 检查准入对象与关系。`fingerprints` 只计算版本值，不能替代关系审读或把status升为accepted。`impact` 生成待复核范围，不宣布所有后继命题为假，替代证明可能仍成立。

草图只呈现已准入区域，状态为 `draft-curated-partial`。正式生成同时要求来源阶段完成、2.5全量准确处置和关系检查通过。子存档、父存档、全仓共享对象和关系身份，跨边界保留联合前提；证据/工作区里的历史map不生成投影。

既有 `graph.json` 仍是阶段一身份种子，不表示已执行本轮2.5或已建正式超图。只复用上游NodeRecord/HyperEdgeRecord/GraphSnapshot容器与Markdown格式，[上游记录](../tools/vendor/UPSTREAM.md)没有声称部署其验证或Agent运行时。
