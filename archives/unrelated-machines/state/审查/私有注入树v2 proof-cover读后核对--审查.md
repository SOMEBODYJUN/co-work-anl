---
id: unrelated-machines/private-injective-tree-v2-read-after-cover-review
kind: review
type_tag: 审查
title: 私有注入树 v2 proof-cover 读后核对
status: integrated-proof-read-after
truth_status: v2-scope-confirmed-no-new-theorem
review_level: full-source-read-and-cross-archive-comparison
summary: 冻结的 read-after-cover 审查全文核对 v2 root proof 与 v1 fractional-floor proof 的配置行、共同 a 树流、blocker/Haxell、完整原任务回填及非单射 promise 过滤；结果与既有五三定理一致，唯一新增边界是无条件 d=1 调度措辞需收紧。
scope: private injective tree configuration v2; proof-read-after-cover; no implementation audit
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_read_after_cover_source.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_read_after_cover_source.md
source_id: bb680b86f0f2928e512b
source_sha256: 75ad91e3215bf5856ae6ae9042947f84d28738142b356c09a2b57f4f42a4f493
source_size_bytes: 8289
related_objects:
  - archives/unrelated-machines/state/定理/私有注入树配置五三界与非注入承诺判定--定理.md
  - archives/unrelated-machines/state/审查/私有注入树v2作者证明读后与范围续审--审查.md
  - archives/unrelated-machines/state/审查/私有注入树v2四源批次语义核对--审查.md
evidence_paths:
  - archives/unrelated-machines/tools/evidence/private-injective-tree-v2-read-after/original/private_injective_tree_configuration_v2_read_after_cover_source.md
---

# 来源身份与处置

该源不是新的 v2 模型陈述，而是一份 cover-consistency 读后审查。源内记录先行 Exact 与独立稿，再全文核对两个 proof 版本：`private_tree_configuration_floor_v2_root_frozen_proof.md`（SHA `e524ac4cf8df7310729477dc12f91c14842a90dff58953e66d3952397574a05a`）和 v1 `private_injective_tree_fractional_floor_frozen_proof.md`（SHA `f4900b3693d6242cd08f218cbc478bb1e40ee6f072fb3205a5619b21fd1f40c5`）。本次全文读取的是冻结源 `bb680b86f0f2928e512b`，字节证据已复制到 `tools/evidence`；不创建第二个五三定理。

# 实质核对

1. **CONFIG 局部行。** 在 `1≤T<2`、`s=floor(d(T−1))`、`a=d−s` 下，源逐项核对
   `sum_e (q−t_e)_+ ≤ s q` 与 `sum_e min(q,t_e) ≥ a q` 的等价性。区间串接/模 q 的分解实现正部条件；q=0、q=1、s=0 端点单独处理，外机 singleton/empty 补足资源行。该处是精确配置分解，不是只给必要松弛；但仍只产生配置分布，不产生整数调度。

2. **共同 a-树流。** 对 `0<b≤q` 使用 `min(b,t)≥(b/q)min(q,t)`，从容量 `min(b,t_e)` 装出总量 `a b`，再在 uniform-matroid base polytope 中有限分解为恰 a 个 child。源确认每个 root 始终选择同一真实 state；叶激活概率受原 unit 边际支配，跨 root 的资源冲突仍由后续 Haxell 匹配处理。支持可指数大，不能升级为总位多项式构造。

3. **阻断与 Haxell 量词。** 满 a 叉树中命中所有满 r 叉高 h 子树的最小叶数为 `(a−r+1)^h`；注入叶映射才允许把叶数换成不同外机资源。每条辅助超边含 root tag 与 `R=r^h` 个资源，rank 是 `R+1`，阈值为 `2R−1`；源内声称其外部定理核对覆盖了严格不等式而非把 `>` 弱化为 `≥`。该证明只依赖源中所记录的 Annamalai/AFS 陈述，不能据此声称重构 Haxell 1995 原证。

4. **完整原任务回填。** 匹配选中的真实 r-子树下送，活跃父机负载为 `2−r/d`；未激活分枝、未选状态和零权状态的全部原 small jobs 留父，负载为 1；外机至多接一枚 unit。辅助树不是新机器/新任务，故该结论没有删掉原实例任务。

5. **非单射 promise 过滤。** `OPT≤1` 时 selector 所在状态被逐层迫使全叶外送，因而状态内注入且跨 root 资源不重叠。删非单射状态只改变 selector 候选，不删其机器和原 jobs；在保留状态上解共同 λ LP。LP 不可行只保证 `OPT>1`；可行时五三存在性加被删状态全父置给出 `OPT≤5/3`。这是区分 promise `OPT≤1` 与 `OPT>5/3` 的总位多项式判定边界，中间带可任答，不是一般非单射配置间隙定理。

# 独有边界、缺口与后续

源内唯一需要进入正式正文的措辞修正是：若没有共同 λ/CONFIG 前提，不能写无条件 “d=1 时实际调度为 1”。两个 root 的唯一叶可指向同一外机，峰值可达 2；因此 d=1 只在正式容量前提下进入证明，普遍安全表述是 `C≤2`。这不反驳 v2 A/B/C。

本源未执行实现代码、有限实例或生产回归，也未认证一般 unrelated-machines 近似、NP-hardness、UM-TARGET-v1 或全球新颖性。其独有内容是 proof-cover 版本链、严格 Haxell rank/不等式的读后核对及 d=1 边界修正；数学对象和五三常数均沿用既有定理。

# 建议处置

`integrated` 到既有 `私有注入树配置五三界与非单射承诺判定`，并以本审查作为 proof-read-after provenance；保留源原件和 SHA。第三阶段建立来源/证明核对边，不建立新的 theorem、software 或一般 hardness 对象。
