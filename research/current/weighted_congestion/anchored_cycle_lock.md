# 锚定三元多项式时钟把双轮改善环锁成全状态非存在

## 精确命题身份

**ID/version：** `WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1`。

**中文数学名称：** 锚定三元多项式时钟的双轮改善环全状态锁定。

**Exact Statement / Objects / Domain / Quantifiers。** 给定任意整数n≥3、p≥0，以及一个MODEL中的有限加权原子拥塞博弈G：玩家为0,...,n−1，权重w_i>0，每人恰有两个资源子集动作S_i^0,S_i^1；资源费用为次数至多p的非负系数多项式，允许零费用及空动作。给定任意实数α≥1，假设从全0动作开始，按玩家顺序0,...,n−1各翻至1，再按相同顺序各翻回0，得到的全部2n次真实单方偏离均严格α改善。则存在一个同玩家、同权重、仍为每人两个动作的MODEL游戏G'，没有α-PNE；G'只在G上增加正系数单项式资源，所有旧资源与旧费用原样保留。

**Definitions / explicit degree。** 记C_i^G(s)为真实负载成本，

\[
 B=\max_{s\in\{0,1\}^n,\ i}C_i^G(s)>0,\qquad
 \eta=\min_{\text{上述环边 }s\to s^{\oplus i}}
 [C_i^G(s)-\alpha C_i^G(s^{\oplus i})]>0.
\]

任意已知统一上界B≥max C_i也可代替精确最大值；仍有η≤B。对三元组T=(0,i,j),1≤i<j≤n−1，写W_T=w_0+w_i+w_j，并定义

\[
 L=\binom{n-1}{2},\quad
 \delta=\max_T\left(1-\frac{\min\{w_0,w_i,w_j\}}{W_T}\right)\in(0,1),\quad
 M=2\alpha B,
\]

\[
 D=\left\lceil\frac{\ln(4\alpha^2BL/\eta)}{\ln(1/\delta)}\right\rceil. \tag{1}
\]

G'的费用次数至多max{p,D}，新增2L个资源，每个新增资源费用为M(x/W_T)^D，其中W_T由该资源所属三元组决定。D≥1，费用系数M/W_T^D严格为正。若原游戏的权重、系数和α全有理，则G'也全有理。

**Conclusion / Scope。** 对G'的每个纯状态，存在玩家的另一动作严格α改善，故没有α-PNE。这是一个依赖完整有限实例参数的编译定理，不是次数保持的定理，也不是全类O(d/ln d)存在或非存在结论。最终游戏只保留指定的两个动作，不能额外加入空动作或全部资源子集2^E；否则可能恢复均衡。

**Dependencies。** MODEL真实成本、有限状态最大最小值、二进制顺序关系和下面的直接费用估计；不导入外部均衡定理。若输入由循环窗口复制提供，该输入定理是应用前提，并非本定理的证明前提。

**Evidence / Objections / Status。** 下文为完整直接证明；[独立审查](../../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md)在读作者稿前完整重构同一构造，随后攻击冻结稿；两份Fraction审计见文末。没有发现代数反驳；全类目标仍缺对D的统一增长控制，尤其δ可接近1，B/η可很大。Status为complete stated-scope proof; independently reconstructed and exactly audited; unrefereed。Truth为所述编译定理，Value为精确cycle-to-no-PNE接口；Novelty未认证，未外审，Ambition保留唯一全类题OPEN。

## 一、锚定三元资源关联

对每个T=(0,i,j)放两个不同资源e_{T,0},e_{T,1}，费用均为

\[
 c_T(x)=M(x/W_T)^D.
\]

在局部位置(0,i,j)上规定模式b=(0,1,0)。玩家k∈T选择动作s_k时使用e_{T,s_k\oplus b_k}；其他玩家不使用这对资源。每个新动作等于原动作S_k^{s_k}加上所有相应时钟资源。新旧资源集合互不相交，因此总成本是原成本与时钟成本之和，全部按偏离后的真实负载计算。

三名玩家完全共享某个资源，当且仅当(s_0,s_i,s_j)为010或101，即s_0=s_j≠s_i。此时资源负载恰W_T，每名参与者支付M。其余局部状态把三名玩家分在两个资源上，每个使用资源的用户集均为真子集；因此每个使用者支付的费用至多Mδ^D。注意这里不假设玩家等权。

## 二、抽象完整触发时钟的全状态覆盖

称状态合法，当其二进制序列最多有一次相邻位变化。合法集合恰由双轮顺序环的2n个不同状态组成：一轮为前缀1后缀0，另一轮为前缀0后缀1。每个合法状态的每个锚定三元局部模式均不是010或101，故没有完整触发。

固定非法状态s。令i≥1为最早与s_0不同的位置。若i之后没有与s_0相同的位置，则s只含一次位变化，矛盾；故有j>i满足s_j=s_0。三元(0,i,j)完整触发，玩家i当前时钟成本至少M。

将i翻回s_0后，它参加的每个锚定三元都不再完整触发：

- 当i为中间位置的三元(0,i,k)，它已与锚点0相同，故不能触发。
- 当i为最后位置的三元(0,h,i)，h<i且由i的最早性有s_h=s_0，故同样不能触发。

所以该偏离后的玩家i时钟成本至多LMδ^D。这个论证给每个非法状态一个确定合法偏离；没有仅检查一个改善环。

## 三、多项式泄漏上界与环上严格改善

由(1)，

\[
 \delta^D\le\frac{\eta}{4\alpha^2BL}. \tag{2}
\]

固定原双轮环的一条边s→t，由玩家i移动。s和t均合法，所以其时钟新成本至多LMδ^D。时钟旧成本非负。因而新游戏的严格改善差至少

\[
 C_i^{G'}(s)-\alpha C_i^{G'}(t)
 \ge\eta-\alpha LM\delta^D
 =\eta-2\alpha^2BL\delta^D
 \ge\eta/2>0. \tag{3}
\]

这里没有把新旧时钟成本假定为相同，也没有把未改动资源费用漏掉；直接丢掉非负旧成本足以得到保守界。因此所有合法状态都保留原环的严格α改善出口。

## 四、非法状态严格改善

对第二节选择的非法状态玩家i，当前总成本至少M。偏离后的原成本至多B，时钟成本至多LMδ^D。结合(2)得

\[
 \alpha C_i^{G'}(t)
 \le\alpha B+\alpha LM\delta^D
 \le\alpha B+\eta/2.
\]

又η≤B且α≥1，所以η/2≤αB/2=M/4。于是

\[
 \alpha C_i^{G'}(t)\le3M/4<M\le C_i^{G'}(s). \tag{4}
\]

每个非法状态因此都有严格α改善偏离。合法与非法状态穷尽全部2^n个纯状态，由(3)(4)即无α-PNE。

## 五、边界、次数与不能省略的限制

- B>0和η>0由严格环自动保证；η≤B，因为每条边的偏离后成本非负。
- n≥3时L≥1，所有权重正使0<δ<1，故D有限且为正整数。新增费用仅含一个正系数x^D；不存在负系数、阈值费用或负常数平移。
- 原模型允许空动作及零费用；证明只使用非负性、严格环与有限性，故覆盖这些情况。成本不作0/0，均用严格不等式。
- n=2时双轮环本身经过全部四个状态，原游戏已经无α-PNE，无需时钟。n=1在非负成本、α≥1下不可能有这种严格双轮环。
- 有理输入的B、η、δ、M有理，D为有限整数，所以新资源系数有理；可用有理数幂逐次检查(2)，无需浮点对数确定D。
- 权重和费用没有依玩家或资源改换规则。不同三元的归一化W_T只进入合法的资源系数M/W_T^D，玩家权重仍统一为w_i。
- 不能扩大最终策略族。尤其若再给每人空策略，全空状态立即是精确PNE，定理结论即失效。

## 六、对唯一主题留下的精确义务

将近线性倍率α≈p的双轮环代入，只能得到次数q=max{p,D}的非存在游戏。要由此严格否定题设的全类Cd/ln d上界，需要一族使

\[
 \frac{\alpha\ln q}{q}\to\infty
\]

（或对每个C提供足够大的该比值），并给出所需增长及整数次数。[统一预算的普适次数障碍](uniform_clock_budget_barrier.md)现已证明：对全部严格双轮输入、任意anchor和满足(2)的D，实际次数q≥D均有αlnq/q<α/(α+1)<1。因此沿本稿保守预算继续调输入环不能完成该义务；必须改用实际新旧clock差、非统一预算或其他全状态机制。本编译定理的量词和正确性不变。

### 当前统一泄漏预算与权重极差

这是式(1)所选D的直接推论，不是当前时钟实际最小可行次数或任意时钟的次数下界。归一化max w_i=1、min w_i=r∈(0,1]，若最大和最小权各至少有两名玩家取得，则对任意锚点都可取其余两名互异极端玩家组成三元（r=1时取任意两名非锚点）。因此

\[
 \delta\ge \frac{1+w_0}{1+w_0+r},\qquad
 \ln(1/\delta)\le\ln\left(1+\frac r{1+w_0}\right)\le\frac r{1+w_0}.
\]

由η≤B，任何被要求满足统一预算(2)的D，特别是(1)选定值，均有

\[
 D\ge\frac{1+w_0}{r}\ln(4\alpha^2L)
 \ge\frac{\ln(4\alpha^2L)}r.
\]

多尺度输入中，这解释了为何仅换锚点未必改善本方案。它不排除逐资源更精细估计、非统一幅度或次数、不同锁定资源或更合适的输入环。[独立审查](../../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md)另行核查此推论及其准确否定范围。

## 字面核验与读取合同

- [实际三玩家编译审计](../../../tests/audits/weighted_congestion/cyclic_clone/verify_clock_compiler.py)（路径以仓库根为准：`tests/audits/weighted_congestion/cyclic_clone/verify_clock_compiler.py`）复用[整数二次三玩家](quadratic_triad/three_player_integer_obstruction.md)的六个真实资源，把原初态010重标为000；权重16,2,5，α=21/20，B=2002，η=677/20，δ=21/23，最小满足(2)的整数D=62。逐资源重算全部8状态、6条环边及指定严格偏离；另枚举n=3,...,9的抽象时钟全覆盖。没有LP、随机性或浮点。
- 运行：`python3 tests/audits/weighted_congestion/cyclic_clone/verify_clock_compiler.py`。标准输出与运行命令、Python版本、源码hash封存在[实际编译结果](../../../evidence/runs/weighted_congestion/cyclic_clone/cycle_lock_triad.json)。该实例已知本身无较小倍率PNE；本次仅核验编译接口，不提高既有下界。
- [独立时钟审计](../../../tests/audits/weighted_congestion/cyclic_clone/independent_clock.py)在读作者稿前编写，按实际资源literal/负载遍历n=3,...,7、α∈{1,3/2,2}及seed=0,...,3的60案例，共2976状态、2376环外状态，最大D=107。它假定B=1、η=1/4，仅核验条件式时钟几何及泄漏余量；没有声称这些参数均有真实输入环。
- 运行：`python3 tests/audits/weighted_congestion/cyclic_clone/independent_clock.py --output <新的输出路径>`，独占创建文件；[独立冻结记录](../../../evidence/runs/weighted_congestion/cyclic_clone/independent_clock.json)保存参数、代码hash、运行环境及结果。两份代码不互相导入。有限核验不替代一般证明。
- 读取顺序为本命题身份→一至五节证明→[独立重构攻击](../../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md)→两份代码与冻结证据→第六节预算障碍与开放替代机制。若输入取自[循环窗口复制](cyclic_clone_improvement_cycles.md)，须先限制为实现环的两个动作，不能保留该旧Claim中的全部2^E策略。

三玩家旧正文曾把原六步环误简写成000→010→001→000；本次只修正叙述为010→110→100→101→001→011→010，原全状态表、286/267结论和Claim身份不变。

## 次数保持的精确架构边界

[三次固定基体证书](anchored_clock_degree_barrier.md)证明：即使独立调所有anchor0三元pair的非负degree≤3多项式，只要保留两条弱环边，指定环外状态仍稳定。这比统一δ预算大D的保守分析更强，但只限制明示固定架构，不反驳本稿允许提高D的一般定理，也不排除常数倍degree。
