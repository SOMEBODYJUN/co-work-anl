# 研究输入：obstacle / full

实际 packet 由 `work.py research packet` 或 `research init` 从同一 spec 生成；不手工维护另一套 blind/boundary 协议。

spec 的最小结构：

```json
{
  "problem_id": "USER-PROBLEM-ID",
  "problem": {"path": "archives/ARCHIVE/state/问题/精确原题--问题.md", "sha256": "实际文件SHA256"},
  "definitions": [{"path": "archives/ARCHIVE/state/定义/模型--定义.md", "sha256": "实际文件SHA256"}],
  "obstacles": [],
  "seed_ids": ["实际登记object_id"]
}
```

问题及定义包含完整的域、目标量词与约束，引用可用 `section` 指定精确标题。obstacles 只选有用的已知失败边界；不把全仓成果塞进该字段。

原题或定义尚无准确正文时，可先按完整原意写到`research/workspaces/<RUN>/problem.md`、`definitions.md`再引用。有相关既有成果才填写其真实seed_ids；没有时用`"seed_ids":[]`，即使尚无registry也可init，两个full槽从空成果context研究原题，不要求先登记新题或填无关对象。此时保留full检索能力，但初始packet没有引入任何成果；后续实际取用的相关结果记进研究笔记，不悄改原packet。指定edge_ids时须同时给相关seed，以准确保留所选证明分支。

需要定向取用时可在 spec 加 `edge_ids` 选择 accepted 正向支持的替代分支，或加 `edge_statuses`、`relation_kinds` 选择研究线索。`hops` 默认 0，仅控制额外导航，不截断已选逻辑支持的全部前提。full context 中各端点保留模型、量词、假设、状态与 objections，关系保留完整 conditions、scope、解释和证据定位；正文按需读取。

obstacle packet 给原题、定义、障碍与自由研究任务。full packet 另给登记检索入口及相关超边，Solver 按需展开完整共同前提、条件和证据。不同支持分支保持 OR，单条逻辑边前提保持 ALL；proposed/refuted/rejected/objections 分别按真实语义理解。

Main 用真实平台工具创建/接续 Solver。保存实际 profile、agent_id、完整数学笔记、具体反馈与下一动作；恢复时保留原 packet 和笔记，并明确当前登记与初始版本的差异。packet 不代表模型已启动，也不代表数学结论已成立。
