# 阅读与比较记录：8b85dc80a79894990d23

## 原文

`clean show` 导出的 1189 字节 Python 源与 inventory SHA-256 `2348814955099606d05e4fda5216706300a1559827f2eee6df5f28946add567c` 一致。逐行阅读了 `rho`、`u`、`cov`、两组响应差矩阵、残余覆盖约束、二标签覆盖差约束、SciPy `linprog` 目标和有限分母打印。

## 独立复现

源脚本运行返回 HiGHS `Optimization terminated successfully` 和 gap `0.03954545454545444`。用源打印的有限分母权重另写 Fraction 复核，不复用 SciPy 浮点结果：`C01=1`、`O23=599/550`、`R=101/100`、`R-C=1/100`；36 个响应差全非负且最小为 0；除 `(2,3)` 外的无序二标签覆盖最小差为 `87/2200`，由 `(1,2)`、`(1,3)` 达到。

## 全仓比较

* 与 `archives/customer-attraction/state/反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md` 比较：该对象有三人四主题、21 个有序节点、完整纯 SPE 和静态 PNE 的 Fraction 核验；本源只有固定响应锥 LP，不能合并为同一证书。
* 与 `archives/customer-attraction/state/障碍/R-373d耦合桥与计数MILP有限证书--障碍.md` 比较：该对象的固定 bridge attack 和计数 MILP 也区分浮点候选与 Fraction 策略证书；本源不含完整策略树，证据等级更低。
* 与 `archives/customer-attraction/state/障碍/R-373d背景支撑分支缺口与三价模板精确障碍--障碍.md` 比较：三价模板页给出特定模板的 `status=2`/Farkas 障碍；本源是另一组六标签响应不等式和覆盖目标，不互相替代。
* 与 `archives/customer-attraction/state/审查/R18个体面行走算法--审查.md` 及其他 R18 固定锥材料比较：共同之处是浮点锥用于候选、随后需要有理/完整历史核验；本源只完成了权重可行性和覆盖间隙的独立重算，未完成 SPE 树核验。

## 处置

分类为 `integrated`：正文进入 R-373d 固定响应锥审查对象，源程序和精确复核进入证据目录。保留“固定锥内可行间隙下界”这一独有内容；不把源的 `linprog` `optimal` 文本直接写成有理全局最优定理，不宣称六人 half 反例或证明。
