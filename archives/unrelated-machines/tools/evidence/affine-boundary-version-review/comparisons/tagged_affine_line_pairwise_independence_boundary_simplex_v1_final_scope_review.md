# 两两独立结构边界合并页：simplex 最终 canonical scope 审查

Reviewer：bicriteria_set_packing_bridge，2026-10-18。仅 clone 外 scratch 新冻；不修改 repo、Git、Work、旧raw或旧审查源。

## 1. 实际读取版本与正式 scope

已实际全文读取合并 canonical：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md`

whole SHA256：`0b94156ecd6552e8ab29961ce03a5d21ddfa75cb945ab802da7115bf781970bf`。

root 正式指定本 reviewer 认证：shared header 中关于 simplex 的范围与分工，以及全部 §3–8；另实际读取 §1.3 的 V/完整 P 编码作为定义依赖。全文读取了 §1–2 作为页面 context，但本记录**不对 one-primary ID 的完整输入域、条件化 Hall/LP 或 unit theorem 作数学认证**，也不把该 Claim 的 general reviewer 读成我的审查。没有读取其原 raw Exact/作者 Proof 或 general 的独立记录。

本次认证 ID：`UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`。one-primary ID 与本 ID 分别保留；两项不互相转记证据。

结论：**PASS。指定 simplex 正文数学自足、与原 Exact 同域；全部精确值、全 PI/common C、全部任务与位长闭合，未发现 fatal。** §1.3 作为通用 norm-one 菜单定义的依赖合法，不要求把 one-primary 特殊前提套给本 simplex。

## 2. 旧证据链、原源保持与 shared header

本 reviewer 先仅据 simplex Exact 独立重构并冻结；root 实读后解封作者 Proof；本 reviewer 随后实际全文读作者 Proof 并另冻 read-after；本次才实际读上述最终 canonical。原文件保持：

- Exact：`tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md`，SHA256 `670bd2deb41f4b5fc9df6ca3f0ed460ca2daaa3a9cca38604561bfff3d7b10d2`。
- 作者 Proof：`tagged_affine_line_pairwise_independent_simplex_tiny_value_proof_v1.md`，SHA256 `4278590caacc424c5df2574ecd8d70a9d53f08fb42f0703aee9bee088913d474`。
- 独立 Exact-only：`tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_independent_review.md`，SHA256 `db3db1a1f09f1392ba880a749959171ea131d044acdb7772e0c315dcadf2112f`。
- 作者读后：`tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_author_proof_read_after.md`，SHA256 `1addfcb4e4c0e771eb7b30e03cfa699b51b4deae55abe173c824d896a618008c`。

shared header 和 §3 metadata 将 simplex 的 Exact-first、作者读后及最终 scope 路由给本 reviewer，将 §1–2 one-primary 路由给 general，符合实际分工。root 事先参与讨论、不记 blind，编写合并页不冒新的独立数学审查，均正确。当前正文没有把一个 reviewer 的结果认证转移给另一个。链接 review 页及其它 Claims 不在本次实读认证范围；metadata 中未引入软件、有限实验、外审或全球新颖性认证。

## 3. 定义依赖 §1.3 与 §3 输入合同

§1.3 的 V 对每组选择一个真实 indexed state 和任意资源子集、跨组两两不交、取 minquality，适用于后文 simplex 的 norm-one menus。它没有把 full supports 不交或某种 CONFIG 约束加入定义。完整 P 是每 indexed state 一个独立 private、每 tagged resource 一机器、每 group 一 unit selector、每个完整 state-resource incidence 一件 private p/resource1 两端 job，其它资格 infinity。零私权及未选 states 全保留。

该通用编码不依赖 one-primary 的 helper 形状。按 simplex 的 primary/fresh sets 和 H 代入，§1.3 的 S+资源数、groups+I jobs、S+2I finite options 与 §8 一致。后文引用 §1.1 的 line 公式也只是同一真实 tagged-line 资源公式，不导入 §1.1 的 one-primary 特殊域。

§3 严格规定 odd prime R>=3、任意非平方ν、显式二次域/trace、随R构成的唯一指定族；不是任意外部source family。V上界量化所有state choices和任意partial，actual下界量化每份完整合法σ。R2明确排除。全部构造、精确值和确定性总位多项式对象与原 Exact 相同，没有新分布承诺、CONFIG、NSW、source hardness或robustness对象。

## 4. §4–5：common C、所有 states、全 pairs 与原资源

变量命名和fresh padding完整：每helper在本block的R+1 parts使用primary，其余每part使用仅属于它的fresh变量；全部变量身份分离。每组真正q-ary且一part一个不同变量；primary degree R、固定intercepts恰0与所有非零j，fresh degree1/intercept0。全部K² indexed states保留，完整local relation为同一公共C的coset。

trace pairing矩阵diag(2,2ν)在odd域非奇异；T恰给K的一维F_R方向。t0对所有w定义，包括w0的first规则。E由block0和∞的basis trace coordinates分别恢复u、v，所以C维数4，R4个不同完整tuples。q个coefficient directions列全F_R4 projective directions，full simplex身份自足。

同block不同t forms独立；不同blocks的w_a,w_b或w_a,v由可逆K-linear map得到独立uniform K元素。因此全部coordinate pairs精确uniform，helper固定coset平移也保全部pairs，包括每对primary、fresh、两者混合，而非只检查其中一种。每组uniform 1/R4 certificate真实显式；它不是global satisfying assignment。

main每个state的α使对应w为0，正点D_α均在线上；v0和ζ0没有缺口。helper每state在t0处E0，真实slope−j、截距j在z1处y0，onehot正点也是原资源。norm-one和完整qR different incidences均由tag与R个横坐标保证。fresh私权0但labels仍变化，不能删去后继续称同一共同code/arity/PI对象。

每个helper能以原state覆盖任意D_a目标点：非零orthogonal w确定唯一t0，finite a用(w,0)、∞用(0,w)。同w_a的R²个原ζ由其它padding coordinates区分且仍保留，不因block投影重复而合并或删jobs。全部这些论证不改变固定编号。

## 5. §6：任意 partial、任意 actual σ、全达到调度

partial上界正确量化全部states：若有helper质量0则min上界已成立，否则每helper必须取得其唯一unit正点。每block的R−1 helpers占R+1个D_a点中的R−1个不同点，任意main state的D_α仅剩至多2个等权正点，故V<=2/(R+1)。zero/fresh资源、任意省略或额外partial cells均不增加质量。

main ζ0、D_∞预留两点、各block helpers各取不同点，并由§5找回原indexed state，给所有helpers质量1、main质量2/(R+1)，证明精确V。same choice输出完整上界：selectors进selected roots，main仅导出两正jobs，helper导出唯一正job，全部其它selected及未选states的全部incidences留自身private。包含所有zero/fresh jobs，无免费外送。资源峰1、未选root1、selected helper1、selected main 2−2/(R+1)。

反向对任意完整eligibleσ：C>=2分支直接满足所需下界；C<2时由真实selector确定原state。selected helper的正job若留private会与selector合负载2，所以必须导出；每resource unit时间使C<2时最多一件，因此每block的selected helpers真的占R−1个不同D_a点。不论未选states的jobs另怎样安排，selected main至多导出两正jobs，private至少留R−1件1/(R+1)再加selector，负载>=2−2/(R+1)。额外exports只能消耗容量，没有假设它们不存在。两端等号均覆盖。

因此完整实际OPT的精确值正确，不是局部configuration或仅partial模式的下界。私时0从未视为删除任务，所有qualifications都是原finite options。

**单main删除边界**也自足成立：按正文明确删除main group的selector、全部main-state incjobs和private roots，保留全部helpers/resources；每block R−1 helpers可注入R+1个D_a点。helper选中onehot导出、其余jobs全留自身private，包含全部未选/helperzero jobs，给unit全调度与V1；remaining helper selectors保证OPT>=1，所以实际OPT1。正文“按§2相同规则”只是在复用这个通用完整assignment模板，本审查不以one-primary定理为删除结论的前提，也不因此认证§2。一个main删除即unit的事实明确阻止把本例升级为dummy-budget/deletion-robust hardness。

## 6. §7：global ordinary CSP 精确值

变量和每组q-ary coset constraint按实际公共parts定义完整。block code每个vector有zero coordinate，所以不含非零constant，线性性给不同j的−j·1+C_block cosets两两不交。main满足时全部block在j0 coset，故没有helper满足；main不满足时每block至多一helper，总数<=B。

全部primary设−1，各block选H_(a,1)的ζ0并把其专属fresh设0，实际同时满足B项。main不能接受全−1：每个main codeword在其指定block全零；其它同blockhelper也不能增加满足数。因此val_CSP=B/[1+B(R−1)]精确。没有用local PI替代global赋值，也没有把小value当复杂性gap。

## 7. §8：exact counts、有限O11、denseO19与总位长

H、G、q及N_var、N_state、I_line、N_resource、N_machine、N_job全部公式与原Exact一致。每incidence的两个namespace端、每selector的R4选项真实保留，finite entries2I_line+GR4正确，即使private p0仍计一有限端。唯一finite处理数值0、1/(R+1)、1正确，local probability1/R4是certificate而非额外处理时间。

q、G为O(R3)，variables O(R6)、states O(R7)、machines/resources O(R8)、incidences/jobs O(R11)，所以完整finite-option表示加state/line/label资料和localcertificates O(R11 polylogR)。§8明确dense job×machine有O(R19)项而非R11，且全部infinity若按主模型列出仍是展开规模多项式，没有混用两种大小。

nonresidue扫描、field operations、trace-kernel目标点查表、rational probabilities与weights、indices、全部assignment输出均按实际展开对象位多项式；不声称binary R下poly(logR)免费展开、compact oracle或隐藏reciprocal-weight复制。小R3没有例外；R2明确不属于simplex域，不从one-primary的R2合法性传递。

## 8. Scope 与最终结论

§8将两个ID的结构差异准确落在helper primary数量：本simplex每helper共同包含R+1个primary，不能套只条件化一个primary的边际推论；它也不声称恰两个primary已有相同构造。本记录认可这些对象差异，但不对one-primary unit theorem作二次数学审查。

每个simplex实例内部C共同，C与q随R变、q约R3，不是固定arity且R相对arity充分大的既核primary参数域；未声称Chan/LST hard image。unique main删除unit、无robust/deletion-budget hardness、无general UM近二hardness或新算法、缺少sourceNO decoder/复杂性归约等限制全部保留。末段的对照应按两项各自已有审查读，不能解释为本 reviewer全审了两项。`UM-TARGET-v1`仍OPEN。

本wholeSHA版本的simplex §3–8和相关shared header完整、正确、自足地落地本reviewer先行Exact-only及作者读后结论；§1.3一般V/full-P定义依赖也已实际读取核对。无须修改数学或范围。本次未运行新软件/有限实验，也不认证外审、全球新颖性或其它页。所有旧raw与两份旧review保持原字节；未来正文改字节须另行指定版本并实读，不自动延伸本认证。
