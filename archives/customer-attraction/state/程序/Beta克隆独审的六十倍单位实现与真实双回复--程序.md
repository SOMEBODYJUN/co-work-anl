---
id: customer-attraction/beta-clone-independent-sixty-unit-realization-and-true-tied-replies
kind: program
type_tag: 程序
title: Beta克隆独审的六十倍单位实现与真实双回复
status: original-independent-code-and-full-report-read; no-replay
truth_status: fixed-fresh-policy-lift-refuted; weaker-global-lifts-not-settled
review_level: informed-source-reconstruction-and-local-analytic-accounting; no-new-blind-audit
scope: original39-topic-two-player-subgame-and-smaller40-topic-three-player-clone-context
summary: 5103原stdlib独审与3067全报告，原40节点1560含self、clone四regular行×全部40末位及5100单位交叉；fresh双BR给当前24或27，重复25只击穿指定B合同。
source_ids: [061f85405dc54b349b25, 5294a4f1436e02e0b592]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/direct_exchange/audit_beta_clone_lift.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/direct_exchange/audit_beta_clone_lift.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/direct_exchange/beta_clone_lift_review.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/direct_exchange/beta_clone_lift_review.json
---

# Beta克隆独审的六十倍单位实现与真实双回复

两primary实际normal取得并全文理解：5103B独立程序、3067B完整报告，共8170B。此前[Beta版本审查](../审查/Beta背景表示的版本与两份单位实现边界--审查.md)只据父审MD记录60倍/5100/1560，明确未读此code/JSON；本次继后补其真实实现域与全部字段，不修改那个原时点叙述。[原固定策略反证](../反例/Beta克隆固定策略提升的不可补全局部合同--反例.md)已有完整数学，不重建反例。**原CLI/import、1560比较、pattern/单位展开核、参数扫描及新数学实现均0。**

## 模型与原合法背景：39主题的两人子局

原客户AB36、C3、AC36、BC10，总85个不同单位客户；对每个AC客户x单独加P_x={x}，先合法依次选36个P_x，使仅AC客户背景1。再余3位单位玩家，首位曾选A，研究hA后的两人子局。全原博弈39人、共同目录39主题A/B/C/P0…P35；**不声称h或hA是根实际路径**。有限BI能向其它孩子/祖先扩出含此子SPE的一份完整σ。

`original()`按三聚合类型AB36/C3/BC10及36个各自含A,C,P_i的单位类型表示客户，没有把原85人另逐个展开。背景字典用`id(customer)`作键，只给这36个独立AC对象1；这些对象一直保在列表，身份不会因相同兴趣合并。断言b值等于按36个P_i主题的实际命中数，核合法背景对应。

`payoff(customers,b,leaf,player)`对当前动作所含客户，用weight/(该对象背景+三位剩余者的覆盖数)加总。权重是不同单位客户的类型重数，不是加权玩家；本子局的完整leaf仍写('A',a,z)，已选首A也保在分母。原36背景动作并不作为这三个剩余者再次计数。

对全部39种第二行动a，程序计算全部39个末位z的精确收益，找所有BR。a=A/B/C时按原局部σ指定B/A/A，并断言确属BR；其它P_i后选catalog序首个BR。最后检查当前A收益24、B/C各22、全部39选择收益≤24。这给40个子局决策节点的完整真实偏离条件，不是完整39人根/所有祖先审计。

原comparisons=39×39+39=1560：前1521是39个末节点各39候选值，再39个当前选择，含40项保持规定动作（非self为1520）。它不是1560份独立策略，也不是clone游戏的检查数。

## 全原表与所有39个当前收益

原root对象只有original、clone两键。original恰六键：catalog_size=39、nodes=40、comparisons=1560、A_B_C_last_rows、current_payoffs、max_singleton_current="1/4"。A_B_C_last_rows三项各含best_value/all_BR/A_B_C_values，下表全部保留：

|第二行动|末位A|末位B|末位C|best_value|all_BR|
|---|---|---|---|---|---|
|A|21|22|22|22|B, C|
|B|24|17|20|24|A|
|C|27|23|31/2|27|A|

current_payoffs的全部39个标签值如下，没有把未列singleton默默当零：

|当前行动|原current_payoff字符串|
|---|---|
|A|24|
|B|22|
|C|22|
|P0|1/4|
|P1|1/4|
|P2|1/4|
|P3|1/4|
|P4|1/4|
|P5|1/4|
|P6|1/4|
|P7|1/4|
|P8|1/4|
|P9|1/4|
|P10|1/4|
|P11|1/4|
|P12|1/4|
|P13|1/4|
|P14|1/4|
|P15|1/4|
|P16|1/4|
|P17|1/4|
|P18|1/4|
|P19|1/4|
|P20|1/4|
|P21|1/4|
|P22|1/4|
|P23|1/4|
|P24|1/4|
|P25|1/4|
|P26|1/4|
|P27|1/4|
|P28|1/4|
|P29|1/4|
|P30|1/4|
|P31|1/4|
|P32|1/4|
|P33|1/4|
|P34|1/4|
|P35|1/4|

这些收益沿**改变历史后的真实**末位回复计算；不能冻结正常B。作为定义级说明，若第二人选P_i，末位A/B/C值分别359/12、28、299/12，其它singleton≤1，故A唯一BR，当前P_i在其AC客户上的分母为背景1+首A+当前P_i+末A=4，恰1/4。此手算解释全部36个相同值，不是新1560重放。

## clone()的实际有限输入：40目录、60倍、含empty

代码只使用A0/A1/B0/C0与每P_i一个clone P_i_0，共40主题；leaf仍是三位空背景玩家，首前缀A0后余两人。它不执行旧36个背景动作，所有clone份额调用b={}。报告encoded_background_not_replayed=true与这一明确代码合同相符，不是额外运行的时间证据。

背景零类型的相关标签为AB→{A0,A1,B0}、C→{C0}、BC→{B0,C0}。每个原AC客户i的四相关标签为A0,A1,C0,P_i_0。程序逐16个布尔pattern建集合，质量

\[
w_R=\frac{|R|!(4-|R|)!}{5!}=\frac1{5\binom4{|R|}}.
\]

它直接构造精确有理factorial矩，而非数值积分/随机客户动作。乘D=60，各指定pattern按|R|取重数：

|R大小|该大小的pattern数|每pattern质量|60倍每pattern单位数|
|---:|---:|---|---:|
|0|1|1/5|12|
|1|4|1/20|3|
|2|6|1/30|2|
|3|4|1/20|3|
|4|1|1/5|12|

源码断言每weight×D为整数、总质量85，然后真用列表位置展开5100个不同单位客户。不同位置可引用同一个不可变frozenset，不将它们变成一位权重客户。空pattern保留：36×12=432名没有任何兴趣，故5100中4668名有兴趣；empty存在不改任何收益/覆盖。这两个派生计数是表的解析后果，原报告只存unit_customers=5100，没有新增声称该计数已跑。

[作者完整构造](../等价/Beta克隆对背景利润的非负静态表示--等价.md)则每原主题3clone，一个AC客户有9相关标签A/C/P_x各3，质量1/[10·C(9,|R|)]以2520清分母、空pattern删除，B三个同覆盖标签要商。**两份有限输入不同**。本较小目录只有两A、一B、一C、一P_x，不能冒q≥r=3的全部主题clone一般输入，也不能由其局部表宣称无约束OPT静态一般身份已对它完整计算。对所用A0/A1/B0/C0叶，忽略未选标签后的指标边际仍由同一Uniform P产生，因此这些局部利润可与作者全构造对应；全目录额外clone的排除仍靠作者的对称类别证明，不能由40目录输出代替。

## 四个当前动作的全末位域与内部双表示交叉

`cloned()`只循环当前a∈[A0,A1,B0,C0]，固定首A0；每行对全部40个末位动作计算加权有理收益，再逐个与显式5100单位的unit_u相等检查。unit_u求每单位1/coverer后除D，故报告利润都在**除60**口径。

每行收集全部末位BR，再对这些BR计算当前者利润，并与unit_u交叉。按实际原报告，BR数量为1、2、1、1，因此结构上有160个末位值与5个当前BR值的内部表示相等断言；源码没存165计数，不能说这是本轮新审计数。两表示共享同一factorial pattern表，这属于内部编码交叉，不是两个独立输入或完整三clone全SPE枚举。

当前P_i_0这36个行动未在clone()外层逐行枚举，不能把它写成40节点全部clone当前选择的程序检查。它们覆盖总质量仅1/2，故当前利润不论后继都≤1/2；该解析cap足以排它们打破24/25/27的局部比较，但不补造36行输出。

## clone报告全部字段与双BR的不同当前利润

clone恰六键：clone_catalog_size=40、scale=60、unit_customers=5100、rows、strict_improvement="25-24=1"、encoded_background_not_replayed=true。四rows各有last_values/singleton_last_max/best_value/all_BR/current_payoff_by_BR五键。全部4×4 regular末位值、精确singleton最大值及best如下：

|当前a（首A0）|末A0|末A1|末B0|末C0|singleton_last_max|best_value|
|---|---|---|---|---|---|---|
|A0|18|22|22|23|5/18|23|
|A1|19|19|22|22|1/4|22|
|B0|21|24|17|20|1/3|24|
|C0|25|27|23|27/2|1/4|27|

|当前a|全部末位BR（原顺序）|当前者在各BR下的完整原利润映射|
|---|---|---|
|A0|C0|C0:25|
|A1|B0, C0|B0:24; C0:27|
|B0|A1|A1:22|
|C0|A1|A1:22|

这些表也说明粗cap1/2之外的精确末位singleton最大值分别5/18、1/4、1/3、1/4，不能统统写成1/2或零。3个分数来自不同相关fresh/reused负载，所有40末位都已在原程序行内比较，但仅保存其regular四值及singleton最大值/全部BR，未输出全部160个literal值。

**固定合同失败。** 按原σ保留fresh A1、末位B0给当前24；若改重复A0，则全部末位BR仅C0，当前25>24。最后C0利润23严格高于另三个18/22/22，所有singleton更低，不能用B0平局威胁。原strict_improvement字符串虽硬编码，旁边assert明确核repeat唯一BR/C0=23、当前25和freshB0=24，身份不能只靠文字。

**同一fresh节点的另一真回复。** fresh A1之后B0、C0都是末位BR22，但当前利润分别24、27。不能将所有BR的当前利润都写成24；程序完整报告确实保了C0:27。若在这个**较小40目录的局部子局**改选C0，当前A1得27，高于repeat25、B0/C0当前各22，且singleton当前≤1/2。对其它singleton当前分支选任意末位BR，即可补一个第二位A1、末位C0的两人子SPE。这只显示改fresh行为有局部自由，不证明原hA根到达或任何全局弱lift。

## 核心积分、同叶债与真正被否定的量词

对AC客户b1，P~Uniform[0,1]，相关I/J条件独立Bernoulli(P)只是确定有限pattern的积分表达：

\[
E\frac{I}{2I+J}=\int_0^1[p(1-p)/2+p^2/3]dp=7/36,
\quad
E\frac{J}{2I+J}=\int_0^1[p(1-p)+p^2/3]dp=5/18.
\]

于是重复A0当前36/2+36·7/36=25，末位C0为3+10+36·5/18=23。fresh A1/B0各方AC用全鲜1/(1+k)，给规定当前24；fresh A1/C0则当前27。这些是已读原数学后的手算解释，不是程序再次运行或新盲审。

[同叶碰撞债](../引理/Beta克隆的单次增益与复用上尾债务--引理.md)仍成立：重复叶A0,A0,C0的当前25≤原投影AAC背景27；这个投影背景总利润76，clone总25+25+23=73，覆盖债D3，单次C收益增1（23对原22），两个复用A总损失4=3+1。它完全允许25大于另一个fresh指定叶AAB24，不能从同叶折扣推出跨不同真实叶的付款。

因此严格否定的仍是“固定给定原完整σ，在**所有fresh历史**逐项保留其原主题行为，再补重复孩子”；只要这个合法离轨局部合同不能补，就排整个强lift。正确的静态非负表示/受限fresh树保SPE不受损；允许重选fresh行为后只保原实际终局、或只求某clone SPE覆盖≤原背景利润的两个较弱全局接口仍未由此判真/判假。更没有half反例、最小见证或一般不可能定理。

## 入口、先验与处置

源码只stdlib itertools/json/math/Fraction/Path，函数original/cloned不导项目model、solver、作者发现器或原MD；有main guard，普通import只定义函数，main下才各调用一次、写同目录beta_clone_lift_review.json固定覆盖并print完整报告。无命令行参数处理/输出路径/拒绝覆盖。所有assert（背景、BR、单位整除/总数、25/24关键点）可被python -O移除，原文件没有运行模式、代码hash、argv/cwd/exit/耗时或stdout日志绑定。写出/print都json.dumps(indent2)各加一LF，按代码合同两份完整序列化相同；没原stdout就不声称本次已比较成功。

[父审原MD](../审查/Beta背景表示的版本与两份单位实现边界--审查.md)记父方先独立手算后读作者定稿，direct先只见四类型/局部σ/待检合同且未导发现器；本代码支持“实现不导入”，精确盲读时间顺序仍按原记录，不靠docstring单独认证。父审还说原计划独立审查Markdown没留下，不虚构其完成。当前清洗已见所有作者稿/既有结果，是知情源理解。

两primary均retained到本程序页、[完整来源闭包](../../tools/evidence/beta-clone-independent-audit-two-primary/README.md)。五正式与三个原MD全文仅related，不额外done/扩旧审范围。19WY原全19ID claim pushed/raw needs-attention，独立38 untracked+2 tracked全同、missing/different/unmerged空且stash保留，并列不改raw为synced。Boss4未Git/claim/done/外发，原CLI/import/单位pattern/SPE核/新数学实现全0，成熟交Root串行发表。
