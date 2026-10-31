---
id: "unrelated-machines/perfect-complete-seed-certificate-final-review"
kind: review
type_tag: 审查
title: "完美完备全种子拒绝证书最终读后与复杂度边界审查"
status: integrated
truth_status: "seed-certificate-and-probability-upgrade-consistent-with-source-contracts; no-UM-compiler"
review_level: "full-read-7499-byte-final-review-and-source-contract-comparison"
scope: "UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1 final appended section, partial Min-Rep v2/v3/v5 contracts, conditional fee bridge, threshold and coRP/coNP consequences, finite interface audit"
summary: "c8b4a86… 是对 partial Min-Rep final canonical 的全种子拒绝证书后缀审查。本文完整读取 7499 字节记录及其列出的 33322 字节整稿/5377 字节后缀 hash，核对 deterministic seed verifier、FAIL、NP=coNP 与逆多项式拒绝概率下 NP=RP=coRP=coNP 的量词、UM threshold、expected-time 修正、v2/v3/v5 源契约和有限 512-case 接口审计；与现有 partial Min-Rep/费用桥/pDM 对象去重，不虚构 UM compiler、decoder、外部 PCP 认证或一般 hardness。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/perfect_complete_seed_certificate_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/perfect_complete_seed_certificate_review.md"
  - "related-source:782a8563344b6f317c3e:research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md"
  - "related-source:7e6307ae7f378198a89b:research/reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md"
related_objects:
  - "部分MinRep费用桥与pDM阈值双源审查--审查.md"
  - "部分MinRep高围长v3读后后缀三源与概率措辞校正--审查.md"
  - "部分MinRep高围长v3三源精读与随机repair边界--审查.md"
  - "../定理/多状态图估值支持域计算障碍--定理.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/perfect-complete-seed-certificate-20261031/original/perfect_complete_seed_certificate_review.md"
source_sha256: "74150c482572b235758796732b95e1e9a7b5b1da4c15f22532fe02ad5e33695a"
source_size: 7499
---

# 1. 来源身份、完整读取和最终版本 hash

本轮完整读取 c8b4a86fcd061015fb8f 的 review 源，7499 字节，SHA-256 为 74150c482572b235758796732b95e1e9a7b5b1da4c15f22532fe02ad5e33695a。该记录称其先独立重构 seed statement，随后完整读取 final appended section，且重读 preceding v2、v3、v5 source contracts 和 conditional fee bridge；没有读取 linked canonical review，也没有重新验证外部 PCP papers。

它绑定的完整 canonical 文件是 partial_minrep_linear_degree_source_and_fee_bridge.md，整文件 SHA-256 33f5fb337e3d002e91aad79c6fb99f273ed01c1978d02fd0131e995a948e2114，33322 字节；实际审查的后缀从 heading “全种子完备源的拒绝种子证书” 到 EOF，SHA-256 40d7d2f0406f50aba5358140967a32deaf3404f3d2cef65bd7e72c0b6c2cf1fa，5377 字节。作者后续改动只有 line 374 的概率措辞和 line 350 的 expected-time 修正，均已实际读取；作者确认无其他变化。

该记录是 final post-read，不是外部同行评审；本页保存其复杂度后果、源契约边界和未闭的 UM compiler/decoder 义务。

# 2. 完美完备全种子证书的确定性结论

设随机完备 source generator R 对每条 seed 返回合法显式实例或 FAIL，且存在一个确定性 composite verifier D。source contract 要求：

- SAT 输入在所有 seeds 上都被 D 接受；
- UNSAT 输入至少存在一条 seed，使 D 拒绝；
- FAIL 按 YES 处理，只有合法非FAIL输出进入 D；
- seed 长度、时间上界和参数固定时均为输入长度多项式。

UNSAT 的拒绝 seed 本身是多项式长度证书：验证器猜 seed，若 R 输出 FAIL 立即拒绝该证书（因为复合判别器把 FAIL 按 YES 处理）；若得到合法实例，运行 D 并接受当且仅当 D 拒绝。Universal SAT soundness 排除任何 false certificate；UNSAT rejection seed 给出 certificate。故直接得到 NP=coNP，但不需要寻找 seed，也不声称所有输入共享同一 seed。

该结论要求 D 的接受/拒绝语义覆盖所有非FAIL输出，而不是只在某一好 seed 或 source promise 上成立。它是复杂度后果，不是 partial Min-Rep 的新删边定理，也不是 UM 编译器。

# 3. 逆多项式拒绝概率的随机升级

若进一步有 uniform worst-case polynomial sampler，且每个 UNSAT 输入都有逆多项式概率抽到满足 compiled NO/all-output decoder contract 的非FAIL seed，则独立重复足够多次即可把拒绝概率放大到常数，从而 SAT 属于 coRP。结合 RP⊆NP 和 coRP⊆coNP，得到

NP = RP = coRP = coNP。

这是比 NP⊆BPP 更强的结论，但没有声称 P=NP。概率要求必须施加在“编译后 NO 且全输出 decoder 合同成立”的 seed 事件上；仅知道 source-NO 事件概率较大，不能替代这个要求。final paragraph 的修订已明确消除这种潜在歧义。

如果构造器只有 expected polynomial running time，不能直接套用硬时间上界的 seed lemma。需要先截断运行时间，并重新分析截断失败/拒绝概率；若有统一期望界和逆多项式拒绝界，通常可选足够大的 polynomial cutoff 保留逆多项式拒绝概率，但该转换是独立证明义务。它不等于声称 expected polynomial time 永远不能转化。

# 4. v2/v3/v5 source contract 的逐项核对

| 版本 | universal YES/FAIL 语义 | unconditional good-NO 概率 | 读后结论 |
|---|---|---:|---|
| v2 | deletion 保留 singleton labeling；empty edge set 是显式 YES | 至少 0.9，且输出非空 | 与后缀表一致；D 必须覆盖 empty-edge YES |
| v3 | nonFAIL 输出复制 perfect labeling；capped permutation sampling/短环拒绝显式 FAIL | 与 nonFAIL 联合至少 0.8 | 与表一致；固定 G 与 Qgamma 域保留 hard polynomial bounds |
| v5 | nonFAIL typed output 保留 perfect labeling；alphabet 非空，capped sampling 显式 FAIL | 与 nonFAIL 联合至少 0.8 | 与表一致；fixed-parameter tag padding 与 uniform Qgamma 域分开 |

这个比较只检查后缀 lemma 对 v2/v3/v5 source contracts 的适用性，不重新认证前置概率不等式、PCP theorem 或 high-girth repair 的所有证明。现有 v3 后缀审查已独立记录 factorial-moment、fresh-image、repair 和 dN/2dN 保守计数修正；本页不重复建立高围长定理。

# 5. UM threshold、严格不等式和 remaining scope

假设一个实际 schedule 算法保证 ratio 2−epsilon，则选择整数 k 必须满足 1/k<epsilon；等号不能区分 promises。固定 k 的编码不需要编码 epsilon。严格 YES test 应为 C<beta_k T，NO complement 为 C>=beta_k T，其中 beta_k=2−1/k；边界等号必须保留。

source review 核对了 positive rational T、合法输出、exact rational load、zero OPT、empty jobs 和 UM approximation index k 与 PCP exact-k-to-1 fiber 参数独立。直接 verifier proof 只需要 composite 的 universal SAT acceptance 和 existential UNSAT rejection；不需要 D 分类 compiler image 外的 source instances。source-only promise-decider 若另有全局 promise correctness，则是更强应用。

v2/v3 的“decider implies NP⊆BPP”仍是较弱后果；random source reduction 与 deterministic hardness under P≠NP 的区分保留。该 seed certificate section 没有把它们改写成 P=NP，也没有把 BPP 作为最强结论。

真实缺口仍是：

- 没有实际 UM compiler；
- 没有把每个 low-load schedule 译成 source lists 的 all-output decoder；
- 没有 fixed-fee realization、selector/endpoint 连接或 source-to-UM reduction；
- 没有证明 uniform inverse-polynomial good-NO probability；
- 没有外部 PCP paper 重新核验；
- 没有一般 UM near-two hardness。

# 6. 有限接口核验的准确范围

来源中给出并运行一个标准库 Fraction 接口核验：

- 四种抽象 seed outputs FAIL/YES/NO/GRAY 的全部 4^4=256 个表；
- gray_rejects 两种行为，共 512 个 cases；
- 其中 32 个全 YES，350 个含 NO；
- 阈值索引 j=2,...,1000 共 999 次，核对 beta_j 差值、T=7/11、C=beta_j T 的严格边界。

代码无随机 seed 参数、无浮点算术，输出应为 512、32、350。它只核验抽象 verifier 的 universal YES/exists rejection 逻辑与有理阈值方向，不构造或执行真实 source、R、D、UM compiler、PCP reduction 或 decoder。普遍结论由正文 verifier proof 承担；这不是复杂度分离的实验性证明，也不能用有限核验替代 compiler/decoder 义务。

# 7. 与仓内对象去重和处置

现有 部分MinRep费用桥与pDM阈值双源审查 已登记相同 legacy identity UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1，并把 seed certificate、条件费用桥、pDM 整数阈值、以及“未完成 UM compiler”写入统一对象。本页不创建第二个 certificate theorem，而保存 c8b4a86 review 的最终后缀读取、概率措辞修正、expected-time 截断要求、v2/v3/v5 对照和 512-case 接口核验。

与 pDM 对象区分：pDM 只给 perfect matching iff OPT<=bd 和无匹配 OPT>=bd+1，不能提供乘性 gap。与部分 Min-Rep source 区分：source soundness/高围长/degree regularization 不等于真实 UM schedule decoder。与多状态估值 coNP 对象区分：后者的外部经典依赖是 Independent Set NP-completeness，和本 seed certificate 的复杂度条件桥不是同一 lemma。

处置为 integrated：原 review 已复制到 evidence；正文保留 seed certificate 的正确复杂度后果和所有未闭义务，不声称外部 PCP、UM compiler、source hardness 或一般 near-two 结果。

