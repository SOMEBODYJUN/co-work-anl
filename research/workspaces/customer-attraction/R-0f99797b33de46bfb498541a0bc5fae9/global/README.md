# 一般全局证明分支：本轮检查点

Q-CAG-HALF 仍 OPEN；没有一般证明或 SPE 目标反例。

最后定向检查：
[聚合尾部截取的删除成本与驻留支付](aggregate_tail_deletion_identity.md) 给一般
精确恒等式 `P_r-r t=epsilon_*+kappa+eta+R-C`。删除低尾部必须支付有符号
稀释成本 C，stationarity 仍留下分母相关 R；两个不交二客户主题的完整三人
SPE 给每分支 C=1，不能裸丢。目标接口明确保留实际尾部聚合 surplus，未重试
已失败的逐人安全值命题。`aggregate_tail_deletion_audit.py` 定义级重放小例。

主要新增：
[联合后继负载与精确同主题支配的任意人数障碍](joint_copy_floor_obstruction.md)。
这是从现有动态极大路由引理出发，保留后继联合主题组合的新递归接口及其解析
反例族。目录为所有 k 元子集时，接口预算精确为 `(k+1)H_m-1`，而 `OPT_m=mk`；
其比值可无界。因此不能仅靠保留联合负载修补旧的独立分母。

反例只针对充分机制：最坏近复制组合违反末位最佳性；正文明确保留完整历史
SPE 的原始量词。下一个可用信息是近包含收益恒等式及外部收益缺口，仍需全局
跨分支预算，不能只依末层补行。

复现：从仓库根运行
`python3 research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/global/joint_floor_obstruction_audit.py`。
`joint_copy_floor.py` 是有限有理递归实现，`joint_floor_5_4.json` 与
`joint_floor_theta.json` 仅记录有限诊断。

最初“全部遗漏由W支付”的候选已发现为旧失败桥后立即放弃，参考正文末尾；
`entry_cone_attack.py` 的有限未发现反例结果不支持此已假命题。
