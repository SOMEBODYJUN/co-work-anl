# READY 阶段交接；原数学义务仍 working

> 历史交接记录：本页保存派发前状态。Actions 已返回且后续有限义务已完成；
> 当前准确结论见上一级 `rze_query_closure_20910.md` 和本目录 `freeze_manifest.json`。

Main 已创建正式请求 `C-six-boss1-rze-closure-20910-01`。
本代理按 Main 指示在 READY 阶段释放运行槽，待真实 Actions 输出落盘后由原代理接续。
这里没有 phase-I 结果，不宣布自由 E 系统可行或不可行，不将本有限义务标为数学完成。

## 冻结派发输入

`actions_ready.json` 精确列出四项依赖：

- `actions_phase1.py`，SHA `dc55b7263303b641d6a01f5871a2100812c00083797a4c7872fa016d9fd4b943`；
- `symbolic_lift.json.gz`，SHA `cf420cca78dd507239aa3baac1538093177d10c8b37af84fc5a945209816fdc8`；
- `preflight_literal_audit.json`，SHA `0a9911393b17de998a2c18a56c2c7d6fcd278c2ddf1c01c8193aa35d482d48ba`；
- 绑定的 `full624_augmented_lp/recovery/augmented_lp_exact.json`，SHA `cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932`。

只授权一次 HiGHS-ds、1,800 秒。全部输入、顺序、数值解、对偶、残差、失败状态由脚本保存。
本地只运行过 `--prepare-only`；优化调用数是零。

## 已完成的数学和精确检查

固定旧 E 证书的 177 条完整新增包络有 51 条负行；原 893 行仍全部非负。
保留全部 776 个 x 自由后，通用矩阵为 21,572 行、11,034 个新变量、206,398 个非零系数。
独立预检已核全部符号行、min 方向与上下界、全部 16 hist、42 轨道及去重映射。
这些结论只排除旧 E 边缘，不排除原 cb45 点的一切 E 补全。

## 输出到达后的操作

若输出在默认位置，依次执行：

```bash
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/recover_exact.py
python research/workspaces/six-boss1-20261111/rze_query_closure_20910/verify_certificate.py
```

若下载路径不同，第一条增加 `--discovery <实际 phase_I_discovery.json 路径>`。
恢复器不导入优化器。可行时只恢复 776 个真实 E 变量，再精确重取所有规范 min；
不可行时恢复非负 Farkas 乘子，消去全部 11,034 个新增列，交付原 4,849 列必要负行。
失败时保存失败原因并接续有理恢复，不允许因失败自动再次求解。

## 可行后的下一明确义务

Main 的 `main_E_B4_conditional_bound.py/json` 已在同一 cb45 点证明两个非对角族
旧 H2→Z 单查询上界恰为零。因此一般共同实现强制每个正 hist、每个 off 节点
`s=|Z∩H1|=min(z,h)`。新 E 可行后，必须再检查

\[
|E\cap H_1|\le\min(ez,s)+\min(e-ez,h-s).
\]

它是本点零面条件下的必要上界，不能直接冒充任意旧点上的恒等式。
本次冻结矩阵未加入该条件；若要产出普遍原 4,849 列切面，须保旧 H2→Z 真预算并引同一 ZH1 变量。
本页记录 Main 指明的后续义务，不将其插入已经冻结的唯一 phase-I 输入。
