# M-6a7c80923ec34610bc83cc446c36da8：联合旧/新原子松弛与 1269 行停界复核

- task：`customer-attraction-3a-3a-a9ce3bd652353c3b`
- object：`M-6a7c80923ec34610bc83cc446c36da8b`
- object pin：`c1bf01a3cb48cdc815d82886c85011ed4c8120be619cadea01a7b6e41c2012ad`
- deferred candidate（本报告不付证据、不写边）：`M-ec99da051b134c469ad29ba01810ff1f`

## 读取范围与证据身份

任务 JSON 声明的 8 个 reading passes 均已读取；两份大 JSON 的阅读在 pass 7/8 连续完成，未把 deferred candidate 当作已付证据。当前快照中 verify 脚本依赖的旧 `R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms.py` 不存在，因此只做了源码静态核验和 JSON 的 Fraction/结构检查，没有冒称重新运行旧科学程序。

|路径|SHA-256|读取范围/用途|
|---|---|---|
|`archives/customer-attraction/state/审查/R-3e17a9推广首位回复与联合原子松弛--审查.md`|`70ef4c6e358ea3b9da2e77c36a6a1d8a984b20a4c37228f13eba4bbd57a4fc95`|pass 1，§3「联合旧/新原子松弛」|
|`archives/customer-attraction/state/审查/R-3e17a9父方首次回复独立审计与1269停界--审查.md`|`b0e4e63965eaa4afd5e36e346f6be1f931ed8dd7dc80f8d9050ca78ec495e6f1`|pass 2 §3、§6；pass 3 §6 verify 范围|
|`archives/customer-attraction/tools/evidence/r3e17a9-parent-verify/promotion_joint_atoms_exact.json`|`9c84403826eb3d4e44d0fed55dcda180e9be80b0f07c4f464aecbe284f2015b3`|pass 4，完整字段/分数/原子/状态读取|
|`archives/customer-attraction/tools/evidence/r3e17a9-parent-verify/verify_promotion_joint_atoms.py`|`de5502b581051d1b6d8aeb5c720b37596c6e50d9a30c1e893ec4c47a6c8f739c`|pass 5，逐行核验旧/新行计数、literal 展开、断言边界|
|`archives/customer-attraction/tools/evidence/r3e17a9-parent-verify/related_joint_atoms.py`|`8a097c6bcf09999282a8112b00b9277c9d9d715517248d8d4adb7fbb19f2d5e9`|pass 6，核验 restricted common-R/Z 构造及 LP/精确回代语义|
|`archives/customer-attraction/tools/evidence/r3e17a9-parent-verify/related_attractive_nested_exact.json`|`cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1`|pass 7/8，完整 816,498 字符、1–59,372 行；作为冻结 3889 行输入点|

## 模型、量词与行系统

外层问题在审查正文中固定为：恰六名提供者、任意有限客户/共同目录、全部有序历史纯 SPE；Q-CAG-HALF 仍开放。当前 object 的数学量词更窄：**存在一个固定、有限、受限必要系统上的非负有理可行点**。它不量化客户整数重数，不给全历史动作映射，不给完整 SPE 或终局福利。

具体对象固定：

1. 16 个 `actual_bits`/histogram；每个 hist 的 `d=1`，组数为 10 个 hist 各 8 组、6 个 hist 各 19 组。
2. 29 个 `RZ_atoms`。每个原子的 `R`、`Z` 向量均为二元，长度按组为 8 或 19；原子质量非负且精确和为 1（`O=1`）。它们是 reply-orbit 上共同的 R/Z 位，不能直接解释为客户类型。
3. 21 个正质量 `promotion_states`，状态仅为 `DE=(0,1),(1,0),(1,1)`；同一 `(hist_index,word_index,DE)` 键不重复。`(0,0)` 状态由每个正 hist-word 的余量补齐。
4. 旧 raw families 1,143 条 + promotion raw rows 88 条 + 条件质量界 38 条 = **1,269 行**。新 88 行由脚本按 literal 定义展开；旧 1,143 行明确复用冻结旧 generator，不能表述成 1,269 行全部独立重构。
5. 新 88 行的代码族计数为：`source` 1、`oldpair-newpair` 1、`oldC` 2、`newE` 14、`pair` 49、`price` 12、`capacity` 2、`actualpair` 7。

`related_joint_atoms.py` 的注释和实现明确这是共同 R/Z 位的 restricted joint-distribution 子集。SciPy/coordinate-ascent 只用于列发现；`exact_recover` 才以 Fraction 回代并检查行松弛。因而不能把其 LP 支持或原子拼接成 full-domain 客户分布、全历史策略或 SPE。

## 已成立的精确整体结论（M-6a7…）

`promotion_joint_atoms_exact.json` 的 exact point 字段为：

```text
O = 1
W = 62639914980892951648306747072697141151134151554374880507144 /
    126208720217724762225533804965567209821942870207757303886307
  ≈ 0.4963200234724811
K = 30369037547445892528789753602637759169683390620777767915515 /
    126208720217724762225533804965567209821942870207757303886307
  ≈ 0.24062550903816915
1 − 2W = 928890255938858928920310820172927519674567099007542872019 /
        126208720217724762225533804965567209821942870207757303886307 > 0
minimum_slack = 0
rows = 1269
RZ_atoms = 29
promotion_states = 21
```

可精确推出的句子是：**在列出的 16-hist、29-atom、21-state restricted 必要系统中，存在 O=1 且 W<1/2 的可行点；因此这 1,269 条有限必要行单独不足以推出半覆盖。** 这是 relaxation obstruction/boundary 结论，不是原博弈的客户实例或半覆盖反例。

独立结构核对（不依赖缺失旧模块）得到：29 个原子质量 Fraction 非负且和为 1；所有 R/Z 位为 0/1；21 个 DE 键均合法且唯一；38 个有正质量 hist-word 的 `(hist mass − listed DE mass)` 余量均非负，其中 28 个为 0、10 个为正。JSON 的 `minimum_slack=0` 只表示该有限行集合的最小松弛为零，不能升级为完整 IC slack 证书。

`verify_promotion_joint_atoms.py` 的断言边界也被逐项读出：

- `len(old_names)==1143`、`len(NAMES)==88`；
- 父审/JSON 的新行逐字 literal 展开；
- 38 个条件质量余量非负，`(0,0)` 由余量补齐；
- literal 新状态案例数 59；
- 总行数 `1143+88+38=1269`，旧/新行与质量界的最小松弛均可为 0；
- 输出状态明写 `exact feasible necessary point verified; no game/SPE or half theorem`。

## 已成立的精确局部结论（同一审查对象中的边界证据）

1. **首位回复局部恒等式。** 父审计枚举 1,024 个 membership coefficient states，投影成 256 个 states；每个状态以 Fraction 检查
   `35r + 22v − H = raw_without_K`。
   这确认的是局部推广公式，不是完整策略。

2. **指定冻结点的严格分离。** 对冻结 `related_attractive_nested_exact.json` 输入点（该点自身是 3,889 行、1,905 列、175 个正列、W≈0.4770435185、minimum_slack=0 的必要系统点），局部共同上界给出

   ```text
   lhs − rhs =
   −69927133130576238991444255183583899 /
    21722188083558433386371840226644560 < 0
   ```

   raw 值约 −3.2191569681；按源 `/74` 缩放约 −0.0435021。该负分数只排除**这个指定 3,889 行旧点在指定首位推广合同下的扩张**。它不排除 1,269 点，亦不表示所有 promotion 方法不可能。

3. `related_attractive_nested_exact.json` 与 `promotion_joint_atoms_exact.json` 的 16-hist/组描述是共同输入骨架，但两者是不同维度、不同列权重和不同 row family 的有限点；不能因同一 hist 标签把它们合并成一个联合客户分布。

## 可写边及方向（需保持条件范围）

以下是可写而不会误报为 hub/全局边的方向；parent 可按现有 registry 名称绑定端点：

1. **restricted-point → finite-row insufficiency（`implies`/`diagnoses`，条件域）。** `M-6a7…` 支持“固定 1,269 行必要系统不足以单独推出 W≥1/2”。`conditions` 必须写明 16 hist、29 R/Z atoms、21 DE states、旧 1,143 行复用、88 新行、38 mass bounds；不得写成任意六人 SPE、全客户或全历史结论。
2. **`verify_promotion_joint_atoms.py` → `M-6a7…`（`verifies`/`supports`，有范围说明）。** 方向是证据复核到对象；只独立展开新 88 行和 38 质量界，旧 1,143 行借用旧 generator。因当前快照缺失旧模块，不能把“静态源码断言”写成此次运行结果。
3. **首位推广分离 → 冻结 nested 点（`separates`，指定点）。** 若接入已登记的 `M-0f1bb5c0749b4b9dac9b6e91b651bc34`（首位推广行严格分离指定 3,889 行旧点）与 `M-ad91b1aee1fc48fc867ded29f60f3361`（3,889×1,905 有理点），方向应为 `M-0f1…` 分离 `M-ad91…`，条件只保同源会员、报价、隐藏位和该固定向量。此边与 `M-6a7…` 的可行点是并列边界，不应写成 `M-0f1… ⇒ M-6a7…` 或反向蕴含。
4. **不建议写的边。** 共同 16-hist/组定义到所有 R-3e17a9 家族对象的 hub 边；“W<1/2”到“存在整数客户/SPE half 反例”；负局部分离到“全部 promotion 系统不可能”；以及 deferred `M-ec99…` 到本对象的任何方向边。

## Remaining / open obligations

- 给出整数客户重数/共同目录和所有有序历史动作映射；将 R/Z/DE 原子与同一客户、同一 `sigma` 的完整策略实现连接起来。
- 对每一个有序历史和偏离后继给 exact IC/SPE 收益比较，并证明新增 promotion rows 与旧 rows 可由同一策略同时支付。
- 若目标仍是 Q-CAG-HALF，需要新增必要行或结构性条件排除该 restricted W<1/2 点；当前 1,269 行本身只证明停界，不形成半定理。
- 恢复缺失的 `R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms.py` 及其依赖后，再运行 verify 脚本并保留独立运行日志；在恢复前保留 JSON 的 SHA 证据而不宣称执行成功。
- 将父审中“实际第三位完整三人尾”的下一义务与现有首位推广分开处理，不能用 1,269 点替代第三位完整通式。

## follow_up_tasks

1. `read-add M-ec99da051b134c469ad29ba01810ff1f`：读取 `third_requery_old_early.py`、`third_requery_old_early_separation.json` 及其声明的旧点元数据；核对 153 行/200×178 系统与 1,269 行的交叠，决定是否只有指定点分离，暂不升级为全局边。
2. 恢复 old `joint_atoms.py` 依赖并执行 `verify_promotion_joint_atoms.py`；把执行状态与静态源码核验分开登记。
3. 若继续六人目标，沿“第三位前移 + 完整 D/E/F 尾 + 共同 u3/u4/u6 预算”构造真实策略/整数实例，逐项付款后才可把必要系统点提升到模型层。

## closed_overlaps

- `promotion_joint_atoms_exact.json` 在联合原子审查、父审和 verify 语境中是同一 SHA 的一份 JSON；不计作三份独立数学证据。
- 1,024/256 父审计与作者报告的 2,560 identity checks 针对同一首位局部公式及同一冻结点；它们是核验层次，不是多个反例。
- 旧 1,143 行在 verify 代码中明确复用冻结旧 generator；只有新 88 行和 38 质量界被该脚本按 literal/余量独立展开。
- `related_attractive_nested_exact.json`（3,889 行点）与 `promotion_joint_atoms_exact.json`（1,269 行点）共享 hist/group 语法但不是同一点、同一行锥或同一客户模型；负分离只针对前者。
- 21 个 promotion states 是 DE 隐藏菜单质量，不能按“21 类客户”计数或和 29 R/Z atoms 相加为客户。
- deferred `M-ec99da051b134c469ad29ba01810ff1f` 的第三位 153 行分离未读成当前证据，也不与本对象产生边。
