# 单固定完整策略的signed调和/query诊断证据

正式对象：[两人固定完整策略程序](../../../state/程序/两人固定完整策略的有符号调和与查询锥诊断--程序.md)；身份资料：[协调工作室路由](../../../state/资料/协调工作室身份的固定路由与实例--资料.md)。本包只有三个主源：3194B源码、857B历史报告和150B身份JSON，均经 `work.py clean show` 全文读取及导出，`source-manifest.json`保存双冻结commit/path/blob/SHA。

`original/`始终保源字节。`replay/`保存一次未改源码执行（共2 LP）的运行副本、stdout、空stderr、新报告和独立行审计。新报告与原报告逐字节相同。`execution-and-row-audit.json`明确保全部数值及无精确负证书边界；`audit_replay.py`先按集合/Fraction重建行，再核71客户整数seed，不恢复最优点或对偶，也不扩展策略扫描。

`comparison-reading-manifest.json`逐份列完整阅读的18份相关文本及其实际SHA；它们仅供比较，不额外作为本组三源主处置。包括signed协调独审、原支持归约/另一计数锥程序、现净预算量词、完整71客户族、较弱self探针的双报告纠错和静态非SPE边界。Boss6旧工作室检索未见本组的先前实质草稿；两个旧路由/交接文件不代替数学阅读或done。

复现须将整个包复制到clone外的新目录（例如 `/workspace/scratch/3e409996c6a3/boss6-runs/signed-harmonic/事件目录/`），保 `original/` 与 `replay/` 相对布局，然后运行复制出的 `replay/audit_replay.py`。脚本会向自身旁边写报告和日志；避免原地覆盖本次已归档事件。依赖Python、NumPy、SciPy，其版本保于事件JSON；原码无规范CAG导入或外部客户输入。

本结果只是两玩家/六菜单/指定完整策略/严格TQ最优间隙的一次浮点阴性。约−1/6不是已认证精确上界，不是全策略或六人half证明。资料JSON只表示旧工作室路由身份，不是研究结论。
