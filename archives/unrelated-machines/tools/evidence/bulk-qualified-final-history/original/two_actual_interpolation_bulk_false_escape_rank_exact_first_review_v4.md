# 一般two-actual插值及bulk全False：rank独立Exact-first审查 v4

审查者：rank_deficiency_fee，2026-10-18。仅实际读取指定v4完整statement后独立重构；未读取作者Proof、其它children策略、旧新root推导或文内链接的旧v1/v3策略文件。本记录先冻，只交root；仅clone外scratch，不改repo/Work/Git。

## 1. 实际读取对象与结论

实际全文读取：

`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_statement_only_v4.md`

wholeSHA256：`fb086626633dcdd8d56115dde34af96f6031873775da36b205bc274d9456420e`。

对象ID：`UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`。

**独立结论：§0一般合同(G1)–(G3)及§1–5全部bulk特化、pool定量与严格threshold必要条件均可闭合，未发现standing fatal。** 以下给自足原job构造与全部边界/位复杂度核查，不把已知strict witness的存在当免费finder。

## 2. 任意P的一般构造：occurrence配对与一致取整

给定同一显式P及两份完整actualσ⁰,σ¹，逐机load≤T≥0；F指定原jobs由原finite端ν执行。先不处理F，对每个z∉F建立两个**算法用occurrences**(0,z),(1,z)。二者始终是不同节点，即使两witness同机同端；它们不是新增真实job。

Occurrence(b,z)附机器σᵇ(z)及原时间p_(σᵇ(z),z)。对每台i，把其N_i个occurrences按附带时间非增排序，固定输入索引打破ties；相邻配成(1,2),(3,4),…，若N_i奇数留下末个未配。另对每个原z，把其两occurrences连成job pair。

在这些occurrence节点上取两类边：job pairs构成perfect matching；machine pairs构成另一matching，可能有未配节点，也可能与某job pair形成平行边。每节点度≤2，cycle边类型交替，所以所有cycles均偶，长度2的平行边cycle也有效。Paths/isolated情形同样可2-color。确定性遍历各component作2-color，选择全部color0 occurrences。

每job pair两端颜色相反，因此每个z∉F恰选一个occurrence，令τ(z)为该occurrence附带的原机器。每machine pair亦恰选一个，odd未配项至多被选一次。故

    #{z∉F:τ(z)=i}≤ceil(N_i/2)。

同一job两witness同端时仍两节点、恰一被选，输出原job一次。不能先把这两occurrences合成一个再套N_i/2；本构造没有这样做。

## 3. 同一输出中的精确逐机负载界

固定i，写排序后时间x₁≥…≥x_N≥0。选中时间至多

    x₁+x₃+x₅+…。

因非增/非负，奇偶差满足

    (x₁+x₃+…)−(x₂+x₄+…)≤x₁。

例如扣去x₁后可将−x₂+x₃、−x₄+x₅等各组为≤0，偶N时最后还剩非正项。因此

    selected load≤(Σ_h x_h+x₁)/2
                 =(L_i⁰+L_i¹+d_i)/2。

N_i0时所有量0，同一式成立。机器排序配对与job选择来自同一2-color，因此件数和负载界在**同一τ**同时成立，而非逐机各挑见证。

最后对每z∈F直接令τ(z)=ν(z)，即便它是两witness未用的新原finite端、其原时间大于T，也只向相应机加已定义t_i。全部原jobs一次、仅原机器/原资格，得到(G1)、(G2)及

    load_i(τ)≤t_i+(L_i⁰+L_i¹+d_i)/2。

ν自己的load无需≤T；不能据此把完整全局峰无条件说成3T/2。

由witness负载≤T，L_i⁰,L_i¹≤T，且每个实际用过的非F时间≤T，所以d_i≤T。若t_i0，得load≤3T/2。若t_i=T且一份witness的F负载为T，该witness的L_i=0、另一份L_i≤T，因此load≤T+(T+d_i)/2=3T/2+d_i/2。若两份witness的F负载均T，则L_i⁰=L_i¹=0；非负性使所有used非F端均0，故d_i0、load_i=t_i。即使存在实际zero jobs，最后等号仍对总负载而非件数成立。

## 4. 一般域全部边界与算法复杂度

T0时所有witness已用端时间均0；非F输出仍全0，F新ν端可以正或很大，输出由t_i准确计入。没有除以T或用T0推出ν也0。F空、Z\F空、Z空、N_i奇偶、同job同机两次出现、witness间不同资格时间、zero端及未用finite>T都已覆盖。

实际生成/验证应逐原job核两witness完整/恰一次/原finite端，逐机有理回算≤T；核F⊆Z与ν完整且原finite，核P有限时间非负。无资格任务不能拥有有效witness；不能用未知witness存在性冒称可计算它。Unused大边不进入非F occurrences、d_i或L_i，但F的ν新端若用到它，照原值进入t_i。

图仅2|Z\F|节点，两类matching边各≤|Z\F|。排序、2-color及逐原job输出总位多项式；时间比较、有理和/与T阈值比较按binary位长计，不按分母、1/tiny或T数值循环。算法occurrences/pairs不是真实新machine/job/slot，输出只有原jobs的一份actual。

## 5. Backbone原矩阵和计数

r≥2、偶k≥2、1/2<ρ<1；每a有2k个M、2k个C、2个A pools。q_i三个端M_i:ρ、M_i+:1、A_(a,s_i):1/k；正b_i在M_i:ρ/C_i1、负b_i在M_i+:ρ/C_i1；f_a在两个A上time1。其余原J及I按statement显式给出，J任务身份独立、每件至少一finite端。

每变量machines4k+2、jobs4k+1。q finite6k、b finite4k、f finite2，合10k+2。因此m=r(4k+2)+|I|、n=r(4k+1)+|J|、finite r(10k+2)+E_J、dense mn，正确。k2时环长4，各原machine端仍不同。J可zero/medium/unused大边，在给定strict witnesses之外不增加隐含结构。

给两份实际σᵘ/σᵛ，其f标签仅u True或仅v True，其余所有q/b/J去向任意。对§0取T1、F={所有f_a}、ν(f_a)=A_(a,0)。该ν全部原资格合法，t_i在正pool恰1、其余机0。故输出所有f False、所有非f只用两witness原目的地。

## 6. 非pool J域：精确3/2及q件数

J无任何A finite端时，pools只有q及f。任何strict witness若f占某pool1，该机不可能还有q的positive1/k时间。非pool全部I/M/C的t_i0，由一般界同时≤3/2，无论J如何在正/负C、M、I实际tiny/medium共居。

对a≠u,v，f在两witness都占正pool，故正pool两份q occurrence都0，输出只有f、load1。

对a=u的正pool，一份witness f不在此（a True），最多k个正q；另一份有f1所以q0。N_i≤k，k偶给ceil(N_i/2)≤k/2。输出加固定f，负载≤1+(k/2)/k=3/2。a=v同理。此处件数界确实必要：仅套一般d_i/2负载项会多一个1/(2k)，不能据此偷得精确3/2。

对u,v负pool，一witness有f1因而q0，另一份最多k个负q，故输出q≤k/2（负载其实≤1/2，满足statement的≤1）。其它负pool两witness每份最多k个q，N_i≤2k，所以输出q≤k、负载≤1。全部pools及非pools在同一τ满足结论，整体≤3/2。

未宣称M/C一机一job、负C恰b、固定branch辅助件数或K_a；一般配对也不需要这些条件。只有strict witnesses存在而未输入时，上述构造仍证全False存在，但不能据此给寻找未知strict witness的算法。

## 7. 任意pool J域：逐类定量与d边界

现在J可在任意A执行。Strict实际边保证used非f时间≤1；d定义恰取u/v正pool、非f实际已用端的max，含q/J/zero，故0≤d≤1。Unused资格不算d。

* 非pool仍t_i0，负载≤3/2。
* u/v正pool的一witness有f1，因此该份非F负载0；另一份≤1。新t_i1，一般界给≤1+(1+d_i)/2≤3/2+d/2。
* 其它正pool两witness都有f1，所以L⁰=L¹=d_i0，输出总load恰1。非f可能有zero J实际共居，不能把“负载0”错说成“无jobs”。
* u/v负pool一witness有f1、另一份没有；新t_i0，非F两份负载之和≤1、d_i≤1，故load≤(1+d_i)/2≤1。
* 其它负pool两witness均无f，新t_i0，一般界≤3/2。

因此完整Cmax≤3/2+d/2，全部非f仍仅两旧目的地。J已可在pool，不能沿用仅q的pool件数界；statement已正确撤销该加强。

## 8. 严格threshold与实际nearunit J必要性

β=2−δ>3/2、0<δ<1/2。若d≤1−2δ，则3/2+d/2≤β；若d<1−2δ，则严格<β。由此：

* 禁止所有C<β的allFalse，必要d≥1−2δ；
* 禁止所有C≤β的allFalse，必要d>1−2δ。

两种等号不能互换，statement区分正确。若1/k<1−2δ，而必要大d成立，则其正max由某原J在u/v正pool的**实际used端**取得；q在此恒1/k、b没有pool端、全部f被排除。Max为正且有限，确有原job达到，不是仅unused近unit资格。

相应正pool仅在该变量为True的那份witness可接positive J，另一份有f1；该J固定同一原machine的时间为正，不能在另一strict witness仍留该机，故确实离开。它可去任何其它合法旧目的地，未证明固定branch归属、离开所有pools、支付某个fee或可实现OR-commit。此是当前两actual witnesses上的必要原job事件。

## 9. 最终结论与范围

§0任意P/T0/F新目的地、逐机件数/负载与同一assignment合同，以及§1–5全部bulk nonpool/pool量词、threshold和位复杂度均通过独立重构，未发现standing fatal。

机制为标准半整数occurrence排序配对/2-color舍入，不作新rounding理论或全球新颖性主张。它只使用给定两份真实完整strict witnesses，不提供一般UM求解/近似算法、源NO或NP-hardness；任意pool连接仍保留实际nearunit J的逃逸义务，没有从必要条件造出可高复用物理OR-commit。

未读作者Proof/其它children策略/旧新root推导，未运行有限测试或实现新软件。原statement保持原字节，后续作者Proof读后需另冻。
