# 坐标切片v3私有输出padding：新增陈述独立重构

实际只读新增Exact `direct_q_coordinate_slice_counterexample/coordinate_slice_private_output_padding_v3_exact_addendum.md`，SHA256 `8abe3bf7eb704ad41acfffae69ed0f0fd1eb1a824fb9b0216698815c455331d7`，未读其证明、canonical或询问其他研究者。v1两阶段与v2新增陈述重构已另冻，本稿不改原稿。以下只审新增E–G；没有外部认证。

## E：padding保真和位规模

H中每个左点a的每个右邻居贡献至多D−1个其他左点，故deg_H(a)≤D(D−1)。按给定顺序贪心可在s≤D(D−1)+1色内proper coloring；对固定b的D个左邻居两两相邻于H，故其颜色全异。显式构造H所需至多对每个b枚举D(D−1)/2对，时间O(nD²)再加常规查重/贪心，在显式输入长度的多项式内。

旧字母与所有新符号严格互异。因此一条新游戏边的任何覆盖只能来自：(i)旧左标签映到旧右标签；(ii)新左标签映到右p_(chi(a))。把新列表限制到旧字母所得列表总代价≤gN，故(i)覆盖的边总数<rho0 M。把尚未归(i)的覆盖边归(ii)。固定右token (b,p_c)，proper coloring使b至多一个邻居a有chi(a)=c，所以该右token最多向一条边收费。于是(ii)边数≤右侧p token数≤新列表总代价≤gN。合计严格小于rho0 M+gN=(rho0+2g/D)M≤rhoM，严格性没有在末步丢失。无需收费每枚左dummy，也不把不同顶点的同一符号合并为一份成本。

旧perfect YES仍用旧单标签、原投影未改故保留。原图未改所以simple、regular、balanced均保留；新映射对共同新字母表每一标签都显式定义且值仍属该表，故为全投影，但不一定满射/均匀纤维，未声称这些附加性质。Σ′大小Q0+1+s≤Q0+D(D−1)+2。

padding不根据g、rho数值大小做循环；仅添加O(D²)符号并列举输入边及新符号。显式原图有D≤n，故即便D二进制给出，这也是统一bit-poly变换；处理条件只需有理数精确比较。

## F：任意padded源上的完整(D−1)分叉证书

所有玩家均选新增原始状态alpha*。沿(a,b)，记c=chi(a)，i为a在b的局部邻居index，则固定坐标是x_(p_c)=i。对每位玩家根层任选D−1个邻居（例如输入排序前D−1个）。在每个被保留b分枝上，按既定坐标次序逐层指定D−1个孩子：

- 对其他邻居a'≠a所用坐标p_(chi(a'))，删去该邻居在b的局部index i(a',b)；
- 对不属于上述坐标且非本玩家固定坐标的任意自由坐标，删去任意一个值，例如D。

proper coloring保证其他邻居的p坐标两两不同，且与本玩家固定坐标不同，因此每坐标只删一个值，没有互相冲突的双删。每层都恰有D−1孩子；首层也是D−1，故深Q′完整(D−1)叉结构成立。

若同一资源(b,x)由两位不同相邻玩家a,a'使用，a'的切片给x_(p_(chi(a')))=i(a',b)，a的自由坐标规则却禁止这个值，矛盾。不同b天然不同块，同一个状态树的叶映射单射，故所有叶资源两两不交。不同左点若颜色相同，它们不共享右邻居，因此不会在同一b资源块相遇，这正是H coloring所需而非全左点不同色。

按v1已审的全任务规范：selector到alpha*根；所有保留树弧下传，其余全部弧留父。保留内部节点unit入+一枚small留父为1+1/D；所有未保留/未选状态内部节点Dsmall为1；资源至多unit1。无其他任务，所有资格合法；完整实际C≤1+1/D。

## G：两种精确最优值

若旧源为E的NO，则新源任意cost≤gN列表覆盖<rhoM≤M，因此不可能有perfect单标签（其cost=N≤gN）。v2 strictP1⇔fullLC给P无C≤1。实际负载1/D网格和F上界合并，OPT恰1+1/D。

若旧源perfect YES，则E保留perfect YES，v1实际σ给C1，selector单位任务给OPT≥1，故OPT恰1。

## Scope/复杂度攻击结论

E–G均已独立重构，无fatal objection。固定D,Q0,g,rho0,rho时，颜色数上界为常数，可补无使用颜色使Q′固定，再对原n点图展开是原图大小的多项式；新dummy均映实际chi(a)，补空颜色从不进入投影像，故不会增添新覆盖策略。D/Q0变化时D^Q′不是uniform原输入poly，正文已明确；无需从E的poly padding错误推得整个坐标树编译poly。

本版确比单个显式NO游戏的v1范围强：保留源promise的padding足以令这个明确compiler一律近1。但没有据此导入未经核的simple fixed-degree/alphabet hard源定理；没有覆盖额外纤维正则性被要求保留的归约，也不排除其他叶排列/资源设计。没有把v3作为一般UM的困难性或算法结论。

未读作者v3证明或canonical，未执行程序；上述均是一般数学重构，不把有限测试当证明。
