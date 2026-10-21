# 可信全历史SPE搜索与旧证书范围审计

主目标 Q-CAG-HALF 仍开放。本目录是 Boss7 团队研究员个人备份，所有有限搜索、
数值界和超时均不改变一般命题真值。只写本目录，未改旧资产或共享账本。

## 已复核的旧资产误标

`audit_old_largest_incumbent.py` 不导入游戏实现、LP、MILP或SPE求解器，展开
963个单位客户，直接用标准库 `Fraction` 检查43个有序决策历史的215项非自身偏离。
源为 `R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json`，
SHA256 `7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd`。

源JSON写 `verified:true`，并给 `OPT/u_0=642/125>5`，但生成脚本
`largest_incumbent_probe.py` 明确删掉所有根偏离约束，只检查后继节点和最大主题条件。
因此该字段不是完整历史SPE定义级验证。审计结果
`old_largest_incumbent_audit.json` 显示实际路径 `(0,2,3)`，收益
`(375/2,579/2,273)`，W=750、OPT=963。根改选1、2、3、4、5分别得
303、303、357、190、303，均严格高于375/2；其他历史没有盈利偏离。
这不是弱逐人桥或half的反例。旧源字节未改。

重放：

```sh
python research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/audit_old_largest_incumbent.py
```

## 已完成的真实SPE候选搜索

`dag_individual_probe.py` 复用
`R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py`，
以W=1最大化 `coverage(J)-(2m-1)u_a(q)`。该DAG不限制计数Markov；浮点MIP
只选证人，展开全历史后再在固定完整策略锥中精确恢复整数客户并核验全部偏离。

三项各12秒的归档运行均超时但有合法incumbent，随后有理恢复成功：

| JSON | m,p及根计数 | 目标主题与J | 精确OPT/u_a | 全历史/非自身偏离 |
|---|---|---|---:|---:|
| `m4p5_11110_a0.json` | 4,5；11110 | a=0；1234 | 19/4<7 | 156/624 |
| `m4p5_21100_a1.json` | 4,5；21100 | a=1；1234 | 6<7 | 156/624 |
| `m5p5_31100_a1.json` | 5,5；31100 | a=1；01234 | 5<9 | 781/3124 |

这不是这些实例规模、固定根或全部策略的最优上界。
`audit_dag_candidate.py` 是另一路不导入规范包的标准库Fraction全历史审计；
`individual_candidate_audit.json` 保留上述三个完整证书的独立核验、源哈希和统计。

`dag_restricted_half.py` 在上述DAG上加每个实际占用a、每个主题T的合法必要行
`|T|<=m*u_a(q)`，并仅在数值发现阶段限定每客户至多关联一个根未使用主题。
两项m5p7、J=23456、比较覆盖门槛1.8：根3200000（23类支持）与2210000
（39类支持）各25秒均无incumbent；各有42345变量/41888二元变量。
JSON为 `m5p7_3200000.json` 与 `m5p7_2210000.json`。这不证明不可行，
也不缩减一般量词。精确固定锥重优化若被触发会重新放开类型支持。

## 正在接续的路线

`tight_markov_probe.py` 复用旧
`R-c4732bee2f7b4e50a70568170e3334ae/credible_search/markov_joint.py`。
在归一化W=1的根SPE中，每名实际玩家偏离T保证至少|T|/m，求和给
每主题大小|T|<=1，故每个辅助终局收益及每客户类型重数都<=1。
显式加此主题size cap，并将旧条件常数m收紧为1。此脚本只探索计数Markov
子类，不声称一般策略可归约为该子类；找到后仍展开全部有序历史精确核验。
五人七主题仅4747变量/2310动作二元变量，尝试改善旧大DAG的启动瓶颈。

另三项m3p6的弱逐人DAG尝试允许被攻击主题出现在任意实际位置；这避免只攻击
根玩家的旧联合树接口限制。所有运行都有限，完成参数和结果写独立JSON。

下一步以真实可实现策略或合法一般不等式推进。尚无一般half证明或反例，弱逐人
`u_i>=OPT/(2m-1)` 也未被本目录真正SPE证书否定。
