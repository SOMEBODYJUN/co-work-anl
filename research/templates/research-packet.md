> 当前研究系统暂停从头设计。以下仅说明既有数学输入与恢复格式，不启动新协作公屏；peers的活动及legacy公屏入口均为空。

# 研究输入

普通研究用 `work.py research init RUN --spec <路径> --mode open` 生成一份 full packet。明确对照用 comparison 生成 obstacle/full；已有RUN恢复数学与原输入，普通派工按现行设计判断，对照保隔离。两种模式用同一spec。

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

问题及定义包含完整的域、目标量词与约束，引用可用section指定标题。obstacles只选有用失败边界。archives内原题以路径最深所属档为准，显式scope不一致会拒绝；若原题暂在workspaces，在spec加 `"collaboration_scope":"archives/ARCHIVE/subarchives/SUBARCHIVE"`（可父档或更深子档），随packet保存，不从跨档定义或clone配置猜。workspace精确同题的旧scope分歧仍以scope_conflicts列出供核对，但公屏状态统一为retired，不自动裁决或改写旧声明。

原题或定义尚无准确正文时，可先按完整原意写到`research/workspaces/<RUN>/problem.md`、`definitions.md`再引用。有相关既有成果才填写其真实seed_ids；没有时用`"seed_ids":[]`，即使尚无registry也可init，研究者从原题开始，可按需查后续证据。此时保留full检索能力，但初始packet没有引入任何成果；后续实际取用的相关结果记进研究笔记，不悄改原packet。指定edge_ids时须同时给相关seed，以准确保留所选证明分支。

需要定向取用时可在 spec 加 `edge_ids` 选择 accepted 正向支持的替代分支，或加 `edge_statuses`、`relation_kinds` 选择研究线索。`hops` 默认 0，仅控制额外导航，不截断已选逻辑支持的全部前提。full context 中各端点保留模型、量词、假设、状态与 objections，关系保留完整 conditions、scope、解释和证据定位；正文按需读取。

obstacle packet 给原题、定义、障碍与自由研究任务。full packet 另给登记检索入口及相关超边，Solver 按需展开完整共同前提、条件和证据。不同支持分支保持 OR，单条逻辑边前提保持 ALL；proposed/refuted/rejected/objections 分别按真实语义理解。

Main用真实平台创建/接续研究者。长线线路保历史并followup；临时Reader/独立挑战以当前精确请求为目标，交清发起者与回送对象。保存真实profile、agent_id、笔记、反馈和下一步；恢复保原packet及版本差异，不改写旧packet。packet不代表已启动模型或结论成立。

普通open的init/resume及research peers仍能定位已保存RUN和数学断点，返回status=retired及空公屏入口，不创建、迁移或重建合作页。旧packet不改；研究Agent的下一版输入和协作方式待超边收尾后设计。

open的worker默认gpt-6.1-sol / ultra / fork_turns=none，用户另指定照办。save记录真实配置，长线用稳定线路ID、临时请求用独立请求ID。给取证者精确接口和回送对象；完整材料留文件。
