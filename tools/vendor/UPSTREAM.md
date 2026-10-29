# 固定上游与复用范围

- math-agent：https://github.com/Ephemeral6/math-agent ，commit 3a161e1f6ced822c340b9e23c0ada2a4b82dbdbe，Apache-2.0。原文件mathagent/epistemic_graph/model.py原样复制到mathagent/model.py；保留其LICENSE。使用NodeRecord、HyperEdgeRecord、GraphSnapshot和序列化格式。没有复制其验证门、代理调度或Lean环境。
- MATEK：https://github.com/PhillipKerger/matek-theorem-agent ，commit 1de478c12f34fc1adea32bbc3f0c5aadadfd6ca5，MIT。从src/matek_theorem_agent/knowledge_graph/markdown.py提取GraphMarkdownError、平坦frontmatter解析及输出函数，去掉与其Pydantic模型/运行时相关的导入；保留LICENSE。数学对象仍以描述性Markdown为正文。
- AI4Algebra亦已克隆并读实际文件，commit 1ef0f16b8b876aa410349860b9c2ab25da9c4e51；该版本主要为Lean声明，未把README宣称的完整代理实现冒充可用代码，因此未引入本树。

适配位于tools/maps.py：使用上游记录格式，增加关系解释、条件、证据和层级投影校验。没有声称整套上游Agent已部署，也没有“最高效”排名结论。此处不安装任何模型CLI或形式化环境。
