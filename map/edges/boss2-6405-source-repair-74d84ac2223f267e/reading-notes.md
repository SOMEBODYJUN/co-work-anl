# Boss2 6405 Cartesian / 稀疏投影 / Santa 定向修复笔记

任务：boss2-6405-source-repair-74d84ac2223f267e。只写本任务 write_paths，队列与 Git 由 Boss 处理。本文记录本次实际连续阅读，不承接旧收据的“本次已读”措辞为本轮事实。

## Pass 0：入口、身份与改版定位

已读 AGENTS.md、IMPLEMENTATION.md 全文、03-map-worker.md、任务完整定义及六核心/七只读对象的当前完整数学字段（来源索引以现行 registry 为准）。旧任务状态 done/Boss1，当前 claimed/Boss2。旧五资产中 Cartesian、quota、DAG 与 q2 的 pins 未变；BLMRS 源 M-5ecd 的资源正文从 3cdd… 改为 c10e…，旧物理构造边必须替换并重绑。原四边可按实际审读保留；不改旧文件。

本轮任务 context_plan 没有单独 reading_passes，采用依序：P1 Cartesian/quota；P2 q2 与开放调度；P3 restricted/DAG；P4 normalized bridge/normal-form；P5 general Santa 位保持与冻结 PDF。每 pass 对指定阅读引用去重，section-only 不冒称全文。大型 exact-witnesses 用完整 JSON 解析和逐 fixture Fraction 枚举复核，未逐字符复述。

## Pass 1a：两条主证明（全文）

已完整实读：逐坐标一致菜单的整数资源配额；裸笛卡尔菜单乘积的精确反向放大。读及 frontmatter、§1–7/8、来源与历史审查界限。

裸族 D=2^t。补组 g+1 的任意选态恰交一真实资源，故任意 partial min 件数≤D−1；循环标签 ℓ_i(g)=g_{i+1}、a≠1 给每组 D−1 件，差分 δ_{i+1}=a_iδ_i 沿零坐标消零；逆恢复给所有 a≠1,b 的唯一领取组。完整任务调度把未选 state 全留 private，已选仅留一 incidence，峰 1+1/D。任意 C<2 时 unit 资源独占，实际 selector 目的地及 exports 解码；共同资源两件原 incidence 至少一件留已选 private，故全调度下界。t=1 自环有效；t=0 不在域。

固定任意二元 f 的全资源统一平移化零标签，不是逐组重命名。每坐标三符号并集给 3^t 总容量。资源有 h 个共同符号向全部兼容组各送 2^−h，给每个组 (3/2)^t，并对任意 Hall 子集 A 给 |N(A)|≥(3/2)^t|A|。槽匹配/整数容量流给每组 k=floor(3^t/2^t)，于是 V_obl=k/D，优化 f 同值。连续所选图值 (3/4)^t 只是分数松弛；不得当不可拆配额或普通 UM 值。

联合而非单独使用两值，任意同菜单 repair 合同对裸达界 A_t 需 c≤k/(D−1)→0。对固定 θ<1 这些 A_t 最终都在高值域，故即使重选全部 f/bundles 且不要求算法仍无固定 c>0。θ=1 空域、衰减 c、改变对象的 compiler 不被排除。普通 selectors 并未物理实现 coordinate consistency；无约束 OPT 仍趋1。

裸 P2 与完整矩阵 Kronecker 平方为不同操作/任务集合，不能混值。正规形保值只保已经改善的 NO，不能恢复源困难性；需另核真实树/path合同，见 P4。

## Pass 1b：审查与冻结清单（全文）

已完整实读分域审查、配额两次读后、反向放大冻结审计、独立实际稀疏审计、q元仿射证明分工审查及 Cartesian manifest。后者只核其清单，未据清单冒称本轮读过全部 raw 输出。审查中的历史审者独立性、有限运行和本轮核读分别保存。二元每固定 f 同值，不能扩成 q>2 每固定非线性 f 同值；qary 三域是选择域优化。固定 A 的 floor Σ_a q^(−nullity) 来自每个 Hall 子集与全 union 两侧；非空域限制保最大值有定义。无新 qary 逻辑端点需要 read-add。

本轮 verify_local.py 自足按定义枚举 t=1..4 的补组交点、循环见证及 canonical f=0 的全部 Hall 子集（含空集），t≤3 完全枚举固定 f 的全局平移；t1 枚举全部 1024 个原调度得 3/2。t4 65536 个组子集已核，未声称枚举全部 t4 f；四组任务/机器计数、k 与 repair 比值由 Fraction 回算。它们是本轮有限复核，任意 t 的结论仍依一般证明。

## Pass 2：q2、开放接口与有限证据

已全文实读 q2 主定理、开放转移问题、UM 定义、候选加强审查；有限核验文件也全文读取（超过任务最低指定两章，不把 heavy 对象作本核心前提）。完整解析 exact-witnesses 的全部字节；逐 fixture Fraction 复算 36 shift 与 1 nonuniform 的所有 μ/π/ξ、非负归一、domination、τ、β、refined、q1、两阶段中间值、实际标签与 1296 单标签对。heavy 部分仅完整解析并识别字段，未作本任务数学认证。

关键推导：右在共同 support S_v 均匀、左按共同 μ_u，α_e≥τ_e 给期望 Σwτ/s_v≥β/L；左各自 argmax 后右各自最佳响应，均不降同一个全局期望，无需 ξ 来自共同全局律。共同顶点 μ 不能换成逐边 μ。q1 β²/L 正确但较弱，初始实际期望不单调；nonuniform 原 μ 19/36 > uniform 11/24，最终 3/4、保证 13/48，经本轮程序精确复算。

q2 已付给证书后的最后 soundness，但 Fδ 合法矩阵、YES 全任务 T 调度、对任意实际 σ:C≤(2−δ)T 的共同 μ/ξ/β/L 提取、相匹配 source hardness 仍独立开放。NO 非空 γ≥1/R，成功须严格 β/L>γ、L<β/γ≤βR；β=θ,L=θR 只给 1/R，所有整数 R≥L 的 shift 锐族恰达，不能凭参数改进。现有 accepted/conditional contribution 精确，不需另发重复研究比较任务；不把 open 归约记为解决。

## Pass 3：DAG / restricted（指定引用及主证明全文）

已全文读 Santa受限/归一化双源审查、压缩DAG桥、原 rooted_dag_token_bridge_review、三源有限审查、根参数双实现核验。压缩 q=min(k,d) 与单filler保每home本地总量1；根unit及 C<2 使每已达点恰一unit输入，所有外送弧进入同一根可达树，正需求输出叶照样计分。反向递归删整棵子树、每点截min(k,度)，保 b(H) 并回填全体非树任务。OPT2端点靠全本地基线，不在C2误用unit独占。Γ按显式出度枚举，不按二进制k值展开。

restricted边界为同一物品所有非零端点必须同值；存在k>1,d>0时q≥1故真实token含1/k与1，最小k2/d1仍有filler但不消冲突。k>1,d0只有单home filler，故统一k1只是消除这种冲突的充分限制，不是逐点必要条件。统一k1下解码树每点≤1条外送、截1分数仅0/1；原DAG可有多孩子。旧资产已精确作此修正，本轮保其原SHA。不能将端点检查称作max-min/makespan目标等价或一般复杂度结论。

## Pass 4：归一化桥及正规形

已读任务指定：归一化菜单资源的“完整flat与SC”；六源后端审查§1/2/3/5；Santa转换资料的五个指定完整H1章节；状态dummy全任务解码审查全文；CONFIG v3审查全文。已全文读三态正规形、资源度三路径、三坐标零权切片嵌入、三坐标/三态范围审查、最终章节版本审查；裸菜单关联审查的根H1覆盖全文（含旧palette对比）。未把这些章节里的来源链接当成又读过全部原件。

norm1完整flat的SC桥每组K−1不可拆own dummies；任意allocation总有一个dummy-free agent，只取它的真实bundle而不拼多个states；得到SCOPT=V、UMOPT=2−V。任意给定t∈[0,1]双向含t0/C2，反向正值仅C<2用unit独占。W≤1必须先增广并重定义V；一般Santa行、resource组度和SC agent度不可替换。

真实树T每顶点一selector，K1原位，K>1旧selector资格改root；任意C<2扩展保全部旧incidence原端，反向root强迫链取一个leaf，off-path可额外活动。路径D每helper恰一selector与两件incidence，旧菜单/selector资格保持，只按组把资源端映port；d0保unused,d1无helper。d−1选中helper必外送占不同port，至多一旧外送；未选helper额外外送只增加占用。先T后D保三态与资源度三，0<v≤1 partial及C<2全任务双向，有限最大值/全private≤2保V0/OPT2。

故裸P_t经N得到精确同V=1−2^−t、OPT=1+2^−t；保值不能修复NO。这是目标bare-read-after §2–5的完整局部贡献，非整个历史/palette审查结论。输出含新增singleton，已不在每state恰2^t项的裸族。三坐标零格表示保任意完整调度但允许零格与indexed异成本，不制造一致性或困难源。palette另一操作坏YES，不能与裸乘积改善NO合成“所有张量失败”。

## Pass 5：一般 Santa 与当前源改版

已读有理位保持主证明全文、Santa条件双源审查全文；当前圣诞老人遇到Makespan资源§1；共同容量导航、三维束入口、困难性导入文献三全文。旧材料中的位增长待补是历史状态；当前M-491 v2主证明已付。强SCHA_det^N仍独立未证；已知Santa低于2困难阈值不能代替无任何固定常数假设。现有 canonical 条件边 um-f6bc5acc-santa-rational-bit-bridge-gives-conditional-reverse-barrier 已承担 M-491→SCHA条件反面，无需新比较任务。

冻结 BLMRS v1 PDF SHA fc907…全37页以pdftotext -layout导出，连续读完整1975行（1–270、271–750、751–1210、1211–1640、1641–1975），并非只读所需定理页。实际承重聚焦物理第3页Theorem1、第9–12页配置与Lemma10–14、第21–23页Appendix B；其余matroid与two-value算法只是完整阅读背景，不作本任务新数学认证。没有用其它版本替代被冻结v1。

方向：Santa实例→UM实例归约，使假设的UM算法→实际Santa算法。配置机含每人一选机unit、每配置按各类型计数的真实jobs；所有未选配置全部留home归一负载1；所选配置外送价值≥|c|(2−C)，资源unit给无重复真实物品。固定α≥2、η>0；一般UM实际det bit-poly算法是桥的前提，而不是已给算法。

Appendix B的字面删值切点对9/20、11/20、ε1/10确留下11/20<10/11，已由新版有理证明修补。取有理s,q=1+s，最低连续grid≤s/n；删除≤s、值rounding/数量rounding/模κ strictly-increasing稀疏各损失q，b=(1−s)/q³。保全部grid下标避免缺类型造成间距失真；数量ceil(q^ell)≤d且≥d/q；tail q^−κ/(1−q^−κ)≤s。每模类支持位置子集和正数量子集唯一递增匹配，配置数(n+1)^O_s(1)。总件数≤n过滤、|c|≥b确保正确猜值有峰1完整见证。

禁止端可用3，所有成功C<2避开；不合法/高峰输出必须实际核回拒绝。固定有理a0∈[α/b,α+η)，每T≤OPT必接受且输出真实原值≥T/a0；高猜可任意接受，拒绝才蕴含T>OPT。输入分母积Q给OPT网格，有界整数二分保上端>QOPT、下端带真实见证，终止相邻下端≥QOPT；无需猜测接受性单调。Q/U/grid/配置分母和物理耗时都是输入位长多项式，零资源/OPT0独立返回零值分配。

verify_rational_contract.py 用Fraction核字面删值反例、7坐标各0..3数量的16384种pattern（q3/2、κ3，确有同类多个位置）及2036种含任意高猜接受性的二分predicate，并核六组固定α/η参数存在性示例。全参数结论依上述证明；本轮没有构造或测试假设中的UM近似算法。

## 交付决定与未付义务

旧四边完整数学仍有效且输入未变，按SHA retained；只以本任务新边替换旧BLMRS物理构造边的过时资源SHA/endpoint pin，保其正确方向并展开有理修补。当前/旧任务均无mandatory follow-up对象对；无read-add需要。q2→开放转移只accepted/conditional局部贡献；SCHA反面只conditional；本轮无尚有缺步却标accepted的新增关系。

已读完本任务全部指定正文跨度和必要PDF，没有将未读原始链接材料、heavy fixture数学、历史程序运行或外部新颖性算完成。仍未付：普通UM物理一致性compiler、q2所列Fδ/YES/任意低σ共同证书/source hardness、一般Santa无常数复杂度假设。这些是已定位研究义务，非本任务输入身份needs-decision。
