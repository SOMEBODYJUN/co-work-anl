---
id: customer-attraction/minimum-sequential-static-pne-bridge-exact-finite-negative-search
kind: program
type_tag: 程序
title: 最差顺序与静态PNE桥的精确有限阴性搜索
status: complete-two-source-reading-and-search-scope-accounting
truth_status: 原603计数有限阴性包保留；一般候选已由既有严格反例否定；无新原运行或一般证明
review_level: 全码全JSON与实际规范依赖实读复用；三边界解析核对；不冒原进程重放或盲审
scope: 有限共同目录单位玩家、全历史纯SPE与全部静态PNE；主搜索2至5玩家/3至5标签，含空覆盖与别名边界
summary: assess以全部SPE最低福利对比全部静态PNE最低福利、命中才展开并verify一棵最差证书。seed606/600随机加3边界的null报告不是桥证明；-O跳过边界调用但checked仍计3，方法assert_valid命中校验不因此去掉。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/static_bridge/search.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/static_bridge/search_result.json
---

# 最差顺序与静态PNE桥的精确有限阴性搜索

3547B原程序和167B结果均正常取得，逐份完整实读，size/SHA256/blob与当前Boss4认领一致。它只攻击辅助候选

\[
\min_{\sigma\in\mathrm{pure\ SPE}(I)}W_I(\sigma)
\ \ge\ \min_{p\in\mathrm{static\ PNE}(I)}W_I(p),
\tag{B}
\]

没有测试一般half。结果记录seed606、600随机试验预算、checked603、status="finite search only"和counterexample=null。该有限过程资产值得保留，但(B)早已被现有完整反例否定，不能把这份阴性包提升为证明或当前开放状态。原字节、全部字段和实际捕获见[证据包](../../tools/evidence/static-bridge-search-two-primary/README.md)。

## 共同模型与两个最小值的精确含义

有限单位客户按兴趣类型的正整数重数表示，m名相同单位玩家各选一次共同标签，终局客户价值在覆盖者间均分。Instance接口允许空覆盖题、覆盖相同的不同标签、零客户及兴趣为空的客户行，标签名字互异；m>0须至少一题。实际静态桥反例可以在非空互异覆盖集合域内成立，边界测试不是改变原严格反例的模型。

计数c下选择占用主题a的玩家获

\[
U_a(c)=\sum_{T\ni a}\frac{w_T}{\sum_{b\in T}c_b};
\tag{1}
\]

只对c_a>0查询其当前收益，故分母正。静态改a→b后必须用c−e_a+e_b重新算U_b；即使b=a也作为合法自行动比较。全部原有序历史和任意平局由规范SPE求解器保留，静态PNE的压缩计数只是相同单位玩家的终局匿名性。

完整纯SPE至少一份，因为这是有限完美信息一次行动博弈，可逐层逆归纳；静态PNE至少一个，因为调和势

\[
\Phi(c)=\sum_T w_T H_{\sum_{a\in T}c_a},\quad H_0=0
\]

在单人改题时的变化等于其收益变化。客户仅喜欢旧题时势失去该玩家旧份额，仅喜欢新题时增加新份额，同时喜欢两题则总人数及其份额不变。有限终局中势最大点没有严格盈利偏离，所以PNE非空，包括零收益/别名边界。这说明两个有限最小值有意义，不靠源中的assert替数学存在证明。

设s(I)为左侧、n(I)为右侧。因为两者均达到，(B)等价于：对同实例**每份**完整SPE σ，都能找到某个静态PNE p使W(p)≤W(σ)。若(B)成立，取最差静态p即可对所有σ；反向取最差SPE得n(I)≤s(I)。它强于“SPE终局也许不是PNE”，与CCE、同时混合Nash、iid安全基准或静态OPT各不同。

## 全部静态PNE和全部顺序终局

`compositions(n,k)`按首坐标0,…,n递归，k=1输出(n,)，对n≥0/k≥1完整枚举总和n的全部k维非负计数，各一次，数量\(\binom{n+k-1}{k-1}\)。`static_equilibria`对每c算全部占用主题收益，对每个c_a>0、每个b测试

\[
 U_b(c-e_a+e_b)>U_a(c).
\tag{2}
\]

遇一条严格盈利偏离便排c、短路其余项；否则yield c。等号不排除，重复题、自行动、空题及别名均保留；不必枚举相同计数的所有玩家排列。返回全部静态PNE计数列表，源没有只取某个好PNE或某个局部搜索结果。

本程序的精确判别域要求k≥1，main及三个边界均满足。规范Instance另允许零玩家空目录，但compositions没有k=0分支，不能把上述合同无条件扩到那个实现边界。

顺序最差福利来自规范ExactSPESolver的全部SPE可实现终局计数R(k)。终层R(z)={z}，非终层令

\[
L_a(k)=\min_{z\in R(k+e_a)}U_a(z),\quad M(k)=\max_aL_a(k),
\]
\[
R(k)=\bigcup_a\{z\in R(k+e_a):U_a(z)\ge M(k)\}.
\tag{3}
\]

当前偏离的真实子SPE利润不低于其最小L_a，给必要性；反向actual孩子保目标、其它孩子各挑达到最小当前利润的合法子SPE，在不同有序子树独立拼合，给充分性。按计数缓存的是可实现**集合**，没有要求同计数的不同有序历史使用同一动作或同一平局。最终福利仅依赖计数，所以在R(0)取最小等于在所有完整SPE策略中取最小，不需要枚举全部策略动作图。

`assess`先建solver，再完整列eqs，assert eqs，计算`sw=solver.minimum_welfare()`和`nw=min(welfare(c) for c in eqs)`。仅当sw<nw才返回见证，否则None。它是固定合法输入上对(B)失败的精确判别；与此前同时测试PNE/RESIDUAL、可能先返回RESIDUAL的`scan_bridges.check`不同，这里没有其它类别遮住后面PNE，也不依赖frozenset遍历时先遇哪个SPE终局。

## 命中才生成最差证书

sw<nw时调用worst_certificate：规范实现先在全部最差福利终局计数中取字典序最小，再用certificate展开一份完整有序动作表。默认合法actual动作/离轨极小利润目标选择足以实现该终局；它不枚举全部完整SPE，也不声称均匀随机取策略。

随后调用verify_certificate(instance,cert)，再report.assert_valid()。该规范校验检查动作表完整性、声明terminal_counts、全部有序历史的原动作与每个偏离后的真实后继；不强迫同计数历史一致。`assert_valid`方法内部是if not valid后显式raise ValueError，**并非Python assert语句**，因此命中路径在−O下仍会执行这个方法与异常检查。

返回counterexample六字段：instance、spe_welfare、minimum_pne_welfare、all_pne_counts、optimum、certificate。all_pne_counts是本输入完整静态计数列表，optimum另由有限至多m支持的静态覆盖枚举得到，不等同于最低PNE或默认总客户数。负报告没有这个对象，不能说本次167B资产已经经过某棵正例证书的校验，或把未走到的代码路径当原执行成功。

## 三个边界的全部数学

main先构造三份边界实例，逐个`assert assess(ins) is None`再checked+=1。它们不是三份随机正权输入；每个都可以不运行而从定义确认：

| 边界 | 原输入与全部 relevant 均衡性质 | s(I),n(I),OPT |
|---|---|---|
| 零客户单题 | 一个标签empty，无客户，1玩家。只有计数(1)，所有利润与覆盖0；唯一SPE/PNE都该计数。 | 0,0,0 |
| 无兴趣客户 | 一个标签empty，一行空兴趣集合含2个不同客户，3玩家。两名客户都不喜欢任何题，无论行动均不覆盖；只有计数(3)，利润与覆盖0。客户总数2不能当福利2。 | 0,0,0 |
| 空题与两别名 | from_topic_sets([∅,{0},{0}],3)给一个单位客户喜欢题1/2、题0空覆盖，标签各异。任何选择题0的静态玩家可改覆盖题获正利润，故PNE恰c₀=0、c₁+c₂=3的四计数。顺序任意历史中改空题得0、覆盖题必获≥1/3，所以所有SPE也每位选1/2；任意实际标签混合可实现。 | 1,1,1 |

第三边界中same-covered标签是动作别名，不能合成两个不同客户；玩家重复/分散选择这些标签均覆盖同一名客户。所有收益相同不妨碍完整历史自由破平局，恰是规范接口要保的边界。以上是本次解析说明，不是重新执行三份边界或新Fraction程序。

**计数有−O区别。** 三次assess调用写在assert表达式内部，优化解释器会连调用一并去掉，checked+=1却仍运行，因而报告仍可写checked603。构造边界Instance的列表仍会求值，但不等于assess已评估它们。`assess`里的assert eqs也会去掉，数学PNE存在保证正常合法输入的min仍有值；命中后的report.assert_valid方法调用则保留。不能笼统说所有校验在−O下都执行，或都不执行。

## 随机域、完整预算与输出

main受`if __name__=='__main__'`保护；import只载入标准库/规范包和定义函数，不启动搜索。本次未import。argparse三个参数：--seed整数默认606，--trials整数默认600，--output为必填Path；seed/trials无额外非负检查，trials≤0使随机循环为空而边界循环仍计3，不是一个拒绝模式或真实负数试验。

Random(seed)每轮先k∈{3,4,5}，再n∈{2,3,4,5}名玩家；对每个非空mask，以概率分支.5决定是否调用randrange(8)，否则置0。即使进入该分支也可能得0，最终只保存正重数1,…,7；非零率的抽样机制是.5×7/8=7/16，并不是每个类型必以.5出现。每mask一次、无重复行；可能无客户、空覆盖题或不同标签覆盖一样。600是随机输入预算，不是12个人数/主题组合全枚举、不同实例数或所有类型权重域穷尽。

每轮assess后checked加1，首个counterexample真值即break；相同输入可能重复。`checked`计输入调用迭代位置，不是SPE策略数、终局数、PNE偏离数或全树校验数。每个随机输入的全SPE/全部PNE判别都是精确的，不会把有限采样提升为全输入量词。

结束构造六字段result：candidate固定(B)字符串、seed、checked、trials_limit、status（refuted或finite search only）、counterexample（完整命中对象或None）。输出用args.output.open('x')排他新建，json.dump ensure_ascii=False/indent2，主动加末换行；无父目录创建，目标已存在会失败而非覆盖。stdout另打印去counterexample后的**五字段**单行JSON，不含进度流、完整证书或每输入明细。

原doc要求从仓库根运行，且须使规范包可导入；源码没有自行改sys.path、安装依赖或从__file__猜根。只有标准库和规范包，无NumPy/SciPy/LP。实际闭包是__init__691B、model8640B、exact9943B、certificate6201B共25475B，已有充分完整实读、本次current同SHA绑定；Fraction和itertools.product在这份程序里未直接用，精确分数来自model/solver。没有外部实例/JSON输入、没有读取本167B结果。

## 167B原报告的全部记录和版本边界

原六字段逐项为：candidate="min SPE W >= min static PNE W"、seed606、checked603、trials_limit600、status="finite search only"、counterexample=null。与源码默认600加3个边界的**字段设计**一致，没有kind=PNE实例、任何实例列表、all_pne_counts、spe_welfare、optimum、certificate或逐输入结果。

在普通解释器且原代码按此seed/limit正常走完的条件下，603表示600个随机输入加3边界、未返回正例；在−O下也可有相同603但少三次边界assess。原包没有argv、解释器优化模式、源码SHA绑定、时间、stdout/stderr、exitcode或运行环境，所以本批只保存其有限阴性声明和源码兼容性，不冒称已经重放、验证seed606的600条轨迹、或排除任何未给域。默认值与显式传同值参数也不能从包中区分。

代码仅在main尾写结果，未附命中说明时counterexample=null就是“这份报告没有正例”，不是候选真。源码还显式写这不是一般half测试，不能因为随机试验无命中就把一般half当有证据接近成立。

## 同一生成支持内已有严格反例

本仓[全部历史严格唯一的12客户例](../反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md)有3玩家、4主题，正类型A3、AB3、C1、AC1、BD1、CD1、BCD2，总12。它的完整21历史策略每个节点严格，唯一SPE福利11，唯一静态PNE计数ABC福利12（所有排列同样静态稳定），OPT₃12。因此(B)严格失败，连消除平局/要求唯一SPE的修补也失败。

这个输入的人数3、题数4和每正类型1,…,7都在当前main允许的生成支持内；并非用超出此搜索域的带权或不同目录反例否定它。有限seed606的600次null报告可以错过这个合法输入，不与既有证明冲突。当前不再跑它来重复已有完整验证，也不称新发现、全局最小或本程序已找到它。

另[16客户三人非严格版本](../反例/三人顺序SPE低于全部静态纯Nash福利--反例.md)及[50客户四人原证书资产](../资源/全局覆盖入口的静态PNE证书与净差合同--资源.md)有自己的完整数据、策略和审计身份。不能因同一候选已假，就把167B文件替换成它们的正例报告，或借那些原程序成功给本3547B源码冒同SHA运行。正反资产保留的是各自真实时态与用途。

## 认领与保全

22XT完整22源claim实际status=pushed，remote_tip `26ab863135a398ab834f336fec5570fb382d9b76`；本两件Boss4/in-progress与原SHA一致。原local_sync=needs-attention保留，独立proof中3untracked/2tracked全same、无missing/different/unmerged、stash保留另存；不伪称synced，也不借上一批2+2替代本次3+2。

本次0原main/assess/static_equilibria/规范import/DP/verify/新数学checker、0网络/Git/共享R写。新增的是完整程序/报告语义和三边界解析说明，不伪造600试验事件或新PNE认证。全部原字节/两normal/完整claim/proof/逐源receipt独立冻结，由Root先数学checkpoint再逐源done。

## 2026-11-02：五人五题保存原图的精确桥反例

[56客户五人完整原图](../反例/五人五题五十六客户的顺序与静态最低福利分离--反例.md)现正式处置Rd28原93093B报告：781个字面历史原动作全部保存，3905含自身比较精确非负；126个静态计数仅一PNE型W56，而原两根SPE计数的最低福利54也由252状态集合递推核同。它严格否定本页搜索所针对的同实例最低SPE不低于最低PNE桥，且half余额52仍正。该桥已有三人反例，此五人原件不主张更早或更小；本页有限阴性报告的旧运行身份不变。
