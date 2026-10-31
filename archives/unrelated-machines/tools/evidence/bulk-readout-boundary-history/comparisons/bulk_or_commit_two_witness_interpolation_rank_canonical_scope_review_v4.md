# Bulk two-witness插值：rank正式v4指定范围审查

审查者：rank_deficiency_fee，2026-10-18。仅clone外scratch新建本记录，不改canonical、repo、raw、旧审查或Work/Git。

## 1. 实际读取对象、精确字节与范围

本次实际读取canonical：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/bulk_or_commit_two_witness_interpolation.md`

whole SHA256：`fa574190fc13aac401ff21a742c005418ed56a64015966ad96d8d4e265b22ddb`，总字节数21517。

实际逐字读取并正式认证的数学范围是 **§6 header、§6.1以及全部§6–10**，对象ID `UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`。实际另读取§1全部backbone定义作为依赖，特别核原job有限端、selector标签、完整两见证及对象计数；§1旧J资格限制已由§6明确为v4替换。

本记录不将旧§1–5 v3冒记为重新全审，也未对§2–5作新的完整数学认证。实际回算canonical最初8153 bytes之SHA256为 `df8d61b09dcdce43f7b76d50c8c981e80d91cdcce5a3a28b063e4cd317004a48`，与root指定旧前缀hash完全一致；这项字节检查不等于旧v3范围的重新证明审查。

## 2. 已冻结来源与实际读取先后

此前仅据指定完整statement独立重构并冻结：

- Exact：`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_statement_only_v4.md`，SHA256 `fb086626633dcdd8d56115dde34af96f6031873775da36b205bc274d9456420e`。
- 独立Exact-first记录：`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_rank_exact_first_review_v4.md`，SHA256 `81bd134c850af6bf78aad4fb067f8605079c6a08e690bff81e064d574efdb9f7`。

Root实际读取独立记录后才解封作者Proof。本agent随后实际全文读作者Proof并另冻读后：

- 作者Proof：`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_proof_v4.md`，SHA256 `d5e37350172b8bc95393352728d1a1a9d6be117c4dc082232564ebf693ff459c`。
- 作者读后：`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_rank_author_read_after_v4.md`，SHA256 `2f3b3599686df0e4cc539a9232c27ed5a40514c930ebfa6af2f4f1c214c7596a`。

此次canonical审查是在root实际读作者读后、提供最终wholeSHA和指定scope后另行进行。原独立证明采用occurrence双matching的二染色；作者及canonical采用整数flow。二者是同一标准配对舍入保证的正确机制，不把读后或root共同推导倒填为blind独立来源。

## 3. 结论与一般逐机合同

**正式结论：指定canonical字节的§6 header与全部§6–10同已冻结Exact、作者Proof及独立重构一致，未发现standing fatal；本记录认证其限定v4数学和构造范围。**

一般输入为显式普通P、m≥1、可空原jobs Z、binary非负有理时间、T≥0及两份同一P的完整actual负载≤T。指定F原jobs及合法原目的地ν，不假设ν曾在旧support中，也不假设ν的load≤T。定义t_i、两份非F负载L_i^b、双见证occurrence计数N_i和used最大值d_i后，canonical正确给出同一完整τ：F全部按ν；每枚非F只用自身两旧实际目的地；全部机器同时满足件数≤ceil(N_i/2)、非F负载≤(L_i^0+L_i^1+d_i)/2、总负载再加真实t_i。

每个非F原job保留两份带标号occurrence，即使两次同机仍计两份。逐机降序配对、odd末项singleton；job到pair的单位容量flow有每occurrence1/2的fractional全覆盖，因此整数maxflow全覆盖。同job两occurrences同pair时合并边仍容量1，支持总流1，避免丢半流。每个flow选中原job恰执行一次，pair属于原machine而非新物理执行端。Same-job/same-machine两次实际p相同，输出时间不含歧义。

Pair至多一件给件数界；选中负载≤奇序项和≤(总和+最大项)/2给负载界。所有机器共享同一整流，故件数与负载非各取不同输出。F按新ν端全部加回，未遗漏原任务或将新端时间误算为旧d_i。

旧见证非负负载保证L_i^b,d_i≤T，故t_i=0时≤3T/2；t_i=T且一份旧F负载T时≤3T/2+d_i/2；两份旧F负载均T时非F used端只能zero，d_i=0且输出总负载恰t_i。这些包括T=0，不能把“负载0”改成“没有原job”。

## 4. §1依赖及§8非pool域

§1实际backbone为每a的2k个M、2k个C、2个A、2k个q、2k个b和一f。q三个原端M_i:ρ、M_(i+):1、所属pool:1/k；正b在M_i:ρ/C_i:1，负b在M_(i+):ρ/C_i:1；f的两个pool端均1。不同名字物理互异。r≥2、偶k≥2、1/2<ρ<1；每J至少一原finite端，无免费preload或隐藏aux。

每变量机器4k+2、原jobs4k+1、finite端10k+2，故加I/J后m=r(4k+2)+|I|、n=r(4k+1)+|J|、finite数r(10k+2)+E_J，dense mn。v4仅按本版本J资格重新计E_J，其余backbone未改变。§1旧c/K统计未作为v4算法容量使用，§6与§8明确撤销旧J范围及旧强输出合同。

§8允许J在任意I/M/正负C原端实际执行，原时间任意非负有理，唯不接任何A。将所有非f原q/b/J共同代入一般flow、所有f固定原正pool，得到全False。同一输出所有非pool实际load≤3/2；**M/C只保证≤3/2，未主张≤1、恰一job或旧返回模式**。

Pool只含q/f。u/v正pool的一份输入被f1占满、另一份至多k个q，偶k结合件数界使新f外至多k/2个q，实际load≤3/2；其余正pool恰1。u/v负pool≤1/2，其余负pool≤1。全部原q/b/f/J在同一完整τ中执行一次，非f仅自身旧目的地，整体≤3/2。任意medium/tiny异权J、zero和实际共居均已计入，没有先只安排J再漏backbone。

## 5. §9任意pool域与d实际身份必要性

J接任意原machine包括正负pool时，d准确限于u/v正pool上两份actual真正用过的非f原时间。包含q/J及zero，空取0，actual strict给0≤d≤1；未用大finite资格不能增大d。

相同完整flow输出非pool≤3/2。u/v正pool有一份f1输入、另一份非F≤1，新增f1后≤3/2+d/2；其余正pool两份均f1，非f实际used端只能zero，输出恰1且可有zero原J。u/v负pool≤1，其余负pool≤3/2，故全原jobs实际峰≤3/2+d/2。Pool有任意J后不沿用§8的q-only件数加强。

β=2−δ>3/2、0<δ<1/2时，d≤1−2δ给allFalse≤β，d<1−2δ给allFalse<β。因此禁止全部C<β要求d≥1−2δ；禁止全部C≤β才要求d>1−2δ，严格/非严格等号方向正确。

若1/k<1−2δ，必要大d必须由某原J的实际positive used端取得，位于u/v正pool。另一见证该pool有f1，该同一原J不能仍停原机，所以实际目的地改变。这个事件依赖所给两见证；未用nearunit资格或静态归属不够。Canonical正确不把它写成物理读标签、固定branch、fee、OR-commit或源NO充分条件。

## 6. 零、构造性、unknown witness与最终边界

T=0、Z/F/非F为空、I/J为空、same-destination双occurrence、odd pair、zero原任务、unused finite>T（bulk >1）、ν在旧support外或ν load>T均由同一一般陈述覆盖。Zero任务保留实际执行，未以负载0删原job。应逐原job核输入assignment完整、目的地有限、真实有理负载≤阈值，并核ν合法；有效actual前件同时排除无finite端原job等不合法包装。

网络的occurrences/pairs/支持边数量按原jobs线性；有理比较排序、L/t/d求和与固定确定性整数maxflow按显式P和所有输入binary编码总位长多项式。不按1/tiny、分母数值或1/(1−ρ)展开。输出仍逐原job一枚原machine；所有算法节点都未进入P。无有限实验/软件/全球新颖性认证。

若两完整strict见证仅知存在，结论仅给相应allFalse输出存在，并非免费求未知见证的finder。无约束bulk OPT确为1：给定strict见证给上界1，r≥2保证存在unit f，而每f全部原finite时间均1给下界1。因此指定allFalse模式的逃逸结论不能当作普通UM近二NO下界。

限定v4所关闭的是§8全部非pool路线，并在任意pool域导出§9实际nearunit身份改变必要义务；它不证明新物理机制可实现，不构造源NO或near2 hardness，`UM-TARGET-v1`仍OPEN。本记录不扩为旧§1–5新全审，也不改任何既有原件。
