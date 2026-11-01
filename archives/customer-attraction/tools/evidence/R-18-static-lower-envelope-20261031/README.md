# R-18 静态 NE 下界桥的有限反例与审计

来源：

- `49f584562754ec7fcfe8`：`gap_sparse_results.json`，与已归档 `R-18-gap-probes-20261031/replay/reduced/gap_sparse_results.json` 逐字相同，作为 duplicate 保留。
- `27576d9bfe3d6691a921`：`static_comparison_probe.py`，用完整历史 SPE 递归和 ExactSPESolver 搜索 `min SPE welfare < min PNE welfare`。
- `b6f24f580ea7de328491`：完整 (m=3,p=4) 证书，`spe_w=25,pne_w=29,opt=29,checked=2322`。
- `c20cc352a689a12bc1de`：较小记录，`spe_w=21,pne_w=25,opt=25`。
- `098b9ccdc86ad20cd4d7`：对同类 25 客户实例的精确有序历史审计，21 histories、84 comparisons、actual welfare 21、opt 25，六个静态 PNE 都是 25。

本 clone 直接运行 `static_comparison_probe.py` 的 stderr 为 `ModuleNotFoundError: No module named 'customer_attraction'`；冻结 JSON 与已保存证书仍按字段阅读和相关 package 记录核对。该失败不是数学否定，只说明当前本地依赖未安装。
