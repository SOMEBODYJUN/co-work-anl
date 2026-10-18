# Take/continue flat menu：严格 statement-first 独立审查

ID：`UM-PARTIAL-SUM-TAKE-CONTINUE-FLAT-MENU-ACTUAL-ESCAPE-v1`。

本次唯一读取的对象：`partial_sum_take_continue_flat_menu_actual_escape_statement_only_v1.md`。

Statement SHA-256：`c78b878296d50e7d84ee1389e0eeb7e3796e1ee7b3c1242b54dd5d4cd3d1e41c`，已实际全文读取并核验。

**隔离记录。** 未读取同 stem 旧 `exact_v1`（获告知它含完整证明）、任何作者/root/其它 agent 推导、review 或 json。下列分配、30-job 时间表与任意调度下界均从新 statement 的明确矩阵独立重构。未运行软件/枚举；只在 scratch 写本记录，未写 repo、Work 或 Git。LST25 canonical 尚未读取，也不混记为此前已经审过本 take/continue 对象。

**判定：陈述通过，无 standing fatal。** 源 SC OPT=0、目标 V=2/5、完整普通 UM OPT=8/5 均可直接证明，不需借用一般 SC↔UM 值桥。

## 1. 完整对象与 counts

三个源 agents、两枚不可拆原 items，各源 value=3/5。任何 allocation 至多两个 agents 收到原 items，故至少一个 utility=0；非负性给源 max-min OPT 精确为 0。

目标每 a 有 r 的一个 state、m 的两个 states、l 的两个 states，共 5 台 private machines、3 selectors、7 distinct incidence jobs。三个 a 合计 private 15、selectors 9、incidences 21、原 jobs 30；再加共享 u1/u2 与 9 个互异 x_a/y_a/z_a resources，共 26 machines。

各 state 的 private sums 恰为 1。尤其 m_off 的 x_a-job 与 r_take1 的 x_a-job 是不同原 jobs；l_off 的 y_a-job 与 m_take2 的 y_a-job 也不同。它们可分别留不同 private machine，不能因为资源同名就合并 jobs。

## 2. 独立重构目标 V

对每 a=1,2,3，选择 r_take1、m_take2、l_accept，分配

    B_r_a={x_a}，质量2/5；
    B_m_a={y_a}，质量3/5；
    B_l_a={z_a}，质量1。

九个 B 全局不交；源真实 items u1,u2 均未领取。因此 V≥2/5。

若一份合法目标 partial allocation 的全组 minimum>2/5，每个 r_a 的唯一 state 都必须领取 u1：不含 u1 的 subset 最多只得 x_a 的 2/5。三个 r groups 不可同时领取同一真实 u1，矛盾。因此 V≤2/5，合得 V=2/5。此 upper 不依赖其它 m/l state 选择，不要求它们遵循某路径语义。

## 3. 全部 30 枚原 jobs 的 actual 达界证书

机器名 M(group,state) 为各自不同 private machines，R(resource) 为对应真实 resource machine。下表时间都是普通 exact rationals，区间为 start→finish；每 row 是一枚原 job，不含辅助 jobs。每 selected private 先排 selector，再排留下的 incidence；所有 exported jobs 在各自不同 resource 上从 0 开始。

| 原 job | 实际机器 | processing | start | finish |
|---|---|---:|---:|---:|
| J_r1 | M(r1,take1) | 1 | 0 | 1 |
| J_m1 | M(m1,take2) | 1 | 0 | 1 |
| J_l1 | M(l1,accept) | 1 | 0 | 1 |
| I_r1,take1,u1 | M(r1,take1) | 3/5 | 1 | 8/5 |
| I_r1,take1,x1 | R(x1) | 1 | 0 | 1 |
| I_m1,off,x1 | M(m1,off) | 1 | 0 | 1 |
| I_m1,take2,u2 | M(m1,take2) | 2/5 | 1 | 7/5 |
| I_m1,take2,y1 | R(y1) | 1 | 0 | 1 |
| I_l1,off,y1 | M(l1,off) | 1 | 0 | 1 |
| I_l1,accept,z1 | R(z1) | 1 | 0 | 1 |
| J_r2 | M(r2,take1) | 1 | 0 | 1 |
| J_m2 | M(m2,take2) | 1 | 0 | 1 |
| J_l2 | M(l2,accept) | 1 | 0 | 1 |
| I_r2,take1,u1 | M(r2,take1) | 3/5 | 1 | 8/5 |
| I_r2,take1,x2 | R(x2) | 1 | 0 | 1 |
| I_m2,off,x2 | M(m2,off) | 1 | 0 | 1 |
| I_m2,take2,u2 | M(m2,take2) | 2/5 | 1 | 7/5 |
| I_m2,take2,y2 | R(y2) | 1 | 0 | 1 |
| I_l2,off,y2 | M(l2,off) | 1 | 0 | 1 |
| I_l2,accept,z2 | R(z2) | 1 | 0 | 1 |
| J_r3 | M(r3,take1) | 1 | 0 | 1 |
| J_m3 | M(m3,take2) | 1 | 0 | 1 |
| J_l3 | M(l3,accept) | 1 | 0 | 1 |
| I_r3,take1,u1 | M(r3,take1) | 3/5 | 1 | 8/5 |
| I_r3,take1,x3 | R(x3) | 1 | 0 | 1 |
| I_m3,off,x3 | M(m3,off) | 1 | 0 | 1 |
| I_m3,take2,u2 | M(m3,take2) | 2/5 | 1 | 7/5 |
| I_m3,take2,y3 | R(y3) | 1 | 0 | 1 |
| I_l3,off,y3 | M(l3,off) | 1 | 0 | 1 |
| I_l3,accept,z3 | R(z3) | 1 | 0 | 1 |

9 selectors、21 incidences 各出现一次；实际 exported incidences 9 枚，private incidences 12 枚。两枚共享资源 R(u1)、R(u2) 都 idle。每个 R(x_a)、R(y_a)、R(z_a) 各一枚 unit job。没有把未选 m_off/l_off states 的 incidence jobs 丢掉。

逐 a 的五台 private loads 为：

    M(r_a,take1):8/5；M(m_a,off):1；M(m_a,take2):7/5；
    M(l_a,off):1；M(l_a,accept):1。

所有正时长区间在原有限资格端执行且同机不重叠，故这是完整 ordinary UM schedule，Cmax=8/5，给 OPT≤8/5。

## 4. 任意完整实际 schedule 的直接 lower

设存在某任意完整 schedule 的 C<8/5。每个 r_a 的 selector 只有 M(r_a,take1) 一个有限端，故其上必有 unit selector。若其原 I_r_a,take1,u1 仍留 private，该机仅这两枚 jobs 的总工作就已经是 1+3/5=8/5，矛盾。因此三枚不同的 r_a,u1 incidences 全都必须导出到唯一 R(u1)。

它们在 R(u1) 各耗时 1，累计负载至少 3，不可能在 C<8/5 完成，矛盾。所以任何完整实际 schedule 都有 C≥8/5。

这个 lower 允许 m/l selectors 任意选态、所有未选 state jobs 任意导出、其它 jobs 任意重排；这些自由不能改变 r 的唯一 selector 端或把三枚 u1-incidences 拆开。不是只对上节预定模式的 lower，也不是只对某个 partial allocation 的 lower。结合实际上界得到 OPT=8/5。

## 5. 正常数 decoder 的准确失败范围

上节目标分配具有共同 positive δ=2/5。若该规则存在对所有 compiled inputs、所有 positive δ partial allocations 都适用的 decoder，保证每个原源 agent 至少 cδ 的效用，其中 c>0 为统一正常数，那么此常数实例应输出三个原 agents 全都正效用的 allocation。

但原源只有两枚不可拆 items，即使 decoder 可以任意重新分配全部原 items、完全不受目标已领取资源束约束，也至少一 agent utility=0。因此这种 all-agents Ω(δ) positive guarantee 不可能；这是不存在相应分配的组合矛盾，不是运算时间障碍。目标证书甚至没有使用 u1/u2，显示 fresh own/accept 资源足以填正 partial mass。

**范围不外推：** 本例不排除只服务部分原 agents、只保总 welfare、另有 source 正值 promise、要求 target δ>2/5 或 strict-unit value1、加入额外一致性资源/jobs、改变取 credit 的规则或其它结构的 decoder。尤其不否定所有 DAG/source compilers，也不否定既有 selector-tree 正规形。原 source 第二 item 的 value 仍是3/5，目标 take2 credit 是2/5；不偷换为一个新源 value 向量。

## 6. 冻结结论

**严格 statement-first 通过。** 已独立给出 SC0、V=2/5、逐枚全部30job actual 8/5 证书、任意完整 schedule lower，以及正常数 decoder 的明确失败量词。未读含 Proof 的旧来源；可在本记录冻结后再转该来源做实际 read-after。
