# 上一主题正价格：直接 OPT 六题平均报价

代理 `previous_price_search`；RUN `six-boss1-20261111`；共同目录内独立工作区 `previous_price_search/`。本页负责记录实际执行、准确合同、证据等级和下一义务，不认领 Main 已证明的上一主题正价接口。

## 当前任务和边界

已读 `main_previous_theme_price.md` 与 `research/GITHUB_RESOURCES.md`。本轮先固定 actual 源 `i∈{1,…,5}`、当前初始合法主题 `T=A_seed`、折扣 `θ∈{1/4,1/2,3/4}`。被定价的上一主题 `F` 依次取六个固定最优比较标签 `T_j`，最后仅对合法索引 `j` 均匀平均。静态查询菜单为六个 actual 标签以及六个比较标签的均匀菜单；动态查询允许 current 和 previous。静态菜单、seed 和全部非负参数先固定，再任取上一主题。

一般客户型为 `(b,d)∈{0,1}^6×{0,…,6}`，共 448 型。`d` 是六比较主题的实际会员计数；它只出现在合法索引均匀平均与静态查询均值中，从不作为分数强制主题。置 `p=Σ_{r<i}b_r`、`ell=Σ_{r≤5}b_r`、`k=7−i`、`t_seed=b_seed`。共有 14 个全局非负参数：`sigma,alpha_m,alpha_l,beta_m,beta_l,mu_A1,…,mu_A6,mu_mean_T,mu_current,mu_previous`，按总和一归一化。`k=2` 时两项 middle 参数没有作用，计算可将其固定为零并明确记录；这样不删任何非零行方向。

四状态为 `(a,t)`，真实下一状态严格为 `(t,c)`，`c∈{0,1}`，`s∈{0,…,k−2}`。单步费用、唯一折扣 Bellman 值以及正价完全沿用 Main 接口。每个案只支付一次

`B = sigma*u_i + ((k−2)*alpha_m+alpha_l)*u6 + ((k−2)*beta_m+beta_l)*K`。

对六比较主题平均的初值是

`(1−d/6)*Psi(0,t_seed) + (d/6)*Psi(1,t_seed)`。

因此一般行是上述预算减去全部客户平均初值。对于当前 15,593 列坐标，只有 `K` 与 `hist` 列可能非零；其余原 4,849 列及全部辅助列系数为零。不需要新的隐式 coupling。空题、重复标签、任意平局、零客户及所有 Boolean 会员型保留；当前点只是必要条件 LP 点，不是 SPE。

## 固定输入与执行约束

- 精确点：`peer_augmented_lp/augmented_lp_exact.json`；SHA-256 `d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f`。
- 精确矩阵：`peer_augmented_lp/exact_matrix.json.gz`；预期 SHA-256 `6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9`。
- 规模：19,621 行 × 15,593 列；原始列 4,849；`W≈0.4925763826272197`。
- 本地至多执行两案，核实现后停止；90 案按三个折扣拆为每份 30 案的 Actions 任务。由 Main 创建请求、checkpoint、触发及取回，代理不接触 Git、凭据、registry 或 RUN 总文件。
- 数值最优权只作发现；固定权用有理数与全部 16 平稳下一位策略重建。负行必须再独立核对完整 Boolean 域、所有原 4,849 系数和辅助零系数。无负时不把所返回权的非负 slack 当成整个权锥无分离；尝试额外恢复精确 occupation-flow 下界证书。

## 当前进度

已核精确点与矩阵 SHA、19,621 行、15,593 列和原始列数。独立参数化发现脚本 `previous_price_search/discover.py`、不导入发现代码的 Fraction 复核器 `previous_price_search/verify.py` 及三批 manifest 均已完成。本地严格只执行以下两案，没有启动 90 案扫描：

| 来源 | 当前种子 | 折扣 | 返回权精确 slack（近似） | 全 14 权锥精确下界（近似） | 有效参数权锥下界（近似） |
|---|---|---|---:|---:|---:|
| actual2 | A6 | 1/4 | 0.00292674754628205 | 0.00292674754628198 | 同左 |
| actual5 | A1 | 1/2 | 0.0216872827462983 | 精确 0 | 0.0216872827462983 |

第一案返回权包含 `mu_previous=716/995907>0`。第二案 `k=2` 的两个 middle 参数是无效方向，优化时固定为零；独立证书仍保留全部 14 坐标，因此完整权锥只能给出精确零下界，有效 12 权锥则有严格正下界。两案的全锥结论均来自精确有理 occupation-flow 证书，不是从返回权非负反推。

两案都已独立重算 448 客户型与每型全部 16 平稳下一位策略，分别检查 262,144 与 32,768 个字面 Boolean 赋值、全部 4,849 原列及 10,744 个辅助零系数；两份 `independent_audit.json` 均通过。结果分别在 `smoke_actual2_seedA6/` 与 `smoke_actual5_seedA1/`，没有新负行。

`computations.json` 按三个折扣拆为各 30 案，固定 NumPy 2.3.5、SciPy 1.17.0，每项算法 600 秒、Actions 预算 15 分钟，输出目录彼此独立。已用现有 `tools/compute.spec` 与 `input_paths` 只读核验每项精确绑定四个计算依赖；请求命令与验收要求见 `COMPUTE_HANDOFF.md`，指纹见 `input_bindings.json`。三批当前待 Main 创建请求并 checkpoint 推送触发，尚未声称 Actions 已运行或完成。四个计算依赖保持冻结；取回后仍须由本代理汇总并审核完整 90 案，不能把这两案结论扩展到其余来源、种子或折扣。
