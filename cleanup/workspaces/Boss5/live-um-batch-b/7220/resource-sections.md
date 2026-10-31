## R-34290：共同激活、复制边界与KDM全层义务

该工作区README（源 `9a5059291fcef595ebeb`）与JSON（`ba6c97e6c24d76e1afa7`）分别为1302B/20行、149B/6行，均在legacy-cleanup `68fad804ec5946cb296f77dc5b336308a66abf12` 与main `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 有冻结定位；双定位不是独立审查。四字段是schema整数1、save=`unrelated-machines`、actor=`R-34290c73313a4c608f2f8dbfc0e8115b`、instance=`5e85fbb0ec52446b95bdf69f133f6ba0`。它们只保来源路由和工作区身份，不是调度输入、当前owner或认证。原字节及指纹见本批manifest。

README把本轮研究定位为UM-TARGET-v1的全输入桥，并列两项规范资产：`multi_activation_cover_and_replication_barriers.md`和`kdm_high_dimensional_quota_obstruction.md`。两者分别回答给定初态/目标的静态共同激活充分条件，以及需求树中完整KDM gap被部分配额层遮蔽的原因；不能合并成已完成的一般正面或反面。UM-TARGET-v1明确仍OPEN。

### 给定sigma/tau的静态cover充分桥

已全文比较[共同激活复制审查](../审查/两份复制多数地板与共同激活复制障碍双源审查--审查.md)、[原始来源记录](../审查/多件共同激活复制原始来源记录--审查.md)及[私有需求/复制障碍](../障碍/私有需求组合与共享三维匹配复制--障碍.md)。在一般UM中给定两份完整实际调度sigma、tau，峰分别≤C、≤T且T≤C≤2T。对改变任务j记源s_j、目标t_j、两端时间a_j、b_j，f_i是不变任务负载，并置

\[
S_i=f_i+\sum_{s_j=i}a_j,\quad Q_i=\sum_{t_j=i}b_j,
\quad U=\max\{2T,C+T/2\},\quad h_i=(S_i+Q_i-U)_+.
\]

若改变任务集合R满足每源机cover及每目标机packing

\[
\sum_{s_j=i,j\in R}a_j\ge h_i,
\qquad \sum_{t_j=i,j\in R}b_j\le U-S_i,
\]

则先迁R、再迁其余改变任务，每阶段内任意顺序均保持全部机器负载≤U。承重恒等式是迁移W后负载S_i−D_i(W)+P_i(W)：第一阶段不超过S_i+P_i(R)≤U；迁完R后，不论后续次序都有S_i−D_i(R)+Q_i≤U。这里只给静态充分证书；找不到R不推出OPT>T，tau未知时也不能免费把它输入。

同一源机的a_j全相等、同一目标机的b_j全相等时，源下界ceil(h_i/q_i)和目标容量floor((U−S_i)/r_i)可放进带上下界整数circulation，给可计算特殊分支；一般异端时间不能擅自用件数替代真实负载。HOLD-EDGE只是在同一静态集合内把保留任务后移，没有扩大cover存在性。两机三任务的已知反例取T=3/4、C=5/4、U=13/8；tau实际可行，但每个必须迁移的首步把峰推到7/4或2，故“有目标即有安全首步”错误。

另一个方向也必须分开：三机六任务每源两件时间1，目标边依次A→B、A→C各3/5，B→A、C→A各3/10，B→C、C→B各1/5。T1、C2、U5/2，h=(1/10,3/10,3/10)，初始目标余量每机1/2。没有静态R同时满足cover/packing，但动态顺序B→A、A→B、B→C、C→A、A→C、C→B的峰仅23/10。因此“静态证书失败”既不能推出OPT>T，也不能推出没有U内动态路径。两机例是否定无条件路径存在，三机例是否定静态证书必要性，不能混作同一反例。

复制也不给该全输入桥：不交块满足OPT(disjoint union)=max各块OPT；共享同机将每任务复制k份，若F为assignment-LP最优值、O_k为复制后整数最优，S=max_iΣ_{j:p_ij有限}p_ij，则kF≤O_k≤kF+S，O_k/k趋F。前者不放大gap，后者会整数化分数解；binary k可能使显式nk输出超出输入位长多项式。私有需求串接的精确min、固定根门的max/min及parity共享复制反例是相关但不同操作，不将它们统称所有复制都失败。

本批还完整读到该规范主稿192行及[实际程序资源](../资源/共同激活与共享复制算术原入口及双路径反例--资源.md)。主稿§7把复制小例写成“三机三任务”，而代码实际为**两机三unit任务**，才有F=3/2、O_k=ceil(3k/2)；保原字节并明确纠错。程序只核固定顺序、64个R子集和k1..12，没有带下界流、通用目标搜索或一般LP实现；q=0<h边界是字面断言，不能冒称运行了不可行flow。有限PASS不提供一般证明，本次未重跑该程序。

### KDM完整层不足与直接robust源的后续排除

[高维配额审查](../审查/三维匹配与高维配额部分障碍双源审查--审查.md)把普通完整KDM matching与所有部分层明确分开。K-均匀超图有q条边，nu_t为最多可同时选择的边数，每条所选边只领t个资源、全局资源不交。在根需求q、边点需求K、资源终端的给定需求树合同中，

\[
b^*=\max_{1\le t\le K}\min\{\nu_t/q,t/K\}.
\]

任意正比例b的树取t=ceil(Kb)就给该层不交束；反向从束族造树。完整K匹配仅控制t=K，不能控制中间t。公共C大小K−t、每边私有P_i大小t的族可使nu_K=1、nu_t=q而b^*=t/K；两份K束在t≤K/2时总能各取互不冲突t子束；甚至资源重数至二也可有完整层比例趋零而部分层比例趋一。README要求任意低载真实调度的KDM decoder，不能降成只解完整匹配层。

真正可接树桥的条件合同为：q≥1个变量，每变量若干显式标签束S_e、|S_e|=K；YES每变量可选完整束且全部不交；NO对任何|X'|≥gamma q、任意标签选择和每变量|B_x|≥delta K的子束，都不可能全局不交。还必须有gamma≤delta。根→变量→标签→资源、需求q/1/K/0的编译才给YES b*=1、NO b*<delta，并由适用的真实token桥得到YES OPT1、NO OPT>2−delta。若不加gamma≤delta，旧NO只给b*<max(delta,gamma)，不能写近二阈值。该条件是已读相关源的重要纠错，不能因README未展开而丢失。

这里必须继续读KDM原件首段的**后续范围更新**，不能止于旧清洗审查§8–9的“robust源待构造”。该更新明确：上述四层私有标签束保完整YES、且只含显式norm1菜单资源领取时，在delta≤3/8、gamma≤delta的直接源合同内已有福利LP分离。原§4–5仍保留其错误字节，不因首段更新而成为正确的旧定理；公屏484的更强半比例草稿也不并作本次已审结果。

为说明这个后来排除的准确范围，令q≥1、K≥1，每变量x有显式非空indexed标签菜单；标签e对S_e内各资源赋权1/K、其余为零，故总权恰1。若输入格式允许空菜单，先判NO即可：完整YES不可能有空菜单；此预检只要求在原promise上正确，不认定所有非promise实例都满足NO。不同变量真实获得的资源集合B_x两两不交，允许空集合及未分配资源；质量为r_x=max_e |B_x∩S_e|/K。这里没有额外coherence、AND或标签相容约束。同一资源可在不同菜单出现，但不能另把同一物理job或共享内部容量约束塞入该福利模型。

每标签设z_xe≥0，只对正incidence设y_xeu≥0，解部分支撑福利LP

\[
\sum_e z_{xe}=1,\qquad y_{xeu}\le z_{xe},\qquad
\sum_{x,e}y_{xeu}\le1,\qquad
L=\max\sum_{x,e,u}y_{xeu}/K.
\]

该LP总可行（任取每组一state并令y全零），且L≤q。任意真实allocation逐组选attaining标签即可嵌入，故完整YES给L=q。这是允许部分领取的福利LP；不能在近完美YES时替换成每组必须取得完整正support的FSLP。

已全文比较[近完美归一化robust四源审查](../审查/近完美归一化robust源四源审查--审查.md)的自足福利机制：组间按z独立选state，条件于选中e以y/z提议资源，每资源交给原系数最大的提议者，零z不除法。固定资源/系数level的总提议概率≤1，独立性及1−e^(−t)弦界给期望福利≥(1−1/e)L>5L/8（L>0）；按state再按coin作精确有理条件期望可确定性化，最终重新取attaining标签不会减福利。菜单、正incidence、levels及原有理因子数均多项式，因此按显式输入总位长计；本次没有运行通用精确LP后端。

若L=q，则实际W=Σ_x r_x>5q/8。令H=#{x:r_x≥3/8}，有W≤H+(q−H)3/8，故**H>2q/5**。当0<gamma≤delta≤3/8时，这些组也满足r_x≥delta，且H>2q/5>gamma q；逐组取attaining标签及其真实已领子束即违反robust NO。因此精确判别器“L=q判YES，否则判NO”接受全部完整YES、拒绝全部该robust NO；不必实际运行舍入finder。不要求q或K被8、5整除，|B_x|≥delta K本来按整数数量与有理阈值直接比较。delta=0且0<gamma≤delta没有合法参数，不另偷补退化promise。

四源审查还给更广的近完美形式：norm1显式菜单的YES只需至少(1−eta)q组质量1，NO可分别用r≥delta或r>delta的高组数严格<gamma q。在0≤eta<1、0≤delta<1、0<gamma≤1且5(1−eta)/8≥gamma+(1−gamma)delta时，精确LP以L≥(1−eta)q判YES；福利严格大于5L/8，而NO任意allocation福利严格小于[gamma+(1−gamma)delta]q。于是0<gamma≤delta≤3/8、eta≤1/40全部包含，连eta=1/40、gamma=delta=3/8等号角点也成立。完整YES是eta=0的特例；近完美证明与KDM首段H>2q/5的完整YES计数不能混为同一个运行记录。

所以README“构造固定delta robust source gap”是当时未完成的义务；此后上述直接四层、显式norm1菜单合同在所列参数域已被可多项式判别边界挡住。没有给出NP-hardness归约；若存在确定性Karp归约从NP完全语言到此完整promise，复合判别器将推出P=NP。非归一化、隐式指数菜单、真正共享内部job/coherence、多层一致性或不同YES/NO量词须另审，不由此排除。更强均匀束半比例草稿保持原作者独立身份。

在这些域外若继续反面研究，要否定存在某统一epsilon改善，仍须对每个固定足够小delta给相应近二gap，并用已知可计算正有理标尺T比较YES≤T、NO≥或>明确的(2−delta)T，给任意低峰实际全原jobs调度的位多项式decoder。不能用一个固定弱gap排全部epsilon，也不能以未知OPT作decoder阈值。高维匹配文献的随机稀疏化层保留NP不含BPP等准确假设；完整KDM困难性不是普通UM困难性。

本工作区另外保留按需在notes/experiments/candidates存有接续价值材料、成熟资产沿规范链接而不另复制的历史约定。它没有列实际notes或实验，不据目录建议生成不存在的资产。可以work.py私聊旧actor、只有checkpoint并确认pushed的本地稿才对其他clone可见，也是历史通信/可见性合同，不授权本次发送消息或证明任何一次推送。这里保全其独有数学导航、robust全层缺口、身份与路由，不把整个工作区一概丢弃或冒称新增证明。

## R-3a72：2026-10-17全输入桥复盘与一侧阈值接口

该README（`3fc271ca139db65fde1b`）2134B/25行，JSON（`089efa8e78ad58ccaade`）149B/6行；完整冻结定位和指纹见manifest。JSON是schema整数1、save=`unrelated-machines`、actor=`R-3a72cffb966f40398a89109a027adebd`、instance=`0e03bfadf3b14765bd72daba919180a5`，只作历史身份。

README唯一目标明确为：存在统一epsilon>0和确定性总位多项式算法，对一般R||Cmax的每个合法输入输出实际完整调度，Cmax≤(2−epsilon)OPT；目标仍OPEN。这里的量词是**存在一个固定统一epsilon**，不是对每个指定epsilon都给算法。历史目标可以复用，旧日期的状态不得冒充未经核对的最新全仓事实。

### 历史交流与三类接口分流

2026-10-17复盘记已向boss1（当时actor `R-f629bcbd1df640d581bb076cf2a410ea`）和boss6（`R-976a3f211e1a4bf58c54998365200e14`）发出请求。这只证明README记载请求，未给回复、已读回执或双方认可；本次没有发送任何消息。其“本地独立审查与当前地图同一分流”也只是当时自报，不能据此新增本轮blind、外审或投票式认证。

已读[任务级共同容量义务](../问题/任务级共同容量的算法义务--问题.md)、[研究状态总账](../审查/不相关机研究状态总账与开放义务--审查.md)、[共同容量修复边界](../审查/共同容量修复的判定与实现边界--审查.md)及[有限阈值核验](../计算/共同容量与未知阈值的有限精确核验--计算.md)，可把三类分流准确理解为：

1. Hall/weighted/distorted group、异构macro、单sink/profile和common-size reopen的实际算法只在各自显式输入合同内闭合。它们分别依赖共同资格、唯一home、宏微尺寸包络、给定核心/支持等，并非每项都依赖同一组条件。各自未知OPT搜索可闭合，不代表能从任意普通矩阵抽取该结构；给定tau、来源、组或核心不能偷作免费输入。
2. 裸C2、独立配置/逐边probe、固定槽/固定向量贪心、严格次二批量和单任务峰值障碍只反驳精确合同。CONFIG gap或坏算法不推出一般近似不可能。README的“C2+CONFIG仍OPEN”保为当时状态，引用时必须写矩阶、共享条目和阈值；不能把当前任一弱合同反例替换成所有共同系统的判决。
3. 下一义务是对任意P,T得到共同容量证书与所有机器同时合法的实际整数分配，或可靠FAIL⇒OPT>T；统一不退化epsilon、原job身份/资格、零/∞和总位复杂度必须同一合同。它是研究目标，README没有实现生成器。

相关纠错不能被“已闭合接口”一句吞掉：共同尺寸搜索必须先验B≥max_i f_i，孤立高核心机器和空残余仍贡献完整峰；旧四例谓词/递归DFS不是完整通用后端，合法1200长链可触发RecursionError，但这不反驳迭代整数流的数学多项式算法。有限400例、guard探针或旧“无fatal”不代替任意矩阵结构生成和全机容量保证。

### 半单位共同选择不是免费前处理

已读[联合选择审查](../审查/联合选择槽舍入三源精读--审查.md)与[半单位双程序资源](../资源/半单位共同选择与同资格计数调度双入口--资源.md)。给定共同big匹配H、T和剩余small分数见证后，ST型槽舍入可给(3/2+delta)T；先找同一个H是另一量词。

T=1、有限时间仅1/2或1、每job恰一个small端、固定0≤delta<1/2时，未入H的jobs在唯一small端已是整数执行；(A_delta)共同选择等价真实OPT≤1。逐x的3DM归约中每x三件half激活任务，每被激活triple机须把两关联任务送Y/Z；激活数r≥q而2r≤2q，迫r=q并解perfect3DM。YES OPT1、NO OPT3/2；delta=1/2时全small峰3/2使接口失去辨别力。它只排将该beta=1/2精确共同选择当免费步骤，不排绕开H或其它松弛/算法。

两原程序有限域也分开：第一程序362源、四delta共1448查询；第二程序265源只在容量2跑一次，四delta另核floor等式，没有跑四遍DFS；缓存状态数不是调度数。程序支持归约与资格边界，不独立证明NP完全性，不是一般多项式共同选择器。本批未运行它们，不把资源页历史运行移接为本次。

### JC-THRESHOLD的一侧合同与下一试验

源所用 `JC-THRESHOLD-epsilon(T)` 应保以下方向：固定统一epsilon∈(0,1)，对任意合法P及非负二进制有理T，总位多项式过程输出完整实际sigma、Cmax≤(2−epsilon)T，或FAIL及可验证依据保证OPT>T。OPT≤T时必成功；OPT>T时仍允许成功输出满足目标界的真实调度，不要求必须FAIL，也不把任意证书搜索失败升级成OPT>T。T=0要真实处理全部jobs的零资格端，不能用正阈值搜索漏掉它。

README计划下一项高信息行动是在两树/共享逃逸族检验“共同矩+完整CONFIG/计数”是否可计算、可舍入；若失败，记录首个失效约束，再转不同桥。这个计划未给新证书。已读[C2一般PSD与CONFIG边界](../审查/C2多切片的一般PSD与最小边界负平方--审查.md)：其unit multislice裸C2证书含同机三job矩−1/m^4，T<2的完整CONFIG却不可行，故不能拿它判共同C2+CONFIG合取gap，更不能说CONFIG全局支配C2。已读[共同Gram/flat原子资源](../资源/共同矩有理Gram平坦原子与低阶Latin点原入口--资源.md)：给定真正flat共同矩可提取实际原子，但低高阶秩不等时返回None不意味无调度；同一一阶law也可有不同二阶和M1；其helper含更强count localizer，不是弱C2-load验证器或矩生成器。上述区别正是该下一行动必须先冻结的完整合同。

原“不要重复已被停止标准排除的独立probe微调”记录当时研究取舍，不限制当前授权Solver自由研究；可复用的是它要求新信息实质减少共同容量/统一余量/可计算生成义务，而不是堆有限局部测试。notes/experiments/candidates、规范资产链接、work.py私聊和checkpoint pushed可见性段与前一工作区同属历史管理合同；无具体材料即不补造。该工作区因此新增一份精确复盘来源和开放合同导航，不新增一般算法或近二hardness。
