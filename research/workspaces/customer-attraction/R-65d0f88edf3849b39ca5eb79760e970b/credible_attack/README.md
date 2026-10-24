# 可信修复与一般根缺陷攻击

2026-10-24。只研究 Q-CAG-HALF 的一般共同目录、任意人数、全历史纯 SPE。
主命题仍 OPEN；本区没有目标反例或新的一般福利证明。父方：R-65d0f88edf3849b39ca5eb79760e970b。

## 已读来源

- 根 `AGENTS.md`；`research/current/customer_attraction/model.md`。
- `research/current/customer_attraction/general_half_proof.md`、本题 RESEARCH_STATE。
- `R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_repair.md` 与 `effective_margin_frontier.md`。
- 父方提示 FREE-ROOT / augmentation 及其 tight 族已有 `R-2d91ff13b4b44effbe7e78a60470bcc7/independent/root_only_independent_checkpoint.md` §3 来源，不认领为本轮新增。

## 当前工作

1. `root_regret/`：子研究员研究一般任意根、正深度全 SPE 的增强候选；收到已有来源后停止同模板扩样。
2. 我研究一般双 SPE 保险界 `2W_H-OPT_m >= 3(h-ell)` 的攻击。H、L 都为同实例完整 SPE，h、ell 是各自首人收益；L 全部根偏离收益均不超过 ell，因此 h-ell 确为可用保险幅度下界。这个候选比原 half 强；任何失败只属于保险接口。
3. `insurance_pair_attack.py` 把既存完整 H,L 的所有有序历史 IC 一起放入同客户类型锥，攻击上述一般候选。只对 root_tax_failure、eight_cce_welfare_gap 这两个已有实例导出的固定策略对作定向测试，未找到正目标。输出 json 是数值 LP 与有理原始点重算；没有对偶证书，不能当严谨最优值证明，更不能外推为一般界。

当前没有新的一般承重关系。尝试将根保险推迟到任意节点时，前缀玩家也能选择保险主题，不能免费保持其 IC；独立新增银行又会成为后继偏离选项。尚无全深度零交叉激励的修复。
