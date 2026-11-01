---
id: customer-attraction/target-terminal-joint-mass-milp-compressed-witness-and-fixed-root-records
kind: program
type_tag: 程序
title: 目标终局联合重数MILP的压缩见证与固定根记录
status: five-primary-fully-read;exact-existential-interface-compared;historical-float-timeouts-and-selftest-preserved;no-new-run
summary: 原12672B用计数与请求终局选择动作并共享可信惩罚，省显式目标指示及末层x；保M=m、合法强化、精确固定锥提取和两次无候选时限及13目标自测原记录。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/full_history_milp.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/m5p7_root221.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/m5p7_root221_first0_guarded.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/true_counterexample/self_test.json
truth_status: exact-formulation-under-stated-domain;floating-MILP-and-historical-report-claims-not-universal-certificates
review_status: full-source-and-all-report-fields-read;existing-equivalence-and-runtime-closure-compared;zero-new-native-mathematical-execution
---

# 对象和实际来源

本批五源为9565B README、12672B代码、742/763B两份五人状态和1919B自测，共25661B；全部原文及JSON字段实读，核size/SHA256/Git blob，两冻结来源同字节不计双次执行。目录名true_counterexample不代表其中已有真正反例，原README也明确否认已解一般half。

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：m≥1名单位提供者、p≥1个共同标签；每位观察全部有序历史，各客户在最终覆盖者间均分。非空兴趣B⊆[p]的整数重数r_B是不同单位客户；实数重数只用于齐次代数优化，有理点清分母才回整数clones。空兴趣客户可删，空主题、同覆盖不同标签、重复选择、零客户、全部离轨平局均保留。若另要求标签覆盖子集互异，须另核，而不能机械去重后假定原策略仍可信。

固定目标终局q⁰≥0、|q⁰|=m，程序不预先固定整条有序在轨路径。比较主题集合J的覆盖为C_J(r)=Σ_(B∩J≠∅)r_B；要把它当m槽合法比较，J须是[0,p)内互异标签且|J|≤m。主两报告J={2,3,4,5,6}满足这个条件。主目标是最大化C_J，在根福利W(q⁰)=1下探索OPT_m/W较大点；单一J不是全部最优组合。

[终局见证DAG等价](../等价/终局见证DAG的完整历史可实现性--等价.md)已经证明同类完整历史存在性和更强M=1界；[全有序树联合表示](../等价/有界联合策略与客户重数表示--等价.md)也已正确联合客户与动作。本源不主张首次联合MILP或新的福利定理。独有的是下面这一压缩变量、M=m实现、松弛强化、提取控制流及三份真实原报告的版本范围。

# 原码的精确系统

令K={k≥0:|k|<m}，C(k)={q≥k:|q|=m}。当q_a>0，收益行
\[
F_a(q)_B=1/q(B)\quad(a\in B),\qquad F_a(q)_B=0\quad(a\notin B),\quad q(B)=\sum_{b\in B}q_b
\]
非零系数有正分母，u_a(q)=F_a(q)r。辅助行只在被当前/偏离动作占用的a求值，不把未选标签的虚值当真实收入。

源码不另建目标存在指示。对每k,q及q_a>k_a建二元y_(k,q,a)，定义
\[
A(k,q)=\sum_{a:q_a>k_a}y_{k,q,a}\le1.
\]
A=1表示这对计数/请求终局有一份子SPE见证。对|k|≤m−2、每偏离标签b及d∈C(k+e_b)，建二元x_(k,b,d)，且Σ_dx=1。它选一份**共同低收益孩子**，供本计数下不同请求终局使用。另每k有0≤T_k≤m，所有客户r_B∈[0,m]，并施加s_a:=Σ_(B∋a)r_B≤m。

完整系统为：

\[
\begin{aligned}
&W(q^0)=\sum_{B:q^0(B)>0}r_B=1,\\
&A(0,q^0)=1,\\
&y_{0,q,a}=0\quad(q\ne q^0),\\
&y_{k,q,a}\le A(k+e_a,q)\quad(|k|+1<m),\\
&F_a(q)r\ge T_k-m(1-y_{k,q,a}),\\
&\sum_{d\in C(k+e_b)}x_{k,b,d}=1,\\
&x_{k,b,d}\le A(k+e_b,d),\\
&T_k\ge F_b(d)r-m(1-x_{k,b,d})\quad(|k|+1<m),\\
&T_k\ge F_b(k+e_b)r\quad(|k|=m-1).
\end{aligned}\tag{1}
\]

末层孩子是唯一终局k+e_b，省去其x及目标指示；沿被选动作到末层也无需再建终端A。非根每k都有父计数，其父对某b的Σx=1会强制这里至少一个A=1，故没有悄悄允许空的子博弈见证。末层所有b均检查，非末层所有k,b均选惩罚，不只检查根可达部分。

若固定根首动作a₀，源码令y_(0,q⁰,a₀)=1，并加
\[
s_b\le m F_{a_0}(q^0)r\quad\text{对所有}b.\tag{2}
\]
这要求q⁰_(a₀)>0且a₀合法；程序不替非法first-action作完整错误恢复。式(2)来自根偏离b至少s_b/m，是真IC后果，不是假设每过去角色均付得起某个假查询。未固定首动时根可以选任意可实现q⁰的动作。

当前代码还对非末层加入
\[
T_k\ge L_b(k):=\sum_{B\ni b}{r_B\over k(B)+m-|k|}.\tag{3}
\]
任一选择b后的最终终局d≥k+e_b，对B∋b的覆盖人数d(B)≤k(B)+m−|k|，故F_b(d)r≥L_b(k)。式(1)已经令T_k不小于一个选中的真实孩子收益，故(3)在整数见证上冗余，但能强化分数松弛。末层(3)等于已有直接终局比较，代码只在非末层另加。不能用(3)替掉全部可信孩子依赖。

# M=m及完整历史双向性

在任何正福利根SPE，根偏离标签a至少得s_a/m，而根实际u₁≤W。归一化W=1后s_a≤m，每r_B≤m、任何被求值的F_a(q)r≤m。取T_k为所选惩罚收益的最大值亦在[0,m]。未选y=0时F_a(q)r≥T_k−m由非负及T≤m自动成立；未选x=0时T_k≥F_b(d)r−m也自动成立。这个常数严格有效，无需依靠浮点容差或经验大数；Σr_B≤Σ_as_a≤mp给有界截面。

**精确整数见证⇒存在完整SPE。** 在原有序历史h、计数k和请求q，A(k,q)=1给唯一选中a。h+a继续请求q；每个其他h+b请求所选x的d，末层用唯一终局。子请求均被依赖约束支持，深度严格增加。逐有序子树独立展开后，当前实际u_a(q)≥T_k，而每个偏离孩子的真实u_b(d)≤T_k，故每节点最佳且所有孩子完美。根到q⁰。相同k不同q可以选不同a；展开仍写每个原有序h，不要求同计数统一动作。

**存在完整SPE到q⁰⇒精确系统有解。** 用[准确全集递推](../算法/完整历史纯SPE终局全集--算法.md)的R(k)。每k,b选d(k,b)∈R(k+e_b)使F_b(d)r最小，T_k取这些最小收益的最大值。对每q∈R(k)分别选能实现它且u_a(q)≥T_k的动作y；其余目标关闭，根只保q⁰。非根的全部可信目标与孩子都可同时保留，约束逐项成立。固定首动作时还须原q⁰确能由该首动实现，根递推同样保证其资格；式(2)亦由原根IC。所有额外界已证明有效。

所以共享惩罚不丢失任何给定重数和根终局的**存在性**，但会删去某些非极小离轨原策略。这不是每份完整动作图的枚举器，不承诺原给定SPE可原样映入。它与[完整历史/计数策略严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)相容：目标请求是额外状态，不能删成每k只选一个动作。W=0根SPE由s_a/m保底推出全部主题零覆盖，效率不等式平凡；W1模型只处理非平凡切片。

既有DAG等价还给更强cap1/M1：每实际角色都可查询同一合法主题获得至少s_a/m，求和W≥s_a。因此源M=m有效但较松，不能将此较旧松弛写成目前最强界，更不能因数值启动困难否定精确存在性定理。

# 压缩规模和已报五人版本

设N=|K|=binom(m+p−1,p)，Y=p·binom(m+2p−2,2p−1)，L=p·binom(m+p−2,p−1)。源码T有N个，y有Y个，x有Y−L个；r有2^p−1个。这里Y不是另一个DAG实现的显式目标指示数。请求对(k,q)数为binom(m+2p−1,2p−1)−binom(m+p−1,p−1)。生成函数对每最终q计算所有坐标前缀，再标记尚未用完的a，给出这些有限计数；没有输入位长多项式求解保证。

对m5/p7：N330、y16660、x15190、二元31850、连续127+330=457、总32307。原全历史树表示39341变量/19607二元/约394949行是README的比较描述，不是本次重新建模测量。当前压缩模型主要少连续变量和约束，二元反而更多；不宣称普遍更快。

两五人JSON都固定q⁰=(2,2,1,0,0,0,0)、J=(2,3,4,5,6)，字段逐项如下：

| 原记录 | 首动作 | 变量/二元 | 行/非零元 | 原求解秒 | 状态与候选 |
|---|---|---|---|---|---|
| 742B m5p7_root221 | 根键无first_action | 32307/31850 | 72656/2315447 | 99.52086676200003 | status1，time limit，primal None，objective/bound/certificate全null |
| 763B first0_guarded | 0 | 32307/31850 | 73503/2370607 | 83.11227940399999 | status1，同样time limit/primal None及三个null |

README命令均给seconds80及minimum2.00001；JSON不含这两个argv字段，不凭数值状态补造完整进程日志。求解时限是HiGHS选项，不是外部严格80秒walltime保证，实际solve计时如表，不含模型构建或后续精确提取。

README明确第一份来自加入(3)前的版本，不冒同字节当前源码运行。当前main无论首动是否None都会写first_action键，第一份亦缺该键。第二份与当前强化的规模相容：非末层k数120，每k七条(3)共840行，固定首动再加七条(2)，故72656+840+7=73503。原非零元差55160也分成840条每条65非零的54600及七根行48+80+80+4×88=560。这个结构对照支持原版本说明，不是新建矩阵/运行认证。两份都无incumbent，没触发certify，不提供不可行、最优、无反例或任何福利上界。

# 实际提取闭包及其认证层次

12672B原码有main guard，运行时向祖先寻找customer_attraction/__init__.py，再加ROOT及ROOT/tests/audits到sys.path。真实自定义闭包是规范四文件25475B及customer_attraction_strategy_lp.py20567B，共46042B，当前R原件同冻结SHA；本轮完整读helper及规范model/certificate/init，exact.py同SHA完整既有上下文复用。环境还需NumPy/SciPy/HiGHS，原具体版本未记录。没有把只有源码的独立stage称成已经可执行重放环境。

solve仅调浮点milp，presolve=True、mip_rel_gap=0、time_limit给定；后者不使实数系数成为精确可行证明。res.x为None则certify直接None。有向量时expand对每(k,q)取最大y分数对应动作，分数低于.5拒绝；其他孩子取最大x且同样.5拒绝。它不逐项先验证整个MILP整数可行性，深度终端核k=q。返回动作键是所有Σ_(t=0)^(m−1)p^t个有序历史，根所达计数还由StrategyCone重算对照。

随后进入[固定完整策略锥](../定理/固定完整策略的客户重数锥--定理.md)：helper从全部有序节点及全部真实偏离子树构造Fraction收益差Γ，去零/去完全相同行；只缓存终局收益，不合并策略历史。在Γr≥0、W1、r≥0下**重新优化**同一J的客户重数。恢复先对浮点解limit_denominator(10⁷)，失败才用浮点支持/活跃行选基并精确消元；每个接受点都再逐Fraction核非负/全部Γ/恰W1。恢复失败只返回certifiedFalse。

这是提取动作后更换重数，不保证重现原MILP的质量向量、minimum约束数值、联合最优值或原候选所在面。helper还尝试精确对偶，但certify只要求精确可行原始点，不要求dual_optimal，也不把对偶/乘子输出到本主报告。因此certifiedTrue表示所得固定策略在某精确客户输入上合法，不能读成固定锥目标或整个联合MILP已证最优。

integer_clones清各分母再除整体gcd，instance_from_clones按mask造不同单位客户。规范verify_certificate不调用全集求解器，而自底向上算所给完整策略每个动作孩子的真实终局，逐节点逐替代动作Fraction比较并核根计数。随后Instance.optimal_welfare枚举大小≤min(m,p)的全部标签支持，算真正整数W和OPT；ratio=OPT/W，portfolio_ratio只是恢复点的C_J/W。只有精确OPT>2W才超过二，不拿minimum2.00001或float状态替代。

程序另外对每标签记录所有正克隆类型mask的覆盖签名，得catalog_has_distinct_subsets。labelled_game_exceeds_two只查OPT>2W；源码counterexample还要求覆盖互异，这是其历史“原集合目录”额外过滤。当前共同标签模型本就允许同覆盖标签；不能把这个额外gate混作本模型SPE验证条件，也不能删除重复标签后沿用旧离轨证书。

non_markov_count_states只统计这份提取动作表在同k是否出现不同a；值0不证明所有策略可计数净化，值正也不证明该终局无法被另一计数策略实现。严格排除另有完整穷尽证据。

# 原自测：13个可达性项与5/3提取回归

small_test内嵌三个原单位输入，非空mask顺序为1至2^p−1：m2/p2重数(2,1,0)，m3/p2重数(3,1,0)，m2/p3重数(1,2,0,2,1,0,3)。对每输入先用ExactSPESolver取R(0)，遍历全部总数m终局，只跳W(q)=0；本记录实际保全3+4+6=13项：

| 输入 | q按原顺序 | 原realizable |
|---|---|---|
| 2/2 | (0,2)，(1,1)，(2,0) | false，true，true |
| 3/2 | (0,3)，(1,2)，(2,1)，(3,0) | false，false，true，true |
| 2/3 | (0,0,2)，(0,1,1)，(0,2,0)，(1,0,1)，(1,1,0)，(2,0,0) | false，true，false，false，false，false |

源码为每q建固定原重数/W(q)的模型，solve10，比较out.x非空是否恰等于q∈R(0)。保存五个true、八个false；true时expand后在**原整数输入**按定义核整树。false的数学真值可由精确oracle承担，不能从浮点未返回incumbent单独作不可达证明。

末尾另造m3/p3、根(3,0,0)、J=(0,1,2)、首动作0的自由重数模型，solve20，再跑上面的固定锥提取。报告十字段为certifiedTrue、W3、OPT5、ratio与portfolio_ratio均“5/3”、覆盖互异True、labelled_game_exceeds_twoFalse、counterexampleFalse、full_ordered_nodes13、non_markov_count_states0。small_test明确过滤strategy和integer_clones，所以该1919B不是一份可独立重放全部13动作/客户的证书文件。

其5/3有独立数学基准：[三人锐界](../定理/三人锐福利界--定理.md)已证明，且大题三客户、另两互斥单例、全部有序历史选大题的完整SPE达到W3/OPT5。在任意离轨历史，跟随大题最终人数≤3，收益≥1，改任一单例最多1；这是全树证明。该解析基准说明回归数值应有何意义，不宣称保存报告缺失的clones和动作必就是这一个输入。

按源码设计，正常完成一次small_test会有13次固定目标MILP、五次原整数验收，再一次自由回归MILP/一次固定锥LP及回归验收；本次没有运行这些过程，也未把1919B历史certified字段冒成新PASS。既有DAG的57目标/60调用和全树联合12路径回归是不同代码/输入/报告，不加到本13项上。

# 入口、状态纠正与保存

CLI默认players5/topics7、root=(2,3,0,0,0,0,0)、portfolio=(2,3,4,5,6)、seconds60，minimum/first-action默认None，out必填。--self-test运行上述固定13项和提取回归；非自测先建模型，stdout打印建模量，再solve/打印meta/certify，最后才覆盖out为完整缩进JSON+LF，不建父目录、不独占旧文件；中途异常不会形成新完整报告。正人数/主题、合法q、首动作、比较集合必须按合同给出；构造器主要assert根长/总数/非负，CLI并未全面验证。helper coverage_row用位值求和而非逐位OR，重复portfolio可能产生进位，不能当并集；越界标签或|J|>m也不自动是合法m槽比较。规范最终OPT仍单独重新枚举。

原JSON的universal_half_coverage_status=OPEN是历史一般目标标签。当前[五人half](../定理/五人半覆盖--定理.md)已由别证解决，不能把这两五人时限恢复成当前五人OPEN；一般人数及恰六人仍未由本五件解决。本轮不重跑旧自测、有限时限或大规模扫描，0原import/main/MILP/固定锥LP/全集/收益/SPE/Fraction审计。

实际22XT完整认领回执status=pushed，raw local_sync needs-attention原样，独立记录证3untracked/2tracked全same、无missing/different/unmerged、stash b9a9e41e35155d585dd528ae184ba5f5784eb5ad保留；未改写synced。Root先checkpoint正文/原件/证据后登记本五源done，其余认领项和46042B已成依赖不额外处置。原件、全报告视图、依赖SHA、比较关系、自查和逐源收据见[本批证据](../../tools/evidence/full-history-milp-and-fixed-root-status-five-primary/README.md)。本线不写共享R/Git/claim/done，无新盲审/外审或新颖性认证。
