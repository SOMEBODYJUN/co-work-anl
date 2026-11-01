# 真实末两人菜单三份发现期原审计

正式说明见[计算对象](../../../state/计算/末两人菜单三原审计的有限范围与版本对应--计算.md)。本目录保存 Boss3 正式认领的六个 direct_global 冻结源，原内容和双来源位于 `source-manifest.json`；所有原字节均通过原清点 SHA-256 和长度核验。

- `original/`：原 README、三份 Python 程序、共同包含与单早期例外两份冻结 JSON，均保持原字节。
- `replay/`：三份原程序的隔离执行副本，以及本次各运行一次所得三个 JSON。每个原入口只依赖 Python 标准库，使用 `Fraction`。未使用 `python -O`，断言全部启用。
- `replay-verification.json`：实际运行命令、exit0、Python3.12.14、原新报告与哈希对应。本批两份历史 JSON 及 Boss6 已保存的少例外历史 JSON，与本次输出三者均逐字段、逐字节一致。

从仓库根运行以下命令可复现。各脚本按原代码覆盖其**同目录的本次输出**，不触及 `original/`：

```sh
python3 archives/customer-attraction/tools/evidence/direct-global-original-audits-boss3/replay/common_penultimate_theme_audit.py
python3 archives/customer-attraction/tools/evidence/direct-global-original-audits-boss3/replay/audit_early_exception.py
python3 archives/customer-attraction/tools/evidence/direct-global-original-audits-boss3/replay/audit_few_exceptions.py
```

共同包含报告的3584是原始位公式实例，127856是压缩参数/交叠边界案例，8是带四次上界和五个精确零点的角值恒等式；单例外报告21504是三个人数下全部客户位模式，2400是100个人数的六角/端点；少例外报告40个参数、125424个客户角点，大人数背景只取代码指定子集。这些数字不是游戏或 SPE 数量。少例外末尾的负余项为范围外模板点，不是 SPE 反例。

本目录没有复制/改写 Boss6 已交付的少例外 JSON 或原付款稿；它们按正式计算对象的相对链接复用。六个本批源以外的相关原程序、独审和规范测试未因此自动完成勾选。
