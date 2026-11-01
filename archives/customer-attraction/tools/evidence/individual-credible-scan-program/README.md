# 有限实例目录逐人门槛扫描器

主源 `f5f61df5ae7393a46e41` 为 [473B 原入口](original/scan_individual.py)，数学与软件合同见[程序正文](../../../state/程序/有限实例目录的逐人半覆盖门槛扫描程序--程序.md)。它调用规范精确纯SPE终局集合算法，测试 `2*m*min_actual_player_payoff < OPT_m`；这只是逐人half充分加强的失败，不自动是总福利half反例。

## 本次保存内容

- [input-scope.json](input-scope.json)完整保22份冻结JSON的解析数据、源提交/size/SHA和已有字节保全路径，共36542B；19份顶层合法且满足尺寸限制、2份超限、1份嵌套包装跳过。这是静态分类，不是执行结果。
- [原同目录README](related/credible_counterexample_README.md)保其padding税桥及复制失败的研究语境，不将整个目录名当本扫描器的输出结论。
- [source-manifest.json](source-manifest.json)绑定原源、四规范依赖、22个输入和实际比较材料；[execution-boundary.json](execution-boundary.json)明确0新入口／import／DP／OPT／LP及无历史完成记录。
- [self-check.json](self-check.json)只核原字节/blob、AST、JSON、字段表、实际链接和回执，不导入或运行原程序。

## 已读依赖与不重跑的理由

规范 `customer_attraction` 的四模块共25475B：`__init__.py`加载model、exact、certificate；本源实际只调用Instance和ExactSPESolver，不调用完整证书展开。四份全文实读并与原库存SHA绑定，复用[规范原实现及11项测试](../../../state/计算/完整历史求解器的精确复现--计算.md)和[全部纯SPE递推证明](../../../state/算法/完整历史纯SPE终局全集--算法.md)。其209小输入／14094完整策略oracle是旧成熟证据，不计作本次运行，不当成这22文件的扫描报告。

473B入口逐行可确定其目录、过滤与输出行为；现有语料及规范算法已有成熟保全。本次选择全静态整理，不再次扫描19个游戏，也没有为了复现已知零人错误或证明空目录静默而执行额外入口。因此没有把未执行说成成功，没有新增负结果或真实新反例。

## 运行合同及重要边界

入口无main护栏、无CLI解析器，导入也会扫描。输入路径取运行CWD下 `examples/customer_attraction/*.json`，不递归、未排序；脚本所在目录无关。若未来重放，须在隔离CWD放入明确清单的合法顶层实例，并提供manifest中同SHA规范包，记录是否正常结束及各跳过原因。当前保全原件没有新增这些功能，也没有提供一个被误认为已执行的重放命令。

`Instance.from_dict`不解包报告的instance；零人虽被规范模型允许，但源在try外对空的已占标签集合取min而失败。正人数零客户则正常为零且不触发严格不等式。所有真实重复主题覆盖、重复行动及弱平局保留，不能为避免上述问题暗改模型或原字节。

当前一般逐人 `OPT/(2m)` 命题已由[银行完整SPE反族](../../../state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)否定；m5的20标签超出本源7标签上限，W10/OPT13仍满足half。现有文件名中含security/tax/failure，亦不意味着它们必命中本源特定的严格(TEST)。本目录不声称22文件在历史某次CWD全部出现、19文件曾完成阴性扫描或有限子域的一般定理。
