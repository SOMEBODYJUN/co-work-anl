# Tagged affine LINE单边际tiny值：rank实际作者Proof读后 v1

审查者：rank_deficiency_fee，2026-10-18。先行Exact-first记录已冻结并由root实际通读；本次获准后才全文读取指定作者Proof。另冻本记录，原raw/独立记录不改，不写repo/Work/Git。

## 1. 读取对象与原路由

实际全文读取：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_balanced_marginal_tiny_value_proof_v1.md`

wholeSHA256：`c502f53e78440eb2e98813a428d57416de1c9e025808df82d838b5ec618dc34a`。

对应Exact：`tagged_affine_line_balanced_marginal_tiny_value_exact_v1.md`，SHA `b081198ffd09ee9e8549c75d4aa2c9d1cef0648a445b45cc6b00f9eb71bb2c50`。

先行独立记录：`tagged_affine_line_balanced_marginal_rank_exact_first_review_v1.md`，SHA `0d8a1657c494f8bffbb8612ba01f7694fdc5936568c8bd117ef45913acba84bc`，本次重新核hash未变。

本审查者先仅据Exact独立重构，未读作者策略/Proof；root已听作者策略，不记为盲审。本次是之后的真实作者Proof读后。没有将root另行数字回算当一般证明，亦无本审查者新软件或有限枚举声明。

## 2. 与独立重构的逐项一致性

**真LINE及正权点合法。** Main state t的B_t在u_t slope t/intercept0 line；helper ℓ≠a的z=j/(a−ℓ)非零且ℓz+j=az，fallback ℓ=a使v_a label−j且点(1,0)在line。每state总权1，完整其它line incidences全为0但仍保留。与独立记录一致，没有替换为cube或只保positive支持。

**标签均匀与degree。** Main label t、helper旧labels ℓ和ℓ−a−j都是state index上的双射；intercepts在u_a为0加非零j、在v_a为非零j，均互异。故每incidence单边际均匀、degree≤R。此来自显式local分布，不来自未知actualYES。

**任意helper选择的上界。** 每个H_(a,j)可选正点恰为B_a∪{P_a}；minquality>0迫selected唯一unit正点被领取。Main任意state t下，blockt的R−1helpers必须取R−1枚不同点，B_t最多剩1枚，给V≤1/(R−1)。未把helper预绑到某点，也未遗漏其它blocks的正值要求。

**显式达界。** Main t=0或任意t领取(u_t,1,t)；H_(t,1)fallback、其余H_(a,j)选ℓ=a−1领取(u_a,j,aj)。所有blocks/helpers都领取unit质量，tag分离确保不交，main质量恰1/(R−1)。与先行独立公式完全相同；R3仍合法，且未扩到域外R2。

**全部原UM上界。** Selectors按选态，仅导出所领正点incidences；其余所有原jobs留各自private，包括所有unselected states、所有zero jobs。Main private负载2−1/(R−1)，selectedhelpers1，unselectedprivate1，资源≤1。没有只调度访问过的states。

**任意完整actual下界。** C<2时每helper selected positive incidence因与selector同private会2而必外送；resource单位容量迫blockt占至少R−2个B_t点。Main最多一枚positive可导出，private≥2−1/(R−1)。C≥2下界自动。未选state额外exports只多占资源，zerojob外送也不减main正private质量。作者Proof覆盖了任意actual，与独立下界相同。

**零权padding双向。** 每helper在其余R−2parts加独有fresh变量/intercept0/labelℓ/全zero line，degree1、边际均匀、arityR且R-partite。Allocation删新零点质量不变，反向不领取新点即可；schedule扩展新jobs于原private0，投影删新jobs/资源不增负载，故V和actualOPT精确不变。新任务不是被静默删除。

**计数/位复杂度。** n=1+R(R−1)、S=Rn，base变量2R/resources2R³、I=R³(2R−1)；padding变量2R+R(R−1)(R−2)、I'=R³n。Machines/jobs及finite/dense由完整incidences直接计算，与Exact和独立记录一致。时间0、1/(R−1)、1、∞，显式polyR生成，不称binaryR的poly(logR)输出。没有优化oracle。

## 3. 范围和结论

作者Proof与先行独立重构在全部关键步骤、完整actual、均匀单边际、zero padding、counts及端点一致，本次未发现standing fatal。

可认证ID `UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1` 的V=1/(R−1)、actualOPT=2−1/(R−1)及det显式构造。它只证明真tagged affine LINE加均匀单标签边际、任意state norm1权仍不保证常数actual partial值。

Main diagonal及helpers affine相差关系的两坐标joint仅R对而非R²对，不具pairwise independence；padding不修复。因此不声称Chan/LST code-coset hard image、PCP输出或困难性，不给sourceCSP最大满足比例或主目标反面。等待canonical全文范围实审，原raw保持不变。
