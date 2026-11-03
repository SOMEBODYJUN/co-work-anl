---
id: "unrelated-machines/arbitrary-sink-cover-mw-frozen-audit-replay"
kind: "computation"
type_tag: "计算"
title: "任意汇点价格覆盖与共同 MW 的独立有限审计"
status: "original-full-cli-replayed-static-full-prefix-and-rejection-separated"
summary: "独立Fraction程序检查unique-home/逐件sink资格的近似覆盖、真实体积极小化、宏注入、完整原矩阵枚举及共同MW菜单；本轮完整CLI复跑，112静态实例/1876oracle调用/104920原调度枚举重现历史数学数据，四个full-N与32/4608prefix、拒绝及T0分别保留；不执行最终matroid舍入。"
source_refs:
  - "clean:26e18e49fd85c8f7dd79"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/arbitrary_sink_price_cover_mw_audit.py"
legacy_ids:
  - "UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1"
---

# 1. 原代码和精确有限输入域

原脚本27461B、584行、SHA256 `bc555c5d6254884d3b9cb41a65b126d0b857021d3bac876edca967f97baa067b`，逐段完整读完。本代码不导入仓内cover/MW实现，使用自己的Fraction DP、subset oracle和枚举注入；“独立”是该历史实现与对照路径的身份，本轮重跑不是新增blind或第二份实现。

机器分不交homes H和sinks Z。宏job只可去显式home边，有限时间>T/2；private job j有唯一home h、原时间a_j≥0，并可去自己逐件sink子集，原时间p_zj≤rho*a_j；没有其他finite端。T>0，0<eta≤1，1/2≤tau<1，delta≥0，rho≥1，W_h=Σa_j≤T、a_j≤delta*T，并令

`B=rho*(1−tau+delta)*T≤T`。

sink数/home数可以变，允许零时间、无出口private、不同任务不共资格、宏边>T（算法剪去）。静态生成器每例homes1–3、sinks0–3、private总数≤8、每private至多2个随机sink端，另有无home/无宏/不相交资格/大分母/真正近似cover/near-tight B等12边界例。seed=2026101811；固定100个随机例与这些边界共同形成112静态输入。单独6个MW输入和3个T0输入不混入“112静态”。全部完整输入和原矩阵枚举结果见[可复现证据](../../tools/evidence/um-next-four-audit-primary/README.md)。

# 2. 一次价格oracle如何保真实任务与近似覆盖

对simplex有理价格pi（零价格允许；无sink时用空向量），每private有出口时选择`min(pi_z*p_zj,z,p_zj)`实现的原sink，用编号破平局。home h的真需求为D=max(W_h−tau*T,0)，无出口任务不可参加cover。`cover_dp`只缩放**成本**，保真实体积a：先收所有零成本物品；不足时对每个正成本guess C，只允许cost≤C，scale=epsilon*C/q，epsilon=eta/4，按floor(cost/scale)做新字典层0/1 DP，存最大真实覆盖和不可变ID回溯。与独立`exact_cover`全subset枚举对照：可行性相同，returned_cost≤(1+epsilon)*exact_cost。guess取最优cover中最大成本时，附加误差≤epsilon*C≤epsilon*OPT，故此比较有明确付款；不是免费精确背包oracle。

返回集合逐个尝试删除，只要剩余真实体积仍≥D就删。D>0时最终每件都不可删，因此

`D≤volume<D+delta*T`。

每件有真实sink目的地，实际出口向量l1≤rho*volume≤B。D=0返回空出口。零a即使曾因零价被拿入也能被极小化删除。代码核ID不复用、回溯真实成本、覆盖、极小性、非负与列预算；在4016次local cover checks中另有8次不可行、96件冗余被删，说明不只零需求pass。

按每home的近似mode cost枚举**全部宏注入**，只允许宏p≤T且该home cover可行，不许两个宏占同home。`best_injection`用指数有限枚举作独立最优对照，**不是**生产min-cost matching实现。没有注入则NO_MATCHING；有注入则共同选homes、模式和全部private目的地。未占home的private全回home，占home留量≤tau*T，加真实宏≤T，故所有home≤(1+tau)T；sink负载从真实目的地逐件回算。

若全局价格成本>(1+eta/4)T，则PRICED_FAIL。为何真实T可行例不应失败：宏>T/2使T调度的home至多一宏；该home的留量<T/2≤tau*T，实际出口给cover，价格总成本≤T。局部FPTAS与共同最小注入至多乘(1+eta/4)，所以不会超过阈值。代码对每个已枚举确认OPT≤T的实例、每个测试pi都assert状态OK；没有声称OK反推OPT≤T。

# 3. 本轮完整CLI的静态与全矩阵枚举结果

本轮使用未经修改原脚本、Python3.12.14实际执行一次CLI，exit0。静态112例中64例OPT≤T，遍历371个价格查询（uniform、basis及固定seed随机prices，去重）。`actual_optimum`遍历每个原job的全部finite端笛卡尔积，包含宏与private的所有原选择，不依赖cover/matching结构。

报告总计：oracle_calls1876、local_cover_checks4016、nonempty_local_covers3415、positive_cost3352、zero_cost63、infeasible8、pruned96、matching_rejections146、priced_rejections1、actual_schedules_enumerated104920。最后一个总数包含静态、6个MW输入及3个T0输入的真实原矩阵枚举，不是仅112静态的总数，也不是算法渐近复杂度。

最大实际cover近似比97/96，来自明确的非精确FPTAS例；mode_l1/B最大549755813888/549755813889，接近一但小于一；priced_cost/T最大2，来自被拒绝的NO例，不是成功oracle价格上界违例。完整case/report按JSON逐结构与冻结历史比较，排除环境字段后数学数据一致；fixture文件逐字SHA亦与原历史fb82…相同。旧运行仍旧，本轮另计一次完整复跑。

# 4. MW的共同菜单、full-N、prefix与拒绝

sink数K>0时，R=max(1,|H|B/T)，gamma=eta/4，规定 `N=ceil(16*R*K/eta²)`。原初始w=1，pi=w/Σw，每轮调用上述真实oracle，更新 `w_z*=1+gamma*l_z/(R*T)`。每轮核u=l/(RT)∈[0,1]、确切乘积势恒等式和有理上包络，检查所有prefix，不计算浮点log。

理论参数交叉相乘给

`[1+eta/4+R*K/(gamma*N)]/(1−gamma)≤1+eta`。

只有真正跑完N的成功例才据此assert平均sink负载≤(1+eta)T；prefix例只核其已执行的乘积势/输出。每次occupied记录mode实际私有ID/sink选择，另记宏边频率，核每home菜单质量=宏占位质量≤1及所有sink累计负载一致。它们来自同一组完整方案的convex combination，不是逐row分别选见证。

| MW例 | 实际OPT（T=1） | 原规定N/实际轮数 | 状态与平均sink负载 |
|---|---:|---:|---|
| single-sink | 1 | 64/64 | OK full，(1/2)，budget3/2 |
| two-sinks sub2 | 1 | 512/512 | OK full，(1/8,1/8)，budget5/4 |
| two-sinks cycling | 3/2 | 384/384 | OK full，(3/4,3/4)，budget3/2 |
| priced rejection | 2 | 256/0（首轮查询即拒绝） | PRICED_FAIL；无完整均值 |
| small-eta three-sink | 1 | 4608/32 | OK strict prefix，(63/512,33/256,63/512)；非full-N认证 |
| joint-home-switch sub2 | 1 | 512/512 | OK full，(1/8,1/8)，2个共同occupied menus |

cycling的actual OPT>T但oracle/MW仍成功，不矛盾：该接口只承诺OPT≤T时必成功，成功负载有放宽预算，不能当精确T判定器。4个full成功共1472轮，加prefix32轮，总1504个成功乘积prefix；另一次拒绝查询使MW oracle calls1505，加静态371恰1876。程序没有把prefix补跑至4608，本轮也未改变这个原scope。

# 5. T=0和未执行的舍入后端

T0三例在任何除T、价格、权重或规模归一化之前，逐job检查原零端：空实例、全jobs有零端返回ZERO_SCHEDULE，含正宏无零端返回FAIL；再以原矩阵枚举确认与OPT=0等价。它不是将T0塞进正T公式。

本程序明确没有：通用rational LP、matroid交/列预算IR+B最终舍入、一般实例结构提取、生产级宏matching、一般UM近似或外部新颖性认证。`cover_dp`与宏/原调度枚举是有限audit路径，后者指数规模只限生成的这些小例。实际主算法的最终整数sink界(1+eta+B/T)T还需要另一个upper-column-budget基舍入；当前报告均值和显式菜单不能冒该末步已执行。

[既有配置审计](../审查/配置剥离与联合匹配有限审计--审查.md)保历史JSON；当前d7bf…原正文给price-cover→MW→模式基→最终matroid的完整数学链。本页新增原代码全读、真正完整CLI复跑、原件/输入/输出及精确scope，不重done旧正文或旧JSON。与同批anchor的固定near-unit角色、菜单的group-degree≤2域都不同，不造共同调度合同。
