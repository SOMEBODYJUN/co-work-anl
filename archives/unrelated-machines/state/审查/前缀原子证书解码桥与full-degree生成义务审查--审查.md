---
id: "unrelated-machines/succinct-prefix-atomic-decoding-review"
kind: "review"
type_tag: "审查"
title: "前缀原子证书解码桥与 full-degree 生成义务审查"
status: "integrated-promised-decoder-with-generator-open"
truth_status: "conditional-prefix-decoding; finite-exact-audit; no-free-oracle"
review_level: "full-source-read-cross-object-and-prefix-precision-comparison"
scope: "UM-PREFIX-ATOMIC-DECODING-v1 前缀 law 解码、full-degree localizer、有限精确审计、prefix precision/rank 边界与生成器义务"
summary: "完整读取 40d76e6d45965e107d47 并比较 current succinct-prefix bridge、prefix finite-precision/relative-Gram 审查、strict-sub2、composition NP 障碍和有限 audit。确认给定全局非负前缀 law 时可用 O(E) 正延伸解码完整原子调度；但从任意 (P,T) 生成该 law、可靠 FAIL=>OPT>T、全阶 localizer 或通用 oracle 仍未完成。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/succinct_prefix_atomic_decoding_review.md"
  - "clean:40d76e6d45965e107d47"
  - "related-source:acefddb37ce983a3c85c:research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md"
  - "related-source:3192730be9a3e5493a30:evidence/runs/unrelated_machines/succinct_prefix_atomic_decoding_audit.json"
related_objects:
  - "前缀原子law解码的生成义务与精度后续--审查.md"
  - "严格次二批量能垒与前缀原子解码双源审查--审查.md"
  - "前缀原子有限精度与相对Gram审计--审查.md"
  - "宽仿射矩形与前缀原子解码双源审查--审查.md"
  - "私有组退出池共同宏任务与有界profile联合选择最终审查--审查.md"
  - "近单位PCSP蕴含与物理复制义务最终范围审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/succinct-prefix-atomic-decoding-20261031/original/succinct_prefix_atomic_decoding_review.md"
---

# 来源身份与审查范围

本页处理 clean source `40d76e6d45965e107d47`，原路径为 `research/reviews/unrelated_machines/succinct_prefix_atomic_decoding_review.md`，冻结 blob `03fe0eb0b6bf94b1415aca3978718a3d96501e5d`，原源 SHA-256 `31a4cb3c6b392efa693c93d6fb5546d83b954d01cb8431f936554a6e6ba83a7e`，大小 1,950 B。原文已复制到 `evidence_paths`。

审查对象是 `UM-PREFIX-ATOMIC-DECODING-v1`，对应当前正文 `research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md`（inventory ID `acefddb37ce983a3c85c`，SHA-256 `a17bde448cd58ab9b637a6050837153006423cf8097b078621bcb302031ff02`）和有限审计 JSON（ID `3192730be9a3e5493a30`，SHA-256 `a6c42e32ebc025e20fa099e53b804e225c3c95d1fb4f794fe45e223bd180e52d`）。本页整合给定 law 的解码合同、full-degree 依赖、有限精确运行和后续精度/秩边界；不把审查摘要或有限代码输出升级为任意输入的 oracle、生成器或一般调度算法。

处置为 **integrated-promised-decoder-with-generator-open**：条件解码桥接入 prefix/relative-Gram/strict-sub2 证据链，明确生成器和可靠 FAIL 义务仍开放。

# 1. Prefix law 的精确合同

给定显式 unrelated-machines 实例 `(P)`、阈值 `T≥0` 和每个任务的有限端集合 `E_j`。对任意相容部分分配前缀 `S`（每任务最多一个已选端）有一个有理前缀值 `π(S)`，要求：

1. `π(∅)=1`；
2. `π(S)≥0`；
3. 对尚未处理任务 `j`，one-hot 守恒
   \[
   \pi(S)=\sum_{e\in E_j}\pi(S\cup\{e\});
   \]
4. 每个完整原子分配 `σ` 和每台机器 `i` 满足
   \[
   (T-L_i(σ))\pi(σ)\ge0;
   \]
5. 每次 `Eval(S)` 的运行时间和输出位长按输入总位长、前缀长度多项式有界。

这些条件必须来自同一个全局 law。不能为不同前缀、不同机器重新选择不相容见证，也不能把只看过的有限原子替代完整全阶局部化器。

# 2. O(E) 确定性解码

从空前缀 `S=∅` 开始，按固定任务顺序查询当前任务的全部有限孩子。若当前 `π(S)>0`，守恒式保证所有孩子权和为正，因非负性至少有一个正延伸；固定平局规则选一个正端加入 `S`。归纳保持 `π(S)>0`，直到得到完整分配 `σ`。查询总数至多为有限端数 `|E|`，不需要枚举完整原子分配集合。

最终 `π(σ)>0`，逐机局部化条件给出 `L_i(σ)≤T`。空任务直接返回空调度；`T=0` 时所有正负载原子会被 localizer 强制为零；零处理时间端不引入除法；不可用端不进入 `E_j`。

逻辑上，存在该合同的前缀 law 当且仅当 `OPT(P)≤T`：

- 正向由上述贪心解码得到合法完整调度；
- 反向若存在可行 `σ`，以该 `σ` 的 Dirac law 定义前缀查询器即可。

这是一个**表示等价和解码定理**，不是算法：它不提供未知 `σ`、不从任意 `(P,T)` 生成 `π`、也不提供可靠 `FAIL⇒OPT>T` 查询器。

# 3. Full-degree、one-hot 与前缀矩边界

若前缀 law 来自全阶矩/functional，`π(S)` 可写成相容端点 monomial 的值；Boolean/one-hot ideal 保障守恒，平方正性保障非负。对 degree-`n` 的负载 localizer，乘完整原子指示的总次数达到 `2n+1`，才能对每个叶分支支付容量。因此低阶 `M2`、有限几阶 Gram 或单个前缀样例都不能自动替代 full-degree 局部化器。

这一点与既有 prefix finite-precision/relative-Gram 审查一致：

- 绝对残差或有限查询误差会产生全叶数 `N=∏_j|E_j|` 的质量/残差因子；
- 相对 localizer 可缓解该 `N` 因子，但需要完整行秩条件；
- 低阶或删行 Gram 不能推出所有原子容量界；
- 非正交基下不能把绝对 identity basis 的逐项系数相等当作表示不变性。

这些是表示和精度边界，不是本来源新建的 full-degree theorem。引用 prefix 解码时必须说明 localizer 是对所有完整原子分配全称，且 law 的守恒/非负性是共同的。

# 4. 有限精确运行与边界

审计程序 `tests/audits/unrelated_machines/succinct_prefix_atomic_decoding.py` 使用 `fractions.Fraction` 构造 Dirac 和均匀证书，运行前缀贪心并逐机重算负载。其有限输出包括：

- 可行两任务例，负载 `(1,1)`；
- `T=0` 的零负载单端例；
- 两机三件单位任务、`T=1` 时 8 个完整原子分配均有机器负载 2，因此任何非负 one-hot law 都被局部化器排除，与总质量 1 矛盾；
- 5 个异质 Dirac 可行证书，逐机通过。

这些案例核对了空对象、零阈值、零处理时间端、不可行全原子集合和异质端点。它们没有生成任意 `(P,T)` 的 succinct oracle，没有验证一般 full-degree law，也没有建立 `UM-TARGET-v1`。

与 strict-sub2 批量能垒的关系是边界互补：严格次二局部修复可能需要 `Ω(1/ε)` 同步动作，但 prefix 解码假定一个已经存在的全局 law；它不提供绕过该能垒的调度算法，也不把有限成功案例写成近二 hardness。

# 5. Oracle 生成义务与复杂度缺口

若存在一个总确定性位多项式生成器 `Gen(P,T)`，对所有 `OPT≤T` 输出满足上述合同的 `π`，并在其余输入可靠 FAIL，则调用 O(E) 解码器便可精确判定 `T` 可行。该 `Gen` 不能免费假设：现有半单位选择/3DM 型 NP 障碍说明，生成完整前缀 law 可能已经包含原问题的计算困难。

因此以下主桥义务仍未完成：

- 从任意 `(P,T)` 生成共同非负、守恒、full-degree 局部化的 `π`；
- 或给出可核验的 `FAIL⇒OPT>T` 证书；
- 在不枚举指数原子集合的条件下构造完整查询器；
- 从低阶矩/配置/相对 Gram 中给出可计算且满行秩的 full-degree 表示；
- 将 prefix bridge 与一般 unrelated-machines 的 near-two/hardness 目标连接。

查询器评估自身是线性于有限端数的，但这不等于整体算法多项式：整体复杂度受 law 生成、验证和 full-degree localizer 构造支配。

# 6. 与相关对象的去重

- 与《前缀原子 law 解码的生成义务与精度后续》：本页补充当前 succinct-prefix source 的原始实际审查和有限运行；两者共同区分“给定 law 的 O(E) 解码”和“从任意输入生成 law”。
- 与《前缀原子有限精度与相对 Gram 审计》：后者给出 `N` 因子、dummy dilution、满行秩和非正交基反例；本页将这些作为 full-degree/精度边界，不重复 finite audit 数值。
- 与《严格次二批量能垒与前缀原子解码双源审查》：前者提供固定参数的批量局部修复障碍，后者提供 prefix bridge 的有限核验；两者不合并成一般 hardness。
- 与 near-unit PCSP、private-group exit-pool 和 raw SH3：这些来源给抽象 promise、共同 pool 或必要 flow；没有一个自动生成本页的 `π`，本页也不关闭 source-to-UM compiler。

# 7. 结论

`40d76e6d45965e107d47` 可靠确认的是：在给定共同前缀 law、非负守恒和所有完整原子逐机局部化的条件下，可以用线性于有限端数的确定性正延伸选择，解码得到完整合法调度；其存在性等价于 `OPT≤T`，但不提供 law 生成器或未知调度搜索器。

有限 Fraction 运行覆盖可行 Dirac/均匀、`T=0`、全原子不可行和异质 Dirac 边界；这些不替代 full-degree 数学合同。后续若要推进，必须构造 `Gen(P,T)` 或可靠 `FAIL⇒OPT>T`，并处理精度误差、叶数因子和 Gram 满行秩。一般 `UM-TARGET-v1`、near-two 算法/硬度、外部审查和全球新颖性仍未认证。
