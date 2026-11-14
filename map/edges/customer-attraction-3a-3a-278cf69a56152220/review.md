# Solver 数学报告：M-e394b173b9b1419588c6c380da4bd326

任务：customer-attraction-3a-3a-278cf69a56152220
核心对象：M-e394b173b9b1419588c6c380da4bd326
角色：Boss1 / Solver；本轮未 commit、未 push。

## 实读与字节核对

按任务 context_plan 的 15 个 reading_pass 完整读取并核对 SHA-256：

1. archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md — 7547538073d8edf42f2430c5ed0d4139c2129fdaa8817ea0dbcba591552328e5。
2. archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md — cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88。
3. archives/customer-attraction/state/引理/三十四权同源双分支的真实行锥与精确计数消元--引理.md — 437d5eacff22808c2392662d29bbd74a83dd1a499fd9c3aa3115eb00db207c8c。
4. archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md — 4dacbe163ea4ea9459395dd4445c0dea25ed28070d0723a750ea6351832f4d2c。
5. research/workspaces/six-boss2-20261111-cross/joint_requery/actual_signature_witness.json — 94f90d815c3f3b1d28b51145191dae0fb0197ac325cbfcf0d0a0b0ee30806a10。
6. research/workspaces/six-boss2-20261111-cross/joint_requery/strict_projection_witness.json — c187eaa9ce5492afcd37c592108cda11ffa99011e4b1610ff9f1f3221c2e13f8。
7. research/workspaces/six-boss2-20261111-cross/joint_requery/find_actual_projection.py — ded8e0af5ce07dac63f936ae1659fb75880448995bc3f25852ab1bf2493443c2。
8. research/workspaces/six-boss2-20261111-cross/joint_requery/explore_projection.py — f64d1d08dc52b935432c993d6712a1888dccea216f737a2d5e3cdc4c175b55da。
9. research/workspaces/six-boss2-20261111-cross/joint_requery/separate_master.py — 20ccb2656d736e7754a9c79ef9d030358ab2534bd8b14a4b4b6d8726803709af。
10. research/workspaces/six-boss2-20261111-cross/joint_requery/selected_cuts_5716.json — 1ade5aeb300b5a33e21e9b6c7d0f95523d3dd4be672be0332cfc03155ed68531。
11–13. research/workspaces/six-boss2-20261111-cross/master_cuts/merged_5716_exact.json 的三个连续区间；全文 1,456,749 字节，SHA c86ea061c22ce1ece9df4955a9861a80935cabe1f293ecb8d62e4c0b17e0caf0。
14. research/workspaces/six-boss2-20261111-cross/main_verify_pair.py — 865b390bf2d993d311f06b02d14de294824dd55eb0fcba4d4bd1dd19bdd627ac。
15. research/workspaces/six-boss2-20261111-cross/main_verify_pair.json — c6228abe9edda7ba3eedbd64d53326ba3c26595a593d4b0912e0113614dfc04e。

第 11–13 段是同一 JSON 的连续区间，不重复计数；4849 列及各 kind 的全量结构均已解析。main_verify_pair.py 的独立 Fraction 复核运行结果为 PASS；保持任务声明的 evidence JSON 原字节与 SHA。

## 1. 模型、量词、假设和核心结果

模型是有限单位客户 N、有限非空共同标签目录 S、覆盖映射 cov:S→2^N。不同标签可以同覆盖，空覆盖、重复、同覆盖异标签、零客户和所有弱平局均保留。m 个提供者按固定次序、每人一次、观察全部先前有序行动；客户在覆盖者之间均分：
c_x(s)=#覆盖者，u_i(s)=Σ_{x∈S_i}1/c_x(s)，W(s)=|∪S_i|。完整纯策略定义在全部有序历史，SPE 对每个历史、当前玩家和合法偏离都沿同一完整策略的真实后继满足弱 IC。相同负载的不同有序历史不能直接商并成同一续局。六人主命题 2W≥OPT_6 在定义文件中仍 open。

核心 M-e394 的量词是任意有限实例、完整有序历史纯 SPE、同一合法源 h、剩余 k≥3、合法查询菜单和客户无关非负权。第一枝强制 T 后真尾为
(H_1,…,H_{k-3},B,C)，返回同一 h 强制第一枝真末题 C 后真尾为
(G_1,…,G_{k-3},J,V)。两枝共享第一枝 C 的身份；源收益为 r，过去负载为 p，actual 末位收益为 u、actual 末前负载为 ell，共同容量上界为 K。客户会员位 t,q,b,c,j,v，中间人数 s,s′，z_1=p+t+s+b+c，z_2=p+c+s′+j+v。离轨源时不得把 r 换成 actual 同位置收益。

任意末对查询 X,Y 的新增行是：
P_1(X,Y)=(x+y)/(β_1+1)−(xy+b)/((β_1+1)(β_1+2))−(b+c)/z_1，
P_2(X,Y)=(x+y)/(β_2+1)−(xy+j)/((β_2+1)(β_2+2))−(j+v)/z_2，
其中 β_1=p+t+s，β_2=p+c+s′。对每枝末对 D,E，强制 X 后真实末回复 R，令 fβ(X)=Σ_X1/(β+1)，gβ(X,Y)=Σ_{X∩Y}1/((β+1)(β+2))，Uβ(X;Y)=fβ(X)−gβ(X,Y)。则
−ΣP_i=[Uβ(D;E)−Uβ(X;R)]+[Uβ(R;X)−Uβ(Y;X)]+[Uβ(E;D)−Uβ(R;D)]+gβ(D,D)−gβ(D,R)≥0。
前三项是三处真实 IC，末项逐客户非负；不冻结离轨末回复，也不要求两枝后继相同。

34 维旧锥含 2 source、4 price、4 cap、两枝各 5 last、两枝各 5 safe、2 middle price、2 middle cap。任意非负 theta 与任意非负 PAIR 权先合账，预算为 B=r+A u+D K（源权和 1），再对同一 b,c,j,v,s,s′ 联合取最小：
Psi=min_{b,c,j,v∈{0,1}, 0≤s,s′≤k−3} F，
得到 r+A u+D K≥Σ_x Psi_x。middle 只通过 s,s′ 出现时，最小域精确是 16(k−2)^2 个计数候选；这不是把策略限制为计数函数，也不证明局部最小可在同一完整 sigma 中同时实现。PAIR 权全为 0 恢复旧 34 锥；旧锥包含于新行族，但不声称逐行支配。

登记对象 M-e960 的强 PAIR 是核心所用的可复用输入：
H=U(C,D)+U(D,C)+g(C,C)≥f(T)+f(Q)−g(T,Q)，并可对任意 M≥2 个有名、可重复索引聚合。核心新增的是保同一 C 作为第一枝真末位和第二枝源，再把两枝真实行、PAIR 和 actual 价格/容量在共同隐藏域先相加后取 min。

## 2. 具体局部推导和严格 actual 证据

k=3 的九行整数权为：
sourceT 50142；sourceC 21056；K−|B| 925；第一枝 C 查询 Q 6052；同一 C 查询 J 2782；同一 C 查询 V 4014；第二枝 V 查询 B 4004；真倒二 J 安全查询 V 924；第一枝 (B,C) 的 PAIR(J,V) 736。源权和 71198。

实际第四源 p=0,1,2,3、16 隐藏态精确消元：
Phi(p,t,q)=(65146t+6052q)/(p+1+2t)+925t。
所以
71198 u_4+925K ≥ Σ_x Phi(p_x,t_x,q_x)
在该 actual 切面成立。p=4,t=1,q=0 是明确边界：真实最小值 29576/3，公式值 71621/7，不能推广。

actual_signature_witness.json 不是离轨伪背景：13 个原子，质量总和 1，K=4384/6423，u_4=785/6423，u_6=4748/19269；六位 actual 收益关联保留。34 行加 actual 末位价格/容量共 50 条旧行的 Fraction 余量全非负，最小为 0；新九行整数尺度余量
71198u_4+925K−ΣPhi_x=−90896/19269<0，
归一为 −45448/685957131。因此新联合投影严格超出旧 34 投影锥；这仍是局部必要锥严格分离，不是 SPE 反例或 half 反例。

strict_projection_witness.json 保留了一般离轨源的可行提升/对偶对照，不能代替 actual 六位证据。find_actual_projection.py 通过浮点 LP 找候选、再用 Fraction 重建；explore_projection.py 明确写明不是 SPE solver；separate_master.py 对固定主点按六个实际索引和 16 隐藏态重建新切面，均不能扩大为全策略结论。

## 3. 5716 固定点和五条精确负切面

merged_5716_exact.json 绑定 SHA c86ea061…，4849 列由 1 个 K、16 hist、582 joint-reply、1306 overlap、896 actual-B-family-state、2048 maximum-root-family-state 组成；标记 exact_feasible=true、verified_rows=5716、exact_optimum_claim=false、最小余量 0。它是 5692 条继承必要行加 24 个冻结有理向量的必要系统，非完整历史 SPE 系统。

selected_cuts_5716.json 绑定 SHA 1ade5aeb…，扫描 96 个结构，保留 5 条两两不同的 exact negative cuts，非零列均在前 1905 列，全部使用新 PAIR：

| member | orbit | query | slack（十进制） |
|---:|---:|---:|---:|
| 0 | (0,0) | 8 | −8.4914141633e−5 |
| 0 | (1,0) | 11 | −8.2355400662e−5 |
| 1 | (0,0) | 5 | −1.5066783245e−4 |
| 1 | (1,0) | 5 | −1.3935059511e−4 |
| 1 | (1,1) | 5 | −8.4084855214e−5 |

每条 exact_slack 分数、权向量、visible 各态、sparse row 和 row_sha256 均在稳定包；main_verify_pair.py PASS，报告 13 原子、50 条旧行 exact nonnegative、new slack −90896/19269、五条 full_coefficients_equal=true。它们排除固定必要系统中对应切面的可行性/补全，不能推出整个客户模型不存在 SPE，也不能声称加入五条切面后的系统不可行。

## 4. 可复用的实际逻辑边

本批比较发现没有新的未发布边。以下 canonical edge 已完整覆盖本核心及任务指定的两个 follow-up 对端：

- edge_id: boss2-six-cross-34-and-pair-shared-projection
- kind: implies
- status: accepted
- source_ids:
  1. customer-attraction/thirty-four-weight-same-source-two-branch-true-row-cone-and-exact-count-elimination
  2. M-e960d7f4ebca40a38760eb3ae044cc19
- target_ids: [M-e394b173b9b1419588c6c380da4bd326]
- premises_mode: all
- relation_mode: unconditional
- conditions: 有限单位客户、有限非空共同标签目录、同一完整有序历史纯 SPE；固定同一有序源余 k≥3，第二枝强制题恰为第一枝真末题 C；所有查询合法、所有权非负、两源权和 1；只有查询不读取 middle 个别身份时使用计数压缩。
- roles: 34 对象给两枝 source/price/cap/last/safe 共 34 行与共享 C 人数域；M-e960 给两枝真实末对任意合法查询的零预算强 PAIR；M-e394 将真实行先相加并对同一 b,c,j,v,s,s′ 联合消元。
- explanation: 三 IC 加 g(D,D)−g(D,R) 给每个 PAIR 非负；任意 34 权与 PAIR 权相加仍非负，预算恰 r+A u+D K；联合 min 只降低右侧，middle 计数域精确 16(k−2)^2；PAIR=0 恢复旧锥。
- scope: 一般局部投影；不支持六人 half、全图 SPE 或逐客户 IC。

Evidence 是：
archives/customer-attraction/state/引理/三十四权同源双分支的真实行锥与精确计数消元--引理.md (437d5eacff22808c2392662d29bbd74a83dd1a499fd9c3aa3115eb00db207c8c)；
archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md (4dacbe163ea4ea9459395dd4445c0dea25ed28070d0723a750ea6351832f4d2c)；
archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md (7547538073d8edf42f2430c5ed0d4139c2129fdaa8817ea0dbcba591552328e5)。

核心已有但本任务不重复创建的下游边是 boss2-six-cross-pair-and-discount-pay-shared-terminal、boss2-six-cross-shared-pair-to-query-hierarchy、boss2-six-cross-three-families-pay-52-added-rows；它们分别处理共享末端组合、76/332/616 查询层级和固定 5716/5727/5744 图的新增必要行，均明确不升级为全局 half。

## 5. follow_up / closed_overlaps 建议

两个任务标记的 follow-up 都已由上述 accepted edge 解决，建议不发布新的 3B 任务，写入：
[
  {
    "core_id":"M-e394b173b9b1419588c6c380da4bd326",
    "peer_id":"M-e960d7f4ebca40a38760eb3ae044cc19",
    "reason":"accepted edge boss2-six-cross-34-and-pair-shared-projection 已以相同共同模型、三IC恒等式、共享C和联合min完整结算；当前无新增数学内容。"
  },
  {
    "core_id":"M-e394b173b9b1419588c6c380da4bd326",
    "peer_id":"customer-attraction/thirty-four-weight-same-source-two-branch-true-row-cone-and-exact-count-elimination",
    "reason":"同一 accepted edge 已完整给出34锥与M-e960强PAIR共同推出核心的预算、量词、条件和16(k−2)^2计数消元；当前无新增数学内容。"
  }
]
follow_up_tasks 建议为空。canonical coverage 中核心目前仍是 needs-decision，虽已列上述 accepted edge IDs；Root 可改为 linked，comparison_scope 写入本报告实际完整实读范围，复用既有 edge IDs。若本批必须产生收据，建议 assets=[] 加上述 closed_overlaps，绝不复制已发布边文件。

## 6. 未付义务、反例和状态

已付：一般双枝真实 IC/PAIR 分解；34 行任意非负权锥与精确计数消元；k=3 actual 第四源的九行闭式；actual 六位 13 原子旧行可行和新行严格负；5716 点五条精确负切面及独立 Fraction 复核。

未付：全部 actual 位置统一支付 r,u,K 的全局共同客户证书；完整有序历史纯 SPE 的可实现策略；从必要系统切面推出原客户模型无 SPE；六人 half 的证明或真实策略反例；p=4 或任意 k 的闭式推广。

准确状态仍为 proved general local necessary-row identity + strict actual-signature projection / fixed-cut separation；不是 SPE counterexample、不是 half theorem、不是全局 refutation。
