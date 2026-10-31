# 稀疏部分投影解码候选：精确加强与实际审查范围

实际最终全文对象为 `research/questions/unrelated_machines/sparse_partial_projection_coupling_decoder_obligation.md`，SHA256 `76e556601c33508dd9574832b6c81e85ea27cde2affd33e27fe53cea5a341b33`，研究问题版本 q2。它仍是开放调度归约接口，不进入已完成 canonical Claim 或证明图。

实际审查顺序如下：

- root 先给部分投影次耦合的精确陈述和 β²/L 推导；`shared_label_attack` 收到该证明后逐式核验，不冒充这一步盲审。
- `cover_consistency` 只收到精确陈述，未读新正文或别人证明，独立加强到 β/L，并给两阶段确定化和 subset-shift 的精确锐族。独立稿 SHA `b8941c1cd14317cf23297f725c9d92173d9156f6f3fe3f3aac7003dc2d7665f8`。root 独立重构：右端在其共同支撑 S_v 均匀，左投影落入该支撑的概率≥τ_e；先 left argmax，再 right 最佳响应，得到 Σwτ/|S_v|≥β/L。
- q2 因结论/开放转移条件改变而显式改版本。两审查者实际读取最终全文，最终 hash 均如上。cover 还将三处锐性措辞逆替换，精确恢复原 q2 稿 `218d8b27ece032038624a8ed605e9730d8e6ade6735e77206f3b252c3eb521d6`，确认其他内容未变。

最终没有尚成立 fatal objection。具体核过：非负权和1、共同 vertex 概率、ξ 投影支持及两边逐点 domination、τ0/β0、非空支撑、明确确定算法与总位长；q-shift 的真实单标签最优值 1/R，subset-shift 的 τ=L/R、β/L=1/R；源 NO 非空时 γ≥1/R，必须严格 β/L>γ，不能只说“γ取小”而固定 R/L/β。参数化锐性准确限于全部整数 R≥L≥1、β=L/R，未声称每个任意实参数组合均被该单族达到。

该证明无需新枚举或通用 LP，也未导入任何未核源困难性定理。标准概率/支撑解码工具不认证为原创；独立加强只改变有给定证书的 decoder，不产生一个调度 gadget。

仍开放且阻止升级的承重义务：从同一真实 UM 输入的**任意** C≤(2−δ)T 调度，在位多项式时间产生统一 μ、正确部分投影 ξ、足够稀疏 L 和覆盖 β，达到 β/L>γ，并同时维持源 YES 的完整实际 T 调度。任何一个只保 token 总数、逐边各自挑分布或使用 L=alphabet 的方案都没有关闭它。外审、新颖性及一般正反面目标均未认证。

Related Files：[候选全文](../../questions/unrelated_machines/sparse_partial_projection_coupling_decoder_obligation.md)、[已完成但范围不同的完整树边界](../../current/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing.md)。本页只记录上述候选的实际数学审查，未声称审查不存在的调度实现。
