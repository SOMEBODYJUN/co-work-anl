# 首轮恢复断点

作者始终是 **boss 1**；工作区始终是 **work/boss 1**。这是首轮 cycle 1；没有正式发布，也没有开始增量周期。

## 当前研究与版本

- run_id：`35440ff34fc845dbaa2b3d94cf6d2c00`；分支：`work/cn-crisis`。
- 研究截点：2026年11月27日，America/Los_Angeles；执行日志采用实际UTC时刻。
- 当前经济内容和家庭源码冻结于 `7394ed770c1b47d134bc51e64aa3bb721dc157e0`。原 `1580e869769a9410b88d040acf08bab394c6f9d2` 版本、失败反例和旧独立回执保留在历史中；旧回执不替新版本背书。
- s01—s17 已完成并重新核对版本绑定。当前 `session next --actor 'boss 1'` 仍要求完成 s18_calculator；s18、s19、s20 未登记完成。后续独立审计记录和研究提交不改变这一阶段事实。
- 图 revision 31：16个节点、13条ALL机制、18项真实独立提案审查及应用；无待裁决节点、边或提案。
- 经济主判断：地产、地方财政与部分私人部门危机已经发生；未来12—24个月以渐进承损与结构分化居首。2027是具体政策与合同窗口，不能判为全国必爆日期。从2021起准备接近十年的修复期，不等于从2026再加十年全面停滞，也不能推出A股十年必熊。家庭先核真实现金、合同与可执行变现。

| 当前正式文件 | SHA-256 |
|---|---|
| formal/report.md | 65afc995b3031ffbdff967633fd0aa37274629cad40b7880bae663cbb20f7b4c |
| formal/judgments.json | af04fefc8348bf50902501082b6cce62d386d91d7336699461cf71d35986049a |
| formal/scenarios.json | 0133496a1354d514372e6bd9ed35efd83eb3ea6e914b5a2074a0e8bedaa7ae9b |
| formal/calculator.html | f0c72e3baa689bdbb6e7c4e75e12186e0fc1e2f6d2d59308ecdd39013a3ca049 |

实际验收结论以同版本 `acceptance.json`、`final_review.md` 和最终 `session_check.json` 为准。任何文件已写成或程序能运行，都不能替代尚未完成的验收。

## 已经修复并实际复测的缺陷

历史训练中未知标签误记负例的问题已经另建纠错实验；纠错实验引用旧目录绝对CSV路径的问题又经新目录恢复发现。当前 `models/compute-current.json` 包含11个有效作业规格，其输入均为仓库内相对路径。主工作区账本保留12次实际运行：重复计算不增加独立样本或经济验证。旧 `compute-audited-history.json` 与 `jst_audited_20261127/experiment.json` 仅为带失败历史的归档，不是当前可移植执行入口。新的规范输入和作业在 `jst_portable_20261127/` 与 `compute/outputs/historical-warning-portable-v3-933f425819ff.json`。

家庭源码已修复错误情景目标被静默忽略、提前还款单次/周期最高额度未执行等缺陷，并明确全清许可、额度重置、抵押物出售和自然到期费用的合同条件。独立家庭审计实际在最终HTML的内联引擎上完成原179项与新增36项，共215项通过；另一终审者另做77项合同检查。默认合成例的500条规则、3条压力路径产生168216行实际月账。原版与新版的经济数值对照、未修复反例、已修复结果分别保存，不将合成例结果当作现实安全概率。

最新家庭独立证据位于 `tasks/household_independent_audit_v2/`，当前恢复证据位于 `tasks/fresh_restore_v2/`。原 `tasks/household_independent_audit/` 与 `tasks/fresh_restore/` 的旧签据和失败保留。第二次新clone实际重跑变更的历史训练及家庭计算，未改的10个作业通过与第一次独立新clone的原始输入、代码、环境和输出逐项衔接，不宣称在第二个目录又新跑了全部11个经济作业。

## 当前真实阻塞：离线浏览器验收

独立审计者对最终 `f0c72…` HTML 实际再次调用本地Playwright；系统Chromium包装器因缺少真正执行文件而退出127，浏览器未创建。该次真实页面操作、截图和下载均为零。此前官方Playwright浏览器下载返回403；云浏览器又明确拒绝本地file URL。没有通过localhost、代理、原始CDP或其他替代路由绕过拒绝。

因此尚未证实：可见输入编辑及错误提示、真实重算按钮、资产贷款增删、情景目标与合同额度控件、情景与排序切换、逐月表和图、JSON往返、CSV文件内容、320/390像素布局，以及真实操作期间零外部请求。Node/Python数值复核和静态打包检查不满足这些界面要求。

证据为 `receipts/offline_ui_blocker.json` 与 `tasks/household_independent_audit_v2/offline_attempt.json`。已有待执行脚本不代表成功操作；后续仍须用实际运行结果检查新增合同控件和所有下载文件，并由独立执行者查看截图。

## 在原工作区恢复

在仓库根目录执行，不创建新身份，不覆盖已有工作区：

```bash
.venv-methods/bin/python work.py --workspace 'work/boss 1' status
.venv-methods/bin/python work.py --workspace 'work/boss 1' session start --actor 'boss 1'
.venv-methods/bin/python work.py --workspace 'work/boss 1' session next --actor 'boss 1'
```

新机器使用完整Git历史或交付包中的 `repository.bundle` 建立真正clone，再运行：

```bash
python bootstrap.py --research
.venv-methods/bin/python work.py methods doctor
```

随后按上一组命令恢复同一身份、路径、run_id和cycle。完整Git历史用于复演 `compare_migration` 对原1580版本的 `git show`；只有最新源码的浅克隆不足以独立重做该历史比较。不要把导出文件夹名称当作新研究身份。

独立环境的完整命令、输入输出、精确依赖、预算和复演说明见两个 `fresh_restore` 目录。原38项精确要求之外，原锁没有固定joblib引入的cloudpickle；本次环境为3.1.3，已另外保存实际约束。不能声称原锁覆盖了全部传递依赖，也不能把复用已建独立环境说成第二次重新安装。

## 剩余工作的具体入口

1. 在正常可用且获准的本地浏览器环境继续，不在本环境重试已明确禁止的替代路由。
2. 将待执行脚本复制到新的独立任务目录，保留本次冻结的失败回执。示例在仓库根目录运行：

```bash
mkdir -p 'work/boss 1/research/tasks/offline_ui_resume'
cp 'work/boss 1/research/tasks/household_independent_audit_v2/offline_replay.py' 'work/boss 1/research/tasks/offline_ui_resume/offline_replay.py'
python 'work/boss 1/research/tasks/offline_ui_resume/offline_replay.py' --html 'work/boss 1/formal/calculator.html'
```

使用装有Playwright的Python及正常已安装浏览器；必要时传脚本已有的 `--chromium` 参数指定获准可用的本地执行文件。新副本中记录的reviewer须改为当次实际独立执行者，不能冒用历史执行者。运行脚本之前核对其选择器和步骤是否覆盖当前新增合同控件；原冻结脚本与回执不得覆盖。

3. 独立执行者查看实际截图、操作日志和下载文件。若发现缺陷，修源码、重建HTML，再对受影响数值和交互复测。新SHA需要新的独立回执和新目录关键复算；原签据只能证明原版本。
4. 真实通过后登记 s18_calculator 并提交。将实际检查填入 acceptance.json，由实际独立执行者审核四件正式文件、全部验收证据和当前恢复记录，再写最终复核、登记 s19_audit 与 s20_release。必须遵守仓库阶段与复核依赖，不以文字替代真实记录。
5. 使用完整作者 `--author 'boss 1'` 和实际复核者执行当前版本 review；只有全部真实通过才用 `--verdict pass`。随后 release 同一四件正式文件，最后执行 `session check --actor 'boss 1'`。只有 `complete: true` 才能宣告首轮完成。

统一入口的拒绝分支只在状态中保存verdict/reviewer/note，不保存author/files/snapshot。当前独立拒绝审计另外保存实际作者、文件哈希和证据绑定，并在拒绝备注中引用；这不构成程序的一次通过快照。最终检查因此还会列出缺少通过的作者/证据快照及正式发布。不要手改状态或程序绕过这些门槛。

首轮尚未发布，不能执行 `init --mode update`。经济研究、数值引擎和源码可阅读复算，下一次执行从 s18 的真实离线验收继续。
