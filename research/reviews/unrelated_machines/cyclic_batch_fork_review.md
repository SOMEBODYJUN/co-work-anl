# 循环批量局部优化与分流槽反例的最终冻结独立审查

审查者：boss6 内部子研究者 algorithm_probe。先从精确合同独立重构并构造分流反例，再阅读本节冻结的规范全文及实现；没有把同意票当证明。未作外部同行评审或全球新颖性认证。

## 1. 实际冻结范围

独立推导基准：`957f04bcdc4dfd0723c8211559ced4c0be988127`；最终入库前基准：`47fc71d61cfce748a96da09d2caea178b32b36b1`，相关冻结字节不变。以下为未提交工作树精确字节SHA256；审查定位依赖文件hash，不假称当前HEAD已包含新增正文。

|文件|SHA256|
|---|---|
|research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md|62169ac26f4e7212cbdf5a2e36c4880bcf58612974e95e4e70d44ade1b11b886|
|tests/audits/unrelated_machines/cyclic_batch_repair.py|47dbed9b77a7ec7e3c12f30a7110adb398ec6d96197ab0b642457584dba8a057|
|examples/unrelated_machines/padded_fork_k2.json|2f58763b5fddfa1eaa394a652359154d56fa7ab69a0f7e7d4c138b3bbc64d3fd|
|evidence/certificates/unrelated_machines/padded_fork_k2_certificate.json|c847f22c0ad3998ed33207f6579d18791e0cbbf52f7877133311ed3711633f07|

审查全部正文、全部规范程序。末两JSON实际读取并核对为uniform-current a版，与独立k=2矩阵和分数值相符。

## 2. 逐项承重结论

1. **E_T与输入身份。** 定理只处理初始σ在p≤T边上、load≤2T的给定合法调度。实现先验证实际分配，再拒绝超T的当前边；每轮候选也筛p_vj≤T。因此终态没有鲁棒循环的范围精确为E_T，不是全体任意大边。
2. **显式菜单提取。** SCC严格弧判据正确。λ=0不能把所有等号环误作改善；λ>0时任意可用转向严格。回程路径构成闭走步，重复机器剪接至少保留一条有余量/严格的分支。不同源机器保证真实任务不重叠，执行负载公式正确。
3. **精确状态DP。** 规范代码的收益状态是exact q，不是饱和q。`nxt=list(dp)`且回溯节点不可变，避免同一物品多次使用；零profit非负cost物品可跳过。总profit≤⌊4n/η⌋，代表cost不增、removal最多损失ηT/2的一般界成立。
4. **鲁棒完备性。** ηT真实循环的每条outgoing removal≥ηT，因此代表q>0；各入出替换后至少留ηT/2，整个循环同时兼容。不能把不同单机代表的分别可行误作共同调度：这里共同性由原machine-simple循环的不同源机器严格提供。
5. **总迭代与位复杂度。** 每次ηT/2循环全部参与机器均至少降该值，总工作量初始≤2mT、非负，故成功轮数≤⌊4m/η⌋。只声称固定η位多项式，η变量时关于1/η多项式；数值表示由原加工值的有限子集和控制。纯“strict下降”版本不获得此轮数界。
6. **批量支持反例。** 全负载初始2使排序lex改善等价于各load≤2且至少一处<2。计数式、最小支持k+1、最小单机最大迁出数k和达到例均正确。不能把达到例写成严格makespan下降或达到OPT。
7. **uniform核心。** OPT=1下界必须用b与其唯一私有任务同留会超1，而不能说min p_bj=1。正文采用正确下界。分流与合流必要性成立。其assignment LP唯一最优点的消元不等式及两处分子因式分解均独立重算正确。
8. **padding与唯一最小成本机器分配。** 全矩阵、新x、当前和最优分配、真实sorted槽注入均成立。正支撑每job当前边严格最便宜，所以所有minimum-cost槽匹配诱导同一坏σ；槽级matching本身未必唯一。H入负载超过C恰θ/2，因此所有makespan≤C修复不能利用padding，one-destination反驳保持，ratio趋2。
9. **关键限制。** A的两大任务质量和2t>1，故x不可能是T=1配置点投影。未证明x为基本点。只否定任意给定assignment-LP点+minimum-cost槽匹配+one-destination非增repair这一合同，未给UM-TARGET-v1的负答案，也不排聪明选x、配置派生x、多目的地共同交换或非单调过渡。

未发现上述精确合同仍成立的致命异议。不得把这一审查结论升级成主目标解答、外部评审或新颖性认证。

## 3. 实际独立计算与覆盖界

所有计算用Fraction，无随机浮点和优化器容差。

- 独立菜单重构先于规范实现审阅；规范存档为 `tests/audits/unrelated_machines/cyclic_menu_independent.py` 与 `evidence/runs/unrelated_machines/cyclic_menu_independent_audit.json`：3000个抽象菜单按全部机器简单循环枚举对照独立Floyd闭包与剪接。
- 最终uniform唯一成本padding脚本 `tests/audits/unrelated_machines/padded_fork_unique_cost_independent.py` SHA256 `25be7b639d34faa0eb9292c08e910d55027fed9cb4e4bd0a7624257ae5c4a538`；k=2,…,64共63实例、17010显式job→slot注入对，全过。冻结JSON `evidence/runs/unrelated_machines/padded_fork_unique_cost_audit.json` SHA256 `4b3b8e666e36e523fda4f3ce73b8366eea02b1249f5f15fe9810ab6c6b550874`。
- 独立k=2全矩阵/x/σ/OPT/slot已拆分成第1节所列实际输入与证书；其具体参数a=3/4,t=7/12,β=1/6,F=5/2，三核心分数负载7/8、各padding分数负载29/32。
- 最终主程序实际重跑到scratch，status passed：720显式菜单比较、86随机优化器输入、3边界与6非法输入，及fanout/ring/fork/padded停滞等其代码明确范围。
- 最终主程序冻结交叉攻击：seed613516，m=2,…,4，各1000份随机显式菜单，在λ∈{0,1/5,7/6}上共9000次独立机器simple-cycle枚举对照，3032次有改善循环，所有判定、不同源机器和余量检查均通过。实际代码 `tests/audits/unrelated_machines/cyclic_frozen_independent_crosscheck.py`，新记录 `evidence/runs/unrelated_machines/cyclic_frozen_crosscheck_reproducible.json`；完整参数与两份源码hash均在记录中。

这些有限计算只验证实际范围和实现对应，不承担一般证明。没有计算一般实例的近似比，也没有声称随机菜单覆盖所有调度来源的菜单。


## 4. 规范重跑命令与内容核对

在仓库根依次运行以下命令，重定向到scratch的新文件，不覆盖冻结记录：

```sh
python3 tests/audits/unrelated_machines/cyclic_batch_repair.py
python3 tests/audits/unrelated_machines/cyclic_menu_independent.py
python3 tests/audits/unrelated_machines/cyclic_frozen_independent_crosscheck.py
python3 tests/audits/unrelated_machines/batch_support_independent.py
python3 tests/audits/unrelated_machines/padded_fork_unique_cost_independent.py
```

主研究者实际重跑上述规范路径，结果与独立冻结范围一致。批量支持独立审计另包含Fraction逐任务k1..3、整数Gray逐任务k1..5，以及k7/31/127/503的全部压缩类型；压缩不是大实例全部逐调度枚举。旧核心探索未重复入库，最终数学对象以uniform-current正文及实际k2输入为准。
