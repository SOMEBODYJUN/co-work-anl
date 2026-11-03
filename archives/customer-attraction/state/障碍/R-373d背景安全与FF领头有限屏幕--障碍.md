# R-373d：背景安全与 FF-LEADER 的有限数值屏幕

本对象整理 R-373d security 目录的四个冻结源：`background_security_probe.py/json` 与 `fractional_background_probe.py/json`。源、clean-show 元数据、重放和独立验证器位于 `archives/customer-attraction/tools/evidence/R-373d-security-20261031/`。这组材料与前面的 R-31bbb 共同 (Q)、SSR 和 background pair 屏幕一样，研究固定策略锥、有限背景和浮点 LP/SLSQP；它们没有构成六人六提供者主模型的 SPE 证书。

`background_security_probe.py` 构造 6 个主题、3 个行动阶段的 reverse-group policy，prefix 由对称的有限背景组成。脚本明确测试较强的 residual assertion：当前玩家收益之和至少为 (r v_r(b))，并说明该断言不被 root aggregate-security conjecture 自动推出。460 个起点（115 个对称 prefix、每个 4 个初始查询）全部没有正 gap。最佳记录为 prefix `[1,1,1,1,1,1]`，gap `-0.0029540146616511276`，安全值 (v=0.10905239573044233)，residual profit `0.3301112018529781`。独立重放生成的完整 JSON 与冻结源逐字段相同，trace 的 gap 全部小于 0，范围约为 ([-0.03333,-0.002954])。

`fractional_background_probe.py` 固定一个策略锥，在有限 cutting-plane 集合上以 SLSQP 近似 oracle，扫描 105 个起点（degree 1--4 的对称 prefix 与三个初始分布）。冻结源的最佳记录为 prefix `[1,0,0,1,1,1]`，gap `-0.002890620997559684`，leader `0.14039193851154405`，oracle value `0.13750131751398437`，使用 82 个 cuts；原文的 scope 明确写着 fixed query、fixed full strategy cone、numerical convex minimization and cutting planes，且没有 proof 或 counterexample certificate。独立重放在相同 seed 下得到同一最佳 prefix 和 gap（浮点轨迹增加了 `cutting_plane_converged`、`finite_cut_upper_gap`、`oracle_cut_gap` 诊断），105 个 gap 同样没有正值；最佳 replay 的 `oracle_cut_gap` 约 (4.31\times10^{-8})，显示数值切平面仍有有限误差。

这些结果提供了两条可用线索：有限背景下 residual/leader 屏幕没有发现越界起点；并且在 fractional oracle 屏幕中，最接近零的 gap 约为 (-0.00289)。它们的失败机制也已保留：策略锥是固定的，背景只取有限对称 prefix，查询分布由浮点 LP/SLSQP 给出，切平面没有精确终止证书，且 residual assertion 的量词不同于 root aggregate-security。因而不能把负 gap 当作所有背景、所有策略、任意平局或完整历史的普遍下界，也不能把它转译为客户覆盖 half 定理。

与 R-31bbb 的共同 (Q) 结果比较时，只能说两者都在固定有限锥上进行数值可行性/安全屏幕；R-31bbb 的共同 (Q) 要求一个 (Q) 同时服务多查询，而本组分别优化 residual 或 FF-LEADER 的固定策略；变量、量词和目标不同，不能合并成一个证明。后续若要继续，应先把 residual、leader、root aggregate 三种量写成同一精确定义，再用 Fraction/整数残差核对所有 ordered histories、任意 tie-break、空/重复主题和零客户情形。
