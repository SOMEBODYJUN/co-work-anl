# 共享激活中的 R/I 联合查询和逐角色 owner 信用

2026-10-23，mixed_menus。R激活核由relay提出，本页与OWNER-ROUTE合并。全输入解析组件，relay及shared收到精确陈述后分别独立重构通过；无外审或新颖性认证。一般Q-CAG-HALF仍OPEN。

## 固定对象

固定任意m、有限单位客户、有限非空共同目录及全有序历史纯SPE σ。实际终局Z、覆盖C，最优m主题T、并集O，固定一次owner分割Q_i⊆T_i。R=O\C，I=O∩C，G=C\O。令J_x为actual覆盖x的角色集，c_x^0=|J_x|，I^-={x∈I:o(x)∉J_x}。

给R固定残质量ρ_x∈[0,1]。I^-质量取1；owner实际已覆盖的I不在本页创建源。所有query仍是原实际前缀后强制合法a、随后沿同一σ的真实叶Y_i(a)。其客户负载c_s(x)=b_i(x)+1+|F_s(x)|，b_i为actual过去coverer数，F_s为真实未来coverer角色集。激活不删除任何真实行动、旧背景或客户负载。

## 一份随机实验

固定0<p<1，全角色独立Ber(p)激活，全部客户共用该组激活；另有一份独立全局均匀priority。客户仅在其owner激活时注入源，质量α_x为ρ_x（R）或1（I^-）。

若J_x有激活角色，源立即记给active J_x中priority最高者，进入actual信用汇。否则从(owner,T_owner,x)出发：若当前真实F中无active角色就在当前query吸收；否则去最早active future coverer，并将其真实主题作下一合法query，重置原实际前缀。后继也可按固定库存规则选任意合法含x主题；额外库存标签须保留。

角色严格递增，token有限终止。按dp/p积分，source概率p使总源质量为α_x。不是玩家隐藏混合承诺或分数SPE。

## I角色信用与剩余query库存

对x∈I^-，owner不在J_x，source激活独立于J。对称priority使各actual coverer积分信用相同，每个恰为

    (1/c_x^0)∫[1−(1−p)^(c_x^0)]dp=1/(c_x^0+1)。

这正是actual e_i(Z;x)。J全未激活的query吸收总质量恰为κ_x=∫(1−p)^(c_x^0)dp=1/(c_x^0+1)。信用与query库存互补为1；各actual角色精确对应自己的e容量，无需跨角色借同客户预算。R的J为空，全部ρ在query吸收。

owner实际已覆盖的I不能照用：source激活此时不独立于J，本文不作这项外推。

## 同一真实owner势边际控制吸收

记A_s(x)为固定state s=(i,a)的积分query吸收，L=|J_x∪F_s(x)|。若i∈J，J全未激活时i不可能激活，A_s=0。若i=o(x)，状态只能是initial query，故

    A_s(x)=α_x/(L+1)<=α_x/c_s(x)。

若i!=o且state可达，i>o。吸收事件包含于{owner及i active，J_x∪F_s全inactive}；正负角色两组不交，所以

    A_s(x)<=α_x∫p(1−p)^L dp
      =α_x/[(L+1)(L+2)]
      <=α_x/[c_s(x)(c_s(x)+1)]。

这里L>=b_i(x)+|F_s(x)|=c_s−1。证明只用事件包含：J-none已经暴露未来，不可在此误用entry与未来独立。

owner未覆盖x，且非owner state在其后，所以真实叶中的owner仍未覆盖。shared固定owner势边际正是owner时1/c_s、非owner时1/[c_s(c_s+1)]。因此

    0<=A_s(x)<=α_x ℓ_i(Y_i(a);x)。               (MARG-CAP)

真实旧背景b_i没有被丢掉。J_x负事件提供足够的额外指数来支付它。每个固定state的F从同一真实叶读取，不把等计数历史的续局强制相同。

## 一份whole-IC系数

令A_s=Σ_(R∪I^-)A_s(x)，D_s=u_i(Y_i(a))，w_s=A_s/D_s；D=0时A=0，取w=0。α<=1及边际非负给

    A_s<=Σ_(O∩a)ℓ_i(Y_i(a);x)<=ℓ_i(Y_i(a))<=D_s，
    0<=w_s<=ℓ_i(Y_i(a))/D_s<=1。                 (STATE-IC)

w是积分后的非负常数，只乘完整原IC D_s<=u_i，不对客户或p被积式分别重权。设L_i=Σ_(s角色i)w_s，κ^-=Σ_(x∈I^-)1/(c_x^0+1)，则

    Σ_s A_s=Σ_Rρ_x+κ^- <=Σ_i u_iL_i。           (JOINT-PAY)

R与I-query吸收确实由同一个w购买；actual I停止信用已精确定位，不得又全部叠加到query付款右端。

## 接half的位置和未付碰撞

取同一actual G运输的ρ=1−γ，则query目标为R−G+κ^-。令κ_i^-=Σ_(x∈I^-∩S_i)1/[c_x^0(c_x^0+1)]，总和κ^-。已有actual净库存η_i=u_i(I)+γ_i，总和W。若能共同选owner、γ、库存路由到

    u_iL_i<=η_i+κ_i^-                           (CAP-JOINT?)

或其总和版本，减同一κ^-后即给R−G<=W，闭合half。κ_i^-是actual势份额，I-query也增加恰同量源，不能叫额外免费福利。

CAP-JOINT尚未证明。多客户可在同一active role提出不同query动作；每state w<=1不能相加成row和<=1，一角色一次激活也不解决碰撞。本页新增的是一份实验中的R/I共同付款和逐角色I信用，未给剩余OPT槽库存的全局仲裁。

## 单一随机排列实现与自适应取消的边界

relay的owner阈值可给更简单的同世界耦合。取全角色iid连续U；对每个客户以U_o为阈值，角色j active当且仅当U_j>U_o，source始终存在。对I^-，若max_(j∈J)U_j>U_o，直接将unit信用记给其中U最高角色；否则走query。R的J为空，source每world始终存在。

每actual j得到信用的事件是j在{o}∪J最高，概率1/(c+1)；owner最高的query源概率也是1/(c+1)。因此没有额外priority或积分即可实现相同逐客户边际。不同owner共用U的跨客户相关性与共同p实验可以不同，本文用到的边际和线性付款不变。

固定nonowner终点必须有U_i>U_o>max_(J∪F_s)U；在这些L+2个角色的均匀排序中，i最高、owner第二，概率1/[(L+1)(L+2)]。这是同一MARG-CAP。路线可依完整world挑任何active未来coverer；有active F时不得提前吸收。每state固定真实F，所以事件包含仍成立。

对R，逐world总源为R。可以在固定actual Hall-A可行取消集内根据U选择γ(U)，逐world取消G；积分后的whole-IC系数仍是常数。但此时不能将MARG-CAP乘平均残源ρ_x=E(1−γ_x)：只保证未缩放上界A_s(x)<=ℓ_s(x)。取消与终点事件可相关。

`joint_source_net.md`的Hall-B取消含I-query平均库存κ，使用U前固定λ和条件删除λ/κ。它不是上述逐world R取消；让λ随U选后，E[(λ/κ)1_query]未必等于Eλ。两种机制各自合法，不将同一G相加，也不无证拼成一种自适应系统。
