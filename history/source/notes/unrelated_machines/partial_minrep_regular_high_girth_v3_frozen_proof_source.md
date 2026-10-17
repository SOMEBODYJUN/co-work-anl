# 正规高围长线性度数源：root证明冻结

对应Exact `0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61`，新身份UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3。root已先将Exact给row及pcsp独立重构，没有给它们本证明。root在提出Exact时已有以下推导，不冒称自身盲审。本稿不提供UM compiler，不认证新颖。

## 1. 固定copy lists的平均覆盖很小

任取全部Nt个copies上的lists，总cost≤gNt。每原vertex v的copy list可完全不同。对每原edge e，令q_e为独立均匀抽其两端各一个copy时lists覆盖π_e的概率。令beta=(Σ_e q_e)/|E_old|。

设H=4g/tau。长度>H的heavy copies数≤gNt/H。在“均匀原edge、两端各独立均匀copy”的试验中，端点边际在Nt个copies均匀，因原图Dregular。因此heavy端点的边概率至多2g/H=tau/2。若beta≥tau，light且covered概率≥tau/2。每原vertex独立均匀选一个copy，再从其非空list均匀选label（空list任取）；每条light-covered边的见证pair被抽中概率≥H^−2。由平均，原某单标签赋值value≥tau/(2H²)=rho³/(32·10^6 g⁸)>gamma，矛盾。故beta<tau。

template每type有z=t/D条边，d个layers均边际均匀copy，所以固定copy lists的输出covered边数Z均值

mu=d z Σ_e q_e=M′ beta<tau M′。

此期望界直接对cheap copy lists成立，未假设各原vertex所有copies同list，也未把随机抽一copy后随机总cost≤gN当成已知。

## 2. 两侧随机permutations的factorial-moment上尾

核心事实：一份uniform [t] permutation在r个不同slots上的images，相对于r份独立uniform [t] samples的点态密度至多

t^r/(t)_r≤e^r，0≤r≤t。

非单射image tuple时前者概率0；单射时概率分别1/(t)_r与1/t^r。最后不等式来自(t)_r≥(t!)^(r/t)≥(t/e)^r：递减ln序列前r项平均≥全t项平均。

任取k条(layer,templateedge)不同的edges。每个原vertex、每个layer只见若干不同slots，其uniform permutation images按上述点态比较；全部涉及slot数恰2k。独立各vertex/layer permutations，因此它们同时被固定lists覆盖的概率≤e^(2k)∏_(edge selected)q_type(edge)。with-replacement参照模型中每edge的两个copy选择与别的edge完全独立，故这里的乘积正确。无需声称真正matching边指示变量负相关。

由factorial moments，

E binom(Z,k)≤e^(2k) (Σ_all_edges q_type)^k/k!=(e²mu)^k/k!。

因此对s≥0有E(1+s)^Z≤exp(e²mu s)。用θ>0、s=e^θ−1作Chernoff，对a=rho M′/2得到

Pr[Z≥a]≤(e³mu/a)^a≤(e³/(50g²))^(rho M′/2)≤exp(−rho M′ ln g)。

最后只需e³<50（如e<3即可）；mu=0时概率0。阈值允许实数。原先“两个fiber permutation会使尾界变成双重指数”的条件MGF捷径不使用；直接joint image点态比较保留了logg。

## 3. 全部copy lists同时NO

cheap lists数K满足K Q^(−gNt)≤(1+1/Q)^(Nt Q)≤e^(Nt)，所以K≤exp(gNt lambda)。又ln g≥ell/2，M′=dNt/2，d≥1000g lambda/(rho ell)，给rho M′ ln g≥250gNt lambda。并界坏概率≤exp(−249gNt lambda)<0.001。

在补集上所有cheap lists均覆盖严格少于rho M′/2。这是修girth前的一次全局同时性；修图每次改两边，任何给定lists的覆盖数变化至多2，故同一确定上界对所有lists同时有效，不再union。

## 4. 短cycle的期望（包含parallel 2cycle）

每layer是perfect matching，所以union图是proper d-edge-colored regular multigraph。固定起始copy vertex和长度l≤G的color序列，若要走成simple cycle，该序列必cyclic nonbacktracking（相邻color不同，包括末/首）。其它序列贡献0。

沿该序列逐步揭所用layer在两端原vertex的fiber permutation及template mate。prefix若是simple路径，最后当前vertex和初始目标vertex在最后color的matching均未被揭过：到当前点的arrival color与last不同，起始first color与last不同，且没有重复copy vertex。任何一个已揭matching edge的两copy端点均在此前已访问vertices中。

揭当前点的fresh slot后，若template mate的原base vertex不是起始点的base vertex，闭合概率0。否则其fresh permutation image在至少t−l个未用copy编号中uniform；初始目标亦未用，闭合概率≤1/(t−G)。这个两端fresh论证不假定新的base edge-type选择uniform，也不默认是原图的D-cover。

共有Nt个起点、至多d^l个color序列，故simple短cycle数X的期望≤Nt S/(t−G)≤2NS，因为t≥2G+1。按起点/方向多计cycle只使上界增大。长度2正是不同matching layers的parallel边，cyclic NB条件仍适用。Markov得Pr[X>B]≤1/20，B=40NS。

## 5. 同type、同layer交换总可选且不生短cycle

在X≤B图上，所有短cycle上vertices至多GB。选bad cycle边e=(u,a)(v,b)。当前maxdegree d，两端G-balls总vertices数≤2Σ_(j0..G)d^j。bucket(originaledge type,layer)始终恰z条matching边。因为bucket本身matching，触及上述禁点的bucket边数≤GB+2Σ_(j0..G)d^j<z。故能找f=(u,c)(v,d)不在任何shortcycle、且两端离e两端>G。四端互异。

去ab、cd，加ad、cb，保持每layer perfect matching、每bucket数目及projection type。若新shortcycle只含一条新边，删它后是旧图跨e/f端点的≤G−1路径，与距离矛盾。若含两新边，删后两old paths的配对若跨e/f端点，同样远距离矛盾；另一个配对为a↔b、c↔d，后者与旧f组成旧长度≤G cycle，与f非bad边矛盾。两条新边不可能自身构成2cycle，四端不同。因此没有新≤G cycle，并至少毁掉选中的旧cycle。循环至多B次，所得girth>G且simple，degree恰d。

每次更改2条约束，任意lists覆盖数至多增加2。t≥8B/(rho m_*)，所以2B/M′≤rho/4。修图前统一cover<rho/2，最终统一cover<3rho/4<rho。

## 6. bounded bits、FAIL与总位复杂度

有2dN份length t的Fisher–Yates permutations，总integer draws≤2dN(t−1)。每draw用固定至多R次ceil(log2 bound)fair bits，单次accept概率>1/2（bound为2幂时为1），耗尽概率≤2^−R。R=ceil log2(2000dN(t−1))给总samplingFAIL≤0.001。条件于全部成功，每draw值uniform且与accept事件独立，因此整个graph是上面独立uniform permutation law。cycleFAIL≤0.05，故全部合法输入FAIL<0.1。NO时再扣pre-soundness坏事件<0.001，总好概率>0.9，蕴含所陈述至少0.8。

Q gamma≥1给10^9g⁸/rho³≤Q，故g数值、1/rho数值及d数值均被显式Q多项式控制（例如(g/rho)^3≤Q/(10^9g^5)≤Q）。G固定时S,U,B,z,t都是N,D,Q及binary参数的多项式；原D≤输入edge数，Q≤显式projection表长度。图、全部permutation bits、枚举长度≤G的simple cycles、逐次BFS找f和至多B次交换均有最坏poly上界。没有把numeric极大g/rho展开而不支付Q的输入长度；G若变参则指数另计。所有参数和ceil可用binary有理运算。

输出每个edge保留原projection type。原perfect赋值复制给每copy，任何随机匹配和交换后均满足全部边。FAIL不是一个假的girth图；源归约caller可在该flag直接接受YES或输出合法empty-job UM实例，所以YES每seed完备、NO错误仅概率代价，复杂度假设仍是NP不包含BPP。

本稿没有读新审查者推导。标准PCP起点、Qpoly_rho(g)和固定参数归约只在完整source corollary处另用；主构造/概率证本身自足。尚无一般UM费用/π解码器。
