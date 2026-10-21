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

## 后续运行实况与边界

`tight_markov_probe.py` 复用旧
`R-c4732bee2f7b4e50a70568170e3334ae/credible_search/markov_joint.py`。
在归一化W=1的根SPE中，每名实际玩家偏离T保证至少|T|/m，求和给
每主题大小|T|<=1，故每个辅助终局收益及每客户类型重数都<=1。
显式加此主题size cap，并将旧条件常数m收紧为1。此脚本只探索计数Markov
子类，不声称一般策略可归约为该子类；找到后仍展开全部有序历史精确核验。
五人七主题仅4747变量/2310动作二元变量，尝试改善旧大DAG的启动瓶颈。
路径00011、00112各25秒都只取得比例1的全兴趣单客户退化点，文件为
`tight_markov_00011.json`、`tight_markov_00112.json`。这两份早期输出保存了
客户点和运行时精确核验结果，但没有保存原MILP策略，不能单靠JSON重放那棵策略；
不是反例证书。脚本现已补上未来输出保存完整策略，未重跑或改写这两份旧运行。

另三项m3p6各20秒，根111000/J345、210000/J345、111000/J034均只取得
精确OPT/u_a=5，文件名分别以 `m3p6_111000_a0_out`、
`m3p6_210000_a1_out`、`m3p6_111000_a0_mixed` 开头。这些incumbent的被
攻击主题最终都被放在根，故增加只固定实际路径012的实验，明确攻击第二位：
`m3p5_mid_J234.json`（15秒额度、实际7.90秒）、`m3p5_mid_J034.json`
（15秒额度、实际5.47秒）、`m3p6_mid_J345.json`（20秒额度、实际12.99秒）
三个浮点MIP返回optimal，`m3p6_mid_J034.json`（20秒）超时；全部精确比值5。
只认证各完整固定策略锥中的有理原始点/对偶，不将浮点MIP状态认证为全类结论。
后来查到任意背景末两位保底已由现行 `last_two_floor.md` 完整证明，所以这些
倒二攻击只是重复检验已证范围，已停止，后续不再加此类MILP次数。

所有上述后台运行均已完成，没有运行中任务。已切向循环对称目录的显式
可信续局构造，或倒三及更早的解析机制。尚未把任何有限取等提升为一般定理。

## 循环目录的根扩张机制

`symmetric_root_extension.md` 给自足构造：循环对称实例中，任意前缀(0)的
完整子SPE都可以逐根分支旋转复制，根全部行动收益相同，因而扩成完整SPE。
这是精确表示，不是half或逐人下界。`cyclic_construct.py` 复用旧候选oracle，
对采到的后缀作上述扩张，再用客户类型轨道坐标的精确锥恢复整数客户。

两项均已结束：m3p7/seed78123/19轨道种子最佳OPT/u1=13/3<5，W11、OPT13；
m5p7/seed78124/19轨道种子目标half只得比例1。完整输入和策略分别为
`cyclic_m3p7_individual.json`、`cyclic_m5p7_half.json`。
不声称穷尽循环目录或统一策略锥，也没有缩减一般目录、无界m的目标。

下一步以真实可实现策略或合法一般不等式推进。尚无一般half证明或反例，弱逐人
`u_i>=OPT/(2m-1)` 也未被本目录真正SPE证书否定。
