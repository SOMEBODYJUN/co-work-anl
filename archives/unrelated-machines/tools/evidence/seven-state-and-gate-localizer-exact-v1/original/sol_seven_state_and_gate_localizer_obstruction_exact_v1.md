# 七态原星的 AND 端点压缩：二次负载检验不延拓边界（Exact-only）

ClaimVersion: UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1

2026-10-18，scratch statement-only；作者候选，未独审，未登记。与仿射分类的 base≤4 合同分开；本合同使用 base≤5。

## 1. 全部基础参数与真实 law

任取正偶数 d、s，2≤s≤d/2。令 eta=s/d、h=s/2、T=1+eta、p=eta^3/1000、u0=4p(1−eta)、e=4/5−p−u0。

基础 Boolean 坐标为 C,Y_1,…,Y_d，H=ΣY_j。P 的 (C,H) 类别及概率如下；类别内均匀选择 H 个不同索引置 Y_j=1：

| C | H | 概率 |
|---|---|---:|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

这是全部参数域的正概率 law，0<eta≤1/2、1≤h≤d/4。基础物理行 v 的负载为 load_v=C+H/d，记 g=T−C−H/d。

物理读法是原 unit job R 在 u/v 两端时间一，原 jobs j=1,…,d 在 v 用时 1/d、在不同 private z_j 用时一；C、Y_j 是它们在 v 的原端点。本文讨论新端点扩展时，要求被检验 v 的负载公式保持不变。

## 2. 精确量词与共同矩假设

任取 i∈[d]。Z 是一个新增原 endpoint 的 degree-one 指示变量，或明确声明的新增 Boolean 坐标；不能只把已存在的 degree-two 多项式 CY_i 改名后仍按 degree one 计数。

设 Lhat 是所有有关变量的次数≤6 多项式上的同一个实线性泛函，并满足：

1. Lhat(1)=1，全部次数≤3 monomials 的共同 M3(Lhat) PSD。
2. 对每个只含 C,Y、次数≤5 的多项式 r，Lhat(r)=E_P[r]。
3. Z 及所有原 endpoint 的 Boolean 等式、原 jobs one-hot 等式支付到总次数六；尤其 Z²=Z 的乘子等式支付到次数五。
4. 所给点忠实实现 AND 的二次 Gram 等式：

       Lhat[(Z-CY_i)^2]=0.

则允许的全局原变量二次多项式

    q=Z(H-h)

严格违反 v 行负载局部化：

    Lhat[g q²]=−p(1−eta)(d−h)²<0.

因此不存在同时满足以上假设和全部 deg(q)≤2 的 v 行非负负载检验的共同点。无需另假设原行 CONFIG first/pair；加入它们也不能消除该矛盾。

## 3. 物理与量词边界

Z 可真实地来自一枚新增原 unit job K 的两个不同 private unit 端点：在候选 assignment law 中按 CY_i 选择第一端，按 1−CY_i 选择第二端。K 不在 v 上收费；所有原 jobs 完整执行。此读法只是定义一个候选 law 的依赖，不向普通 UM 添加逻辑 AND 侧约束。合同说明这种忠实扩展不能保留原 v 行全部全局二次检验。

结论不声称一般所有非仿射接线都失败，不声称任何其他 AND 实现都满足本假设，不给 actual near-two gap、source decoder、算法或 SDP finder。若 base≤5 矩、忠实 Gram 等式或原 v 负载公式改变，则必须另作分析。

本文不把 base≤5 的支付偷换成此前仿射分类的 base≤4，也不声称 base≤5 是最弱必要条件。作者 Proof 另冻；只据本 Exact 的独立审查者不应先读 Proof。
