# 共享遗漏的联合后验席位谱及其一般障碍

范围固定为原 Q-CAG-HALF：任意共同目录、任意人数、全部有序历史纯 SPE。
本目录仅是本轮研究草稿；没有正式提升、外审或新颖性认证。

- [joint_omission_prefix_spectrum.md](joint_omission_prefix_spectrum.md)：任意人数的联合后验谱。用每个真实前缀固定的负载分母，把共享遗漏信用和私有席位放在同一份逐位置利润预算中；并给出与分数覆盖递推的合法组合。
- 同一正文给出完整图共享遗漏与互不相交银行的全人数解析族：所有联合谱行、所有比较集的分数覆盖前缀行均成立，但 m≥13 时该路径违反 half。正文明确证明该路径不是 SPE，因此它只否定这个一般条件接口的充分性。
- [audit_joint_omission_spectrum.py](audit_joint_omission_spectrum.py)：精确有限 SPE 回放及解析障碍的有理算术核验；默认只打印，不覆盖冻结记录。
- [joint_omission_spectrum_audit.json](joint_omission_spectrum_audit.json)：本轮实际运行输出，范围以文件内数字为准。

关键缺口：席位继承仅通过全局私有遗漏触发；共享遗漏对目前谱只提供逐主题的原始分母信用。完整图族展示这些行遗漏了真实末位的跨主题最优回复。一般 half 仍 OPEN，不建议继续仅调优这些有效行的非负组合。

已有边界：`R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md` 已否定存在最优并集使全部遗漏 D≤W；新预算不能把共享遗漏独立再交给 W 支付。
