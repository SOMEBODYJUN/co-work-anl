# 根最小均衡收益原扫描点的独立验证

原冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`，目录`research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/`。

- `scan.json`：源db1cb48198e1d91a0bd3，未改1304B历史输出。
- `workspace.json`：源31596cb0c1313cdbb613，未改150B身份schema，只有save、旧actor、旧instance；不执行旧身份命令。
- `root_payoff_README.md`：相关已处置源33031f5a2cbbcad3e9e0，只关联读，不重复done。
- `independent_check.py`：新标准库Fraction集合值逆归纳，并构造一份完整策略后逐历史强制动作检查。没有导入原规范求解器或重跑随机发现。
- `independent.stdout.json`：新完整结果，含全部85历史动作、两根终局、收益、OPT及边界输出。
- `independent.stderr`：新运行stderr为空。
- `manifest.json`：各文件字节数及SHA-256，不含自身。

复现：`python3 -I independent_check.py`。入口仅读同目录原JSON并打印stdout，原文件不被覆盖。实例14客户、W12、OPT14；只否定W≥4r_min，不反half。

正文：[四人根收益反例](../../../state/反例/四人根最小均衡收益的总付款失败--反例.md)。旧workspace纯身份字段无独有数学；当前有效Boss身份以本clone实际start登记为准。
