---
id: customer-attraction/global-coverage-entry-static-pne-certificate-and-net-gap-contract
kind: resource
type_tag: 资源
title: 全局覆盖入口的静态PNE证书与净差合同
status: complete-entry-and-required-original-closure-reading
truth_status: 原四人50客户有限证书与作者核验合同保全；静态桥已由更强旧对象否定；弱净差匹配仍未付
review_level: 完整入口及五相关原件实读；未重放原程序，不继承原外审声明
scope: 原50客户为四玩家四主题完整85历史；残余正文另为两玩家六题；一般half与特定人数状态分离
summary: 原README全部三条数学方向和文献核对时态闭合；保九类型50客户/完整规则/精确收益及静态检验定义，分清原审计代码、JSON字段和未取得的stdout事件。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/pne_welfare_bridge_failure.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/pne_bridge_reduced.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/audit_pne_bridge.py
---

# 全局覆盖入口的静态PNE证书与净差合同

2344B根README不是残余反例正文的重复标题。它有三个不同合同：以同实例最差静态PNE福利支付顺序福利；以最优并集的全部实际遗漏R支付；以及退回保留浪费覆盖G的净差匹配。前两项已被各自有限见证否定，第三项是源的未付款方向。必要闭包五件16865B现均正常取得并全文读；只作本批related，不额外primary done，也没有为补一个入口重新运行原发现或审计。

## 四人50客户原资产的完整数学输入

四名单位玩家、四个共同主题A,B,C,D，以下九类共50名不同单位客户：AB1、AC2、BC1、ABC5、BD2、ABD16、CD8、ACD6、BCD9。每主题都非空、集合互异，大小分别30、34、31、41。令终局计数为(a,b,c,d)，总数4。占用主题的玩家收益由下列精确式给出：

\[
\begin{aligned}
U_A&=\frac1{a+b}+\frac2{a+c}+\frac5{a+b+c}+\frac{16}{a+b+d}+\frac6{a+c+d},\\
U_B&=\frac1{a+b}+\frac1{b+c}+\frac5{a+b+c}+\frac2{b+d}+\frac{16}{a+b+d}+\frac9{b+c+d},\\
U_C&=\frac2{a+c}+\frac1{b+c}+\frac5{a+b+c}+\frac8{c+d}+\frac6{a+c+d}+\frac9{b+c+d},\\
U_D&=\frac2{b+d}+\frac{16}{a+b+d}+\frac8{c+d}+\frac6{a+c+d}+\frac9{b+c+d}.
\end{aligned}\tag{1}
\]

仅对当前占用主题查询相应式，故各分母正；含零未占用坐标不产生除零。覆盖函数为九个类型“至少一所喜主题被占”的重数之和，重复选择保留。

原完整策略可不漏行地压缩为以下规则，与JSON全部85项动作逐项对应：

1. 根A。
2. 第二人看到首题D时选A，其余首题选D。
3. 第三人看到前两题DD时选A，其余长度二历史选D。
4. 第四人若前三题是BDD的任意排列则选C；是CDD的任意排列则选B；是DDD则选B；其它全部选D。

这里覆盖1+4+16+64=85个**有序**决策历史，前三题的排列条件包括所有离轨排列，不能只保BDD/CDD各一个节点。最后层只有二十个无序计数：AAA、AAB、AAC、AAD、ABB、ABC、ABD、ACC、ACD、ADD、BBB、BBC、BBD、BCC、BCD、BDD、CCC、CCD、CDD、DDD。规则4在BDD取C，在CDD/DDD取B，其余十七态取D；这是此份策略恰有的对称性，不是模型要求所有同计数历史统一。

令F(h)是从精确有序历史h按这四条规则走到四题终局。完整激励检验是

\[
 U_{\sigma(h)}(\operatorname{count}F(h))\ge
 U_t(\operatorname{count}F(ht)),\quad |h|<4,\ t\in\{A,B,C,D\}.
\tag{2}
\]

左右都是**当前位玩家**最后所占主题的利润；F(ht)必须重新跟随上述规则，不能把后人固定成原路径。二十个末态代(1)，再十六个二题历史、四个一题历史及根逐层比较，恰是全部340含self/255非self比较的有限证书定义。原作者审计逐有序历史执行这套系统；本批保存其完整代码和输入，不把(2)的有限域说明当本次已执行340次的事件。

原实际路径ADDD，利润(27/2,71/6,71/6,71/6)，福利49，只有BC型的一名客户遗漏。根四种真实后继收益为(27/2,49/4,143/12,71/6)，A严格最佳。若在**静态**ADDD中把首A改B，后人不动为DDD，首人获55/4>27/2；真实顺序改B后，最后节点BDD按规则改C，使根偏离只获49/4。这条精确差异解释为何不能把同实例某个PNE的不增福利修复当作必然存在。

静态PNE检验与(2)不同：对每个非负整数计数n总数4，逐个占用X与备选Y，比较

\[
U_X(n)\ge U_Y(n-e_X+e_Y).
\tag{3}
\]

四维总和4恰35计数，原正文声明唯一PNE计数为(0,1,1,2)，利润B49/4、C143/12、D各155/12；覆盖50。其余34计数各有严格静态盈利偏离。原审计的代码确遍历所有256有序终局并按计数去重，逐玩家/备选找第一盈利见证，记录PNE和nonPNE。**它的断言只明确要求PNE的最小福利50，没有单独assert“恰一个PNE计数”**；唯一性来自原正文声明及枚举输出设计，五related没有附该stdout原报告，本批不补造一份输出。资源保全这份可复核的固定有限证书，不将作者审计声明改称本次独立数值认证。

因为该静态PNE本身覆盖全部50人，OPT₄50；审计输出中的OPT50是直接字面值，不是又跑一次覆盖优化。完整输入(1)、策略四规则、全域(2)(3)和原字节提供原资产的全部承重对象，读者无须从一个摘要猜模型或离轨动作。其反驳的桥是“每份SPE都存在同实例PNE福利≤该SPE”，不是仅“SPE终局可以不是PNE”，也不是一般half。原点2W−OPT48>0，不声称最小、唯一SPE或全节点严格。

## 2145B原作者审计与10024BJSON的精确接口

原审计只用标准库Fraction/product/json/Path，不导入规范求解器。TYPES及四规则字面嵌入，rollout对任何有序h续到四人终局。margins遍历全部85历史、每历史四动作，断言原动作最终利润不低于真实偏离后继；self差0保在数组，因此输出min_SPE_margin可为0，不能据这个字段推全节点严格。

静态遍历如上按35计数去重，遇首个盈利偏离即break，不会对每个nonPNE做完全部备选；实际payoff调用次数或静态比较次数不能随意写成35×4×4。代码没有输出nonPNE的34个具体见证表，只输出其计数。唯一外部数据输入以**脚本同目录**BASE读取`pne_bridge_reduced.json`；只assert JSON玩家数4、certificate目标[1,0,0,3]，再逐JSON动作核choose(history)相同。没有逐字比较JSON的instance客户表或宣告welfare/comparison字段，也没有在原代码中assert动作表恰85个无重复全历史；本批静态完整性核对补足源JSON实际确为九类型一致和85项全历史，不冒称这两个条件原审计早有assert。

JSON六个顶层字段为kind="PNE"、instance、counts=[1,0,0,3]、welfare49、comparison50、certificate；certificate含terminal_counts与actions。`comparison:50`只是一个标量，没有静态PNE列表、逐计数见证或完整运行报告。所有原客户和85动作已按原字节保留，未改写为本页规则生成的新证书。

原程序print一个JSON，包括types_mask、on_path、utilities、welfare、OPT、SPE_histories、SPE_deviation_checks、min_SPE_margin、PNE_count_vectors、nonPNE_count_vectors、root_action_values，共11字段；没有文件写入、CLI或main guard，import会执行。原assert受−O影响，不能仅凭优化解释器的JSON输出认证校验已发生。当前没有运行该原审计，没有取得它的stdout/stderr/exit事件，也不借规范求解器旧成功替代同SHA原进程身份。

## 71客户related闭包不是另一个新反例

296B`residual_unique_integer.json`全部六字段reply、weights、W35、residual36、OPT38、customers71，与3518B主稿12类型按(A,B,T,D,E,S)完全一致；reply也与主稿一致。1441B`audit_residual_unique_bridge.py`字面嵌入该同一TYPES/REPLY，计算全部六行末位、六根利润、21含重复主题对，assert actual(16,19)/W35、唯一最优(2,5)/OPT38、遗漏36，stdout九字段设计与27原审计同形。

71原审计不读取296B文件，Path/BASE和product未用，无规范包/优化器依赖。它没有逐项检查296B的字段，不过当前相关源完整实读与静态指纹/结构对照可确认原字面数据相同。没有提供新的71审计stdout/运行事件，本批0执行；完整数学已由[主见证资源](残余桥两份整数见证的目标与完整回复版本--资源.md)所有矩阵与21对证明，不依赖缺失结果文件。

## 原入口的先验、优先权与当前用途

此50客户实例在其原稿中已经承认相关文献先有静态PNE失败机制；作者自称定义级交叉实现，不是独立外审，原文“独立审查由Boss另行实施”也不是已经完成的证明。本批是知晓来源结果后的实读与范围整理，不继承盲审身份。

本仓已有更小的[16客户三人实例](../反例/三人顺序SPE低于全部静态纯Nash福利--反例.md)，并有[12客户全部历史严格唯一实例及满支持版本](../反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md)。那些正文有自己的完整表与真实重放，已独立证明相同支配桥失败，并更强排“消平局/唯一SPE”修补；不能因此把本50客户动作表叫同一输入、从旧重放替本原程序认证或重新授桥失败新颖性。当前本资产用途是来源闭合、可重放的四人版本与可信末位切换机制。

根README将一般half记为OPEN，保的是当时研究状态；不能借此否定已经清洗的五人half等特定定理。源文献核对只作历史身份：Brethouwer论文§6.1 Theorem6.13/Example6.14和§7 shared-misery条件，Deng等arXiv:2307.07174v2的当时章节范围；本批没有重新访问网页或读取论文，不认证一般优先权或新的文献结论。原有限数学也不依赖外部福利定理。

最后的未付方向保留正确净差：若O为最优覆盖，R−G=OPT−W；要求匹配真实偏离查询支付OPT−W，比已失败的支付全部R弱。[71与27的精确见证](残余桥两份整数见证的目标与完整回复版本--资源.md)分别只需付3和1，强查询和却只35<36、13<14。源建议未来归纳保离轨从原C获取的份额、或非均匀跨枝收益，是准确的未闭合路线，不是本批已证一般付款、不变量或六人half。简单逐步/逐前缀非负的旧失败也不能自动否定带显式修复信用的所有净差方案。

本组仅五primary，五related只闭包；[完整原件/实际捕获/全20认领](../../tools/evidence/global-proof-residual-bridge-five-primary/README.md)与三正文、逐源收据、自查单独冻结。0原运行/import/新数学checker，无共享R写或Git，数学与done由Root分阶段提交。
