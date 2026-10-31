---
source_id: "22eb4747b3c8214c2765"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md"
source_sha256: "80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d"
source_size_bytes: 3867
status: "statement-only-candidate; proof-withheld-from-exact-first"
disposition: "integrated-candidate"
---

# 读取范围与来源身份

`clean show 22eb4747b3c8214c2765` 已完整读取 3,867 字节的 Exact-only 源。源文件声明它是一个新对象，要求 fresh Exact-first reviewer 先独立攻击；它不包含作者势函数、profile exchange、取整或算法证明，也不把随机 working note 当确定性证明。来源 SHA-256 为 `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`，冻结字节保存在 `archives/unrelated-machines/tools/evidence/shared-ud-tiny-potential-20261031/source/22eb4747b3c8214c2765.md`。

## 精确输入域

- 有输入变量 (kge1) 个 outer groups；每个 outer 恰一个 indexed state，正支持是若干 home (g_j)，每个 outer 的正 home 权重和为 1。
- 所有 home 物理互异，每个 home 有一个 own-unit helper；每个 home 权重满足
  [
  \max_j w_j\le 1/(4096k^4).
  ]
- shared fallback states 是同一有限资源集 (B) 上的任意显式 normalized 非负二进制有理向量；(B) 与 homes 不交，fallback supports 可共享。
- 还允许任意多个额外 leaf groups，但这些 leaf 的全部正支持必须在 (B) 中。固定 (arepsilon=15/16)，令
  [
  H_\ell=\{u\in B:\max_s p_{\ell s u}\ge\varepsilon\},\quad
  b_\ell=\max_s\sum_{u\notin H_\ell}p_{\ell s u};
  ]
  每个 leaf 要求 (b_\ell<\varepsilon)。这是一种 exact threshold-unit-demand 合同，不要求 leaf state 本身是 unit singleton，也不要求 leaf graph 有完整匹配；无匹配的输入仍在量词域内。
- 保留零 incidence、重复 indexed states、unused resources 和所有原 jobs；不允许把活跃子问题或普通矩阵删减后当成完整输出。

由这些输入生成完整 typed ordinary UM (P(Q))：每个 state 有 private machine，每个原资源有 resource machine，每个 group 有 unit selector，listed incidence 是不可拆 job，private 时间为原系数、resource 时间为 1，其余端点无穷。若 states/resources/incidences 数为 (S,U,I)，则机器数为 (S+U)，原 jobs 为 (G+I)，有限端点为 (S+2I)。

## 源文件的候选结论与真实状态

Exact-only 源提出：存在只读取上述显式 (Q) 的固定确定性、worst-case 总位多项式算法，输出全部原 jobs 的完整合法 assignment (sigma)，并满足
[
C_{\max}(\sigma)\le(19/10)\operatorname{OPT}(P(Q)).
]
算法不得得到 OPT、实际 allocation、feasible LP/PSD 点、精度参数或 joint law，不得枚举指数 joint profiles，也不能以随机/Las Vegas 运行时间或 generic exact SDP finder 作为 oracle。允许标准确定性 matching/min-cost-flow、精确有理线性优化和多项式次数的有理算术。

这里的“候选结论”只记录来源的完整量词；该 Exact 文件没有证明、实现、运行输出、外部 referee 或新颖性证据。因此不能把它直接登记为已证 19/10 算法。

## 与已读相关链的比较

1. 同一 shared-UD/tiny-home 研究链的作者 Proof 源 `e2370ab75fef1534990c`（SHA `409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435`）展开了 value bridge、leaf matching/vacancy matroid、profile potential、stable exchange、Frank–Wolfe、sound FAIL 和 prefix-flow 回填；它是独立来源身份，不能把本 Exact 直接当成该证明的摘要替代。
2. `f00e3e92df90c1dab67c` 的作者自核和 `0eb8b34fa84864a54169` 的 canonical append 是后续审查/版本材料；它们可解释作者 Proof 的边界，但不能把作者自核算作 fresh Exact-first 审票，也不能把 v4/k² 扩域的推导反写进本 k⁴ Exact。
3. 现有 `Boss11共享UD叶tiny-home-k二次扩域三源审查` 记录的是 v3/v4 的 k² 与 k=1 放宽版本，量词和版本不同。本源的 k⁴ home 上界、额外 B-only leaves 和单 state outer 必须保持单独身份；不得把 v3/v4 的 proof constants 静默移回本候选，或把本候选的开放状态抹掉。
4. `共享UD最优交换有限网络双源审查` 的 Fraction 小网络只核验有限最优交换边界，不实现本源的全 profile 选择、曲率、叶 circulation 或完整原 jobs 回填。它可以作为局部 finite evidence，不能替代本候选的完整算法证明。
5. 早期 `多outer tiny-home作者证明v1读后与完整算法范围增量` 是另一个 Exact/Proof 版本链（其作者稿对应的 Exact SHA 为 `38c85f...`），不能因标题相近而把 sources 合并；必须保留本 80fd Exact 的额外 B-only leaf 量词和版本 provenance。

## 不能外推的结论

- 不能把候选 19/10 写成一般 unrelated-machines 近似算法，也不能把它当作 UM-TARGET-v1 的解决或 hardness 结果。
- 不能删去 single-state outer、全局互异 homes、(1/(4096k^4)) tiny home、B-only threshold-UD leaves 和完整原 jobs 输出条件。
- 不能以 source-only 的“存在算法”替代 proof、代码、有限审计或外部验证；随机 working note、作者自核和有限交换程序都要单列证据等级。
- 不能把“无全叶匹配仍在域内”改成输入排除条件，也不能把 leaf state 误写成 unit singleton。

## 建议正式去向

将本源作为 `integrated-candidate` 并入一个专门的 shared-UD tiny-state potential 版本审查对象，与作者 Proof、self-audit、canonical append 和后续 read-after 分开列出 source SHA 与角色；证据 manifest 应保留所有原字节。正式对象应明确候选/证明/有限审计/作者自核/一般目标 OPEN 的分层，并把现有 k²/v4 审查作为“版本不同”的关系，而不是直接依赖。
