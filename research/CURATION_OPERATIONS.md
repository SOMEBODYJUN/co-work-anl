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

## 第二步启用前

现有`tools/curation_tasks.py`和`work.py curation-task`已实现对象群认领、写入互斥、提交与交接，不需要另造平台或另一个启动器。数学任务使用`20261103-boss6-current`运行域；其旧分类snapshot保持不变，当前分类以新完整目录为准。144组旧计划与本轮路由变化的对照另见该run的TASKS.md；新增或取消的候选由协调Boss按数学联系补齐/调整任务，再领取。不得机械按文件一份建一组。

纯非数学/证据处置不是数学蒸馏交付。若第二步另行明确执行这类处理，先由协调Boss定范围、去向、现行SHA和引用，按小批串行组织；当前数学task submit要求正式数学资产，不能伪造正文来满足它。不凭第一步的类别或route自动执行。

## 第二步启动模板

先下载结果分支**最新根work.py**，旧上传启动器不认识新参数。由用户明确给Boss编号；N是占位，不能随机选。run和程序须已推送。用独立clone，不改绑旧cleaner clone：

```sh
python3 work.py --repo /明确的新目录/p25-bossN start \
  --actor BossN --role curator --save repository-cleanup \
  --branch rebuild/research-v2 --curation-run 20261103-boss6-current \
  --board-branch wcg/board-curation-25 --token-file /仓库外/有效凭据.txt
python3 work.py --repo /明确的目录/p25-bossN doctor
```

`--curation-run`将工作区放到`curation/workspaces/<run>/<Boss>`，身份注册到`curation/runs/<run>/people/<Boss>.json`；不复用cleanup/workspaces和旧来源people。save暂沿用repository-cleanup作程序兼容，公屏分支和运行域独立，不另建伪数学存档。既有同clone继续复用已绑定run；换run或角色用独立clone。只有明确同对话恢复才使用resume/adopt。

协调Boss在激活第二步时运行一次`board-init`并读回确认，不复制旧历史。公屏按对象群task-id发成果、争议和阻塞；result须带实际pushed资产，不发布四千条打卡。未来研究Agent公屏/运行框架由后续设计，临时公屏不充当数学知识。

## 对象群任务命令

第二步任务须从已定性候选按真实数学联系组建；没有自动按标题生成accepted关系。Boss以[程序契约](PHASE25_PROGRAM.md)给的定义字段写任务JSON（可数组），先本地plan再checkpoint。发布后才能认领：

```sh
python3 work.py curation-task plan --run 20261103-boss6-current --record-file 仓库内任务定义.json
python3 work.py checkpoint curation/runs/20261103-boss6-current/tasks -m '发布对象群任务'
python3 work.py curation-task list --run 20261103-boss6-current
python3 work.py curation-task show --run 20261103-boss6-current 实际task_id
python3 work.py curation-task claim --run 20261103-boss6-current 实际task_id
```

每群领取前先sync并读取实际任务状态，领取后再sync并核对输入SHA。当前list/show查看本clone快照，不能把未同步的列表当远端最新占用。Git同步/整合时由Boss组织暂停相关写入并保住草稿。

已发布任务先只预留各自`curation/workspaces/<run>/groups/<task>`，不预设重写哪篇数学。领取后先找现有充分正文，再用`extend`预留实际要改写、删除或复用交付的正式路径及附件；收到pushed后才能写。paths JSON是仓库相对路径数组，不含凭据：

```sh
python3 work.py curation-task extend --run 20261103-boss6-current 实际task_id --paths-file 实际paths.json
```

别一口气锁整个存档。若不同群要写同一权威页，Boss先合并/串行其写入；只读可共享。混合页被多群作输入时，在各群独有数学已迁出前不整页删除。输入SHA有变化应定向重判受影响群，不重扫全仓、不机械改SHA继承旧判断。

任务认领采用最新远端单任务事务、输入SHA与交叉写入路径检查、正常push和request_id读回；不以公屏说负责代替锁，不预领大量未来任务。所有代理可跨范围阅读，写入按任务互斥；同clone Git由Boss串行。

产物先checkpoint并收到pushed。assets JSON是`[{"path":"实际正文或附件路径","sha256":"当前实际SHA256"}]`，路径必须在任务写入范围。至少一项资产须为现行正式数学；仅工作区草稿、附件或处置摘要会被拒绝。复用已有充分正文时，也须预留其路径并引用它的现行字节，明确本群数学如何被覆盖；不必重写或重证好内容。再提交并说明实质完成出口：

```sh
python3 work.py curation-task submit --run 20261103-boss6-current 实际task_id --assets-file 实际assets.json
python3 work.py curation-task complete --run 20261103-boss6-current 实际task_id --reason '实际数学增量、保全或具体缺口'
python3 work.py curation-task handoff --run 20261103-boss6-current 实际task_id --reason '真实运行边界' --draft-note '草稿路径以及是否共享'
```

claim、产物pushed、submitted与completed分别确认。submitted只接受远端已存在的同版产物；仅本地留在工作区和交接记录。completed是本步骤编辑交付，不是证明新定理或最终图准入。只读输入依赖在提交前已变动时，程序拒绝提交，须按新内容重新判断；属于本任务可写范围的输入允许以本次产物替换。内容变更必须重新判断，不机械刷新SHA继承旧完成。只有owner和本run协调Boss可完成已提交任务；handoff只释放本人未完任务。原`clean handoff`不释放这些任务。

## 暂停与退役

凭据只认证，不入消息、正文、remote或提交。认证失败停止同凭据重试和新认领；本地成果用checkpoint --local-only保存，明确未共享。

第一步暂停收好已回与未回批次、保留剩余lane和位置；第二步暂停交接/释放本人未完任务，写实际原因、草稿位置、共享状态与下一步。没有后台继续承诺。

阶段二旧设施在实际交接后退役；本轮临时工作区和公屏在后续交接完成后退役。先保全被数学/必要证据引用的内容，再清当前树，Git历史留回滚。2.5第三步和最终超边schema不在本手册确定。
