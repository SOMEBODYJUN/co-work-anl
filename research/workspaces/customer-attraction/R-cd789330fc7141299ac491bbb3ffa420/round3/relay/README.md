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

## 新的一般正组件（尚未闭合跨树）

- `optimal_exchange_potential_and_query_credit.md`：自足合并 fixed-pair Beta 势、shared 的 owner partition 单位基线势、同叶 sum e<=I，以及 relay 全深度前缀查询信用预算。原 Beta 查询折扣逐客户至多 H_(a-1)，owner 首次覆盖势更强至多 H_a-1，均由 a-1 重复比较预算支付。root/shared 已分别独立重构；没有宣称 half。
- `audit_exchange_potential_credit.py` / `exchange_potential_credit_audit.json`：定义级核72818个边际、21844个同叶预算、10795个任意未来前缀 incidence；在一个既有完整 SPE 上核六个固定最优槽顺序的精确 ROLL 恒等式，不作实例扩样或特殊正面推断。
- 主稿现追加直接作用于原实际-prefix matching 的 **DIRECT-REPEAT**：任意 x 的所有查询折扣至多 (a_x-1)/2，不需最优前缀；R、I 分别计账。root/shared 均独立重构通过。
- `audit_owner_insertion_identity.py` / `owner_insertion_identity_audit.json`：新增 INSERT 和 DIRECT-REPEAT 的计数级边界核数。附加信用正是非owner覆盖背景1的插入支付，其势 Psi_Q=Σ_O(H_(1+k)-1)，原调和势精确等于 F_Q+Psi_Q；没有由此宣称辅助 SPE。

当前新承重是该正文 ROLL 中联合项 sum_i(e_i^-+D_i)：前项来自不同真实 rollout，后项是同节点两个真实叶的形式去槽势差，必须共同处理。不能把同叶 I 预算跨枝重复用，也不能把形式去槽 profile 当作删人 SPE。

原实际-prefix 版本必须保留 excess E=Σ_iF_Q(Y_i)-OPT；删掉它再要求总 ghost 势一次预算是过强接口，不继续此假桥。保留 E 后只是 matching 原余额，实际新增正关系仍是 owner 势、插入分解及 DIRECT-REPEAT。

- `hall_owner_anchor_connection.md`：连接 credible 的全角色 Hall-B 与 owner 势。owner-complete 角色由最优性自动没有 outside 源，在 Hall-B 的任意可行流中零入零出；强制最优前缀的回流严格避开全部已锚定角色。当前 owned 捕获边与 Hall-B missing-owner 边客户容量不交；将外部源降为真实利润时明确预留同叶 modified 边际 kappa。credible 收到陈述/证明后独立重构通过，非严格盲审。仍无跨叶容量闭合。

所有新写仅本目录；没有改旧冻结、共享或执行 git。
