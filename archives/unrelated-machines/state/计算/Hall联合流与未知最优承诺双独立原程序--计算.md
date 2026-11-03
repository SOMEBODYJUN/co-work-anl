---
id: "unrelated-machines/hall-joint-flow-and-opt-promise-original-independent-audits"
kind: "computation"
type_tag: "计算"
title: "Hall联合流与未知最优承诺双独立原程序"
status: "complete-source-read-and-five-original-clis-retained"
summary: "两个独立有限oracle分别核原任务阈值可行性与精确OPT承诺；共同流、前缀输出、恢复t与原OPT分开。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/hall_group_joint_flow_independent.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/hall_group_joint_flow_independent.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/hall_group_opt_promise_independent.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/hall_group_opt_promise_independent.py"]
source_ids: ["af4686084d064b7e5407", "5f96df68c24c9fd95b18"]
truth_status: "exact finite evidence with separately stated general arguments"
review_status: "informed internal reconstruction; no new blind or external review"
scope: "original code, exact input contract, original finite CLI and historical comparison"
---

# 两个独立入口与原任务合同

两份 primary 分别是 `hall_group_joint_flow_independent.py`（5485字节）与 `hall_group_opt_promise_independent.py`（4756字节）。本批逐份核原件并阅读全文；它们导入同一候选 `hall_group_joint_flow.py`（24011字节），但自己构造原任务、做 DFS 或阈值枚举。候选的 `audit()` 有 main guard，未被这两个入口执行。本页保存其一般接口以解释有限检查，既有完整主证明见[Hall增量审查](../审查/Hall联合流与前缀匹配增量审计--审查.md)，没有把旧审查重新命名为本轮 blind。

机器为不交的 home 集 H 与 sink 集 Z，|H|+|Z|≥1，允许其中一集为空。home h 有私有任务组 J_h，每个任务 j 的时间 w_j≥0 在 h 与共同允许集 E_h⊆Z 上相同，其他端不可用；宏任务只能在 H 处理，有限时间 p_jh 可异。给整数 q≥2（按二进制输入）、δ≥0、qδ<2、T≥0，合同为

\[
\theta=\frac12+\frac1q,\quad \theta T\le W_h:=\sum_{j\in J_h}w_j\le T,
\quad w_j\le\delta T,\quad p_{jh}>T/2\text{ 对所有有限宏端。}
\]

每宏至少一有限端；宏端可以大于 T，网络会剪去这些端。数值限 exact int/Fraction/string，bool/float 被拒；负值、非法 sink、错误行长、越出合同抛异常，不能当成合法输入上的可靠 FAIL。合法合同上的 `solve=None` 才是阈值必要条件失败。

取

\[
\tau=\frac{q-1+q\delta}{q+1},\qquad
\rho=\frac{2q+q\delta}{q+1}=1+\tau=q(1-\tau+\delta)<2.
\]

## 同时选择宏 home 和 group receiver

原 T-可行调度的宏边严格大于 T/2，故各宏占不同 home。任一被宏占用的 home h 必须把超过 W_h−T/2≥T/q 的私有工作送到 E_h。对任意占用 home 子集 A，其外送量受 N(A) 的总容量 |N(A)|T 限制，得 |A|<q|N(A)|，从而 q-复制 Hall 条件成立。这个必要条件必须与宏 home 选择**同时**实现。

实现网络为 source→macro→home-in→home-out→sink→target；宏、home 的容量均1，sink 容量 min(q,#macro)，宏→home 只用 p≤T。若流未覆盖全部宏则可靠推出 OPT>T；成功给每个被占 home 一个 receiver，且每 sink 至多接 q 组。不存在先挑一个宏匹配、再独立挑 receiver 的未经证明步骤。实现不展开 q 个顶点，完整流值至多宏数，二进制巨大 q 不使节点数膨胀。

在每个被占 home 的原组顺序上，依次外送任务，直至留下总量≤τT；未占 home 保留全组。最后一次外送前剩余>τT、任务≤δT，所以外送量<(1−τ+δ)T；若无需外送则量0。宏 home 总负载≤T+τT=ρT，sink 总负载≤q(1−τ+δ)T=ρT，未占 home≤T。返回的是每个原宏和原私有任务的真实端点，不是只有负载向量的抽象证书。

T=0 时私有任务全为0；无宏即直接零调度，有宏则其所有有限时间>0，`solve` 返回 None。空任务和空 eligibility 都按实际合同处理。

## 未知 OPT 承诺、离散 bottleneck 与严格 t<O

令原任务的真实最优值为 O。承诺是在 **O** 上满足上述 W、w、全部有限宏端严格大于 O/2 的条件，而非把一个随意猜测 T 当成 O。δ>0 时先求最小离散宏时间 B，使同一联合网络有全覆盖流；只需二分排序后的有限宏时间，不依赖“全合同对 T 连续单调”。真实 O 调度给 B≤O。

设
\[
t=\max\{\max_h W_h,\max_j w_j/\delta,B\}\le O.
\]
于是 W_h≥θO≥θt、W_h≤t、w_j≤δt、全部有限宏端>O/2≥t/2，且网络在 t 全覆盖。调用 `solve` 获得真实调度≤ρt≤ρO。这里 t 可以严格小于 O，既不是实际 OPT 的另一个名字，也没有违反原任务最优性。δ=0 的正 O 承诺不可能有非零组；合法零承诺走零分支。实现还直接处理有零宏端的全零输入，这是零端 API 扩展，不能倒填为严格宏承诺的非零证明。承诺外 `solve_promise` 可以异常，不是全输入 promise 判定器。

明确的严格例：两 home、一个 sink，两组各六个1/6；两宏分别只在其 home，时间3/5。q=3、δ=1/3。把各组三个任务送 sink、三个留 home，负载 (11/10,11/10,1)，故 O≤11/10。若峰<11/10，每 home 只能留至多两个1/6，sink 至少收到八个1/6，矛盾，故 O=11/10。恢复 t=1；代码输出满足ρt（ρ=7/4），未声称峰≤t。

# 两次原 CLI 的真实有限范围

| 入口 | 实际 oracle 与输入 | 本轮结果 |
|---|---|---|
| joint independent | 自建 job-major 原矩阵；memoized 阈值 DFS，不调用候选 Hall/矩阵/OPT；q=2,3,4 固定模板、全部小 E/宏行组合，150个 seed230782 随机3-home/3-sink例；另零/空/巨大q等边界及7非法例 | 8123 instances；原 T-可行3688；success4066；rejection4057；显式非法拒绝7；PASS |
| OPT promise independent | 每机器所有子集和作为实际 makespan 候选，再用 memoized 原任务 DFS 求精确 O；另独立穷举联合宏/home/sink选择求 B；seed778791 三组各100样本加严格例 | sampled301；真实 O 承诺122且122成功；t<O 恰1；另零δ例不计301；PASS |

第一次成功数大于 T-可行数完全允许：接受只需输出ρT调度，失败可靠性与成功可行性不是同一阈值合同。巨大 q=2^400 例是空 home/空任务加一 sink，未在巨大实体图上跑指数枚举。第二次仅122样本实际满足 OPT 承诺；未把301全部列为承诺通过。

每个成功输出按原任务顺序重新查端点资格、逐机累加 Fraction 负载和ρ界。精确输入由保存完整原码、模板、seed重建；原 CLI 没有 dump 全8123矩阵或301份分配，不伪造那些逐例数据。本轮两次入口分别一次，候选自己的14798例主审计、2079公式、9出口例都**未**重跑。

[原件与18源指纹](../../tools/evidence/um-next-actual-audit-primary/README.md)、[joint新stdout](../../tools/evidence/um-next-actual-audit-primary/runs/hall-joint-independent.stdout)、[promise新stdout](../../tools/evidence/um-next-actual-audit-primary/runs/hall-promise-independent.stdout)、[完整argv/退出码](../../tools/evidence/um-next-actual-audit-primary/runs/execution-manifest.json)。两份旧冻结 JSON 与本轮输出全字段相等；旧独立审查的先后/先验身份仍是历史事实，不是新一轮未读证明的审查。一般 Hall 与恢复 t 的论证、有限实现核验、全 UM 算法目标分开；这里的特殊组模型不自动迁移到任意异权端点。
