# 度数比例复制的任意投影源正规化：root冻结证明

绑定Exact SHA86dcd98daaa2cc479260e444f47f4e9eb3d8ae56936b220f0a1d18e82863d693，ID UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5。root先交Exact给两位v3审查者再冻结本证明，未读它们本次新推导；root自己不是盲审。本稿沿用已证v3的概率/repair机制，新增度数比例质量归一化，不声称全球新颖。

修正记录：v4 Exact未显式排除空字母表，row审查指出val可未定义；v5明确两域非空。本证明的逐点随机取typed标签始终依赖非空，现按v5精确域冻结。v4原证明字节保持，不倒改审查顺序。

## 1. 复制质量和模板

孤点删去不改边值，原perfect赋值在孤点可任取，非空保证两侧非空。令d_v=deg(v)≥1。每侧slot/copy总数均zM₀，因此N′=2zM₀。每层每原edge恰有z条模板边，模板是全部slots上的perfect matching；对每v使用其独立uniform[t_v]重命名后仍为perfect matching。并d层故每copy恰degree d、M′=dN′/2=dzM₀，每(type,layer)bucket仍z条matching边。左右原字母表可不同，所有边保持π_e的原类型；原exact-k-to1等逐表性质原样保留。

## 2. 任意cheap copylists的原边平均覆盖

固定ψ在N′ copies上cost≤gN′，不用原顶点的任何weighted/unweighted成本前提。对原edge e=(u,v)，令p_e为两端各独立均匀选一copy、其lists覆盖π_e的概率。随机均匀原边再随机选其某一侧端点copy，其该侧copy的边际为

deg(v)/M₀ · 1/t_v = 1/(M₀z)=2/N′。

这是新构造相对v3的承重归一化：对左右两端合计，任一copy的heavy命中权相同，不因原图不正规失控。取H=4g/τ，heavy copy长度>H，总数≤gN′/H。因此随机原边两端选到heavy的概率至多2·g/H=τ/2。每原v独立均匀抽一copy，再从其非空list均匀取真实typed标签，空list任取；这是原game的一个随机单标签赋值，期望value≤γ。两端light且lists覆盖的概率至多γH²（兼容pair至少一对，被抽中概率≥H^−2）。故

β=(Σ_e p_e)/M₀ ≤2g/H+γH²=τ/2+16τ/1000<τ。

每原type在d层有dz条边，固定ψ初始covered数Z均值μ=dzΣ_e p_e=βM′<τM′。没有把copylists合并成原廉价lists，也没有假定随机抽代表的原总cost≤gN₀。

## 3. 不同大小permutations的同一稀少上尾

对任何size t_v permutation在r个distinct slots上的images，真实分布相对r个独立uniform[t_v]值的点态密度≤t_v^r/(t_v)_r≤e^r。原因与v3相同：(t_v)_r≥(t_v!)^(r/t_v)≥(t_v/e)^r，非injectivetuple真实概率0。各selected template edges使用的(permutation,slot)互异，总数恰2k；即使各fiber不同大，乘积密度仍≤e^(2k)。参照模型各edge的两个copy样本独立，边间也独立。于是

E binom(Z,k)≤(e²μ)^k/k!，E(1+s)^Z≤exp(e²μs)，s≥0。

取a=ρM′/2给Chernoff

Pr[Z≥a]≤(e³μ/a)^a≤(e³/(50g²))^(ρM′/2)<exp(−ρM′ln g)。

μ0时概率0，a允许实数。列表数按各typed域分别生成函数：Σ_v |Σ_v|≤QN′，x1/Q，K Q^(−gN′)≤(1+1/Q)^(QN′)≤e^N′，故K≤exp(gN′λ)。因d≥1000gλ/(ρℓ)、ln g≥ℓ/2，有ρM′ln g≥250gN′λ。全cheaplists同时越界概率<exp(−249gN′λ)<.001。修图后选lists也被该统一事件覆盖。

## 4. 不同大小fiber的短cycle期望

每layer为matching。实际simple cycle（含parallel2cycle）相邻layers不同且末首不同。固定起始copy x属于原v，及长度j≤G的layer序列，沿walk逐步揭fiberpermutation与模板mate；若prefix不simple，该cycle事件不发生。末步当前copy在该layer fresh，因arrivalcolor不同且未重复；起始copy在末layer也fresh，因firstcolor不同且未重访。已揭的template slots对matchingmate封闭，故当前freshslot的模板mate亦fresh。

如果mate属于原vertex不是v则闭合概率0；若属于v，其image在v的至少t_v−G个unused copies中均匀，故闭合概率≤1/(t_v−G)。闭合到x的概率上界只用起始fiber尺寸；无需所有fiber相同，也无需原type均匀。

把起始点按原v分组而非用最小fiber粗乘N′，有

E X≤Σ_v [t_v/(t_v−G)]·Σ_{j=2}^G d^j ≤2N₀S，

因为每t_v≥z≥2G+1。root/colorwalk多计cycle只增上界，parallel2cycle的相邻layer不同也满足。Markov Pr[X>B₀]≤1/20。

## 5. repair、概率和硬位数

X≤B₀时所有短cyclevertices至多GB₀。maxdegree d，两端G-balls至多2Σ_{j=0}^G d^j。任一(type,layer)bucket是z条matching边，触及这些禁点的bucket边至多GB₀+2Σd^j<z。因此总可选f不在任何短cycle且其两端远离e两端。四端不同，新边若造parallel则原cross距离1矛盾。单新边短cycle给旧短crosspath；双新边短cycle删两新边后旧paths或跨e/f（远距矛盾），或分别连接e两端和f两端，后者与旧f构成短cycle（f干净矛盾）。故不生新短cycle，所选旧cycle被破坏，≤B₀次终止。保same-type/layer保证所有度、bucket、投影表不变。

每次更换两边，任意ψ的covered增加≤2，所有ψ同时成立。M′=zm*≥8B₀/ρ，所以修复后全部cheaplists覆盖<ρM′/2+2B₀≤3ρM′/4<ρM′。

实际integer draws恰K₀=dΣ_v(t_v−1)>0。每draw最多R拒绝轮、每轮accept概率>1/2，any耗尽union≤K₀2^−R≤1/2000。各range预定、bitblocks独立，条件全成功仍是所需独立uniformpermutations。故所有输入FAIL≤.0505<.1；NO好概率至少1−.0505−.001>.9，强于.8。

## 6. 位复杂度与typed source corollary

Qγ≥1给10⁹g⁸/ρ³≤Q，故numericg、1/ρ、d都受显式Q固定多项式控制。孤点删去后N₀≤2M₀，原每degree≤M₀。固定G下S,B₀,U,z和每t_v≤M₀z、N′=2M₀z均总位poly；所有字母表与π表明确显式，Q由输入支付。Fisher–Yates draw数/每轮bits/R皆有poly硬界；枚举cycles按显式顶点+edge-identities的O((N′+M′)^G)、BFS、扫描bucket及≤B₀次switch仍poly。原maxdegree可以随输入长增长，未枚举任何source local菜单或UM树。

perfect赋值逐v复制保持全边，即使FAIL caller可按YES。对固定g,ρ,G，perfect-complete fixed-error常数字母表PCP误差≤γ，其字母表Q和d全为固定常数；不要求原degree固定或两侧等大。若需Qγ≥1，同步clonelabels(α,s)→(π_eα,s)，s∈[k]：新任何满足边丢tag后也满足旧边，故valnew≤valold；旧赋值固定tag给反向≥，所以value恰相等。每右(β,s)仍恰原k_fiber个preimages，equalfibers不变。所需tag数固定（参数已固定），源归约仍poly。

对新ECCC exact4-to1 Paper Fact，此为正规化的条件应用；本稿不代替新paper完整审查。接任意正确确定性promise判别器，YES全seed（FAIL直接YES）、NO以≥.8概率落真NO，得到SAT单侧错误随机poly判别，从而NP⊆BPP。没有将随机归约称仅P≠NP下确定性hard，也没有UMcompiler。若原Qpoly_ρ(g)，d=O_ρ(g)，一般constant-errorPCP不自动给此定量alphabet界。
