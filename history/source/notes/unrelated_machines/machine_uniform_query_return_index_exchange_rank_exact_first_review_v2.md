# 逐机统一时间 query/return 交换：rank 的独立 Exact-first 审查 v2

审查者：rank_deficiency_fee，2026-10-18。此记录只据新 v2 Exact 独立重构。尚未读取 v1/v2 作者 Proof、root 或其它 agent 的本候选推导。此前 v1 Exact-first 记录原字节不变。仅写 clone 外 scratch。

## 1. 实际读取对象

`/workspace/scratch/038d9dcc4cac/machine_uniform_query_return_index_exchange_exact_v2.md`

whole-file SHA256：

`f80c3b9cb7a8b0d3b3b8b0d553426659a036543a1fe9640fbb79a5d3502e20bf`。

认证范围：新 Exact 的逐机统一非负处理时间域、strict 模式交换、实际构造算法、weak B 合同推论、完整 outside-private 测试封装和位复杂度。不是所有同机异权 UM、fullformula 或真实共享 outside 端的全局可行性定理；不认证全球新颖性。

## 2. 容量化与所有退化分支

原任务宇宙 E=A∪Q∪R，三类互斥、族内身份不同，总数N=|A|+2k≥4。T>0。每内部机h所有finite原端同为s_h≥0，资格可任意；s_h可以跨机不同。定义

    c_h=min(N,⌊T/s_h⌋)  当s_h>0，
    c_h=N                当s_h=0。

对任意任务子集Y⊆E及其具体内部执行目的地，h上负载恰n_hs_h，n_h是该机原任务数。若s_h>0，负载≤T等价n_h≤⌊T/s_h⌋；又n_h≤N，故等价n_h≤c_h。若s_h=0，任意n_h≤N均负载0；容量N精确允许全部可能原任务数。没有除零。

若s_h>T，则c_h=0，strict 调度不能使用该机任何有限端；删除这行的slot不改变strict模式。允许机器没有finite资格、c_h=0或整个H为空。空H时每aligned模式含k≥2件边界jobs，故不可行，条件命题为空真；不提供见证的算法可可靠报告。测试封装仍有2k台outside机器，不形成零机普通UM。

容量截断没有改变任意子集Y的strict实际可行性，而不只保留论文列出的模式。它使用真实宇宙N；不得将未截断T/s_h的数值当成输出规模。

将h换成c_h个**证明/算法用虚拟slots**，每个原job对h有finite资格当且仅当它邻接h的全部slots。这样内部模式strict可行恰等价存在覆盖其原jobs的matching：

* 从实际strict调度出发，按任意确定顺序将同机jobs注入不同slots，因n_h≤c_h可行；
* 从slots matching出发，把每枚job投影回其slot所属的原机器，同机job数≤c_h，故原实际负载≤T。

Slots只表示同机统一耗时产生的真实整数容量，不是复制原任务或添加真实机器。最终输出仍是原jobs在原H上的目的地。s_h=0允许多个jobs同机是普通UM的合法零负载，投影同样成立。

## 3. 独立的交换证明与 rank 范围

在上述slot资格图的job侧取transversal matroidN₀。固定不同i,j，设

    C=A∪(R\{b_i,b_j})，
    x=q_i，y=q_j，u=b_i，v=b_j。

Aligned_i、aligned_j实际strict见证分别给C∪{x,v}、C∪{y,u}独立。因此C独立，可收缩。在N₀/C中，{x,v}及{y,u}均独立，u,v均非loop。

Inactive在T不可行正是{u,v}在收缩后不独立。两个非loop组成依赖对，故它们平行且closure相同。由{y,u}独立推出{y,v}独立；否则y∈cl(v)=cl(u)矛盾。同理由{x,v}独立得{x,u}独立。

还原到slot图再投影到原H，恰给mismatch(j,i)、mismatch(i,j)的全部指定原jobs峰≤T实际调度。证明适用于所有i≠j；若全部aligned可行且inactive不可行，逐对得到全部k(k−1)错配。

这里没有假定原容量全满、两见证占同一组slots、|H|或Σc_h有某个特定值，也没有假定任一任意大集合是base。收缩C后可选用秩2截断，因为已有两元素独立见证，截断不改变这里所有大小≤2的独立性。原机容量截N与这个matroid秩截断是两种不同操作，前者来自宇宙最多N件job，后者只可作证明语言；均不改变所用模式的strict可行性。

## 4. 实际二选一构造，不用 inactive 承诺

给两份任意aligned实际strict内部调度，先各自注入slots，得到M_i覆盖C∪{x,v}、M_j覆盖C∪{y,u}。从M_i删除x的matching边，保留M覆盖C∪{v}。

先从未匹配y进行交替增广搜索。

* 若成功，翻转路径得到覆盖C∪{v,y}的matching，投影给mismatch(j,i)峰≤T。虽然可能移动任意多辅助原jobs，但全部C和v仍各匹配一次。
* 若失败，在job集合C∪{v,y,u}上，M大小|C|+1，而M_j是大小|C|+2的matching。因此M不是最大matching，存在增广路。仅y、u未匹配，y起点已证无路，故有u起点增广路。翻转后得到C∪{v,u}的matching，投影即inactive峰≤T。

未匹配y不会作为交替路径的中间matched job；第二分支不会悄悄把y放入inactive。所有A始终保留，输出模式内原job恰一次。空闲slot（包括某非零机未用尽的容量）是普通增广终点，并非要求某台原机完全空闲；这涵盖同一原机已有其它jobs的情况。

若inactive在T不可行，则第二分支不可能发生，第一分支必给错配。交换i,j即可构造另一方向。未承诺inactive不可行时，二选一算法仍有效；“至少一项”不排除两项本来同时可行。

没有输入见证时，先用同一容量/slot图对两份aligned模式分别做matching判定与构造，失败则报告相应aligned不可行；两份都可行时再作上述构造。无需解任何隐藏fullformula或源assignment。

## 5. Weak B 的准确前件

定理的对齐前件始终是**在T可行**。若另有任意B≥T的weak接口合同，且它禁止inactive在B可行，则所有T调度也属于B调度，故inactive在T不可行。Strict错配输出峰≤T≤B，于是违反“所有≤B模式必须同索引”的合同。

此只用阈值单调性，不用B<2T，也不要求将一份任意B可行aligned调度压到T。一般逐机统一时间允许B容量大于T容量；仅知aligned在B可行不能替代原文的T可行前件。Exact未作该错误替换。B不需要参与构造c_h；它只用于合同推论。

## 6. 全部原 jobs 的 outside-private 封装

为每个边界原job j添互异outside机O_j，只给该job一条timeT资格，A没有outside端。对任意内部输出模式X，将全部A∪X按构造在H执行，边界补集E\(A∪X)各去自己的O_j。内部峰≤T，outside至多其唯一原job、负载T，所有N件原jobs恰一次、合法且峰≤T。

反向，封装中满足指定模式X且峰≤T的完整调度，限制到H就是原内部strict模式。因此该测试封装下的模式可行性等价准确。

模式X仍是对具体原jobs去向的指定/投影，不是这些private outside机器已物理强制它。尤其原文inactive是X=R，不是X=∅。若真归约把outside端改接共享变量/锁定机器，改变内部模式就改变外部job集合，其负载可能增加；当前证明只承诺内部可替换性，不负责外部全局回填。不能据此宣称任意fullformula strict可行，亦不能推出所有身份复制器不可能。

## 7. 位复杂度与 v1 的关系

有理数T/s_h可按分子分母的二进制整数运算取floor；所有输入数的组合位长多项式。也可先比较Ns_h≤T，若成立直接取N，避免构造大商。Slots总数≤|H|N；若原finite资格数为L，展开边数≤LN，仍对完整显式输入长度多项式。Dense输入将所有矩阵项计入长度，照常扫描。没有按1/s_h、分母、B/T或隐式生成任务数展开。

匹配、两次交替搜索、slot到原机投影及逐机有理负载回算均为位多项式。输出仅指定全部所需原job的实际目的机；测试封装额外O(k)条赋值。

v1允许同一机不同finite p_hj，只要求(B/2,T]且T≤B<2T；所以其输入矩阵不逐项属于v2。可把v1所有finite内部时间统一为T，保留资格，得到v2的单slot对象；它与v1在strict模式可行性上完全相同。由v2构造返回的资格matching再放回v1真实原端，每机至多一件、每端原time≤T，才得到v1实际输出。这是模式层的化约，不声称替换前后每个矩阵条目或任意高阈值调度完全相同。

## 8. 独立结论

新Exact的全部主要数学与算法量词可独立闭合，未发现standing fatal objection。s_h=0、s_h>T、容量截N、任意aux、空内部机器集、rank截断、空闲slot、strict实际输出和weakB单调前件均如上核清。

它是容量matching交换在这个具体query/return原身份合同上的直接应用，不称新matching理论。内部同机异权、模式相关辅助集、外加预载、bundle或多尺度/内部外部不可分负载仍在域外；未提供实际coherence gadget、全局NO decoder、复杂性源或主near2反面。两版作者Proof均仍未读取。
