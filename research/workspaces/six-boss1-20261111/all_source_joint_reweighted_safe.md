# 任意前四真实源的联合内部 SAFE 重配：完整域与 536 条普遍行

Boss1；RUN `six-boss1-20261111`。**完成：67 个完整域顶点、8064 个全域非负余项、536×513 全部系数及第二份字面核验均 PASS；优化器调用 0。** 旧包未修改，没有绑定点或求解新统一系统。

完整证明见 [proof.md](all_source_joint_reweighted_safe/proof.md)，所有端点见 [endpoint_tables.md](all_source_joint_reweighted_safe/endpoint_tables.md)，可交接的原尺度行见 [exact_family.json](all_source_joint_reweighted_safe/exact_family.json)。这项任意源重配方向、候选锚和根源四上帽由 Main 提出；本包独立重建真实来源、确定完整域并逐列核验，不冒称全部方向由本席独立发现。

## 普遍公式

在[原共同目录完整有序历史纯 SPE 模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)中，取任意实际源 i=1,2,3,4，任意合法强制标签 T、任意六个合法查询及其覆盖并 O。令 p 为原实际前缀客户负载，n=6−i，c_i=(n+1)/2，t、o 为 T、O 的会员位，Θ=Σ_(j=i+1)^5 θ_j，a=25+Θ−s。定义

\[
\begin{aligned}
B_i&=\sum\frac{t}{p+n+1},& H_i&=\sum\frac{t}{\min(p+n+1,5)},\\
M_i&=\sum\frac{o}{6(p+1+nt)},& N_{ij}&=\sum\frac{o}{6[p+(j-i)t+7-j]}.
\end{aligned}
\]

全部下述域内参数均给出

\[
\boxed{a u_i+c_i(K-|T|)-24B_i+sH_i-M_i-\sum_j\theta_jN_{ij}\ge0.}
\]

它直接由原源真实 IC 权 a、同一强制 T 分支的中间尾大小帽各权1/2、末帽权1、同一末节点六查询 BR 均值权1以及真内部 SAFE 权 θ_j 支付。每个内部 SAFE 使用自己的真实分支收益和前缀，直到逐客户最小化都不替换成原实际收益或预设尾覆盖 T。菜单平均保留真实会员重数 d，最后仅用 d≥o；不要求六查询互不重叠，O 不作合法行动。

## 完整参数域

各源共同 θ 约束是

\[
\theta_j\ge0,\qquad
\theta_j+\sum_{\ell=j+1}^{5}\frac{\theta_\ell}{6(7-\ell)(8-\ell)}\le\frac5{12}.
\]

源 i=2,3,4 配 **0≤s≤9**；源 i=1 配

\[
\boxed{s\ge0,\qquad s\le15+5\theta_j\quad(j=2,3,4,5).}
\]

这就是指定仿射最小值在全部局部客户/尾态上的完整非负权域。必要帽分别来自 t=0 的单中间覆盖态、D=6 的全尾态、D=5 的末位不覆盖态，以及根源恰缺一个中间尾/末位不覆盖态；全部充分性由完整有限顶点和每个隐藏态的准确非负余项给出。没有把它宣称为任意 SPE 钱包的完整或最优域。

| 来源 | 顶点数 | 局部状态 | 顶点×状态 | 原行数 |
|---:|---:|---:|---:|---:|
| 1 | 39 | 128 | 4992 | 312 |
| 2 | 16 | 128 | 2048 | 128 |
| 3 | 8 | 96 | 768 | 64 |
| 4 | 4 | 64 | 256 | 32 |
| 合计 | 67 | 416 | 8064 | 536 |

第一源最大 s=1070/63、最小 a=605/63 都唯一在四个 θ=25/63 取得。证明只用 q=min θ、首 θ 帽的系数和21/20及四个 s 上帽；不调用优化。其余三源 a≥16。

所有客户型有公共达到态：t=0 时全尾0；t=1,D≤5 时全尾1；t=1,D=6 时全中间尾1而末位0。444 张最小值表保存所有并列达到态，不把公共锚误写成真实尾必须唯一如此。

## 536 行与接口

每个顶点采用八个纯合法 T=A1,...,A6,X,C，查询菜单始终同一个 O。列为全部512个 `(a1,...,a6,x,o,c)` 类型加独立 K，所有零型、o=0型均保留。原收益列为真正实际 u_i；与强制后 v_i、v_j 不混用。

全部行保持末均值 BR 权1的原尺度，正数值除数25，K列始终 c_i。一般 T 保留 `c_i(K−|T|)`，H_i 也用正确分母；尤其源3、4不能把 H_i 任意变成 K/5。T=C 的质量等式不在原行生成时提前消元。

对源2、T=C 的16个端点，旧已冻行与新行的准确关系为

\[
R_{\rm new}=R_{\rm old}+(s/5-5/2)(|C|-K).
\]

这16条的全部8208列残差均为零，见 [source2_C_endpoint_comparison.json](all_source_joint_reweighted_safe/source2_C_endpoint_comparison.json)。536条完整系数向量本次互异；仍完整保留原行，不声称独立或无其它线性冗余。

## 独立核验与复现

主生成器从封闭公式构造 536 行；第二份 [check_literal.py](all_source_joint_reweighted_safe/check_literal.py) 不导入任何生成器或旧审计程序，逐项构造真实份额、大小帽、六项查询均值，在所有隐藏尾态上重新取 min，再重构每条原收益列与独立 K 列。**274,968 个准确系数全部 PASS**。它还独立重枚举67顶点、确认31个面均余维一、核全部8064余项/444张全部达到态表。第一份程序另外穷举13312个真正六查询会员模式，核线性平均弱化的准确差。

在仓库根目录依次运行：

```bash
python research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/derive_domain.py
python research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/build_family.py
python research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/check_literal.py
```

结果见 [literal_checker_output.json](all_source_joint_reweighted_safe/literal_checker_output.json)；来源与既有105个审计工件字节保护见 [source_manifest.json](all_source_joint_reweighted_safe/source_manifest.json)。最终交付身份见 [freeze_manifest.json](all_source_joint_reweighted_safe/freeze_manifest.json)。所有脚本仅用标准库 Fraction，无网络、优化器、Git/RUN/registry 操作。

本包完成普遍有效族及其精确系数交接。它没有固定支持限制，没有新全局最优值、完整 SPE 实现或 half 定理声明；下一统一输入和求解由 Main 另行授权。
