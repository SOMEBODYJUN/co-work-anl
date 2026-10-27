# research_4：同覆盖标签的完整 SPE 商编译

本分支没有证明 Q-CAG-HALF-6，也没有严格目标反例。同覆盖标签商编译是旧定理 `B10-DUPLICATE-COVERAGE-QUOTIENT-v1` 的独立重构、新实现及压力测试；原正文为 `R-84ce8a8709e34ea6af94f99991d3c2e3/duplicate_quotient/duplicate_coverage_quotient.md`，本轮不认领新数学。其内容是：任意带重复覆盖标签的完整历史纯 SPE，能用依历史选择代表的 lift 编译到真正不同覆盖集合的目录，并保持根覆盖序列、每位收益和 OPT_m。

| 文件 | 准确用途与状态 |
| --- | --- |
| `duplicate_action_quotient.md` | 旧定理的自足独立重构；父方解析审查另记。并非六人 half 证明。 |
| `duplicate_action_quotient.py` | 完整商策略及历史 lift 的构造实现；重写客户类型不改变单位客户。 |
| `test_duplicate_action_quotient.py` | 定义级 Fraction 测试；不调用仓库 solver。 |
| `duplicate_action_quotient_test_report.json` | 64 个两人实例、5184 份完整策略中 856 份 SPE，200 个三人完整 BI 策略，以及一个六人完整规模回归，全部编译核验通过。 |
| `policy_cone_search.py` | 未完成原模型反例搜索工具；支持 count policy 与全部有序历史独立平局、策略锥边界随机侧点、策略 mutation。数值发现工具，未给一般数学结论。 |
| `verify_policy_candidate.py` | 独立整数核验数值候选：重数有理化后整数化，n=6 收益乘 60，核验完整 IC、主题是否相同、真实 OPT_6；未自动调用商编译。 |
| `minimum_reply_commutation.md` | 在旧统一极小重置上重构首回复交换方向；任意原尾可作为交换后极小查询的候选；尚无共同付款或旧坏点分离。 |
| `verify_minimum_reply_commutation.py` / `minimum_reply_commutation_report.json` | 15 单位客户局部严格例，从定义穷举全部 1024 完整两人尾策略，最低旧A收益 71/30、交换后 13/6，差 1/5；不是根 SPE/half 反例。 |
| `potential_side_attack.py` | 以开放辅助势作侧目标的未完成发现工具；没有将势候选加入约束，没有目标反例或新界。 |

一般引理的证明不依赖有限测试。两人有限测试穷举该指定域的全部完整策略；三人随机 BI 是实现压力测试；六人回归只是旧 all-big 家族。它们均不能作为 half 的证明或反例。

从仓库根重放商编译测试：

```sh
python research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/test_duplicate_action_quotient.py
```

反例工具示例（不会宣称有限阴性为定理）：

```sh
python research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/policy_cone_search.py --k 7 --ordered --steps 40 --seed 45 --output /tmp/ordered_candidate.json
python research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/verify_policy_candidate.py /tmp/ordered_candidate.json
```

原始数值扫描只再现旧 `11/6` 型，没有严格 `>2` 候选；其重复候选文件已删除。可用商编译避免把同覆盖标签误称为原目录独立动作，也不必添加区别客户。数值工具仍可选 `--distinct 0` 允许同覆盖标签，之后对精确候选调用本引理编译。

本轮还独立核验了六人实际仅用至多两个覆盖集合时的完整系数证书，随后查明它已由旧 `R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md` 的 Claim A+B 直接蕴含：末位频次 l≥2 时 k≤4，`l(2k+1)≥k²−1`；l=1 时实际路径是 X^5Y，适用 Claim A。因此未新增数学 Claim，也未保留重复 LP 文件。任意人数末两位不同的两支持结果另见 `R-27557809587746c59216a46867c9eb07/terminal_pair/two_support_end_ab.md`。

严格局部 min 例重放：

```sh
python research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/verify_minimum_reply_commutation.py
```
