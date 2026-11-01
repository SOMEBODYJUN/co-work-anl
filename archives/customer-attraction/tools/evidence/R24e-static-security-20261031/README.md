# R-24e static-security evidence

`search_f_static_security.py` 全文读取；它固定 seed=20261024，对 k=3/4、m=3/4、2000 个随机客户权重实例，以 ExactSPESolver+LP 搜索 `minp < v`。当前 clone 缺失 `customer_attraction` 包，直接导入报 `ModuleNotFoundError`，没有输出可复核，因此不宣称 FOUND/none。`workspace.json` 只有元数据。SHA/冻结 commit 见 `source-manifest.json`。
