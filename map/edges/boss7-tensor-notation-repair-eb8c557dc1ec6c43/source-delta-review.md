# A 附属有限审计记号订正：本轮定向复核

审读人 Boss7，2026-11-16。对应任务 `boss7-tensor-notation-repair-eb8c557dc1ec6c43`，直接替代 `boss2-wave22-um-repair-b52d66a972227003`。本轮只写本任务的 edges 目录及收据，未改原边、原证明、冻结输出或旧收据，未操作 Git、同步、checkpoint、队列、公屏或账号连接器。

## 1. 实际阅读、比较与继承范围

本轮实读 AGENTS.md、`prompts/03-map-worker.md`、`research/IMPLEMENTATION.md` 第三阶段接口及本任务原文。定向实读材料为：

- A=`UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1` 当前登记 v3、全部模型／陈述／量词／证据绑定，以及主反例《裸笛卡尔菜单乘积的精确反向放大》全文；承重数学为其 §§1–5。
- 已订正的《裸Cartesian张量反向放大独立实际稀疏审计》全文，以及冻结原件 `tensor-reverse-actual-audit-20261031/original/tensor_reverse_actual_audit_review.md` 全文。
- 核心资源《裸菜单反向放大的完整原矩阵审计入口》全文及原 `audit_normalized_flat_cartesian_tensor_reverse_amplification.py` 全部 363 行。
- `UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1` 当前登记，以及《笛卡尔分块一致性与二度菜单联合取整双源审查》§4、《二元分块配额的限定认证与非空选择域修订》全文；只复核本边使用的唯一全坐标块与普通任务桥，不重新认证其它 q 元、degree-two 或全部无环域结论。
- 《完整矩阵Kronecker偶次幂坍缩》§7.1 的八机十任务定义，用于核对基例逐对象重命名；本任务不重证平方或偶次幂结论。
- 前批收据的全部 17 项 coverage、20 项 assets、follow-up／closed 处置、两条受影响原边全文，以及前轮 `tensor-audit-notation-erratum.json`、`um-transfer-review.md`、`um-transfer-reference-impact.json` 中与此订正和本任务有关的记号、影响和有限核验记录。前轮关于 T/D 迁移的证明不是本任务新增认证。

其余 15 个核心的成熟数学比较沿直接前批收据继承，没有重新全文阅读。另对全部 34 个本任务 input pins 作当前登记比对，并对全部 20 项前资产逐字节核 SHA、endpoint/evidence pins 及 review digest；18 项完全当前，只有本轮替换的两项旧边在 A 的 endpoint pin 上过时。程序读取这些元数据及引用字节不计作对 15 个无关核心的数学重新实读。

## 2. 确认的精确变化

附属审计 §2 的完整菜单支持方程从 `b_i+g_i a_i=\ell_i(g_i)\pmod 2` 订正为 `b_i+g_i a_i=\ell_i\pmod 2`。固定 indexed state 的右端是其向量坐标；不能从支持的 Cartesian 形式另加标签函数只读本坐标的限制。循环见证仍为 `ell_i(g)=g_(i+1)`，在 t≥2 可以依赖下一坐标。

订正附件 SHA 为 `9f737f4273c0ec43254231039be810b99da901ca5ce3af7ebf3d07b2d6d6f74e`，5,678 bytes。本轮将这一处逆替换即精确恢复旧 SHA `fc69adc5dbbdbd9073b8501ec41462c3a52f198487f6dffa7db271732dedfe3f`。冻结原件 SHA `55041afcaa86bf12918f76085449b881a08bad0814cbcd1ba4173069f62508f4` 已写正确的 `ell_i`，不需要改动。

A 的 registration pin 从 `d81f97599f437f633889dd1bbb6df2f76d3f2c3e1e9de833eaf7f0a4f02832aa` 变为 `54a098141d2c72f69ed8b861f27d4f6602bffc7f1e3fcfe768ea0340b9c7e94c`。与前轮保存的 before_object 逐字段比较，实际变化只有 version、evidence 和解释订正的 objections 备注；model、statement、quantifiers、assumptions、scope、kind、truth_status、body、sources 完全相同。主证明 SHA 仍为 `02240942660772bf7a74c05b59ce17fbccd32f7ae1ac5814713a98c906693d7d`，truth_status 仍为 proved。

## 3. 亲自重推一般裸值与完整实际调度

令 t≥1、D=2^t。组 g 和每组 indexed state ℓ 均遍历 F₂^t，真实资源为 (a,b)∈F₂^t×F₂^t，支持由 `b_i+g_i a_i=ell_i` 定义。每个固定 (g,ℓ) 有 D 枚不同资源，每项 private 时间 1/D；全部 private 质量为 1。每组一件 unit selector，每个合法 (g,ℓ,a,b) 有一件不同 incidence，有限端仅是自己的 private（1/D）和该真实资源（1）。所以完整矩阵有 2D² 台机器、D³+D 件任务和 2D³+D² 个有限端。

任取 g 及 h=g+1，任意标签 ℓ、m 的交点唯一：`a_i=ell_i+m_i`、`b_i=ell_i+g_i a_i`。若所有组均领取其 D 项支持，补组的两份领取必相交；所以任意标签和任意 partial bundles 的最小质量至多 (D−1)/D。

取循环标签 `ell_i(g)=g_(i+1)`，只领取 a≠全1 的资源。若 g、h 领取同一 (a,b)，令 δ=g+h，得 `delta_(i+1)=a_i delta_i`。a 至少有一个零坐标，先迫下一位 δ 为零，再沿环迫全部为零，故 g=h。每组确有 D−1 项，得到 V_t=(D−1)/D；t=1 同一消零论证有效。固定任意 a≠全1 和 b，还可从某零位起沿 `g_(i+1)=b_i+a_i g_i` 唯一恢复领取组，故恰使用 D(D−1) 枚真实资源。

完整上界调度将 selector 放所选 private，只将该 state 的上述 D−1 件 incidence 外送。其余所有 incidence 均留自己的 private，包含每个未选 state 的全部任务。所选 private 负载 1+1/D；未选 private 负载 1；每资源至多一件 unit。所有 D³+D 件原任务恰执行一次，故 OPT≤1+1/D。

任意完整调度峰为 C。C≥2 时下界平凡；C<2 时每资源机最多一件 unit incidence。由两个补组 selector 的实际目的机读出实际 states，其唯一共同资源对应两件不同原任务，不能同时外送，至少一件留所选 private，与 selector 共处迫 C≥1+1/D。未选 states 若额外外送，只会占容量，不能消除该冲突。于是对全部完整原调度有 OPT=1+1/D，而非只对规范见证成立。等价的解码接口是：取每组所选 state 的实际外送集合 E_g；它们不交，且 `1+(D−|E_g|)/D≤C`，所以 V≥2−C。C=2 不使用“每资源仅一件”的推理。

## 4. 唯一全坐标块确实特化为 A

分块对象允许同一全 family 函数 `F_j:F₂^(b_j)→F₂^(b_j)`，并禁止读块外坐标。取唯一块 I₁=[t]、b₁=t 后，F₁ 就是任意标签函数 ℓ(g)，没有剩余一致性限制。其 H=D−1/2，故一次全局整数配额为 `floor(H)/D=(D−1)/D`。这与上述补组上界及循环真实不交见证一致；无需把一次全局 floor 错换为逐块 floor。

该唯一块域非空，完整任务桥保留全部 selectors 和所有 states 的 incidences。把配额领取外送并回填其它全部任务给 1+1/D；任意 C<2 实际调度的真实 E_g 给反向下界。因此原 `specializes` 边的完整结论、ALL、unconditional 和 accepted 均保持。较小块的逻辑 Q、固定 chain 半值、或全 singleton 的历史比较不自动成为普通矩阵的物理守卫；本轮只对 one-block 这一部分重新实读推导，其它部分沿原资产继承。

## 5. t=1 八机十任务的完整映射

资源写作 R_u，u=2a+b；四台 private 是 M₀₀、M₀₁、M₁₀、M₁₁。四个支持分别为 `{0,2}`、`{1,3}`、`{0,3}`、`{1,2}`。下表写出全部有限端；其余端均为 infinity。`I_gℓa` 的资源坐标 b=ℓ+ga。循环选择为 ℓ(0)=0、ℓ(1)=1。

| 原 job ID | 本页名称／Kronecker 基例名称 | 全部有限端及原时间 | 本次重推的达界去向 |
|---:|---|---|---|
| 0 | J₀=A₀ | M₀₀:1，M₀₁:1 | M₀₀ |
| 1 | J₁=A₁ | M₁₀:1，M₁₁:1 | M₁₁ |
| 2 | I₀₀₀=B₀₀₀ | M₀₀:1/2，R₀:1 | R₀ |
| 3 | I₀₀₁=B₀₀₁ | M₀₀:1/2，R₂:1 | M₀₀ |
| 4 | I₀₁₀=B₀₁₀ | M₀₁:1/2，R₁:1 | M₀₁ |
| 5 | I₀₁₁=B₀₁₁ | M₀₁:1/2，R₃:1 | M₀₁ |
| 6 | I₁₀₀=B₁₀₀ | M₁₀:1/2，R₀:1 | M₁₀ |
| 7 | I₁₀₁=B₁₀₁ | M₁₀:1/2，R₃:1 | M₁₀ |
| 8 | I₁₁₀=B₁₁₀ | M₁₁:1/2，R₁:1 | R₁ |
| 9 | I₁₁₁=B₁₁₁ | M₁₁:1/2，R₂:1 | M₁₁ |

与 Kronecker 基例的逐机对应为 `M_gℓ=S_gℓ`、`R_(2a+b)=R_(a,b)`。原 sparse 审计的机器次序先 R 后 M；Kronecker 正文先 S 后 R。故原编号 0…7 的置换为 `(4,5,6,7,0,1,2,3)`，不能直接把两个编号当同序。任务次序完全一致：两个 selectors 后接字典序八件 B_gℓa；所有 20 个有限端和时间均保持。

上表负载为 M₀₀=M₁₁=3/2、M₀₁=M₁₀=1、R₀=R₁=1、R₂=R₃=0。任意标签的两组完整支持恰交一资源，C<3/2 时所选 private 都不能留任何半时 incidence，遂迫交点承两件 unit，矛盾。因此八机十任务的精确值是 3/2。该身份映射只说明 P₁ 是同一基矩阵；不把本族 P₂ 的 32机68任务与完整平方的64机100任务混同。

## 6. 有限运行的实际边界与本轮检查

原程序 main 固定 t=1,2,3,4；它从全部资源宇宙按 indexed state 支持方程构建完整 sparse P，未从 witness 倒造输入。每原 job 的全部有限端实际保留；独立检查再核全部任务、资格、原时间、起讫、资源和 private 负载。补组检查只有全部有序补组／状态对，共 D³ 条；不是所有一般组对。`exhaustive_t1_actual_opt` 明确拒绝 t≠1，仅 t=1 取每 job 全有限端的笛卡尔积，枚举 1024 份完整调度。

本轮复用前轮独立 checker `research/workspaces/map-v2/Boss7/final-review-20261116/um-transfer-finite-check.py`，全文实读后以只接收内存结果的 OUT 对象重新执行；没有改它、没有覆盖旧 JSON、没有导入原 363 行构造器／checker。该复用 checker SHA 为 `d39d357f20bb95153b429438e8b944802c21e1e5ae986a1e38032c0d83f41230`。新执行再次核 16 份 raw 的 SHA／长度、从支持方程重构全部 indexed state、全部原任务有限端、每件实际去向／原时间／起讫差／不重叠／全机负载、所有实际互补交点证书，并仅重做 t1 的完整枚举。另逐件检查所有 start/finish/time 等字段确为整数且 start≥0、finish>start。该事件是“复用已有独立实现的新执行”，不冒称又写了一个新的独立程序，也不是重跑历史原 audit 的15输出。

| t | 原任务／机器 | 有限端 | 全状态数 | 重算有序补组证书 | 给定完整见证峰 | 本轮完整优化 |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 10／8 | 20 | 4 | 8 | 3/2 | 1024份；3半单位84份，4半单位940份 |
| 2 | 68／32 | 144 | 16 | 64 | 5/4 | 未做 |
| 3 | 520／128 | 1088 | 64 | 512 | 9/8 | 未做 |
| 4 | 4112／512 | 8448 | 256 | 4096 | 17/16 | 未做 |

上述检查全部通过。原程序产生15个文件，其中 manifest 列14成员；第16份 root_original_matrix_verification 是另一个历史独立事件，不是原程序第16输出。本轮重执行前轮checker也不改变这些历史归属。

有限 t1..4 运行仅给这四份完整 sparse P 的 witness／交点／身份检查和 t1 精确 optimum；t≥2 没有找 optimum，更没有扫描所有 t、实现 T/D 正规形、认证其它 tensor、困难源或一般 UM。一般 V/OPT 精确值由 §3 的全部量词证明承担。规模按显式 D³+D 任务收费，不声称 poly(t)。因此 `checks/context` 边仍只能作有限证据，核心资源 coverage 保持 isolated-after-review，不能改成证明一般定理的 linked。

## 7. 资产与交付处置

本任务复制两个旧 JSON 到独立新目录，保原 edge_id、全部数学文字、kind、status、关系模式和原 evidence，仅更新 reviewed_by／review_note 并重新 edge-bind。旧文件原字节保留。`binary-one-block-bare-matrix.json` 为 accepted 的完整 logical specializes；`bare-matrix-audit-actual-jobs.json` 为 accepted 的 contextual checks，二者范围不同。

新收据对直接前批全部20项资产逐项处置：这两项 replaced 指向新 assets 内对应路径，另18项 retained 保前批 SHA。本说明作为第21项 asset。覆盖17个核心，其中2个核心定向重新实读（one-block core及实际审计入口），15个继承前批；共享只读 A 按 v3 当前 pin 重核。本轮不把继承数学写作新盲审，不把原 source_refresh 的 row-spread 重核重新计作本轮活动。原 follow_up_tasks=[] 与 closed_overlaps=[] 保持。
