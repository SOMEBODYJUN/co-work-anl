# Cartesian 审计记号修订与完整 Kronecker / 固定 L2 分域复核

本任务 `boss7-tensor-notation-repair-f484c80799f20359` 仅直接替代 `boss2-wave10-repair-094b299464e358ff`。当前 definition pin 为 `ccb65e31f22f222e49c1028d62f160b1cd6fed8efd4b584d30ee927f0ce0057d`；17 核心及 9 共享只读对象的 26 个 registration pins 均已逐项按当前 registry 原记录重算，全部吻合。与直接前任任务相比，唯一 input pin 差异是共享只读 A=`UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1` 从 v2 / `d81f97599f437f633889dd1bbb6df2f76d3f2c3e1e9de833eaf7f0a4f02832aa` 更新为 v3 / `54a098141d2c72f69ed8b861f27d4f6602bffc7f1e3fcfe768ea0340b9c7e94c`。本包没有 A 端点边，也没有直接引用被改审计的旧边，故不产生替代边。

直接前任收据的当前原始 SHA 为 `aff5be747b161fc5f0169ced7f0ef93ca54c5926405be848236c28b2e4ba1e93`。其 12 项资产全部按同路径、同原始 SHA retained，包含前任 `source-delta-review.md`，没有覆盖这份历史说明。本次只新增本说明及新收据；supersession 仅处置直接前任的这 12 项资产。

## 1. 唯一源差分及数学作用

当前《裸Cartesian张量反向放大独立实际稀疏审计》§2 的完整菜单支持为

\[
b_i+g_i a_i=\ell_i\pmod2.
\]

附件旧转录多写了 `(g_i)`，把右端写成 `\ell_i(g_i)`。对该唯一一处作反向替换，当前 5678 字节、SHA `9f737f4273c0ec43254231039be810b99da901ca5ce3af7ebf3d07b2d6d6f74e` 恰还原为旧 5683 字节、SHA `fc69adc5dbbdbd9073b8501ec41462c3a52f198487f6dffa7db271732dedfe3f`；无其它字节差异。冻结 original `tensor_reverse_actual_audit_review.md` 的 §3 本来就是 `b_i+g_i a_i=ell_i (mod 2)`，其 SHA `55041afcaa86bf12918f76085449b881a08bad0814cbcd1ba4173069f62508f4` 保持。

固定组 g 和一个 indexed state 向量 ℓ 时，ℓ_i 是该向量的第 i 个坐标。跨所有组选择状态时，函数 ℓ(g) 可依赖整个 g；它不被限制为各坐标只看 g_i。一般证明的循环见证 `ell_i(g)=g_(i+1)` 在 t≥2 正需此自由度。每个已定状态的支持仍是纯 Cartesian 积，这与跨组标签函数是否逐坐标无关。修订恢复了审计摘要与冻结原文、主反例和全部原菜单的一致写法，没有增加选择权限或改变 theorem 的 statement、quantifiers、assumptions、truth_status。

## 2. 亲自核对 A 的一般值及全部普通任务

令 D=2^t，t≥1。组 g、状态 ℓ 均遍历 F₂^t，资源为 (a,b)∈F₂^(2t)，一个状态有 D 项、每项 private 权 1/D。任取补组 h=g+1 和任意所选标签，公共资源由

\[
a_i=\ell_i(g)+\ell_i(h),\qquad b_i=\ell_i(g)+g_i a_i
\]

唯一确定，因此两完整支持恰交一资源。若每组都领取 D 项，则这对补组必冲突，故最优最小质量 V_t≤(D−1)/D。这量化任意状态选择和任意形状的 partial bundles。

反向取 ℓ_i(g)=g_(i+1)，领取所有 a≠1 对应的原资源。若同一资源由 g、h 领取，δ=g+h 满足 δ_(i+1)=a_iδ_i；某 a_i=0，沿环得到全部 δ_i=0。每组的 D−1 项于是同时不交，给 V_t=(D−1)/D。t=1 的自环也有效，t=0 不在域。

普通矩阵每组一个 unit selector、每 indexed state 一台 private 机、每个 state/resource membership 一件不同 incidence。把 selector 放循环标签的 private，所选状态导出 D−1 件，余下所有 incidence 留原 private，**包含全部未选状态的全部 D 件**。已选 private 峰 1+1/D、未选 private 峰1、被用资源峰1；所有 D³+D 件原任务恰一次执行。

对任意完整实际调度，若 C≥2，下界 C≥1+1/D 已成立；若 C<2，每资源至多收一件 unit。由两个补组 selector 的实际目的地读两个实际状态，其共同资源对应两件不同原任务，至少一件留所选 private，与 unit selector 同机给负载≥1+1/D。未选任务若外送只占用额外资源，不消除这对实际任务的冲突。因此一般精确值 `OPT(P_t)=1+1/D` 不是从 t≤4 有限峰值外推。全部显式输出规模为 2D² 机器、D³+D 任务、2D³+D² 有限端；时间按该显式总位长收费。

## 3. t=1 同一种子，t=2 两个不同矩阵

在 t=1 以 J_g↔A_g、M_gℓ↔S_gℓ、I_gℓ,(a,b)↔B_gℓa（b=ℓ+ga）重命名，A 的普通矩阵就是《完整矩阵Kronecker偶次幂坍缩》的八机十任务种子 P。两组各两个 state/private 机、四个资源机；A_g 的两个 finite 端时间1，B_gℓa 的 private/resource 两端分别为1/2和1。两选支持恰交一资源给真实 OPT(P)=3/2，完整上界同时保留未选 state 的任务。

但两个二阶操作保留的对象不同：

| 操作 | 机器类及总数 | 任务类及总数 | 有限端 | 精确实际 OPT |
|---|---|---|---:|---:|
| 裸 state/resource 支持先积，再编译 P₂ | 16 private + 16 resource =32 | 4 selector +64 incidence =68 | 16+128=144 | 5/4 |
| 完整处理矩阵 P^[2] | SS、SR、RS、RR 各16，共64 | AA4、AB16、BA16、BB64，共100 | 每任务对4端，共400 | 1 |

裸 P₂ 的 selector 对应 AA；incidence 对应 BB，但只保 private-private 的1/4端与 resource-resource 的1端。完整平方中的 BB 另有 SR、RS 两个1/2端，还必须真实执行全部 AB、BA 任务。故从完整平方删掉 mixed jobs/machines 才得到另一编译矩阵；不能删完仍称原完整平方，也不能跨两个实例搬用最优值。

完整平方的正文统一初态安排全部100任务；只有 RR 的 (R10,R10)、(R11,R11) 各超载一，(R10,R11)、(R11,R10) 各缺一，其余原机器负载一。15 件不同原任务的同时改派修平这两个缺陷，资格逐项来自原乘积端。它确实使用 mixed 结构：例如任务 (0,7)=(A0,B101) 从 SR 端 (1,7) 的时间1移到 SS 端 (0,2) 的时间1/2，另一 BA 任务 (2,1) 也由 RS 移到 SS；其余 BB 的 mixed 端参与补位。这不是裸 P₂ 所有任务和端上的同一证书。正文逐类净负载账把四台 SS、五台 mixed 机保持原负载，并把两台 RR 超载各减一、两个空 RR 各加一，最终64行全为1。任一 AA 在其全部合法端时间1，给相反下界。

把完整平方调度作 k 份坐标乘积，全部10^(2k)个任务各执行一次，行负载为 k 个单位行负载之积，得到 OPT(P^[2k])≤1；全 selector 元组给≥1。这个一般偶次幂证明独立于裸族的一般 t 证明。裸族 5/4 与完整平方1分别反驳各自的普遍保 NO 合同，彼此不矛盾；奇次幂、受限 hard image 或新实际一致性约束均不在这些反驳的全称范围内。当前 K 核心因此保 `isolated-after-review`，不制造“两个值相同”或互相推出整条结果的逻辑边。

## 4. 固定 t4/L2 replay、一般固定 L 定理与实际 UM 接口

固定 replay 是第三种模型：base 三维匹配 A⊕={000,011,101,110}，q=2、ν=1，未编成普通 UM。原程序固定一个4×4二元 B，令 C=I+B；B²=C、BC=I，使16条 `(x,Bx,Cx)` 的三个完整 word 投影都双射，每层 parity 合法，所以是**同一个**真实整数 perfect matching。

12个行形式 I、B、C 非零互异，F₂ 上任两形式独立；从不同两层各指定一轴的映射秩2。多指定同层其它轴只减少原像，因此28个一层、294个两层，共322个 joint guard families 由同一 F 满足。容量按所选不同层数 s 收费为2^(4−s)，不能按同层指定轴数改收费。12个单轴 prefix families 由完整 word 双射另得，不与322混成同型计数。

54个跨两层、各选一轴的 family，每pattern恰4条边，用4个区分 clones；连同每边3个完整 word 资源，共每边57件、16边912个不同源资源。它证明 simultaneous resource bundles，不是54份不同分配，更不是已经存在912件 ordinary UM 任务。

固定 B 的第三行（0起始 row2）等于 e0+e1，故 X0+X1+Y2=0，三层四个可行 patterns 各4次，超过自然三层容量2。原程序预期并明确输出这次失败；不应删去它或把运行 exit0 误读成通过所有更高阶 guards。

本轮全文读 replay 正文、一般定理及冻结5695字节原脚本，核脚本 SHA `695324d5b1dd689cba7059f4003b8ccf74fd9b797ca1bd3314af4f87335359b1`。已完整解析旧579020字节 JSON和历史 replay stdout，两者原始 SHA 均为 `fe42110a2b0f603abaf5d0a5b28094b452a14b95de5056545fdaee135ff81bbb`，全结构及字节一致；另核 execution 记录 exit0。这是对已存证据的读取和版本比较，**没有在本轮运行该数学程序**，也不冒称逐个 clone 人工重读。

一般 `∀固定L ∃偶t、同一个B/F ∀guards` 由另一解析证明承担：随机共轭 B=CB0C⁻¹ 排除全部支持≤L的非零关系，用 Σ_(s≤L)binom(t,s)3^s<2^t−2 的 union bound，t=6L 足够；独立形式使每pattern容量成立，完整 word 双射给全部单轴 prefix。这里没有按输入 t,L 统一确定性位多项式寻找 B 的承诺。固定 t4/L2 有限 replay 没有最优值搜索，不能承担这条一般存在量词，也不能因三层失败反驳允许另选 t/B 的定理。

真正 functional prefix 一致性、root 乘法收费、保持 YES 的 actual UM 编译及从每个低峰完整 σ 统一解码仍未实现。A 的记号修订不支付任何这些义务。旧 checks/context 边原范围准确，原 SHA 保留。

## 5. 有限证据与一般证明各自承担什么

| 材料 | 已有有限保证 | 一般数学由何处承担 | 本轮行为 |
|---|---|---|---|
| 裸 Cartesian actual 审计 | t1全部1024完整分配得OPT3/2；t2..4只核全 jobs witness、交点、规模 | A 主文补组冲突、循环不交及全部原任务上下界 | 全文及冻结 original 对照；唯一字节差分核验，未重跑审计 |
| 完整矩阵平方证书 | 固定64机100任务400端的完整调度峰1；旧四次幂核验另有记录 | 平方有限证书的逐类负载证明与任意k的调度乘积分解 | 全文比较和资格/负载论证；旧程序与输出保持历史范围，未重跑 |
| 固定t4/L2 replay | 同一16边F、322 joint families、12 prefix、912 clones、明确三层失败；没有优化器 | 一般固定L随机共轭/union-bound证明 | 原代码全文、结果完整JSON解析比较及原执行记录核对，未重跑 |

有限 t1 最优化只属于裸菜单完整普通矩阵枚举；不能移称 L2 matching 的优化，也不从 t2..4 的达界 witness 单独认定其最优性。A 的任意 t 结论、K 的任意偶次幂结论及 source matching 的任意固定 L 结论分别有其明确证明，不能用其中一条有限运行替代另外两条。

## 6. 其它核心、资产继承与交付范围

其余15核心的完整证明、旧数学运行、原PDF、外部科学审读与未变来源按直接前任有效数学交付继承。本轮读取其当前登记合同字段及直接前任17核coverage，并核全部11旧边的端点、条件、whole_result/contribution和scope；没有声称重新读完68份来源。每个核心的新收据同时给当前pin、继承依据及具体数学比较范围。继承不会扩大6条whole、2条step、3条context的作用：条件quota仍只付其额外uniform/λ子域右侧见证；福利LP与正support LP仍不同；slot程序仍非一般优化器，指定profile重组仍不提供未知YES搜索。

本轮元数据检查：108条reading refs、68不同文件、62处精确标题全部SHA/唯一性通过；26当前对象pins通过；12原资产SHA通过；11边的全部当前endpoint pins和43条direct evidence refs通过；原生 `verify_endpoints` 与 `edges(...,verify=True)` 检查11边通过，全部accepted且保ALL。上述字节/结构检查不是未读证明的数学重证。11旧边均无A端点、直接evidence均无被改附件，所以无需edge-bind、复制或重造边；新收据只刷新共享读依赖与说明范围。

直接前任及当前任务没有新声明follow-up对象对。保原 `follow_up_tasks:[]` 与 `closed_overlaps:[]`；前代已闭合的Kronecker/Cartesian分域比较被当前直接前任正式覆盖，本次复核确认其理由继续成立，不重开相同问题。17核仍8 linked、9 isolated-after-review；无新节点、无新科学运行、无新逻辑边。

本说明及收据是当前worker的本地交付，等待Boss反馈。checkpoint、push、done、assemble及最终集成均由Boss串行组织；本文不声称本任务已完成这些队列动作。
