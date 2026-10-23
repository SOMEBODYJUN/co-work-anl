# round3/relay：内生分数价格与全树支付

2026-10-23。只攻一般 Q-CAG-HALF；未得到一般证明或完整 SPE 实质分离。

本轮已核对最新 AGENTS。自由总质量 r 分数背景的根保证并非新候选，精确等于
`R-51ca8c2b36184c41818099bc490374ca/security/extra_mass_interface.md`
中的 EXTRA-ONE-LEADER（t_(r+1)(b)）。旧
`R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md`
已有自由分数 minmax、KKT、Fenchel 切线与 half 归约。
本工作不把换符号或重推静态对偶当作一般推进。

- `endogenous_fractional_transport.md`：从该旧候选的谱对偶，把真实根菜单产生的条件负载相关性写成精确支付对象。全客户价格版本的逐客运输过强；一个很短的真实 SPE 诊断说明为什么必须保留内生价格/实际激励。该诊断只校准全称候选，不独立发展特例或障碍族。
- `audit_conditional_transport.py` / `conditional_transport_audit.json`：只核该精确 all-y 运输加强的一次20客户诊断，43节点258比较均非负；无扩样、无一般正面推断。

当前承重仍是：让完整有序历史的全部真实孩子 IC，对同一内生分数鞍点提供可共同收费的关系。只保留根菜单、后继收益 floor 或末位 BR 均不够；尚未找到不回到完整 BI 的普遍支付。

## 接续：独审最优替槽核并继续连接

- `review_optimal_exchange_kernels.md`：独立重构 root 一般工作稿 §3，BER/HARM/MATCH/KERNEL 及 alpha↓0、J 同槽条件、随机配对、零客户边界均通过。另推适用于原真实查询枝的锚定核、p0 一阶私有块注入，准确保留与原完整 IC 同核连接的限制。
- `audit_optimal_exchange_review.py` / `optimal_exchange_review_audit.json`：不导入 root/shared 程序，精确核5460个单客户替槽事件、91个随机位置概率、45个非整数正 alpha 公式；有限核验不扩大数学范围。

正在把最优主题随机前缀作为全深度路径，使每一步真实 σ rollout 具有逐步增加的锚；期望用锚定核余量与完整原 IC 的常系数合成支付捕获流。尚未得到需要的单调/超鞅关系。独审通过不作为研究终点。

所有新写仅本目录；没有改旧冻结、共享或执行 git。
