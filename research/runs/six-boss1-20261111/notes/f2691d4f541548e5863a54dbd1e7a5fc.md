# 可见真最大 C 联合层 v2：精确求解及新整面排除

Boss1；RUN `six-boss1-20261111`。本轮唯一授权LP已完成；优化器调用 **1**，没有重试或附加求解。全部1003 raw行、513列、两等式完整保留。

## 精确新界

\[
\boxed{W\ge
\frac{112508769242601005698939086121271608650179}
{255504218184559114703526217520973415950853}\operatorname{OPT}_6
\approx0.44034016362630934\operatorname{OPT}_6.}
\]

它是该冻结全必要锥的精确最优值，比上一1002行锥提升约`5.795404848408691e-6`。匹配原始点含13个正客户型及K；完整1003原始余量、513对偶列余量、两自由等式、目标和互补性均通过独立Fraction核验。

正付款仍为12条；旧raw927 `P25(C,Omean)`退出，新raw1002 `SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE`进入，其他11条保留。新行付款按原300尺度恢复。

## 整个最优面不是真实SPE

完整零对偶余量列仍为21列，12条正行加两等式秩14；参数化保留全1003原始约束。整个面固定

\[
u_2-K/5=
\frac{2090367050511169183056222233334689252587}
{30660506182147093764423146102516809914102360}
\approx6.817783888148402\times10^{-5}>0.
\]

然而正NS5行在真实SPE取等时，其全部非负真预算及逐客户最小余项都取等。128态的全部11零态均使强制C源每客户收益等于c/5；额外`(p,c,o;r)=(0,0,1;0010)`弱态被保留，且同样贡献0。故分支v2=K/5；源IC等号又给actual u2=v2，与整面正差矛盾。

因此整个锥最优面不可由完整有序历史纯SPE实现。旧P25(C,Omean)在新面严格松弛，未误套旧等号论证；既知ROOT270加强项在新面两边均0，未额外分离。没有phase-I或新输入行。

此非达到论证尚未给出统一α+ε界；原六人half仍为 **OPEN**。

## 交付入口

- [完整证明](visible_maximum_joint_v2_solve/proof.md)
- [完整精确证书](visible_maximum_joint_v2_solve/exact_certificate.json)
- [独立完整核验](visible_maximum_joint_v2_solve/independent_check_result.json)
- [全最优面](visible_maximum_joint_v2_solve/optimal_face.json)
- [NS5全部零态与真实源诊断](visible_maximum_joint_v2_solve/true_branch_equality_diagnostic.json)
- [正付款变化](visible_maximum_joint_v2_solve/positive_payment_changes.json)
- [最终冻结manifest](visible_maximum_joint_v2_solve/freeze_manifest.json)

输入SHA `0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4`；精确证书SHA `b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea`。所有写入仅本新目录与本页，旧包保持字节原样。
