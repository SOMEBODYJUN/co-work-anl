# Boss7 degree-two tail：route5 门槛与固定根尾利润的比较

## 任务与范围

本边比较三个已声明正文：route5 的完整后继门槛接口、二元共享客户精确根后尾利润定理，以及该族完整均衡负驻留构造。严格保留各自对象的量词；本边是一个带条件的 proof-step contribution，`whole_result` 不填写，因为没有从固定根尾上包络推出 route5 的整条 branch-threshold/half 目标。

## route5 端的精确接口

对完整有序历史 $h$，下一位为 $i=|h|+1$。对每个合法动作 $A$，$R_h(A)$ 是强制当前选 $A$ 后、所有完整孩子子 SPE 可实现的**完整有序终局**集合；当前动作即使未在父节点最优，仍保留在集合中。定义

$$
L_h(A)=\min_{z\in R_h(A)}u_i(z),\qquad\Theta_h=\max_A L_h(A).
$$

若 $R(h,a)$ 是动作 $a$ 的孩子全集，则父终局全集为

$$
R(h)=igcup_a\{z\in R(h,a):u_i(z)\ge\Theta_h\}.
$$

选中枝的正确方向是 $u_i(z_h)\ge\Theta_h\ge L_h(a)$；不能把 $L_h(a)$ 写成至少 $\Theta_h$。沿实际完整 SPE 路径只有 $\sum_i\Theta_{h_i}\le W$。要得 half，还需另证某个最优带位置元组满足

$$
\sum_i L_{h_i}(T_i)\ge\operatorname{OPT}_m-W,
$$

再用 $L_h(T_i)\le\Theta_h$ 才闭合。已有粗分母只给 $L_{h_i}(T_i)\ge |T_i\setminus C(h_i)|/(m-i+1)$，且用的是此前前缀覆盖 $C(h_i)$，不能换成实际终局遗漏或跨互斥枝共享预算。

## 二元族的 exact root-tail 结果

设 $q\ge2$、$b\ge1$、$0\le a\le b$ 为整数；$X,Y$ 各含 $q$ 个标签，跨组边各有 $b$ 名单位客户，组内边各有 $a$ 名单位客户。固定任意根 $Z$，比较槽 $T=(T_1,\ldots,T_q)$ 可重复并可含 $Z$。令 $d_{ij}$ 是边两端标签在 $T$ 中的重数和，$e_{ij}=1$ 当且仅当边与 $Z$ 相接，$\mu_{ij}=b$（跨组）或 $a$（组内），零分子按零处理，则

$$
R_Z(T)=\sum_{ij}\mu_{ij}rac{d_{ij}}{d_{ij}+e_{ij}}.
$$

在 $(a,b)=(0,1)$ 端点，若比较支持两组各命中 $x,y\ge1$ 个、总 $s\le q$，命中跨边数为 $qs-xy\le(q-1)s+1\le q^2-q/2$；完整一组各一次取 $q^2-q/2$。在 $(a,b)=(1,1)$ 端点，非根顶点数 $n=2q-1$，$k$ 个非根支持的满份非根边数为 $f(k)=inom n2-inom{n-k}2$；根未入支持的根边贡献至多 $q/2$，含根支持严格低于 $f(q)+q/2$，故最大仍由 q 个不同非根标签取得。利用

$$
(a,b)=(b-a)(0,1)+a(1,1),\qquad b-a,a\ge0,
$$

逐比较线性合成并由对面组各一次取等，得到对每个根 $Z$ 与所有允许重复的 $T$：

$$
\max_T R_Z(T)=V_Z=qig[(q-1/2)b+(q-1)a/2ig]=qH.
$$

特别，$q=5$ 时为 $45b/2+10a$。取等支持为：$a=0$ 时整组支持；$0<a<b$ 时唯一对面整组；$a=b>0$ 时任意 q 个不同非根标签。

## 完整 SPE 构造与对齐边界

同一族存在一份覆盖全部有序历史的完整纯 SPE：任意根真实利润 $L=qb/2+(q-1)a$，其后 q 位各取相反组标签，尾位真实利润 $H=(q-1/2)b+(q-1)a/2$；根静态纯 best-response 门槛为 $	heta=L$，驻留差

$L-H=-(q-1)(b-a)/2$，当 $b>a$ 严格为负。构造实际福利

$$
W=q^2b+(q-1)(q+2)a/2
$$

且 $W=\operatorname{OPT}$。例如 $q=5,a=1,b=2$ 时 $L=9,H=11,V_Z=55$，驻留差为 $-2$。这些事实是同一真实完整策略的族内证据，而非 half 反例。

## 只能得到的局部 contribution

在固定根背景下，$R_Z(T)$ 是聚合的 q 槽比较利润；真实相反组尾是一个取等的 q 槽。它不等于 route5 的 $R(h)$（后者是完整终局集合），也没有证明任意 $T$ 是某个强制动作 $A$ 下的完整孩子子 SPE，更没有把 $R_Z(T)$ 的最大值转成当前玩家收益 $L_h(A)$ 的下界。构造的 $L=	heta$ 是静态纯查询值，不等同于 route5 的 $\Theta_h=\max_A\min_{z\in R_h(A)}u_i(z)$。

因此已付清的结果仅是：在精确二元族和指定完整 SPE 下，每个固定根的 q 槽联合利润精确上包络为 $V_Z=qH$，并且该上包络可与负驻留差及 $W=OPT$ 同时出现。仍未付的是 selected-branch threshold、互斥离轨枝的共同付款/粗分母、以及 $\sum_iL_{h_i}(T_i)\ge\operatorname{OPT}_m-W$；所以不能从局部 $R_Z\le V_Z$ 推出 half。

## 与旧边的 overlap 处置

旧 3B 边 `cag-degree-two-family-checks-background-five-exact-profit` 已把相同二元族在 $q=5$ 的 $R_Z\le V_Z$ 映射到 one-prefix-five 的独占收费变量，并保留“一般一背景五尾 $R_Z\le2V_Z$ 开放”。本边不重复该收费结论；仅复用三份当前正文中的固定根公式，新增 route5 $L_h/\Theta_h/R(h)$ 的接口对照与 half 缺口说明。两边 scopes 不冲突，也不把旧边的 context/checks 提升为 branch-threshold 或 half 证明。

## 审读与验证

三份 reading_refs 全文逐字读取，SHA 与任务声明一致；未运行策略枚举或收费程序，解析两端点和构造的通量/福利公式承担一般 q 结论。edge-bind 与 edge-check 仅验证结构、端点和证据绑定，不替代上述数学判断。
