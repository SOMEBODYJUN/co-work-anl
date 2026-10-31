# 逐机统一内部辅助的 bulk OR-commit 分摊：作者 Proof v1

作者 fee_cascade_review，2026-10-18。对应 statement-only `unit_aux_bulk_or_commit_backbone_split_statement_only_v1.md`，SHA256 `7ebc7224661903bb08e17b907702caf1d12363f33b7e6efafc38e854cbfc9860`。本 Proof 仅给 root hold，在独立 Exact-first reviewer 冻结之前不转发。root 是平均 flow 方向的共同推导者，非 blind reviewer。只 scratch，不改 repo/Work/Git。

## 1. 完整 strict witness 迫未选正 block 最多一枚 J

在任意输入 strict σ^(j) 中，全部 ring 端的 q/b 时长均至少 ρ>1/2，因此每台 M 最多执行一枚 q/b。正 readout C 的 J job 及原 b 都是 unit，所以该处最多执行一枚 J，也不能同时有 b。

固定 a≠j。其 f_a 在正 pool A_(a,0) 耗时1，而该 pool 的每个 q 端为1/k>0，strict 时没有正 q 可以在该 pool。全部 k 枚正 q 都在原 ring。记 R_a^+ 为正 b 实际返回 pin 的集合。正 q 与这些正 b 只可进入本变量正 block 的 k 台 M，唯一例外是正末 q_k 可用右端 M_(k+1)。正 b 的 pin 都在正 block。因此这 k+|R_a^+| 件原任务中至多一件可到 block 外，其余至少 k+|R_a^+|−1 件必须各占正 block 的一台 M。容量迫 |R_a^+|≤1。其它任务进入该 block 只会减少容量，不削弱这个结论。

每个正 C 上的 J job 都迫本来只能 C/原 pin 二选一的同编号 b 返回，且不同 C 对应不同 b。故 c_(a,j)≤|R_a^+|≤1。对 a=j，仅用 k 台 C 的 unit 容量即得 c_(a,a)≤k。以上计入全部 J 包括 aux，并未把其未选侧 C 占用丢掉。

因而 K_a=ceil(Σ_j c_(a,j)/r)≤ceil((k+r−1)/r)=1+ceil((k−1)/r)。

## 2. 同一整数流共同分配全部 J

令 t=|J|。c_h=0 的 I 机器给整数容量 t；c_h>0 给容量 min(t,floor(1/c_h))。每份 strict 输入在该行的 job 数都不超过此容量。全部 C 正 readout 容量为1。每变量正 C 之后再设 block gate，容量 K_a。

网络为 source→每个 J job（容量1），job→其原有限 I/C 端（容量1），I machine→sink（上述容量），C machine→其 block gate（容量1），block gate→sink（容量K_a）。这些 gates 纯分析用，非原执行端。

把 r 份输入中 J 的实际原目的地各取1/r，给出同一网络的值 t 分数满流：每 job 总一，每 I 计数不超过其整数容量，每 C 总不超过一，每 block 正是 Σ_j c_(a,j)/r≤K_a。容量均为整数，确定性整数最大流因此覆盖全部 J。每个 J 按所选原 machine 执行。

各 I 同时真实负载≤1，包括零行；各正 C 至多一枚 J，每变量正 C 上 J 总数 c_a≤K_a。这里没有只核单个 branch 的独立可行性，所有 J 在同一次整数流中共同分配。

## 3. 任意所选正 C 集合的全部 backbone 回填

对一个变量，令 F⊆[k] 为其最终被 J 占据的正 C 索引，c=|F|。令 f 在原正 pool。F 内的 b 返回其原 pin M_i，其余所有 b 留各自 C，包括全部负 b。这样每个正 C 上恰为一枚 J 或自身 b，每个负 C 恰自身 b，全部负载1。

若 F 为空，将本变量全部 q 放左端 M_i；每 M 只有一枚 q，真实时长ρ，两个 pools 除 f 外均空。

若 F 非空，令 p=max F，按以下原有限端放全部 q：

- i∈F\{p} 的正 q_i 放正 pool；
- i<p 且 i∉F 的正 q_i 放左端 M_i；
- p≤i≤k 的正 q_i 放右端 M_(i+1)；
- k+1≤i<2k 的负 q_i 放右端 M_(i+1)；
- 最末负 q_(2k) 放负 pool。

这覆盖每个正/负 q 恰一次。逐台 ring 计数：p 之前的 M_i 由 F 的 b_i 或非 F 的左向 q_i 各一；M_p 由 b_p；M_(p+1) 至 M_(2k) 分别由前一索引的右向 q 占据。负末 q 已去 pool，不会再从环尾撞 M_1。所有 M 恰一枚原 q/b，真实时长ρ或1，故≤1。

正 pool 的原 q 数为 c−1，连 f 负载1+(c−1)/k；负 pool 恰一 q，负载1/k。这同时说明任意 F（不要求连续或 guard 身份相同）都能回填，而不是只对一份预选 prefix 证书成立。

对每变量独立做这个实际回填并不制造共享冲突：不同变量的 rings/pools 物理互异；J 的共享内部网络和所有 C 分配已经在第2节同一 flow 固定，backbone 只填其余原端。

## 4. 全部原 jobs、负载与界

每枚 J 从第2节恰执行一次；每 q/b/f 从第3节恰一次；J 没有 M/pool/负 C 资格，backbone 没有 I 资格，二者不会重复执行同一 job 或碰撞隐藏原机器。gates 不输出。正 C 在两集合中按是否属于 F 精确二选一，不丢其原 b。

每 I≤1，每 C=1，每 M≤1，每负 pool≤1/k，每正 pool≤1+max(0,K_a−1)/k。因此完整全机 C_max≤B_data。

第1节的 K 界给 B_data≤1+ceil((k−1)/r)/k。因 r≥2、k 为偶数，ceil((k−1)/r)≤ceil((k−1)/2)=k/2，统一界≤3/2。

该上界是全 False selector 读出的一份实际原调度，不是原 P 的较大 OPT。前提已给原 P 的 strict 完整 witness，且每 f 所有有限时间均1，故不固定 selector 时原 OPT 恰1。只给各 strict modes 存在的前提时，在有限模式中先任选 witness 再用上述论证，得仅存在结论；没有求未知 strict schedules 的算法。

## 5. 显式复杂度与边界

I/C 的整数容量可截 t；c_h>0 时 floor(1/c_h) 由有理整数除法求得，不按其数值循环。c_h=0 单列，不除零。t=0 可直接跳过 flow，各 K=0，输出全 False backbone。I 为空或 c_h>1 的未用端均无碍。

网络只用显式有限资格，顶点和边按原 P 规模多项式。整数流可用至多 t 次单位增广；每中间容量与 K 的位长多项式。计算 c/K、验证 r 份实际完整 assignments、最终逐原 job 输出原 machine、回算所有有理负载均按总编码长多项式。q/b/f finite 数每变量10k+2，J finite 计 E_J，原计数和 dense 规模保持 statement-only 所列值。

结论只覆盖该完整 backbone、J 的 I/正 C 资格及 I 逐机统一时间。没有将原 P 的 OPT1 当作 near2 source NO；也没有认证 tiny 同机异权、J 到 ring/pool 或其它新资格。无软件枚举、新源 gap、外审或全球新颖性声明。
