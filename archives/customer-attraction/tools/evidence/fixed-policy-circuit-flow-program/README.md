# 固定完整策略收益回路探针的程序合同

主源 `12d7027e518db2af3c07` 的完整解释见[程序正文](../../../state/程序/固定完整策略收益回路的非负流探针--程序.md)。本目录保存阅读、接口和静态绑定；公共[7066B原件](../fixed-policy-circuit-flow/original/circuit_flow_probe.py)、[25150B原证书](../fixed-policy-circuit-flow/original/circuit_flow_certificate.json)与所有数学执行只在相邻公共目录保存。

程序固定三人、六标签、43个有序决策节点、根路径034与单一比较124；126个非负收益是抽象坐标，不是63类共同非负客户变量。2778条非负行由258真实形式IC和2520同题稀释组成；105条零等式由45完整二主题关系与60条4/8/1六收益式组成。正文给每类行的证明、两个LP的完整符号和有理拒绝条件。

第一次LP用浮点HiGHS发现，再以Fraction核原始可行、对偶可行和同值8/5。第二次固定该β，用3114个变量最小化系数总和，寻找一个分解；没有精确证明该辅助成本最优，更没有最少支持证明。最终证书是 βr−o=Iᵀμ+Cᵀθ+s，μ,s非负而θ有符号。原始达到点违反次模性，不能变成原游戏反例。

## 共享的两类实际事件

[原main事件](../fixed-policy-circuit-flow/replay/execution.json)由[透明包装器](../fixed-policy-circuit-flow/run_original_once.py)在新隔离目录运行未改源码一次，只读profile观察两LP。13.223秒，两次success；断言开启，stderr空，原件前后SHA相同，新25150B报告逐字等冻结报告。它没有修改原函数或矩阵，也没有第二次原main。

[独立核验器](../fixed-policy-circuit-flow/verify_certificate.py)只用标准库，从定义重建行并解码原稀疏证书，不导入原程序或优化器。[核验结果](../fixed-policy-circuit-flow/exact-certificate-audit.json)检查64个含空客户模式、6720恒等式、161280稀释、2778原始不等式、105等式、126对偶坐标和次模余量−8/15。新报告与旧报告同字节，只绑定一次，不增加相同证书的数学核验次数。

本程序整理者完整读取上述源码、126原始项、22非负乘子、28有符号乘子、空坐标余项和审计脚本/结果；不执行任何原main、LP或独立矩阵重建。[source-contract.json](source-contract.json)记录源码作用域与两阶段符号，[source-manifest.json](source-manifest.json)绑定共享原件/事件及实际阅读的数学来源，[self-check.json](self-check.json)只核SHA、JSON/AST、链接和回执。

## 数学依赖与后续用途

全文读取[13242B背景原稿](../fixed-background-circuit-basis/original/fixed_background_circuit_basis.md)含完整附录及[3390B后续审查](../fixed-background-circuit-basis/related/fixed_background_rank_review.md)，以M2、k1的六收益式对接当前60行。[完整二主题纠错](../../../state/定理/固定完整策略的二主题耦合二倍界--定理.md)说明旧15/7遗漏第三关系；[七层严格间隔](../../../state/障碍/同支持守恒与局部客户耦合的严格间隔--障碍.md)区分共同signed与共同非负表示。原码已经加入第三关系，不能按旧两差式给它降格。

配套[数据正文](../../../state/计算/固定策略的共同客户收益回路与八比五证书--计算.md)承担完整证书和次模诊断；程序正文自行给出可接续的行定义与弱对偶证明。现有8/5只认证这一固定策略与比较的抽象系统；没有一般策略、全部比较、六人half或真实客户锐性结论。若换系统，需要重新记录新行、运行与证书，不能复用本数值替代证明。本阶段只作解释和相对链接，不另写关系图。
