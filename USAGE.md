# 运行算法：先核对数学条件

从仓库根目录以 Python 3 运行规范包，不需要第三方依赖。每个命令对应不同的问题；[规范模型](research/current/model.md)规定客户成本与延续选择，[命题登记](research/current/claims.md)记录结果状态。此仓库没有选定公共许可或稳定的安装式 API。

| 所需结果 | 额外输入条件 | 运行命令 | 输出含义 |
| --- | --- | --- | --- |
| 共同目录的普遍 \(\phi\) 构造 | 两家选同一非空目录，可省略 U1/U2 使用全部地点；正有理权重；独立混合精确客户 NE | python3 -m facility_spe.shared_phi examples/shared/tiny.json --output certificate.json | factor 不超过 \(\phi\) 的一个实例证书，非实例最优 |
| 异构目录的普遍 2 构造 | 分别给出非空 U1/U2，可不同；选纯精确客户 NE | python3 -m facility_spe.heterogeneous_two examples/heterogeneous/tight_two_M1000.json | alpha 不超过 2 的一个实例证书 |
| 整个实例的最优因子 | U1/U2 均明确给出；接受对最大公共客户数 \(\kappa\) 指数增长的时间 | python3 -m facility_spe.exact.bounded_overlap examples/heterogeneous/tight_two_M1000.json | 支持区间完整枚举的最优 alpha；短证书独自只证“达到” |
| 至多单交叠的实例最优因子 | 每个跨目录地点对最多一名共有客户 | python3 -m facility_spe.exact.single_overlap examples/heterogeneous/rho_lower.json | 特定输入的最优 alpha；普遍 \(\rho\) 还需一侧目录至多两地点 |
| 共同目录的指数精确比较 | 全部地点可供两设施选；接受指数时间 | python3 -m facility_spe.exact.mitm examples/shared/tiny.json | 实例最优，用作小规模比较 |

输入 JSON 的 weights 为正整数、精确分数或小数字符串；locations[j] 列出地点 j 覆盖的从零开始的客户编号。共同目录程序要求 U1/U2 同时省略，或二者给出相同非空地点集合。其他两个目录程序要求两者都出现。命令行读取 JSON 小数时保留精确十进制；Python API 不接受二进制 float 作为权重。空地点和不被任何地点覆盖的客户可以存在。

例如：

    {"weights":["1/3",2,"0.125"],"locations":[[0,1],[1,2],[0,2]],"U1":[0,1],"U2":[1,2]}

这个例子属于异构模型，不能直接交给共同目录程序。它没有退出选择、距离、设施开设费、容量或第三设施。

## 证书检查与所不能推出的结论

共同目录的输出使用 factor、common、prob_first、loads；异构四种子使用 alpha 与纯概率；支持枚举程序也用 alpha，但可以有真混合概率且把共同客户字段命名为 shared。不要将一种证书传给另一种验证函数。

共同目录可用以下命令复查**该输入**：

    python3 -m facility_spe.shared_phi examples/shared/tiny.json --output certificate.json
    python3 -m facility_spe.cli.verify_phi examples/shared/tiny.json certificate.json

验证器从输入重算客户负载、每名客户的精确最优反应以及每个**实际**设施单方偏离的不等式，允许将未列出的布局交给规范的受保护纯修复规则。它调用构造器内的同一个验证函数；自由文本 default_continuation 和响应环等解释字段不受验证，因此尚不是另一份独立实现的证明检查器。对 EXACT-KAPPA 的 verify 函数同样只验证达到的倍率；“最优”来自算法的完整谱枚举证明。

所有普遍上界仍是内部审读的研究候选，详细未独立闭合的步骤在[共享证明](research/current/shared/proof.md)和[异构证明](research/current/heterogeneous/full_catalog_cycle.md)明确列出。把可核查实例证书用于满足模型的研究数据是当前直接可做的事；不能据此声称算法已通过外部证明认证。

## 回归入口

    python3 -m tests.test_shared_phi
    python3 -m tests.test_four_seed
    python3 -m tests.test_heterogeneous
    python3 -m tests.test_lazy_ring
    python3 -m facility_spe.exact.threshold_dp
    python3 research/build_map.py --check
    python3 research/check_assets.py

测试默认不覆盖[evidence/runs](evidence/runs)中的冻结记录。各个数学保证、实际运算界和详细来源见[研究资产表](ASSETS.md)。
