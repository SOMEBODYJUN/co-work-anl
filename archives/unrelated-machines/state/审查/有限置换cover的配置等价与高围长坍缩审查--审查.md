---
id: unrelated-machines/finite-permutation-cover-config-equivalence-high-girth-review
kind: review
type_tag: 审查
title: 有限置换cover的配置等价与高围长坍缩审查
math_scope: same-type-incidence-permutation-covers-of-ordinary-UM
status: proved-cover-equivalences-and-existence; no-polynomial-size-hardness-construction
summary: 自足给全部cover配置阈值相等、某cover整数OPT实现、正则群高围长及分母logq界；seed的精确Tconf另证，纯cover不自动保整数NO。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/configuration_finite_cover_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/configuration_finite_cover_review.md
---

# 有限置换cover的配置等价与高围长坍缩审查

## 实际对象与版本

5857B/48行主review及95行最终正文ff8d35a5c019fa6c5faaa26fa9848727490ade77141fcff4275273877f1064a1均全文读。旧[cover/消元页](配置覆盖坍缩与永久消元双源审查--审查.md)、[有限cover页](配置激活与有限覆盖增量审计--审查.md)、[seed页](配置有限覆盖种子精确证书--审查.md)全文比较；本页补指定审查的完整量词/分母/正则作用与修订先验，不把有限fixture冒称一般证明。

一般合法P，有限incidence图为machine i—job j，有限边时间p_ij。正整数q的cover由每条原incidence一个置换π_ij:[q]→[q]给定：job(j,a)只在(i,π_ij(a))执行、时间p_ij。全部机器/任务同数复制，无其它机器、任务、端、改时间或跨type接线；允许任务任意度、零时间及空任务。

CONFIG(T)每行可行原任务子集（含空）分布质量1、逐job覆盖恰1。向下封闭使≥1覆盖可逐任务拆权删任务成恰1；有限配置负载断点使T_CONF取得且有理。没有精确配置oracle假设。

## 五个方向与真实见证

1. 任意q-cover的真实T调度在每machine-copy去标签得到**原任务子集**，因置换使该copy对同一原j至多一个邻居；按q平均给P的CONFIG(T)，概率分母整除q。
2. 对任意固定cover，T_CONF(Q)=T_CONF(P)。Q→P把每copy配置去标签按type平均；P→Q在(i,b)把原C中j换成唯一邻居(j,π_ij^{-1}(b))、沿原y_iC权。每job-copy跨i包含概率和仍1，故每T可行性双向等价。
3. 任意原实际σ可提升到**每个**cover：若σ(j)=i，把所有(j,a)送(i,π_ij(a))；每(i,b)恰收到各原σ(j)=i的一份copy，逐机负载等于原i。
4. 给有理配置证书y、q为共同分母，在每type i的q个copies上放qy_iC份配置C。每原j共有q个被选socket位置(i,b)，覆盖等式保证此数；给它们双射标签a。每incidence的已用a/b不重复，构成partial bijection，逐incidence补完置换，并把(j,a)放其socket。实际调度精确实现所有原单机配置分布，峰≤T。
5. 因此全部covers满足T_CONF(P)≤OPT(Q)≤OPT(P)，且

$$\min_{q\ge1,Q\text{是q-cover}}OPT(Q)=T_{CONF}(P),$$

最小值取得，不是只有inf。正OPT时T_CONF>0：若T_CONF0，每job从正权零负载配置得零端，逐任务零端即OPT0。故纯cover的配置gap不超过原gap；不取0/0。

## 小logq不等显式规模小

r=m+n，配置等式矩阵A为0/1、至多r行。取rank r'独立行及r'基列成非奇异0/1方阵B，Cramer使BFS分母整除q=|detB|，Hadamard给q≤(r')^{r'/2}≤r^{r/2}。因此**存在**达到T_CONF的cover且logq多项式；显式mq/nq对象仍可指数。没有找到最小q、求未知配置或按bit(q)输出q份对象的算法。给已列y的socket实现按实际显式q输出规模收费；n0直接q1。

## 高围长要用正则群作用

有限图G，每无向边定向并配独立生成元e，反向e^{-1}。令B为长度≤g的全部freely reduced words含空词；右乘e且约减，在乘前后都在B时为partial injection，任意补成B上的置换h_e，负符号用逆置换。每非空约化w、|w|≤g在空词上的逐前缀仍B内，故h_w不为恒等。

**不能仅用h_w非恒等就称无fixed point。** 取所有h_e生成的有限群H对自身的regular右作用；每顶点v复制(v,h)，边e连接(u,h)到(v,h h_e)。若有短简单lift环，其投影为非回退闭行：局部cover双射排立即沿同一原边回退。独立边符号使投影给非空freely reduced w；闭合要求h h_w=h，从regular作用迫h_w=1，矛盾。因此有girth>g的有限cover，未主张高效或多项式规模。

先造达到T_CONF的Q0，再取其高围长cover并无损提升调度，复合仍是原P的统一cover（fiber用(q,r)索引），得到高围长Q且OPT(Q)=T_CONF(P)。不要求第二cover保留原determinant小degree界。两端任务时incidence girth为machine多重图girth的两倍；base连通时可选一个cover连通分量、其各fiber数仍相同，断连base则各type/分量须保全。

## 四机七任务seed中两个最优值都另有证明

机器A/B/a/b，公共c只可A/B时间1；每根r=A/B有三件r0,r1,r2，在r时间1/3、对应terminal时间1。其它∞。

整数OPT5/3：c在某根，若峰<5/3该根至多再收一small，至少两件到其terminal负载2矛盾；c与两small给A、另一件给a，B三small全home，峰5/3达到。

这里T_CONF**确实恰4/3**，不是仅给证书：T<1无法覆盖c；1≤T<4/3时根含c便不能带small，terminal每配置≤1件迫根期望small数≥2，若根含c概率α则2≤3(1−α)，故两根α各≤1/3，无法合计覆盖c1。T4/3时每根半权全三small、另半权均匀c+一small，各terminal均匀三个singletons，给完整可行点。

共同分母q6，socket构造某6-cover有真实峰4/3，配置阈值相等又迫其OPT≥4/3，所以此cover精确OPT4/3。恒等置换6-cover是六份seed、OPT仍5/3。同seed/同q的接线不同，既不保证任意接线保seed NO，也不保证任意接线自动达到LP。有限report单独的4/3 feasible字段不能独自证明最优；此等式由上面数学补足。

## 独立顺序、澄清和历史实现

reviewer先只精确Claim盲重构，再实际读初c405e6a75649ccaed0be2a4e22869a082672cb0743601b8c5106fa41425a834b与两代码。建议显式补≥1覆盖剪成恰1及T_CONF0⇒OPT0，boss加入ff8d终版后reviewer实际读新增段/句确认；纯澄清未改Claim/代码、没有为文字重复跑。

其亲读后各执行一次规范fe918b144c228e0ca43562654d612400ea32dea8a14a048ac11c9323afaf3378与独立ec33b361e07837b727631f401e80ae7b827f727437a19446b3b58968c64644a6，均exit0：128seed调度无损lift，160真实有理mixtures、3boundary、7invalid；独立不import核心，570非空短约化字分离。先freeze前partial-permutation临时实现另覆盖0..3生成元/长度1..4含无边，不称第三规范长期资产。**未实际生成高围长group cover**、无generic配置solver。本批无新原程序run。

Vontobel–Koetter编码局部多面体/cover伪码字机制原review未独立核页码，依boss原文核验；当前正文记录Prop10页18、AppendixA.1 Lemma55–56页50–52，模型是二元码而非调度。本页调度方向自足证明，不把它们冒称外文原定理或本批PDF全读。

每固定有理δ∈(0,1)若有NP源位多项式YES OPT≤T、NO≥(2−δ)T、T>0归约，取δ<算法ε可分离两类，足以在P≠NP下排任意统一改善；次数可依固定δ但不随输入增长。该路线尚未完成，也非所有反面证明的必要形式。选定接线族、随机/expander/PCP额外限制及source解码不被此存在性排除，亦不由高围长自动提供。[原件/逐源边界](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。
