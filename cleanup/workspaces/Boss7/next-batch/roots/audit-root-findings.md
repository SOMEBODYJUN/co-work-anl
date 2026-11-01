# R-373d root-menu factor 2.5 / 3 output audit

本附录对应两个冻结源：

- `source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json#root`
- `source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json#root`

对应 `main` 冻结路径内容逐字节相同；本地 clean-show 结果与已保存的
`archives/customer-attraction/tools/evidence/root-menu-cap-floating-discovery-Boss8/factor2.5.json`
及 `factor3.json` 逐字节相同。原始 JSON 已保全，但本附录记录其独有参数/屏幕结果，避免因证据副本相同而漏掉两个来源版本的语义处置。

## 固定对象与程序边界

JSON 的状态字符串明确为 `floating discovery; no universal assertion`，种子为 3738，
`full_histories=43`、`true_rows=215`。这来自固定 `m=3,k=6` 的 `group_policy`：历史数
`1+6+36=43`；63 个非空主题掩码作为连续客户权重坐标；完整固定策略的非零 IC 行去重后为 215；根背景是 `out((a,))-e_a` 的两个去重向量。交替 LP 使用浮点 SciPy/HiGHS，逐个固定策略锥和给定 factor 搜索 `factor*cap-W`，输出不含整数客户恢复、Fraction 证书、所有平局策略或所有 SPE 的量词。

## 两个屏幕

factor=2.5 源 167870 字节、trace 278；最佳记录为
`W=0.6388888888888888`、`cap=0.224537037037037`、
`gap=-0.07754629629629628`，有限分母近似分别为 `23/36`、`97/432`、`-67/864`。
查询分布近似 `(0,0,2/3,0,0,1/3)`。trace 中 gap 最大仍为该负值，因此这次固定浮点屏幕没有正分离。

factor=3 源 75139 字节、trace 190；最佳记录为
`W=0.8749999999999999`、`cap=0.3125`、
`gap=0.06250000000000011`，有限分母近似分别为 `7/8`、`5/16`、`1/16`。
查询分布为 `(1,0,0,0,0,0)`，非零 mask 权重近似为
`{2:1/8,16:1/8,47:3/8,61:3/8}`。这是一个浮点候选，不能当作精确单位客户完整 SPE 反例。

`verify_root_caps.py` 已检查两个文件 SHA、状态、参数、trace 长度、每行查询/权重归一、`gap=factor*cap-W` 算术关系和 best 值；检查仅为结构/算术一致性，不证明 LP 全局最优或任何博弈量词。

## 处置判断

两源的 raw JSON 内容已由 Boss8 证据副本保留，但它们的 factor 参数和相反屏幕结果在既有资源页仅以表格出现，仍需本批正式正文吸收。建议两源共同 `integrated` 到一个有限浮点屏幕审查对象；证据路径可复用逐字节副本，正文必须注明“原始文件副本重复、数学参数不同”。该对象只提供 exact-follow-up 的候选输入与回归基线，不提供六人 Q-CAG-HALF 定理、反例或一般 factor 界。
