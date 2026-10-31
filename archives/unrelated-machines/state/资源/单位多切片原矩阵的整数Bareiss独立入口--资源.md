---
id: c2-unit-multislice-independent-bareiss-entry
kind: resource
type_tag: 资源
title: 单位多切片原矩阵的整数Bareiss独立入口
status: integrated
truth_status: exact-finite-PSD-and-nonPSD-audit; general-proof-separate
review_level: full-primary-read-and-frozen-output-identity
summary: 保存独立四阶矩阵的全部基、Boolean矩公式、整数消元及m2失败字段语义；m2的rank4仅是正pivot阶段数。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/c2_unit_multislice_independent.py
---

# 原入口及其有限数学输入

[原件](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/c2_unit_multislice_independent.py) 2181字节，SHA `b12850596bb79361d58803866e5ba29c9366dcf57e98929d561d86fca005b262`。只用Fraction、combinations/product、lcm和json；不导规范代码，无CLI、外部数据、seed或浮点容差。main固定对m=2,3,4调用audit，不能把它当任意输入的SDP可行性程序。

令n=m+1、t=n/m，任务j选机器a的Boolean变量为x_(j,a)。基含常数、全部nm个一次项、每个不同任务对的m²个兼容二次项，维数1+nm+binom(n,2)m²。给两个基项合并literal：同任务不同机返回0；相同literal按Boolean合并。若相容并涉及k个不同任务，每机器出现数c_a，矩为

\[
y_S=\frac{\prod_{a=0}^{m-1}(t)_{c_a}}{(n)_k},\qquad (z)_h=z(z-1)\cdots(z-h+1).
\]

完整M2按每一对基项生成；实际k≤min(4,n)，所以m2/n3不调用分母(n)_4=0。代码不另检查one-hot/count/localizer等式，那些属于一般证明或聚合结果中的另一主程序；不能把其他字段的700/4105等检查计入本独立入口。

# 整数消元逐步义务

先取全部Fraction矩条目的分母LCM，得到正整数scale及整数对称矩阵A=scale·M2。prev初值1。每阶段先检查剩余对角有无负项，有则立即判非PSD并输出阶段/行/数值；否则选首个正对角pivot，同时交换该行和该列。对剩余r,c更新

\[
 A'_{rc}=\frac{pA_{rc}-A_{rk}A_{kc}}{\mathrm{prev}},
\]

并断言每项整除，再把pivot行列交叉项置零、prev=p。所有保留pivot正，故这是正缩放的Schur补/congruence，正性判断精确，无浮点特征值或容差。

若剩余对角全0，代码还扫描**整个尾矩阵**。尾全0才判PSD；若有非零非对角项，二维主块[[0,b],[b,0]]给一正一负方向，判非PSD。只看对角0不能通过。尾零时rank=k确为原完整矩阵rank；失败尾非零时输出键`rank:k`仅记已经取过的正pivot数，不能当整个失败矩阵的代数rank。`tail_nonzero`行列是消元/交换后的矩阵位置，也不直接等于原monomial标签。

# 真实旧结果和m2边界

[冻结结果](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/c2_unit_multislice_gap_audit.json)的independent数组与本代码SHA精确绑定，历史命令为`python3 tests/audits/unrelated_machines/c2_unit_multislice_independent.py`，Python3.12.14。本批复用这次充分真实执行，新增原入口运行0；旧记录无单独数值退出码或耗时，不补造。

| m/n | dim | scale | 实际结果 |
|---|---:|---:|---|
|2/3|19|16|非PSD；4个正pivot后全零对角尾部仍有非零(11,15)，输出rank4不授作总代数rank|
|3/4|67|243|PSD，16正pivot、尾全零，完整rank16|
|4/5|181|6144|PSD，61正pivot、尾全零，完整rank61|

m2的另一显式负平方可从同矩公式直接核：p1=x_(1,1)x_(2,1)，p2=x_(1,1)x_(3,2)，p3=x_(2,2)x_(3,2)，其Gram为

\[
\begin{pmatrix}1/8&3/16&0\\3/16&3/8&3/16\\0&3/16&1/8\end{pmatrix},
\qquad L[(p1-p2+p3)^2]=-1/8.
\]

这给自足非PSD证据；三项最小性及m≥3的一般完整分解已在[多切片一般PSD审查](../审查/C2多切片的一般PSD与最小边界负平方--审查.md)保存。本代码本身没有寻找该负平方，也没有独立运行m5。

# 与一般C2合同及旧版本的关系

相同实例有n=m+1件单位作业、m台全可用机器，整数OPT2；四阶C2-load证书在t=n/m可行、比2m/(m+1)趋2。一般PSD来自完整常数/一次/对称harmonic/反对称harmonic张成和正交分解，不由三次有限消元外推。本合同没有三阶逐项非负、完整CONFIG或prefix localizer；同机三不同任务矩−1/m⁴，故不是概率分布。

旧聚合正文hash5fe91d…，最终规范hash96863e…仅修“C2不蕴含CONFIG”的范围句，两代码未改。本族CONFIG(t)不可行不能反过来证明CONFIG对所有输入可扩为共同M2，因此不称一般松弛全局支配。聚合中m5的dim406/rank171由原主线程另跑主程序，不能倒填本独立入口m2/3/4。当前资源补的是原矩阵与失败分支的真实实现；无新一般定理、通用SDP后端或一般UM困难性。
