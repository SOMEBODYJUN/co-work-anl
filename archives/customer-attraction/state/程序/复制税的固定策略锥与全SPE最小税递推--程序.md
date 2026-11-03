---
id: customer-attraction/copy-tax-fixed-policy-cones-and-all-SPE-minimum-tax-recurrence
kind: program
type_tag: 程序
title: 复制税的固定策略锥与全SPE最小税递推
status: complete-source-and-finite-report-scope;no-new-random-or-LP-execution
summary: 自足证明终局/最小税集合递推，保30浮点政策锥与300整数实例全记录、哨兵/整数域及0重跑。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_potential_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_potential_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_potential_probe.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_potential_probe.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_all_spe_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_all_spe_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_all_spe_probe.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/copy_tax_all_spe_probe.json"
---

# 复制税的固定策略锥与全SPE最小税递推

4857B/5506B固定策略锥代码及30记录，3206B/53506B集合值代码及300记录，四原件所有字段完整实读。两程序攻击同一[六人势候选](../候选/六人全终局调和势与有序自复制税--候选.md)，但搜索变量、平局量词及输出0的语义不同。本批两原main、30/300随机、LP、完整游戏搜索均0新运行；下面将原结果、算法证明与未认证执行分开。

## 共同有限域和整数单位

两程序M6、P7，七个共同标签始终保留，包括某次采样可能为空的标签；终局可重复。客户类型是字典序的全部127个非零七位兴趣串，原码`product((0,1),repeat=7)[1:]`排除的只是对所有标签均无兴趣型，不排除空主题。一般模型仍允许零客户、全部离轨和平局；这两份随机记录不覆盖零实例或任意大目录。

六人终局计数q有C(12,6)=924个；六位以前的计数前缀共792个，连终局共1716。LOAD[q,x]=Σ_jq_j1[x∈主题j]，整数表U[q,j,x]=60·1[x∈j]/LOAD，非接受位或零负载按0；H60=(0,60,90,110,125,137,147)，POT[q,x]=60H_(LOAD)。所有1至6分母整除60。终局welfare为被覆盖客户数W，实际税C依每一步有序前缀，不能只从最终计数直接定一个税。

## A. 固定完整计数政策的客户锥

`copy_tax_potential_probe.py`用seed61246、NumPy2.3.5生成30组初始整数权：每组做20次类型抽取，每次累加1至30。`policy(weights)`从所有792个非终局计数态逆推；每态对七行动分别沿此前已固定的下一政策走到终局，选当前真实利润最大者，平局按标签最小编号。它由此定义一份在**每个有序历史**均可执行的计数政策，不宣称一般SPE必须依计数。

对每态q、规定动作a、每个其它b，记录该固定原政策下两条真实终局的客户收益差行。共792×6=4752行，若新非负客户质量满足全部行，同一固定政策仍是完整纯SPE；不能冻结偏离后的尾而换策略。这是线性固定政策锥，未覆盖所有历史依赖政策。

沿实际六行动算60W+60C的客户系数。每trial选比较终局：初始权的最大势计数、七个单标签六次、另八个随机终局；去重后至多16个，**不是全部924个**。对每个目标以客户质量和1、质量非负和4752行非负为约束，用SciPy HiGHS最大化Φ(T)−W−C。

如浮点gap>10⁻⁷，代码取正支持和近紧IC，以Fraction消元恢复质量，重核非负、质量和1、所有4752行与严格正gap，才旁写完整`copy_tax_potential_counterexample.json`。当前没有该输出源，保存报告也未发现反证；不能从未取得的旁写分支虚构实例。初始计数政策、初始完整客户向量及每个LP的质量/状态/对偶没有写进这份阴性JSON。

原30条记录的实际动作全部保留，逐trial为：

| trial | actual_actions | trial | actual_actions |
|---:|---|---:|---|
|0|1,5,2,2,3,0|15|3,6,6,6,1,1|
|1|0,0,6,6,4,4|16|3,3,0,5,2,4|
|2|4,3,3,3,5,5|17|5,5,2,2,6,6|
|3|2,2,5,5,1,1|18|4,0,0,0,2,2|
|4|6,5,5,5,1,1|19|2,2,3,3,4,4|
|5|5,6,6,1,3,3|20|4,0,0,3,3,3|
|6|3,6,6,6,5,5|21|6,6,3,3,1,1|
|7|3,3,3,3,6,6|22|5,2,3,3,6,6|
|8|2,5,0,0,3,3|23|5,5,4,4,4,4|
|9|6,6,2,2,2,3|24|3,3,3,5,5,2|
|10|0,0,3,5,2,2|25|5,1,1,1,3,3|
|11|1,0,0,5,4,2|26|0,6,1,5,5,5|
|12|6,6,1,1,3,3|27|2,6,6,4,4,4|
|13|0,0,0,5,5,5|28|0,0,2,6,3,3|
|14|4,3,5,5,1,1|29|4,4,1,1,1,3|

每条`largest_discovered_gap_scaled60=0.0`，但程序`best=0`再取max，所以负最优值也被夹成0。它只报告有限浮点攻击未发现正gap；不能从0推出该trial恰有等号、完整比较最优值为0、精确锥对偶或普遍候选成立。原refutation_found=false和scope均保这一等级。

## B. 固定整数实例的全部SPE终局及最小剩余税

`copy_tax_all_spe_probe.py`用不同seed61247，300trial。每次先抽3至13次，再各累加1至4的整数类型客户，理论总人数3至52，非零。保存报告实际人数3至39；两批不共享实例，不能把30个政策当作这300个全SPE集。

理想精确递推对每计数态c保E(c)[f]：存在完整子SPE到终局f时，其规定路径所能达到的**最小剩余复制税**。终局E(f)[f]=0。设剩余r=6−|c|、pₓ=Σc_j1_j，孩子终局集为R_a=keys E(c+e_a)，当前选择a的终局收益为U_a(f)。令

\[
L(c)=\max_a\min_{f\in R_a}U_a(f),
\quad Q(c,a)=\sum_{x\in a}\left(\frac1{p_x+1}-\frac1{p_x+r}\right).
\]

对所有满足U_a(f)≥L(c)的孩子终局，把

\[
E(c)[f]=\min_{a:\ f\in R_a,\ U_a(f)\ge L(c)}
\{Q(c,a)+E(c+e_a)[f]\}.\tag{DP}
\]

以60倍整数实现。当前遵从孩子若满足阈值，其他每个有序孩子可独立选择让偏离者收益最低的一份子SPE，故可组合成完整政策；反过来任何完整SPE的实际孩子必须越过各孩子最低值，故所有可实现终局都被保留。税只沿规定孩子相加，给定终局f的效用不依实现该f的平局政策，因而可另选其中税最小者。这个归纳同时证明(DP)的可达集合和最小税语义。

计数缓存只共享数值集合；把相同计数嵌在不同有序历史时可分别选择不同子策略。它不把完整历史模型改成全局统一的Markov政策，也没有枚举或计数全部SPE策略树。有限单实例候选的最坏gap恰为

\[
\max_{f\in E(0)}\{P_6-60W(f)-E(0)[f]\},
\]

这里P₆用全部924终局势算60倍。每实例因此对所有有序历史纯SPE及其实际路径的税作有限攻击，比A的固定政策/少量比较更完整，但仍只针对该整数实例。

### 冻结实现的数值边界

效用、势、税的矩阵使用NumPy int64；源生成域人数≤52，所有60倍量都远低于溢出界。`kept.get(leaf,10**30)`用固定大数作初始最小税上界。由(KERNEL)，每客户60C≤87，整个生成域至多4524，故本300域该哨兵安全；它不能不审计整数范围便当作任意大重数实例的通用精确求解器。理想(DP)应使用真正的无穷初值或先验合法上界。

## 300条完整报告的准确读出

十个顶层字段含m6、catalog_size7、seed61247、requested_trials300、NumPy2.3.5及

`input_weights_sha256=7f78760375502870f6e654eae2c4ea7f78b97a41a324b361d86997124b281cc0`。

哈希按逐trial的127维权向量以小端有符号8字节顺序累加；它绑定序列，不能单独恢复未保存的300组客户。复现生成序列还依该RNG及版本；本批未为核这个哈希重新生成随机。

300记录从trial0至299不重不漏，每条恰五字段：trial、unit_customers、root_SPE_terminal_counts、largest_auxiliary_gap_scaled60、prefix_count_states。全部原数值及紧凑完整阅读视图在[证据包](../../tools/evidence/same-layer-terminal-closure-and-potential-primary/README.md)。静态字段读数为：人数3…39，根可实现终局计数数量1…28；每次1716计数态；最大gap0、最小−642，48条为0、252条严格负。它与A不同，负gap并未夹0。refutation_found=false。

`root_SPE_terminal_counts`不是SPE政策数，1716也不是1716个实际历史；924终局计数包含其中。未发现正gap仅说明这300原报告实例的有限攻击，不能把300随机样本换成全部127维重数、全部目录或所有六人实例。

## 与已成边界及实际执行的关系

同一候选的[三人逐枝接口反例](../反例/调和复制税逐分支归纳的六客户边界--反例.md)不被这些阴性记录修复；后续[静态势收尾反例](../障碍/全势候选与末位报价静态收尾的整数反证和倒二异议--障碍.md)也不否(PC6)的SPE前提。六人常选大A的七主题等号族则证明C可大于W，是候选本身必须保的支付范围。

旧R291的3/4标签穷尽压力与本30/300域不同。这个比较疑点现已由[原源码、JSON和运行日志勘误](../../tools/evidence/copy-tax-domain-correction-resumed-boss3/README.md)核清：[R286/R291审查§5](../审查/R286链式重查询与R291复制税边界--审查.md)原写“四标签仅单/双兴趣”是清洗措辞错误，已改为**全部15非空兴趣型各0/1、32767非零输入**，含全部三点/四点兴趣。R291源码只删无兴趣型，`run_case(6,4,1)`和JSON域一致；真只保10单/双型的二值域才是1023，但该独立分支不在原main中。

R291既存stdout与JSON六份结果全结构一致，stderr空，原README及既有程序receipt记成功；本次未重扫32767，也无新增claim/done。R286的59048是10单/双型各0..2，目标为最坏福利比且旧运行缺依赖；R-ad571的32767虽同15型二值域，却测W/OPT并保存6/7和最坏点复核，见[独立福利扫描正文](../计算/四主题六人二值客户全集的精确递推与保存最坏点--计算.md)。不把这些记录借来提升本30/300实验，也不把R291成功当作另两程序运行收据。

两原main会覆盖邻接JSON，A的成功反例另写文件；导入时A还导入mixed_pair、six_stress及科学包，且构造924×127静态表，B导入A。它们不是只需四文件即可独立跑的通用CLI。当前四原件保持原字节，相关闭包路径在manifest中保，**0原30/300入口、0LP/RNG、0全六人游戏枚举**。本次对其它固定点/原有限系数核的真实事件不得回填这两次原随机实验。
