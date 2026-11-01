---
id: "customer-attraction/Ra0-fixed-support-background-rows"
kind: "review"
type_tag: "审查"
title: "Ra0 固定支持背景行记录"
status: "finite-exact-primal-on-written-rows"
truth_status: "finite-template-obstruction; not-SPE-witness; not-universal"
summary: "冻结 JSON 在 64 个原子支持上，将 437 条旧行与 1430 条写明的背景行合并，给出一个精确验证的有限 primal 值约 2.0391979934；该记录明确不是游戏 SPE 见证、普遍上界或全域对偶证书。"
source_refs:
  - "clean:24e8313ac2c86cbfbbfd:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_rows_fixed_support.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_rows_fixed_support.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_rows_fixed_support.json"
  - "local:archives/customer-attraction/tools/evidence/Ra0-rows-agent/manifest.json"
  - "local:archives/customer-attraction/tools/evidence/Ra0-rows-agent/summary.md"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-rows-agent/background_rows_fixed_support.json"
  - "archives/customer-attraction/tools/evidence/Ra0-rows-agent/manifest.json"
  - "archives/customer-attraction/tools/evidence/Ra0-rows-agent/summary.md"
related_objects:
  - "../资源/背景BNS与AP的版本身份及固定支持有限声明--资源.md"
  - "../审查/背景近饱和交换的局部常数与独立核对--审查.md"
---

## 记录身份与有限域

冻结源 `24e8313ac2c86cbfbbfd` 是 4,172 字节 JSON，SHA-256 为 `f6ce45f008f88f25438bd2e05e7e71a1cb920b5fc99ad1d5d048b95f594571cc`。它明确把问题限定在“437 条旧行加上冻结 64 原子支持上写明的背景行”，而不是所有客户质量、所有背景或完整策略树。现有资源对象已把它归为 `B10-AP-FIXED-SUPPORT` 一类模板诊断；本页保留该来源的实际字段和边界。

## 数值与核验事实

JSON 报告旧行数为 437、新写背景行数为 1,430，合计是该有限行系统的约束域。浮点目标值为 `2.0391979934373885`；对应精确 primal 值为

`301904989188813053163805000409977755377 / 148050846538890923800466562791232658950`.

`exact_primal_verified=true` 表示这个精确点通过了该有限行系统的验证。旧候选点在新增背景行中不再可行：`old_point_min_background_slack` 为负数，最违反行标记为 `S3_indexed_background:C6:D7`。这两个字段只描述旧点与新行的关系，不能把新 primal 的大于 2 数值解释成更强的模型定理。

## 必须保留的否定边界

同一 JSON 明确给出：

- `game_SPE_witness=false`：没有完整有序历史纯 SPE 见证；
- `universal_bound=false`：没有对全域背景或任意输入的普遍上界结论；
- `full_domain_dual_certificate=false`：没有全域对偶证书。

因此，这个对象可以作为“固定支持、固定写行的有限模板仍允许一个精确值约 2.0392”的障碍记录，说明仅靠这些行不能推出所需的 `2W≥O` 型不等式。它不能被写成全模型反例、可实现 SPE 证书、全客户质量可行点或六人半覆盖结论。

## 与既有对象的衔接

[背景 BNS/AP 版本资源](../资源/背景BNS与AP的版本身份及固定支持有限声明--资源.md) 已区分 fixed-support v1/v2、actual-only 与 full-v1/v2，并明确“不由比值大于 2 认证可行”。本 JSON 对应其中 full-v1 风格的 437+1430 写行记录；本页不把同目录的 v2、actual-only 或其他 `background_rows_fixed_support_*` 版本静默合并。现有 [背景近饱和交换的局部常数与独立核对](背景近饱和交换的局部常数与独立核对--审查.md) 讨论的是一般 BNS/AP 逐客户分母推导，不能替代本有限行的输入合同。

后续若要升级，至少需要公开 64 支持与 1,430 行的生成规则、逐行 slack、全质量域的对偶或分离证书，并给出从质量点到完整 SPE 的策略与离轨续局。当前来源只支持有限模板障碍和旧点失效诊断。
