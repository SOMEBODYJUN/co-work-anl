# 本轮推理缺口与停界

## 遗漏半额推出 half 的算术跳步

尝试以合法付款 R≤W、R≥L/2 结算最优并集。
失效在把 I≤W 和 L≤2W 相加后错误写成 O≤2W；实际只有 O≤3W。
正确需求为 L-E=O-W，不能省外部覆盖信用 E。
这是推导错误；没有建立满足旧条件的 SPE 违反 half。
L1--L4 保留，源稿已修，见[审查](parent/route5a_independent_review.md)。

## 未建立的共享遗漏私有化

实际遗漏客户指定唯一最优 owner 后，实际路径收益不变，但偏离枝后继
可能停止覆盖该客户，抬高早期偏离者收益。尚无保持完整 SPE 的变换，
所以不能套用已有私有遗漏席位定理。这里只记录未成立义务，不称一般不可能。

## 已有来源，不再重认领

FREE-ROOT 与 k 人对 OPT_(k+1) 的增槽加强以及紧族，已有
R-2d91ff13b4b44effbe7e78a60470bcc7/independent/root_only_independent_checkpoint.md。
FTA、完整菜单及 PEEL 漂移都有既存正文。重构可以用于核对，不能算新承重关系。

## 最优前缀存在排列的收费上界

尝试逐步强制一个最优元组的前缀，每次收新强制玩家的真实最终利润 D。
希望选某个最优元组和排列使 D≤原W，再证明 D≥OPT/2。
前一桥已被旧22客户完整 SPE 否定：唯一最优支持的全部24排列 D 最小
193/12>W14。原每个前缀节点的 IC 仍成立，但它们左侧属于不同已强制前缀，
不能相加当作原根实际收益。精确账本代回只是恒等式，不会支付差额。
见 [正文](direct_exchange/optimal_prefix_bill_boundary.md)。停止这套两桥模板，
未判 BILL-LOW，未改变 FTA/自由菜单或原 half。

## Beta-clone 静态表示不保固定完整策略

静态互异 clone 份额 1/(b+k) 及覆盖 k/(b+k) 仍正确。
失败在当前复用早先 clone 时改变末位真实 BR：规定 fresh A_1、末B 当前24，
复用A_0后所有末BR只能freshC，当前25。因此重复孩子无法填可信威胁。
原 hA 仅保证合法离轨子SPE，不称实际根路径；静态表示、只保根终局和允许
重选fresh策略均未被否定。见 [自足见证](full_tree/beta_clone_fixed_strategy_lift_failure.md)
与 [审查范围](parent/beta_clone_review.md)。不继续同候选扫描。
