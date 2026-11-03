---
id: "unrelated-machines/incidence-rank-tiny-primary-seven-brute-queries"
kind: "computation"
type_tag: "计算"
title: "关联环秩tiny原入口的七次穷举与生产缺口"
status: "complete-primary-source-read-and-original-cli-retained"
summary: "1887B原入口只有五矩阵七次brute，核边界不实现反馈枚举/安全叶消元/环DP。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/incidence_cycle_rank_exact.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/incidence_cycle_rank_exact.py"]
source_ids: ["f4c32edec8faa5dd71db"]
truth_status: "exact finite results with separate mathematical reconstruction"
review_status: "informed internal reread, not new blind or external review"
---

# 此次 primary 与已存旁读的区别

原 `incidence_cycle_rank_exact.py` 1887字节，SHA `a46f115cf05d992196b122feb0a9514c5f11a20777dc10e02fef0ed11520f6d8`，本批实际作为认领primary导出、全读、比较并运行一次exit0。此前[七查询实现边界页](关联环秩审计的七个枚举查询与实现边界--计算.md)是在处理数学主稿时旁读和运行该依赖，明确没有给本代码done；本批保留那个历史，不把旧旁读或本次primary处置混成两件数学定理。

当前程序只有 `brute(m,jobs,T)`、四个check helper和main。brute枚举所有机器编号元组s∈{0,…,m−1}^|J|，丢掉不可用端，再从原时间累加Fraction负载；找到第一个峰≤T的实际分配即返回，全部失败才返回None。未用变量best/best_s不使它成为最优求解器。它没有b参数、生成森林、反馈边列表或叶/环DP代码。

# 五个原矩阵、七个阈值查询

| helper | 完整任务菜单（机器:时间） | 目标与实际断言 |
|---|---|---|
| leaf_paths | m4；j0={0:1,1:2,2:1}, j1={1:1,3:3}, j2={2:1} | T2与T1均找到合法分配；原关联图是森林，j0支持度3 |
| cycle_core | m2；j0={0:1,1:2}, j1={0:2,1:1} | T1找到分配(0,1)，T0无可行分配 |
| zero_and_empty | m1、空任务；另m2、j0={0:0,1:3},j1={1:0} | T0空分配((),[0])；另找到零负载完整分配 |
| fail_leaf | m2；j0={0:2},j1={0:2} | T2无可行分配 |

四helper调用次数2+2+2+1=7，五个不同矩阵。原程序没有输出所遇到的所有元组数，且成功时提前终止，不能把m^n潜在空间当作实际枚举计数。main打印 `incidence_components_checked:4` 是固定字面4；不是程序运行时统计四连通分量，也不是四种算法实现。

cycle_core原有限关联图确有4环，但在T1删p>T后只余两条对角边；因此本次没有执行一个保持为环的残余算法实例。原brute甚至不做图剪枝：只是按枚举总负载排除超T端。不能从helper名字推断它触达单环DP。

# 与正确的一般关联反馈算法分开

已全读7413B current与1574B review，并比较[一般算法对象](../算法/有限反馈边与安全叶消元的精确调度--算法.md)。一般定理对任意任务支持度、非负二进制有理端、阈值T≥0，按关联二分图b=|E|−|V|+c给2^b poly(L)精确判定/实际输出：先剪p>T，选生成森林F；枚举反馈边使用集合S，拒同任务选两条，固定所选任务并扣实际容量，删未选反馈边，余下确为F子森林。

森林中任务叶为必选；机器叶i只邻任务j时，p_ij放得下即可交换把j移到i，原机器负载下降，放不下则安全删该边。每个真实调度对应唯一反馈集合，故分支完备；逐机容量控制保证可靠。零端、空任务和孤立冻结机器的负载须仍计入，不能只看残余连通块。真单环核心可按相邻两任务方向的两状态递推、检查闭环后回溯。清分母及整数二分按编码位长计数，不展开时间单位。

上述是已经有自足证明的算法；本1887B代码**没有实现这些步骤**。review泛述有限回算覆盖共任务反馈边和单环核心，可能指未交付的手工检查；不能把这句话当作本程序存在这些路径的证据。本次保留一般证明与字面实现边界，不因tiny弱而宣称定理错误，也不编造生产实现PASS。

# 实际新证据与可续用输入

[新stdout](../../tools/evidence/um-following-audit-contracts-primary/runs/incidence-tiny.stdout)完整为 Python repr `{'incidence_components_checked': 4, 'status': 'ok'}`；[新记录](../../tools/evidence/um-following-audit-contracts-primary/runs/incidence-tiny.execution.json)绑定此次源码SHA、argv、exit0及空stderr。它与既存旁读输出的含义相同，但此次执行单独计1，旧证据仍是旧，不声称从inventory取得了不存在的冻结运行JSON。

程序未用-O；有效断言承担有限检查，-O会移除它们。源码、两份完整数学稿、原认领needs-attention回执和独立恢复核验见[资源说明](../../tools/evidence/um-following-audit-contracts-primary/README.md)。下一实现应另交真实反馈分支、共任务拒绝、残余真环、容量恰等和孤立冻结峰的恢复输出，再与该brute对照；此处不为未来运行预写结果。
