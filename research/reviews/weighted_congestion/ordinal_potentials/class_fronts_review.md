# 循环窗口前沿商与不同步反例的独立重构及攻击

**最终范围结论。** 原freeze遗漏“每类参与test”时，恰商数只对带标签bit成立；缺席类的空/空动作在MODEL会合并。入库初次登记v1前已加每类覆盖、保留零系数资源的假设，并由独立审查重新确认合法域；该实质对象遗漏及修复详见末节，修复后scope PASS。

## 循环窗口 lift 的扭转平移对称性与前沿相位商：独立重构

本稿在未读作者 newfront 草稿或冻结证明前，仅由精确 statement、MODEL 及现行 cyclic_clone_improvement_cycles.md 第三节重构。仅讨论原有两个动作的 lift；类数 M>=1，每类 N>=2 名同权 clone，测试 t=(a,b,K,o) 满足 a!=b, 1<=K<=N, o in {+,-}。每个 t 的 2N 个资源 (t,j,s), j in Z/N, s in {0,1} 具有相同费用函数 c_t；不同 t 可任意不同。所谓“pair 费用相同”须同时包括两个 side，才保证 wrap 时 side 交换。证明不要求 w_a>=w_b。

## 1. 逐资源的 incidence 恒等式

令全序位置 l(a,j)=Mj+a，r(j)=1[j=N-1]。测试的 heavy clone h=(a,j)，light window 为 (b,j+delta+k mod N), k=0,...,K-1，delta=1[a>b]。记 epsilon_t=0 对正向、1 对反向。动作零的资源 side 写为

- heavy: f_h=0；
- light u in L_j: f_{j,u}=1[l(u)>l(h)] xor epsilon_t。

实际使用 side 是 f xor 玩家动作 bit。定义 pi(a,j)=(a,j+1 mod N)，并定义

(Ts)_{pi(a,j)}=s_{a,j} xor r(j),
T(t,j,v)=(t,j+1 mod N,v xor r(j)).

窗口的参与者由 pi 双射到下一个 heavy 的窗口，因为 delta,K 固定，而模 N 平移保留集合。对 light，线性端点换位的唯一作用是

1[l(pi u)>l(pi h)] = 1[l(u)>l(h)] xor r(index u) xor r(j).

理由：恰一个端点处于最后 block 时相对先后翻转；两者都在最后 block 或都不在时相对先后不变。同 block 时类次序也保持。因此

f_{j+1,pi u} xor (Ts)_{pi u}
 = f_{j,u} xor s_u xor r(j),

恰为资源侧的 T 映射。heavy 的恒等式直接由 f_h=0 和自身 bit 翻转得到。orientation 只加同一个 epsilon_t，故两方向均成立。这证明所有动作状态中的资源参与 incidence 协变，而非只沿指定更新词成立。

pi 保留权重，T 保留每个资源费用函数，故每个资源负载和每个玩家成本协变：C_{pi i}(Ts)=C_i(s)。单方 flip F_i 与 T 满足 T F_i=F_{pi i}T，因此对任何 alpha，

C_{pi i}(Ts)-alpha C_{pi i}(F_{pi i}Ts)
 = C_i(s)-alpha C_i(F_i s).

所以 strict improvement、非改善、等号与 PNE 都沿 T 保持。

## 2. 前缀/后缀 front 的唯一相位

对 x in Z/(2N)，定义 f_x(j)=1[(x-j-1 mod 2N)<N]，j=0,...,N-1。

- x=k, 0<=k<=N 时，bits 为前 k 位 1、后 N-k 位 0；
- x=N+k, 0<=k<=N 时，bits 为前 k 位 0、后 N-k 位 1。

相同的端点是 x=0=2N 的全零和 x=N 的全一。去重后正好 2N 个 front，且编码唯一。T 在一个类上满足 f_x -> f_{x+1}：j>=1 时由相邻 residue 直接得证，j=0 时由新 bit=1-f_x(N-1) 得证。因此在 M 类 front 上，T 同时使每个 x_a 加一。

对任意 k=0,...,N，沿 x -> x+k 的路径恰翻动 k 个不同 clone，每步 clone index 为当前 x mod N，故 Hamming distance 为 k；更长 phase 差用反向较短路。因此

d_H(f_x,f_y)=min((y-x mod 2N),(x-y mod 2N)).

N>=2 时，恰一个 bit 改变且仍是 front，当且仅当 y=x+1 或 x-1。正向改 clone j=x mod N，反向改 j=x-1 mod N。不能把某一类视作允许任意 x 跳跃的玩家。

## 3. 精确商空间及其真正边

T 的阶为 2N，T^N 全局补 bit，T^(2N)=Id。front 上对角加法作用自由：若任意 x_a+k=x_a，则 k=0 mod 2N。每个 orbit 因而恰有 2N 个代表；唯一用 T^(-x_0) 归一化为 x_0=0。坐标为 y_a=x_a-x_0, a=1,...,M-1，总数 (2N)^(M-1)。

归一化后的合法单 clone front 边必须保留 mover class 与 +/- 标签：

- a>0 的 +/- 边只使 y_a 加 +/-1；
- a=0 的 +/- 边使所有 y_b, b>0，同时减 +/-1。

这只是坐标重选，原 lift 每条边仍由某一 clone 的单方两动作切换实现。不同标签可投影到相同商边，M=1 时全部投影为自环；不能因此删掉 move label 或引入任意 phase jump。成本/gain 逐玩家协变保证归一化代表的边符号与任意原代表一致。

## 4. 范围限制

商空间精确编码 front 子集及其内部单 clone 边。它不声称所有严格改善都留在 front，不声称 front 内汇点是原两动作游戏 PNE，也不把 class 的 N 名玩家合并为策略为 2N 个 phase 的博弈玩家。一般没有理由将 off-front 偏离视作非法。

## 压缩前沿冻结稿的独立攻击记录

审查对象 `/workspace/scratch/ecf05625b47b/directed_clock_budget/compressed_class_fronts.md`，SHA256 `499a714c84c3b4b579c40575b1b329751f079fa958bc02e20d8db10da3919f06`；其审计 source SHA256 `432b5da4c9fc98c7b6fbde4aaf01f56a6c1b8a36847afbff986bf886c381f013`。独立审查稿与 literal 实现已先于读取上述作者稿完成。没有更改 repo、冻结作者稿或作者证据。

## 1. 判定与量词

未发现命题 A、前沿商、单测试费用表、条件式同权时钟 lemma 或给定12玩家反例的实质错误。以下论证不靠作者157248条有限断言。原 sweep 含改善环不能推出每个类 front 状态都有改善端点；小例严格反驳这一普遍命题。小例不是 alpha-PNE、不是无 alpha-PNE 构造，也不是所有类内时钟机制的不可能性证明。完整策略域仍须为原两动作；若扩大到 2^E 则会引入空策略及更多 off-front 偏离，本文不处理它们。

费用同费条件的精确性：同一测试全部 j 与两个 side 必须共享同一个资源费用函数，或更一般地费用须满足 generator 对资源的映射等式。只说每个 j 上资源 pair 的系数不随 j 变、却允许两个 side 不同，不能保证跨 wrap 的 side swap 保成本。作者写明“一对同费”“所有N对相同”，满足强条件。测试非负叠加、不同测试费用系数不同、某测试系数为0 均无问题。heavy/light 只是 role；证明未用 w_a>=w_b。

## 2. 全状态协变与商

独立稿已给出逐 incidence 证明。关键比较位等式对 a>b、同 clone index 和单方 wrap 同样成立；额外 orientation 异或抵消，T F_i=F_(Ti)T，故当前成本与偏离成本逐玩家完全协变，不只是沿 sweep。模型成本不乘权不会制造额外比例；即使采用逐人乘权，clone 保权同样成立。

front 是2N个互异 bitvector；T 在所有类 phase 上加1，作用自由，故商恰有 (2N)^(M-1) 个点。作者“最多”可加强为“恰”。class0 forward 同减全部相对坐标、backward 同加，作者已正确保留。须保留 move class/direction 标签；例如 M=2 时不同动作可能投影到相同商边，但不是任意 phase 跳跃。所有 front 内单 clone 动作恰为 phase +/-1，这个断言 N>=2 即成立。

## 3. light 成本公式的解析核查

最值得攻击的是 light 公式中 K-k 和 k+1 的方向。把 mover 类 b 的 phase 归零后，所有 b clone 的 bit 都为0。令 mover 为 b0，考察其第k个参加窗口，k=0,...,K-1；heavy index h=(-delta-k) mod N。窗口第t位 light 的 index 为 (t-k) mod N，t=0,...,K-1；mover 正是 t=k。

若 a<b，delta=0：k=0 时 heavy 是 a0，所有窗口 light 都在线性顺序之后，故全K人同侧；k>0 时 heavy index N-k，t<k 的 light 在线性顺序之后，t>=k 的 light 在线性顺序之前（包括 mover0）。因此与 mover 同侧恰 t>=k。

若 a>b，delta=1：heavy index N-1-k。t<k 的 light index N+t-k 严格在 heavy 之后；t>=k 的 light index t-k 至多为 heavy index，等号时类 b<a，故仍在线性顺序之前。mover 也在 heavy 之前。因此与 mover 同侧仍恰 t>=k。

orientation=- 只把本窗口的所有 light side 同时补位，不改变 light 之间是否同侧。故两方向和 K=N 的端点都给当前 K-k 名 light、翻位后 k+1 名 light。heavy 当前使用 side B_r(h)，mover 当前 side sigma_k，故当前同侧指标恰 e_k=1[B_r(h)=sigma_k]；翻位后变为1-e_k。由此作者 old/new 两式逐项精确，而不是仅multiset或期望恒等式。

对任意 mover phase x，T^(-x) 可将其 phase归零并把 forward mover送至clone0，另一类 phase为r。backward 从当前x到x-1，等于前驱状态的 forward 边反向；前驱相对phase为r+1。因此 old=Q(r+1)、new=O(r+1)，不能取 forward margin 的负值。作者写法正确。

p=0 时所有参与资源的当前/偏离后负载都至少含正的 mover 自重，无0^0边界；费用均为1，heavy贡献1、light贡献K，old=new，公式仍真。任意 nonnegative polynomial可逐单项式相加；几何本身并不依赖p。

## 4. 同权 clock 的准确适用范围

三人 side 映射为 (b0,1-b1,b2)，完整触发恰 bits010/101。其他bits将三人分成2+1。若一个单 bit flip前后均非完整触发，mover不可能从 singleton 出发（否则翻后触发），所以当前与另一人共享，old load=2w；翻后加入原singleton，new load=2w。每个这样的同费pair贡献 c(2w)-alpha c(2w)=-(alpha-1)c(2w)。有限非负叠加可直接相加，不要求单项式、单调性或正费用；c(2w)=0和constant费用均覆盖，alpha=1时贡献恰0。

“任意”只能量化到每一 front 边的两个端点都不触发的 clocks。原锚定架构采用按类线性index排序的三元(0,i,j),0<i<j；prefix/suffix 在任何递增三元上最多一次变位，故条件满足。这个事实甚至允许任意递增index三元，不必相邻。若把同样三人乱序、或按rawbits作循环wrap三元，front可触发010/101，此时不能套这个结论。作者称“类内锚定时钟”时应明示原架构或给出上述排序条件，以免自包含量词被误读。新增clock无法给front内原先非改善的端点创造改善，但可能改变off-front出口，完全没有排除锁定后产生PNE或其他机制解决问题。

## 5. 小例的独立 literal 证据

先于读取作者稿，独立按资源pair及两动作集合建24个资源，Fraction重算负载，核验：

- 24步原同序双轮全部strict，回到原状态；
- 全4096个两动作states的逐玩家cost/gain协变；
- 全512 fronts的T相位迁移与front内单clone邻居恰phase +/-1；
- 给定实际系数乘max(P,Q)精确为19/100,1/3,143/300；
- x=(0,4,0)六个端点margin全负，分别约-0.248843,-0.181355,-0.493575,-0.493575,-0.305171,-0.801416（每类forward,backward）；
- class0内部clone1、2的margin分别约+0.245849,+0.253423，确实不是PNE。

独立实现与完整分数见同目录 `independent_literal_audit.py/json`。代码未导入作者程序、仓库或压缩费用公式。

## 6. 建议的轻微文字修改

1. §1的“N=1、2时允许这两个邻居重合”改为“仅N=1时两邻居重合；N>=2时两邻居互异，且它们恰为全部front内单clone动作”。N=2的front为整个二维cube，forward/backward绝不重合。
2. §2“最多保留”改为“恰有”，并添一句对角phase平移作用自由的理由。
3. §4明确clock采用同类线性顺序递增三元（原锚定形式(0,i,j)），或直接将“每条front边两端均非触发”列作假设。不能泛化到任意乱序或raw cyclicwrap三元。
4. 全文声明p为非负整数、alpha>=1，与MODEL对齐。

## 7. 复放与补充独立遍历

作者冻结 audit 重放完成：157248 条 Fraction 断言全部通过，输出 source hash 与冻结 hash 一致。重放输出保存在 `author_audit_replay.json`。

补充程序 `independent_front_and_clock_attack.py/json` 使用审查者自己的 literal resource 实现（不调用作者 endpoint 表）遍历512个 fronts，独立复得恰8个稳定front，即 (t,4+t,t) mod8。另对同权clock的全部12条有向“前后非触发”边核验old=new=2w；这只是对前述一般论证的边界检查，不替代一般证明。

## 入库版本与代码整合合同

现行正文为[循环窗口前沿商与不同步状态](../../../current/weighted_congestion/class_front_phase_quotient.md)，两个新ID分别登记一般表示和出口反例。主研究者按上述建议只修N=2措辞、商数为恰、时钟递增三元的非触发假设，并补精确身份和路径；未加强为PNE非存在或任意clock障碍。作者代码原样迁入`tests/audits/weighted_congestion/cyclic_clone/verify_class_fronts.py`。独立代码由本审查的两份literal程序合并成`tests/audits/weighted_congestion/cyclic_clone/independent_class_fronts.py`：数学输入与检查不变，去掉向源码目录隐式写JSON，改为stdout，加入后续独立512front稳定集及12个clock边检查。规范运行结果在`evidence/runs/weighted_congestion/cyclic_clone/class_fronts.json`及`evidence/runs/weighted_congestion/cyclic_clone/independent_class_fronts.json`，保存新源码hash/环境/命令；原文中的同目录旧hash均只标识先前freeze。

# 类前沿一般表示与反例的规范整合复核

本次仅只读核对仓库，未更改repo、冻结证据或执行Git/公屏动作。

## 1. 来源与原有结果保真

规范正文：`research/current/weighted_congestion/class_front_phase_quotient.md`。
规范审查：`research/reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md`。

前述独立预读重构和冻结攻击已在规范审查中完整拼接；N=2邻居互异、商状态数为恰、clock按递增index锚定三元及非触发条件均已落实。没有引入class任意phase偏离，没有删除class0边，没有升级为PNE非存在或所有clock机制不可能。

作者审计 `verify_class_fronts.py` 的SHA256仍为 `432b5da4c9fc98c7b6fbde4aaf01f56a6c1b8a36847afbff986bf886c381f013`，与原冻结source逐字同一。规范`class_fronts.json`内的result与本审查者先前重放的JSON完全相同，仍为157248条断言。

合并独立审计 `independent_class_fronts.py` 的SHA256为 `7a7f6a2a22a89d0eea38333d06ab0baa655f34fdf45d189c5ee2e5dc151dbe20`。逐字比较确认原literal主体数学代码保留；补充stable/clock loops仅将原模块命名空间`m.front/m.margin`改为同文件本地函数。已删除隐式向源码目录写JSON，改stdout。规范独立证据的result对原literal JSON每个字段完全一致；新增8个稳定front列表、12条clock边数量与load字段均与原独立补充JSON相等。代码与两规范run记录的source hash相符。没有把有限audit当作一般证明。

## 2. 新发现并修复的一般域假设

最终整合核查发现原冻结稿确有一个MODEL层面的退化遗漏，不能仅称“无实质错误”：任意有限测试集可能完全不涉及某一类，故该类所有clone的动作0/1都给出空资源子集。在MODEL的策略族 S_i⊆2^E 中，这两标签实际是同一个策略。

具体地，m=3,N=2而只有test(0,1,1,+)时，类2缺席。三个类的labeled bit前沿商仍有4^(3-1)=16个，但互异MODEL纯前沿只涉及类0、1，真实T商只有4个。因而原freeze的“恰(2N)^(m-1)”若读作互异MODEL纯状态数，假设不足；它原本只严格成立于保留0/1标签的bit-profile表示。逐incidence协变和单test费用表的代数恒等本身不受影响。

修复方式是将一般Claim的合法输入域收窄为：每一类至少参与一个test，且系数为0的资源pair仍保留为不同资源。类a作为distinguished角色时，其每个clone有自己的pair；作为window角色时，每个clone恰属于K>=1个pair。因此每名玩家两个动作均非空且互不相交，必为不同策略；bit profiles与MODEL纯状态一一对应，phase编码和精确商数即可按原证明成立。

严格逐类改善的原Gz>0输入自动满足coverage；12玩家反例也每类参与，故其数学输入、24步循环、六端点稳定及两内部改善均不改变。这是首次登记v1之前由审查发现并显式修复的域假设，不是对既有已发表身份的静默范围修改。

最终read-only复核已确认规范正文首个Claim及第1节明确写入每类参与至少一个测试、保留零系数资源、保证非空互异两策略，以及缺席类单test表仅为代数子项。该修复充分排除上述MODEL退化。

**Scope PASS。** 前述一般证明与独立冻结攻击适用于当前收窄后的规范v1域；代码合并和证据迁入未改变数学输入或检查。此PASS明确包含“原freeze缺coverage假设已由审查发现并修复”的记录，不追认原未覆盖域的真实纯状态精确计数。规范review与账本应保留该objection/fix历史。
