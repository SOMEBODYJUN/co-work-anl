# State-dummy SC 精确值桥：独立 Exact-first 审查

对象：`weighted_menu_state_dummy_sc_value_bridge_exact.md`，ID `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`。

Exact SHA-256：`ae57bf15737c54e6aadf8732869c242622ad75110facc2dbaed5fb8f7549320b`。

读取顺序：本次只读取上述 Exact 并核 SHA；未读取作者 Proof，未向作者或其它 agent 寻找 Proof，未读取其它审查者证明。以下是独立量词/分配/复杂度推导。未运行软件或有限枚举；只在 scratch 写本记录，未修改 repo、Work、Git。

**判定：Exact 通过。** 在完整显式 flat normalized 域中，OPT_SC=V、OPT_UM=2-V 及给定分配的双向转换成立。未发现 dummy、零值、K=1、V=0 或 C=2 的漏洞。不把结论解释成求最优值的算法或外部 source gap。

## 1. 基础域和端点

G 非空，每 group 菜单非空，所以 SC agents 总数 S≥n≥1。每 state private 总和精确为 1，故每 state 至少一个正 incidence；允许零 incidence 和重复内容但不同 index 的 states。每条 clause 的全资源总和是 1，因此任意资源子集 B 上 0≤a_gs(B)≤1，进而 0≤f_g(B)≤1、0≤V≤1。

原 UM 中每 group 的 selector 时间为 1，故 OPT_UM≥1。把所有 incidence 留各自 state，再把 selector 任放本组一 state，所有未选 state 负载 1，选中 state 负载 2，因此 OPT_UM≤2。所有 assignment 选择有限，相关最优值均达到。

没有 resource-degree 限制不妨碍这里的值恒等式：共享冲突由真实 item 的唯一 owner 和 C<2 下真实 resource 的单位容量控制，而不是由局部度数控制。

## 2. Resource allocation → SC

给任何 pairwise disjoint B_g。对每 g 扫菜单选 s(g) 达到 f_g(B_g)。给该 agent B_g 的真实 items，再把 K_g−1 枚不同的 group dummy 一对一给其它 state agents。

选择 agent 的 utility 是 f_g(B_g)。每个其它 agent 至少有其 dummy 的 value 1。由于所有 f_g(B_g)≤1，整份 allocation 的 minimum≥min_g f_g(B_g)。各真实 item 至多给一次，dummy 也各用一次。未用资源可不分配。

K_g=1 时无其它 agents、无 dummy，构造仍然直接成立。state 内零 incidence 只给真实 item 零贡献，不改变有效性。重复内容 states 仍是不同 agents，不合并。

对达到 V 的资源 allocation 应用此构造，得到 OPT_SC≥V。

## 3. SC → 一个 state/group

给任意合法 SC allocation，记实际 minimum utility 为 t≥0。一个 group 有 K_g 个 agents，但只有 K_g−1 枚自己 group 的 dummy，每件不可拆且至多一个 owner。即使 dummy 被浪费、给外组或集中给同一 agent，接到至少一枚 own-dummy 的本组 agents 仍至多 K_g−1。因此必有一个 b_g,s(g) 没接任何 own-dummy。

其它 group 的 dummy 对该 agent 全为零，所以其全部正 utility 都来自它实际接到的真实 items B_g。其真实 row 全资源总量为 1，故

    a_g,s(g)(B_g)=utility(b_g,s(g))≥t，且 utility(b_g,s(g))≤1。

这同时证明任何 SC allocation 的 t≤1。不同 g 选出的 agents 不同，真实 items 原本每件至多一个 owner，因此 B_g 两两不交，且 f_g(B_g)≥a_g,s(g)(B_g)≥t。没有拼接同一 group 的多个 state agents 的 real bundles。

于是 V≥t，对 SC 最优 allocation 取 t=OPT_SC，得 V≥OPT_SC。与上一节合并即 OPT_SC=V。

**不可拆性是实质条件。** 此处不能把 K_g−1 枚 unit dummy 的总价值平均给 K_g agents；若允许共享，pigeonhole 结论失效。当前 Exact 明确禁止共享，故无此漏洞。也不能把这些 dummy 当一枚 value K_g−1 的 item，因为前向要给 K_g−1 个其它 agents 各一枚。

## 4. SC → 完整原 UM

使用上述 dummy-free agent 的 state s(g) 与 B_g。把 selector 放选中 private state；导出该 state 中资源属于 B_g 的原 incidence，零 private job 可选择不导出；所有其它原 incidence——尤其所有未选 state 的任务——都留其原 private state。

每枚 selector 和每枚 incidence 都有且仅有一个原合法端。不同 B_g 不交，且 state 内 resource 身份无重复，所以任何 resource 最多一枚导出的 unit job，负载≤1。未选 state 的全部原 private 工作正好为 1。选中 state 导出的 private mass 是 a_g,s(g)(B_g)，故其负载为

    1+(1-a_g,s(g)(B_g))≤2-t。

因 t≤1，resource 负载 1 和未选 state 负载 1 也≤2-t，得到完整峰≤2-t。去掉零 private job 的导出不会改 private mass，且只减 resource 占用。没有删原 job、复制原 resource 或实现多个 selector states。

选中 state 的 private machine 可先运行 selector、再串行运行留下的 incidences；其它机器依固定顺序串行，即得实际非抢占时间表，位复杂度由有理部分和控制。

## 5. 完整 UM → SC：严格区分 C<2 与 C=2

给任意合法完整 UM schedule，其实际 C≥1。若 C<2，则每台 resource 不可能容纳两枚时间 1 的 incidence。取每 group 的 selector 实际 state；其中所有 private incidences 的原总工作是 1，故该 state 当前负载是

    2-(导出到resource的private mass)≤C。

因此导出 private mass≥2-C。记录这些选中 states 实际导出的资源为 B_g；由所有 resource 的真实 unit 唯一性，B_g 跨 group 不交。其它未选 states 也许导出了原 jobs，但可在 SC 里忽略其占用，不影响 B_g 的合法性。

把 B_g 的 real items 给对应原 selector-state agent，给其余 agents 各一 own dummy。该选中 agent 的 utility≥2-C，其它 agents 的 dummy value 1≥2-C（因为 C≥1），故 SC minimum≥2-C。这里不假设实际 UM 原 schedule 是某种 all-or-none state 模式。

若 C=2，resource 可能有两枚 unit，不能沿用上面的正目标提取；若 C>2 也不提取。此时任意 SC allocation（包括全留空）的 minimum≥0，正好满足 max(0,2-C)。Exact 已明确单列这一边界。

### 值恒等式与 target iff

由最优 SC 到 UM 得 OPT_UM≤2-OPT_SC=2-V。若 OPT_UM<2，用上述正目标逆变换得 OPT_SC≥2-OPT_UM，即 OPT_UM≥2-OPT_SC。若 OPT_UM=2，则所需下界 2≥2-OPT_SC 由非负性已成立。合起来得到精确等式。

对给定 t∈(0,1]，SC minimum≥t 给 UM≤2-t；UM≤2-t<2 给 SC≥2-C≥t。t=0 时，两边分别由非负 SC 空分配及 UM full-private 峰≤2 保证。它是存在性及 assignment 转换等价，不含判定器。

## 6. 零值与 K=1 的显式核对

- K_g=1：没有 dummy，唯一 agent 自动 dummy-free；两个方向退化为该 state 的真实 clause，全部成立。
- V=0 / SC OPT=0：两个单-state groups 只共享一个 private-weight-1 resource 即为概念例。一个 real item 不可同时给两 agent，所以 minimum 为 0；原 UM 不可能低于 2，但全 private 达到 2。此为纯推导示意，未运行枚举。
- V=1：最优资源 bundles 的每组选中 clause mass=1，SC 可把其它 agents 以 dummy 填到 1，UM 全选中 incidence 正工作导出后峰 1。
- 零 incidences：可能出现在 resource bundle 中但不增加 mass；SC 可留零值 items 不用，UM 零 private jobs 留原机。没有通过忽略零值而删除原任务身份。
- full SC partition：把任何未用 item 任分给一个 agent，只会增加非负 utility，故其最优值与“at most one owner”约定一致；这不授权分割 item。

## 7. 规范化、source gap 与 degree 边界

SC state-agent 的真实 item row 总和是 1，但它还给 K_g−1 枚 own dummies 各 value 1，所以 full row 总和是 K_g。不能把该构造误标为 full-row-total-1 SC。

共同输入单位 T>0 的整体缩放只将 SC OPT 乘 T；它不改变 UM，也不提供任意外部 SC 的 optimum normalization。对原 W≤1 菜单可先做 private bonus normalization，但 V 必须在 augmented resources 上重定义。例如空/零工作原 state 的原 V=0 与其 UM OPT=1 显然不能直接套 2-V；Exact 已正确禁止这种偷换。

每固定 δ∈(0,1)，UM YES≤1 等价于 V=1/SC OPT=1；UM NO>2-δ 等价于 V<δ/SC OPT<δ，严格方向无误。SC gap 1 vs 1/2 只给 UM 1 vs 3/2，不能自动升级成 near-two。任意外部 SC 反向列出 target bundles 可能指数大，当前没有声称这样的多项式反向归约。

本 SC 的 agent 是各 indexed states；一个 real item 可以被同 group 很多 agents 正值，一个 dummy 的正 degree 是 K_g。原 resource group-degree 小不意味着新 SC agent-degree≤2，不能直接套 VW degree-two 后端。Exact 已清楚区分。

末段另提 degree-three zero-cell cube embedding 是对单独冻结合同的条件性组合。本次没有读取或审查那份外围 embedding，也不据此认证任何 degree-three source 或 hardness。当前 Exact 的值桥本身不依赖它。

## 8. 精确 counts 与 binary/dense 位复杂度

UM 有 S+m 台机器、n+I 枚原 jobs。SC 恰有 S agents、m 个 real items、Σ_g(K_g−1)=S−n 个 dummy items。每原 incidence 对应一个 state-real valuation entry，最多 I 条非零或显式保留 entry；dummy 非零 entries 恰为 Σ_g K_g(K_g−1)≤S²。Dense matrix 则恰有 S(m+S−n) 个 entries。

所有 entries 为 copied binary rationals、0 或 1，没有数值复制造成伪多项式展开。因为 menus/resources/incidences 都显式列出，S、m、I 均由原输入长度控制，S² 和 dense count 仍为多项式。若只有二进制 K_g 而未列 states，不能引用此界；当前域明确排除这种简写。

各 assignment 转换只需扫描输入 allocation、当前 dummy owners、菜单及全部原 jobs。选 dummy-free agent 按实际归属计数，不能只看其 utility 大小；给定 B 的最大 clause 用显式有理求和。每输出开始时间为输入有理数的有限部分和，数值位长为输入与给定 allocation/target 表示长度的多项式。没有把寻找最优 V 或最优 SC 偷放进转换。

## 9. 冻结结论

**Exact-only 通过，暂无 standing fatal。** 已独立闭合全部主身份、所有给定 allocation 转换、C=2/zero target、K=1、零 private times、V=0，以及 explicit sparse/dense counts。未读 Proof；可在本记录冻结后再交付 Proof 做独立逐步核验。
