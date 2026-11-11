# 64bd fresh 接续核验

当前任务外层definition保持claimed/Boss5。仅写任务write_paths及本resume-64bd目录；未动Git、队列、registry或共享正文。

实读：根AGENTS.md，research/IMPLEMENTATION.md，prompts/03-map-worker.md，任务全部原文，research show返回的两端完整当前记录与body，冻结PDF全部15页文本并渲染第10页Figure5。两端pin和源SHA匹配。

数学：CONFIG投影对每行给合法配置凸组合，所有T合法配置包含于机器计划允许族，得到同一共同x的分数满流；整数容量给完整整数流。真实T调度给确定性配置点，所以支付OPT≤T⇒满流步骤。保accepted/unconditional/contribution而非whole_result。ell2精确等价；ell3/4反向由三任务实例排除。

新澄清：论文第9页把整数二分写成找最小成功T，此措辞可被四任务例否定。此时流接受性非单调：T10成功、T12拒绝，真实OPT15。二分仍正确，因拒绝T必小于OPT，维护拒绝下界L和成功上界H，终止H=L+1≤OPT即可。此澄清已写入交付正文§3.1，并非新增对象或反驳已登记定理。当前v2未声明流接受性单调或最小成功T，无需改共享正文或registry。

独立有限复算：verify-plans.py遍历T1..20、q0..4的53,129个降序处理时间行及757,504个子集，核合法配置包含、输出包络和ell2精确性；另穷举两明确实例的真实和机器计划分配。结果verification.json。有限检查仅作辅助。

edge-bind --write完成；edge-check通过，proof_scope=step。收据assets按最终绑定字节刷新。无read-add、无未闭合follow-up。父Boss可直接checkpoint下列三项并依流程push/done；本目录只作可复核笔记。

- `map/edges/unrelated-machines-3a-3a-64bdf7ec5167df6a/config-projection-completeness.json` SHA256 `6e0c5ca5e044780ddf070448de657d560160ca3ca28761a623fefd6809c2c744`
- `map/edges/unrelated-machines-3a-3a-64bdf7ec5167df6a/config-to-machine-plan.md` SHA256 `4296a5afc318750aaa3a2294f4e1285bb2651191057e33f6e78d7dee6ae5d101`
- `map/receipts/unrelated-machines-3a-3a-64bdf7ec5167df6a.json` SHA256 `16e0644e58edf341ba8138f071d15399bbe5e9c140213c278ce9d0694ebbba9d`
