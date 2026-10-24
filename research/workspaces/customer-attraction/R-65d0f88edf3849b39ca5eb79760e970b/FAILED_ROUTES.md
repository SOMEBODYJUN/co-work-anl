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
