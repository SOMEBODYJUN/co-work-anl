# 初始客户边细化的共同容量回撤与精确分散返还

2026-10-24，common_capacity 分支。适用于 Q-CAG-HALF 的全部原输入：任意有限单位客户、共同非空有限目录、任意人数及任意完整有序历史纯 SPE，保留空主题、重复主题及任意历史依赖平局。**一般目标仍 OPEN。** 本文是固定合法流上的线性修复工具；不新增全树 SPE 资金不等式，不证明任一原实例必可修复，也不认领外审或新颖性。

## 1. 固定来源与同一共同钱包

固定原 SPE、实际叶 B、实际利润 u，以及比较元组 T。令 O=union(T)、C=union(B)、I=O∩C、R=O\C。先取 [joint certificate](../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md) 中 INIT、I-PAY、R-FLOW 的任意一点，不要求 ROLE。其 d、H、J 固定，记

    A_l=d_l+H_l+J_l <= 2u_l.

R 流使用同一份已经固定的 mandatory/common 边金额。本文不修改完成叶、客户分母、旧 σ 或平局；改变的是证明中分配的质量。

每条非零初始 R 边定义一个 atom

    a=(i,x,j),  b_a=a_ijx>0,  owner(a)=i,

其中 x∈R，初始边进入原实际前缀 query W_i 中角色 j>i 的真实 prescribed context。若原实现有同一三元组的多个 source 标签，保留原标签或先合并完全相同的入口即可。允许列出 b_a=0 的 atom；后文对其令 y_a=0、t_al=0。每个 atom 的客户 x 与 owner i 始终保留。

将原 R 流按 atom 分裂：在任一节点 (t,x) 将每条输出边和 current 按进入该节点的各 atom 质量比例拆分；总输入为零时全零。原 mandatory 输出等于 h/c_A，故各 atom 的 mandatory 输出仍恰等于自身输入除以 c_A；原 common 输出在 [0,h/c_A]，各 atom 的 common 输出亦在其自身区间。依角色顺序递推即得所有 atom 的非负流。不同有序 history 只在原图真正同一节点时合并，未按主题计数合并。

令 K_al 为 atom a 终结于实际角色 l 的 current 总量。严格 future DAG 和每节点质量守恒给

    K_al=0 (l<=owner(a)),    sum_l K_al=b_a.

这些 K 来自同一合法 R 流，而非任意独立指定的分支支付。**所有初始 R 边均参加 atom 列表，所有 R 终端 current 均被上述分裂全额追踪**；因此在每个角色 l，原 R 终端总额必须恰为 sum_a K_al，不能只检查两边总和相同。置 t_al=K_al/b_a（b_a>0），否则为0。因此非零 atom 的 t 行是严格未来角色上的概率分布。初始未修复共同 cost 为

    F_l=A_l+sum_a K_al,    cap_l=2u_l,

而 joint certificate 的同一质量恒等式给 sum_l F_l=|O|。

如果另一个实现只追踪部分 R 流，必须把未追踪固定 current f_l>=0 明确加进 A_l，令 F_l=A_l+f_l+sum_aK_al，并把后文 source-price 右边改为 sum_l λ_l(2u_l−A_l−f_l)。仅有总额守恒不能删除 λ·f。本文使用全额逐角色追踪的合同，故 f=0。

## 2. Atom 独立回撤的一般精确关系

选任意 0<=y_a<=b_a。将 atom a 的初始边及其**全部**后代 edge/current 同乘 1−y_a/b_a，并在其初始坐标 (owner(a),x(a)) 的 current 增加 y_a。零 atom 不变。于是

    F'_l=F_l+sum_(a:owner(a)=l)y_a−sum_a t_al y_a.       (ATOM-RETRACT)

证明如下。每个 atom 子系统是同质线性守恒系统，统一缩放保持 mandatory 等式及 common 区间。合并 atom 后仍保持这些条件。每条初始边只减小，因此原加强边容量仍成立。在每个初始坐标，边减少多少就增加多少 current，故 p_ix=P_ix^B+c_ix+sum_j a_ijx 仍逐坐标精确成立。R 仍只在原 R 客户上流动。角色 l 收到其 owner-l 回撤总量，同时失去每个 atom 的 y_a/b_a 比例原终端金额，即得公式。最后 sum_l t_al=1 保证 sum F'=sum F=|O|。

合并后的各节点客户输入不超过原输入，因此原全图客户密度界仍成立；这里没有把不同 context 的密度相加。I、H、J 全不变化，也没有从其钱包再取一笔钱。

**与原 INIT 的准确差别。** 新 d'_i=d_i+sum_(owner(a)=i)y_a 可能超过 u_i。输出属于扩展的证明证书类，不声称仍满足原 INIT 的 d<=u。旧 d<=u 是构造初始可行点的充分条件；最终的守恒付款只要求所有 F'_l<=2u_l。回撤新增 current 不是再次使用 IC，也不是客户 x 的 actual 同客户券。它直接占同一 actual owner 的剩余共同容量。若所有共同 cap 成立，则 |O|=sum F'<=2W，T 最优时即该给定实例的 HALF。

## 3. 精确 cut 与源价格形式

记 s_l=cap_l−F_l。固定这份 atom 拆分和这份原路由后，存在成功回撤，当且仅当对每个 λ∈R_+^m（可含零坐标）满足

    sum_l λ_l s_l
      +sum_a b_a(q_a−λ_owner(a))_+ >= 0,
    q_a=sum_l t_al λ_l.                              (ATOM-CUT)

等价地，令 r_l=2u_l−A_l>=0，要求

    sum_a b_a min(λ_owner(a),q_a)
       <=sum_l λ_l r_l.                              (ATOM-SOURCE-PRICE)

必要性：共同 cap 恰写成

    sum_(owner(a)=l)y_a−sum_a t_al y_a <=s_l.

乘 λ>=0、求和，并在盒 0<=y_a<=b_a 上最小化左边，所得最小值为 −sum_a b_a(q_a−λ_owner(a))_+。这给 ATOM-CUT。

充分性：盒是非空紧凸集，其共同 cost 像是紧凸集。若其与向下闭盒 {z:z<=cap} 不交，有限维凸分离给某个非负法向量 λ，且 min_y sum_l λ_l F'_l>sum_l λ_l cap_l。按上式显式最小化各 y_a 即违反 ATOM-CUT。非负法向量来自向下闭盒的无界负方向，不能删去 λ 的非负要求。有限有理输入时可用普通有理 LP 得到可核验的成功 y 或严格失败 price；本文不声称旧 owner-greedy 仍适用于独立 atom。

将 F=A+sum K 代入，使用 sum_l λ_l K_al=b_aq_a 和恒等式 q−(q−λ)_+=min(q,λ)，得到 SOURCE-PRICE。零 atom 对所有式子贡献零，无除零。

## 4. 相对 owner 比例回撤的精确改进

把同 owner 的 atom 合并，定义

    b_i=sum_(owner(a)=i)b_a,
    bar q_i=(sum_(owner(a)=i)b_a q_a)/b_i (b_i>0).

旧 owner 比例回撤相当于限制 y_a/b_a 对同 owner 全相等。因此其可行集合包含于本文 atom 回撤可行集合；两者同用每个 actual 角色的一个 cap，并非给每条边一个新钱包。

对任意固定 λ>=0，置

    D_i=sum_(owner(a)=i)b_a(λ_i−q_a)_+,
    E_i=sum_(owner(a)=i)b_a(q_a−λ_i)_+.

则逐 owner 有精确恒等式

    b_i min(λ_i,bar q_i)
       −sum_(owner(a)=i)b_a min(λ_i,q_a)
       =min(D_i,E_i)>=0.                            (DISPERSION-REBATE)

若 b_i=0，整行各量定义为0。证明：b_i(bar q_i−λ_i)=E_i−D_i；左边亦为 E_i−(E_i−D_i)_+=min(E_i,D_i)。因此 atom-price 的总需求恰等于旧 owner-price 总需求减去 sum_i min(D_i,E_i)。这是一份共同来源在下游价格两侧分散时的**精确 Jensen 差**，没有把多条 branch 的局部 IC refund 直接相加。

该差在同 owner 的所有下游 q_a 位于 λ_i 同一侧时为0；同一 owner 的 q_a 同时严格跨过 λ_i 且两侧有正质量时严格为正。完全相同终端分布的 atom 合并不会损失任意 cut 的能力。旧 owner-greedy 失败 price 可直接代入本式检测其失败是否被分散返还抵消；一个 price 不再失败并不证明全部 atom cuts 都成立。

## 5. 严格包含的代数检验，准确限定范围

下列只是一组合法三角 source/cap 数据，用于核验两种线性 repair 类严格不同；**未声称来自原 SPE、INIT 或原目录，不能当作任何博弈反例。**

三个角色 u=(1,1,1)，cap=(2,2,2)，A=(3/2,2,1)。owner 1 有两条 atom，均质量1/2，一条全部终结于角色2，另一条全部终结于角色3。故 F=(3/2,5/2,3/2)，总质量11/2<=6。

旧比例回撤 y∈[0,1] 给 cost=(3/2+y,5/2−y/2,3/2−y/2)。第一 cap 要求 y<=1/2，第二要求 y>=1，故失败。atom 回撤只取终结角色2的那条 y_a=1/2，另一条0，得 F'=(2,2,3/2)，成功。

取 λ=(1/2,1,0)。旧 source-price 左边为1/2，右边为1/4，严格失败1/4。两 atom 的下游 price 为1与0；D_1=E_1=1/4。细 atom 左边为1/4，恰由该同一共同 source 的精确返还消除原违反。该例检验一般线性关系及严格包含，不检验原 HALF 的真假。

## 6. 真实义务、m=5 与价值边界

本工具补的是：固定原流如果 owner 比例回撤失败，能否因同 owner 的不同真实初始客户边有不同终端价格而修复。其新增关系为 ATOM-RETRACT、ATOM-CUT 及 DISPERSION-REBATE；它们只用原 admissible flow 的分裂与同一共同 cap，不调用新的 off-history SPE 行。只有输入流由原规范证书产生时，才继承其真实 context、库存及密度合法性。

它没有证明任何原 SPE 的 ATOM-SOURCE-PRICE 必然成立，也没证明可以重选 T、INIT 或路由使其成立。λ恒为1时，每个非零 atom 有 q_a=1，全部 D_i=E_i=0。SOURCE-PRICE 退回

    sum_a b_a<=sum_l(2u_l−A_l),

与原质量恒等式合起来恰为 |O|<=2W。因此本细化无法凭自身补上总资金缺口；价值限于允许更有选择的已有来源回撤、精确诊断旧失败 cut。

同一机制代入 m=5，仍需对任意 λ∈R_+^5 证明上面的 SOURCE-PRICE；尤其 λ=(1,1,1,1,1) 仍是未付的总 half。**没有无条件推出 OPT_5<=2W。** 不做五人专用参数或额外结构假设。

全零客户时无正 atom、u=A=F=0；所有式子为0。空主题无正客户源；重复动作及全部有序历史平局均未修改。原共同证书 d、H、J、K 固定同一次初始化/流，不能混合不同 T 或不同路由的有利项。

## 7. 已做的定义级核验

[独立脚本](audit_atom_retraction.py)不导入原初始化/flow实现，重建既有52单位客户完整SPE，检查1554条含自身的全历史IC、比较元组最优性、max-future初始化及I cashout；再将两条正R初始客户边各自拆成atom，核对每个角色的全额追踪、任意不同比例的全部后代缩放、ATOM-RETRACT及总质量精确守恒，并检验81组含零坐标的有理非负价格下的DISPERSION-REBATE。另在§5的抽象数据上核验严格分离。输出见[冻结结果](atom_retraction_audit.json)。

该真实例的两个atom均只终结末位，且owner不同，因此它只检查实现合同，不提供真实SPE上的细化严格优势。没有声称一般回撤成功、没有新增博弈反例，也没有用这些有限检查证明本文的一般解析结论。
