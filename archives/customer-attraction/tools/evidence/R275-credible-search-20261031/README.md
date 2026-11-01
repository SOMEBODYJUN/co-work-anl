# R-275 credible search evidence

本目录对应正文 `archives/customer-attraction/state/审查/R275可信搜索对称DAG与共同次模投影增量--审查.md`，保存 20 个 clean source 的 materialized 原文、静态检查和运行边界。

- `certificate_audit.json` 与 `audit_stdout.txt`：12 条完整策略证书，均 2801 histories / 16806 deviations，min slack 0，`universal_claim_proved=false`。
- `acyclic_review_stdout.txt`：52 客户、4 人、6 主题、259 histories / 1295 deviations，W=47、OPT=52。
- symmetric q23/q32/q221 warm/single/maximal 输出：exact candidates 通过 definition-level verification，但 `universal_claim_proved=false`；代表比率 9/5、1791/1000、897/500。
- indexed projection：`target_reachable=false`、`OPT_over_minimum_SPE_W=1`，不是 SPE 反例；脚本在当前 materialized 路径因缺相对 `customer_attraction/model.py` 首次真实失败，stderr 保留。
- broader common-submodular JSON：1470 coefficient rows，exact values 2 与 88/57，均明确不属于 customer-attraction half。
- submodular path：30 条 dual-optimal necessary cuts、best value 17/8，但 root target unreachable。

`source-manifest.json` 记录 20 个 clean IDs/path/blob/SHA/size；`comparison-notes.md` 说明与 R275 background-exchange、R216/R24 necessary projections 和既有完整证书的比较。
