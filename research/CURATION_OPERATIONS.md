# 2.5.1/2 操作手册

第一步只分类、标号、建立目录。当前完整入口是[4,619份编号分类表](../curation/catalogs/20261103-classification-only/INDEX.md)，旧run保留冻结阅读记录。此前第一步649份退出与641页链接改动已精确撤销，所有原页面恢复，证据附件也保留。旧actions是历史，不是现行任务。第二步尚未开始；不清空旧公屏，也不创建新公屏。

## 第一步：分类目录，零原件处理

新运行才初始化，Boss编号由用户明确给出；既有冻结run不要覆盖：

```sh
python3 work.py triage init --run 新运行ID --actor Boss编号 --lanes 6
python3 work.py triage next --run 新运行ID --lane 1 --limit 20 --byte-limit 100000
python3 work.py triage ingest --run 新运行ID --batch 实际batch_id --records 实际record_file
python3 work.py triage status --run 新运行ID
python3 work.py triage export --run 新运行ID
```

程序生成路径、SHA和材料编号；代理全文快速定性，只填类别、简短理由、定位、后续建议。七类判据见[分类规格](PHASE25_TRIAGE.md)。分类不是数学真值审查，也不是准入；数字多不等于需要蒸馏，裸计算不因为PASS就成为数学。

`plan-clean`和`apply-clean`已从第一步入口禁用。第一步不得删除、移附件、合并、抽取、改写或修链。`delete/attach`等route只表示第二步建议。后台记录不进入数学正文。

本次跨快照目录生成器为`tools/classification_catalog.py`：只接受精确匹配路径/SHA的已读记录和人工更正，不自动分类；首批编号冻结，新增路径追加。实际生成命令如下，现有输出已完成，不应覆盖：

```sh
python3 tools/classification_catalog.py --source-runs 20261103-boss6-triage 20261103-boss6-current --out curation/catalogs/20261103-classification-only --corrections curation/classification-only-correction/classification-corrections.json
```

材料清单、数学子集、证据/非数学子集、第二步候选及按档目录均有完整编号。每条含原路径、SHA、类别、具体理由、正文定位和建议去向。旧run的同路径版本保存在`source_versions`中；当前链接指向已恢复的原件。目录行号不充当数学对象ID或超边端点。

## 第二步：协作程序v2

完整词见[Boss](../prompts/02.5-2-distill.md)和[worker](../prompts/02.5-worker.md)。新clone仍用curator/20261103-boss6-current和wcg/board-curation-25；已有同身份clone运行sync更新，不换号、不重做分类。先由用户指定一名协调Boss处理差量分组和纯包装批次，其余Boss直接整理数学。旧run中的数量是快照，实时看status。

```sh
python3 work.py sync
python3 work.py curation-task status --run 20261103-boss6-current
python3 work.py curation-task list --run 20261103-boss6-current --owner self --limit 0
python3 work.py curation-task list --run 20261103-boss6-current --available --limit 12
python3 work.py curation-task show --run 20261103-boss6-current 实际task_id
```

list默认最多20条短行；--full保留原完整记录，--limit 0表示全量。status输出聚合、活跃任务及未分组差量数；status --full才输出差量路径。新事务在任务里记录updated_at，无需额外打卡写入；旧记录没有该字段时不伪造活动时间。

batch接收JSON数组，每项包含task_id、operation和该操作参数。支持claim（可同时附write_paths）、extend（write_paths）、finish（assets、reason，可附reuse_paths）、旧submit/complete/handoff。一次正常推送提交一批互不冲突的变更；逐项冲突会列为conflict，其它项可以成功，必须检查results。

```json
[
  {"task_id":"实际A","operation":"claim"},
  {"task_id":"实际B","operation":"claim","write_paths":["实际独占输出路径"]}
]
```

```sh
python3 work.py curation-task batch --run 20261103-boss6-current --record-file 实际批次.json
```

先claim成功再派实质工作；sync一次取得新快照。编辑前预留路径，不锁整个存档。复用原有数学无需制造空修改或占写锁，finish中以reuse_paths显式列出真正原字节复用的正式数学。

```json
[
  {
    "task_id":"实际A",
    "operation":"finish",
    "assets":[{"path":"现行正式数学路径","sha256":"当前SHA256"}],
    "reuse_paths":["其中原样复用的正式数学路径"],
    "reason":"具体结论、机制、修复或准确缺口"
  }
]
```

编辑产物先checkpoint确认pushed，再批量finish；finish一次完成submit+complete，其它旧命令仍兼容。assets保持path/SHA两字段，复用信息另记reused_paths。至少一份正式数学仍是数学交付要求，纯包装批次不伪装为数学完成。

响应未知时，意图保存在本clone的Git缓存中，使用相同request_id继续：

```sh
python3 work.py curation-task retry --run 20261103-boss6-current --request-id 实际ID
```

普通ref竞争会自动读取最新快照并带抖动重试。任务事务只展开本run元数据和当前所需输入，Git索引保留完整原树；不再为每次claim展开全部正文。成果广播复用对象缓存，公屏推送重试不重复验证同一资产；它的延迟不阻塞数学补位。

暂停前先保全实际草稿及逐群下一步，再一次交接本人未完任务：

```sh
python3 work.py curation-task handoff-all --run 20261103-boss6-current --reason '真实原因' --draft-note '实际逐群草稿/下一步表，以及共享状态'
```

handoff-all不释放他人或已完成任务。不得以表中claimed假设进程仍在跑；也不自行冒用他人身份夺取草稿。协调者明确接续分工，普通Boss继续可领数学。

新公屏已存在就复用，默认读最近20条；首次初始化由协调者确认后board-init，不清空原公屏。原阶段二clean命令不处理这些对象群。本步不登记最终节点、不写超边，不改另一侧后续方案。
