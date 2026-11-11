# 第二源最小帽内部SAFE：完整域、28条行与旧域截面

Boss1；RUN `six-boss1-20261111`。**完成：任意非负τ的指定最小帽族有4维11面28顶点；全部128仿射式、3584状态、224张最小值表与14364个系数独立核验PASS。0优化，不读取或绑定数值候选点。**

完整证明见 [proof.md](source2_minimal_cap_safe/proof.md)，端点见 [endpoint_table.md](source2_minimal_cap_safe/endpoint_table.md)，28条准确C-only行见 [exact_family.json](source2_minimal_cap_safe/exact_family.json)，第二份结果见 [literal_checker_output.json](source2_minimal_cap_safe/literal_checker_output.json)。方向、帽公式及C外解析付款由Main提出，本包独立重建完整来源与证书。

## 真实钱包与普遍公式

在实际第二源历史(A1)强制真正最大标签C，|C|=K，保留同一策略的真实R3,...,R6及各自收益。内部SAFE权τ3,τ4,τ5≥0，源IC和中间帽权为

\[
a=25+\tau_3+\tau_4+\tau_5-s,
\]

\[
\beta_3=1/12+\tau_3+\tau_4/72+\tau_5/36,\quad
\beta_4=1/12+\tau_4+\tau_5/36,\quad
\beta_5=1/12+\tau_5.
\]

末帽与末六查询BR均值权均为1。所有查询都是真正合法菜单标签，平均后仅用d≥o弱化，不假设菜单分割或独立性。

令

\[
B=\sum\frac c{p+5},\quad M=\sum\frac o{6(p+4c+1)},\quad
N_j=\sum\frac o{6[p+(j-2)c+7-j]}.
\]

完整域内有

\[
\boxed{a u_2+\frac s5K\ge24B+M+\sum_j\tau_jN_j.}
\]

u2是原实际第二源收益；每个内部SAFE使用同一真实强制分支自己的收益及前缀，直到最小化都不作替换。

## 完整11面参数域

除τj≥0和0≤s≤9，令b4=1/72、b5=1/36，要求

\[
\frac45\tau_j+\sum_{l>j}b_l\tau_l\le43/60,
\]

\[
\boxed{\frac34\tau_j+\sum_{l>j}b_l\tau_l+s/20\le67/60,\qquad j=3,4,5.}
\]

第一组三帽来自p=c=1、o=0、恰缺一个中间尾而末位覆盖的真实状态；第二组来自同一尾态但p=0。s两界来自满尾或缺末位态。不存在漏掉的多缺中间尾附加面。

全部330组四面相交的Fraction消元得到28个顶点：8个s=0、8个s=9、12个中间s。第二份检查器从真预算重得必要面、重枚举顶点，确认11面都余维一。全部3584个隐藏余项非负，公共锚达到准确目标；完整224张表保存所有并列达到态。

帽的坐标最小性也已独立证明：p=0,c=0,o=1的单中间覆盖态强迫每个β至少为上式。采用这些帽后，全部64个c=0余项对任意τ≥0的常数和τ系数均非负；另32个c=1的o1−o0差也逐系数非负。最小性限于本指定预算与零C锚。

## 负自由乘子是合法且必需的

真实尾帽的K总付款是H=1+Σβ，最终行使用有符号等式乘子

\[
\mu=H-s/5,
\qquad R=P+\Delta+\rho+\mu(|C|-K).
\]

τ=0,s=9时，H=5/4而µ=**−11/20**；真实预算权仍全非负，最终K列准确为H−µ=9/5。µ是自由等式系数，不受非负预算权限制。全部14364个有符号列身份已核零。

本包只交付T=C且|C|=K的行；任意T展开必须另保留帽总额与|T|项，不能直接替换最终C行。

## 旧28域是准确截面

旧基底θ*=(12425/31104,175/432,5/12)满足β_j(θ*)=1/2。令τ=θ*+e，便有

\[
\beta_j(\theta^*+e)=1/2+\Gamma_j(e),
\]

源IC、真成本、最小值、C等式付款和最终行都与旧帽联动包相同。两组三帽平移后准确成为旧域的右端3/10+θj*/5和7/10+θj*/4，因此

\[
\boxed{P_{\rm old}\cong P_{\rm new}\cap\{\tau\ge\theta^*\}.}
\]

55个面系数、640个状态仿射系数、3584个旧端点真实成本及14364个旧行系数已独立逐项核对。旧截面顶点不必是新域顶点。最终新行关于τ,s仿射，所以新28顶点行生成这个指定族的全部参数行。

复现：

```bash
python research/workspaces/six-boss1-20261111/source2_minimal_cap_safe/derive_exact.py
python research/workspaces/six-boss1-20261111/source2_minimal_cap_safe/check_literal.py
```

仅用标准库Fraction，不导入/执行其他项目代码。175个既有审计工件及直接来源字节保持不变；旧诊断文件仅作哈希保护，不解析或使用点。最终身份见 [freeze_manifest.json](source2_minimal_cap_safe/freeze_manifest.json)。没有统一输入修改、全局最优值、SPE实现、最佳钱包或half声明。
