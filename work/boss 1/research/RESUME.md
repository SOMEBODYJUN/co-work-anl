# 首轮恢复断点

作者始终是 **boss 1**；工作区始终是 **work/boss 1**。本轮没有发布，也没有开始增量周期。

## 当前事实

* run_id：`35440ff34fc845dbaa2b3d94cf6d2c00`，首轮 cycle 1，分支 `work/cn-crisis`。
* 研究截点：2026年11月27日，America/Los_Angeles。执行日志使用实际UTC时刻。
* 原四件正式内容冻结于 `1580e869769a9410b88d040acf08bab394c6f9d2`。最终审计另发现情景目标错误被静默忽略、提前还款合同最高额度未执行两项缺陷；修复正在进行，原冻结版与179项旧通过记录保留，不覆盖修复版。
* 原冻结版完成 s01—s17。追加第12条可移植性计算改变了s05绑定的账本和方法记录，当前s05及后继暂时失效，须对已核结果重新绑定；具体实时状态见 `receipts/session_after_portability.json`。s18 的120个月引擎已实现，旧数值验证通过，但新增反例使完整家庭引擎验收退回修复；真实离线界面验收也尚未通过，故 s18、s19、s20 未登记完成。
* 当前图 revision 31，16个节点、13条ALL机制，18项实际独立提案审查及应用，无待裁决节点、边或提案。
* 主判断：地产、地方财政与部分私人部门的危机已经发生；未来12—24个月以渐进承损与结构分化居首。2027为具体政策与合同窗口，不是全国必爆日期。以2021为起点准备接近十年的修复期，不等于从2026再加十年全面停滞，也不能推出A股十年必熊。家庭先核真实现金与履约时间。

完整验收看 `acceptance.json`，实际独立结论看 `final_review.md`。`session_check.json` 是最终执行检查的原样输出。任何文件未通过，不能靠修改这些文字或手填 pass 获得完成。

## 实际阻塞

正式HTML SHA-256：`9b4e215c09195bdf0ddcda0713f513b3899c7ced87596e67818a975f398d666b`。

独立审计者对这份文件调用本地Playwright，启动器因缺少真正的Chromium执行文件而退出127。浏览器尚未创建，实际界面操作、截图、导出下载各为零。官方Playwright浏览器下载返回403。当前云浏览器又明确拒绝本地file URL；已停止，没有用localhost、代理或其他浏览器路径绕过限制。

因此仍未证实：可见输入的编辑与校验、真实重算按钮和选择器、资产贷款增删、情景与排序切换、逐月表和图、JSON往返、CSV文件内容、320/390像素布局，以及真实操作期间零外部请求。Node/Python数值核验和HTML静态打包检查不替代这些操作。

证据分别为 `receipts/offline_ui_blocker.json` 与 `tasks/household_independent_audit/offline_attempt.json`。待执行操作保存在后者及同目录 `offline_replay.py`；成功脚本路径不等于成功记录。

## 在原工作区恢复

在仓库根目录执行，不创建新身份或覆盖现有工作区：

```bash
.venv-methods/bin/python work.py --workspace 'work/boss 1' status
.venv-methods/bin/python work.py --workspace 'work/boss 1' session start --actor 'boss 1'
.venv-methods/bin/python work.py --workspace 'work/boss 1' session next --actor 'boss 1'
```

新机器先正常克隆 `work/cn-crisis`，执行 `python bootstrap.py --research` 与 `.venv-methods/bin/python work.py methods doctor`，再恢复上述同一路径。新目录实跑的完整命令、原始输出、精确依赖清单和额外传递依赖约束保存在 `tasks/fresh_restore/`。原38项精确要求之外，原锁没有固定joblib引入的cloudpickle；本次复现环境安装3.1.3，并另存实际约束，不能说原锁穷尽所有传递依赖。

## 下一项实际工作

1. 仅在正常可用且获准的本地浏览器环境，对同一正式HTML运行已有离线脚本。不要在本环境重新尝试被明确禁止的替代路由。
2. 在仓库根目录进入 `work/boss 1/research/tasks/household_independent_audit`，使用装有Playwright的Python执行 `offline_replay.py --html '../../../formal/calculator.html'`。脚本仍需实际浏览器。保留旧失败回执，新的成功或失败记录使用独立目录/版本，避免抹去本次历史。
3. 独立执行者查看实际截图、操作日志和下载文件，核验每个动作对应结果。若发现缺陷，修源码、重建HTML，再对受影响数值和交互复测；修改后的SHA需要新的独立回执及新目录关键复算，旧恢复记录不覆盖新SHA。
4. 实际通过后登记 s18_calculator 并提交。将当前真实检查填入 acceptance.json，由实际独立执行者审核全部引用证据和四件正式文件，写 final_review.md，再登记 s19_audit、s20_release；记录和产物都不能漏出当前复核快照。
5. 使用完整作者 `--author 'boss 1'` 和届时实际复核者执行当前版本 review。只有真实通过才用 `--verdict pass`。随后由统一入口 release 发布同一四件文件，并执行 `session check --actor 'boss 1'`。必须看到 `complete: true` 才算本轮完成。

本次拒绝审查的统一入口只在状态中保存 verdict/reviewer/note，不保存 author/files/snapshot。作者与全部证据的实际绑定另外保存在独立发布审计的内容快照中，并在拒绝备注中引用其SHA；这不构成一次通过的程序快照。最终检查因此仍会列出缺少通过的作者/证据快照及发布。不要手改状态绕过这些门槛。

未发布首轮不能执行 `init --mode update`。当前经济与计算产物可以阅读和复算，剩余工作从 s18 的真实离线验收继续。
