# 归一化菜单福利与配置证书双源审查

## 来源身份与实读范围

本页完整读取并比较两个冻结来源：

- `cbf196e3cb4d102a009e`，`research/current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md`，blob `2cca4e767eeec3b4016412993edd5ae993025d18`，SHA-256 `3c0919735dbc90793fe99336e24f3b15d37b09bb8e7e9e138c71437e08acff01`；
- `7d0842cc19e53d2607fe`，`research/current/unrelated_machines/normalized_menu_configuration_certificate_preservation.md`，blob `baef2fc383d3ca2f68a047465276443cd6d95e7b`，SHA-256 `1617f7913a5399ad062ba36506c54cfe3166b269d41f91426bfe432cd91cf10b`。

两源均冻结于 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）及 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。同时读取了归一化菜单、Santa Claus、配置证书、私有汇点和 finite audit 审查。第一源给出一个完整 gated 普通 UM 类的精确值和确定性 13/8 实际算法，并给 normalized robust source 的 LP 判别边界；第二源保持 machine CONFIG(1)、positive-support 状态 LP 与 state-dummy SC 证书，进一步给三度路径 normal form 和受限四次矩证书桥。两源都只覆盖明示的归一化菜单对象，未给一般 UM-TARGET-v1 或六人 SPE 证明。

## 一、归一化门控菜单的精确实际值

### 1. 对象和四层普通矩阵

组集 G 非空，资源 U 有限；每组有有限 indexed states，每个 state 的资源系数为非负有理数且总和恰为1，允许零 incidence、重复 states 和 unused resources。P_gate 包含根 R、每组 gate X_g、每 state private M_gs、每资源 Q_u；任务是根 pin J0、connector、selector 和 incidence。未选 state 的所有 jobs、零 incidence jobs 和显式 unused 机器都保留。

设真实不交 allocation 的 group value 为 state 在所领 bundle 上的系数和，W* 为最大总福利，β* 为最大化“覆盖组比例与最小组质量”的 balanced value。来源给出精确恒等式

OPT(P_gate) = 2 − β*。

从 β* 见证构造全任务调度：选中组 connector 放 gate、selector 放达到 state 的 private，所领正 incidence 导出资源机；未选 state 与全部其他 jobs 留各自 private。反向从任意峰值 C<2 调度读取在 gate 上执行 connector 的组 H，根负载给 |H|/n ≥ 2−C；selector 不能与 gate connector 同居，故每个选中 state 导出的真实资源质量至少 2−C；资源端在 C<2 时至多接一件 unit incidence，于是导出的 bundles 全局不交。C≥2 时回到 β*≥0 的平凡端点。J0 给 OPT≥1。

这一步严格依赖完整 P_gate 矩阵、单位 connector/selector 和 C<2 的资源独占；不能把它推广到原 flat 菜单、删掉未选 state jobs 或隐式拒绝任务。所有任务身份和零项必须留在正文，β* 与 W* 不是可免费调用的 oracle。

### 2. 福利 LP、确定性化和 13/8 保证

共同福利 LP 使用 z_gs、x_gsu：每组 z 和为1，0≤x≤z，每资源 x 总和≤1，目标 L = Σ p·x。有限有理 LP 给 W*≤L≤n。独立抽 state，再按 x/z 提议资源，固定资源由最大原系数提议者赢。初始每资源提议概率和不超过1，尾积分给期望福利至少 (1−1/e)L，严格大于 5L/8。

确定性化先逐组固定 state，再逐 incidence 固定 0/1 coin。福利用原系数的 distinct levels 逐级重算；条件化后提议概率和可能大于1，不能错误重用初始不等式，必须使用精确的有理公式。固定编号打平局，最终资源赢家互不相交，所有 state 与 incidence 都按输入位长显式处理。

把最终 group quality 排序，扫描 k 计算 beta_hat = max_k min(k/n, r_(k))，从而 W≤n(2 beta_hat−beta_hat²)。结合 W*≥n(beta*)²、福利舍入得到 C≤1+sqrt(1−5(beta*)²/8)，再以有理二次不等式证明

C ≤ (13/8) OPT(P_gate)。

该算法不输入真实 OPT、β* 或源 YES；13/8 是 scoped 上界，不声明锐性或新颖性。LP 的精确有理实现、所有原 jobs 和有限 support 证书的位复杂度需与有限浮点审计分开登记。

### 3. robust source 边界

对每个真实 allocation 定义高质量组数 h≥(δ)。NO 条件必须量化所有 allocation，并清楚区分“高组数小于 γ_hi n”与低质量比例；旧稿把 γ_hi 与低组下限混同的解读已撤回。支持 LP 在 unit-FSLP 完整 YES 下给 L=n；福利地板给低阈值 δ 的高组比例函数 f(δ)=(5/8−δ)/(1−δ)。更一般的近完美 YES/NO 由

(5/8)(1−η) ≥ γ_hi + (1−γ_hi)δ

的显式有理不等式分离。它是源判别条件，不是已完成的归约；不能把未知 OPT 当 decoder 输入，也不能把某个固定 ρ 的困难性解释为所有 ε 的否定。

## 二、完整归一化菜单的配置证书桥

### 1. FSLP 与完整 flat machine CONFIG(1)

对每 state 的正 support P_gs，FSLP 令 λ_gs≥0、每组 λ 和为1、每资源参与的 λ 总和≤1。给定 λ，在 private root 上以 λ 权重放 selector 加零 jobs，以 1−λ 权重放所有 positive incidence；资源机放每个 positive incidence singleton 配置并以 empty 补足。所有配置负载≤1，完整原 jobs（含零 incidence）覆盖恰一。

反向从完整 machine CONFIG(1) 读取 private 上含 selector 的权重 α_gs。selector 与 positive incidence 不能同处 private 合法配置，所以每资源端至少承担相应 α；资源机 unit 配置容量给每资源 Σα≤1。把 α 按组缩成和一的 λ，得到 FSLP。零 jobs 可以与 selector 同居，因此 FSLP 只计正 support；不能拿零项代替这一排斥论证。

### 2. normal form 与 state-dummy SC

来源把每组 states 嵌入 full binary tree，每个内部节点增加 own resource；沿树以流量向 children 和 own singleton 分配，保持旧正资源 support。反向用 root 到 leaves 的容量流恢复旧 λ，不假设只有一条路径活跃。随后将菜单路径转成 rowtotal≤3、item positive-degree≤3、正值只为1和1/D的 state-dummy Santa Claus 对象，保持 CONFIG 最高阈值和实际值。辅助路径属于既有 BCG 机制；本源的独有内容是这份归一化 flat 菜单证书的明确双向保持、零项边界与位长度记录。

该桥保持“给定有限有理证书”的可转换性，不提供配置证书搜索、任意阈值 CONFIG 保持或实际完整调度 law。CONFIG 的存在也不等于 integer YES：源给出完整 flat normal form 的显式族，CONFIG 阈值为1而 actual OPT=1/D，故配置 gap 近二；该族没有 integer perfect-completeness，不构成 hardness。

### 3. 受限四次矩路径合同

正文后段另立独立 ID，要求全局 Boolean degree-four functional、M2 正半定、每 job 精确 one-hot、每机器真实 CONFIG 的 first/pair 边际和 affine load localizer。对正资源 incidence 加 unit-resource path 与二状态叶，利用 quadratic null、pair exclusion 和 affine hole 变换，正向保持原矩与 private CONFIG；反向由相邻叶 selector/heads 的 null 关系证明同一旧 resource 的不同原 jobs 成对互斥，再重建 singleton/empty CONFIG 和 load localizer。

这一合同只保持明示 raw 四次矩证书，量词是给定有限有理证书间的确定性转换，T 在1≤T<2的 scoped 区间内。它不等于任意 SOS/SDP 可行性算法，不提供共同完整调度 law，也不把弱 CONFIG 证书或有限软件结果升级为更强的 gap 定理。多个核心的共同可实现性仍是开放缺口。

## 比较、证据和处置

第一源独有的是 P_gate 的 OPT=2−β* 精确桥、福利 LP 的 13/8 实际保证、确定性化位复杂度和 normalized robust source 的 γ/δ 修正。第二源独有的是 FSLP↔完整 machine CONFIG(1) 的正 support 双向证明、binary-tree/menu-path normal form、三度 state-dummy 证书，以及有限 raw K2 矩路径的 pair-null 保持。

两源共同说明：完整矩阵和所有未选 state jobs 的任务身份必须保留；分数配置边际可以精确传输，却不能自动给 integer perfect completeness 或全局调度分布。有限 Fraction/LP、CONFIG lists、审计脚本和路径重放只作证据，不能替代一般量词证明；外审、全球新颖性和软件生产实现均未认证。

两源均 `integrated`。后续 mapper 应检查是否真的满足 norm1、正 support、完整资源容量、all-allocation NO 和证书给定条件；若使用 robust source，必须另证可靠 YES/NO 编译和实际解码，不能把 13/8 scoped 算法推广成一般 UM。六人 SPE 客户目录、六提供者完整历史、终局均分和任意平局语义不在本对象内，SPE 覆盖目标与 UM-TARGET-v1 继续开放。
