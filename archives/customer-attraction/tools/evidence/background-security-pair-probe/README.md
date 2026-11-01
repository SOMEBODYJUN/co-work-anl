# 合法背景首两人探针：原件与两次新证据

正文：[合法背景首两人安全比的有限探针与三个取等点](../../../state/程序/合法背景首两人安全比的有限探针与三个取等点--程序.md)。四primary合5639B，均全文实读；[source-manifest.json](source-manifest.json)保两冻结提交、SHA、原字节和实际旧模块依赖。

- [original/background_pair_probe.py](original/background_pair_probe.py)：3943B原探针，动态导入4073B旧BackgroundSolver。旧模块只复用[已有同SHA原件](../coverage-step-background/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py)，不另done或运行其随机main。
- 三原JSON：[6_3](original/background_pair_best_6_3.json)、[6_4](original/background_pair_best_6_4.json)、[7_5](original/background_pair_best_7_5.json)。每表12字段全部保存；q为目录，r为剩余人数。trial3/2/11不是总运行数，原记录无历史完成日志。
- [run_saved_points.py](run_saved_points.py)是本次实际执行包装的原字节；[replay/execution.json](replay/execution.json)记录唯一受控事件。每保存输入一次原BackgroundSolver/minimum_pair/security，合3新实例递推、3LP、0原main/0随机trial；逐输入初始化前清方法缓存。旧函数没有改源码，只被动包装linprog捕获实参与res；新提取器恢复完整有序σ。
- [replay/saved-point-capture.json](replay/saved-point-capture.json)720777B保全部1086计数状态、644终局计数、1932实际出现主题支付、3103历史动作及门槛/原返回。这里“1932”是独立后核的出现主题条数，捕获支付表还包含未出现主题辅助值。[replay/lp-capture.json](replay/lp-capture.json)76424B保三LP全部矩阵和实际浮点结果。stdout/stderr均空，是非main函数调用的实际输出。
- [audit_saved_points.py](audit_saved_points.py)是唯一独立定义级审计；[exact/execution.json](exact/execution.json)保存其输入/脚本/输出指纹。它不import原程序、不用BI/LP/RNG；展开291单位客户，核纯对手3行19查询及完整策略的21419含自身动作比较。原capture是它的策略输入，支付及比较按客户定义独立重算。
- [exact/exact-audit.json](exact/exact-audit.json)给三个纯鞍点、精确v与P_min；[exact/full-history-ledger.json.gz](exact/full-history-ledger.json.gz)265054B保全部逐历史两分支、支付与有理余量。三个恒动作策略全历史严格，正文给公共客户取消的不依枚举证明；有限核只证本三个输入，不恢复一般背景的首对桥。
- [comparison-manifest.json](comparison-manifest.json)与[review-record.json](review-record.json)保完整阅读、版本差、后继反例、逐源去向及运行边界。[artifact-manifest.json](artifact-manifest.json)和[self-check.json](self-check.json)仅为静态完整性证据；[check_package.py](check_package.py)不导入或执行数学脚本。

原事件elapsed0.9353758559882408秒；独立事件elapsed0.6945005250017857秒。原pipeline每点pair/witness/v/p/ratio字段与旧表一致，但没有生成或声称逐字重放旧随机trial的JSON。各原新小数均未改；第三点decimal与binaryfloat相对真值的误差甚至异号，精确等号由显式有理鞍点和策略证明承担。

两个执行脚本保的是**实际执行版本**：路径常量及事件内绝对scratch路径属于原事件身份，未倒写成新路径。事件中的basename可由本目录原件/脚本/捕获和source-manifest定位到同字节；静态checker逐一验证。脚本有输出目录已存在即拒绝的保护，直接在本保存包里执行不会覆盖证据。若未来要新复现，应另建隔离目录复制脚本与原输入，并核对/调整仓库路径，生成独立新事件；本轮没有因此重跑。

与同批[目标终局控制器锥程序](../../../state/程序/带目标终局控制器的首对安全值锥探针--程序.md)、[三个锥点及微小IC误差](../../../state/计算/首对安全值锥的三个保存点与微小激励误差--计算.md)区分：它们改变了客户质量，使用不同三份表；不借本三点的严格唯一SPE认证其数值锥点。后继PB大背景反例已否定本普遍辅助桥，原模型根half与实际前缀可达性另论。
