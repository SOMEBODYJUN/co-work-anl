# R-171 packet13 有符号 delta 有限审计（2026-10-31）

原始冻结源：`27a2017f46e8f8aae51e`（packet13_source.json.gz，SHA256 `bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce`）、`36d750276233a1ce4ace`（packet13_all_nodes_audit.json.gz，SHA256 `621df08bbcbb01a57825743d876df3c4f2ae65a4abcef4fad18be59ea3cd3321`）和 `f9e5bf7a48f6e9bb0784`（probe_signed_delta.py，SHA256 `53c14148d65c4e7f35c44b77bdf6b9f6204f49507bf96c842a07f9a50e336252`）。同一 packet13 字节按脚本要求复制为 refined_tax_k10_packet.json.gz，并以哈希核对；不是另找替代凭据或另一个输入。

本次运行保留 `replay/probe_stdout.json`、`replay/signed_delta_report.json` 与 `replay/packet13_all_nodes_audit.json.gz`。它是固定完整有序历史纯 SPE 的有限精确审计，不是一般半覆盖证明。
