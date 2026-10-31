# 有界叶资源重数私有树 v3：作者证明读后审查

审查者：boss11 内部 cover_consistency。实际全文读取 `private_tree_bounded_multiplicity_floor_v3_frozen_proof.md`，SHA256 `30d7ede62e830bca8f27285b0aa64c19de6327dd4d9716bc5a2623927944027e`；绑定已读 Exact SHA256 `8fd533805efaf7ab6168d0512dea327e70360065d05b4df2d52a178a49279142`。

此前Exact-only独立稿 `private_tree_bounded_multiplicity_floor_v3_statement_first_review.md`，SHA256 `fa214dbb0df02518b989d78f37f23326dbad870648e0c807ae8d4843d3b52932`，原字节保持。该稿在未读作者proof或其他v3记录前自行给出raw q、rainbow partition和逆像blocker的新桥；已有v2/Haxell背景已披露。本记录为第二阶段，不倒称为新的盲审。

结论：L/A/B正式合同和核心证明未发现standing fatal objection；§7有一处d1退化的未加条件措辞，建议收紧，见末节。未运行程序或有限测试，未认证算法σ、新颖性或发表价值。

## 1. raw q的归纳

作者给多集合版本的直接高度归纳，我的先行稿先证二集合再迭代，二者一致。h1时q就是原叶数，子可加显然。h≥2、Q>Σb_i时，Q个高union-value孩子中，至多Σb_i个可能有某一i的child value>b_i；故至少一个孩子全部value≤b_i，与孩子归纳的union value<Q矛盾。

当b_i=a时不进入Q>Σb_i分支，所以无需构造超过a的分叉。空集、重复集、a1均有效；没有对h0定义一个与uniform branching不相容的辅助值。raw叶positions和资源colors分开，未把一个非注入资源当作单叶来直接应用旧injective theorem。

## 2. occurrence classes与blocker

每资源至多μ次使occurrence-index classes各自全局rainbow。q(full)=a和子可加给某类q≥ceil(a/μ)。删除资源X的全部preimage后，若剩余有任一class q≥r，类内full r subtree就是避X的rainbow候选；故每类≤r−1，剩余raw q≤μ(r−1)。

设置t=μ(r−1)<a后，删除叶必击中全部raw(t+1)-ary子树。raw精确叶blocker为(a−t)^h，给所需|f^−1(X)|下界。此处没有把raw候选当Haxell资源edge，也没有除μ。r1给t0、X必包含每个出现资源、preimage为全部叶；其公式仍有效。

如果μ比实际叶数大，数学上允许空classes；实际非空类最多叶数。本文无按μ枚举生产算法，binary μ没有隐藏伪多项式承诺。局部μ2/a3任意height都有binary rainbow确由此推出，与先前一般重复色的NP-hardness不矛盾，后者没有该全state multiplicity≤2限制。

## 3. Haxell资源rank、共同预算及严格差

所有候选edge只取rainbow r树，资源rank恰k=r^h，不是原叶multiset长度去重后任意变小，也不是μk。命中I的全部候选时，每state都有|f_us^−1(X)|≥B。作者(3)交换有限求和，内部正是共同λ的实际multiplicity容量，故τ≥B|I|。不能在这一行偷换成|X∩image|；作者没有换。

B≥2k−1给τ≥(2k−1)|I|>(2k−1)(|I|−1)，严格差至少2k−1>0，满足总edge size k+1的Haxell系数2(k+1)−3。I单点、I空、k1及重复edges均无问题。各state局部候选非空由μ(r−1)<d和ceil(d/μ)的局部存在保证；不是对空超图调用匹配结论。

外部定理沿用前两阶段实际核的Annamalai arXiv1509.07007v2 PDF2/印1 Thm1.1及AFS2008 PDF5 Thm2。此次没有重新读取这些primary全篇、重算作者列出的PDF字节hash或取得Haxell1995原proof，因此不把这几项冒称新审查。

## 4. CONFIG auxiliary分布中的multiplicity

v2的精确CONFIG行不需注入。给定q,t，Σmin(q,t_e)≥a q；activated mass b≤q时，Σmin(b,t_e)≥(b/q)Σmin(q,t_e)≥ab。选择b_e≤min(b,t_e)、和ab并用uniform-matroid base分解生成a children，零b分支跳过，实际child activation marginal≤t_e。每root先按selector marginals选一个真实state，和为1，故得到共同有限aux a-tree分布。

每个aux tree是原state的叶子集，其每色重数仍≤μ。关键式(5)计的是一个resource接收的**期望叶数**，不是“至少被一叶使用”的概率：Σ_aux λ|f_aux^−1(z)|恰等于各原leaf activation marginal之和，≤原CONFIG中该z的全部unit-job marginals之和≤1。重复叶都逐job相加，没有偷去重。

于是可以用第3节相同加权Haxell论证，ambient branching改成a。aux分布可能指数支持，不影响存在性；它没有先解决不同root冲突，冲突由匹配定理最后消除。多个aux tree可同属原state并共享内部nodes，但最终每root只选一个witness，跨root原机器私有，所以不产生物理共享。

## 5. μ、r和ratio

r=ceil(a/(μ+2))给a≥(μ+2)(r−1)+1，因此a−μ(r−1)≥2r−1≥1，既有strict μ(r−1)<a，又有h次幂≥2r^h−1。r至少1且不超过a。μ1恢复a−r+1的v2条件；μ2给α7/4。

令β=1/(μ+2)、x=a/d，r≥βa；作者中间差α(2−x)−(2−βx)=2(1−β)(1−x)≥0，正确。T0=1+s/d≤T，故全部阈值下actual OPT≤αT。T≥2直接C≤2补齐；有限显式P的CONFIG在1+j/d网格上变化，Tconf取得于该有限网格，可避免误读为要构造某无限概率极限的整数调度。

μ允许binary增长时α<2对每输入成立，但ε=1/(μ+2)不是输入无关常数；只有μ固定时结构类有统一离二界。作者保持了这一量词，没有声称一般UM sub2。

## 6. 原P全部job回填

selector投真实选state根；选r树内各节点收unit、r个job下送、d−r个small父置，负载2−r/d。未激活分枝父edge并未送来unit，其自身所有d个job父置负载1；所有未选/零权states同样父置。selected leaf经rainbow及跨root matching互异；同色的其它未选原leaf留父，不会额外占external。每个原job恰排一次，未改finite ends、未删aux之外分枝，也没有新造物理aux树。

存在性与构造复杂度保持分离：有限辅助分布、指数候选族和Haxell存在性不提供一般变参的σ位多项式算法。小型CONFIG系统只给分数阈值/判定层面，不代替该缺失步骤。

## 7. 一处退化措辞建议

作者§7第一条“d1的实际调度为1”须明确附加A的共同λ前提或B的CONFIG(T<2)可行前提。在这些前提下a=r=1、Hall给C1确实正确；对任意无条件d1实例则不成立。

精确反例：d=h=1、两个roots各只有一个state，两个state的唯一叶映到同一external。每root selector单位1只可在其根，leaf job父端/外端均1。若任一leaf父置，该根负载2；若两leaf均外送，external负载2，所以OPT=2（全父置达到）。CONFIG(T<2)时根selector强制两个leaf全在external，违反unit容量1，故Tconf=2。这里每state重数其实1，任意给定μ≥1都可作上界。

因此canonical可改为“在A或B的非平凡可行前提下，d1得到C1；否则仍有全父置C2”。这个未加条件的退化表述不影响Exact正式A/B和其条件式证明，不作为定理级standing fatal；也无需改已冻结Exact-only原稿。

本审查未覆盖新增未见的sharp参数家族，未运行代码，未核全球新颖性或一般UM主目标。
