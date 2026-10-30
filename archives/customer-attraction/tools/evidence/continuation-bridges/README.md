# 三种续局捷径的精确证据

数学含义、逐源归属、完整树核验原理和运行限制见[正式计算对象](../../../state/计算/三种续局捷径的完整策略精确审计--计算.md)。

## 文件与复现

- `tests/audits/customer_attraction_continuations.py`、`examples/customer_attraction/residual_counterexample.json`、`evidence/certificates/customer_attraction/residual_counterexample.json` 是原字节资源。
- `evidence/runs/2026-10-09/customer_attraction_continuations.json` 是本轮重新取回的冻结报告；`replay.json` 是此前已保留的重放；`replay-20261030.json` 是本轮实际重放。三者逐字节一致。
- `comparison-20261030.json` 记录Python版本、五份来源指纹、双冻结提交定位和报告对照；`PROVENANCE.json` 保留原有三份资源来源记录。
- `audit_residual_lower_welfare.py` 是本轮补充程序，检查保持五个末位回复、只把根从A改D的完整SPE；输出 `lower-welfare-replay.json` 含新证书及全部收益表，不宣称求出了最差SPE值。

在本目录执行：

```sh
python3 tests/audits/customer_attraction_continuations.py
python3 tests/audits/customer_attraction_continuations.py --output fresh-replay.json
python3 audit_residual_lower_welfare.py
```

依赖仅Python标准库，运行时保留断言，不使用 `-O`。第二条命令要求输出文件尚不存在；固定相对目录不可随意打散。原审计与补充程序均不导入规范求解器，但独立代码路径不等于新完成了盲式独立发现或外部审查。原审计只检查三份给定完整策略，不是任意JSON的严格schema验证器。
