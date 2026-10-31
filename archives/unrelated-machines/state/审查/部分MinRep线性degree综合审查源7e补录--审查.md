---
id: "unrelated-machines/partial-minrep-linear-degree-synthesis-source-7e"
kind: "review"
type_tag: "审查"
title: "部分 MinRep 线性 degree 综合审查源 7e 补录"
status: "integrated-cross-version-synthesis"
summary: "完整实读 7e6307ae7f378198a89b 对 partial-MinRep v2 线性删边、v3 高围长与 v5 度数质量复制的综合审查；其独有价值是把独立重构、读后攻击、外部 primary 边界和三版本量词放在同一审计索引中。稳定数学对象已分别归档，本页承接跨版本关系、避免把旧审查合并为新定理。"
source_refs:
  - "clean:7e6307ae7f378198a89b"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md"
related_archives:
  - "../资料/partial-MinRep线性degree删边源与外部边界--资料.md"
  - "部分MinRep高围长v3三源精读与随机repair边界--审查.md"
  - "部分MinRep高围长v3读后后缀三源与概率措辞校正--审查.md"
  - "部分MinRep度数质量v4-v5陈述与域修复补充--审查.md"
  - "部分MinRep线性degree陈述先行独立审查增量--审查.md"
---

# 实读身份与处置

`7e6307ae7f378198a89b` 的 `clean show` 全文 13,306 字节已实际读取，SHA-256 为
`bf250c421e94ab19811ba04d5481a70af9c4f612b6f36587e7a33668d98108be`。来源是跨版本综合审查，不是一个新的删边定理：它重新核对 v2 的 cheap-list/一次 trimming/严格 ceil 与 fee 接口，随后把 v3 高围长 repair 和 v5 度数质量复制的独立稿、读后稿、外部 primary 比较及域修复并列。原字节保存在本批 evidence 目录，receipt 记录本次完整阅读和去向。

处置为 `integrated-cross-version-synthesis`。v2 的显式随机删边与线性 degree 必要性仍以 `partial-MinRep线性degree删边源与外部边界--资料.md` 为稳定正文；v3 的正规/高围长随机 repair 由对应三源正文承接；v5 的非空 alphabet、异长 fiber、degree mass 和 primary FMW 边界由 v4-v5 审查承接。7e 源的唯一新增是一个交叉索引：它把三版共同保留的严格量词、随机概率层级、外部来源未认证范围和 physical fee OPEN 状态放在同一读后审计中。它不产生第二套参数，也不把不同版本的 `D`, `g`, `rho`, high-girth 或 alphabet 条件静默拼接。

# 1. v2 线性删边核的再核对

7e 重读确认 v2 的输入是显式、平衡、D-regular total-projection game，允许平行 constraint 边；`g>=2`、`0<rho<=1`、`tau=rho/(100g^2)`、`gamma=rho^3/(10^9g^8)`，二分抽样后只按中间 degree 做一次 trimming。它保留三个不同量词：每个 seed 的最大 degree 和完美完备性、NO 情形至少 `0.9` 的同时 cheap-list 禁止、以及任意非空 balanced game 的线性 degree 必要性。heavy-list 抽样、rare covered upper tail、总边数下尾和 size-biased trimming 共同组成概率账；不能把单一列表或单一 seed 的结论改写成统一 deterministic soundness。v2 仍只是显式投影游戏接口，外部 PCP、NP⊄BPP 后果和实际 UM fee/compiler 都是条件或开放边界。

# 2. v3 高围长与 v5 度数质量的分离

7e 的 v3 段落复核了正规、高围长输入中 template 子图、permutation 暴露、cycle/factorial-moment、同型 repair 与全部 lists 的同时概率；它也记录旧字节中的 `2dN` 保守多计与 `z>GB+4U+1` 的不等式勘误，以及 Kun/DKR 只作比较而非隐藏前提。该内容与 v3 三源正文一致，不能把 v2 一轮删边的 output 直接叫 high-girth repair。

v5 段落复核非空 alphabet 修复、异长 fiber 的暴露求和、source-tag clone 保值、逐 copy/typed bit cost 和 FMW primary 只提供 fixed-error/exactification paper fact。v5 保持 typed domain 与所有 lists 量词；不把原 v4 空左域字面问题倒升为已证明全域，也不把外部 primary 的 regularity/degree 常数当作自足推论。相应结论和读后攻击已有独立 v4-v5 正文，本补录仅登记它们在 7e 综合审查中的交叉位置。

# 3. 比较、缺口和后续使用

与已有归档逐段比较后，7e 没有遗漏一个需要另立定理的数学对象：其 v2 常数和 strict boundary 由资料页与 statement-first review 承接，其 v3/v5 独立推导和读后攻击由相应审查页承接。实际保留的独有内容是阅读顺序、跨版本 provenance、外部文献读取范围和“不把共同框架误写成新颖性/物理实现”的审计警告，已在本页与 manifest 标明。

引用本补录时必须按版本使用相应正文的参数；不得把 `O(g)` degree、high-girth repair、v5 alphabet/fiber 约束和 v2 cheap-list fee 代数合成一个未证明总定理。7e 未运行新的生产脚本，也未提供实际 UM decoder、fee=1 或六人 SPE 覆盖结论。