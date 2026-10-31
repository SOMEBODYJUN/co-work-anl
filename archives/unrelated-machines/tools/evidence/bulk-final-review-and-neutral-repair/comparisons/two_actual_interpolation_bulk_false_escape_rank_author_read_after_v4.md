# 一般two-actual插值及bulk全False：rank作者Proof读后 v4

审查者：rank_deficiency_fee，2026-10-18。仅clone外scratch；本记录单独新建，不修改原statement、独立Exact-first记录或作者Proof，不改repo/Work/Git。

## 1. 实际读取对象与先后路由

在root实际全文读取下列独立记录并随后明确解封作者Proof之后，本次实际全文读取作者Proof：

`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_proof_v4.md`

whole SHA256：`d5e37350172b8bc95393352728d1a1a9d6be117c4dc082232564ebf693ff459c`。

对应statement：

`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_statement_only_v4.md`

whole SHA256：`fb086626633dcdd8d56115dde34af96f6031873775da36b205bc274d9456420e`。

此前独立Exact-first全文记录：

`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_rank_exact_first_review_v4.md`

whole SHA256：`81bd134c850af6bf78aad4fb067f8605079c6a08e690bff81e064d574efdb9f7`。

原独立记录只据指定完整statement独立重构，冻结时未读作者Proof或其它children策略。此次另冻作者读后，不把读后结论倒填为独立来源。本次重新回算以上三个原文件SHA，均与指定值一致。对象ID为 `UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`。本记录不认证未来尚未读取的canonical字节。

## 2. 完整结论

作者Proof §§1–6与指定statement以及此前独立重构相合，未发现standing fatal。作者用排序pair节点上的一次整数flow；独立记录用两种occurrence配对形成的偶cycle/path二染色。二者都是标准半整数排序配对舍入机制，算法表达不同不构成数学冲突。本次认证一般逐机合同、完整原jobs输出、bulk两种J域、严格threshold与显式位多项式构造；不认证新的普通UM近似算法、源NO、可复用OR-commit或hardness。

## 3. Flow与same-destination双occurrence

每个原非F job在两actual中均保留各一份带标签occurrence，即便两端相同也计两份。每台原机按本机真实处理时间降序，相邻两份组成容量1 pair，奇数末尾允许singleton pair。原job经自身occurrence向所在pair连边，source到原job容量1、pair到sink容量1。

每occurrence送1/2形成总值恰为非F原job数的可行fractional flow。若同一job两occurrences落同pair，合并其job-pair边后需要且确实允许总流1；不能错误保留容量1/2。整数容量maxflow遂给同value整数流。每原job恰选一条真实occurrence支持的边，最后在该pair所属原machine按原p执行一次。即使同job两候选machine相同或其occurrences分入不同pairs，原job节点容量1仍排除重复执行。

Pair只是算法节点，不是新增真实执行machine，也未复制输出job。若一条job-pair边有两份同pair支持，它们必在同一原机，对同一原job真实处理时间相同，因此不存在选中flow边后真实时间不确定的问题。

## 4. 同一完整输出同时满足件数与负载

对某机排序为p_1≥p_2≥⋯≥0。每pair至多一件，故件数≤ceil(N_i/2)，实际非F负载≤Σ_h p_(2h−1)。降序非负性给交错和≤p_1，因而

    nonF_load_i ≤ (L_i^0+L_i^1+d_i)/2。

同一次全局整数flow决定所有非F原job，所以所有机器的件数界、负载界同时成立。这里不是先取一个低件数schedule再另取一个低负载schedule。Occurrence总和精确计入两份actual；同端两次出现仍按两次加进L_i^0+L_i^1和N_i。最后将F逐原job按合法ν全部加回，得到同一完整τ及

    load_i(τ) ≤ t_i+(L_i^0+L_i^1+d_i)/2。

ν可以用两witness未使用的新原finite端，原时间可大于T；它的全部真实负载按t_i加回，而非套非F的d_i或假设ν也≤T。一般式无遗漏全体原jobs。

T=0、F空、非F空、全jobs空、N_i奇偶、actual zero端均成立。两输入F本机load均T时，非F实际负载与d_i均0；仍可有合法zero jobs，作者正确只断言负载而非空件数。未用finite>T端不进入occurrences或d_i，但若ν实际使用则照原值进入t_i。

## 5. Bulk任意非pool J与任意pool J

取全部原f为F并强制ν(f_a)=A_(a,0)，对所有其余q/b/J一起运行同一个flow，真实输出全部f False。

J不接pool时，非pool I/M/C的t_i=0，统一实际load≤3/2，允许任意原J异权/zero共居。u/v正pool只在一份strict输入中free，故q occurrences≤k；偶k结合件数界给输出q≤k/2，新f加回后≤3/2。其余正pool恰负载1。u/v负pool≤1/2、其余负pool≤1。作者正确使用件数加强取得精确3/2，并未沿用不适用的旧v3 K_a、C/M恰一job等输出合同。

J可接任意pool时，d只取两actual在u/v正pool实际用过的非F原端max，含q/J/zero，空取0且d≤1。u/v正pool一份输入含f1，另一份非F总load≤1，故新load≤3/2+d/2；其余正pool两份均含f1，非F已用端只能zero，新load恰1。u/v负pool≤1，其余负pool≤3/2，全部非pool≤3/2，故完整峰≤3/2+d/2。作者没有将仅q的pool件数加强误搬到任意J域。

## 6. d的used阈值与必要性方向

β=2−δ>3/2、0<δ<1/2时，d≤1−2δ推出实际峰≤β；d<1−2δ推出实际峰<β。因此禁止allFalse的所有C<β只推出d≥1−2δ，禁止所有C≤β才推出d>1−2δ，等号方向准确。

若1/k<1−2δ，则达到必要大d的端不能来自q，b无pool端而f被排除，必为某原J在u或v正pool的一份strict actual中的positive used端。另一份strict actual在此已有f1，该同一原J必须真正离开此原机。Unused大资格不算d，另一份actual也不能通过同机zero时间更换身份，因为同一原job在同一原机的p固定。本必要事件不证明静态guard owner、固定branch归属、跨全部pools迁移、fee或OR-commit。

## 7. 对象计数、位复杂度及范围

Backbone每变量机器4k+2、原jobs4k+1、finite端10k+2；附加I/J后为statement的m、n和finite计数。原矩阵及全部实际输出不增加隐藏aux/preload或删除zero原job。

算法仅2|Z\F|份occurrences、线性数量pair与原job支持边，排序及一次整数maxflow均按显式输入位长多项式。比较与L/t/d有理求和的位长受输入总位长多项式控制，不按1/T、1/tiny、分母数值或ρ精度循环。两完整actual与ν应逐原job核资格、逐机有理回算；无有效actual前件不触发结论。若两witness只知存在，结论给输出存在，不给未知witness免费finder。

未运行有限审计或声称新的软件验证；本次是作者Proof实际全文读后的一致性审查。保留此前Exact-first记录和所有原raw字节。未来canonical若要登记，仍需另行实际读取其完整指定范围及wholeSHA。
