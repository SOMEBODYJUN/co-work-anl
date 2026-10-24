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
| 第二篇 | `04190ddf297500eb24af37280b1dc61f9f6ce5d06f88065f755a85c93deb2e10` | `22a9be2ddbcff76b8c03f2209cf3a7c2e51316e45b27b0df9c256006cf4a23de` |
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
