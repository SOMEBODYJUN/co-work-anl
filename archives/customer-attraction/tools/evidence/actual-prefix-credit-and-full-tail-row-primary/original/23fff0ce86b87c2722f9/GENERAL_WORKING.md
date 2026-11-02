# 完整真实查询：实际覆盖信用已知，多层返还未付

状态：个人接续稿；原 Q-CAG-HALF **OPEN**。本轮没有一般 half 证明、真正目标反例或新增无条件福利界。以下分开记录解析关系、已有来源、内部审查与未证义务；不声称外审或新颖性。

## 1. 对象、目标与精确候选

采用 [CAG-MODEL](../../../current/customer_attraction/model.md)：有限单位客户、任意有限非空共同目录、任意 m>=1、每人依次选一主题、允许重复与空主题、完整有序历史纯 SPE 及任意历史平局。固定任意这种完整策略 sigma，实际叶 z=(S_1,...,S_m)，最终收益 u_i，实际并集 C、W=|C|=sum u_i。对任意合法比较元组 T=(T_1,...,T_q)，记 O=union T_j。以下区分集合 O 与其大小 |O|。

在实际位置 i，固定实际前缀 h=z_<i，强制 T_j 后沿同一 sigma 完成，得到 Z_j=(h,T_j,Y_j)。后继 Y_j 全部可以随 j 改变。记

    R_i(T)=sum_j u_i(Z_j),   d_ij=u_i(Z_j)<=u_i.

已有全位置 ROW 候选是 R_i(T)>=|O|-W。它对末/倒二位置已证，对更早位置仍未证。
本轮也考察较弱的最低收益版本：对每个原实例和每个原完整 SPE，存在最优 m 元组 T 以及 i in argmin_k u_k，使 R_i(T)>=OPT_m-W。
若其成立，则 R_i<=m u_i<=W，立即推出 2W>=OPT_m。这个条件蕴含没有证明最低收益版本；没有找到它的反例。

最低位置仅约束原实际 u_k，不约束各互斥 Z_j 的后继收益。把原最低收益直接施给所有离轨后继是不合法的一步。

## 2. 来源与去重

本节没有认领下列已有接口：

- [已有 ROW 与静态/动态信用分解](../R-105f776c3e6d4a22bb7c380c5df8edc7/new_optimal_queries/dynamic_query_credit.md)；[净差平均/匹配](../R-ffea274483aa4105a317300038fe04ce/direct_global/coverage_credit_debt.md)。
- [真实逐动作尾移植](../R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/hybrid_ic_expansion.md)；[末后继剥离](../R-059140e622784d85a4e3a4dd6554f506/menu_covariance/last_successor_peeling.md)。
- [真实倒二行](../R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md)；[三尾删除返还](../R-e05f01e191354b028004b433016ae1c9/three_remaining_decorrelation_residual.md)。
- [完整续局拼合](../../../current/customer_attraction/credible_continuations.md)已给孩子收益极小值与阈值；在原实际路径外，各首次偏离子树互不相交，因此可同时选其极小值而保留实际叶。该表示不供应福利付款。

研究中重新提出的强冻结最优匹配、Bernoulli/Beta 替槽、调和末位界和复制旧玩家半收益都已去重或被旧完整证书否定。见 [强冻结匹配反例](../R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)、[替槽来源](../R-cd789330fc7141299ac491bbb3ffa420/round3/GENERAL_PROOF_WORKING.md)、[末位负载信用](../R-c93f7ed9e4794dc29b320fe10e5bfe40/terminal_geometry/terminal_load_rank.md)、[COPY2 反例](../R-d3981c0168644971803a9c3380ed687c/round3_general/exchange/copy2_counterexample.md)。这些不是本轮新成果。

## 3. 实际前缀的完整覆盖信用

设实际前缀长度 p=i-1=m-r，r 包括当前玩家。逐客户 b_x 为旧负载，a_x 为实际最后 r 人负载，P={x:b_x>0}。令

    F=|C\P|,
    V=sum_(k=i)^m u_k=sum_x a_x/(b_x+a_x),
    Omega=sum_(x in O) 1/(b_x+1),
    A=W-|O|+Omega.

V 的零 a_x 项按零计；它包含当前 i，不是仅严格后继利润。逐客户消去比较并集在旧覆盖外的项，得到精确式

    A=F+sum_(x in P intersect O)1/(b_x+1)+|P\O|.          (AC-EXACT)

因此对所有原输入、所有实际位置、任意比较元组均有

    A>=beta V+(1-beta)F,
    beta=m/[r(m-r+1)]=(p+r)/[r(p+1)].                    (AC)

证明：新覆盖客户对 A,V,F 各贡献一。旧客户 a=0 只给非负信用；若 b,a>=1，则

    [1/(b+1)]/[a/(b+a)]
      =(b+a)/[a(b+1)]
      >=(b+r)/[r(b+1)]
      >=(p+r)/[r(p+1)]=beta.

其中 1<=b<=p、a<=r；旧覆盖且在 O 外的 A 系数为一，更大。p=0 时 A=V=F 直接处理。0<beta<=1 来自 r(p+1)-m=p(r-1)>=0。

当 m>r，beta 是仅按此式对 V 与 F 收费的最佳普遍系数，甚至限制为完整 SPE：取一个客户、目录仅含覆盖它的主题、m 人全选该题。所有历史均无可选偏离，故完整 SPE；任意非空比较重复该题，有 F=0、A=1/(p+1)、V=r/m，达到 beta。此达到例只说明本静态信用界准确，不是对任意加强机制的障碍。

还可保留真实符号，而非只用 beta：

    A-V=sum_(x in P intersect O) b_x(1-a_x)/[(b_x+1)(b_x+a_x)]
        +sum_(x in P\O) b_x/(b_x+a_x).                  (AC-SIGNED)

这里 b_x>0 保证分母正。负项恰来自旧最优客户被实际后缀至少两次覆盖；其绝对值等于把这 a_x 个后缀覆盖代数压成一个时旧玩家获得的返还 b/(b+1)-b/(b+a)。这仍不是一个删人后 SPE。

本节是任意位置的静态信用组件，是已知倒二信用的全尾版本；没有使用额外目录结构。查询分支先给出 (AC)，父方独立重构 (AC-EXACT)/(AC-SIGNED)，另一个研究员未读查询稿而重构 (AC) 及达到例，见 [盲内部审查](actual_credit_blind_review.md)。不将此小组件的正确性等同于主线付款已完成。

## 4. 接入全部真实后继 IC 后，准确还缺什么

设 d_x=# {j:x in T_j}，k_j(x) 为真实尾 Y_j 的负载。令

    Lambda_j=sum_(x in O) k_j(x)/[(b_x+1)(b_x+1+k_j(x))],
    C_j=sum_(x in O) (d_x-1)/(b_x+1+k_j(x))>=0.

独立均匀抽比较索引 j,l。把 Y_l 逐动作强制移入 T_j 分支，每次强制后均沿原 sigma 完成。记 P^k 为移入前 k 个后继动作后的真实完成，P^0=(T_j,Y_j)、P^(r-1)=(T_j,Y_l)。在第 k 次强制处，

    gamma_jlk=u_(i+k)(h,P^(k-1))-u_(i+k)(h,P^k)>=0,
    E_jlk=Phi_b(P^k without k)-Phi_b(P^(k-1) without k),
    G=E_(j,l) sum_k gamma_jlk>=0,
    D=E_(j,l) sum_k E_jlk.

Phi_b(Q)=sum_x sum_(ell=1)^(c_x(Q))1/(b_x+ell)。without k 只在势计算中删除移入者，真实策略历史没有删人。末个 E_jlk=0；其他 E 无已知符号。

已有逐动作移植恒等式给 Phi_b(T_j,Y_l)-Phi_b(T_j,Y_j)=-sum gamma+sum E。尾主题的边际分布相同，所以尾势平均相消。又对每个固定 Y_l 有

    sum_j U_b(T_j;Y_l)=Omega-Lambda_l+C_l.

合并得到全输入精确诊断：

    R_i(T)-(|O|-W)=A-E Lambda+E C+q(G-D).                 (ROW-ID)

所以 ROW 在本表示中**等价**于

    qD+E Lambda<=A+E C+qG.                              (RETURN?)

这不是新充分付款的证明。把 (AC) 代入给一个更强的、足以用于 ROW 的待证预算；但 (AC) 并不控制 D 或 Lambda。只证明 D<=G 过强，且已有 34 客户完整 SPE 的负去相关反例。丢掉比较重叠 C、实际最优外信用或旧玩家返还也均不合法。

当 r=2，D=0，实际末位最佳回复与已知倒二信用已可支付 Lambda；这里不重复认领该证明。早期 r>2 的共同收费才是尚未解决的对象。最低实际收益条件并未提供对同一 A 的跨 q 个查询分支重复使用权。

## 5. 实际核验及五人压力测试

运行 `python3 research/workspaces/customer-attraction/R-f0d8eee94f204bcc9f4415e6afb383b8/audit_row_credit.py`。
[脚本](audit_row_credit.py)使用标准库 Fraction，从单位客户重新构建已知 34 客户完整策略，不导入发现代码。另含空客户/空主题、单客户重复主题、已有 all-big 全人数公式在多组参数的实现回归。

[实际输出](audit_row_credit.json)核对逐客户 (AC-EXACT)/(AC)/(AC-SIGNED)、达到例、每个具名策略的全部有序历史 IC、每条移植 gamma 非负与 ROW-ID；输出保留非零 D，避免只审零余量实例。有限参数与策略只核实现；解析关系的全输入性来自上文代数，RETURN? 的全输入性没有获得证明。浮点锥中未分离出违反 ROW 的点不增加其真值。

同一一般公式代 m=5，按实际位置 beta=(1,5/8,5/9,5/8,1)。这给可用信用下界，**不能**无条件推出 OPT_5<=2W，因为 RETURN? 仍未支付。没有五人专用加行、拟合系数或结构类项目。

## 6. 交接与停止范围

当前真实新增认识仅是把可用静态信用及其旧客户返还解释接到完整尾 ROW 余量的准确位置；没有新的全树支付机制。候选、解析恒等式、内部审查、外审与新颖性彼此独立。共享主目标与最好已知范围均不变，所以没有修改共享 canonical 地图。

下一步若继续此线，须用新的真实后继联合 IC 控制 (RETURN?)，至少在某个最低收益位置或允许跨位置统一支付；不能只重写此等价式、把旧 scalar 菜单当 SPE、扩固定锥阴性、冻结后继或递归调用代数删人后的策略。其它一般方法仍开放。

安全值分支的另一未闭合对象是原总人数门槛：对固定原实例，所有合法有序前缀与完整续局的当前收益最小值是否 >=v_(m+1)(0)。局部背景 v_(r+1)(b) 已有反例；不能替换量词。此分支没有找到新支付关系，未另外制造资产。独立组件根补偿也回到既有 FREE-ROOT/保险成本接口，没有新重叠坏构造。
