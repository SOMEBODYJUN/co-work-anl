# 完整终局证人DAG的可行热启动与真实反例搜索

目标仍为原模型Q-CAG-HALF，一般命题未闭合；本组没有找到目标反例。这里新增的是可接续的实现改进，不是新的福利定理。

## 改变了什么

上一轮完整DAG已经数学上允许全部历史依赖SPE，但五人七主题、自由客户重数时，已知可行目标1.8也不能在短时限找到incumbent。本轮直接使用SciPy内置的HiGHS私有接口`setSolution`，不另安装依赖：由规范`ExactSPESolver`的整个可实现终局集合构造完整`y/z/x/t`可行向量，再给原MILP热启动。对同计数的不同目标终局分别选实现行动，展开时仍允许同计数有序历史采取不同动作。

同一七主题五人自由模型包含42345变量、41888二元、77065约束。相同HiGHS选项、相同已知输入参数的受控对照中：

| 方式 | 实际求解时间 | 返回情况 |
|---|---:|---|
| cold，不提供可行向量 | 25.02秒 | 无incumbent |
| warm，提供完整证人向量 | 13.37秒 | 返回9/5证人；随后精确核验 |

两者根计数为(5,0,0,0,0,0,0)，比较主题组合为0,1,2,3,4，客户重数仍全部自由。此根的9/5上界本来即可由末位比较得到；该对照只证明实现现在能启动已知可行大模型，完全不构成新的数学上界。MIP整体“optimal”状态未作为有理证书。warm返回策略在固定完整策略锥中重优化，得到独立Fraction全历史核验及精确9/5原始/对偶证书；2801节点、16806非自偏离。原始报告见`warm_m5p7.json`，受控cold见`cold_m5p7.json`。

## 检验范围和当前瓶颈

`audit_warm_start.py`做42个正福利有限输入/根终局检查，完整核对原MILP约束残差、变量界、二元整性，并展开完整策略作Fraction偏离核验。另有全零及不可实现根的两项拒绝边界；空主题和重复覆盖也覆盖。既有三人五主题非Markov可达023例被热启动接受，展开证书确实有同计数不同动作；不默许计数Markov限制。记录在`warm_seed_audit.json`。这些是有限实现回归，不是一般数学证明。

随后攻击多支持根(4,1)、(3,1,1)、全不同行动及(2,2,1)，全部保持一般共同目录客户类型自由。根(4,1)的返回完整策略锥可精确提升到23/14，W28、OPT46；它不是目标反例，也不是新的总体下界。当前主要耗时在根松弛/启发式阶段，有限运行中经常尚未分支；存在热启动并未解决高质量新证人的组合搜索。实际HiGHS时间可能超过请求时限（一次请求40秒实际155.91秒），故程序参数是求解器软时限，不应当作硬墙钟限制。

可选`--radius`仅限制二元证人相对热启动的Hamming距离；`--restrict-outcomes`把允许的终局候选限制为旧输入BI集合。二者都只搜索原模型的合法子集，最终仍展开所有有序历史核验；不能据此排除一般SPE或目标反例。下一步可交替优化重数与扩展真实终局菜单，或利用成熟路径结构减少根类型；直接重复同一短时限配置没有新增信息。

## 文件与复现

- `warm_dag_search.py`：调用上一轮唯一DAG构建/展开/精确核验实现，新增完整热启动、受控cold、局部分支和候选菜单限制。最终输出记录参数、环境版本、代码哈希、实际时间；浮点界明确不认证。
- `audit_warm_start.py`、`warm_seed_audit.json`：有限边界与非Markov回归。
- `warm_m5p7.json`：全自由客户重数下已知9/5证人的完整精确回放资产。
- `warm_m5p7_41.json`：根(4,1)固定返回策略锥的23/14完整精确证书。
- `cold_m5p7.json`、`finite_search_summary.json`：受控性能和十五次有限运行的摘要。除关键证书外不重复保留每次完整策略。没有排除性数学含义。

从仓库根运行：

```sh
python research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/audit_warm_start.py
python research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/warm_dag_search.py --players 5 --topics 7 --seconds 45 --output new_warm.json
python research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/true_counterexample/warm_dag_search.py --players 5 --topics 7 --seconds 25 --cold --output new_cold.json
```

SciPy私有接口不是稳定公共API。若后续版本改变，只需替换solver adapter，数学DAG与规范精确核验保持各自合同；没有把软件接口失败解释为数学障碍。

## 菜单分解的实际边界

`population_gadget_probe.py/.json`保存同伴人口gadget的十二项有限私有主题扫描，提供`population_gadget_seed.json`。在这个seed的真实BI可达菜单内，自由重数MILP从71/48在1.33秒提高到8/5，精确证书见`restricted_m5p7_population.json`。这不是新的总体下界；意义是受限菜单的联合重数/策略优化确能改进seed。

这次LP顶点也暴露了反馈缺点：原输入根终局唯一，全状态共保留882个终局；8/5顶点具有大量平局，根有81个可实现终局，全状态保留2506个，下一次扩展菜单的短时限求解又停在根松弛。probe额外保存六项精确整数混合：把新顶点重数与原seed作100:1混合，仍有根(2,2,1)可实现且根终局唯一、保留数882，比例871/548。这里只展示该有限例的退化机制，不能推广为一般复杂度定理。下一步须结合严格裕度和受控菜单扩张，单纯把退化顶点反复送回去没有本轮进展。

`audit_saved_policies.py`完全不导入规范包，把两个关键证书展开为各个单位客户并重放全部有序历史；记录在`saved_policy_audit.json`。9/5优化输出虽有七行动标签，实际只有五个不同覆盖，审计还按既有覆盖类商构造另一个完整策略，逐781商节点/3124非自偏离核验；23/14输出有七个不同覆盖。覆盖类商的一般接口来自`R-84ce8a8709e34ea6af94f99991d3c2e3/duplicate_quotient/duplicate_coverage_quotient.md`，不是本轮新增数学结果。没有将重复覆盖标签误报为七个不同极大主题。
