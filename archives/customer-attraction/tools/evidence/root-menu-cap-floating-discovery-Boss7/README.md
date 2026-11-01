# R-373d 相邻 factor 输出复现包

本目录保留来源 `25261bdccbe1c27d137b`（factor=2.5）和 `3b4b9db523e90c02ffef`（factor=3）的冻结 JSON 副本、生成器副本、结构与算术核验器及输出。两份 JSON 均声明 `floating discovery; no universal assertion`，固定三人六主题、43 个历史、215 条非零 IC 行和 seed=3738。

`verify_root_caps.py` 只核 SHA、字段、归一化、非负性、trace 长度和 `gap=factor*cap-W` 恒等式；它不证明 HiGHS LP 全局最优、策略完整 SPE 或一般 factor 界。factor=2.5 的最佳 gap 为浮点近似 `-67/864`，factor=3 的最佳 gap 为 `1/16`；正值只属于固定策略/客户锥/有限起点搜索。
