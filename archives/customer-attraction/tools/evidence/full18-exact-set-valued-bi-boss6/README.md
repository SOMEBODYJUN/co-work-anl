# 18主题114类型种子的精确集合值BI重放

本包保留三个主源和两个比较依赖的冻结原字节。父方本次实际原样运行 `full18_exact_bi.py` 一次，全部非时间字段与冻结报告相同；未执行 `full18_cone_attack.main`、任何浮点LP、随机锥搜索或恢复发现。

依赖 Python、NumPy、SciPy（Attack在导入时加载linprog，BI未调用）。从本目录复现：

```sh
python3 original/research_1/full18_exact_bi.py
```

该原入口会在original/research_1下写新的报告；原冻结报告另有源指纹，本次报告为replay.json。复现比较时仅移除stages各项seconds，其余字段逐个相等。comparison.json和replay-stdout.txt记录本次结果。原始数据与源SHA见source-manifest.json。

full18_vertex_recovery.json只有恢复摘要，缺少88个正质量、恢复方程与可重放新实例，不能用这个包认证其旧策略完整IC；不补造缺失数据。
