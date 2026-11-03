---
id: unrelated-machines/single-home-cascade-original-program-review
kind: computation
type_tag: 计算
title: 单home级联原程序与分层审查证据
status: frozen-success-reused-and-certificates-rechecked
summary: 保留规范构造器、原审查及原14机14任务8模式成功输出；本轮只独立回算旧证书，不重复运行成功构造器。
fixture_source_sha256: cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573
source_ids:
  - 978ef2be866136ae323d
  - ba9c71e2bc6052c4f3c0
  - a6f3780bd6fb78eeece6
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/single_home_cascade_query_separation.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/single_home_cascade_query_separation.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/single_home_cascade_query_separation_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/home_cascade_query_patterns.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/single_home_cascade_query_patterns_v2.json
---

# 数学接口与实现身份

数学对象是[单home级联完整查询族](../定理/单home级联的完整查询族与可加费用--定理.md)，不是一般UM求解器。输入同一原矩阵的两份完整strict1调度，初态全部 \(J\) 留唯一正小端home，第二态将非空query集全部送unit。构造输出不交非query支持；给显式 \(S\subseteq Q\) 后输出完整原分配，峰至多 \(1+\delta(S)\)，费用恰为所选query支持费之和。证明适用所有合格输入/子集；本页程序证据只适用一个冻结有理实例的显式请求。

本批 Boss5 重新实读输入夹具 `examples/unrelated_machines/home_cascade_query_patterns.json`（SHA-256 `cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573`），其独有内容是 14 机/13 home job/3 query 的严格输入字段、unit 迁移链、无根环、零端和八模式审计参数；它与已有证据包中的同字节副本一致，不构成新运行。

原程序完整16781字节，SHA256为 `c52eb5be01a64e7d13f1e80a7ad1cb5711ed187f0a8ad1000269847d004d59cd`。原review完整3035字节，SHA256为 `3f92aec8afd506dd6ed879311cbb4b48e6482f8e1bd0e4673a62f8b6798bc934`。两份冻结提交各绑定同一字节版本，不计为两个程序或两次实验。原字节连同fixture、run和六份历史证明/审查均保留在[证据包](../../tools/evidence/single-home-cascade-originals/README.md)。

程序的各层职责如下。

| 层 | 实际执行与精确范围 |
|---|---|
| `frac`、初始化 | 输入时间/权重仅接受字符串或整数，拒绝浮点与bool；用Fraction。核机器/任务标签、有限端、非负时间，\(U\) 全unit，\(J\) 唯一严格正小端且其它端仅0/1。 |
| `check_schedule` | 逐原任务核合法端与恰一次分配，重算全部原机器的负载、每机任务清单和峰；先核两strict输入、强home和query出口。 |
| `_construct_paths` | 从 \(M_0\) 的原unit owner向后追 \(M_1\) 边，逐 \(D\) 存储不交增广路及单射终点；显式检查 \(M_0\) 避home以及被占home的全部正任务属于 \(D\cup Z\)。 |
| `_construct_closures` | 以终点home定义children，切断指向query的边，求固定 \(B_q,A_q\)，核互斥、费用和界以及fixture给出的手工支持/丢弃集/终点。 |
| `construct` | 只处理一个传入列表，拒绝重复或非query；按所选闭包翻转 \(U\) 路径，\(Z\) 固定零端，其余 \(J\) 回home；重新从原矩阵算完整负载、实际unit集合、费用和余量界，空/全子集另核strict1。 |
| `main` | `--subset` 可重复，每项为显式JSON列表；若给定则覆盖fixture的 `audit_patterns`。否则逐个读该列表，缺省只构造全query。输出写代码/输入SHA、Python版本和实际命令；`open("x")`拒绝覆盖旧文件。 |

程序没有自行生成 \(2^{|Q|}\) 查询模式，也没有枚举全部原调度或计算OPT。它输出的是完整分配和逐机审计表，未显式输出各任务开始时刻；普通UM中按机串行即可恢复完整时间表。其分配不是匿名token、复制任务或只算被触发home的局部见证。

# 原成功记录与本轮复核

旧冻结run `single_home_cascade_query_patterns_v2.json` 共32918字节，SHA256为 `846ec8efc0e0b3ea2f92e71a548ea4b62aaef60f40c2d74ed2ef8cd001dcf286`。它记录Python3.12.14、`all_checks_passed=true`、原程序SHA及fixture SHA `cfb25856400d6d0ee6b6cea9cb100d8545c97fe2025643f8a62260763fc69573`，与本轮读到的原字节一致。故复用这次真实成功记录，没有重跑原构造器或伪造新退出码。

本轮新增的[独立旧证书回算器](../../tools/evidence/single-home-cascade-originals/verify_frozen_record.py)不导入/执行原构造器，不寻找闭包或新调度。它读取原fixture及run，核四个源文件SHA绑定，从原处理矩阵独立重算两输入见证和8份旧输出，逐份验证所有原任务的实际端、全部机器负载及每机任务身份；又核stored增广路径的原端与顶点不交、实际query模式、home/zero合同、原 \(U\) 端、费用、\(\delta(S)\)、人工期望及空/全strict。

[实际复核结果](../../tools/evidence/single-home-cascade-originals/frozen-record-verification.json)为exit0、`all_checks_passed=true`，共10份完整分配、140次原任务归属、140次逐机负载以及140个每机任务表条目。该程序检查的仍是旧证书；它既不是第二次原构造run，也不是一般定理/OPT/全部可行调度的验证。该三queryfixture显式列全8个子集，不能由此把任意query数的一般量词降成实验枚举。

## 有限实例的全部模式

机器和任务各14个，\(U=\{U\}\)，query为 \(q_1,q_2,q_3\)，其中 \(q_2,q_3\) 共home \(H2\)，小时间为 \(1/8,1/16\)。\(q_1\) 在 \(H1\) 时间 \(1/8\)。\(Z=\{z\}\)；所有输出将原 \(z\) 从 \(A\) 的 \(1/5\) 送到 \(Z0\) 的原零端。非query原支持为
\[
A_{q_1}=\{f_1,f_2,f_3,f_5,f_6\},\quad
A_{q_2}=\{f_4\},\quad A_{q_3}=\{g\}.
\]
相应费用 \((c_{q_1},c_{q_2},c_{q_3})=(34,7,17)\)。原 \(r_0,r_1\) 是无根费用环，不进入任何query闭包，费用 \(19+23=42\) 不采用。因此全query构造费58，而输入 \(\sigma_1\) 非query unit费100。\(f_5\) 的路径经 \(W0\) 的原 \(U\) 迁移到 \(W1\)，终点为 \(W1\)，继而触发 \(f_6\)；这实际检查了unit迁移压缩而不只是直接home→unit边。

| 显式 \(S\) | 实际峰 | \(\delta(S)\) | 实际非query费 |
|---|---:|---:|---:|
| 空 | 1 | 3/16 | 0 |
| \(q_1\) | 19/16 | 3/16 | 34 |
| \(q_2\) | 9/8 | 1/8 | 7 |
| \(q_3\) | 1 | 1/8 | 17 |
| \(q_1,q_2\) | 17/16 | 1/16 | 41 |
| \(q_1,q_3\) | 9/8 | 1/8 | 51 |
| \(q_2,q_3\) | 9/8 | 1/8 | 24 |
| 全部 | 1 | 0 | 58 |

原review还报告独立调用显式 `--subset ["q1","q3"]` 的峰9/8；本证据包直接可核的是8模式冻结输出中同一子集的完整证书。没有另找到该CLI调用的独立冻结输出，不将review的这一叙述另算一份本轮run。

# 原审查的分层身份

六份冻结历史文档已经全文对读，不能用较晚成功记录重写较早时点。

| 文档阶段 | 真实内容与状态 |
|---|---|
| v1 Exact、v1 Proof | 原量词为每个单query，统一界 \(1+\delta\)；作者增广路构造已能支持后续加强，但旧陈述不追溯改成v2。 |
| v2 Exact、v2作者Proof | root提出同一组不交支持同时用于任意 \(S\) 和精确余量 \(\delta(S)\)，作者给完整增广路证明；构造保留原任务身份。 |
| v2独立review | 记录先据父任务的精确加强描述独立重构机器图，再读冻结Exact核SHA，再首次读v2作者Proof；未读v1作者证明。随后逐条攻击增广路、home交叉、无根圈、零端及所有子集。其独立性属于这个历史顺序。 |
| v2最终组合review | 精确绑定canonical SHA `679f77588505455e5810e2c8e6e147274d0cddef6eff05bb383fce67945d49d1`；数学通过，完整调度时刻属可明确化建议，代码/fixture/run当时pending。 |
| 当前认领的root review | 日期2026-10-18，boss11/root负责最终核对与Git，内部agents无独立Work身份；另记后续root实际审代码并运行一次8模式完整Fraction实例。无standing fatal，外审/新颖性未认证。 |

本轮是先读原程序/review后读取canonical及冻结证明/审查的语义清洗，未进行新的blind或Exact-first独立审查。新验证器仅在旧实际调度证书的算术和任务身份检查层面独立。

# 与全仓相关对象的实际比较

已有[共居SAT与单home双源审查](../审查/共居查询SAT与单home级联查询分离双源审查--审查.md)保存canonical的一般量词与 \(1+\delta(S)\) 论证，[单端口与单home双源审查](../审查/单端口向下闭集与单home级联双源审查--审查.md)保存旧run的有限范围。本批独有增量是完整规范程序的输入/输出/路径/CLI合同，六份历史记录的阶段区分，以及绑定原字节的独立旧证书回算；不把旧正文或旧run重复计成新结果。

已实际对读一般 `two_witness_query_separation.md` 的v2主陈述、阈值染色与3/2锐例：它不需要强home或唯一正小端，但同一组不交支持只保证各单query的 \(\max(3/2,1+\delta_q)\) 界。本对象更强的全子集族依赖严格normal form；锐例的 \(x_1,x_2\) 初态已从共同home导出，正好不满足强home。相关已清洗入口为[双见证审查](../审查/对称重置与双见证查询双源审查--审查.md)。

对 `home_unit_cycle_elimination_and_directed_token_bridge.md` 的比较仅用于区分输入合同：其单实际调度的去环/根可达规范化不提供本对象的第二strict见证、完整query立方体或费用可加性。共同使用单位入度机制不构成量词互换。六人共同目录SPE属于另一模型，不在该矩阵、证据与推论的范围。

后续可直接复用本页代码及支持合同，但任何扩大到多正小端、预先导出、其它费、弱模式或源解码都须重新证明承重条件。一般UM主目标保持开放。
