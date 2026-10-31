# 完整三叉树的二叉彩虹子树：独立陈述先行重构

审查者：boss11 内部 cover_consistency。实际只读 Exact `private_ternary_rainbow_binary_subtree_exact_statement.md`，SHA256 `3264ae3c3a2100fe0ef50aff1a729f9282346dba45059e20f9dcdc28d739563d`。冻结此稿前未读作者任何proof、其它review或pcsp目录，未向作者询思路；root未给本归约提示。已有私有树调度背景不等于已知本NP-hardness构造。

结论：能够自行给出确定性显式多项式3SAT归约，支持Exact的NP-completeness和原P推论，没有发现standing fatal objection。下面是本审查者的独立构造，不冒称与作者构造相同；不认证新颖性。本次没有代码实现/有限实验/Git/Work。

## 1. 固定palette的完整树bundle gadget

给一组恰2^t个不同颜色B，定义完整三叉高t树G(B)：t0为该色单叶；t≥1把B等分成非空B0,B1，三个child依次为G(B0)、G(B1)、G(B0)的独立树副本，副本颜色保持相同。

归纳性质：G(B)存在二叉彩虹子树，且其任一二叉彩虹子树的叶颜色集都恰为B。因为每个active child的子树本身彩虹，归纳其输出是B0或B1；第一、第三child输出均含整个非空B0，二者不能同时选。故必须选B1和一个B0，恰输出B。所有原叶深t，每内点3孩子，树大小Θ(3^t)。这允许在多项式显式树内强制一个固定的颜色bundle，尽管原树中颜色重复。

## 2. 两个通用逻辑组合

以下树均完整、等高；复制树时保留颜色ID。

**二选一。** A、B为高t的两个alternative树，且它们每个可能彩虹二叉子树都含一个相同lock颜色ℓ。令D=G(Dpalette)为高t fixed bundle，其全部颜色新鲜且不同于A/B所有潜在颜色。根放children(A,B,D)。任何彩虹二叉子树不能选A+B，必须D加恰一个alternative。其输出中D的任一指定颜色都是公共anchor。

**AND/合并。** A、B为高t树，且A的每个可能彩虹二叉子树都含某个anchor α。令新根children(A,B,A-copy)。两个A不能同选，故任一彩虹二叉子树必由B和一个A组成，等价于分别给A、B选择互不相交颜色的彩虹子树。它仍含α，作为下一层公共anchor。若A没有彩虹子树，这个陈述同样安全：A和copy均不能被选，输出也不可能存在。不同逻辑模块需跨模块约束时，直接用共享颜色来禁止它们同时出现。

不需要引入底层不可行“坏叶”：叶单独总是可行，使用共锁和固定bundle避免这个常见缺口。全局AND的A-copy与A即使选不同内部options，也都含同一anchor，仍不能绕开排斥。

## 3. 从3SAT构造等高变量/子句模块

先将有效显式3SAT输入中的出现变量重新编号，不按最大二进制变量ID创建空变量。标准3-literal clauses即可作为NP-hard源；若需要覆盖≤3-literal形式，可重复literal补成3个positions。每个literal occurrence e有单独颜色c_e，即使同一literal在同一clause重复也给不同occurrence ID。空clause直接映成固定NO树；空conjunction直接映成固定YES树，见第6节。

记输入编码长度s，取b=ceil(log2(s+4))，K=2^b。所有接下来需装入palette的specified colors至多s+2个；容量2K足够，较小clause palettes容量K也足够。用不同的新鲜颜色补齐每个palette，除明确要求共享的locks/c_e之外，所有fillers彼此不同。令统一模块高度H=b+2。

### 变量模块V_v

用高b+1、各含2K颜色的fixed bundles B_v,0和B_v,1。两者均含同一个变量lock ℓ_v；B_v,t另含恰那些在truth assignment v=t下为假的occurrence颜色c_e（只限这个变量的occurrences）。其余填新鲜颜色。第三child为高b+1 fixed dummy D_v，颜色全部新鲜。

以第2节二选一把它们放在根，得到高H完整三叉树。其每个彩虹二叉子树选择恰一个truth option，加D_v。D_v的一个私有颜色α_v是该模块每个输出必含的anchor。模块只在选择使某literal为假时，才输出该occurrence的c_e。

### 子句模块C_c

设该clause的三个occurrences为e1,e2,e3。取两个私有locks ℓ0_c、ℓ1_c，按下面构造高H的三选一：

- M2、M3是高b、各K颜色的fixed bundles；Mi包含c_ei和共同inner lock ℓ1_c。
- D1是高b fixed bundle，含outer lock ℓ0_c，余色新鲜，与M2/M3不交。
- R的children为(M2,M3,D1)，高b+1。inner lock迫其选D1加恰一个Mi；所以其任何输出都含outer lock ℓ0_c，且恰一个c_e2/c_e3。
- L是高b+1 fixed bundle，含c_e1和outer lock ℓ0_c。
- D0是高b+1 fixed dummy，全部颜色新鲜，与L、R所有颜色不交。最终clause根children(L,R,D0)，高H。

outer lock排除L+R，故根必选D0加恰一个L/R；若选R再由inner gate选M2或M3。正好得到选择本clause三个literal之一的语义。除所选occurrence c_e之外，其它全部输出颜色是此clause私有控制色/fillers。D0任一颜色α_c是所有输出必含的anchor。

此处L有2K叶色，R也由两个K叶色组合，故同高b+1；各gate三个children始终等高，未用不完整树或早停叶。变量模块和子句模块都统一为高b+2。

## 4. 合成单棵完整树并证明等价

将全部变量、子句模块排入一个balanced二元AND组合树；补足到N为2的幂，N≥max(1,n+m)，padding模块用高H fixed bundle，其4K颜色全部新鲜并带公共anchor。按第2节AND规则逐层组合：每个逻辑pair(A,B)用真实三叉根(A,B,A-copy)，完整复制A的结构与颜色。

得到一棵完整三叉树，全叶高度h=H+log2N。AND每层可抽取恰一个原逻辑A和一个B的输出，故全局二叉彩虹子树等价于为每个原模块各选一个局部输出、所有这些输出颜色互异；复制不会使原逻辑模块少选、多选或免费重命名颜色。

不同原模块的可能输出之间，除occurrence colors外没有共享颜色。对每occurrence e，其c_e只可能同时来自其变量的“令e为假”选项，及其clause的“选择e”选项。故：

- 若Φ可满足，各variable选该truth option，每clause选择一个true literal。没有clause-selected c_e同时出现于variable输出，其余控制色和fillers全私有，可组合成全局彩虹子树。
- 若有全局彩虹子树，从各变量模块抽取truth option、从每clause抽取被选literal。若被选literal为假，同一c_e会在它的变量和clause模块各出现一次，矛盾。因此每clause被选literal都真，所得truth assignment满足Φ。

同一clause重复literal、相反literal、任意变量occurrence数均不破坏这个推理：使用的是独立occurrence颜色。变量两个truth options之间允许共享自己的lock；它们绝不会同时选中。

## 5. 深度、完整显式size与颜色编码

n+m=O(s)，b=O(log(s+2))，故h=b+2+ceil(log2(max(1,n+m)))=O(log(s+2))。所有AND及bundle复制均构造真正完整三叉树，因而总node数恰(3^(h+1)−1)/2，是s的多项式；没有根据h生成超多项式隐式树。

可先生成O(n+m)个base palettes，每个最多4K=O(s+1)颜色，颜色总数O((s+1)^2)；复制仅重用已有ID。用顺序整数作为ID，所需位长O(log(s+2))。整个树和叶ID列表的编码长度仍多项式。对任一固定常用显式3SAT编码，可取一个保守绝对常数C（例如30）同时支配h≤C log2(s+2)和全部输出规模≤(s+2)^C；未依赖Φ内容调整C。

因此这确是确定性多项式many-one归约，不是只对不完整tree、增长叉数或指数height成立的归约。所有构造的“copy”都是多项式规模输出中的真实节点，不是oracle共享子图。

## 6. NP成员与小退化

见证给每个active internal node两个child编号，直到深h。可在完整输入大小多项式内检查prefix closure、root激活、每active内点恰2 children、全部叶深h和叶色ID互异。见证节点数不超过原T节点数，所以NP成员成立。

需要常量YES时，可给height1叶色(a,b,a)，存在二叉rainbow；需要常量NO时给height1叶色(a,a,a)，不存在。二者都是合法完整三叉树，非空显式颜色域，满足h≥1。标准非空3SAT源也可直接避开这些特例。只要tree有叶，任选root到叶一路给full1-ary subtree，故q≥1；q≥2当且仅当存在binary rainbow，q=3必能剪成2，所以区分q≥2与q1等价。

## 7. 明确原P的全部jobs与严格阈值

给定binary rainbow subtree，root pin固定root time1；其二叉子树内每active node恰2个出job下送child或该叶真实resource，其余1个出job留parent time1/3。每active machine收一unit（根pin、其它来自父edge），负载1+1/3=4/3。所有inactive原分枝全部出job留父，每machine恰3个small、负载1；external因彩虹各至多1unit。每个原job恰一次、资格和机器不变，得完整C≤4/3。

任意tree选择一条root到叶路径，全路径出job各下送1个、另2个留父，active负载1+2/3=5/3；其它分枝父置负载1，唯一外送叶使资源负载1。这给对所有输入的实际C≤5/3。

反向给完整实际σ且C<5/3。root已有pin unit；任何被选路径上收到unit的active机若留≥2个small，就负载≥1+2/3=5/3，故其至少2个出job确实下送。按固定顺序选其中2个，递归到原深h，得到full binary subtree。所有其叶job都已在external实际执行time1，而C<5/3<2保证一个资源不可能放两枚这样的unit，所以叶色互异。提取只需遍历实际树及σ，多项式。

若不存在binary rainbow，以上排除一切C<5/3调度；通用路径上界又给OPT≤5/3，故真实OPT=5/3。YES只声称OPT≤4/3，不要求等于4/3（全三叉rainbow等特殊输入可能OPT1）。

UM矩阵的机器、jobs和全部finite ends均是tree/颜色数的多项式，若按dense矩阵列∞也仍多项式；时间只1/3、1，每job至少一finite端。无需任何零值或概率对象。本归约给(4/3,5/3)promise NP-hardness与5/4的间隙比，远未给near2困难性，不升级为UM-TARGET-v1反面。

## 状态

本稿是实际Exact-only阶段的独立完整归约和原P数学审查。依赖标准3SAT NP-completeness；未引用其它彩虹/Steiner问题的不同目标困难性，也未审作者构造。正确性审查与原创性、实现及成文价值分别保留。
