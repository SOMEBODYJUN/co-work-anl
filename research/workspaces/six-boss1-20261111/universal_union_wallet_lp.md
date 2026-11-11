# 全客户型 union / actual-wallet 路线：精确完成

Boss1；RUN `six-boss1-20261111`。本路线没有 16-hist 支持限制；保留全部 \((a_1,\ldots,a_6,x,o)\in\{0,1\}^8\) 的 256 客户型，另有全目录真实最大大小 K。状态：**完成一次 LP、精确原对偶和独立公式审计；不再扩跑本路线。**

## 结论

设

\[
\alpha=\frac{243427385229576983115}{571565195660569935844}
=0.4258960956295508\ldots.
\]

1. 13 个普遍有效预算的非负组合与全部257列非负余项，严格证明原完整模型的 **\(W\ge\alpha\operatorname{OPT}_6\)**。OPT6=0 单列；不删最优并外客户，不限制目录标签别名，不选择有利完整策略。是否优于旧最佳下界未在本路线认领。
2. 同时给出13原子加K的精确非负有理数点，满足全部217原始不等式、归一化与变量非负，且 \(W=\alpha<1/2\)。因此本次指定必要系统的精确最优值为 α，不能证明 half。**该点不是 SPE 反例。**

## 系统与付款

系统含所有六实际源 SAFE；UP 系数31/25/19/10；共同 \(F_X\) 最大性与 actual5 MX；actual RC 和 PAIR 对全部 A1–A6、X、Omean 无序可重复查询对；全部七个 six-of-seven OPT 帽；真实 K 大小界和六源 K/6 地板。Omean/Omean 使用全部36真实查询配对，不使用对角平均或伪独立交叠。

Main 在唯一 LP 前指定追加已证 ROOT_NEAR 和56条保留 K 的 ROOT_RIG，均先实读 owner 完整证明。最终217原行，仅去一个零行与11个完全重复行，剩205行、1等式、257非负变量。没有再次优化或读取旧点。

精确正对偶付款为：SAFE2(A5)、SAFE2(A6)、SAFE6(Omean)、UP2、UP3、UP4、MX(Omean)、RC(Omean,Omean)、ROOT_NEAR、RIG(A4,A5)、RIG(A4,X)、RIG(A5,A6)、RIG(A6,A5)。其余行仍在完整可行性检查中保留。

证书直接给全局恒等式 \(DW-N|O|=\sum_{13}L_RR+\sum_{256}h_vz_v\)，所有整数权 \(L_R>0\)、所有 \(h_v\ge0\)、K列系数恰为零。239个客户列严格正，17个为零；逐列证据全存。

## 可读证明与复核

[完整证明、13项整数权、精确13原子表和后续缺口](universal_union_wallet_lp/proof.md)给出全部数学责任与解释；[独立checker结果](universal_union_wallet_lp/checker_output.json)确认55769个语义系数等式、全部217行和257对偶列通过精确审计。

直接复核：

```sh
python research/workspaces/six-boss1-20261111/universal_union_wallet_lp/check_certificate.py
```

该checker不导入优化器。精确证书在 [exact_certificate.json](universal_union_wallet_lp/exact_certificate.json)，全输入在 [exact_input.json](universal_union_wallet_lp/exact_input.json)。

极值点把0.574103904370的最优并质量留在实际动作与X外；X全部位于P=0且仅和A5或A6相交。真正缺口是各真改分支共享后继的联合信息、K最大标签会员、六最优标签与真实回复的细分耦合。当前PAIR钱包由RC加实际末位对X的BR及逐客户非负项控制，不能把继续列相同PAIR视为新锥信息。下一步接口由 Main 选择，本目录到此冻结数学结论。
