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
