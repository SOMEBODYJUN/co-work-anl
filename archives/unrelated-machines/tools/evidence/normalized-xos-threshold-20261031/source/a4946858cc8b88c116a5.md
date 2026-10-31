# 归一化菜单阈值保真的最小状态数：冻结 Exact v2

ID / Version: UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2。

这是v1同对象的强化结论：给出最小indexed clause数的精确有限组合表示，并在ηt为正整数时给达到的锐界。不改变同资源宇宙、全部subset保真的接口；不是一般Santa Claus/UM困难性或全局归约障碍。仅Exact，供独立重构，另冻Proof不提供给初审者。

## Objects / Domain / Quantifiers / Definitions

固定有理η∈(0,1)，整数t≥1，显式资源宇宙U有2t项；d=floor(ηt)，k=max{1,ceil(d/η)}，故1≤k≤t，0≤d<t。可将η与t作为明确参数给定作有限陈述，固定η的渐近结论另列。

显式K≥1个indexed非负有理加性clauses w_s，逐clause Σ_{u∈U}w_su=1；允许零系数和重复indexed clauses。f(B)=max_s Σ_{u∈B}w_su。要求：

(i) 所有|T|=t的子集有f(T)=1；
(ii) 所有|B|≤d的子集有f(B)≤η。

对该固定η,t，K_min为满足(i)(ii)的显式indexed菜单最小clause数。它是有限数学量，不声明能poly计算该数。

定义 Θ(2t,t,k)为最小family F⊆binom(U,k)的大小，使每个t-subset T至少包含某个F∈family，即F⊆T。这是“每个t集含一个k集”的定义；不混同另一方向的covering design。重复F不降低最小值。

## Exact Statement / Conclusion

1. K_min = Θ(2t,t,k)。任意满足域的菜单，其每clause正support大小至少k。存在一份同资源宇宙菜单，最多使用原K个、每个在k资源上均匀权1/k的clauses，并仍满足(i)(ii)。相反任意达到该Θ的family，给其每k集均匀权1/k就满足(i)(ii)。

2. 因而任意满足域的K满足

   K ≥ binom(2t,t) / binom(2t−k,t−k)。

   这强化v1的r=d+1下界，不称该比值对全部参数都达到。

3. 若d=0，则k=1且K_min=t+1，此界达到。包括t=1，η∈(0,1)时K_min=2。

4. 若ηt为正整数，则k=t且K_min=binom(2t,t)，此界由所有t-subsets的均匀clauses达到。η有理固定，t取其约分后分母的任意正倍数即有此锐界；不以省略state索引或共享相同数值代替显式输出。

5. 固定η，令c=ceil(1/η)−1。当d≥1，0≤t−k≤c，故

   K ≥ binom(2t,t)/(2t)^c ≥ 4^t / ((2t+1)(2t)^c)。

   与一名additive玩家2t个各值1/t的显式源输入O(t log(t+1))相比，任何保持(i)(ii)的此类显式逐玩家归一化都需超多项式输出。这里不声称2^{Ω(源总位长)}，不声称η随输入趋零仍有同一常数c。

## Dependencies / Evidence / Limits / Status

原v1来源另冻，不覆盖。v2依赖同一明示norm1/非负/有限explicit max与全subset阈值量词；不依赖有限枚举或外部hardness。Proof拟独立审查，Exact本身未由保存升级真值；软件/外审/全球新颖性未认证。

只排除同U、逐玩家、保所有unit/tiny子集的显式norm1 shortcut。允许辅助资源/玩家、全局耦合、仅特定可达分配保真、unit completeness损失、未归一化clauses或另证可处理的隐式表示，都不在否定范围内。定理不供应normalized YES V1 / NO V≤η的hardness源。
