---
id: "unrelated-machines/real-optimal-moment-full-hs-versus-state-original-audit"
kind: "computation"
type_tag: "计算"
title: "真实最优矩上全空间HS与单状态贪心原程序"
status: "complete-primary-source-read-and-original-cli-retained"
summary: "210个真实最优调度、17维压缩算子、全HS精确二倍与单状态平衡输出；限指定顺序和真实矩。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py"]
source_ids: ["cd7597c69d8924fb8c0f"]
truth_status: "exact finite results with separate mathematical reconstruction"
review_status: "informed internal reread, not new blind or external review"
---

# 原任务与真正的最优分布

7379B `hs_effect_greedy_exact_m3.py` 全文已读，无外部模型输入、无导入其它数学源码；本轮原CLI一次退出0。三台相同机器，任务0耗时1，任务1,…,8耗时1/4，所有机器均合法。总工作量3给 OPT≥1。大任务独占一机，八个小任务在另两机各四个能达1，所以 OPT=1。所有峰1调度恰3·C(8,4)=210个；代码逐一生成、去重并回算每份负载(1,1,1)，给每份权1/210。不是伪矩、独立行边际或事后选出的坏分布。

V1为这210点上常数及27个原任务指示函数的span，内积为均匀期望。程序从常数和每任务机器0/1的19个候选特征作有理Gram–Schmidt，机器2由任务守恒生成，删零方向后维数17。基向量 φ_a 缩放成primitive integer，不要求欧氏正交归一；平方范数为

`210,420,140,140,420,1680,5040,1200,3600,800,2400,480,1440,240,720,80,240`。

给端e=(i,j)，压缩乘法算子 A_e=Π1_[σ(j)=i]Π 在此基中为
\[
A_e[a,b]=\frac{\sum_{s:s(j)=i}\phi_a(s)\phi_b(s)}{h_a},\qquad
G=\operatorname{diag}(h_a)/210.
\]
程序核 G自伴、每任务Σ_iA_(i,j)=I、每机Σ_jp_jA_(i,j)=I，都是整个17维空间的精确恒等式。矩来自真实最优分布，不能把它当成缺少行容量的松弛伪例。

# 两条不同的选择规则

全空间规则初 K=I，任务按0,1,…,8，逐端计算
\[
\|A_eK\|_{HS,G}^2=\sum_{a,b}(h_a/h_b)(A_eK)[a,b]^2,
\]
取最大、平局最小机器编号，再左乘K←A_eK。所有分数、平局和正差值用 Fraction 决定。

| 任务 | 最大机器 | 所选score−最大其它score |
|---:|---|---:|
| 0 | 0,1,2 | 0 |
| 1 | 1,2 | 0 |
| 2 | 1 | 205/6804 |
| 3 | 1 | 355/61236 |
| 4 | 1 | 1260349/756142128 |
| 5 | 1 | 7320679/6805279152 |
| 6 | 1 | 668387317/979960197888 |
| 7 | 1 | 10109132665/35278567123968 |
| 8 | 1 | 12131586226051/108904936711689216 |

首步scores全37/9，次步为(10/81,361/324,361/324)。输出 `(0,1,1,1,1,1,1,1,1)`，真实负载(1,2,0)，比率恰2。最终HS平方 `3369699728819633/18296029367563788288>0`。所以压缩算子连乘非零不等于这组选择在真实支撑中有非空共同事件：这个坏分配并不属于原210个最优调度。

另一条 rank-one-state 规则初state为常数基坐标(1,0,…)，每步取使 ‖A_e state‖_G² 最大的端再更新state；它不保存完整矩阵K。实际输出 `(0,1,2,2,1,1,1,2,2)`，负载(1,1,1)，最终G范数平方 `28360619690999/1016446075975766016`。这个例上成功只是范围对照，不是该规则的一般保证。两规则全部18步的三个候选分数、maximizer集合、chosen和gap完整保存在[新stdout](../../tools/evidence/um-following-audit-contracts-primary/runs/hs-effects.stdout)，未只留两份最终分配。

# 大缺陷不反驳给定近平坦证书的定理

全空间缺陷 δ=Σ_e tr(A_e−A_e²) 实际精确等于66。相关17973B canonical 和9154B review本批全读，其 NF 条件是给定显式四阶共同 C2-load 矩、R=rank M1、n≥1、剪枝端数d时
\[
\delta\le\min\{1/(64ndR),\eta/16\},\quad 0<\eta\le1.
\]
在该条件下同一个全HS规则有负载≤(1+3δ)T≤(1+η)T的解析保证；本例n9,d27,R17,δ66，根本不在NF域内。常数state上的缺陷恒0不替代全空间迹；本例已经显示只看这个state会丢关键信息。给定证书提取、矩证书生成、无NF的大缺陷规则须分开。

本程序直接利用完整真实分布构造A_e，不实现近平坦validator、一般SDP、任意四阶伪矩提取或寻找分布。canonical的原T强近平坦生成困难性依赖另一个半单位3DM归约，本有限程序没有执行或证明该归约。空任务、零目标、未剪枝细界等一般API也不是这个固定3机脚本本次新测的范围。

原review保留statement-first定位全HS反例、随后整合者知情读后的历史顺序；本轮没有新blind。review还记canonical数学正文曾只规范化三行尾空格，当前 c49e… 与旧5ec0…的载体SHA不同；该变化不涉及本程序9adc…源码。旧HS JSON没有代码hash字段，绑定靠review/包来源，而不是伪称旧JSON内原有hash。本包完整保留已读review和本次记录。

# 复用边界与证据

本轮该原CLI一次，完整旧HS JSON与新输出**全字段相等**。[记录](../../tools/evidence/um-following-audit-contracts-primary/runs/hs-effects.execution.json)、[源/依赖/比较清单](../../tools/evidence/um-following-audit-contracts-primary/README.md)、[历史比较](../../tools/evidence/um-following-audit-contracts-primary/historical-comparison-and-version-scope.json)。[既有HS有限审查](../审查/循环路径与HS贪心有限审计--审查.md)及[四阶/全阶双源审查](../审查/全阶矩提取与近平坦HS贪心双源审查--审查.md)已承载一般背景，不重复其数学done。

反例约束的是指定big-first顺序、K初I和全空间HS左乘规则。原任务机器对称可解析处理首两处平局，但本次代码只跑最小label一次；没有枚举所有tie策略或任务顺序，更没有否定所有moment方法或一般次二算法。
