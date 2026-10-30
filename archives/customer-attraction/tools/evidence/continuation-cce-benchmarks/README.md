# 静态CCE基准、同策略缩小和原程序重放

[数学对象](../../../state/计算/静态CCE原始对偶基准与缩小记录--计算.md)完整给五基准、70/13客户输入、静态原始/对偶、完整策略及另一个十三客户达到分布。

`source-manifest.json` 列13个冻结原件及完整commit、源路径、SHA-256；其中六个是本批主源，四份规范包、两个起始输入和初次JSON仅为运行/比较依赖，不被本批再次完成。`source/` 保持原始相对目录，使两个原程序无需改字节即可运行。`comparison/` 存放前批已认证的初次JSON。

`probe-replay.json` 和 `cone-replay.json` 是两原程序本轮完整输出，分别与冻结五基准和初次交替结果完整JSON结构相同。原程序需要NumPy和SciPy；实际版本保存在 `replay-environment.json`。它们是浮点发现加有理证书程序，原始数值状态不替代证书。

从仓库根重放原程序：

```sh
python3 -B archives/customer-attraction/tools/evidence/continuation-cce-benchmarks/source/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/probe.py
python3 -B archives/customer-attraction/tools/evidence/continuation-cce-benchmarks/source/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_cce/cone_attack.py
```

`audit_benchmarks.py` 是本轮不导入作者或规范代码的标准库Fraction实现，依赖只在本目录：核原件SHA、逐有序静态列的对偶、原始分布全部个体CCE约束、70/13客户完整策略、两起始策略、整数化公分母、完整有序历史集合值最低SPE递推，以及原程序完整输出等值。输出 `independent-replay.json` 保留全部记录。

```sh
python3 -B archives/customer-attraction/tools/evidence/continuation-cce-benchmarks/audit_benchmarks.py
```

未声称一般CCE桥、UP或六人half的结论；70客户证书的静态下界未给匹配原始分布，13客户的数值缩小最优状态未认证全局最小客户数。没有新增外审。
