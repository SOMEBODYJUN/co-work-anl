---
id: "customer-attraction/Ra0-background-near-saturation-audit"
kind: "review"
type_tag: "审查"
title: "Ra0 背景近饱和有限审计"
status: "finite-fraction-audit-read"
truth_status: "finite-certificate-evidence; no-universal-lemma"
summary: "冻结 JSON 汇总了九个指定完整纯 SPE 证书上的 BNS 背景近饱和审计；全部记录使用 Fraction，最小松弛为 0，但文件明确不推出普遍界。"
source_refs:
  - "clean:cccee651921646bbb325:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit.json"
  - "clean:b2193e7b539b0b40ef69:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit.py"
  - "clean:b91a4bf0212740cc694c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit_v2.json"
  - "clean:cbd7d354e0b358cc2510:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit_v2.py"
  - "local:archives/customer-attraction/tools/evidence/Ra0-json1-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-json1-agent/background_near_saturation_audit.json"
  - "archives/customer-attraction/tools/evidence/Ra0-json1-agent/background_near_saturation_audit.py"
  - "archives/customer-attraction/tools/evidence/Ra0-json1-agent/background_near_saturation_audit_v2.json"
  - "archives/customer-attraction/tools/evidence/Ra0-json1-agent/background_near_saturation_audit_v2.py"
---

主源 JSON 大小 5,075 字节，明确声明审计范围是“指定有限完整纯 SPE 证书”，算术全用 `Fraction`，且 `lemma_status` 仍是 analytic candidate、independent review pending。它不是一个策略搜索器，也没有把抽样案例量词扩展到所有客户分布、所有人数或 Q-CAG-HALF-6。

九个记录覆盖 zero、common_duplicate、big_private_m5p7、sparse_m3p4、sparse_m4p5、sparse_m5p7、sparse_m6p4 和 existing_nonpne_m5p7。每条都报告完整历史/偏离核验数、eligible ordered histories、maximizer/arbitrary query pairs、saturated branches、非 Markov 计数类数量、minimum_BNS_slack 与最小案例。典型规模包括：m=5,p=7 的 big-private 记录核验 2,801 个历史和 16,806 个偏离；m=6,p=4 记录核验 1,365 个历史和 4,095 个偏离；最大 existing_nonpne 案例有 1,992,009 个客户单位。

所有记录的 `minimum_BNS_slack` 都是 0。该数值表示在给定证书与实现的有限算术检查中达到等号或边界，不能解释为普遍 BNS 引理已证明。主源 v1 的代码使用全局 `M=k+max(b)`，相关 v2 脚本把 `M` 改成按客户类型的 `M_C` 并把输出状态写成“analytical recheck”；这说明对象存在后续修正轨迹，不能把 v1 与 v2 的结论混写。

可复用的是有限审计的字段合同：先用 ExactSPESolver/StrategyCertificate 验证全部有序历史与偏离，再用 Fraction 逐项检查 BNS、arbitrary-topic 与 observed continuation 不等式，并保留最小松弛位置。当前材料只支持“这些指定证书通过了实现级检查”；普遍引理、主问题半覆盖和跨所有完整历史的定理仍需独立证明。
