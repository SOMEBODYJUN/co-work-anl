# 独立奖励多惩罚者目录的十八份诊断

正式正文：[十八份完整续局诊断](../../../state/计算/独立奖励多惩罚者目录的十八份完整续局诊断--计算.md)。本批五主源35585B，原字节及双冻结来源在[source-manifest.json](source-manifest.json)，`original/`完整保留四JSON和2732B程序。R-a5cc根README只作旁读，正式来源处置由根另外负责，不在本批done重复计数。

四份完整报告分别有6、4、3、5条不同参数记录，共18。三条target与指定路径成功、十五条目标计数不可实现；后者不表示目录无SPE。原JSON的成功项只有verification字符串，没有完整策略。原main仅列最初六参数，因此不能将另外12记录倒填成该main历史运行结果。

本批只为补足这些具体证据，运行[固定18参数驱动](run_frozen_18.py)一次：隔离worker加载原模块一次、调用原trial18次，每原参数一次、cert=True，原main零次、无参数扫描。18份新记录删去额外certificate后与四冻结JSON的全部字段逐项完全一致。三个新完整动作表均经不调用solver的规范定义级verify实际核验：

| 点 | 历史数 | 真正偏离数 | 资产 |
| --- | ---: | ---: | --- |
| results/0，(1,1;2,1,1,1) | 5 | 15 | [完整实例和策略](replay/certificate-parallel_attack_results-0.json) |
| results/1，(2,1;2,1,1,1) | 57 | 342 | [完整实例和策略](replay/certificate-parallel_attack_results-1.json) |
| support/3，(2,2;6,3,3,3) | 1111 | 9999 | [完整实例和策略](replay/certificate-parallel_attack_support_results-3.json) |

运行Python3.12.14、assert开启、1.095秒、exit0、stderr0；真实argv、driver SHA和stdio SHA在[execution-record.json](replay/execution-record.json)，完整标准流为[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)，逐记录字段/用时/证书SHA在[all-eighteen-results.json](replay/all-eighteen-results.json)。计数集合递推的不可实现性和完整动作表验证是不同证据义务，正文均说明；没有声称第二个独立solver、外审或新发现。

复用 `../exact-spe/customer_attraction/` 的 `__init__.py`、`model.py`、`exact.py`、`certificate.py`，不重复复制。四依赖已完整实读，字节SHA与冻结清单逐件相同，详见[dependency-manifest.json](dependency-manifest.json)。`all-eighteen-results.json`还保存实际载入路径/版本指纹。不能把按计数缓存的终局**集合**误当成一份固定Markov策略；恢复和核验仍展开全部有序历史。

可从仓库根运行同一有限入口：

```sh
python3 archives/customer-attraction/tools/evidence/parallel-tail-eighteen-boss3/run_frozen_18.py --repo .
```

该命令会覆写此目录replay中的新生成资产，不写旧原件、不调优化器、不扩大参数。当前证据来自恰一次已完成运行，未将未来复跑计入本次核验。

正文完整列出18参数及W_P/OPT/W_min/比率/根门槛；原first_local_failure全部depth0、target_in_child=false，其中三点根收益等于门槛，故不能据该字段伪造严格根偏离。r2存在完整成功点也禁止“所有多惩罚者都失败”的外推；原所谓repaired三点则确实全部失败。与多围堵全参数末位障碍、双奖励特定子树障碍和单色尾障碍的不同量词，见[relationship-review.json](relationship-review.json)。这是第二阶段关系依据，没有机械写第三阶段超边，也没有六人half结论。
