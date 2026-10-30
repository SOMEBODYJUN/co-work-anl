---
id: "customer-attraction/iid-extra-query-exceeds-average-forced-payoff"
kind: "counterexample"
type_tag: "反例"
title: "三人八客户的同分布额外查询高于平均强制收益"
status: "exact-finite-counterexample-to-average-D-comparison; original-actual-u-scope-corrected"
summary: "完整31历史纯SPE和明确p给pᵀKp−pᵀD=13/1722>0，但pᵀKp−实际u=−839/574<0；保存原脚本一次运行、完整策略及单位客户定义级核验。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/diagonal_push_obstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/diagonal_push_obstruction.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/covariance_reset_criterion.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/relay/aggregate_extra_slot_gap.md"
---

# 三人八客户的同分布额外查询高于平均强制收益

## 被否定的比较及源范围纠错

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)的根，固定完整纯SPE。强制当前行动A后沿该策略得到包含根本人的完整终局Z(A)。定义D(A)为该根玩家在本分支的实际收益，K(T,A)为额外查询T面对Z(A)时的收益。矩阵K的**行是查询T，列是强制根A**；同分布独立抽A,T于p给G(p)=pᵀKp。

本例严格否定
\[
G(p)\le\bar D:=p^{\mathsf T}D\quad\text{对全部p成立}.
\tag{D-CAP}
\]
原脚本docstring和stdout的`scope`却称它否定G(p)≤实际根收益u，并将13/1722误叫G−u。实际代码计算并断言的是`quadratic-expected_d`，即G−\bar D。配套md开头也把被测加强式写为实际u，后文则已明确承认G<u；同目录协方差稿和后续`aggregate_extra_slot_gap.md`均正确收窄为平均D比较。本对象按实际有理量确定真值，原文件、错误范围文字和原stdout全部原样保存。

真实SPE激励仅给每个D(A)≤u，并不令\bar D=u。G>\bar D不能推出G>u。以下完整证书中
\[
G-\bar D=13/1722>0,\qquad G-u=-839/574<0.
\]
因此本例没有反驳全p实际u封顶、自由Mfull、路径Mpath、完整额外槽聚合预算Σ_iG_i(p)≤W或半覆盖。

## 八个不同单位客户与完整纯策略

三名单位提供者依次选择共同目录T0,…,T4，观察完整有序历史。八个单位客户的兴趣主题标签依次为
\[
\{3\},\{0,3,4\},\{0,1,3\},\{0,2\},\{2,4\},
\{0,3\},\{0,2\},\{0,1,2,3\}.
\]
两名兴趣为{0,2}的客户仍为不同单位客户，全部客户/提供者均非加权原子设施模型。主题覆盖两两不同。

第一人规定选0。第二人在首历史A=0,…,4后规定行动依次为
\[
(0,0,0,3,2).
\]
末位在每个有序二主题历史(A,B)的规定行动及最终收益为下表各格“行动；收益”。行是A，列是B；重复主题历史全部保留。

| A\B | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| 0 | 3；7/3 | 3；8/3 | 3；17/6 | 0；7/3 | 3；17/6 |
| 1 | 3；8/3 | 0；14/3 | 0；23/6 | 0；11/3 | 0；9/2 |
| 2 | 3；17/6 | 3；23/6 | 3；13/3 | 0；17/6 | 3；4 |
| 3 | 0；7/3 | 0；11/3 | 0；17/6 | 2；10/3 | 0；23/6 |
| 4 | 0；17/6 | 0；9/2 | 3；4 | 0；23/6 | 0；16/3 |

每格收益均等于该历史五个合法末动作的最大收益，直接按八客户最终覆盖者数核得。于是末层25节点均为最佳回复，不要求最佳动作唯一。再沿这份固定末策略检查第二人的所有行动：

| 首历史A | 规定B | 第二人分别选0,1,2,3,4后，执行原末策略的收益 |
| --- | ---: | --- |
| 0 | 0 | 7/3，2/3，7/3，7/3，4/3 |
| 1 | 0 | 11/3，2/3，7/3，8/3，3/2 |
| 2 | 0 | 17/6，5/6，11/6，17/6，1 |
| 3 | 3 | 7/3，2/3，7/3，7/3，4/3 |
| 4 | 2 | 17/6，1，3，17/6，5/6 |

每行规定B达到该行最大值。根的五个真实分支为
\[
(0,0,3),\ (1,0,3),\ (2,0,3),\ (3,3,2),\ (4,2,3),
\]
对应根原收益
\[
D=(7/3,2/3,7/3,7/3,1).
\]
规定根0同样最佳。末层、第二层及根的这些比较给31个有序决策历史全部124个非自身偏离；每人只动一次，逐层归纳即为完整纯SPE。所有对比使用该偏离历史后的真实规定动作，未冻结在轨后缀。

实际路径(0,0,3)的终局计数为(2,0,0,1,0)，三人收益均7/3，W=7。主题0,2,3覆盖全部八客户，所以OPT_3=8。原程序调用规范`worst_certificate()`选择此证书；反例只需要上述明确完整策略，有限认证不依赖它在其他所有SPE中的最差性质。

## 额外槽矩阵和明确分布

对每个分支Z(A)保留全部三位原玩家，另放查询T，逐客户计算
\[
K(T,A)=\sum_{x\in T}\frac1{1+c_x(Z(A))}.
\]
所得精确矩阵为
\[
K=\begin{pmatrix}
5/3&13/6&23/12&9/4&8/3\\
1/2&1/2&7/12&7/12&5/6\\
23/12&9/4&17/12&7/4&5/3\\
3/2&5/3&7/4&19/12&13/6\\
5/4&4/3&5/6&5/6&2/3
\end{pmatrix}.
\]
取
\[
p=(10/287,157/287,0,0,120/287).
\]
非负且总和一；直接有理乘法给
\[
G=p^{\mathsf T}Kp=1501/1722,\qquad
\bar D=248/287=1488/1722.
\]
所以G−\bar D=13/1722>0，证明(D-CAP)假。同时
\[
u=7/3,\qquad \bar e=u-\bar D=1265/861,
\qquad u-G=839/574>0.
\]
被省略的真实激励松弛大于此正去相关差，故本节点实际u预算仍安全。

按[根重置协方差引理](../引理/根重置对恒等式与辅助尾份额协方差--引理.md)再直接算得
\[
ER=20840/82369,\quad EJ=58789/247107,
\quad\tfrac12(ER-EJ)=13/1722.
\]
EJ使用正确的一次p_x无条件税系数。原错误平方系数会给8500463/70919709，不能代回恒等式。这些值验证正差的确属于同一真实分支的有符号重置账本，不是客户分母或矩阵方向的数值混淆。

## 原程序实跑、独立复验与复现合同

本轮在外部固定相对路径树，普通Python3.12.14、`PYTHONDONTWRITEBYTECODE=1`，执行原`diagonal_push_obstruction.py`真实`__main__`一次，原assert全部通过。未改原代码，也未把错误stdout范围改写为正确文字；原[stdout](../../tools/evidence/dynamic-flow-workspace/replay/diagonal.stdout.txt)及空stderr完整保存。Python profiler仅在原main返回时取已有局部变量，保存同一次求解产生的[instance和完整证书](../../tools/evidence/dynamic-flow-workspace/replay/diagonal-export.json)，没有为取证再次调用求解器。

真实依赖为规范包原四文件`__init__.py`、`model.py`、`exact.py`、`certificate.py`；四件均全文读并核冻结SHA。`exact.py`集合值逆向归纳与[既有全集算法](../算法/完整历史纯SPE终局全集--算法.md)一致：按计数缓存可实现终局集合，逐有序历史独立展开证书，不能说它只认证计数策略。规范verifier另遍历31有序节点、不调用全集求解器，原返回valid=True、checked_deviations=124。

追加的定义级复核从导出的原八客户和31行动重建每个真实子分支，按逐名单位份额算全部155项含自身收益（其中124非自身），独立重建K、D、p乘积与上述两种gap；不导入规范模型、solver或verifier。[diagonal-independent.json](../../tools/evidence/dynamic-flow-workspace/replay/diagonal-independent.json)保存每历史全部五行动收益、全部分支、根矩阵及前两层6节点共150个RESET对的逐项检查。它认证这一个有限证书，未运行随机搜索、非线性优化或全部分布搜索。

[统一复现器](../../tools/evidence/dynamic-flow-workspace/replay.py)还执行八人局部账本的原DAG核验一次；两个原入口和后加定义检查分别记计数，不合称两个独立求解器。其命令为

```sh
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/dynamic-flow-workspace/replay.py --run-dir /absolute/new-run-directory
```

复现器先核14原文件及完整来源指纹，复制到新目录，运行原入口并保存所有日志/精确对象，最终再核原文件未变；已存在输出目录直接拒绝。原代码含承重assert，须用普通Python。实际命令、绝对cwd、耗时、Python版本与日志SHA见[execution.json](../../tools/evidence/dynamic-flow-workspace/replay/execution.json)。本轮成功一次，保存或入库不再重跑。

## 数学接续与来源边界

八客户例排除的是“对所有p，将自适应根收益D无损换成同p的独立额外查询K”的强局部捷径。它保留当前u封顶、自由重选源Q和实际路径总支付的可能；W=7、OPT=8也严格满足half。原当前目标是任意有限单位客户、有限非空共同目录、**恰六**提供者的每份完整历史纯SPE半覆盖，本三人有限例不能替代该量词。

与[笛卡尔局部付款障碍](../障碍/根重置局部账本的笛卡尔放大--障碍.md)的关系是测试不同加强式：后者在e(A)=e(T)=J=0的一个根对上失败，本例在同分布平均上只超过\bar D；两个对象都不解决原目标。与[完整终局平均负载响应债务](../引理/完整终局推送的协方差响应恒等式--引理.md)的区别是本页先对真实整数分支取倒数，额外槽和原当前槽均保留。四主源共15063字节的身份、比较稿、原程序及全部证据见资源manifest；不以旧范围标签、程序PASS或多份相同来源表决真值。无外审或新颖性声明，关系已解释，超图留第三阶段。
