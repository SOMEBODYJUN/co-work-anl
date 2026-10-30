---
id: "customer-attraction/static-cce-benchmarks-and-shrinking-certificates"
kind: "computation"
type_tag: "计算"
title: "静态CCE原始对偶基准与同策略缩小记录"
status: "complete"
truth_status: "五基准及十三客户另一个达到分布精确认证；70/13客户完整SPE严格分离；未认证规模最小性"
review_level: "两原程序原字节重跑全结构相同；不导入作者或规范模型的新Fraction审计"
scope: "三人共同目录单位客户有限实例；任意不对称相关静态CCE；含零客户、单人及重复覆盖/空主题软件边界"
summary: "最低CCE可修复16客户PNE例和472客户iid起始例，却不能修复同策略改重数后的70/13客户例；保存精确原始/对偶、完整SPE与十三客户另一15点有序达到分布。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/benchmark_regression.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/benchmark_regression.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_candidate.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_candidate.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_small.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_small_benchmark.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_small_benchmark.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cce_failure_small.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cone_attack.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cone_attack.py"
---

# 静态CCE原始对偶基准与同策略缩小记录

## 同名“静态比较”不能互换

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、单位提供者依次观察全部有序历史，客户价值在最终覆盖者间均分。纯SPE必须在全部离轨节点可信，保留重复选择、空主题、零客户及任意平局。静态CCE另要求任意有序终局分布 $\mu$ 满足每位玩家对每个固定主题的事前不盈利偏离；偏离冻结其他终局行动。

[十六客户PNE反例](../反例/三人顺序SPE低于全部静态纯Nash福利--反例.md)只有SPE福利15、全部静态PNE福利16；本批证明**同一实例的最低静态CCE福利其实小于15**。同样，472客户iid起始实例的最低静态CCE福利小于其最低纯SPE福利358。它们不能作为“低于全部CCE”的反例。后来沿完整策略锥改变客户重数，才得到[初次归一化分离](静态CCE福利分离的初次策略锥证据--计算.md)、70客户中间例及十三客户例。实例和量词都不能因共享程序或策略而合并。

本页保存六份源：五例原始/对偶回归、70与13客户完整策略、十三客户另一锐达到分布，以及两个发现/证书程序。它们是有限精确结果和工具，不是一般人数定理或六人half证明。

## 任意CCE下界与可达上界如何配合

令 $m$ 为玩家数，$k$ 为主题数；对静态终局 $z$，

$$
G_a(z)=\sum_i[u_i(z)-u_i(a,z_{-i})],\qquad
D_\lambda(z)=W(z)-\sum_a\lambda_aG_a(z),\quad\lambda_a\ge0.
$$

任意CCE都有 $\mathbb E G_a\ge0$，所以如果全部终局 $D_\lambda\ge\gamma$，就有 $\mathbb E W\ge\gamma$，不要求 $\mu$ 对称。一个客户在负载 $d$ 下对 $D_\lambda$ 的贡献是

$$
(1-\textstyle\sum_a\lambda_a)\mathbf1_{d>0}
+\lambda(B)\begin{cases}m,&d=0,\\(m+1)/(d+1),&d>0.\end{cases}\tag{1}
$$

这里 $B$ 是它喜欢的标签集合。该列只依赖终局计数 $q$，故可检查 $\binom{m+k-1}{k-1}$ 个计数列而覆盖全部 $k^m$ 个有序终局。原始分布则给每个计数一个总概率，再在该多重集的不同玩家排列间均匀抽取。玩家对称使个体CCE差为聚合差的 $1/m$，所以聚合非负足以证明**这个构造分布**是CCE。

此外，任一CCE均匀重排玩家身份后仍为CCE且福利期望不变，因此匿名博弈的最低CCE可在这种计数分布上求得。下界本身仍覆盖不对称CCE。由全列有理下界和达到分布匹配才能称精确最低值；一个数值LP的 `Optimal` 状态不承担这个结论。

## 五个基准的完整输入和锐值

前两个实例均为三人，兴趣mask第 $a$ 位对应主题 $a$，整数重数都是不同单位客户。

- 十六客户四主题：$\{2:1,3:2,7:2,10:3,12:3,13:5\}$。
- 472客户五主题：$\{2:38,4:38,8:38,15:50,16:74,23:78,27:78,29:78\}$。
- 零客户：三人、两标签、无客户。
- 单人：两不交主题，分别覆盖1和2名客户。
- 空/重复覆盖：三人、三标签覆盖分别为 $\varnothing,\{x\},\{x\}$；软件保留重复覆盖标签，集合目录可合并后两标签，福利和本边界结论相同。

原 `benchmark_regression.json` 的全部五例现均以不导入规范求解器的有序历史递推独立核对：

| 基准 | 最低纯SPE福利 | 最低静态CCE福利 | OPT | 静态计数/有序终局 |
|---|---:|---:|---:|---:|
| 十六客户PNE例 | 15 | $72669/5132$ | 16 | 20 / 64 |
| 472客户iid起始例 | 358 | $20980/59$ | 434 | 35 / 125 |
| 零客户 | 0 | 0 | 0 | 4 / 8 |
| 单人 | 2 | 2 | 2 | 2 / 2 |
| 空/重复覆盖 | 1 | 1 | 1 | 10 / 27 |

前两行的最低CCE分别比最低SPE低 $4311/5132$、$142/59$。故在这两个具体实例，下面明确构造的CCE能支付任意纯SPE的福利替换；这个有限事实不证明普遍桥。零客户不使用效率比，它的两标签也都为空覆盖，合并不影响零等式；单人没有竞争者。软件重复覆盖边界没有悄改原数学目录。

### 十六客户原始/对偶

非负乘子为 $\lambda=(1001,3223,1289,1527)/10264$。达到分布如下，每行概率均匀分到该多重集的不同排列：

| 多重集 | 总概率 |
|---|---:|
| 333 | $3423/10264$ |
| 123 | $504/1283$ |
| 111 | $21/5132$ |
| 013 | $1281/5132$ |
| 000 | $205/10264$ |

共15个有序支持点，全部12项个体CCE差均为0。20个计数对偶列均至少 $72669/5132$，最小差0；上述分布福利恰为该数。它与旧PNE证明相容，因为CCE允许相关混合，不能把“所有PNE福利16”改写成“所有CCE福利16”。

### 472客户原始/对偶

取 $\lambda^0=(0,421/944,23/944,0,75/236)$，达到分布为

| 多重集 | 总概率 |
|---|---:|
| 044 | $1275/2183$ |
| 004 | $837/2183$ |
| 000 | $71/2183$ |

共7个有序支持点，全部15项个体CCE差中，对主题0的三项均为12，其余均0。全部35个计数列的下界为 $20980/59$，最小对偶差0，分布福利匹配。这里没有重新认证该源附带的iid $q,Z,\alpha$；那些属于另一个静态分布对象。起始完整31动作已另在本轮按此472客户向量核为SPE，实际福利358。

三个边界分布和乘子也全部保留：零客户集中于111（第二标签重复三次），乘子全0；单人集中于主题1，乘子 $(0,1)$，聚合差 $(1,0)$；空/重复覆盖集中于222，乘子 $(0,1/3,0)$，聚合差 $(1,0,0)$。各自达到表中锐值，零客户的四个计数列仍完整被检查。

## 同策略锥缩小的两个有限证书

70客户 `cce_failure_candidate.json` 和13客户 `cce_failure_small.json` 使用与[初次策略锥证据](静态CCE福利分离的初次策略锥证据--计算.md)完全相同的31动作：根0；第二人在首0至3后选4、首4后选0；末位两个先前行动均非4时选4，04/40时选4，14/34/41/43/44时选2，24/42时选3。规则穷尽全部有序历史；本轮逐历史直接比对三份完整策略相同。

它们的单位客户向量不同：

| mask / 兴趣 | 70客户例 | 13客户例 |
|---|---:|---:|
| 2 / $\{1\}$ | 13 | 2 |
| 4 / $\{2\}$ | 4 | 1 |
| 8 / $\{3\}$ | 2 | 1 |
| 15 / $\{0,1,2,3\}$ | 8 | 2 |
| 16 / $\{4\}$ | 12 | 4 |
| 24 / $\{3,4\}$ | 4 | 0 |
| 29 / $\{0,2,3,4\}$ | 27 | 3 |

每个实例都核全部31节点、155项含自身比较，最小SPE差0；实际路径均044。70客户收益 $(17,17,17)$，$W=51$、$\operatorname{OPT}_3=68$；13客户收益 $(3,3,3)$，$W=9$、$\operatorname{OPT}_3=12$。两个都是原模型完整SPE，没有用“同一策略”代替另一客户向量上的激励检查。

它们都保留同一个旧乘子 $\lambda^0$。逐个有序终局的精确最小对偶列分别为

$$
\begin{array}{c|c|c}
&\min_zD_{\lambda^0}(z)&\min_zD_{\lambda^0}(z)-W(\sigma)\\\hline
70\text{客户}&3070/59&61/59\\
13\text{客户}&8621/944&125/944
\end{array}
$$

两者都严格大于指定SPE福利，因此都反驳静态CCE福利替换。它们仍满足half：$2W-\operatorname{OPT}_3$ 分别为34和6。没有给70客户例匹配原始分布，不能称 $3070/59$ 为其最低CCE锐值。

13客户源还记录 `solver_status` 为HiGHS最优、`total_clients=13`、`constraint_scales=[6,2832]`。本轮独立确认客户数13，并对全部31个非空单客户兴趣类型重构SPE系数和 $D_{\lambda^0}-W(\sigma)$ 系数的公分母，恰为6与2832；这保存了整数化元数据的含义。来源没有附出证明全实例/全策略最小客户数的生成程序或对偶，数值最优状态不认证目录或客户数最小性。

后续正式十三客户例换用简单乘子 $(0,1/5,1/5,1/5,2/5)$ 得稍强下界 $137/15$，再以锐乘子确定 $2785/297$。所以
$8621/944<137/15<2785/297$ 是**同实例不同证书**，不能把旧缩小JSON写成已经内含后两证书。

## 十三客户的另一个锐达到分布

`cce_failure_small_benchmark.json` 给相同13客户输入、同一个锐乘子
$\lambda^*=(0,38/99,1/11,1/11,28/99)$，却给出不同于已清洗正式证书的原始分布：

| 多重集 | 本源总概率 |
|---|---:|
| 334 | $4/33$ |
| 224 | $4/33$ |
| 144 | $20/297$ |
| 044 | $673/1188$ |
| 004 | $49/396$ |

均匀展开后是15个有序支持点，概率和1，15项个体CCE差均为 $(277/297,0,0,0,0)$ 按玩家重复，期望福利 $2785/297$；35个计数/125个有序对偶列下界匹配。旧正式证书另用014、044、004、224、334组合并展开成18点，也达到相同锐值。本源是另一可行达到分布，既没有推翻旧分布，也不能把两份概率逐行相同地合并。

## 两个程序到底做什么

`probe.py` 递归生成全部静态计数，按式(1)构造聚合固定偏离差，使用SciPy/HiGHS求最低福利LP；将概率、非负乘子和常数用分母至多 $10^7$ 的Fraction重构后，显式检查概率和1、非负、全部原始差、全部对偶列及原始值等于对偶值，才设置 `exact_optimal=true`。它另调用规范全集纯SPE求解器输出最低SPE，枚举支持输出OPT；两种输出不是同一个LP。该程序检查上面五个固定实例，没有穷尽任意实例。

`cone_attack.py` 固定一份完整有序策略，枚举全部非空客户兴趣类型；每个节点每个非自身动作都构造沿**原策略真实后继**的SPE行。固定非负CCE乘子，在线性约束“全部SPE行非负、重数非负、实际 $W=1$、每个静态对偶列至少 $\gamma$”下最大化 $\gamma$。数值重数经有理化后，程序重算全部SPE差、全部真实静态列、福利与间隙，仅严格有理分离才返回 `exact_counterexample`。候选不需在重构后仍恰归一化到1，证明依靠重算的严格间隙。

若未分离，程序把数值重数乘 $10^6$ 后非负取整，仅用于下一轮重新取得静态对偶；它没有用这些取整数冒充当前已验证证书。它只启动472客户完整策略与一个规范求解器选择的PNE来源最差SPE策略，每条固定策略默认至多8轮；不枚举所有完整策略。起始 `benchmark` 的 `exact_optimal` 标志未被调用处强制使用，不过最终严格候选仍独立复核全部有理列，所以不靠种子LP的浮点状态成立。

## 可复现依赖、实读和关系

独立证据目录 [continuation-cce-benchmarks](../../tools/evidence/continuation-cce-benchmarks/README.md)保留六主源和七份运行/比较依赖的原字节，原相对树 `source/` 保证原 `ROOT=parents[5]` 与导入路径正常；清单逐文件列完整冻结提交、原路径、源ID和SHA。规范包四文件是运行依赖，本六源批不再完成它们；472客户源由另一批处理，这里仅保留精确输入。初次JSON是本轮首批已经完成的比较依赖。

两原程序本轮真实复跑，`probe-replay.json` 与五基准冻结JSON完整结构相同，`cone-replay.json` 与初次交替输出完整结构相同。保存的环境为Python及NumPy/SciPy具体版本，发现程序需要这些数值库。

[新增标准库审计](../../tools/evidence/continuation-cce-benchmarks/audit_benchmarks.py)不导入作者脚本、规范模型、规范求解器或首批审计。它从兴趣重数逐客户计算收益、展开原始分布全部有序排列、检查每个玩家每个固定偏离、枚举每个有序对偶列；独立按**完整有序历史**作集合值递推：每个子节点的可实现终局独立选取，当前动作可实现某终局当且仅当其收益不低于各动作子博弈最差当前收益的最大值。此有限递推核五基准和13客户的最低SPE，没有把相同计数历史绑定为单一续局。完整输出见[独立核验](../../tools/evidence/continuation-cce-benchmarks/independent-replay.json)，包含全部CCE个体差、静态列、根SPE终局与70/13客户逐历史收益表。本轮是原实现重放加新的内部独立实现，未新增外部同行审查。

实读比较了全部六主源、四份规范包依赖、两个起始输入、前批初次JSON、已清洗PNE反例/核验资源、CCE反例/核验资源和强弱iid桥对象。没有发现推翻十三客户分离或其锐值的后续纠错；区别是本源更早的旧对偶下界和另一个原始最优点。

供第三阶段：五回归数据与原始/对偶条件共同认证具体最低CCE；规范求解器及本轮有序递推是不同实现的有限最低SPE核验；两个发现程序实现固定输入/固定策略的探索，不是一般定理；同完整策略但不同客户向量连接初次、70、13客户的构造复用与缩小来源链；新15点和旧18点分布是同一LP的不同达到解。真正静态安全值、真实查询UP和六人half没有被这些有限基准判定，本批不导入旧图、不认证新颖性或规模最小性。
