# R-33e8 六提供者 optimal-query decorrelation 清洗

本批六源围绕同一辅助命题：能否把一个完整六提供者 SPE 的历史，改用任意全局最优六槽 tuple，并把跟随者尾部独立重采样而不损失比较量。六源均由 `clean show` 完整导出；冻结 SHA/blob/大小在 `source-manifest.json`。由于原仓库根部没有可导入的 `customer_attraction` 包，所需 `model.py`、`certificate.py`、`exact.py`、包入口和 `individual_security_failure.json` 以同一字节的冻结依赖复制到 `dependencies/`，其哈希也登记。

## 复现结果

- `optimal_six_query_decorrelation.py`：六提供者、七主题、34 客户、`EMPTY^3` 实际历史；完整历史 SPE 验证 `19608` 个有序历史、`117648` 个非自身偏离，实际 `W=34=OPT6`。四个最优三槽的 `delta=-5/18`；重复最优六槽 `delta=-3/8`；六个不同主题的最优六槽 `delta=0`。
- `actual_optimal_six_decorrelation.py`：在真实来源 `(6,7,8)` 前缀加入三个各 18 客户的银行主题，六提供者、九主题、88 客户；完整验证 `66430` 历史、`531440` 偏离，实际路径 `(6,7,8,0,3,4)`，`W=86`、`OPT6=88`。穷举 3003 个终局多重集找到四个全局最优六槽，每一个的 `delta` 都为负（`-11/72` 或 `-1/9`）。
- `audit_actual_optimal_decorrelation.py` 不调用模型/证书模块，独立用整数倍 60/Fraction 重建策略与 531440 个 IC，输出逐字匹配源 audit JSON；最小 IC 松弛为 0。

这些是辅助 decorrelation shortcut 的精确障碍。它们保留任意平局和完整历史量词，却明确**不是**当前六人目标的 `W<OPT/2` 反例，也不是 ROW 反例：第二个实际路径仍有 `2W=172>88`。任何后续全局证明不能无条件使用“任意最优六槽 tuple 可独立重采样”的桥接步骤；必须重新证明 signed option/尾部相关项，或改用其他证书。
