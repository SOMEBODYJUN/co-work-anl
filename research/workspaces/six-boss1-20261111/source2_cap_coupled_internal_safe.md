# 第二源C分支的帽联动SAFE：非乘积完整域与28条行

Boss1；RUN `six-boss1-20261111`。**完成：4维11面28顶点的完整仿射最小值域；全部3584状态、224张最小值表及14364个系数独立核验PASS。0优化、无点读取或绑定。**

完整来源与证明见 [proof.md](source2_cap_coupled_internal_safe/proof.md)，端点见 [endpoint_table.md](source2_cap_coupled_internal_safe/endpoint_table.md)，准确原行见 [exact_family.json](source2_cap_coupled_internal_safe/exact_family.json)，第二份重建结果见 [literal_checker_output.json](source2_cap_coupled_internal_safe/literal_checker_output.json)。

## 普遍付款

在实际第二源历史(A1)强制真正最大裸大小标签C，|C|=K，保留其同一真实续局R3,...,R6。固定

\[
\theta^*=(12425/31104,175/432,5/12),\qquad
a=25+\sum_j\theta_j^*-s+e_3+e_4+e_5.
\]

新增内部SAFE权ej并增加源IC权Σej，同时把三个中间大小帽权分别改为1/2+Γj，其中

\[
\Gamma_3=e_3+e_4/72+e_5/36,\quad
\Gamma_4=e_4+e_5/36,\quad\Gamma_5=e_5.
\]

末大小帽和末六查询BR均值权保持1。原实际u2、强制后v2及各内部真实收益各自保留到逐客户最小化，查询均值使用真实六合法标签后再d≥o弱化。

记

\[
B=\sum\frac c{p+5},\quad M=\sum\frac o{6(p+4c+1)},\quad
N_j=\sum\frac o{6[p+(j-2)c+7-j]}.
\]

完整参数域内普遍有

\[
\boxed{a u_2+\frac s5K\ge24B+M+\sum_j(\theta_j^*+e_j)N_j.}
\]

真实尾帽支付K的总权是H_K=5/2+ΣΓ，而不是s/5。最终行由非负真预算、菜单弱化、隐藏余项，以及自由等式乘子 `(H_K−s/5)(|C|−K)` 得到；独立K列符号已逐项核对。必须有真正最大C才能消元。

## 完整域不是乘积

除了ej≥0、0≤s≤9，令b4=1/72、b5=1/36，必须同时满足两组三帽：

\[
\frac45e_j+\sum_{l>j}b_l e_l\le\frac3{10}+\frac{\theta_j^*}{5},
\]

\[
\boxed{\frac34e_j+\sum_{l>j}b_l e_l+\frac{s}{20}\le\frac7{10}+\frac{\theta_j^*}{4}.}
\]

第二组是本次独立审查发现的缺失约束，来自p=0,c=1,o=0、恰缺一个中间尾而末尾覆盖的真实状态。第一组来自同一尾态而p=1。s的两界由原公共满尾/缺末位状态给出。

简单失败见证：e=(0,0,23/48)在s=0合法，但在s=9、状态(p,c,o;r3r4r5r6)=(0,1,0;1101)的余项为 **−1/192**。原乘积猜测全部16个顶点共出现12个负状态，均保存在 [rejected_product_candidate.json](source2_cap_coupled_internal_safe/rejected_product_candidate.json)。

加齐三条混合面后，全部330组四面交点的Fraction消元得到28个顶点：8个s=0、8个s=9、12个中间s。全部28×128状态余项非负，公共锚达到目标最小值，没有多缺中间尾带来的遗漏面。第二份程序从真预算状态重新导出必要面并重新枚举顶点，还核11个面都具有余维一。

“完整”指此指定仿射MIN及非负ej的钱包域，不是任意SPE钱包最优性。由于最终行对(e,s)仿射，这28个顶点行是本指定族的完整有限生成器。

## 与旧基底的准确关系

全部513列满足

\[
R(e,s)=(1-s/9)R_0(0)+(s/9)R_0(9)+\sum_j e_j(u_2-N_j).
\]

这解释新增内部SAFE缺口如何转为定量约束；未声称单个u2−Nj本来非负。新行有效性由独立真付款证明，不靠从旧行减去正预算。

已完成检查：128个仿射隐藏式、8个非平凡必要态见证、3584个完整余项、224张全部达到态表、4096个真实六索引菜单模式、14364个准确系数，以及同数的C等式身份列和基底比较身份列。全部原513列与零型/o=0型保留，数值正除数25，末BR原权1。

```bash
python research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/derive_exact.py
python research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/check_literal.py
```

两程序仅用标准库Fraction，只写本包，不导入或执行其他项目程序。153个旧审计工件字节保持不变；旧诊断文件只作哈希保护，不解析点。冻结身份见 [freeze_manifest.json](source2_cap_coupled_internal_safe/freeze_manifest.json)。没有新全局最优值、SPE实现、最佳钱包或half声明。
