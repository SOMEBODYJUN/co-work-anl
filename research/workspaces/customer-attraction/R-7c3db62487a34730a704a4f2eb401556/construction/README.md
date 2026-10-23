# construction 分支：共同公共核心与重复奖励尾的任意人数屏障

2026-10-23；未提交，由主代理统一 checkpoint。只写本目录，不改共享正文。

## 当前最强资产

[common_core_arbitrary_catalog_v2.md](common_core_arbitrary_catalog_v2.md)，精确身份 **CC-r-v2**：任意 k,r，单位客户分块 X_j、P_j、B、E，目录含 C_j=X_j、A_j=X_j∪P_j、D=B∪E；其余任意多主题每个可为任意跨组纯局部 T⊆X∪P，或包含全部公共核心 B 的 B∪V（V⊆X∪P）。D 之外不触 E。若完整纯 SPE 实际是 C_1…C_k,D^r，则最后组 a_k≤x_k/2；均匀组因此 2OPT≤3W。空主题、零客户、任意平局保留。非均匀仅结论于最后组，不能称所有组均满足。

同一对象的 query 变体：任一纯局部目录主题 A⊇C_k 均满足 β(A)=|A∩X|/2+|A∩P|≤x_k。若 U0由实际末位直接得β(A)0；U>0复用响应分类。

真正机制是同一 D 在整个真实偏离子博弈提供 U=|D|/r 的无条件保证。它允许至多一个纯局部响应，并阻止其与公共惩罚混搭；全公共时每个惩罚主题局部收益必须精确达到实际末位上界 β(V)，因此不能碰新加客户，也不能在原目标客户上二次拥挤。这一结论不能靠增加同类惩罚变体、任意跨组脚印或尾玩家数量绕开。

主代理与 harmonic 分支各自独立提出跨组推广。harmonic 已从精确陈述盲重构并逐行检查 RT-r 与 CC-r-v2，未留致命异议；其资产为 `../harmonic/review_reward_tail.md`、`../harmonic/cross_group_tail_extension.md`。主代理已独立核对 CC-r-v2 与 query 变体，暂无致命异议。没有外部同行审查、新颖性或一般 half 结论。

## 保留资产

- [arbitrary_reward_tail_obstruction.md](arbitrary_reward_tail_obstruction.md)：最初任意 r 模板 RT-r，自足四步证明。目录恰为 C_j=X_j、A_j=X_j∪P_j、B_j=X_j∪B、D=B∪E。范围由 v2 严格包含，保留发现过程与简单入口。
- [common_core_local_catalog_obstruction.md](common_core_local_catalog_obstruction.md)：中间单组脚印 CC-r-v1，保留原scope。其 d=0处排除所有目标纯局部响应依赖单组支持，不能直接照搬成跨组证明；v2已明确改为允许唯一局部响应覆盖X_k。
- [diagnose_reward_tail.py](diagnose_reward_tail.py)：只做一个明确模板诊断 k4,r3,x2,a2,b6,d3，求 fixedprefix C0,C1,C2,A3 后的全部 SPE 终局，并用单位客户公式重放一份完整有序子策略。未扩样。
- [reward_tail_diagnostic.json](reward_tail_diagnostic.json)：560 个计数状态、8 个 SPE 终局，目标偏离者最低收益3>候选实际2；183 个有序节点、2379 项含自行动比较（2196 真偏离）全通过。只是一份三响应者子博弈证书，不是完整七人 SPE。

## 剩余范围

一般 Q-CAG-HALF 仍 OPEN。当前屏障依赖全部公共主题拥有同一个完整 B、D 之外 E 隔离、同一个实际尾 D 重复 r 次和实际 X 上负载恰一。尚未判定公共主题只覆盖部分 B、D 外可触 E、或实际尾是不同主题时的真值；这些是未解决机制，不是已证必要条件。不要再调本族的块重数或重复惩罚数。

本分支已收束，无后台任务或继续扩样；本目录六项资产均待主代理统一 checkpoint/push，未自行提交或推送。
