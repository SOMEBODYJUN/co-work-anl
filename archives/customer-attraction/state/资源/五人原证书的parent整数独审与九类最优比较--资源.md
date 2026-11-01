---
id: customer-attraction/five-provider-parent-integer-audit-and-nine-optimal-comparison-multisets
kind: resource
type_tag: 资源
title: 五人原证书的parent整数独审与九类最优比较
status: 原3848程序及1517报告全文实读；同59型raw充分旧上下文与5026实际成功复用，parent本批0运行
summary: parent用LCM1至m整数核32767真IC、792多重集OPT与九类最优的全部排列，原minQ与5026同而达者不同。完整解析private012及剩56/57给九类和840有序指派，基本J负差与相邻C正差分层；顶层数学后排他写不冒新run。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/parent/audit_strong_adjacent_integer.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/parent/strong_adjacent_root_integer_audit.json
---

# 同一个已核输入，第三个原实现

3848B原程序及1517B完整报告均正常show、核size/SHA/blob后全文读。输入只HERE.parent/credible/strong_adjacent_gap_attack.json：563651B/SHA96a9341a65e09f4423ce7dbcdfa4fd4cd6756939374d06f08cfdd6d5396a3b40，59正整数客户型及全部4681有序处方已在[完整原始证书与5026一次真实核验](../计算/五人原始相邻钱包证书的完整数据与一次核验--计算.md)全文实读/无损给定。这里精确复用同SHA完整上下文并保全原字节，不重扫大packet，不借十客户compact替它认证。

原5026一次exit0/新934同冻结/输入前后不变，是该输入的充分实际证据；[tree5339全矩阵](五人相邻钱包原证书的tree全矩阵独审与最优选择界--资源.md)此前完整码/报告也已读，但没有tree新run。本3848又是独立stdlib实现：不导入作者audit、canonical模型或solver；这种代码依赖事实不授本次新盲审、外审、新反例或新颖性。当前0本3848/其它数学入口、import、BI/LP或新收益IC checker。

## 模型、真实收益和冻结查询

有限共同集合目录、不同价值一客户、五名单位顺序行动者。兴趣型I重数n_I表示相应多个不同单位客户；终局z的c_I(z)=Σ_j1_(z_j∈I)，u_i(z)=Σ_(I:z_i∈I)n_I/c_I(z)，W(z)=Σ_(c_I(z)>0)n_I，OPT=max_(T∈目录^5)W(T)。完整SPE在每个有序h、每个当前替代动作，都沿同σ真实孩子完成比较当前利润；空主题、重复、零客户、任意平局属于一般模型，不删这些边界。本具体8覆盖互异/59正型已由原表证明。

实际z=(5,5,0,0,1)，固定其它实际角色的查询
\[
f_i(T)=\sum_{I:T\in I}\frac{n_I}{1+c_I(z)-\mathbf1_{z_i\in I}},\quad Q=\sum_i\max_Tf_i(T).
\]
分母正；这不是改动作再跟σ的真偏离。令ℓ_I为实际四条相邻角色边上从覆盖I退出I的次数，
\[
C_{adj}=\sum_{I:c_I(z)>0}\frac{n_I\ell_I}{c_I(z)(c_I(z)+1)},\quad
J_{base}=\sum_{I:c_I(z)>0}\frac{n_I}{c_I(z)+1}.
\]
两个预算在比较tuple及指派变化时均固定，不互换命名。StrongA要求Q−W≤C_adj；存在最优tuple/指派、每个最优指派、每个共同query及使用J的更宽预算都是不同命题。

# 3848的整数实现和输入边界

模块顶层读raw/全部数学/最后open('x')写parent/strong_adjacent_root_integer_audit.json，**无main guard**。排他写发生在全部计算与assert以后，拒覆不阻导入执行数学；本批只AST/文义阅读，未import。报告source_sha256是读原输入bytes算的，未给本3848代码SHA/原生argv/exit或耗时；本次文件SHA绑定不伪补成历史运行载体。

读endpoint.players/topic_count为m/k，并把每兴趣列表先转frozenset，检查非空、n为正int、兴趣标签为合法int；另显式检查k个客户覆盖向量两两不同。它没有tree5339的nonbool重数/原列表无重复标签检查：Python bool属于int且frozenset先去重，故不把该断言授为任意原始JSON严格格式解析。当前同raw均为合法正整数、兴趣列表不重复，满足各实现真实输入域。

sig字典键需等于全部有序长度0…m−1历史，且长度等于原actions数，拒重复history；动作只检查0≤a<k。该程序不单立endpoint.m/k与packet顶层m/topics、实际path与packet.actual_path、策略terminal_counts字段一致性assert，5026已核这些；它也未重读旧source40矩阵或LP对偶。不能把别的原检查记成3848自己的检查，当前确切raw已由前次充分认证。

取L=lcm(1,…,m)，本点L60。data(q)按终局计数缓存每标签的整数缩放收益Σn_I L/c_I；只为q_a>0标签填收益，payoff(z,i)查询的标签z_i必在该profile内，所以不误用缺席标签的零占位。所有终局有m角色，正覆盖数c∈1…m且整除L，故缩放确切；把冻结查询实现为替换实际一槽后再调用同终局payoff，仍有m角色。5026用lcm1…m+1、m5也60，C和J另用Fraction；规模相同不是同代码。

每个有序h调用finish(h)按原h续行，逐非规定a比较当前真实整数收益；只终局收益按计数缓存，不合并策略节点。原报4681历史、32767非自身IC、minimum_IC_slack_scaled=0；该字段是L倍整数，不是一般未缩放值，当前0除L仍0。随后核Σu=W，内算全部5×8冻结cost、每行max及最小标签破平局的chosen，但1517只存五行max和chosen，**不存完整矩阵/全ties**，完整矩阵另见tree资源。

OPT遍combinations_with_replacement(range8,5)全部792多重集，随后再次遍这些多重集，对最优者的set(permutations(q))全部角色指派求最低成本。这里允许重复主题，不是只枚56个五不同支持；也不是5026直接遍8^5=32768有序tuple。原报告九个最优多重集及全排列成本min的量词，与5026的840最优有序指派对应，解析分类如下。

# 九类最优多重集与840种有序指派的完整分类

以下只是从同一已认证59型表显示的本次解析后果，非1517原字段已经列出的九张表、非新数学run或新颖性。原表正private0/1/2分别4534396403094558、4173033154307888、22692106861683633，故任何覆盖宇宙的最优五槽tuple都必须含0、1、2。OPT=N，因为0,1,2,5已盖全部客户，余一槽可补合法主题。

逐原59行看，不被0/1/2覆盖的正型**恰**56、57、567，重数分别8818629371113047、4728154402593864、12598185837682839。因此余两槽须同时命中{5,6}和{5,7}。若含5，另一槽任意0…7；若不含5，只能各取6、7。其余所有兴趣型已有012之一覆盖，故此条件也充分。

|最优无序五元多重集|不同有序指派数|
|---|---:|
|0,0,1,2,5|60|
|0,1,1,2,5|60|
|0,1,2,2,5|60|
|0,1,2,3,5|120|
|0,1,2,4,5|120|
|0,1,2,5,5|60|
|0,1,2,5,6|120|
|0,1,2,5,7|120|
|0,1,2,6,7|120|

其中四种含一个重复标签，分别为a∈{0,1,2,5}，每种5!/2!=60；其余五类每种5!=120，合4·60+5·120=840。此处保“9个多重集”“840个最优有序tuple”“792个被枚多重集”“56个足以求覆盖OPT的不同支持”四种口径，不把它们当冲突或某个普遍枚举结论。

# 1517全部字段及与旧两实现的精确差异

players5/distinct_catalog_topics8、unit_customers_represented761588195074452900、positive_interest_types59、complete_ordered_histories4681、nonself_true_IC32767、minimum_IC_slack_scaled0、actual55001、source_sha256均原样保留。五真实利润为
\[
(142400688797178900,142400688797178900,
142353183896993025,142353183896993025,152516641360396500).
\]
五行max依次(152516641360396500,152516641360396500,152469136460210625,152469136460210625,152516641360396500)，fixed_maximizers=(2,2,2,2,1)是本程序重算后各行取首个最大标签，不是断言原LP固定查询是唯一最大者；tree全ties允许最后一行也选2。

|原1517字段|精确值|
|---|---:|
|W|722024386748740350|
|OPT|761588195074452900|
|Q|762488197001610750|
|adjacent_wallets|0，17765105218601400，0，19984015920010725|
|Csum|37749121138612125|
|StrongA_gap|2714689114258275|
|J|182175821951597100|
|common_static_surplus_gap_J|−141712011698726700|
|minimum_optimal_Q|630010849990532175|
|optimal_multisets|9|
|weak_optimal_assignment_gap|−129762657896820300|
|HALF_margin|682460578423027800|

原minimum_optimal_assignment=(1,0,1,2,5)，而旧5026顺序product选(0,1,1,2,5)。前两actual都是5，完整冻结前两行相同，互换所分0/1不改成本；两个都是最低成本达者。parent从set(permutations)枚举且只在严格更低时更新，不承诺lex最小达者；不能把元组差当数值矛盾或承诺不同Python版本按同一并列顺序写出。没有声称本1517与旧934字节相同，只有相关字段同值。

status=passed是原冻结声称，不是本次parent进程成功；arbitrary_half=OPEN为原全人数状态，当前五人half另已证/六人目标独立，不能用字段恢复旧全局边界；optimal_assignment_Csum_candidate=not_refuted_here准确指本点，后m≥7族已有一般存在性反例，不把本点min便宜升成一般桥成立。

原3848只显式比较packet的true_Q、Csum、true_signed_StrongA_gap三字符串并核gap>0及2W≥OPT；没有像5026合并核W/OPT等全标量，也没有tree的原true_maximizers属于全ties检查。其完整cost/真利润/C/J皆由当前endpoint重算，不用raw.source_frozen_payoffs旧seed矩阵，不能借源40表承重。

# 较宽J与三种相邻量词分流

同点Q−W−C_adj>0反StrongA；所有共同query价≤Q且query2在全部行同时达max，所以COMMON-ALL对C也失败。另一方面原J差Q−W−J=−141712011698726700<0，此点连rowmax都被较宽J付得起；字段名common_static_surplus_gap_J用的是rowmax Q，本点因共同2同时达max也可解释为共同价最大差。这个单点性质不挽救一般J全query命题，旧13人37/66属于另输入。

原parent只求最优指派**最小值**，所以它自身不测试每个最优指派是否通过。此前tree资源用该输入private0必选和完整endpoint矩阵得统一损δ，已显示所有最优指派均有Q_T−W−C_adj≤−7401263448959325；这与本min负差相容，却不是由min小推出all。十客户compact有坏最优指派且min可逃、后继m≥7连存在版失败，均为不同输入，不回填本五人原报告成新例/一般half反例。

[原件与闭包](../../tools/evidence/strongA-parent-integer-audit-two-primary/README.md)保本2源、同raw和旧成功/矩阵报告context；相同字段比较只是JSON值对照，九类/840及达者并列由上面显示推导承担。20XH实际claim pushed/synced e6219d33a7cf892816a8195f0984e9c110f4d41a，本次不借前批needs-attention状态；Root串行Git/checkpoint/done，旧冻件不改。本线程0共享R写、Git/start/claim/done/network/凭据/数学运行。
