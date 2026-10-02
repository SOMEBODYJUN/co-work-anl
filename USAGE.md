# 运行算法：先核对数学条件

从仓库根目录以 Python 3 运行规范包，不需要第三方依赖。每个命令对应不同的问题；[规范模型](research/current/model.md)规定客户成本与延续选择，[命题登记](research/current/claims.md)记录结果状态。此仓库没有选定公共许可或稳定的安装式 API。

| 所需结果 | 额外输入条件 | 运行命令 | 输出含义 |
| --- | --- | --- | --- |
| 共同目录的普遍 \(\phi\) 构造 | 两家选同一非空目录，可省略 U1/U2 使用全部地点；正有理权重；独立混合精确客户 NE | python3 -m facility_spe.shared_phi examples/shared/tiny.json --output certificate.json | factor 不超过 \(\phi\) 的一个实例证书，非实例最优 |
| 异构目录的普遍 2 构造 | 分别给出非空 U1/U2，可不同；选纯精确客户 NE | python3 -m facility_spe.heterogeneous_two examples/heterogeneous/tight_two_M1000.json | alpha 不超过 2 的一个实例证书 |
| 整个实例的最优因子 | U1/U2 均明确给出；接受对最大公共客户数 \(\kappa\) 指数增长的时间 | python3 -m facility_spe.exact.bounded_overlap examples/heterogeneous/tight_two_M1000.json | 支持区间完整枚举的最优 alpha；短证书独自只证“达到” |
| 共同目录的实例最优因子（异址参数） | U1/U2 同时省略，或二者为同一非空地点集；只对**不同地点**交叠人数 $\kappa_{\ne}$ 指数增长 | python3 -m facility_spe.exact.shared_offdiag examples/shared/sparse_four_rational.json | 最优有理 alpha $6327/4000$ 和全部实际偏离 NE；同址续局统一对半。单张证书只验证达到值，最优性依赖同址正规形 |
| 至多单交叠的实例最优因子 | 每个跨目录地点对最多一名共有客户 | python3 -m facility_spe.exact.single_overlap examples/heterogeneous/rho_lower.json | 特定输入的最优 alpha；双方目录任意长的普遍 \(\rho\) 结论另由 SPARSE-RHO-ALL 证明 |
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

`facility_spe.cli.verify_phi` 是只依赖 Python 标准库的独立检查器，不导入构造器、菜单或共用 NE 核心。它从原始覆盖集合直接计算每名共同客户选择两设施时的条件期望成本，检查概率端点与真混合的精确最优反应，重算两家负载，并要求每个**实际**单方偏离恰有一条证书。所有比较用有理数；`factor >= 1` 与 `factor² - factor - 1 <= 0` 精确检查黄金比界，包括在轨收益为零的情形。Python 调用不接受布尔值或二进制浮点数充当权重、概率、负载、倍率或索引；CLI 保留 JSON 十进制数的精确值，并拒绝重复 JSON 字段与非有限数。输入覆盖列表与目录中的重复索引按集合规范化，与构造器一致；证书共同客户列表仍必须排序且唯一。

默认续局字段必须精确等于 `guarded_repair of all common customers at facility 1`。检查器对每个尚未列出的**带标签布局**自行复算该规则：共同客户先全部到设施 1；当其负载较大时，将仍在那里且权重严格小于负载差的最大权重客户移到设施 2（并列取最小客户编号），首次负载反转或无人严格改善即停止。它还逐个检查生成的纯策略满足上述客户最优反应。因此通过检查覆盖整个续局，不能任填默认规则文本。响应环、菜单威胁、菜单计数、`family` 与 `guarantee` 文本是解释信息，不受此检查器认证；通过只证明该输入达到所给倍率，不证明菜单极小性、实例最优性、普遍定理或运行时间。对 EXACT-KAPPA 的 verify 函数同样只验证达到的倍率；“最优”来自算法的完整谱枚举证明。

另一个冻结实例的在轨均衡使用三个真混合客户，可直接检查：

    python3 -m facility_spe.cli.verify_phi examples/shared/on_path_chord.json evidence/certificates/shared/on_path_chord.json

共享黄金比和异构因子 2 的普遍上界均已有完整成文主稿与内部审读，尚无外部同行评审。[共享证明 Markdown](research/current/shared/README.md)已将 G1–G3、L1–L2 分支重写到对应页并进行内部逐式核对。把可核查实例证书用于满足模型的研究数据是当前直接可做的事；证书只核验所给实例。

## 回归入口

    python3 -m tests.test_shared_phi
    python3 -m tests.test_shared_offdiag
    python3 -m tests.test_verify_phi
    python3 -m tests.test_four_seed
    python3 -m tests.test_heterogeneous
    python3 -m tests.test_lazy_ring
    python3 -m facility_spe.exact.threshold_dp
    python3 research/build_map.py --check
    python3 research/check_assets.py

测试默认不覆盖[evidence/runs](evidence/runs)中的冻结记录。各个数学保证、实际运算界和详细来源见[研究资产表](ASSETS.md)。
