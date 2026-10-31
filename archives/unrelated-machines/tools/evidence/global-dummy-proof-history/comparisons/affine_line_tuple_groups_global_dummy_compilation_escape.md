# 仿射线逐tuple分组加全局dummy的三半逃逸

读取目的：[constraint作group的旧分析](line_set_packing_and_take_continue_compilation_obstructions.md)明确没有处理tuple自成group的不同编译。本页直接处理一种自然的全局dummy选择器：严格端确实保整set packing阈值，但弱端仍有不求源解的三半完整调度。只关闭下述uniform/dummy计数规则，非所有source-to-UM桥。

## 1. 真实source与新编译的精确域

**ID / Version：`UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1`。**

**Objects / Domain / Definitions / Quantifiers / Assumptions。** 采用已核原文的仿射线表示，prime R≥2、k≥1，有限变量X和indexed relations G，每g含k个不同变量X_g，每变量relation-degree≤R；给注入j_x:G(x)→F_R。每relation显式allowed tuple表A_g可空。每allowed indexed tuple e=(g,s)给full set

\[
 S_e=\biguplus_{x\in X_g}\{(x,z,s(x)z+j_x(g)):z\in\mathbb F_R\},
 \qquad |S_e|=D=kR.
\]

不同变量资源带tag互异。令n=Σ_g|A_g|、m_0=非空relations数，给整数q满足1≤q≤m_0，d=n−q≥0。这里n数tuples、m_0数relations，不能混作同一degree。

每个indexed tuple e现在是一个不同group。它的menu含原state S_e及每枚global dummy δ_l的singleton state，l=1,…,d。原state每项private权1/D，dummy state私有权1，所有state质量严格1。Dummy资源与原U=⊔_x{x}×F_R²分离，**同一δ_l由所有groups共享**。

完整普通P：每indexed state一不同private机，每U/dummy资源一不同resource机；每group一件selector1仅可去自身menu所有private；每state-resource一件不同原incidence，仅可去自己private按其权执行或对应唯一resource机按1执行，其余∞。所有未选states的全部jobs存在；无其它任务、预载或逻辑守卫。d=0时没有dummy资源/states/jobs。域内n≥1，全部原任务有有限端且机器数正。

**Paper Fact与本页作用分开。** 原[14页arXiv v1](../../../history/source/literature/unrelated_machines/lee_svensson_thiery_2024_affine_line_set_packing_v1.pdf)的§3是整sets匹配与源满足约束数的对应，§4声明near-perfect YES及NP⊆BPP例外；本页只用其明确几何表示，并自足证明新的编译合同，不认证外部完整困难性证明。

## 2. 两个实际结论

**Exact Statement / Conclusion。** 对每个§1输入，不给源赋值、OPT或full-set packing见证，可确定性总位多项式输出原P全部任务的具体共同分配，满足

\[
 C_{\max}\le 2-\frac{\lceil kR/2\rceil}{kR}\le\frac32. \tag{1}
\]

同时，原P完整峰≤1可行**当且仅当**原indexed full sets {S_e}有大小至少q的两两不交packing。Selector给OPT≥1，因此strict端确实保此packing阈值；式(1)算法不求unit调度，也不把两种结论混成一个unit判定器。固定q阈值的整set困难性不能直接成为这里近二的NO。

## 3. 选择不同relations以恢复所有Hall不变量

按输入次序取q个不同非空relations，各取表内第一tuple，让这些q个groups选原state。其余n−q=d个groups与d枚dummy作任意确定性bijection，选各自指派的dummy singleton。此选择不需要共同source assignment或求最大packing。

对所选q个原sets的**任意子族F**，每变量x出现r_x≤R条长R的selected lines。因为每relation只选一个tuple，intercepts彼此不同；同slope的线平行，异slope在prime field恰交1点，所以不会重合。二阶容斥给

\[
 \left|\bigcup\text{selected lines in }U_x\right|
 \ge r_xR-\binom{r_x}{2}\ge\frac{R+1}{2}r_x.
\]

资源tag分离，Σ_xr_x=k|F|。因此每个F的资源邻域满足

\[
 |N(F)|\ge\frac{k(R+1)}2|F|
 \ge\lceil kR/2\rceil |F|.
\]

最后也包括kR奇数：ceil(kR/2)≤kR/2+1/2≤k(R+1)/2。空F和r_x=0自然成立。整数capacitated Hall给每选中原group b=ceil(kR/2)枚真实资源B_e，所有B_e共同不交；不要求partial bundles是整line或按变量分解。

注意此论证没有在全部n个tuple groups上错误套原relation-degree。全局dummy使我们只须为q个不同relations采用原state，恰恢复真正承重的不重合线/degree条件。这是本具体compiler的逃逸，不是断言任意tuple grouping都有同一个Hall下界。

全部原jobs的实际输出：selectors去上述选态；选中原state仅外送B_e对应的b件incidences，选中dummy state外送唯一incidence；**其余全部incidences留各自private**，包括原state及所有未选dummy states。Selected原private负载2−b/D；selected dummy private仅selector1；未选private质量1；U资源和dummy资源各至多一件unit。每个原任务合法一次，所有机器在同一分配中同时受控，证明(1)。

## 4. 严格unit端的任意调度提取

若有q个原full sets不交，选这些groups的原states，其余groups分别选不同dummy，导出每个selected state的全部incidences，其余states全park，得到完整实际峰1。

反向取任意完整实际峰≤1分配。每selector在其某一private上占unit，该selected state所有incidence的private时间都严格正，故全部必须导出。Resource端时间1，使selected groups领取的资源全局不交；selected dummy groups至多d个。因此至少n−d=q个groups选了原state，其全S_e已同时导出、两两不交，给原packing。未选states如果另有exports只多占资源，不会破坏提取。这个论证覆盖所有unit实际分配，并未事先规范其余jobs的去向。

## 5. 空表、显式规模与否定范围

q=n推d=0及m_0=n，各非空表恰一tuple，算法就选全部groups的原states；Hall和unit等价都仍成立，无除以d。空relations不产生groups，也不改变原j_x的注入；m_0只用于本页阈值域与构造选择，不能把primary source的value分母从|G|改成m_0或免费强化near-perfect YES。m_0=0、q>m_0在域外，完整归约若需这些分支须另证合法处理。

令v=|X|。Private机n(d+1)，resource机vR²+d；原incidences n(D+d)、selectors n，所以原jobs n(D+d+1)，finite条目n(d+1)+2n(D+d)=n(2D+3d+1)，dense条目

\[
 [n(d+1)+vR^2+d]\cdot n(D+d+1).
\]

原时间1/D的位长O(logD)，其余finite为1。选表首项、枚举真实lines、整数flow、dummy bijection及输出所有原jobs均按完整显式总编码长多项式；若用b槽/组，qb≤qD≤nD。不枚举source assignments或全部Hall子集，不按更大隐藏分母展开。任意二进制R的vR²资源/原incidences输出必须收费，不能称succinct poly(logR)编译；固定source k,R时才直接是其source-polynomial。

**Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 依赖UM-MODEL-v1、本页完整矩阵及同一仿射线degree/intercept/tag条件，标准Hall与完整flat回填自足重构，非新匹配理论。精确否定uniform private权、d=n−q个global dummy、1≤q≤m_0这一编译的近二soundness；不排更换资源/权/任务、其它激活阈值、真实shared guards或一般source桥。

Root先以完整消息Exact给rank；rank只据消息及旧current前27行source定义独立全证先冻。正式statement文件与root作者Proof其后才建立并给rank实际读后，记录不倒填。Root实际通读并亲核，再由rank实际读本canonical，见[审查](../../reviews/unrelated_machines/affine_line_tuple_groups_global_dummy_review.md)。无standing fatal，无新软件/有限实验，标准方法的新颖性已扣除，外审/全球新颖性未认证；UM-TARGET-v1保持OPEN。
