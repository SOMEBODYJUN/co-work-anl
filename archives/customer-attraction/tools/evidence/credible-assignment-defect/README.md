# 可信分配缺陷探针的原件与复核

[数学对象](../../../state/计算/可信分配缺陷的有限探针--计算.md)说明客户模型、真实偏离缺口、费用矩阵、条件覆盖界和两次搜索的量词。

| 冻结源 ID | 原字节副本 | 内容 |
| --- | --- | --- |
| `e63c0de156e1c7259af3` | [探针程序](source/assignment_defect_probe.py) | 稀疏目录抽样、计数策略、真实响应缺口及最优互异标签指派 |
| `001c9668a03adbfffeaa` | [9主题最佳快照](source/assignment_probe_m5p9.json) | 客户—主题矩阵、715个计数动作、最佳比较和成本 |
| `9a116a544d231eb32e28` | [9主题运行摘要](source/assignment_probe_m5p9.json.summary.json) | 400次请求及执行、3个实际不交样本、最大评分−7 |
| `b24d472369a20268f0cb` | [10主题最佳快照](source/assignment_probe_m5p10.json) | 客户—主题矩阵、1001个计数动作、最佳比较和成本 |
| `3f8c738c1e24e7cdf553` | [10主题运行摘要](source/assignment_probe_m5p10.json.summary.json) | 4000次请求及执行、153个实际不交样本、最大评分−3 |

五件均来自冻结目录 `research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/credible/`，在提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的对应路径内容相同。原件 SHA-256 由复核器按清点值逐件验证。

从本目录复现。原程序需要 NumPy 与 SciPy，本轮版本分别为 2.3.5、1.17.0。精确复核器仅用 Python 标准库。

```sh
replay_dir="$(mktemp -d)"
python3 source/assignment_defect_probe.py --topics 9 --players 5 --customers 30 \
  --trials 400 --seed 721028 --output "$replay_dir/assignment_probe_m5p9.json"
python3 source/assignment_defect_probe.py --topics 10 --players 5 --customers 16 \
  --trials 4000 --seed 892139 --output "$replay_dir/assignment_probe_m5p10.json"
python3 check_snapshots.py "$replay_dir"
```

[复核实录](exact-check.json)中的 `replay_matches` 同时要求完整快照逐字节相同、摘要除 `seconds` 外逐字段相同。省略复核器参数可独立核验原件。复核器展开两个保存策略的全部有序历史，用 `Fraction` 逐行动比较真实终局收益，用真实收益松弛及逐客户核函数双算每一早期缺口，再穷举全部最优多重集和指派。源程序只保存两个完整极值快照；其余试验由定种子扫描重放。两组样本的最大最小评分可由两侧核对得到：每个试验原程序找到的合法指派给该试验最小值的上界，保存试验的最小值经独立穷举达到相同上界。
