---
id: "customer-attraction/joint-threshold-controller-and-root-exact-audit-assets"
kind: "program"
type_tag: "程序"
title: "异质资源产品的指定控制器独审与原始两尾枚举"
status: "complete-source-and-frozen-record-account; no-new-mathematical-run"
summary: "六参数给定控制器6708节点/240198含ownIC与七参数原始Fraction两尾枚举150912项分开；保144份完整孩子控制器及E2J1预算9，原读序、整数余量和仅数值修复费范围。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/counter/audit_joint_threshold_independent.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/counter/joint_threshold_example_independent_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/counter/joint_threshold_independent_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/root/audit_joint_threshold_example.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/root/audit_joint_threshold_example.py"
---

# 模型、原件与可复用数学

所有资源大小a,b及所述坐标份数均为正整数。三名单位权提供者依次观察完整有序历史。经济坐标有三个互不相交、每个含a名不同单位客户的资源，银行坐标有两个互不相交、每个含b名不同单位客户的资源；全部坐标客户互不相交。主题是每坐标选一个资源的完整Cartesian向量，客户由最终覆盖者均分。所有离轨末位平局保留，不能冻结未改变坐标的旧回复，也不把相同计数历史强制为同一策略。

本组五主源为8437B代码、10247B独审、4593B独审报告、108920B原research父方报告和4958B原research父方代码。全文实读代码的所有函数/顶层/guard、独审六节和两份JSON的所有字段；108920B报告的144条孩子见证及4320项末位策略表也全部展开读取。双冻结定位、size、SHA-256、Git blob和唯一原件去向见[清单](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/source-manifest.json)。10247B与此前保存的[同一相关原件](../../tools/evidence/pooled-successor-and-sharing-boundaries-primary/context/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/counter/joint_threshold_example_independent_review.md)逐字节相同，直接复用该原件。

等份q经济/q银行时，对每个强制根A，ell(A)是在A后所有完整纯尾SPE中根利润的最小值，M=max_A ell(A)。已自足证明

\[
\ell(A)=M=\frac{q(a+b)}2+\frac a2\max\{0,q-\lfloor qb/a\rfloor\},
\quad M_2=q(a+b/2).
\]

完整末位菜单、k/r/p下界、全部A的达到控制器、signed目标/退出叶区别与修复费用见[精确门槛定理](../定理/三角色异质资源产品的精确全强制门槛与修复节省--定理.md)。10247B的数学完全由该页承接；本程序资源新增的是原实现、原报告和准确计数/出处，不用有限PASS替代全参数证明。

b<a仅a整除qb才使连续值qa精确；a3/b1/q2虽qa/b整数，M仍7而非6。b≥a无需整除。节省a min(q,floor(qb/a))可为0，目标B=q(a+2b)>0。原稿写一般/五人OPEN是当时范围；五人现有[别证](../定理/五人半覆盖--定理.md)，本组没有六人half付款。

# counter代码实际核什么

[8437B源码](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/original/counter/audit_joint_threshold_independent.py)只导入stdlib itertools/Fraction/Path/json；没有仓库模型、作者程序、SPE solver、LP或随机入口。audit(a,b,q)自建不同整数客户编号，产生K=6^q个集合主题。三人负载仅1、2、3，payoffs6用6//load精确表示1/6收益，并断言利润和等于六倍覆盖。Fraction只作公式和输出精确分数，不使用浮点容差。

prescribed_second按b<a的floor或b≥a的ceil指定第二向量；prescribed_last对每个完整(root,second)历史先判断**整个第二向量**是否规定向量，再决定所有异银行坐标复制根或第二。该规则允许离轨未改坐标一起重选真平局，经济总取未用资源。

程序遍历K个根、各K个第二行动、各K个末位替代，检查规定末位在准确历史上的全部K个BR比较；缓存全部历史的规定收益。然后逐根核第二角色的全部K个联合偏离，规定收益至少M2，非规定第二收益至多M2；最后以根0为规定根比较全部K个根替代。它还断言每个强制根的**构造达到值**等于给定精确公式。因此该程序独立核给定控制器的完整SPE和公式达到；它没有枚举全部可实现尾SPE来重新证明最低M的反向下界，后者由10247B解析计数承担。

目标另取(root,root,last)=(全0,全0,全1)。它检查目标利润和末位全部K个替代，再在固定目标根下遍历第二×末位的K²终局，保全部末位BR，求max_second min_lastBR u2=M2。目标末位BR与费用代入不把目标前两人变成SPE。这些目标附加检查和M2枚举**不在**报告all_legal_IC_comparisons的三项计数中。

[4593B冻结报告](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/original/counter/joint_threshold_independent_audit.json)逐项保存：

|a,b,q|客户/K|M|M2|g1,g2|旧C/新C/节省|B/新总预算|strict IC|
|---|---|---|---|---|---|---|---|
|1,1,1|5/6|1|3/2|0,1/2|5/2,3/2,1|3,9/2|150|
|2,1,2|16/36|4|5|1,2|10,8,2|8,16|42156|
|3,2,2|26/36|13/2|8|3/2,3|15,12,3|14,26|42732|
|3,1,2|22/36|7|7|3,3|15,15,0|10,25|42732|
|2,3,2|24/36|5|7|0,2|10,6,4|16,22|42732|
|1,3,2|18/36|4|5|0,1|5,3,2|14,17|42732|

每输入决策节点1+K+K²；root/second/last计数K/K²/K³。K6一行43节点、258项，K36五行各1333节点、47988项；合6708节点/240198项，含6708项own、233490项非own。报告六行minimum_IC_gap均0，strict总213234。strict和gap是counter报告字段，不能移给没有这些字段的root报告。

# 原research父方raw BI及不等份输入

[4958B源码](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/original/root/audit_joint_threshold_example.py)另用单位客户的兴趣标签集合list表示输入，相同兴趣重复a或b次仍逐客户付一单位，未改变提供者权重。收益全部Fraction；无作者/规范模块、外部solver、LP或随机数。未使用的floor导入及局部rem不参与结论。源码没有参数schema验证器或命令行参数接口；这里只保main字面参数的精确有限域。

check(q,a,b,bank_copies=None)中q是经济份数，j=bank_copies是银行份数，默认j=q，K=3^q 2^j。对**每个**根A、第二B枚举全部末位C，以最大u3确定全部真实BR集合R(A,B)，theta(A)=max_B min_C∈R u2。枚举中B未预筛为第二BR。

随后保所有u2≥theta(A)的(B,C∈R)，在其中最小化根u1，得到ell(A)。此筛选是精确的：真实尾SPE的第二必须至少取得theta；反之，对任一所保叶，规定第二取B/末位取C，其它B′取真实末位BR中最低u2者，偏离至多theta，故是完整尾SPE。程序对该最小叶保存全部K个第二行动的末位回复，逐项断言这些回复属于真实BR集、规定第二不低于所有偏离；再检查每个ell等于公式、根0对K个根替代无改善。它是该有限三人实例的原始两尾完整枚举，不是任意人数SPE solver。

q经济/j银行的实际断言为

\[
M=\frac{qa+jb}2+\frac a2\max\{0,q-\lfloor jb/a\rfloor\},\quad
\theta=M_2=qa+jb/2,
\quad\Psi=\max\{qa,(qa+jb)/2\}.
\]

这与已证等份式及[E/J字典整数式](../定理/异质EJ字典的全半轴菜单与精确最优预算--定理.md)一致。其解析原因仍是U=(qa+jb)/2+(ak+bp)/2、V=(qa+jb)/2+(ak+br)/2、r+p≤j和第二保底qa+jb/2；故k≥max(0,q−floor(jb/a))。不足银行资本时取该数经济非根并奖励全部银行；资本足时取ceil(qa/b)个奖励银行、经济全复制，离轨银行复制第二即达到。这里只解释源码所断言的真实合同，不把main七点外推为穷尽所有整数运行。

共同价格dual在[0,1]及[1,∞)各为一条线，后一段斜率−jb/2<0，所以源码比较τ0、1足够计算**此已解析家庭**的Ψ；这不是对一般菜单只抽两个价格。原目标利润为((qa+jb)/2,(qa+jb)/2,qa+jb)，W=2(qa+jb)、OPT3=3qa+2jb、B=qa+2jb>0。旧C=5qa/2、新C=2(g1+g2)+g2、节省a min(q,floor(jb/a))；源码只核这些数值，不重证一般signed修复定理。

# root冻结报告的全部输入和策略闭包

[108920B完整报告](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/original/root/audit_joint_threshold_example.json)七行如下，参数顺序统一写(q,j,a,b)：

|q,j,a,b|客户/K|M/Ψ/余量|M2|旧C/新C/节省|B/新总预算|terminal/完整IC|
|---|---|---|---|---|---|---|
|1,1,1,1|5/6|1,1,0|3/2|5/2,3/2,1|3,9/2|216/258|
|1,1,1,2|7/6|3/2,3/2,0|2|5/2,3/2,1|5,13/2|216/258|
|1,1,2,1|8/6|5/2,2,1/2|5/2|5,5,0|4,9|216/258|
|2,2,2,1|16/36|4,4,0|5|10,8,2|8,16|46656/47988|
|2,2,3,1|22/36|7,6,1|7|15,15,0|10,25|46656/47988|
|2,2,3,2|26/36|13/2,6,1/2|8|15,12,3|14,26|46656/47988|
|2,1,1,2|10/18|2,2,0|3|5,3,2|6,9|5832/6174|

每行full_child_witnesses有K条，root_action恰0…K−1；每条给next_action、last_action、root_profit、next_profit、theta和长度K的last_action_for_each_next_action。最后一项在所选next位置必须等于记录last_action；144条见证/4320项末位动作都保在原JSON，没有只保存一条在轨路径。动作标签按经济向量外层、银行向量内层的itertools.product字典序解释，root_action0定义完整根策略。报告可能next_profit>theta，例如a1/b2/q1时5/2>2，a3/b2/q2时17/2>8；可信筛选是≥，不能误改为等号。

原代码的all_terminal_profiles计K³，last_action_comparisons_plus_next_IC计K³+K²：前一部分是对全部末位终局收益的max/全部BR分类，再加K²项第二IC；没有逐项记录counter那种chosen-minus-alternative gap。complete_strategy_IC_checks再加K项根IC，仍含own。七行合146448终局分类、4320项第二、144项根，总150912；决策节点从维数算为4471，分别含7根、144第二、4320末位节点。该4471也是概念上own总数，报告自身没有decision_histories字段。

E2J1就是q2/j1/a1/b2，不是counter的等份q2。它有18主题、5832终局、6174完整IC，M(2,3)、目标(2,2,4)、预算9；与字典x=2/3清分母精确对应。没有用此6174替代counter六参数或signed作者单点。

# 独立性、版本和本次验证的准确边界

10247B独审先只收父方/signed精确合同，独立推k/r/p和门槛，之后才收到作者动作规则及目标/费用，完成时未读作者全文或代码。这是相对作者全文的合同独审，先验不是零；旧跨组件平局机制归R44，非首次/外审/新颖性认证。独审只数值核一般修复函数在本例的代入。root源码/报告的independence字段另声明原research父方只用raw兴趣与Fraction、无作者或canonical导入；代码确无该导入，人的阅读史仍是原来源声明，不能由程序自动认证。当前清洗者已读作者稿及既有正文，是知情整理。

counter main六参数/字段与冻结报告一致；root main七参数和全报告亦一致，未发现默认main与保存记录输入域冲突。两份原main都在guard内执行、写源码所在目录的同名JSON；root stdout仅打印选定摘要，108920B完整报告由write_text保存，不能把stdout摘要冒成全报告。import本身不执行数学入口；本次也没有import或运行源函数。

[本次核对](../../tools/evidence/joint-threshold-controller-and-root-audits-primary/frozen-data-and-integrity-check.json)只解析AST、读取全JSON、核全部保存标量公式/数组维数与标签范围、逐原件size/SHA/Git blob及10247B原件同一性。不调用收益、BR、IC、controller、BI、LP或原main；新数学运行0。原冻结PASS可连同全参数解析证明继续使用，但两原报告没有绑定源码SHA的历史执行journal，本次不补造旧argv/时间，也不把静态相容写成重新运行成功。

此前精确门槛定理和共同池资源中的“四程序/报告missing”保留其原批时点。本组现在恢复counter代码/报告与root代码/报告，仍没有在此冒领signed作者另一对程序/报告；后者由其逐源资源处理。作者单点1333/47988、counter六点6708/240198和root七点150912是不同实现/输入，重叠输入不能相加成更大搜索覆盖。

关系依据为：共同目录定义提供收益和完整历史量词；精确M定理给全参数下界/达到证明；本资源两程序分别实现指定控制器核与raw两尾枚举；E/J字典对象给末行预算9的归一化接点；共同池接口仅提供上帽及有限修复充分条件。每种联系保持同一模型/目标，均未推出六人half。正式超图仍留第三阶段。
