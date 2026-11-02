# d398父层八原件与有限检查

对应正文为[230根遗憾证书](../../../state/计算/正深度根遗憾锥的二百三十份有理证书--计算.md)、[七输入有效保险幅度](../../../state/程序/有效保险幅度的七输入完整续局诊断--程序.md)、[计数统一CSP](../../../state/算法/计数统一策略终局的精确CSP与既有分离合同--算法.md)。现有根交接资源、静态拥挤引理和审查页另补已恢复原件的状态。父层两个Markdown前已完成，不在本八条再次done。

| 源ID | 完整原件 | 字节 |
|---|---|---:|
| bb868f2d46c1a2b4d277 | [audit_static_crowding_review.py](original/audit_static_crowding_review.py) | 1740 |
| 7c9ce13b6f39c3291a34 | [count_policy_probe.py](original/count_policy_probe.py) | 6164 |
| a271e641130c716ae435 | [known_markov_obstruction_replay.json](original/known_markov_obstruction_replay.json) | 720 |
| 54f2c452dcda562edcf3 | [overlap_insurer_probe.json](original/overlap_insurer_probe.json) | 3256 |
| e1a109467f63e0aae7fd | [overlap_insurer_probe.py](original/overlap_insurer_probe.py) | 2014 |
| 6fe7d7a1109d2d2711af | [root_regret_probe.json](original/root_regret_probe.json) | 445332 |
| 24ab74dd58e0719474c0 | [root_regret_probe.py](original/root_regret_probe.py) | 5032 |
| f9aa84069b51ee9d64fe | [static_crowding_review.json](original/static_crowding_review.json) | 400 |

总464658B，两个冻结提交各同字节。双commit/path/blob/SHA和16项既有依赖在[manifest.json](manifest.json)：七原整数实例、四份精确SHA动作证书、strategy_lp helper和规范包四文件。不重复复制这些已保存输入，尤其不以同名另一例替原证书SHA。

## 本轮一次标准库检查

[check_saved.py](check_saved.py)没有原探针/helper/规范solver/verifier或NumPy/SciPy导入，不调用LP、随机CSP样本或K5原入口。它补两项实际证据缺口：

1. root大报告全部230份稀疏primal/dual和每项字段，按四原完整策略/精确Fraction排序重建根IC删除后的真实正深度行、根Δ行及比较目标，逐份核原始非负、W1、逐列对偶余项、目标=上界、root_regret和actual_gap。全部通过，四组最大7/4、3/2、33/23、9/8。230个Δ均等真实regret；仅2项正，为1/24。
2. 七保险报告只存赢家，本轮绑定实际整数输入并按定义级集合值BI补全每个根后全部可信终局集合，核M、OPT、提交winner及全部候选最大值。714个计数态、113个h≥M根/终局对，七最大均同原负值。

从仓库任意可写位置可以用：

~~~sh
python3 /absolute/path/to/check_saved.py /absolute/path/to/result-repository /absolute/path/to/new-verification.json
~~~

当前输出为[verification.json](verification.json)，包括230条逐项检查和七输入全部根后终局集合，原大报告完整字节仍独立保存。实际一次执行exit0：

~~~json
{"root_certificates":230,"root_maxima":["7/4","3/2","33/23","9/8"],"insurer_inputs":7,"all_insurer_scores_nonpositive":true,"new_CSP_or_K5_runs":0,"original_probe_runs":0,"optimization_calls":0}
~~~

代码/输出SHA及实际执行范围见[run-metadata.json](run-metadata.json)。新检查不是重跑230个LP或原七输入main；原探针/规范solver/优化器调用0。

## 两项成熟证明直接复用

K5的1740B代码无main guard，导入会覆盖400B报告。当前原31/155、五根3、θ3、C5需求/覆盖成本3>2与现有完整解析证明一致，故只恢复代码与完整输出、比较字段，不为重复再执行。源报告“independent”是历史实现身份，不新增本轮外审。

known Markov的720B记录与既有24831客户严格分离的六count根、023目标和22428/22429福利全同。新CSP关系已完整读并重构必要充分性；known JSON却不是该CLI的输出schema，没有原驱动/argv，100 DFS/2拒绝按原报告保留，不伪称默认80例或本轮DFS复现。旧648/130776成功穷尽不重跑。

八件一一消费全部实际字段；四类对象分别是固定正深度客户锥、固定整数实例全集BI、计数统一实现决策和K5可信菜单覆盖。没有用其中一个成功替另一类的认证，没有从有限阴性得到一般六人half或交叠保险不可能性。
