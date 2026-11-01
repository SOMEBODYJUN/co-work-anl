# R-18 next_boss gap MILP proposals

三份冻结 JSON 的源字段均写明 `limitation: numerical MILP proposal, not an exact or general theorem`，本目录只保存候选数值与求解状态：

- `0f058ff99f06d6dd1009`：m=3,p=5, player=1, objective=gap；两次 `status=0`、mip_gap=0，proposal 均 2。
- `0a4e32f3f28fd7849789`：m=4,p=5, player=0；两次 `status=1`，40 秒超时，proposal 约 (8.96\times10^{-13},6.49\times10^{-13})，mip gap 约 (1.67\times10^{13},2.27\times10^{13})。
- `45d455cbe472e843691a`：m=4,p=5, player=1；两次 `status=1`，40 秒超时，proposal 均 1，mip gap 约 14。

这些不是精确 SPE 证书，不能解释为 half 违反或一般 gap 下界。
