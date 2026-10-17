# 私有树配置间隙随重数的一阶锐渐近：作者冻结证明

绑定 `UM-PRIVATE-TREE-MULTIPLICITY-GAP-ASYMPTOTIC-v1`，Exact 文件 SHA256 `fb1283d4bd3346be0dedae6e19acbef50876d68643fafdccbe537d7051156adf`。

来源：literal 在 bounded-multiplicity v3 的一般上界完成后独立构造下述一层平星族，向 root 报告两侧夹逼与 limit；root 因看过摘要不称本项盲审。新 Exact-only 已另交 root，本文在独立审查者冻结重构前不向其交付。

## 1. 下界族的精确配置阈值

取 Exact 的 d=μ、h=1、单 root、μ states，state s 的 μ 个叶 jobs 全映到其私有 z_s。记 state 根为 v_s。所有内部机器仅 v_s；每叶 job 在 v_s 用时 1/μ，在 z_s 用时1；selector 在全部 v_s 用时1。

selector 保证 T_conf≥1。给 T=1 的具体配置点：

- 每根 v_s：selector singleton 权重 1/μ；全部 μ 个本 state small 叶 jobs 的配置权重 1−1/μ。后一配置总负载 μ·(1/μ)=1。
- 每外机 z_s：给其 μ 枚叶 jobs 各自 singleton 配置权重 1/μ，权重和为1。

每根权重和1；每 selector 覆盖 μ·(1/μ)=1；每叶 job 覆盖为 `(1−1/μ)+(1/μ)=1`。所有配置负载均≤1，故 T_conf=1。其共同 λ_s=1/μ，外容量按 μ 次 multiplicity 计，恰为1；此处没有把 μ 片同色叶偷合并成一枚 job。

## 2. 下界族的精确实际最优值

任何实际调度都把 selector 放在某个 v_s。若其 makespan C≥2，则当然 C≥2−1/μ。若 C<2，每个外机 z_s 只能接至多一枚 unit 叶 job；于是 selector 所在 v_s 的 μ 枚叶 jobs 中至少 μ−1 枚必须在 v_s 以 small 端执行。该根负载至少

\[
 1+\frac{\mu-1}{\mu}=2-\frac1\mu.
\]

反向取任一 s，selector 放 v_s，该 state 任取一枚叶外送 z_s，其余 μ−1 枚父置；全部其它 states 的原叶 jobs 全父置。选中根负载2−1/μ，其余根负载1，唯一使用外机负载1。全部原 jobs 恰安排一次，故

\[
 \operatorname{OPT}=2-\frac1\mu,
 \qquad \operatorname{OPT}/T_{\mathrm{conf}}=2-\frac1\mu.
\]

状态内实际重数恰为 μ，该族属于 C_μ。它有 μ 个根机、μ 个外机、μ² 枚叶 jobs 和一枚 selector，所有端、处理时间与∞可显式列出。这是一个参数化显式实例族，不声称仅按 log μ 生成全部 μ² jobs。

## 3. 上确界夹逼与整数参数极限

v3 的一般全 CONFIG(T) 结论对每 P∈C_μ 给出

\[
 \frac{\operatorname{OPT}(P)}{T_{\mathrm{conf}}(P)}
 \le 2-\frac1{\mu+2}.
\]

所以对所有输入取上确界，结合第2节显式族，

\[
 2-\frac1\mu\le G(\mu)\le2-\frac1{\mu+2}.
\]

这些界本身已保证 G 有限，无需主张上确界达到。两边的差为

\[
 \frac1\mu-\frac1{\mu+2}=\frac2{\mu(\mu+2)},
\]

即 Exact 所述精确误差界。等价地，

\[
 \frac\mu{\mu+2}\le\mu[2-G(\mu)]\le1.
\]

沿整数 μ→∞ 两端同趋1，得到 limit=1。因此正确的锐性表述为参数 μ 的一阶渐近，而非每个固定 μ 的 exact G 或 α_μ 锐利。

## 4. 准确身份

本项下界是能显式求解的一层平星实例的配置整数间隙，不能作为 NP-hardness、TFNP 搜索困难性或一般 UM 反面。它仅说明 bounded-multiplicity 上界中距2的 Θ(1/μ) 阶、乃至第一阶系数1不可改善；未消除 O(μ^−2) 范围。

一般上界依赖 v3 的 rainbow blocker/Haxell/全阈值证明；其真假和审查状态应共同登记。下界族和极限不引入额外外部定理。没有新软件实现、有限运行证书、全球新颖性或一般 σ 多项式算法认证。
