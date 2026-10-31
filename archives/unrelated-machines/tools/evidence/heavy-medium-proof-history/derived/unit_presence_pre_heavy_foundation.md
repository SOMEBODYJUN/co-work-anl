# 两份实际见证下单位占位读出的锐胶合界

读取目的：检验反面归约中的可读Boolean复制接口。这里读的是原机器上是否实际接到unit任务，允许同一原job在两个见证之间small↔unit切换，所有资格arity不受限。它不以两个见证替代求解未知见证，也不推出一般UM算法或hardness。

## 1. 精确对象与结论

**ID/version：UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1。**

**Objects / Domain / Quantifiers。** 任意显式合法UM，m≥1、n≥0，全部有限p∈{1,1/k}，二进制整数k≥2。每job可有任意多个两类端，不要求small行预算、DAG、树或time-consistent见证。输入两份实际完整σ₀、σ₁，C_max均≤T=1+1/k。

定义U_i(σ)=1当且仅当原机i在σ中执行至少一件处理时间1的原job；否则0。指定不同原机v,w，且U_v(σ₀)=U_w(σ₀)=0、U_v(σ₁)=U_w(σ₁)=1。T<2保证两见证每机最多一件unit。

**Exact Statement / Conclusion。** 对每个(b_v,b_w)∈{0,1}²，可确定性总位多项式输出全部原任务实际σ_b，使两个unit-presence恰为指定向量，且

\[
 C_{\max}(\sigma_b)\le B(k):=1+\frac{\lceil(k+2)/2\rceil}{k}. \tag{1}
\]

对每个k≥2有四机、2k+6任务、每job恰两端的实例，两见证最大负载均恰T，而每个mixed向量的最优值恰B(k)。因此这是本接口的锐绝对胶合界。k2、3时B2；k≥4时B≤9/5<2，且k→∞时B→3/2。全部k≥2还满足B(k)≤3T/2，不把这项局部合同称为一般3/2近似。

**Assumptions / Definitions / Dependencies / Scope。** 两份见证是实际输入，非只给分数点或未知存在量词；unit读出不指定究竟哪枚job产生占位。仅依赖两个unit匹配之并及整数二部流，不调用PCSP/Feder或正规形。没有把零/满预载、指定unit任务身份、更多外部锁定状态或不同small大小自动纳入结论。空任务无法满足此两机新unit边界，因而不构成隐藏假输入。完整证明如下；独立审查见后述记录，外审与新颖性未认证。

## 2. 从实际见证提取两个unit匹配

在“原job—原machine”二部图上，N_a={(j,σ_a(j)):p_{σ_a(j),j}=1}是匹配：每job只选一个端，T<2使每机至多接一件unit。共同边是孤立的固定匹配边，先保留不动；其余并图度≤2，分解为交替路径或偶环。每条边保留它来自0/1匹配的颜色。

- machine–machine路径：两端的unit-presence分别从0到1、从1到0，中间机器在两见证中都接unit。可以自由选整条路径的0或1匹配。一个分量至多包含一台从0到1的测量机器。
- job–job路径：两端job分别只在一个见证中走unit，且颜色相反；另一份见证里各走其已知small端。每个方向恰有一个端点job走small。内部机器两见证均unit-occupied，方向选择不改任何machine presence。
- job–machine路径：同一颜色在两端都多一条匹配边。称该方向active：端点job走unit，端点machine有unit；inactive时该job走已知small端、该machine无unit。内部machine仍两方向都unit-occupied。
- 偶环及共同边：所有机器两方向都unit-occupied，选择任一完整匹配方向即可。

每个并图内部job在两见证中都走unit，因此改整个分量方向不会产生遗漏任务。并图外的job在两见证中都走small。以下正是安排这些small任务及各路径端点，不将原任务拆分执行。

## 3. 测量零位若位于job–machine路径，单分量翻转即够

只需证明mixed向量；00/11直接返回原见证。记指定应为0的测量机为v，应为1者为w。从σ₁出发，若v位于job–machine路径，则该路径的active颜色为1。将它整体翻成0。

此举仅删去v的unit-presence，所有内部机器的unit数保持1；新增一枚端点job在其σ₀ small端执行，成本1/k，另有unit任务只是换到同时间的unit端。w不可能是该分量内部机器，因为w在σ₀无unit；该路径仅有一个machine端点v，所以w属于其它分量，其presence仍1。其它原任务均不动。因此全机负载≤T+1/k=1+2/k≤B(k)，并实现所需两位。

## 4. 其余情形：全部activation打开，small端做一次共同整数流

v若不在job–machine路径，则必在machine–machine路径。将其路径选0方向；w不在同一路径，可将w所在machine–machine路径选1方向，或若w在job–machine路径则选active。其余machine–machine路径与偶环任取方向；全部job–machine路径一律active。这样已正确固定两个measurement，并且全部此类路径端点job走unit，不产生固定small额外负载。

剩余small选择写成真实整数流的items：

1. 每件两见证均走small的原job，item有其两见证目的机器（相同则合并为一个选项）。
2. 每条job–job路径建一个virtual item，两个选项分别为两个方向所留下的端点job的已知small机器。选该item的一个端，就确定整条路径的匹配方向，并把对应端点原job放small、另一端点原job放unit。内部原job全部随该方向走unit。

virtual item不是新增执行任务，只编码“两个方向中恰有一个原端点job走small”的选择。选项即使是同一机器也可按任一方向解码，真实small成本相同1/k，所有原任务仍各一次。

每个item在两个选项上各放1/2分数（重合则放1）。设机器总分数item数为μ_i，两原见证small任务数为s_i⁰,s_i¹。两者的均值还计入job–machine路径在inactive见证中的半枚small；当前把这些路径全部active，故

\[
 \mu_i\le(s_i^0+s_i^1)/2. \tag{2}
\]

任务到两个small机器的二部流已有此共同分数满流，机器容量ceil(μ_i)时由整数性得到实际整数满流。它为每个真实small job选一个原端，为每个virtual item选一个方向；按前段恢复全部unit匹配及原端点job，便得到完整σ_b。所有unit机器的presence已确定，job–job选择只改变内部unit job身份，不改变机器是否有unit。

### 全部原机器逐项负载

严格见证里，无unit机器的small数≤k+1，有unit机器的small数≤1。

- 若某机两见证均unit-present，s_i⁰+s_i¹≤2，整数small数≤1，最终仍只有一件unit，总负载≤T。
- 若某机两见证的presence不同，small均值≤(k+2)/2，整数small数≤ceil((k+2)/2)；最终unit数至多1，总负载≤B(k)。
- 若两见证均unit-vacant，它不可能由所选匹配新接unit。整数small数≤k+1，总负载≤T。

这覆盖了所有机器与全部原任务，不只核测量端。由(1)得统一锐界；没有将局部端点流与其它原机器负载分开隐去。

### 独立的整数费用流证明

另一位研究者只看精确陈述，独立得到不用virtual路径解码的证明。令h=ceil((k+2)/2)，仅保留每job在两见证中用过的至多两个原端。给每机一个unit计数节点，通到该机总任务计数节点的容量为1。job走unit端须先过unit节点，走small端可直接进总计数节点。总计数节点到汇的整数容量按两见证presence取

\[
 N_i=\begin{cases}
 k+1,&(U_i^0,U_i^1)=(0,0),\\
 2,&(U_i^0,U_i^1)=(1,1),\\
 h+1,&U_i^0\ne U_i^1.
 \end{cases} \tag{3}
\]

源到每job容量1，要求完整满流。两见证各取半给一个分数满流：变化行平均任务数≤(k+3)/2，与N_i至少有1/2余量；其余两类行也分别满足k+1与2容量。unit容量同样成立。

为得到v1、w0，固定σ₁在v执行的那枚unit job j_v完整留v。相比半流，v的unit量从1/2到1、总任务数增加1/2，由余量可行；j_v在σ₀的另一端减半流。w的unit分数量仍为1/2：j_v不是σ₁的w-unit，也不可能是σ₀的w-unit（后者不存在）。即使另端在w，也只是删small流。

删去已固定j_v并扣其容量后，对剩余完整整数流，只给w-unit入口费用1，其余0。已有分数满流费用1/2，整数最小费用满流的非负整数最优值≤1/2，故恰0。补回j_v，得到真实v1、w0分配。另一mixed交换v,w。

每机**同时**受unit数≤1和总任务数≤N_i限制；变化行有unit时small数≤h，负载≤1+h/k，无unit时只更低；恒1行负载≤T，恒0行在保留端里根本没有unit、负载≤T。因此全机仍是(1)。机器容量可截到原job数，无须展开k个槽。该证明也保住v上具体的j_v身份，但不固定所有其它job的外部位置。

## 5. 四机锐族与全部mixed最优值

机器P,Q,M,N。两枚unit-only二端任务x可P或M，y可Q或N。另有两组各k+2枚不同small-only任务：第一组每枚可M/Q，第二组每枚可P/N，时间均1/k。以M,N为测量机。

σ₀令x→P,y→Q；第一组分k+1枚到M、1枚到Q；第二组分1枚到P、k+1枚到N。σ₁令x→M,y→N，两个small组相反分配。两份完整实际最大负载恰1+1/k，测量presence分别00、11。

mixed10强制x→M,y→Q，第一组的k+2枚small只能去两个unit已占机器M,Q，至少一机持有ceil((k+2)/2)枚，所以C≥B(k)。把该组尽量平分、另一组也尽量平分，所有机器负载≤B(k)，达到下界。mixed01同理交换两组。因此两种mixed最优值均精确B(k)，而非只对某个输出算法给下界。

这是对每个k的显式存在族，任务数本来是2k+6；没有声明按二进制bit(k)可以写出k件任务。一般输入的胶合算法只扫描现有任务，见下一节。

## 6. 位复杂度、扣除和反面作用

先按实际输入验证两份完整σ、资格与负载，再构造两个unit匹配及度二分量。分量扫描线性；small item数≤原任务数，机器容量可截到item总数。半分数均值分母至多2，整数流只用显式原端，不按k值循环。最终每个原任务实际目的地与有理负载均可按总输入位长回算，k只参与有理比较。

与[三外接机器空满预载选择器](three_host_selector_sharp_three_halves.md)区分：旧合同以三台机器的独立零/满外加预载描述两种可用性，输出至少一坏侧；本合同读固定同一P里真实unit job的presence，任务可在两见证间改变时间，指定两个mixed输出各自都可构造。旧证明不直接给这些matching端点条件，本证明也没有覆盖旧任意时间及外部预载模型的全部范围。单位匹配分量和流整数性本身是标准工具；全球新颖性或独立成文价值未认证。

若一个候选复制器在同一个原P中以多个machine unit-presence编码同一Boolean位、两种完整严格模式都可行，并要求所有弱调度仍全相等，则任取两个输出，本定理会在B(k)阈值给mixed实际σ，击破该**裸presence**合同。它不排除任务身份标签、其它外部边界锁定、不可私有化的共同资源或一般source相关decoder；也不给任何NO实例的严格见证。它是反面归约工具的准确限制，不是主目标反面。

Evidence / Counterevidence / Status / Related Files：精确陈述先行独立重构与后读实际证明见[审查](../../reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md)。完整数学证明与sharp家族不依赖有限枚举；没有新通用胶合软件。外审/新颖性未认证，UM-TARGET-v1及其反面保持OPEN。

## 7. 任意不同tiny时间的三半系数推广

**ID/version：UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1。**

**Exact Statement / Objects / Domain / Quantifiers。** 任意显式合法UM、全部有限p∈{1}∪[0,a]，给二进制有理0≤a<1；两份实际完整σ₀,σ₁均C_max≤T=1+a。定义unit-presence同前，给两不同测量机，presence在σ₀均0、σ₁均1。无arity、small行预算、DAG或同小时间假设。对每个两位向量可确定性总位多项式输出全部原任务实际σ，使两位恰指定且

\[
 C_{\max}(\sigma)\le\tfrac32(1+a)=\tfrac32T. \tag{4}
\]

特别a<1/3时mixed绝对负载<2。统一系数3/2不能降低：§5奇数k→∞、a=1/k给mixed恰3T/2，且a→0。a1/3的k3例mixed恰2，不声明边界也总能绝对<2。不声明每个单独a均达到该系数。

**Definitions / Assumptions / Dependencies / Scope。** tiny端可为0且可彼此不同；unit始终指时间精确1，a<1确保它与tiny端不重合。依赖第2节同一unit匹配分量分解及下述两选择加权半整化，不调用一般ST算法或新source hardness。两实际见证仍必须给出；这不是一般调度三半算法，也没有处理只给分数点、改变任务身份或锁定其它边界的复制器。

### 两选择半分数的加权舍入，引理与自足证明

给若干items，每个可选两台不同机器，两个端的非负成本可不同、都≤a。若两选项在同一机器，则固定选择较便宜成本（virtual item的两个选项可对应不同端点job），其负载不超过原半半均值。单选项也先固定。其余每个item保留两个incidences，各有该机真实成本。

每台机器把这些incidences按成本非增排序，相邻两两配对，至多剩一个。另把每item的两个incidences配成job对。由“机器对”和“job对”组成的图度≤2、路径或交替偶环，故可二着色，使每个job对及机器对都一红一蓝。选所有红incidences，每item恰选一合法端。

在某机器i，设待舍入端成本q₁≥q₂≥…≥q_s≥0。每机器对恰选一个，所以所选总成本相对半半均值的偏差至多

\[
 \frac12(q_1-q_2+q_3-q_4+\cdots)\le q_1/2\le a/2. \tag{5}
\]

奇数尾项按+q_s计入；最后不等式由q₂≥q₃、q₄≥q₅等相邻比较。偶数尾项同样成立。这是全部机器同时的实际选择，非独立随机期望；固定项只减原均值。排序、路径/偶环二染色、实际选择都按显式item数与有理位长多项式。

### 用在真实unit匹配分量上

第2节分量分析仍成立，因为两见证T=1+a<2。若应vacant的测量机位于job–machine路径，从σ₁翻该单分量，只新增一枚tiny端点job、成本≤a，其余unit数不增；全机负载≤1+2a≤3T/2（a<1）。

否则同第4节选machine–machine方向，全部job–machine分量active。剩余两见证都tiny的原job及job–job virtual items，两个备选成本分别是相应真实tiny端成本，可能不同。半半分数的逐机负载μ_i仍不超过两见证tiny负载的均值；全部active只删除一些非负half tiny。用引理(5)得到实际tiny负载≤该均值+a/2，并据virtual选择恢复全部原unit匹配及端点job。

两见证都unit-present的机器，tiny均值≤a；最终至多一件unit，所以总负载≤1+3a/2≤3T/2。presence不同的机器，tiny均值≤[(1+a)+a]/2=1/2+a；最终总负载≤1+(1/2+a)+a/2=3T/2。两见证都unit-vacant的机器不会新增unit，tiny总负载≤1+a+a/2≤3T/2。全部原机器同时受控，测量位不受virtual方向影响。a0时所有tiny成本0，同一构造合法，无除a或按1/a枚举。

Evidence / Counterevidence / Status / Related Files：这是输入域与时间规则改变后的新ID，未悄悄改写前述uniform锐B(k)；uniform版偶k的格整化仍更强。精确陈述先行与后读审查的实际对象见[审查](../../reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md)。没有新通用胶合实现或外审；新颖性未认证。它只排除tiny时间下的裸unit-presence复制合同，保留medium时间、任务身份/共同外部约束与一般主目标的开放性。
