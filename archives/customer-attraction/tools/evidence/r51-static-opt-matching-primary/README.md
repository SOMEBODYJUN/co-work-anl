# 最优支持冻结指派的两个有限程序

源 `5f85b7bcf0b6bca3c682` 是固定完整策略锥的发现/精确恢复器；源 `d2ec05dffb737730fbee` 是随机整数客户BI、非PNE筛选和锥攻击的编排器。两份原源码及依赖恢复到 runtime 的原始层次，无 ROOT 改动。

在本包目录运行（需 NumPy、SciPy）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 runtime/research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_opt_matching.py
PYTHONDONTWRITEBYTECODE=1 python3 runtime/research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/cone/probe_static_matching_random.py
```

本次16恢复锥均无接收候选；420随机种子只筛后进入两个非PNE锥。日志和输入身份分别保留，不称与未保存的旧stdout字节重现。程序只检查互异m比较支持和排列，不能据覆盖OPT数值相等就称已覆盖重复最优比较槽。既有1953/52客户反例已否静态强桥，有限阴性不恢复该桥，也不否真实净差候选或六人half。
