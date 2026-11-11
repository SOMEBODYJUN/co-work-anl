# 可见真最大 C 联合层：唯一求解、精确最优与全等号面排除

Boss1；RUN `six-boss1-20261111`。Main 的一次明确释放已完成：全部1002 raw 行、513非负列、两等式原样进入数值模型，随后精确恢复和独立 Fraction 复核全部通过。优化器总调用 **1**，没有重试。

## 新的普遍界与必要锥最优值

\[
\boxed{
W\ge\frac{4757095109515738566700794768667543071677}
{10803370013405844497554807694481975324637}\,\mathrm{OPT}_6
\approx0.44033436822146094\,\mathrm{OPT}_6.
}
\]

比 Main ROOT270 原构造界提高约0.00007242594168749014。精确原始点含15个正客户型及K；对偶含12个正 raw 行和两个自由等式付款。所有1002原始余量、513对偶列余量、两等式、目标和互补性逐项精确通过。

唯一新增正 C 查询为 raw927 `PORTFOLIO25_i2_TC_QOmean`。以目标公分母 D 表示，它的原尺度付款为 `4003977123299586559012577657310326472/D`；C大小等式付款为 `28695169383647037006256806544057339716/D`。正行全部rhs0，其余仿射上帽仍完整核验。

## 全最优面与真实策略边界

21个零对偶余量列上，12条正行与两等式的秩是14。完整面以自由坐标 `(z0,z11,z15,z19,z23,z51,z75)` 参数化，并保留全部非负及1002原始约束。旧八位投影和 K 固定；六个非全零自由参数只分配 C 共会员。

互补性强制 A1⊆C、A1∩X=∅。若完整 SPE 达到该锥最优值，新正 P25(C,Omean) 取等将迫使真分支(A1,C,B3,B4,B5,B6)中的 B3、B4、B5 覆盖恰C。p=a1=1时末位B6可以覆盖或省略该C客户，弱平局完整保留。

源IC等号令第三真节点当前收益等于 original u2；其改选合法X的安全收益要求

\[
u_2\ge |X|/4-|X\cap C|/20
\ge |X|/4-(K-|A_1|)/20.
\]

但整个面上右侧减u2准确为

\[
\frac{73001712264841918690793563657687463721}
{108033700134058444975548076944819753246370}
\approx0.0006757309263151635>0.
\]

故该**整个必要锥最优面不可由完整有序历史纯SPE实现**。这尚不产生统一更大ε界；六人 half 与完整SPE反例仍为 **OPEN**。

## 入口与绑定

- [完整证明](visible_maximum_joint_solve/proof.md)
- [完整精确证书](visible_maximum_joint_solve/exact_certificate.json)
- [全最优面](visible_maximum_joint_solve/optimal_face.json)
- [真实分支等号诊断](visible_maximum_joint_solve/true_branch_equality_diagnostic.json)
- [独立检查结果](visible_maximum_joint_solve/independent_check_result.json)
- [冻结 manifest](visible_maximum_joint_solve/freeze_manifest.json)

冻结输入 SHA `b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33`；精确证书 SHA `8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347`。所有写入仅在本新目录及本页，旧资产保持原样。
