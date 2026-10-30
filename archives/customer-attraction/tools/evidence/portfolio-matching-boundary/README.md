# 真实组合匹配与两人平均偏离证据

本目录保存5主题86客户完整两人SPE的匹配收费障碍，以及任意背景下两名剩余玩家平均偏离恒等式的必要输入和精确复核。

- `original/`：逐字节冻结实例、完整策略、两个原审计和两个原报告；来源ID、路径与SHA-256见 `source-manifest.json`。
- `audit_reconstructed.py`：本轮标准库Fraction独立重构；从所有末位最佳回复函数枚举本实例全部SPE，另检查64型符号背景恒等式。
- `replay/reconstructed.json`：独立复核全部通过的完整输出。
- `replay/original_uniform_rerun.json`：原均匀审计的原样复跑输出。原匹配审计依赖旧目录定位与规范包，只保留原件；其数学结果由独立重构复现，不声称原样复跑。

从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/portfolio-matching-boundary/audit_reconstructed.py
python3 archives/customer-attraction/tools/evidence/portfolio-matching-boundary/original/customer_attraction_uniform_portfolio.py
```

相应正式正文为 `state/障碍/最优组合真实偏离匹配不足--障碍.md`、`state/定理/两名剩余玩家跨分支平均偏离恒等式--定理.md` 与 `state/计算/真实组合匹配与两人平均偏离的精确核验--计算.md`。匹配公式的失败不等于半覆盖反例；两人恒等式不证明一般人数接口。所有数学假设与审查边界以正式正文为准。
