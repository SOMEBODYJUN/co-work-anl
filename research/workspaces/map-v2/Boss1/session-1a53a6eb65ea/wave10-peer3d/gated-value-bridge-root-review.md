# Boss1 对归一化门控值桥的定向3D复核

本次只复核当前 canonical 关系 `um-normalized-welfare-to-general-ratio-value-bridge` 及两个当前端点 WELFARE v6、13/8 v6。它位于 Boss2 的十一核心源修复包，但本次不把对这一关系的实读扩成对其余九核心或另外三条关系的重新审查。完整读当前边和两端点登记、该包 source-delta-mathematics、双源审查全文、gated-v2 审查全文及八源溯源全文；四源 FSLP 页实读一至三节的定义、福利与完整值桥，旧 repair_mathematics 仅定位相关标题。未重跑科学程序、LP、舍入或 scheduler。

## 同一完整矩阵的双向保证

组数 n≥1，每组有非空有限 indexed states，每 state 的非负有理资源系数和恰一。资源 bundles 必须全局不交，四类机器 R、X_g、M_gs、Q_u 互异。全部物理作业包括根 pin、connector、selector 和每个列出的 incidence；未列零系数不产生新作业，已列零 incidence 与所有未选 states 的作业均执行。

给定非空 H、全局不交 bundles 以及各组 attaining states，令 b=min(|H|/n,min_g value_g)。b>0 时根 pin 留 R，H 内 connector 去 gate、selector 去其 attaining private，H 外 connector 留 R、selector 去 gate。只导出 H 内所选 state 在其 bundle 上的正 incidence，其余 incidence 一律留自己的 private。于是

- R 负载为 2−|H|/n；每个 gate 恰一枚 unit 作业。
- H 内所选 private 负载为 2−value_g；其它 private 负载至多一。
- 资源端每台至多接一枚 unit incidence，因 bundles 不交。

因此所有原作业均被执行，峰值不超过 2−b。b=0 则用 pin 与全部 connector 在 R、全部 selector 在 gate、全部 incidence 在 private 的峰二基线。这是给出 witness 后的显式回填，不提供求最佳 witness 的 oracle。

反向取任意完整实际调度 C<2。connector 去 gate 的组集 H 满足根负载 2−|H|/n≤C，故 |H|/n≥2−C>0。H 中 selector 不能和 connector 同在 gate，必须进入某个本组 private。该 state 全部 incidence 的原总量一，加上 selector 的一，迫使至少 2−C 的正质量被导出。各资源机在 C<2 时不能接两枚 unit incidence，所以读取的 bundles 全局不交。其它 state 可能导出的作业只占用额外资源，忽略它们不会破坏已读 bundles 的不交性。因此 β*≥2−C。

结合正向、C≥2 的平凡端点和根 pin 的下界，精确得到 OPT(P_gate)=2−β*∈[1,2]。全部步骤不要求 unit-FSLP；不能把同一个符号 β* 换成 flat 全组 max-min，也不能删去未选 jobs。

## 值桥只支付目标的这一部件

v2 目标另求一般福利 LP，满足每组 Σz=1、0≤x≤z、每资源 Σx≤1，并用两阶段精确有理条件期望得到 W≥(1−1/e)L。固定单资源时跨组独立足够；不同资源共享 state 的相关性不影响总目标的期望可加。条件化后概率和可能超过一，此后必须重算真实乘积期望，不能继续套用初始概率和≤1的下界。

从最终质量 r_g 排序，令 b̂=max_k min(k/n,r_(k))，保存实现该最大值的前 k 个组与原 bundles。这个实际见证才允许本边回填 C≤2−b̂。令 h=#{g:r_g>b̂}，若 h>nb̂ 则第 h 项违反 b̂ 的定义，故 h≤nb̂，从而 W≤h+(n−h)b̂≤n(2b̂−b̂²)。另由 β* witness 得 W*≥n(β*)²。这些额外步骤与福利 LP 才导出 C≤1+sqrt(1−5(β*)²/8)。

Root 独立代数核对 D=(18−13β)/8>0，D²−(1−5β²/8)=(209β²−468β+260)/64；在 [0,1] 上导数 418β−468<0，最小余量为 1/64。因此目标自己的完整成熟证明支付 13/8 比例，但源中的 FSLP 福利子定理不能单独提供这一全类算法。现边的 accepted / unconditional / ALL / contribution 判定准确：result 是精确分母和值 witness 的全作业回填，remaining 保一般 LP、两阶段舍入、排序和二次比较，不升级为 whole。

## 零 incidence 勘误与审查边界

双源审查第二部分 CONFIG(1) 构造中，private 的 λ 配置含 selector 和零 jobs，互补 1−λ 配置含全部 incidence。正 job 在 private 获 1−λ、资源 singleton 获 λ；零 job 在两个 private 配置获得 λ+(1−λ)=1，且不占资源容量。资源端只按正 support 计 λ。该勘误修复逐 job 覆盖摘要，不改变本边引用的第一部分值桥，但全文件 SHA 及两个登记 pins 需要正式刷新；当前 canonical 替代已完成此刷新。

本轮不重审十一核心包中 raw/fixed-d、NC、fixed-sink、DGR、palette 等其它数学，不替其 pending 作处置；也不把任意 gated 比例算法误报成绝对峰 13/8、一般 unrelated-machines 近似、可靠 hardness 归约或 CAG 结论。精确引用和当前边/端点 pins 另存同名 refs，供一次联合整合按这一个关系的真实范围采用。
