# 全局叶色重数2/3门槛：root冻结证明

绑定Exact SHA `8e47cc088a50d6f8609c9dcbd11f142407229e7ef5c6171fdd6b3dc5a8b2c6a9`，ID `UM-PRIVATE-TERNARY-RAINBOW-MULTIPLICITY-THRESHOLD-v2`。root在已读原v1作者/独立证明，以及literal提出有界重数分组机制后独立加强此NP源。root不是盲审。此文在给pcsp仅Exact后、未收到其本次重构反馈前冻结，不给该审查者直到其独立稿冻结。

## 1. 重数2全部YES

把同色至多两个occurrences分别放入叶类A、B；每类本身rainbow，允许空类。已证raw q对子集并子可加，q(L)=3，所以3≤q(A)+q(B)。整数性保证至少一个类q≥2，其满二叉子树自然rainbow。任意height均有效，不借固定height枚举。q子可加性可独立按height归纳：若Q=q(A∪B)>q(A)+q(B)=a+b，在支持Q的Q个孩子中，至多a个孩子的A值>a，至多b个孩子的B值>b，故有孩子两值各≤a,b，与孩子归纳Q≤a+b矛盾。h1为叶计数。

## 2. 全局重数3的dead与固定palette

修改原v1的Dead：D_H，H≥1，为完整三叉高H树；对每个深H−1的父节点，给其三个叶同一全局新色c_v，且不同父节点及不同dead构件的c_v全部不同。每色恰3次。任何满二叉高H子树在末层必选同一父节点的两个同色叶，因此没有binary rainbow。不能在H0调用dead。

固定palette构件R_H(S)，|S|=2^H，所有S内颜色不同。H0为单叶。H1设S={a,b}，三个叶(a,b,a)，必选b与一个a，任何binaryrainbow叶色恰S。若S含一个指定的protected颜色p，则在H1将它放b位，使其实际出现恰1次。H≥2时，把S等分A、B，三个children为R_(H−1)(A)、R_(H−1)(B)、全局新色的D_(H−1)。若p指定，递归传给其所在的唯一A/B子树。两个palette孩子各出现一次，dead无binaryrainbow，故任何binaryrainbow必选A与B且色集恰S；这种选择存在。每个palette颜色实际出现1或2次，protected p恰1次；所有dead辅助色恰3次。R内的dead色与S及全部其它逻辑构件颜色全局不交。

以上不是用旧(A,B,A-copy)的palette递归，该旧递归会让颜色重数随height增长。新构件上层只各用A、B一次，以dead代替重复A；最底H1仍合法，protected位置可以保证某个共享色不重复。

## 3. 不复制逻辑子式的AND/OR编译

沿用已完整证明的v1中间彩色表达式：每literal occurrence e的原色c_e出现在变量的false branch atom和其clause literal atom恰两处；空false bundle用fresh neutral atom。变量恰选truth branch、clause恰选literal，所有逻辑模块由balanced AND组合。该中间realization rainbow iff SAT。逻辑表达式是树，任何子式只被使用一次；不要把它编成共享DAG或复制子式。

Atom(c)现在编R_1({c,p})，p全局fresh，且protected c取单出现b位；于是本atom中c实际一次，p实际两次。非空短clause可重复literal补三positions，但这些positions仍给不同occurrence色；每色c_e仍在上面两atom位置各一次。所有原色在整个输出中最多2次。

AND(T,U)：先用下面Pad补到共同H≥1，新root children(T,U,D_H)。选中binaryrainbow不能走dead，必须T与U，保持原语义且不复制任何子式。Pad(T,H*)每次以AND(T,R_H(S_private))升高1，新的palette全部fresh；该次AND两输入同高，故不会互递归。Pad只增加fresh色，T本身出现一次。

OR(T,U)：先Pad到共同H≥1，取fresh guard g，分别取palette S_T,S_U，各2^H色且交集恰{g}；其它色全局fresh。用新R_H(S_T),R_H(S_U)，两份都将g指定protected，所以g分别只出现一次，总重数2。T'=AND(T,R_H(S_T))和U'=AND(U,R_H(S_U))高H+1。OR新root的第三child是R_(H+1)(S_F)，S_F全fresh。每option的每个binaryrainbow必含g，不能同时选择两option；必须fresh filler加一option，精确OR语义。全root没有复制T/U。

全局辅助色命名规则：先占住原occurrence/neutral颜色ID，再从不交namespace逐构件新分配；只有一个OR的两guard共用同一个g。每palette构件的dead部分用独占新色，不重用别的构件aux。于是逐类统计整个最终T：原occurrence c_e恰2（或≤2），neutral原atom色1，atom私有p2，每OR guard g2，每其它palette色1或2，每个dead底层色3。没有颜色超过3，所有控制色也已计入，不是别名免费复制资源。

## 4. 完整性、NP、size与原P

所有构件完整三叉、全叶同深；Atom高1，AND=max+1，OR=max+2，Pad只达max。中间表达式各false bundle及顶层AND balanced，clauseOR深≤2，故logicalheightO(log(s+2))，输出hO(log(s+2))，完整节点数(3^(h+1)−1)/2为固定多项式。R和D均显式展开，颜色数≤叶数，整数ID位长O(log|T|)。实际出现的binary变量ID可排序重编号，输入空/常量SAT直接给height1(a,b,a)YES或(a,a,a)NO；均全局重数≤3。构造时间按显式输出多项式，没有hidden exponential tree。

新R仍强制同一palette，新D仍无binaryrainbow，其余AND/OR/Pad语义与v1一一相同，因此SAT iff存在binaryrainbow。全局≤3限制在所有YES/NO输出都成立。给定binary subtree可多项式核验颜色单射，故受限问题在NP。标准3SAT源给NP-hardness，合起来是NP-complete。

转换原P完全沿v1明确矩阵，未更改times/端点；所有叶色全局≤3使每resource machine至多有3个eligible leaf jobs（仍不同原job）。Root pin单资格，其余各父1/3与唯一下端1。给binaryrainbow时activeunit+一个small=4/3、inactive原jobs父置1、外机≤1；给actualC<5/3时每active节点至少2down、每外机至多1unit，递归提取binaryrainbow；任意path给完整C5/3。因此NO恰5/3，YES≤4/3，仍只有5/4比值，非near2。

无软件实现、有限运行、新颖性、外审或独立成文价值认证。全局重数2/3的sharp复杂性边界是限定树源结果，未升级UM-TARGET-v1。
