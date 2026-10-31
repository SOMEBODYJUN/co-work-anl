# 全仓、存档和子存档超图

## 已复用的开源格式

已实际克隆并复用 math-agent 的NodeRecord/HyperEdgeRecord/GraphSnapshot及MATEK的Markdown平坦frontmatter编解码；源码、固定提交、许可证和改动范围见 [上游记录](../tools/vendor/UPSTREAM.md)。只复用知识格式，不部署它们的模型/形式化/持续审查运行时。

节点是具体数学对象或命题版本；文件是正文地址，不能因放在同一文件就把所有结论捆为一个依赖。多前提共同蕴含一个结论是一条多源超边；两个对象的关系是其特例。

第二阶段写对象，第三阶段逐边建立解释：

- source_ids与target_ids：参与对象的稳定ID，可多源多目标。
- kind：implies、refutes、specializes、transfers、motivates、derived_from、implements、checks等，按真实语义扩充。
- explanation：为什么能联系、各对象起什么作用；正文详细论证。
- conditions：必须同时保留的共同条件、适用模型及不覆盖范围。
- evidence：可定位到正文段落、证明或冻结来源的依据；仅关键词相似不够。
- status与reviewed_by：proposed/accepted/rejected和实际斟酌者；accepted是关系审读声明，不是形式化或外审认证。

边的Markdown放本层map/edges/，格式见 [边模板](../cleanup/templates/联系--关系.md)。保留未知或孤立对象是允许的。不能按人数/目录顺序自动连推论边，不因同父归档就生成因果边。

## 三层投影

全仓graph.json包含所有已整理对象与已接受关系；各存档与子存档map/graph.json为同一稳定ID体系的局部投影，包含必要的边界对象，跨档边保留完整共同前提。详细正文仍留各自存档。当前graph为draft-scaffold，只有问题身份种子，没有已接受数学边。

```sh
python3 work.py map check
python3 work.py map build --draft
python3 work.py map build
```

最后一条为第三阶段正式生成：源清点尚有未完成语义处置时会拒绝；--draft明确保留待建状态。检查结构、路径和字段不证明边的数学正确性。

以后正式入库不只复制Markdown：Boss或其一个subagent需看对象与既有节点的关系，补充分层图或解释为何暂时孤立；不强制另设常驻审核角色。
