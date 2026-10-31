# 低重数标签资源的确定性比例地板与成对一致性锐界

本页攻击反面归约的一项具体承重义务：用共享资源编码标签冲突后，较小正比例的真实需求树是否仍能逃过一致性？结论是**资源重数有界时存在可构造的正常数地板**；若每枚冲突资源最多关联两个标签，地板恰为二分之一，任意增大标签的资源束仍不能降低它。这里没有证明一般调度困难性或 `UM-TARGET-v1` 的反面。

## 1. 精确对象与命题身份

使用 [UM-DAG-DEGREE-TOKEN-IDENTITY-v1](rooted_dag_degree_token_bridge.md) 的真实树定义：输入正需求点即使在输出中成为叶也收费，每个非根选中点恰一个父点，零需求仅允许在原终端；
\[
b(H)=\min\bigl(\{1\}\cup\{\deg_H^+(v)/d_v:v\in H,d_v>0\}\bigr),
\qquad b^*(D)=\max_H b(H).
\]

本页的显式简单 DAG 分为四层。根为 \(r\)，变量集 \(X\) 大小 \(q\ge1\)，变量 \(x\) 的标签集 \(E_x\) 两两不交，资源集为 \(R\)。边仅为
\[
r\longrightarrow x\longrightarrow e\longrightarrow u,\qquad
e\in E_x,\quad u\in S_e\subseteq R.
\]
需求为 \(d_r=q,d_x=1,d_e=K_e\ge1,d_u=0\)。各 \(K_e\) 是二进制整数，可大于显式度；没有假定全部标签都局部可行。允许空标签集、不可用标签和无关联资源。所谓**局部完整选择**是给每个 \(x\) 一个标签 \(e_x\in E_x\) 及显式子集
\[
B_x\subseteq S_{e_x},\qquad |B_x|=K_{e_x}.
\]
给定该选择，定义其实际资源重数
\[
\Delta=\max_{u\in R}|\{x:u\in B_x\}|\ge1.
\tag{1}
\]
这里的重数是**所选资源子集的实际重数**，不必等于所有标签的总关联度；改变标签时重数也可能改变。

**UM-BOUNDED-COLLISION-LABEL-FLOOR-v1。** 对每个上述 \(D\) 及给定局部完整选择，存在确定性总位多项式算法输出真实根树 \(H\)，满足
\[
\boxed{b(H)\ge1/\Delta.}
\tag{2}
\]
输出只用给定的 \(e_x,B_x\)，不需要源 CSP 见证、配置证书、分数解、最大束匹配或最优树。不同标签的 \(K_e\) 可以不同，也不要求 \(K_e=|S_e|\)。通过既有实际任务桥梁得到
\[
C_{\max}(\sigma_H)\le2-1/\Delta,\qquad
1\le\operatorname{OPT}(P(D))=2-b^*(D)\le2-1/\Delta.
\tag{3}
\]
式(3)为该桥梁的绝对负载界，也给这个受限输入族的 \((2-1/\Delta)\) 近似；它不是任意 UM 输入的逆表示或一般算法。

**UM-PAIRWISE-LABEL-FLOOR-SHARP-v1。** 对每个整数 \(k\ge1\)，存在所有 \(K_e=|S_e|=k\)、资源总关联度至多二且局部完整的上述 DAG，恰有 \(b^*=1/2\)，桥梁实例的真实 \(\operatorname{OPT}=3/2\)。因此二重资源下的式(2)对每个束宽都锐。对任意 \(\Delta\ge1\)，单资源束另有 \(b^*=1/\Delta\) 的例子，故不额外限制束宽时，式(2)的通用常数也锐。

上述身份无复杂度假设。总位多项式相对于显式图、二进制需求及给定选择的合计编码长度；没有给出寻找最小可达重数 \(\Delta\) 的算法。第3a节另立不需给定选择的结构类近似身份，不扩写式(2)的输入合同。

## 2. 局部关联着色的确定性证明

在每个资源 \(u\) 处，将所有 \((x,u)\) 关联任意**单射**着色为 \(1,\ldots,\Delta\)；不同资源的着色互不约束。可按固定变量次序直接赋色，不求二部图正常边着色，也不要求某变量的关联颜色不同。

令 \(a_{xc}\) 是 \(B_x\) 中颜色 \(c\) 的关联数。对每个 \(x\)，
\[
\sum_{c=1}^{\Delta}a_{xc}=K_{e_x}.
\]
所以至少一个颜色满足 \(a_{xc}\ge\lceil K_{e_x}/\Delta\rceil\)。令
\[
G_c=\{x:a_{xc}\ge\lceil K_{e_x}/\Delta\rceil\}.
\]
每个变量至少计入一个 \(G_c\)，故
\[
\sum_c|G_c|\ge q,\qquad
\max_c|G_c|\ge\lceil q/\Delta\rceil.
\tag{4}
\]
取使 \(|G_c|\) 最大的颜色 \(c\)。对每个 \(x\in G_c\)，保留边 \(r\to x\to e_x\)，并从 \(e_x\) 接上其所有颜色为 \(c\) 的资源。资源处着色单射保证每个资源至多获得一个父点；各标签专属于其变量，故所得图是真实根树。

根出度比至少 \(\lceil q/\Delta\rceil/q\ge1/\Delta\)，变量出度比为一，每个选中标签的出度比至少
\[
\lceil K_{e_x}/\Delta\rceil/K_{e_x}\ge1/\Delta.
\]
终端不收费，截断项一不小于该界，证明式(2)。这是一般组合证明；有限枚举只核实现。无需独立抽样、条件期望、Chernoff 界或随机期望保证。

**复杂度。** 先列各资源的所选关联并求实际 \(\Delta\)，再赋色、计数、构树。由于每个 \(B_x\) 是集合且只有 \(q\) 个变量，\(1\le\Delta\le q\)。至多 \(q\Delta\) 个计数器；显式所选关联总数不超过原图边数。使用整数上取整和交叉乘法即可比较比例，位长受输入控制；不存在按巨大二进制需求作循环。若需自行获得一个局部完整选择，只须对每个变量扫描有 \(K_e\le|S_e|\) 的标签，并取任意 \(K_e\) 个资源；此时 \(K_e\) 被显式度界定。

## 3. 锐例与负控制

**二重资源、每个束宽都锐。** 取偶数 \(q=2s\ge2\)，变量成对。每个变量仅一个标签，需求 \(k\)；同一对的两个标签关联同一个大小 \(k\) 的资源集，不同对的资源不交。局部完整且实际重数为二。

每对只选一个变量并取其全部资源，得到根比例二分之一、标签比例一，故 \(b^*\ge1/2\)。若某树评分严格大于二分之一，则每个选中标签都要取严格多于 \(k/2\) 个资源；同对不可能同时选中两个变量。因此根最多选 \(s=q/2\) 个变量，根比例至多二分之一，矛盾。故 \(b^*=1/2\)，不依赖 \(k\) 的奇偶。由精确桥梁反算得到 \(\operatorname{OPT}=2-1/2=3/2\)。

**一般重数锐性。** 取 \(q=s\Delta\) 个变量分成大小 \(\Delta\) 的组，各变量仅一个需求一标签，同组关联同一枚资源。任何正评分树至多选每组一变量；取每组一个即达到 \(b^*=1/\Delta\)，桥梁 \(\operatorname{OPT}=2-1/\Delta\)。\(\Delta=1\) 正确给满比例一和最优负载一。

**缺局部完整选择时不可套用。** 仅一变量、一标签、需求 \(K>1\) 而只关联一资源，即使资源度一，也只有 \(b^*=1/K\)，不能由资源度推出满比例。算法扫描失败仅说明不存在 \(b=1\) 树；不说明没有较小正比例树。

**空变量边界。** 若另允许 \(q=0\)，根按需求树模型是原零需求终端，单点树评分为一，桥梁最优负载为一。式(1)的 \(\Delta\) 未定义，本定理分支不使用它。不能默用其他分层公式另设的“空实例值零”约定。

## 3a. 全局变量关联度下的无承诺比例近似

定义全局**变量组关联度**
\[
\Delta_G=\max\bigl(\{0\}\cup\{|\{x:\exists e\in E_x,\ u\in S_e\}|:u\in R\}\bigr).
\tag{6}
\]
它计不同变量组，不计同组标签数；比所有标签的资源总入度可能严格小。这里不再假定局部完整选择存在。

**UM-GROUP-DEGREE-LABEL-APPROX-v1。** 对所有第1节四层 DAG，当 \(q\ge1,\Delta_G\ge1\) 时，有确定性总位多项式算法，不给 \(b^*\) 或任何标签见证，输出真实树满足
\[
b(H)\ge b^*(D)/\Delta_G.
\tag{7}
\]
经既有桥梁输出全部实际任务分配，有
\[
C_{\max}\le2-b^*/\Delta_G
\le(2-1/\Delta_G)(2-b^*)
=(2-1/\Delta_G)\operatorname{OPT}.
\tag{8}
\]
第二个不等式的右减左等于 \(2(1-1/\Delta_G)(1-b^*)\ge0\)，未把绝对界与近似比混淆。若 \(\Delta_G=0,q\ge1\)，无标签有资源，故 \(b^*=0\)，根单点和桥梁精确给负载二。若 \(q=0\)，按前述根终端分支精确处理。

**算法及证明：局部比例上界。** 对每个变量计算
\[
a_x=\max_{e\in E_x}\min\{1,|S_e|/K_e\},
\]
空标签集的最大值为零。降序排列为 \(a_{(1)}\ge\cdots\ge a_{(q)}\)，定义可直接计算的局部上界
\[
U=\max_{1\le s\le q}\min\{s/q,a_{(s)}\}.
\tag{9}
\]
任意评分 \(\beta>0\) 的真实树至少选 \(\beta q\) 个变量，且每个被选变量的某个标签有 \(|S_e|/K_e\ge\beta\)。因此对其所选变量数 \(s\)，有 \(s/q\ge\beta,a_{(s)}\ge\beta\)，所以 \(b^*\le U\)。这里没有假设每个变量只可选一个标签；只从原树每个所选变量取一个已有的标签，即足以证明上界。

若 \(U=0\)，输出根单点；上界已证明 \(b^*=0\)。否则取达到式(9)的 \(s\)，为前 \(s\) 个变量各选达到 \(a_x\) 的标签，并任选
\[
|B_x|=\min\{K_{e_x},|S_{e_x}|\}>0
\]
个资源。将这些标签的**临时需求**设为 \(|B_x|\)，根临时需求设为 \(s\)，运行第2节算法。所选束的实际重数 \(\Delta'\le\Delta_G\)，故输出至少 \(s/\Delta'\) 个变量；在原 DAG 中根比例至少 \(s/(\Delta'q)\ge U/\Delta_G\)。每个保留标签获得至少 \(|B_x|/\Delta'\) 个资源，原需求下比例至少 \(a_x/\Delta'\ge U/\Delta_G\)，变量出度比为一。因此实际输出更强地满足
\[
b(H)\ge U/\Delta_G\ge b^*/\Delta_G.
\tag{10}
\]
所有评分都用**原需求**核验，临时需求仅用于算法分流。

最大局部比例、排序、\(q\) 个断点和实际束着色均为显式多项式；有理数交叉比较的位长受输入控制。巨大二进制 \(K_e\) 仅出现在 \(|S_e|/K_e\) 中，不按其数值复制任务或枚举阈值。\(\Delta_G=1\) 时式(10)与上界还给真实最优树。对 \(\Delta_G=2\) 的受限类得真正的三半调度算法；没有去掉四层表示或有界变量组关联度。该局部比例排序构造由独立审查者在未读主稿证明时重构，规范实现采用此简化，不保留冗余阈值枚举为第二套生产算法。

## 4. 对近二困难性归约的准确限制

若资源在**全部标签**中的关联度至多固定 \(\Delta_0\)，每个变量均有局部完整标签，则任选局部完整选择都有 \(\Delta\le\Delta_0\)。本页算法直接输出 \(b\ge1/\Delta_0\) 的真实树及 \(C_{\max}\le2-1/\Delta_0\) 的真实调度。特别地，每枚资源仅对应一对不相容标签的直接冲突编码有 \(\Delta_0=2\)，无论束宽、标签数、底层冲突图的围长或源 CSP soundness，均不能把此直接 DAG 的 NO 值压到小于二分之一。

更精确地，若 \(b^*(D)\le\eta\)、\(0<\eta<1\) 且存在局部完整选择，则该选择的重数必须满足
\[
\Delta\ge\lceil1/\eta\rceil.
\tag{5}
\]
这对**每个**局部完整选择成立。为满足既有充分归约合同 NO \(b^*\le\varepsilon/2\)，必须使每个这种选择都有 \(\Delta\ge\lceil2/\varepsilon\rceil\)。这是必要条件；较大重数本身不保证 NO、低比例解码或复杂度困难性。随固定 \(\varepsilon\) 增长的常数重数完全允许，未被本页排除。

即使归约没有承诺每个 NO 输出均局部完整，只要其输出始终满足全部标签资源度 \(\le\Delta_0\)，YES \(b^*=1\) 与 NO \(b^*<1/\Delta_0\) 的 promise gap 仍可多项式区分：扫描每个变量是否有 \(K_e\le|S_e|\) 标签。YES 必全部通过；若全部通过，式(2)排除 NO。这里利用的是归约的两侧 promise，不把扫描接受当成 \(b^*=1\) 的判定。

**真正尚缺。** 构造源相关的高重数标签接口，使所有局部完整选择均遭足够大碰撞，而且任何仍有较小正比例的实际树都解码源见证；同时保留完整 YES 与每个固定 \(\varepsilon\) 的位多项式规模。跨层资源复用、额外中间约束、加权收益及其他表示不属于本页四层合同，不因本结果而被排除。

## 5. 与现有资产和文献的扣除

[k-均匀分层恒等式](k_uniform_bundle_matching_floor.md)指出必须控制所有 \(t\)-层，但本身不给随束宽无关的低重数地板。本页允许异质需求，并通过资源处着色和根选择共同保证 \(1/\Delta\)；奇数束宽也得到精确二分之一，强于只给全部变量分配 \(\lfloor k/\Delta\rfloor\) 资源的直接 Hall 界。

[两层半比例贪心](rooted_dag_degree_token_bridge.md#7-两层需求树的半比例贪心与任务桥梁的二分之三负载界)输入为根→中心→资源，保证相对未知 \(b^*\) 的一半。本页多一个变量到标签的选择层，给定低重数局部选择后保证绝对比例；两者条件、量词和算法不同。既有 token 桥梁只承担式(3)的调度翻译，不是新构造。

**Paper Fact，非本页依赖。** Bateni–Charikar–Guruswami，*New Approximation Algorithms for Degree Lower-bounded Arborescences and Max-Min Allocation*，TR-848-09，[作者原始 PDF](https://mhbateni.com/academic/pubs/maxmin-tech09.pdf)，§7 Definition 7.1/Lemma 7.2（PDF页47–48，印页47–48）已讨论 duplication gadget 的困难性限制：保留两个完整分配的并集可将其资源度压到二，再用度二 Santa Claus 算法限制 gadget 强度。本页不是该文的一般新版本：其对象是 Santa Claus 加性效用和三个外部可用物品，本页是四层需求树、按已选束重数的局部着色。这里只核对该定位，不导入该算法定理、不宣称全文重构。来源取得状态见专题文献记录。标准鸽巢/着色工具的全球新颖性和独立论文价值均未认证。

**Truth / Mechanism / Value / Ambition。** 所述范围有自足证明；机制是局部冲突可按颜色分流并只保留足够多变量；价值是给共享标签归约一个可检验的重数必要条件和真实调度上界；没有得到近二困难性或一般目标的正反答案。

## 6. 实现、审查与复现入口

规范实现：[bounded_collision_bundle_floor.py](../../../tests/audits/unrelated_machines/bounded_collision_bundle_floor.py)。独立原资源父点枚举：[bounded_collision_bundle_independent.py](../../../tests/audits/unrelated_machines/bounded_collision_bundle_independent.py)，不导入规范核心。实际锐例：[pairwise_label_resource_floor.json](../../../examples/unrelated_machines/pairwise_label_resource_floor.json)。冻结结果：[bounded_collision_label_floor_audit.json](../../../evidence/runs/unrelated_machines/bounded_collision_label_floor_audit.json)。独立 statement-first 重构与冻结攻击：[bounded_collision_label_floor_review.md](../../reviews/unrelated_machines/bounded_collision_label_floor_review.md)。

一般证明、实际内部审查、软件实现、有限核验、外审及新颖性分别登记；尚未消除的 fatal objection 将阻止状态提升。有限枚举不证明一般式(2)。`UM-TARGET-v1` 保持 OPEN。
