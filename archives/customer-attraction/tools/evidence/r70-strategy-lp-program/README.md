# 六人七主题固定策略LP证据

[正式程序正文](../../../state/程序/六人七主题固定完整策略的福利比线性规划程序--程序.md)完整保全3577B主源1ee3fd3da1dc3b243cc8。模型是完整有序策略的客户重数锥，六人七标签的七个遗漏支持恰给OPT₆归一；其它n不能自动继承六人福利比。正文定义全部变量、IC与LP，并列新增证书全部21条真实IC及七组正乘子。

- [original/strategy_lp.py](original/strategy_lp.py)：未修改原主源，SHA6c2162c4d99e8c4b168e679f20beab5c68faf1e798fadacc46af7105fa9479b4。
- [original/spe_dp.py](original/spe_dp.py)：实际6396B本地依赖，主源另由配套代理处理。
- [原random输入](related/random_best.json)、[原LP输出](related/lp_best.json)：均全文读取，数据主源由配套代理处理。[来源清单](source-manifest.json)保四原件提交、路径和SHA，不把相关文件额外done。
- [comparison-manifest.json](comparison-manifest.json)：七份模型/锥/完整菜单/七极大口径/根入口的实际比较绑定。

[replay_main.py](replay_main.py)将原件复制至新隔离目录，runpy执行原main一次；标准库profile只观察返回值，不替换helper或增加求解。此次1solve(witness)、1constraints、1matrix、1optimize、7linprog；exit0，8.746459276秒。未跑原verify、随机历史或其它n。完整[执行记录](replay/execution.json)、[进程捕获](replay/process-capture.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)均保存；源/依赖/输入前后SHA相同。

原事件保留：

- [dp-return.json](replay/dp-return.json)：W43、OPT58、root_outcomes6、1716状态。
- [complete-strategy.json](replay/complete-strategy.json)：19608个真实有序决策历史，entries为history/action对象；不是计数策略。
- [constraint-keys.json](replay/constraint-keys.json)：117648非自身比较去重后的3048个(a,q,b,r)键。
- [ic-matrix.json](replay/ic-matrix.json)：该次原3048×127 CSR，198672非零。
- [seven-lp-results.json](replay/seven-lp-results.json)：7次真实OptimizeResult及传入目标、归一化、矩阵指纹；原旧JSON不含这些信息。
- [optimize-return.json](replay/optimize-return.json)和[lp_best.json](replay/lp_best.json)：原函数结果与原main序列化；后者1423B逐字同冻结旧输出。

[audit_fixed_cone.py](audit_fixed_cone.py)为独立标准库新核，仅执行1次，不导入原源码、不调用DP/LP、不重复两点收益审计。它从完整σ重建全部历史到键的映射及387096系数，再将七浮点对偶作为候选恢复、精确核889列。[exact-cone-audit.json](exact-cone-audit.json)保存全部有理非零乘子及127列余项，每组最小0。omit0/2下界6/11，其余下界3/5；七覆盖上界乘子全0，故直接有W−βC−ΣμG≥0。

[配套数据](../r70-six1-best-data/README.md)独立认证同一σ的58客户点及清分母11客户点；后者W6、OPT11。与七个下界合并，才得到**本固定σ的全部非负重数锥精确最小比6/11**。这不是全体σ的六人half证明或反例。7个标签在两点均有同覆盖重复；精确小数缩放与IEEE二进制值分别说明。共享[绑定文件](shared-audit-binding.json)保独立核验身份，本包不重跑。

复现原保存点到新目录（会重新求解，仅作接续命令，本轮不重复执行）：

```sh
python3 -B archives/customer-attraction/tools/evidence/r70-strategy-lp-program/replay_main.py --source archives/customer-attraction/tools/evidence/r70-strategy-lp-program/original/strategy_lp.py --dependency archives/customer-attraction/tools/evidence/r70-strategy-lp-program/original/spe_dp.py --input archives/customer-attraction/tools/evidence/r70-strategy-lp-program/related/random_best.json --run-dir /tmp/r70-strategy-new-run
```

[execution-scope.json](execution-scope.json)区分原运行、新独立证书、共享点审计与未运行项。[check_package.py](check_package.py)仅做字节/结构/JSON与AST/链接/回执、捕获CSR与七调用绑定检查，不重做数学入口；[artifact-manifest.json](artifact-manifest.json)和[self-check.json](self-check.json)保最终交付。
