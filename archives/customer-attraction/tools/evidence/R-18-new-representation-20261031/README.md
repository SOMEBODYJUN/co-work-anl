# R-18 背景利润表示与共同目录障碍（2026-10-31）

本目录保存三份冻结源的逐字副本及一次本地 Fraction 复跑。源 ID：

- `4282bd971cbe6ce465be`：`audit_background_thinning.json`，冻结 SHA-256 `f77109e58d6af6cb55122a5950568da4488455822095e631a6b6b757db8a96aa`。
- `0a0f4e59d71378f29cb1`：`audit_background_thinning.py`，冻结 SHA-256 `00b75ca59147b49c04f1aa0ddc5d4c17d148c50c77dedf6ede4c84498c3c6542`。
- `5b1feed3fa7db9824463`：`background_thinning.md`，冻结 SHA-256 `e8c7e78f82cb5683beacfddc77aac6d34689de1fb9da2934c3bcd3f5ffe104ae`。

复跑命令：

```sh
python3 audit_background_thinning.py > replay.stdout.json
```

复跑使用 Python `Fraction`，完整输出与冻结 JSON 相同：1778 个单客户覆盖枚举、56 个端点、196 个有符号中间残差、3 个有限 SPE 见证历史、42 个编译终局、414 个完整策略、56 个相对误差端点检查；状态仍是 `all finite exact checks passed; no general half-bound claimed`。输出只支持有限精确核验，不支持背景利润半界或共同目录半覆盖定理。
