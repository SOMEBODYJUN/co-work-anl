# R-373d 根菜单容量相邻因子源比较

本批完整读取两个冻结 JSON：

- `25261bdccbe1c27d137b`，`root_cap_group_factor2.5.json`，167870 bytes，SHA-256 `fa95ba29e2130fa52f1d9fb138064f5c97f90b0d86427555a5456ee762567968`。
- `3b4b9db523e90c02ffef`，`root_cap_group_factor3.json`，75139 bytes，SHA-256 `89d34bf1f96e51bd7ee571e831a617b59de7128001c7c8e4c39ea0b840cb8028`。

两源顶层状态都明确为 `floating discovery; no universal assertion`，均固定 `factor`、43 个完整有序历史（深度 0/1/2，三人六主题）和 215 条非零 IC 行，seed=3738，两个去重首步背景。它们是同一 `probe_root_cap.py` 发现器的相邻因子输出，不是两个独立模型。

逐条结构核验 `p` 和客户权重的非负性/归一化、`gap=factor*cap-W` 算术恒等式、trace 长度和摘要值；脚本输出见 `evidence/validation.json`。这是 JSON 完整性和浮点内部一致性核验，不是重新求解 LP、全局最优证明或有理证书。

factor=2.5：trace 278 条，gap 全部为负，最优记录 `W=23/36`、`cap=97/432`、浮点 gap 约 `-67/864`；这只说明该有限搜索未找到正 gap。

factor=3：trace 190 条，最大记录 `W≈7/8`、`cap=5/16`、gap≈`1/16`，但该值来自浮点交替 LP 的固定策略/客户锥/有限起点；不能称完整 SPE 反例或普遍 factor=3 不安全。

与现有对象 `archives/customer-attraction/state/资源/R-373d根菜单容量交替LP浮点发现器--资源.md` 比较：该对象已经正确吸收发现器源码、模型、量词边界和 factor=3 复现，并明确本两相邻 JSON 当时尚未单独处置。本批独有内容是两个结果文件的完整冻结摘要、精确 SHA、trace 数、相邻因子对比和内部算术核验；应并入同一资源对象的“相邻输出”段落及 evidence 目录，不新增第二个数学命题。

建议两源均 `integrated` 到同一资源对象；不要标为 duplicate，因为每个 JSON 是不同 factor 的独立冻结输出，分别有 source ID、字节和数值轨迹。也不要标为 retained：其有限结果和证据在清洗后正文中有明确用途（复现相邻因子输出及防止把正/负 gap 混成定理）。
