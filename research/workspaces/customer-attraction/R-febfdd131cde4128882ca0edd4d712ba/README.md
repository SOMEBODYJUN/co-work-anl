# Boss18：只攻五人半覆盖

程序身份 `R-febfdd131cde4128882ca0edd4d712ba`，独立 clone、main、customer-attraction。
2026-10-25 本轮用户明确只攻 m=5，先证明 HALF(5)，再考虑推广；
本轮范围优先于旧 general-only 指令，不改变其他会话的方向。

## 精确目标

采用 [CAG-MODEL](../../../current/customer_attraction/model.md)，恰五名单位提供者，
任意有限共同目录、单位客户、每个完整有序历史纯 SPE、任意平局、重复和空主题。
欲证 `OPT_5<=2W`。五人及一般 Q-CAG-HALF 均仍 **OPEN**。
旧约2.06169478572上界及旧必要条件坏点不属于本轮新结果。

## 本轮新增与文件地图

| 路径 | 数学内容、真实状态和接续用途 |
| --- | --- |
| [parent/five_root_binary_tail_credit.md](parent/five_root_binary_tail_credit.md) | 新二值根背景四人利润证书：F4≤1.999V_out+(5/3)V_in；含13行精确乘子、全类型证明及匹配根偏离12000OPT+997J≤5997ΣV_i+997Σz_i。已独立定义级内审，无外审/新颖性认证，未闭合五人half。 |
| [parent/binary_tail_pareto.py](parent/binary_tail_pareto.py)、[证书](parent/binary_tail_exact_1999.json) | 发现LP和有理重构，穷尽1280客户系数条件；不是有限游戏无反例。 |
| [independent/binary_tail_review.md](independent/binary_tail_review.md)、[独立实现](independent/audit_binary_tail_certificate.py) | 不导入父方公式，从原始终局份额和六索引对复核全部4096原始会员类型、13非负乘子和19零余项。 |
| [root_tail/aligned_complement_credit.md](root_tail/aligned_complement_credit.md) | 旧四人证书在二值背景的残余信用、匹配互补四主题总利润精确4OPT；保留更细会员表。 |
| [root_tail/binary_pareto_residual_table.json](root_tail/binary_pareto_residual_table.json) | 新证书按真实尾4会员及匹配比较重数保留的逐客户最小剩余，用于增强根直方图；数值结果须独立标级。 |
| [template/aligned_root_pricing.py](template/aligned_root_pricing.py) | 根真实四人回复32类型直方图定价，与旧索引系统组合新对齐、信用和真实菜单行；正在运行的浮点探索，不是上界证书。 |
| [exchange/optimality_union_probe.py](exchange/optimality_union_probe.py) | 用最优组合替换子集的精确必要关系检验旧松弛；旧坏点最优主题已分割全部原子，因此仅最优性不补真实续局IC。不是SPE反例。 |

## 真正缺口

新根信用仍含互斥真实根分支的尾利润和 ΣV_i。不能用实际W直接替换。
已独立核验的组件不等于 HALF(5) 已证。继续保留完整J、根实际偏离利润、
比较重数及客户残余，寻找跨分支共同付款；不以粗强桥的失败作为研究终点。
六名指定 gpt-6.1-sol ultra 已实际启动，父方同时推导；不承诺回合结束后后台常驻。

## 复现

```sh
python research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_pareto.py --exact --beta0 1999/1000 --beta1 5/3 --output binary_tail_exact_1999.json
python research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/independent/audit_binary_tail_certificate.py --certificate research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json
```

阶段资产由根 work.py checkpoint 提交，只有回执 status=pushed 才报告远端保存。
