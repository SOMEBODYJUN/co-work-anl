# Boss4 终局价格源证据

本目录保存 Boss4/cleaner 对 `R-486bb9adb8cd4d9a940dbf3b1ab0b1de/terminal/` 五个已认领源的逐字节导出、一次隔离重放及哈希清单。原始源来自冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）；两版文件内容相同，source ID 与 SHA 写在对象正文。

## 重放

- `audit_mass_two.py` 只用 Python 标准库和 `Fraction`，在 32 个 Boolean membership、5 个 `(d,ell)` 角点和 `p=0..3` 的有限表上生成 Newton 余项；随后用二项式基校验 `p=5,9,50,1000`。重放报告与冻结 JSON 的 SHA 均为 `e04e5a8ae9f73cbc24715b8afe1901a2c6f73e4fa2d5beb30e2b6df00f4526ab`，显示 4 个负 Newton 行。
- `audit_three_remaining_truncated_price.py` 对两组有理证书各核 160 个角点，断言 `p=0` 与所有 Newton 系数非负，并在 `p=5,17,1000` 复核二项式展开。重放报告与冻结 JSON 的 SHA 为 `9b1252b5f0dd663748b2895f5e83fe2a627350a485ed8891327d994e6d75e758`，状态 `all exact coefficients nonnegative`。

重放仅验证脚本写出的精确代数范围，不把有限实例或证书自动提升为 Q-CAG-HALF 的一般结论。`four_price_best.json` 是固定四人实例的完整策略输入；本批未取得其生成器与价格语义，故仅作为资源保留。
