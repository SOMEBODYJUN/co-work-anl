# 多见证共享收费 v2 的作者全文读后核验

实际顺序：先仅读 v1 Exact，独立冻结 `multiwitness_fee_exact_first_review.md`（SHA256 `182c1c6318b24f2cd88247cfff50c9d8465946de41e4ffbea2714429d52b35b1`），并完成独立 Fraction 全原分配枚举；之后收到 v2 通知，才实际全文读取以下两件原文：

- v2 Exact：`global_decoder/multiwitness_shared_job_fee_exact_v2.md`，SHA256 `b3b3f2d98a6b81d5ee525bcdfa0fb26d1021994db58419f11f4862b321e6a607`。
- 作者 Proof：`global_decoder/multiwitness_shared_job_fee_proof.md`，SHA256 `0a7cf2b347cb8cf1627faafd0ac8da03ad565905c58d07c486e5b868a6ff56be`。

已读完 v2 Exact 的完整矩阵、7项结论及范围段，也已读完作者 Proof 全部6节；未仅阅读摘要或别人的概述。

v2明确把第7项限制为非空K，并保留v1空集0<0异议。作者Proof第5节对空K另列strict1可行、fee0，指出真空前件不能给严格和式；修复有效。原v1原件与原独立审查不改。

作者第1节逐机sigma0/sigma_r、OPT>=1的容量反证；第2节两份完整实际上界与C<2的x_K强制；第3节闭阈值等号；第4节多见证但无全开见证；第5节容量s与异权收费和式；第6节总位复杂度及旧星合同区别，均与此前独立重构一致。没有发现额外 standing fatal。作者未把同一f的owner费误记为所有参数下的新增unit费，也未把这个OPT1族冒称OPT gap或源归约。

独立精确有限核验：`multiwitness_fee_fraction_audit.json` SHA256 `d76e97007447f87c3c1c4d7d5d7ec520a8a3bbb1f85dd63f71761597f61f9afc`；359参数组、135712完整原分配、4660子集OPT、23908闭阈值fee比较。有限测试只支持实现与边界检查，普遍证明在独立review与作者Proof；此审查不认证全球新颖性、外审或UM反面。

准确评价：v2所述受限合同证明完整、独立Exact-first重构及作者实际全文读后核验通过；仅需保持“多个互斥strict singleton见证不能替代共同全开strict见证”的范围。源标签复制、全局decoder、费用跨测试不重复的预算仍未解决。
