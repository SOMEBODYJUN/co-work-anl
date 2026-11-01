# 四人结构化相对私有块证据

正式数学对象：[四人结构化相对私有块最优点](../../../state/计算/四人结构化相对私有块最优点--计算.md)。

- `original/structured_packing_4.json`：主源c44723ed32d119642928，594B；原字节SHA-256 `8a071bd9145e0e89ea833355b243355df42c2337e85513e3c926312286fb8e97`。
- `original/structured_packing_scan.py`：实读配套源df0869a6fbef9062a300，2000B；原字节SHA-256 `635b06a919eaeb2b7a237a80b734cc87ddba1620aa0a1732ce351d5106414f8a`。复制用于审计来源定位；本包不运行原入口。
- 两原件在冻结commit `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 同字节；路径均为 `research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction/` 下同名文件。
- `audit_exact.py`：此次新增独立检查器；从本包读原JSON，不导入原源代码、不调用SciPy/LP。固定n4策略按源配方重建，NumPy只比较seed浮点选择，Fraction认证所有504计数IC、1554有序IC、63列对偶、1296个终局与216种根动作后补全。
- `exact-audit.json`：新增执行输出；每一项有理数用字符串保存，包含原float与恢复候选差额。它不是原报告。原有稀疏float被保留在original。
- `replay-comparison.json`：和另包唯一原入口复跑的n4字节、动作表比较。完整原入口环境/stdout/动作观测见[扫描器复跑](../structured-packing-scanner/rerun/)，该证据不是本包另一次执行。

从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/structured-packing-n4/audit_exact.py
```

精确输出认证该**固定策略锥**的最优值3/2。有理点×4成为28个单位客户，SPE路径ABBB，W16/OPT24；首步机会损失仅2，即根收益4的1/2。原变量ratio、福利比和机会损失比保持区分。没有对所有四人目录、所有策略或六人half的结论。

全仓比较实际读取：共同目录完整历史模型、最优补全私有块交换与分支账本、固定六主题根收益单锥诊断、指定策略安全锥与七极大来源边界、真实计数策略在轨探针及固定尾深保底障碍。后续来源关系由阶段三按正文理由登记。
