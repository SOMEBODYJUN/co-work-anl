# 任意稀疏槽位的实际 hit 时钟租金与精确跳过溢价

2026-10-22；作者解析推导，父方独立核对单 hit 差系数，完整表示待独审。CAG-MODEL / Q-CAG-HALF 不变，一般半覆盖仍 OPEN。本稿是普遍路径表示与共同根支付接口；尚未从真实全树激励产生所需系数。

## 1. 对象：允许任意稀疏未来槽位

固定任意实际主题路径 S_1,...,S_m，不要求 SPE。客户均单位，允许重复主题、空主题和零客户。记

    b_t(x)=sum_(v<=t) 1_(x in S_v),    b_0(x)=0,
    c_x=b_m(x),    W=|{x:c_x>0}|.

对每个 j=1,...,m-1 任取 I_j subset {j+1,...,m}，不要求连续。取与客户无关的全行权 theta_j>=0 和 reserve rho>0。定义同一槽位拥塞

    D_t=sum_(j:t in I_j) j theta_j,    Gamma=max_t D_t.

原来的 **重置时钟租金** 为

    E_j^reset=sum_x b_j(x)[1/(rho+b_j(x))
                          -1/(rho+b_j(x)+q_j(x))],
    q_j(x)=sum_(t in I_j) 1_(x in S_t).

“重置”只描述其代数：被跳过的实际 hit 不进入后一个选中 hit 的分母，未声称任何策略真的重置。

定义 **实际时钟租金**

    E_j^clock=sum_(t in I_j) sum_(x in S_t)
              b_j(x)/[(rho+b_(t-1)(x))(rho+b_t(x))].       (1)

式(1)始终保留每个所选实际槽位此前的全部真实 hit；未选中槽位不给本行直接收费，但会稀释之后的收费。两种租金都非负。

固定 H_j 的旧玩家群体，其在安装 reserve 后、到实际槽位 t 的代数总租金是

    R_(j,t)=sum_x b_j(x)/(rho+b_t(x)),   t>=j.

因此 (1) 正是 sum_(t in I_j)[R_(j,t-1)-R_(j,t)]。旧群体始终固定，未把后插入的玩家加入分子；reserve 只是代数装置，不是合法目录行动。

## 2. 任意稀疏集合仍可共同支付 clock 部分

**SPARSE-CLOCK-RENT。** 对上述任意路径、稀疏集合、全行权及 rho>0，

    sum_j theta_j E_j^clock
      <= Gamma sum_(x:c_x>0)[1/(rho+1)-1/(rho+c_x)]
      <= Gamma W/(rho+1).                                (2)

**证明。** 固定客户 x，真实 hit 槽位为 t_1<...<t_c。按实际 hit 排名交换有限和，(1) 的加权总贡献精确等于

    sum_(k=1)^c [1/((rho+k-1)(rho+k))]
                    * sum_(j:t_k in I_j) theta_j b_j(x).   (3)

当 k=1 时，每个 j<t_1 的 b_j(x) 都为零。其余每个 k 的内层非负，且 b_j(x)<=j，故内层至多 D_(t_k)<=Gamma。于是 (3) 至多

    Gamma sum_(k=2)^c 1/[(rho+k-1)(rho+k)]
      =Gamma[1/(rho+1)-1/(rho+c)].

对客户求和得到 (2)。c=0 或1的贡献为零；m=1或空槽位集合也给零。证毕。

特别 rho=1、Gamma<=1 时 clock 部分至多 W/2；Gamma<=2 时至多 W。这里几何连续性完全不是前提，真正承重的是分母使用同一个真实 hit 排名。

## 3. 原重置租金 = clock 租金 + 精确非负 skip-premium

对行 j 和客户 x，将 I_j 中覆盖 x 的槽位按时间写为

    t_(j,1)<...<t_(j,q),    q=q_j(x).

对第 k 个选中 hit 定义

    a=b_j(x)+k,       b=b_(t_(j,k))(x).

a 是将未选中实际 hit 删除后得到的虚拟 hit 排名，b 是真实 hit 排名，所以整数 b>=a>=1。a,b 可随 j,k,x 变化。旧租金的倒数差展开给该 hit 系数 b_j/[(rho+a-1)(rho+a)]；clock 系数是 b_j/[(rho+b-1)(rho+b)]。两者之差严格等于

    p_(j,k,x)
      = b_j(x)(b-a)(2rho+a+b-1)
          /[(rho+a-1)(rho+a)(rho+b-1)(rho+b)] >=0.         (4)

这是乘分母后使用

    (rho+b-1)(rho+b)-(rho+a-1)(rho+a)
       =(b-a)(2rho+a+b-1)

得到的恒等式。令 P_j=sum_(x,k) p_(j,k,x)，则有完整精确表示

    E_j^reset=E_j^clock+P_j,     P_j>=0.                  (5)

因而

    sum_j theta_j E_j^reset
      <= Gamma sum_(x:c_x>0)[1/(rho+1)-1/(rho+c_x)]
                       + sum_j theta_j P_j.             (6)

(6)没有丢失任何重置误差：唯一尚未支付的量被准确隔离为 skip-premium。全行权没有按客户选择；客户排名只用于展开已固定的同一代数行。

当 I_j={j+1,...,j+ell_j} 时，每个 a=b，所以 P_j=0，clock 精确等于原 E，恢复已有连续窗口引理。反之 P_j=0 的充要条件是：对每个已有正前缀负载 b_j(x)>0 的客户，每个选中 hit 之前均未跳过该客户的实际 hit。槽位可以不连续，只要省略的行动不会产生这种对已有客户的 hit 缺口即可。因此允许“对每个收费客户的 hit 初段连续”，比几何槽位连续更宽。

## 4. 真正完整 SPE 的全部无界成本恰在 premium

使用相邻稿 `sparse_slot_complete_spe_obstruction.md` 的两客户完整 SPE：A={x}, B={y}, m=2q，实际路径 A,B^q,A^(q-1)，j=1,...,q-1 选择 I_j={q+1+j}、theta_j=1/j。已证明完整策略在全部有序历史最优，W=OPT=2、Gamma=1。

该行对 x 的前缀负载为1，唯一选中 hit 的虚拟排名 a=2，真实排名 b=j+1。因此 rho=1 时

    E_j^reset=1/6,    E_j^clock=1/[(j+1)(j+2)],
    P_j=1/6-1/[(j+1)(j+2)].

于是

    sum_(j=1)^(q-1) E_j^clock/j
      =sum_(j=1)^(q-1) 1/[j(j+1)(j+2)]
      =1/4-1/[2q(q+1)] <=1/4,                            (7)

其中用 1/[j(j+1)(j+2)]=(1/2)[1/(j(j+1))-1/((j+1)(j+2))] 望远镜。

另一方面

    sum_(j=1)^(q-1) P_j/j
      =H_(q-1)/6-1/4+1/[2q(q+1)] -> infinity.           (8)

因此完整 SPE 性、每槽一次与1/j权归一化，并不支付 premium。此处 clock 部分甚至一致小于1/4，全部调和发散都准确落在 premium，而不是(2)的共同根支付失败。

## 5. 对全树连接的严格要求

本表示提供两个可接续的充分接口：

1. 从同一给定 SPE 的真实不等式构造运输，使误差直接等于 clock 部分，并有可控 Gamma；
2. 若真实代数必然产生 reset 部分，则必须另外用真实激励松弛、带符号抵销或其他根信用支付 sum theta P。

目前两者都未构造。不能仅把 reset 系数改写成 clock 并删除 P，也不能让额外实际 hit 的分母凭空出现。固定m pair-circuit 的合法终局仍不自动是所给 SPE 的真实偏离终局；本稿未改变这个缺口。

`audit_chronological_sparse_rent.py` 用 Fraction 对全部有限二元路径与任意稀疏集合独立重建 reset、clock、premium 和槽位预算，并核对(7)(8)。一般结论依据第2、3节证明，有限检查不提升成全树支付或半覆盖证明。
