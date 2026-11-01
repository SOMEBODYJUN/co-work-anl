# 全部 reset coverer 的同客户 NET：独立代数、价格递推与范围

2026-10-24，payment9，按 root 的精确陈述先独立展开，再读旧 NET 原文核对来源。对象为任意人数、一般有限共同目录及每份完整历史纯 SPE。本文是一般合法性和价格消元的独立检查，**不证明共同 ROLE 存在，不给新的福利下界**。Q-CAG-HALF 仍 OPEN。

主要依赖为 [第八轮共同付款 primal](../../round8/residual/linear_joint_payment_certificate.md)、其 GENERAL-DENSITY 与 [旧同客户密度](../../round8/inventory/source_preserving_density_envelope.md)。旧 NET 精确来源为 [round5 credible §6](../../round5/credible/all_fresh_submarkov_elimination.md)：同 context、同客户的等价正负取消。本文的新允许域由 root 提出；payment9 独立检查如下。

## 1. 固定数据、局部线性允许域

沿原 R-only 图，固定自然 context t=(g,i)、输入客户 x in R intersect sigma_i(g)。记

    V=finish_sigma(g),
    A=finish_sigma(B_<i,sigma_i(g)),
    v=c_V(x)>=1,  a=c_A(x)>=1,
    Q={j>i:x in A_j},  |Q|=a-1.

R 不被 actual B 覆盖，所以 A 中没有 past x-coverer。对同一输入 h>=0，允许全部 reset coverer 边满足

    0<=z_j<=h/a  (j in Q),
    L=h-sum_j z_j,
    L<=v h/a.                                    (NET-ALL)

这是固定有理系数的线性域。由边上限自动有 h/a<=L<=h。故也可显式写成

    h/a<=L<=min(h,vh/a).

不使用 h 与选择参数的乘积。h=0 时所有量自动为0。全部 coverer 各发 h/a 给出 L=h/a，所以对每个 h 域非空。

h>0 时设 beta_j=a z_j/h，可将该域写成

    0<=beta_j<=1,
    sum_j beta_j>=d:=max(0,a-v),
    L=h[1-(sum_j beta_j)/a].

这里 d 是整数，0<=d<=a-1；它只是核验和价格计算的事后归一化，不用于 primal 线性约束。

## 2. 全图库存、密度和一次完整 IC 均保留

每条边仍进入真实 prescribed target (A_<j,j)，而每边质量上限仍为 h/a。父节点对该目标的客户密度贡献因而最多为 h；旧 DENSITY 证明只用这个不等式，并不需要 new-coverer 边强制等于 h/a。因此，对非 actual target 仍有同一首次偏离角色的父反链，和同一 source 前缀界

    c_Vt(x)h_tx<=sum_(owner<=first-divergence(t))p_owner,x<=1.

源的逐客户库存、每 origin 的角色反链和质量守恒没有变化。NET-ALL 没有 whole-profit 重采，不将来源 x 变成其它客户。

由额外 current 上限，对同一个 context 先求和，得到

    sum_x L_tx<=sum_x[c_Vt(x)h_tx]/c_At(x)
                 <=sum_(x in sigma_i(g))1/c_At(x)
                 =u_i(A_t)<=u_i.

最后仅使用 actual-prefix 对 sigma_i(g) 的一条完整 IC；没有逐客户加权调用 IC。不同 context / action 的这些上界仍不能相加当成一份实际钱包。

## 3. 与旧 NET 的精确关系

记 nNew=|cover_A(x) minus cover_V(x)|、nLost=|cover_V(x) minus cover_A(x)|。两叶当前都覆盖 x，故 a-v=nNew-nLost。旧 round5 NET 在同客户、同 context 中取消 min(nNew,nLost) 个等价正负项，只保留原 NEW recipients，剩余边的总份数为

    (nNew-nLost)_+=(a-v)_+=d.

若将旧局部代数按同客户密度 f=vh 缩放，每个保留正边的质量为 f/(av)=h/a，current 恰为 min(h,vh/a)。这给 NET-ALL 内一个合法点。旧稿随后以整行利润归一化，可能重新采样客户；那份完整旧流不能因此被称为新的来源保持流。此处只复用了旧等价取消的局部代数，再由已证全图密度重新取得来源保持流。

NET-ALL 还允许把所需总输出 d 份移到 COMMON reset coverers；旧 NET 的保留正边域不含这些 common recipients。因此二者不是同一个允许集合。一个局部计数例是 v=3、a=4：旧叶 coverers 为 {old-past,current,common-future}，reset 为 {current,common-future,new-future-1,new-future-2}。旧 NET 必须保留一份 NEW 输出；NET-ALL 可以只向 common-future 发 h/4，留 L=3h/4。这里只说明局部允许集合严格变大，不声称这个局部模式单独构成完整 SPE 或任何福利反例。

第八轮原 R-FLOW 也包含在 NET-ALL 中：其边均<=h/a，原 current 为 h times common-count/a，而 common-count<=v。域扩大是局部路由自由度，不是新增资金。

## 4. 角色价格的精确递推

固定角色非负价格 lambda_i，令 psi_j 为 x 在真实 child(t,j) 的最小终端单位价格系数。这里的单位系数是同质线性流的成本，不声称可独立注入一单位后仍满足密度。将 q=a-1 个未来价格排序为

    psi_(1)<=...<=psi_(q).

NET-ALL 的局部最小单位成本为

    Psi_t(x)=min_(k=d,...,q)
       [(a-k)lambda_i+sum_(r=1)^k psi_(r)]/a.      (NET-PRICE)

证明：normalized 费用为 lambda_i + sum_j beta_j(psi_j-lambda_i)/a。先取所有负系数的 beta=1；若还未满足 sum beta>=d，再按非负系数从小到大填至 d。由于盒及整数下限 d 的极点为0/1，总有某个整数 k 实现最优。平局可任取分数或端点；所有选择同时受第2节密度证明保护。未来角色严格增加，故反向递推有限且唯一确定最小值。

常数 lambda=1 时，全部 child 单价为1，NET-PRICE 仍恰为1；总价仍等于原客户质量 |O|。该价格递推没有支付 HALF 的常数价格 cut。

## 5. 可变所有权与扩张共同 primal

把 [可变所有权](roleobstruction/fractional_ownership_extension.md) 的 p_ix、OWN、OWN-CAP 及同一点的 r/H/d/J 全部保留，只将原 R-FLOW 的“NEW 固定满、COMMON 可选”替换为 NET-ALL，其余 R 守恒及 ROLE 不变。所有变量仍线性，I 的现金出口仍必须从同一新 a_ix 重算。

该扩张忽略 ROLE 后非空：canonical p 恢复旧 INIT 可行点，I 按剩余 actual 份额付清，R 取全部 reset coverer 满边得到旧 uniform-reset 点。任意可行点都保留源库存、全图密度、完整 IC 及 MASS；若再满足同一 ROLE，则 |O|<=2W，最优 T 时给 HALF。此处未证明每份原 SPE 都存在最优 T 的 ROLE 点。

对固定 lambda，R 可用 NET-PRICE 消元，其余 OWN/INIT/I-PAY 保留。这样最小价格不大于第八轮旧域的最小价格，但没有取得它必<=2 sum_i lambda_i u_i 的新一般不等式。

## 6. 一般有限传播及 m=5 代入

每个真正到达的 R natural context 其旧叶至少有两个 x-coverers：此前 source/reset owner 和当前接收者。所以 v>=2。若取局部最少输出 sum beta=d，则有

    total future output = h(a-v)_+/a
                        <=h(r-2)_+/r,
    r=m-i+1.

每条非零 natural-to-natural 边均有 a>v；child 的旧负载恰为这个 a。因此这种最少输出选择同时严格增加角色与同客户旧负载。若一个 source owner 为 i、其初始 query x-load 为 w>=2，任一路径最多有 floor((m-i-w+1)/2) 条 natural-to-natural 边：每次增加的角色与旧负载至少各1，而能继续输出的节点满足 role+oldload<=m。该路径性质是旧 NET “保留边使客户负载严格上升”与 R 无 actual past 的直接合成，不当作新的付款不等式。

直接取 m=5，每个 natural context 的最少输出比例最多1/2；剩余人数r=3时最多1/3，r<=2时可把全部输入留在 current。每条 source 路径至多一条 natural-to-natural 边。这些是无条件合法核的结构性质；没有将一个 role 的多个 actions 共同放入2u_i。故任意目录/每份完整纯 SPE 的五人 HALF 仍只由 ROLE 可行性条件推出，尚无无条件证明。

## 7. root 完整正文的后读核查，含整行 ROW 家族

完成上面的合同重构后，完整读取 root 的 [all_future_coverer_payment_family.md](../parent/all_future_coverer_payment_family.md) §1--6。ALL-FUTURE、退款展开、旧 NET/新增 common recipient 区别、局部价格示意、sorted-price DP、可变所有权合成及状态表述均通过。本页只作内部数学核查，不是外审或新颖性认证。

§3 的价格示意按单位 h 核对如下：a=4、v=3，当前价格1、common 后继0、两个 NEW 后继各2。旧强制两个 NEW 输出，common 取满后价为 1/4+2/4+2/4=5/4；旧 NET 仍须留一个 NEW，同时 common 取满后价为 1/2+2/4=1；ALL-FUTURE 只给 common 输出1/4，价为3/4。取 h<=1/3 保障 f=3h<=1。只是固定局部数据的价格比较，不是完整 SPE 反例或全树付款。

menu9 的 §6 ROW 扩张也通过。它保留同客户守恒及全部边上限，但用

    sum_x L_tx<=u_i                               (ROW)

替代各客户的 L_tx<=v_tx h_tx/a_tx。该 actual 行上限是整行预算，允许一个客户使用本 context 其它客户未花的退款；current 仍保留自己的来源标签。它不将 per-client IC 重权，也不对客户重采。

非空性及可达到的最大 current 可直接检验。固定输入向量 h，从 uniform 点 z_tjx=h_tx/a_tx 开始，令

    H=sum_x h_tx,
    C0=sum_x h_tx/a_tx<=D_t<=u_i,
    Delta=min(H,u_i)-C0.

有 0<=Delta<=H-C0，而 H-C0 正是现有全部边的总质量。因此总能从这些边取消 Delta，取消的每份仍落回同客户 current，得到总 current min(H,u_i)。这恰使用不超过同一整行退款 u_i-C0；任何单个客户 current 即使超过 v h/a，也没有超过这一共同实际行预算。

若把某处边取消，所有 downstream 输入逐客户只会减少。将旧 downstream 每客户 current 和全部子边按新 h/旧 h 的同一个比例缩放，原每客户守恒、edgecap 及非负性保持；每个下游整行 current 亦逐项不增，故 ROW 保持。再由同一反链证明保留全图密度。可依角色顺序作这些选择，不需假设 downstream 互不合流。

较窄的固定输入上限 beta_*u_i、beta_*=max_x f_tx<=1 也包含 uniform 点，因为

    C0=sum_x f_tx/(v_tx a_tx)
        <=beta_* sum_(x in R intersect a_t)1/a_tx
        <=beta_*D_t<=beta_*u_i.

这里 beta_* 是给定输入的事后量；一般 h 也为变量时，max_x f_tx 本身不应未经处理称作固定线性系数。root 正文只把它当较窄可选上限，没有把它用入主 ROW LP。

整行 ROW 约束耦合不同客户，并且 cap=u_i 是固定实际金额；因此 §4 的独立逐客户单位价格 DP 不能用于这一更大族。保留整个有限 LP、同一点的所有 ROLE 和 I 补余，才是准确接口。常数角色价格仍由 MASS 精确给 |O|，没有新总资金。

这项整行取消思路承接 [round6 SAFE/CLIP §3](../../round6/credible/safe_coupon_netting.md)：从同一 current 行的非负退款中取消传播。旧稿按整行利润归一化，可能重采客户；ROW 扩张是在已证明的 per-client edgecap / 库存下逐客户留回质量，不能把两份实际钱包重复相加，也不认领旧 scalar CLIP 思想的新颖性。

最后实读 OWN 的旧源：任意 R owner 已见 [round3 §2](../../round3/credible/increasing_role_capture_flow.md)，任意 Q_i⊆T_i、rho_x 来源见 [round5 §4 INIT](../../round5/credible/all_fresh_submarkov_elimination.md)。对应引用已补进子研究员 OWN 正文。新增合同限于 round8 full-O 坐标 primal 的 H/r/qhat 同点变量化及其 TAME 证明；不把任意 R 分割再次称作新自由度。
