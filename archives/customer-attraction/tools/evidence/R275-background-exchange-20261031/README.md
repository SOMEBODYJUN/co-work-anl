# R-275 background-exchange evidence

20 个冻结源均以 `clean show` 全文读取，绑定见 `source-manifest.json`。

实际重放：

- `audit_penultimate_exchange.py` exit 0：98 个 m=3..100 exact checks，scope 明确 NOT FULL SPE。
- `audit_tax_projection_polynomials.py` exit 0：10 个 pair rows，公共正倍数 2m(m-1)，逐系数非负。
- `exact_terminal_projection.py` exit 0：m=2..8 terminal projection LP。
- `middle_floor_projection.py` exit 0：m=2..9、last/lasttwo/all projection LP。
- `fresh_maxima_projection.py` exit 0：m=5、4095 variables、798 rows、objective 2.084593514818204。
- `overlap_consistency_projection.py` 在临时模块目录导入 fresh maxima 后 exit 0：954 rows、objective 2.084593514818203。

`audit_reply_cap.py` 需要当前 clone 不存在的 `examples/customer-attraction/*.json`，未伪造执行；`full_actual_reply_cap.py`、`exact_strengthened_projection.py` 等依赖同工作区其他冻结模块，源内 JSON 结果保留但不冒称独立重跑。所有 projection 输出均不升级为 full SPE 或 Q-CAG-HALF 结论。
