# 三色固定 palette v4：归约核验与共享 canonical 复用

## 当前目标、输入与共享正文修正

本审读对应 `boss5-mz-visual-repair-d32f4aff6be569e7`，定向替代 `boss5-localfix-repair-adb7b167780b9c90`。核心是 `M-d007675a9ed240898c90e831af80b092` v4：对每个预先固定整数 k≥3，有限无向图上区分 YES“存在完整合法三着色”与 NO“不存在合法 k 着色”是 NP-hard。不是仅在大部分顶点上的三着色，k 也不作为随实例增长的免费参数。

| 对象 | 版本 | 当前 registration_pin |
| --- | --- | --- |
| 三色固定 palette `M-d007675a9ed240898c90e831af80b092` | 4 | `99d7c06058a4c711748cbebb1e385f2fe1ce667604d22407eda463831c1f8edb` |
| perfect exact4 `M-ab4a576ed0be482b89d4a646ffc102b9` | 4 | `e2f4d171f9174665027371524263e60473a991292495c0041683392feaa38077` |
| 八色小独立集 `M-922feb7b429f49d4b5f13ca51b34aae7` | 4 | `551be6c145cf6c5ee53f5828c71aeef6fbd22f50a958928a01a802fe2b213aed` |

三个完整记录及 `research show` 返回的 body/evidence bindings 均已实读；输入 pins 与任务一致。共享正文由 SHA `6d5be138de6825a1208776cbb485316c5b0e9d197870e32ab7c1d8ca5cf2f746` 更新为 `d0273adacbf4ccbb9d6cd954cdfd44dddb5f8a8e969067107f63c77bdaaf4b78`。现行全文、父 Boss 的 `source-correction.json` 和既有 MZ 印18页图均已实际读取。图中 Ψ 的重复指数明确是 `k/ceil(q^r/β)`，原分组方向正确；撤回旧 review 把抽取文本读成相反次数的判断。事件句的补事件修正与一般 k 不整除时的 `floor(k/m)` 补充仍保留。

这次修正发生在 MZ 不完美完整性的 Claim3.2 证明。当前三对象的 statement、model、quantifiers、assumptions、scope 和 truth_status 与 v3 相同，仅共用正文及说明字节更新。以下图归约调用 FMW 完美 exact4、GS20 Theorem9 及 Lemma8，不调用 MZ Claim3.2。旧 v3 边的数学保持有效，旧 endpoint/evidence bindings 则不能充作当前 v4 绑定。

## 八色小独立集到三色的整条目标

源对象给出：对每个固定 δ>0，区分完整 8-colorable 图与 `α(G)/|V(G)|<δ` 的图是 NP-hard。为取得非退化互斥承诺，本调用始终取 `0<δ<1/C≤1/8`。

本轮新抽取 GS20 正式冻结 PDF，并连续实读抽取行104–145与285–345，另渲染并目读印62:6整页，核对 Lemma8、紧接的证明及 Theorem9。Lemma8 的完整方向是：若某固定 q 的可 q 着色图对任意固定常数 palette 的着色区分 NP-hard，则可三着色图对任意固定常数 palette 的着色区分也 NP-hard。它明确给出的基本归约为

\[
\operatorname{GraphColoring}(b(t),b(c))\le_p
\operatorname{GraphColoring}(t,c),\qquad
b(n)=\binom{n}{\lfloor n/2\rfloor}.
\]

这里 `GraphColoring(t,c)` 的 YES 是完整 c 着色，NO 是不能 t 着色。`b(4)=6`、`b(6)=20≥8`。固定最终整数 k≥3 后，可取四色阶段的 NO palette `t4=2^(2^k)`，再固定 `C=b(b(t4))`。源 YES 的八色也就是二十色，源 NO 为非 C 色；两步一般归约依次输出 YES 六色/NO 非 b(t4) 色、YES 四色/NO 非 t4 色。Lemma8 所列的后续两次 arc 构造把完整四色 YES 转成完整三色 YES。若最终图可 k 着色，arc 的子集着色反推界两次给四色阶段原图至多 `2^(2^k)=t4` 色，违背其 NO 承诺。这里复用的是 Lemma8 已证的图承诺归约，并未声称另行重证其引用的原始 arc-graph 论文。

为支付上述源 NO，先按 k 固定这条有限链及 C，再固定 `0<δ<1/C` 并调用源硬度。若源 NO 图可 C 着色，C 个色类之一是大小至少 `|V|/C>δ|V|` 的独立集，与源承诺矛盾。因此它确实给出所需的 `GraphColoring(C,8)` 硬度。所有归约次数和参数按 `k→t4→C→δ→源参数→实例规模` 的顺序固定，复合归约为确定性多项式；巨大 C 仍是常数。

所以该单一源支付核心的整句结论，具有 accepted、unconditional、whole 作用范围。它只转移着色 promise，不把同一张八色输入图直接称作三色图，也不推出三色图的小独立集密度结论。

## 旧 exact4 支持的实质与证明去重

旧 exact4→三色边的 conditions、roles、whole_result、explanation、scope、evidence 与旧 review 已完整实读，并与新八色 proof 的两个完整段落及两条新边逐项比较。旧推导先以 FMW 的 perfect exact4 源支付 GS20 d=4 的 exact d-to-1 合同，再用 §2.1 induced-list 桥和 Theorem9 得 q=2d=8 的完整八色/任意小独立集 gap，最后使用上一节相同的颜色类桥及 Lemma8。它是 exact4→八色→三色的复合关系，未提供绕过八色结果的另一条证明。不同 source 的两个充分关系不能据此计作两条相互独立的技术证明。

本轮完整读取并复用 `boss5-localfix-repair-8c728e95a224313d` 的当前两条关系及完整 `comparison-proof.md`。其中 exact4→八色的新证明保留以下承重合同：strict val=1、每个右标签恰四左原像、常数字母表在固定 soundness 之后选取、带身份平行约束按重数计值；附录B 的 exact 化保完美 YES 且 soundness 增量至多 2/h；GS20 induced-list 桥保留对任意固定列表界及正诱导比例的量词。Theorem9 的 influence/list-decoding 使用安全列表界 `ceil(d²h/η)` 与严格均值门槛，得到完整八色 YES 和任意小独立集 NO。对这些成熟技术输入，本轮实读的是既有 proof、当前两边与旧完整历史记录，未声称重新逐句审读 FMW 内核、GS20 全文或 DMR09 原论文。

新 canonical 的 exact4→八色边与八色→三色边正好分解并保留旧复合论证的全部数学。旧 exact4→三色封装因此退休，以免复制同一支持链；其完整推导及有效参数在当前两边和本审读中仍可重建。新八色→三色边直接 incident 本包核心，精确共享为本包唯一 coverage 逻辑边。exact4→八色仅作为只读 canonical 依赖：它不 incident 本包核心，不列为本包 asset，不虚增覆盖。

## 当前复用与逐资产替代

精确共享边为 `eight-color-independent-set-v4-to-three-color-gap-8c728e95a224313d`，路径位于 `map/edges/boss5-localfix-repair-8c728e95a224313d/`；SHA 以收据 `assets` 中冻结的实际字节为准。其只读前段为同目录 `exact-four-to-one-v4-to-eight-color-independent-set-8c728e95a224313d.json`；引用与精确 SHA 单列在收据 `reused_read_only_evidence`。两条当前边已完整读取并经本地 `edge-check` 核当前 bindings。

| 旧资产 | 处置 | 数学理由及去向 |
| --- | --- | --- |
| `exact4-to-three-color-fixed-palette-v3.json` | retired | 旧 v3 复合封装无独有数学；当前 canonical exact4→八色→三色链完整保留同一归约，不重复新造直接边。 |
| `eight-color-independent-set-to-three-color-v3.json` | replaced | 完整相同数学由当前 v4 八色→三色 canonical 精确共享，完整 YES、固定 k 和严格 NO 保持。 |
| `review.md` | replaced | 本文给当前 pins、视觉勘误、Lemma8 原文与常数核验，并更正“两个独立技术证明”的归类；旧记录仍作为有 SHA 的历史文件。 |
| `reading-ledger.json` | replaced | 新 ledger 全量嵌入旧记录，明确其历史读页、旧版本与本轮新读；撤回抽取误读，未把继承阅读改写为本轮 PDF 全文审读。 |

旧四文件均未覆盖。原始旧 review 中关于相反重复次数的判断只作为已被纠正的历史记录；本交付不再引用其为当前正确结论。本包不创建任何新边身份。

## 实读边界与 follow-up 处置

本任务没有 `overlap_comparisons` 标为 follow-up 的对象对，故 `closed_overlaps:[]`、`follow_up_tasks:[]`。核心与八色源的完整支持、核心与 exact4 的复合支持属于实际普通比较，记录在 coverage 和 `additional_comparisons`，不冒充关闭其它队列义务。

反向逐实例主张“非 k 色推出任意小独立集比例”不成立：`K_(k+1)` 与 N 个孤点的不交并有色数 k+1，而独立集比例 `(N+1)/(N+k+1)` 趋近1。这只阻止该直接反向桥，不反驳任何现有硬度定理，也不证明不存在专门反向归约。可随输入增长的 palette、常数最大度、调度或 SPE 均不在已付目标内。

本轮新读与旧历史逐项分开列于 reading-ledger。没有读取凭据、网络/Library 检索、Git 或队列操作，没有修改共享源或 registry，也没有重跑旧数学程序或科学实验。边结构检查只核绑定和格式，不替代以上数学判断。
