# 共享全槽池的末两行：真实 IC、插入税与共同 Jensen 余量

2026-10-25。一般有限共同目录、任意单位客户与人数、每个完整有序历史纯 SPE。
原 Q-CAG-HALF、删槽 SHARED 以及父方 full-pool 候选仍 **OPEN**。
本页只给可直接接入父方 full-pool 的末两行付款；关键去相关机制已经在
`research/current/customer_attraction/general_half_proof.md` 式(5)成立，
此处不认领新的去相关定理，也不把末两行付款冒充全路径付款。

## 1. 全槽对象和准确蕴含

固定原实际叶 z=(S_1,...,S_m)，利润 u_i，W=sum_i u_i。
原实际位置 i 强制 A 后沿同一原策略的完整叶记 Z_i(A)，完整负载 C_i(A)。
删当前槽的负载为 L_i(A)=C_i(A)-1_A。定义

    K^-=(1/m) sum_i conv{L_i(A): A in S},
    K^+=(1/m) sum_i conv{C_i(A): A in S}.

对于任意相同菜单系数 q_i，有

    L^+(q)=L^-(q)+(1/m)sum_i E_(A~q_i)1_A >= L^-(q).

故逐查询 p 都有 min_(K^+)F_p<=min_(K^-)F_p，其中
F_p(L)=sum_x rho_x/(1+L_x)，rho_x=Pr_(T~p)[x in T]。
强删槽 SHARED 付款蕴含 full-pool 付款。弱删槽 half 付款
W>=(m-1/2)gamma^- 没有仅由此大小关系推出 m gamma^+<=W。

原 Mpath 在全体 (i,A) 上允许任意列分布，而 K^+ 要求位置边际均匀，
因此**不能仅凭跨列 Jensen 得到 gamma^+<=Mpath**；该比较需要改成
uniform-position 的旧菜单值

    M_unif = min_(q_1,...,q_m) max_T
             (1/m)sum_i E_(A~q_i) sum_(x in T)1/[1+C_i(A)_x].

Jensen 正确给 gamma^+<=M_unif。一般有 Mpath<=M_unif；
两条上/下界方向不能合成 gamma^+ 与 Mpath 的比较。
若父方采用所有位置自由权重的 full-load 凸包，才可由同一列分布直接给
其值<=Mpath；那是另一个更大的负载域。本页保持父方均匀 Minkowski 定义。

父方的指定充分 helper 取 q_i=p：

    Cbar(p)=(1/m)sum_i E_(A~p) C_i(A),
    F_p(Cbar(p))<=W/m.                              (PF?, OPEN)

PF? 若真便给 full-pool。它比自由选 q_i 的候选更强。

## 2. 末两行独立全槽查询的无条件付款

设 m>=2，倒二实际前缀客户负载为 beta。倒二实际主题 P，末位实际主题 Q。
倒二强制 A 后的原真实末位最佳回复记 B(A)。因此

    C_(m-1)(A)=beta+1_A+1_(B(A)),
    C_m(A)=beta+1_P+1_A.

写 U_beta(T,B)=sum_(x in T)1/[beta_x+1+1_B(x)]。
对相互独立的 A,T~p，定义独立额外查询

    J_(m-1)=E_(A,T) sum_(x in T)1/[1+C_(m-1)(A)_x],
    J_m=E_(A,T) sum_(x in T)1/[1+C_m(A)_x].

真实当前 IC 给

    I_(m-1)=u_(m-1)-E_A U_beta(A,B(A))>=0,
    I_m=u_m-E_T U_beta(T,P)>=0.

原末位在历史 (prefix,A) 上允许改为 B(T)，所以整条 BR slack

    G(A,T)=U_beta(B(A),A)-U_beta(B(T),A)>=0.

末两人对称交项恒等式平均后（一般工作稿式(5)）给

    E_A U_beta(A,B(A))-E_(A,T)U_beta(T,B(A))
        =E_(A,T)G(A,T).                             (DC)

全部真实比较来自原末位在各自原历史的整主题 IC；没有客户重加权。
对 beta 客户逐项做额外插入，定义

    Tax_p(A,T)=sum_(x in A intersect T)
       1/[(beta_x+1+1_(B(A))(x))
          (beta_x+2+1_(B(A))(x))],

    Tax_m(A,T)=sum_(x in A intersect T)
       1/[(beta_x+1+1_P(x))(beta_x+2+1_P(x))].

二者均非负，而且精确有

    u_(m-1)-J_(m-1)
       =I_(m-1)+E G+E Tax_p >=0,                  (PENULT-PAY)
    u_m-J_m=I_m+E Tax_m >=0.                       (LAST-PAY)

这不需要 p 是某个 saddle，也不需要 query 支持的主题价格相同。
任意背景 beta、任何原历史依赖的末位平局均保留。m=2 的 PF? 因此直接成立。

## 3. 共同池的准确剩余付款

对全部行 i 仍使用同一 p，令

    J_i=E_(A,T~p) sum_(x in T)1/[1+C_i(A)_x],
    V(p)=sum_i J_i-m F_p(Cbar(p)) >=0.

V 是把全部位置和强制主题共同平均之后的 reciprocal Jensen 余量，
不是每行各拿一份同额资金。上面的真正终端付款给精确式

    W-m F_p(Cbar(p))
      =sum_(i<=m-2)(u_i-J_i)
         +I_(m-1)+I_m+E G+E Tax_p+E Tax_m+V(p).

因此 PF? 的明确剩余义务是

    sum_(i<=m-2)(J_i-u_i)
      <=I_(m-1)+I_m+E G+E Tax_p+E Tax_m+V(p).      (EARLY-PAY?, OPEN)

这给实际非负终端银行，但未证明早期税可由它支付。
早期各行的后继是一整段真实 SPE；不能把整段后继当一个玩家，免费调用 DC。
V(p) 已使用全部行的同一池；不能再把其逐行 Jensen 余量重复加入右端。

同一一般推导代入 m=5，前3行仍需 EARLY-PAY?，故未无条件推出 OPT_5<=2W。
对一般 m 的全路径付款仍然是主目标。

## 4. 有限压力测试的准确范围

`pooled_full_probe.py` 对6份旧输入逐定义重放完整策略，全部通过原始 IC，
再多起点浮点优化 PF? 的 p。未发现分离，见同名 JSON。
`attack_pooled_full_cone.py` 在24个完整有序历史 BI 策略上，保留全部 IC 线性锥，
归一 W=1，交替优化 p 与非负客户类型重数；仍未分离。
这两组均为有限浮点阴性，既不是 PF? 的证明，也不是 full-pool 或 half 的证据。
它们只记录已经检验的精确候选和可复跑方法，不作为继续扫描的理由。

`attack_shared_cone.py` 另在30个完整策略锥、每锥3个固定 p 上检验原删槽
SHARED；切平面保留完整策略全部 IC，并对共享负载做凸全局最小化。
未分离同样不提升 SHARED。共同 core 类型造成等号边界，诊断力有限。

没有发现原目标反例，没有新增一般福利常数，没有调用 git 或 work.py。
