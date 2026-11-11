# 新 20910 点：177 查询包络精确可行，新 E 的 B4 条件联合诊断失败

RUN `six-boss1-20261111`；Boss1 内部义务 `/root/rze_query_closure_20910`。
**本有限义务已完成、冻结并释放：全部指定 177 条单查询上包络有精确可行 E，
但这份新 E 在同一 B4 的两条条件联合上界中严格失败。**
这里没有共同客户律或完整 SPE 的结论，没有从条件诊断产出普遍原点负行。
原 cb45 点的其它排除及后续 20911 点由 Main 独立处理，本目录不再扩展优化。

## 1. 唯一输入和完整范围

输入是 `full624_augmented_lp/recovery/augmented_lp_exact.json`，SHA256
`cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932`。
原 E 符号层 SHA 是 `76573a43318fd55f38b5ccab8eee04b4c2e2bb7f54ea5b68a4c5bc4930f6c48b`，
原 E 证书 SHA 是 `00c78a5f23de4ff30d5fc66af362d95767a8b67c101dfa863ad701cffa225c30`。
没有读取或迁移旧 b0ca 点的共同原子网络。

保持有限单位客户、有限非空共同标签目录和全部完整有序历史纯 SPE；
保留非严格平局、空覆盖、重复行动、同覆盖异标签与零客户。
完整保留原 4,849 列、16 个 hist、194 组和 776 个 E 四态质量，包含零 hist
`1,59,366,449,524,574`。旧 00 态始终保为符号式 `H−m01−m10−m11`。

新增域是 42 条四索引轨道各自的 E→R、E→Z、E→E、Z→E，共 168 行；
另有同一 B4 真末位 H2→E 三行及 E→H1/H2 六行。原 42 条 R→E 和原 893 行完整保留。
Z 源使用 `P+r_e+1`，E 源使用 `P+z_e+1`；同源交叠从 R/Z/E 八态读取。
非同源使用正向 `min(前缀位质量,查询质量)` 单查询上包络。
B4 钱包来自同一份完整八态，第三位未被当作标签。

## 2. 原固定 E 的 51 条负上界

原 00c78 证书在新增 177 行中有 51 条精确负行：E→E 21 条、Z→E 27 条、H2→E 3 条。
按名称排序的第一条是 `E-to-E,(0,1,0100)`，约 `−0.00018409716986315217`；
最负是 `H2-to-E,(1,0)`，约 `−0.02192262112066653`。
它们只排除原固定 E 边缘，因此随后允许全部 776 个 x 重选。
完整分数、符号表达式、负行与去重映射保存在
[fixed_envelopes.json](rze_query_closure_20910/fixed_envelopes.json)。

## 3. 自由 E 完整提升及唯一云端发现

177 条要求行按完整符号表达式去重后新增 163 条主行；
其余为 3 条自查恒零、9 条原同源重复和 2 条新行之间的确切重复。
每个非同源 min 引入非负 t，并保 `t≤a`、`t≤b`。
所有主行中 t 系数为正，可行后把 t 全部重取为 `min(a,b)` 不会损害任何主行。

|规模|数量|
|---|---:|
|原符号坐标|4,849|
|可重选 E 四态质量|776|
|min 辅助|10,258|
|新非负变量总数|11,034|
|保留原行|893|
|新增唯一主行|163|
|min 两侧上界|20,516|
|显式总行数|21,572|
|全部非零符号系数|206,398|

通用矩阵 `symbolic_lift.json.gz` SHA256：
`cf420cca78dd507239aa3baac1538093177d10c8b37af84fc5a945209816fdc8`。
它先保存原 4,849 列的全部符号系数，再固定 cb45 点做 phase I。

正式请求 `C-six-boss1-rze-closure-20910-01` 在 Actions run `43087374448`、
job `130755301825`、artifact `13886408585` 执行；源提交
`e4b9a8702cab8fe47ca4370fd5d025ee3b7d70cc`。
**仅一次 HiGHS-ds，1.678407391 秒、8,172 次迭代，数值 δ=0。**
原始云输出完整保留且未覆盖；输入 SHA、NPZ 矩阵/向量和全部行列顺序均再次独立核对。
本地没有优化调用，也没有第二次数值求解。

## 4. 精确恢复及独立核验

有理消元只恢复 776 个真实 E 变量：活动方程秩为 **768**，
自由变量零基索引为 `167,199,209,312,318,415,446,576`。
八个自由量取靠近云结果的有理值后，全部约束精确通过；
最大 E 浮点位移约 `3.074×10⁻¹⁵`，它只说明发现来源，不作为可行证明。

随后从已恢复的精确 E 和原点逐项重取全部 **10,258 个规范 min**。
全部 **21,572 行精确非负**：17,798 行为零、3,774 行严格正；
85 个 E 四态质量严格正，其余 691 个为零。
所有 177 条指定查询及完整别名映射均独立核验：**169 条严格正、8 条精确零**。

|指定查询族|总数|精确零|严格正|
|---|---:|---:|---:|
|E→R|42|0|42|
|E→Z|42|0|42|
|E→E|42|3|39|
|Z→E|42|3|39|
|H2→E|3|2|1|
|E→H1|3|0|3|
|E→H2|3|0|3|

除三条 E 自查和两个非对角 H2→E 外，其余三个零为
`Z-to-E,(0,0,0123)`、`Z-to-E,(0,1,0123)`、`Z-to-E,(1,1,0111)`。

新精确证书 SHA256：
`976099de1f968062f94bd839bb2c5597d7be74e0d7bade5a6fb8c2966749e79e`。
证书见 [exact_certificate.json](rze_query_closure_20910/exact_certificate.json)，
全部 177 行新余量见 [new_envelopes_exact.json](rze_query_closure_20910/new_envelopes_exact.json)，
独立核验见 [independent_certificate_audit.json](rze_query_closure_20910/independent_certificate_audit.json)。

预检的字面重构覆盖全部旧、新系数，核 42 个四索引轨道及三个节点轨道的 720 置换频数，
另核全 16 hist 的 483,840 个轨道置换像、全部 min 正向和两侧上界、10,258 个二元极大运输表、
177 个真实钱包和完整去重映射。最终核验还逐条确认冻结输入及八个原始云输出未变。

## 5. 新 E 的 B4 条件联合诊断：两条严格负

按 Main 的 `main_E_B4_conditional_bound.md`，本点两个非对角族的旧 H2→Z 上界均精确为零。
因此，任何保存这些旧边缘并满足旧真实查询的共同客户律，在每个正 hist、每个 off 节点须有

\[
c=|Z\cap H1|=\min(z,h).
\]

新 E 的 own RZE 边缘还确定 `e=|E|`、`k=|E∩Z|`，故同一 H1 的交叠必须满足

\[
|E\cap H1|\le\min(k,c)+\min(e-k,h-c)
=\min\{e,h,k+(h-z)_+\}.
\]

以这个分层上界替换普通 `min(e,h)`，重新评价 H2→E，得到：

|节点轨道|普通包络|条件联合包络约值|严格加强的具名 hist 块|
|---|---:|---:|---:|
|family 0，非对角|0|**−0.0023925499522877685**|21|
|family 1，非对角|0|**−0.001404590751783132**|30|

对角族的旧 H2→Z 上界严格正，没有使用饱和推论。
独立程序对全部 16 hist、66 节点核边缘和适用域，
对两个零面的 **960 个块、7,680 个字面 (Z,E,H1) 运输格**重算真实 B4 末位查询价，全部吻合。

这严格排除**本次恢复的这份 E 边缘**与同一 B4 共用满足相关真查询的共同客户律。
它没有证明所有可重选 E 都失败，未产生一条可脱离本点零面使用的普遍旧列切面。
本轮按明确范围完成一次诊断，不再在这个原点上增开优化。
完整分数与运输格见 [conditional_B4_diagnostic.json](rze_query_closure_20910/conditional_B4_diagnostic.json)，
独立核验见 [conditional_B4_independent_audit.json](rze_query_closure_20910/conditional_B4_independent_audit.json)。

## 6. 复现、保存和完成边界

原始 Actions 输出位于 `actions_output/`，仅供读取。
以下命令都只作有理运算或核验，不调用优化器：

```bash
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/recover_exact.py
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/verify_certificate.py
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/conditional_B4.py
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/verify_conditional_B4.py
```

完整证明方向、源历史和 min 线性化见 [derivation.md](rze_query_closure_20910/derivation.md)。
最初一次旧 hist 索引解析失败及修正前源码已保存在 `failure_log.json` 和 `failures/`；
它未调用优化器、未参与任何数学结论。此次有理恢复和两份最终独立核验没有失败。
输入、代码、全部精确产物与原始云文件 SHA 汇总于 `freeze_manifest.json`。

**177 查询必要包络义务和一次明确条件联合诊断均已完成。**
后续若研究同一机制，应在 Main 指定的新点另立义务；
仍须保留共同条件律、第五源强制 E 的真实后继及全部有序历史策略闭包。
六人 `2W≥OPT₆` 仍 **OPEN**。
