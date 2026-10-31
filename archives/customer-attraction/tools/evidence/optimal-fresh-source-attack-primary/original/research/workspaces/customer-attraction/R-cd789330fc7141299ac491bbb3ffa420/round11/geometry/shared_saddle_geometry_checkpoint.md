# 共享负载 saddle 的等价格几何与 half-slot 未付款

2026-10-25，round11/geometry。执行窗口 checkpoint。
一般 Q-CAG-HALF 仍 OPEN；**本轮此段没有证明新的金额付款。**
以下精确归一化承接 parent/shared_load_bregman_working.md，保存可接续对象，
不把 saddle、PSD 或非负 Bregman 余项本身当作福利证明。

## 1. 同一共享 saddle，全部真实历史保留

实际位置 i 强制主题 A 后，原完整 SPE 的真实完成叶删除当前槽，负载记 L_i(A)。
自由共享负载域为

    K=(1/m) sum_i conv{L_i(B): B in catalog}.

取凸 minimax 的 saddle (p*,L*)，其值记 gamma，令

    rho_x=Pr_(A~p*)[x in A],
    t_x=1/(1+L*_x),
    F_p(L)=sum_x rho_x/(1+L_x).

于是全部合法主题都有 g_t(A)=sum_(x in A)t_x<=gamma，
p* 正支持上的主题等号成立。没有断言原策略在这些主题间隐藏随机化；
p* 只是分析中对真实偏离行的非负组合。

令

    v_A=(t_x 1_(x in A))_x,
    v=E_p* v_A=(t_x rho_x)_x,
    w_i(A)=(t_x L_i(A)_x)_x,
    h=(t_x L*_x)_x=(1-t_x)_x.

所有向量都在同一个有限客户空间中，不合并有序历史。
正支持查询满足 ||v_A||_1=gamma。

## 2. tangent payoff 是一个共同 Gram 核加非负误差

令 c_i(A)=1_A+L_i(A) 为该真实偏离叶的最终负载。
逐客户恒等式给当前真实收益

    d_i(A)=2 g_t(A)-||v_A||_2^2-<v_A,w_i(A)>+D_i(A),

    D_i(A)=sum_(x in A) (1-t_x c_i(A)_x)^2/c_i(A)_x >=0.

分母正，因为只在 x in A 上求和。正支持查询的第一项准确等于2gamma。
因此非误差部分具有共同 PSD 交互核

    G(A,B)=<v_A,v_B>,

但 ||v_A||_2^2 可以随等价格主题 A 变化，不能把等 L1 价格误读为等自范数。
令 s=E||v_A||_2^2=sum_x rho_x t_x^2，则

    <v,h>=gamma-s.

这一切只是同一真实收益的合法 tangent 展开，没有把原 SPE 移植到 affine 游戏。

## 3. KKT 真正支付了哪个线性部分

设 M_i=max_B <v,w_i(B)>。
负梯度 KKT 给：L* 的第 i 行凸实现只在最大化该内积的菜单列上有正质量，且

    sum_i M_i=m<v,h>.

由此对真实 query 推送分布有一个确实非负的 KKT 松弛

    G_KKT=m<v,h>-sum_i E_A<v,w_i(A)> >=0.              (KKT)

定义 query-response 协方差

    Vcorr=sum_i E_A <v_A-v,w_i(A)>.

原 parent 草稿的线性关联项 C 精确分解为

    C=Vcorr-G_KKT.                                    (GEO)

故 KKT 已支付的是去相关的平均方向，尚未支付与查询实现相关的那部分负载。
共同等价格超平面与 Gram PSD 不推出 Vcorr<=0，也不推出 C<=0。
parent/aggregate 的真正 saddle 保险例已有 C>0；本分支未重算或改写它。

## 4. HALF 只需 half-slot，不必要求整槽聚合

令

    I=sum_i [u_i-E_A d_i(A)] >=0,
    D=sum_i E_A D_i(A) >=0.

真实行与 tangent 恒等式给

    W-m gamma=I-C+D.

若目标是更强 W>=m gamma，需要 C<=D+I；这仍未证。
但是原 HALF 只需要更弱的

    W >= (m-1/2) gamma,

因为静态比较给 OPT_m<=(2m-1)delta_m，且 K 是合法分数背景域的子集，
所以 delta_m<=gamma，继而 OPT_m<=(2m-1)gamma。
准确的剩余充分付款义务为

    C <= D+I+gamma/2,                                 (HALF-SLOT?, OPEN)

或者结合真正非负的 (KKT)，写成

    Vcorr <= D+I+G_KKT+gamma/2.                        (GEOM-HALF?, OPEN)

这是减少了要求的**条件充分目标**；额外 gamma/2 是允许的误差，
没有已证可花的 gamma/2 钱包。本页没有从终端钱包导出该金额。

同一一般公式代入 m=5 需要 W>=(9/2)gamma，并由 OPT_5<=9gamma 得 HALF。
本页仍没有证明该不等式对任意五人输入成立。

## 5. 为什么普通 PSD/Cauchy 并未自动补款

把 Vcorr 中 w_i(A) 换成 w_i(A)-h 不改其值。
普通 Cauchy/Young 只能把它变成 query 方差与**完整响应向量**方差的乘积或和。
而 D_i(A) 只含被当前 query 覆盖的坐标，并且权重为

    t_x^2/[1+L_i(A)_x].

因此完整欧氏响应方差没有自动由 D 支配：query 未覆盖坐标上的响应变化
不进入该条 D_i(A)。中心化项在那里仍可能为正。
这是指出两种准确对象不匹配，不是证明 PSD 路线不可能。
若能从全历史 IC、共同二元主题几何或终端信用证明 (GEOM-HALF)，即可接回原目标；
目前没有此新关系。

## 6. 可接续状态

已经保存：等价格向量化、PSD tangent 核、KKT 支付项 G_KKT>=0、
其与剩余协方差的精确分解，以及只需 half-slot 的充分目标。
未取得：把剩余协方差按同一金额支付的正通用不等式。
没有新扫描、没有新一般福利定理、没有原 HALF 反例，也没有任何方法不可能断言。
