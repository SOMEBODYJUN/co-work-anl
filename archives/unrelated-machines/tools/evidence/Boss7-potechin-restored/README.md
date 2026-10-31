# Potechin会议原文与本轮有限核对

本目录恢复冻结来源 `6cfd61c7a86bbe0e41b9`，并提供明确区分于原论文的有限补核。正式中文文献对象为[对称平方和背包下界](../../../state/文献/对称平方和背包下界--文献.md)。

## 原始资源

- `Potechin2019.pdf`：Aaron Potechin，*Sum of Squares Lower Bounds from Symmetry and a Good Story*，ITCS 2019，LIPIcs 124，article 61，61:1–61:20。
- DOI：<https://doi.org/10.4230/LIPIcs.ITCS.2019.61>。
- 冻结文件：`history/source/literature/unrelated_machines/potechin_2019_symmetric_sos_knapsack.pdf`。
- 冻结提交：`68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，两处字节相同。
- 文件大小：441551字节；SHA-256：`6e5b866215d85365d6cde9e9f43528081b6382b45f8590f13e5f13cc89c774ca`。
- 原文首页标注CC-BY许可。原文提及的arXiv较长版本未在本轮导入或宣称读过。

## 本轮新增的有限核对

`verify_fractional_slice.py` 是本轮整理者补写的纯标准库程序，不是Potechin论文附属程序，也不是一般PSD定理的证明。用法：

```sh
python3 archives/unrelated-machines/tools/evidence/Boss7-potechin-restored/verify_fractional_slice.py
```

实际运行记录为 `finite-verification.json`。它检查两组 `(n,k,s)`：`(8,3/2,2)` 和 `(7,7/2,3)`，其中 `s=⌊D/2⌋`、`D=min{2⌊min{k,n−k}⌋+3,n}`。全部次数至多 `s` 的Boolean单项式组成完整矩阵，分别为37维、64维；有理Schur消元给正主元28、35个，剩余零方向9、29个。另检查15条基数递推、81组全部合法基数参数的柱面恒等式、形式均值与二阶方差，以及 `n=8,k=3/2` 时负三文字事件的精确值 `−1/896`。

一般量词仍依赖原论文good-story框架及其表示论基础。有限运行不认证完整表示论证明、外部同行评审、最新文献状态、调度间隙或CAG半覆盖结论。

抽取全文、关键页图、比较原件、检索边界和未提交receipt保存在 `cleanup/workspaces/Boss7/resume-20261031-current/potechin/`。本地存在不表示已checkpoint、已推送或已执行clean done。
