# 有界叶资源重数私有树 v3：陈述先行独立重构

审查者：boss11 内部 cover_consistency。实际只读 Exact `private_tree_bounded_multiplicity_floor_v3_exact_statement.md`，SHA256 `8fd533805efaf7ab6168d0512dea327e70360065d05b4df2d52a178a49279142`。冻结前未读作者proof、其它代理本v3记录或询作者思路。已知本人v2 CONFIG/hitting/Haxell证明及原先单树q子可加性背景，明确披露；本v3的rainbow限定、multiplicity blocker、全部CONFIG阈值和α_μ是在新陈述后重新证明，不把v2注入结论自动套用。

结论：L/A/B均可独立闭合，未发现standing fatal objection。资源hitting必须按逆像multiplicity计数；在共同容量也按同一multiplicity计的前提下，不额外损失一个μ因子。存在性没有升级为一般变参下的σ算法。

## 1. q的子可加性：本次自足复核

在满a叉高h树上定义q(W)为叶集W含有的最高uniform branching。h1时q(W)=|W|，显然q(X∪Y)≤q(X)+q(Y)。h>1时设p=q(X)、t=q(Y)。若p+t≥a则结论由q≤a自动；否则假设union有full(p+t+1)-ary子树，它在至少p+t+1个children中分别含相同branching的子树。

对子树用高度归纳，每个这样的child都满足q_child(X)+q_child(Y)≥p+t+1，故或q_child(X)≥p+1、或q_child(Y)≥t+1。然而前一种children最多p个（否则X有full(p+1)-ary树），后一种最多t个，总数不足p+t+1，矛盾。故q子可加，可反复用于任意有限叶集合的并。

空集合q0有效。高度0不直接套此q定义；归纳从height1开始，因此没有把单叶的空分叉误当a叉。任意非空叶集至少含一条full1-ary根路径。

## 2. L：rainbow提取与资源blocker

给任意叶集W，将每个颜色在W中的occurrences任意编号1,…,m_z≤μ，把同编号的各色occurrences放在同一组W_i。得到至多μ个组，每组全局rainbow；不存在同一资源在同一组重复的问题。

完整叶集的q为a，因此a≤Σ_i q(W_i)。至少一个组的q≥ceil(a/μ)，该组内相应full subtree的叶全部异色，证明L1。特别μ2、a3给binary rainbow，对任意h成立。

更一般地，若某叶集W内不存在rainbow full r叉高h子树，则每个组W_i都只能q≤r−1，否则其raw r叉子树本身已rainbow。因此

 q(W)≤Σ_i q(W_i)≤μ(r−1)。             (1)

现在X命中全部rainbow r子树的资源像。删去D=f^−1(X)，剩余W没有rainbow r子树，故q(W)≤μ(r−1)。令k=μ(r−1)+1；假设μ(r−1)<a保证1≤k≤a，D必命中全部raw full k叉高h子树。

raw叶blocker精确值为(a−k+1)^h：归纳上要杀死至少a−k+1个child，各需前一高度blocker，且递归删除可达。因此

 |f^−1(X)|=|D|≥(a−k+1)^h=[a−μ(r−1)]^h，

即L2。这里不是先把一资源算成一叶，更没有声称X自身大小也满足同一界；一个资源可能删μ枚原叶，原命题只要求逆像计数。该推理给下界，没有证明每参数都达到它。

当r1时k1，X要命中所有单叶路径的资源，即包含全部出现资源；逆像就是全a^h叶，与公式一致。当μ很大时ceil(a/μ)=1仍合法。μ是binary输入也无存在性困难：证明可只列非空occurrence groups，最多原叶数，其余空组q0，不需执行μ次循环。

## 3. A：multiplicity容量与Haxell严格条件

为每root列所有真实state内的rainbow full r子树资源集。每candidate含R=r^h个不同资源，故加root后每超边总大小R+1。L1及μ(r−1)<d保证各state存在此类candidate；也可从L2对空hitting集的矛盾得到非空性。

任取非空root集合I，若资源集X打中它们的全部candidate edges，则对每u∈I、每state s，由L2（ambient branching为d）有

 |f_us^−1(X)|≥b=[d−μ(r−1)]^h。

对给定共同λ加权：

 b|I|≤Σ_(u∈I,s) λ_us |f_us^−1(X)|
      =Σ_(z∈X) Σ_(u∈I,s) λ_us |f_us^−1(z)|
      ≤|X|。

因此资源transversal number τ_I≥b|I|。与v2注入证明不同，本次中间项不能写成|X∩image(f_us)|，它可能小很多；使用真实逆像数恰与Exact共同容量中的multiplicity相同，交换有限求和后仍得到|X|，没有额外μ因子。

若b≥2R−1，则τ_I≥(2R−1)|I|>(2R−1)(|I|−1)，严格差至少2R−1>0。有限Haxell bipartite hypergraph条件给每root一条资源不交edge，每edge保留一个真实state/r子树见证。因为候选本来只收rainbow树，rank确为R个不同resources，不是μR，也不把raw非rainbow叶集混入。

外部定理及资源/总edge-size参数沿用前一阶段已实际核primary：Annamalai arXiv1509.07007v2 PDF2/印1 Thm1.1、AFS2008作者稿PDF5 Thm2；总edge size k=R+1给2k−3=2R−1。没有新读作者v3proof或冒称重证Haxell1995原作。

## 4. B：CONFIG(T)到有界重数a-tree共同分布

v2已核的行系统对非注入f也精确：T∈[1,2)，s=floor(d(T−1))、a=d−s；incoming边际q、各out-unit边际t_e满足Σmin(q,t_e)≥a q。资源行是对所有真实leaf jobs求Σt_e≤1，重复资源不去重。

按v2独立抽取机制，从每root先按selector marginals选一个state，在私有树上生成满a叉高h的局部分布。节点activation mass b≤q时，Σmin(b,t_e)≥(b/q)Σmin(q,t_e)≥a b；选择child masses≤min(b,t_e)、和a b，并分解成size-a子集条件分布。零b跳过。每leaf activation marginal≤原t_e，故所有root共同resource expected request **multiplicities** ≤1。

每个生成candidate a树只是一个完整原state的叶子集，原每资源重数≤μ立刻给candidate内重数≤μ。它无需注入。对有限局部分布中的每个正权candidate，应用L2（ambient branching为a），任意命中其所有rainbow r子树的X均使候选内|preimage X|≥[a−μ(r−1)]^h。按同一局部分布加权，仍得root-subset transversal下界与第3节相同；假设提供Haxell阈值即可选全roots资源互斥的rainbow r树。

本次distribution的resource行必须是expected number of leaves，不是仅“某资源被至少使用一次”的概率。CONFIG外机job边际正好是前者，所以L2所需multiplicity加权成立。每root归一化和1、各资源行共同，未为不同X或resource另选分布。

辅助a-tree可指数多，且来自同一原state的不同candidate可能共享内部机器；最终每root只取一条Haxell edge的一个见证，跨root原机器全私有，故不会产生内部冲突。只是在有限组合论证中列candidate，并未新建原P机器或任务。

## 5. 特别r与α_μ算术

取r=ceil(a/(μ+2))。a≥1给1≤r≤a。又r−1<a/(μ+2)，故μ(r−1)<a，所需strict前提成立。

由整数ceil界，(μ+2)r≤a+μ+1，等价

 a−μ(r−1)≥2r−1。

对r,h≥1有(2r−1)^h≥2r^h−1（写r=1+x展开二项式，每个正次项的2^j≥2）。所以全部数值前提成立，包括a1、r1、h1和μ远大于a。

记c=1/(μ+2)、x=a/d∈(0,1]，r≥ca，故C≤2−c x。T0=1+s/d=2−x，α_μ=2−c。计算

 α_μ T0−(2−c x)=2(1−c)(1−x)≥0。

因此Exact的完整链OPT≤2−r/d≤α_μ(1+s/d)≤α_μ T成立。μ1给α5/3；μ2给α7/4。并非把r/d直接当r/a，也不要求μ固定才能成立这条输入相关界；只有要从它得输入无关的ε时才须固定μ。

T≥2的所有outjobs父置、selector任选状态根给C≤2，补齐阈值。非空selector给Tconf≥1，CONFIG可行阈值在有限网格1+j/d上变化且2可行；所以整体配置gap≤α_μ。没有把T1结论无证明推广到全T。

## 6. 原d树全部jobs与退化

最终每root选一真实state/r树，selector放根。r树内节点有一unit incoming、r个出job下送、d−r个small留父，实际负载2−r/d。原state其它分枝的父edge留在上方，故无unit incoming；其全部d个出jobs父置，负载1。未选或零权states也全部父置，负载1。rainbow且跨root资源互斥保证每外机至多一个unit，负载≤1。未选叶即使与选叶同色也留父，不向外机加负载。每个原job恰处理一次，机器/finite ends/处理时间都未改变。

d1、a1、r1有效：每state单叶自然重数1≤给定μ，Haxell退Hall，实际C1。U为空时所有tree/selector jobs为空，返回0/空σ，不套下界1。非空state有至少一叶，合法f不可能映到空Z；不额外制造资源。λ0状态仍有原jobs，按上述回填。μ可大于真实max multiplicity，只使α界更弱；不造成错误。

## 范围及算法层级

本v3不要求E、Latin或任何路由结构。凡具体编译器输出符合该完全私有unit/1d模型且每完整state重数≤固定μ，已能对其整个CONFIG间隙得统一常数α_μ<2。自然CONFIG1证书、具体μ bound和外部source性质仍须另证，不从source balance自动获得。

μ随输入无界时α_μ趋2，不能据此宣布一般UM统一sub2算法。Haxell候选族与匹配搜索不保证一般变参位多项式；前面的局部组合存在性和v2精确LP可行性也不能替代σ构造。本稿只给Exact-only独立数学审查，未读作者proof、无实现/有限枚举/新颖性或发表价值认证。
