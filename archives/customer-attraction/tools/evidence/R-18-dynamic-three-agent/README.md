# R-18 dynamic_induction/step_profit_search.py 复现证据

主源为冻结源 ID `5878a511362d7d461809`，路径
`research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/dynamic_induction/step_profit_search.py`，blob `fbbb91458fd1f7c00b967b7fd074cf7736f3fa82`，SHA-256 `37ad28e1c86f75b4fb9d24f172a98fdbefc318bd5faf576529f0392fb3aba3d9`，大小 1608 bytes。源文件由 `clean show` 导出后逐行阅读。

复现使用已有精确 `customer_attraction` 实现的字节副本（`related/customer_attraction/`），没有替换模型或修改主源。重放命令为：

```sh
PYTHONPATH=related python3 original/step_profit_search.py
```

输出保存在 `replay/step_profit_search.stdout.json`。固定 `Random(20261021)`，每次随机选 `k,n∈{3,4,5}`，每个非空主题支持独立取 0–7 的客户重数，最多 1000 次；当比值首次超过 2 时提前停止。实际在第 306 次达到 `25/12` 并输出五人三主题实例。该运行是有限实验，不是穷举或一般定理。

依赖副本来源于仓库已有 `R-18-harmonic-counterexample-20261031/related/customer_attraction`，各文件 SHA 见 `source_hashes.sha256`；它仅用于固定 ExactSPESolver、Instance、CustomerType 的语义，不改变主源的数学结论。
