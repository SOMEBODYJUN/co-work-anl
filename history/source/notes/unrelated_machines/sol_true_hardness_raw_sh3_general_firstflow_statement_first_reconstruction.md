# 原端 M3 条件出口到单根新一阶流：陈述先行的独立重构

日期：2026-10-18。审者/重构者：sol_true_hardness（6.1sol max）。仅 scratch。

## 1. 读取与独立性边界

本记录依据 parent 发来的 general-flow Exact 文字自行重构，先冻结再看作者 flow addendum 或合并稿；本轮未读取这两类文件。已知且已实际读过的是 inclusion Exact/作者 Proof 的 unit-pair null 工具，因此不称完全 blind 或对所有背景全新。此前 inclusion Exact-first/读后记录原字节均不改。
本文从原端变量完整推导 general claim，不以未来合并稿、作者软件或未读 primary 为依赖。未运行新软件。

## 2. 精确陈述在前

给有限 layered DAG。每个 internal u 有 k_u>=1 枚**显式、不同**原 token jobs；各 job 的唯一 home 是 u，时间 1/k_u，其余有限端均是向后继顶点的 unit heads。不同 jobs 的 head 菜单可以不同。sink 没有自有 jobs。另有任意 mandatory unit-only entry jobs，允许多个候选 unit endpoints。所有处理时间、job 身份和实际 endpoints 均显式输入；不存在免费复制。

取 rational 1<=T<2，delta=2-T。共同 L 定义到次数六，原 Boolean/one-hot ideals 到次数六、M3 PSD、所有物理行完整 CONFIG(T) first/pair compatibility，以及每行 L((T-load_u)q²)>=0（deg q<=2）。不假设 inactive exports=0 或 raw export<=activity。

对任意一枚**非 home** 的原 unit entry endpoint E（在顶点 v），若 p=L(E)>0，则存在下列 NEW flow。在 v 的可达后代子图上，a_v=p；其余顶点 a_w 等于进入它的**原 token head flux** 总和。对每个原 token j 和其合法 head w 设 f_ujw>=0，有

    0<=a_u<=p,
    sum_w f_ujw <= a_u                       (每原 token),
    sum_j f_ujw <= a_u                       (每条原 arc u→w),
    sum_(j,w) f_ujw = delta k_u a_u          (每 internal).

sink 只要求入流活动量<=p。除根的指定 entry 之外，不用任何额外 unit-only entry jobs 作为新流源。可达集之外全零。

还有一个**可选加强版**：对 k_u=1 的 internal 行令总 out=a_u，其余仍等于 delta k_u a_u。这个版本也存在。T>1 时加强版在 k=1 行不再同时声称 out=delta k a；两种输出合同应分开。任意非网格 k 一般不在本证明中替换为 ceil(delta k)。

若所有 internal u 的 (T-1)k_u 均是整数，则 delta k_u 也是正整数。将上述流除以 p，得到的 first marginals 可分解为**辅助单根后代实例**的每行 full CONFIG(T)：只保留该后代图自有原 tokens，并把 E 的 owner 在 v 的端作为固定 root unit entry；其余外来 unit-only jobs 不加入此辅助实例。E 若是某前驱 token 的 head，其 owner 在该后代图之外（DAG），不会重复计为后代自有 token。

这不是原全实例的新 CFG/M3 点，也不保给定 L 的 first、pair、higher moments。给出 rational L 时可总位多项式构造新流；整数网格时还可位多项式给上述逐行有限 CFG 分解。

由此可写一个只依原 input、root v 和 T 的 ordinary rational LP（将 p 归一化为一）。若该 LP infeasible，则在每个 raw L 中每个非 home unit endpoint into v 的质量都为零。可反复删这些原 unit heads，保持所有 token jobs、k_u 和 home 不变；mandatory job 的 one-hot 资格被删空时 sound FAIL，原 OPT>T。未 FAIL 只给 UNKNOWN，不给实际调度或 hierarchy point。

## 3. 原 unit projections 与条件质量

令 C_u 是进入 u 的全部**非 home unit endpoints**之和，包括原 token heads 和 unit-only entry endpoints；k_u=1 时也不把该行自有 token 的 home 加入 C_u。T<2 的 row CONFIG pair compatibility 给不同 unit endpoints x,x' 的 L(xx')=0。

M3 中 xx' 是零范数列，且 xx'l（linear l）仍是零范数列：其范数为 L(xx'l²)=0。故 L(xx'w)=0 对 deg w<=4 成立，总次数至多六。于是任一同机 unit-entry 子族的和是这里所需的 linear projection。原单个 endpoint、complement，以及原 job 一部分 one-hot endpoints 的和也按原 ideals 幂等。

总共至多三个这样的 linear projections 的乘积 P 满足 L(P²)=L(P)>=0。特别有给定 entry E 的条件行质量

    b_u = L(E C_u),             0<=b_u<=p,
    z_ujw = L(E C_u X_ujw) >=0,

其中 X_ujw 是原 token j 的 head endpoint。v 行 C_v 包含 E，其他 unit entries 与它二阶互斥，所以 b_v=p。

## 4. 原条件 z 的四类界

每个 token j 的所有 heads 的和是 1-H_uj（H 是其唯一 home endpoint）。因此

    sum_w z_ujw = b_u-L(E C_u H_uj) <= b_u.                  (4.1)

对一条 arc u→w，sum_j X_ujw 是 unit row w 的子族 projection，所以三投影 positivity 给

    sum_j z_ujw <= b_u.                                     (4.2)

对任一原 head X=X_ujw，非负平方 E X(1-C_u) 的次数是三，幂等约化给

    z_ujw <= L(E X_ujw).

同一物理 w 的全部原 incoming endpoints 只有一份 unit 容量，故

    sum_(u,j token heads into w) z_ujw
        <= sum_(all nonhome unit entries x into w)L(E x)
        = b_w.                                               (4.3)

被丢弃的额外 unit-only arrivals/前驱外部 token entries 的条件质量非负，所以第一和只是子和。这里 (4.3) 是上界，不是把 z 的 incoming 偷换成 b_w。

u 行所有自有 tokens one-hot 给 load_u=C_u+1-O_u/k_u。对每个原 unit entry x into u，用 q=E x（deg 2）做该行 load localizer。平方 Boolean 约化后最高原次数五；unit-pair nulls 给 L(E x C_u)=L(E x)。对所有 x 求和，得到

    D_u:=sum_(j,w) z_ujw >= delta k_u b_u.                   (4.4)

若 k_u=1，其 home H_u 也是 unit。CONFIG pair 给每个 incoming x 与 H_u 的 L(xH_u)=0，再经 M3 零列乘 E，得 L(E C_u H_u)=0。所以此特殊行实际满足

    D_u=b_u.                                                 (4.5)

上述只用原矩与平方，没有给条件后伪分布免费添加原 CFG inequalities，也未要求原 z 已是从 v 单独出发的守恒流。

## 5. DAG 前推与重新缩放：真正 NEW 的步骤

基本版取 r_u=delta k_u；加强版只在 k_u=1 改 r_u=1。由 (4.4)–(4.5)，D_u>=r_u b_u。
对 D_u>0，预先固定 transition coefficients

    c_ujw = r_u z_ujw / D_u.

它们非负、总和 r_u；每 token/每 arc 的系数和<=1，因为 z 的对应和<=b_u 且 D_u>=r_u b_u。
若 b_u=0，则所有 z=0；这种行随后 a_u=0，系数取零即可。

从 v 按 DAG 拓扑序前推：a_v=p，其他 a_w 为已经生成的原 token incoming flux 之和，令 f_ujw=a_u c_ujw。
归纳有 a_u<=b_u：根是等号；若前驱已经满足此界，则

    f_ujw = a_u r_u z_ujw/D_u <= (a_u/b_u)z_ujw <= z_ujw

（b_u=0 时全零），所以 (4.3) 给 a_w<=b_w<=p。每 token/arc 的父活动上界由 c 的对应和<=1 给出；总 out 恰 r_u a_u。

这解释了为什么可去掉别的原 entry sources：从未把 b_u 直接设置成新活动量，而只用其出口形状，在真正从 v 到达的 a_u 上重新定比例。DAG 保证后继不能反过来改变已定 a_u；根也不会收到其后代 tokens。若 root v 本身为 sink，只有 a_v=p，结论平凡。

## 6. 整数网格时的完整逐行 CFG 恢复

以 p 归一化。记 A_u=a_u/p，e_uj=sum_w f_ujw/p。每 token 的 home marginal 取 1-e_uj，head marginals 取 f_ujw/p。其他原 unit-only jobs 没有加入辅助子实例；固定 root entry 的 marginal 是一。每个保留原 token 的 home/head marginal 求和恰一。

令 d_u=delta k_u∈{1,...,k_u}。有 0<=e_uj<=A_u，sum_j e_uj=d_u A_u。A_u=0 时全 home；A_u>0 时 e_uj/A_u 属于 hypersimplex {s∈[0,1]^k:sum s=d_u}，可分成恰 d_u 个 exported tokens 的有限分布。

一个显式多项式支持构造是：令 S_j 为这些 s_j 的累积和。随机 t∈[0,1)，在每段 [S_(j-1),S_j) 中查看是否含 t+n（n=0,...,d_u-1）；每次恰选 d_u 个不同 j，且第 j 项被选概率 s_j。按所有 S_j 的 fractional parts 划分 [0,1)，得到至多 k_u+1 个 rational weights/sets，位多项式可算。

u 的新行分布：概率 1-A_u 取全部 home tokens；概率 A_u 时，按其实际 incoming token marginals/A_u 选择一枚 incoming unit（根则固定 E），独立选上述 export subset，并取其补集的 home tokens。active 配置负载

    1+(k_u-d_u)/k_u = T.

inactive 配置负载一。sink 用各 incoming singleton 加 empty。每行 marginals 都是上述新 first vector；每行支持至多 (k_u+1) 乘 incoming endpoint 数加一，显式多项式。

非网格时不能直接宣称此分解。例如 T=9/5、root k=2，原 actual 可把两个 token 分别全导出到不同 sinks；上述基本 exact-r 缩放可给每 token export=1/5、home=4/5。其 root 一阶负载为 9/5，但有 fixed incoming unit 的 CONFIG(9/5) 至多含一个 home token，故两枚 home 的 marginal 和至多一，而该新 first vector 为 8/5。这个例子只说明非网格 basic exact-r 输出不能免费做 CFG 分解，不反驳可能存在另一种更强输出；本记录不认证 general ceil demand。

## 7. 给 rational point 的总位多项式构造

b、z、D 都是给定 rational moments 的显式和；所需次数至多三，M3/CFG 条件只用于正确性，不调用 SDP finder。c 系数预先固定，长度多项式。后续是 DAG 线性递推 a_w=sum a_u c_ujw，没有反复平方。

可取给定 p 的 denominator 与全部 c coefficients denominators 的乘积作为共同分母上界：每条 DAG path 不重复 arc，路径乘积的分母整除该乘积；a_w 是这些路径乘积之和且 0<=a_w<=p。因此其分子/分母位数被所有原系数位数之和及 input point 位数多项式控制。归一化除 p、逐行 hypersimplex 分解和 incoming-product 权重也只付多项式位数与支持，不按 1/p 数值循环。

## 8. 普通 LP 检测与逐删的 soundness

把 §2 的 p 固定为一就得到 ordinary rational LP：变量数/约束数随原 finite token endpoints 和顶点数多项式。可选择 basic 或包含 k=1 加强式的版本；上述构造分别证明任意 raw point 的正 unit entry 都使对应 LP feasible。
因此 LP infeasible at v 时，每枚非 home unit endpoint into v 在**所有** raw points 中均有一阶质量零，不只是某一个 supplied point。

删掉这些 unit heads 不删任何 home、不改变 k_u、不把原本有自有 tokens 的无后继顶点改成免费 sink。实际 T-schedules 必不使用被删头，因此每次删除都保持“原实际 T-schedule 若存在，则在剩余资格仍存在”。mandatory unit-only job 的资格删空即 sound FAIL。

若还需跟踪 raw points 的 restriction，也合法：L(x)=0 的原 Boolean endpoint x 是 M3 零列；对 deg<=2 的单项式 m，xm 仍是零范数列，因此 L(xw)=0 对 deg w<=5 成立。删除端点涉及的全部次数<=6 moments 均为零，principal M3、ideals 和负载 localizers 可限制到剩余变量。原 row CFG 分布中 x 的 marginal 为零意味着所有包含 x 的非负权配置都没有质量，故原 first/pair compatibility 同样可限制。one-hot 被删空就矛盾。

最多删除原 unit endpoint 总数次，每轮 ordinary LP 大小、T/k_u 系数位数都由原显式输入支付，所以迭代可总位多项式完成。UNKNOWN 无可行性承诺，整数网格的辅助单根 CFG 也不给原全实例 decoder。

冻结意见：parent 所给 general NEW-firstflow 合同可以这样自足重构；k=1 optional strengthening 与 generic exact-out 要分合同表述，非网格 ceil/full-CFG 不外推。作者 flow addendum/合并正文尚未读，不提前代签。
