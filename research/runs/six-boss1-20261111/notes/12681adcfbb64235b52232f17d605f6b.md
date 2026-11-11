# 可见真最大 C 联合 v4：精确界与整个最优面排除

Boss1；RUN six-boss1-20261111。Main 明确释放的唯一 1586 行 LP 已完成，实际优化调用 **1 次**；后续精确恢复、独立核验、全脸及真实源诊断均为 **0 新优化**。

\[
\boxed{W\ge\alpha_4\mathrm{OPT}_6,\qquad
\alpha_4=\frac{208101173892952666162424962783956947305005629564084333}
{471722007522064528882747177426615554317607603285651548}
\approx0.4411521416736506.}
\]

完整 **1586 raw／513 非负列／2 等式** 必要锥的原始与原尺度对偶准确匹配。相对上一个实际求解的 1003 行系统提高约 0.0008119780473412091；1050 中间输入未求解。完整保留所有零/重复原行、全 512 客户类型、独立 K、仿射 rhs 和两条自由等式付款。

## 精确最优面及真源排除

正付款共 11 条：46、47、134、218、221、222、868、1018、1433、1438、1439。后四条具有实际 source IC 权，数值除数仍为 25。

整个最优面保留 20 个零对偶余量列，正行加两等式的秩为 13，自由列为 0、11、15、19、23、51、75；全部 1586 原始不等式和坐标非负条件均保存。

两条正 C 预算使用同一个真实历史 (A1,C,R3,R4,R5,R6)，共同内部权为
\[
(\theta_3,\theta_4,\theta_5)
=(12425/31104,\ 175/432,\ 5/12),
\]
分别 s=0、s=9。全部端点弱零态先保留，再在同一历史取交；正中间大小帽迫使 R3、R4、R5 覆盖恰 C，交集源份额为 c/5。因此这三个真正内部源收益均为 K/5。

但它们的真实菜单 SAFE 在整个面上的差 K/5−N3、K/5−N4、K/5−N5 均为固定负数，近似为 −0.002172959、−0.013486980、−0.036115021。每项均有全 513 列精确有符号身份。**整个最优面都不可由原模型完整纯 SPE 实现。**

全部 256 个端点局部态、30 个端点零态及 13 个共同零态保留；另核 8192 个菜单差。s=9 的 p0c1/1110、s=0 的 p1c1/1111 和 c0o1 的三个单中间弱态均没有被预先删除。没有固定 C 734 绑定、phase I、未冻菜单行或新输入行。

## 交付

- [完整证明](visible_maximum_joint_v4_solve/proof.md)
- [完整精确证书](visible_maximum_joint_v4_solve/exact_certificate.json)
- [独立全域核验](visible_maximum_joint_v4_solve/independent_check_result.json)
- [完整最优面](visible_maximum_joint_v4_solve/optimal_face.json)
- [全列固定量身份](visible_maximum_joint_v4_solve/true_branch_face_functionals.json)
- [真实 C 分支排除](visible_maximum_joint_v4_solve/true_branch_equality_diagnostic.json)

初始等待骨架的摘要字节另存 scaffold_summary_before_release.md，原骨架 manifest 保留为历史记录；最终证书使用本目录最终 freeze_manifest.json 和 SHA256SUMS。

这确立必要锥的准确最优值及真实 SPE 不可等号达到性，没有给出统一更大的 epsilon，也没有证明原六人半覆盖；原题仍 **OPEN**。
