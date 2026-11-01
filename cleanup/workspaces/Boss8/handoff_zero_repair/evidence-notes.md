# 证据核对记录：R105 `zero_repair_simplified.json`

- 源 ID：`9dc1659211141206f258`
- 冻结路径：`research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/zero_repair_simplified.json`
- 文件字节：406
- SHA-256：`7d33861f0ce051b21c01e05d23d3de4083f8d2a8bcb5db633c817217232a213a`
- 两个来源提交：`68fad804ec5946cb296f77dc5b336308a66abf12`、`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`

## 逐字段核对

- `weights` 长度 16；非零下标与重数为 `2:2, 3:2, 4:2, 6:1, 9:1, 11:4, 12:4, 13:2`。
- 采用 `mask = A*1 + B*2 + C*4 + D*8` 后，八类客户依次是 B、AB、C、BC、AD、ABD、CD、ACD，重数 `2,2,2,1,1,4,4,2`。
- 总客户数为 18；与 canonical `zero_regret_repair_witness.json` 的 topics/multiplicity 逐项相等。
- `old_policy=[2,2,1,2]` 与 canonical `old_tail_strategy.last_after_first` 相等；`path=[2,1]` 是首位 2 后按旧菜单取出的实际路径。
- `new_policy=[2,3,1,1]` 与 canonical `new_unique_tail_strategy.last_after_first` 相等，首位为 3。
- `background=0` 是简化记录的数组索引，不是旧背景的主题标签；相关 README 和 witness 共同说明旧背景是 A，删后为空。
- `purpose` 明确写出“actual-regret-only welfare repair”的有限障碍，且排除 Q-CAG-HALF 反例解释。

## 与正式证据的关系

canonical witness 的 SHA-256 是 `4f2397c2ace31a594dcc1f7f36547dd2a33a094f1baf4e1b88c5c66c88e6ba5a`，已存在于 `archives/customer-attraction/tools/evidence/R105-zero-regret-json-20261031/`。完整枚举和收益结论在 `R105零regret修复JSON完整枚举接续审查--审查.md` 与父方独立复核中已有承重说明，因此本文件不复制收益表或伪造新证明。

处置：`duplicate`；独有内容仅为 16-mask 压缩表示和简化过程元数据。未发现需要新增的数学对象或新的证据程序。
