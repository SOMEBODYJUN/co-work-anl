# 自由分数几何均值对偶：盲核范围与查重停界

2026-10-24。先独立重构下列公式，再读旧稿；本文件不是新数学工具或 Q-CAG-HALF 进展。

设共同有限目录为 S，`b_x>=0`、`s>=0`，`a_x=b_x+1>0`。对主题分布 q 写客户边际 `q_x=Pr_(T~q)(x in T)`，定义

    Lambda_s(b)=min_q max_T sum_(x in T) 1/(a_x+s q_x).

准确凸对偶为

    Lambda_s(b)=max_(p in Delta(S),r>=0)
      {sum_x [2 sqrt(p_x r_x)-a_x r_x]
       -s max_T sum_(x in T) r_x}.

理由：原式先用查询分布 p 线性化 max_T。关于 q 的函数连续凸、关于 p 线性，两个单纯形紧凸，故可换 min/max。逐坐标恒等式 `p/(a+s q)=max_(r>=0)[2sqrt(pr)-(a+s q)r]` 的最大点是 `r=p/(a+s q)^2`。任意 `r_x>a_x^-2` 可截回 `a_x^-2`，因为此区间导数 `sqrt(p_x/r_x)-a_x-sq_x<=0`；截断同时对所有 p,q 有效，故第二次交换可在两个紧凸域上执行。关于 (p,r) 的几何均值目标联合凹；对 q 仿射。最后极小化 q 给 `-s max_T r(T)`。零边际 p_x=0 时取 r_x=0，空主题及零客户均覆盖。

KKT 中 p 支持原最优 q 的活跃最大查询。s>0 时，q 支持最大化 `sum_(x in T) r_x` 的主题，并有 `r_x=p_x/(a_x+s q_x)^2`。s=0 时 q 完全无约束，不应删去因子 s 后仍强加此支持条件。

对任意 m 个比较主题的并集 O，`|O|<=(m+s)Lambda_s(0)` 的静态代数正确。一般非空背景则不能原样写此式：单客户、唯一主题、m=1、s=0、b=1 已给 Lambda=1/2、|O|=1。对最优 q*，一个正确通用版本为

    |O| <= (m+s)Lambda_s(b)
           +sum_x b_x/(b_x+1+s q*_x).

逐客户使用 `1_(d_x>0)<=(d_x+b_x+s q*_x)/(b_x+1+s q*_x)` 即得；若只对 O 求和，亦可保留更小的背景项。这一背景项不能凭空删除。

查重结论：该对象是旧 `t_(s+1)(b)` 的实质量写法；整数 s 时完全同一对象。定义、minimax、KKT、静态最优覆盖比较已有

- `research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md` §§1、2、4；
- 完整几何均值对偶及齐次商式已有 `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/relay/endogenous_fractional_transport.md` §2。

因此本轮独立重构只核对旧工具和退化范围，不登记新结果，不做数值重复。自由分数值的动态 SPE 支付仍未证明；这些静态公式不能推出 W 的下界。
