---
id: "unrelated-machines/private-injective-tree-v2-four-source-batch-review"
kind: "review"
type_tag: "审查"
title: "私有注入树 v2 四源批次语义核对"
status: "integrated-into-existing-v2-theorem"
truth_status: "same-v2-object; no-new-constant; scope-preserved"
summary: "四份冻结来源分别是 Exact 陈述、independent cover、independent literal 与 independent shared 审查；全文核对后均指向既有私有注入树配置五三界与非注入承诺判定对象。独有内容是对配置行充分性、共同树分布、Haxell rank、完整回填和过滤器量词的独立重构；不增加一般 UM 算法、非单射 gap 或新颖性结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_cover_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_cover_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_literal_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_literal_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_shared_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_configuration_v2_independent_shared_source.md"
related_objects:
  - "archives/unrelated-machines/state/定理/私有注入树配置五三界与非注入承诺判定--定理.md"
  - "archives/unrelated-machines/state/审查/私有注入树v2作者证明读后与范围续审--审查.md"
  - "archives/unrelated-machines/state/审查/私有注入树v1独立与证明三源增量--审查.md"
source_ids: ["ccfd0e8e7c80f777eb02", "9faec0619249f914393e", "f3a1af533f2763f1be3a", "cad532492f4728fd9157"]
source_sha256:
  - "ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900"
  - "e197ac223247fb90471bb701dc139440b8f3f2c00419425a8adab8f88e4434d2"
  - "13491bd3332d25c5b49dccc9812b3c5cc61f7e5b4e4ba3be3ef03b55a04d9ff7"
  - "0dd146d01bd47f6a403418c3899ed64759d4accb4c8c27e358b1137ec69be474"
---

# 阅读范围和版本身份

四份源均已通过 `clean show` 全文取得。Exact 源（`ccfd0e8e7c80f777eb02`，3,398 字节）只给候选 v2 的精确模型和 A/B/C 三项结论；不含证明。`9faec...`（independent cover，9,788 字节）、`f3a1...`（independent literal，12,130 字节）和 `cad5...`（independent shared，5,921 字节）均以 Exact 的 SHA `ad33f6b2…87900` 为对象，分别重构配置边际、共同树流、资源阻断/Haxell 以及过滤承诺边界。四源的稳定数学对象是既有 `unrelated-machines/private-tree-configuration-floor-v2`；它们不应另建第二个五三定理。

# Exact 模型和量词

有限非空 root 集合 `U`，每个 `u` 的非空菜单 `S_u`；每个 `(u,s)` 是满 `d` 叉高 `h` 的完全私有状态树。内部机器仅在状态内使用；selector 根处理时间 1，内部 incoming unit 的父端为 `1/d`、子端为 1，叶 job 的父端为 `1/d`、指定外机端为 1，其他端无资格。树和叶映射显式输入，状态内要求 `f_us:[d]^h→Z` 单射。空 `U` 另处理；不含共享内部机器、非均匀处理时间、多单位叶端、预载或一般 UM。

完整 `CONFIG(T)` 是每机配置权重和为 1、每个原 job 恰覆盖一次的通常配置 LP。对 `1≤T<2`，令 `s=floor(d(T−1))`、`a=d−s`。若 `q_v` 是 incoming unit 边际、`t_e` 是 outgoing job 在下端的 unit 边际，则四源都核对同一精确局部条件

`sum_e (q_v - t_e)_+ <= s q_v`, 等价于 `sum_e min(q_v,t_e) >= a q_v`。

根边际按菜单和为 1，内部 child 的 incoming 边际等于父 job 的 `t_e`，每个外机的叶 unit 边际总和不超过 1。cover/literal/shared 均特别排除了仅以 `sum t_e` 代替逐端 `min(q,t)` 的错误松弛；例如单个大 `t_e` 不能代表多个 small 端的可联合配置。

# 配置可行性、共同树分布和完整调度

independent cover 给出局部正部的有理配置分解：当 `q>0` 时以 `c_e=(q−t_e)_+` 为 incoming 分支所需 small 的联合质量，在均匀 matroid 基多面体中分解为恰 `a` 个向下端口；其余质量在无 incoming 分支放置。q=0、1、s=0 单独退化，外机由 singleton/empty 配置补足。由此可构造显式规模的线性系统，但不把它误写为指数配置列举或整数调度算法。

给定一份 `CONFIG(T)` witness，每个 root 先按根边际选一个真实 state，随后递归抽取同一 state 内的满 `a` 叉树分布。若节点激活质量为 `b_v≤q_v`，则 `sum min(b_v,t_e)≥a b_v`；选取 `b_e≤min(b_v,t_e)` 且总量 `a b_v`，分解为大小恰 `a` 的 child 子集。每个叶资源激活概率不超过配置的 unit 边际，所以所有外机的期望请求仍不超过 1。支持可能指数大；该步骤是共同存在证书，不宣称生成总位多项式的 schedule。

在一个满 `a` 叉高 `h` 树中，命中全部满 `r` 叉高 `h` 子树至少需要 `(a−r+1)^h` 个叶。状态内单射把叶数转为不同外机资源。为每个 root 的候选树的每个满 `r` 子树建立含 root tag 和 `r^h` 个资源的超边，总边大小为 `r^h+1`。共同资源容量给任意 root 子集 `I` 的资源 transversal 下界 `(a−r+1)^h |I|`；若该数不小于 `2r^h−1`，按已核对的 Annamalai/Haxell 版本得到覆盖全部 root 的匹配。匹配选出的真实子树回填原 jobs：活跃内部机负载 `1+(d−r)/d=2−r/d`，未选节点和未选状态全父置负载 1，外机至多一枚 unit。取 `r=floor((a+2)/3)=ceil(a/3)` 后条件自动成立，得到 `OPT≤(5/3)T`；`T≥2` 用全父置 `C≤2` 补齐。该结论是存在性，不能称任意变参下输出匹配的确定性算法。

# 非单射过滤承诺

若原实例实际 `OPT≤1`，selector 所在状态的所有 small 必须逐层下送，所有叶 unit 到外机，因此被选状态必为单射且跨 root 资源不重叠。删去非单射状态仅作为 selector 候选，在剩余状态上解共同 `lambda` LP：无候选或 LP 不可行保证原 `OPT>1`；LP 可行则对保留结构用五三存在性，再把被过滤 state 的全部原 jobs 父置，得到原完整实例的 `C≤5/3`。这只给 promise 区分 `OPT≤1` 与 `OPT>5/3`，中间带可任答；不保证非单射原实例 CONFIG gap≤5/3，也不输出 Haxell 调度。

# 独有内容和处置

- Exact：冻结 v2 候选陈述，新增 A（`CONFIG(1)` 与共同 λ 等价）、B（任意可行 `T<2` 的五三存在性）、C（非单射过滤的严格承诺接口）。处置：`integrated` 到既有定理。
- independent cover：最完整的局部配置正部充分性、共同 `a`-树质量和 blocker/Haxell 资源计数；核对了 `2r^h−1` 严格阈值和总 rank `r^h+1`。处置：`integrated` 到既有定理，保留独立论证身份。
- independent literal：独立逐字重构 A/B/C、端点/零概率/`d=1,h=1` 退化和位复杂度边界；未读外部 Haxell 原始证明全文。处置：`integrated` 到既有定理和本批审查。
- independent shared：共享标签攻击视角再次核对 A/B/C 量词，明确配置 LP 可行与真正匹配调度之间的存在性间隔；非单射过滤只删除 selector 候选而不删原 jobs。处置：`integrated`，不新建反例。

# 严格保留的缺口

四源没有新软件或有限运行；不认证生产实现、一般 unrelated-machines 近似、NP-hardness、UM-TARGET-v1、Haxell 1995 原文或全球新颖性。共同 lambda、状态内单射、完整原 jobs 回填和私有内部机器是不可删除的承重条件。与已有 v1 proof/read-after 和 v2 author-proof read-after 的关系是版本互补，而非重复定理；第三阶段只需建立 provenance/核对边，不应把该批升级为更宽对象。

# 处置建议

四个 source ID 均 `integrated`，目标为 `archives/unrelated-machines/state/定理/私有注入树配置五三界与非注入承诺判定--定理.md`，并以本批审查作为独立证据入口。原始冻结来源保持在 `history/source/notes/...`，不复制或修改；checkpoint 和 `done` 由 Boss1 串行执行。
