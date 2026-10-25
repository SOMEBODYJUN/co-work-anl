# Atom 回撤稿逐式重构：合法固定流上的精确修复，尚无新增 SPE 付款

2026-10-25，Boss3 个人区独立数学审查。只检查 seq310 指定的明确稿及其所引用的 joint certificate 合同；没有泛扫、修改作者材料、外发或提交。一般 Q-CAG-HALF 仍 **OPEN**。

**结论：在“同一固定合法 R 流、全部初始 R 边入 atom、全部终端按实际角色全额追踪”的明示合同下，ATOM-RETRACT、对所有非负角色价格的 CUT 充要条件、SOURCE-PRICE 及精确 DISPERSION-REBATE 均成立。零 atom、mandatory/common、同一 cap 与扩展 INIT 没有发现致命缺口。它确实允许同 owner 的不同 atom 采取不同比例，因此扩大旧固定比例修复类；但没有新增一条从原完整 SPE 激励推出的付款不等式，也没有证明任一原实例必可修复。**

## 1. 审查对象与证据边界

被审完整文本来自本轮工具读取的 `c8_retraction_visit.json`，不是从未合并的本地路径猜测版本：

- actor：`R-c8ca54e5f2854c2c93bf83abc2f24f5c`；save：`customer-attraction`。
- 提交：`b22021bbfb77e3340bf1b497bc0a5269bfefbfbc`。
- 原路径：`research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/common_capacity/atom_retraction_and_dispersion_rebate.md`。
- 工具返回 `text` 的 UTF-8 SHA-256：`d14b56fd312203f9fc298b9a8c76ab7cfc467aa4e3f32740b8359dfc70aca48b`。

相关合同按本地正文 `R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md` §§1–3 重构，未把 ROLE 当作已知。已读根 AGENTS、根四入口、本题 README、模型和精确目标。以下是解析审查及被审稿 §5 的 Fraction 精确算术复核；没有重新运行其 §7 的 52 客户脚本，故不另认证该脚本报告的 1554 条 IC 或完整实现。

## 2. Atom 拆分：必须同时包括直接注入与上游合流

用节点 `v=(t,x)` 简写原 R 图。原流满足

\[
h_v=b_v+\sum_{e\to v}z_e,\qquad
\sum_{e:v\to}z_e+L_v=h_v.
\]

每条正初始边是一条 atom，质量为 `b_a`，只在其指定真实入口注入这一次；不同 source 标签若保留，就分别计入。设 `b_v^a` 是该 atom 在 v 的直接注入。由于**所有**初始 R 边都列出，逐节点有 `b_v=Σ_a b_v^a`。

当 `h_v>0` 时，固定原流比例

\[
\gamma_e=z_e/h_v,\qquad \gamma_v^L=L_v/h_v.
\]

按角色顺序递推

\[
h_v^a=b_v^a+\sum_{e\to v}z_e^a,\qquad
z_e^a=\gamma_e h_v^a,\qquad
L_v^a=\gamma_v^L h_v^a.
\]

`h_v=0` 时所有这些输出为零。这里 `h_v^a` 包含直接注入和全部上游到达，不能只拆过境部分。严格 future DAG 上归纳即得

\[
h_v=\sum_a h_v^a,\quad z_e=\sum_a z_e^a,\quad
L_v=\sum_a L_v^a.
\]

所以这不是只保存两边总和的分解，而是每一节点、每一条边和每个实际角色的精确分解。节点的有序 history 不变；没有把不同历史按主题计数合并。

对 mandatory 边，原 `γ_e=1/c_A(x)`，故 `z_e^a=h_v^a/c_A(x)`；对 common 边，原 `0≤γ_e≤1/c_A(x)`，故 `0≤z_e^a≤h_v^a/c_A(x)`。current 也保持非负守恒。由此每条 atom 子流本身是同一固定图上的合法齐次流。

定义

\[
K_{a l}=\sum_{v:\operatorname{role}(v)=l}L_v^a.
\]

对每条 atom 的守恒式求和，内部边消去；图有限且所有边严格向未来，因此

\[
\sum_lK_{a l}=b_a,\qquad K_{a l}=0\quad(l\le i(a)).
\]

尤其原 R 终端角色行**逐个**满足

\[
\sum_{v:\operatorname{role}(v)=l}L_v=\sum_aK_{a l}.
\]

这是后续价格公式不可省略的合同。若实际实现只追踪一部分，剩余 `f_l` 必须在 cost 中保留为 `A_l+f_l`；只核对 `Σ_l` 的总额无法保证任意非恒定价格下正确。被审稿已明确这一点。

## 3. 独立缩放保留 mandatory/common，回撤占同一角色钱包

对 `b_a>0` 取 `0≤y_a≤b_a`，记 `α_a=1-y_a/b_a`。将 atom 的初始边、每条后代边与 current 同乘 `α_a`；将 `y_a` 加到原初始坐标的 current。对同一节点合并后，mandatory 边仍满足

\[
z'_e=\sum_a\alpha_a z_e^a
=\frac{\sum_a\alpha_a h_v^a}{c_A(x)}
=h'_v/c_A(x),
\]

common 边仍在 `[0,h'_v/c_A(x)]`，并且 `L'_v=Σ_aα_a L_v^a≥0`。即使不同 atom 在中途合流，线性相加仍保留约束，不要求它们采用相同缩放比例。

每条初始边只减小，原加强边容量继续成立。对原初始坐标 `(i,x)`，令

\[
c'_{ix}=c_{ix}+\sum_{a:\ i(a)=i,\ x(a)=x}y_a.
\]

该坐标减少的边质量恰为增加的 current，故 `p_ix=P_ix^B+c'_ix+Σ_j a'_ijx` 逐坐标成立；`c'` 没有凭空增加来源库存。R 客户与 I 客户不交，因此 I 初始源、I-PAY 的右端及 H、J 不变化。

各节点 `h'_v=Σ_aα_a h_v^a≤h_v`，旧固定 context 的客户密度上界自动保留。这一步没有把不同 context 的密度相加，也不需要重新调用原 SPE 或改变其分母、完成叶和平局。

原 `A_l=d_l+H_l+J_l≤2u_l` 确实不需要 ROLE：INIT 给 `d_l≤u_l`，I-PAY 给 `H_lx+J_lx≤w_lx`，故 `H_l+J_l≤u_l`。用同一组原数据定义

\[
F_l=A_l+\sum_aK_{a l},\qquad
t_{a l}=K_{a l}/b_a,
\]

则变化精确为

\[
F'_l=F_l+\sum_{a:i(a)=l}y_a-\sum_at_{a l}y_a.
\tag{R}
\]

owner 所收回的是其角色共同钱包的新增 current；终端所减少的是原来已经计入同一钱包的质量，不能再给每个 atom 一份 `2u_l`。由 `Σ_lt_al=1`，`Σ_lF'_l=Σ_lF_l=|O|`。

**扩展 INIT 的定位准确。** 新 `d'_i=d_i+Σ_{a:i(a)=i}y_a` 可能超过 `u_i`，故修复后一般不再是原 joint LP 的 INIT 点。被审稿没有隐藏这一退出。对最终的充分结论，只要所有质量非负、来源守恒且同一角色行 `F'_l≤2u_l`，就已经有 `|O|≤2W`；不必另外声称 `d'≤u` 或为新增 current 再造一条 IC。反过来，若后文要把输出当作旧 INIT 的可行点继续使用，便必须恢复 `d'≤u`；本稿没有作这种结论。

## 4. 全非负价格 CUT 的必要性和充分性均成立

记 `s_l=2u_l-F_l`，`q_a=Σ_lt_al λ_l`。对固定非负价格 `λ`，(R) 的增量价格为

\[
\sum_a(\lambda_{i(a)}-q_a)y_a.
\]

各 atom 的盒变量独立，故其最小值为

\[
-\sum_ab_a(q_a-\lambda_{i(a)})_+.
\]

存在一个同时满足所有角色 cap 的 y，必有

\[
\sum_l\lambda_ls_l+
\sum_ab_a(q_a-\lambda_{i(a)})_+\ge0
\quad\text{对所有 }\lambda\in\mathbb R_+^m.
\tag{C}
\]

充分性不能只说逐价格可择不同 y 然后交换量词；此处由凸分离补上了这一步。盒 `[0,b]` 的 cost 像 `P={F'(y)}` 是非空紧凸集，目标集合 `D={z:z≤2u}` 是闭凸向下集合。若两者不交，紧集与闭集的有限维强分离给

\[
\min_{p\in P}\lambda\cdot p>
\sup_{z\in D}\lambda\cdot z
\]

的非零法向量；D 在各负坐标方向无界，右端有限要求 `λ≥0`，此时右端等于 `λ·2u`，与 (C) 矛盾。所以全非负价格条件等价于**存在同一个**成功 y。

该证明包括零坐标、零 slack 和紧贴 cap 的退化情况。`λ=0` 只是平凡等式；非零价格可按 `Σλ=1` 归一化，但原非负锥表述已完整。有限有理输入下，成功 y 或严格失败价格均可取有理数。没有理由沿用旧 owner-greedy 算法；稿件也未这样声称。

代入 `F=A+ΣK`，或直接逐 atom 最小化，可得等价式

\[
\min_{0\le y\le b}\lambda\cdot F'(y)
=\lambda\cdot A+
\sum_ab_a\min(\lambda_{i(a)},q_a).
\]

因此 SOURCE-PRICE 的右端确实为 `Σ_lλ_l(2u_l-A_l)`，没有漏掉某份已追踪终端质量。这个精确充要条件的可行域是**冻结该份 K、该份流后的独立 atom 缩放类**；不能把某次失败价格解释为任意改 INIT、改路由均不可能，亦不能把某个价格被消除解释为已检验全部 cut。

## 5. 分散返还等式与严格包含例

固定 owner i，`b_i=Σ_{a:i(a)=i}b_a>0`，`b_i bar q_i=Σ_a b_a q_a`。置

\[
D_i=\sum_{a:i(a)=i}b_a(\lambda_i-q_a)_+,
\quad E_i=\sum_{a:i(a)=i}b_a(q_a-\lambda_i)_+.
\]

一方面 `b_i(bar q_i-λ_i)=E_i-D_i`；另一方面，逐项写 `min(λ_i,q_a)=q_a-(q_a-λ_i)_+`，得到

\[
b_i\min(\lambda_i,\bar q_i)
-\sum_{a:i(a)=i}b_a\min(\lambda_i,q_a)
=E_i-(E_i-D_i)_+
=\min(D_i,E_i).
\]

所以这里有真实的固定修复类扩容，不只是把旧 owner-price 改名。旧类限制同 owner 的 `y_a/b_a` 相同，当然是新盒的子集；同一价格下源需求减少量恰为上式。只有价格在 owner 价两侧均有正质量时返还严格为正；一侧分散没有返还。相同终端分布的 atom 合并对每个价格都没有损失，也确实不损失可行域：它们的总代回撤仍能取 `[0,Σb_a]` 的任意值。

稿件 §5 的指定抽象数据用 Fraction 从头计算通过：

| 量 | 精确值 |
| --- | --- |
| 原 F | `(3/2,5/2,3/2)` |
| 只回撤终结角色2的 atom 后 F' | `(2,2,3/2)` |
| 旧比例修复的必要区间 | 同时要求 `y≤1/2`、`y≥1`，空集 |
| `λ=(1/2,1,0)` 的旧需求、共同 RHS | `1/2`、`1/4` |
| 同一 λ 的 atom 需求 | `1/4` |
| `D_1=E_1`、精确返还 | `1/4`、`1/4` |

因此两种抽象线性修复类严格不同的结论成立。稿件已准确说明该数据未实现为原 SPE/INIT，不是博弈反例；不能从此例宣称真实 SPE 已出现严格收益。

零 atom 的正确处理是 `b_a=y_a=K_al=t_al=0`，由 DAG 递推它也没有正后代流，不做除零。`b_i=0` 的 owner 行全为零。最后角色不存在正 outgoing atom；m=1、空客户与全零输入都与这些约定相容。

## 6. 新增了什么，仍欠什么

本稿得到的通用关系是：对每一份已固定、真实 context 合法的初始流，能以独立 atom 选择扩大已有源质量的退回方式，并精确刻画何时共同 cap 可满足。分散返还是该固定优化问题的需求减少量，**不是从 SPE 行新提取的一笔收入**；没有额外的 `u_i`、没有重复的客户券，也没有额外 whole-query IC。

取 `λ=(1,…,1)` 时，每个正 atom 的 `q_a=1`，所有 `D_i=E_i=0`，SOURCE-PRICE 正好是

\[
\sum_ab_a\le\sum_l(2u_l-A_l)
\iff |O|\le2W.
\]

故 atom 细化本身不改变总质量，也不能付出总资金缺口。这不是证明该方法无用：在已有足够总容量时，它可能减少旧比例回撤造成的角色错配；但一般原 SPE 为什么满足全部价格约束，仍没有证明。重选最优 T、INIT 或合法路由是否能补足价格约束，也仍是另外的开放命题。

代入 m=5 完全同样：得到一个正确的条件修复判据，未无条件推出 `OPT_5≤2W`。当前没有新全人数或五人福利界；此结论不反驳 Q-CAG-HALF，也不反驳将来使用真实 off-history IC 支付这些价格约束。

本次无需数学勘误。建议将其保留为边界已写清的固定流修复工具，下一步若继续投入，应明确提出一条由完整 SPE 导出、对任意目录/人数成立的 source-price 上界或新的可付款来源；不把继续分割标签、验证更多固定样例或消除单条失败价格计为该义务已经完成。
