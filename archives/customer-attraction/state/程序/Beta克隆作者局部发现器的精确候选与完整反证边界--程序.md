---
id: customer-attraction/beta-clone-author-local-discovery-lp-and-exact-candidate-boundary
kind: program
type_tag: 程序
title: Beta克隆作者局部发现器的精确候选与完整反证边界
status: original-code-helper-and-full-report-read; no-replay
truth_status: existing-fixed-fresh-policy-lift-refutation-retained; weak-lifts-not-settled
review_level: informed-source-contract-and-stored-candidate-analysis
scope: three-regular-local-background-template; full-directory-proof-is-separate
summary: 原3519发现器以21类型22变量共同余量LP提出候选再精确12IC和4严格行复核，560十字段完整保存；3048收益依赖实读，非singleton或全clone树运行。
source_ids: [6b7c6492a5091957e478, 8166811e061cdd0f3755]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/attack_beta_clone_local_lift.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/attack_beta_clone_local_lift.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_local_lift_attack.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_local_lift_attack.json
---

# Beta克隆作者局部发现器的精确候选与完整反证边界

两primary为3519B原发现程序和560B完整原报告，共4079B，均已actual normal取得、全文理解。它们补全[固定fresh合同反例](../反例/Beta克隆固定策略提升的不可补全局部合同--反例.md)引用的发现过程；现有解析反证仍在原对象，不把已证反例重授为新定理。当前原CLI/import/LP/有理重验/模式展开/单位展开/IC及新数学程序运行均0。

## 原入口真正搜索的有限合同

程序有main guard，但普通import也会加载numpy、scipy.optimize.linprog以及同目录probe_beta_clone_lift.original_pay/clone_pay。numpy以np导入后未使用；没有项目完整SPE求解器。HERE=Path(__file__).parent，main不处理argv、不读输入JSON；客户权重由内部LP产生，输出固定覆盖同目录beta_clone_local_lift_attack.json。不能将此程序说成stdlib或与独审不导作者的代码同一实现。

原主题0/1/2记A/B/C。TYPES按B=1,…,7、b=0,1,2的字典顺序列21种类型；B为接受哪些regular的三位掩码，b是原固定整数背景。一种类型的权重是该类单位客户数的有理重数，不是玩家权。类型B0不在搜索域，背景≥3亦不在域。搜索仅有regular三主题，未在此处增加P_x实现历史或完整clone单位客户目录。

固定原前缀A（count e0），尚余当前和末位两人。terminal(a,t)=e0+e_a+e_t保留首A的拥挤。对每个候选末位回复映射r=(r0,r1,r2)∈{0,1,2}³，令

\[
 d_a=O(e_0+e_a+e_{r_a},a),
\]

这里O是21维逐类型精确原收益系数，实际向量点客户重数即利润。每个a加入三个末位比较

\[
 O(e_0+e_a+e_{r_a},r_a)-O(e_0+e_a+e_t,t)\ge0
 \quad(t=0,1,2).
\]

选定当前s∈{0,1,2}后再加d_s−d_a≥0。共12行：9末位、3当前，含3末位self和1当前self；原三regular局部树实际只有4决策节点、8个非self比较。不枚举39主题背景全树，也不核首A玩家或更早祖先的当前选择。

## 已实际normal取得的收益依赖

必要同目录probe_beta_clone_lift.py共3048B已另actual normal取得并全文读，只作related，不在本包额外done。author只从中导两个构造器，模块有main guard，导入不会运行其随机probe；当前也没有导入它。

original_pay(types)返回带lru_cache的pay(q,a)，对B包含a的各类型加w/[b+Σ_(j∈B)q_j]，正是原合法背景下**单个当前玩家**的收益。这里代码接受的是给定背景，不负责证明这个背景由早期共同目录行动生成。author每次为各(B,b,1)建一个闭包取系数。

clone_pay(types,clones=3)将a//3投影原主题。对当前clone使用次数own=q[a]，其它已被使用且与该客户相关的clone次数组成others，令d=1+len(others)。同一clone的own名使用者共享一个兴趣指标，不能用own个独立Bernoulli替代。b0时per=1/(own+Σothers)；b≥1逐其它标签子集mask、s=|mask|计算

\[
 \frac{b(s+1)!(b+d-2-s)!}{(b+d)!}
 \frac1{\mathrm{own}+\sum_{j\in mask}n_j},
\]

再对mask求和、乘类型重数。首因子是该当前标签被含、恰mask这些其它**不同标签**被含的Beta积分质量，已经含当前指标的概率；分母仍按重复使用者次数，不是按不同标签数。它以精确Fraction/factorial求积分边际，没有采样客户或列举全部9标签pattern，更没有在这里清分母展开单位客户。当前author调用处的own恒正。

依赖文件还完整保有add/fresh和reachable：后者按count状态缓存全部可实现终局，bound=max_a min_(z∈child_a)pay(z,a)，保孩子中当前收益≥bound的终局。它的guarded main另用Random(2601024)、n=2/3各150次、三玩家/每主题3clone、类型背景randint1…4和重数randint0…9，比较原SPE计数的canonical fresh映射是否可实现并查重复clone SPE；首发现覆盖beta_clone_probe.json，否则报有限阴性。author没有调用这些随机/集合值BI函数。本包未取那几份probe报告，不将依赖全文读取扩成它们已处置、旧300输入已审或重新BI成功；相关未处置程序/报告可另作primary接续。

## 重复孩子和严格共同余量LP

clone有每regular三个标签，编码a*3+j。前缀固定A0，当前偏离为再选A0；末位原主题last仅试B或C，即last∈[1,2]，选其clone0。重复叶z=2e_A0+e_(last,0)。令C(z,c)为精确clone逐类型收益向量，则strict的首行是

\[
 C(z,A_0)-d_s,
\]

其余行比较选定末位与fresh A1、fresh B0、fresh C0、重复A0四代表，跳过与last同原主题的代表。因此strict恰4行：一个当前盈利差和三个末位严格优差。未用的同主题其它fresh clone在此固定重复前缀下对称；代表类别足以做三regular局部模板，不能据代码认为P_x或全部补充目录已被程序扫过。

每个模板的LP有21个w和共同margin t共22变量，全部bounds≥0，另Σw=1；12个普通约束row·w≥0和4个严格族约束row·w≥t，共16不等式、一等式。源码转为HiGHS浮点矩阵并最小化−t。回复映射27×当前3×last2给最多162次LP；按源码嵌套顺序遇首个精确接受候选便return，所以这个数不是已发生调用数或全局最优性声明。

成功且sol.x[-1]>1e−8后，每个浮点w单独转Fraction(float(v)).limit_denominator(10**6)，重新以精确有理点积核全部12行≥0及strict四行>0；失败就continue。它没有用float positive margin直接发结论，也不输出对偶/最优界。各坐标舍入后没有另断言Σw=1或w≥0；具体560B报告列出的全部非零整数重数均正，故本实际输入没有负客户问题。齐次约束也不需要把舍入后总质量强行恢复为1。

用所有有理分母的lcm乘回整数wi，再输出非零(B,b,wi)。这只是原类型权重的清分母，不是后续2520全clone构造或独审60倍单位展开，代码也未以gcd求最小见证。所有12/4精确复查只属于三regular局部合同；不等于原full SPE、单位pattern、合法singleton背景或全clone目录认证。

## 完整原报告十字段

|原字段|完整原值|
|---|---|
|status|`"exact_local_fresh_lift_counterexample"`|
|types|`[[3,0,36],[4,0,3],[5,1,36],[6,0,10]]`|
|prefix_original|`0`|
|original_last_reply_after_current|`[1,0,0]`|
|original_current_action|`0`|
|clone_last_reply_original|`2`|
|original_current_payoffs|`["24","22","22"]`|
|clone_repeat_payoff|`"25"`|
|minimum_original_IC|`"0"`|
|minimum_strict_gain_or_reply_margin|`"1"`|


原types四项全部为：

|B|原兴趣|b|单位客户数wi|
|---:|---|---:|---:|
|3|A,B|0|36|
|4|C|0|3|
|5|A,C|1|36|
|6|B,C|0|10|

总85客户；未列17种类型重数为0。prefix_original=0表首A；replies[1,0,0]给A/B/C后的末位B/A/A；selected=0是当前A；clone_last_reply_original=2是重复A0后的末位fresh C0。报告原收益24/22/22、repeat25、原IC最小0、严格族最小1，与代码positive分支字段结构吻合；报告没有代码hash、依赖hash、argv/cwd、exit、运行耗时、solver版本、实际LP次数或stdout轨迹绑定。当前仅实读与解析，未以新run认证其历史产生过程。

按现有原定稿手算，9个末位IC行在a=A/B/C分组分别为(1,0,0)、(0,7,4)、(0,4,23/2)，再加当前行(0,2,2)，最小0。零包括self和A后B/C的真实平局，非“都严格”。重复后末位C23对fresh A22、B22、repeatA18，strict按源顺序为(25−24,23−22,23−22,23−18)=(1,1,1,5)，最小1。这组解析余量解释报告两个minimum字段，没有再跑21系数/12IC/LP。

## 从局部发现到真实反证仍需哪些解析步骤

作者7027B定稿另给每个AC客户一个共同目录P_x={x}，依次选择36次实现其背景1。再余3人、首A，hA为合法离轨两人子局；原39主题/39人完整策略通过其余孩子和祖先BI补齐。P_x收益≤1、C单靠13个背景零客户保证13/3，排除新增动作。**没有证明h或hA为根实际路径**。发现器21类型矩阵本身没有执行这些补齐或产生有序全树动作证书。

全clone标准单位实例由作者另将每原主题造3clone：每AC客户涉及A/C/P_x共9标签，各非空pattern质量1/[10 C(9,|R|)]，2520清分母、空兴趣删去；B三标签同覆盖须商。所有singleton clone总质量1/2，末位所有未用A/C按fresh类别、repeatA0单列，故全部真BR为某C，当前25>指定fresh叶24。原发现器使用精确Beta利润函数，不构建这份完整单位客户清单。

[已冻结独审程序页的本次比较快照](../../tools/evidence/beta-clone-author-local-discovery-two-primary/comparison/archives/customer-attraction/state/程序/Beta克隆独审的六十倍单位实现与真实双回复--程序.md)另保40目录/60倍/5100含empty的独立实现，不导本发现器。其完整真回复表还显示fresh A1后B0/C0均为末位BR22，但当前24/27；重复A0只25。故此处失败精确是逐项保留给定原σ在**所有fresh历史**的行为，特别保A1→B0。允许换fresh回复C0可使本较小局部合同给当前27，不能把25>24扩成优于全部fresh后继或一般clone无SPE。

静态[非负背景表示](../等价/Beta克隆对背景利润的非负静态表示--等价.md)及受限fresh树SPE仍成立。重复叶当前25≤原投影AAC背景27，[同叶复用债](../引理/Beta克隆的单次增益与复用上尾债务--引理.md)与跨不同叶25>freshAAB24相容；上尾后来已获父审，但不自动给跨树付款。较弱的只保原实际叶、或某clone SPE覆盖≤原背景剩余总利润，仍未由此判真/假，也没有half反例。

## 输出、先验与本次去向

成功分支写json.dumps(out,indent=2)且不补LF，再print紧凑默认json.dumps(out)并换行；stdout与文件按代码本来就不同格式，不要求字节相同。全模板无接受候选时仍覆盖同一文件，只写status=no_separation_in_exact_local_template和scope="Finite template computation only, not a proof or negative evidence."，再print；该分支未在本560B报告发生。程序未捕获LP/导入/写文件异常，不拒绝已有文件，无独立运行日志。

作者原定稿明确发现器只提出类型，后续父审先手算后读定稿，direct先接四类型/局部σ/合同而未导发现器；当前先已知这些源再读3519/560，是知情清洗，不新blind或外审。原未留下的独审Markdown不补造；[版本审查](../审查/Beta背景表示的版本与两份单位实现边界--审查.md)中当时“程序未读”是旧时点，本次补真实代码/报告，不能倒填早期已核。

两primary均retained到本程序对象与[真实来源闭包](../../tools/evidence/beta-clone-author-local-discovery-two-primary/README.md)。15XD完整15ID claim pushed，raw local_sync=needs-attention和38untracked+2tracked零差proof/stash并列，未将raw改为synced；只处置本2、不额外done依赖或旧对象。本次不导入/运行原程序、LP、有理系数、clone模式/单位客户或SPE，不重旧成功。
