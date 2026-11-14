# Review — customer-attraction-3a-3a-424f91c57e167bce

## 完成范围

本轮完整读取了任务声明要求的核心计算、低阶提升程序页、独立 Fraction 摘要和 388,712 字节的全逐行检查文件。另按 deferred candidate 规则读取并比较了 registry 中的 `M-ea8b88f526d44d619a0c86ad10acb6b0`（三人五客户精确点）及方法对象 `customer-attraction/global-low-degree-customer-lift-local-full-policy-moment-probe`。没有运行原浮点搜索、LP、随机 BI 或未知 trial，也没有将程序输出摘要代替数学正文。

核心 registry pin：`56bcd82c7238a69fa8f075c0ae75b691aa963c65bcb92f825e922aebbd51cd55`。

方法 registry pin：`b9f570eeb17eceffc56c0d9165d50cc1b180228983fa5ed35cc86b0bb9bbf4d5`。

三人构造对象 pin：`e5151a837ae8f02d87e4f0c783062f1de890707d18235e858a105f4d7394eb66`。

## 数学判断

模型是有限 Boolean 交集矩、固定完整有序策略和真实偏离续局；全部有序历史、空覆盖、重复行动、同覆盖异标签和平局均保留。二阶提升只要求同一组 `x_B≥0` 恢复所有 singleton/pair 矩；它不是逐 pair 另找资料，也不约束三阶以上坐标。只有绑定全部可见阶，程序页才允许同一 `x_B` 同时解释全部收益和覆盖。

独立 Fraction 检查共核对 1,845 个有序历史、9,194 个非自身 IC 行、1,123 个局部圆柱行和 57 个二阶提升等式；所有局部与 IC slack 最小值均为 0。三点固定分类为：

- `m3p5`：25 个矩、31 个历史、105 个局部行、124 个非自 IC；保存 lift 为 `1/3,1,1/3` 三类，乘以 3 得五个单位客户。该完整策略在全部历史是真实 SPE，`W=3`、`OPT_3=5`，比值 `5/3`。
- `m4p6`：56 个矩、259 个历史、416 个局部行、1,295 个非自 IC；保存点为 `t=(9/10)t*+(1/10)1`，根 `(2,0,0,0)`，固定点比较值 `19/10`。全目录行 `P=Q-z_1z_3z_4` 在每个 Boolean 类型非负，但在保存点为 `-1/10`，所以没有共同非负全矩实现。
- `m5p6`：62 个矩、1,555 个历史、602 个局部行、7,775 个非自 IC；保存点为 `t=(24/25)t*+(1/25)1`，根全 2，固定点比较值 `49/25`。取叶 `(0,1,3)` 得行值 `-1/25`，同样排除所有共同非负全矩实现。

三次分离使用

`Q(z)=z_A-Σ_i z_Az_i+Σ_{i<j}z_iz_j`，
`P(z)=Q(z)-z_iz_jz_k`。

若 `k=Σ_i z_i`，则 `Q` 为 `binom(k,2)` 或 `(k-1)(k-2)/2`；三叶全出现时 `Q≥3`（无中心）或 `Q≥1`（有中心），故 `P≥0` 对全部 64 个原标签赋值成立。保存 m4p6/m5p6 具有 `Q(t)=0`，而三叶坐标分别为 `1/10,1/25`，形成严格负值。给定 degree-2 lift 的高阶不匹配数虽分别为 13、31，但真正排除任意非负延拓的是这条全目录三次有效行。

## 新建和复用的数学边

1. `cag-424f-degree2-lift-cubic-separation`（`specializes`，accepted）：核心对象 specialization 到低阶提升方法。它支付 degree-2 放松的精确边界：全树 IC、全部局部圆柱和同一全目录二阶非负 lift 仍可与三次全目录正性不相容。它不否定方法作为放松的正确性，也不宣称固定策略 LP 全锥最优、一般 half 或六人结论。
2. `cag-424f-m3p5-lift-gives-real-five-customer-spe`（`implies`，accepted）：核心对象对 deferred 三人构造对象的完整推出。该边仅覆盖 m3p5 的五客户真实 SPE；不把 m4p6/m5p6 的 signed 分解误作客户输入。

没有复用同模型 hub，也没有把共同目录定义、低阶局部圆柱或“探索警告”单独建边。原任务声明的 core↔method follow-up overlap 已由第 1 条边、support 和本 review 完成，receipt 以 `closed_overlaps` 记录其关闭；M 与方法对象的独立比较留给其 own 3A/3B 任务。

## whole / contribution / remaining

**Whole result（核心对象）：** 三个保存点的完整 fixed-policy 记录已分类：m3p5 有真实五客户实现；m4p6、m5p6 各有完整全树 IC 和共同非负二阶 lift，但被有效三次行 `P` 分别以 `-1/10`、`-1/25` 排除任何共同非负全矩实现。

**Contribution（本轮边）：** 将“低阶共同客户提升不等于完整客户实例”的抽象警告落为两个可复核的全目录三次分离，并将 m3p5 真实化为五客户完整 SPE；把 `W=1` 的保存点比较值与真实单位客户 `W=3`、`OPT=5` 清楚分开。

**Remaining：** 其它 `(m,p)`、其它完整策略、degree≥3 的一般分类，固定策略锥 LP 的精确最优性，以及任何一般 half/六人命题仍未付清。`trial/seen` 只描述保存改善时索引；不据此宣称浮点搜索完备。三次分离不构成原 CAG 的福利反例，因为 m4p6/m5p6 不是非负共同客户实例。

## 证据哈希

- 核心计算：`8bad08c48994ea8b7479e9e2e709aa0f9fdca8eca49c0f87351bacbe5cd696fb`
- 低阶程序：`86d023fe94edc24bb0ca73bdfb4021a93d9d446ade5113c21201d95aee916711`
- 独立 exact audit：`1d53851ae07156920f846091c8623ae2ac5f92debdf2d8600865aa321d738c01`
- 全逐行检查：`fcaa317118c3f96aee303ea5273fcc83140d0d9cf3045538a2a8d24af73c7264`
