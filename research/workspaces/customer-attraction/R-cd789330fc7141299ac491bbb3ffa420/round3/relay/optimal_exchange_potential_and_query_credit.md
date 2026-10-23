# 最优交换势、同叶收益信用与全深度查询重复预算

2026-10-23。一般有限共同目录、任意 m、单位客户/玩家；所有原有序历史分别保留。
**本文给全输入有效的证明组件，未证明 Q-CAG-HALF。**

来源：Bernoulli 最优替槽及调和核由 shared 提出、root 重构；固定配对 Beta 势由 relay/shared 同时得到；同叶信用预算由 shared 给出；全深度最优前缀查询信用由 relay 给出并获 root/shared 独立重构；owner partition 薄化由 shared 给出并获 relay/root 独立重构。外审及世界新颖性未认证。

## 1. 固定一个全局最优槽配对

令 T=(T_1,...,T_m) 为任意最优 m 槽元组，O 为并集，a_x 为其中覆盖数。比较索引允许重复。固定一次槽配对后，任何主题 profile B 的客户负载为 c_x(B)，并令 J(B) 为 O 内没有任何同槽 T_i∩B_i 覆盖的客户。

最优替槽调和核给

    Phi_T(B)=sum_(x outside O) H_(c_x(B))
                -sum_(x in J(B)) Beta(a_x,c_x(B)+1)<=0.    (P)

空槽只作为形式势计算：它不是一个新的 SPE 行动。若某槽空着，可填任意合法主题；下文的单调性也保证其势不超过最优上界。没有删除祖先并调用较小 SPE。

将当前槽 i 的主题形式去掉，记 B_-i。定义势边际

    ell_i(B)=Phi_T(B)-Phi_T(B_-i).

若 i 覆盖 x，写 c=c_x(B)>=1。有三种情形：

- x outside O：边际为 1/c，恰等于真实收益。
- x in O，且另一个槽已经同槽保护 x：边际为0。
- x in O，无其他同槽保护：若 x in T_i，边际为 Beta(a,c)；若 x notin T_i，边际为 Beta(a,c)-Beta(a,c+1)=Beta(a+1,c)。

这些数均位于 [0,1/c]。因此真实收益可精确分为

    u_i(B)=ell_i(B)+e_i(B),    e_i(B)>=0,              (D)

且 e_i 的客户支持全在 O。这个分解对任意 profile 成立，不要求 B 为 SPE。

固定**同一个** B，逐客户真实收益总和为覆盖指标，所以

    sum_i e_i(B)<=|O intersect union(B)|.               (LEAF)

特别在原实际叶 Z，此预算至多 |I|。不能将不同真实 rollout 的 e_i 分别装进同一 I 预算。

## 2. owner partition 薄化：单位最优基线

将 O 任意分割为 Q_1,...,Q_m，满足 Q_i subset T_i。Q_i 不必是合法主题，不能当偏离使用；只用于静态最优性基线。

任意 Q/B Bernoulli hybrid 可以逐槽将未替换的 Q_i 扩为 T_i，覆盖只增，扩大后是合法 m 槽组合。因此每个原 hybrid 覆盖仍<=OPT。基线 union Q=O，每个 O 客户的基线覆盖数恰为1，所以同一调和核给

    F_Q(B)=OPT+sum_(x outside O)H_c
                 -sum_(x in O: owner槽B不覆盖x)1/(c+1)
           <=OPT.                                    (OWNER)

等价的非负、空 profile 归零形式是

    F_Q(B)=sum_(x outside O) H_c
       +sum_(x in O) [1-(1-s_x(B))/(c_x(B)+1)],

其中 s_x=1 表示 x 的固定 owner 槽在 B 中覆盖 x。F_Q(T)=OPT；所有实际主题仍为原目录主题。

F_Q 对带槽标签的主题 token 是单调次模函数。逐客户看：O 外是凹序列 H_c；O 内在没有 owner 保护时为 c/(c+1)，一旦 owner 覆盖则饱和为1。普通覆盖边际随已有 c 减少，owner 的饱和边际也随 c 减少，保护之后所有额外边际为0。

形式空槽可以用合法主题补满，单调性说明所有不超过 m 槽的合法/形式空混合 profile 也满足 F_Q<=OPT。此处只做静态填槽，不更改原策略树。

owner 势的边际特别简单。对 i 覆盖的 x、完整负载 c>=1：

| 客户情形 | ell_i^Q(x) |
| --- | --- |
| x outside O | 1/c |
| i 为 owner，且 i 覆盖 x | 1/c |
| 另一 owner 槽已覆盖 x | 0 |
| owner 槽不覆盖 x，i 非 owner | 1/[c(c+1)] |

因此仍有 u_i=ell_i^Q+e_i^Q、e_i^Q>=0，O 外 e=0。同叶有精确式（c>0）：

    sum_i ell_i^Q(x)=s_x/c+(1-s_x)/(c+1),    x in O,
    sum_i e_i^Q(x)=1-s_x/c-(1-s_x)/(c+1).

故原实际叶的 sum e_i^Q<=|I|，O 外的 sum ell_i^Q=|G|。这些信用每叶一次；没有跨枝免费复用。

### 信用本身是非owner插入势边际

令 k_x(B) 是除 owner 槽之外覆盖 x 的槽数。每个非owner i 覆盖 x 时，其信用始终恰为 e_i^Q(B;x)=1/(1+k_x(B))，不依 owner 是否实际覆盖。owner 已覆盖时真实收益就是该数、势边际0；owner 未覆盖时真实收益1/k减势边际1/[k(k+1)]仍为该数。owner 本人信用0。因此

    sum_i e_i^Q(B;x)=k_x/(1+k_x),
    Psi_Q(B)=sum_(x in O)[H_(1+k_x(B))-1],
    e_i^Q(B)=Psi_Q(B)-Psi_Q(B_-i).                    (INSERT)

逐客户精确有 H_(c_x)=F_(Q,x)+H_(1+k_x)-1（x in O），故原调和 Rosenthal 势正好等于 F_Q+Psi_Q。附加信用是固定背景1的非owner插入支付，不是任意误差标量；原 sigma 没有自动成为其中任何一个分量游戏的 SPE。

## 3. 全深度最优前缀的查询信用

固定任意排列 pi，一次性把最优主题 T_(pi(i)) 配给时序槽 i。令

    h_i=(T_(pi(1)),...,T_(pi(i-1))),
    Y_i=同一原完整策略sigma在h_i后强制T_(pi(i))再真实继续的终局。

这里每个 h_i 是原游戏的合法有序历史；不合并计数，不替换后继，不要求 Y_i 各自独立可选。下述界事实上对任何保留该最优前缀的 Y_i 均真，不要求理性。

当前真实查询收益为 d_i。形式势边际为 ell_i(Y_i)，查询信用为

    r_i=d_i-ell_i(Y_i)>=0.

### 固定原 Beta 势

逐客户 x，a=a_x，按它在最优查询顺序出现的第 s 次计数：首次查询的信用<=1-1/a（a=1 精确0）；之后第 s>=2 次已经有前缀中的同槽保护，故势边际0、信用<=1/s。因此

    sum_i r_i(x)<=1-1/a+sum_(s=2)^a1/s
                  =H_(a-1)<=a-1.                    (REPEAT)

首次界的证明：若没有其他同槽保护，信用为1/c-Beta(a,c)。c=1 时恰1-1/a；c>=2 时<=1/2<=1-1/a（a>=2）。若已有未来同槽保护，则 c>=2，仍用同一1/2界。a=1 不可能有另一个同槽保护，且 Beta(1,c)=1/c。

### owner 势的更强界

owner Q 取这个固定最优查询顺序中首次覆盖 x 的槽。第一次查询就是 owner，势边际恰1/c，故信用0。之后第 s>=2 次查询已有前缀 owner 保护，势边际0、当前真实分母至少 s，故信用<=1/s。因此

    sum_i r_i^Q(x)<=sum_(s=2)^a 1/s=H_a-1<=a-1.       (OWNER-REPEAT)

特别最优覆盖次数 a=1 的客户，沿整个前缀查询过程没有任何折扣信用；共享比较客户的全部折扣由重复比较预算支付。对 O 外客户，所有查询 T_i 均不含它，信用0。

这是对全部输入有效的联合预算，确实接到捕获流中重复比较信用 sum_R(a_x-1) 的口径；它没有声称这些前缀查询收益就是原实际位置的 matching 矩阵收益。

### 直接适用原实际前缀 matching 的重复界

不用改变到最优前缀。固定任意 matching pi、任意 Q_i subset T_(pi(i)) 分割 O，令 Y_i 是原实际前缀 i 后强制 T_(pi(i)) 的真实 rollout。对每个 x，owner 行的查询势边际恰等于该行真实收益，故 r_owner(x)=0。非owner 查询若 owner 在该叶覆盖 x，则 c>=2，信用为1/c<=1/2；若 owner 不覆盖，信用为1/(c+1)<=1/2。因此

    sum_i r_i(x)<=(a_x-1)/2                          (DIRECT-REPEAT)

对这些**原实际前缀**枝直接成立。前缀锚定版本提供另一 harmonic 界，不是 DIRECT-REPEAT 的前提。此界在原捕获矩阵中保持同一重复预算口径，但尚未给出把所有项相加后完成 FLOW 的证书。必须分别记账：R 上至多 sum_R(a_x-1)/2；I 上另有 sum_I(a_x-1)/2，不能把 I 上多次查询的信用丢进只有 R 的重复预算。

每个 O 客户在其 owner 查询枝的 F_Q 客户值恰为1，其余枝值非负，因而 sum_i F_Q(Y_i)>=OPT。不过不能丢弃跨枝 excess

    E=sum_i F_Q(Y_i)-OPT>=0

后要求总 ghost 势小。完整代数为

    OPT=sum_i d_i-sum_i r_i+sum_i F_Q(Y_i_-i)-E.

若 Y_i 以原实际前缀取出，sum_i d_i<=W。这把任务写为净 ghost 势而不是总 ghost 势；保留 E 后仅是原 matching 支付的另一余额身份，不计新一般付款。

特别 outside O 的 F_Q(Y_i) 与 F_Q(Y_i_-i) 完全相同（当前查询属于 O），其贡献在 ghost 和 E 之间逐项相消。不能把所有这些互斥枝的 outside 势改称原实际 G，也不能独立重复收其预算。

## 4. 完整原 IC 在新势下留下的精确跨 rollout 项

固定同一 pi、Q。令 B^0 为原实际叶；B^(i-1) 是原 sigma 在 h_i 后的真实 rollout，B^i=Y_i。最后 B^m=T_pi。

在节点 h_i，当前规定收益 u_i^h，强制 T_(pi(i)) 的收益 d_i，原 SPE 给

    g_i=u_i^h-d_i>=0.

原规定动作在 B^(i-1) 的信用记 e_i^-，查询在 B^i 的信用记 r_i^+。只做形式去当前槽，定义

    D_i=F_Q(B^i_-i)-F_Q(B^(i-1)_-i).

直接相减得精确恒等式

    F_Q(B^i)-F_Q(B^(i-1))
        =e_i^- -r_i^+ -g_i+D_i,

因此全深度 telescoping 给

    OPT-F_Q(Z)+sum_i r_i^+ +sum_i g_i
       =sum_i e_i^- +sum_i D_i.                    (ROLL)

这里每一项原 IC 都完整使用，没有乘改变积分符号的 Beta 权。OWNER-REPEAT 只定量控制查询折扣：当把它移到右侧时带负号，不能将其上界代入以虚增有利的扣除量。LEAF 只支付固定实际叶的信用，不能把右侧来自不同 B^(i-1) 的 e_i^- 简单求和后套 |I|。

**剩余承重为联合控制 sum_i(e_i^-+D_i)。** D_i 的两边来自同一个原真实节点的两个真实终局，但形式去槽 profile 只是势计算；没有宣称它们是删人 SPE。F_Q 各自有 [0,OPT] 静态界，这并不能给全路径一次预算。当前尚未得到所需的全树非负运输或超鞅，不据此宣称 half 或 FLOW 已闭合。

## 5. 边界和审查

m=1、零客户、空主题、重复主题按槽索引处理；所有和允许为空。H_0=0。O 外 c=0 没有收益项；O 内边际公式只在当前确实覆盖、c>=1 时用分式。owner 只赋给 x in O，不给未最优覆盖客户强造索引。

固定一次 pi 后才固定 owner。若平均多个 pi，需对每个 pi 分别使用其势和其真实前缀，不能跨配对混用边际。

取 first-owner Q_i=T_(pi(i))\union_(l<i)T_(pi(l)) 时还有分析性三角性质 T_(pi(i))∩Q_j=empty (i<j)。对未来 owned-R 客户，原实际祖先与先前最优查询祖先均不覆盖它；真实中间 σ 动作仍可提前覆盖，不能假设其消失。将这部分作为 forward 捕获流候选继续研究，尚无共同容量证明。

root/shared 已独立重构 REPEAT；shared 的独审记录见 `../shared/review_global_exchange_potential.md`。OWNER 薄化及 OWNER-REPEAT 已由 relay 从陈述独立重构并报 root。数值审计只核这些精确公式与边界，普遍性由上述证明承担。
