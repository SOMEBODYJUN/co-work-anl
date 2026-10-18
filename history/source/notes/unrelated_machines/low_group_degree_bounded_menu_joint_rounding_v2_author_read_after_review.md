# Degree-two bounded-menu joint rounding v2：作者 Proof read-after

审查者：general_query_response_review。2026-10-18。

读取顺序：先仅据新 Exact 独立推导，并实际读取/渲染获准 primary PDF §5.1；冻结独立审查后，才首次读取新作者 Proof。本文件与独立审查分开，独立原字节保持不改。未向 rainbow 或其它审查者索取 proof，未读 canonical 新页，未修改 repo/Work/Git。

本次读取内容 SHA-256：

- Exact：`7435885c698e741f0dc762cd1fc79be270ad7de164859477645b37affbd9a298`
- 独立 Exact-first：`c02dbb9c9735ab6d816b3de4ea210b60824095ad9d941f5649fd5dc9917a173e`
- 作者 Proof：`d90349f902c63d9d7814661c5a118e17811c951a669422bfdda8ab07d26437ec`
- VW2010v1 primary PDF：`2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`

**结论：作者 Proof v2 与独立推导一致，核心定理及2SAT附带结论通过，未发现 fatal。**

## 逐项核对与攻击

1. **完整原任务恢复。** 每组先选唯一原 indexed state；selector只放该机。仅选中状态已获资源对应的 incidence jobs export，其余全部原 incidence jobs保留各自私有机，包含未选状态的全部任务及零时间原 jobs。私有机按状态独有，无其它组或状态的 job 可合法进入，故各未选状态负载1的 normalized 计算完整。
2. **Allocation→schedule。** B_g跨组不交且状态内资源无 multiplicity，每个 R_u最多一枚 unit job；选中私有机负载2−f_g(B_g)≥1，包含selector。原 resource set 先裁到获胜状态 support 不改变已达质量。由此得到完整调度上界2−V，不需要任何未知 σ 输入。
3. **Normalized OPT=2−V 的 endpoint。** OPT∈[1,2]来自selector及全私有基准。仅在C<2时使用资源机至多一枚unit；拉回未选状态任务不会增C。OPT=2时作者单独用正V会构造C<2而矛盾，因此V=0。未在C=2误用资源独占；全部最优值由有限显式空间达到。
4. **平均在group层面。** 对每个原group一agent，v是其全部clause的平均。`f/K≤f/K_g≤v≤f`的每一步正确。没有把state作独立agent，也没有把resource在同组多个states出现误算成多个 eligible agents。aux max-min A≥V/K正确。
5. **Published theorem真实接口。** 已实际读 primary printed9–10/PDF10–11，含§5.1输入定义、preassignment、二分、配对二着色及Theorem12证明；允许item两端异值，degree≤2，binary input多项式，degree1 items允许。Aux resource只有至多两个正值groups，zero edges及degree0 items可删；bonus为degree1。适用条件恰满足，未导入makespan LP gap或未证的2K→2 reduction。
6. **联合状态选择与relative bound。** additive返回min v≥A/2≥V/(2K)，随后每组argmax clause≥其平均，再一次恢复原调度，给 `C≤2−(2−OPT)/(2K)`。V、A、OPT只用于证明，不交给算法；没有先锁heavy matching再分配剩余states。
7. **Bonus双向保实际OPT。** 每个欠量状态仅加一枚独有resource及bonus job；degree和K不变。augmented→original删bonus降负载；original→augmented将包括未选状态在内的所有bonus导出至各自独有机，负载1≤原C。两向均保留所有原jobs与原赋值，故OPT完全相等。空状态、W=0、零原端、重复indexed states都不破坏论证。
8. **Ratio与promise。** 作者差值 `(2−1/K)(OPT−1)≥0`正确。只在OPT=1时给绝对阈值R=2−1/(2K)；NO若OPT>R任何调度均不能达到R，所以实际返回schedule足以决定promise。没有把relative guarantee误写成所有输入无条件C≤R。
9. **A=0与二进制复杂度。** A=0只需零值allocation，实际恢复≤2。若V>0则A>0，因此退化不丢相对保证。分母统一放大是编码长度操作，不复制数值份items；averages、1−W、argmax及逐job输出都poly。published binary input保证适用；K显式，允许随输入增长，但改善量随K变小，不虚称统一constant gap。
10. **2SAT。** 选中机unit selector使全部正权incidences必须export；zero jobs可留private。因此unit可行恰是每组选一个state且跨组正supports不交。不同groups的每个冲突state对给2CNF禁止同时选择；single-state组固定，empty/zero supports不禁，重复state indices可作为不同choices。自然的pair生成应只针对不同groups；同组两choices已互斥，而不可将state自身作为自冲突。该实现澄清不构成数学缺口。该算法只解unit阈值，不解更大makespan精确OPT。
11. **Tagged cube。** Proof把resource tag x与injective index j_x固定，可能包含该resource的groups索引必须属于Q个坐标值，因此group-degree≤min(d,Q)。Q=2及K≤7的27/14算式正确，不把任意grouping或Q>2无条件纳入。其它旧unweighted/DGR比较不参与本新证明，本次未重新审查那些旧结果。
12. **范围。** resource外端exact1、private work每state≤1、私有机互不共享、显式菜单、无其它jobs/preloads/side constraints均是实质前提。degree3、任意外端成本、succinct指数菜单和general UM未被覆盖。数学constructibility与generic backend软件实现明确区分，未声称已实现。

作者Proof无需因本轮数学审查修改。该结论是已发表additive定理与上述显式转换的结构推论，不认证新颖性或一般UM主目标。

**冻结判断：v2核心Exact/Proof通过；等待canonical组合后的实际最终read-after。**
