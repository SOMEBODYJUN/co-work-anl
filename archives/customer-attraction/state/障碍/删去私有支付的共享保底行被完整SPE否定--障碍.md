---
id: customer-attraction/shared-only-floor-after-dropping-private-payments-full-SPE-failure
kind: obstruction
type_tag: 障碍
title: 删去私有支付的共享保底行被完整SPE否定
status: complete-original-model-counterexample-to-auxiliary-row; not-a-half-counterexample
summary: 原mixed_private_probe把singleton列的整个M置零，不能由总利润混合保底推出。18单位/7极大/6人、全历史恒选0给共享行−6B_t，且符合其首个singles/route/最小省略case；实际W12、OPT18仍满足half。
source_refs:
  - source:3821a7c7b30610dceea3e0affadfb75047877c9d:intake/reviewed-local-20261029/raw/research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/mixed_private_probe.py
  - clean:3feb8cff1b0cd00ad1d8
---

## 被否定的具体行

原2950B程序的path_rows先给六个M：当客户极大归属|I|≥2时取s_t−B_t，singleton列却将**整个行系数设为0**。B=(1/21,2/37,1/16,2/27,1/11,7/72)。所以它的全局合同是“当前角色从共享客户得到的利润≥B_t乘共享客户总数”，不含私有利润也不含私有下界。

[正确全历史混合保底](../引理/混合私有共享路由保底--引理.md)给的是总利润u_t≥c/6+P/12+B_tV；它没有把实际私有利润限定恰P/12。不能从一个总利润下界分别消掉私有实际支付和私有预算后保留共享项。以下见证在程序真正测试的第一个case内否定该共享行，无需原LP或新的IC扫描。

## 18个单位客户、全部七个极大主题

六位单位提供者，七个共同标签0,…,6。12名不同客户仅喜欢0；另外六名单位客户x₁,…,x₆，其中标签j=1,…,6覆盖{x_j,x_{j+1}}，循环令x₇=x₁。客户兴趣型就是{0}:12及{1,2},{2,3},{3,4},{4,5},{5,6},{6,1}各1。

全部七个覆盖非空且互异。0的12客户与环客户不交；其余六覆盖大小都为2且互不包含，所以恰有七个不同包含极大覆盖。核心为空，私有块X₀大小12，其余X_j大小0；共享V=6。

完整纯策略σ在**每个**长度t<6的有序历史都选0。历史允许任意重复、离轨和平局；若此前a次选0，则当前遵循的真实终局共有a+6−t个0，当前所得
\[
\frac{12}{a+6-t}\ge2,\qquad 0\le a\le t.
\]
若当前改任何j≠0，其后仍按同一σ全选0。j最多有两名客户，每名终局分账至多1，故当前偏离利润≤2。此论证对每个有序历史和每个合法行动同时成立；由逐子局当前最优的有限归纳，σ是完整纯SPE，不只是actual路径证书。0自身偏离相同，全部等号均保合法平局。

实际路径0⁶，六人各得2，W=12。B₀、B₁、B₃、B₅已覆盖全部18客户，补两个重复0成六槽，所以OPT₆=18；上界是全客户数，故确为最优。2W−OPT=6>0，这不是原half反例。

## 在源实际case里的负行

actual前五路由是(0,0,0,0,0)，末位也是B₀。六个共享客户actual会员E=0，J=0，所以每位共享利润都是0，原选择性行总和恰
\[
\widetilde M_t=0-6B_t=-6B_t<0\quad(t=0,\ldots,5).
\]
这个输入仅私有0为正，完全属于source main第一组singles={0,6}；允许的X₆只需非负，不要求正。源码omit6确为最小私有块，六条|X_j|−|X₆|≥0全部成立；路由00000也是真实合法容器路由。因此不是利用主程序未测的私有块数或错误省略条件来制造反例。

正确完整M在此例为u_t−P/12−B_tV=1−6B_t≥1−7/12=5/12>0。私有利润2大于预算P/12=1，正是不能按组拆掉利润的具体原因。原Q、尾税和排序等其它合法行不受这个否定；若某证书把所有这六个M权置0，仍可尝试由其它真实行证明结论，但不能将正权M免费当SPE约束。

完整参数和纸面证明见[18客户定义](../../tools/evidence/reviewed-local-remaining-search-and-private-extensions-five-primary/analytic-shared-row-failure-instance.json)。此处新的是对源字面辅助行的明确处置，不授新颖性；本轮0原程序/收益/IC/LP/新checker运行，不伪造有限全集执行。程序其它合同见[私有扩域与分组资源](../程序/私有列扩域与十五组对称乘子的真实合同--程序.md)。
