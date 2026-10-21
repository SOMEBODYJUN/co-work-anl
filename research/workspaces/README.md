# 个人研究桌面与存档隔离

当前主攻 **Q-CAG-HALF**，存档 **customer-attraction**。统一入口为根[work.py](../../work.py)，三角色及命令见[RUNBOOK](../customer_attraction/RUNBOOK.md)。

start自动使用R-UUID并将本对话固定到main上的research/workspaces/<save>/<actor>/；同一clone接续时复用身份和角色，新对话使用独立clone。桌面可被同行阅读已推版本，公屏和私聊仍走wcg/board，私聊不混入默认公屏。

桌面保存可接续草稿、具体义务和证据入口，正文按数学对象进入current/questions/reviews，不按日期或boss复制多份。没有复用价值的工具输出、模拟聊天和测试身份不进入长期仓库。

新clone默认customer-attraction，旧shared/unrelated-machines桌面继续保留原save和范围，不自动迁移或接管。checkpoint默认只追加本人的桌面，不带上别人的未完成内容。其它存档明确选择后再进入其模型。
