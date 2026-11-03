# 最小缺口逐项与联合扫描证据

正式对象：[最小缺口攻击的逐项与联合扫描](../../../state/审查/最小缺口攻击的逐项与联合扫描--审查.md)。四primary完整原件位于original，六项比较依赖位于dependencies，冻结双commit定位、size/SHA256/blob SHA1及复用来源见source-manifest.json。依赖不另记primary done。

73条逐图报告有918目标/916份对偶，71图全部覆盖，m4p5 cone46与54各缺一个；联合报告保存四张21节点完整图及40份对偶。全部956份保存上界由新标准库检查器一次独立重建有序树、均分IC、原排序行序后核真：6949非零乘子、31748残差全非负，最大β=−1/4。verification.json逐条保原目标、β、残差最低值、完整图签名、节点/比较数和精确缺项。

复现只需Python3，在任意cwd运行verify_saved_duals.py；将更新本目录verification.json。不调用原main、LP/MILP、规范模型、网络或随机扫描。execution.json记录本次真实一次运行与哈希，后续运行若环境/程序变化应另存执行记录。

原报告未保逐目标原始客户向量；best字段只保原程序的历史恢复声明，字段与β相等不变成独立原始最优证书。联合MILP的浮点status0/gap0不认证全策略族上界。两个缺对偶目标没有被新优化补齐；本批没有MG或half反例。
