# 原树导入/输入闭包与旧核验复用

5701B audit只标准库，parents[5]定位original根，固定读history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json。完整原路径保留可解析该输入；没有其它本地import。main只stdout，不写report。

相关旧auditor放在original/tests/audits，其parents[2]同样为original根，读同一JSON；仅作既有SPE证明方法和同SHA报告复用。两源都只ast.parse、无导入或执行。原旧report以输入SHA be96cbb…和auditor SHA0fa3dd…绑定1885/22620事件，当前不补造其argv/exit/time或一次新stdout。

当前输入规范读取是数据解码而非策略真实性审计：weights全正、mask全域、policy完整有序域、compact重建等都不能代SPE IC。真正旧SPE身份依既有完整核验记录和其原源码，当前新Ψ/Z/G仍为769B旧字段，不冒当前重算。
