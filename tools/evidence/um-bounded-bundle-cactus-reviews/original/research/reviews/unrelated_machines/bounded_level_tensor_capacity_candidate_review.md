# 固定层共同上容量的整数张量逃逸：候选源接口实审

最终实际全文为 `research/questions/unrelated_machines/bounded_level_tensor_capacity_escape.md`，SHA256 `8812cf5487a05ff72b322e2e18dccf295452fb4c0a9910faa5cb34d5d8c7ce53`。候选身份仍 `UM-TENSOR-JOINT-GUARD-ESCAPE-q1`，不进入 canonical Claim/graph；没有 actual UM 归约或一般算法困难性结论。

## 独立顺序和数学判断

`hardness_route` 先构造随机共轭证明与显式 L2,t4 例，root 另行重构后保存候选。`cover_consistency` 随后只收到精确 guard 合同，未读上述证明，先独立构造 complete linear mapping 和低支撑码证明；盲稿 SHA `457a0ba7542607a5a541e44f256ab65d8d3a5f3643137ab36902e6da42d48d77`。冻结后才实际读旧稿 `02720b8c2028fe4ffe2e0482fd7181af60baddac8467393295c1742356b247a5`，再实际读取上记最终全文。最终读后报告 SHA `2889066d5072a7593a25a8abb8bdbb7e8c5e3e79e721cf01fcd2ba316e3b3df1`，没有把旧稿 hash 冒作最终读取。

在精确源乘积合同内，没有尚成立 fatal objection。实际核过：parity base 的整数 ν1、每边1/2的 fractional perfect 证书；YES 的任意 base 完美匹配乘积确满足每个共同上容量；B、I+B 的可逆性，Bᵀ 的共轭对称；低支撑坏关系计数和 union bound；多个轴落在同一层时先选一轴，额外指定只会缩小 fiber；全长三轴双射给任意单轴 prefix exact。不存在把分别的 guards 见证错合成一个共同 F：证明构造的是同一个全局 F。

独立证明还给一个明确的充分维数选择 t=6L：非平凡坏对数至多

\[
\sum_{s=1}^L {6L\choose s}(3^s-3)
\le 9^L(4/3)^{6L}
=(4096/81)^L<62^L\le 64^L-2.
\]

各坏事件概率为 1/(2^t−2)，故 union bound 严格小于1。构造者正文用较粗的 Σbinom(t,s)3^s 也同样充分；无需修改原存在性结论。行向量与列向量约定相差转置，不改变共轭类或坏对计数。此明确选择仍不等于给出了按输入 t,L 位多项式寻找成功共轭的算法。

显式 B 的 B²=I+B、12 个非零互异 forms、16 点表、28+294 类 guard family 及三层反例 X₁+X₂+Y₃=0 均在数学上核过。独立审查者没有运行或审计程序，不将下段 root 的软件核验归到其名下。

## 实际代码和有限证书范围

root 亲读72行独立程序并实际重跑，源 SHA `695324d5b1dd689cba7059f4003b8ccf74fd9b797ca1bd3314af4f87335359b1`，冻结输出 SHA `fe42110a2b0f603abaf5d0a5b28094b452a14b95de5056545fdaee135ff81bbb`。只对同一给定 B /16条整数边核全部322类一/二层多轴测试、12类单轴 prefix、54类 pair 资源的912个不重复 clones，并明确该 B 失败一个三层 guard。没有随机扩样、通用 matching/LP oracle或实际调度矩阵。

一般 L 由上面的全称数学推导承担，不由这一个 L2 实验承担。外审、新颖性、统一位多项式构造、受限 PCP 源族以及实际 source-to-UM 转移均未认证。真正 joint-prefix functional association 和 root 乘法计数尚未实现，所以该候选不能升级为近二困难性。

入口：[候选](../../questions/unrelated_machines/bounded_level_tensor_capacity_escape.md)、[精确代码](../../../tests/audits/unrelated_machines/bounded_level_tensor_escape.py)、[冻结候选输出](../../../evidence/runs/unrelated_machines/bounded_level_tensor_escape_candidate.json)。
