# 十八主题BI与指定路径阈值复现

四个primary均由`work.py clean show ID --out`取得并全文实读。另从已归档原字节读取六份依赖/比较资料，并逐件按冻结inventory核size与SHA256；完整commit、路径、源ID、保存路径见source-manifest.json。没有修改原共享正文或其它证据包。

`original/`保冻结字节；`input-summary.json`逐条核三输入的正整数重数、合法18标签下标、类型不重复，并记精确总客户数及int64适用界。88类型输入只用于身份比较，没有重放它的BI、恢复或策略锥。

本次在临时独立复制树顺序运行两个原入口：114类型`full18_exact_bi.py`一次、252类型Rdiag的`audit_seed_actual_prefix.py`一次。均exit0、stderr为空；递归仅删除报告中的seconds字段，全部其它字段精确等于冻结JSON。实测新报告、stdout/stderr及实际Python/NumPy/SciPy版本保留在replay/。这是原实现重放，不是第二套独立SPE求解器；没有LP、随机控制器、浮点策略搜索或恢复算法调用。

在新输出目录复现（输出必须尚不存在）：

```sh
python3 reproduce.py --out /absolute/new/replay-directory
```

程序先核包内全部十份源的SHA，再复制original布局；两原入口只覆写新复制树中的报告。完整副作用、集合值递推、数值、指定有序路径及恢复缺口见[计算正文](../../../state/计算/十八主题完整逆推与前缀种子复核--计算.md)。
