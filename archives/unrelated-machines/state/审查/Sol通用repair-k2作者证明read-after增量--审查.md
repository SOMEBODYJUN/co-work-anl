---
id: "unrelated-machines/sol-general-repair-k2-author-proof-read-after-20261031"
kind: "review"
type_tag: "审查"
title: "Sol 通用 repair-k2 作者证明 read-after 增量"
status: "retained-exact-family-narrow-obstruction"
truth_status: "full-source-read-consistent-with-frozen-exact-first"
review_level: "full-source-read-and-cross-object-comparison"
summary: "对 18 台机器、17 个作业、34 个端点的 K=2 local-law 族，实际全文阅读作者 Proof read-after；七维 cube signed-law、全局 M2、raw localizer、逐机完整 row law、OPT=1 调度和跨行负三重矩均与已冻结 Exact-first 对象一致。该来源只强化指定 direct canonical pullback 的给定点障碍，不升级为一般 unrelated-machines 间隙或算法结论。"
source_refs:
  - "source:e6c573d8785724df9f5c:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_author_read_after.md"
legacy_ids:
  - "UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-v1-read-after"
related_objects:
  - "unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1"
  - "unrelated-machines/raw-k2-local-law-canonical-pullback-obstruction"
---

# 1. 阅读范围与版本身份

本源 `e6c573d8785724df9f5c` 已由 `clean show` 导出并逐行阅读。工作区副本为 70 行、7,271 bytes，SHA-256 `1ca2515b431457cb7301c26a325339e8a878ae51bd51ed99260f6fecb55903b1`；原作者证明在其首行给出的外部工作区文件为 8,131 bytes、122 行、SHA-256 `e9b2bba2cf3784e86ba9560ebddec0a520a7c51361f4af48358aa3f4c7eb467c` 的同一 read-after 记录（本页以可复核的 inventory 源 ID 和本地副本 hash 为准）。本页保存原字节于 `archives/unrelated-machines/tools/evidence/sol-general-repair-k2-author-read-after-20261031/original/`。

该文本是在 parent 先读完 151 行 Exact-first 重构后才释放的 Author Proof read-after；它不是 blind 独立复核，也没有把作者程序输出伪装成新运行。此前三源综合页已保存 Exact 规格、作者原 proof 和独立 Exact-first；本页只记录此次作者证明的新增读后核对，不重写旧结论。

# 2. 实例、量词与同一点对象

定义域仍为五组、十个 indexed roots、12 个 incidence、8 个资源、18 台机器、17 个作业和 34 个有限端点。对每个有理参数

\[
0<c<1,\qquad T=1+c,\qquad \varepsilon=1-c,
\]

所有系数为正，原 assignment endpoints 即使其 marginal 恒为 0 或 1 也保留；未加入 `export≤activation` 之类新逻辑，未删除 inactive state。selector 与 incidence 端在同一 Boolean substitution 中互补，one-hot、同作业排斥及至 degree 4 的恒等式均由 Boolean 商代数成立。

作者证明使用三位 `b_1,b_2,b_3` 和与 Exact-first 相同的单、双、三阶矩，故它仍描述同一个物理 instance 与同一个伪矩点。实际调度和伪矩点必须分开：作者后文给出实际峰值 1，而负值来自该点的跨行三重矩。

# 3. 新读到的全局 M2 证明

作者给出的七维 Gram/cube 证明与已冻结的对称块重构逐项一致。七个正权 cube 点为 000 及三个 singleton，各重 `35/160`；三个 doubleton 各重 `7/160`；111 权为 `-1/160`。其总和为 1，single、pair、triple moments 分别为

\[
\frac{35+14-1}{160}=\frac3{10},\qquad
\frac{7-1}{160}=\frac3{80},\qquad
-\frac1{160}.
\]

三位 degree≤2 polynomial 的三阶差分为零，因此

\[
q_{111}=q_{110}+q_{101}+q_{011}-q_{100}-q_{010}-q_{001}+q_{000}.
\]

七个正权点上的加权平方和记为 `S`。作者的 weighted Cauchy 常数为

\[
4(160/35)+3(160/7)=608/7,
\]

从而 `ell(q²)≥[1-(608/7)/160]S=(16/35)S≥0`；若 `S=0`，差分式把第八点也强制为零。由此得到 Boolean quadratic 的正定 M2，而不是只检查一个七维 principal submatrix。原 34 端点的所有 quadratic 都是该七维 span 的线性拉回，596 个 square-free degree≤2 单项均在合同内。此处仍允许全局三重单项为负；M2 不等于 global triple-literal positivity。

# 4. raw localizers 与逐机完整 CONFIG law

新增证明逐项核对两条特殊 slack：

\[
(1-b_1)+cb_2,\qquad b_1+c(1-b_3),
\]

其余为 `c` 或 `c` 加 Boolean literal。对任意全局 affine `q`，`zq` 是 degree≤2，且 Boolean 约化给 `L(zq²)=L((zq)²)≥0`；`0<c<1` 保证系数非负。因而所有 physical raw affine localizers 对全参数成立，未以有限网格或 SDP 输出代替符号证明。

作者给出的每行 membership law 与旧页的 `(35,21,21,3)/80` 完全相同，即 `(70,42,42,6)/160` 的缩放写法。M/0 行依赖 `(b_1,b_2)`，M/1 行依赖 `(b_1,b_3)`，其余行至多依赖一个位或常数；每行所有 endpoint 子集的 membership moments 因而都由该行真实 law 决定。负值不来自行内缺少 triple：三个负因子分属 M/0 private、M/0 的 `u` resource 和 Hs/0 private 三台不同机器。

特别需要保留的边界是：CONFIG law 逐行真实，并不拼成一个全局 schedule law；也没有给 activation localizer 免费增加全局三阶扩展。作者因此没有把本例升级为所有更强 global triple 合同也失败。

# 5. 实际调度与失败机制

作者的 `C=1` witness 选择 M/0、Hu/Hv fallback、Hr/Hs own；选中 incidence 导出到相应 unit resource，未选 state 保留 private，17 个 job 各执行一次，资源峰值为 1。unit selector 给出下界，所以实际 `OPT=1` 对所有 `0<c<1` 成立。

指定 direct canonical product 仍为 `b_1b_2b_3`，其值为 `-1/160`。state-0 quality polynomial 为 `cb_1b_2`，乘 Hs/0 activation 后值为 `-c/160`。这两个负值是跨三行的 canonical pullback 失败；它们不证明原排程不可行、近二 gap、SA1 不可行、一般 UM 算法不存在或复杂度下界。端点 `c=0,1` 也不在本对象域内。

# 6. 独有内容、去向与接续

本源独有的是作者 read-after 的完整七维 cube signed-law 推导、weighted-Cauchy 常数 `608/7`、逐机完整 membership law 的重复确认，以及作者明确区分“全局 functional / raw localizer / local CONFIG law / actual schedule”的文字边界。它没有新软件运行、没有新的 checker 或 SDP solver，也没有改变 Exact-first 的对象身份。

第三阶段可把本页作为三源综合页的“作者证明 read-after”增量边，并继续检查任何 K2→primitive-SA1 桥是否暗含跨机器 triple coupling。若桥只要求本页已满足的 raw/local 合同，direct canonical extraction 仍遇到 `-1/160` 与 `-c/160`；若桥增加 global triple 正性、改选 extraction 或重新求解，应作为新的量词与对象单独证明。
