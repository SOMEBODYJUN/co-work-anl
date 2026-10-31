# 逐玩家归一化菜单的阈值保真规模：作者证明 v1

对应候选 `UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v1`。冻结 Exact 为 `normalized_xos_menu_threshold_size_exact_v1.md`，SHA256 `f10774625ddc30e09db98088a8c4cee579da027c8ae2512f6baba3ed5203bb44`。本证明另存，供完成 Exact-first 重构后读取。

记每个归一化 clause 的正支撑

    S_s={u∈U:w_{s,u}>0}。

零系数不属于正支撑；Σ_u w_{s,u}=1保证S_s非空。

## 1. 每个正支撑至少 r 个资源

若某s有|S_s|≤d，则令B=S_s。全部质量都在B内，故该clause在B上的值为1，从而f(B)≥1>η，与小集合条件矛盾。因此

    |S_s|≥d+1=r。

当d=0时同一结论只是S_s非空，仍正确，不暗加|S_s|≥2。

## 2. 每个 unit 集合必须包含一整个正支撑

对任意|T|=t，有限max的f(T)=1由某个clause s取得。因为全部w非负且总量恰1，

    Σ_{u∈T}w_{s,u}=1  iff  S_s⊆T。

因此全部binom(2t,t)个t-subsets都必须包含至少一个正支撑S_s。此处不依赖各个正系数的大小；它们可极不均匀。

若|S_s|=k≤t，该支撑可被恰binom(2t−k,t−k)个t-subsets包含；若k>t则一个也不能覆盖。对r≤k≤t，这个数至多binom(2t−r,t−r)，因为随着必须包含的集合变大，可包含它的t-subsets数不会增加。

对K个indexed clauses作覆盖计数（允许重复计数），于是

    binom(2t,t) ≤ K binom(2t−r,t−r)，

给出第一条下界。重复clauses只反复覆盖同一些T，不能减少所需indexed数；零系数已被正确排除在S_s外。

## 3. 二进制规模下界与端点

因1≤r≤t，所有下式分母均为正，且

    binom(2t,t)/binom(2t−r,t−r)
      = ∏_{j=0}^{r−1}(2t−j)/(t−j)
      ≥ ∏_{j=0}^{r−1}2
      = 2^r。

每个因子≥2，因为2t−j−2(t−j)=j≥0。r=1时比值恰2；t=1仍合法，因η<1给d=0、r=1。

若表示另列冗余全零clause，它从不取得unit值1，可先删除；上述覆盖必须由非零归一化clauses完成。总indexed数只会更大。

固定η>0时，r=⌊ηt⌋+1>ηt，故K≥2^r≥2^{ηt}。原一名additive玩家的2t个资源各值1/t，显式长度O(t log(t+1))；K的下界超过该长度的任意固定次幂。每个显式indexed clause至少需要一个记录，稀疏零省略和重复系数都不能以多项式输出写出如此多的clauses。没有声称对随t趋零的η仍有同一指数常数。

## 4. 非空性与准确转换范围

假设不是空泛不可满足：可以为每个t-subset T列一个clause，在T的各项设1/t、其它项设零。所得有限菜单满足

    f(B)=min(|B|/t,1)，

从而全部unit/tiny要求都成立，只是该显式菜单本来就大。这里不声称本构造达到所有η,t的下界。

下界排除的只是同一资源宇宙上的、对所有这些子集同时保真的逐玩家显式归一化。额外辅助资源/玩家、全局耦合、只在可达集合上保真、损失unit completeness、未归一化clauses或经另行证明可处理的隐式表示均不受本计数证明否定。也没有由此推出任何一般 Santa Claus 或 UM hardness。
