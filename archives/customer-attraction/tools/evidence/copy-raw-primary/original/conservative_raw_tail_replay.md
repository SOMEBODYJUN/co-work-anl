# 同一源行的保守 raw-tail replay：正确终端边际与 signed floor 付款

2026-10-25，geometry12，回应 parent 的 canonical-floor 域。
原任意人数、共同目录、完整历史 HALF 仍 OPEN。
本页构造一个真正的单位保守耦合，并证明共同 shadow 部分只用同一源银行。
**对角 covariance 的金额仍未闭合。** 没有改根角色或借不同历史的正部银行。

**域版本注意。** 第3节分别 E_Qd_i<=u_i、E_QF_i<=0 用于较早的 mean-FLOOR 域。
最新单一 uniform NET-cap 不蕴含两者，必须改用第7节组合潜力，不混用旧分银行。

## 1. 源、终点及必须释放的 tag

固定实际位置 i 与其实际前缀 h_i，未来人数 n=m-i。
源分布 P_i 是 A~p 后的原真实 source 叶

    Z=(h_i,A,B1,...,Bn).

目标 Q_i 为 selected canonical-mean-floor 最优 raw-tail 分布，记录写成

    Y=(h_i,T,C1,...,Cn).

独立抽取 Z~P_i、Y~Q_i。源和目标的根角色始终是同一个 i。
目标 tag T 的边际不假定等于 p，不能把它换成 A 后仍宣称终点是 Q_i。
因此使用 parent 所说**所有实际 tag 均释放**的 raw 域；若仍固定实际 tag，
以下某些中间记录可能被排除，不能使用本构造。

## 2. 逐坐标 replay 的确切流

保持源查询 A，依次用目标未来动作替换源未来动作：

    X_k=(h_i,A,C1,...,Ck,B_(k+1),...,Bn), k=0,...,n.

最后才换 tag：X_(n+1)=Y。每条 (Z,Y) 路径的质量是 P_i(Z)Q_i(Y)。
按层聚合相同记录得到有限 DAG 流：内部每个状态入流等于出流，每层总质量一，
起点边际准确 P_i，终点边际准确 Q_i。没有自行重选一个更方便的 terminal marginal。
所有 X_k 都是同一实际前缀后的合法单位玩家 raw 记录；不要求它们本身 SPE。

删除 i 槽后的负载 ell_i(X_k) 不依赖其 tag，故最后 tag 边没有 shadow 变化。
其余全部对角 shadow 工作发生在原查询 A 仍是记录根 tag 时。

## 3. 固定 floor 函数的 signed telescope

令 canonical dual 为

    r_i(z)=eta_i+mu_i d_i(z)+F_i(z)-w·ell_i(z)>=0,
    F_i(z)=sum_h lambda_ih 1_(z extends h)[M(h)-u_k(z)],
    mu_i,lambda_ih>=0.

这里只对同一个 i 使用同一个 F_i、mu_i、r_i；没有重索引到别的根行。
在上述保守流上，逐边保留符号，准确有

    sum_edges flow(e)[F_i(e+)-F_i(e-)]
       =E_Q F_i-E_P F_i <= -E_P F_i.                  (F-TELESCOPE)

原源为真正 child SPE，所以 F_i(Z)<=0；目标满足各 mean floor，所以 E_Q F_i<=0。
不能将左侧换成各边正部，也不按不同历史单独复制右侧银行。
同样根 cap 与 reduced cost 给

    mu_i(E_Qd_i-E_Pd_i)<=mu_i I_i,
    E_Pr_i-E_Qr_i<=E_Pr_i,
    I_i=u_i-E_Pd_i>=0.

故真正全输入的共同 shadow 工作上界为

    w·(E_Q ell_i-E_P ell_i)
       <=mu_i I_i-E_PF_i+E_Pr_i.                    (COMMON-WORK)

在目标为该行 shadow LP 最优、与 dual 互补时，均值 cap/floor 与 reduced-cost
松弛精确取消，COMMON-WORK 为相应源 KKT 银行的等式。这只使用已知 G 的同一份，
不产生第二份额外资金。

## 4. 一个可加入的零统计代价 posterior retag

每次替换一个未来动作后，设剩余旧 source 后缀为 B_(k+1:n)，目标 Y 全部已抽定。
可再从原条件分布 law(A|B_(k+1:n)) 独立重抽根 tag A_k。
条件于新 tail，旧根 tag 的分布正是这个 posterior，所以刷新前后
(tag,raw tail) 的**完整联合分布相同**。
因此每个 floor 统计、d_i、r_i 和任何 raw-terminal 函数的期望都不变。
这是真正单位记录间的分布保持流，不是把根玩家改成分数质量。

重复到尾部全部为 Y 时，根 tag 为 p 抽样并独立于 Y 的 tail；仍须保留最后
换成目标 T 的 tag 边，终点才是 Q_i。不能删掉这条边并偷换终端边际。
此 posterior 刷新提供合法 mean 统计耦合，但本身不减少对角工作总额。
这是第2节的一个可选变体。若使用它，不能仍宣称后续记录 tag 一直等于最初源 A；
也不能把对角 work 的固定源系数偷偷改成刷新系数而不计二者差额。
第5节为避免这个混用，始终采用第2节不刷新 tag 的基准 replay。

## 5. 对角工作的确切 martingale 表达

在所有源行使用同一个 A~p，并独立抽取联合目标 Y，其每行边际为 Q_i。
固定一个全局顺序，逐个替换所有行中的未来 source 动作；同一行内顺序如第2节。
记总共 N=m(m-1)/2 个未来 action 单元，源/目标加权动作向量分别为 b_e,c_e，
其中 v_A=t·1_A、b_e=t·1_(source action)、c_e=t·1_(target action)。
所有 root tag 最后各自换到目标；它们不改 deleted load。
令

    G_k=sigma(Y, all source action cells not yet erased after k),
    M_k=E[v_A|G_k],       M_N=v=E[v_A],
    Delta_k=M_(k-1)-M_k.

这是一个 reverse martingale，且

    sum_k E||Delta_k||²=E||M_0-v||²<=Vp.             (ONE-QUERY)

总 deleted shadow load 在第 k 层是 G_k 可测。
将独立终端与源配对给准确的 covariance 工作

    Cov=sum_i E <v_A-v, t ell_i(Z)-t ell_i(Y)>
       =sum_k E <M_(k-1)-v,b_k-c_k>
       =sum_l E <Delta_l, sum_(k<=l)(b_k-c_k)>.       (DIAGONAL)

因此保守 replay 已给正确的终点和 signed floor 总额，但 ONE-QUERY 的半能量
还不是 DIAGONAL 的上界：每个信息增量乘的是全部已替换 prefix 的向量，
不是它自身。一个信息增量可以代表许多旧 source 动作的共同依赖。
不能把这些 prefix 乘数删掉或为每次出现另领 Vp/2。

可继续尝试用 genuine floor/IC 与 reciprocal 曲率支付这些 prefix 乘数；
本页没有该 bound，也未把终点 floor 非正误用成所有中间点 floor 非正。

## 6. 五人压力与状态

m=5 时 N=10，所有流、端点边际和 COMMON-WORK 原式成立。
尚未证明 DIAGONAL<=D+IC+G+(gamma+Qstat)/2，
所以没有 W>=(9gamma-Qstat)/2 或 HALF 新结论。
本次完成的是一个实际可检查的同根保守耦合及其共同银行付款，不是扫描或改名。

## 7. 最新 uniform NET-cap 版本及独立检查

令 B_i=d_i+sum_(k>i)[M(z_<k)-u_k]，只要求全局 sum_i E_Q B_i<=W。
同一个已构造保守流准确给

    sum_(all edges)flow Delta B_i
      =sum_i(E_Q B_i-E_P B_i)<=I_total+S_total,
    I_total=W-sum_i E_Pd_i>=0,
    S_total=sum_i E_P sum_(k>i)[u_k-M]>=0.

有一个统一 mu>=0 时，共同 shadow 双式中的 mu Delta B_i 由这一份组合 cap 银行付；
不得再分别使用 E_Qd_i 或 E_Qfloor 的符号。

tree12 与 credible12 已独立核验 raw flow、终点、最后 tag 零 deleted shadow、
signed telescope、posterior retag 与 DIAGONAL。raw 坐标边通常不是真 sigma 偏离，
不能给它 Γ>=0。tree12/real_replay_covariance_flow.md 给同端点的另一条真实 replay：
逐个强制目标前缀，每次沿原 sigma 完成，从而未来边各有 genuine Γ>=0。
对每个 passive A，固定势及总对角 work 路径无关，两种总表达可相等；
不能逐边识别或互借局部银行。尚无对角金额结论。
