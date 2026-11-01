# 配置下界的有限覆盖实现与近2困难性归约的可靠性缺口

本稿针对 UM-TARGET-v1 的反向困难性路线，证明有限置换覆盖的准确边界。核心是已知图覆盖/局部多面体机制的调度专门重构，非新的困难性结果；独立论文价值与全球新颖性未认证。目标仍 **OPEN**。

## 精确对象

给定合法一般不相关机实例P，有限incidence图的左右点为机器i与任务j，每个p_ij<∞有一条边。固定整数q≥1。一个q-cover Q由每条有限incidence边的置换π_ij:[q]→[q]决定：机器为(i,b)，任务为(j,a)，任务(j,a)只可在机器(i,π_ij(a))上执行，时间仍为p_ij。机器和任务全部复制相同q次；没有额外机器、任务、有限边、处理时间修改或跨类型接线。任意度数任务均允许。

C_i(T)是原机器i负载≤T的任务子集（含空集）。配置可行解是非负y_i,C，Σ_C y_i,C=1且每个j满足Σ_i Σ_{C∋j} y_i,C=1。T_CONF是配置可行性的最小阈值。若用任务覆盖“≥1”的惯例，可逐个任务删去正配置中的该任务、把相应权重转到删后配置，直至其边际恰1；向下封闭与非负负载保证合法，其他任务边际不变。因此等式合同与该惯例等价。

全部实例有限、全部有限时间为非负有理数；T_CONF取得且为有理数：配置全集有限，阈值只在有限个有理配置负载处改变，而固定阈值的可行polytope有有理解。零最优值、空任务均包括。

## UM-CONFIG-FINITE-COVER-v1：精确覆盖关系

对上述任意合法P成立：

1. 任意q-cover Q的任何真实makespan≤T调度，去除copy标签并按q平均，给P的T配置可行解。其概率分母整除q。
2. 对任意q-cover Q，T_CONF(Q)=T_CONF(P)。
3. 任意P的真实调度可以提升到每一个q-cover Q，且每个(i,b)的负载恰为原i负载。
4. P的任意有理T配置证书y（共同分母q）可由某个q-cover的真实T调度精确实现其所有单机配置分布。
5. 因此每个cover满足T_CONF(P)≤OPT(Q)≤OPT(P)，且min_{q≥1,Q为q-cover} OPT(Q)=T_CONF(P)，最小值取得。

这里的min不是一个位多项式算法。q是配置证书分母，cover或证书的枚举尺寸可能极大。结论不把有理点的存在升级成高效寻找，不给定一个任意cover的调度算法。

**分母尺寸补充。** 令r=m+n≥1。固定T_CONF下的有限配置LP可写Ay=1,y≥0，其中A为0/1矩阵、至多r行；每个列恰在所属机器行与配置所含任务行取1。取rank r'≤r的独立行与一个basic feasible solution，补齐r'个基列得到非奇异0/1方阵B。Cramer法则保证所有基变量的分母整除q=|det B|，并且Hadamard界给q≤(r')^(r'/2)≤r^(r/2)。因此存在达到最优配置阈值的cover，其log q为poly(m+n)，但显式q本身可能指数，cover的机器/任务数都与q成正比。不能把这个界叫作位多项式规模归约。给定证书的具体实现仅可声明相对显式输出q规模的输出敏感复杂度；它没有保证找到最小q或高效求配置LP。

### 证明1：真实调度的投影

每个机器copy(i,b)的邻域中，对每个原任务j最多出现一个job-copy，这是置换incidence的关键。将该copy所执行的任务去除copy标签得原任务子集C_i,b，负载保持且≤T。定义y_i,C=(1/q)|{b:C_i,b=C}|。每个原任务j共有q个copy，调度恰执行q次，因此其总覆盖概率为q/q=1。

### 证明2：配置阈值在任意cover下不变

Q→P：在每个机器copy的配置分布中去掉copy标签，再按机器type平均；由于每个原j的q个copy均恰覆盖一次，得到P的配置解，负载保持。

P→Q：对固定机器copy(i,b)，其原j邻居是唯一job-copy(j,π_ij^{-1}(b))。将原配置C替换成这些copy的集合，沿用y_i,C概率。每个job-copy(j,a)在machine-copy(i,π_ij(a))上的包含概率恰为原x_ij；对i求和等于1。故每个T的两边可行性等价。

### 证明3：任意整数调度无损提升

若原调度σ(j)=i，则所有copy(j,a)都送(i,π_ij(a))。对固定(i,b)，每个σ(j)=i的原任务恰贡献一个job-copy，故负载与原i相等。

### 证明4：有理配置证书的精确实现

令q y_i,C全为整数。在每个原i设置q个machine-copy，将配置C分配给恰q y_i,C个copy。对原j，统计所有含j的已选machine-copy位置(i,b)；覆盖等式保证恰q个位置。将这q个位置任意双射编号为job-copy标签a∈[q]。如果位置(i,b)被编号a，规定π_ij(a)=b并把(j,a)安排在(i,b)。对每条(i,j)，这给出一个partial bijection：所用a不同，所用b不同。将其任意补成[q]的完整置换。每个job-copy恰安排一次，每个machine-copy所执行原任务集合就是预先分配配置，故真实负载≤T并精确实现y。

5由1、3、4并取T=T_CONF推出。若T_CONF=0，每任务在配置覆盖中必有零时间可用边，逐任务选择零边即得OPT=0。因此对OPT>0有T_CONF>0，故额外有OPT(Q)/T_CONF(Q)≤OPT(P)/T_CONF(P)：纯cover不能放大原配置间隙。

## 任意固定围长限制仍允许collapse cover

**引理。** 对任意有限图G及整数g≥1，存在G的有限cover使其围长>g。这里不主张构造尺寸或时间多项式。

**自足证明。** 为每条无向边选方向并配不同形式生成元e；反向配e^{-1}。令B是字母e^{±1}上所有长度≤g的freely reduced words（含空词）的有限集。对每个生成元e，右乘e并自由约减定义从B的一个子集到B的partial injection，只保留乘前乘后都在B的项；用任意双射补全为B上的置换h_e。其逆在相应partial map的逆上也正确。

每个非空freely reduced word w、|w|≤g，其字母依次作用于空词时，所有前缀仍在B并沿预定partial map运行，因此将空词送到w，而非空词。故对应置换积h_w不等于恒等。令H为这些置换生成的有限置换群，取H对自身的正规右作用。为G的每个点v建立(v,h),h∈H，定向边e:u→v接(u,h)与(v,h h_e)。这是有限cover。

若此cover有长度≤g的简单环，它投影成G上的非回退闭行：cover局部邻接双射保证投影若立刻沿同一边回退，则lift也立刻原路回退，不能是简单环。由于每条原边用不同生成元，非回退闭行给非空freely reduced word w，长度≤g。回到同一fiber h迫h h_w=h，故h_w=1，矛盾。证毕。

cover的复合仍是cover：q-cover后r-cover可按原点type将(q,r)成对索引，每个原incidence的连接是[q]×[r]的一个双射。先用证明4得到T_CONF可行cover，再对其incidence图取上述高围长cover并用证明3提升调度，就得到原P的某个有限cover Q满足

OPT(Q)=T_CONF(P)，且incidence图围长>g。

若每任务恰有两台可用机器，incidence图相当于机器多重图逐边细分；machine-graph girth>h只需incidence girth>2h。原seed连通时可取连通分量：有限cover的每个连通分量仍以某个相同fiber数覆盖原连通图，且调度与围长性质保持。

## 明确小例：同一种子与相同复制数下的不同真实OPT

原机器A,B,a,b。任务c在A,B两端时间都为1。对r=A,B及对应terminal t=a,b，任务r0,r1,r2在r时间为1/3、在t时间为1。其他边不可用。

整数OPT=5/3：任何调度中c送某根r。若makespan<5/3，则r最多再接一个小任务，至少两个任务须送terminal t，令t负载至少2，矛盾。5/3调度可令c与两小任务给A、剩余一任务给a，B执行其全部三个小任务。

T_CONF=4/3：T<1时c不能被覆盖。1≤T<4/3时，根含c的配置不得含任何小任务；其terminal的每个配置最多一个任务，故根所含小任务数的期望≥2。如果根含c概率为α，根的小任务期望≤3(1−α)，所以α≤1/3。两根覆盖c需两概率和1，矛盾。

在T=4/3，每根以概率1/2执行三个小任务，以另1/2均匀选择c+一个小任务；每terminal均匀执行其三个singleton。c两根各覆盖1/2，每小任务根覆盖2/3、terminal覆盖1/3，故可行。共同分母q=6。证明4实现6-cover有真实4/3调度；每根前三个copy执行全部三个小任务，后三个copy分别执行c+一个小任务；每terminal执行每个singleton各两个copy。按socket分配job-copy即可补全全部incidence置换。

与之对比，全部incidence置换均为恒等的6-cover是六个原seed的互不相交并，其OPT仍为5/3。于是同一seed和相同q并不决定整数OPT；“任意接线都保留seed soundness”和“任意接线都自动实现配置LP”均为错误。

规范[精确构造与审计](../../../tests/audits/unrelated_machines/configuration_finite_cover.py)验证给定有理配置证书并实际构造覆盖的逐边置换及逐任务分配；[独立审计](../../../tests/audits/unrelated_machines/configuration_finite_cover_independent.py)不导入该程序，另行枚举种子调度、构造覆盖并检查自由字置换。实际[输入](../../../examples/unrelated_machines/configuration_finite_cover_seed.json)、[真实调度证书](../../../evidence/certificates/unrelated_machines/configuration_finite_cover_witness.json)、[规范冻结结果](../../../evidence/runs/unrelated_machines/configuration_finite_cover_audit.json)与[独立冻结结果](../../../evidence/runs/unrelated_machines/configuration_finite_cover_independent.json)分开保存。一般命题来自上述证明，有限枚举不替代普遍证明。

## 对困难性路线的准确含义

- 这否定从一个LP-gap seed直接声称“所有（或所有高围长）置换lift都有近2真实OPT”的soundness合同。存在适当cover恰把整数OPT降到原配置下界。
- 它不否定**选定接线族**的困难性归约，不证明随机独立接线以高概率collapse，也不证明expansion或其他伪随机条件足以collapse。高围长结论是存在，不是随机概率结论。
- 单个显式NO seed本身没有源NP-hard输入；想得到近2困难性仍需与源问题相关的YES/NO接线选择，并证明任何低负载调度可解码出源对象或违反精确soundness阈值。
- 一个成立的目标soundness可能排除上述collapse接线，但必须给出新的全局限制及其解码证明。配置局部可行、边置换、复制数与短环控制本身都没有提供该证明。
- Vontobel–Koetter 的原始机制已核：arXiv:cs/0512078v1 的 Proposition 10（PDF18/印18）、Appendix A.1 的 Lemmas 55–56（PDF50–52/印50–52）将编码局部多面体的有理点与有限覆盖伪码字联系。原文模型是二元线性码，本文自行证明调度全部方向，不把调度恒等式标作原文定理。原字节、版本与范围见本题文献清单。

## 真正反面目标所需的下一条桥

要在 P≠NP 下否定所有统一改善，一条足够路线是：对每个固定有理 δ∈(0,1)，从某 NP 完全语言构造总位多项式归约，输出合法 (P,T)，T>0，并有 YES⇒OPT(P)≤T、NO⇒OPT(P)≥(2−δ)T。假如目标算法对某 ε>0 成立，选择固定有理 0<δ<ε；算法输出的精确负载即区分两类，因为 YES 输出≤(2−ε)T<(2−δ)T，NO 的每个合法输出均≥(2−δ)T。归约次数可依固定 δ，但不能依输入数值或随规模增长的复制阶。

这只是充分的 proof obligation，**尚无这样的归约**。一个固定 ρ<2 的困难性不够；一个无限大的、无法在源输入位长多项式内写出的覆盖也不够；仅仅引用 UGC/ETH 不会自动补出调度归约。特定接线族可以排除本稿的坍缩覆盖，但必须证明对该族全部低负载真实调度的解码可靠性，且同时保 YES 调度与总位规模。

无条件证明目标算法不存在还会蕴含 P≠NP：若 P=NP，可在公共分母整数格点上用调度判定与逐任务自约化精确求最优，格点端点位数为输入多项式。这里没有将 P≠NP 当作已证明事实。

## 价值与审查边界

Truth：以上所列等价式和有限覆盖构造有自足证明；独立先重构后冻结攻击见[实际审查](../../reviews/unrelated_machines/configuration_finite_cover_review.md)。Value/Mechanism：排除把局部配置间隙、纯复制接线与高围长自动拼成整数 soundness 的步骤，并提供可执行的坍缩证书生成器。Novelty：旧图覆盖机制的专门重构，不认证新颖。Ambition：保留一般输入反向归约为主目标；未排除精选接线、扩张性、PCP/Label Cover 归约或其他算法，也未证明 UM-TARGET-v1 的反面。
