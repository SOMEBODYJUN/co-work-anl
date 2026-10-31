---
id: "unrelated-machines/one-outer-primitive-sa1-author-read-after-count-dp-20261031"
kind: "review"
type_tag: "审查"
title: "单外层 primitive-SA1 作者 read-after 与 count-DP 审查"
status: "retained-supplied-point-duplicate-provenance"
truth_status: "full-read-consistent-with-v1-scope-no-new-algorithm"
review_level: "full-source-read-and-cross-object-comparison"
summary: "完整阅读作者对单外层 primitive-SA1 v1 的 read-after 记录。它在给定 rational full primitive-SA1 点的前提下，逐式确认 singleton closure、同一条件点、Bernoulli-count 卷积 DP、确定性去随机化、epsilon²/4 阈值和完整 ordinary 调度回填；与既有单外层 v1/v2 审查一致，独有的是 count-DP 后端和其多项式位长论证，不升级为 Q-only 13/8 算法或一般 unrelated-machines 结论。"
source_refs:
  - "source:760f2dcc719ea21fdecc:history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_author_read_after.md"
legacy_ids:
  - "UM-ONE-OUTER-PRIMITIVE-SA1-AUTHOR-READ-AFTER-COUNT-DP-v1"
related_objects:
  - "unrelated-machines/one-outer-normalized-flat-three-source-review-20261031"
  - "unrelated-machines/one-outer-supplied-point-rounding"
---

# 1. 来源身份、时序与阅读范围

`clean show` 导出的来源 `760f2dcc719ea21fdecc` 为
`history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_author_read_after.md`，6,478 bytes，SHA-256 `5c1f16cee1d7a1825e7a65552ca5fdab2fca0e8f193fed6c990fe5a92ae986ff`。本页逐行读完其 94 行，并把原字节保存到
`archives/unrelated-machines/tools/evidence/one-outer-primitive-sa1-author-read-after-20261031/original/`。

作者记录明确：此前已冻结 Exact-first 独立重构（`04b3653d65dbfd764651`，SHA `419df2115facfc2b8cbd976d7f3a3a94fed2dc707ab915f34be10f5d19c8ca94`），随后才释放作者全文 `sol_identity_coupling_single_outer_sa1_threshold_floor_v2.md`。因此本源是知情 read-after，不是另一份 blind 独立证明。它审的是给定 rational full primitive-SA1 点的数学后端，没有运行作者程序，也没有把既有 CDF audit 当作 count-DP 的实现认证。

# 2. 精确量词与 singleton closure

本源承接单 outer、互异 home、每 home own unit helper、与 homes 不交的 shared fallback 资源 `B` 以及完整 ordinary unrelated-machines 矩阵。其结论只在给定共同 primitive-SA1 点、`epsilon>0` 下成立：从该点可确定性恢复质量至少 `epsilon²/4` 的不交 allocation，并回填完整作业得到

\[
V\ge \epsilon^2/4,\qquad C_{\max}\le 2-\epsilon^2/4.
\]

作者用 own-state value 行乘 claim 补、box 行乘 `Z` 和一阶 gate 得 `x_A=x_Z=Y_{AZ}`；再用 gate 与任意原 `F,1-F` 相乘，得到所有原条件项的 `Y_{AF}=Y_{ZF}`。这些都是 degree 2 关系，需要 `epsilon>0`，不借 triple 或二次条件化。选一个正 outer marginal 后，所有 state value、gate、resource 行都乘同一 outer primitive，因而 `mu_{js},t_{jsu}` 真正在同一个条件点；不能将每个 helper 的独立点拼接。

home singleton 的 pair equality 给 `f_j\ge b_j`，weighted fallback benchmark 至少 `epsilon²`。丢去其他外行 helpers 的 claims 只使用二阶非负，最终在回填阶段统一把它们放回 own homes；这一步不等于删掉真实组。

# 3. 作者独有的 Bernoulli-count 卷积 DP

作者后端与既有独立重构采用的 maximum-weighted-score CDF 不同。其算法先让各 helper 独立选择 state/inactive，再以 `t/mu` 请求资源，资源请求者中均匀给一人；随后按资源逐项确定性化。若某资源上其他 helper 的请求数为 `N_{-j,u}`，helper `j` 的贡献含精确因子

\[
\mathbb E\left[\frac1{1+N_{-j,u}}\right].
\]

在只固定若干 helper state 的任意前缀下，未固定 helpers 仍独立，自己的 value/request 与其他请求数独立，故作者的因子分解有效；同一 helper 在不同资源上的请求相关性不会破坏按资源分别取期望。概率分布由

\[
P_0(0)=1,\qquad P_{k+1}(\ell)=(1-r)P_k(\ell)+rP_k(\ell-1),
\]

逐个 Bernoulli helper 更新，再计算 `sum_l P(l)/(1+l)`。只有正请求概率候选参与除法，`mu=0` 或 inactive 直接贡献零；若没有正请求者，该资源的原期望也为零。固定所有 states 后，取正请求者中最大 `w_j p_{jsu}` 的 helper，不小于原均匀赢家期望。

关键版本边界是：既有 32 个 Fraction 小例只检查独立 CDF 后端，不是作者 count-DP 的运行；作者 read-after 只完成了数学因子化和算法描述，不能把 finite CDF 输出移植为 count-DP 软件证据。

# 4. 确定性去随机化与位长

对每个前缀，state/inactive 候选的加权平均等于当前条件期望，因而选择最大候选保持福利下界。作者把所有请求率写作显式有理数 `t/mu` 或有限和；正 `mu` 的倒数只增加有理编码长度，不按其数值循环。每个资源的卷积状态数至多 helper 数，公共分母可取输入参数分母乘积；再乘 `1/(1+ell)` 时新分母可被 helper-count 阶乘控制，位长仍为多项式量级。对显式资源、helpers、states 重算多项式次数，最终精确比较，不用对数、无理数或随机失败率。

这是一段对 count-DP 实现可行性的数学位复杂度论证，不是已运行程序、不是对所有 profiles 的指数枚举，也不是一般 LP/SA1 solver 的复杂度认证。后续若实现该后端，应单独提供 source hash、输入 manifest 和 count-DP 运行证据。

# 5. 阈值、完整 jobs 与实际调度边界

令坏组 value 小于 `tau=epsilon²/4`。由 `q_j\le1` 和 weights 总和一，作者得到高值 helpers 的总 home 权

\[
W_R\ge \frac{\epsilon^2}{4-\epsilon^2}\ge \tau.
\]

只把高值 helpers 的 fallback bundles 导出到 shared resources；outer 领取各自 own homes，其他本行及所有外行 helpers 领取 homes。homes 物理互异且与 `B` 不交，故 fallback overlap 不影响 home 回填；没有辅助 core，也不允许多个 outer 同时使用 `B`。原 selector 放在 root；selected state 实际领取的正 incidence 才导出，其余全部原 jobs（未选 state、零 incidence、重复 indexed state、unused resource 对应 jobs）留在各自 private 端。未选 roots 总负载为一，selected roots 为 `2` 减所领值，资源机至多一枚 unit job，因而调度确实是完整 ordinary 合法 schedule。

# 6. 与既有对象的关系、独有内容与未完成义务

与 `单外层normalized-flat三源精读与13-8版本边界审查--审查.md` 的重复部分是 v1 supplied-point 的 `epsilon²/4` 结论、singleton closure、shared fallback/互异 home 物理域和完整 jobs 回填。本源新增且保留的内容是：

* 作者后端是 Bernoulli-count convolution DP，而既有独立审查使用 maximum-weighted-score CDF；两者都给 1/2 级别，但实现与证据不能互换；
* 对任意 state-prefix 条件化的请求独立性、同 helper 跨资源相关性处理和 `P_{k+1}` 卷积递推的逐式核对；
* 有理请求率、公共分母和 factorial 分母造成的位长边界；
* 明确未运行作者 count-DP、未穷举完整物理矩阵，且不把 32-case CDF audit 当作该算法的 software certificate。

该 read-after 不能升级为 Q-only 13/8：它以 supplied full primitive-SA1 点为前提，未证明从任意 typed Q 生成该点，也未提供 v2 的 11 次阈值 LP。它也不涉及多 outer、无 own home、隐式菜单、一般 UM-TARGET 或六人 SPE。后续实现或第三阶段映射应把本页连到 v1 supplied-point 对象，并保留与 v2 Q-only 算法的“前提不同”边。

