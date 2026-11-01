# 全菜单与首对背景原诊断

五个primary正常`clean show`全文取得并核字节/SHA256/Git blob：入口1968B、U程序3948B/U三行日志2386B、pair程序3150B/pair两行含66row日志23346B，总34798B。完整冻结来源和本地路径见[source-manifest.json](source-manifest.json)。另全文读取5个required-related：model8640B、exact9943B、36客户输入1846B、86客户输入4405B、包络证明5529B；它们仅支撑比较，不额外receipt/done。

正式对象：

- [完整菜单包络的离轨终局选择诊断](../../../state/程序/完整菜单包络的离轨终局选择诊断--程序.md)：精确E拼合/包络、全部MILP变量与big-M、返回字段/早停、三条日志的两份提案、48path历史状态，分清有理提案和缺失精确上界。
- [合法背景首对利润与静态安全下界诊断](../../../state/程序/合法背景首对利润与静态安全下界诊断--程序.md)：可信终局递推/同时首对筛选、r静态槽LP/有理query下界、全部66row分类和后来的PB反例/可达性范围。

检索原程序/数据SHA及名称，只见旧导航、待处理清单和MD历史报告，未见同SHA成功重放包；没有为增加阴性记录重跑原MILP/LP/SPE。新[标准库算术检查器](check_record_arithmetic.py)实际调用1次exit0，0原入口、0optimizer、0SPE solver。它核两份U提案的全部G/psi/gap和30旁枝计数/当前收益上限；核pair66个合法query、保存首对终局利润、全部21252静态计数价格的精确最小值、margin/best。完整逐row结果见[record-arithmetic-check.json](record-arithmetic-check.json)，实际观察范围见[run-record.json](run-record.json)。

这次新检查**不认证**SPE孩子membership/首对全SPE最低值，不重算48path，也不认证任何浮点最优或真实静态值上界。因此正pair margin不能证明那66个背景PB；U负提案不能证明全菜单无分离。原source版本和原日志均未覆盖；新输出另名。

10篇正式比较全文及SHA见[comparison-manifest.json](comparison-manifest.json)，已解释关系见[relation-review.json](relation-review.json)。任意背景PB已由后来解析完整子SPE反例否定，其精确背景又被排除成为actual根前缀；两点都不反U或六人half。原入口的待审/OPEN只保历史身份，不覆盖当前状态。

交付草稿、逐源语义receipt、全文件copy manifest及结构自查在`cleanup/workspaces/Boss4/resume-menu-diagnostics-20261101/`。Worker未Git、claim、done、checkpoint或sync；Root统一串行提交。本证据包不是原诊断新run或外审证书。
