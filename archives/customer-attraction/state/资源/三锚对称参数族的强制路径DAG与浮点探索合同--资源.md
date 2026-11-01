---
id: customer-attraction/three-anchor-symmetric-parameter-family-forced-path-DAG-and-floating-discovery
kind: resource
type_tag: 资源
title: 三锚对称参数族的强制路径DAG与浮点探索合同
status: four-whole-primary-sources-read;required-helper-same-SHA-full-read;zero-new-search
summary: 保存k2r3的65聚合参数列、x1/a及core箱约束、强制路径压缩DAG的全历史展开义、两种目标/重置过程和三报告全部权重；0.5无动作/弧/矩阵及精确核，不证明全族半屏障。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/anchor_general_cones.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/general_anchor_k2r3.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/general_anchor_k2r3_jitter.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/general_anchor_k2r3_seeded.json
---

# 三锚对称参数族的强制路径DAG与浮点探索合同

6482B程序及182/1195/1450B三报告共9309B全文实读、核原size/SHA256/Git blob。动态加载的6427B旧cone_search原件此前正常show已取，本批同SHA又全文读；实际只用其comp，不调用旧Search/main。原探索未被本次重跑；完整数学域、源内条件性可实现机制和有限浮点记录分别保存。

## 65列不是65个客户：每组等权的参数族

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，k组、r个锚点，p=k(r+2)+r标签、m=k+r位单位玩家。第i组标签按(C_i,A_i,B_(i,0),…,B_(i,r−1))排列，最后r标签D₀…D_(r−1)。

每组一个私有客户类型X_i，恰喜欢该组全部r+2标签；另H_i只喜欢A_i。默认把所有k个X_i聚成一列、各自同权x，把所有k个H_i聚成另一列、各自同权a。它们是k个**不同兴趣类型**的共同参数，不是把k名不同客户当一个加权玩家，x=1也不意味着私有客户总量1。

公共core遍历2r位的全部非空集合S。前r位b表示同时喜欢所有组的B_(i,b)，后r位d表示喜欢锚D_d；每个S独立有质量c_S≥0。公共客户不喜欢C_i/A_i，跨组共享同一公共块，并非Cartesian分量。默认总参数数
\[
n=2+(2^{2r}-1),
\]
展开兴趣类型有2k+2^(2r)−1个。三报告均明确k=2,r=3，故p13、m5、n65、实际67个类型；第0/1列为x/a，第j≥2列对应core整数j−1。不是任意13主题的8191种兴趣锥。

class另支持individual=True，把X_i/H_i各自独立成2k列，但main没有CLI选择它，当前三报告的65项不能归该模式。main始终固定目标路径
\[
(C_0,\ldots,C_{k-1},D_0,\ldots,D_{r-1}).\tag{1}
\]
它不计算OPT或覆盖比。路径覆盖为kx加所有带至少一D位的公共质量，遗漏所有H_i和只含B位的公共core；因此“最高a/x”本来就不是直接的福利比。

## 缩放收益表与浮点set-valued BI

令s=lcm(1,…,m)。对每层t枚举全部p维非负计数向量Σq=t，末层为所有m槽终局。每个非零客户分母d在1…m，故s/d为整数；零分母先写0，再乘主题会员位。raw表在各聚合列内求和，得到int32的`pay[leaf,action,column]`，是客户利润的s倍。k2r3时s60，私有聚合列按两不同X/H类型的贡献相加。

solve(w)用pay·w得到浮点收益。孩子集合起自各终局，非终局floor=max_a min_(z∈child_a)u_a(z)，保当前收益≥floor−10⁻⁷的孩子终局并去重，故是带绝对容差的全集合BI探索。w可为上一步浮点LP向量乘120，不能因为pay基础是整数就说整个过程精确；容差使用的是缩放s后的收益单位。

按计数缓存终局集合本身不限制所有可实现策略为Markov；当前代码随后另外选择一种DAG共享形式。任意CLI规模还受实际int32实现约束，本源没有一般位复杂度或整数安全证明；这里三报告的固定尺度60不承担更大m的实现认证。

## 强制路径DAG如何覆盖全部有序历史

cone从root指定目标终局t为(1)的计数，递归key=(计数状态i,目标终局t,forced)。forced为真时，选择(1)在该计数前缀规定的行动，不要求该目标已是当前w的BI结果。forced为假时，从能实现t、当前收益达到floor容差的行动中随机挑选。

对每个替代b，指定其孩子目标s：b为当前规定行动时s=t；否则在该孩子out全部终局中挑使当前b收益最低（容差10⁻⁷）的终局，再递归。它不是从所有非极小可信菜单均匀取样；与[另一可信菜单搜索](均匀真实组合强接口的完整策略锥搜索合同--资源.md)的三模式不同。

每个非自身孩子都加入
\[
\operatorname{pay}(t,a)-\operatorname{pay}(s,b)\ge0.\tag{2}
\]
零行省去，非零int32向量按bytes去重。seen共享同key，forced真假分开；同计数的在轨与离轨节点可选择不同路线。由于每一步深度增加，若保留所有孩子指向，可把DAG展开成完整有序历史策略：每次沿该节点预先指定的孩子目标继续，(2)即每个真实替代的利润差。这样**精确非负w与全部(2)精确可行**便足以使展开策略为完整SPE，即使原初w上的强制路径并非SPE。

这解释source的“forced path initially may fail但LP能约束它”，不把初始seed当成一份已认证SPE。DAG共享也只采样全部完整策略中的一部分，不代表对所有策略找遍。

报告policy_objects是len(routes)，routes仅记key到当前行动a，不能当完整历史数。p13/m5的完整非终局有序域有1+13+13²+13³+13⁴=30941节点；报告5646/5664为共享对象数。rows11504/11436是去重系数行数，不是原有序IC数。报告未存动作、孩子目标弧、rows矩阵或DAG，本次无法仅凭这些计数重建其完整policy证书。

## LP边界、两种目标及继续机制

每步LP用A_ub=−rows、b0，变量边界
\[
x=1,\qquad0\le a\le5,\qquad0\le c_S\le50.\tag{3}
\]
这是每组私有x归一，不是W=1或客户总质量1。默认目标min(−a)；step≡1 mod3时公共列另加10⁻⁵(rng.random()−1/2)，所以那些步最小化−a加微小core成本，**并非每步都纯最大化a**。它没有给恢复的有理点、整数客户或精确对偶。

best初0，只有res.success且a>best+10⁻⁸才记录一个改进：step、a、完整weights、rows数、policy_objects数、min_slack=min(rows·res.x)。它不要求精确非负或验证完整展开，tiny负weights/负slack仍可进入记录。没有每步状态/失败计数，因此max_a0、records空不等所有LP都不可行，也不等数学最优为0；0.5不证明任何全族a≤x/2。

当前默认k2/r3/steps150/seed610215。known_seed的非零列为x2、a1、core D₀-only 1、B₀+D₀ 1、D₁-only 2、D₂-only 2。每7步重置该seed乘60；非第0步再对2…7次随机公共列加1…9。LP成功后w=res.x·120，失败则某公共列加1…3。当前源码同时含known_seed和上述目标抖动，文件名jitter/seeded不对应两个不同CLI开关；源没有--jitter或--individual等参数。

## 三报告全部字段及完整65项权重的无损表示

三报告各7顶层字段，status均为`floating complete-policy cone discovery; no universal conclusion`：

| 原文件/bytes | k,r | steps | max_a | records数 | seconds |
|---|---|---:|---:|---:|---:|
|general_anchor_k2r3.json /182|2,3|100|0|0|102.98363947868347|
|…_jitter.json /1195|2,3|100|0.5|1|283.7083716392517|
|…_seeded.json /1450|2,3|150|0.5|1|440.13927841186523|

两个record均step0、a0.5、weights长65；jitter的rows11504、policy_objects5646、min_slack0.0；seeded的rows11436、policy_objects5664、min_slack=`-1.2082005066650824e-13`。完整数组可由下表、随后负零索引及“其余为正0.0”无损还原；不是将小数清成有理数：

| index | jitter token | seeded token |
|---:|---|---|
|0|1.0|1.0|
|1|0.5|0.5|
|3|0.5|0.500000000000001|
|4|-0.0|-1.0658141036401502e-15|
|5|0.5|0.4999999999999994|
|9|0.5|0.4999999999999994|
|10|0.5|0.49999999999999983|
|14|0.0|8.959292031117775e-16|
|15|0.0|2.404370230721564e-16|
|17|1.0|1.0|
|19|-0.0|1.0658141036401502e-15|
|21|0.0|-9.655074490801973e-16|
|23|0.0|-1.9475412320929455e-16|
|25|-0.0|1.519763383529084e-16|
|33|1.0|1.0000000000000002|
|35|-0.0|-1.4210854715202005e-15|
|37|-0.0|1.4210854715202005e-15|

jitter负零索引完整为{4,8,11,13,16,19,25,29,31,35,37,39,41,43,47,49,51,53}；seeded为{16,27,39,41,51,57}。取0…64域，先用表，再给未列出的这些负零，其余0.0，便完整保130个数值token。原JSON及全部indexed-token阅读另存证据，未丢tiny负数或把−0改正0。

seeded包含负坐标且最小slack为负，不能直接称精确可行；jitter虽只有简单0/0.5/1及float slack0，也缺完整动作/弧/矩阵。限分母或舍小量后仍需该原policy的精确证书才可认证SPE，本批没有机械重跑来制造它。

## steps、版本与“250次”准确边界

main每step做一次LP，但每5步的中途覆写使用steps=当前0基step索引（此时已经做step+1次），结束后覆写steps=args.steps。两种快照的status/字段相同，没有completion标志。因此仅看100/150不能区分最终记录还是更长调用的中途快照，也无seed/argv/源码SHA/solver版本/动作图绑定。三文件字段形状均与当前程序相容，不猜它们因何得到不同结果或认为标签足以重建旧版本。

复制主稿所述250次专指后两份100+150的历史说法，并非把前182B再加成一个本批新350次实验，也没有证明这些是250次成功/精确可行LP。当前全部原值及seconds保留，但无每步日志可验实际求解次数/失败。本源没有普遍半屏障或全族最优证书，改进记录也不是所有终点列表。

## 比较、闭包与当前执行

与[两尾复制路径障碍](../障碍/两尾公共锚点族的旧组逃生与复制路径障碍--障碍.md)相比，那是r2固定X6/H4的全k严格偏离；本三锚r3的受限参数浮点best不反推整个族a≤x/2，亦不与k1的a/x2/3矛盾。与[两尾Cartesian FILTER](../定理/任意背景两尾产品门槛与可信叶过滤--定理.md)相比，本家族公共客户跨组，不满足分量独立；r3也不能套两剩余的θ可加。

[完整策略客户锥](../定理/固定完整策略的客户重数锥--定理.md)是全部兴趣类型/给定完整动作图的精确表示；这里另外限制公共兴趣族、私有等权、箱界和共享DAG，且未导出动作图。条件性锥语义可由展开证明，具体浮点记录仍不是规范证书。旧同B复制障碍不覆盖本全r参数族；有限阴性不能扩为一般SPE或half。

primary用parents[5]定位ROOT，再importlib执行旧R-ffea…/credible_counterexample/cone_search.py；实际只调用comp枚举弱组合。helper只有标准库/numpy/scipy，main有guard，不调用其Search/opt/旧扫描。原树保6482及6427完整路径；本批只AST读取，0import/BI/LP/随机计划/策略展开/IC执行。output是必填Path，每5步及最终直接覆盖，不建父目录或独占；stdout只进度BEST/STEP，未保全这些旧日志也不补造。

完整7源claim8d9726f7…pushed/synced、本4 Boss4 owner/sourceSHA/normal-show、helper早先原show及逐源核验见[证据](../../tools/evidence/general-anchor-cone-search-primary/README.md)。没有新盲审/外审/新颖性、全族上界或一般half结论；空/重复同覆盖/零客户与离轨平局在一般模型不删除，源内x=1/参数族等限制如实保留，第三阶段不建图。
