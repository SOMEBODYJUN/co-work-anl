# 任意异权辅助与重读口的批量 OR 三半逃逸

## 精确身份、义务与范围

- **ID/version**：`UM-UNRELATED-AUX-HEAVY-READOUT-BULK-OR-COMMIT-SPLIT-v3`。对应冻结 statement-only v3；v1/v2是不同域的过程来源，保原字节，不重复登记成熟资产。原 statement 文件未写此ID，本文将该合同统一赋予此稳定身份。
- **Objects / Domain / Definitions**：下述共享双 pool、正负连续 block 的完整环 backbone；r≥2、偶数 k≥2、1/2<ρ<1皆按显式输入计。所有辅助 J 只接任意 unrelated 内部 I 或正 readout C；在 C 上的全部有限时间属于(1/2,1]，内部非负有理含0/未用>1。
- **Quantifiers / Exact Statement**：对每个该域完整矩阵及两份不同“一真其余假”的真实完整 strict≤1调度，可确定性总位多项式构造同一矩阵全部原 jobs 的实际≤3/2调度，所有 selectors 实际均为 False。J 每件仅使用它两份见证中的原目的地之一；全部内部 I≤3/2、所有 C/M≤1、所有 pools≤3/2。
- **Assumptions / Conclusion**：无复杂度假设。若两 strict modes 只承诺存在，则只得全 False 调度存在；不承诺求未知 witnesses。原不固定 selectors 的 OPT本来恰1，此结果是指定读出模式的逃逸，不是源NO或大的实际OPT。
- **Dependencies**：`UM-MODEL-v1`与完整定义；证明自足使用两半项配对及整数流，标准工具不主张新颖。全部 J（含guards/aux）共用同一次流，不能只核每 branch 内部。
- **Evidence / Counterevidence / Objections**：general分别对v1/v2/v3只读陈述独立重构，之后才解封作者Proof；root为共同推导者，不记盲审。实际读后与最终正文范围另记[审查](../../reviews/unrelated_machines/bulk_or_commit_two_witness_interpolation_review.md)。未忽略未选侧aux、零时间、重复同端jobs或helper的真实身份。
- **Scope / Limits**：仅排上述已有两种完整strict模式的独立committer抗split合同，不排跨多子句耦合且没有这两全局strict模式的NO实例；不覆盖J去ring/pool/负C、C≤1/2的小端或不同backbone。不能由局部读出障碍推出一般算法或困难性。
- **Status**：限定证明完整；独立先行、作者读后与最终正文审查按真实事件分别记；无软件/有限实验/外审/全球新颖性认证。`UM-TARGET-v1`仍OPEN。
- **Related Files**：[私有single-query模板与共享外端边界](general_weighted_private_clause_exchange_and_shared_outside_boundary.md)、[审查](../../reviews/unrelated_machines/bulk_or_commit_two_witness_interpolation_review.md)。

## 1. 全部实际机器、任务与输入见证

变量a∈[r]有环索引i∈[2k]，正block为1,…,k，负block为k+1,…,2k，后继按本环循环。每变量机器为M_(a,i)、C_(a,i)及两个pools A_(a,0/1)；任务为q_(a,i)、b_(a,i)及selector f_a。不同名字物理互异，下面是全部finite端，其余∞：

| 原job | 全部finite端及时间 |
| --- | --- |
| q_(a,i) | 自身M_i:ρ；后继M_(i⁺):1；所属block pool A_(a,s_i):1/k |
| 正b_(a,i)，i≤k | M_i:ρ；C_i:1 |
| 负b_(a,i)，i>k | M_(i⁺):ρ；C_i:1 |
| f_a | A_(a,0):1；A_(a,1):1 |

f实际在负pool表示True，正pool表示False。另有不同机器I及全部辅助原jobs J，J仅可在I耗任意非负有理原时间，或正C耗(1/2,1]内原时间；资格任意、同机可异权、可跨branches。每J至少一finite端；backbone不接I，J不接负C/M/pools。没有另删的aux、预载或虚拟关系。

原机器m=r(4k+2)+|I|，原任务n=r(4k+1)+|J|，finite条目r(10k+2)+E_J；dense输入mn。给定不同u,v及两完整实际调度σ^u、σ^v，每份全部原任务一次、全部原机负载同时≤1，且仅相应u或v的f为True。其它q/b/J位置不作预设。

令c_a^t为σ^t中正block a接收的**全部J任务数**，t=u,v，并令K_a=ceil((c_a^u+c_a^v)/2)。这些是输入见证的统计，不是新容量或匿名需求。

## 2. Strict模式强迫的正C计数

strict≤1时M至多一q/b，因为各原ring时间≥ρ>1/2。每正C至多一J，因为J在此时间>1/2；任一J与unit b也不能共居，所以它迫同编号b返回M。

若某f在正pool，该pool已满，无正q可导出。k枚正q加t枚正返回b中，除q_k可去M_(k+1)外，其余只能去k台正M。容量迫k+t−1≤k，即t≤1。负block的额外入流只会减少余量。因此False branch正C接J数≤1；True branch至多k。

两见证于是给K_u,K_v≤ceil((k+1)/2)=k/2+1，其余K_a≤1。所有aux在C的占用都计入，不能忽略未选branch的任务。

## 3. 异权内部的两半项配对与一次共同流

先固定两份σ中目的地相同的J任务。令固定任务在I机器h的真实负载为F_h≤1，在branch a的正C固定数为d_a。固定C在strict中已不可能再接第二件J，故剩余选择排除它；branch剩余gate容量K_a−d_a≥0。

每个未固定J在两不同原端各给1/2。对I机器h，列其全部剩余半项原时间并非增排序w_1≥…≥w_s≥0，相邻两项组成一个分析slot，奇数末项独立slot。每slot半流≤1。每正C作单容量顶点，其后接branch gate。

网络为source→每未固定J（cap1），job→它的两个见证原端对应的I slot或C（cap1），I slot→sink（cap1），C→branch gate（cap1），gate→sink（cap K_a−d_a）。两输入均值给一份全job满分数流；所有容量整数，以确定性增广得到整数满流。解码只输出各job自己的原端；slots/gates从不作为实际执行端。

I机器h每slot至多选一项，选中负载≤O=w_1+w_3+…≤(Σw+w_1)/2。两strict输入给Σw≤2(1−F_h)，每个w_i≤1−F_h，故

\[
F_h+O\le F_h+\frac{2(1-F_h)+(1-F_h)}2
=\frac32-\frac{F_h}2\le\frac32.
\]

空表单列为0，零时间项照常排序，无除法。最终正C每台至多一J，branch总J数≤K_a。固定J与所有其它J共属这同一次完整实际分配；没有逐机独立选颜色或对各branch另外花一份内部容量。

## 4. 任意正返回集合的全部backbone回填

固定一个变量，令F⊆[k]为最终被J占的正C，c=|F|≤K_a。f放正pool；F中的b回M_i，所有其它b（含全部负b）留C。于是每C恰有一个原J或b，真实负载≤1，负C仍unit b。

F空时全部q放自身M，无exports。F非空时令p=max F：

- 正q_i在i∈F\{p}时送正pool；i<p且i∉F时送自身M；p≤i≤k时送后继M。
- 负q_i在k+1≤i<2k时送后继M，负末q_(2k)送负pool。

所有原q恰一次。p之前各M由相应返回b或自身q各一；M_p由b_p；M_(p+1),…,M_(2k)由前驱q各一。环末q已导出，无环尾撞M_1。因此每M恰一原q/b、负载≤1。

正pool负载为1+max(0,c−1)/k，负pool至多1/k。由K界，两特殊branches正pool≤3/2，其余≤1。与§3同一J分配合并，全部原机器同时受控：I≤3/2、C/M≤1、pools≤3/2。J不接ring/pools，backbone不接I，所以合并没有隐藏冲突；全部原q/b/f/J各一次。

## 5. 总位复杂度与准确剩余义务

给定两完整调度先按原矩阵验证资格、任务一次与所有有理负载。未固定J至多两个半项，总slot数≤2|J|，流网络和全部gate/原C顶点按显式输入多项式；整数流至多|J|次正增广。原有理数只需比较、排序、有限求和，不按tiny时间倒数、分母数值、ρ精度倒数展开。固定同端J、空I/J、零内部时间、未用finite>1均有上述处理。每次输出按原job给原machine，没有虚拟执行。

两strict witnesses给原OPT≤1，f所有finite端unit又给OPT≥1，所以原OPT=1。只承诺两见证存在时，上述证明给全False调度存在；没有因此得到寻找未知strict模式的算法。

该结果关闭的是独立OR committer以任意异权内部aux或重C读口抵挡weak split的接口。它不证明跨多个子句的全局NO矩阵有两份strict witnesses，也不关闭J接ring/pool/负C、正C小任务共居等新机制。真实near-2归约仍须在完整源NO下证明任意低载调度可解码；不能把本地指定读出或CONFIG障碍当成该证明。

## 6. 一般两见证插值：独立 v4 合同

以下 §6–10 是范围扩展，保留 §1–5 的 v3 身份与原陈述。v4 沿用 §1 的 backbone 机器、原任务、有限端与参数，但另行指定辅助任务 J 的资格域；不将 v3 对 J 的限制带入 v4；本扩展只保证 M/C 负载≤3/2，不另主张逐机件数或负 C 返回模式。

- **ID**：`UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`。
- **Domain / P**：一般插值部分适用于任意显式普通 unrelated 矩阵 P，机器数 m≥1，原任务集 Z 可空；有限处理时间为 binary 非负有理数，其余为 ∞。bulk 特化使用 §1 的 r≥2、偶数 k≥2、1/2<ρ<1，以及任意额外原机器 I 和辅助原任务 J。§8 要求 J 不接 A pool；§9 允许 J 接任意原机器，包括全部 A pool。除各节明确限制外，J 的有限时间任意，可为零、可逐机异权、可 strict 共居多枚 tiny J，也可有未在见证中使用的有限时间大于 1 的端。
- **Input / witnesses**：一般部分给同一 P 的两份完整 actual assignments σ⁰、σ¹，均负载≤T，其中 T≥0 为 binary 有理数；另给任意原任务子集 F⊆Z 及其指定合法原目的地 ν。bulk 部分给不同 u、v 及两份完整 actual strict≤1 见证 σᵘ、σᵛ，分别仅 f_u、仅 f_v 位于负 pool，其他 f 均位于正 pool。所有 q、b、J 都包含在这两份实际见证中，其目的地不再另加模式假设。
- **Exact / output**：一般部分固定 F 按 ν 执行，其余每枚原任务只选自己两见证中的一个实际目的地，并同时满足 §7 的逐机件数与负载界。bulk 非 pool 域得到完整 allFalse actual≤3/2；任意 pool 域得到完整 allFalse actual≤3/2+d/2，其中 d 仅取 §9 指定正 pool 上两见证真正使用的非 f 处理时间。
- **Complexity assumptions**：无。给定两份见证时是确定性总位多项式构造；若仅知两份完整 strict 见证存在，则只推出相应调度存在，不承诺求出未知见证。
- **Dependencies / attribution**：普通 UM 模型、§1 的实际 backbone 定义，以及标准半整数出现项配对、排序槽与整数最大流。一般舍入步骤不声称原创；本 v4 记录其在完整 bulk 矩阵中的适用范围和实际 pool 身份的必要逃逸义务。typed_edge_gap 先冻结非 pool 特化陈述，root 独立闭合并提出一般逐机合同，随后整理为本版本；不标作 blind 单作者结果。
- **Evidence / review route**：v4 Exact 与作者 Proof 已分别冻结，rank 已先作 Exact-only 独立重构，后经 root 路由实际读作者 Proof。root 已实际全文读 v4 Exact、Exact-first 记录及作者 Proof。本次 §6–10 的最终指定范围审查另冻，实际版本和结论路由到本页现有的[审查记录](../../reviews/unrelated_machines/bulk_or_commit_two_witness_interpolation_review.md)，不把 root 的共同推导记作独立盲审。
- **Status**：限定插值证明完整；独立先行、作者读后、最终指定范围各以实际冻结记录为准；没有软件/有限实验/外审/全球新颖性认证。
- **Scope / nonclaim**：全部输出均为同一 P 的完整原任务调度，无新增物理机器、任务、资格或可拆分执行。一般插值不是求未知 strict 见证的 UM 近似算法；bulk 结论不是源 NO 解码或 near2 hardness。`UM-TARGET-v1` 仍 OPEN。

### 6.1 一般逐机陈述

在上述一般输入下，对每台原机器 i 定义

\[
t_i=\sum_{z\in F:\nu(z)=i}p_{iz},\qquad
L_i^b=\sum_{z\notin F:\sigma^b(z)=i}p_{iz}\quad(b=0,1).
\]

令 N_i 是非 F 任务在两见证中落于 i 的**出现项**数：每个有序对 (b,z) 各计一次；同一原任务在两见证中同机时仍计两次。令

\[
d_i=\max\{p_{iz}:z\notin F,\ \sigma^0(z)=i\text{ 或 }\sigma^1(z)=i\},
\]

空最大值为 0。ν 只须是 F 的原有限合法目的地，可不在旧两见证 support 中；不假定 ν 本身负载≤T。

存在确定性总位多项式构造的完整 actual τ，使每个 z∈F 满足 τ(z)=ν(z)，每个 z∉F 满足 τ(z)∈{σ⁰(z),σ¹(z)}；且在同一份 τ 中，每台 i 同时满足

\[
\#\{z\notin F:\tau(z)=i\}\le\left\lceil\frac{N_i}{2}\right\rceil,
\qquad
\sum_{z\notin F:\tau(z)=i}p_{iz}
\le\frac{L_i^0+L_i^1+d_i}{2},
\tag{6.1}
\]

因而

\[
\operatorname{load}_i(\tau)
\le t_i+\frac{L_i^0+L_i^1+d_i}{2}.
\tag{6.2}
\]

特别地，t_i=0 时完整负载≤3T/2。若 t_i=T 且一份旧见证在 i 的 F 负载为 T，则完整负载≤3T/2+d_i/2；若两份旧见证在 i 的 F 负载都为 T，则 L_i⁰=L_i¹=d_i=0，完整负载恰为 t_i。这些是对所给完整见证的推论，不需要 T>0。

## 7. 自足构造：出现项配对与一次整数流

先暂时移除 F。每枚非 F 原任务 z 保留两个带标号的出现项 (0,z)、(1,z)，各位于相应见证的真实原机器，带该处真实处理时间；即使两次同机也不合并出现项。

在每台原机器上，把它的 N_i 个出现项按真实时间非增排序，按相邻两项配成一对；奇数时最后一项单独成对。每个这样的对只是算法中的一个容量 1 节点，并非新增原机器或执行位置。

建立整数容量网络：源到每枚非 F 任务节点容量 1；任务节点连到包含其任一出现项的对节点；每个对节点到汇容量 1。若同一任务的两个出现项落在同一对，只保留一条容量 1 边即可。给每个出现项送 1/2 流，便得到覆盖全部非 F 任务的分数流：每枚任务总流 1，每对总流至多 1。因此整数最大流存在同值整流。选定一个确定性整流，每枚原任务由其唯一被选中的对节点，执行在该对所属的原机器上。此机器就是它在至少一份旧见证中的实际目的地。所有原任务仍各执行一次；双出现项不代表双执行。

每台机器至多选到每对一枚任务，故件数界为 ceil(N_i/2)。设该机排序时间为 w₁≥w₂≥⋯≥w_N≥0，则选中总负载至多

\[
w_1+w_3+w_5+\cdots
\le\frac{\sum_{j=1}^{N}w_j+w_1}{2}.
\]

后一不等式来自交替和 w₁−w₂+w₃−⋯≤w₁：从第二项起，可按 (−w₂+w₃)、(−w₄+w₅) 等分组，每组非正，若剩最后一个负项也非正。空机器时两边均为 0。代入 Σw=L_i⁰+L_i¹、w₁=d_i 即得 (6.1)。最后把 F 按指定 ν 放回，得到 (6.2)。所有机器共用这一份整流，因此各机界同时成立。

旧见证负载≤T 且处理时间非负，给出 L_iᵇ≤T、d_i≤T。若某见证的 F 负载已为 T，则该见证的非 F 正负载为零；若两份都为 T，所有相关实际出现项都为零，故 d_i=0。这也核实了 §6.1 的各项特化，包括 T=0。

## 8. J 可接所有非 pool 原机器时，完整 allFalse≤3/2

本节保留 §1 的全部 q、b、f 有限端；J 可接 I、任意环机器 M、正或负 C，时间任意非负有理，但不接任何 A pool。两完整 strict 见证分别仅 u 为 True、仅 v 为 True，u≠v。这里不用 §2–4 的返回计数或 backbone 重填：直接把两见证中的全部非 f 原任务一起代入 §6–7。

取 F={f_a:a∈[r]}，把每个 f_a 的指定目的地 ν(f_a) 设为其原正 pool A_(a,0)。于是实际标签全 False。每台非 pool 原机器均有 t_i=0，故其全部 q、b、J 实际负载同时≤3/2。这允许同一 M/C 执行多枚原任务；不主张这些机器负载≤1，也不主张每机恰一任务。

pool 上除 f 外只有原 q，每枚时间都是 1/k。对于 a∈{u,v} 的正 pool，一份旧见证已有 unit f，故其中没有 q；另一份最多 k 枚 q。因此 N_i≤k，(6.1) 的件数界至多 k/2，固定新 f 后负载≤1+(k/2)/k=3/2。其余正 pool 在两见证中都有 unit f，因此 N_i=0，输出负载恰为 1。

对于 a∈{u,v} 的负 pool，同样有一份旧见证被 unit f 占满，故 q 的 N_i≤k；移除 f 后输出至多 k/2 枚 q，负载≤1/2。其余负 pool 在各旧见证中各至多 k 枚 q，故 N_i≤2k，输出至多 k 枚 q，负载≤1。这里用到 k 为偶数，以便 ceil(k/2)=k/2。

由此得到同一 P 的完整 allFalse actual≤3/2。每个非 f 原任务只用自己的两见证原目的地，全部 q、b、J 均已执行一次；没有先处理辅助任务后遗漏原 backbone 的步骤。本节覆盖 v3 原范围之外的 tiny 正 C、所有负 C、环 M、跨变量共享辅助以及实际共居，但不保留 v3 的逐 branch J 件数、M/C 恰一任务等加强。

## 9. J 可接 pool 时的定量界与实际 nearunit 身份义务

进一步允许 J 接任意原机器，包括全部正负 A pool，其他 backbone 和两份完整 strict 见证保持不变。定义

\[
d=\max\{p_{A_{a,0},z}:a\in\{u,v\},\ z\notin F,
\ \sigma^u(z)=A_{a,0}\text{ 或 }\sigma^v(z)=A_{a,0}\},
\tag{9.1}
\]

空最大值仍为 0。这里包括 q 和 J 的实际出现项；仅有一条未用的大处理时间资格不进入 d。两见证实际负载≤1，故 0≤d≤1。

仍固定全部 f 到正 pool，令全部非 f 任务执行 §7 的同一次整流。非 pool 原机器负载≤3/2。对 a∈{u,v} 的正 pool，一份旧见证的 unit f 已占满，故该处非 f 负载为零；另一份非 f 负载≤1，且 d_i≤d。因此 (6.2) 给出

\[
\operatorname{load}_{A_{a,0}}(\tau)
\le1+\frac{1+d}{2}=\frac32+\frac d2.
\]

其他正 pool 在两份旧见证中都被 unit f 占满，其非 f 实际出现项只能为零；输出负载恰为 1，可同时执行实际零时间 J。对 a∈{u,v} 的负 pool，一份旧见证的 unit f 同样给出非 f 总负载和≤1，且 d_i≤1；新调度已移除 f，故负载≤1。其他负 pool 的两份非 f 负载各≤1，故输出负载≤3/2。于是完整实际峰值满足

\[
C_{\max}(\tau)\le\frac32+\frac d2.
\tag{9.2}
\]

本节不沿用 §8 的 q 件数界，因为 J 可以在 pool 执行，甚至可有任意多枚实际零任务。所用负载界仍覆盖全部原任务。

令 β=2−δ>3/2，即 0<δ<1/2。若 d≤1−2δ，则 (9.2) 给出完整 allFalse actual≤β；若 d<1−2δ，则给出完整 allFalse actual<β。因此，“排除全部 C_max<β 的 allFalse 实际调度”要求 d≥1−2δ；“排除全部 C_max≤β 的 allFalse 实际调度”要求 d>1−2δ。两种阈值的等号不能混用。

若再有 1/k<1−2δ，则上述必要大 d 不能来自 q 的 1/k pool 端，必须来自至少一枚 J。该枚 J 在两份所给完整见证之一中，**真正执行于** A_(u,0) 或 A_(v,0)，其实际处理时间至少相应必要阈值。另一份见证在同一 pool 已有 unit f，正处理时间 J 不能与其 strict 共居，所以**同一枚原 J 的实际目的地必然改变**。这是关于所给见证中实际任务身份与原目的地的必要条件；未用 nearunit 资格、静态归属或一句“pool 可读取标签”都不足以满足它。它不是反向充分条件，也没有产生源赋值解码。

## 10. 零端、位复杂度与最终适用范围

一般构造保留每枚非 F 原任务的两个出现项，包括同机重复出现项和零时间出现项。零时间仍是合法实际执行，不能删除原任务；仅其负载贡献为零。未用的大时间端不参与排序或 d_i、d 的最大值，但仍保留在原 P 中。F 或 Z\F 为空、空 I/J、T=0、ν 使用旧 support 外的原有限端，以及 ν 本身负载大于 T，均由 §6–7 的同一陈述覆盖；bulk 中则仍使用原 f 的 unit 正 pool 端。

应先实际核验两份输入见证覆盖全部原任务、目的地有限、负载满足给定阈值，并核验 ν 合法。网络至多有 2|Z\F| 个出现项、相应 O(|Z|) 对节点和边；所有网络容量为整数，所需最大流值≤|Z|。处理时间只用于有理比较、排序与负载求和，不按分母数值、1/tiny 或 1/(1−ρ) 次数展开。固定相同时间与流搜索的顺序即可确定性实现。总复杂度按显式 P、两完整 assignments、F、ν、T 及所有 binary 有理编码的合计位长为多项式。

bulk 机器数、任务数和原有限端数仍为 §1 的计数，其中 E_J 按本版本允许的全部 J 原有限端计。算法中的对节点与流节点只是计算工具，没有进入 UM 矩阵；输出逐枚原任务给出唯一原机器。新 M/C 负载保证是≤3/2，不把旧 v3 的≤1 或恰一原任务保证带到较大范围。

本版本去除了“J 只能接正 C/内部 I”“正 C 端都大于 1/2”等旧范围限制，并在允许任意 pool 端时给出实际已用 d 的界。它没有移除“两份完整实际 strict 一真模式”的前提，也不证明任意源 NO 实例具有这些模式。所给模式仅存在而未提供时，结论仅为相应 allFalse 实际调度存在。bulk 的原无约束 OPT 仍为 1：strict 见证给出上界，任一原 f 的全部有限端均为 unit 给出下界；这里的 allFalse 是指定实际 selector 目的地后的构造，不能当作普通 UM 的近二 NO 下界。

因此，需要排除 near2 下 allFalse 的新物理机制，至少必须离开 §8 的非 pool 域；在保留本 backbone 与两完整模式的前提下，还必须承担 §9 中一个实际使用的 nearunit J pool 端及其任务身份改变。此必要义务并不证明该机制可行，未关闭 `UM-TARGET-v1`。
