# 最终规范全文与旧 NSW 纠错的实际范围审查

日期：2026-10-18。审者：current_hardness_sources。仅写 clone 外本记录；未编辑任何共享/隔离仓库文件，未作 git 或 Work 操作。

## 1. 实际读取的精确版本与作者关系

本次先核哈希，再实际全文读取新规范正文：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11-negative/research/current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md`

191行，SHA256 `3c0919735dbc90793fe99336e24f3b15d37b09bb8e7e9e138c71437e08acff01`。读取覆盖标题、引言、全部§1–6、三个新IDs与最后Evidence，不是只读hash或抽样段。

本人此前对v1/v2先冻结独立重构，再实际读正式Exact，再实际全文读作者Proof；该次序及各hash见本目录既有独立稿和read-after记录。本轮是最终规范正文的实际读后审查，不新增blind或全新独立票。**§5近完美YES判别是本人提出/编写的子结论：该部分此次只记作者自查与规范忠实性核对，不记本人独立审查；应由另一位Exact-first审者的记录承重。** 对值桥、一般福利LP/舍入、whole-class13/8与γ纠错，可记此前独立重构基础上的最终实际读后攻击。

随后按root请求实际读取现行旧NSW页的header/共用前置文字、第三ID对象及全部C–F、来源/范围结尾；**未重审A或B正文和其完整长证明**。现行文件SHA为 `214eb466e53629952d70b6c78a857af628dd5a523a01b64a372f06b686b9b6e0`。另核原规范全文备份hash为 `2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81`，路径 `history/source/notes/unrelated_machines/explicit_xos_fractional_nsw_original_canonical_before_gamma_correction.md`；本次只核该备份hash，不冒称重新通读备份全部A/B。

本次亦实际全文读旧 `explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md`；新规范指向的 `normalized_gated_menu_welfare_review.md` 在本次读取时尚未存在，因此不代签其将来内容或记为已读。root需在checkpoint前建立真实审查记录链接。

## 2. 新规范正文数学攻击结果

**在上述关系限制下，未发现fatal。** 三个新ID的对象/量词/结论与已冻Exact及自足证明一致；没有把一般UM、原flat或NP条件夸大。

### §1–2 完整域与实际值

norm1、显式有限indexed states、同state资源distinct、非负binary rationals、四类机器互异、全部原jobs/有限端均明示；零incidence真实job保留。数目 `1+n+S+m`、`1+2n+I`、`1+3n+S+2I` 核算正确。缺失项仅作为效用0、不造物理job，避免隐藏零端。

任意H的前向构造同时控制root `2−|H|/n`、gates1、selected private `2−quality`、其它private1、resources≤1；重新attaining state不会改变bundle资源身份，所有未选states任务仍执行。β0有完整峰2基线。任意C<2逆向时connector固定原gate；gate两unit不能同住，selector必到本组state；每resource只收unit，C<2使跨选中states导出资源不交。额外未选state导出只忽略、不复用。C≥2不偷用独占。pin使OPT≥1，值恒等覆盖n1、β0/1和C边界。

### §3 一般福利LP、claims与bit复杂度

LP总可行、紧有界且W*≤L≤n；没有unit-FSLP假设。x是原resource claim概率，z是state概率，p*x是目标贡献，三者没有混用。z0迫x0，不作0/0。组内共state相关不影响逐resource跨组乘积；条件化后sumQ可>1，但正文明确仅初始使用≤1的弦界，此点已正确保留。

所有CDF阈值来自原p；state候选≤S、selected coin≤I_+、level总数≤I_+。每次从原z/x/ratio重新算有理表达式，公共分母多项式次幂界有效；没有极小概率倒数、全子集或数值分母循环。标准rational LP可输出多项式位长BFS，和有限浮点候选经Fraction对偶认证的证据区分正确。精确随机分布只作分析，实际去随机化不比较e。

### §4 balanced与13/8

对任意实际r，h=#{r>b}若h/n>b会使k=h候选>b，所以h≤bn；W≤n(2b−b²)含非整阈值和w0/1。最优balanced见证可对未选组补空bundle，得W*≥nβ*²，未删除任何物理job。D=(18−13β)/8≥5/8，二次式在[0,1]导数≤−50，最小1/64；平方比较符号正确，sqrt仅用于证明。全算法不输入OPT或β*。三步不是各机器独立可行，而通过同一全局bundle共同回填；正文实际包含完整原任务桥依赖。

### §5 parameter equality与source量词

eq(11)的≥/<互补和另版>/≤均正确。unit-FSLP⇒L=n、W>5n/8与高组fraction f(delta)严格下界对两种高端语义分别成立；delta0/≥NO空类明示。

近完美部分（本人作者自查，不计独立票）与本人另冻Exact一致：YES目标下界(1−eta)n；NO真实福利≤[gamma+(1−gamma)delta]n；LP接受时输出严格大于5L/8，故eq(13)等号也矛盾。正文用NO弱上界是安全的，未免费使用本人证明中更强严格上界。gamma≤delta≤3/8、eta≤1/40给两侧39/64，三重等号覆盖；输入参数二进制与非整count无数值展开。没有将一般LP的‘总可行’误作unit-FSLP infeasible判据。

### §6 来源与不可外推

DNS §3.2 Theorem3.2/Lemma3.3机制与finite-n更强因子的归属准确；本人实际下载原作者PDF，并渲染看过PDF1/5/8/9，记录在本目录DNS来源页。未把该福利机制、1−1/e或条件期望认作新原创。本文仍未认证门控后果的全球新颖性。

flat两组共一unit资源OPT2、gate OPT3/2负控正确。整个gated类ratio只限制该image内实际YES/NO gap；复杂度后果均条件化，未把固定rho反证夸成排所有epsilon。共享内部机器、多层coherence、非norm1/隐式states、不同原资格、非all-allocation partial NO均明确域外。主UM正反面保留OPEN。

## 3. 旧NSW现行C–F的纠错攻击

原C–D低质量fraction定理和F.1本身没有被高低比例纠错推翻。本次不重新认证其依赖A/B长算法，只审所读C–F的参数翻译及其连接新正文。

新F明确区分gamma_hi与gamma_lo=1−gamma_hi。若h_≥delta<gamma_hi*n，则low_<delta>(1−gamma_hi)n。C.4给low_<q_eta<eta*n；当delta≤q_eta、gamma_hi≤1−eta时，C输出有high_≥delta>(1−eta)n≥gamma_hi*n，矛盾；双等号安全。高端改>delta时不能免费沿用delta=q_eta边界，正文已明确要求按C.4相应条款重核。链接到新gated §5现行文件存在，且没有把新gated算法变成原flat全组minimum-quality finder。

旧规范原字节2365f5…已另存，未倒改旧Proof/Exact/审查。新header与F均明确‘旧PASS没抓出’，不虚构历史审查已发现此错误；这一事实必须在旧review追加勘误中同样清楚。

## 4. 旧review现行文本需要明确撤回的scope

本次实际读到旧review仍保留：

`根本范围：C–D禁区 delta_q<=c_eta<eta<gamma，而条件需求树源解码在直接阈值delta_q处通常需要gamma<=delta_q；本页不覆盖后者。`

该段正是已被证伪的scope解释，**不能继续作为现行review结论承重**。旧review开头的‘当前正文SHA2365f5…’目前也只对应历史原稿，现行正文已是214eb4…。建议不改冻结source review原件，在该现行导航review头部/末尾追加明确有日期勘误：撤回上述‘不覆盖’判断，指出不同gamma被混用，原C–D/F.1保留；列新旧正文hash与原稿保真路径；注明旧PASS未发现、现今新独立攻击才纠正。不能只更新链接却继续保留未标撤回的旧scope。

此问题是审查状态/历史归属修正，不是新规范正文的数学fatal。root本轮可在建立新review时同步加这段勘误；若未加，不应声称旧review已经准确反映本轮纠错。

## 5. 未取得的证据

本人未读/跑当前canonical所链新audit代码/JSON，故有限Fraction36/72/3/12、20枚非平凡coins等不能记为本人独立实现核验。新review尚未存在，本文不预先审它。near-perfect子结论本人是作者，独立状态由另一审者另给。A/B长NSW不在本次重审范围。无外审/新颖性认证、无主目标完成。
