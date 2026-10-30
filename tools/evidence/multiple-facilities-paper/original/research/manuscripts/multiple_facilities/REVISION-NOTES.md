# 本轮英文校准及两项审查修正

基线 `main.tex`：`ceb6cb53b7bcb18fcce4bc7c7fbdea4f7cb85890c0215e81f0b6707a3c9f0dbe`。本轮范围为摘要、Introduction、各引理/定理前后的叙述，以及主agent明确转来的两项非致命精度修正。

## 真实范文与使用方式

实际读取 Harks--Klimm, *On the Existence of Pure Nash Equilibria in Weighted Congestion Games*, Mathematics of Operations Research 37(3), 419--436 (2012)，DOI `10.1287/moor.1120.0543`，作者公开PDF：

https://www.fim.uni-passau.de/fileadmin/dokumente/fakultaeten/fim/lehrstuhl/harks/HK-MOR-2012.pdf

阅读位置为摘要p.419、§1.1--1.2 p.420和Lemma 3.1完整陈述/证明pp.422--423。文风观察只针对这些已读段落：先明确研究对象和结论范围，再介绍机制；技术段落先交代需要完成的义务，再写构造与推导；使用直接的主谓与逻辑连接词。未复制独特句子，也没有将其论文中的数学结果借入本稿。

## 叙述改动

- 摘要按前人模型/界限、本文常数保证、精确续局、证明机制组织，末句明确是 improvement factor，不是绝对收益增量。
- Introduction先明确本文研究的博弈和全续局义务，再展开原文结果及本文方法。机制段先说需要控制偏离后的重量和客户最优性，再解释两类选择。
- §2及装箱、修复、续局补全的段首先给出该步所需的数学输出；移除“额外一家设施的重量”等需要转译的简称。
- 定理后的解释明确区分在轨等负载和离轨重原子隔离；证书段首直接陈述有理输入的编码后果。

## 实质性数学触及清单

1. 摘要、Introduction结果段、Theorem 2.7（label `thm:main`）：把在轨“each client”明确为“every covered client”。未覆盖客户仍不参与服务。量词和已有模型保持一致。
2. Proposition 2.8（label `prop:certificate`）证明最后一段：输入分母乘积只给客户权重和的分母；在轨设施负载还除以至多k的整数。现明确每个负载的分母再乘一个不超过k的整数，因此bit length额外增加 `O(log k)`，精确比较的位长仍为多项式。

没有改变任何显示公式、编号、label/citation key、构造、原子装箱或纯改善证明。七段proof中仅最后的编码证明改变上述分母说明，其余六段逐字未改。结构与两节安排不变。

## 验证

对基线与本轮的显示数学提取结果逐项比较一致；所有ref/eqref仍有定义。实际重编译后以 `WRITING_STATE.md` 最新记录为准。独立math audit的原始意见保留，不将写作者自查升级为独立审查。


## 完整editorial报告后的三项局部修复

原冻结稿c8bfa0d…的隔离报告保留其FAIL判定。SE-1在Lemma\ref{lem:deviation} Case2明确把原J_t与新增客户一起装箱；SE-2在默认规则开始固定客户枚举；SE-3用两个具体lemma引用替换描述性指称。三项均采纳，不改变定义域、存在性结论、显示公式或证明路线。主agent逐段核对实际diff及重编译；没有伪称新的隔离delta或editorial PASS。
## Round-1 referee repair

- **`main.tex:137,153--155` (`lem:capped`)**: replaced the ambiguous phrase
  “all other facilities” with “every facility that does not host one of these
  heavy clients.” A heavy singleton is intentionally allowed to exceed the
  cap, so the original wording contradicted the packing conclusion used in
  the deviation proof. The proof's invariant and theorem statement are
  otherwise unchanged.
- **`main.tex:195`**: repeated the non-heavy-facility qualification in Case 2
  so the application of `lem:capped` matches its corrected invariant.
- **`main.tex:215`**: separated polynomial checking of the stored profiles from
  the symbolic correctness argument for the implicit default rule; this
  removes an avoidable reading that the exponentially many default executions
  are all enumerated by a polynomial verifier.

## Round-2 independent proof review fixes

The independent round-2 audit found no S0--S3 issue and three S4 exposition
items. All three were adopted without changing a theorem, hypothesis, formula,
or proof strategy:

- **`main.tex:80`** fixes the tie rule for the finite lexicographic maximum by
  specifying a fixed total order and retaining the first maximizer.
- **`main.tex:123`** makes the occupied-target comparison explicit:
  `W_t/q_t>((q_t+1)a)/q_t>a` before the sorted-vector contradiction.
- **`main.tex:214--220`** calls the continuation outside the stored layouts a
  deterministic default-rule program, and uses the same fixed enumeration in
  the certificate proof. This states that the certificate stores a succinct
  rule rather than an exponentially expanded table.

The round-2 proof report (`REFEREE_REPORT_round2_proof.md`) re-derived the
model, lexicographic selection, both source-location cases, packing, the cap
potential, all deviations, continuation compatibility, and rational encoding.
It found no remaining correctness blocker. The final audit still treats finite
arithmetic runs as regression evidence rather than a proof of the universal
claim.

## Round-2 editorial gate

The final fresh-eyes language gate is recorded in
`EDITORIAL_REVIEW_round2.md`. It found no must-fix prose issue: the earlier
humanizer pass remains mathematically faithful, terminology is stable, and
further shortening would remove proof-bearing cases rather than reduce
unnecessary complexity. The only additional source change after that gate is
the layout-only `\\enlargethispage` line that keeps the reference entry on the
last page.
