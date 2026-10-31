# 七态 AND endpoint / 二次 localizer：Exact-first 独立重构

2026-10-18。本轮实际全文只读新候选 Exact `/workspace/scratch/038d9dcc4cac/sol_seven_state_and_gate_localizer_obstruction_exact_v1.md`，SHA256 `8ca3b942276658319808f3c32d5057b53611555d76bfbf6f4c5f94ea18e511ab`，header、§1–3 全部 56 行 / 3070 bytes，工具完整返回 791 tokens、无截断。未读作者新 AND Proof 或策略，未索取机制。

独立性只针对此新 Exact 的具体共同矩 / degree 合同。七态及此前 affine 分类已知且作者 Proof 已获释读过；此前自己的共同机制思考也考虑过非线性 Boolean observer 可能压低局部检验次数，因此不冒方向零背景 blind。以下是新合同从 Exact 的独立重构，不是另一份作者读后记录。

结论：PASS/no fatal。只证明所述忠实 AND 扩展不能保留原 v 行所有 global degree-two load localizers，不推一般非线性 gluing 禁止，不推软件、算法、hardness 或 source decoder。

## 1. 参数与有限度数

正偶 d,s 且 2≤s≤d/2 给 d≥4，0<eta≤1/2，1≤h≤d/4<d。p=eta³/1000>0，u0>0，e>0；所有七态类都有正质量。固定 i 任意，无须假设 h≥2。

Z 是新增 degree-one Boolean 坐标/原 endpoint，而 CY_i 是 degree two。所测 q=Z(H−h) 真是全局变量中的 degree two；g=T−C−H/d 为 degree one，所以 gq² 的总次数为 5，属于 Lhat 的 degree≤6 定义域。这里没有把已有多项式改名偷减次数。

## 2. 关键 null 提升，逐步记 degree

令 D=Z−CY_i，次数≤2。假设 Lhat(D²)=0；D 在共同 M3 的 index 空间中。因此 PSD 给

 Lhat(D r)=0，任意次数≤3 的多项式 r。                       (1)

这一步合法地使用 degree-two null vector 对 degree-three vector 的正交性；总乘积次数至多五，而非无界乘子。

取 B=g(H−h)²，其次数≤3。Z Boolean 的乘子等式以 B 为乘子（总次数≤5）给

 Lhat[g Z²(H−h)²]=Lhat[g Z(H−h)²]。                          (2)

再以 r=B 用 (1)，得

 Lhat[g Z(H−h)²]=Lhat[g C Y_i(H−h)²]。                      (3)

最后右边是只含 C,Y 的 degree≤5 多项式，所以 Exact 的 base≤5 匹配精确给

 Lhat[g q²]=E_P[g C Y_i(H−h)²]。                             (4)

不需要 base≤6；但本论证确使用了 base 第五次矩，不把它回写成此前 affine lemma 的 base≤4，也不声称它最弱。

## 3. 真实七态期望精算

C=0 的全部四类被 C 因子消去。C=1 的三类中：

* H=0 时 Y_i=0，项为零。
* H=h 时 (H−h)²=0，项为零。
* H=d 时 Y_i=1，g=eta−1，项为 −(1−eta)(d−h)²。

故

 Lhat[gq²]=−p(1−eta)(d−h)²<0。

这是 exact 有理值，不靠渐近、平均某些索引或数值 SDP。最小 d=4,s=2,h=1 也完全成立。无需原 CONFIG first/pair；加入它们不改变这一已经出现的负值。

## 4. 普通原 job 的读法与 scope

在真实候选 law 中新增一枚 unit job K，两个新且不同的私有端点取 Z=CY_i、1−Z，即逐样本完整执行 K；新增两行各负载≤1，不碰原 v。这样提供真实共同 assignment law、任意阶 M_k PSD、Boolean/onehot 与 faithful Gram=0，但上面 q 仍切掉原 v 的 load localizer。它说明‘这样忠实复制 AND’没有保留全局二次检验，绝不说明普通 UM eligibility 已经强制该 AND 关系。

若 Z 不是新增 endpoint/显式 degree-one Boolean 坐标，或只给一阶边际，或改了基础第五次矩/Gram/原 v 负载，以上证明均不能直接套用。其它非仿射依赖及跨背景路线仍须具体核算。

没有读取作者 AND Proof、没有运行软件、没有 repo/Git/Work/外部修改。此记录冻结后应与后续作者读后记录分开保存。
