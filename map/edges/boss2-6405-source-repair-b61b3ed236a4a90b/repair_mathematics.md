# 当前输入的定向数学复核

本页属于 `boss2-6405-source-repair-b61b3ed236a4a90b`。只修复改变的登记输入及其受影响关系；四条旧边的具体去向在收据中逐项给出。这里的独立复算不替代全称证明，也没有重新认证历史软件或外部新颖性。

## 固定行度的插值和原 raw 合同

两对象使用相同的普通 U/B/Z 端点结构，但指定的组件数 M、背景法则和配置合同不同。raw 对象是 degree-four common functional、M2、first/pair CONFIG 与全输入 affine localizer；固定行度对象先固定整数 d≥2，再令 k≥d、s=d−1、D=max(4,d)，逐机匹配全部 degree≤d 行矩。即使 d=2，指定 M/Qnew 也不同，不能把两条整定理标作等价。

实际 OPT 不依赖 M。若 selector 所在 U 的峰 C<2，至少 r=k−floor(k(C−1)) 件 f 离开 U；它们进入不同 B，每个这样的 B 又至少导出 r 件 unit e。k 台终端不能装下超过 k 件 unit，故 r²≤k。反向取 u=floor(sqrt(k)) 件 f 去不同 B，并从每台选中 B 导出 u 件 e 到 u² 个不同终端，其余所有组件所有任务留 home，得到完整峰 2−u/k。

固定行度的新增步骤须自己支付。令 Z=sum_{u=0}^s binom(k,u)、Amax=binom(k−1,s)，并对 |S|≤s 取 b_S=(−1)^(s−|S|)binom(k−|S|−1,s−|S|)。有限差分在零点的展开给任意 degree≤s 的 f 以 f(1)=sum_S b_S f(1_S)；等价地每个 |A|≤s 都有 sum_{S⊇A}b_S=1，且 sum_S b_S=1、|b_S|≤Amax。

关键是整行多项式 p(R,Y)=p0(Y)+sum_j R_j p_j(Y) 中只插值 p_j，因 deg(p_j)≤d−1；纯 home 的 p0 可有 degree d，不能错误地对它套 degree s 的插值。采用

    (1−a)rho_Q + a delta_(0,all)
      + (a/L) sum_(j,S)b_S delta_(j,S)
      − (ak/L)sum_S b_S delta_(0,S)

后，pure-home 修正逐项相消；一个 incoming 与至多 s 个 home 的矩由插值匹配；两个不同 incoming 的矩两侧均零；重复因子用 Boolean 化简。这覆盖整行合同。Rfill 提供每个 (j,S) 至少 1/(4LkZ)、每个 (0,S) 至少 1/(4LZ) 的背景质量，M−1≥4kZAmax 正好吸收所有负修正。总质量仍一，所有 unit 配置至多 s 件 tiny home，负载≤1+s/k。

raw 证明可独立复用的另一部分是维度无关 affine slack。写单组件 q=beta+sum c_jb F_jb+sum d_blt G_blt。Qold 三类样本值满足 c_jb=qF_jb,pi−sum_l qN_bl,pi(l)+(k−1)q0。三项平方估计、置换平均和三分支权重给

    ||c||² ≤ [12kL+12Lk³+6kL(k−1)²] E_Qold(q²)
            ≤30Lk³ E_Qold(q²).

Qnew 有一半 Qold；在目标 T=1+s/k 下 Qold slack≥1/k、Rfill slack≥0，故 Qnew 的贡献至少 ||c||²/(60Lk⁴)。H 的平均 slack (s−1/2)/k>0；将截距完成平方，利用 E_H S²≤(k/L)||c||² 和 |g|≤1，得到 H 贡献≥−2||c||²。以 a=1/M 混合且 M−1≥120Lk⁴，localizer 非负。对全输入 q，条件于 selector 后其他组件独立；它们的均值吸收入截距，方差乘正平均 slack，故无 M 维度因子。

这是旧边真实的局部 contribution；Rfill、插值、非负质量、固定 d 生成复杂度和归一化趋二仍由目标独立证明。下一阶 mixed term 的自然有限-law 延伸为 a/L，而合法 CONFIG 给零；跨行 selector×incoming 的负容量事件也仍失败。它们只切给定点/给定延伸，不能宣布所有更强点不可行。固定 d 的指数可依 d，不能推广到 variable-d 统一多项式算法。

## 完整门控值桥与两种福利保证

输入每 state 非负有理资源系数和恰一；组与 indexed state 显式有限，bundles 全局不交。完整矩阵保 root pin、每组 connector、每组一个 selector、每个 listed incidence，包括零 incidence 和未选 states。未列零系数不凭空生成物理 job。

给平衡见证 b>0，root pin 留 root；H 内 connector 去 gate、selector 去 attaining private；H 外 connector 留 root、selector 去 gate。只将选中 state 在其 bundle 中的正 incidence 导出资源机；其余全部 incidence 留各自 private。根负载 2−|H|/n，选中 private 负载 2−v_g(B_g)，其他 private≤1，每个 gate 恰一 unit，每个资源至多一 unit。因此覆盖全部原任务且峰≤2−b。b=0 用 pin/connector 全留根、selector 去 gate、incidence 全留 private 的峰二基线。这里不能把“其余全部 incidence 留 private”写成“其余全部 jobs 留 private”。

反向任意完整 C<2 调度，令 H 为 connector 真正在 gate 的组。根给 |H|/n≥2−C；这些组的 selector 必须去 private，并导出至少 2−C 的正 incidence 质量；资源 unit 不能双占，故 bundles 全局不交。因此 OPT=2−beta*，根 pin 给 OPT≥1。这一值桥不要求 FSLP。

unit-FSLP 则另要求正支撑容量 sum lambda≤1，而非加权 sum p lambda≤1。独立 state 的正 tail 总概率≤1，尾层求和给福利≥(1−1/e)n>5n/8；精确条件期望用有理乘积，条件化后不重套初始概率和≤1。由每组价值≤1，高质量组数在 0≤delta<5/8 时大于 ((5/8−delta)/(1−delta))n。该有 FSLP 的绝对峰保证与任意 norm1 菜单的比例算法分立。

全类比例算法另解 z/x 福利 LP，state/coin 两阶段给 W≥(1−1/e)L。排序扫描给 beta_hat；若 h=# {g:r_g>beta_hat}，则 h/n≤beta_hat，否则第 h 项会超过扫描最大值。因而 W/n≤h/n+(1−h/n)beta_hat≤2beta_hat−beta_hat²。最优平衡见证给 W*≥n(beta*)²，结合 13/8 的正二次余量才得全类比例。值桥边只完成 OPT 分母与完整回填这一步，不冒充这些额外步骤或两份独立证明。

## 正事件 NC 的完整达到 law 和共同联合性

固定 k≥2、r≥k、1≤d,q≤k，同一 x 要求 B 的各 home 边际 1/r、每件 small 的 sink 边际 1/r，并仅在同组的正 cylinder 上要求阶数≤d 的上 NC。若 B 在 h，令 D_i 为该组送 sink 件数，每态精确峰为 2−D_h/k。成功强迫 sum_i binom(D_i,s)≥binom(q,s)，NC 求和给期望≤binom(k,s)/r^(s−1)。A_(s+1)/A_s=(k−s)/(r(q−s))≤1，故最强阶 t=min(d,q)。t=1 时最大成功率一；否则为 min(1,A_t)。

达到是同一完整联合 law：均匀选 h；概率 p 用 q-type，在 h 选 q 件、在另外 k−q 个不同组各选一件；概率 1−p 用 1-type，在 h 选一件、在另外 k−1 个不同组各选一件。组与组内选取均匀，每态总 sink 件数恰 k，因此每件 small 边际 1/r。任意同组 s-subset 的全送概率 (p/r)binom(q,s)/binom(k,s)，同时满足所有合同阶。r≥k 使所有 filler 组都可选择。q=1 或 d=1 直接取 p=1，不能形式套一阶比值。补事件和跨组 NC 从未要求。

这份固定 x 的完整 law 不修复条件叶 MC 的 all-core 缺口：每个 (c,s) 的 matching mixture 加相同平均叶边际，仍未给同时抽所有核心状态、同一个叶匹配且逐样本共同不超容量的 law。三 Bernoulli 的互斥警告只是概率兼容性示例，未从原 UM 恢复成反例。两状态多数地板另依赖同一状态内残余束真实不交，不保本节 x/NC；本节 NC 也不提供那份不交束。因此共享审查页不产生两对象的蕴含边。每历史仍保相同 x/NC 时才可用条件乘积；仅每轮无条件合同只可用 union bound。

## 固定汇点的给定阈值与未知最优值

受限算法保持固定 K≥1、唯一 home 的互不交私有组、宏只到 homes、每有限宏端>T/2。共同 sink 向上取整预算按所有 N 个私有任务只花一次；mode 必须带实际任务回溯。占位是覆盖所有宏的 transversal base，而非独立集。模式只记 occupied/empty、不依具体宏身份，才能由 base 面维数和标签纤维得到 K 条侧约束只留≤2K 个非单值 home。大贡献模式先固定，小贡献改变支付 sink 增量；带下界宏匹配及每组实际回溯恢复全部任务。这是数学算法，旧有限枚举不是通用 LP 或生产 scheduler。

原 whole_result 边仍完整有效。未知 OPT 另承诺每有限宏端>OPT/2。零端预检处理 OPT=0；共同分母积 D 给正整数 q*=D OPT。宏非空时 a=min finite macro time，U=2aD−1≥q*，且所有 q≤U 都满足 q/D<2a，合法调用源算法；宏空另取任意合法完整调度 C 的 U=DC。初始化 U 成功且存见证，维护 lo<q*、hi 成功。FAIL 只更新 lo，成功只更新 hi，不推断成功阈值可行。终止 hi=lo+1≤q*，输出峰≤3hi/(2D)≤3OPT/2。接受集合无须单调。此含 OPT promise 不能免费删除或验证，也不能解除固定 K、给定分区或唯一 home。

## 严格大备选过滤的用途和零删固定点

对当前域 D_j⊆{i:p_ij≤T} 测边 j→i，F 中任务在 i 可用且所有外部备选严格>T/2。任何真实 T 调度若使用被测边，其移出 i 的 F 任务占据互异外机，构成一份部分匹配；其移出收益≤最大权匹配 W。因此 i 负载≥p_ij+sum_F p_iell−W。仅当该下界>T 才删，安全性保持所有真实 T 调度，逐轮同步删域也如此；它仅是必要性过滤。

严格号承重。取 T=1，j 只在 i 时间一；a,b 在 i 和共同外机 z 都时间一半。真实调度 j→i、a,b→z 的峰一。若把严格号弱化成≥T/2，则 a,b 都进 F；最大部分匹配只移一件，错误下界一加一减一半为三半，会删掉真实使用的边。

对 raw 与 fixed-d 的 U/B/Z 两套矩阵，在各自 T 有 1/k≤T/2<1≤T，M>1。U 行的 F 中 f 可注入不同 B；若含 selector，可送另一 U，与那些 B 不冲突。B 行的 incoming f 因 U 小端不在 F，home e 可注入 k 台 Z。Z 行的 incoming e 因 B 小端不在 F。因此每个查询都能饱和 F，W=sum_F p_iell，下界只剩 p_ij≤T；第一轮零删就是固定点。这是本矩阵与 filter 的具体解析比较；没有已登记的“组合系统间隙”终点，故不将 filter 的安全性定理标成接受后可调度或强系统 gap 的逻辑边。

## 其余核心及复算边界

VW Theorem16 的全局潜在 big 资源数为常数，不能换成某份最优分配实际使用 big 的个数。当前资料只有定理句，缺技术报告的完整算法，因此仍 unassessed，无 accepted 推导。

仿射线 review 保持三个合同：单 primary 的 pairwise 条件化可产生 Hall/unit escape；多 primary 的 all-pair simplex 仍拥塞；R-states 单边际族缺 primary/auxiliary pairwise。它的登记 body 是来源范围章节，不能把后两项混成同一个反例或把第一项推给多 primary。未重开单边际反例原件，不声称本轮独立重证其具体构造。

DGR 第五节完整随机 packing 证明仍保允许裁剪、期望集合数和分割 promise。小集匹配用 a 个元素至多碰分割 a 块，故 a+R≥m；热门概率必须条件于 S 已采样；留下大集的 K=|S\T|>0.9|S|，对非热门元素独立分配，取 e0=delta²/800，最后比例 9delta²/8000。delta≥1 空输出，空集合先全选入。它没有保持完整原集合，也不直接提供全任务调度或两状态不交束。

单 pin 树的 S0 任意实际调度反向提取及全任务回填仍支撑 palette 的实际值贡献。张量目标另需末层两色、tuple 单射、binary 乘积见证、固定 YES/NO 常量与正高度、G_k 递减及纯收缩界。全局颜色重数与局部末层两色不同。原 contribution 保留，未用它覆盖目标独有的组合论证。

`repair_audit.py` 使用 Fraction/整数完成当前修复的有限复算，输出 `repair_audit.json`。它重建六个整行交易的实际非负配置分布及矩匹配（多个 incoming 的零矩另由结构证明），七个完整 NC laws，四份完整门控矩阵的全部端点分配，排序与二次余量，非单调接受表、严格阈值反例、原矩阵星饱和所用参数不等式、DGR 常数及 palette 交乘差。OPT 网格枚举采用已证明的 r²≤k 充要归约，不冒称枚举展开的全部 U/B/Z 分配。未重跑旧审计、未运行通用 LP/SDP，也不把有限通过代替上述证明。
