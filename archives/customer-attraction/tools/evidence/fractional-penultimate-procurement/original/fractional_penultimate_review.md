# 倒二分数采购合同：盲独立审查

2026-10-25。只审查 tree_coupling 发来的精确合同与证明概述，未读取其正文。原 Q-CAG-HALF 仍 OPEN。以下核对适用于任意合法背景、单位客户、共同有限非空目录、全部有序历史纯 SPE 和任意真实末位最佳回复；仅倒二位置，不提供更早位置的一般付款。没有运行 git 或 work.py。

固定背景负载 b，实际末两主题 A,B，实际末位最终利润记 u。对合法当前动作 T，D(T) 为同一原完整策略的真实末位最佳回复，d(T)=U_b(T,D(T))。令 z_T>=0，a_x=sum_(T contains x) z_T，v_x=min(1,a_x)，F=sum_x v_x。定义 t_b(T)=sum_(x in T)1/[(b_x+1)(b_x+2)]，W 为含旧背景的实际最终覆盖。待审合同为

    sum_T z_T d(T) >= F-W+t_b(A).

## 去相关尺度与截断

若 tau=sum z_T>0，取 p=z/tau。单后继去相关对 p 的正确乘法是

    sum_T z_T d(T) >= E_(T'~p) sum_T z_T U_b(T,D(T')).

右侧没有额外 tau，也没有遗漏 tau。逐客户系数为

    a_x [1/(b_x+1)-1_(x in D)/((b_x+1)(b_x+2))]。

括号严格为正，所以把 a_x 降到 v_x 合法。记 Omega_v=sum_x v_x/(b_x+1)，即得

    sum z_T d(T) >= Omega_v-E_D sum_(x in D) v_x/[(b_x+1)(b_x+2)].

因 0<=v<=1，每个罚项至多 t_b(D)。又逐客户有

    1/[(b_x+1)(b_x+2)] <= 1/[b_x+1+1_(x in A)]，

因此 t_b(D)<=U_b(D,A)<=u；最后一步只是实际末位在背景 b+A 的合法主题比较，未把 D 当作该处真实回复。于是得到 sum z_T d(T)>=Omega_v-u。

## 最终覆盖付款逐客户复核

需证明 W-F+Omega_v>=u+t_b(A)。若 b_x>0，左侧该客户系数为 1-v_x+v_x/(b_x+1)>=1/(b_x+1)。右侧系数是

    1_(x in B)/[b_x+1+1_(x in A)]
    +1_(x in A)/[(b_x+1)(b_x+2)]。

当 x 同属 A,B 或只属 B 时，右侧恰为 1/(b_x+1)；只属 A 或两者皆非时更小。若 b_x=0，左侧就是实际覆盖 indicator，右侧为 1_B/(1+1_A)+1_A/2，四种 A/B membership 均不超过该 indicator。因此合同成立。

tau=0 时 F=0、左侧为零，只需 t_b(A)<=W；每个 A 客户贡献不超过一且都被实际覆盖，成立。零客户、空主题、重复选择均不产生零分母。

## LP 对偶

合同对全部非负 z 成立，等价于

    max_(z>=0) [sum_x min(1,sum_(T contains x)z_T)-sum_T d(T)z_T]
    <= W-t_b(A)。

该有限 LP 的对偶可取客户价格 y_x，0<=y_x<=1，sum_(x in T)y_x<=d(T)，目标 min sum_x(1-y_x)。因此存在同一价格向量满足 sum_x(1-y_x)<=W-t_b(A)。不可覆盖客户可保留并取 y_x=1；它们不给主题约束增加负担，也不给缺口增加成本。

审查结论：当前倒二分数合同、尺度、截断、同一次付款与对偶符号通过上述独立数学核对。未审查代码或世界新颖性；未把倒二付款推广给任意早期位置。

## 后读核对：旧证明保留当前 IC 松弛的更强推论

以上盲审完成后，读取 `tree_coupling/fractional_penultimate_procurement.md` 及其旧来源 `R-e5d83af532dc495c966f99cf70cda2a2/parent_tail/penultimate_price_defect.md`。旧稿定义 S=tau*u_A-sum z_T d(T)，G=S+H，其中 H=Z/(2tau)+V/tau+L/2>=0。旧稿逐客户公式减去 S_x 后，正得到

    [F-sum z d+H]_x = beta_x+r_x-a_x/[2(b_x+2)]，

其中这里 a_x 是实际 A 的 indicator（非前文分数负载），r_x 为旧角点表的截断余项。联合会员 h_x 精确抵消。故直接沿旧角点表给

    F-sum z d+H <= u_B+P_old+E = W-u_A+E。

H>=0 即给菜单价格敏感加强 F-sum z d<=W-u_A+E，不需要当前 IC。tau<1 时分数覆盖和真实菜单成本都线性缩放，且右侧非负，所以旧缩放论证仍有效。旧收费定义 E 及 E<=u_A/2 未改变。逐客户 u_A-E>=t_b(A)，故加强确实覆盖先前弱合同。

该加强是旧证明保留松弛的合法推论；未加入新的早期机制，不应重新认领旧端点或称一般 half 完成。
