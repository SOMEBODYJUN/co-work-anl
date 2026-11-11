# repair_25：近完美 robust 源改版与两个 LP 的精确比较

## 本次处理的问题和实读边界

任务为 `boss5-localfix-repair-25d12f7253028f37`，直接替代 `boss3-sourcefix-repair-d1188acb9358b2e6`。17 个核心、9 个共享只读对象中，任务输入与当前 registry 的 pin 全部一致；与前次收据相比只有 `UM-NEAR-PERFECT-NORMALIZED-ROBUST-SOURCE-v1` 改版到登记 version 5、pin `4dfe055bb9bcc7ce75cee4da19f61871b56a22c8b4f0f6e5df32c69d234fc642`。前次对应 pin 为 `859595a005d35624d87b05a370bf8e728fa59a9bcec1cbc37215ed21a30db338`。

本次完整实读：AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md、当前任务；前任务的结构、元数据和与当前相同的阅读引用表逐项对照，前次收据全文；本包所有当前对象的陈述、模型、量词、条件、范围和 body 定位；11 份旧边全文。前任务与当前阅读引用只有两文件的 SHA 变化，重复 section/full-file 引用共四条，未把该引用元数据比较称为对全部原材料正文的重新阅读。

本次新实读数学正文：

* 《近完美归一化robust源四源审查》全文 160 行，尤其 §§1–6；
* 《部分激活菜单福利地板》全文 185 行，尤其正支撑 λ、W−δA 及给定见证筛选；
* 《归一化菜单福利与配置证书双源审查》全文 87 行；
* 《归一化门控福利证明与参数互补八源溯源》全文 175 行；
* 《显式均匀束robust源的福利排除域》全文 42 行；
* 《归一化门控菜单福利源判别与比例纠错最终审查》全文 55 行；
* 《门控归一化FSLP四源清洗》仅唯一节“四、robust 参数互补的正确量词”。

其余同 pin 核心与 10 份不受改版影响的旧边，沿用前次正式 done 收据的数学审读，不宣称重读其全部 68 文件证据包，不重跑历史数学程序。本次实际核对旧边的 ALL 前提、whole_result/contribution、条件关系与语境边分类，并验证旧资产 SHA、端点 pin、证据 SHA。唯一过时绑定是下述 context 边的 robust 目标 pin；其余 10 边及全部所引证据字节一致。

## 1. 近完美福利 LP 判别保持不变

令 n≥1；每个显式非空菜单 state 的非负有理权和为 1，组间资源束两两不交，无 coherence、标签相容或共享内部任务。总可行福利 LP 是

\[
\sum_s z_{gs}=1,\quad 0\le x_{gsu}\le z_{gs},\quad
\sum_{g,s}x_{gsu}\le1,\quad
L=\max\sum_{g,s,u}p_{gsu}x_{gsu}.
\]

任意真实 allocation 取 attaining state 后嵌入，故 W*≤L≤n。给 LP 最优有理解，先按 z 抽 state，再以 x/z 提议资源，逐资源给最高原系数提议者；精确有理条件期望给实际 W≥(1−1/e)L>5L/8（L>0）。零 z 对应零 x，禁止作零除。条件化后使用精确有限 levels 的乘积公式，不再要求条件概率总和≤1。

YES 有至少 q=(1−η)n 个 unit 组，故 L≥q。对两版 NO 分别令 h= #{r_g≥δ} 或 h=#{r_g>δ}。第一版低组 <δ，第二版低组 ≤δ；两版均有

\[
W\le\delta n+(1-\delta)h
<[\gamma+(1-\gamma)\delta]n
\]

因为 h<γn、δ<1。若接受且 (5/8)(1−η)≥γ+(1−γ)δ，则 W>5L/8≥上述右端，矛盾。由此两版各自正确；没有偷换 >δ 与 ≥δ，亦不需整除。

统一子域 0<γ≤δ≤3/8、η≤1/40 中右侧≤39/64，左侧≥39/64。η=1/40、γ=δ=3/8 的三重等号成立。δ=0 的 NO_≥ 为空类，η=1、δ=1 域外。该证明不提供 NP-hard 源归约。

## 2. 此次改版补全的 P_gate 前向全任务调度

两份变更证据现在都明确列出 root pin、未选 connector、未选 selector 和所有其余 incidence 的位置。核对完整矩阵：J0 只在 root 耗时1；connector 在 root 耗时1/n、在本 gate 耗时1；selector 在 gate 或本组某 private 耗时1；incidence 在原 private 耗时 p、在对应 resource 耗时1。

给 β>0 的真实 balanced 见证 H、attaining states 和两两不交 bundles，|H|/n≥β、每选中组质量≥β。root pin 留 root；H 的 connector 去 gate、selector 去 attaining private、所领正 incidence 导出 resource；未选组 connector 留 root、selector 去 gate；其余全部 incidence（含未选 states、零 jobs）留原 private。于是：

* root 负载为 1+(n−|H|)/n≤2−β；
* 每 gate 只收一枚 connector 或 selector，负载1；
* 每个选中 private 的负载为 1+未导出质量≤2−β；其他 private 负载≤1；
* 每资源因 bundles 不交至多收一枚 unit incidence；unused 机器负载0。

全部物理原任务各执行一次。β=0 取所有 connector 留 root、selectors 去 gate、incidence 留 private，峰2。反向 C<2 仍从 root 给选中组数、private 给导出质量、unit resource 给不交。故 OPT(P_gate)=2−β* 的有效部分保留。此补全与近完美对象所指定的福利 LP 阈值本身无相互新增假设；不把 P_gate 结论转移到 flat 或一般 UM。

## 3. F2 给另一子域判别，但不等于福利 LP

F2 的正支撑部分 LP 是

\[
\lambda_{gs}\ge0,\quad \sum_s\lambda_{gs}\le1,\quad
\sum_{g,s}\lambda_{gs}=q,\quad
\sum_{g,s:p_{gsu}>0}\lambda_{gs}\le1.
\]

YES 有 r≥q 个 unit 组。归一化迫每个 attaining state 的全部正支撑属于对应 bundle；给所选 states 各权 q/r，即给该 LP 的可行 λ，哪怕 q 非整数。

只在 η≤1/40、0<γ≤δ≤3/8 取 q=(1−η)n 和固定 τ=19/50。F2 在 τ 处的高组地板及 1−1/e>5/8 给

\[
H_\tau>
\frac{5/8-19/50}{1-19/50}\,q
=\frac{49}{124}q
\ge\frac{1911}{4960}n
=\left(\frac38+\frac{51}{4960}\right)n
>\gamma n.
\]

τ>3/8≥δ，所以这些组同时属于 r≥δ 与 r>δ；两版 NO 都排除 λ 可行。只检查正支撑 λ-LP 可行性即为一个替代子域判别器，精确有理算法不计算 e。这个论证完整，但它得到的是另一 LP 的判别，不是从 F2 推出目标指定 L 的全部结论，更未覆盖一般 (E) 域。因此对应图边仍为 accepted / context / motivates，不能把 robust coverage 改成 linked。

### 明确分离两个 LP 的小例

两组 g=1,2 各仅一个 state。共有资源 u，私有资源 a,b；第一组在 a 上权19/20、u 上权1/20，第二组在 b 上权19/20、u 上权1/20，其余权0。各 state 正常 norm1。

福利 LP 取 z1=z2=1、两个私有 x=1，共享资源只给任一组 x=1，即 L=39/20。上界也恰为两个私有贡献38/20加共享最大贡献1/20，所以该值最优。正支撑 λ 因 u 同时出现而必须 λ1+λ2≤1，故最大总质量仅1。取 η=1/40 时 q=(1−η)·2=39/20，福利 L≥q 而同质量 λ 不存在。

该例只否定“任意福利 LP 点/阈值可转成同质量整正支撑 λ”的桥。它在该参数下既非 near-perfect YES（两个 unit 组不可能），也非 robust NO（两组可各领私有资源达到19/20）；没有反驳任一 promise 判别器。这个范围限定防止把 LP 分域小例误登记为 robust 定理反例。

## 4. 交付、继承与未付义务

原 `partial-support-versus-welfare-lp.json` 保 edge_id 与 context 身份，补明确 LP 分离例、此次前向调度复核与当前目标 pin，再进行本地 edge-bind/edge-check。其旧 SHA 标 replaced，replacement_paths 指向同一实际路径；不把修改字节标为 retained。其余 10 个 canonical 边按原 SHA retained；8 个 whole/step 逻辑关系继续保各自 ALL，two-rail 的条件局部贡献和 selector 上界 contribution 的 remaining 不缩短。

任务与前任务均无标为 follow-up 的对象对；前次已闭合 Kronecker/裸 Cartesian 的分域比较属于继承范围。closed_overlaps 与 follow_up_tasks 均为空，未新发布队列任务。

仍未付：一般 (E) 域从 F2 整支撑 λ 的判别不成立为此处已证结论；福利/正支撑两个 LP 不可免费转换；无隐式菜单、共享内部任务、一般 UM、未知实际见证搜索、source hardness/可靠归约或全方向 FAIL。以上均是数学接口边界，未产生新的身份或来源待决。
