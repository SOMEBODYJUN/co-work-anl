---
id: customer-attraction/beta-clone-finite-probe-set-valued-contract-and-four-report-versions
kind: program
type_tag: 程序
title: Beta克隆有限探针的集合值合同与四份报告版本
status: full-code-four-reports-reviewed; no-replay
truth_status: finite-logs-and-repeated-outcome-candidate; no-universal-lift-conclusion
review_level: informed-source-version-and-set-recursion-analysis
scope: fixed-three-player-three-clone-default-vs-unbound-mixed-and-four-player-records
summary: 3048原程序同SHA复用与四报告1748B完整主读；集合值递推不强迫Markov策略，mixed九重复count与空fresh失败分离，四人记录不冒当前main生产。
source_ids: [8ef2bf0e6d9fef6e4d5e, 41bf99bd30010891eae1, ec742900e800a05e8d71, 49e9a6f407d48fcd10f7, a9e917fb69a7ec1303cf]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/probe_beta_clone_lift.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/probe_beta_clone_lift.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_mixed.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_mixed.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_n3r4.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_n3r4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_r4.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_probe_r4.json
---

# Beta克隆有限探针的集合值合同与四份报告版本

本包五primary实际共4796B：3048B原程序、128/1379/120/121B四报告，合计以actual manifest逐字节为准。程序此前作为[作者局部发现器](../../tools/evidence/beta-clone-probe-and-four-reports-five-primary/comparison/archives/customer-attraction/state/程序/Beta克隆作者局部发现器的精确候选与完整反证边界--程序.md)的必要收益依赖actual normal取得并全文读，本次同SHA精确复用，不新show、不再执行；四报告本次新normal完整主读。本次CLI/import/BI/随机样本/LP/IC/clone模式/单位展开/新数学程序运行全0。

## 当前3048入口的实际域与副作用

程序只stdlib Fraction/lru_cache/itertools.combinations/factorial/json/random/Path，combinations未使用，不导项目求解器、SciPy或作者LP。main guard使普通import只定义函数/常量，当前未import。无argv解析/输入文件或输出路径选项；HERE取源码所在目录，输出固定beta_clone_probe.json覆盖，不拒绝已有文件。

一个Random(2601024)跨全循环共享：先n=2的150个case，再n=3的150个case。每个case按非空掩码B=1,…,2^n−1升序分别抽背景b=randint(1,4)与重数w=randint(0,9)，两次抽样都发生后才删w0类型。因此当前默认域不含背景0，重数最多9；重数是不同单位客户的类型聚合，不是非单位玩家权。全部w为0时允许空types，程序没有非空过滤。

每case创建original_pay(types)、clone_pay(types,3)；原主题n、三位剩余玩家，clone标签3n、仍三位玩家。主函数分别调用reachable(n,3,op)、reachable(3n,3,cp)，只保存可实现SPE终局的**计数集合**，不保存完整策略动作表。checked只在两次调用完成后加1。当前固定三人/三clone，没有四人分支，也不会根据文件名r4改参数。

## 原收益与精确Beta边际

对当前行动a，original_pay(q,a)=Σ_(B含a)w/[b+Σ_(j∈B)q_j]，背景另留在b内；各pay闭包按tuple q/a缓存。它接受一个给定背景参数，不生成对应早期共同目录历史。

clone_pay以a//clones识别原主题。某客户包含当前clone时，用own=q[a]计同clone使用者次数，把其他相关且被使用的不同clone各自次数列为others。b0时每人份额1/(own+Σothers)。b≥1时，令d=1+len(others)，对其它标签子集mask、s=|mask|加

\[
 \frac{b(s+1)!(b+d-2-s)!}{(b+d)!}
 \frac1{\mathrm{own}+\sum_{j\in mask}n_j}.
\]

乘各客户类型重数后求和。首因子是Beta密度b(1−p)^(b−1)下当前兴趣指标和恰mask其它指标被含的精确积分；同一clone的own名玩家共享一个指标。分母按玩家次数，不按不同标签数，不能把own次重复独立化。所有运算Fraction/factorial，无数值积分或兴趣抽样；当前用途调用a时q[a]>0，故相关分母正。

这是[非负Beta静态表示](../等价/Beta克隆对背景利润的非负静态表示--等价.md)的有限标签边际，不是在源码内列全兴趣pattern、清共同倍数或展开单位客户。权重清分母和合法singleton背景的另行构造仍需相应解析，不能由一个count数组冒已完成全目录认证。

## reachable为何表达全部可实现终局而非一个Markov策略

固定总人数m、k行动，R(q)在Σq=m时为{q}。否则每个候选行动a的孩子集合R(q+e_a)先递归求出，令

\[
 v(q)=\max_a\min_{z\in R(q+e_a)}u_a(z).
\]

返回

\[
 R(q)=\bigcup_a\{z\in R(q+e_a):u_a(z)\ge v(q)\}.
\]

必要性：若a/z是一份完整SPE的当前选择，任意其它行动t的真实孩子终局都属于R(q+e_t)，收益至少其最小值；当前最优性迫使u_a(z)≥每个这样的下界。充分性：若目标z在某a孩子中且收益≥v，给所选a孩子接实现z的完整子SPE；其它孩子分别接令当前者收益最小的子SPE。当前者不愿偏离，所有孩子本身SPE，故可接成完整策略。有限集合非空/最小值存在及末层基础使归纳闭合；使用≥保留所有平局。

因此缓存相同count状态的**结果集合**可复用，但在不同有序历史的各次出现可独立选择实现策略。源码不承诺一份count-Markov策略，不输出某个固定平局选择器的完整证书。报告叫original_spe的数组也是终局计数，不是σ动作表或有序路径；证明集合值递推正确，不等于本次重跑历史记录。

## fresh失败和重复终局是两个不同判据

fresh(q,c)把每个原主题的q_a次使用转为该主题前q_a个clone各用一次，公式为逐主题串接int(j<q_a), j=0,…,c−1。它保持人数当且仅当每q_a≤c；当前默认m=c=3自动满足。若有人把该函数直接用于m4/c3且某q_a=4，会丢掉一位，不能默认为正确四人fresh映射。两份四人报告没存clones或生产程序，不能据文件名替它们假定c3或c4。

failed收原R中的q且canonical fresh(q,3)不在clone R；repeated收clone R中max(q)>1的终局。程序以failed **或** repeated非空触发candidate_found。前者针对“原可实现count是否存在全鲜clone实现”；后者针对“clone是否也能出现复用”，并不否定仍有全鲜SPE。全fresh叶存在也没有逐项保留给定原σ在所有fresh历史的义务。每主题clone置换保收益和完整策略，故正确域内canonical fresh只是该原count全鲜实现的一个对称代表。

这里“复用”针对同一个完整clone标签，不是原主题重复：原主题两次可选两个不同clone而仍全鲜。程序使用标签目录；若若干标签同覆盖，须按[覆盖标签的策略商](../等价/覆盖等价标签的完整策略商--等价.md)重新构造完整策略再谈集合目录。商保实际收益/覆盖路径，但fresh/repeated的标签count不自动成为商目录内在量。记录没有执行这个商或产生商后动作表，不把别名计数直接冒成严格集合目录反例。

因此同一输入可以failed为空而repeated非空。作者[固定所有fresh行为提升反例](../反例/Beta克隆固定策略提升的不可补全局部合同--反例.md)属于另一个更强合同；不能拿本探针有限阴性推翻那个已证24→25失败，亦不能把重复候选改名为fresh存在性lift反例。当前默认也不抽原反例中的背景0类型，测试域与逻辑合同均不同。

## 四报告所有外层字段

### beta_clone_probe.json（128B）

|原字段|全部原值|
|---|---|
|status|`"no_candidate_in_finite_batch"`|
|checked|`300`|
|scope|`"No general conclusion; fixed candidate test only."`|

### beta_clone_probe_mixed.json（1379B）

|原字段|全部原值|
|---|---|
|status|`"candidate_found"`|
|n|`3`|
|m|`3`|
|clones|`3`|
|types|`[[1,0,20],[2,1,3],[3,0,13],[4,2,12],[5,1,9],[6,1,14],[7,1,19]]`|
|original_spe|`[[2,0,1],[3,0,0]]`|
|fresh_lift_failures|`[]`|
|repeated_clone_spe|`[[0,0,2,0,0,0,0,0,1],[0,0,2,0,0,0,0,1,0],[0,0,2,0,0,0,1,0,0],[0,2,0,0,0,0,0,0,1],[0,2,0,0,0,0,0,1,0],[0,2,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0,1],[2,0,0,0,0,0,0,1,0],[2,0,0,0,0,0,1,0,0]]`|
|checked|`141`|

### beta_clone_probe_n3r4.json（120B）

|原字段|全部原值|
|---|---|
|status|`"no_candidate_in_finite_batch"`|
|n|`3`|
|m|`4`|
|checked|`60`|
|scope|`"No general conclusion."`|

### beta_clone_probe_r4.json（121B）

|原字段|全部原值|
|---|---|
|status|`"no_candidate_in_finite_batch"`|
|n|`2`|
|m|`4`|
|checked|`100`|
|scope|`"No general conclusion."`|



128B默认名记录只有status/checked/scope三个字段，checked300与当前main走完两个150循环的阴性分支schema相容。它不含seed、n分组、各case输入/集合、代码依赖hash、argv/cwd/exit/耗时或逐次日志；不能据三个字段证明其历史全300次已被本轮认证，更不成为普遍lift或无复用定理。

两份r4记录各五字段：n3/m4/checked60与n2/m4/checked100，scope都仅No general conclusion.。当前main固定m3，阴性输出也不含n/m，并只写默认文件；没有参数能生成这两份不同schema。它们是各自有限记录，未保存其生产代码/克隆数/抽样域/seed/输入/运行绑定；不把当前m3程序套成旧r4入口，不自行补写版本历史。两个不同n域亦不能合成160个同分布样本。

## mixed的完整输入、原count和九个重复count

1379B记录九字段，无scope；全部七种非空掩码和重数/背景为：

|B|兴趣|b|w|
|---:|---|---:|---:|
|1|A|0|20|
|2|B|1|3|
|3|A,B|0|13|
|4|C|2|12|
|5|A,C|1|9|
|6|B,C|1|14|
|7|A,B,C|1|19|


这组原客户总数90，区别于作者严格固定合同的85客户；背景0/1/2混合。original_spe两个count按原顺序为(2,0,1)、(3,0,0)，fresh_lift_failures=[]。canonical fresh分别为(1,1,0,0,0,0,1,0,0)及(1,1,1,0,0,0,0,0,0)；记录未存完整clone R或两份对应完整策略，空failure是原字段声明，不是本次新证书。

repeated_clone_spe九行全部逐字如下，索引按A0,A1,A2,B0,B1,B2,C0,C1,C2：

|原行序|完整9维count|
|---:|---|
|1|`[0,0,2,0,0,0,0,0,1]`|
|2|`[0,0,2,0,0,0,0,1,0]`|
|3|`[0,0,2,0,0,0,1,0,0]`|
|4|`[0,2,0,0,0,0,0,0,1]`|
|5|`[0,2,0,0,0,0,0,1,0]`|
|6|`[0,2,0,0,0,0,1,0,0]`|
|7|`[2,0,0,0,0,0,0,0,1]`|
|8|`[2,0,0,0,0,0,0,1,0]`|
|9|`[2,0,0,0,0,0,1,0,0]`|


这些count仅A的一个clone被用两次、C的一个clone被用一次，B全0；3×3标签选择同投影(2,0,1)。不是九条有序行动路径或九份完整SPE动作表，也不能以计数等价强迫同一σ对所有等负载历史相同。若原集合值计算被对应代码完整执行，这些行表达可实现的重复终局；本次只保实际存储记录和语义，不重新求SPE或声称另有完整策略证书。

mixed不是当前3048默认main的原始输出，有三个独立可见差异：其b含0且多个w>9；n3却checked141，而当前先走完n2的150例才能到n3（进入n3后checked至少151）；positive分支当前必写scope而此记录没有。字段大体同族不等于生产版本相同。不能根据文件名、类型或同一算法给它编造旧seed/旧脚本修改/执行顺序，也不把141与默认300、r4的60/100简单累计为601个同域成功实验。

## 与已整理数学的去重及执行边界

[Beta版本审查](../审查/Beta背景表示的版本与两份单位实现边界--审查.md)此前仅保“有限probe不是普遍正面证据”，本次补其真实main/四报告全部字段和生产合同。收益依赖定义先前已完整保，当前新增的是集合值递推的必要充分解释、fresh人数边界及四记录的实际不同域，不宣称新BI方法。既有来源稿与现正式静态/反例/复用债、后来父审的时序保持原样，不再认领。

[独审较小单位实现的比较快照](../../tools/evidence/beta-clone-probe-and-four-reports-five-primary/comparison/archives/customer-attraction/state/程序/Beta克隆独审的六十倍单位实现与真实双回复--程序.md)所用60倍/5100含empty、原39主题两人子局，以及作者2520全3clone，是各自不同输入；本1379B/90客户和四有限记录不冒其中任何运行。fresh另末位BR给当前27、repeat25只击穿指定freshB24；同叶25≤投影AAC27也不付另一真实叶的比较。较弱全局实际叶/福利lift和一般背景half未由这些有限记录闭合；没有half反例/最小性或外审声明。

当前代码的文件输出用json.dumps(indent=2)无LF、stdout紧凑json.dumps加LF；报告原字节不归一化，不假两者字节相同。当前5primary均retained：helper首次primary、prior normal/fullread同字节复用；四报告完整首读，分别保字段/域/未知生产者。20XH原完整20ID claim pushed/synced及五源owner/hash按actual回执封存，不裁造五ID回执。[来源闭包](../../tools/evidence/beta-clone-probe-and-four-reports-five-primary/README.md)含精确normal路径和既有全文比较；Boss4未Git/claim/done/新运行，交Root审后串行发表。
