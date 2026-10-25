# 三篇成文：实际检查与修订范围

本记录区分数学检查、表述审读和构建。它不更改原 Claim 身份，不认证优先权，不替代外部同行评审。基线为 `69e6012bd585e1e1b53b7535a1cff661fe35a855`；每次检查以下列源码 SHA-256 绑定版本，而不是以文件名表示覆盖任意后续稿。

## 第一篇：共同目录双设施

初稿数学检查输入：`main.tex` SHA-256 `c712665b5136b472f5dac525494ef50a8d9206fc7cbcfbf1a5acf72f4a58d8bd`，包括三个完整附录和 bibliography。独立检查者未继承写作者上下文，按定义重构菜单、坏环和完整续局义务；检查者确认已读完全文，阶段回执未发现已确认的致命异议；最终回执没有完成，因此不登记独立数学审查PASS。

Harks–Klimm 范文校准后的源码 SHA-256为 `6aaa893eeab3f818fdfee71819830e4880bee66365a077a4d66c092190ec4c3e`。正式陈述、显示公式、标签和附录证明与初稿保持一致；主agent已核对叙述diff：公式、正式陈述与附录proof保持。完整独立editorial读者因工作区额度错误中断，没有可验收报告；不能登记PASS。

## 第二篇：任意设施数

独立数学检查完整读取227行初稿和bibliography，输入源码SHA-256 `ceb6cb53b7bcb18fcce4bc7c7fbdea4f7cb85890c0215e81f0b6707a3c9f0dbe`。未读取原证明、其他审查或项目状态；按目标重构在轨NE、逐偏离精确NE与上界、续局兼容性、默认规则和显式证书五项义务。

检查未发现致命异议：字典序比较保持源坐标在目标阈值之上；源地点消失时两类orphan预算保留；装箱的重原子单独放置；严格改善不破坏cap且平方负载势终止；不同标签偏离的目的子局互异。零覆盖、同址和未服务客户均按模型处理。验证的是数学论证，未核验文献优先权。

发现并修正两项精度问题：

1. `each client`在摘要、结果描述及主定理的在轨随机化说明中，应限定为被覆盖客户；未服务客户概率仍全零。当前改为 `every covered client`。
2. 编码证明不能只用输入权重分母的乘积来估计在轨负载分母；还需除以同址设施数。当前说明每个负载额外乘至多k的整数，其位长多 `O(log k)`，原多项式编码结论保持。

修正及英文校准后源码SHA-256 `c8bfa0d94aaf22a732338fba5b1cc9216ba878329c62ddca04f485858240172a`。所有显示公式和其余六段证明逐字不变，仅最后的编码证明修正分母说明；另有叙述调整。原检查者的bounded delta已通过：15个显示数学块逐字一致，前6段proof逐字一致，第7段仅修正分母说明；原两项问题已关闭。完整隔离editorial报告另见下文，旧版检查不自动覆盖后续修复。

## 第三篇：加权拥塞

独立数学diff检查输入：旧稿SHA-256 `65dbc684fac86dccfdbafa116bdce118bff04369fa400859c97a00c204c5271c`，新稿SHA-256 `b1776c3c161330d6766f3b566858173872b0cc4f0693472ac6b6ddab3ac9d64a`。检查者未读项目旧审查，允许读取两个冻结全文、bibliography和实质改动日志。

已机械核对24个正式命题陈述逐字相同，120个旧标签全保留；旧22段proof中21段逐字相同，共同尺度proof改写，另新增统一族与近次数定理的短proof。已收到的独立回执核对共同尺度改写、移位前提、全状态接口、新参数例及短proof依赖，尚无已确认致命异议，但最终回执没有完成，不登记完整PASS。这个diff检查不称为从零认证全部旧技术证明。

完整独立editorial reading没有完成报告；不能把读完材料或阶段观察当作审查PASS。

## 构建与最终交付状态

各写作者均实际编译；初次产物为第一篇25页、第二篇8页、第三篇26页。统一构建脚本已成功运行；局部修复后重构建第二、三篇。最终log无错误、未定义引用或Overfull。三篇全部59页已渲染并检查逐页排版概览，未见裁切、公式越界、页眉碰撞或空白缺页。视觉核查不替代证明。

最终期刊和作者信息尚未确定。不能因检查通过而将这些成文稿称为已完成某刊格式或已投稿。


## 第二篇完整editorial报告与修复裁决

[原始隔离审读报告](../reviews/facility/multiple_facilities_article_editorial.md)完整读取冻结的c8bfa0d稿与bibliography，未读引用来源或其他review。保留真实原判：Necessity audit **PASS**；Referential-precision audit **FAIL**；Overall editorial verdict **FAIL**。不把修复后的自查伪称新隔离审读PASS。

| Finding | 观察与成功标准 | Burden / repair裁决 | 实际修复与关闭依据 |
| --- | --- | --- | --- |
| SE-1 | Case2的these clients最近先行词只有新增客户，而packing必须包含原J_t | accepted / reader's | 明确原J_t与新增客户合并，并对地点t全部已分配客户装箱。主agent核对原预算、公式和路线保持。 |
| SE-2 | 默认规则用least-index client，有限客户集却未固定顺序 | accepted / reader's | 默认规则首先固定客户枚举，按此取首个改善者；不新增模型假设。 |
| SE-3 | 描述性packing/cap别名代替已编号引理 | accepted / reader's | 直接引用lem:packing及lem:capped。 |

三项发现均有实际改文，主agent逐段diff核对并重编译；未再运行一轮隔离复审，故状态是“已实施修复并自查关闭”，不是新editorial PASS。上述3项各映射一个修复，原始FAIL不覆盖为PASS。

## 第三篇阶段回执后的范围澄清

独立复算确认n=2,d=2^21满足统一族条件：d≥8n；T=(17/16)^d≥d(d−1)/512>32d；400(log d)^2<400·21²<d/3<d log(3/2)。目标倍率2^20；未声称该例最小。

依阶段审查的非致命观察澄清：ordered-marginal段的section改为subsection；深度推论指向主文构造及附录验证；相位归一化只保持基础window游戏成本，完整锚定门泄漏另按最坏预算支付。没有改变正式陈述、公式、参数或全状态证明路线；最终diff回执未完成。

## 最终交付版本

| 文章 | TeX SHA-256 | PDF SHA-256 |
| --- | --- | --- |
| 第一篇 | `6aaa893eeab3f818fdfee71819830e4880bee66365a077a4d66c092190ec4c3e` | `c9b1deb3bd400142626c12e6cba0aa8665226f058d06c89506e99125763c19c5` |
| 第二篇 | `e745ec526dccb9f874837729c6ec3d092ea6ea9e44edf602a749cef9f18fe922` | `e7aa2337c1979bef95d78dc2afc4ed383d3142d6bd193f72c0be94f67d5c94fd` |
| 第三篇 | `f6f65fd53db59261933663ca08cbf042e2cc0eb8d93cfe66b2138b0212d9af0f` | `ee30c135b9825353328ed1ff3ad5f9757bfe9fce8065982b9b99e1121f29c7d8` |

三篇结构成文和PDF已完成。剩余工作是第一、三篇未完成的独立审读回执、第二篇修复后的新隔离复审，以及主人定刊后的格式转换。当前不是某刊最终提交包，外审与新颖性仍独立未认证。

## 第一篇 round-1 修订与 round-2 状态

Round-1 referee findings were repaired in the shared-catalog source:

- the false equal-reach quota sentence was removed;
- the large-pair chord now states the normalized no-witness scope and derives
  its quota inequality;
- the common-\(h\) reach-order implication is written as an explicit
  contradiction before \(\Delta=R_s-R_t\) is introduced;
- the fixed-largest-client stability bound is stated for every intermediate
  repair state; and
- the polynomial strong-chord constructor now gives an ordered branch table
  with exact tests.

The revised first-paper source passes the proof-sanity audit (zero duplicate
labels, undefined references/citations, environment warnings, and unlabeled
theorem-like blocks). The fresh build has no LaTeX warnings or overfull boxes,
and all 26 rendered pages were visually checked. The revised source hash is
`fcf7d3a912cc1140d6b2fb700a8233f9ec1e67485d5062af7fcf78b7ed31f555`; the
revised PDF hash is
`3c2a384564e21d9cab30e9a374eb579de2d15a572c1f7e8e4066af3284af39b7`.

A fresh targeted independent review of these repaired proof regions is still
pending. Until that review closes, the first theorem is a repaired manuscript
claim, not a publication-grade verified proof.

## 第二篇 round-2 完整闭环（当前）

第二篇已完成针对当前正文的独立第二轮 proof audit。审查者从模型、字典序选择、在轨 NE、两类源地点转移、原子装箱、重原子 cap、全部单方偏离、续局补全和有理证书重新推导；结果为 **S0=0、S1=0、S2=0、S3=0、S4=3**。前一轮的重原子不变式问题已关闭，3 个 S4 均为表述澄清并已采纳：

1. 明写占用目标旧负载 `W_t/q_t>((q_t+1)a)/q_t>a`；
2. 固定有限最大值的 tie-breaking 顺序；
3. 把未列出布局的续局明确为 succinct default-rule program。

证明审查记录见 `research/manuscripts/multiple_facilities/REFEREE_REPORT_round2_proof.md`，逐目标 review notes 已通过 `lint-notes.py`。英文清洗的最终门见 `EDITORIAL_REVIEW_round2.md`；没有必须修的语言问题，也没有为缩短篇幅删除证明承担的分支。最终源码和 PDF 均通过 proof-sanity、编译日志检查和 8 页逐页渲染检查；最后一页孤立参考文献行已通过版面调整收回。

团队将第二篇主投定为 **SIDMA**，采用 SIAM 最新标准宏包 `siamart251216`；官方要求、摘要/关键词/MSC/短标题和作者元数据清单见 `VENUE_TEMPLATE_REVIEW_round2.md`。当前可复核 PDF 仍为 `amsart`，因为真实作者元数据未提供且官方宏包需在提交阶段转换；这不再是数学或写作审查阻塞。

## 第三篇 round-2 完整成稿闭环（取代上文第三篇旧版本状态）

第三篇当前稿是 TEAC `acmart` 单栏匿名审稿版，四主节与完整技术附录保持。最终源码 SHA-256 `3ee2db7cadce655e4534d27a0aa1b923ad2a05be383fe82ab8a7f781908cd847`，PDF SHA-256 `33727a90d83c2300658d1bcf89355c998f435af9ba6bdc4a8ef2d0c052407256`，27页。上文 `f6f65...`/`ee30...` 是前一轮的历史快照，不覆盖此新版本。

- 独立数学攻击从共同尺度、端点面积、两型校准、权深度、稳定核，到全部 front 相位、非法态和同次数预算以及社会成本，未发现 S0–S3；有限精确审计仅核对给定参数范围。第二位独立读者对格式、文献范围和写作修订做数学 diff，无新增 S0–S3。单项式 CF2021 的 `d` 上界扩展到非负多项式是逐项拆分的明确推论，不能记作文献原模型逐字陈述。
- 冻结全文两遍编辑审读先给 necessity FAIL / referential precision FAIL（八项局部问题）。修复后同一读者按 bounded delta 逐项确认八项 CLOSED，修复簇 necessity PASS / referential precision PASS。原始 FAIL 与修订验收分别保留在[第二轮报告](../current/weighted_congestion/structural_reconstruction/REFEREE_REPORT_round2.md)，不将 bounded delta 冒充一篇新全稿盲读。
- TEAC 主投、SIDMA 备选和 MOR 旧页数错误的纠正，见[选刊与模板核验](../current/weighted_congestion/structural_reconstruction/VENUE_TEMPLATE_REVIEW_round2.md)。编译测试采用 ACM 上游 v2.20 tag 的仓库外测试 class，正式生产 class、TEAC 门户细则及真实作者元数据仍需投稿前完成；没有上传投稿系统。27页已渲染核对无裁切/溢出，proof-sanity 无重号、未定义引用/文献或环境问题。

这些检查是内部证据，不是外审、新颖性认证或期刊接收保证；完整逐命题两遍 proof-review tracker 未完成。其他两篇版本与本节第三篇更新无关。
