# 双small包的完整数学比较与关系审读

本次范围是任务 unrelated-machines-3a-3a-3f8b771c0276b1b2 的10核心、7只读对象，使用当前registration pins。按问题依次实读：双small/ST/3DM；raw SH3；稀疏与紧凑配置；复制；18机/14机K2和S3；完整门控与robust；固定边际NC。77个声明refs去重为56文件、57连续区间，全部已读；逐文件SHA、精确行范围及完整/section边界见同目录reading-manifest.json。JSON独立NC审计以无删字段的紧凑JSON实读，未把既有50559原子输出说成本轮重新生成。未运行旧数学审计程序，未读未列出的经典PDF或外围链接；成熟中文正文自足论证与必要声明evidence已逐一核对。

以上及第11节是前序worker留下的已完成阅读记录。2026-11-12恢复接续复用这些成果，独立复核ST完成时间费用桥、复制界和9边作用范围；实际新增阅读及校验见同目录recovery-review.md，不将既有56文件记录重复宣称为恢复worker的新增实读。

## 1. ALL的双small全目标

令ST表示逐机L_i≤ell_i+r_i的费用保持有序槽定理，Karp表示显式带坐标标签perfect3DM的NP完全性。这两个是完整锐界的联合外部前提：ST负责大OPT分支，Karp负责复杂性起点；本节补付结构类内部全部流和实际assignment解码，不能把其中任一前提单独写成整个目标成立。

输入是共同二进制有理b>0、全部finite p≤b、每行不同原job的正small资格至多两条。先把每个有zero端的job安置到其真实zero端，删除正子问题并最终回填，OPT不变。对T<b，只保p≤T的small。每行两项和≤T时容量2，否则容量1；二部整数满流等价于实际C≤T。OPT<b的最重行是零、单项或两项和，只有O(m)候选，因此得到精确解，不以数值T迭代。

对b≤T<2b，写a=T−b、c=b/2+a、D=b+c。若行small总和A_i≤c，unit门容量1，small自由；输出负载≤b+A_i≤D。若A_i>c，机器总件数容量2，unit和p>c的small共享容量1的big门，其余为light。真实T调度不可能在hard行接三件，因为一unit加两small的负载b+A_i>b+a=T；也不可能接两big：两个unit超T，unit+heavy超T，两heavy>2c=b+2a≥T。因此每个真实T调度嵌入整数满流。任意满流的hard行至多两件且至少一件light，故负载≤b+c=D≤3T/2。FAIL只推出OPT>T，成功不判定OPT≤T。最优峰在此区间时，是同机0/1枚unit加至多两small之和；枚举O(m)候选至T=OPT必成功。

普通assignment-load LP的最优L≤OPT。ST在支撑最大件≤b时给完整实际调度C≤L+b；OPT≥2b时≤3OPT/2。并行取得三类候选输出，以原矩阵实际负载选最小者，无需知道OPT所在区间。所有候选为固定项数有理和；整数流/匹配、标准精确有理LP、排序均按显式输入总位长多项式。空残余直接给zero调度，松b也无问题。

困难性用Karp的三份等大坐标X,Y,Z各q>0。每triple e=(x,y,z)建M_e，X_x、Y_y在该机各1/2；J_e仅可在M_e或Z_z机用1。Z机器没有small，所有行small资格数至多2。perfect matching选中的q个M接两small，其J到互异Z；其它J留原M，完整C≤1。若任意完整assignment C<3/2，Z机器最多容纳q个J；只有这些至多q个opened M能接small。2q件X/Y迫恰q个opened M各接两small，并且其J占互异Z，解码perfect3DM。无incident元素的NO源可送一机两unit的合法常量NO；空q源先单列YES。NO实际OPT≥3/2。固定rho<3/2保证将给YES输出<3/2，故可判perfect3DM，除非P=NP。这里结论是证明“P≠NP时无该rho”；没有把P≠NP当成已证事实。全目标只在common-b双small域，不成为一般UM算法或近二困难性。

## 2. ST转移到共享复制的更强完整界

固定原实例，F是**不作额外端点剪枝**的普通assignment-LP最优峰，O_k是每原job复制k份、共享原机器后的整数最优。复制解中每job在各机的份数除k给原LP点，故kF≤O_k。反向取最优有理x，对每个带身份的复制job j,t给同一分数x_ij。其行负载为k ell_i≤kF，最大支撑处理时间r_i不随复制增长。ST（费用取0）输出全部nk件实际分配，故

O_k≤kF+p_max≤kF+S，p_max=max有限p_ij，S=max_i sum有限j p_ij。

于是F≤O_k/k≤F+p_max/k，极限为F，完整推出原对象的较松S界。空任务或全零实例直接取0；若F=0则每job可选zero支撑，仍成立。时间复杂度按显式nk输出计，不把二进制k展开误称按log k多项式。此处桥是把原点复制到带身份jobs，并非把CONFIG证书或某个剪枝LP当F。

## 3. 完整CONFIG pin到确定count pin

两对象用同一精确紧凑族：k≥2、N=2k²、G=N−2k，X在自身V/全G为unit，Z在V为1/k、在本块k+1个R为unit，Y在R为unit、在共享z为1/k。

MACHINE-CONFIG-PROBE对象给每(v,C)各自一个完整CONFIG(1)点y，固定v行C概率1。投影x满足每job列和1，且每行sum_j x_ij≤c_i，其中V,z的c=k、G,R的c=1，因为每个真实配置的件数不超过这些整数。固定C中jobs在v为1且其它端为0；其它jobs在v为0。删除v与C中的jobs后，x是其它机器整数容量c_i的分数b-matching。二部b-matching整数性给其全部剩余原jobs一个实际count合法分配，再放回C。因此从完整分数CONFIG延伸得到的是**真实计数assignment**，没有把其它行负载也误称≤1。C=empty还给每机的避机count assignment；任意有限边的singleton是合法C，故所有逐边count查询通过。

source对象另已给同一族完整CONFIG(1)、各pair自己的GPC2及OPT=2−1/k。OPT直接计数也可核：低于theta时至少2k个X留V，各须外放至少两个Z；k+1个R unit槽迫每活跃块至少一Y去z，z≥2矛盾。每活跃块只外放一Z、余Y填R，选择2k活跃块即可达到theta。每job资格数X为G+1≥5、Y/Z为k+2≥4，单/双域闭包无初始点；每资格行删去一最小项仍超1（V为2−1/k，G为N−1，R为2k−1，z为N−1/k），所以所引极小星规则也无起点。由此完整得到COMPACT-COUNT对象的全部合同，不需要假设不同pin的y相容，也不声称每个y同时具有所有GPC2耦合。

共同base的更强要求确会切掉本族：固定V_a={X_a}时本块2k单位需求面对k+1个R，Y去z总边际≥k−1。若条件点来自同一base且逃逸坐标满足条件混合，base的本块Y逃逸≥(k−1)a_a。全局X容量给sum a_a≥2k，z负载≥2(k−1)>1。这是具体的一阶条件混合缺口，非需要重新寻找的身份问题。

## 4. ST机制转移到共同平均与峰值

目标为无释放、无权完成时间；不能把线性分配费用直接当完成时间，也不能把两个独立最优调度当共同见证。给同一真实调度可同时达到(M,T)，建立位置LP z_isj：每job和1、每机每倒数位置s质量≤1、每机处理总量≤T、删除p_ij>T，且sum s p_ij z_isj≤nM。共同见证给LP可行性，n个位置/机足够，精确有理输入下规模多项式。

令x_ij=sum_s z_isj，保持每机所有job分数。把它按p非增依次填倒数位置1,2,…的单位槽。任何较大p落在较大s、较小p落在较小s时交换等量质量不增sum sp；空缺向较小s压紧也不增。故新分数槽匹配费用≤nM。对同一槽图以**槽边费用s p_ij**取最小费用覆盖匹配；二部匹配整数性使费用不增。这里新费用依赖槽，不冒称是原generic c_ij定理字面直接代入；使用的是ST证明中“任意覆盖匹配均有逐机负载界”与独立的最小费用匹配步骤。

ST的前一完整槽收费证明与所选边费用无关，故该匹配同时有L_i≤ell_i+r_i≤2T。实际按匹配槽s由大到小执行；实际倒数位置是已用槽的压紧秩，≤原s，因此完成时间总和≤匹配sum sp≤nM。全部原jobs只执行一次，zero、空槽和空任务保持。于是得到整个共同(M,2T)定理。特别取M*与达到M*的调度中最小T_M*，只得到(M*,2T_M*)，未得到(M*,2T*)。论文附注报告的Rote/Hurkens反面没有可核矩阵，本批不造精确反例节点。

## 5. 固定边际NC的局部贡献

固定真实OPT凸包点x：宏B均匀在r≥k个homes，第i组k件small在H_i/Z_i时间1/k，每件sink边际1/r。若B在h，D_i是送sink数，则逐态C=2−D_h/k，其它行≤1。这与保单个分数点的行包络、固定边际随机law、允许重选x三种输出量词分别比较。

对每组所有2≤|S|≤d的正sink事件上NC，令t=min(d,q)。成功C≤2−q/k迫sum_i binom(D_i,s)≥binom(q,s)，其期望≤binom(k,s)/r^(s−1)，故p≤A_s。相邻比A_(s+1)/A_s=(k−s)/(r(q−s))≤1，于是t=1时p*=1，否则p*=min(1,A_t)。

达到law明确为：均匀选B的home h。q-type概率p*，在h均匀选q件，并在其它r−1组中均匀选k−q个**不同组**、每组选一均匀small；1-type概率1−p*，在h均匀选1件并在其它均匀k−1个不同组各选1件。r≥k、1≤q≤k使所有选择合法，q=k时空选择有唯一可能；q=1两模式相同。每态恰k件外送，整个law在组和组内标签置换下对称，故每small sink边际=1/r，B边际=1/r。固定组s-subset事件概率(p*/r) binom(q,s)/binom(k,s)（s≥2，s>q时0），满足全部所需阶。q=1或d=1时成功为1，不套虚假的一阶公式。

两两NC期望再由D_h≤1+sum_i binom(D_i,2)得到E C≥2−1/k−(k−1)/(2r)。r≥max(k,binom(k,2))时取q=2、p=binom(k,2)/r，以上law每态D_h为1或2，所有pair事件恰1/r²，期望等号成立。这是从同一阶乘矩机制导出的期望sharpness，并未声称q>2的尾sharp law也同时使期望sharp。

增长阶d=k、r=k²、q=ceil(epsilon k)给p*≤2^k/k^(2epsilon k−2)，显式输入长度poly(k)，任意固定多项式采样的union bound趋0。若要1−(1−p*)^B乘积界，必须每个正概率历史后仍保同一x及全部NC；仅无条件逐轮合同只用union bound。固定d不能排所有poly预算。允许重选x、采后重排或集中正相关迁移均域外；本族本就有OPT1。

本关系只支付FROZEN-MARGINAL资源中NC期望、成功率及采样部分；固定常数逐行包络的floor精确值和计数包络不由该关系推出，故使用contribution而非whole_result。原高阶审查短句“其它不同组”在本证明显式展开为k−q组，按其后句每态恰k补全，未修改公共原文或registry；pair资源的等价“先选k活跃组再在其中选B”与此1-type一致。

## 6. 值桥转移到未知OPT全门控算法

源WELFARE对象的**值恒等与完整回填**不需要FSLP：完整P_gate含root pin、connector、selector、所有listed incidence、zero和未选state jobs，OPT=2−beta*。它的unit-FSLP绝对13/8子结论有额外前提。本节只以无条件值桥作为源，补付一般LP与两阶段条件期望，因而可交目标whole_result，而不是把unit-FSLP假设扩到全类。

每组state总质量sum z=1、0≤x≤z、每资源sum x≤1，最大L=sum p x。真实allocation嵌入LP，W*≤L≤n，且总可行。按z选state、按x/z提议incidence，z=0时不除；每资源给最大原系数提议者。正水平a下q_gu(a)=sum_{s:p≥a}x_gsu，各组独立且初始sum_g q≤1，故尾概率1−prod(1−q)≥(1−1/e)sum q。对原正系数的有限levels求和后才得到E福利≥(1−1/e)L≥(5/8)L；L>0时后一号严格。

先逐组固定正概率state，再逐coin固定0/1分支，每次取不低于候选加权平均的精确有理期望。条件化后概率和可能>1，之后只重算sum_levels delta_a[1−prod(1−Q)]，不重用初始弦界。最终真实不交bundle福利W≥(1−1/e)L；每bundle再选attaining state只增值。状态/coin/levels个数均显式多项式；LP有多项式位长最优基本解，每轮从原有理表重算固定次乘积，分母因子数量和指数多项式，不使用浮点提案作通用LP认证。

排序r_(1)≥…≥r_(n)，令b=max_k min(k/n,r_(k))。设h=#{r_g>b}，则h≤nb，否则第h项使min(h/n,r_(h))>b。于是W≤h+(n−h)b≤n(2b−b²)。最优平衡见证覆盖至少n beta*组且各质量≥beta*，所以W*≥n(beta*)²。因此b≥1−sqrt(1−5(beta*)²/8)。回填所有原jobs给C≤2−b≤1+sqrt(1−5(beta*)²/8)。

对beta∈[0,1]，D=(18−13beta)/8≥5/8，且D²−(1−5beta²/8)=(209beta²−468beta+260)/64≥1/64，因为导数418beta−468<0且beta=1取1/64。因此C≤(13/8)(2−beta*)=(13/8)OPT。sqrt只用于分析，实际排序/比较/回填全有理。beta*=0时完整峰2基线足够；所有原jobs回填按值桥执行：pin留根，未选connector留根，未选selector去gate，其余incidence留private。算法不输入OPT、beta*或source YES，也不要求unit-FSLP，不承诺全类绝对C≤13/8。flat不含门控机器，两组单unit共享资源已给flat OPT2/gated OPT3/2，故不是保值normal form。

## 7. 一般福利保证到两阈值robust判别

13/8对象陈述中包含一般福利LP舍入W≥(1−1/e)L>5L/8（L>0），不是仅有最终近似比。保持同一个显式norm1菜单、全局不交bundles。取0≤eta<1、0≤delta<1、0<gamma≤1且(5/8)(1−eta)≥gamma+(1−gamma)delta。

YES中至少(1−eta)n个质量1组嵌入同一福利LP，L≥(1−eta)n。对任一NO allocation，分别令h为#{r≥delta}或#{r>delta}；两版均有W≤delta n+(1−delta)h<[gamma+(1−gamma)delta]n。严格性来自h<gamma n与delta<1，不需组数整除。如果NO也有L≥(1−eta)n>0，源舍入给W>5L/8≥(5/8)(1−eta)n，矛盾。因此单个精确LP阈值判别器在两个promise分别正确；算法不需运行福利finder。统一子域0<gamma≤delta≤3/8、eta≤1/40满足右端≤39/64≤左端，包括三重等号。delta=0的NO_≥为空，eta=1/delta=1域外；不混用严格阈值。没有提供NP难可靠源或编译器，若标准NP完全语言确定性归约到此完整promise才会推出P=NP。

## 8. K2两反例与S3的精确非逻辑比较

14机固定证书只有同机first/pair CONFIG匹配：M0三个membership的L(S P_u P_v)=7/160>0，但合法配置不含该三件（负载2>T=7/4）。所以该点不能升级到完整row law。18机参数族修复此问题：每row至多依赖两位，(00,10,01,11)=(35,21,21,3)/80给完整law；共同M2由七维正pivots或signed-cube Cauchy证明，所有raw-affine localizer成立。然而跨三物理机L(b1 b2 b3)=−1/160，指定A=a、Z=aE的claim×state为−1/160、quality×state为−c/160。14机的负quality是−1/80，并非18机c=3/4的−3/640；机器、任务和参数不可替换。

两者各有完整OPT1调度，反例只否定**给定点、指定direct substitution**，不否另一个canonical点或调度存在。18机全row law并不推导14机固定矩阵结论，也不是退休14机对象；故只交motivates语境边“修复单row欠款后跨row欠款仍在”。

S3桥要求同一L对boxes、物理slack、独立unit-cap1行的至多3个raw-literal lifts，以及规定Boolean/cover等式。其quality恒等式q−a h=(a²−a)+sum p a(D+E−1)恰要third-literal付款；resource恒等式1−sum aE=(1−sum E)+sum(1−a)E需要cap1，不能用T-cap免费替代。上述两K2点已因raw三literal负项违反完整S3；这只说明它们不给桥的前提，不反驳桥。S3本身不要求K2的M2/CONFIG，也不能写成无条件层级包含。任选实际调度可另造S3 Dirac点，不会改变手中另一个K2点。18机到S3只交motivates语境边，coverage仍为isolated-after-review，未伪造refutes边。

## 9. SH3与稀疏review的无逻辑边结论

SH3在native unique-home/unit-head分层DAG、共同degree6/M3、完整row CONFIG first/pair与全局quadratic-load localizer下，从每个正入口推出新的一阶parent-bounded流。quota k_u(2−T)是实数；只有整数网格可用hypersimplex恢复**新流**一阶CONFIG，k=1无衰减另用incoming/home pair zeros。端点first为0可用M3零列迭代删除，但只有mandatory one-hot删空才sound FAIL。包含切delta d1(delta d2−M)≤H的共同terminal容量跨全部W只收费一次，乘delta d2−M前分符号，floor比较用规范的左端/C≥delta²/(8q^(a+b))。旧资料中未归一化1/4句不作本批前提。该系统在包含族固定T<2最终FAIL，不能误称它在近二gap点仍可行。

K2反例只有M2且负三literal，不满足共同M3：若保原degree3负项并满足Boolean degree6，则L((b1b2b3)²)=−1/160违M3。S3桥则是不同完整flat模型的同点表提取，无shared integer forest解码。紧凑族共享z有Nk件home时间1/k，总home工作N，并非SH3的每行home总工作1，不能免费对该矩阵套SH3定理。故本包未找到从其它已声明端点完整推出SH3目标或其否定的逻辑关系；新流到共享integer owner仍是已明确的数学开放义务，不是身份needs-decision。

稀疏review必须分两族：深树对每e各有完整CONFIG点，OPT/T趋2，缺跨query共同base；fixed-r奇N的K2,2全unit族实际OPT1，保给定跨块二阶的真实matching law却因Var(sum B)=0且均值N/2半整数不可能，其最小最大pair修复1/[4N(N−1)]来自整数方差≥1/4并由邻近两层混合达到。前者的gap不从后者的矩证书取得；后者全unit甚至属于双small域，但求一个实际matching会改变给定二阶，并不与双small算法冲突。完整bag联合分布且separator一致可glue，是比独立query/独立pair强的合同。紧凑probe的forall(i,C)exists y和稀疏forall e exists y在不同矩阵上，不能互相导出族构造或把两个gap相乘。因此本review在本次声明端点内也以isolated-after-review交付，具体比较与缺口已付清。

## 10. follow-up与有限证据的处置

任务当前没有overlap_comparisons/follow-up对象对；77声明refs全部完成，25个deferred_candidate_ids只是未指定的候选池，不冒称已读或自动转成承接义务。本收据的comparison_outcomes逐对给本次实际比较结论；closed_overlaps只用于任务明确声明的follow-up对，故此处为空。没有身份/版本未辨问题；未发布新队列任务，follow_up_tasks为空。共享integer owner、跨query共同相关性、改变extraction或保矩修复、一般UM近似与可靠hardness源仍分别开放，但本包未提出一个尚待分派且精确端点未比较的新follow-up。

所有accepted逻辑边都保完整ALL前提；whole_result仅用于本页已补付完整目标的六条关系，NC资源只用contribution。两条K2语境边不计逻辑linked。程序检查仅校SHA、schema、绑定、receipt覆盖，不能替代上面的数学判断。

## 11. 实读文件范围

以下行号是当前整文件的闭区间，仅用于精确报告本轮实际读取，不替代正式引用的全文SHA/唯一标题。全文包含frontmatter；section按原ATX标题截到下一同级/更高级标题前。

| 文件 | 已读行 | 总行数 |
|---|---|---:|
| `archives/unrelated-machines/state/审查/双小资格三半锐界三源精读--审查.md` | 1–73 | 73 |
| `archives/unrelated-machines/state/审查/共同匹配联合槽舍入与包络配置三源审查--审查.md` | 54–65 | 90 |
| `archives/unrelated-machines/state/文献/Karp归约框架与完全问题--文献.md` | 1–326 | 326 |
| `archives/unrelated-machines/state/审查/双small资格root证明读后适用边界增量--审查.md` | 1–44 | 44 |
| `archives/unrelated-machines/state/审查/双小资格三半独立共享重构--审查.md` | 1–59 | 59 |
| `archives/unrelated-machines/state/资源/固定边际宏位置与正支撑释放的精确前沿--资源.md` | 13–24 | 67 |
| `archives/unrelated-machines/state/资料/rawSH3根条件流与实数配额边界--资料.md` | 1–85 | 85 |
| `archives/unrelated-machines/state/资料/rawSH3真困难性流与容量切最终边界--资料.md` | 1–73 | 73 |
| `archives/unrelated-machines/state/审查/原作业SH3子树流与包含容量双源续审查--审查.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/审查/集合包含入口切陈述先行重构与实阈值边界--审查.md` | 1–122 | 122 |
| `archives/unrelated-machines/state/审查/SH3包含切口二项式有限审计--审查.md` | 1–72 | 72 |
| `archives/unrelated-machines/state/资料/rawSH3条件子树流与集合包含切--资料.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/审查/rawSH3作者证明与Exact-first全入口差异--审查.md` | 1–91 | 91 |
| `archives/unrelated-machines/state/审查/稀疏配置与共享容量审计程序补档--审查.md` | 1–68 | 68 |
| `archives/unrelated-machines/state/审查/稀疏配置与强矩匹配双源增量审查--审查.md` | 1–151 | 151 |
| `archives/unrelated-machines/state/审查/全局基数与逐行均匀相关读出边界有限审查--审查.md` | 38–61 | 90 |
| `archives/unrelated-machines/state/资源/紧凑共享逃逸的双路原矩阵与商动态规划--资源.md` | 1–62 | 62 |
| `archives/unrelated-machines/state/审查/紧凑共享逃逸k2原始矩阵增量--审查.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/审查/全局行计数审查的原冻结范围与多行追加证明--审查.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/审查/未归档配置证书批次与量词边界--审查.md` | 1–224 | 224 |
| `archives/unrelated-machines/state/资源/完整单机配置延伸的双装配原入口与有限范围--资源.md` | 1–85 | 85 |
| `archives/unrelated-machines/state/审查/两份复制多数地板与共同激活复制障碍双源审查--审查.md` | 61–75 | 82 |
| `archives/unrelated-machines/state/审查/激活与共享费用源去重补录--审查.md` | 1–16 | 16 |
| `archives/unrelated-machines/state/审查/单层平方根配额与单外层选择器双源审查--审查.md` | 140–153 | 172 |
| `archives/unrelated-machines/state/审查/Sol通用repair-k2全局local-law与canonical-pullback三源审查--审查.md` | 1–140 | 140 |
| `archives/unrelated-machines/state/审查/K2局部行律拉回障碍--审查.md` | 1–79 | 79 |
| `archives/unrelated-machines/state/审查/Raw-K2与SH3条件流两源精读--审查.md` | 19–24 | 43 |
| `archives/unrelated-machines/state/审查/Sol通用repair-k2作者证明read-after增量--审查.md` | 1–85 | 85 |
| `archives/unrelated-machines/state/审查/Raw-K2-S3组合最终两节Sol-NSW实际实读与边界增量--审查.md` | 1–156 | 156 |
| `archives/unrelated-machines/state/审查/identity-coupling-raw-k2-sa3-final-sections--审查.md` | 1–157 | 157 |
| `archives/unrelated-machines/state/资源/归一化配置与原任务矩证书的层次边界--资源.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/资源/广义指派的费用保持与加性负载舍入--资源.md` | 24–68, 98–109 | 133 |
| `archives/unrelated-machines/state/审查/归一化门控菜单v2三源精读与13-8算法版本审查--审查.md` | 1–226 | 226 |
| `archives/unrelated-machines/state/审查/归一化门控菜单福利源判别与比例纠错最终审查--审查.md` | 1–55 | 55 |
| `archives/unrelated-machines/state/审查/归一化门菜单福利与对数调色板padding有限审查--审查.md` | 28–94 | 147 |
| `archives/unrelated-machines/state/计算/门控菜单福利双原程序的证书舍入与冻结输入重放--计算.md` | 1–67 | 67 |
| `archives/unrelated-machines/state/审查/归一化菜单福利与配置证书双源审查--审查.md` | 1–87 | 87 |
| `archives/unrelated-machines/state/审查/归一化门控福利证明与参数互补八源溯源--审查.md` | 1–175 | 175 |
| `archives/unrelated-machines/state/障碍/固定14机原始K2同点canonical拉回失败--障碍.md` | 1–167 | 167 |
| `archives/unrelated-machines/state/审查/门控归一化FSLP四源清洗--审查.md` | 1–169 | 169 |
| `archives/unrelated-machines/state/审查/归一化门菜单福利独立语义证书程序审查--审查.md` | 1–146 | 146 |
| `archives/unrelated-machines/state/资料/不相关并行机文献清单范围与证据层级--资料.md` | 1–44 | 44 |
| `archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md` | 31–49 | 100 |
| `archives/unrelated-machines/state/资源/单边界消元与独立配置探针的恢复合同--资源.md` | 37–46 | 54 |
| `archives/unrelated-machines/state/审查/完整单机配置审查的均匀装配与共同基点范围--审查.md` | 1–79 | 79 |
| `archives/unrelated-machines/state/审查/高阶负相关两状态多数与鲁棒环相位边界有限审查--审查.md` | 25–74 | 108 |
| `archives/unrelated-machines/tools/evidence/higher-nc-duplication-cycle-20261030/private_sink_higher_order_nc_independent_audit.json` | 1–823 | 823 |
| `archives/unrelated-machines/state/审查/私有汇点高阶上负相关精确尾概率最终独立审查--审查.md` | 1–126 | 126 |
| `archives/unrelated-machines/state/审查/高阶NC前缀与对称推送审计补档--审查.md` | 1–55 | 55 |
| `archives/unrelated-machines/state/审查/长链联合投影与最优凸包边际障碍有限审查--审查.md` | 1–151 | 151 |
| `archives/unrelated-machines/state/资源/最优凸包逐行枚举与两两负相关分布双原入口--资源.md` | 1–78 | 78 |
| `archives/unrelated-machines/state/审查/私有组退出与高阶负相关有限审计--审查.md` | 1–155 | 155 |
| `archives/unrelated-machines/state/审查/近完美归一化robust源四源审查--审查.md` | 1–160 | 160 |
| `archives/unrelated-machines/state/引理/显式均匀束robust源的福利排除域--引理.md` | 1–42 | 42 |
| `archives/unrelated-machines/state/资料/rawS3到canonicalSA1同点提取--资料.md` | 1–128 | 128 |
| `archives/unrelated-machines/state/审查/完整原端三次条件的作者合同与拉回证明--审查.md` | 1–156 | 156 |
