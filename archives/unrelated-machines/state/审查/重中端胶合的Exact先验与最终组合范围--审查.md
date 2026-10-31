---
id: "unrelated-machines/heavy-medium-gluing-exact-prior-and-final-combination-scope"
kind: "review"
type_tag: "审查"
title: "重中端胶合的Exact先验与最终组合范围"
status: "five-frozen-sources-fully-reconciled"
truth_status: "strict-witness-gap-theorem-internally-reviewed"
review_status: "historical-exact-first-with-authorized-foundation; author-and-final-read-after"
summary: "保全五源原字节、真正Exact-first的旧基础先验、两稿同路线、作者十项和canonical十项全核对及T0/控制字节修正，不把whole SHA变成全稿认证。"
legacy_ids:
  - "UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/heavy_medium_presence_strict_witness_gluing_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/heavy_medium_presence_strict_witness_gluing_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/heavy_medium_presence_strict_witness_gluing_independent_review_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/heavy_medium_presence_strict_witness_gluing_author_read_after_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/heavy_medium_presence_strict_witness_gluing_canonical_read_after_v1.md"
---

# 1. 五个主源和真实先验

本页保存审查资源，数学完整构造见[完整分量证明](../证明/重中端严格双见证的完整分量胶合--证明.md)。五原件已逐份全文实读并重新核inventory大小/SHA，原件见[manifest](../../tools/evidence/heavy-medium-proof-history/manifest.json)。两冻结提交指同字节，不当两次数学活动。

| 源ID | 原角色/大小 | SHA256 |
| --- | --- | --- |
| 17f4bdb12baa1e64a1f9 | statement-only Exact，3623B | f9dad0a0f70f272446042091e0bb400c7a87c6a3f96bae512cfbed34c230183e |
| 61a697b0d7eeb9361187 | 作者Proof，7691B | 48f5ac5459cfcc5ef62244b830207c72b4700521df9e9e68bc6e5fb8ae82dee1 |
| da891b36e1b3231bd29d | Exact-first独立完整证明，8255B | ab6b2472da757bed7428fdb629b386d06b51b78429b0c3c90a1fd15bcbb7a3a9 |
| 824269c33c2e6b8869fb | 作者Proof实际读后，4348B | 32de696171941e598eaf388e0a01d6e42e8351fca14b39a87e05daf8f208e7a2 |
| e4984b6192106f26116f | canonical新§8最终读后，4003B | dec3f3a6fc9e3251dc0b9f0ce1f7741526e526604eebac8182efe1a5615760a4 |

原记录日期2026-10-18。作者先把Exact和Proof分开；Exact文件明确是候选陈述、无作者证明且待独立重构。general_query_response_review先仅读新Exact及parent明确许可的旧unit/tiny基础SHA **1d5d27a9a80c64dbcca319531da735f23b1d65e29d1ef1f16a011a85a4adf4ba**，未读新作者Proof、未询问作者构造，冻结8255B独立证明后才首次读作者Proof，再冻4348B读后；最后才读canonical新§8及组合上下文、另冻4003B最终读后。独立稿/旧记录字节未改。

旧基础已经包含matching分量和不等成本两选择舍入，独立稿明确使用它们。历史独立性是**新Proof之前的独立推导**，有获准旧基础先验；不冒零背景盲审。本轮清洗早已读全部资料，不把本轮比较重新叫Exact-first。作者Proof与独立证明同数学路线，区别是冻结的先后和独立核对，不虚构成两种算法。

# 2. 新Exact和旧基础的承重区别

新Exact不预给策略，完整指定正T、两actual峰≤T、ε<1/2、a<1−ε、仅见证已用端两档、输出原两端、全部原jobs及任意两位heavy-presence，承诺确定性总位多项式和B=3/2+(ε+a)/2。旧unit为精确1与1/k、T=1+1/k；旧tiny为精确1与[0,a]、T=1+a。不能从旧T<2的unit匹配直接偷渡heavy成本相等：新匹配须重新由2(1−ε)T>T证明，内部heavy身份替换须新计εT。

作者Proof与独立稿共同给的完整数学为：匹配四类分量；两测量机在不同颜色1端点分量；单路翻转全机(1+ε+a)T；其它分支全部job—machine active、真实medium/virtual原端选择；共同二染色增量aT/2；最终三行1+ε+a/2、3/2+(ε+a)/2、1+a/2。证明页已完整展开，不仅留“通过”或路由。

该Exact初态候选与后来证明成立的状态同时保真：statement-only的候选身份不是缺证明的现行主对象，也不能因后来审过把原Exact改写成含证明输入。

# 3. 作者Proof读后十项全部义务

作者读后先列Exact/独立稿/Proof三SHA，明确本次不读其它作者新证明、repo正文或Work，仅在新Proof实际读取后比较。其十项为：

| 原项 | 实际检查与承重内容 |
| --- | --- |
| 1 | 重图为原job—原machine二部匹配；每机≤一heavy来自2(1−ε)T>T，共同边固定；不误把cross-role job当heavy-only。 |
| 2 | v/w为颜色1machine端点；machine—machine两端相反、job—machine仅一机端，故不同分量；实现同一份mixed而非拼两份单机存在解。 |
| 3 | 内部heavy最多加εT，新medium≤aT可叠同机，两项均计，全机(1+ε+a)T≤BT。 |
| 4 | 全job—machine active只删平均half-medium；job—job恰留一原端点job于medium；virtual仅方向编码，恢复全部原jobs一次。 |
| 5 | virtual成本可异、目的机可同；同机选廉可能改变其它机heavy身份，但每机仍至多一heavy且≤T，全机表覆盖关联。 |
| 6 | incidence的job/machine对为两匹配，路径/交替偶环二染色，每项一端；排序交错差给全部机器共同aT/2，非逐机期望。 |
| 7 | 三类全部原机器完整负荷如上，00类无重边所以不新增heavy；不遗漏非测量机。 |
| 8 | 仅σ₀/σ₁已用有限端入图/输出；其它有限端可gap中、任意大或0，不偷要求全P两档。 |
| 9 | a0、ε0、静止/共同边、同机virtual异成本均合法；图线性、有理排序和部分和总位多项式，不按参数倒数循环。 |
| 10 | ε+a<1给B<2；只否定裸presence读口，不锁job身份/其它边界/源标签，不改旧unit/tiny域/锐性，不给一般算法、困难性或全参数sharp。 |

该记录结论为作者Proof与独立重构一致、声明全域无standing fatal，无需数学修订；不是对未来尚未读canonical的预先批准，也不是软件测试报告。

# 4. 最终canonical十项及whole SHA的范围

最终实际通读canonical新§8及其旧§1–7上下文，whole SHA为 **0b9ab7d50bba3b4b7c5825c6208e51d23d20cdb5460d8e7478a6ef866f986e00**。本批已核并阅读全文，冻结比较字节保在证据包。正式批准的是**该SHA的新§8数学与组合**；whole SHA锁承载文档，不自动另认证旧§1–7全部主张、旧锐族的软件或一般研究目标。

| 最终原项 | 完整组合核对 |
| --- | --- |
| 1 | 新ID、T>0、两actual≤T、ε/a域与Exact相同，未偷加旧unit或T=1+a。 |
| 2 | 仅实际已用端两档；输出原端/全部原jobs一次；读取heavy-presence而非任务身份/源标签。 |
| 3 | B=2−[(1−ε)−a]/2的等式、gap≥κ的阈值及00/11原见证正确，无未知见证oracle。 |
| 4 | 新heavy匹配按2(1−ε)T>T成立，旧§2仅组合事实；两测量端点分量可同时定mixed。 |
| 5 | 单路翻转加εT和aT且可叠同机；不能沿用精确unit时间不变。 |
| 6 | 全active、真实medium与job—job virtual的半半质量≤原均值，全部原jobs恢复。 |
| 7 | 旧§7加权引理按成本上界aT缩放；不继承其容量规则；同机选廉、异成本/零成本及共同aT/2界。 |
| 8 | 三行完整负荷均≤B，00机不会新增heavy，全部机而非只v/w。 |
| 9 | 静止/共同边、a0/ε0/同机virtual、有理位长及不按倒数展开。 |
| 10 | 不添全参数锐性、一般算法/困难性；追加§8前的旧§1–7字节保持先前SHA。 |

原最终review称通过、无standing fatal，仅内部审查。原root简review377a另亲核翻转叠加和三行界，已是前批done源，本批只作比较，不重复计主源。

# 5. 两项修正和可复核字节身份

首次组合稿式(6)中LaTeX反斜线被字符串转义成TAB/FF/VT/CR控制字节；root在发布前定向修复，最终命令为真实反斜线。原最终review另发现句子“T=0不在本ID域，由旧身份分别处理”末尾无旧身份支持：旧unit/tiny容量均固定正值。删去后仅“T=0不在本ID域。”。这是删去不成立的跨域指称，不证明T0新结论，正T数学不变。

本批实际[身份核验](../../tools/evidence/heavy-medium-proof-history/identity-verification.json)检查：

- 五主源和两比较原件均等inventory size/SHA。
- 最终canonical没有LF之外的ASCII控制字节（含DEL检查），式(6)保有真实`\tau`、`\frac`、`\varepsilon`、`\right`、`\tag`命令。
- 取最终原件第一次`## 8.`之前字节，再去除为新节追加的最后两个LF，得到15542B[重建旧基础](../../tools/evidence/heavy-medium-proof-history/derived/unit_presence_pre_heavy_foundation.md)，SHA精确等于1d5d…4ba；该原文已全文实读。它是从最终源精确恢复、经独立稿命名SHA核实的派生字节，不冒作新增冻结inventory来源。

没有首次坏draft的独立原件，故不重建或声称比较过坏稿原字节。控制字节的发生/修复和旧T0原句由冻结最终review直接报告；当前最终字节和旧基础身份另有实际核验，两种证据地位分开。没有数学程序或有限调度实验，身份核验脚本只检查内容字节，不把旧uniform枚举归本heavy域。

# 6. 全部独有内容去向与准确接续

Exact的全域/四输出/原端/全部任务/位长/裸读口后果完整入证明页§1/7/8；作者Proof六节和独立稿六节完整构造共同展开于§2–7，两稿原字节独立保留；独立稿额外明确获准旧基础、严格flip余量和分母总位界；作者读后十项入本页§3，最终读后十项及修正/旧前缀身份入§4–5。没有以同路线为由删去先验或证明资源。

与旧unit/tiny是改变时间域和容量的限定推广，不覆盖旧uniform更强逐k锐界；与任意异权query-return或共享outside是不同读口，详见证明页§8。算法是给定actual后重组的数学算法，不是一般输入近似或未知strict finder；finite experiment/软件/外审/全球新颖性/新上界全参数锐性均未认证，UM主目标和六人SPE均未由此完成。

这五源现在有完整数学及版本去向。阶段二只记证明/条件推广/来源与范围关系，未重建阶段三超图，不把“内部通过”独立作逻辑前提。
