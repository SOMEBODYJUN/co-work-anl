# 全局叶重数门槛 v2：只据 Exact 的独立重构

审查者 pcsp_occurrence。实际只读 `ternary_rainbow_multiplicity_threshold_v2_exact_statement.md`；读前、读后 SHA256 均为 `8e47cc088a50d6f8609c9dcbd11f142407229e7ef5c6171fdd6b3dc5a8b2c6a9`。未读或询问 root 的新 proof，未与其他审查者交换本次证明。

先验披露：我是无重数限制v1的作者，知道彩色AND/OR表达式的SAT归约与等高树编译。v1中的Rigid复制和全树单色Dead不满足新重数3合同，本稿不引用它们为自动证明。下面重新构造所有控制色，并逐类计算整个输出树的实际出现次数。root事先仅给新Exact，root自己已有证明不冒称root盲审。

结论：新Exact四项均可独立重构，无 standing fatal。重数2的存在性另有直接可构造证明；本稿只说明数学构造，未登记生产实现/运行。重数3的NP-hardness使用新的低重数构件，原atom色与全部辅助色的全局重数都≤3。

## 1. 重数2时总YES

给每个颜色的两次叶出现分别赋辅助桶0、1；若只有一次则任取桶0。于是每个桶内的原颜色均不重复。

任意两色叶着色的完整三叉树都有同桶full binary subtree：height0为其叶桶；自底向上，每个child已经有某桶binary witness，三个children中至少两者有同桶，选这两个children的对应witness。这一归纳保存完整深度，不是只找到路径。根所得binary subtree全部叶同桶，原色因桶内单射而rainbow。该推导对任意height有效。实际上给定显式树，记录两个child并traceback即可位多项式构造；Exact只声明存在性，因此没有实现夸张。

## 2. 低重数三叉构件

所有tree均完整三叉、叶统一深度。以下fresh指在**整个最终构造**中的新色，不与任何别的构件复用，除非明确写两条guard共用。

### Fresh_H

完整三叉heightH，每个叶一个全局fresh色。因此每色出现1次，任意binary pruning皆rainbow。没有要求每个witness使用同一color set，故不需要旧Rigid。

### Dead_H，H≥1

对最底层的每个internal parent p，其3个叶赋同一个私有fresh色d_p；不同p给不同颜色。每色在整个Dead_H中恰3次，且不出现在别处。任意full binary subtree在其某个active最底parent处选2叶，而二者同色，故绝无rainbow binary witness。这个构件不是把全树染同色；不同bottom triplets使用不同实际颜色ID。

### Must_H(g)，H≥1

要求每个rainbow binary witness必含g、至少一个witness存在，而且g在整个ambient构件只出现一次。

H=1时，三叶着色g,x,x，其中x为该构件私有fresh色。合法binary对必须含g及一枚x，所以g必含、出现1次，x恰2次。

H≥2时，三个child依次为Must_{H−1}(g)、Fresh_{H−1}和Dead_{H−1}，所有辅助色fresh。Dead不可选，故必须选前两child；归纳保证必含g且存在。g仍只在第一个child的一枚叶上，出现1次；其他色由归纳、Fresh和Dead分别有上界2或3。没有复制g到同构的其他branches。

这些构件每个都是显式完整三叉tree，且所有辅助色全局出现次数≤3。

## 3. 同等高的AND、padding和OR

初始彩色atom c编为Must_1(c)。原色c只出现1次；它的私有控制色x出现2次。

给两个heightH≥1的构件T,U，AND输出root三个child为T、U、Dead_H。因为dead不可选，rainbow binary witness必须用T和U，且两者颜色集不交。私有辅助色不会给不同构件意外制造冲突。若height不同，反复用AND(T,Fresh_H)升高较矮树，直到同高；padding只添fresh色和某些私有dead triples，不增加原有任何色的出现次数。

OR先将T,U补到共同heightH，取一个全新guard色g，分别建立Must_H(g)的两份实体构件：它们只有色g被刻意共用，其所有辅助色不同。用AND将T与第一guard相接、U与第二guard相接，得T′、U′，共同heightH+1，各rainbow witness必含g。新root三个child为T′、U′和Fresh_{H+1}。不能同时选T′、U′，因为g冲突；故必须选filler加两option之一。这精确实现OR。g在整个新ambient OR中恰出现2次（一option一次）；父层从不复用该g。

与v1相比，OR依赖的是Must只含g一次的性质，而不是高重数固定集合Rigid。其他私有padding colors允许随witness选择变化，不影响抹掉auxiliary colors后的原逻辑语义。

Height仍为atom1、AND=max+1、OR=max+2；所有padding只升到目标max，不改变此递归上界。

## 4. 标准3SAT归约及每个原色的精确次数

预处理任意显式3SAT编码：用实际出现的binary变量ID建dictionary，不按最大数值ID遍历。若含空clause，直接输出height1的三叶同色NO实例；若clause集为空，直接输出height1三叶互异YES实例。长度1或2的clause可重复其中literal补成3个occurrences，保持SAT且只增常数倍长度；每个新occurrence仍给不同ID。若另允许输入仅变量声明而无约束，仍按空CNF的YES分支处理。

非平凡实例有n个实际出现变量、m≥1个恰3-occurrence clauses。每个literal occurrence(j,l)给一个独有颜色c_{j,l}。对变量x_i的truth t，建立它所有取false的occurrence colors的balanced AND，若为空用一个私有neutral atom代替；变量子式为两truth bundles的OR。每clause子式为其3个occurrence atoms的binary OR。顶层对全部变量、clauses作balanced AND。

每个c_{j,l}恰在两个原atom中出现：一次在它的变量取false的那个truth bundle，一次在其clause的literal option。每个atom编成Must_1，因此c_{j,l}在整个最终树中**恰2次**。补短clause产生的是不同occurrence colors，不把三个重复literal误当同色三atom或更多。每个neutral atom色只出现1次。

按assignment选false bundles、每clause选一true literal，得到全体原色无冲突；反过来一份rainbow realization若选择false literal，则其颜色与所选variable false bundle冲突，所以每clause必须选true literal。这与v1的辅助语义同构，但实际树使用本稿低重数构件。

全局辅助色分类：

- Fresh_H的每色出现1次；
- Must_1内部x出现2次；
- OR共guard g在两份Must中各1次，总2次；
- Dead_H的每个bottom triple色恰3次；
- 所有以上类别/不同构件之间fresh IDs互不复用。

故每个原色、neutral色、guard、filler和dead控制色都真实满足≤3；没有把超重辅助色视为隐藏别名或不计费资源。

## 5. 高度、显式规模及NP成员性

false bundle的balanced AND高度O(log(m+2))；变量OR增加2，clauseOR常数层；顶层balanced AND增加O(log(n+m+2))。因此h=O(log(s+2))，其中s是实际binary编码长，n,m≤O(s)。完整三叉树顶点数(3^(h+1)−1)/2为s的固定多项式。

所有Fresh、Dead、Must、Pad实际展开，颜色个数≤实际叶数，依次分配整数ID只需O(log |T|)位。大binary变量ID已用dictionary消除伪多项式循环。重色triplet和guard都只有规定少量实体出现；没有通过共享DAG偷偷压缩指数树。

见证按active nodes的两个child编号写出，核root、统一深度、每active内点恰2child以及叶颜色distinct均位多项式。结合归约得重数≤3下NP-complete。重数≤2时所有输入YES，与重数3下有NO及NP完全共同给准确复杂性门槛；若声称无poly判定器才另用P≠NP。

## 6. 原P完全回算与范围

P与v1同一对象：internal private机器、每色一台resource；单端root pin time1；每树edge job parent time1/3、唯一internal child或叶色resource time1，其他∞。每个非pin job恰两端，root pin仅一端。

binary rainbow见证把选中edge jobs down，其他全parent，active internal负载1+1/3=4/3，inactive internal负载1，每resource最多1。任意实际C<5/3时，root unit使其active，每active node不能留2枚small，故至少2条down，递归选2得到binary subtree；外resource两枚unit将负载2，所以所得叶色必不同。任意单路径产生实际C≤5/3，故无binary rainbow时OPT恰5/3。

本归约中每resource的eligible叶jobs恰其全局leaf色次数，因此≤3；不能把其容量1重复复制。资源最多3个leaf jobs并不保证问题容易，因为原private tree内部路径长度随输入增长。

最终接受的是重数门槛及其5/4 UM比值锚点，不是∀δ大k编译。没有实现/运行或全球新颖性认证，没有UM主目标升级。到本稿冻结为止仅见新Exact，root proof尚未读。
