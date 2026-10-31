# 全局叶重数2/3门槛 v2：root冻结证明读后攻击

审查者 pcsp_occurrence。实际全文读取 `ternary_rainbow_multiplicity_threshold_v2_root_frozen_proof.md`，读前、读后 SHA256 均为 `042250b0fcb40f0fdb2e5998f6854bb71e05efa49778925d4c0953a01562f785`。绑定 Exact SHA `8e47cc088a50d6f8609c9dcbd11f142407229e7ef5c6171fdd6b3dc5a8b2c6a9`。

这是读后审查。此前真正仅据Exact的独立稿 `ternary_rainbow_multiplicity_threshold_v2_statement_first_review_pcsp.md`，SHA `affeee5ccbc9f1bc193f97e9476c4b69faa7da0d8f4f0501f3a5033524741b6b`，原字节不动。我的v1作者先验已披露；我独立v2实现数学使用Must/Fresh/Dead，root冻结proof使用新的低重数Rigid/palette与protected色，不能把两份实际构造来源混为一份。

结论：root冻结proof所述全局重数门槛及P推论无 standing fatal。以下为实际逐段核查，没有实现或有限实验声明。

## 1. 重数2的全体YES与raw q子可加性

每原色至多两个叶occurrences分到不同A/B桶，保证各桶内部原χ单射，空桶无碍。作者用raw q(A∪B)≤q(A)+q(B)及q(全叶)=3，得到某桶q≥2，此推导正确。

我也独立核了本页给的子可加性归纳，而非仅引用旧账本：height1的q是选中叶计数。height≥2时，令a=q(A)、b=q(B)，若Q=q(A∪B)>a+b，则支持Q的Q个children中，q_child(A)>a的children至多a个，否则rootA值至少a+1；B同理至多b个。因为Q>a+b，余下一个支持Q的child两值分别≤a,b，按其更小height的子可加性，q_child(A∪B)≤a+b<Q，矛盾。Q最多3、a/b可0均无问题。只对子集合并使用raw q，不把χ原色数误当q。

因此本页论证与本人独立的两桶majority递归均有效，对任意height成立；没有固定height枚举依赖。

## 2. 新Dead及低重数palette的逐层检查

Dead_H只在H≥1调用；每个最底parent自己的3叶用一个全新色，其他最底parent用别色。任一binary subtree到最底必须选同一parent的2叶，所以确实dead。每色全局恰3次；没有沿用v1全树同色导致的高重数。

R_H(S)的H1有(a,b,a)，其合法binary叶色集恰S；protected p指定放b位，因此p单出现。H≥2时只使用A与B两份palette children各一次，加Dead_{H−1}作为第三child。因为dead不可选，必须选A+B，色集恰S且可行；palette色不被结构性复制，每个只在其所属A/B子树一次传递。归纳到底，各palette色实际出现1或2次，protected p沿唯一子树传递而保持恰1次。H0单叶也良定，但实际atom/guards/padding入口均至少H1，不会从H1误调Dead0。

所有R内Dead色必须与S及其他构件完全fresh；作者明确要求这一点，故辅助色不会与protected原色或另一个palette产生隐藏全局重复。新Rigid不等于旧(A,B,A-copy)递归；使用dead替代结构复制是重数界成立的关键。

## 3. Atom、Pad与OR的真实全局重数

Atom(c)用R1({c,p})且protected c单出现，另一私有p两次。于是每原occurrence颜色c_e即使在variable false branch和clause option各出现一个atom，整个输出也恰2次；不能把旧atom(c,p,c)中c双出现的方案混入本版。

Pad只把原T嵌入新AND一次，另加全新palette和Dead；不复制T或source子式。不等高AND先Pad到max，此时两输入等高，所以Pad内部的AND不触发无穷互递归。

一个OR的两个guard palettes只共用fresh g；两份R均指定protected g，因此各仅1个实体leaf出现，总共2次。其他palette颜色互相不同、与T/U及全局其余aux不同。两个guarded options的任何binary witness均含g，不能同时选，第三fresh filler必选，精确实现OR。父层不复用g。

全局类别逐项均成立：原occurrence c_e两次，neutral原atom色一次，atom私有p两次，OR共guard两次，其他私有palette色一或两次，Dead底层色三次。逻辑表达式是树、每个子式实体只用一次；只共享颜色ID而不共享逻辑子树。没有被排除统计的控制色，没有将超重色称alias从而免费复制resource。

## 4. 原SAT语义、边界和显式复杂度

每occurrence c_e在变量将它置false的branch及它所在clause的option各一处；两处同色实现false选择冲突，其他occurrence IDs不同。非空短clause重复literal补3positions时仍给各position不同ID，保SAT且不把一个原色多用。Empty false bundle用fresh neutral atom没有跨模块冲突。

给satisfying assignment，可为每clause选true literal，source颜色不冲突；反之任何realization选择false literal都会撞它的variable branch色，所以得到SAT assignment。新R/D保v1各gate语义，因而正确移植该中间表达式，不需要其他目标Maximum Colorful Subtree的困难性。

空CNF/常量YES用height1(a,b,a)，NO用(a,a,a)，都满足≤3；不可调用Dead0。实际出现binary变量ID排序重编号避免按最大数值ID遍历。输入如果允许前导零等同一数值多编码，按变量ID的实际语义归一化即可，不把编码字符串误作不同变量；这属于常规显式语法解析。

Atom高1、AND=max+1、OR=max+2，Pad只升到max。balanced false-bundle AND及balanced顶层AND给h=O(log(s+2))，完整tree为s固定多项式。每个R/D都显式展开，palette大小2^H不超过同高3^H树规模，辅助颜色个数≤叶数，整数ID长度O(log|T|)。没有隐藏DAG或指数oracle。NP成员性按给定binary subtree直接验证，正确。

## 5. 全P和比值范围

实际矩阵没有变：每private internal一台机器，root pin单资格time1；每tree-edge job父time1/3、唯一下端time1，叶下端是该色唯一resource。每个非pin job恰两端。整棵树每色≤3意味着该resource至多3枚eligible leaf jobs；不同leaf jobs仍为不同任务。

YES binary rainbow见证按选中edge down、其他parent回算：active internal unit+one small=4/3，inactive internal三个small=1，resource≤1。实际C<5/3时rootactive且每active node至少2down，沿私有树递归选2；resource若有两枚unit将达2，所以所选叶色必须distinct。任意root-to-leaf path的完整σ有C≤5/3，故NO实际OPT=5/3。处理时间、机器资格、root单端、全部任务负载均未遗漏。

因此只给限定树源的重数2/3 sharp复杂性门槛，以及(4/3,5/3) promise/5/4比值锚点；没有uniform branching gap放大，更不排除一般UM的所有2−ε算法。

最终状态：作者root低重数palette/protected构造与我的Must/Fresh重构是两份不同实际证明，两者均闭合；本次实读root冻结proof无 standing fatal。旧Exact-first保持原字节，无实现/实验、外部新颖性或主目标升级。
