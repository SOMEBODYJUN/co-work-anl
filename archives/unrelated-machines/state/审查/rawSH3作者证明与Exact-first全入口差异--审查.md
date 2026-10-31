---
id: "unrelated-machines/raw-sh3-author-proof-read-after-inclusion-entry-cut"
kind: "review"
type_tag: "审查"
title: "raw SH3 作者证明与 Exact-first 全入口差异"
status: "integrated-scoped-author-proof-audit"
truth_status: "author-proof-consistent-under-explicit-raw-sh3-contract; no-global-hardness"
review_level: "full-source-read-after-exact-first"
scope: "ordinary-job raw SH3 inclusion-entry cut; degree-six common functional and finite floor/bit bounds"
source_refs:
  - "clean:cdc1792de9afcc2d4a14"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_inclusion_entry_cut_author_read_after_v1.md"
  - "clean:1444ad7e876999f0a6ff"
  - "clean:69b54480b55976701857"
  - "clean:a083b5f2d1a594ab06f8"
  - "related:unrelated-machines/raw-sh3-conditional-subtree-flow-inclusion-cut"
---

# 来源身份与阅读边界

本页整理 `cdc1792de9afcc2d4a14` 的完整审查。冻结路径为 `history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_inclusion_entry_cut_author_read_after_v1.md`，原始尺寸 6002 bytes，SHA-256 `704bd6ca24eb1a059275bb54e3601b695fd5e6bde735bd56aedd227271a8b96a`。来源标题是“包含图 raw SH3 入口切：作者证明实际读后对照”，记录审查者在先读 Exact-first 后再读作者 proof 的结果，因此是知情 read-after，不是第二份 blind Exact-first。

该记录明确只实际读取作者证明的引言和 §1–7，并核对对应 Exact-first 的哈希及数学断点；没有读取作者 audit/code/output、general-DAG 新合并稿、Bamas primary，也没有运行软件。本页不把这些未读材料或作者自报的程序结果升级为本轮证据。

# 1. M3 零支付与 projection 范围

作者从同一物理机器上两个不同 unit endpoint 的 CONFIG 二阶零矩出发，令 `n=RR'`。Boolean 约化给 `L(n^2)=L(n)=0`，所以 `n` 是共同 `M3` 的零范数列，并与次数至多三的多项式正交。对任意 linear `l`，`nl` 的次数不超过三，且

`L((nl)^2)=L(n l^2)=0`。

因此 `nl` 也是零列，再把 `n` 与次数至多四的乘子配对，可得 `L(nw)=0`（`deg w<=4`）。这正好支付 raw inclusion 证明中总次数不超过六的 Boolean 乘积：同机入口子族和其补量可视作幂等投影，至多总共三个此类 linear factors/projections 的乘积 `P` 满足 `L(P^2-P)=0` 和 `L(P)>=0`。

范围必须保留：该支付只覆盖证明中实际出现的二或三个投影，不能解释成“三个投影之后还能任意追加其它因子”。Exact-first 中较窄的 pair-null/unit-capacity 引理与这里较强的提升不冲突，二者是同一合同的不同证明强度。

# 2. 作者全入口质量与 Exact-first 固定子族的差异

Exact-first 固定 `U_S` 的原始 `f`-entry 子族，写作 `F_SW`，并定义对应入口质量 `L(A F_SW)`。作者 proof 改取中间机器 `B_W` 的**全部** incoming `f` entries 之和 `C_W`，令

`b_W=L(A C_W)`, `y_WR=L(A C_W X_WR)`。

这是一个更粗但合法的入口质量。因为 `F_SW` 是 `C_W` 的子和，且额外项的 `L(Ax)` 非负，Exact-first 的固定 `S` 下界继续推出

`\sum_{W\supseteq S} b_W >= delta d_1 p`。

额外祖先、inactive row 或其它来源的外送只增加 `b_W`，不会破坏下界；每个 `W` 的坏终端数仍由同一包含结构给出，等于 `M`。因此作者使用全入口 `C_W` 并没有偷偷改变原任务身份，但它也不能被误读成每个 `f` 的质量都来自固定 `S`。

作者对 `B` 的 load localizer 使用原多项式 `A R_j`（次数二），其最高总次数为五；同机 pair-null 和 M3 支付足以推出式 (2.3)。这是原共同 functional 下的多项式推导，不是先条件化后免费获得一个新的可行点。

对 `p=A x(1-C_W)`（次数三），`L(p^2-p)=L(Ax(C_W^2-C_W))=0`，得到 parent-bound。对同一个物理 `Z_R` 的全部原 `e` endpoints 累加，再用 `A(1-C_{Z_R})` 的非负平方，得到

`sum_W y_WR <= p`。

这条共同 terminal capacity 包括所有 `W`，不能为每个祖先或每个 terminal 重复分配容量。`delta d_2-M` 非负和负的两个分支分别处理；等号情形左端为零，符号没有跨分支偷换。

# 3. 完整 original jobs、CONFIG(1) 与有限界

作者完整 CONFIG(1) 分布与 Exact-first 重构一致：`U` 的 selector/all-home-f；`B` 的 singleton incoming-f/all-home-e；`Z` 的 singleton incoming-e/empty。原 endpoint 边际的和恰为一。关键总量为

- `a_B=K d_1/(N C)<=1`；
- terminal 总质量 `d_1 d_2/N <= C/N <=1`；
- selector unit 质量给 CONFIG optimum 恰一。

对任意 `S\subset W`、`R\subset W` 的一条 f/e 链，其余 original jobs 全回 home，实际路径峰值至多

`max(1, 2-1/d_1, 2-1/d_2)`。

这是完整调度的上界和 job 身份审计，不是有限 `q` 下的精确 OPT 断言。原证明仍把 unit 独占、同 `B`/同 `Z` 的完整 job 计数放在同一容量预算内。

# 4. floors、渐近支付与 bit scope

作者使用 `e_1=K s_1/C`、`e_2=s_2/K` 支付

`d_1=floor(C/(K s_1))`, `d_2=floor(K/s_2)`

的取整损失。在 `delta d_2-M>=0` 分支，`d_1>=1` 使 `e_1<=1`，因此把 `d_1` 的下界乘到非负项并代入 `d_2` 的下界时方向保持。对充分大 `q`，取 `e_1<=1/2`、`e_2<=1/4`、`s_2M/(delta K)<=1/4`，右侧可保守支付为 `delta^2/(4q^(a+b))`；与 `H/C` 的指数衰减比较后仍得到严格 FAIL。作者此处的常数比 Exact-first 的较窄 `1/8` 支付更强，但结论身份相同。

二项式/H/M 计算只涉及 `O(m)` bits，且 `m<=N` 已由显式物理机器数支付；该记录没有声称 exact SDP feasibility 的位多项式算法，也没有把 binomial arithmetic 当成巨大矩阵构造或端到端软件认证。

# 5. 真值、来源关系与未完成义务

冻结结论是：在明确 ordinary-job raw SH3 合同下，作者 proof 的 projection/null、全入口 flux、共同 terminal capacity、完整 jobs、floors 和 bit 界均与 Exact-first 一致；本次未发现新的核心 fatal 或“免费条件化”漏洞。独有差异是作者采用 `C_W` 的全部 incoming，而 Exact-first 固定 `F_SW`；这只改变入口质量的粗细，不改变必要切的量词或容量共用。

以下边界不得省略：

- 记录没有读取 Bamas 原文来认证 §7 的 assignment-LP、shadow 或 `rho` 对应；不能将作者引述升级为外部文献定理。
- 只覆盖该明确包含族的 ordinary-job raw SH3；不是 hierarchy integrality gap，也不反驳其它编码的论文结果。
- 没有给一般 UM 算法、near-two gap、Karp/PCP hardness reduction、actual integer forest decoder 或软件认证。
- rational `T`/real `delta` 的定义域澄清仍需由 canonical 正文显式说明，例如用略大的 rational `T'` 单调解释；本来源本身没有完成该补款。
- growing-depth 下 shared integer ownership 与 first-moment subtree flow 的耦合仍开放；必要流或 sound FAIL 不等于存在实际 forest。

因此该来源应与已有 `rawSH3条件子树流与集合包含切` 资料合并作为作者 read-after/provenance 审查层，处置为 `integrated`；不得单独新增“真困难性定理”。证据原件和 manifest 在 `archives/unrelated-machines/tools/evidence/raw-sh3-author-read-after-20261031/`。
