---
source_id: "e2370ab75fef1534990c"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md"
source_sha256: "409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435"
source_size: 13302
kind: "author-proof-candidate"
status: "integrated-candidate; independent-exact-first-still-required"
disposition: "integrated"
---

# 来源与读取

clean show e2370ab75fef1534990c 完整读取了 13,302 字节作者证明候选；原件 SHA-256 为 409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435。源文件明确说它对应一个尚待 fresh reviewer 先行冻结的 Exact-only，源内声明 SHA 为 80fd4ff5…；因此本源不是 blind 独立证明，不能把作者稿和之后的独立审查重复计数。

## 精确域

输入为显式 normalized-flat unrelated-machines 构造：k≥1 个 outer，helper 集 J，每 helper 一个物理互异的 unit home，outer 内 home 权重和为 1，最大 home 权重 nu=max_j w_j≤1/(4096k^4)。fallback states 只使用共享资源集 B，每个 state 系数非负且归一化；额外 leaves 也只使用 B，并以 epsilon=15/16 的 exact threshold-UD 条件给出叶的 H_l 支持。所有 indexed ordinary jobs、zero incidences、未选 state payload、duplicate/unused 项和 leaf groups 均保留，不能因证明方便删除。

源建立 normalized-flat group welfare V 与完整普通 UM 矩阵的值桥 OPT(P(Q))=2−V，1≤OPT≤2。无全叶 matching 时，源声称 V<15/16，全 private baseline 峰值不超过 2，故比率 <32/17<19/10。有 full matching 时在 vacancy transversal matroid 上工作。

## 证明候选的主要承重链

作者固定 epsilon=15/16、c=5/16、theta=1/32、xi=1/(2^20 H^2)、tau=1/(2048H)、w_stop=25/128。给每个 helper 选择一个 fallback state 或 empty 的 profile。对固定 profile，资源 ownership/叶 matching 是显式 network polytope；任意正 outer 权重 lambda 的线性最优值由 weighted matroid greedy 加普通 matching 得到。由 matroid rank 次模性，profile 线性值对 option 集合单调次模。

profile 势取
Phi(W)=(theta/k) sum_i W_i − sum_i(c−W_i)_+^2，P(S)=max_W Phi(W)。
梯度 lambda_i=theta/k+2(c−W_i)_+ 正且 Lipschitz。源的关键状态替换引理声称：若一个 helper 的 state 被替换，存在新 profile 的最优面向量 W'，其 weighted 总变化等于线性最优值增量，且坐标加权 Linf/L1 变化分别受 lambda_i(j)w_j、2lambda_i(j)w_j 控制；随后以二次 smoothness 支付曲率误差。

若实际 V≥epsilon，源在仅用于反证的目标 profile O 上给出 f_lambda(O)≥epsilon^2 sum_i lambda_i。结合 option-submodularity 和状态替换误差，得到当精确 deficit 总和 D≥9/80 时至少有一个 helper replacement 使 P 增长 rho=293/81920>0；k=1 另用实际 lambda_min 分支，不能套 k≥2 的粗界。

算法用 rational Frank–Wolfe 近似每个 P(S)，固定误差 xi，枚举每 helper 的显式 states/empty；若没有增量至少 tau，soundFAIL 反推出 V<15/16，否则 profile moves 数为多项式。若所有 W_hat_i≥25/128，用每 outer 的最大资源 claim、整数 prefix-flow 和叶 matching 回填，得到实际 W_i≥25/128−nu≥799/4096>19/100。取 q=1/10 的 Good helpers 后恢复全部原 jobs，给出 C_max≤2−q=19/10，而不是仅给一个 fractional allocation。

## 证据等级与严格边界

该源没有端到端代码、有限运行、外部 referee 或新颖性证明；它明确等待 Exact-first 独立重构。最需要独立攻击的承重点是：任意线性最优 fractional allocation 的 stable weighted-matroid state exchange；由加权 Linf/L1 变化推出统一曲率常数；Frank–Wolfe/近似 deficit 到 soundFAIL 的连接；以及 prefix-flow 对完整 ordinary jobs 的实际回填。不能用已有小型 exchange audit 代替这些全域证明。

本源的 19/10 目标只属于上述单态 outer、互异 tiny homes、共享 B、exact-threshold-UD leaves 和完整 job 保留的 typed 域；不扩到多 state outer、home 重合、非 UD 额外 groups、heavy states 或一般 unrelated-machines。它也不涉及六人 SPE、客户目录覆盖或 Q-CAG-HALF。

## 与现有对象的关系和去向

本源应与同一 shared-UD tiny potential 链中的 Exact、独立重构、k²/v4 修订和有限 exchange evidence 保持独立 source identity。数学独有内容是 k⁴ tiny-home 候选的完整 profile-势、稳定交换、FW、soundFAIL 和 prefix-flow 承重链；建议并入 archives/unrelated-machines/state/审查/Boss11共享UD叶tiny-home-k二次扩域三源审查--审查.md 的版本沿革或单独建立该链的来源审查页，原字节放入 archives/unrelated-machines/tools/evidence/shared-ud-tiny-potential-20261031/ manifest。不要把作者候选自动当无条件已证定理。
