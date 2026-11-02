# 新末菜单价格与指定实际路径的两份原审计

三primary共4253B，均全文读取并按双冻结inventory核size/SHA；原件在frozen-inputs，完整定位在source-manifest.json。

- 新末菜单有理审计：1592B标准库代码和719B严格分离记录；正式对象在state/程序/新末菜单普通价格的有理审计--程序.md，既有价格资源追加读取时序。复用同SHA5259完整点已有成功七行精确检查，不重跑母矩阵。
- 指定实际路径阈值审计：1942B代码；正式对象在state/程序/指定实际路径的全续局阈值审计--程序.md。依赖已正式归档bigint_controller_attack/full18_cone；Rdiag原seed、历史六层报告和独立18×18末两人审计均已有，不重复完整BI。

本次verify_recovery.py只核三源字节、JSON与已有精确summary对应、标量减法，以及按Rdiag完整252类型直接计算六条记录的实际收益与所报floor终局见证收益；全部PASS。它不认证历史floor的全续局最优性、retention布尔或完整SPE。原程序调用0、BI0、LP0。verification.json保完整实读/计算范围。

复跑恢复核验可用`python3 verify_recovery.py --repo <结果仓库> --sources frozen-inputs --out <新输出>`；不应把该恢复核验称为原审计重放。原程序若另行执行，须按正式对象的路径/副作用说明使用隔离副本。

关系审查见relation-review.json；本批只交第二阶段正文与资源，未把引用自动导入超图。
