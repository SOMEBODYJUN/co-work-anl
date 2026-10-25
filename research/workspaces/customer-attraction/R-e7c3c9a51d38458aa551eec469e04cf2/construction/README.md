# 原目标反例构造：当前接续

2026-10-25。本区只处理原 Q-CAG-HALF 的真实反例或明确一般反例机制。
目前没有主目标反例；没有一般 half 证明。

- [indexed_projection_seed.md](indexed_projection_seed.md)：仅检验已知437行最优点的两个明确投影能否经已证 signed 编译器成为真实坏种子。两者均失败，不能外推到该点所有实现或一般命题。
- [indexed_projection_seed.py](indexed_projection_seed.py)：精确重建10主题、或加 `--full-fixed` 的15主题组件；使用规范完整SPE续局集计算全部强制行动（含正常行动）的门槛。
- `indexed_projection_seed_result.json`、`indexed_projection_15_seed_result.json`：实际精确数值、源SHA、单位客户复制尺度及状态数。

下一步：共享遗漏的全人数构造。多尾污染只污染实际块、遗漏块保持私有时，容易在尾端暴露更有利的未污染主题；仅一条目标路径上“复制偏离者”不能当作真实SPE威胁。尚未得到能绕过这一问题的新机制。
