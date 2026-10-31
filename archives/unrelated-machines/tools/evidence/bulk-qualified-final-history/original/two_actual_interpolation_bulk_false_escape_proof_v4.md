# 一般两actual见证插值与bulk全False逃逸：作者Proof v4

对应Exact：`/workspace/scratch/038d9dcc4cac/two_actual_interpolation_bulk_false_escape_statement_only_v4.md`，SHA256 `fb086626633dcdd8d56115dde34af96f6031873775da36b205bc274d9456420e`，ID `UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4`。

作者typed_edge_gap，2026-10-18。仅scratch，不改旧raw/repo/Work/Git。Proof在root告知rank已冻结Exact-only独立记录后才写；作者未读取rank记录。root的先行独立重构与fee随后共同核验不是本Proof冒充blind来源的依据；Exact已明确共同研究顺序。此为标准半整数排序槽/配对舍入的精确后果，不宣称原创舍入定理或新的普通UM近似算法。

## 1. 一般逐机插值：全部原jobs的一次整数flow

采用Exact §0的一般P、T、两完整actual σ^0,σ^1、distinguished原jobs F及指定legal原目的地ν。把F从两witness中暂时移除，仅分析原jobs Z\F；最后必须按ν全部加回。

对每个非F原job z，保留两份标记不同的actual occurrences (0,z),(1,z)，其原machine与真实时间分别为σ^0(z),p_(σ^0(z),z)和σ^1(z),p_(σ^1(z),z)。即使两目的地相同也保留两份；这不复制输出job，只在内部构造中标记两条候选。

每原machine i将其N_i份occurrences按本机真实时间降序排为

  p_1≥p_2≥⋯≥p_(N_i)≥0，

并依序分成pairs (1,2),(3,4),…，最后奇数份允许单独一pair。对每pair建一个内部容量1节点。pair不是实际新machine，不输出原job到虚拟执行端。

构造二分flow：source到每原job z∈Z\F容量1；job到它的两occurrences所属pair节点连边；pair到sink容量1。若两occurrences落在同pair，可合并该job-pair边，但保留它能支持总流1的容量。每份occurrence给其job-pair边1/2 flow，故每job输出恰1、每pair接收至多1；得到value |Z\F|的fractional flow。容量均整数，因此存在同value的integral flow，可由确定性多项式整数maxflow求出。

每个非F原job恰匹配一个pair，在该pair所属的真实原machine执行。job-pair边本来来自它自己的一份actual occurrence，故目的地恰为σ^0(z)或σ^1(z)，原finite资格及真实时间均未改变。同一个job两次同机不会多执行：job节点总容量一直是1。F则全部在各自ν(z)执行。

由每pair至多一个原job，每machine i的非F原job件数≤ceil(N_i/2)，证(G1)与件数界。

## 2. 一般精确逐机负载界

对machine i，若N_i=0，则非F负载、L_i^0、L_i^1、d_i均0。否则按上一节排序，并令末尾缺失的偶数项为0。匹配到第h个pair的原job真实处理时间≤p_(2h−1)，所以同一份integral flow的实际非F负载满足

  R_i≤Σ_h p_(2h−1)。

又有

  Σ_h p_(2h−1)
    = (Σ_j p_j)/2 + (p_1−p_2+p_3−p_4+⋯)/2
    ≤ (Σ_j p_j+p_1)/2。

最后一步用降序非负性：交错和≤p_1；可将p_1以外写成−(p_2−p_3)−(p_4−p_5)−⋯，偶数末项也为非正贡献。Σ_j p_j按actual occurrence精确等于L_i^0+L_i^1，p_1=d_i。因此

  R_i≤(L_i^0+L_i^1+d_i)/2。

把F按ν加回，完整actual load为t_i+R_i，得到Exact(G2)。每machine的pairs来自同一次全局整数flow，所以全部逐机界同时成立，没有逐机各选一份不同输出。

两输入actual峰≤T，因此每个used非F端p≤T，L_i^b≤T，0≤d_i≤T。于是t_i=0给load_i≤3T/2；若t_i=T且一输入F本机负载T，该输入非F负载必0，得load_i≤3T/2+d_i/2。若两输入F本机负载都T，非F输入只能用本机zero端，L_i^0=L_i^1=d_i=0，输出load_i=t_i。unused finite>T不在occurrences中，不影响任何bound。

T=0时所有used端均0，上述排序、flow、计数与逐机界仍逐字成立。F或非F为空同样成立；ν可为不同于旧supports的legal原端，其真实总load始终是明算的t_i，未假设其≤T。

## 3. 完整backbone特化：J不接任何pool

以下归一化T=1，按Exact §1–3的全部原backbone和任意J非pool资格。F取全部原f_a，ν固定每f_a在A_(a,0):1。对所有非F原q/b/J一起运行同一flow；不单独先选J，也不假设C/M仍恰一任务。

每个非pool原machine（I、全部M/C）没有任何f资格，故t_i=0，直接由一般界得实际load≤3/2。J可在ring或正/负C，以任意真实异权时间共居；包括zero、多枚tiny、以及unused finite>1。只要它在输入strict中实际使用，该端就自动≤1；因此没有额外size假设。

pool在本节只允许对应q及f。strict witness中若f_a在某pool，其unit1已占满，任何同pool q的1/k>0都不可能执行。free pool至多k件对应q。统计两份非F actual occurrences：

- 对a=u或v的正pool，一份输入free、另一份输入有unit f，所以N_i≤k。
- 对其余a的正pool，两份输入都有unit f，所以N_i=0。
- 对a=u或v的负pool，同样只有一份输入free，所以N_i≤k。
- 对其余a的负pool，两份输入都free，所以N_i≤2k。

k为偶数，件数界ceil(N_i/2)分别≤k/2、0、k/2、k。每输出q的真实pool时间均1/k，故u,v正pool在新unit f外至多负荷1/2，峰≤3/2；其它正pool仅f、峰1。u,v负pool至多1/2，其它负pool至多1。所有原f均已加回且只执行一次，所有非F q/b/J已由同一flow一次分配，因此完整全False实际峰≤3/2。

此论证明确不需旧v3的K_a、C上J单件性、负C恰b或M恰q/b。输出在非pool出现的合法实际cohabitation全部计入3/2，不能为了旧强输出合同而错误排除它们。

## 4. 任意J pool资格与准确d

现在允许J接任意pool，但F仍为全部f，ν仍固定到正pool。对其它原jobs一起用同一一般算法。

对非pool机器仍有3/2。pool逐类读取两actual中已用非F原端：

1. a=u或v的正pool：一份输入有unit f，故该输入非F实际load=0（仍可执行zero J）；另一份输入非F实际load≤1。因此L_i^0+L_i^1≤1。按Exact定义该machine d_i≤全局d≤1，添加新unit f后的峰≤1+(1+d_i)/2≤3/2+d/2。
2. 其余正pool：两份输入都有unit f，所以L_i^0=L_i^1=0，所有该处used非F端若存在都为zero，故d_i=0。新unit f加回后实际load恰1；输出可以带任意数量合法zero J，不省略这些原jobs。
3. a=u或v的负pool：一份输入有unit f，另一份free，故L_i^0+L_i^1≤1且d_i≤1；输出不再放任何f，所以负荷≤1。
4. 其余负pool：两份输入free，L_i^0+L_i^1≤2且d_i≤1，输出没有f，负荷≤3/2。

所有类别同时属于同一份完整flow输出，得到Cmax≤3/2+d/2。这里d只由两actual已用的非F原pool端定义；unused大处理时间绝不需要，也不能被拿来满足必要性。若同job在两actual于同pool执行且p>0，该pool不可能在其中一份已含unit f，故在两新增正pool的正d事实上伴随实际job目的地改变。

## 5. 弱阈值、等号与真正大pool原job必要性

给β=2−δ>3/2，即0<δ<1/2。代入完整实际上界：

- d≤1−2δ ⇒ Cmax≤β；
- d<1−2δ ⇒ Cmax<β。

所以若某候选仅禁止allFalse的C<β actual，能推出的必要条件是d≥1−2δ，不能在等号时误写为严格大于；若候选禁止allFalse的C≤β actual，才推出d>1−2δ。

在1/k<1−2δ时，q的所有pool端1/k都严格小于该阈值。因此任何满足d≥1−2δ的大d必须来自一枚实际J原job z，在u或v的正pool于其中一份strict witness实际执行，且本机处理时间至少1−2δ。另一份witness该pool已有unit f；因为此p>0，该同一z必须真正离开，不能是相同静态owner或unused有限资格。若J不接pool，上一节的更强3/2直接排除β>3/2的allFalse forbidden合同，不依赖d这个较松式子。

该必要性不构造可复用OR-commit，不把单个pool overspill当hardness；其作用仅是准确关闭非pool/tiny-C/negative-C/ring路线，指出后续源必须落实的原任务身份与真实pool端。

## 6. 全部对象与位复杂度

一般算法有2|Z\F|份occurrences、至多同阶pair节点、每原job两条occurrence支持（可重合），flow规模显式多项式。排序只比较输入binary rationals，计算L/t/d、核原资格与完整σ也只需有理数加法比较；中间分子分母位长按输入总位长多项式增长。flow容量整数，求一次整数maxflow即可，单位value≤|Z\F|。算法不按1/tiny、1/T、ρ精度或分母数值循环。输出逐原job一个真实原machine，内部pairs不成为执行资源。

backbone对象数完全沿Exact：m=r(4k+2)+|I|，n=r(4k+1)+|J|，finite数r(10k+2)+E_J。没有删除zero job、增加免费约束、隐藏aux或预载。两actual witnesses未知时，本Proof只给存在性，不给它们的免费计算。

本Proof不证明普通UM ratio-hardness，不构造源NO，不认证全球新颖，不声称运行审计/枚举。最终可合并旧bulk页的一个一般插值Claim，不拆成新的重复数学树。
