---
id: "customer-attraction/Ra0-background-near-saturation-audit-v2"
kind: "review"
type_tag: "审查"
title: "Ra0 背景近饱和审计 v2"
status: "finite-fraction-audit-reviewed"
truth_status: "finite-certificate-regression; no-universal-bound"
summary: "v2 JSON 汇总了 8 个指定完整纯 SPE 证书上的背景近饱和 BNS 行审计；使用主题特定 M_C 与 Fraction 全部算术，所有列出的最小 BNS 松弛均为 0，但这仍是有限回归而非一般上界。"
source_refs:
  - "clean:b91a4bf0212740cc694c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit_v2.json"
  - "local:archives/customer-attraction/tools/evidence/Ra0-json2-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-json2-agent/background_near_saturation_audit_v2.json"
  - "archives/customer-attraction/tools/evidence/Ra0-json2-agent/manifest.json"
---

主源是冻结的 v2 汇总 JSON，5,114 字节，SHA-256 为 `e165feee24cf6d7d0b567618042e878c2403d552bfc57a96f9082ee41e8881f1`。其范围字段明确限定为“指定有限完整 SPE 证书”，并写明“不能推断普遍界”；算术字段为 Fraction 全程。v2 的修改是把背景客户列中使用的最大负载常数改为主题特定的 `M_C`，并在独立审阅意见后做解析复核。

各案例的定义级历史和真实偏离计数如下；`minimum_BNS_slack=0` 在每个案例都出现，表示至少有饱和行，不表示存在负松弛或违反。

| case | players | topics | customers | histories | deviations | eligible histories | min BNS slack |
|---|---:|---:|---:|---:|---:|---:|---:|
| zero | 4 | 3 | 0 | 40 | 80 | 13 | 0 |
| common_duplicate | 4 | 3 | 5 | 40 | 80 | 13 | 0 |
| big_private_m5p7 | 5 | 7 | 11 | 2801 | 16806 | 400 | 0 |
| sparse_m3p4 | 3 | 4 | 14 | 21 | 63 | 5 | 0 |
| sparse_m4p5 | 4 | 5 | 25 | 156 | 624 | 31 | 0 |
| sparse_m5p7 | 5 | 7 | 136 | 2801 | 16806 | 400 | 0 |
| sparse_m6p4 | 6 | 4 | 15 | 1365 | 4095 | 341 | 0 |
| existing_nonpne_m5p7 | 5 | 7 | 1992009 | 2801 | 16806 | 400 | 0 |

小规模 `zero` 与 `common_duplicate` 案例保留空客户/重复主题边界；`big_private_m5p7`、`sparse_m5p7` 和 `existing_nonpne_m5p7` 展示较大客户数或稀疏支持；`sparse_m3p4`、`sparse_m4p5`、`sparse_m6p4` 保留不同人数/主题比。`minimum_case` 字段给出每个案例的具体最小行位置、背景计数和效用值，例如 `sparse_m4p5` 在历史 `(0,0)`、`C=1,D=1` 处的 `u=43/4`，而 `existing_nonpne_m5p7` 的最小行是 `(2,6)`、`C=D=0`、`u=620115/2`。

这份 JSON 是审计结果的有限汇总，不包含生成器或逐行证明正文；因此可复用内容是案例覆盖范围、计数和 Fraction 饱和结果。它不能单独证明任意客户目录、任意人数、所有离轨平局或 Q-CAG-HALF-6 的半覆盖目标。后续若要扩大结论，必须恢复对应 v2 程序、逐历史核对 BNS/AP 不等式，并区分固定证书回归、局部引理和跨历史付款桥。
