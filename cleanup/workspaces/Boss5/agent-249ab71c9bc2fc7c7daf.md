---
id: "weighted-congestion/historical-runbook-routing-20261031"
kind: "review"
type_tag: "审查"
title: "历史拥塞运行手册与新题路由处置"
status: "retained-historical-operational-context"
truth_status: "historical-routing-record-only"
review_level: "full-source-read-cross-archive-comparison"
summary: "完整读取旧 weighted_congestion_frontier/RUNBOOK.md；它是从 customer-attraction transition 包切换到 UM-TARGET-v1/unrelated-machines 时的运行与路由手册，不承载新的拥塞数学命题。原件应保全并标记为已被新版工作流取代的历史操作材料。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/RUNBOOK.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/RUNBOOK.md"
source_ids:
  - "249ab71c9bc2fc7c7daf"
blob: "a4f63523174a677e611d6dfa9e64183a4e8ae4fc"
source_sha256: "cedfd6d3639eda519a28895f319ebcae07f2aa31604294ca6cb5d7a42a69f9f7"
source_size: 2173
source_commits:
  - "68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup)"
  - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)"
---

# 实读范围

经 `clean show 249ab71c9bc2fc7c7daf` 完整读取 2173 字节 Markdown，并以 `clean list --full` 核对 blob、SHA-256、大小和两个冻结提交。两个提交给出相同内容指纹 `cedfd6d3639eda519a28895f319ebcae07f2aa31604294ca6cb5d7a42a69f9f7`；没有观察到该 RUNBOOK 在两版间的正文分歧。

`archives/customer-attraction/tools/evidence/history-transition-20261031/transition-manifest.json` 已将同一原路径列为 `superseded navigation or operating prompt; not a mathematical claim retirement`，并给出相同 SHA。该 manifest 是版本迁移证据，不能代替本源的语义阅读。

# 内容与准确范围

该 RUNBOOK 只有操作和路由信息，没有定义、定理、证明、反例数值或可独立复现的数学证书。其独有内容分为四组：

1. **当时的新题默认路由。** 文档把当前主攻标为 `UM-TARGET-v1`、存档 `unrelated-machines`，规定新对话使用新题 BOSS 提示词与新题 RUNBOOK；单一 `tools/work.py` 恢复后调用仓库内最新版 `checkpoint.py` 和 `board.py`。新未绑定 clone 默认绑定新题；已有 `shared` 或其他 save 不改绑，新旧题必须用独立 clone。
2. **发布/保存纪律。** 首次显式指定 save，后续复用绑定；默认 checkpoint 只追加个人桌面；显式 paths 会替换默认范围且必须列出本次全部成果；待推历史要全部检查并保留真实冲突两侧；只有远端确有提交的 `pushed` 状态才可报告“已保存”。这属于历史工程约束，不是数学事实。
3. **旧题接续语义。** 继续旧拥塞题必须显式选旧存档 `shared`，示例命令把旧题 actor 和仓库外 token 文件作为启动输入。旧题数学入口是当时的拥塞地图、`MODEL.md`、`CLAIMS.md`；文档明确 Cd/ln d 全类存在任务已经被后续线性全状态结果否定，旧冻结 Pro 包不能代表当前状态。该句是版本导航/状态指示，RUNBOOK 本身没有给出否定证明，应由已有拥塞 state/定理与审查对象承重。
4. **兼容协作程序。** 日常操作统一走 `work.py`；旧 `board.py` 事件无 save 时仍归 shared；`say/ack/view` 的无 save 兼容、pending/retry 的原消息 ID 与 save 保持、私聊视图分流及历史记录可读，都是程序路由说明。工程记录 `active_topic_routing_release.json` 与 `incremental_chat_release.json` 只作为操作版本证据，不能作为数学研究前置。

因此，本文档不能推出 `UM-TARGET-v1` 的算法、拥塞题的近似界或任何客户吸引结论；也不能把它的“Cd/ln d 已否定”一句话当作独立证明。它只证明历史切换时采用了怎样的存档、clone、消息和保存规则。

# 跨档案比较

- 旧三源审查 [历史旧题拥塞入口三源处置](../../../../weighted-congestion/state/审查/历史旧题拥塞入口三源处置--审查.md) 已完整处置同一历史目录的 `AGENTS.md`、`PROTOCOL.md`、`README.md`，并把旧题/新题身份边界、旧协作语义和旧数学入口分别归为历史保留。RUNBOOK 与该三源互补：它给出实际 start/save/checkpoint/board 路由，而不是旧题模型定义；不能把本源并入三源的原有 source_refs 而丢失独立指纹。
- `archives/customer-attraction/tools/evidence/history-transition-20261031/transition-manifest.json` 将本源和旧三源统一标作迁移期的 superseded navigation/operating prompt；这支持“历史保留、当前不执行”的处置，但不把四源合并为同一数学对象。
- 新版 `archives/unrelated-machines/tools/evidence/history-transition-research-20261031/REPOSITORY_GUIDE.md`、`research_README.md` 和 `ROADMAP.md` 已承接当前主攻、存档、证据和入口。它们明确当前使用结果分支和当前题目入口；旧 RUNBOOK 的 `shared`/旧程序兼容细节只作为历史迁移证据，不能覆盖新版 `work.py` 的 Boss/结果分支/clean claim-done 约束。
- `archives/weighted-congestion/README.md` 和 `state/审查/历史旧题拥塞入口三源处置--审查.md` 已把旧拥塞数学放入独立存档。关于 Cd/ln d 的否定、奇环/线性全状态族及其他结论，必须链接相应 `state/定理`、`state/反例`、`state/计算` 和审查文件；本 RUNBOOK 不新增这些对象。

# 独有内容去向与处置

建议将该源标记为 `retained`，并在 `archives/weighted-congestion/state/审查/历史拥塞运行手册与新题路由处置--审查.md`（或等价的稳定命名审查页）中保留本页要点，同时把原 2173 字节按原指纹复制到独立 evidence 目录，例如 `archives/weighted-congestion/tools/evidence/history-frontier-runbook-20261031/original/research/weighted_congestion_frontier/RUNBOOK.md`，附 manifest、来源提交和 SHA。不要把它标成 `duplicate`：虽然与新版/其他历史入口有路由重叠，但它独有“旧题显式 save=shared、兼容 board/pending/retry 及仅 pushed 才算保存”等迁移细节。也不要标为数学 `retired`：其操作主张已被新版流程取代，但历史事实和版本边界仍有接续价值。

应在正式审查页中明确：

- `status=retained-historical-operational-context`；
- `truth_status=historical-routing-record-only`；
- 旧命令示例只供历史复核，当前 Boss5 清洗继续服从结果分支 `rebuild/research-v2`、新版根 `work.py`、固定 actor、checkpoint pushed 和逐源 done；
- “Cd/ln d 已否定”仅作指向已有数学对象的状态导航，不在本页重复证明；
- 不把当前 `UM-TARGET-v1` OPEN/否定路线、旧拥塞近似边界或协作脚本测试结果混成一个命题。

# 接续与缺口

第三阶段如建立关系边，适合的边类型是“历史迁移入口 → 当前 unrelated-machines 运行指南”和“历史旧题 RUNBOOK → weighted-congestion 历史上下文审查”，不应建立“RUNBOOK → 定理”的数学依赖。若需要复现历史协作版本，先读取本源引用的工程记录并核对其原提交；若需要复现拥塞数学，改读对应冻结源和已清洗的 state/evidence 对象。当前没有需要由本源单独补做的数学实验或证明。
