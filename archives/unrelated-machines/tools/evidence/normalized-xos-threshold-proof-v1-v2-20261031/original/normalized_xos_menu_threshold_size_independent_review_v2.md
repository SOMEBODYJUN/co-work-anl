# 归一化XOS阈值菜单的最小规模：v2 Exact-first 独立审查

审查者：general_query_response_review。2026-10-18。

冻结前只读取 `normalized_xos_menu_threshold_size_exact_v2.md`，SHA-256 `6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d`。未读取旧v1作者Proof、其它review或新v2Proof；本轮不做软件枚举，不修改repo/Git/Work。

**明确结论：新Exact v2有效，无fatal。最小菜单数的有限组合恒等式、两处精确值及固定η的近中央二项式下界均成立。**

记d=floor(ηt)、k=max(1,ceil(d/η))。因0<η<1、t≥1，`0≤d<t`，且d/η≤t，故`1≤k≤t`。全资源宇宙固定为2t项。

## 1. 任一clause的正support必须至少k项

每clause非负、总量恰1，因此正support非空。d=0时k=1，立即成立。

设d≥1，某clause正support有L项。因f(B)是所有clause值之max，条件(ii)也逐一限制每clause在全部|B|≤d上的值≤η。

若L≤d，取B为整个正support，clause值1>η，矛盾。因此L>d。取正support中权最大的d项。其质量至少d/L：前d项平均不小于全部L项的平均1/L。由(ii)，

\[
\frac dL\le\eta,
\qquad L\ge\frac d\eta,
\qquad L\ge\left\lceil\frac d\eta\right\rceil=k.
\]

等号允许，不能错误改为L>d/η；这正是ηt为整数时锐例的重要边界。此论证覆盖无用clause，例如support大于t、从不使任何t集值1的clause，也不假设所有clauses都被某T调用。

## 2. 抽取k-subsets并均匀化，得到精确Θ恒等式

对给定可行菜单的每个clause s，从其正support任选k项F_s，改为F_s上均匀权1/k，其余0。新clause仍为有理、非负、总量1。

给任意t-subset T。原条件(i)给f(T)=1；因为菜单有限，必有实际clause s达到w_s(T)=1。其norm为1、所有权非负，所以T外权全零，即该clause的整个正support包含于T。于是F_s⊆T，新uniform clause在T上也为1。全部新clause总量1，故新max在T上恰1。

对任意|B|≤d，新clause值至多d/k≤η；d=0时为0。故(ii)也保持。相同F可去重，所得集合family大小≤原K，每个t-subset都包含其中某个k-subset。

因此Θ(2t,t,k)≤任何可行K。注意这里family的方向是“每t集**含**一个k集”，不是另一方向的covering design。

反过来，任意具有该包含性质的k-subset family，每F上取uniform 1/k；每t-set含某F给(i)，任一|B|≤d质量至多d/k给(ii)。有限family存在，例如全部k-subsets。取最小family即得可行菜单，故

\[
\boxed{K_{\min}=\Theta(2t,t,k).}
\]

重复indexed clauses或重复F不能降低最小值。转换可在给定显式菜单的规模内选support项并输出；但没有声称多项式找到最小family。该转换只保持(i)(ii)，不声称逐B保持整个原函数f或新f≤旧f；中间大小subset的值可能变化而不违反合同。

## 3. 计数下界及两个达到的精确参数

固定k-set F恰包含于

\[
\binom{2t-k}{t-k}
\]

个t-sets。全部t-sets共binom(2t,t)个，union bound/counting给任何覆盖family

\[
K\ge\frac{\binom{2t}{t}}{\binom{2t-k}{t-k}}.
\]

不需要假定这些覆盖族互不交，也不把非整数比值说成必能达到。因d≥1时k≥d+1、d=0时k=d+1=1，该下界至少不弱于使用r=d+1所得下界。

### d=0

k=1，family等同选一批points H⊆U，每个t-subset必须与H相交。等价于U\H没有t-subset，即`2t−|H|≤t−1`，所以|H|≥t+1。任取t+1个points就达到，故K_min=t+1。特别t=1始终d=0，K_min=2。

### ηt为正整数

此时d=ηt≥1、d/η=t，故k=t。一个t-subset包含另一个t-subset当且仅当两者相等。因此每个T本身都必须在family中，K_min=binom(2t,t)。所有t-subsets上的uniform 1/t clauses达到该值：对|B|≤d，值≤d/t=η，等号符合(ii)。

固定约分有理η=p/q，t取q的任意正倍数就有ηt为正整数；无遗漏t小/ηt=0例外，因为该分支明确要求正整数。

## 4. 固定η的4^t/poly界

设d≥1，令r=ηt−d∈[0,1)。max(1,...)已不影响k，由ceil/floor整数恒等式，

\[
k=\lceil t-r/\eta\rceil=t-\lfloor r/\eta\rfloor,
\qquad
t-k=\lfloor r/\eta\rfloor.
\]

由于r<1，`0≤t−k<1/η`，其整数值至多`c=ceil(1/η)−1`。当1/η本身为整数，此处严格小于仍正确给c而不是多放1。

记h=t−k≤c。则

\[
\binom{2t-k}{t-k}=\binom{t+h}{h}\le(2t)^h\le(2t)^c.
\]

包括h=0时左边1。再用中央二项式是2t行最大项、该行总和4^t，

\[
K\ge\frac{\binom{2t}{t}}{(2t)^c}
\ge\frac{4^t}{(2t+1)(2t)^c}.
\]

固定η使c为常数。简单取所有t-subsets的uniform 1/t clauses对任何η也可行，所以K_min≤binom(2t,t)；因此其最小数确实夹在中央二项式除固定多项式与中央二项式之间。d=0只在固定η下的有限多个小t出现，由上一节精确处理，不影响渐近结论。

## 5. Binary输入、显式输出与准确范围

一名additive玩家有2t个显式items，每个值1/t，则每t-set值恰1，所有|B|≤floor(ηt)值≤η。它可用O(t log(t+1))位列出；资源宇宙本来显式有2t项，不能把该source长度误作O(log t)。

任何同U、逐玩家、norm1显式max菜单只要保(i)(ii)，至少输出上述K个indexed clauses，长度至少Ω(K)。固定η时4^t除固定poly(t)增长快于任意(t log t)的固定次幂，因此相对该显式source是超多项式输出。没有推出`2^{Ω(源总位长)}`，也没有要求枚举到这个规模能在原输入时间poly完成。

η若随输入趋零，c可以随其编码变化而不再是固定常数；本证明不能据此宣称同一个fixed polynomial分母。Θ最小值只是有限数学量，不声称能poly计算。Uniform 1/k系数位长O(log t)，但重复/共享同一个数值不能抹掉显式K个state身份；隐式family/函数表示则属于另一个接口。

关键假设是同一U、非负且每clause**恰norm1**、有限explicit max、全部t-sets unit和全部≤d-sets tiny。允许辅助资源/玩家、全局耦合、只保可达bundles、放松unit completeness、未归一化或另证可处理的implicit表示时，本障碍不自动适用。尤其允许辅助资源的bonus保OPT normalization与本same-U阈值接口不同，不被此下界否定。

该定理没有提供normalized YES V=1 / NO V≤η的hardness源，也不是一般Santa Claus/UM困难性或全球归约障碍。

**最终冻结判断：v2 Exact全量词下有效，无fatal；未读任何作者Proof或其它review。**
