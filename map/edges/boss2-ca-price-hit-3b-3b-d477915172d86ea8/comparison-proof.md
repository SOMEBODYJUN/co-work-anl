# LOCAL-PRICE、实际吸收与PROJ续行的精确比较

任务 `boss2-ca-price-hit-3b-3b-d477915172d86ea8`，Boss2。三个核心分别简称 GLOBAL、LOCAL、PROJ-BOUNDARY；补入的只读 SAFE 对象负责真实净券的非负守恒和终点语义。全部结论按当前登记版本及本收据的精确字节引用理解。本稿给比较证明，不新增游戏、完整SPE、钱包或half结论。

## 同一行上的四个等价接口

固定有限**角色**集，指定current角色 $i$，其它角色集合为 $J$，$i\notin J$。一行满足

\[
p_i\ge0,\quad p_j\ge0,\quad p_i+\sum_{j\in J}p_j=1.
\]

在这同一概率行上，以下四种表述等价：

1. 对每个角色 $j\in J$，$p_j\le p_i$。
2. 该行是均匀行 $u_{\{i\}\cup U}$、$U\subseteq J$ 的凸组合，允许 $U=\varnothing$。
3. 对每个实当前价 $c$ 和实recipient续价 $z$，
   \[
   p_i c+\sum_jp_jz_j\le\max_{U\subseteq J}\frac{c+\sum_{j\in U}z_j}{1+|U|}.
   \tag{LS}
   \]
4. 对每个非负recipient续价 $z\ge0$，
   \[
   \sum_jp_jz_j\le\max_{U\subseteq J}\frac{\sum_{j\in U}z_j}{1+|U|}.
   \tag{P}
   \]

LOCAL已完整证明1⇔2及2⇒3：对 $0<t\le p_i$ 取 $U_t=\{j:p_j\ge t\}$，以质量 $(1+|U_t|)dt$ 混合，恰恢复每个坐标；有限断点给有限凸组合。3⇒4取 $c=0$。为核4⇒1，固定 $j_0\in J$，取 $z_{j_0}=2$、其它 $z_j=1$。所有包含 $j_0$ 的非空子集在$P$右侧均给1；不含它的子集给小于1，所以右侧恰为1。于是

\[
\sum_jp_j+p_{j_0}\le1,
\qquad p_{j_0}\le p_i.
\]

若 $J=\varnothing$，概率行就是纯current行，四式均直接成立。这里的“所有价格”不可换成一个固定价格或有限网格；精确支持函数的可达最大值只针对抽象概率行类，不证明所有均匀极点可由CAG同一份数据共同实现。

## 原GLOBAL图的承重假设与归纳

原图固定原完整SPE、actual叶 $Z$、一种合法full或fresh核、该核自己的分母、来源和重新计算的流。正future边进入严格更深角色的真实context；past边与current金额均进入actual角色终点。核在观察随机路径结果之前固定；允许客户重采与多个context同角色，但终点流按同一份来源线性计算。

SAFE在同一context给 $v-D=P-N$、$e=u_i-D\ge0$，退款 $F=N+e\in[0,u_i]$，故full行的current金额是 $D-N\ge0$，其它正额 $q_j\ge0$，且

\[
v=(D-N)+\sum_jq_j.
\]

逐客户两叶共同coverer至少含current；每个单一recipient角色只从该客户取得一次 $1/(c_Ac_B)$，故

\[
q_j\le J_0\le D-N.
\]

fresh用自己的 $\nu,D^F,N^F,q^F$，只接fresh来源；合法删正边把删去量留current，保持上述支配。不同图的分母、初始化或付款不能合并。由LOCAL归一后得到$P$，由SAFE的严格future图得到有限守恒终点流。这两个联合前提正是已发布canonical边 `ca-causal-closure-r34-same-context-to-hitting` 的ALL输入；本任务复用原边，不拆成LOCAL单独足够或另造重复边。

固定目标角色集合 $K$，$k=|K|$，$h=k/(k+1)$。在current $i\notin K$ 的节点，current**已经实际吸收**，其最终 $K$ 值为0。past是实际终点，其值为 $\mathbf1_{j\in K}$。future在 $K$ 中的续值只用≤1，在 $K$ 外的续值按更深角色归纳用≤$h$。没有假定“到达 $K$ 中的natural context就停下”；在 $K$ 中的节点仍可传播，只是总质量上界1。

把这些**完整续值**代入$P$，每个角色子集有 $a\le k$ 个高价项≤1及 $b$ 个其它项≤$h$，故

\[
\frac{a+bh}{1+a+b}\le h
\quad\Longleftrightarrow\quad a\le k.
\]

有限严格future归纳闭合，得到 $i\notin K\Rightarrow H_t(K)\le h$。$K=\varnothing$ 给0；current在 $K$ 时只用≤1。真实owner query初始化也是含owner的均匀角色行，并保current实际付款、past终点和future真实续值，故同一图的全部来源给

\[
A(K)\le M(K)+\frac{|K|}{1+|K|}M(K^c),
\qquad \sum_jA_j=\sum_iM_i.
\]

fresh来源的“不早于源”还须另用actual-prefix reset的不变量；LOCAL的行凸包本身不含此时间支持。原GLOBAL对象已给完整支持证明，本包没有将它推广给任意SD+PROJ图。

## 角色聚合支持不能换成逐端口支持

上述 $a\le|K|$ 使用的是每个recipient**角色**至多算一次，而非每个context端口各算一次。若同一角色有多个输出端口，必须先合并它们的概率，并将该角色的完整续值写成这些端口续值的条件加权平均，再检验合并后的 $p_j\le p_i$。仅有逐端口支配不足。

例如一行在current $i\notin\{\ell\}$ 及两个都终止于角色 $\ell$ 的端口上各给 $1/3$。它在三个端口上是均匀行，但按真实角色合并后 $p_\ell=2/3>p_i=1/3$，最终 $\{\ell\}$ 质量 $2/3>1/2$。它不是LOCAL的角色行反例，而是错把重复端口当不同角色后失去LOCAL前提的诊断。

真实SAFE及PROJ的 $q_\ell\le J\le J+L$ 是对一个**角色**汇总其全部相关客户后成立，不能给该角色复制多份预算。未来只进更深角色、past只到actual客户券，也各自是实际coverer/history条件，不由任意非负图或局部凸包定义产生。

## PROJ保留哪一行，又改变哪一个续值

在同一原策略 $\sigma$ 下，PROJ从任意合法synthetic叶 $F$、角色 $j$、$g=F_{<j}$、$a=F_j$ 定义

\[
R=\operatorname{finish}_\sigma(g,a),\quad
H=\operatorname{finish}_\sigma(g),\quad
f=u_j(F),\quad d=u_j(R),\quad V=u_j(H)\ge d.
\]

逐客户coverer差给

\[
f=(d-N)+\sum_{\ell>j}q_\ell,
\quad d-N=J+L\ge0,
\quad q_\ell\le J\le J+L.
\]

正 $f$ 时这确实是LOCAL的一行：$p_{cur}=(J+L)/f$、$p_\ell=q_\ell/f$。但是其current质量进入**同角色真natural context** $(g,j)$，不是立即进入actual $j$ 终点。相应完整利润系数为 $\alpha=(J+L)/V\le1$；$\alpha$ 与概率 $p_{cur}$ 的分母不同，不能互换。输入 $wf$ 的current金额为 $w(J+L)$，future金额为 $wq_\ell$，所有项共用一个 $w$，恰守恒；若继续接SAFE，必须合并同context输入重算同一份 $\beta$。

重新记 $h=|K|/(1+|K|)$。对 $j\notin K$，若current续行只知最终 $K$ 值≤$h$，把它正确代入完整$LS$给子集上界

\[
\frac{h+a+bh}{1+a+b}.
\]

要求它≤$h$ 等价于 $a(1-h)\le0$，而不是原来的 $a\le k$。有 $a>0$ 时一般不能闭合原归纳。失败处是current的续值从0变为可能非零；不是原GLOBAL证明把所有 $K$ 节点误作吸收节点，也不是LOCAL本身失效。

字面上“立即停止”可放宽成“此current分支的完整终点律恰为 $\delta_j$”；对固定 $K$ 只须该分支最终 $K$ 值为0。要在有一般current续行的网络继承HIT，也可另证相应全网Bellman/超调和屏障与终点闭合。单独 $\alpha\le1$、严格STATIC行损失或有限单次ancestry均没有完成这些全局条件。

## 两层3/4诊断的完整计算与适用域

取两个抽象节点 $s_0,s_1$，current角色都为 $j<\ell$，以及实际终点 $e_j,e_\ell$。在 $s_0$ 各以 $1/2$ 进入同角色续点 $s_1$ 和终点 $e_\ell$；在 $s_1$ 各以 $1/2$ 进入 $e_j,e_\ell$。每一局部**角色**行都是二元均匀行 $u_{\{j,\ell\}}$，非负且和1。每条通往 $e_\ell$ 的边也可等价地先进入一个纯current吸收的角色 $\ell$ 节点；其它recipient仍严格更深，所以此toy不靠放松非current future的角色顺序。LOCAL的抽象凸包合同被准确满足，没有利用它在CAG实例上的适用性来宣称网络可实现。

终点律为

\[
T_{s_1}=\tfrac12e_j+\tfrac12e_\ell,
\qquad
T_{s_0}=\tfrac12T_{s_1}+\tfrac12e_\ell
=\tfrac14e_j+\tfrac34e_\ell.
\]

故 $K=\{\ell\}$ 时 $H_{s_0}(K)=3/4>1/2$。这是有限、无环、完全吸收的网络，说明即使这些性质另已满足，**允许current非零续行的裸LOCAL接口**仍不足以推出原HIT常数。原吸收规则下，$s_0$ 的current一半必须立即成为 $e_j$，不能再去 $s_1$；同一首行的实际终点就只给 $H=1/2$。因此3/4网络不属于原GLOBAL的图类。

这完整核实PROJ-BOUNDARY登记的抽象存在陈述及其精确否定对象：只否定“任意有LOCAL的current续行网络都继承旧HIT”这一放宽后的推断。它不否定原GLOBAL或LOCAL，不给任何同一CAG/完整SPE反例。尤其没有提供同一组客户、标签目录、完整策略、F/R/H、actual Z，以及两层共同的coverer支持和初始化：真实future $\ell$ 端口进入natural context，不保证终点值恰为1；即使它是最后角色，SAFE仍可能有past实际券出口。真实coverer约束是否能给更强的组合定理，要另作证明；本toy既未证明这些约束排除所有此类现象，也未证明它们允许该3/4合成。

## 同一终点律上的HIT与GLOBAL-PRICE互推

固定源角色 $i$，固定一份总质量为1的非负终点律 $T$。若源质量为 $M_i>0$，先除以该质量；零源直接略去。以下两种**终点**接口等价：

- 对所有不含 $i$ 的角色集合 $K$，$T(K)\le |K|/(1+|K|)$。
- 对所有非负actual终点价 $\lambda$，$\sum_j\lambda_jT_j\le H_i(\lambda)$，其中高于 $\lambda_i$ 的其它价格排序为 $\lambda_{(1)}\ge\cdots\ge\lambda_{(l)}>\lambda_i$，且
  \[
  H_i(\lambda)=\frac{\lambda_i}{l+1}+\sum_{s=1}^l\frac{\lambda_{(s)}}{s(s+1)}.
  \]

正向证明以 $\lambda_i$ 为基线，丢去低于基线的负差。设 $\lambda_{(l+1)}=\lambda_i$、$K_s$ 为前 $s$ 个高价角色，则

\[
\sum_j\lambda_jT_j
\le \lambda_i+\sum_{s=1}^l(\lambda_{(s)}-\lambda_{(s+1)})T(K_s)
\le\lambda_i+\sum_{s=1}^l(\lambda_{(s)}-\lambda_{(s+1)})\frac{s}{s+1}
=H_i(\lambda).
\]

反向取 $\lambda=\mathbf1_K$，其中 $i\notin K$；若 $k=|K|>0$，右侧为 $\sum_{s=1}^k1/[s(s+1)]=k/(k+1)$，故直接恢复HIT。空集给0。含 $i$ 的集合只需守恒给≤1。这两个方向均针对同一终点律、同一源与同一核；不能拿不同选择的各自好处组成一份钱包。

## 终点HIT不等价于把终点律当局部行

LOCAL中的完整续价与actual终点角色价不能逐节点直接互换；GLOBAL-PRICE的包络也不同于一次局部最大均价。一个采用原吸收语义、future严格增角色的**抽象**三角色图已能区分它们：节点1的角色行为 $u_{\{1,2,3\}}$，节点2为 $u_{\{2,3\}}$，节点3纯current实际吸收。每个current立即终止，future角色2、3进相应节点，没有past边。其源1终点律是

\[
T_1=(1/3,1/6,1/2).
\]

源1外的单角色质量分别≤1/2，二角色总量2/3，因此满足全部终点HIT及上节等价的GLOBAL-PRICE。然而终点坐标 $T_1(3)=1/2>T_1(1)=1/3$，所以它本身不在以角色1为current的LOCAL凸包。取actual价 $(0,1,2)$，终点价为 $7/6$，局部一次均价最大仅为

\[
\max\{0,1/2,1, (1+2)/3\}=1,
\]

而正确GLOBAL包络为 $2/2+1/6=7/6$。这不是CAG实现声明；它在原抽象吸收合同内已足以证明“终点HIT/终点价⇒终点律仍是源current的局部行”不成立。原LOCAL定理仅约束每个节点自己的行，未作这个复合封闭断言。

## 终点价格与实际共同预算仍是不同义务

HIT/价格上界只对固定来源库存 $M$ 的最终质量成立。指示价给例如

\[
A_j\le M_j+\tfrac12\sum_{i\ne j}M_i,
\]

但未给这个右侧≤actual $u_j$ 或 $2u_j$。常数价 $\lambda\equiv1$ 只给总量守恒；非集中、因果支持、全K同时界均不能把来源 $M$ 改成actual利润。PROJ的natural利润系数≤1、STATIC同一parent列容量≤L、单孩子prefix回推系数≤L，也不能让多个parent、多个来源或已有请求各自重复领取同一actual券。

全SD+PROJ还须单独结算原负项与完整IC松弛、建立适用的非负整体流、控制循环和累计系数、合并同context请求并满足终点角色/客户共同资金。有限单次ancestry只修复利润域；它不保证把所得natural请求再送入SD之后整体仍有限。这里不给一个未经实现的抽象toy增加完整SPE或钱包反例资格。

## 三对核心的处置与交付边界

GLOBAL↔LOCAL：原正向归纳已经由canonical的SAFE+LOCAL ALL边完整实现，本包按原SHA复用；同一终点律的HIT⇔GLOBAL-PRICE已逐式核清，但终点律不保LOCAL凸包。没有另造同义逻辑边。

LOCAL↔PROJ-BOUNDARY：PROJ真实单层确有LOCAL的角色行结构；current入natural续行后，完整续价不能设为actual终点价。抽象两层3/4确证放宽接口失败，未完成同一CAG数据的模型实现。本包新建一条accepted `checks/context`边记录此精确检查，不宣称LOCAL真实适用实例自动产生该toy。

GLOBAL↔PROJ-BOUNDARY：原GLOBAL吸收合同与toy的current续行合同不同；两者不矛盾。PROJ-BOUNDARY只反裸继承步骤，不是原GLOBAL的反例。缺吸收/角色合并支持/真实coverer和整体终点预算时都不能调用原结论。此定向比较已完成；没有将一般开放研究义务再包装成裸重复follow-up。

全部17个原计划refs（12个文件）及新增SAFE的body/evidence已按所列范围实读；计划引用覆盖的短正文另全文读取。九context、六策略、鲜利润等成熟程序均未重新执行。本次只作解析证明、元数据/引用/hash/JSON/边结构自查；所有新文件限于本任务edgefolder与receipt，Git、队列、registry及全图投影由Boss处理。
