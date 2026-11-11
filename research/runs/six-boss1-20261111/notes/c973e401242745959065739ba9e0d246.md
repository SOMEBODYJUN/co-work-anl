# Universal wallet v2：精确219行结论与独立分支诊断

Boss1；RUN `six-boss1-20261111`。状态：**Main明确释放后仅一次257列LP；精确匹配原对偶及独立源系数检查完成；停止扩跑。** 两旧包与摘要共30文件保持原哈希。

## 全域下界及指定系统最优

完整保留旧217行与全部256个实际/X/O客户型、真实K，仅加入Main根分支NEW和已释放的同一X真实第四源两尾cut。得到219原始行、207去重行、257非负变量。

精确最优为

\[
\boxed{\alpha_2=\frac{22634634904624698063}{52739368771603064323}
=0.4291791015294076\ldots.}
\]

10个正预算与全部257列非负余项严格证明原完整模型的 \(W\ge\alpha_2\operatorname{OPT}_6\)。10个正原子加K给匹配精确可行点，故本219行系统最优值就是α2，仍低于half。没有固定16-hist限制，不删o=0客户；不认领优于已有最佳全域界。

10正付款为SAFE3(A5)、SAFE6(Omean)、UP2、UP3、MX(Omean)、RC(Omean,Omean)、RIG(A4,A6)、RIG(A6,A4)、ROOT_BRANCH_NEW、TRUE_X_TAIL_CUT。两新行都紧且有正权；tail cut的K系数准确为+71，16个负m值原样保留。

输入SHA `bb7c66e141b9ab6080c5fbafe6c00f966a95247269ff54d2ae3abae7809f35f2`；精确证书SHA `12d4f059b7be021c8b3c89ed6adf3bde208750da6ce0eee79c383a813d50b36b`。[完整证明、整数付款与10原子表](universal_union_wallet_v2/proof.md)。

## 当前点已暴露的新缺陷，未改219行

匹配点有新根行L=0而旧根行H>0。对同一真实root-C分支独立核128型，得到

\[
\tau+\frac5{12}(p-y_5)\le\frac{65}{84}\rho.
\]

按完整非负钱包合账，另证

\[
13L-504H=67140u_1-9878K-627|O|\ge0.
\]

该行在新点的slack为 \(-2694628988940630887460/52739368771603064323<0\)，所以该点不能为原模型SPE。它作为[独立诊断附录](universal_union_wallet_v2/root_refinement_diagnostic.md)保存，**没有加入219行、没有重优化、没有宣称整个v2最优面排除**。新普遍行由实际非负付款证明，不能仅从L、H分别有效推出其差有效。

## 精确复核

[独立checker](universal_union_wallet_v2/check_certificate.py)不导入builder或优化器，重建219×257=56283源系数、核ROOT_NEW128型和tail1024尾态、全219原行、257对偶列；另核附录128型与单点排除。[结果](universal_union_wallet_v2/checker_output.json)全部PASS。

```sh
python research/workspaces/six-boss1-20261111/universal_union_wallet_v2/check_certificate.py
```

本轮提高了指定路线中Main先前已证的0.42608659882235334严格下界，但未证明half，也没有完整SPE反例。下一步真实根分支更细合账由Main接续。
