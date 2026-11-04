---
id: "unrelated-machines/shared-ud-tiny-state-potential-and-19-over-10-completion"
kind: "candidate-proof"
type_tag: "证明"
title: "共享 UD tiny 状态势与 19 比 10 回填"
status: "scoped-candidate; independent-review-and-end-to-end-implementation-pending"
truth_status: "author-proof-chain-with-versioned-conditional-domains"
review_level: "author-proof-self-audit-and-informed-version-read; no-fresh-blind-audit"
summary: "在单态 outer、互异 home、shared-B fallback 与 B-only exact-threshold-UD 叶的显式结构域中，作者候选用 profile 势、稳定 matroid 交换、Frank–Wolfe 和 prefix-flow 回填声称 19/10；各 k⁴、k² 与 v5 版本保持独立量词，尚未升级为一般 unrelated-machines 定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_author_self_audit_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_O1k_v5_final_actual_read_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_shared_ud_k2_refinement_informed_audit_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_19_10_independent_exact_first.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_19_10_independent_exact_first.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_19_10_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_19_10_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_v4_append_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_shared_ud_tiny_state_potential_v4_append_actual_read.md"
evidence_manifest: "../../tools/evidence/shared-ud-tiny-potential-20261031/manifest.json"
legacy_ids:
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1"
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4b"
  - "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v5"
---

# 1. 对象、输入和版本

这是共享 UD 叶的 **state-profile 势证明合同**。它恢复下述显式结构域中的对象、量词及算法接口，保留原作者证明链的版本身份；原件中的独立重构、作者读后与有限软件证据分别使用。无额外叶的 SA1/CDF/MW 算法见[多 outer 原算法合同](../审查/多outer%20single-state%20tiny-home%2019-10%20Exact-only与proof-canonical-backend版本审查--审查.md)，两者不能因都写作“v1”而合并。

输入是有限、完整显式的 normalized menu $Q$。每组有非空的 indexed states，每个 state 是资源上的非负二进制有理向量，系数和为一。$k\ge1$ 是输入变量，不是固定常数。

- Outer $O_i$ 恰有一个 state，正支持是 $g_j$（$j\in J_i$），权重 $w_j>0$、$\sum_{j\in J_i}w_j=1$。所有 homes $g_j$ 全局物理互异，$\nu=\max_jw_j$。
- 每个 home 恰有一个 helper $H_j$，有自己的 unit-singleton state；其余原 fallback states 的正支持只在公共资源集 $B$。$B$ 与 homes 不交，各 helper 的 fallback 支持可任意重叠；无 fallback 的 helper 仍保留 own state。
- 额外 leaf groups 的正支持也只在 $B$。固定 $\varepsilon=15/16$，令

$$
E_\ell=\{u\in B:\max_s p_{\ell su}\ge\varepsilon\},\qquad
b_\ell=\max_s\sum_{u\in B\setminus E_\ell}p_{\ell su}.
$$

要求 $b_\ell<\varepsilon$。因此对任意 bundle $A$，该叶的原菜单值至少 $\varepsilon$ 当且仅当 $A\cap E_\ell\ne\varnothing$：一个 $E_\ell$ 元素提供达到阈值的原 state；不含这种元素时，每个 state 的整条尾巴都小于阈值。这是 whole-menu 的 exact-threshold UD 条件，叶本身可以有多个非 singleton states。叶资格图无完整匹配的输入也在域中，算法必须处理。

每个 indexed state/resource pair 至多一个 listed incidence。显式零 incidence、重复 indexed states、unused resources 全部保留；零系数不参加正支持判断，仍是原普通调度的 jobs。不存在其余任意类型的 groups，不给 actual target、OPT、联合 law、可行 LP 点、profile 或调度 oracle。

版本的 home 条件与算法如下，不能迁移常数或软件身份：

| 来源对象 | 额外叶 | home 条件 | 算法与区别 |
|---|---|---|---|
| 原 multi-outer Exact `38c85f…` / proof `ce05c7…` | 无 | $\nu\le1/(4096k^4)$ | SA1、请求 winner、MW、双资源矩条件期望；不由本页的曲率放宽 |
| shared-UD Exact `80fd4f…` / proof `409ce8…` | 上述 UD 叶 | $\nu\le1/(4096k^4)$ | 本页 §3–5 的 profile 势；$k=1$ 用实际 $\lambda_{\min}$ 单独付款 |
| shared-UD 中间 $k^2$ 扩域 | 同上 | $k\ge2$ 时 $\nu\le1/(16384k^2)$；$k=1$ 仍 $\nu\le1/4096$ | 同一 profile 势的曲率重估；知情核查不改成独立首读 |
| shared-UD v4/v4b | 同上 | $k\ge2$ 同一 $k^2$ 界；$k=1$ 无 tiny 限制 | $k\ge2$ 用 profile/FW/prefix-flow；$k=1$ 改用 §6 的整数 greedy |
| shared-UD v5 的 actual-$I$ 版本 | 同上 | $k\ge2$ 时 $\nu\le1/(1024k)$；$k=1$ 无 tiny 限制 | 相对曲率与分段 reciprocal 势，直接维护整数集合 $I$；不是把旧 FW 界换一个 $\nu$ |

v4 另有以实际 allocation 为状态的独立构造，保留在[既有 v4 资料](../资料/shared-UDtiny-home-v4势函数与完整回填--资料.md)及其原件；上表 v4 行列的是本页复用的 profile/FW 证明。独立构造的势常数、实际集合和停止界继续按其原版本使用，不能与本页的分数 profile 中间量互换。

各版本目标均为：对该版本域内每个完整 $Q$，由一个固定确定性总位多项式算法输出全部原 jobs 的原有限端点 assignment $\sigma$，使 $C_{\max}(\sigma)\le(19/10)\operatorname{OPT}(P(Q))$。本页不把某版作者证明的身份升级为一般 UM 定理或端到端软件实现。

# 2. 完整普通矩阵、值桥与叶匹配

每个 indexed state 建一台独立 private machine，每个资源建一台 resource machine。每组一枚 unit selector，可去该组全部原 state-private machines；每个 listed incidence 是不可拆 job，在自己的 private 上时间为原系数、在指定 resource 上时间为一，其余端点不合法。若 groups、states、incidences、resources 数为 $G,S,I,U$，则矩阵有 $S+U$ 台机器、$G+I$ 个 jobs、$S+2I$ 个有限端点。所有未选 state payload、零 jobs 和重复 states 都在这个计数及输出中。

令

$$
V=\max_{\text{各组 bundles 两两不交}}\min_g\max_s\sum_{u\in A_g}p_{gsu}.
$$

有限输入保证最大值达到。完整矩阵满足

$$
\operatorname{OPT}(P(Q))=2-V,\qquad 0\le V\le1,\qquad 1\le\operatorname{OPT}\le2.
$$

正向给每组选择一个 attaining state，selector 放其 private，将该 state 在所领 bundle 上的正 incidence jobs 送到对应 resource，其余全部原 jobs 留在自己的 private。资源负载至多一，未选 private 至多一，所选 private 至多 $2-V$。反向若完整调度峰值 $C<2$，每个 resource 至多有一个 unit incidence；只读取每组 selector 所在 state 的输出资源，得到同一组两两不交 bundles，值至少 $2-C$。若 $\operatorname{OPT}=2$，正向式迫使 $V=0$；unit selector 给下界一。这里没有用分数 profile 替代实际调度。

若 leaf—$B$ 图 $\ell\to E_\ell$ 无完整匹配，则任意所有组值至少 $\varepsilon$ 的实际 allocation 都会导出这种匹配，矛盾。因此 $V<15/16$；把所有 incidence 留 private、selector 任放合法 private 的完整 baseline 有 $C\le2$，比率严格小于 $32/17<19/10$。

以下假设完整叶匹配存在。$B$ 上的 vacancy matroid 定义为

$$
X\in\mathcal M\iff\text{全部叶可匹配到 }B\setminus X.
$$

它是叶—资源 transversal matroid 的对偶，允许零秩和 loops；独立性由普通二分匹配判断。所有 helpers 共用这一个剩余资源条件，不能为不同 outer 各复制一份叶匹配。

# 3. 固定 profile 的线性 oracle 与真实共同参考

Profile $A$ 给每个 helper 选一个原 fallback state 或 empty。只分配 $B$，同时完整匹配所有叶，每资源至多一个 owner；此时还不分配 homes，也不要求每个 helper 达到阈值。令

$$
Q_j=\sum_u p_{j,s_j,u}x_{ju},\qquad
W_i=\sum_{j\in J_i}w_jQ_j\in[0,1].
$$

固定 profile 的分数可行域是普通 ownership/leaf-matching 网络：叶行恰为一，资源列至多一，helper claims 无额外下界。它是整数网络多面体。对 $\lambda>0$，令 $f_\lambda(A)=\max\lambda\cdot W$。置 $t_u=\max_{j\text{ active at }u}\lambda_{i(j)}w_jp_{j,s_j,u}$（空最大值取零），则

$$
f_\lambda(A)=\sum_{u\in B}t_u-
\min_{\text{完整叶匹配}}\sum_{u\text{ 被叶匹配}}t_u.
$$

一次普通最小费用完整匹配即可求值并输出整数 allocation。等价地，可在 $\mathcal M$ 的资源平行扩张上做 weighted matroid greedy；零 dummy 补足 basis。这个 oracle 只优化**已给定 profile**，没有优化指数多个 state profiles。

把每个 fallback option 看作 candidate copies 集，weighted matroid rank 的次模性给 $f_\lambda$ 在 option 集上的单调次模性。非 profile 集可在分析中含同一 helper 的多个 options；$Q_j\le1$ 及后述大小界只用于合法的一 helper 一 option profiles。

若真实 $V\ge\varepsilon$，从同一次实际 allocation 得到一个共同 profile $O$，对所有 $\lambda>0$ 同时有

$$
f_\lambda(O)\ge\varepsilon^2\sum_i\lambda_i.
$$

理由是 outer 取走的 home 权重至少 $\varepsilon$；失去 own home 的 helper 必须使用值至少 $\varepsilon$ 的 fallback。保留这些 helper bundles 和每叶的一枚 $E_\ell$ 资源即可，它们仍两两不交。这个 $O$ 仅在进展／失败判定的反证中存在，算法不输入也不枚举它。

# 4. Profile 势、曲率及可执行停止条件

令 $H=\sum_i|J_i|$，取

$$
c=\frac5{16},\quad\theta=\frac1{32},\quad
\xi=\frac1{2^{20}H^2},\quad\tau=\frac1{2048H},
\qquad
\Phi(W)=\frac\theta k\sum_iW_i-\sum_i(c-W_i)_+^2,
\quad P(A)=\max_{W\text{ 在 }A\text{ 可行}}\Phi(W).
$$

在精确最优点 $W^*$ 处，$d_i=(c-W_i^*)_+$、$D=\sum_i d_i$、$\lambda_i=\theta/k+2d_i>0$。一阶最优性给 $f_\lambda(A)=\lambda\cdot W^*$，并且

$$
P(A)-\Phi(\widehat W)\ge\|d(\widehat W)-d(W^*)\|_2^2.
$$

精确 $W^*$ 只作分析。稳定交换引理说：替换一个 helper $j$ 的 state，$\Delta_j=f_\lambda(A')-f_\lambda(A)$，任意旧 $\lambda$-optimal fractional 点均能耦合到一个新 optimal 点 $W'$，满足

$$
\lambda\cdot(W'-W)=\Delta_j,\quad
\max_i|\lambda_i(W'_i-W_i)|\le\lambda_{i(j)}w_j,\quad
\sum_i|\lambda_i(W'_i-W_i)|\le2\lambda_{i(j)}w_j.
$$

整数 basis 的证明先删旧 $j$ copies、再加新 copies：删除时其它 helpers 只增、总 weighted 增益至多旧 $j$ 值；插入时其它 helpers 只减、总损失至多新 $j$ 值。聚合时包括与 $j$ 同 outer 的其它 helpers。对同一 optimal face 的整数分解逐项更新再平均，得到分数版本；算法不用显式求这份耦合。于是二次余项与跨 profile 进展满足

$$
B_j=2\left(\frac{\lambda_{i(j)}}{\lambda_{\min}}\right)^2w_j^2,
\qquad P(A')-P(A)\ge\Delta_j-B_j.
$$

对共同参考 $O$ 的单 helper 替换求和，次模性给 $\sum_j\Delta_j\ge f_\lambda(O)-2f_\lambda(A)$。若 $V\ge\varepsilon$，则

$$
\sum_j\Delta_j\ge\frac{65}{128}D-\frac{287}{8192}.
$$

由每 outer 的 $\sum_jw_j^2\le\nu$，只用 $\lambda_{\min}\ge\theta/k$ 已得

$$
\sum_jB_j\le2\nu k+
\left(\frac{8\nu k}{\theta}+\frac{8c\nu k^2}{\theta^2}\right)D.
$$

当 $k\ge2$、$\nu\le1/(16384k^2)$ 时，右侧至多 $1/16384+(21/128)D$，原 $k^4$ 域也满足此界。因此 $D\ge9/80$ 时总进展至少

$$
\frac{11}{32}D-\frac{575}{16384}\ge\frac{293}{81920}=:\rho>0,
$$

某单 helper 替换便有 $P$ 增益至少 $\rho/H$。旧 $k=1$ tiny 分支须用实际 $\lambda_{\min}=\lambda_1$，得 $\sum_jB_j\le2\nu\le1/2048$；不能套用粗 floor 付款。v4 无 tiny 的 $k=1$ 使用 §6 的另一分支。

**可执行评价。** 每个 profile 从 $W=0$ 和完整叶匹配开始，以步长 $\gamma_t=2/(t+2)$ 做有理 Frank–Wolfe，每步调用 §3 的线性 oracle。固定执行 $\lceil4k/\xi\rceil$ 步，返回可行 $\widehat W$ 及 $\widehat P=\Phi(\widehat W)$，有 $P-\xi\le\widehat P\le P$。初始匹配、平局、次数固定，故 $\widehat P(A)$ 是确定函数。

从全 empty profile 开始：若全部 $\widehat W_i\ge25/128$ 则取整；否则枚举所有原 helper options 加 empty，接受使 $\widehat P$ 至少增加 $\tau$ 的最佳替换；无此替换则输出完整 baseline。若此时 $V\ge\varepsilon$，某 $\widehat W_i<25/128$ 与 deficit 稳定式迫使精确 $D>9/80$，进而有候选提升至少 $\rho/H-\xi>\tau$，矛盾。因此失败分支确有 $V<15/16$，并非由某个局部线性查询失败直接宣布实际不可行。

$-kc^2\le P\le\theta$，故接受次数 $O(kH)$；每轮候选数至多原 fallback states 数加 $H$。FW 每次评价 $O(kH^2)$ 次普通匹配。若原 payoff 产品取公共分母 $D_1$，$t$ 步后的 vertex 权重为 $2(r+1)/(t(t+1))$，flow 分母可取 $t(t+1)$、payoff 分母可取 $D_1t(t+1)$。运算位长随输入长度多项式增长，不按原分母数值循环，也不把 exact profile/QP/SDP 最优值当 oracle。完整推导保存在[原 profile 证明](../../tools/evidence/shared-ud-tiny-potential-20261031/source/e2370ab75fef1534990c.md)及[v4 规范追加 §14–18](../../tools/evidence/shared-ud-tiny-potential-20261031/source/0eb8b34fa84864a54169.md)。

# 5. 一张 prefix-flow 与全部原 jobs 回填

成功 profile 有全部 $\widehat W_i\ge25/128$。定义 $a_{iu}=\max_{j\in J_i}w_jp_{j,s_j,u}$，empty 不提供 candidate，空最大值取零。则 $0\le a_{iu}\le\nu$、$\sum_u a_{iu}\le1$。把同 outer 在每资源上的分数 claims 合并并交给取得该最大值的 helper，只会增加 payoff，仍保留所有叶行与共享资源容量。

每 outer 按 $a_{iu}$ 降序排列正边 $u_1,\ldots,u_m$，令 $F_\ell$ 为前 $\ell$ 个资源的分数 claim 总数。要求整数前缀 count 至少 $\lfloor F_\ell\rfloor$：用 nested-prefix 链表示这些下界，每个资源边容量一；把每叶的“恰匹配一次”与同一资源容量一并放入**同一张**整数 lower-bound circulation。原分数流见证可行，流整数性同时给所有 outer 的整数 claims 与一份完整叶匹配。不能逐 outer 独立取整后再拼。

分部求和将所有前缀少于一的 count 损失加权望远镜化，得到每 outer payoff 损失至多 $\max_u a_{iu}\le\nu$。故旧 tiny 分支及 v4 的 $k\ge2$ 分支中

$$
W_i\ge\frac{25}{128}-\nu\ge\frac{799}{4096}>\frac{19}{100}.
$$

令 $q=1/10$，Good helpers 满足其所选 state 在实际 bundle 上 $Q_j\ge q$，相应 home 总权重为 $z_i$。由归一化 $Q_j\le1$，

$$
W_i\le z_i+q(1-z_i),\qquad W_i>19/100\Longrightarrow z_i>q.
$$

保留 Good helpers 的 fallback bundles，outer 取这些 helpers 的 homes；其它 helpers 回 own home；每叶保留共同匹配资源并选择提供该 $E_\ell$ incidence 的原 state。所有 groups 值至少 $q$。按 §2 的同一规则放置全部 selectors 和全部 incidence jobs，所选 private 负载至多 $2-q=19/10$，未选 private 与资源至多一；零、重复、inactive payload 没有删掉。$\operatorname{OPT}\ge1$ 给相对 $19/10$ 保证。

# 6. $k=1$、v5 与有限证据的准确去向

v4 的 $k=1$ 无 tiny 上界。对固定 helper 顺序，每次从其 fallback options 加 empty 中，选使整数 matching welfare $f$ 最大者。单调次模性与逐步最佳 marginal 的望远镜和给任意参考 $O$ 的 $f(O)\le2f(G)$。若结果 $W<1/4$，则 $f_{\mathrm{opt}}<1/2<\varepsilon^2$，反证真实 $V<\varepsilon$，baseline sound；若 $W\ge1/4$，已经是整数 allocation，Good home mass 至少 $(1/4-1/10)/(9/10)=1/6>1/10$，直接完整回填。此分支不用 prefix-flow，也不支付 $\nu$ 损失，因此覆盖 $\nu=1$。见[v4 原规范追加 §14.1、§19](../../tools/evidence/shared-ud-tiny-potential-20261031/source/0eb8b34fa84864a54169.md)。

v5 actual-$I$ 版本维护每 helper 至多一个原 state 的实际 matroid incidence 集，以分段 reciprocal 势和相对曲率付款，在 $k\ge2$ 的 $\nu\le1/(1024k)$ 域工作；$k=1$ 另有实际-$I$ 分支。其停止反证使用 $V>18/19$，故失败时只需 $V\le18/19$，等号仍有 $(19/10)(2-18/19)=2$。这与上文 profile 算法的 $V<15/16$ 不同。成功阈值 $L_i\ge19/100$ 允许等号，已足够给 Good home mass $\ge1/10$。本页保留其[最终 actual-$I$ 读后与总位界](../../tools/evidence/shared-ud-tiny-potential-20261031/source/c357f938944fbee92d56.md)和[正式 v4/v5 范围正文](../审查/Shared-UD-v4v5两源实际读后--审查.md)，不以旧 profile 曲率替代这套推导。

原 $k^2$ 知情核查的独有内容是重推全部 $\nu$ 依赖、保留旧 $k=1$ tiny 支路和 $\rho=293/81920$，见[原件](../../tools/evidence/shared-ud-tiny-potential-20261031/source/09654b68c8ce88dfbc5a.md)。它不是新的 Exact-first 独立票。

数学上的有理步骤及多项式位长论证与软件交付分开：上述原证明给出了它们所声称版本的构造和复杂度推导；现存软件没有完成 profile/FW/prefix-flow 或全部 jobs 的端到端运行。两资源 winner-moment/CE 有限核属于原无额外叶算法，交换引理有限核只校准交换命题，均不能冒作这些全域算法的实现证明。正文仍不覆盖多 state outer、重合 homes、homes 上额外叶、一般 non-UD groups 或任意 UM；没有从一般 UM 到该 typed 域的免费归约。原构造、独立 greedy、共同叶匹配、等号边界与不同版本证据均保留，修复公式不另认证新定理。

## 本轮清洗记录（Boss8，2026-10-31）

本轮实际以 `clean show` 导出并全文阅读三份新增冻结文本：独立 Exact-first `a75610d59f434a20ce79`、作者证明 read-after `763df8bd92e8632c9ca0`、v4b 追加 actual-read `e73eae47950670afa3b3`。三者均有 legacy/main 双来源，原字节、SHA 与角色记录见 [v4b 三源证据](../../tools/evidence/shared-ud-tiny-state-potential-v4b-20261031/README.md)。

独立稿只承重旧 k^4 typed 域的完整 value bridge、叶匹配/剩余供给 matroid、profile 次模性与强凸势候选；它没有读取作者 Proof，不能当作作者路线的盲审。作者 read-after 逐项复核 profile smooth-deficit、stable weighted-matroid exchange、Frank–Wolfe、soundFAIL、prefix-flow、完整 ordinary jobs 回填及位复杂度，但没有端到端软件或全参数运行认证。v4b 追加稿明确 k=1 无 tiny 上界、k>=2 的 `nu<=1/(16384 k^2)` 扩域与单独 greedy/曲率分支，同时保留 shared-UD、single-state outer、互异 homes、B-only leaves 和所有 zero/duplicate/inactive payload 的 typed 量词。

这些来源只补足版本化候选证明链和范围边界；不把 k^4、k^2、v4b 或 v5 量词互换，不把作者自述运行当本轮重放。一般 unrelated-machines 19/10、multi-state outer、重合 homes、非 UD extra groups、hardness、六人 SPE/Q-CAG-HALF 仍未解决。
