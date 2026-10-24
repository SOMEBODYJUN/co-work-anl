# Round7/coupling：源时间、静态列容量与真 query 投影

一般 Q-CAG-HALF 仍 **OPEN**。只研究任意人数、一般有限共同目录、每份完整历史纯 SPE；未扩结构或固定规模。

- [fresh_source_order_and_suffix_hits.md](fresh_source_order_and_suffix_hits.md)：从 round5 因果区间与 round6 GLOBAL-HIT 推出的 fresh 源支持定理、逐源后缀 HIT、前缀 cut 和后缀角色价格包络。全范围解析推导，root 独立重构/对稿与 credible 盲重构/对稿通过；没有 actual-wallet cap 或福利付款，不主张新颖性。
- [fixed_parent_static_column_capacity.md](fixed_parent_static_column_capacity.md)：同一parent B、不同SD row/不同W_i的第一类正边联合列容量≤L*u_l(B;(C∩B_l)\S_l)。root独立重构与independent独立审查通过，精确密度另经global重构；不含直接项、第二类边或旧请求，不给actualcap。
- [joint_prefix_claim_transfer_blind_review.md](joint_prefix_claim_transfer_blind_review.md)：只读 credible 精确合同后的独立盲重构；同一孩子的全部 prefix利润请求联合送回同一个 parent B，输出每角色系数不超过输入L上限。确认解析容量；不允许多个孩子或已有suffix请求免费叠加。
- [static_denominator_and_query_projection_review.md](static_denominator_and_query_projection_review.md)：只读 global 精确合同后的独立重构：确认静态分母 SD 身份、两类边利润支配与直接 backward 域缺口；另给任意 synthetic 叶利润的守恒 QUERY-PROJECTION，送回真 natural current/future context。QUERY-PROJECTION经root独立重构；§6另独立核查root提出的“保留第一类正边”反向非负kernel。整体循环、方向与实际付款仍未闭。
- [audit_diagonal_full_menu.py](audit_diagonal_full_menu.py) 与 [diagonal_full_menu_audit.json](diagonal_full_menu_audit.json)：只检验一个明确的强全菜单耦合候选，六份旧完整策略的定义级 Fraction 回归；没有新游戏搜索。该候选及其 pair 加强实际已有旧反例，故有限 pass 不能用于支持普遍性，已经停止这条加强测试。

## 已停止的重复候选与准确来源

本轮最初提出任意 prefix/任意 p 的强式 D(p)>=p^T Kp，K为完整真实 forced 叶再加一个独立查询；并尝试 pair 加强 d(A)+d(B)>=K(A,B)+K(B,A)。六份旧证书全部history的测试没有发现负项，但读到旧资产后确认两者早已失败：

1. 另一工作区 R-d22a706a03c5499d941a6a97f94128a8/[两剩余完整推送正文](../../../R-d22a706a03c5499d941a6a97f94128a8/induction/two_player_full_terminal_pushforward.md) 记录既有34客户六主题加空主题的完整 SPE，p(X2)=1/10、p(empty)=9/10，有 D=29/30、C=41/40、D-C=-7/120。它不反驳更弱 C<=u。
2. 该来源 [full root menu 义务](../../../R-d22a706a03c5499d941a6a97f94128a8/induction/full_root_menu_mixed_obligations.md) 已记录348客户完整 SPE 的根 pair (2,5)：d2=d5=147/2，K25=K52=159/2，pair gap=-12。round7/security 在 [cross_pair_scope.md](../security/cross_pair_scope.md) 独立精确重放旧证书；本组不重复计新反例。
3. 任意背景的更弱 Mfull 也已被 round5 PB-extra 构造排除（见本轮 security 对精确量词的审查）；root-empty、自选混合与全路径共同支付须各自保持原量词，不能把上述辅助失败称为 half 反例。

这些都是旧失败桥的恢复，不算本轮正进展。该测试已停止。其后完成上列 fresh 源因果序、STATIC-COLUMN/ROW、QUERY-PROJECTION 及两项独立联合接口审查；它们各自的确切范围已接到相应一般推导，但仍没有已付的新增福利关系。
