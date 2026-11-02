---
id: customer-attraction/two-group-first-pair-alternation-and-restricted-common-Q-negative-records
kind: program
type_tag: 程序
title: 双组首对安全攻击与受限共同Q的有限阴性
status: four-sources-fully-read; finite-floating-results-retained; zero-current-mathematical-run
summary: 三人两组固定完整策略的全类型质量/查询交替攻击，与两个未保存模式的共同Q不可行记录分开；100起点无已存正点不证明全锥pair，status2不作真实SPE反例。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/aggregate_security/group_pair_cone.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/aggregate_security/group3_simple_Q.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/aggregate_security/group4_pair.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/aggregate_security/group4_within_Q.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/aggregate_security/group_common_Q.py
---

# 四原件的准确身份

本组四主源共3510B，全部全文实读：2739B `group_pair_cone.py`（`642d69a813578786459b`）、255B `group3_simple_Q.json`（`49fe1ba6d82a3a15e167`）、261B `group4_pair.json`（`c36396d204ada7abb768`）、255B `group4_within_Q.json`（`b61cab7d8f560782d674`）。[原字节与清单](../../tools/evidence/two-group-pair-attack-and-Q-negatives-primary/README.md)逐项保全完整冻结定位、大小、SHA与本次正式claim。旧两个冻结分支同路径同字节，不算两次独立结果。

三份JSON中，只有`group4_pair.json`的schema与本组attack输出相容；另两份status/message记录符合相关`group_common_Q.py`失败分支的schema，不能冒充同一个交替攻击脚本的失败运行。为判断其含义，本次还全文读了2908B相关共同Q程序，仅作related，不重复该源的主处置或原件复制；其[独立程序合同](反组首对共同静态背景的浮点探针与双组规模边界--程序.md)另行保留。

本批没有运行原程序、import执行、LP、随机搜索或新数学checker。有限负面输出按原有字段保，不为复现旧数值阴性而重扫。

# 固定完整策略、客户锥和真正静态安全值

程序人数始终n=3。参数t是每组标签数，k=2t为标签数，两组X={0,…,t−1}和Y={t,…,2t−1}。**group4指每组4标签、共8标签，不是四名玩家。** 根选0；首行动a后，若a∈X则第二位取t，否则取0；两行动历史(a,b)后，末位选b所属组中此前未用的最小标签。t≥3保证所有两步历史都有该标签。源码未验证t范围，不能把较小t的CLI值自动算成合法完整策略。

沿用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。每个非空兴趣mask T有非负质量w_T，整数质量就是不同单位客户；客户价值最终在所有覆盖者之间均分。固定上述完整σ后，对所有有序决策历史h及非规定动作a建立

\[
\Gamma_{h,a}(w)=u_{|h|+1}(\operatorname{finish}_\sigma(h))
-u_{|h|+1}(\operatorname{finish}_\sigma(ha)).
\]

偏离后沿同一σ的真实孩子续局，不冻结实际后继，不合并同计数的不同历史。其合法客户锥是K_σ={w≥0:Γw≥0}。根完成叶为(0,t,t+1)，首两人收益L(w)=u₁+u₂。这里是零旧背景；程序没有客户背景负载输入。

对查询分布p、合法两槽静态竞争背景B，令

\[
\beta_B(p)_T={\sum_{a\in T}p_a\over1+c_T(B)},\qquad
v_3(w)=\max_p\min_B\beta_B(p)\cdot w.
\]

B在查询抽样前固定，允许重复、任意相关，不受真实回复菜单限制。源码用全部无序两主题多重集无损代表有序竞争对，因为这些静态份额只依计数。客户型列是全部2^k−1个非空mask，未施加组内或交换两组的客户轨道对称；这与[九标签轨道探针](../资源/九标签首对策略的轨道锥与全类型交替探针--资源.md)的19变量不是同一个域。

# 交替两种LP的真实目标

`group_pair_cone.py`先生成所有真实IC，再对浮点行作`np.unique(axis=0)`字面去重；它没有保存去重行数或完整G。t3/k6的原始历史/非规定行/客户型/静态背景数为43/215/63/21；t4/k8为73/511/255/36。215、511是去重前的行数，不能写成原报告已认证的unique数。

固定p时，第一LP为

\[
\max_{w,s}\quad 2s-L(w),\qquad
w\ge0,\ \sum_Tw_T=1,\ \Gamma w\ge0,\
0\le s\le\beta_B(p)\cdot w\quad(\forall B).
\]

它归一的是总客户质量1，不是L=1或安全值1。代码以最小化L−2s实现相同目标。若交付一个严格正的**精确有理**可行点，就有L<2s≤2v₃；清分母后可得到该固定σ的单位客户标签游戏。质量为0可能使某些主题为空或同覆盖，不能从k个标签断言覆盖两两不同；若按严格集合目录提取反例，还须核这一输入合法性。浮点点还需逐历史、全部背景及概率精确检查；这也不自动反half，仍须另算真实覆盖与OPT。

给定第一LP的新w，第二LP用全部静态背景重新优化查询p，最大化该w上的真正静态保证值。随后再用新p进入第一LP。p与w联合选择含双线性项，有限交替并不是一次覆盖全部p,w的LP，也不提供联合最优或精确对偶。

第一个起点是均匀查询，之后用一次初始化的`default_rng(seed)`顺序抽Dirichlet：奇数rep参数向量全0.2，正偶数rep全1。每起点最多10次交替；查询最大坐标变化<10⁻⁹时结束该起点。每个第一LP后仍调用第二LP，即使已发现正候选，外层也只在该起点内循环结束后才因positive退出。不能把starts当作LP总调用数。

第一LP失败会raise并不写新的最终报告；第二LP没有检查`sr.success`便访问`sr.x`，源码并非对任意失败状态都有完备输出。JSON里的status2记录因此不是本attack脚本按这个失败分支生成的报告。此处只说明原程序控制流，不改写或运行原件。

该脚本只依赖标准库、NumPy和SciPy，无项目模块或客户输入文件。import只定义attack，不执行LP；main的`--group`默认4、`--starts`默认100、`--seed`默认9013，`--output`路径必填。源码也未检查starts为正；starts≤0会在末尾引用尚未定义的rep，不能当作合法空扫描。正常结束后覆盖指定JSON文件；候选改进时另逐行打印简短JSON，最终stdout是删去w/p的Python字典repr，不是完整JSON报告或有理证书。

# group4_pair的全部有限记录

261B原JSON全部字段为scope="floating fixed full-history strategy cone; not universal proof"、t4、k8、positive=false、max_gap=0.0、root=[0,4,5]、starts100、seed9013、completed100、seconds8.114664793014526。没有w、p、t_lower、pair、start或iteration字段，也没有完整原命令、Python/SciPy版本、矩阵、对偶和执行事件。

代码把max_gap初始化为0，只在gap比已存值大10⁻⁹时写候选w/p等字段，positive阈值另为10⁻⁷。因此该摘要只能保“没有保存超过更新阈值的正改进”；**0.0不是已证明的全锥精确最大值，也不表明所有试过目标逐字等于0。** 同理，100起点的阴性不证明所有查询分布或所有完整策略。

若确由当前代码完整产生此记录，则每个成功迭代包含两个LP，每起点1至10个迭代；100起点对应200至2000次LP的条件性控制流范围，而非报告已保存的实际调用计数。原件未记迭代次数，不能补出一个确定LP数。本次实际调用数仍为0。给出的8.1147秒是原JSON耗时字段，不是本次重放。

# 两个共同Q不可行记录：模式缺失须保留

两份小JSON各自的全部字段如下：

| 原件 | t / k | status及消息 | seconds |
|---|---|---|---:|
| group3_simple_Q.json | 3 / 6 | 2；HiGHS Status 8，model_status Infeasible，primal_status None | 0.02174520492553711 |
| group4_within_Q.json | 4 / 8 | 同上 | 0.46280860900878906 |

两者scope均为"floating fixed formal strategy cone, not a general result"。它们没有Q、λ、客户质量、查询、Farkas证书、源码SHA、模式字段或argv。文件名是导航线索；不能仅凭名称给它们补写确定的`--simple`或`--within`调用，也不能宣称精确LP不可行已获认证。

相关`group_common_Q.py`的目标是在固定σ整个客户锥上，以同一Q同时对全部合法查询a满足

\[
L-2\mathbb E_Q f_B(a)=\Gamma^{\mathsf T}\lambda_a+r_a,
\qquad Q,\lambda_a,r_a\ge0,\quad\sum_BQ_B=1.
\]

其三个可选背景限制确切为：

| 选项 | Q的实际允许范围 |
|---|---|
| simple | 固定各1/2取(0,1)与(t,t+1)，其余全0 |
| within | 任意同组不同标签对；重复背景及跨组对全0 |
| rational | 固定(0,1)取7/12、(0,2)取5/12，其余全0 |

源码依次执行simple、within、rational，每项都**重写全部Q变量bounds**，后者覆盖前者，多个flag不是把三组约束取交。模式不保存在输出中。两份失败JSON与该程序失败输出schema相容，但未有原调用绑定，不能判定实际开启了哪组限制；本组不为确定旧flags再跑LP。

即使某个受限模板被精确证明不可行，也只排除该类共同Q/整锥证书。它不交付一个w和查询p的真实首对反例。已有[完整策略锥安全对偶](../定理/完整策略锥的静态安全值对偶--定理.md)在固定p时允许Q随p变化；同一个Q同时支付整个客户锥及全部查询是更强合同，受限支持又再缩小它。不能把这些量词逆转。

# 已有正证书、关系和接续

同t3/k6固定σ已经有[任意逐客户背景的等权Q/单位Γ证明](../审查/反组六标签全背景首对支付的原多项式核验--审查.md)：Q各半取01/02，20个查询附标项对应12条不同真实IC。另早期零背景证书使用7/12、5/12及38条非负有理乘子。二者都具有完整精确范围，故本组小浮点失败记录不能推翻该固定图的既有首对结论。simple固定的01/34与这些已知Q不同；未知flags的失败也不能借文件名改写成一般共同Q已不可能。

这不把t3证书免费扩大到t4/k8，也不把八标签100起点未命中变成t4一般证明。非零背景PB-extra反例、全位置pair和六人half各有不同人数、槽数与前缀量词，本四源均未解决它们。

本对象保留两个程序接口的对照、交替攻击的完整固定策略与行域、全部三个原小报告，以及没有交付精确证书的实际边界。关系为：原程序→固定策略/客户锥的实现；小报告→有限浮点来源；共同Q程序→模式语义比较；成熟六标签正证书→范围校准。未从status2或max_gap0造一条真实反例/定理边，本批不生成第三阶段图。未来若有新严格正点，应完整保存w/p、全部真实IC及静态背景的有理核验；若研究模板不可行，应另给准确模式和精确对偶，不能沿用本三个摘要字段替代。
