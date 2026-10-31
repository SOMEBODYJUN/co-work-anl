# 原作业三阶共同矩的条件子树流与集合包含容量证书

2026-10-18，scratch canonical 草稿。建议统一 ID：`UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2`。

本文合并一般 DAG 的必要条件流与一族可直接计算的容量反证。它不修改此前冻结的 Exact、作者 Proof、精度说明或审计。一般 UM 的固定小于二近似及其否定都没有解决。当前证据是作者证明、有限精确算术审计及 root 对前置材料的实际阅读；独立审查仍待完成，不能把 root 已知作者论证称为独立重构。

## 一、原作业、共同量词与必要系统

原输入是有限分层 DAG。全部 jobs 是两个不交集合：unique-home native jobs，以及额外 unit-only 入口 jobs。每个内部机器 v 拥有 k_v>=1 枚不同的 unique-home 原作业，每枚在其唯一 home v 的时间为 1/k_v，其余有限位置只可能是后层机器，时间均为一；不同作业的 unit 菜单可以不同。每个内部行的完整 home 预算恰为一。额外 unit-only job 没有 home，只在其有限菜单上时间一。sink 没有 home jobs、没有 k_v、r_v 或导出配额，只有 unit 流入容量。全部原作业必须完整分配；不得把需求 k_v 当成免费展开的二进制数量。所有系数均为普通二进制有理数。

对内部行 v，记其原 home 指示和、原 unit 导出指示和及非home unit 流入占用为 H_v、O_v、C_v。于是

    H_v+O_v=k_v,
    load_v=C_v+H_v/k_v,
    g_v=T-load_v=T-1-C_v+O_v/k_v.

对 sink 另有 load_v=C_v，其 g_v=T-C_v；不把上面的内部行恒等式用于 sink。

以下固定有理数 1<=T<2。使用同一个作用于全部原有限端点变量、次数至多六的线性泛函 L，满足 L(1)=1、原 Boolean 及 job-one-hot 理想至六次、共同矩阵 M3 半正定，并对每行及每个次数至多二的全局多项式 q 有

    L(g_v q^2)>=0.                              (1)

每行的一阶和同一行二阶矩，须与该机器完整合法 CONFIG(T) 的某个分布一致。这是完整行配置的一、二阶接口，不是仅负载期望。所有行使用同一个 L；不能分别找逐机二阶表后声称有全局点。

每个真实 T 调度的 Dirac 泛函满足上述必要系统。本文不假设一般有理 SDP 精确可行性可以在标准位复杂度下免费求解，亦不把某个低阶点的扩展当成免费操作。

## 二、三阶矩支付的投影规则

T<2 意味着合法行配置不含两枚不同原 unit 流入端点 R、R'，故 L(RR')=0。n=RR' 是次数二的 M3 零向量；它先消去所有次数至多三的乘子。若 l 为线性式，则

    L((n l)^2)=L(n l^2)=0,

所以次数三向量 n l 也为零。将任意四次单项式拆成线性因子乘三次因子，可再得 L(n w)=0 对所有 deg(w)<=4 成立。所有 Boolean 化简的总次数不超过六。

因此 C_v 及任意 unit 行流入端点的子集和，在下文所需次数内都是线性投影。原作业的导出总指示 1-home 也为线性投影。至多三个这些投影或补投影的乘积 P 有

    L(P)=L(P^2)>=0.                             (2)

这是共同 M3 中的平方与零向量推导，不是假设跨机器乘积自动非负。特别地，全文没有把任意半正定矩阵的非对角元称为非负。

## 三、任一正质量原入口产生一个新的子树一阶流

取某原非home unit 入口端点 E，位于机器 v，p=L(E)>0。E 可来自上游 unique-home job 的导出，也可来自额外 unit-only job；即便 k=1 时 home 时间恰为一，home 端点也不据此被算作入口 E。对所有机器 u 定义 b_u=L(E C_u)；对内部后继行 u 和它的原导出端点 x_(u,j,w)，再定义

    b_u=L(E C_u),
    y_(u,j,w)=L(E C_u x_(u,j,w)),
    S_u=sum_(j,w) y_(u,j,w),
    r_u=k_u(2-T).

由 (2)、原作业 one-hot 及 unit 行容量，得到

    0<=b_u<=p,
    y_(u,j,w)>=0,
    sum_w y_(u,j,w)<=b_u        每枚原 job j,
    sum_j y_(u,j,w)<=b_u        每条原机器弧 u->w.    (3)

例如最后一式使用 w 行投影 F_uw=sum_j x_(u,j,w)，以及非负量 L(E C_u(1-F_uw))。不能把多枚同菜单作业压成无身份的大流而跳过这个每弧上界。

逐个取 q=E R 对 u 的每个原 unit 流入端点 R 使用 (1)，再求和，给出

    S_u>=r_u b_u.                               (4)

由次数三平方 E x(1-C_u)，还有

    L(E x)-L(E C_u x)>=0.

故对任意后继 w，

    sum_(u,j) y_(u,j,w)<=L(E C_w)=b_w.            (5)

入口 E 自身属于 v 的 unit 行，因而 b_v=p。

现在从 a_v=p 开始，其他同层及上层活动量置零，按 DAG 拓扑序构造新流。到达 u 时，令 a_u 等于已经构造的总流入；由 (5) 归纳有 a_u<=b_u。若 b_u=0，导出置零；否则可取

    f_(u,j,w)=(a_u/b_u)y_(u,j,w).

则每个原 job 的总导出及每条原机器弧的流量至多 a_u，所有顶点活动至多 p，并在每个内部行有总导出至少 r_u a_u。sink 只接收流，不施加导出 cover。若需要精确实数配额，可改取

    f_(u,j,w)=(r_u a_u/S_u)y_(u,j,w)

于 a_u>0 的行；系数至多 a_u/b_u，故所有约束仍成立。除以 p 后，这正是根 v 活动为一、所有机器容量为一的 canonical 分数子树流。

这里的“新”有实质量词：所得流不保留原点的一阶、二阶或更高矩，不是原共同点的 canonical 扩展。辅助子树 LP 保留根及后继的原 home-token jobs 的原菜单，以 E 为固定根入口；若 E 属于上游 unique-home job，其 home 和上游所在行不在此辅助子问题中。其他外来 selector/unit jobs 不在这个辅助问题中。它不是原完整实例的一个新全局配置点，也没有给那些其他原作业免费找到分配。

若给定的是有理矩条目，以上算式是多项式位时间构造。也可完全不求 M3 点，直接从显式原菜单建立普通有理子树 LP，测试是否存在上述新流。若该必要 LP 对 v 不可行，则所有进入 v 的原 unit 端点在任何所述共同点中质量均为零。结合 mandatory job 的 one-hot，可得整个实例的 sound FAIL；单个入口或单个候选点被拒绝本身不能推出 OPT>T。可迭代删除已证明强制零的 unit-head 选项再测，仍只需多项式个普通 LP。只删这样的端点选项，不删除 home、不删除整枚原 job，也不丢弃额外入口 jobs；原完整实例的 one-hot 始终保留。

## 四、实数配额、整数网格和单位走廊

一般 r_u=k_u(2-T) 是实数，不得免费换成 ceil(r_u)。真实调度的整数导出需求并不自动成为条件一阶矩的不等式。因此不能先向上取整，再直接套整数 fullquota 的 half-star 贪心。

若每行 h_u=(T-1)k_u 为整数，则上述精确 r_u 流还可作辅助子树问题的完整 CONFIG(T) 一阶分解。活动行的保留 home 边际为

    1-sum_w f_(u,j,w)/a_u,  j=1,...,k_u.

它们在 [0,1] 内且和为 h_u，属于 h_u-subset hypersimplex；故可分解成恰保留 h_u 枚 home 的配置。将 home 子集与原 unit 流入标签分布配对，再以剩余概率使用全 home 的非活动配置即可。这只匹配新流的一阶，不匹配原同一行二阶；也不补齐原实例的其他外来 unit 作业。一般非整数网格不据此声称完整 CONFIG 一阶分解。

k_u=1 有一条额外精度：它唯一的 home 端点 Y 时间也是一，完整同一行 CONFIG(T<2) 给每个 unit 流入 R 的 L(RY)=0。这些 incoming/home 零向量不同于一般证明只用的 incoming/incoming 排斥。M3 零向量支付

    L(E C_uY)=0,
    S_u=L(E C_u(1-Y))=b_u.

故新流可在这行精确发送 a_u 单位，任意显式长度的 k=1 走廊均不衰减，T<2 即足够。若抽象合同只给 incoming/incoming 零矩，不能据此宣布同样的走廊结论。混合网络可以只在有此额外 pair 支付的 k=1 行将有效系数改为一，其他行保持实数 r_u。

## 五、明确集合包含原矩

令 q 为正的四倍数，m>=100q。定义

    N=binom(m,q), C=binom(m-q,q), K=binom(2q,q),
    G=binom(m,2q)=NC/K.

给正整数 s1、s2，且 d1=floor(C/(K s1))、d2=floor(K/s2) 均至少一。物理机器分为不同的三层：每个 q-subset S 对应 U_S，每个 2q-subset W 对应 B_W，每个 q-subset R 对应 Z_R。

- 一枚原 selector h 在所有 U_S 上时间一。
- 每个 U_S 拥有 d1 枚不同的原 f 作业，home 时间 1/d1，所有 S subset W 的 B_W 上时间一。
- 每个 B_W 拥有 d2 枚不同的原 e 作业，home 时间 1/d2，所有 R subset W 的 Z_R 上时间一。
- 其余位置均为无穷，无其他 jobs 或预载。

共有 2N+G 台机器、1+N d1+G d2 枚原 jobs、N+N d1(1+C)+G d2(1+K) 个有限条目。d1、d2 均由显式 jobs 支付。

定义整数

    H=sum_(j=q/4)^q binom(q,j)binom(m-q,q-j),
    M=sum_(j=0)^(q/4-1) binom(q,j)^2,
    delta=2-T.

任何正质量原 selector 入口必须满足

    delta d1(delta d2-M)<=H.                    (6)

因此严格反向不等式直接输出 FAIL，并证明原 OPT>T，无须求解 SDP。

## 六、共同容量切的证明及全部 jobs 证书

固定 U_S，令 A 为其 selector 端点，p=L(A)>0。第一层负载的 q=A 局部化给 L(A O_S)>=delta d1 p。对 B_W 定义 b_W=L(A C_W)、y_W,R=L(A C_W X_W,R)，其中 X_W,R 是该 B 的所有原 e jobs 导到 Z_R 的和。第二、三节给

    sum_(W containing S)b_W>=delta d1 p,
    0<=y_W,R<=b_W,
    sum_R y_W,R>=delta d2 b_W,
    sum_W y_W,R<=p.                             (7)

令 H_S={R:|R intersect S|>=q/4}。其大小为 H。每个 W containing S 可写成 S 与另一 q-set 的不交并；它的 q-subsets 中，恰有 M 个不在 H_S。因此该 B 至少向 H_S 发送 (delta d2-M)b_W 的条件流。若系数非负，求和 (7) 即得 (6)；若为负，(6) 自动成立。

真实调度也有完全独立的计数解释。选中 U_S 后至少 delta d1 枚不同原 f jobs 导到不同 B；每个这样 B 至少把 delta d2 枚自己的原 e jobs 导到不同终端。每 B 至多 M 个终端在 H_S 外，H_S 全部只能接 H 枚 unit jobs。其他非活动行的额外导出只会占用容量。

CONFIG(1) 的完整一阶证书可显式列出。令 a_U=1/N、a_B=K d1/(NC)。selector 每个 U 的质量 a_U；每枚 f 的 home 质量 1-a_U、每个 eligible B 质量 1/(NC)；每枚 e 的 home 质量 1-a_B、每个 eligible terminal 质量 a_B/K。U 行以质量 a_U 用 selector singleton、否则全 home；B 行对每个 eligible 原 f endpoint 用质量 1/(NC) 的 singleton、否则全 home；terminal 对每个 eligible e endpoint 用质量 a_B/K 的 singleton、否则 empty。所有原 job 覆盖和为一，terminal 总质量 d1d2/N<=C/N<=1。该证书的支持规模多项式于原 incidence；selector 时间一又给出 CONFIG optimum>=1，故其最优值恰为一。

实际完整上界也不省略未选 jobs。选任意 S subset W 及 R subset W，把 selector 放 U_S、一枚 f 放 B_W、一枚 e 放 Z_R，其余每枚原 f/e 都回自己的原 home。峰值为 max(1,2-1/d1,2-1/d2)。这是一个全调度上界，不断言它在有限 q 时最优。

## 七、有限二项式界、取整与总位复杂度

对 j>=q/4，

    binom(m-q,q-j)/C
      =(q)_j/(m-2q+1)^(overline j)
      <=[q/(m-2q+1)]^j.

因此

    H/C <=2^q[q/(m-2q+1)]^(q/4)<(8/49)^(q/4).

又由二项式单调性、在概率 1/4 处的二项式定理及中心项下界，

    M/K<=(q+1)(2q+1)(256/729)^(q/4),
    K>=4^q/(2q+1), C>=99^q, K/C<=(4/99)^q.      (8)

对有理 delta=2-T，取任意固定 a,b>=0，允许 1<=s1<=q^a、1<=s2<=q^b。写 e1=K s1/C、e2=s2/K。真实整数定义给

    d1>=C/(K s1)(1-e1),
    d2>=K/s2(1-e2).

当 q 足够大，e1<=1/2、e2<=1/4、s2 M/(delta K)<=1/4。由此

    delta d1(delta d2-M)/C>=delta^2/(4q^(a+b)),

而 H/C 指数下降，故最终严格违反 (6)，且 d1、d2 为正。对每个固定有理 T<2 都会 FAIL。若要表达任意固定实数 delta>0 的渐近结论，先取有理 0<delta'<min(delta,1)，对算法输入 T'=2-delta' 使用同一证明；OPT>T'>2-delta。这样得到 OPT 趋近二，不要求算法接收或精确计算实数 delta。与此同时 CONFIG optimum 恒为一，而本文指定的 raw SH3 系统在每个固定有理 T<2 最终均无点；更低阈值按可行性的单调性一并排除。这不是 raw SH3 的 near-two gap。

全部二项式数只有 O(m) 位，H、M 各需 O(q) 项，可用精确整数算术。输入识别与有限菜单检查按显式原矩支付，严格比较有理 (6) 不需开方。一般新流部分如需寻找只解普通有理 LP；全文没有免费 exact SDP finder。

## 八、来源扣除、实际阅读及证据边界

原集合包含图与 rare-terminal 计数来自 Bamas 的 primary 论文 [Lift-and-Project Integrality Gaps for Santa Claus](https://arxiv.org/abs/2406.18273)。目标阅读包括其 graph/assignment-LP/subtree/shadow 定义及 connecting-the-dots 段，并读过 growing-depth 图与计数相关段；没有将整篇论文或其全部近似率转换记为已审。literal_budget_attack 另实际 target 核了其参数和条件转换段。paper 只说固定 rho 充分小，本文不把 1/100 冒称为 paper 已认证的全局常数。

原 paper 的 assignment-LP subtree 不必满足 parent 活动约束；raw shadow 的真实共同 Gram 也不自动满足原 unit 行的零 pair。本文的内容是：给定明确的原作业 raw SH3 合同，可合法推出条件 parent-bounded 一阶流，从而在本族得到 sound FAIL。它不反驳原论文所述 hierarchy 结论。固定 rho 下 q 与显式图规模的对数成比例，只有明确付过固定幂 q 的缩放才纳入第七节。

实际有限审计由 `sol_raw_sh3_inclusion_entry_cut_binomial_audit_v1.py` 执行：120 组精确二项式 case，85 组严格 FAIL；q=64 的全部所测尺度与 delta 均 FAIL。另单独检查 q=2,m=6 的小包含原矩：45 machines、106 原 jobs、750 finite entries，690 个显式 CONFIG 支持、全部 106 cover 和 750 一阶端点，完整 106-job path 调度峰 11/6。这个小矩不属于 m>=100q 的渐近反证范围。未生成巨大族的全部矩阵、未枚举全部调度、未调一般 SDP。有限检查不代替上述通用证明。

继续主目标需要更强的共享 owner 机制：低阶条件子树流已经可行，真实分枝仍不能同时拥有其后继。本文没有构造这样的近二共同 SH3 点。把直接 B->terminal 边细分成多层后，不能免费保留“每 B 向同一 terminal 至多 a_B”的一阶上界；多条路径可能在同一 owner 内重合。该 growing-depth 问题另行探索，不混入本已完整陈述的容量结论。


本 v2 仅将 sink/内部行、unique-home 与 unit-only 作业、原非home入口、迭代删端点范围及实数渐近阈值的有理解释写明；v1 和所有旧源字节不变。审计 CLI 的新输出接口另在 v2 脚本中记录，不冒称重跑原默认输出命令。
