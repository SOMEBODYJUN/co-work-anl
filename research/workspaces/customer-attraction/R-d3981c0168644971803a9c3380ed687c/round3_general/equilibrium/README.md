# round3 equilibrium 子任务：一般聚合安全值攻击

2026-10-24。只编辑本目录；未spawn、git、work.py或共享正文。主目标 half、
W≥m v_m、W≥(m−1/2)v_m 及自由分数对应聚合桥均仍 **OPEN**。

本轮未取得新的全输入正向福利界。没有把已败单步安全值增长、逐人v、iid福利或
minCCE福利桥当成前提。自由分数门槛及其KKT已在R-077c0…/security/
free_fractional_security.md存在，本轮没有重复认领。

保存的唯一新精确边界是 `fractional_global_payment_boundary.md`：一个针对任意p的
全路径分数Jensen付款加强式的817客户完整SPE反例。实际u=(197,200,200)、W597、
OPT710；固定p=(X2+Y2)/2时ΣF_i−W=199/60。全部43有序历史258行动比较经单位
展开Fraction核验。静态固定竞争对(0,2)的cap=199=W/3，故它不反驳任何原聚合桥。

原始材料为 `fractional_global_raw.json`；审计为 `audit_fractional_global.py` 与
`fractional_global_audit.json`。`probe_fractional_global.py` 与
`fractional_global_probe.json`只记一次明确候选的定向发现，不是一般证明或扫描项目。
独立研究员r3_direct已只据raw按单位客户定义重构通过；其报告在相邻direct目录
`review_jensen_candidate_counterexample.md`。独审另严格证明坏p非自由分数/真正安全值
最优查询：固定(0,2)使其值≤275/2，而静态覆盖下界t_3≥OPT/5=142。

真正剩余步骤仍是：对自由分数安全值的适当最优查询，或直接对任意最优m主题联合，
建立保留全部原树IC的共同支付。全p负差与Jensen不足只排除一个加强形式，未接通此步骤。
