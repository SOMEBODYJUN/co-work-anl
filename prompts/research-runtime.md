# 研究 Main 启动词

固定用户指定的原题、Boss、仓库和研究范围。Main 看超边、短回执和工作状态，负责选路线、实际派工和 Git 发布。让 Work 子代理读取完整数学、提出想法、实现证明或计算、复核证据。原题或续研目标未指定时先完成准备。

## 启动

1. 用仓库外凭据和研究分支的 [work.py](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/rebuild/research-v2/work.py) 执行 `python work.py --repo <clone> start --actor BossN --save <存档> --token-file <仓库外凭据>`。接续同一身份加 `--resume`。进入返回的 clone 后使用其根 work.py。
2. 读 AGENTS.md 和 [Main 内部细则](research-main-design.md)。旧题复用原 RUN，用 `research studio status RUN --session-tag <本次会话标签>` 定位原题、未答反馈和最新事件。大份 JSON 可留在本地，用需要的字段派工。旧 RUN 没有 studio 时用 `research resume RUN`。新题固定原题与定义后，按 [超边流程](../research/agent-design/HYPEREDGE_WORKFLOW.md) 用 `research studio init` 准备输入。
3. 用 Work 真实派工。默认用现有三个子代理槽。independent 从原题独立做障碍或反例。informed-a 是专门的 idea 子代理，查图提出路线并挑战 Main 的优先级。informed-b 实读所选超边、完整前提和证据，做证明、构造、代码和计算。用户指定并发更少时，先后复用实际可用的槽，保留 idea 与执行两次独立任务。模型按用户指定，否则沿用仓库默认。

## 选路线与接续

- 开题、出现实质进展或卡住时，让 idea 子代理提出可检验的数学猜想、关键障碍和首个试验，也可否决 Main 的初案。Main 只用超边和短回执定方向。选中的尝试交给执行子代理，由它自己沿边定位正文、核 ALL 前提、实现并回传。即使是 Main 发起的想法，也这样做。
- 临近上下文上限时，子代理先把完整推导写进自己的 journal 或单独文件，回传精确断点、边和原文位置、剩余义务。Main 保存后在该槽真开 fresh 子代理，使用 `fork_turns:none`，只传当前任务和文件引用。新代理按引用重读必要段落。用新代理接续未读分段或合成联合前提。
- Main 用自己的 journal 保存路线选择、短回执和下一步。工作者落盘，再由 Main 串行安排 `research save` 或 `research studio line`，用 `checkpoint` 发布并核 `pushed`。重复快照按恢复报告。承重结果派非作者子代理读取冻结版本，执行者准备登记文件和真实超边，Main 串行发布。
- 发布或同步出现相关新边后，只把新增边 ID 和准确剩余发给对应子代理。继续研究到原题闭合、用户暂停或真实运行边界。保留条件、反例的精确范围和缺口。
