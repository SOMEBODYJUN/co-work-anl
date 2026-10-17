# 单根树重数精确 CONFIG gap：作者冻结证明读后攻击

内部研究者 pcsp_occurrence，仅 scratch；不修改 repo、Git 或 Work。

## 读取顺序与实际字节

先仅读 Exact 并自行完成全证明、独立下界族与 CONFIG 证书，冻结于
`single_pinned_tree_multiplicity_exact_gap_statement_first_review_pcsp.md`，SHA256
`b5ecdb360057776518e05cf9d38be5517ebcc13868bc1574e92708520cee410c`。
本次没有覆盖该稿。

在 first-review 已交 root 后，才实际全文读取作者冻结文件
`single_pinned_tree_multiplicity_exact_gap_author_proof.md`，读取前后 SHA256 均为
`10ff5f08b67f01de019ff5cdb328b1275d6c80b560d6095adfba8e06e86c7913`。
作者稿披露其构造来自 cover_consistency、全类上界来自 root；我的 first-review
自行重构了同一个最底层分组族，不能把作者构造来源倒写给我。

**读后结论：没有 standing fatal objection。** 本页没有亲跑新软件或重新认证旧软件，
没有新颖性认证。以下指出两处正文整理事项，均不构成数学反例。

## 逐段承重核验

1. **实际 P 与所有任务。** 作者 §1 的 I+L 计数正确：I−1 枚 internal edges、L 枚
   leaf edges、一枚 pin；每条原边 job 恰有 parent-small 与 child-unit 两个有限端，
   root pin 只有一个有限端。internal/颜色机器 namespaces 分离。把所有边留 parent
   确实给 C=2（root 为 pin+全部 d 枚 small，其他 internal 为1，颜色资源0）。

2. **CONFIG 最小阈值。** 有限配置负载集合给最小 T 取到，root pin 给 T_conf≥1。
   coverage≥1 /机器质量≤1 与恰覆盖1 /机器分布质量1 的等价，只用配置向下封闭删 job
   及 empty 补齐，不偷偷改变原 P。本文显式下界即使不调用这种归一化也成立。

3. **raw q 次可加。** §2 的例外 child 计数完整：若 b_i=q(A_i)，q_child(A_i)>b_i
   的 root children 至多 b_i 个；并集 Q 见证若 Q>Σb_i，必有一个被选 child 对所有 i
   都不例外，然后 child 高度归纳矛盾。空 bucket、重叠 A_i 均不妨碍。它没有把 q
   误称次模，也没有将叶密度当 branching。

4. **全局 µ 分桶与算法。** 按同色 occurrence 的次序分桶，每桶确为 rainbow；只创建
   实际 m≤µ 个 bucket。h-index DP 的 leaf sentinel d/0 用来允许任意 r≤d 在高度0
   终止，与高度≥1 的数学 q 定义一致。逐 bucket 求 q、回溯实际 r 树、再安排所有
   未选 edges 到 parent，均是显式输入位多项式，不计算一般 rainbow 最优值。
   µ 为巨大 binary 上界时仍只循环实际 m≤L；ceil(d/µ) 的比较是整数位算术。

5. **真实逐机负载。** §3 的三类机器回算都正确。inactive machine 的 parent edge
   没被选所以在其上游 parent，不能在它这里额外算一枚 unit；其全部 d outgoing small
   才留本机。active machine 恰一 incoming unit，余 d−r outgoing 留 parent；资源
   unit 数≤1。所有 original jobs 都已安排一次。

6. **独立下界族及 q。** §4 在每个底层 parent 内用 µ 大小的重复色 block，different
   parents 的 palettes 不交。每色在完整 ambient U 恰 µ 次，不是 per-state 重数。
   最后一层只有 b=d/µ 个颜色直接给 q≤b；选 b children/每 block 一叶给 q≥b。
   h=1 也完全适用，不需要不存在的中间层。

7. **整数 OPT 下界。** §4.2 对任何实际 σ 的低负载论证成立，而不是只审自家算法。
   若 C<2−b/d，每个 active internal 必有≥b+1 个 down jobs；逐层可达某个 active
   底层 parent，其 b+1 leaf jobs 只能去 b 个颜色资源，产生两个 unit 的 load2，矛盾。
   C<2 的门槛来自所设反证阈值，不是额外假设。

8. **完整 CONFIG 证书。** §4.3 每个 depth l row 的 active d 个配置质量 q_l/d，
   inactive 一个配置质量1−q_l，总和1。active 配置包括同一枚 incoming unit job 和
   恰一枚不同 outgoing small，load1+1/d；inactive 为原 d small，load1。
   每枚 outgoing parent marginal 为1−q_(l+1)，child marginal q_(l+1)，相加1。
   root pin q_0=1；颜色资源 µ 个 singleton 各 q_h，empty 1−µq_h≥0。
   重色叶没有被免费拆成多个资源；证书确实是逐机合法配置分布。

9. **T_conf 的匹配下界。** §4.4 在 T<1+1/d 时 active incoming unit 与任何正 small
   不相容。root pin 强制 root 每个正权配置含 pin，递归迫所有 tree jobs 的下端边际1。
   任意一个重复色的资源有≥2 unit jobs 各需边际1，而 T<2 每配置最多含一个，矛盾。
   该证明不依赖底层 block 结构，可用于 §5 的所有非 injective finite U。

10. **高度、上确界和不取到。** β^d<1/2 的二项式下界正确，h=d ceil(log2µ) 使
    µβ^h≤1（实际严格<1）。d 沿 µ 的正倍数趋∞，每个 finite U 合法且 gap 比趋于
    2−1/µ。非 injective finite U 有 T_conf≥1+1/d>1，而 OPT≤2−1/µ，所以比值
    严格小于该常数；injective U 的比值1也严格小于（µ≥2）。µ1 时 full d 树
    rainbow，OPT=T_conf=1。没有误把有限达到值与 supremum 混淆。

11. **位复杂度。** d/h 不以压缩参数展开承诺计时；显式树有 L=d^h 叶。证书支持数及
    job-incidences 按 I+L 多项式；q_l 有理分子分母位长 O(h log d)，d≥2 时等于
    O(log L)。全部 P 只有1/d与1处理时间。没有本页新增实现、有限试验或定理外审。

## 两处正文整理事项（非 fatal）

### A. 原 Exact 的全实例 OPT 等式应在 canonical 明列证明

Exact 第1项包括全部 U 的 `OPT=2−q_rainbow/d`。作者正文目前把全类 §3 写成上界，
而 §4.2 明列的下界只针对特殊底层 block 族。这不是反例：first-review §1 已独立给出
一般反向，且原 active-node 论证可直接补一句。对任意 C<2 实际 σ，每个 active node
至少有 `r=ceil(d(2−C))` 个 down children，从 root 递归抽 r 叉树，所有 selected leaf
jobs 的颜色资源至多一 unit，故 q_rainbow≥r，推出 C≥2−q_rainbow/d。
建议 canonical 显式加入这段，以使 Exact 每一 conclusion 都有正文承重。

### B. d=1 是作者稿额外的边界说明，不应静默改正式 Claim 的对象域

原 Exact 固定 d≥2，作者稿 §1/§2/§6 还说明 d=1。该额外边界本身正确：只有一叶，
沿全部 edges 下传给每台 internal 与该资源恰一 unit，OPT=T_conf=1；分桶/DP 也有效。
但若本轮只登记原 Claim，canonical 可保 d≥2 并把 d=1 放非正式补记；若要把它计入
正式对象域，应按仓库的版本规范明确表达，不能让文件之间不知不觉改变 formal domain。

## 限定结论

以上全是 single forced root、uniform d、整棵 ambient input 的颜色重数。作者 §6
正确区分旧多 root/multiple states 的 G(µ) 未知问题，未把本公式迁移过去。一般 s* 阈值
特化是已存在 unit-readout LP 方法的直接回收，本轮不新增 Claim 或扩大此稿结论。
本族可显式最优调度，CONFIG gap 不产生 NP-hardness，更不解决一般 UM 近2正反面。
