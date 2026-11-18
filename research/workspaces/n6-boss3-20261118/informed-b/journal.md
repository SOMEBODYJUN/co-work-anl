# Boss3 execution line journal

- Identity: Boss3 execution line, studio slot `informed-b`; session `boss3-20261118-live1`.
- RUN: `n6-boss3-20261118`; target: `customer-attraction/six-providers/exact-six-full-history-half-cover`.
- Start state: branch `rebuild/research-v2`, requested starting HEAD `e0b8e7d28c5164fbd5fd0ef689886c1279e380b7`. Repository state will be verified read-only.
- Assignment: audit Boss2's `partial-fractional-cover-to-six-half` and `four-extras-to-six-half` against this RUN's original model and section-scoped target; identify exactly uncovered catalog structures; prepare a reproducible original-model versus relaxation boundary experiment. Read this RUN spec and packet-full first, then context/show evidence. Do not rerun certified computations and do not promote conditional subclasses to general half-cover.
- Write scope: this `informed-b/` workspace only. No commits, pushes, studio save/line, registry edits, or credential access.
- Status: started; awaiting applicable repository instructions and primary RUN context.

## 研究断点 1：边适用性与 q=5 三类剩余

已按 context/show 实读两边源正文、必要上游真实行与partial证书原件，未重跑已认证计算。准确适用性及未覆盖目录结构见 `boundary-audit.md`。本 RUN 题面/模型SHA与Boss2完全一致，section限定不改数学；两条边均只支付条件子类。

Main 指定q=5后，解析分类完成：倒二全部历史由精确P折扣、重复层和真实末位IC可给K/2；前四位的条件归纳只剩A=(第3位前两不同锚)、B=(第4位前两不同锚+一额外)、C=(第4位前一锚+同额外两次)。详见 `q5-prefix-reduction.md`。这是本线待非作者复核的局部推导，不是q5整体已证。

对idea给出的K5循环区间原目录，已独立编写精确全部SPE子局/根可达集合实现 `exact_tail.py`，原输入 `q5-cyclic-K5-input.json`，实际输出 `q5-cyclic-K5-output.json`，完整真实子局策略DAG `q5-cyclic-K5-policy.json`；子局DAG再由不调用集合递推的直接偏离核验器核完。下一动作：读实际输出并把静态暴露失败与真实SPE结论精确并列；再攻B/C真实tail约束。

## 审查反馈与v2修复

review_q5确认旧K5输入B0=T0，实际q4，“q恰5”是错误范围声明。已真实告Main/idea/reviewer并接受；全部v1冻结字节不改。新 `q5-stress-trial-corrigendum-v2.md` 解释准确影响与修复。真正q5改用K6、循环起点1/5/10/15/20，先由 `verify_q5_stress_input.py` 检查实际集合互异/非锚，再计算：互异额外后手静态损失(10/3,10/3,19/6,19/6)>K/2=3；但全部真实子局及根SPE均唯一终局计数六锚各一次，W=36，子局当前最低收益6。固定输入/输出/1405节点策略DAG全为 `q5-cyclic-K6-v2-*`，未覆盖旧文件。

B/C新参数化探针均另文件保存：`probe_bc_tail_lp.py` 的独立尾必要松弛给B=21/44、C≈0.454386，不能实现原策略；接着 `probe_shared_bc_tail.py` 在同一客户空间上固定四个unused额外覆盖，显式加入末位跨枝共享合法菜单查询，第一轮100模式正在核。它仍排除了后继为锚的情形，且只是一组必要约束，不作反例。
