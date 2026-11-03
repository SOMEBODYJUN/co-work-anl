# 2.5.1/2 操作手册

材料程序和对象群任务程序已实现。当前第一步运行 `20261103-boss6-triage`，Boss6与六名gpt-6-sol/high内部代理持续分类；初始快照4,608份。新公屏尚未创建，第一步只用内部批次，不需要发消息。旧阶段二公屏和来源认领不混用、不清空。

## 第一步实际命令

本轮已初始化，**不要再次init覆盖**。新运行才执行第一条：

```sh
python3 work.py triage init --run 明确的新运行ID --actor Boss编号 --lanes 6
python3 work.py triage next --run 20261103-boss6-triage --lane 1 --limit 30 --byte-limit 150000
python3 work.py triage ingest --run 20261103-boss6-triage --batch 实际batch_id --records 实际record_file
python3 work.py triage status --run 20261103-boss6-triage
python3 work.py triage export --run 20261103-boss6-triage
```

next返回本批路径、SHA和记录文件；内部代理自己实读、填六字段，再ingest。程序只检查覆盖、重复、类型/路由和版本，不替代内容判断。普通正文读全，机械巨大数据可结构投影，但全篇章节和数学解释不能漏。长文按实际阅读量减小批次，不以文件数追速度。

Boss单独收回六lane，不每材料发远端claim。明显数学页只作内容/结构定性，不逐句消化长证明；X/E删除或移出候选仍须覆盖全篇防藏数学。原件在本轮阅读中保持固定；明确纯非数学页可在已收回且无活跃读取后清理。数学/必要证据先保全，再删混合包装。分类记录与清理动作分开：动作在actions/记原SHA、去向、理由、是否落实与共享状态。SHA变化只定向重读变化材料，不能按旧SHA覆盖。

## 全量定性后的清理

全部材料已定性后，Boss先导出并检查清理计划，再明确应用：

```sh
python3 work.py triage plan-clean --run 20261103-boss6-triage
python3 work.py triage apply-clean --run 20261103-boss6-triage
python3 work.py triage export --run 20261103-boss6-triage
```

程序只处理实读者已判non-math/delete或evidence-only/attach/delete的正式包装页；clarify与混合/数学内容不会被自动清掉。仍被保留数学页直接或间接引用的计算说明移作附件并修相对链接；无引用的证据包装删除，原始代码/输入/输出不删除。X身份链接取消，后台actions和retired-paths记录当前去向，不在state再造替代空壳。

应用前全量检查原SHA、分类是否变化和目标是否冲突，检查失败不开始删除。正文改动限于本次退休路径的链接路由；不改数学陈述或证明。检查通过只保证所声明动作/字节，不认证分类数学价值。数学清单见mathematics.json，按存档目录见by-archive/，剩余问题见stage2-candidates.json。

## 第二步启动模板

先下载结果分支**最新根work.py**，旧上传启动器不认识新参数。由用户明确给Boss编号；N是占位，不能随机选。run和程序须已推送。用独立clone，不改绑旧cleaner clone：

```sh
python3 work.py --repo /明确的新目录/p25-bossN start \
  --actor BossN --role curator --save repository-cleanup \
  --branch rebuild/research-v2 --curation-run 20261103-boss6-triage \
  --board-branch wcg/board-curation-25 --token-file /仓库外/有效凭据.txt
python3 work.py --repo /明确的目录/p25-bossN doctor
```

`--curation-run`将工作区放到`curation/workspaces/<run>/<Boss>`，身份注册到`curation/runs/<run>/people/<Boss>.json`；不复用cleanup/workspaces和旧来源people。save暂沿用repository-cleanup作程序兼容，公屏分支和运行域独立，不另建伪数学存档。既有同clone继续复用已绑定run；换run或角色用独立clone。只有明确同对话恢复才使用resume/adopt。

协调Boss在激活第二步时运行一次`board-init`并读回确认，不复制旧历史。公屏按对象群task-id发成果、争议和阻塞；result须带实际pushed资产，不发布四千条打卡。未来研究Agent公屏/运行框架由后续设计，临时公屏不充当数学知识。

## 对象群任务命令

第二步任务须从已定性候选按真实数学联系组建；没有自动按标题生成accepted关系。Boss以[程序契约](PHASE25_PROGRAM.md)给的定义字段写任务JSON（可数组），先本地plan再checkpoint。发布后才能认领：

```sh
python3 work.py curation-task plan --run 20261103-boss6-triage --record-file 仓库内任务定义.json
python3 work.py checkpoint curation/runs/20261103-boss6-triage/tasks -m '发布对象群任务'
python3 work.py curation-task list --run 20261103-boss6-triage
python3 work.py curation-task show --run 20261103-boss6-triage 实际task_id
python3 work.py curation-task claim --run 20261103-boss6-triage 实际task_id
```

每群领取前先sync并读取实际任务状态，领取后再sync并核对输入SHA。当前list/show查看本clone快照，不能把未同步的列表当远端最新占用。Git同步/整合时由Boss组织暂停相关写入并保住草稿。

任务认领采用最新远端单任务事务、输入SHA与交叉写入路径检查、正常push和request_id读回；不以公屏说负责代替锁，不预领大量未来任务。所有代理可跨范围阅读，写入按任务互斥；同clone Git由Boss串行。

产物先checkpoint并收到pushed。assets JSON是`[{"path":"实际正文或附件路径","sha256":"当前实际SHA256"}]`，路径必须在任务写入范围。再提交并说明实质完成出口：

```sh
python3 work.py curation-task submit --run 20261103-boss6-triage 实际task_id --assets-file 实际assets.json
python3 work.py curation-task complete --run 20261103-boss6-triage 实际task_id --reason '实际数学增量、保全或具体缺口'
python3 work.py curation-task handoff --run 20261103-boss6-triage 实际task_id --reason '真实运行边界' --draft-note '草稿路径以及是否共享'
```

claim、产物pushed、submitted与completed分别确认。submitted只接受远端已存在的同版产物；仅本地留在工作区和交接记录。completed是本步骤编辑交付，不是证明新定理或最终图准入。只读输入依赖在提交前已变动时，程序拒绝提交，须按新内容重新判断；属于本任务可写范围的输入允许以本次产物替换。内容变更必须重新判断，不机械刷新SHA继承旧完成。只有owner和本run协调Boss可完成已提交任务；handoff只释放本人未完任务。原`clean handoff`不释放这些任务。

## 暂停与退役

凭据只认证，不入消息、正文、remote或提交。认证失败停止同凭据重试和新认领；本地成果用checkpoint --local-only保存，明确未共享。

第一步暂停收好已回与未回批次、保留剩余lane和位置；第二步暂停交接/释放本人未完任务，写实际原因、草稿位置、共享状态与下一步。没有后台继续承诺。

阶段二旧设施在实际交接后退役；本轮临时工作区和公屏在后续交接完成后退役。先保全被数学/必要证据引用的内容，再清当前树，Git历史留回滚。2.5第三步和最终超边schema不在本手册确定。
