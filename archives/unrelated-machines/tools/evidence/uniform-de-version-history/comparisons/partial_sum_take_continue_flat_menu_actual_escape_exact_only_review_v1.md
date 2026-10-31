# partial-sum take/continue 局部编译：Exact-only 独立反例审查

审查者：general_query_response_review。2026-10-18。

冻结前仅读：
/workspace/scratch/038d9dcc4cac/partial_sum_take_continue_flat_menu_actual_escape_exact_v1.md

Exact SHA-256：27d2926563eeb34591ca44a75cf09ca623719827a67eedff485edf78e22053ac。

未读作者Proof、root其它推导或其它agent输出。本次独立生成完整稀疏矩阵及一份实际assignment，用精确Fraction回算；解析下界与任意partial上界另行直接证明，不由有限算例代替。仅scratch新增，无repo/Work/Git修改。

**明确结论：Exact反候选有效，无fatal。原SC真实max-min值0；目标26 machines、30 jobs全部实际执行下OPT=8/5；任意选态及任意partial bundles的值精确V=2/5。它否定明示take/continue additive局部split的正partial解码合同，不否定所有configuration DAG或既有selector-tree。**

## 1. 原SC与真正的unit路径

三名agents、两件不同且不可拆items，每个原value均3/5。任何合法allocation把两件items各至多给一名agent，因此至少一名agent完全无item、效用0；所有效用非负，故max-min OPT_SC=0。允许decoder从头重新分配全部原items也不能改变这一计数。

每agent达到unit至少需要两件items；两件原总值6/5>1。按cap1的累计路径，第一步credit3/5，第二步credit2/5≤原value3/5，累计恰1。没有舍入、虚增credit或DAG合并。该路径只是单agent可达unit的合法记账，不给三agent不交unit allocation。

## 2. 规则与完整矩阵逐对象重构

所攻规则将一步credit c变成一个normalized additive state：item权c、next-own权1−c。其节点off state为自身own singleton，终点有fresh accept singleton。源中两步因此对应：

- root take1：u_1权3/5、x_a权2/5；
- middle off：x_a权1；take2：u_2权2/5、y_a权3/5；
- leaf off：y_a权1；accept：z_a权1。

每agent有3 groups、5 indexed states、7 incidences，故全体有9 selectors、15 private machines、21 incidences、30 jobs。资源u_1,u_2全局共享，另有每agent三个互异fresh x_a,y_a,z_a，共11资源机；加private共26 machines。Selector有限资格每agent1+2+2=5，共15；incidences各两端，共42，合计57 finite job-machine entries。所有未述资格∞。每state权之和严格1，所有原jobs在矩阵中，无删除的off state。

这个构造与Exact表逐项一致。特别同一x_a的root incidence与middle off incidence是两件独立jobs，后者可留其private；共享的是外端R_(x_a)，不是把job合并或免费复制资源。

## 3. V(P)=2/5：任意partial的解析上界与达界

这里V按目标全部9 groups各选一state、领取该state内任意资源子集且全局不交、最大化最小private质量定义。

每root仅有take1 state，支持{u_1,x_a}、权3/5和2/5。全局不交使u_1最多供一个root领取。另至少两个roots没有u_1，其任意partial子集质量最多2/5。因此无论middle/leaf选哪个indexed state、其它资源如何分配、部分集合是否具product形状，最小group质量总≤2/5。

达界时三个root均选take1并只取x_a，middle均选take2并只取y_a，leaf均选accept并取z_a。所有9枚fresh资源互异，原u_1,u_2均不用。三类质量分别2/5、3/5、1，最小2/5。因此V(P)=2/5。

这是真实不可分resource subsets；没有分数切割资源，也没有把多个node质量求和后冒充单group质量。

## 4. 完整actual达界：全部30 jobs逐类执行

Selector分别放root take1、middle take2、leaf accept private。仅将这些selected states里的x_a、y_a、z_a incidence导出；所有其它原incidences留各自private，包括两个off states的全部jobs及selected states的u_1/u_2 incidence。

对每个agent：

- root private：selector1与u_1 incidence3/5，load8/5；
- middle take2 private：selector1与u_2 incidence2/5，load7/5；
- middle off private：其唯一incidence1，load1；
- leaf accept private：selector1，load1；
- leaf off private：其唯一incidence1，load1；
- x_a,y_a,z_a资源机各一件unit，load1。

共享u_1,u_2资源机都空载。每件selector/incidence恰一次、每端都在原资格中，全部30 jobs完整执行，所有26 machines均被列入回算。峰8/5，证明actual OPT≤8/5。

## 5. 任意完整actual的解析lower

每root selector只能去自己唯一take1 private。若一份完整调度峰C<8/5，该private上的原u_1 incidence若留private，就与selector组成1+3/5=8/5，矛盾。因此三个root的三件不同u_1 incidence全部被迫去同一R_(u_1)，每件耗时1。

但C<8/5<2时该机连两件unit都不能容纳，更不可能三件。故不存在C<8/5的完整actual调度，OPT≥8/5。结合完整上界，OPT(P)=8/5。

这覆盖任意selectors、全部未选jobs可能的额外exports和所有合法原端选择；没有先将actual调度规范化、假定未选state无exports或求解器返回。已独立解析得到V=2/5、OPT=8/5，二者亦与normalized flat relation OPT=2−V一致，但lower不依赖该relation。

## 6. 解码失败与准确范围

达到delta=2/5的allocation和actual witness没有用任何原item，且所有agents都激活take1→take2→accept这同一条合法unit路径。目标逃逸并非选择了另一条错误路径；它发生在每个additive take state允许只领取continuation部分而不领取item部分。

因为原SC任何合法allocation的最小实际效用都是0，所以对任何c>0，都不可能给每名原agent至少c·delta的效用。即使decoder任意重新分配原items、不要求保持target领取的item集合，也没有这样一个输出。这排除该精确规则的“任意正partial allocation可解码为所有agents的Omega(delta)效用”合同，且与计算效率无关。

Full threshold1下，两个正权部分必须都领取；但partial threshold≤其中某部分时可只取该部分，所以unit AND不蕴含正partial AND。这一局部split的缺口不能靠只压缩partial-sum reachability来补足。

本例没有排除其它AND、守卫、共享activation、complete configuration leaf、不同processing times或所有DAG compiler。尤其既有selector-tree只从root链抽取一个已经存在的normalized original state；本反例另把本应合取的items拆成沿路additive states，再以fresh accept结束。新增AND步骤不是既有selector-tree定理的结论，因此不存在对其已证域的反驳。原SC行总质量6/5也没有被免费当作原normalized leaf state。

没有提供tiny-gap复杂性源、普遍最小机器反例或主目标反证。

## 7. 独立精确Fraction检查与证据层级

独立检查文件：
/workspace/scratch/038d9dcc4cac/partial_sum_take_continue_flat_menu_actual_escape_independent_fraction_check_v1.json

SHA-256：9cf13ec0f81346889d177095e1c04b0dac13230ff8fd13f3fc8d23e537edd2f7。

该文件包含从Exact表独立生成的全部机器、完整finite稀疏矩阵（未列端∞）、30-job assignment、各机Fraction负载、selected states/bundles/qualities。实际断言通过：
26 machines、30 jobs、9 selectors、21 incidences、57有限条目；峰8/5，partial最小质量2/5，两个原item资源load0。没有读取作者代码或枚举最优值。

所有参数是固定小有理数，矩阵完全显式、位复杂度常数。此有限检查仅验证完整witness及数字，任意partial与任意actual的解析lower分别已在§3/§5证明。

**最终Exact-only冻结：所述明确take/continue additive编译候选的完整实际反例成立，无fatal；未读作者Proof。**
