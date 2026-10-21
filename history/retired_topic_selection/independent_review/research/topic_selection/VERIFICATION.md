# 本轮选题资产的核验与复现

本页把工程、有限计算、内部证明审查和新颖性分开。原始候选记录共45条，包含跨线复核的同题，**不是45个互异开放问题**。结构审计检查了每条的精确范围、来源、文章类型和首个proof obligation；不自动证明来源事实或数学结论。

## 已实际执行的检查

| 类别 | 实际范围 | 准确限制 |
| --- | --- | --- |
| 统一程序工程回归 | work 23、checkpoint 47、board 27、collaboration 17，合计114项通过 | 本地隔离Git remotes；包括新分支首发、恢复、独立公屏、main不变、scope与凭据审计。不是数学验证 |
| 数学重放 | boss4在新临时目录重跑原子势/格外反证、Nash v2、跨线独立copies/rank2/K8、chores构造、goods独立标量检查及GAP模块审计；JSON逐项与冻结输出一致 | 重放范围明确，未把所有随机审计重新运行一遍 |
| 参数反算 | Fraction检验ζ=1/d,d=100,…,1000的预算差式及阈值不等式；显示公式另有代数推导 | 有限grid仍不等于全域证明 |
| 文献导入边界 | 单物品重量大于各bin容量而可分配的精确反例，枚举全部完整整数分配 | 只否定字面全覆盖子合同，不否定允许unused的BMKP定理 |
| 仓库登记 | catalog/map/crosswalk/assets/WC及旧main active-routing合同检查 | 旧active-routing校验保兼容；新题实际路由由显式branch/save/board及启动回执核实，不能混称同一合同 |

冻结汇总：[selection_validation.json](../../evidence/runs/topic_selection/selection_validation.json)。逐文件SHA-256见[artifact_manifest.json](../../evidence/runs/topic_selection/artifact_manifest.json)。第一阶段工程/导航checkpoint为 `8cc87ba84e429968e4acdc08f07c20b760015289`，不是数学突破。

## 数学脚本及证据

每条子线的代码统一在 `tests/audits/topic_selection/<line>/`，原始输出在 `evidence/runs/topic_selection/<line>/`。文件名与报告中记载一致；生成候选JSON的短期脚本未作为数学资产保存。

| 子线 | 可运行脚本 | 输出与含义 |
| --- | --- | --- |
| 原子博弈 | [toy_checks.py](../../tests/audits/topic_selection/atomic_games/toy_checks.py) | [输出](../../evidence/runs/topic_selection/atomic_games/toy_output.json)：改进环、短策略有限动态、有限LP势及格外失败；SciPy只提候选，证书用Fraction |
| Nash | [toy_checks.py](../../tests/audits/topic_selection/nash_equilibria/toy_checks.py)、[v2](../../tests/audits/topic_selection/nash_equilibria/toy_checks_v2.py) | [原输出](../../evidence/runs/topic_selection/nash_equilibria/toy_results.json)、[v2](../../evidence/runs/topic_selection/nash_equilibria/toy_results_v2.json)：单步恒等式/噪声/导数/宽3图证；旧版本未覆盖 |
| goods | [toy_checks.py](../../tests/audits/topic_selection/fair_goods/toy_checks.py)、[copies穷举](../../tests/audits/topic_selection/fair_goods/copies_exhaustive.py)、[独立核查](../../tests/audits/topic_selection/fair_goods/verify_frozen.py) | K8/K12随机估值、copies有限穷举与五个冻结极小证人数的纯标量重算；[标量结果](../../evidence/runs/topic_selection/fair_goods/independent_scalar_verification.json) |
| chores | [构造](../../tests/audits/topic_selection/fair_chores/construct_rank2.py)、[混合图](../../tests/audits/topic_selection/fair_chores/toy_search.py)、[扩展](../../tests/audits/topic_selection/fair_chores/mixed_extension_toys.py)、[partition-rank](../../tests/audits/topic_selection/fair_chores/rank_toys.py)、[真正rank-cap2](../../tests/audits/topic_selection/fair_chores/rank2_cap_toys.py) | 秩构造、图定向与带配额MMS；各脚本固定seed/域写在源头。三类触达数与rank cap2严格分开，不能混用 |
| 指派 | [toy_audit.py](../../tests/audits/topic_selection/generalized_assignment/toy_audit.py) | [输出](../../evidence/runs/topic_selection/generalized_assignment/toy_audit.json)：transversal例、pair穷举、joint交换、参数反算；不是完整BMKP算法实现 |
| 跨领域独立反方 | [toy_checks.py](../../tests/audits/topic_selection/cross_field_battle/toy_checks.py) | [输出](../../evidence/runs/topic_selection/cross_field_battle/toy_results.json)：9216 copies profiles、12825 rank2 word multisets、K8随机1000，独立实现整数检查 |
| 导入合同反例 | [complete_rounding_capacity_counterexample.py](../../tests/audits/topic_selection/complete_rounding_capacity_counterexample.py) | [输出](../../evidence/runs/topic_selection/complete_rounding_capacity_counterexample.json)：精确可分解与完整整数可行性区分 |

## 安全复现

这些探索脚本默认把新JSON写在脚本旁边。为保持冻结证据不变，复制对应子目录全部Python脚本到一个新的临时目录，在那里运行；无需改代码中的数学参数。`verify_frozen.py`另需把本线的 `toy_results.json` 与 `copies_exhaustive_results.json` 复制到该临时目录作只读输入。指派脚本需要临时目录中有 `evidence/` 子目录。Python依赖：标准库、NumPy；原子势LP另用SciPy。当前环境的Python/NumPy/SciPy/Git版本已写入selection_validation.json；原文命令与参数由各脚本/JSON给出；如更换版本，应重新核Fraction证书而非仅接受浮点LP输出。

工程命令为 `python3 -m unittest discover -s research/weighted_congestion_frontier/tests -p 'test_work.py' -q`，依次替换pattern为test_checkpoint.py、test_board*.py、test_collaboration*.py。不输出或读取凭据内容。

没有运行完整BMKP候选算法的通用实现；没有对连续估值域作SMT全覆盖证明；没有把任何有限样本当普遍真理，也没有认证新颖性。


## 同行加入的合并范围

保存时远端新增boss17的commit `f07dda4772575a9d0b777199e59206b696c9e2b1`。合并保留其原子精炼候选、两份审计/输出与个人工作区；双方比较表拆成带来源的入口，目录登记按路径合并后重新生成。同行材料不计入boss4的45条记录，也未追溯标为本轮六线已审。数学审计的成功只支持其明确有限范围。

同行的两份算术程序也已在合并后实际运行，标准输出解析为JSON，与原冻结结果逐项相等；这不替代其精炼算法的完整审查。
