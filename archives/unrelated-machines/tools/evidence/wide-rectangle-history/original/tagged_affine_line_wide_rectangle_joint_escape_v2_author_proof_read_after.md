# Wide-rectangle tagged affine LINE v2：作者 Proof 实际读后

Reviewer：bicriteria_set_packing_bridge，2026-10-18。仅 scratch；不修改 repo、Git、Work 或旧冻结源。

## 1. 实际顺序、文件与认证范围

先只读作者 v2 Exact，独立完成全文证明并冻结，root 实际全文读取该独立记录之后，才由 root 解封作者 Proof。此时实际全文读取的作者文件为：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_wide_rectangle_joint_escape_proof_v2.md`

SHA256 `e7254f500b3331febc2136b478ec40662a60538bcf9b639adbb7945ce0a83d1a`。

对应 Exact：

`tagged_affine_line_wide_rectangle_joint_escape_exact_v2.md`

SHA256 `6be53020ad2e0f8f810fa1cbc862fa0ba931378c04b60c2e7d81d34a564d9063`。

保留不改的本 reviewer Exact-only 独立源：

`tagged_affine_line_wide_rectangle_joint_escape_v2_independent_review.md`

SHA256 `f2786b3bed4533bdb273dfe8dfa1eb53e1674afdc81726bcee64a79dfbccdaf4`。

作者 Proof 的六节均已实际全文读。没有读取 v1、其它新源或其它 reviewer 的策略。本文只认证 ID `UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2` 在该 v2 Exact 输入域上的论证；不扩张到任意 hard images、一般 tagged-line、SC 或 UM。

结论：作者 Proof 与本 reviewer 在解封前的独立重构一致，未发现 fatal 或缺失分支。下述核对包括联合 allocation、任意完整-state-dependent marks/权、重复 label vectors、全部原 jobs、端点及总位多项式要求。作者文件开头“仅交 root hold、未向 reviewer 发送”的描述按原冻结时刻理解；本次接触是其后 root 正式解封，不倒填成作者冻结前已外审。

## 2. 作者 §1：固定 intercept 与 state-dependent marks

逐组、逐坐标的禁 slope 计数正确。一个较早 marked 点 (x,z,y) 对当前组的 line `y=az+j_x(g)`：z!=0 时恰禁一个 slope，z=0 时因为旧点的 y 为旧 intercept、且固定 intercept 单射，故禁零个。因每变量至多 d_x−1 个较早 groups，实际旧 marked 列表大小<=b(d_x−1)<=b(D−1)<L，当前显式 A_{g,x} 必有可选 label。

全部坐标所选 labels 形成 rectangle 内的 vector，containment 才保证存在对应的 indexed state。作者查出并固定该 index 后才读取其实际 marks；未来禁 slope 使用的也必须是该 index 的真实列表。相同 vector 的不同 indexed states 可以有不同权和不同 marks，不影响此顺序。

新完整 line 避开旧 marks，所以新 marks 也不可能与旧 marks 重合。作者没有把“marks 不重合”偷换成“所有完整 supports 不交”：新 marks 可以打中旧 unmarked 点。这正是本 reviewer 独立证明所保留的方向性，也是下一节必须计账的实际损失。无需在选 vector 之前预测新 state 的 marks，亦无需权与标签独立的分布假设。

## 3. 作者 §2：同一个联合整数 allocation

作者取 selected support 的全体独占点 C_g，并取 `B_g=E_g union C_g`，与独立源中的 `E_g union Q_g` 是同一个构造。

由于任意两个 selected states 的 marked 点不重合，所有 E_g 作为资源集合两两不交。C_g 则不属于任何其它 selected support，不会冲突于其它 marks 或独占点。因此全部 B_g 同时两两不交，包含全部本组 marks 及全部几何独占点。不存在先为 marked、再为 unmarked 各作一份冲突 allocation 后叠加的步骤。

若某点在 g 中 marked、在 h 中 unmarked，它不在 C_h，也不在 E_h，只由 g 领取。所有没有被 g 领取的点均为 g 的 unmarked 点，同时属于其它某个 selected support。每个共享变量上，每对不同-intercept lines：同 slope 时不交，不同 slope 时恰交一点。因此 g 的真实共享点 union 大小至多 `M_g=sum_{x in X_g}(d_x−1)`。同一点遇到多个对手可以被该和多计，只会使上界更松；多变量的资源带 tag，不能跨变量抵消或合并。

每个损失点在 g 中的权<=β，故总损失<=M_gβ，保留质量>=1−M_gβ>=1−Mβ。结合质量非负，正好得到 `v=max{0,1−Mβ}`。此保证对同一组完整选态与同一整数 allocation 的全部 groups 同时成立；非期望界，无 fractional 资源。

## 4. 作者 §3：全部原 jobs 的实际调度

作者显式放置全部 selectors，并对选中 state 仅导出 B_g 对应 jobs，其余 incidences 全留自身 private，包括全部未选 indexed states 和私时为 0 的原 jobs。每件 job 恰分配一次、使用真实 finite option。

每台 resource 至多一个 unit incidence，因为 B_g 两两不交且 state 内资源无重；负载<=1。未选 private 的真实行和恰为1，负载1。选中 private 的 selector 加未导出私时为 `2−p(B_g)<=2−v`。由于 v∈[0,1]，这也覆盖资源及未选 roots。作者对导出的零私时 jobs 仍按真实 resource unit 时间计账；允许把它们留回 private 的替代做法同样不漏任务。

v=0 时只需给出合法峰值<=2，作者没有使用正质量逆投影。v=1 时实际峰值<=1，而 selector 的 unit finite 时间给所有合法调度峰值>=1，所以实际 OPT=1。此处是 complete ordinary schedule，未省略 inactive/未选任务，也没有改 objective。

## 5. 作者 §4–5：应用及边界

Sparse-positive：将全部正权点 marked、β=0，且实际每 line 列表<=b，主条件给完整质量1和实际 unit schedule。额外零权 marks 不影响几何证明，只要列表预算仍合法。

Arbitrary weights：D>1 时 K=2q(D−1)>0 为整数，β=1/K；每 line 私时总量<=1，所以权严格大于β的点数严格小于K，因而<=b=K=floor(1/β)。阈值等号点不 marked，但仍满足 unmarked 权<=β。L>K(D−1) 正是主条件，Mβ<=1/2，因此质量>=1/2、实际峰值<=3/2。作者未以 K 的数值复制对象。

D=1 时不同 groups 使用的变量块分离，任意 states 全领取即可实际 OPT1，不需要除以 D−1、M 或 β。若 M=0 却有某变量 degree>=2，则任何使用它的 group 的 M_g 都>=1，矛盾；所以在非空输入域 M=0 与 D=1 等价。unused 变量不在任何 X_g 中，其 degree0 不会给 M_g 引入负项，资源可空置。

β=0 不计算1/β；b=0 的所有 marked 列表为空，禁 slope 步骤仍合法。b=β=0 联合时归一化使非空实例前提不成立，作者已明确该空子域。R=2、q=1、只含一组、共点在 z=0 及各阈值等号均无遗漏；正文严格条件 L>b(D−1) 仍需保留。本 reviewer 独立源中位于等号外侧的 R2 反例不反驳本合同，作者 Proof 也没有声称更弱的条件。

## 6. 作者 §6：rectangle 核验、查表与位复杂度

取菜单中位于 rectangle 的 distinct label vectors 数 K_g，而非 indexed states 数。它们构成 product 的子集，所以 K_g 与 binary product N_g 相等当且仅当完整 containment 成立。product 位长至多各坐标 log R 之和加常数，即使其数值比菜单大仍只需乘法比较，不枚举该巨大 product。重复 vector 的不同权和 marks 不可合并，作者只为 containment 去重，并仍通过 index 取真实 state。

求 forbidden slopes 扫描实际旧 marks，找可用 label 扫描实际 A；不迭代 giant binary b、极小β的倒数或有理分母。构造 B 只扫描实际选中完整 supports 并按 tagged cell 计出现次数，再加入真实 marks。输入域承诺的 prime R 保证非零 inverse 合法；z=0 从不求逆。所有质量和、Mβ与比较均用精确 binary rational 运算，其位长由真实输入位长的多项式控制。

令 n=Σ_g|S_g|、m=RΣ_g|S_g||X_g|、u=|X|R²、h=|G|，则机器数 n+u、jobs 数 m+h；finite options 恰2m+n，含私时0的两个真实端点。dense 大小 `(n+u)(m+h)` 是上述完整展开输入的多项式；完整 assignment 输出 m+h 项同样为位多项式。作者所需的 planes、states、权、marks、rectangles 都显式给出或实际展开，因此没有从二进制 R、compact CSP 或权 oracle 偷取 poly(log R) 输出保证。

## 7. 最终读后范围

作者六节与此前独立构造在所有承重点上相同。未发现主证明依赖 uniform weights、state-independent marks、随机独立边际或免费过滤未选 jobs。固定 intercepts 始终未改变；真正的结构前提是给定 wide rectangles、足够 label slack、每变量不同组 intercept 单射和变量资源 tag 分离。

本次没有运行有限数值扫描或程序实现，不给任何作者代码认证。原独立记录的事实顺序和 SHA 保持；root 已听作者策略，不能将 root 的核对记作此候选的盲审。主域以外的 hard source 是否具有合适 rectangles、实际规模、perfect completeness 或困难性仍未由本读后记录认证。后续 canonical 实读范围审查应另存，不修改本文件所引用的原冻结源。
