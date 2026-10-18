# State-dummy SC 值桥：作者 Proof 实际 read-after 审查

审查对象：`weighted_menu_state_dummy_sc_value_bridge_proof.md`。

Proof SHA-256：`5decc348be346acd663478d1c13a768d0e7d06c407abacf593fc09018ff34665`，已实际读取全文并核 hash。

对应 Exact SHA-256：`ae57bf15737c54e6aadf8732869c242622ad75110facc2dbaed5fb8f7549320b`。

先前独立 Exact-only 记录 `weighted_menu_state_dummy_sc_value_bridge_independent_review.md` 的 SHA-256 仍为 `575a8d52e90779f8a3bb6c6e2496f1b890ad2383cd273e77012cbaa648d5557a`，本次复核确认原字节未变。顺序确为先独立重构并冻结，再经 root 授权读取作者 Proof；本记录另存，不覆盖旧记录。

**结论：Proof 在本次实际读取的值桥域内通过，无 standing fatal。** 作者各主要步骤与独立重构相符，没有使用分割 dummy、合并多 state bundles、删原 incidence jobs、C=2 资源唯一性、未知 OPT 规范化或 degree-two SC 后端等未获授权假设。没有复跑后端、软件或枚举。

## 1. §1 的 OPT_SC=V

前向对给定 disjoint B_g 选择一个最大 clause state，给其它 K_g−1 agents 各一不同 own dummy。所有 clause≤1，因此 dummy value 1 足以覆盖共同最低目标，得到 OPT_SC≥V。不是把 selected agent 与其它 state agent 合并。

逆向对任意实际 SC allocation，K_g−1 枚单 owner 不可拆 own dummies 最多覆盖 K_g−1 个本组 agents，必有一个 own-dummy-free agent；foreign dummies 值为 0，其 utility 就是实际 real bundle 的值。各组选中 agents 的 real items 不交，得到 V≥该 SC minimum。因为 real row 总量为 1，也同时给任意 SC minimum≤1。

K_g=1、dummy 浪费/外送/集中分配、零 real values、未用 items 和 full-partition 约定均被覆盖。Proof 没有从 utility 高低推断 dummy-free，而是使用实际 dummy assignment，方法正确。

## 2. §2 的完整原任务 accounting

资源 allocation 到 UM 的构造只选一个 selector state/group，仅导出该 state 中分配给该 group 的 resources 对应的原 incidence；所有其它原 incidence 留各自 private machine。不同 B_g 与 state 内资源无重复给 resource≤1 unit。未选 state 负载精确 1，选中 state 负载 2-a_gs(B_g)，且 selected loads≥1，故控制全部机器。

对 SC-decoded state，虽不必是其 B_g 的最大 clause state，但其自身值已≥t；保留它或重新取最大者都给同一 2-t 上界。Proof 的“same assignment”在两种阅读下都成立，没有在此处偷换不同 state 的质量。零 private job 是否导出不影响质量等式。

全部 n+I 枚原 jobs 各一次的 assignment 给出合法实际时间表：普通 UM 可逐机串行，不需额外释放时间、先后约束或资源匹配假设。

## 3. §3 的实际 schedule 逆变换和边界

实际 C<2 时，resource 上每枚 incidence 时间为 1，所以最多一枚。这是唯一需要严格小于 2 的位置。selector state 的全部 incidence 只可在该 state 或其各自 resource 执行，因此其 private load 正好为 2-a_gs(B_g)，给导出质量≥2-C。

未选 states 可能导出的 jobs 不妨碍所取 B_g 不交；把这些额外 exports 忽略于 SC 只是不使用对应 items，不删除原 UM 的存在性见证。由于 C≥1，其它 agents 的 dummy value 1 足以满足 2-C。

Proof 明确在 C≥2 不再应用 resource 唯一性，只构造非负零目标，故 C=2 容许双 unit 的边界没有漏洞。由 V≥0，C≥2 时下界 C≥2-V 本已成立；与 C<2 论证及前向构造合起来得到完整最优值身份，包括 V=0/OPT_UM=2 与 V=1/OPT_UM=1。

## 4. §4 的 target 与规范化范围

每给定 t∈(0,1]，UM≤2-t 强制实际阈值<2，可以逆变换；t=0 则分别由 SC 非负分配与 UM full-private≤2 处理。两边只在给定 assignments 时作多项式转换，没有优化算法。

Proof 正确区分每 SC row 的 real 总值 1 与 full 总值 K_g，也正确说明 supplied common T 只是全体 SC valuations 的共同已知倍乘。W≤1 时不能继续使用原 unaugmented V；需先 bonus-normalize 并在 augmented resources 重新定义 V。其引用先前 bonus 结果只是说明可选前处理，本值桥的证明本身仅依赖输入 W=1。

## 5. §5 的 binary/dense complexity

S agents、m real items、S-n dummies；dummy positive entries 恰 Σ_g K_g(K_g−1)≤S²；dense entries 恰 S(m+S-n)。所有计数由显式 states/resources/incidences 控制，值只复制原 binary rational 或写 0/1。没有以数值大小复制 item，也没有把二进制 K_g 当已显式列出的菜单。

给定分配的 dummy 扫描、real bundles 提取、最大 clause 扫描与 n+I 原 jobs 重建均为显式多项式操作，有理部分和的位长为多项式。不声称搜索最优 allocation 或枚举所有选择。

最后的 degree 警告正确：state-agent SC 中同一 real item 可以被同 group 多 states 正值，dummy degree 可为 K_g；原 group-degree≤2 不够调用 at-most-two-agents SC 算法。

## 6. §6 与本次认证边界

式 OPT_UM=2-OPT_SC 精确转移 YES≤1↔SC=1、NO>2-δ↔SC<δ；严格号方向正确。SC 的 1 与 1/2 阈值只给 UM 的 1 与 3/2 阈值，不给 near-two。作者明确不提供 hardness、任意外部 SC 的多项式反向 normalization、显式小菜单 source 或 all-state/partial-export NO 证明。

Proof 末尾提到的 separately frozen degree-three zero-cell cube embedding 并未在本次读取。其“保持 normalized UM optimum、因而保持 V”是条件性外围组合；本审查不独立认证该 embedding，也不认证即将合并到 canonical 的菜单规模障碍或其它未实际读取文字。

## 7. 冻结判定

**作者 Proof read-after 通过；旧 Exact-only 记录保持原字节。** 本次认证范围仅为本页开头 hash 的 Proof 主值桥及其直接阈值、规范化、复杂度说明。待收到实际 canonical 后才能对其新增同页内容另行审查。
