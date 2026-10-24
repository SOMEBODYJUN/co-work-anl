# 任意人数与一般目录的本轮工作稿

2026-10-24。固定 [CAG-MODEL](../../../current/customer_attraction/model.md)。
Q-CAG-HALF 原始完整量词仍 OPEN。本文区分实际推导、重复来源与未付义务。

## 父方直接推导与去重

1. 对任意实际并集 U 与最优并集 C，令遗漏 L=|C\\U|、外部信用 E=|U\\C|，
   half 的准确需求是 L-E≤W。将遗漏半额或遗漏全额当作必要需求都会改变接口。
   重构时发现并修正了已有 route5a §4 的算术错误；
   [独立审查](parent/route5a_independent_review.md)给精确范围。
2. 尝试在根空背景直接证自由根 HALF / 理性 k 人对 OPT_(k+1) 的增槽比较。
   已定位到旧 [FREE-ROOT 原稿](../R-2d91ff13b4b44effbe7e78a60470bcc7/independent/root_only_independent_checkpoint.md)；
   同一空根紧族及增槽接口早已存在，不另认领。任意根计划的全部正深度理性
   不自动给根 IC，更不能直接调用原 half；本轮没有闭合此加强。
3. 考察把实际遗漏客户按最优主题指定唯一 owner，从共享遗漏降到私有席位。
   只在实际路径删兴趣不会改变实际收益，但会改变偏离枝后继的理性：
   其后继停止覆盖 owner 客户可能提高原偏离者收益。
   因而没有可用的“私有化保原 SPE”引理，没有将其作为归纳步骤。
4. 从完整终局的势差和随机优先份额展开全树比较。
   当前 IC 比较的是两份真实终局；删除当前槽后的背景也改变。
   删槽势差、旧玩家份额变化及中间后继背景漂移均不能丢弃。
   现有 [一般工作稿](../../../current/customer_attraction/general_half_proof.md)、
   [末位剥离](../R-059140e622784d85a4e3a4dd6554f506/menu_covariance/last_successor_peeling.md)
   已准确记录这些余项，本轮尚未给新的共同容量控制。

以上 2--4 是未闭合的探索和来源去重，不是证明或方法类不可能性结论。

检查实际受影响的本题 CLAIMS 时，又发现其 `CA-CROSS-BRANCH-RELAY-v1`
仍登记旧的错误非根式 ΔW≤ΔV，而源正文在前一轮早已修正。
此次仅同步滞后账本：保留原 v1 全量词并记 FALSE，单列既有含 ΔP 的 v2，
证据链接沿用前轮的三客户完整 SPE 反证和独立审查。
R-d64c8ab728b84b1aa054dd6d84ea3155/global_potential/relay_background_correction.md
也已指出同一滞后条目；本轮不认领首次发现该漏项。

## 仍需的新关系

应在同一完整策略的真实离轨 IC 中找到一份付款 P，同时证明
L-E≤P≤W，或绕开该付款表示直接证明 2W≥O。
逐节点、逐分支各有一份容量，不会自动得到全树的一份容量。
六名研究员的工作只按其实际推导登记；人数、有限阴性与正确恒等式不算闭合。
