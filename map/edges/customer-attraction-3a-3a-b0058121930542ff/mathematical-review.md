# `cag-727-indexed-single-menu-enhancement-exact-primal`：完整 staged reading 与迁移边界

## 核心核验

本任务只声明一个 core：`cag-727-indexed-single-menu-enhancement-exact-primal`，登记 pin 为 `963a82432a4bf60244b42f3337a5d6e02126e4001d91c42eee84e40457866d4a`。八个 staged reading pass 已按任务的精确字符区间完成；两个 JSON 均作全字节/全字段结构化读取，没有以截断输出冒充完整阅读。

冻结原件 `exact_optimum_primal_terminal_cross.json` 的 SHA-256 是 `e2caa8f504da61dd41c6980671f2ce3d0c715f5d4dcce4b16dd656af25363acb`。原件包含 69 个正有理原子、727 个不同原行名、`W=1`、

\[
 O=\frac{136132273842587239488826855279451539729}
 {66662552162457874669169528301970771146},
\]

并且

\[
 O-2W=\frac{2807169517671490150487798675509997437}
 {66662552162457874669169528301970771146}>0.
\]

同 SHA 的新核验包 `new-727-primal-and-signature-factorization.json`（SHA-256 `2b6040eb5f6dd2d32343f9ca5bd40a6ad9580c0f3570a1f9e4d2a3a60c9af162`）报告：727 行按 `437+10+110+160+10` 分块；725 行（50025 个原子系数）新求值，`crossfinal:AB:Sbranch:2O` 与 `crossfinal:AB:Sbranch:3O` 两行（138 个系数）沿用同 SHA 的成熟精确核；全部 727 个保存值逐项相同，78 行 slack 为零，其余非负，负 slack 为零。`W`、`O` 与原子域也沿用同 SHA 的 HG 入口。没有重新运行旧 CLI、LP、QR、外部 solver、旧 217 匹配或全型 dual loop。

## 固定菜单与索引范围

每个原子只有以下固定字段：

- `bits` 为十位 `ABCDEUVWXY`；
- `AB_hist`、`AE_hist` 各为 8 桶 `(t,r,s)`；
- `second_hist`（正文称 `Sbranch`）为 16 桶 `(t,h,i,j)`；
- `menus_lh` 为 `actual`、`second`、`third` 三个旧末回复菜单的 `(ell,h)` 对；
- `exact_mass` 为正有理质量。

三个直方图各自总数为 5，共同 `t=1` 的重数为 `d`；合法菜单满足

\[
0\le h\le d,\qquad 0\le \ell-h\le 5-d.
\]

727 行的增量范围是固定的：

1. 旧 437 行使用原五人索引系统的 `actual/second/third` 规则。
2. 10 条同族末位去对角单菜单行：AB 源到 AE 位置 1、2，以及到 Sbranch 位置 1、2、3；每个目标菜单各有一条 `D` 和一条 `O`。共同 `t` 坐标 0 不在这十条 single 行中。
3. 110 条同族保一份交叠的两查询模式：AB、AE 各 6 个可重复无序位置对，Sbranch 10 对；每对五种等号模式。
4. 160 条跨族 pair 行：AB→AE/Sbranch 与 AE→AB/Sbranch 的目标位置对，每对五种等号模式；source 在共同 `t` 组内背景相同，所以这一步是按必要 envelope 计值，不选择随机 coupling。
5. 最后 10 条为上述 AB source 跨族末位单 `D/O`。`727` 不含 Sbranch 位置 2、3 的共同 `OO` 行；该共同行属于 728 扩展，不能把两个 single 行的最大值相加来替代它。

因此，当前原始点的 `O` 只是五个固定比较槽并集的投影覆盖；它不是补全目录后的 `OPT`，也不是已实现完整 SPE 的福利。

## 必要性与反例口径

在固定五人模型内，每一行来自同一完整 SPE 合法节点/查询的 IC 必要条件，或把单客户匹配/配对逐客户取上包络后得到的必要行。聚合时先在客户外选择非负行乘子；不能为每个客户分别挑最有利的 IC。于是任何真实五人完整 SPE 的投影都落在该 727 行非负锥中，而冻结 69 原子点给出该锥中的精确有理证人，直接反驳“这 727 条必要行本身就推出 `O≤2W`”。

这只是固定投影模板的反模型：直方图族在共同 `d` 之外按扩大域独立组合，且逐客户 envelope 不保证所有客户极大配对可由一张共同主题表实现。源正文还记录同一点在加入 AB→Sbranch 位置 2、3 的共同 `OO` 后出现严格负 slack；故该质量点没有保持那些边缘的完整共同菜单/SPE 补全。该负分离加强了“有限必要系统不充分”，却没有把点升级成真实目录或真实 SPE 反例。

## 可迁移性审查

本对象没有可在本任务内登记的新逻辑端点：`read_object_ids` 为空，`CA-FIVE-INDEXED-UPPER`、`CAG-MODEL`、`M-60da76cf3a0943d79e740518cf376645` 与 `cag-two-tail-comparison-three-index-equality-pattern-closure` 都是 deferred candidate。任何把本点连接到共同 OO 证书、全型 dual、`Q-CAG-HALF` 或恰六人完整历史问题的边，都必须先通过 read-add 实读相应对象，不能仅凭共享词汇或既有导航边扩端。

即使作为数学判断，727 行也不能无条件迁移到六人：行名、十位索引、五比较槽、三旧菜单及其末位量词都绑定五人必要投影；增加一名提供者会改变真实历史、末位源和新增偏离集合，必须重新定义六人行系统并证明其必要性。当前点既不证明也不反驳 `Q-CAG-HALF`，也不构成恰六人完整 SPE 的福利反例。

## 交付判定

本包只保存本 core 的完整读取账、精确范围与负迁移审查，`edge_ids=[]`。不创建未经 read-add 授权的 endpoint edge，不把 727 primal 误记为 full dual、SPE 或六人 half 证书。
