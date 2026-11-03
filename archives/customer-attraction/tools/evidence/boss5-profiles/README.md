# 五人归纳轮廓：原数组、生成器与精确松弛证书

正式语义见 [五人归纳检验样本与轮廓数组--计算.md](../../../state/计算/五人归纳检验样本与轮廓数组--计算.md)。本包不是完整SPE反例，也不重新判定当前五人half。

- `original/test_profiles.py`：3942字节冻结生成器，未修改；原两个死helper的缺陷见正式正文。
- `original/tests/audits/`：生成器实际导入的两份三/四背景有理依赖，原字节保留。这里只作related依赖，不额外提交它们的done。
- `test_profiles.arrays.npz`：474206字节无损压缩后的全部八数组。shape、dtype、值及键序均与37435352字节冻结源一致，ZIP容器字节不同；原SHA只标识冻结源，详见manifest。
- `audit_profiles.py`：完整载入八数组；原生成器只重建矩阵，替换linprog为不求解结果；随后Fraction重构原16原子、14乘子，穷尽1507行和3072列判号。
- `array-and-exact-lp-audit.json`：实际成功报告，含每数组SHA、统计、全部分数、精确残差、依赖SHA和环境。
- `source-manifest.json`：两主源、两个related依赖的冻结commit/path/blob/SHA，新压缩容器及同值保留关系，比较过的正式对象指纹。

从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/boss5-profiles/audit_profiles.py
```

需要Python3、NumPy、SciPy；不求解LP、不采样游戏、不连接网络。显式 `--output NEW_PATH.json` 可写另一次审计报告。

旧原生成器本来会运行HiGHS并写未压缩NPZ；本次没有重复运行那个大LP。精确结果
`1036960650927089/471489290197392` 是这个必要行松弛的最优值，不能当成可实现SPE效率比。新证书的恢复不追认为原作者历史已交付的有理证书。
