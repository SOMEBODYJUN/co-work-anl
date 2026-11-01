---
id: customer-attraction/complete-spe-sparse-slots-author-proof-and-two-finite-reports
kind: resource
type_tag: 资源
title: 完整SPE稀疏槽作者证明与两份原始有限域
status: integrated-author-proof-and-finite-frozen-reports
truth_status: proved-unbounded-sparse-reset-bridge; finite-program-claims-separated
source_refs:
  - clean:a736ca58ff82a1a2192b
  - clean:1fcf4d32e4c24b455d9f
  - clean:a8f608020c5f7b69f334
related_objects:
  - archives/customer-attraction/state/反例/R-171完整SPE稀疏槽租金障碍--反例.md
  - archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md
---

本资源完整处置原作者5464B证明及两份原始冻结JSON，不把Boss3已done的两个生产者再次认领或完成。原证明SHA `4594a404e513e2e27881ca8f190deec227e107788f8b842e24b34ca8bc3110f1`，chronological报告535B/SHA `19e80bc2890ad906ac50467a966d552b753248394d77bfcbe67209c74e067683`，complete-SPE报告500B/SHA `754eb43745fc8eed9d55dd8795823554a2b336107150ebc9d0d7f9bd26d9ab62`。全部原件、完整比较生产者和独审在 [证据](../../tools/evidence/root-sparse-slot-primary/README.md)。两稀疏报告保留为**原有限声明**：当前本地未找到两个同SHA原生产者的成功stdout/event，不把“源码已读”当作实际运行，更不补造exit0。本批原入口新运行0。

## 完整模型、量词与策略族

两个单位客户x,y，共同目录恰A={x},B={y}，整数q≥2、单位提供者数m=2q。每人观察全部有序历史各选一主题，终局客户均分。固定任意完整纯函数χ(h)∈{A,B}。在任意非终端历史h令a=#A(h),b=#B(h)，a+b<2q；定义同一纯策略：

1. a≥q时规定B。
2. b≥q时规定A。
3. a<q且b<q时规定χ(h)。

前两项不能同时触发，否则历史已至少2q长。χ可以依赖整个有序历史；“任意”意为每节点预先固定一个确定行动，不是随机策略或有利平局存在性。

**全部有序历史的SPE证明。** 若a,b<q，选任一当前行动都不能令该类跨过q。一类一旦达到q便永不再选，剩余动作恰将另一类填到q。因此两条当前分支无论后继χ怎样，终局都(q,q)，当前两行动收益均1/q，任何χ最优。

若a≥q，含a>q的严格超载离轨前缀，同策略规定当前及全部后继选B，终局(a,2q−a)，当前遵从收益 **1/(2q−a)**。若当前改选A，则A计数a+1、以后仍全B，偏离收益1/(a+1)。因为a≤2q−1及a≥q，有0<2q−a≤q<a+1，所以遵从严格优。b≥q完全对称。这个比较穷尽全部有序历史和两个行动，并真实调用同一策略的偏离后续局；不能将所有离轨终局写成(q,q)，也不能将遵从收益一律写成1/q。

q=1同规则亦为完整SPE，但没有下面q−1行租金。选择χ(empty)=A、其余未满历史χ=B得到实际路径

$$S=A,B^q,A^{q-1}.$$

根终局(q,q)，每人1/q，根W=OPT_(2q)=2。它没有福利损失，故不是half反例。无界性在q→∞、m随之增长时成立，不声称固定六人也有无界租金；q=3给六人实例且仍福利最优。

## 单个未来实际槽位也产生调和发散

任意固定代数reserveρ>0。对j=1,…,q−1取实际未来单槽I_j={q+1+j}及客户无关全行权θ_j=1/j。这些槽正是末尾q−1个A，各仅用一次，且D_t=Σ_{j:t∈I_j}jθ_j∈{0,1}，Γ=1。

记b_j(z)为实际前缀j中客户z的hit数，q_j(z)为选中I_j的hit数。重置租金为

$$E_j^{reset}=\sum_z b_j(z)\left[\frac1{\rho+b_j(z)}-\frac1{\rho+b_j(z)+q_j(z)}\right].$$

在该实际路径，x始终b_j=1、q_j=1；y的q_j=0，所以每行精确为1/[(ρ+1)(ρ+2)]。于是

$$\sum_j\theta_j E_j^{reset}=\frac{H_{q-1}}{(\rho+1)(\rho+2)},\qquad W=2,\ \Gamma=1.$$

固定任意ρ，H发散，因此不存在只依ρ且与人数无关的有限K(ρ)，能对全部此类完整SPE普遍给ΣθE≤K(ρ)ΓW。ρ=1时比值为H_(q−1)/12。取q=2^k，每个二进区间的倒数和≥1/2，H_(q−1)≥k/2，取k>24K即超过KW。每个q都是有限游戏，不需显式列出指数个策略节点来定义该纯函数。

反例去掉了旧“任意路径可能非SPE”的限定，但只否定把相同reset费、1/j归一化和槽拥塞从连续窗口无条件移到任意稀疏未来槽的辅助非负预算。它没有否定实际连续窗口支付、带符号抵销或任何尚未构造的真实全树运输。

## clock与skip-premium：原535B报告所核的完整代数

为了理解其有限字段，保留相邻一般路径稿的自足推导，数学身份仍属已入引理。对任意主题路径S₁,…,S_m（不要求SPE，允许空主题/重复/零客户），任意稀疏I_j⊆{j+1,…,m}、θ_j≥0与ρ>0，使用**真实累计hit**定义

$$E_j^{clock}=\sum_{t\in I_j}\sum_{x\in S_t}\frac{b_j(x)}{(\rho+b_{t-1}(x))(\rho+b_t(x))},\quad\Gamma=\max_t\sum_{j:t\in I_j}j\theta_j.$$

固定客户的真实hit为t₁<…<t_c。交换有限和后，第k次hit系数的内层为Σ_{j:t_k∈I_j}θ_j b_j(x)。k=1该和为0，k≥2由b_j≤j至多Γ。因此望远镜给

$$\sum_j\theta_j E_j^{clock}\le\Gamma\sum_{x:c_x>0}\left[\frac1{\rho+1}-\frac1{\rho+c_x}\right]\le\frac{\Gamma W}{\rho+1}.$$

这里不需要槽连续。对某行j和客户，第k个选中hit的虚拟排名a=b_j+k，真实排名b=b_(t_(j,k))≥a。reset与clock的该hit差为

$$p_{j,k,x}=\frac{b_j(x)(b-a)(2\rho+a+b-1)}{(\rho+a-1)(\rho+a)(\rho+b-1)(\rho+b)}\ge0.$$

分子恒等式来自(ρ+b−1)(ρ+b)−(ρ+a−1)(ρ+a)=(b−a)(2ρ+a+b−1)。故E_j^reset=E_j^clock+P_j，P_j=Σp≥0，不能删掉P。对于b_j(x)>0，零差恰为b=a；P_j=0当且仅当每个已有客户的每个选中hit之前均未跳过该客户真实hit。连续窗口充分，但客户hit级连续比所有槽几何连续更宽。ρ只代数reserve，未假设有合法公共主题或新增提供者，也不对reserve调用SPE。

在本SPE族ρ=1，虚拟a=2、真实b=j+1，逐行reset=1/6、clock=1/[(j+1)(j+2)]。因此

$$\sum_jE_j^{clock}/j=\sum_{j=1}^{q-1}\frac1{j(j+1)(j+2)}=\frac14-\frac1{2q(q+1)},$$
$$\sum_jP_j/j=\frac{H_{q-1}}6-\frac14+\frac1{2q(q+1)}\longrightarrow\infty.$$

真正clock共同支付不失败；全部发散恰在跳过的hit被反复记为局部第二hit所产生的premium。一般全树若只得到reset，须另付premium；若得到clock，则还须证明来自同一SPE真实激励行的运输及可控Γ。两义务均未完成。

## 500B complete-SPE冻结报告：完整有限域与计数

比较生产者 `251ddedf0a4a923e6fc4`，3440B，SHA `4e50d31d0e2bd298a7708cc0dcce00edb73a2c17e488079874466cd4f457498c`。标准库Fraction、lru_cache、product与json，无研究模块导入；main是字面域，无CLI/外部输入。

`policy`先执行满q分支；未满时variant0为空历史选A、之后选B；variants1、2、3按完整有序历史的加权sum((i+1)(v+1))对modulus=variant+2取余决定行动，确实顺序敏感而非计数Markov。`terminal`缓存并按同一policy真实完成。对q=1,…,6每种variant的**每个有序前缀**比较两个合法行动，含自身比较，确认未满终局(q,q)和满类后继全选另一主题。

报告43632项是

$$4\cdot2\sum_{q=1}^{6}(2^{2q}-1)=43632,$$

不是43632个不同游戏或非自身偏离。root_welfare=2，catalog=[[x],[y]]，unit_customers=2。预算部分q=1,…,79，对ρ∈{1/3,1,5/2,7}共79·4=316；从实际路径逐客户算background/inserted、Γ及加权租金，核任意给定q的有理恒等式。报告 `slot_congestion=1`描述q≥2非空族；q=1没有行，源码另断言Γ=0。一般任意χ、任意q和发散来自上述证明，有限4变体不代替它。

## 535B chronological冻结报告：全二元路径与所有稀疏子集

比较生产者 `2a3ae62cdcb1da780b81`，3953B，SHA `fc059b95363385506568e7bfd1f2164c43d2f6bfe1d482b1f74181bd5611adbb`。每个客户用0/1 membership路径表示，`row`直接算prefix、selected hits、reset、clock和精确premium，断言非负与相等；`audit_family`用同一ρ和全行θ构造每槽Σjθ，核clock总预算。

main穷举m=1,…,8每条2^m路径、每个j=1,…,m−1和{j+1,…,m}的全部稀疏子集，对ρ={1/3,1,5/2}三值；总row cases为

$$3\sum_{m=1}^{8}2^m\sum_{j=1}^{m-1}2^{m-j}=259080.$$

它另每条路径构造3个非均匀、不连续族：I_j由(t+(f+1)j) mod(f+2)=0选择，θ_j=((j mod3)+1)/(j(f+1))，f=0,1,2；再三reserve，9Σ_{m=1}^8 2^m=4590个family预算检查。这里259080覆盖所有单行稀疏子集，4590仅三种指定共同族，不是所有I_j/θ组合的穷举。最后q=2,…,99共98个实际SPE形状membership路径，仅ρ1，核上述reset/clock/premium闭式；这部分并不调用policy或重算完整SPE激励。

两报告的 `scope` 均写finite，`general_target`均OPEN；特别chronological写“no real full-tree transport established”，complete-SPE写“OPT=W=2”。它们没有producer源码hash、环境、exit code或实际命令字段。当前缓存的两生产者和有限声明吻合，但找不到成功stdout/event，所以本包如实记“原有限冻结声明+完整源码/证明核对”，不称已复跑或同SHA成功运行。新独立小数据检查只核计数公式、两额外槽stdout绑定、q2/3/10租金及超载离轨见证，不冒充上述259080/43632原循环。

## 作者版本、独审与已有正文的关系

原作者稿2026-10-22首部记另一研究员独立重构全部历史/无界性通过，尾部“尚无独立外部审查”与内部独审不冲突。比较原 `c814… sparse_spe_rent_review.md` 开始确为声明先行重构、未读作者实现；其后§5另读chronological正文而仍未读实现，独立复核clock及premium。该独审自实现的q2…5全部历史、q2…12任意选择终局全集、q2…30租金是**另一程序/报告**，不能并入本500B生产者的q1…6/四变体/316次计数。本次清洗已读全部证明和实现，不再自称盲审。

已有《R-171完整SPE稀疏槽租金障碍》已吸收一般族，但旧页在严格超载离轨分支把终局和收益概括过强，并误写2W≥OPT取等。本包保存该页精确快照、SHA、三处未应用最小patch：只有未满历史保证(q,q)；超载遵从1/(2q−a)；本族W=OPT=2而half不等式严格。共享页未写，生产者已done不复领。其余既有clock引理/独审有限页保持原身份；本资源补齐当前主作者稿的完整证明与两份primary有限报告独有范围，不授新一般定理或主目标结论。
