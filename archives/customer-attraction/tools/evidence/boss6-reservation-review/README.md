# 预留菜单盲审三源证据

对应[实质复核正文](../../../state/审查/预留菜单盲审三源实质复核--审查.md)。本包只处置menu的三份冻结主源，不额外勾选security两必要输入。

- `source-manifest.json`：三个primary及两个related输入的完整路径、源ID、双冻结commit、size/SHA256/Git blob和本地路径。三主源由本轮`work.py clean show ID --out`取得；两输入逐字复用已有`disjoint-reservation-literal-audit-four-primary/related-original`中的同指纹原件。
- `original/`：原相对树中的2738B JSON、4857B Markdown、5437B Python、1549B游戏、43258B完整策略及静态证书，原字节不改。
- `all-400-actions-readable.txt`：全部400动作的紧凑可逆分层视图。首行根动作；每个prefix行的七数字依次给prefix+(0,…,6)处的动作。与原动作映射回拼完全相等；没有计算收益或IC。
- `data-contract-check.json`：本轮实际纯数据/AST自查。核五件完整指纹、400动作键域、可逆视图及四个标准库模块；收益、IC、OPT、静态枚举及LP执行均0。

五件原件总57839B。原代码从自己的`parents[5]`取得原根，保持`original/research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/{menu,security}`布局即可恢复真实两输入。未来若要重放，先复制整个`original/`到临时目录，再以未优化Python运行临时副本的menu脚本。程序没有main guard，import同样执行，成功时会覆盖副本中同名JSON；不要在保全原件中直接覆盖原报告。

原报告的2800比较、343有序静态背景和2219/181细分属于σ₀输入，不能嫁接到14处平局不同的literal策略。当前没有伪造旧运行命令、exit、解释器版本或stdout/stderr。关系及证据责任完整见正文。
