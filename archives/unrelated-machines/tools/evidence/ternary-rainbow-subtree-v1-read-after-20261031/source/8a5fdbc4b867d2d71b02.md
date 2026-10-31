# 完整三叉二叉彩虹子树：作者冻结证明读后审查

审查者：boss11 内部 cover_consistency。实际全文读取 `private_ternary_rainbow_binary_subtree_author_frozen_proof.md`，SHA256 `7609ddc76e434c4e3d7ee5171753ef71dcbf1909d2349e63a15a717cfd6c2510`；对应已读 Exact SHA256 `3264ae3c3a2100fe0ef50aff1a729f9282346dba45059e20f9dcdc28d739563d`。

本人此前Exact-only独立稿 `private_ternary_rainbow_binary_subtree_statement_first_review.md`，SHA256 `e0d8a963d389ac578b799ac30717ca59a25e31bbabd010b9c3e128c96f41bdba`，原字节保持。该稿的anchor-copy AND归约在未读作者proof或其它review前形成；本记录才读取作者的Dead-AND方案。两条证明来源不可互相倒置。没有代码运行、有限枚举、Git/Work或新颖性认证。

结论：没有发现standing fatal objection。作者完整归约和原P阈值成立；有一处末尾资格数措辞需准确化，见第7节。

## 1. 彩色表达式的SAT等价

每occurrence颜色只用于其clause的相应literal atom，以及对应variable的唯一false-assignment branch；即使重复literal也给不同occurrence ID，正确。变量branch选一truth、clause选一occurrence后，后者若为false，颜色恰在变量false bundle和clause各出现一次，禁止rainbow。若Φ满足，选择每clause一个true literal，所有occurrence颜色无这种重复；不同occurrence和private neutral atoms也不冲突。故中间语义精确等价SAT。

空false bundle用private neutral atom，不是省掉一个叶或引入empty subtree。它不会和任何clause颜色碰撞。全部false bundles的总occurrence atoms数是3m，每occurrence恰属于一truth branch，另有至多2n个neutral atoms；clause部分O(m)。因此表达式大小O(n+m)。每个bundle用balanced AND、全局再balanced AND，logical depth O(log(n+m+2))；不是按变量occurrence数串成长链。变量只需保留实际出现的ID，可排序后重新编号，无需按最大binary变量编号建指数多个模块。

## 2. Rigid、Dead、Atom的边界

Rigid的二分递归与我的固定palette bundle一致：两个A-copy任何局部rainbow witness都含同一个非空A，所以不能双选；必B加一A，叶颜色恰S。H0只作单叶Rigid，不作为Dead。原叶/机器复制而色ID相同是明确对象，不是资源容量复制。

Dead(H,c)仅H≥1时成立，因为任何full binary witness有2^H≥2叶。Atom全部编成高1的Rigid(c,p)，所以所有logical输入树height≥1；Pad、AND、OR以后只增height，作者没有在height0错误调用Dead。

Atom的private padding p必出现在其rainbow witness中，但只与本atom相关，不会导致原来可满足的全局选择冲突。Rigid内部的重复palette是其模板本身的刻意共享；独立构件新分配的aux IDs不能因此全局重复。

## 3. AND、Pad和OR的完整高度与逻辑

AND把T,U先Pad到H=max高度≥1，再加Dead(H)。Dead不可能被任何全局rainbow witness选中，故必须T+U。双方aux色私有，跨子式碰撞恰是原atom颜色所要求的碰撞；完整高H+1树和原逻辑AND一致。

Pad每次调用AND(T,Rigid(H,S_private))时两输入已等高，所以其内部“补高”是零次，定义不存在无限互递归。每次增加1到目标H*，没有跳过层或早停原叶，也不超过目标max。新private palette与已有全部颜色不交，故只加必含dummy colors，不改变原语义。

OR先Pad到H；guard sets各2^H个不同色、交集恰{g}，且与T,U全部色 disjoint。两option T'=AND(T,G_T)、U'=AND(U,G_U)均高H+1，所有witness都含g。外root选择两option会碰g，故必须选fresh filler加恰一个option，准确实现原OR；总height H+2。

freshness在全表达式范围分配：某OR的g只属于该OR两guard，其余guard/filler/padding/Dead/atom辅助色不在别的逻辑子式重新使用。因此父级AND不会因为两个独立子式的aux相同而误拒，父级OR也不会继承一个在两边无意重合的guard。实际实现应先保留全部original occurrence/neutral IDs，再从不相交namespace分配aux；“全局fresh”按此标准含义读取时proof成立。Rigid内部palette复制与上述逻辑构件私有性不冲突。

## 4. 规模、显式展开和NP

编译height递推为Atom1、AND=max+1、OR=max+2；Pad只达到max。因此logical depth O(log s)给H=O(log(s+2))。完整三叉heightH的node数恰(3^(H+1)−1)/2，故显式polynomial。

所有Rigid/Dead都实际展开，2^H palette大小≤3^H，颜色分配的循环不会超出输出树规模。Pad保留原T作子树，OR/AND保留所有选项的ambient subtree，构造不是用隐式共享DAG代替输出树。全部distinct IDs数不超过最终叶数，可用O(log|T|)bits编号。常量/空公式可直接给高1固定YES/NO合法树，不破坏统一多项式常数。

见证active nodes及两个child编号不超过原T大小；root、每active内点恰2 children、统一深度和actual leaf colors单射均可poly核验。故在NP。整个3SAT多项式many-one归约是本文自行证明的逻辑构造，不依赖其它彩虹/Steiner问题的不同目标困难性。

## 5. 与我先行证明的比较

我的独立方案用“具有公共anchor的A”来构造AND(A,B,A-copy)，并先把所有变量/子句模块固定到共同高度后balanced合并。作者的AND用不可行Dead作第三child，再用显式Pad对任意logical children补齐高度。两者都保持完整三叉，但承重不变量不同：我的A-copy需每个A-witness公共anchor，作者Dead需其height≥1且所有颜色相同。

双方都独立使用了Rigid固定palette和共guard排斥两alternative；在已冻结各自稿件后发现一致，不能据此把任何一方来源改为阅读另一方后的独立发现。作者中间colored AND/OR表达式把每种逻辑的归纳更直接写出，当前读后没有发现量词漂移。

## 6. 原P的全job回填及严格阈值

给binary rainbow F，选中edge jobs全down，其他原edge jobs全parent。Root pin和每active machine的unit incoming各恰一，另恰一个small留父，负载4/3。F外private machines无unit incoming，三个small总1。外resource因选中叶rainbow最多一unit。重复颜色的原leaf jobs没有合并；未选leaf/分枝全部留父，故是完整原P的σ。

反向C<5/3时，每个active机已有unit，若留两small就达5/3，不允许；所以至少两个出job实际down。从pin root出发递归取两条，得到完整binary subtree，不能在内部提前停止。其leaf jobs全是实际σ的外机unit子集，C<5/3<2禁止同resource两个unit，故叶色单射。提取所需时间按原树/σ为poly。

任意root-to-leaf path给one-ary选择，active机unit+两个small=5/3，inactive机1、唯一外机1。于是所有输入OPT≤5/3；NO没有C<5/3，故真实OPT恰5/3。YES只上界4/3，不把某些OPT1输入误称exact4/3。q1基线由一条单叶路径保证，q≥2等价binary可行，q3可剪成binary。

这与先前私有树(1,5/3)decision结论不冲突：本归约YES是OPT≤4/3而非OPT≤1，NO恰5/3而非严格>5/3；该decision的中间带允许任答。仍只有5/4间隙比，不能用于任意δ的near2 soundness。

## 7. 非承重文字修正建议与范围

作者§5末“各job两资格”按字面不准确，root pin只有一个finite端。应改“每job至多两资格”，或“除root pin单资格外其余jobs各两资格”。前面的完整P定义和所有负载证明已按单端pin处理，因此此处是文字范围修正，不是standing fatal。

本文未审实现或运行，未核全球新颖性或独立成文价值。没有把leaf比例(2/3)^h下降当uniform branching趋零；一般UM近二目标仍未解决。
