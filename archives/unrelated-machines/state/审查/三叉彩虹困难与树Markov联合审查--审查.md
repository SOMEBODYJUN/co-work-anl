---
id: "unrelated-machines/ternary-rainbow-hardness-and-tree-markov-review"
kind: "review"
type_tag: "审查"
title: "三叉彩虹困难与树 Markov 联合审查"
status: "full-source-read-with-prior-content-reconciled"
truth_status: "restricted ternary rainbow hardness and multiplicity threshold retained; tensor amplification obstruction retained; five-machine tree-Markov completion contract refuted by an exact finite counterexample"
summary: "完整读取两份当前来源、对应冻结程序与既有对象，分别保留三叉彩虹树的三层结论和五机生成树再耦合反例；明确重复内容、独有内容、量词边界与后续缺口。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/tree_markov_completion.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/tree_markov_completion.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/tree_markov_completion.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/tree_markov_completion.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/tree_markov_completion_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/tree_markov_completion_audit.json"
related_objects:
  - "../定理/单强制根树精确配置间隙--定理.md"
  - "../定理/私有菜单树有界叶重数配置界--定理.md"
  - "双件见证树Markov与类型压缩三源审查--审查.md"
  - "独立稀释残余与树Markov完成审计--审查.md"
  - "裸菜单读后与保值降度及调色板障碍--审查.md"
---

## 读取范围、版本身份与处置

本次完整读取了两份当前数学正文、`cleanup/inventory.jsonl` 中的路径、尺寸、SHA-256 和 legacy-cleanup/main 双冻结定位，并对照现有三叉树定理、树 Markov 审查、独立有限审计和问题页。三叉来源稳定 ID 为 `fc5c981c58f0cee5df66`，路径为 `research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md`，33621 字节，SHA-256 为 `3f3075ec56543f2e2b1f909614c853762b66232c0081d311e9c3d1f58d8b1903`。树来源稳定 ID 为 `9e66cf0e6411197f7a23`，路径为 `research/current/unrelated_machines/tree_markov_completion.md`，5545 字节，SHA-256 为 `73628429e0c9773a3cfc083a8b3d87ef3b20004a583df6f5dce2492309a31817`。两份来源在两个冻结提交中内容相同；这不是两份独立数学证据。

树 Markov 的原规范程序稳定 ID 为 `2171ba148bfb1f9ac193`，SHA-256 `981a354cfb9a41c939a967df8767a3f988d2d13cc732ceaeae802588ea6d72fb`；精确结果稳定 ID 为 `72369fac674ccdc4c862`，SHA-256 `cf2d1bd613e8ac0567f051cc0cf22c0e3059e1775a2e78cff3aec17a5e51b855`。另有独立路径的 `4793fd8514c206c37797`，它核同一个五机反例的全分配枚举和 Fraction 输出；不能把两条程序路径重复计为两个实例族。

本页的新增处置是把三叉来源的 v1 归约、v2 全局重数门槛和张量/收缩障碍连成一个有范围的审查对象，并把当前来源版本、冻结定位和既有对象的关系写清。树 Markov 的数学反例已在既有 `双件见证树Markov与类型压缩三源审查`、`独立稀释残余与树Markov完成审计` 和冻结原 review 中出现；本页重新核当前正文的量词、数值和四机边界，保留当前来源的唯一身份记录，但不把重复审计伪装成新实验。

## 一、三叉二叉彩虹子树 v1：完整对象与困难性范围

### 定义域和量词

输入是显式完整 rooted ternary tree (T)，所有叶深度为 (h\ge1)，每个内部节点恰有三个 children；叶颜色函数 (chi:L(T)\to C) 的颜色集合有限且显式，颜色可以重复，包括在同一个 child subtree 内重复。高度随输入增长，完整树和颜色编码都计入输入长度。一个 full binary subtree 必须含原 root，并在每个 active internal node 恰选两个原 children，叶仍在深度 (h)；rainbow 指选出的 (2^h) 个叶颜色两两不同。它不是任意连通子树、路径异色或“每种颜色至少出现一次”的问题。

令 (q(T,\chi)) 为可实现的根满 (r)-叉 rainbow 子树的最大 (r\in\{1,2,3\})。来源只建立 (q\ge2) 与 (q=1) 的受限可行性困难，不建立任意固定 (delta) 的 strong ((k-1))/weak (delta k) gap，也不由叶比例 ((2/3)^h) 自动推出逐层分叉比例。

### 3SAT 到彩色 AND/OR 的自足归约

每个 literal occurrence 使用独有颜色，即使文字重复也不共用 occurrence ID。对变量 (x_i)，建立两个 branch：在赋值 (x_i=t) 时取 false 的 occurrence 颜色作 AND；空集合用私有 neutral color。变量子式为两个 branch 的 OR。每个 clause 是三个 occurrence 颜色的 OR。所有变量、clause 子式用平衡 binary AND 合并。彩虹 realization 恰好选择一个变量分支和每个 clause 的一个 occurrence，并要求全局颜色不冲突：若 clause 选择了一个在所选变量 false bundle 中的 occurrence，其颜色重复；所以 realization 存在当且仅当 3CNF 可满足。平衡化使表达式高度 (O(\log s))，而不是把指数树藏在输入里。

完整三叉编译使用三类构件。`Rigid(H,S)` 的 (S) 有 (2^H) 个互异颜色；递归 children 为 `Rigid(H-1,A)`, `Rigid(H-1,B)`, `Rigid(H-1,A)`，任一 rainbow binary witness 必须取 (A) 与 (B)，故恰产生颜色集 (S)。`Dead(H,c)`（仅 (H\ge1)）的所有叶同色，任何 binary witness 取同色叶而失败。AND 先等高，再把两个输入和 Dead 放在新 root 的三个 children，迫使选择两输入并要求颜色集不交；Pad 以私有 Rigid 调高；OR 给两候选各加一个具有唯一共享 guard (g) 的 Rigid，第三 child 是完全 fresh 的 filler，选择两候选会因 (g) 冲突，选择 filler 加一个候选正好实现 OR。辅助色的全局新鲜规则、统一高度和每次构件的显式展开是归约成立和多项式规模的承重条件。

### NP 完全性和矩阵后果

见证只需在每个内部节点给出选中的两个 child，按完整树检查深度和 (2^h) 个颜色的单射性，故属于 NP。来源的构造给确定性位多项式的 3SAT many-one 归约，输出高度 (O(\log(s+2)))，节点数和颜色 ID 均为输入长度的固定多项式。它没有调用 Maximum Colorful Subtree 或 Group Steiner 的别的目标定理来替代证明；本形式与已知彩色选择编码相近，全球新颖性仍未认证。

对同一树构造普通 unrelated-machines 实例：每个 internal node 一台私有机器，每个颜色一台 resource machine；root pin 只有 root 的 unit 端；每条树边一个不同 task，父端时间 (1/3)，internal child 或叶颜色端时间 (1)，其它端无限。若有 binary rainbow subtree，将选中边的 unit job 下送，其余 jobs 留在父端，active internal load (1+1/3=4/3)，外机至多一件 unit，得 (C_{\max}\le4/3)。反向若完整调度 (C_{\max}<5/3)，每个带 incoming unit 的 active internal 至少下送两个 outgoing jobs，否则父端负载至少 (1+2/3=5/3)；资源端不能接两个 unit，于是递归抽出 binary rainbow subtree。任意根到叶路径给 (C_{\max}\le5/3)，故 NO 树的实际最优值为 (5/3)。这是该私有、可重复叶色、增长高度类的 ((4/3,5/3)) promise，间隙比 (5/4)，不足以支持一般 UM 近二困难性。

## 二、全局叶色重数 v2：2/3 的精确门槛

这里的重数限制是整棵输出树所有叶的全局颜色出现次数，而非只在某一见证中计数，也不是跨多个 state 的容量约束。颜色重数不超过 2 时，整棵三叉树总共有三个末层 child；按颜色出现次序把叶分成至多两个各自 rainbow 的叶类。raw (q) 的并集子可加性给 (3=q(L)\le q(A)+q(B))，所以某一类有 (q\ge2)，每个输入都存在 binary rainbow subtree。这个结论是存在性陈述，没有顺带声称一般树上已给出多项式寻找算法。

颜色重数不超过 3 时，来源重新定义 Dead：每个深度 (H-1) 父节点的三个叶用该父节点独有颜色，故每个 dead 色恰三次而没有 binary witness。新版 palette (R_H(S)) 的两个逻辑 children 是 (R_{H-1}(A)) 和 (R_{H-1}(B))，第三个是死构件；这样避免 v1 的 `Rigid` 复制 (A) 随高度增长的重数。protected guard 在每个 palette 中只出现一次，OR 的两个 option 共享 guard 后全局恰两次。逻辑子式只使用一次，不复制 DAG；atom、AND、OR、Pad 的所有辅助色都纳入全局计数。于是 3SAT 仍可归约到存在 binary rainbow，且每色全局至多三次；问题在 NP，故在该受限域中 NP-complete。其对应矩阵仍是 YES (C\le4/3)、NO (OPT=5/3) 的 (5/4) 比值。

这是一个实际 sharp 的局部门槛：

| 整棵树每色最大重数 | 结论 | 证据状态 |
|---|---|---|
| 2 | 所有显式输入都有 binary rainbow | raw (q) 子可加性与 occurrence 分桶 |
| 3 | 存在确定性 3SAT 归约，判定 NP-complete | 新 Dead/palette/AND/OR 全局计数证明 |

该门槛与现有 `私有菜单树有界叶重数配置界--定理` 的菜单/CONFIG 结果有关但对象不同：菜单定理允许多个 root、state 和跨 state 共享资源，v2 是单棵完整三叉树的全局叶色约束；不能把 v2 的 NP-hardness 直接换写成菜单定理的任意近二算法结论。

## 三、v1/v2 对齐张量和纯收缩：放大失败的精确范围

来源另立张量对象：若每个末层父节点的三个直接叶至多两种颜色，且 tuple 颜色按逐坐标相等编码，定义 (T^{[k]}) 为同深节点的有序 (k)-元组、逐坐标 child，分叉度 (d=3^k)。每个张量末层父节点的颜色集合是至多 (2^k) 个 tuple，因此 (q(T^{[k]})\le2^k)。若基树有 binary rainbow (F)，其 Cartesian product 给出满 (2^k)-叉 rainbow，故等号成立。

对任意完整 (d)-叉树 (U)，同一来源证明该私有矩阵满足
\[
  OPT(P(U))=2-q(U)/d.
\]
上界由给定 rainbow 子树的完整回填构造；下界从任意 (C<2) 调度抽出 (r=\lceil d(2-C)\rceil) 个真实下送 child，递归到叶并利用颜色 resource 至多接一件 unit。它是实际完整矩阵恒等式，不是把抽象 q 当作已知算法，也不适用于共享内部机器或改变任务端点的模型。

所以张量 YES 的实际值为 (2-(2/3)^k)。任意同域输入都有路径调度 (OPT\le2-3^{-k})，故若试图仅靠该张量操作给出 NO/YES gap，其比值至多
\[
 G_k=\frac{2-3^{-k}}{2-(2/3)^k},\quad G_1=5/4,
\]
并随 (k) 严格下降到 1。这里没有假设张量后的 NO 谓词仍保持；这只是对任何可能声称的 gap 的上包络。若 (k\ge2) 且 (k\mid h)，纯 k 层收缩而保留原叶色后，末层 macro-parent 至多含 (2\cdot3^{k-1}) 种颜色，严格小于 (3^k-1=d-1)，所以连已有 YES 输入也不能提供 strong ((d-1))-ary rainbow。收缩结论不适用于补齐高度、改色、跨副本加一致性或重编物理任务；这些必须另证。

该部分是三叉来源相对既有 `裸菜单读后与保值降度及调色板障碍` 的完整补足：既有页已把 v1/v2 的末层性质与 T1–T4 作为关联范围，但没有把本次领取的 fc5c 全文 v1 归约、v2 2/3 门槛、(G_k) 单调性和纯收缩边界作为当前来源的独立语义处置。现有 `单强制根树精确配置间隙` 已有更一般的 (OPT=2-q/d) 形式；本页保留 fc5c 对其在三叉彩虹编译族、重数和放大路线上的具体应用，不重复宣称一般定理。

## 四、树 Markov 再耦合：被反驳的合同与精确反例

### 合同的完整量词

输入满足：每任务恰两台可用机器、每机器对至多共享一个任务。给定一个真实全局 (T)-调度分布 (D)，以及机器图的连通生成树 (F)。只取完整单机配置分布和 F 上相邻机器对的完整配置联合分布，沿 F 按父状态条件分布做 Markov 树耦合；它保持单机边际和树边 pair 边际，却不承诺非树 pair 或更高阶交叠。对每个正概率的树耦合配置，只冻结 F 任务的分配并最优补齐非树任务。被反驳的是“每一个这样的正概率态都能补成 makespan 严格小于 (2T)”的全称合同。

### 五机输入和四态

取 (T=1)，机器为 (1,\ldots,5)，任务 (a,b,d,e,c)，其中树 (F) 是路径 (1-2-3-4-5)，树任务为 (a,b,d,e)，非树任务 (c) 只能放在机器 1 或 5。有限处理时间为

| task | 两个端点 |
|---|---|
| (a) | (p_{1a}=1, p_{2a}=1/2) |
| (b) | (p_{2b}=1/2, p_{3b}=1) |
| (d) | (p_{3d}=1, p_{4d}=1/2) |
| (e) | (p_{4e}=1/2, p_{5e}=1) |
| (c) | (p_{1c}=p_{5c}=1) |

真实分布 (D) 以概率 (1/2) 取调度 A 或 B：A 的配置为 (1:\{c\},2:\{a,b\},3:\varnothing,4:\{d\},5:\{e\})；B 为 (1:\{a\},2:\{b\},3:\varnothing,4:\{d,e\},5:\{c\})。两者 makespan 都为 1，任务 (c) 的单位处理时间给出 \(\mathrm{OPT}=1\)。

机器 3 始终为空，路径 Markov 耦合使左侧 ((a,b)) 分支与右侧 ((d,e)) 分支独立，因而四种左/右组合各概率 (1/4)。坏态是左 B、右 A：冻结 (a\to1,b\to2,d\to4,e\to5)，机器 1 和 5 的树负载都为 1，(c) 放任一端都使 makespan 至少 2，且达到 2。树边 pair 边际和全部单机边际仍与 D 一致；失效只来自丢弃非树兼容性，而不是原 D 不存在。

冻结正文还给出实际修复：把 (a) 从 1 移到 2，再把 (c) 放到 1，机器 2 的 (a,b) 负载恰为 1。因此反例只否定“任一再耦合态、冻结树任务、无迁移且严格小于 (2T)”合同，不否定择态、换树、迁移或保留更多相关性。

### 四台机器边界

在同一合同和模型下，至多四台机器的连通树是星或路径；存在覆盖所有树边的中心顶点或中央树边。中心配置或中央 pair 配置在真实 D 的某个支持态中出现，并决定每条树任务的端点方向：中心未取的任务只能在其唯一另一端。这个 D 支持态给出冻结树任务的 T 补全。因此五台是本具体合同的最小机器数边界。该正面边界不扩展到断开森林、每对机器共享多个任务或不来自真实全局 D 的 pair 数据。

现有精确程序逐一枚举 32 个合法完整分配，核对两个源调度、四个耦合态、所有树边 pair 边际、最佳 (c) 补全和坏态概率；数值使用 Fraction/整数，无随机抽样。有限枚举只验证该实例，不能升级为一般树 Markov 定理。

## 五、独有内容、证据去向和接续义务

| 来源 | 已保留的独有/精确内容 | 与已有成果关系 | 后续用途 |
|---|---|---|---|
| `fc5c...` | v1 完整 3SAT 到 Rigid/Dead/AND/OR 的三叉编译、全局重数 2/3 sharp 门槛、末层两色张量上界、(G_k) 单调下降、纯收缩 (d-1) 障碍 | 与 `单强制根树精确配置间隙` 的一般矩阵恒等式相交；与裸菜单页的 v1/v2 末层比较相交，但本页补足当前源全文 | 后续若研究 near-2 gap，必须另给 strong/weak 分叉和全局颜色一致性；不能把叶比例或张量当放大证明 |
| `9e66...` | 五机路径的全称再耦合失败、精确坏态概率 (1/4)、OPT=1 与补全=2、至多四机中心覆盖的正面边界 | 数学数据和代码审查已在既有 Markov reviews 出现；本页重新绑定当前正文 SHA/来源身份，不计重复程序为新证据 | 任何树边际算法必须保留非树兼容性、择态或迁移修复，并重新证明余量和位复杂度 |
| `2171...` / `72369...` | 当前源的主程序与精确结果 | 作为树反例的证据，不是主目标的 hardness 归约 | 保持在 `tools/evidence` 与第三阶段关系证据中 |

v1/v2 的 NP 完全性是受限树问题的条件完整证明，未认证全球新颖性、论文独立性或一般 UM 的 NP-hard gap。v2 的“重数 2 全 YES”没有给寻找 rainbow 的统一多项式算法；v2 的“重数 3 NP-complete”只在单棵完整三叉树和全局叶重数域内成立。张量部分不排除改色、非对齐操作、跨副本一致性、padding 或其它任务接口。树 Markov 反例不排除信息择态、重新选择生成树或允许迁移。两类来源不能合成一个主目标解答，均保持 `UM-TARGET-v1` 的开放状态。

本页没有将旧图关系直接导入为完成，也没有将重复的 legacy/main 版本或两条相同实例的审计结果重复计数为独立数学对象。后续第三阶段如建边，应分别建立“受限三叉彩虹归约 → (5/4) 调度承诺”“张量/纯收缩 → 放大失败边界”“树 Markov pair 边际 → 五机非树兼容性反例”三条有证据的解释关系，并保留量词与适用范围。
